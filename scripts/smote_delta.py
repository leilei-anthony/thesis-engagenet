"""
SMOTE effect: baseline vs SMOTE, from a matched pair of runs.

The earlier analysis reported SMOTE deltas that reconciled exactly for SVM and
Random Forest but not for LSTM and MLP -- the mismatch fell precisely on the two
unseeded architectures, indicating the baseline and SMOTE tables had been
populated from different sweep runs. This script removes that failure mode: both
arms are read from the same log (so they come from one session), and for the
stochastic models the delta is computed per seed and then averaged, so baseline
and SMOTE are always compared at the same seed.

Usage:
    python scripts/smote_delta.py --log artifacts/ablation_threshold3_common.txt
    python scripts/smote_delta.py --log artifacts/ablation_threshold3_seeds.txt
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from summarize_threshold3 import parse_log, MODEL_ORDER, SAMPLING_ORDER  # noqa: E402

METRICS = ["accuracy", "macro_f1", "class0_f1", "class1_f1", "training_time"]
DETERMINISTIC = {"svm", "rf"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", type=str, default="artifacts/ablation_threshold3_common.txt")
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()

    log_path = Path(args.log)
    if not log_path.is_absolute():
        log_path = REPO_ROOT / log_path
    frame = parse_log(log_path)
    if frame.empty:
        raise SystemExit(f"No runs parsed from {log_path}")

    # Pair baseline against SMOTE on (sampling, model, seed). Including seed in
    # the key is the whole point: it guarantees like-for-like comparison for the
    # stochastic models.
    key = ["sampling_method", "model", "seed"]
    baseline = frame[frame.condition == "baseline"].set_index(key)
    smote = frame[frame.condition == "smote"].set_index(key)

    shared = baseline.index.intersection(smote.index)
    if len(shared) == 0:
        raise SystemExit("No matched baseline/SMOTE pairs found in this log.")

    unmatched = (len(baseline) - len(shared)) + (len(smote) - len(shared))
    if unmatched:
        print(f"WARNING: {unmatched} run(s) had no counterpart and are excluded.\n")

    rows = []
    for metric in METRICS:
        if metric not in frame.columns:
            continue
        delta = smote.loc[shared, metric] - baseline.loc[shared, metric]
        delta = delta.reset_index()
        delta.columns = key + ["delta"]
        delta["metric"] = metric
        rows.append(delta)
    deltas = pd.concat(rows, ignore_index=True)

    print(f"Matched pairs: {len(shared)}  (log: {log_path.name})")
    seeds = sorted({s for s in frame['seed'].dropna().unique()})
    print(f"Seeds present: {seeds if seeds else 'none (deterministic models only)'}\n")

    print("=" * 88)
    print("SMOTE effect (SMOTE - baseline), averaged over sampling methods")
    print("=" * 88)

    summary = []
    for model in MODEL_ORDER:
        sub = deltas[deltas.model == model]
        if sub.empty:
            continue
        row = {"model": model,
               "determinism": "exact" if model in DETERMINISTIC else "mean over seeds"}
        for metric in METRICS:
            values = sub[sub.metric == metric]["delta"]
            if values.empty:
                continue
            row[f"d_{metric}"] = values.mean()
            if model not in DETERMINISTIC:
                # Spread of the per-pair deltas. With several seeds present this
                # is dominated by seed variance; with a single seed it reflects
                # variation across sampling methods only. The printout below
                # labels which case applies rather than assuming.
                row[f"sd_{metric}"] = values.std()
        summary.append(row)

    summary = pd.DataFrame(summary)
    display_cols = ["model", "determinism", "d_accuracy", "d_macro_f1",
                    "d_class1_f1", "d_training_time"]
    display_cols = [c for c in display_cols if c in summary.columns]
    print(summary[display_cols].to_string(index=False, float_format=lambda v: f"{v:+.4f}"))

    if "sd_accuracy" in summary.columns:
        n_seeds = len([s for s in frame['seed'].dropna().unique()])
        source = ("across seeds and sampling methods" if n_seeds > 1
                  else "across sampling methods only (single seed in this log)")
        print(f"\nFor the stochastic models, spread of the accuracy delta {source}:")
        for _, r in summary.iterrows():
            if r["model"] in DETERMINISTIC or pd.isna(r.get("sd_accuracy")):
                continue
            mean, sd = r["d_accuracy"], r["sd_accuracy"]
            verdict = ("indistinguishable from that spread"
                       if abs(mean) < sd else "larger than that spread")
            print(f"  {r['model'].upper():4s}: {mean:+.4f} +/- {sd:.4f}  -> {verdict}")

    print("\n" + "=" * 88)
    print("Per sampling method (accuracy delta)")
    print("=" * 88)
    acc = deltas[deltas.metric == "accuracy"]
    pivot = acc.pivot_table(index="sampling_method", columns="model",
                            values="delta", aggfunc="mean", observed=True)
    pivot = pivot.reindex([s for s in SAMPLING_ORDER if s in pivot.index])
    pivot = pivot[[m for m in MODEL_ORDER if m in pivot.columns]]
    print(pivot.to_string(float_format=lambda v: f"{v:+.4f}"))

    overall = acc["delta"].mean()
    print(f"\nOverall mean accuracy delta across all matched pairs: {overall:+.4f}")

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        deltas.to_csv(out_path, index=False)
        print(f"\nWrote per-pair deltas to {out_path}")


if __name__ == "__main__":
    main()
