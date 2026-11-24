# Study Guide: First Full Draft (5 Nov 2026)

Read this alongside the PDF. For each chapter drafted overnight it gives:
- what the chapter is for;
- the decisions I made that you must approve or change;
- the claims ledger (each claim and its source);
- what you must read;
- the questions the panel is likely to ask, with model answers.

Rewrite the model answers in your own words before the defense. The panel will notice memorized phrasing.

**Contents:**
- §0 Decisions I made overnight
- §1 Chapter 2
- §2 Chapter 1
- §3 Abstracts
- §4 Likely panel questions
- §5 Things only you can verify
- §6 Reading plan
- §7 Answers to your 10 Nov review comments
- §8 Dr. Azcarraga's 13 Nov objectives comments: what changed and a lesson on temporal representations
- §9 Dr. Azcarraga's 14 Nov notes: Data preparation, Chapter 5, and the calendar (§9.5: her second round of notes)
- §10 Dr. Azcarraga's 15 Nov request: the three papers
- §11 k-BOCPD as a fifth rule, and nested random draws (15 Nov): lesson, decisions, ledger, panel questions
- §12 How "improves on the mean" is decided: replicability analysis (15 Nov)
- §13 The research ethics forms (16 Nov)

---

## 0. Decisions I made overnight (approve or change)

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D1 | **Chapter 2 outline.** Seven sections in a funnel, from detection in general down to frame use in engagement, then a synthesis. The outline gate was skipped because you asked for a full draft. | Ch. 2 | R3: the order itself argues for your study (§1.1 below) |
| D2 | **Research questions** (revised 22–23 Nov: Doc Jay asked for questions that can't be answered yes or no): (1) "How does content-based frame selection compare with position-based and random selection in classifying observer-rated student engagement at equal frame budgets?" (2) "How does this comparison vary with the frame budget and the classifier?" (3) "What are the effects of representing the order and change of the selected frames on engagement classification, compared with averaging them?" | §1.1, last paragraph; §4.1 | They follow from the variables you approved. Before 22 Nov: "Does content-based frame selection improve …?" |
| D3 | **Four specific objectives:** extract, then train and evaluate, then compare rules, then examine budget and boundaries. | §1.2 | One per step of Chapter 4; each is measurable |
| D4 | **Not-Engaged stated as a limitation.** The binary task does not detect the minority class that matters most. | §1.3 | Honest, and pre-empts the panel. It conflicts with `AGENTS.md`'s class-0 priority, so be ready to defend it (Q3) |
| D5 | **VLMs: literature only**, for three stated reasons. | §1.3, §2.4 | Your choice last night |
| D6 | **Philippine context:** one cited sentence (CHED CMO No. 4, s. 2020), plus a limitation that EngageNet wasn't collected for Filipino learners. | §1.1, §1.3 | Your choice last night |
| D7 | **Abstract keywords.** Template says to use ACM CCS terms; I chose free keywords plus "E-learning" (a CCS term). | `abstract_en.tex` | Check them at dl.acm.org/ccs and swap in exact CCS terms if your adviser wants |
| D8 | **Template clean-up.** Sample bib entries deleted; `figures/DisneyChart.png` is now unused (delete it if you like). | `myreferences.bib` | Day 6 task in the plan |
| D9 | **Table layout.** New ragged-right column type `L{width}` for narrow table cells (Ch. 2 and Ch. 4). Layout only; no content changed. | `preamble.tex` | Justified narrow cells had large gaps between words |
| D10 | **`.gitignore` fix (important).** A second copy of your signed EULA is in `oral-comprehensive-exam/`. The rule now ignores `EULA_*.pdf` in every folder. | `.gitignore` | Without this, committing `oral-comprehensive-exam/` would have committed your signature |
| D11 | **Appendix B.** Only Dr. Azcarraga listed, with a red PENDING marker for her e-mail. | `appendix_B.tex` | I won't guess an e-mail address |

**Added 10 Nov 2026, after your review.** D12–D15 are your answers. D16–D20 are defaults that came with the plan you approved.

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D12 | **SMOTE in every condition**, training split only. | §1.3, §4.5, Fig. 3.1 | Your choice |
| D13 | **Not-Engaged stays in the negative class**, with three stated reasons. | §1.3 | Your choice; keeps the scope narrow |
| D14 | **Fredricks' definition kept**, with a note that affective computing (DAiSEE, D'Mello 2013) calls engagement an affective state. | §3.1 | Your choice; answers your "is engagement an emotion?" question |
| D15 | ~~**Calendar fits within April.** Final defense in early April, then post-defense revisions and submission.~~ **Superseded by D32** (14 Nov). | §5.3 | Your choice |
| D16 | **Processing time reported**, descriptive only, on one computer. Dates removed from Exclusions. | §1.3, §4.3, §4.6.1 | Your suggestion |
| D17 | **MediaPipe blendshapes kept**, with the reason and the limitation stated. | §1.3, §3.3 | Answers your OpenFace question |
| D18 | ~~**PELT and BOCPD named as not used.**~~ **Superseded by D43** (15 Nov): BOCPD is now a rule; PELT is still not used (D50). | §1.3, §3.5 | Your OCE slides showed them (Q12) |
| D19 | **Per-level error breakdown**: how often Not-Engaged, Barely-engaged and Engaged clips are predicted as Highly-Engaged. | §1.3, §4.6.1 | Keeps Not-Engaged visible without a second task |
| D20 | **"Set before any results are seen" kept** in §1.4, reworded. | §1.4 | It is what makes the protocol trustworthy |

Added 14 Nov, after Dr. Azcarraga's comments on the objectives (§8):

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D21 | **Objectives rewritten as broad goals.** One general objective and five specific objectives. All details moved to §1.3. | §1.2, §1.3 | Adviser's comment |
| D22 | **New objective: temporal representation.** For the MLP, SVM and RF: mean (baseline), concatenation, mean + change, and mean + cosine self-similarity. For the LSTM: averaging vs. attention readout. Run in all 10 selection conditions. | §1.2–1.3, §2.7, §3.6, §4.5 | Your choice; "combine frames" means representing their temporal aspect |
| D23 | **New test family 6:** each temporal representation vs. the mean, 100 comparisons. Total is now 176. | §4.6.2 | Your choice |
| D24 | **New objective: best configuration**, chosen by validation macro F1 and reported once on test, descriptively. | §1.2, §4.6.6 | Adviser's comment; validation avoids an inflated test score |
| D25 | ~~**A temporal representation "improves on the mean"** for a classifier only if it is reliably better in at least half of the ten conditions and reliably worse in none.~~ **Superseded by D51** (15 Nov). | §4.6.5 | My default rule, which had no source |
| D26 | **PCA exploration** is not in the manuscript for now. | n/a | Your choice; ask the adviser what she meant (§5) |
| D27 | **Open review items from 10 Nov fixed** (list in §8). Items 12 (smoothing at the clip edges) and 13 (extraction workload) are still open. | Several | Your choice |

Added 14 Nov, after Dr. Azcarraga's notes on the 14 Nov revision (§9):

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D28 | **"Frame combination" renamed and broadened into "Data preparation (Objectives 1 and 3)".** It walks through how a clip becomes classifier input. The paragraphs are reordered: Data → Data preparation → Frame selection → Task and classifiers. | §1.3 | Adviser's note; your choice of option |
| D29 | **New Chapter 5, "Preliminary Results and Future Work".** The old §4.7 (preliminary results) and §4.9 (calendar) moved there unchanged. Ethics is now §4.7. | Ch. 5 | Adviser's note |
| D30 | **Binarization explained, no new runs.** A class-size table for thresholds 1–3 and the reasons for keeping threshold 3. The early threshold 1 and 2 runs are not reported. | §5.2.3 | Your choice |
| D31 | **Algorithms as pseudocode:** 5.1 frame selection and 5.2 training and evaluation. | §5.2.2 | My default for "algorithms" |
| D32 | **Calendar from MSLABS1 (May 2025) to March 2027.** Final defense in late March; revisions in April, outside the calendar. Terms: T1 Sep–Dec, T2 Jan–Apr, T3 May–Aug. First drawn as a Gantt chart (Fig. 5.1); **now Table 5.4** (D33). | §5.3, Table 5.4 | Adviser's note; your answers |
| D33 | **Second round of notes (14 Nov), §9.5.** Gantt chart replaced by a bullet table like the old Table 4.6. One bullet per term (MSLABS1–3) or per month (from May 2026). §5.3 text cut to one sentence. Steps 1–3 removed from §5.2.1. Four lines removed from Ch. 1 and Ch. 4. | §1.3, §1.4, Ch. 4, §5.2.1, §5.3 | Adviser's notes |

Added 14–15 Nov, while preparing the main study and after Dr. Azcarraga's request for the three papers (§10):

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D34 | **Item 12 closed: edge smoothing kept** as in the preliminary study (zero-padded five-point average). | No manuscript change | Your choice; matches the ICCE paper and Algorithm 5.1 |
| D35 | **Item 13 closed: nested random draws.** One shuffle per seed (42–46); k = 3, 5, 7 take its first k frames. The manuscript text (M1) was drafted on 15 Nov (§11.5). | §4.4, Algorithm 5.1 | Your choice; cuts the extraction workload |
| D36 | **Old code tagged, then removed** from main. Nothing goes into `archive/`. | Repository | Your choice |
| D37 | **You write the main-study code; I spec and review** (`docs/implementation-spec.md`). | Repository | Your choice; you must defend the code |
| D38 | **§5.1 is now "Preliminary Work".** 5.1.1 summarizes the two DAiSEE papers (PERSUASIVE, TENCON), one paragraph each. 5.1.2 is the old §5.1 on the ICCE study, with only its first sentence changed. The label `sec:prelim` stayed on the ICCE subsection, so every existing cross-reference still points to it. | §5.1 | Adviser's request; your choice of layout and depth |
| D39 | **The DAiSEE papers are reported narrowly:** what was done, the results the thesis builds on, and the papers' limits. Their broader claims are not repeated. TENCON's internal inconsistencies are not discussed anywhere. | §5.1.1 | Your choice; the same stance as the ICCE section |
| D40 | **New Appendix B, "Publications":** Table B.1 (venue and status), then the three papers in full. Resource Persons moved to Appendix C. Statuses: PERSUASIVE published (DOI checked on Crossref); TENCON presented but not yet published, marked "Accepted for publication" at your request; ICCE accepted for presentation. | `appendix_publications.tex`, `main.tex` | Adviser's request; your statuses (15 Nov) |
| D41 | **ICCE is "accepted for presentation"**, not "accepted for publication". This replaces the 14 Nov wording (§9.5). | §5.1.2, bib note | Your correction (15 Nov) |
| D42 | **Bibliography fixes.** Every `booktitle` keeps its capitalization. apacite had been lowercasing it ("ieee", "cvpr") throughout the reference list. Your name is now in BibTeX's "Last, Jr., First" form, so it renders "Sityar, L. A., Jr." instead of "Sityar, L. A. J.". | `myreferences.bib` | Formatting errors found while adding the papers |

Added 15 Nov (later), after you asked about BOCPD (§11). D43 is your choice; D44–D50 are my proposals for you to approve.

| # | Decision | Where | Why |
| :-- | :--- | :--- | :--- |
| D43 | **k-BOCPD added as a fifth rule** (k = 3, 5, 7). Velocity peaks stay, under their old name, k-Changepoint. 13 conditions, 25 feature sets, 590 runs, 254 comparisons. | §1.3, §4.1, Table 4.1, §4.4, Ch. 5 | Your idea; you chose both rules over replacing (§11.1) |
| D44 | **Signal:** the centered landmark positions of Eq. 4.1, reduced within each clip to 3 principal components, all divided by the standard deviation of the first. | §4.4 | Your choice of 3 PCs; one common scale keeps noise components small |
| D45 | **Model:** each component Gaussian with unknown mean and variance, independent; normal–inverse-gamma prior μ₀ = 0, κ₀ = 1, α₀ = 2, β₀ = 1. | §4.4 | Expected variance 1 on the clip's scale; fixed, not tuned |
| D46 | **Hazard 1/20; run lengths capped at 50.** | §4.4 | About seven changes per 150 valid frames, as many as the largest budget; the cap removes the start-of-clip bias (§11.3) |
| D47 | **Score:** probability that a new segment begins at frame t, read L = 7 frames later, computed forward and backward and averaged. Then peaks ≥ 7 apart, top k, as for velocity peaks. Frames need L valid frames on each side; clips with fewer than 14 valid frames (and more than k) leave the common set. | §4.4, Eq. 4.2, Alg. 5.1 | §11.3 |
| D48 | **Seven families, 254 comparisons:** 24 / 24 / 12 / 12 (new: velocity peaks vs. BOCPD) / 48 / 4 / 130. Holm stays per family. | §4.6.2, Ch. 1, Ch. 5 | Families grouped by question |
| D49 | **Table 4.3** (interpretation) has one block for each content rule and one for the two content rules against each other. "Improves on the mean" needs 7 of 13 conditions. The positions of the selected frames are reported for every rule. | §4.6.1, §4.6.5 | Shows whether a content rule favors part of the clip |
| D50 | **PELT still not tested.** It finds the same kind of lasting change as BOCPD. | §1.3, §3.5 | The study compares two definitions of content, not every changepoint method |
| D51 | **"Improves on the mean" is decided by replicability analysis** (Dror et al., 2017). For each representation and classifier, k̂ is the number of the 13 conditions in which it is better (Eq. 4.3), with α = 0.005 per count (0.05 over 10 counts). It improves if k̂ ≥ 7 in every version and the reverse count is 0 in every version. | §4.6.5, Eq. 4.3; Ch. 5 step 6, Alg. 5.2 | Your choice (15 Nov); replaces D25 with a published method that is valid for dependent conditions (§12) |
| D52 | **Ethics forms answered; preliminary processing disclosed; smoke test only after approval.** No conflict of interest. Duration left blank. | Appendix A, §4.7, `notes/ethics-answers.md`, spec §5 step 3 | Your choices (16 Nov); see §13 |

