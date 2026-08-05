"""
Parses a Threshold 3 sweep log into a tidy DataFrame and prints the results
table, plus the effect-size comparison the thesis's central claim rests on.

The sweep writes each run's stdout under a 'RUN: <label>' header (see
run_ablation_threshold3.py), so runs are keyed by that label rather than by
position -- unlike the legacy markdown tables, which had to be maintained by
hand.

Usage:
    python scripts/summarize_threshold3.py --log artifacts/ablation_threshold3_common.txt
    python scripts/summarize_threshold3.py --log ... --seeds   # aggregate mean+/-sd over seeds
"""
import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]

SAMPLING_ORDER = ["targeted", "3-changepoint", "5-changepoint", "7-changepoint"]
MODEL_ORDER = ["lstm", "mlp", "svm", "rf"]

PATTERNS = {
    "accuracy": re.compile(r"^Accuracy: ([\d.]+)", re.M),
    "macro_f1": re.compile(r"^Macro F1-score: ([\d.]+)", re.M),
    "weighted_f1": re.compile(r"^Weighted F1-score: ([\d.]+)", re.M),
    "mse": re.compile(r"^Overall MSE: ([\d.]+)", re.M),
    "pcc": re.compile(r"^Pearson Correlation \(PCC\): ([-\d.]+) \(p-value: ([\d.e+-]+)\)", re.M),
    "training_time": re.compile(r"^Training Time: ([\d.]+) seconds", re.M),
    "n_test": re.compile(r"Loaded (\d+) video sequences for split 'test'", re.M),
}
CLASS_F1 = re.compile(r"^\s+Class (\d+): Precision=[\d.]+, Recall=[\d.]+, F1-score=([\d.]+)", re.M)


def parse_label(label):
    """targeted_lstm_baseline_readout-mean_seed42 -> dict of components."""
    out = {"sampling_method": None, "model": None, "condition": None,
           "readout": None, "seed": None}
    for sampling in sorted(SAMPLING_ORDER, key=len, reverse=True):
        if label.startswith(sampling + "_"):
            out["sampling_method"] = sampling
            rest = label[len(sampling) + 1:]
            break
    else:
        return None
    parts = rest.split("_")
    out["model"] = parts[0]
    out["condition"] = parts[1] if len(parts) > 1 else "baseline"
    for part in parts[2:]:
        if part.startswith("readout-"):
            out["readout"] = part.split("-", 1)[1]
        elif part.startswith("seed"):
            out["seed"] = int(part[4:])
    return out


def parse_log(path):
    text = Path(path).read_text()
    # Split on the run headers the sweep driver writes.
    chunks = re.split(r"^RUN: (.+)$", text, flags=re.M)
    rows = []
    for i in range(1, len(chunks), 2):
        label, body = chunks[i].strip(), chunks[i + 1]
        meta = parse_label(label)
        if meta is None:
            continue
        row = {"label": label, **meta}
        for key, pattern in PATTERNS.items():
            match = pattern.search(body)
            if not match:
                row[key] = np.nan
                continue
            if key == "pcc":
                row["pcc"] = float(match.group(1))
                row["pcc_p"] = float(match.group(2))
            elif key == "n_test":
                row["n_test"] = int(match.group(1))
            else:
                row[key] = float(match.group(1))
        for class_idx, f1 in CLASS_F1.findall(body):
            row[f"class{class_idx}_f1"] = float(f1)
        rows.append(row)
    return pd.DataFrame(rows)


def order_frame(frame):
    frame = frame.copy()
    frame["sampling_method"] = pd.Categorical(frame["sampling_method"],
                                              SAMPLING_ORDER, ordered=True)
    frame["model"] = pd.Categorical(frame["model"], MODEL_ORDER, ordered=True)
    return frame.sort_values(["sampling_method", "model", "seed"])


