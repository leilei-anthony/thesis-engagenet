# Proposal defense: storyboard

For the proposal defense around 20 Nov 2026. The panel is the same as at the OCE: Tiam-Lee (chair), Gonda, Antioquia, and Dr. Azcarraga. Everything here is taken from the manuscript as of 14 Nov 2026 (`dlsu-manuscript/main.pdf`).

## How to use this

- **You build the deck in Google Slides and write every word on it.** For each slide, this file gives:
  - a working title;
  - the one point the slide makes;
  - what goes on it;
  - notes on what to say;
  - the source in the manuscript;
  - the question it is likely to invite.
- **Titles.** The OCE panel wrote that "some of the slide titles slightly misrepresent the content". Each working title below states what its slide shows. If you reword a title, check that it still matches the slide.
- **On the slide:** keywords, numbers, and the figure only. Full sentences go in your speaker notes, in your own words.
- **Say:** these are notes, not a script. Say them your way, and don't read them aloud.
- **Numbers:** use only the ones given here. Each is traced to a section or table, and is rounded as the manuscript rounds it.
- **Timing:** 20 main slides take about 20 minutes. Slides marked ✂ can be cut or merged into a neighbor for a 15-minute slot, which saves about 4 minutes.
- **Images:**
  - All are in `figures/`, on white backgrounds.
  - In Google Slides, use Insert → Image → Upload from computer.
  - Resize from a corner so the image keeps its proportions.
- **Colors:** each selection rule has one color in every figure: SME orange, positional green, random yellow, k-Changepoint blue. If you color text or shapes yourself, keep to these.
- **Never** put a frame, face, or still from EngageNet on any slide (user agreement; §4.7). The figures use diagrams and one made-up signal only.
- **Left out on purpose** (your 14 Nov comments): the ethics review before extraction, obtaining the missing training videos, and the extraction changes. The calendar still shows "Revisions and ethics review" in Nov–Dec, as in Table 5.4.

## Figures

| File | Slide | Made from |
|---|---|---|
| `positioning.png` | 4 | Table 2.5 |
| `prelim-macro-f1.png` | 9 | Table 5.1 |
| `prelim-vs-sme.png` | 10 | Table 5.2 |
| `design.png` | 12 | Table 4.1, §4.5 |
| `selection-rules.png` | 13 | §4.4; frames for n = 20, k = 3 |
| `velocity-peaks.png` | 14 | made-up signal, labeled as such |
| `pipeline.png` | 15 | Figure 4.1, §1.3 |
| `frame-combinations.png` | 16 | §4.5 |
| `interpretation.png` | 18 | Table 4.3 |
| `calendar.png` | 20 | Table 5.4 |
| `class-balance.png` | B2 | Table 5.3 |
| `conceptual-framework.png` | B13 (or slide 5) | Figure 3.1 |

To rebuild after a change, run from the repo root:

```
conda run -n thesis-engagenet python -I proposal-defense/figures/src/charts.py
conda run -n thesis-engagenet python -I proposal-defense/figures/src/build_tex.py
```

---

## Main slides

### 1. Title · 0:15
- **On the slide:** thesis title, your name as on the title page, Dr. Judith Azcarraga (adviser), Department of Software Technology, College of Computer Studies, De La Salle University, and the date.
- **Say:** one sentence on what the study compares: frames chosen by their content against frames chosen by their position or at random.

### 2. Working title: "How the OCE revisions were addressed" · 1:00
- **One point:** each required revision has a specific place in the manuscript.
- **On the slide:** a four-row table, built natively in Slides (revision → what was done → where):

  | Revision | What was done | Where |
  |---|---|---|
  | R1 Working definitions | 14 definitions; engagement is operationally the observer-rated EngageNet label | §3.1 |
  | R2 Generative AI (VLM/MLLM) | six works reviewed (Table 2.3), and why none is tested | §2.4, §1.3 |
  | R3 RRL positions the study | Ch. 2 narrows from engagement detection to frame use, then compares the closest work | Ch. 2, §2.8 (Table 2.5) |
  | R4 Unsupported conclusions | every preliminary claim checked against the data; outcomes read by rules fixed in advance | §5.1, §4.6.5 |

- **Say:** don't read the table aloud. Give one concrete R4 example: the claim is now "the gain over SME was significant only for the Random Forest", not "changepoint sampling improves every classifier".
- **Source:** `dlsu-manuscript/notes/revisions-summary.md`. Its section numbers are from 5 Nov; the ones above are current.
- **If asked** "Did you use AI for the slides this time?": answer plainly and truthfully. AI drafted the storyboard and figures from your manuscript; you wrote the slides. See `notes/ai-disclosure-draft.md`.