No items are marked in red in the PDF any more. The §4.1 question "[Is this scope good enough for the proposal?]" was removed on 14 Nov at her request, and her e-mail was added to Appendix B the same day.

---

## 1. Chapter 2: Related Works

### 1.1 Lesson: synthesis, not summary

**A summary** goes paper by paper: "X did A. Y did B." **A synthesis** goes idea by idea, comparing papers on the same criteria. For example: "Most approaches use every frame (X, Y); only two select a few frames by rule (Z, W)."

The template asks for synthesis, and so did the panel (R3: the discussion flow must "introduce and position" your study). Every section of Chapter 2 does three things:
1. Compares works on fixed criteria: data, signal, how frames reach the model, model, result.
2. Ends with what that body of work **leaves open**.
3. Hands over to the next section, which is narrower.

**The funnel, and the gap each section leaves:**

| § | Topic | The gap it leaves (leads to the next section) |
| :-- | :--- | :--- |
| 2.1 | Automated engagement detection | Webcam video alone is the practical case for online learning |
| 2.2 | Datasets | Why EngageNet; a single dataset is a limitation |
| 2.3 | Models | Frame handling is fixed preprocessing, never a studied factor |
| 2.4 | VLMs (R2) | VLMs also see few frames, so frame choice matters to them; not reliable yet; excluded |
| 2.5 | Frame selection in video understanding | Selection matters there, but those tasks differ, so test it for engagement |
| 2.6 | Frame use in engagement | The two rule comparisons had one budget and no random control |
| 2.7 | Synthesis | **The gap:** no matched-budget comparison of content vs. position against a random control |

**How to explain the whole chapter in 30 seconds:**

> People have improved engagement detection mostly by changing features and networks. The choice of which frames to use has been treated as fixed. In other video tasks, that choice clearly matters. The only two engagement studies that compared selection rules couldn't separate the rule from the number of frames, and had no random baseline. My study fixes both.

### 1.2 Claims ledger: Chapter 2

**Checked** values:
- **Full:** I read the relevant section of the paper.
- **Abs:** abstract or listing only.
- **2nd:** the figure is reported by another paper.

