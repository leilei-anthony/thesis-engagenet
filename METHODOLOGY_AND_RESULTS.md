---
title: Methodology and Results — Student Engagement Prediction from Video (EngageNet)
type: project
status: in-progress
area: thesis
tags: [thesis, deep-learning, computer-vision, affective-computing, engagement-detection]
updated: 2026-08-06
supersedes: 2026-08-05 revision (see §6)
---

# Sampling Strategy or Architecture? A Controlled Ablation of Temporal Frame Selection for Engagement Detection

## Abstract

Temporal frame selection is treated as an unreported preprocessing detail in most engagement-detection work, yet every system makes such a choice. This study isolates its effect by crossing four sampling strategies (Start-Middle-End, and content-aware *k*-changepoint for *k* = 3, 5, 7) with four architectures (LSTM, MLP, SVM, Random Forest) on the EngageNet dataset, holding features, partition, and task fixed. Evaluation uses the Threshold 3 binarization (`{0,1,2}` vs `{3}`), a subject-independent split, seeded neural runs, and paired McNemar significance testing. The findings show that architecture dominates: 19 of 24 architecture comparisons are significant against 4 of 12 sampling comparisons, and architecture accounts for 8.9–12.0 accuracy points of spread against 1.0–4.8 for sampling. Content-aware sampling nevertheless produces two effects the prior revision missed. First, the benefit is **capacity-dependent** — Random Forest, the weakest model, is the only one where sampling significantly matters (+4.79 pts, *p*<0.001), while SVM, the strongest, gains least. Second, 3-changepoint sampling reduces LSTM seed variance six-fold, buying reproducibility where it does not buy accuracy. A readout ablation further shows the LSTM's apparent lack of temporal advantage is partly an aggregation artefact: replacing mean-pooling with attention gains 2.04 points. This revision supersedes the 2026-08-05 results, which were computed across mismatched evaluation sets (§6).

**Keywords:** Engagement Detection, Temporal Sampling, Changepoint Detection, Ablation Study, Reproducibility, EngageNet.

## 1. Summary of Findings

1. **Architecture dominates sampling.** 19/24 architecture comparisons significant vs 4/12 sampling comparisons; spread of 8.9–12.0 pts vs 1.0–4.8 pts.
2. **Ordering is SVM > {LSTM ≈ MLP} > Random Forest.** LSTM and MLP are never distinguishable in any condition — the sequence model never beats a feed-forward net seeing only a temporal average.
3. **SVM is both most accurate and cheapest** (0.6848–0.7017 accuracy, 2.5–2.7 s training). No accuracy/compute trade-off exists on this task.
4. **All four architectures peak at 3-changepoint**, but only Random Forest reaches significance. The benefit is capacity-dependent.
5. **More frames hurt.** Every architecture declines from *k*=3 to *k*=7; monotonically and noise-free for the deterministic models.
6. **3-changepoint sampling stabilises training.** LSTM seed SD falls from 0.0129 (SME) to 0.0022 — a six-fold reduction.
7. **The LSTM readout is a bottleneck.** Attention gains 2.04 pts over mean-pooling in all four conditions; `last` is worse than both.
8. **SMOTE has no material effect.** The split is already near-balanced.
9. **BOCPD is not evaluated.** It was never implemented (§3.4.1).

## 2. Dataset and Preprocessing

This study uses **EngageNet** [Singh et al., 2023], comprising short video clips of students in online-learning activities, annotated per clip on a 4-point engagement scale (0 Not-Engaged, 1 Barely-engaged, 2 Engaged, 3 Highly-Engaged). `SNP` (Subject-Not-Present) rows carry no valid score and are dropped.

**Features.** Per-frame descriptors comprise Facial Action Units (`AU_*`), facial-landmark coordinates (`FLM_*`), and MediaPipe pose keypoints (`MP_*`), giving a **1518-dimensional** vector per frame. Feature columns are selected positionally, so the loader now asserts this dimensionality; a schema change would otherwise shift the window silently.

**Partition.** The official EngageNet split is used without re-partitioning. It is **subject-independent** — `person_id` sets are disjoint across all three splits, verified directly. This excludes the failure mode in which a model identifies individual students rather than engagement states.

