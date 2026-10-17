# Agent Guidelines - Thesis EngageNet Project

Welcome to the `thesis-engagenet` workspace! This file contains development guidelines and architecture patterns to ensure consistency when working on the deep learning training pipeline.

## Core Guidelines

1. **Environment Consistency**:
   - Always run commands and python scripts using the `thesis-engagenet` conda environment:
     ```bash
     conda run -n thesis-engagenet python <script.py>
     ```
   - Run scripts from the repo root (for example `python scripts/experiments/run_ablation_threshold3.py`). See [README.md](README.md) for the layout and pipeline.

2. **Dataset Swapping**:
   - Keep dataset loading modular. Use the `sampling_method` parameter to select one of `SUPPORTED_SAMPLING_METHODS` in `src/dataset.py`: `targeted` (Start-Middle-End), `3-changepoint`, `5-changepoint`, `7-changepoint`. BOCPD is not implemented, and `bocpd` is rejected.
   - Do not hardcode paths or sampling-specific logic in the training loop. All data preprocessing should be contained within `src/dataset.py`, and frame extraction within `src/feature_extraction.py`.

3. **Label Handling**:
   - Correctly map the labels:
     - `Not-Engaged` -> `0` (Completely Disengaged)
     - `Barely-engaged` -> `1` (Barely Engaged)
     - `Engaged` -> `2` (Engaged)
     - `Highly-Engaged` -> `3` (Highly Engaged)
   - Keep class 0 (`Not-Engaged`) as a priority since it is a critical minority class.
   - Filter out `SNP(Subject Not Present)` from training and verification splits.

4. **Experiment Logs**:
   - Always document your runs, hyperparameters, and resulting evaluation metrics (MSE, Class-wise MSE, PCC, Confusion Matrix) in [docs/experiments.md](docs/experiments.md), following its protocol and entry template.
   - Do not add to or cite `archive/`. It holds superseded pre-remediation material (see [archive/README.md](archive/README.md)).
