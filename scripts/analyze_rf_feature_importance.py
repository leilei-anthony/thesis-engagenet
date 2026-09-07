"""
Trains a Random Forest exactly as src/train_traditional.py does (same pooling,
scaling, and hyperparameters) for a given config, then reports which pooled
input features drove its splits most, and renders one example tree from the
forest (depth-limited for readability -- the forest itself has 100 trees).

train_traditional.py does not persist the sklearn model to disk, so this
script retrains rather than loading a checkpoint.
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.tree import plot_tree

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dataset import EngagementDataset  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = REPO_ROOT / "artifacts" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_SECONDARY,
    "text.color": INK_PRIMARY,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def parse_args():
    p = argparse.ArgumentParser(description="Random Forest feature importance + example tree")
    p.add_argument("--sampling_method", type=str, default="targeted")
    p.add_argument("--mode", type=str, default="classification", choices=["classification", "regression"])
    p.add_argument("--binarize_threshold", type=int, default=3, choices=[1, 2, 3])
    p.add_argument("--no_class_weights", action="store_true", default=True)
    p.add_argument("--restrict_to_common", action="store_true",
                   help="Restrict to videos covered by every sampling method")
    p.add_argument("--top_n", type=int, default=25)
    p.add_argument("--tree_max_depth", type=int, default=3,
                   help="Display depth only -- the underlying tree is trained unrestricted, same as train_traditional.py")
    return p.parse_args()


def extract_pooled_features(dataset):
    X = []
    for seq, length in zip(dataset.sequences, dataset.lengths):
        l = length.item()
        pooled = seq[:l, :].mean(dim=0)
        X.append(pooled.numpy())
    return np.array(X), dataset.labels.numpy()


def main():
    args = parse_args()
    suffix = f"_{args.sampling_method}_{args.mode}"
    if args.binarize_threshold is not None:
        suffix += f"_thresh{args.binarize_threshold}"

    print(f"Training RF ({args.sampling_method} / {args.mode} / thresh={args.binarize_threshold}) "
          f"to inspect feature importance...")

    train_dataset = EngagementDataset(args.sampling_method, "train",
                                      binarize_threshold=args.binarize_threshold,
                                      restrict_to_common=args.restrict_to_common)
    # Sampling method is validated by EngagementDataset (which rejects the former
    # 'bocpd' alias), so the CSV name maps directly.
    header_csv = Path(train_dataset.data_dir) / f"{args.sampling_method.lower()}-train.csv"
    feature_names = list(pd.read_csv(header_csv, nrows=0).columns[5:-1])

    X_train, y_train = extract_pooled_features(train_dataset)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    if args.mode == "classification":
        class_weight = None if args.no_class_weights else "balanced"
        model = RandomForestClassifier(n_estimators=100, class_weight=class_weight, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        class_names = [f"Class {c}" for c in sorted(np.unique(y_train))]
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        class_names = None

    importances = model.feature_importances_
    order = np.argsort(importances)[::-1][:args.top_n]
    top_features = [feature_names[i] for i in order]
    top_importances = importances[order]

    # --- Figure 1: top-N feature importances ---
    fig, ax = plt.subplots(figsize=(8, max(4, args.top_n * 0.28)))
    y_pos = np.arange(len(top_features))[::-1]
    ax.barh(y_pos, top_importances, color=BLUE, edgecolor=SURFACE, linewidth=1.0, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top_features, fontsize=8)
    ax.set_xlabel("Gini importance")
    ax.set_title(
        f"Random Forest Feature Importance — Top {args.top_n}\n"
        f"({args.sampling_method}, {args.mode}"
        + (f", threshold {args.binarize_threshold}" if args.binarize_threshold else "") + ")",
        fontsize=11, loc="left", color=INK_PRIMARY,
    )
    ax.grid(axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(length=0)
    fig.tight_layout()
    imp_path = FIGURES_DIR / f"fig5_rf_feature_importance{suffix}.png"
    fig.savefig(imp_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {imp_path}")

    # --- Figure 2: one example tree from the forest, truncated for display ---
    fig, ax = plt.subplots(figsize=(22, 10))
    plot_tree(
        model.estimators_[0],
        max_depth=args.tree_max_depth,
        feature_names=feature_names,
        class_names=class_names,
        filled=True,
        rounded=True,
        fontsize=7,
        ax=ax,
        impurity=False,
    )
    ax.set_title(
        f"Random Forest — Tree #0 of {model.n_estimators} "
        f"(display truncated to depth {args.tree_max_depth}; full tree is deeper)\n"
        f"({args.sampling_method}, {args.mode}"
        + (f", threshold {args.binarize_threshold}" if args.binarize_threshold else "") + ")",
        fontsize=12, color=INK_PRIMARY,
    )
    fig.patch.set_facecolor(SURFACE)
    tree_path = FIGURES_DIR / f"fig6_rf_example_tree{suffix}.png"
    fig.savefig(tree_path, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {tree_path}")

    print("\nTop 15 features by importance:")
    for name, imp in zip(top_features[:15], top_importances[:15]):
        print(f"  {name:30s} {imp:.4f}")


if __name__ == "__main__":
    main()