### 3. Working title: "Classifiers see only a few frames of each clip, and which frames is rarely tested" · 1:00
- **One point:** engagement research has improved features and networks, while the choice of frames has been treated as fixed preprocessing.
- **On the slide:**
  - engagement: behavioral, emotional, cognitive (Fredricks et al., 2004);
  - webcam video, clips labeled by observers;
  - a 10-s clip has well over 100 frames;
  - DAiSEE, four-level accuracy: 57.9% → 67.5%, from new features and networks.
- **Visual:** none needed. If you want one, draw a plain strip of boxes for a clip's frames (no real frames).
- **Say:**
  - Why webcams: cheap and unobtrusive compared with physiological sensors.
  - Most approaches use every frame or a fixed subsample.
  - When only a few frames are kept, which ones may matter.
- **Source:** §1.1; §2.3 (57.9% and 67.5%).
- **If asked:** Q8 "Is about 70% good?" (study guide).

### 4. ✂ Working title: "Two engagement studies compared selection rules, both at three frames and without a random control" · 1:00
- **One point:** the closest prior work cannot separate the rule from the number of frames, or from chance.
- **Visual:** `positioning.png`
- **Say:**
  - Singh et al. (2023): every frame, pooled into segments.
  - Resurreccion (2024): Targeted vs. Changepoint, three frames, academic emotions on DAiSEE.
  - Your preliminary study: SME vs. k-Changepoint.
  - Neither has positional selection beyond three frames, and neither has a random control.
- **Source:** §2.6, §2.8, Table 2.5.
- **If asked:**
  - Q4: how you differ from Resurreccion.
  - "What about Abedi & Khan (2024)?" They changed only the sampling rate, not the rule (Table 2.4, "No (rate only)").

### 5. Working title: "Research question" · 0:45
- **On the slide:** the research question, word for word from §1.1: *Does content-based frame selection improve the classification of observer-rated student engagement over position-based and random selection at equal frame budgets, and does the answer depend on the frame budget and the classifier?* Add one line for the second question: does representing the order and change of the selected frames improve on averaging them?
- **Say:** the two things earlier comparisons couldn't separate:
  - the rule from the number of frames;
  - content-based selection from chance.
- **Optional visual:** `conceptual-framework.png`, if you want the variables on screen here. Otherwise keep it for B13.
- **Source:** §1.1, §2.8.

### 6. Working title: "One general and five specific objectives" · 1:00
- **On the slide:** the general objective, plus the five specific objectives, shortened without changing their meaning:
  1. extract features;
  2. characterize the selection techniques;
  3. evaluate temporal representations;
  4. implement and evaluate the classifiers;
  5. find the best-performing combination.
- **Say:** objectives 3 and 5 were added at Dr. Azcarraga's request (13 Nov).
- **Source:** §1.2.
- **If asked:** Q15: "Doesn't adding temporal representations broaden the scope again?"

### 7. Working title: "Scope: one dataset, one binary task, fixed features and classifier settings" · 1:00
- **On the slide:**
  - **in:**
    - EngageNet only, official subject-independent split (91 / 11 / 26 participants);
    - Highly-Engaged vs. the rest;
    - MediaPipe, 1,518 values per frame;
    - four classifiers at default settings, no tuning;
  - **out:**
    - the four-level task;
    - separate Not-Engaged detection;
    - end-to-end deep networks;
    - VLM experiments;
    - a classroom tool.
- **Say:** Not-Engaged stays in the negative class for three reasons:
  - one task keeps the study focused;
  - the preliminary results exist only for this task;
  - a second task would double the 176 comparisons.

  How often Not-Engaged clips are predicted as Highly-Engaged is still reported.
- **Source:** §1.3.
- **If asked:**
  - Q3 or B10: Not-Engaged.
  - Q2 or B6: VLMs.
  - B12: MediaPipe vs. OpenFace.
  - Q1: why EngageNet.

### 8. ✂ Working title: "The preliminary study compared SME with velocity-peak selection at 3, 5, and 7 frames" · 0:45
- **On the slide:**
  - EngageNet, threshold 3;
  - SME (k = 3) vs. k-Changepoint (k = 3, 5, 7);
  - LSTM, MLP, SVM, Random Forest;
  - 2,719 / 867 / 2,005 clips (training / validation / test);
  - neural networks: five seeds;
  - accepted for publication (ICCE 2026).
- **Say:** three differences from the proposed study:
  - only part of the training split;
  - no SMOTE;
  - the MLP, SVM and Random Forest got only the mean of the frames.
