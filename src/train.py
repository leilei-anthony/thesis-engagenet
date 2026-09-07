import os
import time
import random
from pathlib import Path
import argparse
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from imblearn.over_sampling import SMOTE

from dataset import EngagementDataset, get_dataloader
from model import EngagementLSTM, EngagementMLP

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / 'artifacts' / 'checkpoints'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class WeightedMSELoss(nn.Module):
    """
    Weighted MSE Loss for regression that penalizes errors on class 0 (Disengaged) samples.
    Since targets in regression are continuous (representing engagement score),
    we penalize targets that are close to 0 (i.e. < 0.5) more heavily.
    """
    def __init__(self, weight_class_0=2.0):
        super(WeightedMSELoss, self).__init__()
        self.weight_class_0 = weight_class_0
        
    def forward(self, pred, target):
        squared_errors = (pred - target) ** 2
        # Apply weighting factor if ground truth is less than 0.5 (representing Level 0)
        weights = torch.where(target < 0.5, self.weight_class_0, 1.0)
        return torch.mean(squared_errors * weights)

def apply_smote_to_dataset(dataset, num_classes):
    """
    Oversamples a sequence EngagementDataset with SMOTE so every class matches the
    majority class count. Classification only (SMOTE needs discrete labels).

    Sequences are flattened to (max_seq_len * feature_dim) vectors for SMOTE, with
    the per-sample valid length appended as an extra column so it gets interpolated
    consistently with the features, then reshaped back afterward.
    """
    sequences = dataset.sequences.numpy()
    labels = dataset.labels.numpy()
    lengths = dataset.lengths.numpy()
    n, max_seq_len, feat_dim = sequences.shape

    class_counts = np.bincount(labels.astype(int), minlength=num_classes)
    min_class_count = class_counts[class_counts > 0].min()
    if min_class_count < 2:
        print(f"Skipping SMOTE: smallest class has only {min_class_count} sample(s), need >= 2.")
        return dataset
    k_neighbors = min(5, min_class_count - 1)
    print(f"Applying SMOTE (k_neighbors={k_neighbors}). Class counts before: {class_counts}")

    flat = sequences.reshape(n, max_seq_len * feat_dim)
    x_aug = np.concatenate([flat, lengths.reshape(-1, 1).astype(np.float32)], axis=1)

    smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
    x_res, y_res = smote.fit_resample(x_aug, labels)
    print(f"Class counts after SMOTE: {np.bincount(y_res.astype(int))}")

    seq_res = x_res[:, :-1].reshape(-1, max_seq_len, feat_dim).astype(np.float32)
    len_res = np.clip(np.round(x_res[:, -1]), 1, max_seq_len).astype(np.int64)

    dataset.sequences = torch.tensor(seq_res, dtype=torch.float32)
    dataset.labels = torch.tensor(y_res, dtype=torch.long)
    dataset.lengths = torch.tensor(len_res, dtype=torch.long)
    return dataset