*Table 1: Partition, before and after the common-subset restriction (§3.4.2).*

| Split | Subjects | Videos (raw) | Videos (restricted) |
| :--- | ---: | ---: | ---: |
| Train | 32 | 2,825 | **2,719** |
| Validation | 11 | 1,068 | **867** |
| Test | 26 | 2,227 | **2,005** |

Under Threshold 3 the restricted training split is **1,375 negative / 1,344 positive** — near-balanced, which bears directly on the SMOTE result (§4.5).

## 3. Methodology

### 3.1 Temporal Sampling Strategies

Each strategy retains a small fixed-size subset of frames per clip. The manipulated variable is *how* frames are chosen — by position or by content.

*Table 2: Sampling strategies.*

| Strategy | Selection rule | Frames |
| :--- | :--- | :--- |
| **SME** (baseline) | Start-Middle-End: first, middle, last valid frame | 3 |
| **3/5/7-Changepoint** | Top-*k* landmark-velocity peaks, restored to temporal order | 3, 5, 7 |

SME is the sparse-uniform control, following the Start-Middle-End strategy used in prior work; the changepoint conditions are its content-aware counterpart. Both sample sparsely, so the contrast isolates *position-based vs content-based* selection.

Sequences are zero-padded at the tail with a per-sample valid length for masking. Rows are now explicitly sorted by `(video, frame_id)` before grouping; previously temporal order held only because of CSV row order, which nothing enforced.

### 3.2 Models

*Table 3: Architectures. All use default hyperparameters; no search was performed.*

| Model | Input | Configuration |
| :--- | :--- | :--- |
| LSTM | Ordered sequence | `1518 → LSTM(64) → 32 → out`; readout ∈ {mean, last, attention} |
| MLP | Pooled | `1518 → 64 → 32 → out` (dimensions matched to LSTM as its non-sequential control) |
| SVM | Pooled | RBF kernel, standard-scaled |
| Random Forest | Pooled | 100 unpruned trees |

Neural training uses AdamW (lr 1e-3, weight decay 1e-4), batch 64, ≤20 epochs, early stopping (patience 10), `ReduceLROnPlateau`, unweighted cross-entropy. **Comparisons are between architectures at defaults, not at their respective best-tuned settings.**

**Determinism.** SVM and Random Forest are deterministic (`random_state=42`). The neural models previously seeded nothing — fatal for an ablation with sub-point effects. All runs are now seeded (Python, NumPy, torch, DataLoader generator); two seed-42 runs give bit-identical losses, seed 43 diverges. **LSTM and MLP are reported as mean ± SD over seeds 42–46.** Because SVM and RF carry no training noise, their sampling comparisons are noise-free measurements rather than single draws.

### 3.3 Task, Metrics, and Significance Testing

Five task formulations exist; **this document reports Threshold 3 only** (`{0,1,2}` vs `{3}`), which isolates the minority Highly-Engaged class and corresponds to the realistic deployment question. The other four have not been re-run under the corrected protocol and are not comparable.

Metrics: accuracy, macro/weighted F1, per-class F1, PCC, MSE, training time.

The PCC *p*-values test correlation with ground truth, **not** differences between conditions. Since the common-subset restriction guarantees identical evaluation clips, predictions are paired per clip and **exact McNemar** applies. Two families are tested — sampling vs SME within each architecture, and architecture pairs within each sampling condition — with Holm-Bonferroni correction within family and 95% paired-bootstrap CIs on accuracy differences.

*Caveat:* McNemar operates on one prediction set, so neural tests use seed-42 predictions and inherit that draw. §4.2 shows this mattering.

### 3.4 Two Corrections to the Experimental Setup

Both were found by auditing the code against the prior revision's claims.

#### 3.4.1 BOCPD was never implemented

The prior revision listed BOCPD as a condition and noted the loader mapped it to the `3-changepoint` files. The deeper problem is that **no BOCPD implementation exists in the project**. The extraction pipeline offers exactly two modes — SME and top-*k* velocity peaks — with no run-length posterior, hazard function, or any component of the Adams–MacKay algorithm. Every figure previously reported as BOCPD was 3-changepoint data under a different label.

BOCPD is dropped and the loader now raises on the identifier. Re-instating it requires implementing the algorithm and re-extracting from source video, which is no longer available locally.

