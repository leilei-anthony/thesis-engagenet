# thesis-engagenet

Student engagement detection from video on the EngageNet dataset (Singh et al., 2023). The thesis asks how much **temporal frame selection** matters compared with **model architecture**. It crosses four sampling strategies (Start-Middle-End, and 3/5/7-changepoint on landmark-velocity peaks) with four models (LSTM, MLP, SVM, Random Forest) on the Threshold 3 task (`{0,1,2}` vs `{3}`).

The current write-up, results, and significance tests are in [docs/methodology-and-results.md](docs/methodology-and-results.md). The ICCE 2026 paper is in [paper/](paper/).

## Setup

```bash
conda env create -f environment.yml
conda activate thesis-engagenet
```

Data is not tracked. Place it as follows:

```
data/
├── raw_videos/{Train,Validation,Test}/*.mp4    EngageNet clips
├── labels/                                     {train,validation}_engagement_labels.xlsx, test_engagement_labels.csv
└── processed/                                  <sampling_method>-<split>.csv  (written by step 1)
```

## Pipeline

Run everything from the repo root.

```bash
# 1. Feature extraction (MediaPipe face/pose + AUs) -> data/processed/
python scripts/extraction/run_extraction.py --mode targeted
python scripts/extraction/run_extraction.py --num_changepoints 3   # repeat for 5 and 7

# 2. Threshold 3 sweep (all conditions restricted to the common video set)
python scripts/experiments/run_ablation_threshold3.py --smote both
python scripts/experiments/run_ablation_threshold3.py --seeds 42 43 44 45 46 --models lstm mlp --tag seeds
python scripts/experiments/run_ablation_threshold3.py --models lstm --readouts mean last attention \
    --seeds 42 43 44 45 46 --tag readout

# 3. Analysis
python scripts/analysis/summarize_threshold3.py --log artifacts/ablation_threshold3_common.txt
python scripts/analysis/significance_tests.py --preds_dir artifacts/predictions_threshold3_common
python scripts/analysis/smote_delta.py --log artifacts/ablation_threshold3_common.txt
python scripts/analysis/analyze_rf_feature_importance.py --sampling_method targeted --restrict_to_common

# 4. Regression tests
python -m pytest tests/ -v
```

Individual runs can also be launched directly with `src/train.py`, `src/evaluate.py` (LSTM/MLP) and `src/train_traditional.py` (SVM/RF). Use `--help` on each for the options.

## Layout

```
src/            pipeline code: feature_extraction, dataset, model, train, train_traditional, evaluate
scripts/
  extraction/   run_extraction.py, benchmark_feature_extraction_time.py
  experiments/  run_ablation_threshold3.py
  analysis/     summaries, significance tests, SMOTE deltas, RF feature importance
tests/          dataset-integrity regression tests
assets/         MediaPipe face/pose landmarker models
docs/           methodology-and-results.md, experiments.md (run log), meeting-notes/
paper/          LaTeX sources (paper.tex, anonymised paper-anonymous.tex), references.bib
archive/        pre-remediation scripts and docs, kept for the record (see archive/README.md)
data/           local only, see Setup
artifacts/      local only: extraction outputs, checkpoints, sweep logs, predictions, figures
```
