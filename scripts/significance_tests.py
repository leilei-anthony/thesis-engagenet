"""
Paired significance testing for the Threshold 3 ablation.

Why this exists: the metrics printed by evaluate.py include a Pearson p-value,
but that tests whether predictions correlate with ground truth -- it says
nothing about whether two experimental conditions differ from each other. The
thesis's central claim is comparative ("sampling strategy does not matter,
architecture does"), so it needs a test appropriate to that claim.

McNemar's test is the right choice here: the conditions are evaluated on the
identical set of clips (guaranteed by --restrict_to_common), so predictions are
paired per clip, and the test conditions only on the discordant pairs -- the
clips where exactly one of the two models was correct.

Reports, per comparison: the discordant counts (b, c), the exact-binomial
p-value, the accuracy difference, and a bootstrap confidence interval on that
difference. Holm-Bonferroni correction is applied within each comparison family.

Usage:
    python scripts/significance_tests.py \
        --preds_dir artifacts/predictions_threshold3_common
"""
import argparse
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]

SAMPLING_ORDER = ["targeted", "3-changepoint", "5-changepoint", "7-changepoint"]
MODEL_ORDER = ["lstm", "mlp", "svm", "rf"]


def parse_args():
    p = argparse.ArgumentParser(description="Paired significance tests (McNemar)")
    p.add_argument("--preds_dir", type=str,
                   default="artifacts/predictions_threshold3_common",
                   help="Directory of per-sample prediction CSVs")
    p.add_argument("--condition", type=str, default="baseline",
                   choices=["baseline", "smote"],
                   help="Which arm to analyse")
    p.add_argument("--seed", type=int, default=42,
                   help="Seed suffix for stochastic models' prediction files")
    p.add_argument("--readout", type=str, default="mean",
                   help="Readout suffix for LSTM prediction files")
    p.add_argument("--bootstrap", type=int, default=10000,
                   help="Bootstrap resamples for the accuracy-difference CI")
    p.add_argument("--out", type=str, default=None,
                   help="Optional path to write results as CSV")
    return p.parse_args()


def load_predictions(preds_dir, sampling, model, condition, seed, readout):
    """Locates the prediction CSV for one run, tolerating the naming variants."""
    parts = [sampling, model, condition]
    if model == "lstm":
        parts.append(f"readout-{readout}")
    if model in ("lstm", "mlp"):
        parts.append(f"seed{seed}")
    path = Path(preds_dir) / ("_".join(parts) + ".csv")
    if not path.exists():
        return None
    frame = pd.read_csv(path)
    return frame.set_index("video_id").sort_index()


def mcnemar(correct_a, correct_b, n_bootstrap=10000, rng=None):
    """
    Exact McNemar test on paired correctness vectors.

    b = A correct, B wrong;  c = A wrong, B correct.
    Under H0 (equal accuracy) each discordant pair is a fair coin flip, so
    b ~ Binomial(b + c, 0.5). The exact binomial test is used rather than the
    chi-square approximation because discordant counts here are small enough
    that the approximation is unreliable.
    """
    b = int(np.sum(correct_a & ~correct_b))
    c = int(np.sum(~correct_a & correct_b))
    n_discordant = b + c

    if n_discordant == 0:
        p_value = 1.0
    else:
        p_value = float(stats.binomtest(b, n_discordant, 0.5).pvalue)

    acc_a = float(correct_a.mean())
    acc_b = float(correct_b.mean())
    diff = acc_a - acc_b

    # Paired bootstrap CI on the accuracy difference.
    rng = rng or np.random.default_rng(0)
    n = len(correct_a)
    idx = rng.integers(0, n, size=(n_bootstrap, n))
    diffs = correct_a[idx].mean(axis=1) - correct_b[idx].mean(axis=1)
    ci_low, ci_high = np.percentile(diffs, [2.5, 97.5])

    return {
        "b_only_a_correct": b,
        "c_only_b_correct": c,
        "n_discordant": n_discordant,
        "acc_a": acc_a,
        "acc_b": acc_b,
        "acc_diff": diff,
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_value": p_value,
    }


