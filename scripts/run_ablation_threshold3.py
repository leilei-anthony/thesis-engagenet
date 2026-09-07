"""
Threshold 3 ablation sweep, post-remediation.

Replaces the duplicated run_ablation_targeted_3_5_7{,_smote}.py pair with a
single parameterised driver. Differences from the legacy scripts:

  * --restrict_to_common is always passed, so every sampling condition is
    trained and evaluated on the identical set of videos (2719 train / 2005
    test). The legacy sweep compared targeted/3-changepoint on 2227 test videos
    against 5-/7-changepoint on 2005, confounding sampling with test-set
    composition.
  * SMOTE is a flag rather than a forked copy of the script, so baseline and
    SMOTE runs come from the same code path in the same session (the legacy
    pair produced deltas that did not reconcile for the unseeded models).
  * Seeds are explicit. LSTM/MLP run once per seed; SVM/RF are deterministic
    and run once regardless.
  * LSTM readout is sweepable (mean/last/attention) for the readout ablation.
  * Per-sample predictions are dumped for paired significance testing.
  * A JSONL manifest records every run's configuration and output path, so
    downstream analysis does not depend on regex-parsing the text log.

Examples
--------
# main re-run: baseline + SMOTE, single seed, default readout
python scripts/run_ablation_threshold3.py --smote both

# multi-seed for the stochastic models
python scripts/run_ablation_threshold3.py --seeds 42 43 44 45 46 --models lstm mlp

# readout ablation
python scripts/run_ablation_threshold3.py --models lstm --readouts mean last attention \
    --seeds 42 43 44 45 46
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
ARTIFACT_DIR = REPO_ROOT / "artifacts"

SAMPLING_METHODS = ["targeted", "3-changepoint", "5-changepoint", "7-changepoint"]
MODELS = ["lstm", "mlp", "svm", "rf"]
STOCHASTIC_MODELS = {"lstm", "mlp"}

# Threshold 3 only: binary {0,1,2} vs {3}, unweighted, 20 epochs -- matching the
# legacy CONFIGS entry ("classification", 3, ["--no_class_weights", "--epochs", "20"]).
MODE = "classification"
BINARIZE_THRESHOLD = 3
EPOCHS = "20"


def parse_args():
    p = argparse.ArgumentParser(description="Threshold 3 ablation sweep (common-video restricted)")
    p.add_argument("--seeds", type=int, nargs="+", default=[42],
                   help="Seeds for the stochastic models (LSTM/MLP). SVM/RF ignore this.")
    p.add_argument("--models", type=str, nargs="+", default=MODELS, choices=MODELS)
    p.add_argument("--sampling", type=str, nargs="+", default=SAMPLING_METHODS,
                   choices=SAMPLING_METHODS)
    p.add_argument("--smote", type=str, default="both", choices=["off", "on", "both"])
    p.add_argument("--readouts", type=str, nargs="+", default=["mean"],
                   choices=["mean", "last", "attention"],
                   help="LSTM temporal readouts to sweep. Ignored for non-LSTM models.")
    p.add_argument("--tag", type=str, default="common",
                   help="Suffix for the output artifact filenames")
    p.add_argument("--dry_run", action="store_true",
                   help="Print the commands that would run, without running them")
    return p.parse_args()


def run_cmd(cmd, dry_run=False):
    printable = " ".join(cmd)
    print(f"\n>>> {printable}", flush=True)
    if dry_run:
        return True, ""
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"ERROR: exit {res.returncode} after {dt:.1f}s", flush=True)
        print(res.stderr[-2000:], flush=True)
        return False, res.stdout + "\n" + res.stderr
    print(f"SUCCESS ({dt:.1f}s)", flush=True)
    return True, res.stdout


def check_data_present(sampling_method):
    for split in ["train", "validation", "test"]:
        f = PROCESSED_DIR / f"{sampling_method}-{split}.csv"
        if not f.exists():
            print(f"ERROR: missing required data file {f}", flush=True)
            return False
    return True


def build_runs(args):
    """Expands the requested sweep into a flat list of run descriptors."""
    smote_settings = {"off": [False], "on": [True], "both": [False, True]}[args.smote]
    runs = []
    for sampling in args.sampling:
        for model in args.models:
            for use_smote in smote_settings:
                # SVM/RF are deterministic (random_state=42), so multiple seeds
                # would produce identical output. Run them once.
                seeds = args.seeds if model in STOCHASTIC_MODELS else [None]
                # Readout only applies to the LSTM.
                readouts = args.readouts if model == "lstm" else [None]
                for seed in seeds:
                    for readout in readouts:
                        runs.append({
                            "sampling_method": sampling,
                            "model": model,
                            "use_smote": use_smote,
                            "seed": seed,
                            "readout": readout,
                        })
    return runs


def run_label(run):
    parts = [run["sampling_method"], run["model"]]
    parts.append("smote" if run["use_smote"] else "baseline")
    if run["readout"] is not None:
        parts.append(f"readout-{run['readout']}")
    if run["seed"] is not None:
        parts.append(f"seed{run['seed']}")
    return "_".join(parts)


def main():
    args = parse_args()

    out_file = ARTIFACT_DIR / f"ablation_threshold3_{args.tag}.txt"
    manifest_file = ARTIFACT_DIR / f"ablation_threshold3_{args.tag}_manifest.jsonl"
    preds_dir = ARTIFACT_DIR / f"predictions_threshold3_{args.tag}"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    preds_dir.mkdir(parents=True, exist_ok=True)

    for sm in args.sampling:
        if not check_data_present(sm):
            sys.exit(1)

    runs = build_runs(args)

    print("=" * 60, flush=True)
    print("THRESHOLD 3 ABLATION (common-video restricted)", flush=True)
    print(f"  sampling : {args.sampling}", flush=True)
    print(f"  models   : {args.models}", flush=True)
    print(f"  seeds    : {args.seeds} (stochastic models only)", flush=True)
    print(f"  readouts : {args.readouts} (LSTM only)", flush=True)
    print(f"  smote    : {args.smote}", flush=True)
    print(f"  runs     : {len(runs)}", flush=True)
    print(f"  results  : {out_file}", flush=True)
    print(f"  manifest : {manifest_file}", flush=True)
    print("=" * 60, flush=True)

    n_ok = n_fail = 0
    mode_flags = ["--mode", MODE, "--binarize_threshold", str(BINARIZE_THRESHOLD),
                  "--no_class_weights", "--restrict_to_common"]

    with open(out_file, "w") as f_out, open(manifest_file, "w") as f_manifest:
        for i, run in enumerate(runs, 1):
            label = run_label(run)
            preds_path = preds_dir / f"{label}.csv"

            print(f"\n[{i}/{len(runs)}] {label}", flush=True)
            f_out.write("\n" + "=" * 40 + "\n")
            f_out.write(f"SAMPLING METHOD: {run['sampling_method'].upper()} | "
                        f"MODEL: {run['model'].upper()}\n")
            f_out.write(f"RUN: {label}\n")
            f_out.write("=" * 40 + "\n")
            f_out.flush()

            if run["model"] in ("svm", "rf"):
                cmd = ["conda", "run", "-n", "thesis-engagenet", "python",
                       "src/train_traditional.py",
                       "--sampling_method", run["sampling_method"],
                       "--model", run["model"],
                       "--mode", MODE,
                       "--binarize_threshold", str(BINARIZE_THRESHOLD),
                       "--no_class_weights", "--restrict_to_common",
                       "--dump_preds", str(preds_path)]
                if run["use_smote"]:
                    cmd.append("--use_smote")
                ok, output = run_cmd(cmd, args.dry_run)
                f_out.write(output)
            else:
                train_cmd = ["conda", "run", "-n", "thesis-engagenet", "python", "src/train.py",
                             "--model", run["model"],
                             "--sampling_method", run["sampling_method"],
                             "--epochs", EPOCHS,
                             "--seed", str(run["seed"])] + mode_flags
                if run["readout"] is not None:
                    train_cmd += ["--readout", run["readout"]]
                if run["use_smote"]:
                    train_cmd.append("--use_smote")

                ok, train_output = run_cmd(train_cmd, args.dry_run)
                if not ok:
                    f_out.write(train_output)
                    f_out.flush()
                    n_fail += 1
                    f_manifest.write(json.dumps({**run, "status": "train_failed",
                                                 "label": label}) + "\n")
                    f_manifest.flush()
                    continue

                eval_cmd = ["conda", "run", "-n", "thesis-engagenet", "python", "src/evaluate.py",
                            "--model", run["model"],
                            "--sampling_method", run["sampling_method"],
                            "--mode", MODE,
                            "--binarize_threshold", str(BINARIZE_THRESHOLD),
                            "--no_class_weights", "--restrict_to_common",
                            "--seed", str(run["seed"]),
                            "--dump_preds", str(preds_path)]
                if run["readout"] is not None:
                    eval_cmd += ["--readout", run["readout"]]
                if run["use_smote"]:
                    eval_cmd.append("--use_smote")

                ok, output = run_cmd(eval_cmd, args.dry_run)
                f_out.write(output)

            f_out.flush()
            n_ok += int(ok)
            n_fail += int(not ok)
            f_manifest.write(json.dumps({
                **run,
                "label": label,
                "status": "ok" if ok else "failed",
                "predictions": str(preds_path.relative_to(REPO_ROOT)),
            }) + "\n")
            f_manifest.flush()

    print(f"\nDone. {n_ok} succeeded, {n_fail} failed.", flush=True)
    print(f"Results:     {out_file}", flush=True)
    print(f"Manifest:    {manifest_file}", flush=True)
    print(f"Predictions: {preds_dir}", flush=True)
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
