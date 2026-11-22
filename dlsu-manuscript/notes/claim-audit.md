# Claim Audit: ICCE Paper and Methodology Doc

This audit addresses panel revision R4: tone down conclusions the data doesn't support.

It checks every conclusion in `paper/paper.tex` (P) and `docs/methodology-and-results.md` (D) against the evidence. **Only the approved revised wording may appear in the thesis manuscript.**

- **"Table 1"** is the paper's main results table, with macro F1 and accuracy for 16 configurations.
- **"Table 2"** is the paper's McNemar comparison against SME (accuracy difference in points, Holm-corrected *p*).

**Verdicts:**
- **Error:** a factual or arithmetic mistake. Fix it everywhere, including the ICCE camera-ready if still possible.
- **Overstated:** the direction is right, but the wording goes beyond the evidence. Narrow it.
- **Unsupported:** there's no evidence for it in this study. Remove it, or state it as a hypothesis.
- **Supported:** keep as written.

**How to review:** mark each item `Approve` or `Change: <your note>`.

---

## Part A: Errors (fix first; most are also in the submitted ICCE paper)

**E1. "the SVM gains least"**
- **Where:** P l.192, P l.209; D §1 item 4, D §4.2 item 1.
- **Evidence:** Table 2, gains under 3-CP, from the seed-42 predictions used for McNemar: RF +4.79, **SVM +1.70**, MLP +1.05, LSTM −0.15. The five-seed mean accuracy gains are RF +4.79, SVM +1.69, MLP +1.21, LSTM +0.73.
- **Problem:** SVM gains the *second most*. The gain does not follow model strength. SVM is the strongest model and gains second most, while LSTM and MLP sit in the middle and gain least. The only part that holds is that RF, the weakest, gains most.
- **Revised:** "The gain from 3-Changepoint over SME was largest for Random Forest (+4.79 points, the only significant result) and smaller for SVM (+1.70), MLP (+1.05), and LSTM (−0.15)."
- **Decision:**

**E2. "a 7.8% increase" in extraction time for 7-CP**
- **Where:** P l.200.
- **Evidence:** Mean per-clip extraction time was 6.04 s (3-CP) and 6.22 s (SME), against 8.36 s (7-CP). That is **+34% to +38%**.
- **Cause:** The 7.8% came from averages that included one video with corrupted metadata (`subject_102`, about 150 s per run). Excluding it gives the per-clip numbers above.
- **Also:** The timing table survives only in the pre-remediation log, and the raw log `artifacts/feature_extraction_timing_sample.txt` is missing. Re-run `scripts/extraction/benchmark_feature_extraction_time.py` before the thesis reports any timing, and log the run in `docs/experiments.md`. The benchmark used 10 convenience-sample videos, so report it as indicative.
- **Revised:** "On a 10-video sample, 7-Changepoint extraction took about 35% longer per clip than SME or 3-Changepoint (8.4 s vs 6.0–6.2 s)." Use the re-run numbers once available.
- **Decision:**

**E3. "re-inference adding about 0.9 s per selected frame"**
- **Where:** P l.200.
- **Evidence:** Final-pass time rose from 1.41–1.54 s (3 frames) to 3.44 s (7 frames), which is **about 0.5 s per extra frame**. The paper's own numbers don't reconcile either: 4.5 + 0.9 × 3 = 7.2 s, not 6.0–6.2 s.
- **Revised:** Use the re-run benchmark from E2.
- **Decision:**

**E4. EngageNet author names**
- **Where:** `paper/references.bib`.
- **Problem:** "Xarly", "Di", "Yang" and "Kazuhiro" should be Ximi, Donghuo, Yanan and Kazushi.
- **Status:** Fixed in `dlsu-manuscript/myreferences.bib`. Still wrong in the ICCE paper.
- **Decision:**