- **Source:** §5.1 (second paragraph); Table 4.2.
- **If asked:** Q9: why only part of the training split.

### 9. Working title: "Every classifier had its highest macro F1 with three velocity-peak frames" · 1:00
- **One point:** the direction was consistent across classifiers. Whether it is reliable is the next slide.
- **Visual:** `prelim-macro-f1.png`
- **Say:**
  - Best: SVM with 3-Changepoint, 0.701 macro F1 (0.7017 accuracy).
  - Classifiers differed more than conditions did. The SVM was 8.9 to 12.0 accuracy points above the Random Forest, while no condition changed a classifier's accuracy by more than 4.8 points.
  - LSTM and MLP values are means over five seeds.
- **Don't say:** "3-Changepoint is better". This slide shows the highest means, not a test.
- **Source:** Table 5.1; §5.1.

### 10. Working title: "Only the Random Forest improved significantly over SME" · 1:00
- **Visual:** `prelim-vs-sme.png`
- **Say:**
  - Random Forest: +4.79 points at k = 3 (p < 0.001), and significant at k = 5 and 7 too.
  - SVM and MLP: no significant difference.
  - The one significant LSTM result (−2.49 at k = 5) is not reliable. It came from a single seed, and the direction reversed in three of five seeds. That is why the proposed study requires significance in all five seeds or draws.
- **Don't say:** "content-aware sampling improves classification". This is exactly the kind of claim R4 asked you to remove.
- **Source:** Table 5.2; §5.1.
- **If asked:**
  - Q14: why the paper's wording differs from the manuscript's.
  - B8: seeds.

### 11. Working title: "Five gaps in the preliminary study, and the design change for each" · 1:00
- **On the slide:** a two-column table (gap → change):

  | Gap | Change |
  |---|---|
  | position-based rule only at k = 3 | positional selection at 3, 5, 7 |
  | no random baseline | random selection, five draws |
  | frame budgets not compared | test family 4: k = 3 vs. 5 vs. 7 |
  | neural tests on a single seed | five seeds or draws; reliable only if significant in all five |
  | MLP, SVM, RF got only the mean | three temporal representations |

- **Source:** §5.1 (last paragraph); §4.1, §4.4, §4.5, §4.6.

### 12. Working title: "Ten selection conditions, each run with four classifiers" · 1:15
- **Visual:** `design.png`
- **Say:**
  - Three rules × three budgets, plus SME at k = 3, gives ten conditions. SME is kept to link to the preliminary study.
  - Within each condition, the frames are combined four ways for the MLP, SVM and Random Forest, and two ways for the LSTM.
  - Dataset, split, features, task and classifier settings are the same everywhere, so conditions differ only in which frames are used and how they are combined.
- **Source:** §4.1, Table 4.1, §4.5.
- **If asked:**
  - Q7: why 3, 5, 7.
  - Q6: why a random baseline.

### 13. Working title: "On one clip, the four rules pick different frames" · 1:00
- **Visual:** `selection-rules.png`
- **Say:**
  - SME: first, middle, last.
  - Positional: the centre of each of k equal parts (from Temporal Segment Networks).
  - Random: uniform draws, seeds 42–46.
  - k-Changepoint: the frames at the k highest velocity peaks.
  - At k = 3, SME vs. positional tests whether the first and last frames matter (family 5).
  - Tell the audience that the random and k-Changepoint frames on the slide are an example.
- **Source:** §4.4; Algorithm 5.1.
- **If asked:** B3 (Algorithm 5.1).

### 14. ✂ Working title: "k-Changepoint keeps the frames where the face moves fastest" · 1:00
- **Visual:** `velocity-peaks.png`. Say it is a made-up signal.
- **On the slide:** velocity, in words: how far all 478 landmarks move between consecutive valid frames, after removing movement of the whole face. You can show Eq. 4.1 if you can explain each symbol.
- **Say:**
  - The 5-frame smoothing removes one-frame jitter.
  - Peaks must be at least 7 scanned frames (14 video frames) apart.
  - The k highest peaks are kept, so a clip can give fewer than k frames.
  - It is the simplest case of window sliding (Truong et al., 2020), so you call it velocity-peak selection.
- **Source:** §4.4 (Eq. 4.1), §3.5.
- **If asked:**
  - B1: where Eq. 4.1 comes from.
  - Q10: why still call it "changepoint".
  - Q12 and B7: PELT and BOCPD.

