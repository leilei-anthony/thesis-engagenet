# Agent Guidelines - Thesis EngageNet Project

Welcome to the `thesis-engagenet` workspace! This file contains development guidelines and architecture patterns to ensure consistency when working on the deep learning training pipeline.

## Core Guidelines

1. **Environment Consistency**:
   - Always run commands and python scripts using the `thesis-engagenet` conda environment:
     ```bash
     conda run -n thesis-engagenet python <script.py>
     ```

2. **Dataset Swapping**:
   - Keep dataset loading modular. Use the `sampling_method` parameter to distinguish between Method A (`targeted`) and Method B (`bocpd`).
   - Do not hardcode paths or sampling-specific logic in the training loop. All data preprocessing should be contained within `dataset.py`.

3. **Label Handling**:
   - Correctly map the labels:
     - `Not-Engaged` -> `0` (Completely Disengaged)
     - `Barely-engaged` -> `1` (Barely Engaged)
     - `Engaged` -> `2` (Engaged)
     - `Highly-Engaged` -> `3` (Highly Engaged)
   - Keep class 0 (`Not-Engaged`) as a priority since it is a critical minority class.
   - Filter out `SNP(Subject Not Present)` from training and verification splits.

4. **Experiment Logs**:
   - Always document your runs, hyperparameters, and resulting evaluation metrics (MSE, Class-wise MSE, PCC, Confusion Matrix) in [EXPERIMENTS.md](file:///Users/lei/Desktop/repos/thesis-engagenet/EXPERIMENTS.md).