**E5. What happens to clips with too few frames: three sources disagree**
- **P §2.3:** "When a clip contained fewer valid frames than *k*, all valid frames were kept."
- **D §3.4.2:** "Extraction skips a clip when it has fewer valid frames than the requested changepoint count."
- **Code, `src/feature_extraction.py:246-253`:** keeps all valid frames when there are ≤ *k* of them. It *also* returns fewer than *k* frames when `find_peaks` finds fewer than *k* peaks, a case neither document mentions.
- **Resolved (Day 2).** The code is right and D §3.4.2 is wrong.
  - Every version of the extractor in git history keeps short clips.
  - The processed 5-CP and 7-CP test files both contain clips with only 1–4 frames: 5-CP has 146 clips with fewer than 5 frames; 7-CP has 235 clips with fewer than 7.
  - Both files hold the *same* 2,005 test clips.
  - So the 222 clips missing relative to SME and 3-CP were lost for a reason that wasn't recorded (timeout, crash, or a different input set at extraction time), **not** because they had few valid frames.
- **Also unsupported:** D's claim that the excluded clips "are those with the fewest detectable behavioural transitions, plausibly correlated with engagement level".
- **Action:** Chapter 4 describes the common-subset restriction factually, and proposes logging each clip's extraction outcome during re-extraction.
- **Decision:**

**E7. The "32-subject training split" is a subset of the official training split**
- **Where:** P l.107; D §2, Table 1.
- **Evidence:**
  - The official label file `data/labels/train_engagement_labels.xlsx` lists **7,983 clips from 91 participants**.
  - `data/raw_videos/Train` holds **2,925 clips from 32 participants** (37% of the labelled training clips).
  - Validation (1,071 clips, 11 participants) and test (2,257 clips, 26 participants) match the official files exactly.
- **The data actually used is smaller again.** The processed training CSVs (`data/processed/*-changepoint-train.csv`) contain 2,719 non-SNP clips from **31** participants. The processed test CSVs contain 2,005 clips from **25** participants, so one training and one test participant lost all their clips during extraction.
- **Problem:** The paper presents 32 subjects as "the official EngageNet partition … without re-partitioning". The *partition* is official, but the training data is a subset of it.
- **Resolved (Day 2):** The proposed study uses all 91 training participants.
- **Action:** State in Chapter 4 why only 32 training participants were used (only you know). Decide with Dr. Azcarraga whether the proposed experiments keep this subset, for comparability with the preliminary study, or use all 91 participants.
- **Decision:**

**E6. "minimum separation of seven frames"**
- **Where:** P §2.3.
- **Problem:** The units are missing. It is 7 *sampled* frames. With `frame_skip = 2` (code l.248) that is 14 video frames, about 0.5 s at 30 fps; confirm the fps.
- **Revised:** State the units.
- **Decision:**

---

## Part B: Headline claims (abstract, results, conclusion)

**B1. "Every architecture reached its best macro F1 score under 3-Changepoint sampling"**
- **Where:** P abstract l.81, l.169, l.209.
- **Evidence:** Table 1 is true descriptively. But only RF's gain is significant, and LSTM's +0.73 points is below its seed SD (0.0129).
- **Lens:** Significant vs. consistent direction.
- **Verdict:** Overstated.
- **Revised:** "All four architectures had their highest mean macro F1 under 3-Changepoint sampling; the improvement over SME was statistically significant only for Random Forest."
- **Decision:**

**B2. "performance declined as further frames were added" / "macro F1 declines as the frame budget grows"**
- **Where:** P abstract l.81, l.196.
- **Evidence:** Macro F1 from *k* = 3 → 5 → 7:

  | Model | k = 3 | k = 5 | k = 7 | Pattern |
  | :--- | ---: | ---: | ---: | :--- |
  | LSTM | 0.6548 | 0.6413 | 0.6494 | Down, then up |
  | MLP | 0.6617 | 0.6471 | 0.6445 | Declines; gaps comparable to seed SD (0.005–0.012) |
  | SVM | 0.7010 | 0.6966 | 0.6884 | Declines |
  | RF | 0.5904 | 0.5612 | 0.5610 | Flat from 5 to 7 |

  No significance test compared different values of *k*.
