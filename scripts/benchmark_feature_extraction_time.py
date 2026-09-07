#!/usr/bin/env python3
"""
Benchmark feature extraction time across temporal sampling methods.

Runs 40 timed extractions (4 sampling methods × 10 sample videos) and logs
timing data to artifacts/feature_extraction_timing_sample.txt for analysis.
"""

import sys
import os
from pathlib import Path
import glob
import time
from datetime import datetime

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.feature_extraction import VideoFeatureExtractor

SAMPLE_DIR = REPO_ROOT / "sample"
OUTPUT_ROOT = REPO_ROOT / "artifacts" / "feature_extraction_timing_sample"
LOG_FILE = REPO_ROOT / "artifacts" / "feature_extraction_timing_sample.txt"


def main():
    """Run feature extraction timing benchmark on sample/ videos."""
    # Create output root
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Collect sample videos
    video_files = sorted(glob.glob(str(SAMPLE_DIR / "*.mp4")))
    if not video_files:
        print(f"ERROR: No .mp4 files found in {SAMPLE_DIR}")
        sys.exit(1)

    print(f"Found {len(video_files)} sample video(s)")

    # Configuration: 4 sampling methods
    configs = [
        {"name": "targeted", "mode": "targeted", "changepoints": 0},
        {"name": "3-changepoint", "mode": "changepoint", "changepoints": 3},
        {"name": "5-changepoint", "mode": "changepoint", "changepoints": 5},
        {"name": "7-changepoint", "mode": "changepoint", "changepoints": 7},
    ]

    # Initialize extractor ONCE (all 40 runs will reuse the same instance)
    print("\nInitializing VideoFeatureExtractor...")
    extractor = VideoFeatureExtractor(
        output_root=OUTPUT_ROOT,
        extraction_mode="targeted",
        num_changepoints=0,
        frame_skip=2,
        fast_rembg=True,
        mp_complexity=1,
        labels_df=None
    )

    # Warm-up: load models once, untimed
    print("Loading AI models (warm-up, untimed)...")
    extractor.init_models()

    # Open log file for writing
    with open(LOG_FILE, 'w') as log:
        log.write(f"Feature Extraction Time Benchmark\n")
        log.write(f"Timestamp: {datetime.now().isoformat()}\n")
        log.write(f"Sample directory: {SAMPLE_DIR}\n")
        log.write(f"Number of sample videos: {len(video_files)}\n")
        log.write(f"Number of configs: {len(configs)}\n")
        log.write(f"Total runs: {len(configs) * len(video_files)}\n")
        log.write("\n" + "="*120 + "\n\n")

        run_count = 0
        all_timings = []

        # Run all 40 configurations
        for config in configs:
            config_name = config['name']
            extraction_mode = config['mode']
            num_changepoints = config['changepoints']

            # Update extractor configuration for this batch
            extractor.extraction_mode = extraction_mode
            extractor.num_changepoints = num_changepoints

            print(f"\nProcessing config: {config_name}")
            log.write(f"Config: {config_name}\n")
            log.write(f"Extraction mode: {extraction_mode}, Changepoints: {num_changepoints}\n")
            log.write("-" * 120 + "\n")

            for i, video_path in enumerate(video_files, 1):
                video_filename = Path(video_path).name
                video_name = Path(video_path).stem

                # Create timing dict for this run
                timing = {}

                # Run extraction with timing
                print(f"  [{i}/{len(video_files)}] {video_name}...", end=" ", flush=True)
                try:
                    df = extractor.process_single_video(
                        video_path,
                        relative_dir=config_name,
                        timing=timing
                    )

                    # Extract timing values
                    scan_sec = timing.get('scan_seconds', 0)
                    frame_extract_sec = timing.get('frame_extract_seconds', 0)
                    final_pass_sec = timing.get('final_pass_seconds', 0)
                    total_sec = timing.get('total_seconds', 0)

                    status = "OK" if df is not None else "SKIPPED"
                    n_frames = len(df) if df is not None else 0

                    print(f"{status} ({total_sec:.3f}s)")

                    # Log detailed timing
                    log_entry = (
                        f"  {video_filename:<40} | "
                        f"Scan: {scan_sec:7.3f}s | "
                        f"FrameExt: {frame_extract_sec:7.3f}s | "
                        f"FinalPass: {final_pass_sec:7.3f}s | "
                        f"Total: {total_sec:7.3f}s | "
                        f"Frames: {n_frames:3d} | "
                        f"Status: {status}\n"
                    )
                    log.write(log_entry)

                    if df is not None:
                        all_timings.append({
                            'config': config_name,
                            'video': video_filename,
                            'scan_seconds': scan_sec,
                            'frame_extract_seconds': frame_extract_sec,
                            'final_pass_seconds': final_pass_sec,
                            'total_seconds': total_sec,
                            'n_frames': n_frames
                        })

                    run_count += 1

                except Exception as e:
                    print(f"ERROR: {e}")
                    log.write(f"  {video_filename:<40} | ERROR: {str(e)}\n")

            log.write("\n")

        # Write summary statistics
        log.write("\n" + "="*120 + "\n")
        log.write("SUMMARY STATISTICS\n")
        log.write("="*120 + "\n\n")

        # Average per video (across all configs)
        if all_timings:
            import pandas as pd
            df_timings = pd.DataFrame(all_timings)

            log.write("Average Total Extraction Time per Video (across all 4 configs):\n")
            log.write("-" * 120 + "\n")
            per_video = df_timings.groupby('video')['total_seconds'].agg(['mean', 'std', 'count'])
            for video, row in per_video.iterrows():
                log.write(f"  {video:<40} | Mean: {row['mean']:7.3f}s | Std: {row['std']:7.3f}s | N: {int(row['count'])}\n")

            log.write("\n")
            log.write("Average Time per Sampling Method (across all 10 videos):\n")
            log.write("-" * 120 + "\n")
            per_config = df_timings.groupby('config')[['scan_seconds', 'frame_extract_seconds', 'final_pass_seconds', 'total_seconds']].agg(['mean', 'std'])
            for config_name in per_config.index:
                row = per_config.loc[config_name]
                log.write(f"  Config: {config_name}\n")
                log.write(f"    Scan:        {row[('scan_seconds', 'mean')]:7.3f}s ± {row[('scan_seconds', 'std')]:7.3f}s\n")
                log.write(f"    FrameExt:    {row[('frame_extract_seconds', 'mean')]:7.3f}s ± {row[('frame_extract_seconds', 'std')]:7.3f}s\n")
                log.write(f"    FinalPass:   {row[('final_pass_seconds', 'mean')]:7.3f}s ± {row[('final_pass_seconds', 'std')]:7.3f}s\n")
                log.write(f"    Total:       {row[('total_seconds', 'mean')]:7.3f}s ± {row[('total_seconds', 'std')]:7.3f}s\n")
                log.write("\n")

            # Deltas from targeted baseline
            log.write("\nDelta from Targeted Baseline (change in total_seconds):\n")
            log.write("-" * 120 + "\n")
            targeted_mean = df_timings[df_timings['config'] == 'targeted']['total_seconds'].mean()
            for config_name in sorted(df_timings['config'].unique()):
                config_mean = df_timings[df_timings['config'] == config_name]['total_seconds'].mean()
                delta = config_mean - targeted_mean
                delta_pct = (delta / targeted_mean * 100) if targeted_mean > 0 else 0
                log.write(f"  {config_name:<20} | Mean: {config_mean:7.3f}s | Delta: {delta:+7.3f}s ({delta_pct:+6.1f}%)\n")

    print(f"\n✓ Benchmark complete. Logged {run_count} runs to {LOG_FILE}")


if __name__ == "__main__":
    main()
