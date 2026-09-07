"""
Generates baseline-vs-SMOTE comparison figures from the tables in EXPERIMENTS.md
("Baseline Model Comparison" and "SMOTE Ablation Comparison" sections).
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
BASELINE_EDGE = "#c3c2b7"

VARIANT_COLORS = {"Baseline": "#2a78d6", "SMOTE": "#eb6834"}  # slot 1 blue, slot 2 orange
MODEL_ORDER = ["LSTM", "MLP", "SVM", "Random Forest"]
TASK_ORDER = ["Multi-class", "Binary Thresh 1", "Binary Thresh 2", "Binary Thresh 3"]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "axes.edgecolor": BASELINE_EDGE,
    "axes.labelcolor": INK_SECONDARY,
    "text.color": INK_PRIMARY,
    "xtick.color": INK_MUTED,
    "ytick.color": INK_MUTED,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

TABLE_RE = re.compile(
    r"#### \d?\.?\s*([^\n(]+?)(?:\s*\(([^)]+)\))?\n"
    r"\| Sampling Method \| Model \|.*\n\| :--- \|.*\n"
    r"((?:\|.*\n)+)"
)


def task_label(table_name, detail):
    if table_name.startswith("Multi-class"):
        return "Multi-class"
    if table_name.startswith("Binary"):
        thresh = re.search(r"\d+", detail).group() if detail else "?"
        return f"Binary Thresh {thresh}"
    return None


def parse_section(md_text, variant):
    rows = []
    for m in TABLE_RE.finditer(md_text):
        table_name, detail = m.group(1).strip(), m.group(2)
        task = task_label(table_name, detail)
        if task is None:
            continue  # skip Regression tables: SMOTE doesn't apply
        for line in m.group(3).strip().splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            model = re.sub(r"\s*\(Run \d+\)", "", cells[1]).strip()
            row = {
                "variant": variant,
                "task": task,
                "sampling_method": cells[0].replace("*", "").strip(),
                "model": model,
                "accuracy": float(cells[2]),
                "macro_f1": float(cells[3]),
            }
            training_time = cells[-1].strip()
            try:
                row["training_time"] = float(training_time)
            except ValueError:
                row["training_time"] = np.nan
            rows.append(row)
    return rows


def load_data():
    text = EXPERIMENTS_MD.read_text()
    baseline_text = text.split("## Baseline Model Comparison", 1)[1].split("## SMOTE Ablation Comparison", 1)[0]
    smote_text = text.split("## SMOTE Ablation Comparison", 1)[1].split("## Random Forest Feature Importance Analysis", 1)[0]
    rows = parse_section(baseline_text, "Baseline") + parse_section(smote_text, "SMOTE")
    df = pd.DataFrame(rows)
    # BOCPD was never part of either automated sweep (baseline table keeps it as a legacy
    # reference row); drop it here so both variants cover the same 4 sampling methods.
    df = df[df.sampling_method != "BOCPD"]
    assert len(df) == 2 * 4 * 4 * 4, f"unexpected row count: {len(df)}"  # 2 variants x 4 tasks x 4 methods x 4 models
    return df


def style_axis(ax, ylabel, title):
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, color=INK_PRIMARY, pad=10, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE_EDGE)
    ax.tick_params(axis="both", length=0, labelsize=9)


def grouped_bar(ax, df, task, value_col, ylabel, title, log_scale=False):
    sub = df[df.task == task]
    x = np.arange(len(MODEL_ORDER))
    width = 0.32
    for i, variant in enumerate(["Baseline", "SMOTE"]):
        vals = [sub[(sub.model == model) & (sub.variant == variant)][value_col].mean() for model in MODEL_ORDER]
        offset = (i - 0.5) * width
        ax.bar(
            x + offset, vals, width * 0.9,
            label=variant, color=VARIANT_COLORS[variant],
            edgecolor=SURFACE, linewidth=1.2, zorder=3,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(MODEL_ORDER)
    if log_scale:
        ax.set_yscale("log")
    style_axis(ax, ylabel, title)


def fig_accuracy_comparison(df):
    fig, axes = plt.subplots(2, 4, figsize=(16, 7.5))
    for col, task in enumerate(TASK_ORDER):
        grouped_bar(axes[0, col], df, task, "accuracy", "Accuracy" if col == 0 else "", task)
        grouped_bar(axes[1, col], df, task, "macro_f1", "Macro F1" if col == 0 else "", "")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Accuracy / Macro F1: Baseline vs. SMOTE, by task and model\n(averaged across all 4 sampling methods)",
                 fontsize=13, y=1.03)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig7_smote_accuracy_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_training_time_comparison(df):
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
    for col, task in enumerate(TASK_ORDER):
        grouped_bar(axes[col], df, task, "training_time",
                    "Training Time (s)" if col == 0 else "", task)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, -0.08))
    fig.suptitle("Training Time: Baseline vs. SMOTE, by task and model\n(averaged across all 4 sampling methods)",
                 fontsize=13, y=1.08)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "fig8_smote_training_time_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    df = load_data()
    print(f"Parsed {len(df)} rows: variants={df.variant.unique().tolist()}, tasks={df.task.unique().tolist()}")
    fig_accuracy_comparison(df)
    fig_training_time_comparison(df)
    print(f"Saved figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