- **Lens:** Significant vs. consistent direction.
- **Verdict:** Overstated.
- **Revised:** "Among changepoint conditions, no model improved beyond *k* = 3; macro F1 declined steadily from *k* = 3 to *k* = 7 only for SVM. Differences between *k* values were not tested for significance."
- **Decision:**

**B3. "noise-free" decline for the deterministic models**
- **Where:** P l.196.
- **Evidence:** SVM and RF have no *seed* variance, but test-set sampling variance remains: one accuracy point is about 20 of 2,005 clips.
- **Verdict:** Overstated.
- **Revised:** "For the deterministic models, which have no seed variance, the decline was monotonic."
- **Decision:**

**B4. "frame selection matters most where a classifier is least able to compensate for uninformative frames" / "the benefit … depends on model capacity rather than applying uniformly"**
- **Where:** P abstract l.81, l.192, l.209; D §1 item 4.
- **Evidence:** Four models, one significant result, and gains that don't follow model strength (see E1).
- **Lenses:** Mechanism wording; few units.
- **Verdict:** Unsupported as a general pattern.
- **Revised:** "The effect of sampling strategy varied by architecture: it was significant only for Random Forest, the lowest-accuracy model. Whether this reflects model capacity could not be determined with four architectures."
- **Decision:**

**B5. "Temporal sampling therefore warrants deliberate tuning"**
- **Where:** P abstract l.81.
- **Evidence:** One significant effect, for one model, on one dataset and one task.
- **Verdict:** Overstated.
- **Revised:** "These results suggest that temporal sampling should be reported and compared rather than fixed by default."
- **Decision:**

**B6. "Content-based sampling also reduced LSTM seed variance six-fold" / "Content-based frame selection therefore improves reproducibility"**
- **Where:** P abstract l.81, l.198, l.213; D §1 item 6, D §4.3.
- **Evidence:**
  - LSTM SD was 0.0129 (SME) vs. 0.0022 (3-CP), a ratio of 5.9. But 5-CP (0.0077) and 7-CP (0.0080) give only about 1.6×.
  - **The MLP SD under 7-CP (0.0121) is *higher* than under SME (0.0096).**
  - Each SD is estimated from 5 seeds, so it is itself imprecise.
- **Lenses:** Small-sample statistics; generalizing from one condition to "content-based".
- **Verdict:** Overstated. The general "improves reproducibility" claim is contradicted by the MLP 7-CP result.
- **Revised:** "Across five seeds, LSTM accuracy varied less under 3-Changepoint sampling (SD 0.0022) than under SME (SD 0.0129). This pattern was weaker at *k* = 5 and *k* = 7 and did not hold for MLP at *k* = 7, and five seeds give only a rough estimate of spread."
- **Decision:**

**B7. "frames beyond the top few … more likely to capture blinks or camera jitter"**
- **Where:** P l.196, l.211.
- **Evidence:** Untested.
  - Code l.148 mean-centres the landmarks in each frame, so camera shake that shifts the whole face cancels out.
  - A blink moves only a few of the 478 landmarks, so head movement would dominate the velocity signal.
- **Lens:** Mechanism wording.
- **Verdict:** Unsupported, and partly implausible given the code.
- **Revised:** "Frames beyond the top three peaks have lower landmark velocity by construction; whether they carry less engagement-relevant information was not tested."
- **Decision:**

