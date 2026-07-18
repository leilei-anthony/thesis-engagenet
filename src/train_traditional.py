import os
import argparse
from pathlib import Path
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, accuracy_score

from dataset import EngagementDataset

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / 'artifacts' / 'checkpoints'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Train and Evaluate Traditional ML Baselines (SVM, RF)")
    parser.add_argument('--sampling_method', type=str, required=True,
                        help="Temporal sampling method to use (e.g. targeted, bocpd, 5-changepoint)")
    parser.add_argument('--mode', type=str, default='classification', choices=['classification', 'regression'],
                        help="Task mode: classification or regression")
    parser.add_argument('--binarize_threshold', type=int, default=None, choices=[1, 2, 3],
                        help="Threshold for binarizing labels. If None, uses original 4 classes.")
    parser.add_argument('--model', type=str, required=True, choices=['svm', 'rf'],
                        help="Traditional ML baseline model: svm, rf")
    parser.add_argument('--no_class_weights', action='store_true', help="Disable class weighting / sample weighting")
    return parser.parse_args()

def extract_pooled_features(dataset):
    """
    Averages sequences over their actual lengths to construct a single feature vector per sample.
    """
    X = []
    for seq, length in zip(dataset.sequences, dataset.lengths):
        l = length.item()
        # Temporal average pooling
        pooled = seq[:l, :].mean(dim=0)
        X.append(pooled.numpy())
    return np.array(X), dataset.labels.numpy()

def get_regression_sample_weights(y, weight_class_0=2.0):
    """
    Computes sample weights for regression that penalize class 0 (< 0.5) errors more heavily.
    """
    weights = np.ones_like(y, dtype=np.float32)
    weights[y < 0.5] = weight_class_0
    return weights

def main():
    args = parse_args()
    
    # Determine the number of classes
    if args.binarize_threshold is not None:
        num_classes = 2
        bin_str = f"BINARY THRESHOLD {args.binarize_threshold}"
    else:
        num_classes = 4
        bin_str = "MULTI-CLASS"
        
    print(f"--- Training {args.model.upper()} ({args.sampling_method.upper()} - {args.mode.upper()} - {bin_str}) ---")
    
    # 1. Load splits
    train_dataset = EngagementDataset(args.sampling_method, 'train', binarize_threshold=args.binarize_threshold)
    val_dataset = EngagementDataset(args.sampling_method, 'validation', binarize_threshold=args.binarize_threshold)
    test_dataset = EngagementDataset(args.sampling_method, 'test', binarize_threshold=args.binarize_threshold)
    
    X_train, y_train = extract_pooled_features(train_dataset)
    X_val, y_val = extract_pooled_features(val_dataset)
    X_test, y_test = extract_pooled_features(test_dataset)
    
    # 2. Preprocess: standard scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    # 3. Model Initialization and Fitting
    if args.model == 'svm':
        if args.mode == 'classification':
            class_weight = 'balanced' if not args.no_class_weights else None
            model = SVC(kernel='rbf', class_weight=class_weight, random_state=42)
            model.fit(X_train_scaled, y_train)
        else:
            model = SVR(kernel='rbf')
            if not args.no_class_weights:
                sample_weight = get_regression_sample_weights(y_train)
                model.fit(X_train_scaled, y_train, sample_weight=sample_weight)
            else:
                model.fit(X_train_scaled, y_train)
    elif args.model == 'rf':
        if args.mode == 'classification':
            class_weight = 'balanced' if not args.no_class_weights else None
            model = RandomForestClassifier(n_estimators=100, class_weight=class_weight, random_state=42, n_jobs=-1)
            model.fit(X_train_scaled, y_train)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
            if not args.no_class_weights:
                sample_weight = get_regression_sample_weights(y_train)
                model.fit(X_train_scaled, y_train, sample_weight=sample_weight)
            else:
                model.fit(X_train_scaled, y_train)
                
    # 4. Inference
    preds = model.predict(X_test_scaled)
    
    # 5. Metrics Computation
    overall_mse = np.mean((preds - y_test) ** 2)
    
    class_mses = {}
    for c in range(num_classes):
        indices = np.where(y_test == c)[0]
        if len(indices) > 0:
            class_mses[c] = np.mean((preds[indices] - c) ** 2)
        else:
            class_mses[c] = 0.0
            
    # Pearson Correlation Coefficient (PCC)
    if np.std(preds) == 0 or np.std(y_test) == 0:
        pcc, p_val = 0.0, 1.0
    else:
        pcc, p_val = pearsonr(preds, y_test)
        
    # Discrete predictions for Confusion Matrix
    if args.mode == 'regression':
        discrete_preds = np.clip(np.round(preds), 0, num_classes - 1).astype(int)
    else:
        discrete_preds = preds.astype(int)
        
    cm = confusion_matrix(y_test, discrete_preds, labels=list(range(num_classes)))
    
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, discrete_preds, labels=list(range(num_classes)), zero_division=0
    )
    accuracy = accuracy_score(y_test, discrete_preds)
    macro_f1 = np.mean(f1)
    weighted_f1 = np.sum(f1 * support) / np.sum(support)
    
    # 6. Output Metrics
    print("\n" + "="*40)
    print(f"Evaluation Results ({args.model.upper()} - {args.sampling_method.upper()} - {args.mode.upper()} - {bin_str})")
    print("="*40)
    print(f"Overall MSE: {overall_mse:.4f}")
    print(f"Pearson Correlation (PCC): {pcc:.4f} (p-value: {p_val:.4g})")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClass-wise Metrics:")
    for c in range(num_classes):
        print(f"  Class {c}: Precision={precision[c]:.4f}, Recall={recall[c]:.4f}, F1-score={f1[c]:.4f} (Support={support[c]})")
    
    print(f"\nMacro F1-score: {macro_f1:.4f}")
    print(f"Weighted F1-score: {weighted_f1:.4f}")
    
    print("\nClass-wise MSE:")
    for c in range(num_classes):
        print(f"  Class {c}: {class_mses[c]:.4f}  (N={np.sum(y_test == c)})")
        
    print("\nConfusion Matrix:")
    print(cm)
    print("="*40)
    
    # 7. Save Confusion Matrix Plot
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
    plt.title(f'Confusion Matrix ({args.model.upper()} - {args.sampling_method.upper()} - {args.mode.upper()})')
    
    plot_path = str(OUTPUT_DIR / plot_name)
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved confusion matrix heatmap to {plot_path}\n")

if __name__ == '__main__':
    main()