def report_effect_sizes(frame):
    """
    The thesis's headline claim is that architecture matters far more than
    sampling. Quantify both, using only the deterministic models where the
    sampling estimate carries no seed noise.
    """
    print("\n" + "=" * 78)
    print("EFFECT SIZES: sampling vs architecture (accuracy)")
    print("=" * 78)

    print("\nSampling-attributable spread, per model (max - min across sampling methods):")
    for model in MODEL_ORDER:
        sub = frame[frame.model == model]
        if sub.empty or sub.accuracy.isna().all():
            continue
        per_sampling = sub.groupby("sampling_method", observed=True)["accuracy"].mean()
        spread = per_sampling.max() - per_sampling.min()
        deterministic = model in ("svm", "rf")
        note = "deterministic - noise-free" if deterministic else "UNSEEDED - includes run variance"
        print(f"  {model.upper():4s}: {spread * 100:5.2f} pts   ({note})")

    print("\nArchitecture-attributable spread, per sampling method (max - min across models):")
    arch_spreads = []
    for sampling in SAMPLING_ORDER:
        sub = frame[frame.sampling_method == sampling]
        if sub.empty or sub.accuracy.isna().all():
            continue
        per_model = sub.groupby("model", observed=True)["accuracy"].mean()
        spread = per_model.max() - per_model.min()
        arch_spreads.append(spread)
        best = per_model.idxmax()
        worst = per_model.idxmin()
        print(f"  {sampling:15s}: {spread * 100:5.2f} pts   "
              f"(best {best.upper()} {per_model.max():.4f}, worst {worst.upper()} {per_model.min():.4f})")

    det = frame[frame.model.isin(["svm", "rf"])]
    if not det.empty and arch_spreads:
        samp_spreads = []
        for model in ("svm", "rf"):
            sub = det[det.model == model]
            if sub.empty:
                continue
            per_sampling = sub.groupby("sampling_method", observed=True)["accuracy"].mean()
            samp_spreads.append(per_sampling.max() - per_sampling.min())
        # Guard against a single-sampling-method (or partial) log, where the
        # sampling spread is zero and the ratio is undefined.
        samp_spreads = [s for s in samp_spreads if s > 0]
        if samp_spreads and len(arch_spreads) > 0:
            lo = min(arch_spreads) / max(samp_spreads)
            hi = max(arch_spreads) / min(samp_spreads)
            print(f"\n  Architecture effect is {lo:.1f}x to {hi:.1f}x the sampling effect")
            print("  (sampling measured on deterministic models only, so noise-free)")
        else:
            print("\n  (ratio not computable yet - need >1 sampling method with results)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--log", type=str, default="artifacts/ablation_threshold3_common.txt")
    p.add_argument("--seeds", action="store_true",
                   help="Aggregate mean+/-sd across seeds instead of listing every run")
    p.add_argument("--condition", type=str, default="baseline",
                   choices=["baseline", "smote", "all"])
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()

    log_path = Path(args.log)
    if not log_path.is_absolute():
        log_path = REPO_ROOT / log_path
    if not log_path.exists():
        raise SystemExit(f"Log not found: {log_path}")

    frame = parse_log(log_path)
    if frame.empty:
        raise SystemExit(f"No runs parsed from {log_path}")

    if args.condition != "all":
        frame = frame[frame.condition == args.condition]

    frame = order_frame(frame)

    n_test = frame["n_test"].dropna().unique()
    print(f"Parsed {len(frame)} runs from {log_path.name}")
    print(f"Test-set size(s): {sorted(n_test.astype(int))}"
          f"{'  <-- OK, single common set' if len(n_test) == 1 else '  <-- WARNING: conditions differ!'}")

    cols = ["sampling_method", "model", "accuracy", "macro_f1", "weighted_f1",
            "class0_f1", "class1_f1", "pcc", "mse", "training_time"]
    cols = [c for c in cols if c in frame.columns]

    if args.seeds:
        grouped = frame.groupby(["sampling_method", "model"], observed=True)
        summary = grouped.agg(
            n=("accuracy", "size"),
            acc_mean=("accuracy", "mean"), acc_sd=("accuracy", "std"),
            f1_mean=("macro_f1", "mean"), f1_sd=("macro_f1", "std"),
        ).reset_index()
        print("\n" + "=" * 78)
        print(f"THRESHOLD 3 -- {args.condition} (mean +/- sd across seeds)")
        print("=" * 78)
        print(summary.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    else:
        print("\n" + "=" * 78)
        print(f"THRESHOLD 3 -- {args.condition}")
        print("=" * 78)
        print(frame[cols].to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    report_effect_sizes(frame)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(out_path, index=False)
        print(f"\nWrote parsed results to {out_path}")


if __name__ == "__main__":
    main()