**B8. "Controlled frame-sampling benchmarks report the same pattern, with larger frame budgets failing to improve performance monotonically" (Brkić et al., 2025)**
- **Where:** P l.196.
- **Evidence:** From the abstract only, Brkić et al. benchmark small VLMs for video QA under a *shared 96-frame budget* and report that results vary by dataset and task. I could not confirm that they varied the frame budget.
- **Lens:** Citation match.
- **Verdict:** Needs checking. The "varies by dataset and task" part is supported; the "larger budgets" part is unconfirmed. Comparing 96-frame VLM video QA with 3–7-frame engagement classification as "the same pattern" is overstated either way.
- **Action:** You read the full paper (it's on your must-read list).
- **Decision:**

**B9. "this dependency also holds within a single dataset and task"**
- **Where:** P l.196.
- **Evidence:** It follows from B2 and B8, both of which are qualified.
- **Verdict:** Overstated. Remove it.
- **Decision:**

**B10. "Brow movement is the strongest single signal … more likely a property of the task than of one sampling configuration"**
- **Where:** P l.204; D §4.7.
- **Evidence:**
  - These are Random Forest Gini importances only, with tiny values (top feature 0.0149) spread across 1,518 correlated features.
  - "AU_*" features are MediaPipe blendshapes, not coded Action Units.
- **Lens:** Feature importance.
- **Verdict:** Overstated.
- **Revised:** "In the Random Forest, the right outer-brow-raise blendshape had the highest Gini importance under both SME and 3-Changepoint sampling. Gini importance reflects what this model used, not which behaviours indicate engagement."
- **Decision:**

**B11. "suggesting the classifiers converge on similar underlying signal and that the gap between strategies reflects frame quality rather than different learned features"**
- **Where:** P l.211.
- **Evidence:** Importance was computed for RF only, so "the classifiers" isn't supported. Frame quality was never measured.
- **Verdict:** Unsupported. Remove it.
- **Decision:**

**B12. "temporal sampling is a design decision with measurable consequences … one that argues against simply sampling more frames"**
- **Where:** P l.213.
- **Evidence:** The "measurable consequences" part rests on RF only. The "more frames" part rests on 3 vs. 5 vs. 7 sparse frames within one method; dense sampling was never tested.
- **Verdict:** Overstated.
- **Revised:** "In this setup, sampling strategy had a significant effect for one of four architectures, and selecting more than three velocity peaks did not improve any model."
- **Decision:**

**B13. "Engagement signals detected from video also serve as behavioral inputs to agentic AI systems"**
- **Where:** P l.92.
- **Evidence:** No citation.
- **Verdict:** Unsupported. Cite a source or remove it. It also widens the scope the panel asked you to narrow.
- **Decision:**

**B14. "At roughly 70% macro F1, such signals should serve as advisory inputs rather than deterministic triggers"**
- **Where:** P l.215.
- **Evidence:** A normative recommendation, appropriately hedged.
- **Verdict:** Supported as an opinion. Keep it only if Chapter 1 discusses deployment; otherwise drop it to keep scope tight.
- **Decision:**

---

## Part C: Background claims to verify against sources (Days 3–5)

| # | Claim (location) | What to check |
| :-- | :--- | :--- |
| C1 | "Student engagement is a well-established predictor of learning outcomes" (P l.92) | Fredricks et al. (2004) report *associations*, strongest for behavioural engagement. Likely revision: "is associated with academic achievement." |
| C2 | DAiSEE facts: 9,068 snippets, 112 participants, ages 18–30, settings (P l.94) | Gupta et al. (2016) |
| C3 | EngageNet facts: 127 participants, ages 18–37, three 5-minute videos, avatar narrator, two questions per video, about 11,300 clips, three annotators (P l.94) | Singh et al. (2023). The arXiv abstract confirms 127 participants and 11.3K 10-second clips. |
| C4 | Uniform segmentation is used in the DAiSEE benchmark and the EngageNet baselines (P l.96) | Gupta et al. (2016) and Singh et al. (2023), methods sections |
| C5 | "Content-aware methods that select frames by motion salience" (Korbar et al., 2019) (P l.96) | SCSampler selects *clips*, not frames, using lightweight saliency features. Reword. |
| C6 | Velocity-peak sampling "remains largely untested for engagement recognition" (P l.96) | Your literature review must show this. Check Resurreccion (2024), which classifies academic emotions from landmark changes over time. |
| C7 | Threshold 3 "provided the most balanced distribution of the thresholds considered" (P l.125) | Needs the class counts for the other thresholds (your PERSUASIVE paper?). |

---

## Part D: Methodology-doc claims, if they go into Preliminary Results

**D1. "Architecture dominates sampling: 19/24 architecture comparisons significant vs 4/12 sampling"**
- **Where:** D §1 item 1, D §4.4.
- **Evidence:**
  - Counting significant tests isn't a measure of effect size.
  - The sampling count of 4/12 includes the LSTM seed artefact; the genuine count is 3/12, all of them RF.
  - All architectures were run at default hyperparameters.
- **Verdict:** Overstated.
- **Revised:** "In this setup, differences between architectures (SVM vs RF: 8.9–12.0 accuracy points) were larger than differences between sampling strategies (at most 4.8 points)."
- **Decision:**

**D2. "the sequence model never beats a feed-forward net seeing only a temporal average"**
- **Where:** D §1 item 2.
- **Evidence:** True for the mean-pooled LSTM at defaults with 3–7 frames. The readout ablation (D §4.5) shows an attention readout gains +2.04 points.
- **Verdict:** Overstated.
- **Revised:** "With a mean-pooling readout and default settings, LSTM and MLP accuracies did not differ significantly in any condition."
- **Decision:**

**D3. "SVM is both most accurate and cheapest. No accuracy/compute trade-off exists on this task."**
- **Where:** D §1 item 3, D §4.4.
- **Evidence:** Only training time was measured, on one machine; inference cost wasn't measured.
- **Verdict:** Overstated.
- **Revised:** "SVM had the highest accuracy and the shortest training time of the four models."
- **Decision:**

**D4. "The LSTM readout is a bottleneck. Attention gains 2.04 pts"**
- **Where:** D §1 item 7, D §4.5.
- **Evidence:** The gain was consistent across 4 conditions × 5 seeds but not significance-tested. The readout was also compared on the *test* set, so choosing it from these results would be selection on test data.
- **Verdict:** Overstated.
- **Revised:** "An attention readout had higher mean accuracy than mean-pooling in all four sampling conditions (+2.04 points over 20 runs; not significance-tested)." In the proposal, plan to choose the readout on the validation split.
- **Decision:**

**D5. "RF's deficit is minority-specific … not an imbalance artefact"**
- **Where:** D §4.4.
- **Evidence:** Class 1 F1 is 0.40–0.49 vs. 0.66–0.69 for Class 0. But Class 1 is not the minority in the restricted training split (1,344 vs. 1,375).
- **Verdict:** Overstated wording.
- **Revised:** "Random Forest's lower accuracy came mainly from the Highly-Engaged class (F1 0.40–0.49 vs 0.66–0.69 for the other class)."
- **Decision:**

**D6. SVM 3-CP: "its CI excludes zero, so the effect is probably real but small"**
- **Where:** D §4.2.
- **Evidence:** It mixes an *uncorrected* confidence interval with a Holm-*corrected* test that was not significant (p = 0.082).
- **Verdict:** Overstated.
- **Revised:** "The SVM's +1.70-point gain did not reach significance after correction."
- **Decision:**

---

## Part E: Supported as written

- **Best of the 16 configurations at default settings:** 3-Changepoint with SVM, 0.7010 macro F1 and 0.7017 accuracy (Table 1).
- **Only Random Forest's sampling effect survives Holm-Bonferroni correction.** The LSTM 5-CP result is a seed artefact: it reverses sign in 3 of 5 seeds (Table 2, D §4.2).
- **The subject-independent split** prevents a model from scoring well by recognising individual students (P l.107).
- **SMOTE had no material effect;** the training split is near-balanced (D §4.6).
- **RF importance is diffuse.** The top feature carries about 22 times its uniform share: 0.0149 × 1,518 (D §4.7).

## Must-read papers for this audit

- **Brkić et al. (2025):** resolves B8.
- **Fredricks et al. (2004):** resolves C1.
- **Singh et al. (2023):** C3 and C4.
- **Truong et al. (2020):** the window-based section, for the "changepoint" terminology.