#### 3.4.2 The Evaluation-Set Confound

Extraction skips a clip when it has fewer valid frames than the requested changepoint count. The conditions therefore covered different videos: SME and 3-changepoint scored **2,227** test clips, while 5- and 7-changepoint scored **2,005** — a strict subset.

Every sampling comparison in the prior revision consequently conflated the sampling effect with test-set composition. The discrepancy is not random: the 222 excluded clips are those with the fewest detectable behavioural transitions, plausibly correlated with engagement level.

All conditions are now restricted to the intersection (2,719 train / 2,005 test), applied to training as well as evaluation. This yields the clean statement that **every condition is trained and evaluated on identical clips, differing only in which frames were sampled.** Regression tests assert the conditions yield identical video sets, not merely equal-sized ones.

## 4. Results and Discussion

### 4.1 Main Results

*Table 4: Threshold 3, baseline (no SMOTE), n = 2,005. LSTM/MLP are mean ± SD over five seeds; SVM/RF exact.*

| Sampling | Model | Accuracy | Macro F1 | Class 0 F1 | Class 1 F1 | PCC | MSE | Train (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SME** | LSTM | 0.6480 ± 0.0129 | 0.6475 | 0.6526 | 0.6424 | 0.2983 | 0.3520 | 10.4 |
| **SME** | MLP | 0.6509 ± 0.0096 | 0.6497 | 0.6485 | 0.6508 | 0.3042 | 0.3491 | 9.3 |
| **SME** | SVM | 0.6848 | 0.6838 | 0.7013 | 0.6663 | 0.3754 | 0.3152 | 2.6 |
| **SME** | RF | 0.5651 | 0.5307 | 0.6578 | 0.4036 | 0.1705 | 0.4349 | 1.8 |
| **3-CP** | LSTM | 0.6553 ± 0.0022 | 0.6548 | 0.6511 | 0.6585 | 0.3113 | 0.3447 | 10.6 |
| **3-CP** | MLP | 0.6630 ± 0.0047 | 0.6617 | 0.6450 | 0.6784 | 0.3267 | 0.3370 | 9.2 |
| **3-CP** | **SVM** | **0.7017** | **0.7010** | **0.7163** | **0.6856** | **0.4090** | **0.2983** | 2.7 |
| **3-CP** | RF | 0.6130 | 0.5904 | 0.6866 | 0.4941 | 0.2700 | 0.3870 | 3.0 |
| **5-CP** | LSTM | 0.6454 ± 0.0077 | 0.6413 | 0.6143 | 0.6683 | 0.2945 | 0.3546 | 13.0 |
| **5-CP** | MLP | 0.6491 ± 0.0045 | 0.6471 | 0.6333 | 0.6609 | 0.3001 | 0.3509 | 9.7 |
| **5-CP** | SVM | 0.6973 | 0.6966 | 0.7111 | 0.6820 | 0.3995 | 0.3027 | 2.5 |
| **5-CP** | RF | 0.5910 | 0.5612 | 0.6756 | 0.4467 | 0.2290 | 0.4090 | 2.0 |
| **7-CP** | LSTM | 0.6520 ± 0.0080 | 0.6494 | 0.6336 | 0.6652 | 0.3068 | 0.3480 | 11.2 |
| **7-CP** | MLP | 0.6466 ± 0.0121 | 0.6445 | 0.6299 | 0.6591 | 0.2950 | 0.3534 | 9.8 |
| **7-CP** | SVM | 0.6898 | 0.6884 | 0.7091 | 0.6677 | 0.3871 | 0.3102 | 2.6 |
| **7-CP** | RF | 0.5890 | 0.5610 | 0.6720 | 0.4499 | 0.2213 | 0.4110 | 2.1 |

Best cell: **3-Changepoint SVM (0.7017)**. Every architecture attains its best accuracy under 3-changepoint sampling, without exception.

### 4.2 Sampling: A Capacity-Dependent Effect

*Table 5: Sampling comparisons vs SME. Positive = changepoint better. ✓ = significant after Holm-Bonferroni.*

| Model | 3-CP | 5-CP | 7-CP |
| :--- | :--- | :--- | :--- |
| **RF** | **+4.79, *p*<0.001 ✓** | **+2.59, *p*=0.004 ✓** | **+2.39, *p*=0.004 ✓** |
| SVM | +1.70, *p*=0.082 | +1.25, *p*=0.209 | +0.50, *p*=0.558 |
| MLP | +1.05, *p*=0.413 | −0.45, *p*=0.611 | −1.65, *p*=0.233 |
| LSTM | −0.15, *p*=0.890 | −2.49, *p*=0.011 ✓† | −0.60, *p*=0.751 |

**† The one neural "significant" result is a seed artefact.** The LSTM SME−5CP difference reverses sign across seeds: +0.0249, +0.0219, −0.0080, −0.0135, −0.0125. Seed 42 — the seed McNemar used — is the most extreme draw, and the effect is negative in three of five seeds. Across seeds the means differ by 0.26 pts. Discounting it, **only Random Forest shows a genuine sampling effect.**

Two findings follow.

1. **Capacity-Dependent Benefit:** Random Forest, the weakest architecture, is the only model where frame selection significantly matters. SVM, the strongest, gains least and does not survive correction (its CI [−0.031, −0.003] excludes zero, so the effect is probably real but small). Better frame selection appears to help most where the classifier is least able to compensate for uninformative frames.
2. **More Frames Hurt:** All architectures decline from *k*=3 to *k*=7 (SVM −1.19 pts, RF −2.40 pts, both monotonic and noise-free). Frames 4–7 are by construction weaker velocity peaks, so more likely to capture blinks or camera jitter than engagement-relevant transitions.

### 4.3 The Variance Dividend

Sampling strategy affects *reproducibility* even where it barely affects accuracy.

*Table 6: LSTM accuracy SD across five seeds.*

| Sampling | Accuracy SD |
| :--- | ---: |
| SME | 0.0129 |
| 3-Changepoint | **0.0022** |
| 5-Changepoint | 0.0077 |
| 7-Changepoint | 0.0080 |

3-changepoint sampling reduces LSTM seed variance **six-fold** relative to SME (MLP: 0.0047 vs 0.0096, roughly two-fold). Content-aware frame selection buys stability where it does not buy accuracy — a practically useful result independent of the accuracy question, and one invisible without seeded runs.

### 4.4 Architecture Dominates

*Table 7: Accuracy spread across architectures, per sampling condition.*

| Sampling | Worst | Best | Spread |
| :--- | :--- | :--- | ---: |
| SME | 0.5651 (RF) | 0.6848 (SVM) | **11.97 pts** |
| 3-CP | 0.6130 (RF) | 0.7017 (SVM) | 8.87 pts |
| 5-CP | 0.5910 (RF) | 0.6973 (SVM) | 10.63 pts |
| 7-CP | 0.5890 (RF) | 0.6898 (SVM) | 10.08 pts |

**19 of 24 architecture comparisons are significant**, against 4 of 12 sampling comparisons. Against sampling spreads of 0.99–4.79 pts, the architecture effect is roughly two to twelve times larger.

Four of the five non-significant pairs are **LSTM vs MLP** — indistinguishable in every sampling condition. The ordering is **SVM > {LSTM ≈ MLP} > RF**, with SVM ahead of RF by 8.9–12.0 pts throughout (*p*<0.001).

Two observations:

1. **RF's deficit is minority-specific.** Class 1 F1 of 0.4036–0.4941 against Class 0 F1 of 0.6578–0.6866. It is weak precisely at the class the task exists to detect, and since the split is near-balanced this is not an imbalance artefact.
2. **No accuracy/compute trade-off.** SVM trains in 2.5–2.7 s against 10.4–13.0 s for the LSTM, while being more accurate in every condition. The sequence model's additional cost purchases nothing measurable.

### 4.5 The Readout Bottleneck

The LSTM receives the full ordered sequence but mean-pools its hidden states across timesteps — an aggregation that is permutation-invariant, discarding much of the ordering the recurrence encodes. This ablation replaces it with two order-sensitive alternatives.

*Table 8: LSTM readout, mean accuracy over four sampling conditions × five seeds (n = 20 each).*

| Readout | Accuracy | SD | Macro F1 |
| :--- | ---: | ---: | ---: |
| **Attention** | **0.6706** | 0.0130 | 0.6691 |
| Mean (default) | 0.6502 | 0.0088 | 0.6482 |
| Last | 0.6430 | 0.0090 | 0.6421 |

**Attention beats mean-pooling in all four sampling conditions** (+2.04 pts overall; +3.16 under SME). The LSTM's apparent lack of temporal advantage is therefore **partly an aggregation artefact, not purely an architectural finding** — mean-pooling was handicapping it.

The effect does not overturn §4.4, however. Attention-LSTM under SME (0.6796) nearly matches SVM (0.6848), but under 3-changepoint it reaches only 0.6685 against SVM's 0.7017. **The readout was a real bottleneck; removing it narrows the gap without closing it.**

`last` performing *worse* than mean is consistent with the short sequences here: with 3–7 timesteps, the final hidden state alone discards information that averaging retains, whereas learned attention recovers it selectively.

### 4.6 SMOTE

SMOTE is applied to the training split only, with `k_neighbors` capped at `min(5, smallest_class − 1)`. Deltas are computed from **matched pairs** — both arms from one session, paired on (sampling, model, seed).

*Table 9: SMOTE − baseline.*

| Model | Δ Accuracy | Δ Macro F1 | Δ Class 1 F1 | Basis |
| :--- | ---: | ---: | ---: | :--- |
| LSTM | −0.0032 ± 0.0150 | −0.0032 | +0.0001 | 5 seeds |
| MLP | −0.0013 ± 0.0111 | −0.0010 | −0.0049 | 5 seeds |
| SVM | −0.0001 | −0.0000 | +0.0012 | exact |
| RF | +0.0056 | +0.0068 | +0.0099 | exact |

**SMOTE has no material effect.** SVM is unchanged to four decimal places; RF gains half a point; both neural means are an order of magnitude smaller than their own spread. The split is already near-balanced (1,375 vs 1,344), so little imbalance exists to correct. SMOTE is not recommended as a default here.

### 4.7 Random Forest Feature Importance

Random Forest discards temporal ordering entirely, so it is worth inspecting which pooled features it splits on. A forest with identical hyperparameters was retrained on the restricted subset.

*Table 10: Top 10 features by Gini importance, Threshold 3.*

| Rank | 3-Changepoint | | SME | |
| ---: | :--- | ---: | :--- | ---: |
| 1 | `AU_browOuterUpRight` | 0.0149 | `AU_browOuterUpRight` | 0.0127 |
| 2 | `MP_LEFT_WRIST_v` | 0.0106 | `AU_browInnerUp` | 0.0109 |
| 3 | `AU_browInnerUp` | 0.0090 | `MP_LEFT_WRIST_v` | 0.0074 |
| 4 | `MP_LEFT_HIP_v` | 0.0077 | `AU_cheekSquintLeft` | 0.0054 |
| 5 | `MP_RIGHT_WRIST_y` | 0.0063 | `FLM_x_138` | 0.0048 |
| 6 | `MP_LEFT_SHOULDER_v` | 0.0049 | `AU_browDownRight` | 0.0047 |
| 7 | `AU_cheekSquintLeft` | 0.0049 | `MP_LEFT_HIP_v` | 0.0047 |
| 8 | `AU_jawRight` | 0.0049 | `AU_mouthSmileLeft` | 0.0044 |
| 9 | `FLM_z_271` | 0.0044 | `MP_RIGHT_WRIST_y` | 0.0043 |
| 10 | `MP_RIGHT_ELBOW_z` | 0.0044 | `MP_LEFT_SHOULDER_v` | 0.0041 |

Three observations:

1. **Brow movement is the strongest single signal.** `AU_browOuterUpRight` ranks first under both sampling strategies, with `AU_browInnerUp` in the top three of both.
2. **Wrist visibility ranks unexpectedly high** (`MP_LEFT_WRIST_v`, 2nd and 3rd), plausibly proxying hand-raising or note-taking. This is an interpretation, not a validated finding; distinguishing genuine behavioural signal from a detector artefact such as camera framing would require dedicated analysis.
3. **Importance is diffuse.** The top feature carries ~22× its uniform share (1/1518) and the top 15 about 9%, so decisions rest on broad accumulation of weak signals rather than a few strong predictors.

The prior revision reported AU features dominating 10-of-15. On the restricted subset the mix is more even (6 AU / 5 pose / 4 landmark under SME; 5/5/5 under 3-changepoint). **The AU-dominance claim is weakened**, though the brow-specific finding survives.

## 5. Limitations

1. **Single partition.** One accuracy point ≈ 20 clips. The paired tests address clip-level variance but not subject-level; a different 26-subject test set could shift absolute accuracies.
2. **Threshold 3 only.** The other four task formulations have not been re-run under the corrected protocol; whether the sampling effect is task-dependent remains unanswered, and their existing numbers must not be cited alongside these.
3. **BOCPD unevaluated** (§3.4.1).
4. **No hyperparameter search.** A tuned LSTM might narrow the gap to the SVM further; no upper bound is established for any architecture.
5. **Neural significance tests are single-seed**, which §4.2 shows mattering. Per-seed McNemar with aggregation would be more robust.
6. **Sampling conclusions may be capacity-dependent** (§4.2). A model weaker than those tested might depend on frame selection considerably more.

## 6. Superseded Findings

*Table 11: Changes from the 2026-08-05 revision.*

| Prior claim | Status |
| :--- | :--- |
| BOCPD is a sampling condition | **Retracted.** Never implemented (§3.4.1) |
| Targeted = "Subject-Matter-Expert-selected" | **Corrected.** SME denotes *Start-Middle-End* — first/middle/last frame. The method was right; the expansion was wrong |
| All result tables | **Superseded.** Computed across mismatched evaluation sets (§3.4.2) |
| Best result: 5-CP SVM (0.6973) | **Superseded.** Now 3-CP SVM (0.7017) |
| "SVM clusters tightly around 69% whichever frames it's given" | **Refined.** 0.6848–0.7017; the 3-CP advantage is borderline (*p*=0.082), not clearly null |
| "RF declines monotonically with more frames" | **Retracted.** An artefact of the test-set boundary; RF's worst condition is SME |
| SMOTE deltas (LSTM −0.0075, MLP −0.0121) | **Superseded.** Unreproducible from their own tables; now −0.0032 / −0.0013 from matched pairs |
| "Sampling differences are within run-to-run noise" | **Partly false.** RF shows a genuine, significant effect (§4.2) |
| "AUs dominate feature importance 10-of-15" | **Weakened.** Mix is more even on the restricted subset (§4.7) |
| "No fixed random seed" (limitation) | **Resolved.** Seeded; five seeds (§3.2) |
| "Test LSTM on unpooled features" (open question) | **Reframed and answered.** The LSTM already receives unpooled input; the order-insensitive step is the readout, and replacing it gains 2.04 pts (§4.5) |

**Claims that survived unchanged:** architecture matters more than sampling; SVM is both most accurate and cheapest; LSTM shows no temporal advantage over MLP; SMOTE does not help; RF is weakest, especially on the minority class. All are now supported by significance testing rather than inspection.

## 7. Reproducibility

- **Sweep driver:** `scripts/run_ablation_threshold3.py` (parameterised; replaces the duplicated baseline/SMOTE script pair).
- **Analysis:** `scripts/summarize_threshold3.py`, `scripts/significance_tests.py`, `scripts/smote_delta.py`, `scripts/analyze_rf_feature_importance.py`.
- **Results:** `artifacts/ablation_threshold3_{common,seeds,readout}.txt`, with `*_manifest.jsonl` and `predictions_threshold3_*/` dumps.
- **Tests:** `tests/test_dataset_integrity.py` — 14 regression tests, one per defect found. `conda run -n thesis-engagenet python -m pytest tests/ -v`
- **Implementation:** `src/dataset.py` (restriction, ordering, padding), `src/model.py` (readouts), `src/train.py` (seeding, SMOTE), `src/train_traditional.py`, `src/evaluate.py`.
- **Environment:** Apple M1 (8 cores, 8 GB), macOS 26.5.2, PyTorch 2.5.1, Python 3.10.20, scikit-learn 1.7.2.
- **Prior revision:** preserved at commit `f0d514a`.
- **Not re-run under the corrected protocol:** `EXPERIMENTS.md` — do not cite alongside this document.