| § | Claim | Source | Checked |
| :-- | :--- | :--- | :--- |
| 2.1 | 90 multimodal systems; fusion beat the best single modality in 85%; mean +9.83%; smaller on natural data | D'Mello & Kory (2015) | Abs |
| 2.1 | Clip labels predicted from the frame-label average, r = 0.85; static expressions hold most of the information | Whitehill et al. (2014) | Abs |
| 2.1 | Above-chance detection from face and body video in a school lab; generalized across times and days | Bosch et al. (2016) | Abs |
| 2.1 | Video-based facial features plus heart rate to detect self-reported engagement | Monkaresi et al. (2017) | Abs |
| 2.1 | Webcam is cheaper, more ubiquitous, and less intrusive | Abedi & Khan (2021), introduction | Full |
| 2.2 | DAiSEE: 9,068 clips, 112 users, 4 states × 4 levels, crowd labels plus psychologists' gold standard | Gupta et al. (2016) | Full |
| 2.2 | DAiSEE engagement: very low 61, low 459 (5.7% in the two lowest levels) | Gupta et al. (2016), Table 2 | Full. (61 + 459) / 9,068 = 5.73% |
| 2.2 | EngageWild: 195 videos, 78 subjects, 4 levels | Kaur et al. (2018) | Abs |
| 2.2 | EngageNet: 127 participants, 3 annotators, κ 0.73 / 0.79 / 0.77; class shares 48.57 / 20.97 / 12.3 / 18.16% | Singh et al. (2023), §3 | Full |
| 2.2 | CMOSE: 12,193 segments, 102 participants, 7 trained labelers, ICC = 0.84; says DAiSEE's label quality has been questioned | Wu et al. (2024) | Full |
| 2.2 | RAER: about 2,700 clips, about 140 students, academic emotions, about 10 annotators; context cues | Zhao et al. (2025) | Abs. **Read the full paper (panel's suggestion).** |
| 2.2 | EngageNet has the most participants among the engagement-labeled datasets in Table 2.1 | Table 2.1: 127 vs. 112, 102, 78 | Arithmetic. RAER (about 140) is excluded because it isn't engagement-labeled |
| 2.3 | Accuracy table (57.9 → 67.6) | Each paper. Liao's 58.84% is from Abedi & Khan | Full or Abs or 2nd (see `literature-matrix.md`) |
| 2.3 | EngageNet Transformer 67.6% test; MARLIN fusion 66.5% | Singh et al. (2023), Tables 4–5 | Full |
| 2.3 | TCCT-Net beat the baselines with 2 head-pose signals vs. 98 features; an order of magnitude faster than image-based RNNs | Vedernikov et al. (2024) | Abs |
| 2.3 | Abedi & Khan: 50 frames per clip; Singh: 20 equal segments, mean and SD | Both papers' method sections | Full |
| 2.4 | Emotion-LLaMA F1 0.9036 on MER2023-SEMI | Cheng et al. (2024) | Abs |
| 2.4 | VLMs good at basic emotion struggle with engagement; reading vs. bowing the head | Teotia et al. (2024) | Full (abstract and introduction) |
| 2.4 | Zero-shot Llama / Qwen: good on happy, missed distracted | Wang et al. (2025), preprint | Abs |
| 2.4 | κ ≤ 0.10; 85–100% of predictions in one class; up to 32 points from prompt wording; GPT-4o refused 98% of chain-of-thought requests | Goyal et al. (2026), preprint | Abs |
| 2.4 | VLM as label checker; up to +1.21% in 3 of 6 EngageNet settings | Vedernikov et al. (2025), preprint | Abs |
| 2.4 | Sending clips to a hosted model isn't permitted without approval | EngageNet user agreement (no redistribution or dissemination) | Your EULA |
| 2.5 | TSN, SCSampler (+7%, more than 15×), AKS (relevance plus coverage; uniform can miss), Brkić (strategy matters; best varies) | Each paper | Abs |
| 2.6 | FAN attention; Kaur MIL; Bag of States 66.58% and shuffling robustness; Das & Dev frame-level transfer | Each paper | Abs |
| 2.6 | Resurreccion: Targeted vs. Changepoint, 3 frames, DAiSEE academic emotions; Changepoint slight edge for engagement and frustration | Resurreccion (2024) | Abs. **Verify the full thesis (§5)** |
| 2.6–2.7 | Neither rule comparison included random selection | Resurreccion: "two frame selection methods"; prelim: your design | Abs plus your own work |
| 2.7 | "Among the works reviewed here, none has compared…" | Scoped to *the works reviewed*, deliberately not "no study ever" | R4 wording |

### 1.3 Must-read for Chapter 2 (in order)

1. **Resurreccion (2024)**, Chapters 3–4. The closest prior work, from your adviser's group. Know how Targeted and Changepoint were defined, how many frames they kept, and whether any random condition existed. If Targeted turns out to be SME, say so in §2.6. If a random condition existed, §2.6–2.7 must change.
2. **Singh et al. (2023)**, §3–4. Your dataset and the baselines you're positioned against.
3. **Zhao et al. (2025)**, the panel's suggestion. Know RAER's label set and why it's academic emotion, not engagement.
4. **Teotia et al. (2024)** and **Goyal et al. (2026)**. Your R2 answer.
5. **Whitehill et al. (2014)**. The r = 0.85 frame-average result, the best argument that a few frames can carry the signal.

---

## 2. Chapter 1: Introduction

### 2.1 Lesson: the inverted pyramid, and the panel's scope comment

The panel said the scope "seems to be very broad, and would benefit from a tighter narrative that narrows into the specific study". The template's inverted pyramid is the fix: one paragraph per level, each narrower than the last.

| Paragraph | Level | Content in your draft |
| :-- | :--- | :--- |
| 1 | Research area | Engagement (Fredricks), automated measurement (D'Mello), affective computing |
| 2 | Domain | Video-based learning; CHED flexible learning; webcams; datasets with observer labels |
| 3 | Synthesis of previous work | Accuracy gains came from features and networks; frame choice under-studied; two prior rule comparisons |
| 4 | Problem and question | Neither comparison can separate rule from budget or beat chance; the research question |

**Problem vs. objective.** The problem says what is *not known*. The objective says what you will *do* to find out. The problem statement must not contain your solution, and the background must not contain your objectives.

**SMART check of the objectives:**

| Obj. | Specific | Measurable | Attainable | Realistic | Time-bound |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | 10 conditions, named | Common clip set, per-clip log | Pipeline exists from the preliminary study | Extraction is the bottleneck (calendar: Dec–Jan) | Table 4.6 |
| 2 | 4 named classifiers, fixed settings | Macro F1, accuracy, MCC | Training code exists | Seeds 42–46 | Feb |
| 3 | Named tests and margin | p-values, CIs, equivalence | Analysis script exists | 5 families, Holm | Feb–Mar |
| 4 | Budget and boundaries | Family 4 and 5 tests | Same | Same | Feb–Mar |

**Scope and Limitations.** The template's rule is one paragraph per objective, each saying what is in, what is out, and **why**. The template also says: "Do not use weak excuses such as the lack of time and/or knowledge." Every exclusion in your draft has a methodological reason. For example: features are held constant so that frame selection is the only factor that changes; there is no hyperparameter search so that differences reflect selection, not tuning.

### 2.2 Claims ledger: Chapter 1

| Claim | Source | Note |
| :--- | :--- | :--- |
| Engagement's three dimensions; possible remedy; malleable | Fredricks et al. (2004) abstract | Same wording as Ch. 3 |
| Automated measurement at a finer time scale | D'Mello et al. (2017) | As in Ch. 3 |
| Affect detection is an established line of work in affective computing | D'Mello & Kory (2015) | A 90-system review supports "established" |
| CHED issued flexible-learning guidelines in 2020, including online delivery | CHED CMO No. 4, s. 2020 | **Read the CMO** to confirm it lists online delivery |
| DAiSEE accuracy 57.9% → 67.5% | Table 2.2 | |
| Velocity peaks: highest mean macro F1 for all four; significant only for one | Preliminary study (audit B1) | Approved audit wording |
| 91 / 11 / 26 participants; 4,139 vs. 3,740 clips | Ch. 4, Table 4.2; your data | |
| Participants 127, aged 18–37, labs, dorms, open spaces | Singh et al. (2023) §3 | |
| "EngageNet's documentation describes participants only by sex and age range" | Singh et al. (2023) §3 | True of the paper. Check the dataset's own documentation too |
| The second extraction pass runs once per selected frame | `src/feature_extraction.py` (second pass on selected frames only) | Code fact; no timing claimed |

---

## 3. Abstracts

**English** (229 words; limit 150–250). It has the template's four moves:
1. Motivation (sentence 1).
2. Problem (sentences 2–3, which include the preliminary result).
3. Contribution (sentence 4).
4. Methodology (sentences 5–7).

There is no results move, because this is a proposal. There are no citations, as the template requires.

**Filipino.** Not included, by your decision (5 Nov 2026).

---

## 4. Likely panel questions, with model answers

**Q1. Why EngageNet and not DAiSEE, the most-used dataset?**
DAiSEE's engagement labels are extremely skewed: only 5.7% of clips are in the two lowest levels. They came from crowd annotators, and later work has questioned their quality. EngageNet has more participants (127), three annotators with reported agreement (κ 0.73–0.79), a subject-independent split, and a more even label distribution. (§2.2)

**Q2. The panel asked about VLMs. Why didn't you use one?**
Three reasons. First, current zero-shot results for individual students' engagement are near chance: in one benchmark, κ never exceeded 0.10 on DAiSEE. Second, sending clips to a hosted model would disseminate the data, which my dataset license doesn't allow without approval. Third, the scope was already judged too broad.

But my question applies to VLMs: they also only see a handful of frames, and which ones changes their results. So my findings could inform how frames are chosen for them. (§2.4, §1.3)

**Q3. Not-Engaged is the class that matters most. Why a task that ignores it?** *(updated 10 Nov)*
There are three reasons:
1. One task keeps the study about frame selection.
2. The preliminary results that motivated the design exist only for this task.
3. A second task would double the 76 planned comparisons.

I don't hide Not-Engaged, though. For every condition I report how often Not-Engaged clips are wrongly predicted as Highly-Engaged. Detecting Not-Engaged on its own is the natural next study, once we know which frames carry information. (§1.3, §4.6.1)

**Q4. How is your work different from Resurreccion (2024)?**
Different dataset (EngageNet vs. DAiSEE) and different labels (observer-rated engagement levels vs. academic emotions). Most importantly, a different design. Resurreccion compared two rules at three frames. I compare position-based, content-based, and random rules at three matched budgets. That separates the effect of the rule from the number of frames and from chance. (§2.6–2.7)

**Before the defense:** read the thesis so you can say exactly how her Targeted rule worked.

**Q5. Why not use RAER, which the panel suggested?** *(corrected 10 Nov)*
RAER labels five academic emotions: enjoyment, neutrality, confusion, fatigue, and distraction. Its only engagement label is a coarse grouping, where "engaged" just means "not distracted", and 65% of clips are neutral. EngageNet instead has four engagement levels rated from visible behavior. RAER's method also uses scene context (phone, book), while my question is about which frames of the student carry engagement information. All my preliminary work is on EngageNet. RAER would be a good second dataset for future work. (§2.2)

**Q6. Why is a random baseline worth anything?**
Without it, "changepoint beats SME" could mean that changepoint frames are informative, or just that *any* change from fixed positions helps. If random selection does as well as changepoint, the velocity peaks add nothing beyond chance. That's a real, useful finding: it would mean simpler rules suffice. (§2.6, Table 4.3)

**Q7. Why only 3, 5, and 7 frames?**
They extend the preliminary study, which found no improvement beyond 3 frames among changepoint conditions. They also keep the question about *sparse* selection, where the choice matters most. Dense sampling and learned attention are out of scope, and I say so. (§1.3)

**Q8. Is about 70% accuracy good?**
It isn't comparable to the 58–68% four-level figures in Table 2.2: those are four-class results, while mine is binary. I don't claim state-of-the-art. The study compares frame selection rules under fixed conditions, so what matters is the *differences between conditions*, tested on the same clips. (§1.4)

**Q9. Your preliminary study used 32 participants. Why?**
The download of the training split was incomplete. It's disclosed in §4.2, and the proposed study uses all 91.

**Q10. Why call it "changepoint" if it's velocity-peak selection?**
See Chapter 3 (§3.5). With the L2 cost and one-frame windows, Truong et al.'s window-sliding discrepancy equals ½v². Be able to derive it on a whiteboard.

**Q11. What if nothing is significant?**
Then equivalence testing decides between two answers. Either the rules are equivalent within ±2 points, which means the selection rule doesn't matter at that budget, or the result is inconclusive. The interpretation table was fixed in advance, so no result is wasted and none is over-claimed. (§4.6, Table 4.3)

**Q12. At the OCE you said PELT or BOCPD. What do you use now?** *(added 10 Nov; rewritten 15 Nov)*
Both kinds of content. Velocity peaks (k-Changepoint) are kept from the preliminary study: the simplest form of window-sliding changepoint detection (Q10), which finds moments of fast movement. BOCPD (k-BOCPD) is added as a second content rule, which finds the beginnings of lasting changes. Comparing the two tells me which kind of moment carries more engagement information. PELT is not used, because it looks for the same kind of lasting change as BOCPD. See §11 for the details.

**Q13. Your data are nearly balanced. Why SMOTE?** *(added 10 Nov)*
The full training split is 4,139 vs. 3,740, so SMOTE adds about 400 synthetic Highly-Engaged clips. It makes every condition train on exactly balanced data, in the same way. In the preliminary study SMOTE had no material effect, so I don't expect it to change the comparison. Know one caveat: for the LSTM and MLP, a synthetic clip blends two real clips frame by frame, so it is not a real frame sequence. It is used only for training, never for testing.

**Q14. Your ICCE paper says X, but your manuscript says something narrower. Which is right?** *(added 10 Nov)*
The numbers are the same, but the manuscript's reading is more careful. Know these four differences:
1. **Model capacity.** The paper says the benefit "depends on model capacity". The manuscript says four classifiers can't settle that.
2. **SVM gains.** The paper says the SVM "gains least". In Table 4.5 the SVM gains *more* than the MLP and the LSTM at every *k*, so the manuscript now says the gain "did not follow the accuracy of the classifiers".
3. **Frame budget.** The paper says the drop from 3 to 7 frames was monotonic for the SVM and the Random Forest. The manuscript says macro F1 fell at each step for the SVM, MLP and Random Forest, but the MLP and Random Forest moved by less than 0.003 from 5 to 7, so only the SVM declined clearly. Both readings fit the numbers.
4. **"Six-fold variance".** The paper says "six-fold variance", but 0.0129 / 0.0022 ≈ 5.9 is a ratio of *standard deviations*. The variances differ about 34-fold.

§5.1 now says the interpretation is narrower than the paper's.

**Q15. The panel said your scope was too broad. Isn't adding temporal representations broadening it again?** *(added 14 Nov)*
The research question hasn't changed: it is still content-based vs. position-based frame selection. Temporal representation is a supporting question that my adviser asked for. It needs no new data and no new feature extraction. It only re-combines frames I already extract, and training is cheap. Its tests are kept in their own family, so they don't weaken the frame-selection tests.

**Q16. Where do your temporal representations come from?** *(added 14 Nov)*
The mean and concatenation are standard: Temporal Segment Networks average segments, and Karpathy et al. merge frame features. Frame differences come from action recognition, where TSN used them as a motion input. Self-similarity matrices come from action recognition too (Junejo et al.). I adapted the last two to three to seven selected frames, and I didn't find either used for engagement. Each one carries a different temporal aspect: none, order, amount of change, and pattern of change.

**Q17. Why pick the best configuration on the validation split?** *(added 14 Nov)*
If I picked the best of about 100 configurations by their test scores, that top score would be inflated by luck: something always comes out on top. Choosing on validation and then reporting the test score once keeps that score honest.

**Q18. Why standardize before cosine similarity?** *(added 14 Nov)*
The raw landmark coordinates are all positive and barely change between frames, so every frame vector points almost the same way and every cosine is about 1. After standardization, the values describe how each frame differs from a typical frame, so the cosine can show real similarity.

**Q19. Why threshold 3 and not another binarization?** *(added 14 Nov)*
It is the only threshold that gives two classes of about equal size, in every split (Table 5.3). At threshold 1, a model that calls every test clip "engaged" would already be 79.7% accurate without looking at the video. At threshold 3, the same model gets 50.3%. My comparisons are in accuracy points, with a ±2-point equivalence margin, so I need a task where accuracy isn't inflated by class sizes. Threshold 1 would isolate Not-Engaged clips, which matter most. I explain in §1.3 why that is a separate study, and I still report how often Not-Engaged clips are called Highly-Engaged.

**Q20. What did you do before EngageNet, in MSLABS1 to MSLABS3?** *(added 14 Nov)*
Topic exploration, related literature, dataset search, and experiments on DAiSEE; work on EngageNet began in MSLABS3. *Add in your own words why you moved from DAiSEE to EngageNet. The manuscript doesn't state a reason, so the panel may ask.*

**Q21. Isn't Chapter 5's future work just Chapter 4 again?** *(added 14 Nov)*
Chapter 4 says what the design is. Chapter 5 says in what order it will be carried out and when (Table 5.4), and gives the two core procedures as pseudocode precise enough to implement. The pseudocode for SME and k-Changepoint is the preliminary study's code; positional and random selection are still to be written.

---

## 5. Things only you can verify (before the defense)

1. **Resurreccion (2024):** what Targeted means, and whether any random or uniform condition existed. This affects §2.6 and Table 2.5.
2. **CHED CMO No. 4, s. 2020:** confirm it includes online delivery (§1.1).
3. **Abedi & Khan (2021):** pages 151–157 and the DOI came from a third-party listing. Check IEEE Xplore.
4. ~~Liao et al. (2021)~~ Done 10 Nov: 58.84% confirmed in Liao's own abstract.
5. **Preprints** (Wang 2025, Goyal 2026, Vedernikov 2025, Brkić 2025, DAiSEE): before submission, check whether any has since been published at a venue, and update the bib entry if so.
6. **ACM CCS keywords** (D7).
7. ~~**Adviser's e-mail** for Appendix B.~~ Done 14 Nov.
8. ~~**Data Privacy Act** (§4.7).~~ Decided 14 Nov: §4.7 states that the Act applies because the clips are stored and processed in the Philippines. **Be ready for:** "Doesn't Section 4 exclude research?" It lists research processing among its exceptions. Treating the Act as applying is the cautious choice, and the study's measures (storage, no images, aggregate reporting) meet it either way.
9. ~~**Before submission:** remove the red `\askadviser` question in §4.1.~~ Removed 14 Nov at Dr. Azcarraga's request.
10. **Ask Dr. Azcarraga about "PCA exploration / time series represented as 2D".** Two possible readings:
    - project each frame to two numbers with PCA, so a clip becomes a path you can plot;
    - the self-similarity matrix, which is itself a 2-D picture of a clip.

    Nothing is in the manuscript yet (D26).
11. **D25 rule:** ~~confirm "reliably better in at least half of the ten conditions and worse in none", or choose another rule.~~ Settled on 15 Nov: replaced by replicability analysis (D51, §12).
12. **The 2025 frame-differencing engagement paper** (Neural Computing and Applications, doi 10.1007/s00521-025-11317-z): a search summary said it found that differencing landmark frames helped. I couldn't open it, so it is **not cited**. If your library has access, check it; it would be a direct engagement precedent for "mean + change".

---

## 6. Reading plan (about 4 hours, in priority order)

| Order | Reading | Time | Why |
| :-- | :--- | :--- | :--- |
| 1 | Your PDF, Ch. 1 → 2 → 3 → 4 in order | 90 min | Comment as you go. That's the list you'll send me |
| 2 | Resurreccion (2024), Ch. 3–4 | 45 min | Q4; affects §2.6 |
| 3 | Singh et al. (2023), §3–4 | 30 min | Q1, your dataset |
| 4 | Zhao et al. (2025) | 30 min | Q5; the panel's own suggestion |
| 5 | Truong et al. (2020), §5.2.1 | 15 min | Q10 derivation |
| 6 | Teotia et al. (2024) | 20 min | Q2 |
| 7 | Whitehill et al. (2014), abstract and §on frame vs. clip labels | 15 min | §2.1 claim |

---

## 7. Answers to your 10 Nov review comments

Each entry answers your question in plain words. **Changed** says what changed in the manuscript. Section numbers are from the 10 Nov PDF.

### Abstract

**What is an equivalence test?**
A normal significance test asks "is there a difference?" A large *p*-value only tells you that no difference was detected. Maybe there is none, or maybe the test set was too small to see it. An equivalence test asks the opposite question: "is the difference small enough to ignore?"

You first choose a margin, here ±2 accuracy points. Then you compute the 95% confidence interval of the accuracy difference. If the whole interval lies between −2 and +2, the two rules are called equivalent.
- A difference of 0.5 with an interval of −0.9 to +1.9 is *equivalent*.
- An interval of −0.9 to +2.6 is *inconclusive*, because the true difference could be larger than 2.

**Changed:** the abstract explains it in one clause, and §4.6.4 is rewritten.

**What is "a two-point accuracy margin fixed in advance"?**
The margin is the smallest difference you would care about. Two percentage points of accuracy is about 40–45 test clips. "Fixed in advance" means it was chosen before any results were seen, so it can't be picked to make a result look the way you want. Why 2 points is explained under Chapter 1 below. **Changed:** the abstract now says "a margin set before any results are seen."

### Chapter 1

**"Attracted attention … malleable" sounded AI-written.**
You were right to flag it. It was a close paraphrase of Fredricks et al.'s abstract ("a possible antidote to declining academic motivation and achievement", "presumed to be malleable"). **Changed:** §1.1 now says in plain words that engagement responds to the classroom, such as the task and the teacher's support, "which is one reason to measure it". The same phrase was removed from §3.2.

**The semicolon in the DAiSEE sentence.** **Changed:** split into two sentences. I also removed the other prose semicolons in Chapters 1, 3 and 4. Semicolons inside tables stay.

**What is the Matthews correlation coefficient (MCC)?**
MCC is one number for how well predictions agree with the true labels, using all four cells of the confusion matrix (TP, TN, FP, FN).
- **Range:** +1 is perfect, 0 is no better than chance, and −1 is always wrong.
- **Why not just accuracy:** accuracy can look good when a classifier mostly predicts the bigger class. MCC is high only when *both* classes are predicted well.
- **For binary labels:** MCC equals the Pearson correlation between predictions and labels. The "PCC" in your preliminary tables *is* the MCC.

**Changed:** Objective 2 points to §3.7, where it is defined.

**What is Holm–Bonferroni correction?**
If you run 12 tests at the 0.05 level, the chance that at least one gives a false positive is much higher than 5%: about 46% if the tests are independent (1 − 0.95¹²). Holm's procedure gives each test a stricter pass mark:
1. Sort the *p*-values from smallest to largest.
2. The smallest must beat 0.05/12, the next 0.05/11, and so on.
3. Stop at the first one that fails. It and all later ones are not significant.

**Changed:** §3.6 now has a three-test worked example.

**Why five training seeds or random draws?**
One training run can be lucky or unlucky:
- A neural network gives a slightly different result each time it is trained with a different seed.
- Random selection gives different frames on each draw.

In your preliminary study, the one "significant" LSTM result came from seed 42 and reversed direction in 3 of the 5 seeds. Repeating each comparison five times, and calling a difference reliable only if it is significant in all five, guards against this. Five matches the preliminary study. Be honest if asked: five runs give only a rough estimate of spread.

**Why ±2 accuracy points?** Three reasons, all from the preliminary study (§4.6.4):
1. Retraining the LSTM with different seeds moved its accuracy by up to 1.3 points (SD). A smaller effect of frame selection would be lost in that variation.
2. A confidence interval for an accuracy difference on this test set is about 2.8 points wide (±1.4). Equivalence needs the *whole* interval inside the margin, so a margin much below 1.5 could almost never be confirmed.
3. The significant effects you found were 2.39–4.79 points. A 2-point margin won't call differences of that size "equivalent".

**"The activities that carry out these objectives…": required? In the template?**
No to both. I added it. The template's own comment says activities such as literature review, programming and documentation "must not be included" among the objectives. **Changed:** deleted.

**Does this mean OpenFace action units (FAUs) are not used? Why blendshapes?**
Yes, OpenFace AUs are not used. The reasons are practical:
- The preliminary study used MediaPipe.
- MediaPipe gives both the landmark positions that *k*-Changepoint needs (to compute velocity) and the classifier features.
- Your variable is frame selection, so the features must stay fixed. Switching extractor would be a second change.

Are blendshapes *better*? That hasn't been shown. OpenFace estimates AU intensities with models trained on data coded by FACS experts, and the EngageNet baselines used OpenFace. That is a fair point for the panel to raise. **Changed:** §1.3 and §3.3 now give the reason and state the limitation. Panel answer: "I hold the features fixed because my variable is frame selection. Whether the results hold with OpenFace AUs is a natural follow-up."

**Is it using BOCPD?**
No. *k*-Changepoint keeps the *k* highest peaks of smoothed landmark velocity, and the code has no BOCPD (`AGENTS.md` says so too). Your OCE slides (slide 26 and backup B20) said "PELT (whole clip) or BOCPD (live, frame by frame)", so the panel may remember it. **Changed:** §1.3 and §3.5 now name PELT and BOCPD as not used. See Q12. **Update 15 Nov:** BOCPD is now a fifth rule, k-BOCPD (§11). The code still has no BOCPD; you will write it in December.

**Not-Engaged is the most important. Why isn't it included?**
Your decision (D13). The reasons are in Q3. Some numbers to know:
- Not-Engaged is 18% of EngageNet. Barely-engaged (12%) is actually smaller.
- Detecting Not-Engaged on its own would be an 18:82 task with its own imbalance problem.

**Changed:** §1.3 gives three reasons. §4.6.1 adds a per-level breakdown showing how often Not-Engaged clips are called Highly-Engaged (D19).

**"Fixed default settings and no hyperparameter search … End-to-end deep networks … not included": what does this mean?**
Every classifier has settings (hyperparameters), such as the learning rate, the number of trees, or the SVM's C. *Tuning* means trying many values and keeping the best. If you tuned separately for each condition, a better result might come from luckier tuning rather than better frames. So every condition uses the same untuned settings.

*End-to-end* networks (e.g., a CNN on raw pixels) learn their own features from the images. Using them would change the features as well as the frames, which breaks the "only the frames change" design. **Changed:** §1.3 says this in these words.

**Vision-language models: can you cite specific numbers?**
**Changed:** §1.3 now cites two results:
- **Goyal et al. (preprint):** across five models, agreement with individual students' labels never exceeded Cohen's κ 0.10, and 85–100% of clips were assigned to one level.
- **Teotia et al.:** models that recognized basic emotions well still confused engaged and distracted behavior.

**Add "directly" to "felt or thought".** **Changed.**

**Report processing time? Do the dates need to be specified?**
**Changed (D16):** processing time is now reported. That is the second-pass extraction time per clip for each condition, plus training time, measured on one computer, descriptive only. The dates are not needed in the scope, because the calendar (§5.3) has them, so they were removed.

### Chapter 1.4

**"All fixed before the experiments are run": is it necessary?**
I kept it (D20), because it is the point of the protocol. If you choose the tests, the margin and the interpretation *after* seeing results, you can, even without meaning to, choose the ones that make your favorite rule look good. Fixing them first prevents that, and it is your strongest answer to R4. **Changed:** reworded as "set before any results are seen, so the analysis cannot be adjusted to fit the results."

### Chapter 2

**RAER: should the panel be named? Use RAER instead? Does it measure engagement? Isn't engagement an academic emotion?**
- **Naming the panel:** no. A manuscript doesn't credit the panel's suggestions in its text. That mapping belongs in `revisions-summary.md`, where it already is. **Changed:** removed.
- **Use it instead:** no. RAER has 5 academic emotions, about 2,700 clips of 5–15 s, and 65% "neutrality". Its train/test split was only made "striving to exclude overlapping individuals", which is not a guarantee of subject independence. All your preliminary work is on EngageNet. It is a good candidate for future work.
- **Does it measure engagement:** partly. My draft missed this, and I corrected it. RAER also has a coarse two-way label: *distracted* (= distraction) vs. *engaged* (= enjoyment, neutrality, confusion or fatigue). So "engaged" there means "not distracted". It does not provide engagement *levels* rated from behavior.
- **Engagement as academic emotion:** see Chapter 3 below.

**Changed:** §2.2 and Table 2.1 now give RAER's real labels and its 5–15 s clip length.

**"Datasets differ and results on one need not hold on another" sounded AI.** **Changed:** "The datasets in Table 2.1 were recorded in different settings, with different people and labels, so a result found on EngageNet may not hold on the others."

**Table 2.2 footnotes a and b: check them.**
- **a (Liao, 58.8%):** now confirmed in Liao's own abstract (Applied Intelligence 51(10), 6609–6621). I removed the footnote, since it is no longer second-hand.
- **b (TCCT-Net):** I checked the paper. It reports **68.91% on the EngageNet *validation* split**, using two head-pose signals. Singh's 67.6% is on the *test* split, so the two are not like-for-like. The table now shows 68.9 with a footnote saying exactly that. My earlier text, "exceeded the EngageNet baselines", was too loose. TCCT-Net beat the baselines in *its own* table, all on validation.

**Teach me about MARLIN and TCCT-Net.**
- **Singh et al.'s baseline:** OpenFace features (gaze, head pose, action units) go into a Transformer, giving 67.6% on test.
- **MARLIN** (Cai et al., CVPR 2023) is a model pretrained on many *unlabeled* face videos. It learns by hiding parts of the video and filling them in (a masked autoencoder). The result is a general-purpose vector describing a face video. Adding MARLIN's vectors to the OpenFace features gave 66.5%, slightly *lower*. The big generic features didn't help here.
- **TCCT-Net** (Vedernikov et al., CVPRW 2024) uses just two head-pose rotation signals as time series, in two streams:
  - one models the signals over time with convolution and a Transformer;
  - the other turns them into a time–frequency picture (wavelet transform).
  
  The two are fused, giving 68.91% on validation. It is fast because it never processes images: inference on the whole validation set took 2.59 s, against 61–97 s for image-based recurrent networks. That figure doesn't count the time needed to extract the head-pose signals.
- **The lesson for your study:** a few well-chosen signals can match many. That is the same spirit as a few well-chosen frames.

**"Two limitations of this body of work bear on the present study" sounded AI.** **Changed:** sentence deleted. The paragraph now states the two points directly.

**"Frame selection is treated as preprocessing rather than as a factor whose effect is measured": explain.**
*Preprocessing* means the steps done to the data before the model sees it. They are usually chosen once and not questioned, like resizing images. Each paper picked one way to handle frames (50 frames; 20 segments) and never tried another. So nobody knows how much that choice changes accuracy, and that is exactly your question. **Changed:** a plain "In other words…" sentence replaces it.

**What is a preprint?**
A paper posted publicly, usually on arXiv, before peer review or without it. You may cite it, but it carries less weight, so it is labeled "(preprint)" in Table 2.3 and the text. Before submission, check whether each one has since been published (§5).

**CLIP-CAER: what does that sentence mean?**
CLIP is a model trained on millions of image–caption pairs. It puts pictures and sentences in the same "space", so it can score how well a picture matches a sentence. CLIP-CAER works like this:
1. It writes a short text description for each academic emotion, saying what the face and the setting look like.
2. It adds a few *learnable* words to each description.
3. It labels a clip with the description it matches best.

It looks at the face crop *and* the whole frame, so context like a phone or a book counts. On RAER it reached a 68.0% unweighted average recall (the mean recall across classes). The best video facial-expression method built for basic emotions, such as happy or angry, reached 61.2%. **Changed:** the sentence is rewritten in these terms, with the numbers.

**Don't say "recur".** **Changed:** "The works reviewed here follow one of two ideas, or combine them."

### Chapter 3

**"Fixes": the right word?** No. **Changed:** "defines".

**Is engagement not an emotion? I understood it as an academic emotion, as in DAiSEE.**
Both usages exist. That is exactly why R1 asked for working definitions:
- **Affective computing.** DAiSEE calls boredom, confusion, engagement and frustration "user affective states". D'Mello's 2013 meta-analysis of learning with technology counts "engagement/flow" among the discrete affective states students experience, and it was consistently one of the most frequent. RAER even groups four emotions under "engaged".
- **Educational psychology.** Fredricks et al. treat engagement as a broader construct with behavioral, emotional and cognitive dimensions; emotions are *part* of emotional engagement. Pekrun's academic emotions (enjoyment, boredom, anxiety, …) do not include engagement. Emotions are seen as influencing it.
- **Why the manuscript follows Fredricks:** EngageNet describes its levels by attention and behavior (glancing away, fidgeting, "glued to the screen"), plus visible interest. That matches behavioral engagement more than a felt emotion.

**Changed:** §3.1 now names the affective-state usage (DAiSEE, D'Mello 2013) and says why this study uses Fredricks. Panel answer: "In affective computing, engagement is often treated as an affective state, as in DAiSEE. I use Fredricks' definition because EngageNet's labels describe attention and behavior. §3.1 notes both."

**§3.2 "attracted attention" sentence.** **Changed:** rewritten. It now says only what the manuscript needs: Fredricks recommended studying the three dimensions together.

**Blendshapes vs. OpenFace AUs: which is better?** See the Chapter 1 entry. **Changed:** §3.3 states the reason and the limitation.

**Define fidgeting.** **Changed:** "fidgeting, that is, small restless movements such as shifting in the chair". EngageNet's own wording is "fidgets restlessly in the chair".

**Sports1M sentence sounded AI.** **Changed:** the numbers were in both §2.5 and §3.4. §3.4 now just says the sampler made the classifier "both more accurate and much cheaper to run". §2.5 keeps the checked numbers in plain words: +7% accuracy, more than 15 times cheaper.

**"Piecewise stationary": in simpler words.**
The signal is made of stretches where it behaves steadily, for example a still face, then a moving face, with sudden switches between them. Changepoint detection finds the moments of switching. **Changed:** §3.5 opens with exactly this.

**"Equation 4.1": shouldn't it be 3.1?**
The reference was correct but confusing. Equation 3.1 is the discrepancy Z_t itself. The velocity v_t is defined later, in Chapter 4, as Equation 4.1. **Changed:** the text now says in words what v_t is ("the distance the landmarks move between the two frames") and points to Section 4.4.

**What does "discrepancy" mean here?**
It measures how different the "before" window and the "after" window are. It is the cost of treating them as one segment, minus the cost of treating them separately, where cost is the sum of squared distances from the mean.

Tiny example: before = 0 and after = 2, one value each.
- Separately, each costs 0.
- Merged, the mean is 1, so the cost is (0−1)² + (2−1)² = 2.
- The discrepancy is 2, which is ½·(2−0)²: half the squared velocity.

*Update 10 Nov:* the equation for this (old Equation 3.1, Z_t = ½v_t²) was dropped at your request. §3.5 now makes the same argument in words. The ½ comes from each frame being half the gap away from the pair's mean, and it doesn't change which frames peak.

**Is window sliding needed in such detail?**
Only the core matters. It is the bridge that justifies calling the rule "changepoint" (Q10). **Changed:** I cut the taxonomy (cost function, search method, constraint). I kept one plain paragraph on window sliding, the equation, and the paragraph on the name's limit.

**RBF kernel: what does "curved boundary" mean?**
A plain SVM separates the classes with a straight line, or a flat surface when there are many features. The RBF kernel judges two clips as similar when their features are close, which lets the boundary bend around groups of examples. **Changed:** this gloss is in §3.6.

**McNemar: in simpler words.**
Only clips where the two classifiers *disagree* tell you which is better. If both were equally good, each disagreement would be a fair coin toss. Suppose they disagree on 100 clips and classifier A wins 60:
- A 60–40 split or a more uneven one happens with probability ≈ 0.057 under fair coins, so it is not significant.
- At 61–39 it would be ≈ 0.035, which is significant.

**Changed:** §3.6 is rewritten with this example.

**Holm: in simpler words.** See Chapter 1 above. **Changed:** §3.6 now has a worked example. With three tests the pass marks are 0.0167, 0.025 and 0.05. Sorted *p*-values of 0.01, 0.03 and 0.04 give one significant result.

**Bootstrap: what is its use here?**
It gives the 95% interval of the *accuracy difference* between two conditions, which the equivalence test needs. The procedure:
1. Resample the 2,005 test clips with replacement 10,000 times.
2. Recompute the difference each time.
3. Take the 2.5th and 97.5th percentiles.

**Changed:** §3.6 says this.

### Chapter 4

**4.1 PENDING marker.** **Changed:** it is now a red "[Is this scope good enough for the proposal?]", using a new `\askadviser` macro. Remove it before submission (§5, item 9).

**Table 4.2 footnote (91 vs. 90 participants): what does it mean?**
I counted the distinct participant numbers in the training label file, using names like `subject_8_…`, and found 91. Singh et al. say 90. Three numbers (67, 99 and 101) each appear with two session codes, so some people may have recorded twice. That doesn't explain the gap, though. **Changed:** the footnote now says the source of the difference is unknown, and the session-code detail is dropped.

**4.2.3, 222 clips.** **Changed:** deleted, along with the sentence before it.

**4.3, software versions.** **Changed:** deleted. "Three changes" is now "Two changes", and the second now also logs timing (D16).

**The positional formula f_{⌊(j−½)n/k⌋+1}.**
Here n is the number of valid frames and k the number to keep. Split the frames into k equal parts. (j−½)·n/k is the middle of part j; the floor and the +1 turn it into a frame number. Example with n = 20 and k = 3:
- j = 1: 0.5·6.67 = 3.33, giving frame 4.
- j = 2: 1.5·6.67 = 10, giving frame 11.
- j = 3: 2.5·6.67 = 16.67, giving frame 17.

So the positional rule keeps frames 4, 11 and 17. SME would keep 1, 11 and 20. **Changed:** the plain-words version is added after the formula.

**The velocity formula.**
- p̃ is each landmark's position minus the average position of all 478 landmarks in that frame. This "centering" removes movement of the whole face across the image.
- v_t is the square root of the summed squared distances that the 478 centered landmarks move from frame t to t+1. In other words, it is how much the face's shape changed between consecutive frames.
- A large v_t means fast facial movement: talking, blinking, or turning the head.

**What is smoothing?**
A 5-frame moving average replaces each value with the mean of itself and two neighbors on each side. Example: 0, 0, 10, 0, 0 becomes 2 in the middle. A one-frame spike, such as tracking jitter, is flattened, while sustained movement stays high. **Changed:** the gloss is added in §4.4. The code confirms it (`np.convolve(…, np.ones(5)/5, mode='same')`).

**"The name k-Changepoint is retained…".** **Changed:** deleted.

**SVM C = 1, γ = "scale": what does it mean?**
- **C** trades off two goals. A large C fits the training data tightly, with a narrow gap and a risk of overfitting. A small C keeps a wider gap and tolerates some training errors.
- **γ** sets how far one training example's influence reaches. "scale" sets it automatically from the data (1 / (number of features × variance of the features)).

Both are scikit-learn defaults, i.e., untuned. **Changed:** the gloss is added in §4.5.

**SMOTE (your decision, D12).**
SMOTE makes synthetic examples of the smaller class by placing new points between a real example and one of its 5 nearest same-class neighbors, until the classes are equal in size.
- **Where it runs:** on the training split only, after the common clip set is fixed. For the SVM and Random Forest it works on the standardized frame averages. For the LSTM and MLP, each sequence is flattened (with its number of real frames), interpolated, and restored, so a synthetic clip blends two real clips frame by frame. Random state 42. This matches `src/train.py` and `src/train_traditional.py`.
- **Numbers to know:** the full split is 4,139 vs. 3,740, so about 400 synthetic Highly-Engaged clips. In the preliminary study SMOTE had no material effect. See Q13.

**Changed:** §1.3, §4.2 (comparability), §4.5, and Figure 3.1's "held constant" box.

**LSTM readout: explain.**
The LSTM gives one output per frame, and these must be combined into one prediction for the clip. The current setting *averages* them. In an earlier side comparison, letting the network learn how much weight to give each frame (*attention*) was 2.04 points better on average over 20 runs, but that wasn't tested for significance. That comparison was made on the **test** split, which should only be used once, at the end. Choosing a setting from test results is a form of peeking. So the choice between averaging and attention will be made on the **validation** split, before any test results. **Changed:** §4.5 is rewritten in these words.

**MSE = error rate: what does it mean?**
With labels and predictions of 0 or 1, each wrong prediction has squared error 1 and each correct one 0. The mean is therefore the fraction wrong, which is 1 − accuracy. Class-wise MSE is the error rate within a class, which is 1 − that class's recall. MSE adds nothing new, so it's reported (for continuity with your older runs) but not interpreted. **Changed:** §4.6.1 explains this.

**What is a paired bootstrap?**
Each resample draws the *same* clips for both conditions, so their difference is always measured on identical clips. That keeps the pairing, just as McNemar does. **Changed:** a one-sentence gloss is added in §4.6.2.

**Seed vs. draw?**
- A **seed** fixes the randomness of *training* a neural network (starting weights, batch order).
- A **draw** fixes which frames random selection picks, which changes the *features*.

SVM and RF have no seeds, but they still have 5 draws under random selection. For an LSTM on random selection, seed *i* is paired with draw *i*. **Changed:** both are defined at the start of §4.6.3.

**Equivalence (4.6.4): explain simply.** See the Abstract entry above. Every comparison ends in one of three outcomes:
1. a **reliable difference** (significant in all 5 runs);
2. **equivalent** (the whole interval within ±2);
3. **inconclusive** (neither).

**Changed:** §4.6.4 is rewritten around these three outcomes and the three reasons for ±2.

*Update 14 Nov:* there are now **four** outcomes. A difference can be reliable and still sit inside ±2, which happens when two configurations disagree on few clips. That result is called "a reliable difference smaller than the margin": real, but too small to matter. With five seeds or draws, equivalence must also hold in all five.

**5.1 McNemar paragraph: simpler.**
1. Only the Random Forest improved significantly over SME, at all three *k*.
2. Gains didn't line up with how accurate the classifiers were. The weakest (RF) gained most, but the strongest (SVM) did not gain least.
3. The one significant LSTM result is a single-seed fluke: it reversed in 3 of 5 seeds.

**Changed:** §5.1 now makes exactly these three points. The frame-budget sentence is also corrected: macro F1 fell at each step for the SVM, MLP and RF, but only the SVM clearly. Also added:
- §5.1 now says the study was published as Sityar and Azcarraga (2026).
- Tables 4.4 and 4.5 are marked "Adapted from…", which your APSCE copyright agreement requires.
- The interpretation is stated as narrower than the paper's (Q14).

**Why "proponent"?**
DLSU's templates and ethics forms use it for the student proposing the thesis. It's fine to keep. "The researcher" would also work, but keep one term throughout.

**Data Privacy Act: does it apply if the data weren't collected in the Philippines?**
Good catch. My draft was wrong to say flatly that the clips "are personal information under" the Act. Section 4 of the Act excludes from its scope, among others:
- personal information processed for research purposes;
- personal information collected from residents of other countries under those countries' laws and processed in the Philippines.

EngageNet's paper doesn't say where participants were recorded. The authors are at IIT Ropar (India) and KDDI Research (Japan), and participants used a web platform from wherever they were. **Changed:** §4.7 now says the clips are *treated* as personal information, that whether the Act applies in full is uncertain, and that the ethics review will settle it. The safeguards apply either way. Ask Dr. Azcarraga or the ethics office (§5, item 8).

**Ethics-review sentence: necessary?**
Yes. The DLSU template includes Appendix A (Research Ethics Documents), and General Checklist Q1 ("human participants, new or pre-existing data") is Yes, which triggers Checklist A. **Changed:** shortened to one sentence.

**5.3 Calendar: leave time for revisions after the final defense.** **Changed (D15):**
- Statistical analysis: Feb •, Mar •.
- Writing: Mar •••.
- Final defense: Apr •.
- Post-defense revisions and submission: Apr •••.

It all stays within Term 2, so the ethics-form duration (Nov 2026 – Apr 2027) still holds.

*Superseded on 14 Nov (D32, D33):* the calendar is now Table 5.4 in §5.3, running from MSLABS1 to March 2027, with one bullet per term or month. The final defense is in late March (§9).

---

## 8. Dr. Azcarraga's 13 Nov objectives comments

### 8.1 Why the objectives are now general

Objectives say *what* the study will achieve. Scope and Limitations says *how far* and *with what*. Your adviser's EEG example uses broad verbs (build, recommend, implement, characterize, assess) and keeps the details out. Every detail removed from §1.2 now lives in §1.3:

| Removed from the objectives | Now in |
| :-- | :-- |
| velocity peaks, random selection, k = 3, 5, 7, the ten conditions | §1.3 "Frame selection" (was "Features and frame selection") |
| the four classifier names, macro F1, accuracy, MCC, subject-independent test split | §1.3 "Task and classifiers" (the classifier names are now introduced in "Data preparation") |
| the four ways of combining frames, and the LSTM readouts | §1.3 "Data preparation" (was "Frame combination"; see §9) |
| McNemar, Holm, five seeds or draws, ±2 equivalence, best configuration chosen on validation | §1.3 "Evaluation" |
| including the first and last frames (old Objective 4) | §1.3, SME vs. positional at k = 3 |

The old Objective 4 (frame budget and clip boundaries) is now part of Objective 2, "characterize frame selection techniques" (renumbered 14 Nov at the adviser's request).

### 8.2 Lesson: representing the temporal aspect of frames

Take three selected frames with two features each: A = (1, 0), B = (0, 1), C = (1, 0). The face moved, then came back.

| Representation | Result | What it carries |
| :-- | :-- | :-- |
| Mean | (0.67, 0.33) | What the frames look like on average. No temporal information. |
| Concatenation | (1, 0, 0, 1, 1, 0) | Everything, in order. The classifier must work out what the order means. |
| Mean + change | mean, then (1, 1) | How much each feature changes between neighbors: \|B−A\| = (1, 1), \|C−B\| = (1, 1), averaged. |
| Mean + self-similarity | mean, then (0, 1, 0) | Cosines of A–B, A–C and B–C. The 1 for A–C shows the face **returned** to where it started. |

**Shuffle test.** Reorder the frames as A, C, B:
- **Mean:** unchanged.
- **Concatenation:** (1, 0, 1, 0, 0, 1).
- **Change:** (0.5, 0.5).
- **Self-similarity:** (1, 0, 0).

Only the mean ignores order, which is why it is the "no temporal information" baseline.

**Why self-similarity ties back to your method.** §3.5 admits that velocity peaks can't tell a quick head turn that comes back from a lasting change. Self-similarity can: a high first–last similarity means the face returned.

**Two rules you must be able to explain:**
1. **Only the selected frames are used.** Neither the velocity signal nor the frame timestamps feed into these representations. Otherwise k-Changepoint would sneak in information from frames it didn't select, and the comparison of selection rules would be unfair.
2. **Standardize first (Q18).** Raw cosines are all about 1.

**An honest limitation.** In the SVM, the 3 to 21 similarity values sit beside 1,518 features. Because the SVM measures distance over the whole vector, they may barely count. The Random Forest and MLP can give them more weight. The manuscript says this in §4.5.

### 8.3 What changed in the manuscript (14 Nov)

- **Ch. 1:**
  - new general objective and five objectives;
  - §1.3 restructured, with a new "Frame combination" paragraph;
  - one sentence in §1.1 adding the secondary question;
  - §1.4 rewritten to follow Table 4.3, with sentences on temporal representation and the best configuration.
- **Ch. 2:**
  - new **§2.7 "Temporal Representation of Frames"**: Karpathy 2014, Ng 2015, TSN, Junejo 2011, Singh, Abedi 2021/2024, Meng, and your preliminary readout result;
  - **Abedi & Khan (ICPR 2024)** added to Table 2.2, Table 2.4, §2.3 and §2.6. It uses MediaPipe landmarks on EngageNet, reaching 71.2% on validation, and sparser frame sampling lowered accuracy only slightly. **Read it:** it is the closest work to your feature set.
  - Synthesis renumbered to §2.8.
- **Ch. 3:**
  - definitions of *frame combination* and *temporal representation*;
  - new **§3.6** with the toy example above;
  - the LSTM-vs-MLP paragraph softened to "descriptive indication";
  - Figure 3.1 gains the frame-combination variable.
- **Ch. 4:**
  - §4.1 design and Figure 4.1 updated;
  - §4.5 defines the four combinations, the standardization rule and the SVM limitation;
  - both LSTM readouts are now run, replacing the "choose on validation" paragraph and resolving the tuning conflict;
  - family 6 added (100 tests, 176 in total);
  - new §4.6.6 Best Configuration;
  - calendar row renamed.
- **Abstract:** one sentence on temporal representation, still 250 words.

**Review fixes from 10 Nov applied in the same pass:**
- class counts in the right order;
- §5.1 now says what the preliminary study did differently;
- the equivalence gaps (four outcomes; all five versions);
- the positional rule's first/last frame exception (n ≤ 2k);
- the number of frames kept is reported;
- §1.4 aligned with Table 4.3, and the velocity-cost claim dropped;
- D'Mello & Kory reworded;
- VLM definition now includes CLIP;
- EngageNet annotators described accurately ("three annotators", majority vote, expert tie-break; "trained" removed);
- cognitive engagement "gauged through a brief questionnaire", which is EngageNet's own wording;
- the `_neutral` blendshape;
- the PELT/BOCPD reason;
- the VLM future-work sentence;
- semicolons in prose;
- the signpost sentences ("Three points stand out", "…bear on…", "supports four observations", "Two points connect…");
- the repeated "neither included random selection" sentence varied;
- §4.3's duplicate blendshape text cut;
- the 127/128 pointer;
- "four reasons" in §2.2;
- the §4.6.3 label.

**Still open:**
- item 12, smoothing at the clip edges in `feature_extraction.py`;
- item 13, extraction workload (random draws make up about 69% of the second-pass frames).

---

## 9. Dr. Azcarraga's 14 Nov notes

Her three notes:
1. §1.3: add a "Data preparation" paragraph on how the frames will be aggregated.
2. Add a Chapter 5 for preliminary results and future work: the specific steps within the thesis, the algorithms, and the binarization approach.
3. Gantt chart from MSLABS1 to March 2027, including the preliminary experiments and the RRL.

### 9.1 What changed in the manuscript (14 Nov)

- **§1.3:**
  - "Frame combination" became **"Data preparation (Objectives 1 and 3)"**. It walks a clip through, in order: SNP removed, labels binarized, valid frames, selection, MediaPipe features (the OpenFace rationale moved here), combination into one input, standardization, and SMOTE on training only.
  - The classifier names are introduced there.
  - "Features and frame selection" became **"Frame selection (Objective 2)"**.
  - Each fact now appears once in §1.3.
- **Ch. 4:**
  - the old §4.7 (preliminary results) and §4.9 (calendar) moved to Chapter 5;
  - Ethics is now §4.7;
  - the intro points to Chapter 5;
  - §4.2.2 points to §5.2.3.
- **New Ch. 5, "Preliminary Results and Future Work":**
  - §5.1, the preliminary results, word for word except for one cross-reference ("described above" became "described in Chapter 4");
  - §5.2.1, the remaining steps (ten numbered steps; seven since §9.5);
  - §5.2.2, Algorithms 5.1 (frame selection) and 5.2 (training and evaluation);
  - §5.2.3, the binarization approach with Table 5.3;
  - §5.3, the calendar as a Gantt chart (Figure 5.1, on a landscape page; now Table 5.4, see §9.5).
- **Preamble:** `algorithm`, `algpseudocode` (`pgfgantt` and `pdflscape` were added for the Gantt chart and removed with it).

### 9.2 Lesson: why threshold 3 (Table 5.3)

A threshold *t* makes levels ≥ *t* positive. These counts are from the official label files (`data/labels/`), counted on 14 Nov with SNP clips removed. They are dataset counts, not results, and the totals match Table 4.2.

| Split | Clips | Negative at t = 1 | t = 2 | t = 3 |
| :-- | --: | --: | --: | --: |
| Training | 7,879 | 1,446 (18.4%) | 2,481 (31.5%) | 4,139 (52.5%) |
| Validation | 1,071 | 132 (12.3%) | 229 (21.4%) | 502 (46.9%) |
| Test | 2,256 | 457 (20.3%) | 703 (31.2%) | 1,122 (49.7%) |

**Majority-class baseline.** A "classifier" that always predicts the larger class scores that class's share as its accuracy. On the test split:
- At t = 1, 1,799 of 2,256 clips are engaged: 79.7%.
- At t = 3, 1,134 of 2,256 clips are Highly-Engaged: 50.3%.

So 70% accuracy means very different things at the two thresholds. Your comparisons and your ±2-point margin are in accuracy points, which is why a balanced task matters.

**Why the early threshold 1 and 2 runs aren't reported.** They are Runs 5–10 in your MSLABS4 week 9 notes. They were made before the common clip set was introduced (the 5 Aug fix), and they label the changepoint method "BOCPD", which was never implemented. Don't cite them. The manuscript says only that they were exploratory and are not reported.

### 9.3 Lesson: reading the two algorithms

**Algorithm 5.1 (frame selection).** Try it with n = 20 valid frames and k = 3:
- **SME:** f₁, f₁₁, f₂₀.
- **Positional:** j = 1 gives ⌊0.5 · 20/3⌋ + 1 = 4; j = 2 gives ⌊1.5 · 20/3⌋ + 1 = 11; j = 3 gives ⌊2.5 · 20/3⌋ + 1 = 17. So f₄, f₁₁, f₁₇.

The two share the middle frame. SME takes the clip boundaries, and positional doesn't. That difference is exactly what family 5 tests.

- **k-Changepoint:** there are n − 1 velocities, one per pair of neighboring frames.
  - The returned frame f_t is the *first* frame of the pair whose smoothed velocity peaked. That is what the code does (`valid_indices[p]`).
  - Item 12 (edge smoothing; which frame of the pair to keep) is still open, and the pseudocode records the current behavior.
- If the smoothed velocity had no local maximum at all, the clip would get no frames and would drop out of the common set. This is unlikely, because smoothing pulls the edges down, but it is why every exclusion is logged.

**Algorithm 5.2 (training and evaluation).** One "version" per seed or draw:
- **Neural network on a fixed rule:** 5 seeds.
- **Random rule:** 5 draws. With a neural network, seed i is paired with draw i, so it is still 5 runs, not 25.
- **SVM or RF on a fixed rule:** 1 run.

My count of training runs, not stated in the manuscript:
- LSTM (2 readouts) and MLP (4 combinations): 6 × 10 conditions × 5 = 300 runs.
- SVM and RF (4 combinations each): 8 × (7 fixed conditions + 3 random × 5 draws) = 176 runs.

That is 476 runs in total, each a few minutes or less.

### 9.4 The calendar (Table 5.4): sources and what you should check

The dates below are those of the Gantt chart. Table 5.4 marks the same activities by term or month, so a row that ends in early September (preliminary experiments) still gets a September bullet. The two preliminary-study rows are now called "Preliminary feature extraction" and "Preliminary experiments".

| Row | Dates | Source |
| :-- | :-- | :-- |
| Topic exploration, dataset search, DAiSEE experiments | May 2025 – Apr 2026 | Your answers (MSLABS1–3) |
| Review of related literature | May 2025 – Oct 2026 | Your answers; MSLABS4 notes (DAiSEE papers, ViBED-Net); OCE |
| EngageNet access | Jan – Jun 2026 | Your answer (MSLABS3); notes week 7 (EULA signed, download link) |
| Preliminary study: feature extraction | mid-Jun – mid-Jul 2026 | Notes weeks 7–8 ("took almost one week") |
| Preliminary study: experiments and analysis | Jul – 7 Sep 2026 | Notes week 9; commits 5–6 Aug (corrected protocol, tests), 7 Sep (timing benchmark) |
| Paper writing and submission | Aug – Sep 2026 | Paper sources committed 7 Sep |
| Oral comprehensive examination | Oct 2026; diamond on 29 Oct | OCE panel report |
| Planned rows | Nov 2026 – Mar 2027 | The old calendar, about two weeks shorter |

**Please check:**
1. **T3 2025–26 has no course label.** Your notes call that period "MSLABS4", and you said MSLABS4 is Thesis Writing 1. But the flowchart puts Thesis Writing in T1 2026–27, and the notes (EULA, extraction, first results) were all written by 18 Jul 2026, which falls in T3 2025–26 under the Sep–Dec term months you confirmed. Tell me what label that term should carry.
2. **EngageNet access:** does Jan 2026 match when you first requested it?
3. **Paper writing:** check against the actual ICCE 2026 submission deadline.
4. **Planned schedule:**
   - proposal writing and defense until about 20 Nov;
   - revisions, ethics review and the missing videos in late Nov – Dec;
   - new rules and frame combinations in Dec;
   - extraction from late Dec through Jan;
   - training in Feb;
   - statistical analysis from late Feb to early Mar;
   - writing from late Feb to 21 Mar;
   - final defense about 25 Mar.

   The ethics-form duration (Nov 2026 – Apr 2027) still holds, because the revisions run into April.

**Still open:** items 12 and 13, and the PCA question. (`\askadviser` in §4.1 was removed in §9.5, and `\pending` in Appendix B was replaced by her e-mail on 14 Nov.)

### 9.5 Her second round of notes (14 Nov)

| Her note | What changed |
| :-- | :-- |
| §1.3: remove "which also explains why these add up to one more than the 127 participants the dataset authors report" | Removed. The pointer to §4.2 stays, and the footnote of Table 4.2 still explains the count (91 training participants by file name vs. 90 reported). |
| §1.4: remove "a question on which earlier work disagrees (Section 2.7)" | Removed. The sentence now ends at "beyond their average". |
| Ch. 4: no need for "is reported in Chapter 5, together with the remaining steps of the thesis and …" | The intro's last sentence is gone. Ch. 4 still cites §5.1 where the preliminary study shaped the design. |
| §4.1: remove "[Is this scope good enough for the proposal?]" | Removed. |
| §5.2.1: remove steps 1, 2, 3 | Ethics review, remaining videos and extraction changes are gone. Seven steps are left, starting at "New selection rules". |
| §5.3: no detailed description; Gantt chart → table like the previous one | One sentence plus Table 5.4. Columns: MSLABS 1, 2, 3, then May 2026 – Mar 2027 by month. One bullet per term or month. "Completed" and "Planned" groups. |

**Two things to know for the defense:**
- **Weekly detail is gone.** The old Table 4.6 had one bullet per week. With 14 columns, only one bullet per term or month fits in portrait.
- **Steps and calendar.** "Obtaining the remaining videos" was removed from the calendar on 14 Nov (your decision). "Revisions and ethics review" stays (Nov–Dec), although it isn't a numbered step. If asked: it is an administrative step, not a research step, and it comes before the first listed step.

**Also changed later on 14 Nov, before sending the draft:**
- §5.1 says the ICCE paper "has been accepted for publication", not "was published". Switch back once the proceedings are out, and add the pages and DOI.
- §5.2.1 step 2 now says "on the full training split" instead of "on the full data".
- Table 2.4: the last column is now "Rules compared", and Abedi & Khan (2024) reads "No (rate only)".
- §4.7: the Data Privacy Act applies (your decision; see §5, item 8).
- Appendix B: Dr. Azcarraga's e-mail added.
- `main-changes-since-10nov.pdf` was rebuilt and includes all of the above.

---

## 10. Dr. Azcarraga's 15 Nov request: the three papers

She asked for your three accepted or presented papers to be added to the appendix and discussed in Chapter 5. The decisions are D38–D42 in §0.

### 10.1 What changed

| Where | Change |
| :-- | :-- |
| §5 intro | The sentence about §5.1 now mentions both the DAiSEE studies and the EngageNet study. |
| §5.1 | Renamed "Preliminary Work", with a three-sentence opening that points to Appendix B. |
| §5.1.1 (new) | "Earlier Studies on DAiSEE": one paragraph on PERSUASIVE, one on TENCON. |
| §5.1.2 | The old §5.1. Only its first sentence changed: "the first experiment of this thesis on EngageNet … accepted for presentation at … ICCE 2026". Tables 5.1 and 5.2 are unchanged. |
| Appendix B (new) | "Publications": Table B.1, then the three PDFs from `past-papers/` in full, listed in the TOC as B.1–B.3. |
| Appendix C | Resource Persons, previously Appendix B. Nothing refers to it by letter. |
| `myreferences.bib` | New `carandang2026tencon`. PERSUASIVE gains series, publisher, and pages. ICCE gains `note = {Accepted for presentation}`. The D42 fixes. |

### 10.2 Claims ledger: §5.1.1 and Appendix B

| Claim | Evidence |
| :-- | :-- |
| PERSUASIVE examined three choices for the four DAiSEE emotions | PERSUASIVE abstract and §1 |
| Feature sets: action units, face and upper-body landmarks, or both | PERSUASIVE §3.2 (Py-Feat 20 AUs; MediaPipe Holistic, 68 face + 12 body landmarks), §3.3 |
| Representation: per-frame values, or change by Euclidean distance or cosine similarity | PERSUASIVE §3.2, "Feature Representation" |
| Three frames per clip by SME | PERSUASIVE §3.1, Eq. 1 |
| Three classifiers, SMOTE, 80/20 split keeping each student on one side | PERSUASIVE §3.4 |
| Best configuration differed between emotions | PERSUASIVE Table 2 |
| Engagement: F1 of the smaller class 0.03–0.08 at thresholds 1–2; 0.55 at threshold 3 with cosine change features | PERSUASIVE §4.5 and Table 2. At threshold 3 the smaller class is level 3 (3,987 vs. 4,938 clips, Table 1), so "smaller class" is correct at every threshold. |
| One result per configuration, no significance tests | PERSUASIVE Table 2 and §4 report single values; no test is described |
| TENCON: four-qubit VQC vs. a single-layer perceptron of comparable size | TENCON §III.C–D (12 vs. 5 trainable parameters, "comparable") |
| Three frames by BOCPD on OpenFace landmarks | TENCON §III.A, Fig. 2 |
| Four principal components, one per qubit | TENCON §III.B |
| Threshold 3 for engagement and 1 for the others, following PERSUASIVE | TENCON §III.B, citing its ref. [10] |
| Perceptron higher test accuracy for three of four emotions, all but boredom | TENCON Table I (boredom: 52.63% VQC vs. 48.92% perceptron) |
| Your role in TENCON | Your answer, 15 Nov |
| Single selection rule, so no evidence on whether changepoints help | TENCON's design has no comparison rule |
| ~~Velocity peaks instead of BOCPD, reason in §1.3~~ Replaced 15 Nov: "This thesis uses BOCPD again, as one of its two content-based rules" | D43; §4.4 |
| ICCE accepted for presentation at the 34th ICCE | Your note, 15 Nov; the PDF's proceedings header |
| Table B.1: PERSUASIVE "Published" | Crossref record for DOI 10.1007/978-3-032-19687-3_23: LNCS *Persuasive Technology*, pp. 318–328, published online 9 Mar 2026 |
| Table B.1: TENCON "Accepted for publication" | Your note, 15 Nov: presented, not yet published |
| Calendar: "Paper writing and submission" in MSLABS3 | PERSUASIVE PDF saved 19 Jan 2026 (MSLABS3, T2 AY 2025–26). The September bullet also covers TENCON's camera-ready (IEEE PDF eXpress, 3 Sep 2026). |

### 10.3 Likely panel questions about the papers

The panel can now read all three papers in Appendix B, so expect questions on them.

1. **"PERSUASIVE concluded that temporal sampling matters more than features. Is that what you are testing?"**
   - That conclusion came from setting our SME results beside Resurreccion's changepoint results. Her study differed in features and setup, so the comparison couldn't isolate sampling.
   - This thesis compares rules on the same clips, features, and classifiers, with significance tests.
   - The ICCE study already found the gain over SME significant only for the Random Forest. So I don't claim that sampling matters more than features.

2. **"Why is PERSUASIVE's 0.55 for engagement so far below ICCE's 0.70?"** The two numbers aren't comparable. They come from different datasets (DAiSEE vs. EngageNet), labels, features, and splits. They also use different metrics: F1 of the smaller class vs. macro F1.

3. **"PERSUASIVE found change features best for engagement. Why not just use them?"** It was one result per configuration on a different dataset, with no significance test. The thesis tests change and self-similarity against the mean in every condition (family 6), with five versions and Holm correction.

4. **"Is your BOCPD the same as TENCON's?"** *(rewritten 15 Nov)*
   - Same method (Adams & MacKay, 2007). TENCON ran it on OpenFace landmarks. The thesis runs it on MediaPipe landmarks reduced to 3 principal components within each clip, with every setting fixed in §4.4 (prior, hazard, cap, the 7-frame wait, and the two directions).
   - TENCON used one rule only, so it gave no evidence that BOCPD frames are better than others. The thesis tests BOCPD against positional and random selection and against velocity peaks.

5. **"What did you do in TENCON?"** You contributed the changepoint frame selection, the binarization thresholds, and the classical baselines, and you took part in the analysis and writing. The other parts were led by your co-authors. The paper's question was quantum vs. classical models, not frame selection.

6. **"PERSUASIVE calls its first classifier a Decision Tree but describes 'an ensemble of 100 estimators'. Which was it?"** Check your code before the defense. A single tree is not an ensemble, and 100 trees would be a Random Forest or bagged trees. §5.1.1 says "three classifiers" so that it doesn't repeat the ambiguity.

### 10.4 Still to do

- **TENCON:** add the pages and DOI to `carandang2026tencon` once it is in IEEE Xplore, then change its status to "Published".
- **ICCE:** add the editors and pages once the proceedings are out.
- **PERSUASIVE:** the LNCS volume number isn't in Crossref. Add it if you find it on the printed book; the DOI is enough without it.
- **Before the final thesis is deposited online:** check each publisher's reuse rules. IEEE asks for a credit line on reprinted papers and allows only the accepted version to be posted online.

### 10.5 Your answers to the check questions (15 Nov)

1. **Why PERSUASIVE's 0.55 can't be compared with ICCE's 0.70** (you asked me to explain). Nearly everything that affects the number differs:
   - **Metric:** PERSUASIVE's 0.55 is the F1 of one class, the smaller one (highly engaged). ICCE's 0.70 is macro F1, the average of both classes' F1. A classifier can do well on one class and poorly on the other, so one class's F1 and the average of two can differ even for the same predictions.
   - **Data and labels:** DAiSEE, labeled by crowd annotators, vs. EngageNet, labeled by three experts. The clips, participants, and meaning of "level 3" differ.
   - **Features:** Py-Feat action units and 2D Holistic landmarks vs. MediaPipe blendshapes, 3D face landmarks, and pose.
   - **Split:** an 80/20 split of your own vs. EngageNet's official partition.

   Each difference alone would prevent a fair comparison. So the 0.55 says nothing about whether EngageNet or the newer pipeline is "better".
2. **Why PERSUASIVE doesn't settle the frame-combination question.** Your answer, that the thesis also explores other combinations, is right but incomplete. The main reason is the strength of the evidence. PERSUASIVE reports one result per configuration, with no significance test, on a different dataset and with different features. That suggests change features might help, but doesn't show it. The thesis compares change (and concatenation and self-similarity) with the mean in all ten selection conditions, with McNemar tests, Holm correction, and five versions (family 6).
3. **Why TENCON says nothing about changepoint selection.** Correct: its question was quantum vs. classical models. For the panel, add: it used only one selection rule, BOCPD, so there was no other rule to compare it with.

---

## 11. k-BOCPD as a fifth rule, and nested random draws (15 Nov)

You asked what would happen if the experiments used BOCPD. You first chose to replace velocity peaks, then asked whether to keep both. I recommended both, and the manuscript now has five rules. This section explains the change and gives what you need to defend it. The nested random draws (M1) and the Table 4.1 status fix (M2) went into the same pass (§11.5).

### 11.1 Why both rules, not a replacement

1. **The main question keeps its pilot.** "Does content-based selection help?" is still answered by velocity peaks, which the preliminary study tested. BOCPD's settings were fixed without any EngageNet data. If they turn out poor, only the BOCPD comparisons suffer, not the main result.
2. **The preliminary study stays a pilot.** The 2-point margin and the five-version rule come from it, and it tested velocity peaks.
3. **A caveat becomes a test.** §3.5 already said velocity peaks catch fast movement, not lasting change. Now the thesis tests which of the two matters more (family 4, Table 4.3).
4. **The smoke-test check survives.** The new velocity-peak frames can still be matched against the old 5- and 7-changepoint CSVs.

**The cost:**
- 13 conditions (was 10) and 25 feature sets (was 22);
- 590 training runs (was 476) and 182 configurations (was 140);
- 254 comparisons in seven families (was 176 in six);
- about 12% more second-pass extraction, and ~3 GB more disk for the stored landmark positions.

### 11.2 Lesson: what BOCPD computes

**Segments and run length.** BOCPD assumes the signal is a series of segments, each with stable behavior. For example, the face is held in one position, then moves to another and stays there. The *run length* r_t is the number of frames in the current segment so far, counting frame t.

**Hazard.** Before looking at the data, a new segment begins at any frame with probability H. We use H = 1/20. Segment lengths then follow a geometric distribution with mean 20 frames.

**Prediction.** For each possible run length, BOCPD asks how probable the new frame is, given only the frames of that run. Each of the 3 components is modeled as Gaussian with unknown mean and variance. With the normal–inverse-gamma prior, the prediction has a closed form, a Student-t distribution. You will code this, so here are the formulas for one component. Start from the prior (μ₀, κ₀, α₀, β₀) = (0, 1, 2, 1). After each frame x of the run:
- μ ← (κμ + x)/(κ + 1)
- κ ← κ + 1
- α ← α + ½
- β ← β + κ(x − μ)² / (2(κ + 1)), using the old κ and μ

The prediction of the next x is a Student-t with 2α degrees of freedom, centered at μ, with squared scale β(κ + 1)/(ακ). The three components are independent, so their log-probabilities add.

**Update.** At each new frame, every current run either continues (probability 1 − H) or a new segment starts at this frame (probability H). Each possibility is weighted by how well it predicted the frame, and the weights are normalized. The result is a probability for every run length. These are the "probabilities of the run lengths" in §4.4.

**Why the score waits 7 frames.** One frame is weak evidence. A single odd frame could be noise, or the start of a new position. Seven frames later the difference is clear. If the face really moved and stayed, the run length that starts at that frame now has most of the probability. If it moved and came back, the old segment explains the later frames again. Equation 4.2 reads exactly this: the probability that the segment holding frame t + 6 began at frame t.

A side note you may be asked about. In Adams and MacKay's own bookkeeping, the probability that a change happened *at the newest frame* always equals the hazard. So it can't rank frames, which is another reason the score waits.

**Why one scale for the 3 components.** Principal components are ordered by how much the landmarks vary along them. If each were scaled to variance 1, a third component that is mostly jitter would count as much as the first, which carries the real movement. Dividing all three by the first one's standard deviation keeps their order of importance.

**Why within each clip.** Each clip has its own main movements. A PCA fitted within the clip makes each clip's selection depend only on that clip, as under every other rule. A PCA fitted across clips would have to be fitted on the training split, and the frames chosen for a test clip would then depend on other people's videos.

**Why forward and backward, with a cap.** See §11.3. Run forward only, BOCPD favored frames near the start of the clip. The cap and the second direction remove that bias without losing detection.

**What the two rules can and cannot show.**
- They can show whether, at a given budget, frames of fast movement or frames where a lasting change begins give better classification (family 4, Table 4.3).
- They cannot show which changepoint method is best. PELT and other settings are not tested.
- Both rules look only at the landmark positions. Blendshapes and pose don't influence which frames are chosen, only what the classifier sees.

### 11.3 Synthetic check of the settings (my scratch code, not yours)

Before writing §4.4, I tested the proposed rule on made-up signals: 150 frames and 3 components. These are not EngageNet clips, and the code is a scratch check, not project code. Your spec tests will repeat these checks on your own implementation.

**Where the picks fall.** I used 300 noise-only clips, top 3 picks per clip. The table gives the share of picks in each fifth of the clip, where 1 means even. The hit rate is from 400 clips, each with one shift of the mean (1.0, noise SD 0.5) at frame 12, 40, 75, 110 or 138. A hit means the highest score was within one frame of the shift.

| Version | Picks per fifth of clip (1 = even) | Max / min | Hit rate |
| :-- | :-- | --: | --: |
| Forward only (standard BOCPD) | 1.47, 0.98, 0.83, 0.79, 0.93 | 1.86 | 0.78 |
| Forward + backward | 1.12, 0.77, 0.80, 0.92, 1.39 | 1.81 | 0.83 |
| Forward, run length capped at 50 | 0.95, 1.05, 0.92, 1.00, 1.08 | 1.17 | 0.71 |
| **Forward + backward, capped at 50 (chosen)** | 0.94, 0.96, 0.96, 1.03, 1.11 | 1.18 | 0.78 |

Standard BOCPD put nearly 1.5 times its share of picks in the first fifth of a clip with no real changes. That matters, because a content rule that leans toward the start would partly be a position rule.

**Other checks of the chosen version:**
- **A shift at frame 50:** the top score is at frame 50 (score 0.95). On noise only, the top score is 0.12.
- **A 3-frame excursion vs. a lasting shift:** the excursion scored 0.48 and the lasting shift 0.70. The lasting shift wins, but a big brief movement still scores, so don't claim BOCPD *ignores* brief movements.
- **Landmark-like data** (478 landmarks, posture shifts at frames 70 and 120, through the 3-PC step): both shifts are among the top 3.
- **Nesting:** the 3-frame picks are inside the 5-frame picks, and those inside the 7-frame picks, on all 200 noise clips.
- **Enough candidates:** every 150-frame clip had at least 12 candidate peaks (median 15), so k = 7 is always possible.
- **Short clips:** 13 valid frames give no candidate frame, and 14 give one, which matches "fewer than 2L = 14".

### 11.4 Claims ledger: the BOCPD and nested-draw text

| Claim | Evidence |
| :-- | :-- |
| Five rules, thirteen conditions, 254 comparisons, 590 runs | D43, D48; recomputed from the design: 13 conditions; families 24 + 24 + 12 + 12 + 48 + 4 + 130 |
| BOCPD tracks the run length and combines predictions with a hazard into run-length probabilities | Adams & MacKay (2007), §2 |
| With a conjugate prior, the prediction has a closed form | Adams & MacKay (2007), conjugate-exponential models |
| Like BOCPD, PELT divides the signal into segments of stable behavior | Killick et al. (2012); Truong et al. (2020) |
| A quick head turn and return gives weaker evidence for a new segment | §11.3 (0.48 vs. 0.70) and the reasoning in §11.2 |
| 956 values per frame | 478 landmarks × 2 coordinates |
| Expected variance 1 | Inverse-gamma mean β₀/(α₀ − 1) = 1/1 |
| Segments of 20 scanned frames on average, about 1.3 s | Geometric mean 1/H = 20; scanned at 15 frames/s (30 fps, every second frame) |
| About seven changes in 150 valid frames | 149 transitions × 1/20 ≈ 7.5 |
| The cap of 50 is 2.5 times the expected segment length | 50 / 20 |
| Run in one direction, the method favors the start of the clip | §11.3, first row of the table |
| Clips with more than k but fewer than 14 valid frames can't be scored | Frames need 7 on each side: t from 8 to n − 6, so n ≥ 14 |
| BOCPD selections are nested across k | Top-k of one score; §11.3 |
| Random draws: each set of k frames is still a uniform random draw | The first k of a uniformly random order are a uniformly random k-subset |
| Abstract within 250 words | Counted: 250 |
| "This thesis uses BOCPD again" | TENCON used BOCPD (TENCON §III.A) |

No sentence reports a BOCPD result on EngageNet; none exists yet.

**§4.4 rewritten in plainer language (15 Nov, at your request).** The settings and Eq. 4.2 are unchanged. The new wording adds three claims:

| Claim | Evidence |
| :-- | :-- |
| "as when a student leans back or looks down at notes for a while" | An illustration of a lasting change, not a finding. If asked, say it is an example of what the rule looks for, not evidence that such moments occur in EngageNet. |
| The prior is "a weak starting guess, which a few real frames quickly override" | κ₀ = 1 counts as one frame for the mean, and α₀ = 2 as about four frames for the variance, so a segment's own frames soon outweigh it. |
| "a blink or a quick glance also makes one frame look different" | The reason for waiting L frames (§11.2). The 3-frame excursion in §11.3 scored lower than the lasting shift. |

### 11.5 Nested random draws (M1) and the Table 4.1 status (M2)

- **§4.4, Random:** five draws at seeds 42–46. Each draw orders the valid frames randomly once, and k = 3, 5, 7 take the first k. Within a draw, a larger budget only adds frames, as under both content rules, and fewer distinct frames need extracting.
- **Algorithm 5.1:** the random branch now says "put the positions in a random order, keep the first k".
- **Table 4.1:** SME now reads "Completed; to be re-extracted", like k-Changepoint, because §5.2.1 re-extracts it on the full training split.

### 11.6 Likely panel questions

1. **"Why add a rule five days before the defense?"** It turns a stated limitation of velocity peaks (§3.5: fast movement, not lasting change) into a tested question. The pipeline, features, and classifiers are unchanged, and the cost is 114 more runs.
2. **"How did you choose the hazard and the prior?"** In advance, with reasons in §4.4, and not tuned.
   - The hazard of 1/20 allows about as many changes per clip as the largest budget.
   - The prior expects variance 1 on the clip's own scale.
   - Tuning them on validation would give BOCPD a tuning step that no other rule gets.
3. **"BOCPD is an online method. Why run it backward?"** The whole clip is available, so nothing needs to be online. Run forward only, BOCPD favored the start of a clip in my synthetic check (§11.3). Averaging the two directions judges every frame from both sides.
4. **"Why 3 principal components?"** Few enough that the mean and variance of each can be estimated from a 20-frame segment. And the first components carry the largest movements. It's a fixed choice; other numbers aren't tested.
5. **"What if the two content rules pick the same frames?"** Then family 4 will show them equivalent or inconclusive, and Table 4.3 says what that means: the two definitions select equally useful frames at that budget.
6. **"Doesn't adding comparisons cost power?"** A little. Families 1 and 2 grow from 12 to 24 tests, so Holm's first threshold goes from .05/12 ≈ .0042 to .05/24 ≈ .0021. Small effects near the threshold could be lost. Grouping by question is the more cautious choice, and the families were fixed before any results.
7. **"Invalid frames are dropped. Doesn't that create fake changes?"** It can, for both content rules. A run of invalid frames joins two frames that are far apart in time, and a jump there looks like movement. The reported positions of the selected frames and the number of valid frames per clip will show how often this happens.

### 11.7 Check questions (answer in your own words)

1. Why does BOCPD's score for frame t wait for the next 7 frames, and what would go wrong if it scored each frame as soon as it arrived?
2. A student looks down at a phone for 5 seconds, then looks back at the screen. Which frames would velocity peaks pick, and which would k-BOCPD pick?
3. Why would it be unfair to tune BOCPD's hazard on the validation split?

**Still your call (from the 14 Nov plan):**
- **M3:** how Holm handles families that mix 5-version and 1-version comparisons. My proposal: run Holm once per version index; a 1-version comparison enters every pass with its one p-value; "reliable" also requires the same direction in all five versions.
- **M4:** state that a frame chosen by several rules is extracted once, and that a condition's second-pass time is the sum of its frames' times.

### 11.8 Still to do

- **Before the defense, tell Doc Jay about the fifth rule.** It changes the design Doc Jay saw on 14 Nov. Send `main.pdf` and `main-changes-since-14nov.pdf`, which marks both the papers and the BOCPD changes.
- **Slides:** see the storyboard (new slide 14b, B7). The figures are rebuilt.
- **After the defense:** update `docs/implementation-spec.md`:
  - `select_bocpd` and its tests;
  - the pass-1 store keeps landmark positions;
  - 590 runs, 254 comparisons, 182 configurations.

  `AGENTS.md` and the `bocpd` rejection in `src/dataset.py` change when your code lands.

---

## 12. How "improves on the mean" is decided: replicability analysis (15 Nov)

You asked where "seven of the thirteen" came from. Honest answer: it was my default rule (D25), with no source. On 15 Nov you chose to replace it with a published method (D51). It is written into §4.6.5 as Eq. 4.3.

### 12.1 The problem with the old rule

- **Demšar (2006)** is the standard reference for comparing classifiers over several datasets. He warns against counting only significant wins: such a count "draws an arbitrary threshold of p < 0.05 between what counts and what does not" (§3.1.4). His example: if A beats B on 1,000 datasets but never significantly, counting significant wins gives 0, although A is clearly better.
- **His recommended test,** Wilcoxon over datasets, assumes the datasets are independent. Our 13 conditions are not. They share the same test clips, and many share frames.

### 12.2 Lesson: what replicability analysis does

**Dror et al. (2017)** ask exactly our question: across N datasets, in how many is method A really better than method B?

**Recipe**, for one representation and one classifier:
1. In each of the 13 conditions, run a one-sided exact McNemar test of "the representation is better than the mean". That gives 13 p-values.
2. Sort them: p₍₁₎ ≤ p₍₂₎ ≤ … ≤ p₍₁₃₎.
3. Go up the list. At position v, check whether (13 − v + 1) × p₍ᵥ₎ ≤ α.
4. k̂ is how far you get before the first check fails.

**What k̂ means:** with 95% confidence, the representation is truly better in **at least k̂** conditions. The chance that k̂ is too high is at most α. Dror et al.'s Bonferroni version "does not make any assumptions about the dependencies between the participating datasets", which is why it suits us. Their Fisher version is more powerful but needs independence, so it isn't used.

**A fact worth knowing:** step 3 is exactly the Holm–Bonferroni procedure applied to the 13 conditions. I checked this on 20,000 random sets of p-values, and they agreed every time. So k̂ is "how many conditions Holm finds significant". The paper adds the meaning: a lower bound on the true number, valid under dependence.

**Why α = 0.005.** There are 10 counts: 3 representations × (MLP, SVM, RF), plus attention for the LSTM. Splitting 0.05 over them (Bonferroni) keeps the chance that *any* count is too high at 5% or less.

**Worked example** (α = 0.005). The sorted p-values are 0.00001, 0.00004, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.002, …

| v | p₍ᵥ₎ | (13 − v + 1) × p₍ᵥ₎ | ≤ 0.005? |
| --: | --: | --: | :-- |
| 1 | 0.00001 | 0.00013 | yes |
| 2 | 0.00004 | 0.00048 | yes |
| 3 | 0.0001 | 0.0011 | yes |
| 4 | 0.0002 | 0.0020 | yes |
| 5 | 0.0003 | 0.0027 | yes |
| 6 | 0.0004 | 0.0032 | yes |
| 7 | 0.0005 | 0.0035 | yes |
| 8 | 0.002 | 0.012 | **no**, so stop |

k̂ = 7, which meets the "at least 7" bar.

**The other conditions for "improves on the mean":**
- **The reverse count must be 0.** The same count is made the other way, for conditions where the mean beats the representation.
- **All five versions.** Both counts are made in every version. A condition with only one version (SVM and RF on the non-random rules) gives the same p-value in every version, which is the same convention as the M3 proposal.

### 12.3 What it does not fix (say this if asked)

- **A small but consistent gain can still be missed.** If all 13 p-values were 0.04, k̂ would be 0. Each condition is still tested on its own. Catching that case would need either Fisher's version, which assumes independent conditions, or one test of the gain averaged over the 13 conditions. §4.6.5 now states this limitation.
- **"At least 7" is still a choice.** It means "more than half", that is, most conditions. What changed is that the 7 now applies to a count with a known error rate.
- **The arithmetic barely changed.** The old rule counted results that passed Holm over all 130 tests of family 7. The new count uses Holm within the 13 conditions at α = 0.005, and the thresholds come out similar. What changed is the justification: a published method with a stated guarantee, valid for dependent conditions.

### 12.4 Claims ledger: §4.6.5

| Claim | Evidence |
| :-- | :-- |
| A plain count of significant results is a weak basis; the cut-off is arbitrary | Demšar (2006), JMLR 7, §3.1.4 (quoted above; checked in the PDF) |
| Replicability analysis was developed for comparing two methods across several datasets | Dror et al. (2017), TACL 5, 471–486; checked on Crossref and arXiv |
| Eq. 4.3 and k̂ = 0 when 13·p₍₁₎ > α | Dror et al.: p^(u/N) = (N − u + 1)·p₍ᵤ₎, monotone in u; k̂ = max{u : p*^(u/N) ≤ α} |
| k̂ equals the Holm count among the 13 | The definitions coincide; checked on 20,000 random cases |
| With probability ≥ 1 − α, at least k̂ conditions are truly better | Dror et al.: "α is the desired upper bound on the probability to overestimate the true k" |
| Valid without independence | Dror et al.: Bonferroni's method "does not make any assumptions about the dependencies" |
| One-sided p-values | Dror et al. test "versus the alternative statement that A is superior" |
| α = 0.005 for each of ten counts | Bonferroni over 10 counts: 3 × 3 + 1 |
| A small gain in every condition may go undetected | Worked case above: all p = 0.04 gives k̂ = 0 |
| §4.6.5 rewritten in plainer steps on 15 Nov (Testing, Counting, Deciding); the example "the seventh is 0.0005, multiplied by 7, giving 0.0035, which passes" | (13 − 7 + 1) × 0.0005 = 0.0035 ≤ 0.005; the same as row 7 of the worked table in §12.2 |

### 12.5 Check question

Five conditions give p = 0.0001 and the other eight give p = 0.3. What is k̂, and does the representation "improve on the mean"? (Work it out with the table method in §12.2.)

---

## 13. The research ethics forms (16 Nov)

The three forms in Appendix A are now filled in. The full answers, the e-mail to the EngageNet authors, and the submission checklist are in `notes/ethics-answers.md`.

### 13.1 What changed and why

- **The preliminary work is disclosed.** EngageNet clips were processed in June and July 2026 (after the user agreement of 19 June), but before any ethics review. Both the forms and the declaration you sign say data collection starts only after approval. So Checklist A's description, the Ethics Review Form's "Other concerns" row, and a new sentence in §4.7 all state it plainly. (The forms are now your Word files in `ethics-forms/filled/`; the Ethics Review Form, ver. Oct2024c, replaces the old clearance form.)
- **The smoke test moves to after approval.** The 14 Nov plan allowed a 20-clip test before approval. That would contradict what you sign, so `docs/implementation-spec.md` (§5, step 3) now says after approval. Code can still be tested on synthetic data at any time.
- **The first pass is described as it now works.** Since k-BOCPD, the first pass keeps facial-landmark positions for every scanned valid frame, not only the selected ones. The description says so, and the storage restrictions cover all derived data.

### 13.2 Likely panel questions

1. **"You processed the data before ethics review. Isn't that a problem?"** Answer plainly, and don't minimize it:
   - It was the preliminary study, run under the dataset's user agreement.
   - It is disclosed in the forms and in §4.7.
   - Nothing more will run on the clips, not even code tests, until the committee approves.
2. **"Did the EngageNet participants consent to this use?"**
   - The dataset's paper says their consent was requested "for the scope of usage of the data" (Singh et al., 2023, §3.1).
   - The user agreement limits use to academic, non-commercial research, which is what this is.
   - You've asked the authors for the participant information statement for the ethics committee.
3. **"Are the faces sensitive personal information?"** They are treated as personal information under the Data Privacy Act, which is the cautious reading. The safeguards in §4.7 apply either way. The form's own "sensitive data" examples (sexual activity, substance use) don't apply.

### 13.3 Claims ledger: the new §4.7 sentence

| Claim | Evidence |
| :-- | :-- |
| Features first extracted in June and July 2026 for the preliminary study | Table 5.4 (calendar: "Preliminary feature extraction", Jun–Jul) |
| Under the same user agreement | `docs/EULA_EngageNet_signed.pdf`, signed 19 June 2026 |
| Before any ethics review | Your answer on 16 Nov ("disclose it"; no earlier clearance) |
| No further processing, including code tests, until approval | Your decision on 16 Nov; spec §5, step 3 |

