"""
Feature extraction runner for one sampling method across dataset splits.

Replaces the duplicated run_extraction_pipeline{,_7}.py pair (now in
archive/scripts/) with a single parameterised driver. Differences from the
legacy scripts:

  * Mode and changepoint count are arguments rather than forked copies, so
    targeted and any k-changepoint extraction share one code path.
  * Extraction only. The legacy scripts also trained and evaluated every model
    afterwards under the pre-remediation protocol; training is now driven by
    scripts/experiments/run_ablation_threshold3.py.
  * The merged collective_features.csv is moved (not copied) into
    data/processed/, so the ~1 GB per-method CSVs are not stored twice.

For each split this runs src/feature_extraction.py, which reads videos from
data/raw_videos/<Split>/ and labels from data/labels/, writes per-video outputs
to artifacts/feature_extraction/<Method>_Dataset_<Split>/, and merges them into
collective_features.csv there. That file is then moved to
data/processed/<sampling_method>-<split>.csv, the name EngagementDataset loads.

Examples
--------
# 5-changepoint features for all splits
python scripts/extraction/run_extraction.py --num_changepoints 5

# targeted (start/middle/end) features for the test split only
python scripts/extraction/run_extraction.py --mode targeted --splits Test
"""

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FEATURE_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "feature_extraction"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

SPLITS = ["Validation", "Test", "Train"]


def parse_args():
    p = argparse.ArgumentParser(description="Extract features for one sampling method and stage them in data/processed")
    p.add_argument("--mode", type=str, default="changepoint", choices=["targeted", "changepoint"],
                   help="targeted: first/middle/last valid frame; changepoint: top-k landmark-velocity peaks")
    p.add_argument("--num_changepoints", type=int, default=3,
                   help="Frames selected per video in changepoint mode. Ignored for targeted.")
    p.add_argument("--splits", type=str, nargs="+", default=SPLITS, choices=SPLITS)
    p.add_argument("--dry_run", action="store_true",
                   help="Print the commands and file moves that would run, without running them")
    return p.parse_args()


def output_names(mode, num_changepoints, split):
    """Returns (extraction output dir, processed CSV path) for one split.

    Mirrors the naming in src/feature_extraction.py and src/dataset.py.
    """
    if mode == "changepoint":
        subdir = f"{num_changepoints}_Changepoint_Dataset_{split}"
        sampling_method = f"{num_changepoints}-changepoint"
    else:
        subdir = f"Targeted_Dataset_{split}"
        sampling_method = "targeted"
    return FEATURE_OUTPUT_ROOT / subdir, PROCESSED_DIR / f"{sampling_method}-{split.lower()}.csv"


def run_cmd(cmd, dry_run=False):
    print(f"\n>>> {' '.join(cmd)}", flush=True)
    if dry_run:
        return True
    t0 = time.time()
    # Not captured: extraction takes hours and prints per-video progress.
    res = subprocess.run(cmd, cwd=REPO_ROOT)
    dt = time.time() - t0
    if res.returncode != 0:
        print(f"ERROR: exit {res.returncode} after {dt:.1f}s", flush=True)
        return False
    print(f"SUCCESS ({dt:.1f}s)", flush=True)
    return True


def stage_processed_file(src_dir, dest, dry_run=False):
    src = src_dir / "collective_features.csv"
    print(f"Moving {src} -> {dest}", flush=True)
    if dry_run:
        return True
    if not src.exists():
        print(f"ERROR: Source file {src} does not exist!", flush=True)
        return False
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))
    return True


def main():
    args = parse_args()
    label = "TARGETED" if args.mode == "targeted" else f"{args.num_changepoints}-CHANGEPOINT"
    print("==================================================")
    print(f"STARTING {label} FEATURE EXTRACTION")
    print("==================================================")

    for split in args.splits:
        print(f"\n--- Extracting features for split: {split} ---", flush=True)
        cmd = [
            "conda", "run", "--no-capture-output", "-n", "thesis-engagenet", "python",
            "src/feature_extraction.py", split, args.mode, str(args.num_changepoints),
        ]
        if not run_cmd(cmd, args.dry_run):
            print(f"Pipeline stopped: Feature extraction failed for split {split}")
            sys.exit(1)

        src_dir, dest = output_names(args.mode, args.num_changepoints, split)
        if not stage_processed_file(src_dir, dest, args.dry_run):
            print(f"Pipeline stopped: Staging features failed for split {split}")
            sys.exit(1)

    print(f"\n{label} feature extraction completed. Processed CSVs are in {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
