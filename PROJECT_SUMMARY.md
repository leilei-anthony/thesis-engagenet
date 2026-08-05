---
title: Student Engagement Prediction from Video (EngageNet)
type: project
status: in-progress
area: thesis
tags: [thesis, deep-learning, computer-vision, affective-computing, engagement-detection]
updated: 2026-08-03 (SMOTE ablation added)
---

# Student Engagement Prediction from Video (EngageNet)

## What this research is about

The project predicts a student's **engagement level** (4-point ordinal scale) from short video clips of online-learning sessions, using per-frame facial/behavioral features extracted from the [EngageNet](REFERENCES.md) dataset. The core research question is:

> **Does *how you select which video frames to feed a temporal model* matter more than the model architecture itself?**

Video clips are long, but only a handful of frames are actually informative (e.g. moments where a student's attention visibly shifts). Rather than feeding a model every frame, this project compares several **temporal sampling strategies** that each pick a small, fixed-size subset of frames per clip, then measures how much that choice affects downstream prediction quality — holding the model, features, and task fixed.

## Dataset

- **EngageNet**: video recordings of students in online-learning activities, labeled per-clip on a 4-point engagement scale:
  - `0` Not-Engaged (Completely Disengaged)
  - `1` Barely-engaged
  - `2` Engaged
  - `3` Highly-Engaged
  - (`SNP` / Subject-Not-Present rows are filtered out)
- Features are per-frame facial/behavioral descriptors (~1518-dim), extracted by `scripts/feature_extraction.py`.

## Method

**Temporal sampling strategies** (the independent variable under test) — each produces a fixed-length sequence of frames per clip:

| Method | How frames are chosen | Sequence length |
|---|---|---|
| **Targeted** | SME-selected / validly-detected frames (baseline) | variable, ≤3 |
| **BOCPD** | Bayesian Online Changepoint Detection — picks the 3 frames where the underlying signal's generative process shifts | 3 |
| **3 / 5 / 7-Changepoint** | Same changepoint-detection idea, generalized to pick the top-*k* velocity peaks in the behavioral signal | 3, 5, or 7 |

**Models trained on each sampling method's output** (four architectures, to separate "does sampling matter" from "does model choice matter"):
- **LSTM** — sequence model, native to the temporal structure
- **MLP** — feed-forward on temporally-averaged (pooled) features
- **SVM** (RBF kernel) — traditional ML, on pooled features
- **Random Forest** — traditional ML, on pooled features

**Tasks evaluated** for every (sampling method × model) pair:
1. **Multi-class classification** (all 4 engagement levels)
2. **Regression** (continuous engagement score)
3. **Binary classification** at 3 different thresholds — collapsing the 4 levels into "disengaged vs. engaged" at different cut points:
   - Threshold 1: `{0}` vs `{1,2,3}`
   - Threshold 2: `{0,1}` vs `{2,3}`
   - **Threshold 3: `{0,1,2}` vs `{3}`** — i.e. "Highly-Engaged" vs. everything else

Full run log and hyperparameters: [EXPERIMENTS.md](EXPERIMENTS.md). Ablation sweep script: `scripts/run_ablation_targeted_3_5_7.py`.

## Key insight (the headline finding)

**Sampling method barely matters once training is stable — model architecture and task framing matter far more.**

An earlier round of experiments (documented as "Run 1/2" in `EXPERIMENTS.md`) seemed to show that longer changepoint sequences (5/7 frames) dramatically rescued the LSTM from collapsing to a single predicted class, while 3-frame sequences caused it to collapse. That turned out to be **partly a bug**: `src/dataset.py` was zero-padding/truncating every sequence to a hardcoded 3 frames regardless of the sampling method actually requested, silently discarding frames 4+ for the 5- and 7-changepoint configurations. After fixing the padding logic and re-running the full sweep (84 train+eval runs across `Targeted`, `3-Changepoint`, `5-Changepoint`, `7-Changepoint` × LSTM/MLP/SVM/RF):

- The **collapse was a training-stability artifact**, not a sequence-length limitation — `Targeted` (still just 3 frames) now trains to ~49–53% multi-class accuracy on its own (varies run-to-run, no fixed seed), no longer collapsing.
- **Sequence length (3 vs 5 vs 7 changepoints) has only a modest, non-monotonic effect** on any model once training is stable — differences are within run-to-run noise (no fixed random seed), not a clean "more frames = better" trend.
- **`BOCPD` and `3-Changepoint` load identical underlying data** (`src/dataset.py` maps both to the same `3-changepoint-*.csv` files), so their SVM/RF results are numerically identical by construction — a good reminder to sanity-check "distinct" experimental conditions actually differ.
- **Traditional ML (SVM/RF) on simple temporally-pooled features is consistently competitive with, and often beats, the LSTM** across every sampling method and task. The temporal-sequence modeling advantage the LSTM was expected to provide did not clearly materialize in this dataset/feature setup.

## Latest results: Binary Classification, Threshold 3 (Highly-Engaged vs. rest)

This is the most conservative/hardest binary split — it isolates the minority "Highly-Engaged" class (`3`) against everyone else (`0,1,2` pooled), so it best reflects a real use case like "flag the small number of highly-engaged students."

![Threshold 3 binary classification: accuracy and macro F1 by sampling method and model](artifacts/figures/fig3_binary_threshold3.png)

| Sampling Method | Model | Accuracy | Macro F1 | Class 0 F1 (rest) | Class 1 F1 (Highly-Engaged) | PCC | Training Time (s) |
|---|---|---|---|---|---|---|---|
| Targeted | LSTM | 0.6349 | 0.6295 | 0.5846 | 0.6744 | 0.2727 | 52.5 |
| Targeted | MLP | 0.6668 | 0.6655 | 0.6443 | 0.6867 | 0.3337 | 8.4 |
| Targeted | **SVM** | **0.6933** | **0.6921** | 0.7112 | 0.6730 | 0.3933 | 2.8 |
| Targeted | Random Forest | 0.6147 | 0.5926 | 0.6875 | 0.4977 | 0.2725 | 2.4 |
| BOCPD | LSTM | 0.6533 | 0.6487 | 0.6081 | 0.6892 | 0.3099 | N/A (legacy run) |
| BOCPD | MLP | 0.6960 | 0.6910 | 0.6519 | 0.7302 | 0.3989 | N/A (legacy run) |
| BOCPD | SVM | 0.6902 | 0.6879 | 0.7146 | 0.6611 | 0.3910 | 3.8 |
| BOCPD | Random Forest | 0.6098 | 0.5848 | 0.6866 | 0.4830 | 0.2660 | 2.7 |
| 3-Changepoint | LSTM | 0.6843 | 0.6793 | 0.6389 | 0.7196 | 0.3747 | 13.8 |
| 3-Changepoint | MLP | 0.6286 | 0.6160 | 0.5464 | 0.6857 | 0.2674 | 9.6 |
| 3-Changepoint | SVM | 0.6902 | 0.6879 | 0.7146 | 0.6611 | 0.3910 | 3.8 |
| 3-Changepoint | Random Forest | 0.6098 | 0.5848 | 0.6866 | 0.4830 | 0.2660 | 2.7 |
| 5-Changepoint | LSTM | 0.6479 | 0.6466 | 0.6679 | 0.6253 | 0.3015 | 16.7 |
| 5-Changepoint | MLP | 0.6474 | 0.6472 | 0.6556 | 0.6387 | 0.2968 | 13.8 |
| 5-Changepoint | **SVM** | **0.6973** | **0.6966** | 0.7111 | 0.6820 | **0.3995** | 3.3 |
| 5-Changepoint | Random Forest | 0.5910 | 0.5612 | 0.6756 | 0.4467 | 0.2290 | 2.2 |
| 7-Changepoint | LSTM | 0.6454 | 0.6449 | 0.6322 | 0.6577 | 0.2902 | 14.7 |
| 7-Changepoint | MLP | 0.6519 | 0.6514 | 0.6644 | 0.6383 | 0.3070 | 12.4 |
| 7-Changepoint | SVM | 0.6898 | 0.6884 | 0.7091 | 0.6677 | 0.3871 | 2.8 |
| 7-Changepoint | Random Forest | 0.5890 | 0.5610 | 0.6720 | 0.4499 | 0.2213 | 2.1 |

**Threshold-3-specific takeaways:**
- **SVM wins regardless of sampling method** — it's the top or near-top model in every column, clustering tightly around **69% accuracy / 0.69 macro F1**, whichever frames it's given. This is the strongest single signal in the ablation: for this task, *feature representation (pooled facial descriptors) and classifier choice dominate; frame-selection strategy is close to irrelevant.*
- **Random Forest is the consistent loser** (~59–61% accuracy), and its Class-1 (Highly-Engaged) F1 is the weakest of all four models (0.45–0.50) — it struggles most with the minority "highly engaged" class specifically, even though it does comparatively better on the other 4 threshold splits.
- **LSTM and MLP are roughly tied with each other** (~63–70%) and sit between SVM and RF — the sequence model's temporal advantage doesn't show up here either.
- **Best single result**: 5-Changepoint SVM, 69.73% accuracy / 0.6966 macro F1 / 0.3995 PCC — but it's a razor-thin margin over Targeted SVM (69.33%) and BOCPD/3-Changepoint/7-Changepoint SVM (~69.0%), i.e. not a meaningfully different result, just noise-level variation around "SVM gets ~69% on this split no matter what."
- **SVM also wins on training time, not just accuracy**: 1.0–3.8s per run across every sampling method, vs. 8–53s for LSTM/MLP and 2–4s for RF on this task. Combined with its accuracy lead, SVM strictly dominates on this dataset — there's no accuracy/compute tradeoff to weigh, it's simply the better choice on both axes. Full training-time breakdown (all 5 tasks, all models) is in `EXPERIMENTS.md`.

## SMOTE: does oversampling help?

Tested `SMOTE` (`--use_smote` on `src/train.py` / `src/train_traditional.py`) as an alternative/complement to the existing class-weighted loss, re-running the full `Targeted`/`3`/`5`/`7`-Changepoint × LSTM/MLP/SVM/RF sweep with it enabled. **Verdict: it doesn't help here.** Averaged across all sampling methods and classification tasks, accuracy moves *down* by 0.1–2.8 points and macro F1 is roughly a wash — the existing class-weighted loss was already doing the useful work. SVM and Random Forest (the two strongest, cheapest models) lose the most accuracy from it (−2.4 / −3.0 points avg). The one clear win: the truly under-weighted minority class ("Barely-engaged," which gets no explicit loss boost) gains +0.045 F1 — but that comes at the cost of the class that *does* already get a loss-weight boost ("Not-Engaged," −0.013 F1), suggesting SMOTE and the existing class-weighting partly fight each other rather than compound. Full breakdown, per-model deltas, and figures: `EXPERIMENTS.md` → "SMOTE Ablation Comparison".

## Open questions / next steps

- The lack of a clear sampling-method or LSTM-sequence-modeling effect raises the question of whether the temporally-pooled features already destroy most of the sequential signal before it reaches any model — worth testing an LSTM on raw (unpooled, per-frame) features vs. the current setup.
- No fixed random seed is used across training runs; observed differences between sampling methods are within run-to-run noise, so a seeded multi-run (e.g. 5 seeds × config) would be needed to claim any ranking with confidence.
- Threshold 1 (`{0}` vs `{1,2,3}`) showed the highest absolute accuracy across the board (~83–87%) — worth investigating whether that's a genuinely easier decision boundary or an artifact of class imbalance (Class 0 is the rare class there too).

## Repo pointers

- Full experiment log & hyperparameters: [EXPERIMENTS.md](EXPERIMENTS.md)
- Methodology / dataset / metric definitions: [REFERENCES.md](REFERENCES.md)
- Ablation sweep script: `scripts/run_ablation_targeted_3_5_7.py` (SMOTE variant: `scripts/run_ablation_targeted_3_5_7_smote.py`)
- Raw run output: `artifacts/ablation_targeted_3_5_7_changepoint_results.txt` (SMOTE: `..._smote.txt`)
- Figures: `artifacts/figures/` (generated by `scripts/generate_ablation_figures.py` and `scripts/generate_smote_comparison_figures.py`)
- Dataset loading logic: `src/dataset.py`