def holm_bonferroni(p_values):
    """Returns Holm-Bonferroni adjusted p-values, preserving input order."""
    m = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(m, dtype=float)
    running_max = 0.0
    for rank, idx in enumerate(order):
        value = (m - rank) * p_values[idx]
        running_max = max(running_max, value)
        adjusted[idx] = min(1.0, running_max)
    return adjusted


def compare(rows, label_a, label_b, frame_a, frame_b, family, rng, n_bootstrap):
    if frame_a is None or frame_b is None:
        return
    if not frame_a.index.equals(frame_b.index):
        raise ValueError(
            f"{label_a} and {label_b} were evaluated on different clips. "
            "Both runs must use --restrict_to_common for a paired test to be valid."
        )
    correct_a = (frame_a["y_true"] == frame_a["y_pred"]).to_numpy()
    correct_b = (frame_b["y_true"] == frame_b["y_pred"]).to_numpy()
    result = mcnemar(correct_a, correct_b, n_bootstrap=n_bootstrap, rng=rng)
    rows.append({"family": family, "a": label_a, "b": label_b,
                 "n_paired": len(frame_a), **result})


def main():
    args = parse_args()
    preds_dir = Path(args.preds_dir)
    if not preds_dir.is_absolute():
        preds_dir = REPO_ROOT / preds_dir
    if not preds_dir.exists():
        raise SystemExit(f"Predictions directory not found: {preds_dir}")

    rng = np.random.default_rng(0)
    rows = []

    def load(sampling, model):
        return load_predictions(preds_dir, sampling, model, args.condition,
                                args.seed, args.readout)

    # Family 1: sampling strategy vs the Targeted baseline, within each model.
    # This is the comparison RQ1 turns on.
    for model in MODEL_ORDER:
        baseline = load("targeted", model)
        for sampling in SAMPLING_ORDER[1:]:
            compare(rows, f"targeted/{model}", f"{sampling}/{model}",
                    baseline, load(sampling, model),
                    family=f"sampling|{model}", rng=rng, n_bootstrap=args.bootstrap)

    # Family 2: architecture pairs, within each sampling strategy.
    # This is the comparison the thesis's headline claim turns on.
    for sampling in SAMPLING_ORDER:
        for model_a, model_b in itertools.combinations(MODEL_ORDER, 2):
            compare(rows, f"{sampling}/{model_a}", f"{sampling}/{model_b}",
                    load(sampling, model_a), load(sampling, model_b),
                    family=f"architecture|{sampling}", rng=rng,
                    n_bootstrap=args.bootstrap)

    if not rows:
        raise SystemExit(
            f"No prediction files matched in {preds_dir}. "
            "Run scripts/run_ablation_threshold3.py first."
        )

    results = pd.DataFrame(rows)

    # Holm-Bonferroni within each family, since the families answer different questions.
    results["p_adjusted"] = np.nan
    for family, group in results.groupby("family"):
        results.loc[group.index, "p_adjusted"] = holm_bonferroni(
            group["p_value"].to_numpy()
        )
    results["significant_05"] = results["p_adjusted"] < 0.05

    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 50)

    for family, group in results.groupby("family"):
        print("\n" + "=" * 100)
        print(f"FAMILY: {family}   (condition={args.condition}, n={group['n_paired'].iloc[0]})")
        print("=" * 100)
        display = group[["a", "b", "acc_a", "acc_b", "acc_diff",
                         "ci_low", "ci_high", "n_discordant",
                         "p_value", "p_adjusted", "significant_05"]]
        print(display.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    n_sig = int(results["significant_05"].sum())
    print("\n" + "=" * 100)
    print(f"SUMMARY: {n_sig} of {len(results)} comparisons significant at "
          f"alpha=0.05 after Holm-Bonferroni correction.")
    sampling_sig = int(results[results.family.str.startswith("sampling")]["significant_05"].sum())
    arch_sig = int(results[results.family.str.startswith("architecture")]["significant_05"].sum())
    n_sampling = int((results.family.str.startswith("sampling")).sum())
    n_arch = int((results.family.str.startswith("architecture")).sum())
    print(f"  sampling comparisons     : {sampling_sig}/{n_sampling} significant")
    print(f"  architecture comparisons : {arch_sig}/{n_arch} significant")
    print("=" * 100)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(out_path, index=False)
        print(f"\nWrote results to {out_path}")


if __name__ == "__main__":
    main()
