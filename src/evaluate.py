import os
from pathlib import Path
import argparse
import numpy as np
import torch
import torch.nn as nn
from scipy.stats import pearsonr
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from dataset import get_dataloader
from model import EngagementLSTM, EngagementMLP
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / 'artifacts' / 'checkpoints'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Engagement LSTM Model")
    parser.add_argument('--sampling_method', type=str, required=True,
                        help="Temporal sampling method to use (e.g. targeted, bocpd, 5-changepoint)")
    parser.add_argument('--mode', type=str, default='classification', choices=['classification', 'regression'],
                        help="Task mode: classification (4 classes) or regression (continuous)")
    parser.add_argument('--binarize_threshold', type=int, default=None, choices=[1, 2, 3],
                        help="Threshold for binarizing labels. If None, uses original 4 classes.")
    parser.add_argument('--batch_size', type=int, default=64, help="Batch size for evaluation")
    parser.add_argument('--hidden_dim', type=int, default=64, help="LSTM hidden state dimension")
    parser.add_argument('--no_class_weights', action='store_true', help="Disable class weighting in loss functions")
    parser.add_argument('--device', type=str, default=None, help="Device to use (cpu, mps, cuda)")
    parser.add_argument('--model', type=str, default='lstm', choices=['lstm', 'mlp'],
                        help="Model architecture to evaluate")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.device is not None:
        device = torch.device(args.device)
    else:
        device = torch.device('cuda' if torch.cuda.is_available() 
                              else ('mps' if torch.backends.mps.is_available() else 'cpu'))
    print(f"Using device: {device}")
    
    # Determine the number of classes
    if args.binarize_threshold is not None:
        num_classes = 2
        print(f"Binarization active with threshold = {args.binarize_threshold}")
    else:
        num_classes = 4
        
    # 1. Load Test Data
    print(f"Loading test loader for {args.sampling_method}...")
    test_loader = get_dataloader(
        args.sampling_method, 'test', 
        batch_size=args.batch_size, 
        shuffle=False, 
        binarize_threshold=args.binarize_threshold
    )
    
    # 2. Load Checkpoint
    checkpoint_name = f"best_model_{args.model}_{args.sampling_method}_{args.mode}"
    if args.binarize_threshold is not None:
        checkpoint_name += f"_binary_thresh{args.binarize_threshold}"
    if args.no_class_weights:
        checkpoint_name += "_unweighted"
    checkpoint_name += ".pt"
    checkpoint_path = str(OUTPUT_DIR / checkpoint_name)
    
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}. Run training first.")
        
    print(f"Loading checkpoint from {checkpoint_path}...")
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
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
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    # 3. Inference
    all_preds = []
    all_targets = []
    
    with torch.no_grad():
        for features, labels, lengths in test_loader:
            features = features.to(device)
            lengths = lengths.to(device)
            outputs = model(features, lengths)
            
            if args.mode == 'classification':
                preds = torch.argmax(outputs, dim=1).cpu().numpy()
            else:
                preds = outputs.cpu().numpy()
                
            all_preds.extend(preds)
            all_targets.extend(labels.numpy())
            
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    
    # 4. Metrics Computation
    # Overall MSE
    overall_mse = np.mean((all_preds - all_targets) ** 2)
    
    # Class-wise MSE
    class_mses = {}
    for c in range(num_classes):
        indices = np.where(all_targets == c)[0]
        if len(indices) > 0:
            class_mses[c] = np.mean((all_preds[indices] - c) ** 2)
        else:
            class_mses[c] = 0.0
            
    # Pearson Correlation Coefficient (PCC)
    if np.std(all_preds) == 0 or np.std(all_targets) == 0:
        pcc, p_val = 0.0, 1.0
    else:
        pcc, p_val = pearsonr(all_preds, all_targets)
        
    # Discrete predictions for Confusion Matrix
    if args.mode == 'regression':
        discrete_preds = np.clip(np.round(all_preds), 0, num_classes - 1).astype(int)
    else:
        discrete_preds = all_preds.astype(int)
        
    cm = confusion_matrix(all_targets, discrete_preds, labels=list(range(num_classes)))
    
    # Classification specific metrics (F1, Precision, Recall)
    if args.mode == 'classification' or args.mode == 'regression':
        precision, recall, f1, support = precision_recall_fscore_support(
            all_targets, discrete_preds, labels=list(range(num_classes)), zero_division=0
        )
        accuracy = accuracy_score(all_targets, discrete_preds)
        
    # 5. Output Metrics
    print("\n" + "="*40)
    bin_str = f"BINARY THRESHOLD {args.binarize_threshold}" if args.binarize_threshold is not None else "MULTI-CLASS"
    print(f"Evaluation Results ({args.sampling_method.upper()} - {args.mode.upper()} - {bin_str})")
    print("="*40)
    print(f"Overall MSE: {overall_mse:.4f}")
    print(f"Pearson Correlation (PCC): {pcc:.4f} (p-value: {p_val:.4g})")
    
    if args.mode == 'classification' or args.mode == 'regression':
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClass-wise Metrics:")
        for c in range(num_classes):
            print(f"  Class {c}: Precision={precision[c]:.4f}, Recall={recall[c]:.4f}, F1-score={f1[c]:.4f} (Support={support[c]})")
        
        macro_f1 = np.mean(f1)
        weighted_f1 = np.sum(f1 * support) / np.sum(support)
        print(f"\nMacro F1-score: {macro_f1:.4f}")
        print(f"Weighted F1-score: {weighted_f1:.4f}")
        
    print("\nClass-wise MSE:")
    for c in range(num_classes):
        print(f"  Class {c}: {class_mses[c]:.4f}  (N={np.sum(all_targets == c)})")
        
    print("\nConfusion Matrix:")
    print(cm)
    print("="*40)
    
    # 6. Save Confusion Matrix Plot
    plt.figure(figsize=(8, 6))
    if num_classes == 2:
        labels_list = ['Disengaged (0)', 'Engaged (1)']
        suffix = f"_binary_thresh{args.binarize_threshold}"
    else:
        labels_list = ['Level 0', 'Level 1', 'Level 2', 'Level 3']
        suffix = ""
        
    if args.no_class_weights:
        plot_name = f"confusion_matrix_{args.model}_{args.sampling_method}_{args.mode}{suffix}_unweighted.png"
    else:
        plot_name = f"confusion_matrix_{args.model}_{args.sampling_method}_{args.mode}{suffix}.png"
        
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues', 
        xticklabels=labels_list,
        yticklabels=labels_list
    )
    plt.ylabel('True Engagement Level')
    plt.xlabel('Predicted Engagement Level')
    plt.title(f'Confusion Matrix ({args.sampling_method.upper()} - {args.mode.upper()})')
    
    plot_path = str(OUTPUT_DIR / plot_name)
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved confusion matrix heatmap to {plot_path}\n")

if __name__ == '__main__':
    main()
