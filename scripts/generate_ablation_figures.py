"""
Generates comparison figures for the sampling-method / changepoint-count ablation
from the tables in EXPERIMENTS.md ("Baseline Model Comparison" section).
"""
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS_MD = REPO_ROOT / "EXPERIMENTS.md"
FIGURES_DIR = REPO_ROOT / "artifacts" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# --- Palette (validated categorical order, see .claude memory / dataviz skill) ---
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"

# BOCPD is deliberately excluded: it was never implemented, and the former
# 'bocpd' option silently loaded 3-changepoint data (see src/dataset.py).
METHOD_ORDER = ["Targeted", "3-Changepoint", "5-Changepoint", "7-Changepoint"]
METHOD_COLORS = {
    "Targeted": "#2a78d6",       # slot 1 blue
    "3-Changepoint": "#1baf7a",  # slot 3 aqua
    "5-Changepoint": "#eda100",  # slot 4 yellow
    "7-Changepoint": "#e87ba4",  # slot 5 magenta
}
MODEL_ORDER = ["LSTM", "MLP", "SVM", "Random Forest"]

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


def parse_tables(md_text):
    """Parse the 5 markdown comparison tables into one long DataFrame."""
    table_re = re.compile(
        r"#### \d?\.?\s*([^\n(]+?)(?:\s*\(([^)]+)\))?\n"
        r"\| Sampling Method \| Model \|.*\n\| :--- \|.*\n"
        r"((?:\|.*\n)+)"
    )
    rows = []
    for m in table_re.finditer(md_text):
        table_name = m.group(1).strip()
        detail = m.group(2)
        threshold = None
        if detail and "Threshold" in detail:
            threshold = int(re.search(r"\d+", detail).group())
        def parse_time(cell):
            try:
                return float(cell)
            except ValueError:
                return np.nan  # e.g. "N/A (legacy run)" for un-timed legacy BOCPD LSTM/MLP rows

        for line in m.group(3).strip().splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            row = {"table": table_name, "threshold": threshold}
            sampling_method = cells[0].replace("*", "").strip()
            model = re.sub(r"\s*\(Run \d+\)", "", cells[1]).strip()
            row["sampling_method"] = sampling_method
            row["model"] = model
            if table_name.startswith("Multi-class"):
                row["accuracy"] = float(cells[2])
                row["macro_f1"] = float(cells[3])
                row["weighted_f1"] = float(cells[4])
                row["pcc"] = float(cells[5].split()[0]) if cells[5].split()[0] != "nan" else np.nan
                row["mse"] = float(cells[6])
                row["training_time"] = parse_time(cells[7])
            elif table_name.startswith("Regression"):
                row["mse"] = float(cells[2])
                row["pcc"] = float(cells[3].split()[0]) if cells[3].split()[0] != "nan" else np.nan
                row["accuracy"] = float(cells[4])
                row["training_time"] = parse_time(cells[5])
            elif table_name.startswith("Binary"):
                row["accuracy"] = float(cells[2])
                row["macro_f1"] = float(cells[3])
                row["weighted_f1"] = float(cells[4])
                row["class0_f1"] = float(cells[5])
                row["class1_f1"] = float(cells[6])
                row["pcc"] = float(cells[7].split()[0]) if cells[7].split()[0] != "nan" else np.nan
                row["mse"] = float(cells[8])
                row["training_time"] = parse_time(cells[9])
            rows.append(row)
    return pd.DataFrame(rows)


def style_axis(ax, ylabel, title):
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, color=INK_PRIMARY, pad=10, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.tick_params(axis="both", length=0, labelsize=9)


def grouped_bar(ax, df, value_col, ylabel, title, higher_is_better=True, agg="mean"):
    n_methods = len(METHOD_ORDER)
    width = 0.8 / n_methods
    x = np.arange(len(MODEL_ORDER))
    for i, method in enumerate(METHOD_ORDER):
        sub = [
            df[(df.model == model) & (df.sampling_method == method)][value_col]
            for model in MODEL_ORDER
        ]
        vals = [(s.sum(min_count=1) if agg == "sum" else s.mean()) for s in sub]
        offset = (i - (n_methods - 1) / 2) * width
        ax.bar(
            x + offset, vals, width * 0.9,
            label=method, color=METHOD_COLORS[method],
            edgecolor=SURFACE, linewidth=1.2, zorder=3,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(MODEL_ORDER)
    style_axis(ax, ylabel, title)
    note = "higher is better" if higher_is_better else "lower is better"
    ax.text(1.0, 1.03, note, transform=ax.transAxes, ha="right", fontsize=8, color=INK_MUTED)


def fig_multiclass(df):
    sub = df[df.table.str.startswith("Multi-class")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    grouped_bar(axes[0], sub, "accuracy", "Accuracy", "Multi-class Accuracy")
    grouped_bar(axes[1], sub, "macro_f1", "Macro F1", "Multi-class Macro F1")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle("Multi-class Classification: Sampling Method × Model", fontsize=13, y=1.03)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig1_multiclass_classification.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_regression(df):
    sub = df[df.table.str.startswith("Regression")]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    grouped_bar(axes[0], sub, "pcc", "Pearson Correlation (PCC)", "Regression PCC")
    grouped_bar(axes[1], sub, "mse", "Overall MSE", "Regression MSE", higher_is_better=False)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle("Regression: Sampling Method × Model", fontsize=13, y=1.03)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig2_regression.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_binary_threshold3(df):
    sub = df[(df.table.str.startswith("Binary")) & (df.threshold == 3)]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    grouped_bar(axes[0], sub, "accuracy", "Accuracy", "Threshold 3 Accuracy (0-2 vs 3)")
    grouped_bar(axes[1], sub, "macro_f1", "Macro F1", "Threshold 3 Macro F1 (0-2 vs 3)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, -0.05))
    fig.suptitle("Binary Classification (Threshold 3): Sampling Method × Model", fontsize=13, y=1.03)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig3_binary_threshold3.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_training_time(df):
    fig, ax = plt.subplots(1, 1, figsize=(7, 4.2))
    grouped_bar(
        ax, df, "training_time",
        "Total Training Time (s, log scale, summed across all 5 tasks)",
        "Training Time: Sampling Method × Model",
        higher_is_better=False, agg="sum",
    )
    ax.set_yscale("log")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=5, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig4_training_time.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    md_text = EXPERIMENTS_MD.read_text()
    # Only parse the refreshed "Baseline Model Comparison" section (after this marker)
    md_text = md_text.split("## Baseline Model Comparison", 1)[1]
    df = parse_tables(md_text)
    assert len(df) == 5 * 5 * 4, f"unexpected row count: {len(df)}"  # 5 tables x 5 methods x 4 models
    print(f"Parsed {len(df)} rows across tables: {df.table.unique().tolist()}")

    fig_multiclass(df)
    fig_regression(df)
    fig_binary_threshold3(df)
    fig_training_time(df)
    print(f"Saved figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