### 15. ✂ Working title: "Every clip goes through the same pipeline; only the highlighted steps change" · 1:00
- **Visual:** `pipeline.png`
- **Say:**
  - First pass, on every second frame: face and pose, the validity check, and velocity.
  - Selection.
  - Second pass, on the selected frames only: background removed; 1,518 values per frame (1,434 landmark coordinates, 52 blendshapes, 32 pose values).
  - Then the frames are combined and passed to a classifier.
  - SMOTE balances the training split only.
- **Source:** §1.3 (Data preparation), §4.3, Figure 4.1.
- **If asked:**
  - B12: MediaPipe.
  - B5: SMOTE.

### 16. Working title: "Four ways to combine the selected frames, and two readouts for the LSTM" · 1:15
- **Visual:** `frame-combinations.png`
- **Say:**
  - The mean is the baseline and carries no temporal information. Concatenation keeps the order.
  - Change: the average absolute difference between consecutive frames, feature by feature.
  - Self-similarity: the cosine similarity of every pair of frames (3, 10 or 21 values). Features are standardized first; otherwise almost every cosine would be close to 1.
  - Only the selected frames are used, with no timing information, so that the rules stay comparable.
  - LSTM: averaging vs. attention. In the preliminary study, attention was 2.04 points higher over 20 runs, but this was untested and measured on the test split. So both readouts are compared, and neither is chosen in advance.
- **Source:** §4.5, §2.7, §3.6.
- **If asked:**
  - Q16: where these representations come from.
  - Q18: why standardize first.

### 17. Working title: "Conditions are compared clip by clip, in 176 comparisons fixed in advance" · 1:30
- **On the slide:**
  - **Metrics:** macro F1 (primary), accuracy, MCC.
  - **Tests:** exact McNemar tests, with Holm–Bonferroni correction within each family.
  - **Families** (a small table you build):

    | Family | Comparisons |
    |---|---|
    | content vs. position | 12 |
    | content vs. chance | 12 |
    | position vs. chance | 12 |
    | frame budget | 36 |
    | clip boundaries | 4 |
    | temporal representation | 100 |
    | **total** | **176** |

  - **Seeds and draws:** five each; a difference is reliable only if significant in all five.
  - **Equivalence:** the 95% CI of the accuracy difference lies within ±2 points (paired bootstrap, 10,000 resamples).
  - **Best configuration:** chosen on validation macro F1, reported once on test.
- **Say:** why ±2 points:
  - seed-to-seed SD was up to 1.3 points;
  - the CI half-width was about 1.4;
  - the significant effects were 2.39–4.79 points.
- **Source:** §4.6.1–§4.6.4, §4.6.6.
- **If asked:**
  - Q11: what if nothing is significant.
  - Q17: why choose the best configuration on validation.
  - B8: seeds.

### 18. Working title: "How each pattern of results will be read was set before the experiments" · 1:00
- **Visual:** `interpretation.png`
- **Say:**
  - This answers R4 in advance. For example, if changepoint ≈ random, you will not claim that velocity peaks carry engagement information.
  - Temporal representations: one "improves on the mean" only if it is reliably better in at least half of the ten conditions and worse in none.
- **Check before the defense:** this rule (study guide D25) is still marked "approve or change". Confirm it with Dr. Azcarraga, or present it as provisional.
- **Source:** Table 4.3; §4.6.5.

### 19. Working title: "Pre-existing data, used under the EngageNet user agreement and the Data Privacy Act" · 0:45
- **On the slide:**
  - pre-existing data only; no contact with participants;
  - user agreement: academic and non-commercial use, no redistribution;
  - Data Privacy Act of 2012 applies (processing in the Philippines);
  - videos only on your computer, not in version control;
  - no participant images anywhere;
  - aggregate results only;
  - not for decisions about individual students.
- **Source:** §4.7.
- **If asked:**
  - B9: the research exemption.
  - B6: VLMs and the user agreement.

### 20. Working title: "Remaining work: November 2026 to the final defense in March 2027" · 1:00
- **Visual:** `calendar.png`. Point only at the Planned rows.
- **Contributions** (keywords on the slide, from §1.4):
  - evidence on a design choice usually fixed without testing;
  - a reusable evaluation protocol: common clip set, paired tests over seeds and draws, equivalence margin, rules fixed in advance;
  - practical guidance on the best configuration, within this dataset and task.
- **Say:** close with thanks and invite questions. If this slide feels crowded, split it into calendar and contributions; you have about a minute of slack.
- **Source:** Table 5.4; §1.4.

---

## Backup slides (after a "Backup" divider; shown only if asked)