def set_seed(seed):
    """
    Seeds every source of randomness that affects a training run: Python's RNG,
    NumPy, and torch (CPU + CUDA). Without this, LSTM/MLP weight initialisation
    and batch ordering vary run to run, which is fatal for an ablation whose
    effects are on the order of a single accuracy point.

    Returns a torch.Generator seeded identically, to be handed to the DataLoader
    so that shuffle order is reproducible too.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    generator = torch.Generator()
    generator.manual_seed(seed)
    return generator


def parse_args():
    parser = argparse.ArgumentParser(description="Train Engagement LSTM Model")
    parser.add_argument('--sampling_method', type=str, required=True,
                        help="Temporal sampling method: targeted, 3-changepoint, 5-changepoint, 7-changepoint")
    parser.add_argument('--mode', type=str, default='classification', choices=['classification', 'regression'],
                        help="Task mode: classification (4 classes) or regression (continuous)")
    parser.add_argument('--binarize_threshold', type=int, default=None, choices=[1, 2, 3],
                        help="Threshold for binarizing labels. If None, uses original 4 classes.")
    parser.add_argument('--epochs', type=int, default=50, help="Number of training epochs")
    parser.add_argument('--batch_size', type=int, default=64, help="Batch size for training")
    parser.add_argument('--lr', type=float, default=1e-3, help="Learning rate")
    parser.add_argument('--hidden_dim', type=int, default=64, help="LSTM hidden state dimension")
    parser.add_argument('--patience', type=int, default=10, help="Patience for early stopping")
    parser.add_argument('--weight_decay', type=float, default=1e-4, help="Weight decay for AdamW")
    parser.add_argument('--no_class_weights', action='store_true', help="Disable class weighting in loss functions")
    parser.add_argument('--use_smote', action='store_true',
                        help="Apply SMOTE oversampling to the training split (classification mode only)")
    parser.add_argument('--device', type=str, default=None, help="Device to use (cpu, mps, cuda)")
    parser.add_argument('--model', type=str, default='lstm', choices=['lstm', 'mlp'],
                        help="Model architecture to use")
    parser.add_argument('--seed', type=int, default=42,
                        help="Random seed for weight init, dropout and batch shuffling")
    parser.add_argument('--restrict_to_common', action='store_true',
                        help="Restrict to videos covered by every sampling method, so sampling "
                             "conditions are compared on identical clips")
    parser.add_argument('--readout', type=str, default='mean', choices=['mean', 'last', 'attention'],
                        help="LSTM temporal readout: mean-pool over timesteps (default, legacy), "
                             "last valid hidden state, or learned attention. Ignored for --model mlp.")
    return parser.parse_args()

def main():
    args = parse_args()
    loader_generator = set_seed(args.seed)
    print(f"Random seed: {args.seed}")
    if args.device is not None:
        device = torch.device(args.device)
    else:
        device = torch.device('cuda' if torch.cuda.is_available() 
                              else ('mps' if torch.backends.mps.is_available() else 'cpu'))
    print(f"Using device: {device}")
    
    # Determine the number of target classes
    if args.binarize_threshold is not None:
        print(f"Binarization active with threshold = {args.binarize_threshold}")
        num_classes = 2
    else:
        num_classes = 4

    # 1. Load Data
    print(f"Creating loaders for {args.sampling_method} sampling in {args.mode} mode...")
    train_dataset = EngagementDataset(args.sampling_method, 'train',
                                      binarize_threshold=args.binarize_threshold,
                                      restrict_to_common=args.restrict_to_common)
    val_dataset = EngagementDataset(args.sampling_method, 'validation',
                                    binarize_threshold=args.binarize_threshold,
                                    restrict_to_common=args.restrict_to_common)

    if args.use_smote:
        if args.mode == 'classification':
            train_dataset = apply_smote_to_dataset(train_dataset, num_classes)
        else:
            print("--use_smote was set but mode is 'regression'; SMOTE requires discrete labels, skipping.")

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True,
                              drop_last=False, generator=loader_generator)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, drop_last=False)
    
    # 2. Setup Class Weights
    train_labels = train_dataset.labels.numpy()
    class_counts = np.bincount(train_labels, minlength=num_classes)
    class_counts = np.maximum(class_counts, 1)  # avoid division by zero
    total_samples = len(train_labels)
    
    # Inverse frequency weights
    inv_weights = total_samples / (float(num_classes) * class_counts)
    # Apply extra scaling factor of 2.0 to Class 0 (Disengaged) specifically
    inv_weights[0] *= 2.0
    
    print(f"Class counts in training data: {class_counts}")
    if args.no_class_weights:
        print("Class weights are disabled (--no_class_weights is set).")
        class_weights_tensor = None
    else:
        print(f"Computed loss weights: {inv_weights}")
        class_weights_tensor = torch.tensor(inv_weights, dtype=torch.float32).to(device)
    
    # 3. Initialize Model and Loss Function
    if args.model == 'mlp':
        model = EngagementMLP(
            input_dim=1518, 
            hidden_dim=args.hidden_dim, 
            num_classes=num_classes, 
            mode=args.mode
        ).to(device)
    else:
        model = EngagementLSTM(
            input_dim=1518,
            hidden_dim=args.hidden_dim,
            num_layers=1,
            num_classes=num_classes,
            mode=args.mode,
            readout=args.readout
        ).to(device)
        print(f"LSTM temporal readout: {args.readout}")
    
    if args.mode == 'classification':
        if args.no_class_weights:
            criterion = nn.CrossEntropyLoss()
        else:
            criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)
    else:
        if args.no_class_weights:
            criterion = nn.MSELoss()
        else:
            criterion = WeightedMSELoss(weight_class_0=2.0)
        
    optimizer = AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # 4. Training Loop
    best_val_loss = float('inf')
    epochs_no_improve = 0
    
    checkpoint_name = f"best_model_{args.model}_{args.sampling_method}_{args.mode}"
    if args.binarize_threshold is not None:
        checkpoint_name += f"_binary_thresh{args.binarize_threshold}"
    if args.no_class_weights:
        checkpoint_name += "_unweighted"
    if args.use_smote and args.mode == 'classification':
        checkpoint_name += "_smote"
    # Disambiguate non-default readouts and non-default seeds so that multi-seed
    # and readout-ablation runs do not overwrite one another's checkpoints.
    if args.model == 'lstm' and args.readout != 'mean':
        checkpoint_name += f"_readout-{args.readout}"
    if args.seed != 42:
        checkpoint_name += f"_seed{args.seed}"
    checkpoint_name += ".pt"
    
    checkpoint_path = str(OUTPUT_DIR / checkpoint_name)
    
    print("Starting training...")
    training_start_time = time.time()
    for epoch in range(1, args.epochs + 1):
        # Train epoch
        model.train()
        train_loss = 0.0
        for features, labels, lengths in train_loader:
            features = features.to(device)
            lengths = lengths.to(device)
            
            if args.mode == 'classification':
                labels = labels.to(device, dtype=torch.long)
            else:
                labels = labels.to(device, dtype=torch.float32)
                
            optimizer.zero_grad()
            outputs = model(features, lengths)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * features.size(0)
            
        train_loss /= len(train_loader.dataset)
        
        # Validation epoch
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for features, labels, lengths in val_loader:
                features = features.to(device)
                lengths = lengths.to(device)
                
                if args.mode == 'classification':
                    labels = labels.to(device, dtype=torch.long)
                else:
                    labels = labels.to(device, dtype=torch.float32)
                    
                outputs = model(features, lengths)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * features.size(0)
                
        val_loss /= len(val_loader.dataset)
        
        # Scheduler update
        scheduler.step(val_loss)
        
        print(f"Epoch {epoch}/{args.epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")
        
        # Early Stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
                'args': args,
                'training_time_seconds': time.time() - training_start_time
            }, checkpoint_path)
            print(f"--> Saved best model checkpoint to {checkpoint_path}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= args.patience:
                print(f"Early stopping triggered! Training stopped after {epoch} epochs.")
                break

    total_training_time = time.time() - training_start_time
    print(f"Training completed. Best validation loss: {best_val_loss:.4f}")
    print(f"Total training time: {total_training_time:.2f} seconds ({total_training_time / 60:.2f} minutes)")

    # Record the full run's wall-clock time (not just time-to-best-epoch) on the saved checkpoint.
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
        checkpoint['training_time_seconds'] = total_training_time
        torch.save(checkpoint, checkpoint_path)

if __name__ == '__main__':
    main()
