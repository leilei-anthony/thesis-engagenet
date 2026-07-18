import os
from pathlib import Path
import argparse
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau

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

def parse_args():
    parser = argparse.ArgumentParser(description="Train Engagement LSTM Model")
    parser.add_argument('--sampling_method', type=str, required=True,
                        help="Temporal sampling method to use (e.g. targeted, bocpd, 5-changepoint)")
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
    parser.add_argument('--device', type=str, default=None, help="Device to use (cpu, mps, cuda)")
    parser.add_argument('--model', type=str, default='lstm', choices=['lstm', 'mlp'],
                        help="Model architecture to use")
    return parser.parse_args()

def main():
    args = parse_args()
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
    train_dataset = EngagementDataset(args.sampling_method, 'train', binarize_threshold=args.binarize_threshold)
    val_dataset = EngagementDataset(args.sampling_method, 'validation', binarize_threshold=args.binarize_threshold)
    
    train_loader = get_dataloader(args.sampling_method, 'train', batch_size=args.batch_size, shuffle=True, binarize_threshold=args.binarize_threshold)
    val_loader = get_dataloader(args.sampling_method, 'validation', batch_size=args.batch_size, shuffle=False, binarize_threshold=args.binarize_threshold)
    
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
            mode=args.mode
        ).to(device)
    
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
    scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3, verbose=True)
    
    # 4. Training Loop
    best_val_loss = float('inf')
    epochs_no_improve = 0
    
    checkpoint_name = f"best_model_{args.model}_{args.sampling_method}_{args.mode}"
    if args.binarize_threshold is not None:
        checkpoint_name += f"_binary_thresh{args.binarize_threshold}"
    if args.no_class_weights:
        checkpoint_name += "_unweighted"
    checkpoint_name += ".pt"
    
    checkpoint_path = str(OUTPUT_DIR / checkpoint_name)
    
    print("Starting training...")
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
                'args': args
            }, checkpoint_path)
            print(f"--> Saved best model checkpoint to {checkpoint_path}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= args.patience:
                print(f"Early stopping triggered! Training stopped after {epoch} epochs.")
                break
                
    print(f"Training completed. Best validation loss: {best_val_loss:.4f}")

if __name__ == '__main__':
    main()