### B1. Where Eq. 4.1 comes from
- It is your own formula: it writes out `get_landmark_velocity` in `src/feature_extraction.py` (lines 145–152).
- How it relates to Truong et al. (2020): in window sliding with one-frame windows, the discrepancy between neighboring frames is ½v². So it has the same peaks as the velocity, before smoothing.
- What has no source: removing whole-face movement, the 5-frame smoothing, and the 7-frame gap. These were fixed choices in the preliminary study and were never tuned.
- **Source:** §3.5, §4.4.

### B2. Why threshold 3
- **Visual:** `class-balance.png`
- Only threshold 3 gives near-equal classes in every split.
- Majority-class accuracy on test: 79.7% at t = 1 vs. 50.3% at t = 3.
- The early runs at t = 1 and t = 2 were exploratory, made before the common clip set, and are not reported.
- **Source:** §5.2.3, Table 5.3. Study guide Q19.

### B3. Algorithm 5.1, frame selection
- Take a screenshot of Algorithm 5.1 from `main.pdf` (§5.2.2). It is pseudocode, so there is no data on it.

### B4. Algorithm 5.2, training and evaluation
- Take a screenshot of Algorithm 5.2 from `main.pdf`.
- If asked how many training runs: about 476. This is **your own count, not stated in the manuscript**:
  - LSTM (2 readouts) and MLP (4 combinations) × 10 conditions × 5 seeds = 300;
  - SVM and RF (4 combinations each) × (7 fixed conditions + 3 random × 5 draws) = 176.

### B5. SMOTE
- Applied to the training split only, after the common clip set is fixed. Never applied to validation or test.
- For the neural networks, each sequence is flattened before SMOTE and restored after it.
- In the preliminary study it had no material effect, because the data were nearly balanced. It is used so that every condition trains on exactly balanced data.
- **Source:** §4.5. Study guide Q13.

### B6. Why no VLM experiments
- There is no evidence of reliable zero-shot engagement classification. Goyal et al. (preprint): agreement κ ≤ 0.10, with 85–100% of clips assigned to one level. Teotia et al.: engaged and distracted behavior confused.
- The user agreement forbids sending the videos to an external service.
- Scope.
- VLMs also see only a few frames, so the question of this study applies to them too; this is left as future work.
- **Source:** §1.3, §2.4, Table 2.3. Study guide Q2.

### B7. PELT and BOCPD not used
- The study asks whether choosing frames by content helps at all, not which changepoint method is best.
- **Source:** §1.3, §3.5. Study guide Q12.

### B8. Seeds and draws
- Five seeds (42–46) for the neural networks and five draws for random selection; seed i is paired with draw i.
- A difference counts as reliable only if it is significant in all five versions.
- The reason: the preliminary LSTM result that reversed in three of five seeds.
- **Source:** §4.6.3.

### B9. The Data Privacy Act's research exemption
- Section 4 of the Act lists research processing among its exceptions.
- Treating the Act as applying, because processing happens in the Philippines, is the cautious choice. The study's measures (storage, no images, aggregate reporting) meet it either way.
- **Source:** §4.7. Study guide §5, item 8.

### B10. Not-Engaged
- The three reasons it isn't a separate task (as on slide 7).
- For every condition, the study reports the share of Not-Engaged, Barely-engaged and Engaged clips predicted as Highly-Engaged.
- Threshold 1 is left for future work.
- **Source:** §1.3, §4.6.1, §5.2.3. Study guide Q3.

### B11. Common clip set
- Every condition is scored on the same clips. Without this, a difference could come from scoring different clips rather than from selecting different frames.
- Preliminary study: 2,719 / 867 / 2,005 clips.
- **Source:** §4.2.3.

### B12. MediaPipe rather than OpenFace action units
- MediaPipe gives both the landmarks that k-Changepoint needs and the classifier features.
- Blendshapes have not been shown to work better than action units, and results with action units are not tested. This is stated as a limitation.
- **Source:** §1.3, §3.3.

### B13. Conceptual framework
- **Visual:** `conceptual-framework.png`
- Independent variables: the selection rule and k, the frame combination, the classifier.
- Dependent variable: macro F1, accuracy, MCC.
- Everything else is held constant.
- **Source:** §3.9, Figure 3.1.

---

## Before you present

- [ ] Every title matches what its slide shows.
- [ ] Every number on a slide appears in this file or in the manuscript at the cited place.
- [ ] No frame, face, or still from EngageNet on any slide.
- [ ] Timed once out loud. If you're over time, cut the ✂ slides first.
- [ ] The D25 rule on slide 18 is confirmed or marked provisional.
- [ ] Export the deck to PDF (File → Download → PDF) into `proposal-defense/`, so it can be reviewed against the manuscript.
