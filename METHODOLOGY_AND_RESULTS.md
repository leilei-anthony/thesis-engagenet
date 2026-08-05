---
title: Methodology and Results — Student Engagement Prediction from Video (EngageNet)
type: project
status: in-progress
area: thesis
tags: [thesis, deep-learning, computer-vision, affective-computing, engagement-detection]
updated: 2026-08-05
---

# Methodology and Results: Student Engagement Prediction from Video

## Abstract

This document is the standalone methodology-and-results reference for the EngageNet engagement-prediction thesis project, focused on the **Binary Classification, Threshold 3** task (`{0,1,2}` vs. `{3}` — "Highly-Engaged" vs. everything else), the project's headline evaluation split. It covers the dataset, temporal sampling strategies, model architectures, task and metric definitions, the Threshold 3 ablation results across five sampling methods and four models, a SMOTE oversampling ablation on the same split, and a Random Forest feature-importance analysis. The project also evaluates multi-class classification, regression, and two other binary thresholds; those results are not reproduced here — see `EXPERIMENTS.md` for the full multi-task sweep. `REFERENCES.md` is the short dataset/metric primer.

## 1. Executive Summary

- **On Threshold 3, sampling method barely matters once training is stable — model architecture matters far more.** Across `Targeted`, `3-Changepoint`, `5-Changepoint`, and `7-Changepoint` sampling, differences in accuracy/F1 for any given model are within run-to-run noise (no fixed random seed on the LSTM/MLP side), not a clean "more/fewer frames = better" trend.
- **SVM is both the most accurate and the cheapest model to train on this task.** It clusters tightly around 69% accuracy regardless of sampling method, while training in 1–6 seconds — an order of magnitude faster than LSTM/MLP and comparable to or faster than Random Forest.
- **Traditional ML (SVM, Random Forest) on simple temporally-pooled features is competitive with, or beats, the LSTM/MLP on this task** despite discarding all temporal ordering. SVM is the clear winner; Random Forest is the clear loser, with the weakest minority-class (Highly-Engaged) F1 of all four models.
- **SMOTE oversampling does not clearly help on Threshold 3** and is not recommended as the default here; the split was already close to naturally balanced, leaving little class imbalance for SMOTE to correct. Effects are small and model-dependent — see [§11](#11-smote-key-observations).
- **BOCPD and 3-Changepoint sampling load identical underlying data** (`src/dataset.py` maps both to the same `3-changepoint-*.csv` files), so their SVM/RF results are numerically identical by construction — BOCPD is therefore not tabulated as a separate row below; read `3-Changepoint` as also covering BOCPD's SVM/RF result.

## 2. Dataset

- **EngageNet**: video recordings of students during online-learning activities, labeled per-clip on a 4-point engagement scale:
  - `0` — Not-Engaged (Completely Disengaged)
  - `1` — Barely-engaged
  - `2` — Engaged
  - `3` — Highly-Engaged
  - `SNP` (Subject-Not-Present) rows are filtered out before training (`src/dataset.py` drops rows where `label == 'SNP(Subject Not Present)'`, since they carry no valid engagement score).
- **Features**: per-frame facial/behavioral descriptors — Facial Action Units (`AU_*`), raw facial-landmark coordinates (`FLM_*`), and MediaPipe pose keypoints (`MP_*`) — extracted by `scripts/feature_extraction.py`, giving a **1518-dimensional** per-frame feature vector (confirmed against `input_dim=1518` in `src/model.py`'s `EngagementLSTM`/`EngagementMLP` constructors).

## 3. Temporal Sampling Methods

Video clips are long, but only a handful of frames are typically informative (e.g. moments where a student's visible attention shifts). Rather than feeding a model every frame, this project compares several **temporal sampling strategies**, each producing a small, fixed-size subset of frames per clip, and measures how much that choice affects downstream prediction — holding the model, features, and task fixed. This is the project's central research question: *does how you select which frames to feed a temporal model matter more than the model architecture itself?*

| Method | How frames are chosen | Sequence length |
| :--- | :--- | :--- |
| **Targeted** (baseline) | Subject-Matter-Expert-selected / validly-detected frames | variable, ≤3 |
| **BOCPD** | Bayesian Online Changepoint Detection — an online Bayesian algorithm that picks the frames where the underlying signal's generative process shifts | 3 (fixed) |
| **3 / 5 / 7-Changepoint** | Same changepoint-detection idea, generalized to pick the top-*k* velocity peaks in the behavioral signal | 3, 5, or 7 |

**Implementation note**: `src/dataset.py` maps `sampling_method == 'bocpd'` to the same `3-changepoint-*.csv` files as `3-changepoint` — the two are not independent data sources. This means BOCPD and 3-Changepoint produce numerically identical results for the deterministic models (SVM, Random Forest); the LSTM/MLP columns for BOCPD instead carry only the original single-run pilot's numbers, which predate the padding-bug fix described in [§7](#7-experimental-procedure) and so aren't comparable to the rest of this document's rerun. For this reason, **BOCPD is not tabulated separately below** — its SVM/RF numbers are, by construction, identical to the `3-Changepoint` rows, and its (non-comparable, legacy) LSTM/MLP numbers are preserved in `EXPERIMENTS.md` for historical reference only. Read every `3-Changepoint` row below as also representing BOCPD's SVM/RF result.

## 4. Models

Four architectures are trained on each sampling method's output, chosen to separate "does sampling matter" from "does model choice matter":

1. **LSTM** (`EngagementLSTM` in `src/model.py`) — a sequence model native to the temporal structure. Architecture: `input_dim (1518) -> LSTM(hidden_dim=64) -> fc1 (64 -> 32) -> fc2 (32 -> num_classes or 1)`, with masked mean-pooling over the LSTM's per-timestep outputs (via the sequence-length mask) before the fully-connected head.
2. **MLP** (`EngagementMLP` in `src/model.py`) — a feed-forward network on temporally-averaged (pooled) features. Architecture: `input_dim (1518) -> fc1 (1518 -> 64) -> fc2 (64 -> 32) -> fc3 (32 -> num_classes or 1)`.
3. **SVM** — an RBF-kernel Support Vector Machine (`sklearn.svm.SVC`, `kernel='rbf'`) trained on standard-scaled, temporally average-pooled features.
4. **Random Forest** — an ensemble of 100 unpruned decision trees (`sklearn.ensemble.RandomForestClassifier`, `n_estimators=100`, `random_state=42`) trained on the same pooled features.

SVM and Random Forest are deterministic given identical input data (`random_state=42`); LSTM and MLP are trained with no fixed random seed, so their results vary run-to-run — a caveat that recurs throughout the results below (see [Limitations](#13-limitations--open-questions)).

## 5. Tasks

The project evaluates every (sampling method × model) pair on five tasks: multi-class classification, regression, and binary classification at three thresholds (`{0}` vs. `{1,2,3}`; `{0,1}` vs. `{2,3}`; `{0,1,2}` vs. `{3}`). This document reports only the third of those:

- **Binary classification, Threshold 3**: `{0,1,2}` vs. `{3}` — i.e. "Highly-Engaged" vs. everything else. This is the most conservative/hardest binary split, isolating the minority "Highly-Engaged" class against everyone else pooled — it best reflects a real use case like "flag the small number of highly-engaged students."

Multi-class classification, regression, and Thresholds 1/2 are evaluated in the same ablation sweep but are not reproduced in this document; see `EXPERIMENTS.md` for those tables.

## 6. Evaluation Metrics

Metrics reported in the Threshold 3 tables below:

- **Accuracy** — overall proportion of correct predictions.
- **Macro F1** — F1 averaged unweighted across the two classes; sensitive to minority-class performance regardless of class size.
- **Weighted F1** — F1 averaged weighted by class support; closer to overall accuracy on imbalanced data.
- **Class 0 F1 / Class 1 F1** — per-class F1 ("rest" vs. "Highly-Engaged"), to show whether accuracy gains come at the minority class's expense.
- **Pearson Correlation Coefficient (PCC)**, with p-value — linear correlation between true and predicted labels (−1 to 1).
- **Overall MSE** — mean squared error against the true (binarized) label.
- **Training Time (s)** — wall-clock time for the model-fitting step only (`model.fit()` for SVM/RF; full epoch loop for LSTM/MLP), excluding data loading and evaluation.

## 7. Experimental Procedure

An initial single-run LSTM-only pilot (preserved in full as "Runs 1–10" in `EXPERIMENTS.md`) compared `Targeted` and `BOCPD` sampling and appeared to show the LSTM collapsing to a constant-class prediction on several tasks. Investigation traced this to a bug in `src/dataset.py`: every sequence was zero-padded/truncated to a hardcoded 3 frames regardless of the sampling method actually requested, silently discarding frames 4+ for the 5- and 7-changepoint configurations. This was fixed so that sequence padding dynamically matches the changepoint count.

Following the fix, a full ablation sweep (`scripts/run_ablation_targeted_3_5_7.py`) was run: 84 train+eval subprocess calls covering `Targeted` / `3-Changepoint` / `5-Changepoint` / `7-Changepoint` sampling × LSTM / MLP / SVM / Random Forest × all 5 tasks (`BOCPD` was not part of the automated sweep — see [§3](#3-temporal-sampling-methods) for why it is not tabulated separately below). This sweep was re-run twice more: once (2026-08-03) with training-time instrumentation added to `src/train.py`, `src/train_traditional.py`, and `src/evaluate.py`; and once more (2026-08-05) as a same-session paired rerun alongside the SMOTE ablation sweep, used to refresh the SMOTE comparison in [§10](#10-smote-results). The Threshold 3 slice of both reruns is reported below; the original Run 1–10 pilot detail and the other four tasks are preserved in full in `EXPERIMENTS.md`.

## 8. Results: Binary Classification, Threshold 3

This is the most conservative/hardest binary split — it isolates the minority "Highly-Engaged" class against everyone else pooled, so it best reflects a real use case like "flag the small number of highly-engaged students."

![Binary classification (Threshold 3): accuracy and macro F1 by sampling method and model](artifacts/figures/fig3_binary_threshold3.png)

| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 (rest) | Class 1 F1 (Highly-Engaged) | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.6349 | 0.6295 | 0.6303 | 0.5846 | 0.6744 | 0.2727 (2.8e-39) | 0.3651 | 52.5 |
| **Targeted** | MLP | 0.6668 | 0.6655 | 0.6659 | 0.6443 | 0.6867 | 0.3337 (4.8e-59) | 0.3332 | 8.4 |
| **Targeted** | **SVM** | **0.6933** | **0.6921** | 0.6918 | 0.7112 | 0.6730 | 0.3933 (2.7e-83) | 0.3067 | 2.8 |
| **Targeted** | Random Forest | 0.6147 | 0.5926 | 0.5909 | 0.6875 | 0.4977 | 0.2725 (3.2e-39) | 0.3853 | 2.4 |
| **3-Changepoint** | LSTM | 0.6843 | 0.6793 | 0.6800 | 0.6389 | 0.7196 | 0.3747 (3.5e-75) | 0.3157 | 13.8 |
| **3-Changepoint** | MLP | 0.6286 | 0.6160 | 0.6173 | 0.5464 | 0.6857 | 0.2674 (9.3e-38) | 0.3714 | 9.6 |
| **3-Changepoint** | SVM | 0.6902 | 0.6879 | 0.6874 | 0.7146 | 0.6611 | 0.3910 (2.9e-82) | 0.3098 | 3.8 |
| **3-Changepoint** | Random Forest | 0.6098 | 0.5848 | 0.5830 | 0.6866 | 0.4830 | 0.2660 (2.2e-37) | 0.3902 | 2.7 |
| **5-Changepoint** | LSTM | 0.6479 | 0.6466 | 0.6462 | 0.6679 | 0.6253 | 0.3015 (2.1e-43) | 0.3521 | 16.7 |
| **5-Changepoint** | MLP | 0.6474 | 0.6472 | 0.6470 | 0.6556 | 0.6387 | 0.2968 (4.6e-42) | 0.3526 | 13.8 |
| **5-Changepoint** | **SVM** | **0.6973** | **0.6966** | 0.6963 | 0.7111 | 0.6820 | **0.3995** (1.1e-77) | 0.3027 | 3.3 |
| **5-Changepoint** | Random Forest | 0.5910 | 0.5612 | 0.5589 | 0.6756 | 0.4467 | 0.2290 (2.8e-25) | 0.4090 | 2.2 |
| **7-Changepoint** | LSTM | 0.6454 | 0.6449 | 0.6452 | 0.6322 | 0.6577 | 0.2902 (3.3e-40) | 0.3546 | 14.7 |
| **7-Changepoint** | MLP | 0.6519 | 0.6514 | 0.6511 | 0.6644 | 0.6383 | 0.3070 (5.1e-45) | 0.3481 | 12.4 |
| **7-Changepoint** | SVM | 0.6898 | 0.6884 | 0.6880 | 0.7091 | 0.6677 | 0.3871 (1.1e-72) | 0.3102 | 2.8 |
| **7-Changepoint** | Random Forest | 0.5890 | 0.5610 | 0.5588 | 0.6720 | 0.4499 | 0.2213 (1.2e-23) | 0.4110 | 2.1 |

**Takeaways:**
- **SVM wins regardless of sampling method** — top or near-top in every column, clustering tightly around **69% accuracy / 0.69 macro F1** whichever frames it's given. For this task, feature representation (pooled facial descriptors) and classifier choice dominate; frame-selection strategy is close to irrelevant.
- **Random Forest is the consistent loser** (~59–61% accuracy), with the weakest Class-1 (Highly-Engaged) F1 of all four models (0.45–0.50) — it struggles most with the minority "highly engaged" class specifically.
- **LSTM and MLP are roughly tied with each other** (~63–70%), sitting between SVM and RF — the sequence model's expected temporal advantage doesn't show up here.
- **Best single result**: 5-Changepoint SVM (69.73% accuracy / 0.6966 macro F1 / 0.3995 PCC) — but the margin over Targeted SVM (69.33%) and BOCPD/3-Changepoint/7-Changepoint SVM (~69.0%) is razor-thin, i.e. not a meaningfully different result, just noise-level variation around "SVM gets ~69% on this split no matter what."
- **SVM also wins on training time, not just accuracy**: 1.0–3.8s per run across every sampling method, vs. 8–53s for LSTM/MLP and 2–4s for RF. There is no accuracy/compute tradeoff to weigh — SVM strictly dominates on both axes for this task.
- **BOCPD and 3-Changepoint sampling load identical underlying data** (see [§3](#3-temporal-sampling-methods)), so BOCPD is omitted from the table above rather than restated as a duplicate `3-Changepoint` row; its SVM/RF results are, by construction, identical to `3-Changepoint`'s, and its LSTM/MLP numbers are the non-comparable original pilot values preserved in `EXPERIMENTS.md`.

## 9. SMOTE: Methodology

`imblearn.SMOTE` oversampling of the minority engagement classes was added to the **training split only** (never validation/test), as an alternative/complement to the existing inverse-frequency class weighting. Implemented in `src/train.py` (LSTM/MLP — sequences are flattened to `(max_seq_len × feature_dim)` vectors, with each sample's valid length appended as an extra column so it interpolates consistently with SMOTE's synthetic samples, then reshaped back) and `src/train_traditional.py` (SVM/RF — applied directly to the scaled, pooled feature vectors). `k_neighbors` is auto-capped to `min(5, smallest_class_count - 1)`. The Threshold 3 config runs with `--no_class_weights`, so the comparison below isolates the effect of SMOTE alone (not SMOTE + weighted-loss).

Full sweep script: `scripts/run_ablation_targeted_3_5_7_smote.py` — same `Targeted`/`3`/`5`/`7`-Changepoint × LSTM/MLP/SVM/RF scope as the baseline sweep (`BOCPD` was not part of either automated sweep). Raw run log: `artifacts/ablation_targeted_3_5_7_changepoint_results_smote.txt`.

**On reproducibility**: both the baseline and SMOTE sweeps were re-run end-to-end in the same session (2026-08-05, back-to-back on the same machine) specifically to produce a matched pair of runs for this comparison. SVM/RF rows are deterministic (`random_state=42` on identical pooled features) and reproduce exactly across reruns; LSTM/MLP rows differ run-to-run since no fixed seed is used.

## 10. SMOTE: Results

Threshold 3 comparison (SMOTE, `--no_class_weights`, same scope as [§8](#8-results-binary-classification-threshold-3)):

| Sampling Method | Model | Accuracy | Macro F1 | Weighted F1 | Class 0 F1 | Class 1 F1 | PCC (p-value) | Overall MSE | Training Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Targeted** | LSTM | 0.6466 | 0.6401 | 0.6410 | 0.5916 | 0.6886 | 0.2982 (5.7e-47) | 0.3534 | 10.6 |
| **Targeted** | MLP | 0.6686 | 0.6639 | 0.6647 | 0.6242 | 0.7036 | 0.3415 (6.2e-62) | 0.3314 | 9.7 |
| **Targeted** | SVM | 0.6924 | 0.6913 | 0.6909 | 0.7101 | 0.6724 | 0.3914 (2.1e-82) | 0.3076 | 2.2 |
| **Targeted** | Random Forest | 0.6017 | 0.5798 | 0.5781 | 0.6757 | 0.4840 | 0.2411 (8.2e-31) | 0.3983 | 1.5 |
| **3-Changepoint** | LSTM | 0.6538 | 0.6459 | 0.6469 | 0.5931 | 0.6987 | 0.3151 (1.6e-52) | 0.3462 | 10.1 |
| **3-Changepoint** | MLP | 0.6210 | 0.6018 | 0.6034 | 0.5144 | 0.6892 | 0.2583 (2.8e-35) | 0.3790 | 8.1 |
| **3-Changepoint** | SVM | 0.6888 | 0.6865 | 0.6860 | 0.7135 | 0.6595 | 0.3884 (4.5e-81) | 0.3112 | 2.1 |
| **3-Changepoint** | Random Forest | 0.6390 | 0.6205 | 0.6190 | 0.7042 | 0.5369 | 0.3225 (4.6e-55) | 0.3610 | 1.4 |
| **5-Changepoint** | LSTM | 0.6324 | 0.6302 | 0.6307 | 0.6014 | 0.6590 | 0.2647 (1.7e-33) | 0.3676 | 7.4 |
| **5-Changepoint** | MLP | 0.6449 | 0.6418 | 0.6412 | 0.6749 | 0.6088 | 0.3001 (5.3e-43) | 0.3551 | 8.7 |
| **5-Changepoint** | SVM | 0.6943 | 0.6936 | 0.6933 | 0.7077 | 0.6796 | 0.3932 (4.0e-75) | 0.3057 | 2.4 |
| **5-Changepoint** | Random Forest | 0.5955 | 0.5671 | 0.5649 | 0.6780 | 0.4561 | 0.2379 (3.4e-27) | 0.4045 | 1.4 |
| **7-Changepoint** | LSTM | 0.6479 | 0.6426 | 0.6435 | 0.5993 | 0.6859 | 0.2990 (1.1e-42) | 0.3521 | 12.0 |
| **7-Changepoint** | MLP | 0.6499 | 0.6499 | 0.6499 | 0.6472 | 0.6525 | 0.2999 (6.0e-43) | 0.3501 | 9.6 |
| **7-Changepoint** | SVM | 0.6873 | 0.6860 | 0.6856 | 0.7063 | 0.6656 | 0.3818 (1.4e-70) | 0.3127 | 2.1 |
| **7-Changepoint** | Random Forest | 0.6090 | 0.5855 | 0.5836 | 0.6841 | 0.4869 | 0.2620 (7.8e-33) | 0.3910 | 1.4 |

**Delta vs. baseline** (SMOTE − Baseline, averaged across the 4 sampling methods; computed by comparing the table above to [§8](#8-results-binary-classification-threshold-3)):

| Model | Δ Accuracy | Δ Macro F1 | Δ Training Time (s) | Δ Class 0 F1 | Δ Class 1 F1 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| LSTM | −0.0075 | −0.0113 | −0.94 | −0.0364 | +0.0140 |
| MLP | −0.0121 | −0.0148 | −0.95 | −0.0037 | −0.0259 |
| SVM | −0.0020 | −0.0019 | −0.39 | −0.0021 | −0.0017 |
| Random Forest | **+0.0102** | **+0.0133** | −0.64 | +0.0051 | +0.0217 |

Overall (averaged across all 16 sampling-method × model pairs): Δaccuracy −0.0028, Δmacro F1 −0.0037.

## 11. SMOTE: Key Observations

- **On Threshold 3, SMOTE's effect is small and model-dependent — not a uniform win or loss.** Averaged across sampling methods, LSTM, MLP, and SVM all lose a little accuracy (−0.008 to −0.012 for LSTM/MLP, −0.002 for SVM), while **Random Forest is the one model that gains** (+0.010 accuracy, +0.013 macro F1) — the opposite direction from SVM/RF's SMOTE losses on the other (removed-from-this-document) tasks. This split-specific reversal is a reminder that SMOTE's effect is not a fixed property of a model, but interacts with how imbalanced the particular task already is.
- **This split was already close to naturally balanced** (1093 vs. 1134 train-adjacent samples for the two classes), so there was comparatively little class imbalance for SMOTE to correct — consistent with the small magnitude of every delta above (all within ~1.5 accuracy points).
- **SVM, the best-performing model on this task, is also the most SMOTE-insensitive** (Δaccuracy −0.002, Δmacro F1 −0.002) — its already-strong Threshold 3 performance ([§8](#8-results-binary-classification-threshold-3)) is essentially unaffected either way.
- **Training time drops slightly for every model under SMOTE on this task** (−0.4 to −1.0s), the opposite of the increase typically expected from a larger (oversampled) training set — plausibly because better-balanced classes let early-stopping-sensitive models (LSTM/MLP) or tree-splitting criteria (RF) converge in fewer effective steps on this already-near-balanced split. The magnitude is small enough to be within normal run-to-run wall-clock variance.
- **Bottom line for this task**: SMOTE is not clearly harmful or helpful on Threshold 3 — effects are small, model-dependent, and plausibly explained by the split's near-balance rather than a genuine imbalance-correction mechanism. SVM remains the best choice on this task with or without SMOTE.

## 12. Random Forest Feature Importance

Since Random Forest is directly compared against the LSTM/MLP/SVM above despite discarding all temporal ordering, it's worth inspecting *which* pooled input features it actually splits on for this task. `src/train_traditional.py` does not persist the fitted sklearn model to disk, so `scripts/analyze_rf_feature_importance.py` retrains a Random Forest with identical hyperparameters (`n_estimators=100`, `random_state=42`, same `StandardScaler` + temporal-average-pooling pipeline), then reports `feature_importances_` and renders one example tree.

Config used below: **Targeted sampling, binary classification, Threshold 3** (`{0,1,2}` vs `{3}`, unweighted — matching the results table above).

![Random Forest feature importance, top 25 features (Targeted, Threshold 3)](artifacts/figures/fig5_rf_feature_importance_targeted_classification_thresh3.png)

**Top 15 features by Gini importance:**

| Rank | Feature | Importance |
| :--- | :--- | :--- |
| 1 | `AU_browOuterUpRight` | 0.0100 |
| 2 | `AU_cheekSquintLeft` | 0.0100 |
| 3 | `MP_LEFT_WRIST_v` | 0.0081 |
| 4 | `AU_browInnerUp` | 0.0071 |
| 5 | `AU_browDownRight` | 0.0058 |
| 6 | `AU_mouthUpperUpRight` | 0.0057 |
| 7 | `AU_mouthSmileRight` | 0.0050 |
| 8 | `MP_RIGHT_WRIST_y` | 0.0049 |
| 9 | `FLM_x_136` | 0.0048 |
| 10 | `FLM_x_138` | 0.0043 |
| 11 | `AU_mouthUpperUpLeft` | 0.0042 |
| 12 | `MP_LEFT_SHOULDER_v` | 0.0041 |
| 13 | `AU_mouthSmileLeft` | 0.0041 |
| 14 | `FLM_z_82` | 0.0039 |
| 15 | `AU_eyeWideRight` | 0.0037 |

**Observations:**
- **Facial Action Units (AUs) dominate over raw pose/landmark coordinates.** 10 of the top 15 features are `AU_*` (eyebrow, cheek, mouth, eye), vs. only 4 raw facial-landmark (`FLM_*`) coordinates and 3 MediaPipe pose features (`MP_*`) in the top 15. For distinguishing "Highly-Engaged" from everything else, **eyebrow movement** (`browOuterUpRight`, `browInnerUp`, `browDownRight`) and **mouth/smile activity** (`mouthUpperUp*`, `mouthSmile*`) carry the most signal — not gross body pose.
- **Wrist visibility/position sneaks into the top 10** (`MP_LEFT_WRIST_v`, `MP_RIGHT_WRIST_y`) — plausibly a proxy for hand-raising or note-taking behavior correlating with high engagement.
- No single feature dominates: the top importance is only 0.0100 out of 1517 total pooled features, so the RF's decisions are spread thin across many weakly-informative facial/pose signals rather than relying on one strong predictor.

![Example tree from the Random Forest — tree #0 of 100, display truncated to depth 3 (Targeted, Threshold 3)](artifacts/figures/fig6_rf_example_tree_targeted_classification_thresh3.png)

**Caveats on the tree figure:**
- The forest has **100 unpruned trees** (`max_depth=None`); a fully rendered tree would be thousands of nodes, so this shows only the first 3 levels of one representative tree (`estimators_[0]`), truncated for legibility — not the full decision logic.
- This single tree's top splits (`FLM_z_317`, `FLM_y_216`, `FLM_x_223` — raw landmark coordinates) don't match the *forest-wide* importance ranking above (which is AU-dominated). That's expected: importance is averaged across all 100 bootstrap-sampled trees, while any one tree's early splits reflect whatever separated its particular bootstrap sample best. Don't read this one tree as "the model's logic" — use the feature-importance chart for that.

Regenerate for another sampling method with:
```bash
conda run -n thesis-engagenet python scripts/analyze_rf_feature_importance.py \
  --sampling_method <targeted|bocpd|3-changepoint|5-changepoint|7-changepoint> \
  --mode classification --binarize_threshold 3
```

## 13. Limitations / Open Questions

- **No fixed random seed is used across LSTM/MLP training runs**; observed differences between sampling methods, and some SMOTE deltas above, are within run-to-run noise. A seeded multi-run (e.g. 5 seeds × config) would be needed to claim any ranking with confidence.
- **The lack of a clear sampling-method or LSTM-sequence-modeling effect raises the question of whether the temporally-pooled features already destroy most of the sequential signal** before it reaches any model — worth testing an LSTM on raw (unpooled, per-frame) features vs. the current setup.
- **This document reports Threshold 3 only**; the same models perform differently on the other tasks (multi-class, regression, Thresholds 1/2) — see `EXPERIMENTS.md` for the full sweep before generalizing any finding above beyond this specific split.

## 14. Reproducibility / Repo Pointers

- **Underlying lab notebook**: [EXPERIMENTS.md](EXPERIMENTS.md) — the full 5-task × 5-sampling-method × 4-model sweep, dated update notes, and the original Run 1–10 pilot in full detail.
- **Dataset / method background**: [REFERENCES.md](REFERENCES.md).
- **Ablation sweep scripts**: `scripts/run_ablation_targeted_3_5_7.py` (baseline), `scripts/run_ablation_targeted_3_5_7_smote.py` (SMOTE variant).
- **Raw run logs**: `artifacts/ablation_targeted_3_5_7_changepoint_results.txt` (baseline), `artifacts/ablation_targeted_3_5_7_changepoint_results_smote.txt` (SMOTE).
- **Figure generation**: `scripts/generate_ablation_figures.py` (fig3, plus the other task figures not used here), `scripts/generate_smote_comparison_figures.py` (fig7–8, full-task SMOTE comparison), `scripts/analyze_rf_feature_importance.py` (fig5–6) — all under `artifacts/figures/`.
- **Core implementation**: `src/dataset.py` (data loading, sampling-method mapping, sequence padding), `src/model.py` (`EngagementLSTM`, `EngagementMLP`), `src/train.py` (LSTM/MLP training, SMOTE/class-weighting), `src/train_traditional.py` (SVM/RF training), `src/evaluate.py` (evaluation/metrics).
