# Proposal defense: storyboard

For the proposal defense. The slot is 25–30 minutes. The panel is the same as at the OCE: Tiam-Lee (chair), Gonda, Antioquia, and Dr. Azcarraga. Everything here is taken from the manuscript (`dlsu-manuscript/main.pdf`), as of 20 Nov 2026.

**20 Nov: reordered after Doc Jay's run-through.**
- The talk now tells a story instead of following the chapters.
- Doc Jay's comments are in `adviser-comments-2026-11-20.md`. The next table shows where each one is handled.

## How to use this

**Building the deck**
- **You build the deck in Canva and write every word on it.** For each slide, this file gives:
  - a working title;
  - the one point the slide makes;
  - what goes on it;
  - notes on what to say;
  - the source in the manuscript;
  - the citations to put on the slide;
  - the question it is likely to invite.
- **Titles.** The OCE panel wrote that "some of the slide titles slightly misrepresent the content". Each working title below states what its slide shows. If you reword a title, check that it still matches the slide.
- **On the slide:** keywords, numbers, the figure, and short citations (Author et al., year). Full sentences go in your speaker notes, in your own words.
- **Citations (Doc Jay, 20 Nov):** "whenever you present a concept or an idea, if there is something you can cite, cite it." The table "Cite on slide" lists them for every slide.

**Saying it**
- **Say:** these are notes, not a script. Say them your way, and don't read them aloud.
- **Numbers:** use only the ones given here. Each is traced to a section or table, and is rounded as the manuscript rounds it.

**Supporting material**
- **Draft deck:** a Slides artifact built from this storyboard, with a spoken script in its speaker notes: https://claude.ai/artifact/CHCZWgqMGpUeaNYN25XpLt (private).
  - Rebuilt on 20 Nov in the new order.
  - It downloads as PPTX, and Canva can import PPTX. It is still a backbone: rebuild the slides in your own design and words.
- **Timing:** 34 main slides and 4 part dividers take about 25:20. Slides marked ✂ (15, 19 and 32) save 2:00, which brings the talk to about 23:20.
- **Images:**
  - All are in `figures/`, on white backgrounds.
  - In Canva, use Uploads → Upload files, then drag the image onto the slide.
  - Resize from a corner so the image keeps its proportions.
- **Colors:** each selection rule has one color in every figure: SME orange, positional green, random yellow, k-Changepoint blue, k-BOCPD pink. If you color text or shapes yourself, keep to these. Two exceptions:
  - `bocpd-score.png` and `bocpd-run-length.png` use the blues of `velocity-peaks.png`, so the signal figures look alike (your choice, 20 Nov).
  - `content-rules-compare.png` uses blue for k-Changepoint and pink for k-BOCPD, because it compares the two.

**Hard rules**
- **Never** put a frame, face, or still from EngageNet on any slide (user agreement; §4.7). The figures use diagrams, made-up signals and made-up numbers only.
- **Left out on purpose** (your 14 Nov comments):
  - the ethics review before extraction;
  - obtaining the missing training videos;
  - the extraction changes.

  The full calendar (backup) still shows "Revisions and ethics review" in Nov–Dec, as in Table 5.4.

## Doc Jay's comments (20 Nov) and where each is handled

| Comment (time in the recording) | Where |
|---|---|
| Tell it as a story, not in chapter order: domain → related works → gap → problem → objectives with scope (00:21) | The running order below |
| No separate theory section; bring in each concept where it is used (03:45) | Working definitions moved to backup (B15). Terms are defined where they first appear (see "The narrative") |
| "Why does it matter?" can be your first slide (05:09) | Slide 3 |
| Cite every statement you can (02:52, 06:12) | "Cite on slide" table |
| The research question must not be answerable by yes or no (08:30) | Slide 9. Revised on 22 Nov into two "how" questions, now in §1.1 and §4.1; sent to Doc Jay for comment |
| Objectives word for word; drop only "To" (10:09) | Slides 9–14 |
| Scope and limitations per objective, e.g. one slide each (11:13); keep the general one hidden (37:06) | Slides 10–14; B16 |
| Bring up the definition of engagement: how the three kinds differ, and where the study comes in (13:49) | Slide 3 |
| A dedicated EngageNet slide: labels, number of people, male/female, task, setup (14:12, 17:24) | Slide 18 |
| A line separating the position-based and content-based rules (15:27) | Slide 20 (`selection-rules.png`, now grouped) |
| Be ready: what the changepoint is computed on (19:39) | Slide 21; "Be ready", question 1 |
| Be ready: how k-BOCPD differs from k-Changepoint (21:54) | Slide 24; "Be ready", question 3 |
| A visual explaining mean + change and mean + self-similarity (24:45) | Slide 26 |
| Interpretation table: too much, hide it as a backup (25:49) | B14 |
| Preliminary work: pass through the three papers (27:35) | Slide 29 |
| **Main comment:** explain the changepoint technically, "as simple as you can", including how it knows it found something (29:04, 31:56) | Slides 21–24; "Be ready" |
| Calendar: only the work still to do (31:03) | Slide 33; full calendar as B17 |
| Citations on the related-works table; a long table can be a backup screenshot (50:31) | Slide 6; B18 |
| Keep your OCE slides on the algorithms ready (51:19) | B20 |

## Running order (20 Nov, story order)

"Spec" points to the slide notes further down:
- **"20 Nov: …"** is under "New and changed slides (20 Nov)" just below.
- **"19 Nov: …"** is under "Slide specs added 19 Nov".
- **A number** is under "Main slides".

| # | Slide | Spec | Time | ✂ |
|---|---|---|---|---|
| 1 | Title | 1 | 0:15 | |
| 2 | How the OCE revisions were addressed | 2 | 0:45 | |
| D1 | *Divider, Part 1: "If a classifier can see only a few frames of a student's video, which should it see?"* | Part dividers | 0:10 | |
| 3 | Why does it matter? Engagement's three kinds, and which one this study is about | 20 Nov: slide 3 | 1:00 | |
| 4 | How engagement is detected from video: the webcam is the sensor, observers' ratings are the labels | 19 Nov: Background 2 (figure moved to slide 18) | 0:45 | |
| 5 | Which frames does the classifier see? | 19 Nov: Background 3 | 0:45 | |
| 6 | Related works: the review narrows to how frames are used | 19 Nov: Review, plus 20 Nov: slide 6 | 1:00 | |
| 7 | Synthesis: only this study has matched budgets and a random control | 4 | 0:30 | |
| 8 | What is still unknown: two comparisons that could not say why, and the problem | 19 Nov: Background 4 | 0:45 | |
| D2 | *Divider, Part 2: "What does the study ask, and what does it cover?"* | Part dividers | 0:05 | |
| 9 | Research questions and general objective | 20 Nov: slide 9 | 0:45 | |
| 10 | Objective 1: features, and their scope | 20 Nov: slides 10–14 | 0:25 | |
| 11 | Objective 2: frame selection, and its scope | 20 Nov: slides 10–14 | 0:25 | |
| 12 | Objective 3: temporal representation, and its scope | 20 Nov: slides 10–14 | 0:25 | |
| 13 | Objective 4: classifiers and task, and their scope | 20 Nov: slides 10–14 | 0:25 | |
| 14 | Objective 5: best combination, and the limits of the conclusions | 20 Nov: slides 10–14 | 0:25 | |
| 15 | Significance | 19 Nov: Significance | 0:30 | ✂ |
| D3 | *Divider, Part 3: "How will the comparison be made fair?"* | Part dividers | 0:05 | |
| 16 | Conceptual framework | 19 Nov: Conceptual framework | 0:45 | |
| 17 | Thirteen conditions, four classifiers | 12 | 1:00 | |
| 18 | EngageNet: who was recorded, doing what, where, and how it was labeled | 20 Nov: slide 18 | 1:00 | |
| 19 | Pipeline | 15 | 0:45 | ✂ |
| 20 | The five rules on one clip: position-based, control, content-based | 20 Nov: slide 20 | 1:00 | |
| 21 | k-Changepoint step by step: how velocity is computed | 20 Nov: slide 21 | 1:15 | |
| 22 | k-Changepoint keeps the k highest velocity peaks | 14 | 0:45 | |
| 23 | k-BOCPD step by step: run length and the score | 20 Nov: slide 23 | 1:15 | |
| 24 | One clip, two content rules: fast movement vs. lasting change | 20 Nov: slide 24 | 1:00 | |
| 25 | Four ways to combine the frames, two readouts for the LSTM | 16 | 0:45 | |
| 26 | Mean + change and mean + self-similarity on a small example | 20 Nov: slide 26 | 1:00 | |
| 27 | 254 comparisons, fixed in advance | 17 | 1:00 | |
| 28 | Ethics | 19 | 0:45 | |
| D4 | *Divider, Part 4: "What has been seen so far, and what remains?"* | Part dividers | 0:05 | |
| 29 | Preliminary work: three papers | 8 (shortened) | 0:30 | |
| 30 | Highest macro F1 with three velocity-peak frames (ICCE 2026) | 9 | 0:45 | |
| 31 | Only the Random Forest improved significantly (ICCE 2026) | 10 | 0:45 | |
| 32 | Five gaps and the design change for each | 11 | 0:45 | ✂ |
| 33 | Remaining work: the planned steps | 20 Nov: slide 33 | 0:30 | |
| 34 | Back to the question, and thanks | 19 Nov: closing | 0:20 | |
| | **Total** | | **≈ 25:20** | ≈ 23:20 after the ✂ cuts |

**Backups** B1–B20 follow a "Backup" divider (see "Backup slides"). New on 20 Nov:
- B14: interpretation;
- B15: working definitions;
- B16: general scope;
- B17: full calendar;
- B18: Table 2.4;
- B19: `bocpd-score.png`;
- B20: OCE algorithm slides.

### Part dividers (20 Nov)

Four parts replace the five chapters. Each divider shows its question and a four-step bar marking where the talk is.

| Part | Question on the divider | Slides |
|---|---|---|
| 1 | If a classifier can see only a few frames of a student's video, which should it see? (the hook) | 3–8 |
| 2 | What does the study ask, and what does it cover? | 9–15 |
| 3 | How will the comparison be made fair? | 16–28 |
| 4 | What has been seen so far, and what remains? | 29–34 |

### Headers (20 Nov, in your style)

Each content slide has a short header in blue (#004AAD, IBM Plex Sans bold). Under it is the statement bar: one sentence in black with a dark left bar. The statement is the working title from this file, so the header can stay short and neutral while the statement says what the slide shows.

| # | Header | # | Header |
|---|---|---|---|
| 2 | OCE Revisions | 18 | Dataset: EngageNet |
| 3 | Why does it matter? | 19 | Feature Extraction |
| 4 | How is engagement detected from video? | 20 | Frame Selection Rules |
| 5 | Which frames does the classifier see? | 21 | k-Changepoint: Computing Velocity |
| 6 | Related Works | 22 | k-Changepoint: Selecting Frames |
| 7 | Synthesis | 23 | k-BOCPD: Finding Lasting Changes |
| 8 | What is still unknown? | 24 | Velocity Peaks vs. k-BOCPD |
| 9 | Research Questions | 25 | Frame Combinations |
| 10–14 | Objective 1 … Objective 5 | 26 | Change and Self-Similarity |
| 15 | Significance | 27 | Evaluation |
| 16 | Conceptual Framework | 28 | Ethical Considerations |
| 17 | Research Design | 29 | Preliminary Work |
| | | 30 | Preliminary Results |
| | | 31 | Tests Against SME |
| | | 32 | From Gaps to Design |
| | | 33 | Remaining Work |
| | | 34 | Back to the Question |

### The narrative (20 Nov)

The talk follows Doc Jay's order:
1. The general domain: why engagement matters, and how it is detected from video.
2. The specific problem: which frames a classifier sees.
3. Related works, then the gap.
4. The research question and the objectives, each with its scope, then the significance.
5. The method.
6. The preliminary evidence and the remaining work.

Keep these devices when you rebuild, even if you change the wording.

- **The hook.** The Part 1 divider asks: "If a classifier can see only a few frames of a student's video, which should it see?" The last slide answers it: the study compares content, position and chance at equal budgets.
- **The running example: a brief glance away.** It is made up, never EngageNet data, and it is grounded in §3.4. It appears:
  - on slide 5, as a strip in which three evenly spaced frames miss it;
  - on slide 20, where the position-based rules are separated from the content-based ones;
  - on slide 24, where velocity peaks keep the glances and k-BOCPD keeps the lasting moves;
  - on slide 34, as the brief-vs.-lasting question.
- **Concepts where they are used** (Doc Jay, 03:45):
  - engagement and its three kinds: slide 3;
  - observer-rated engagement: slide 4;
  - position-based and content-based selection, and the frame budget k: slides 5 and 20;
  - velocity and changepoint: slide 21;
  - run length and BOCPD: slide 23;
  - temporal representation: slide 25.

  The full list of definitions is backup B15.
- **Bridges.** The draft deck's scripts end with "Bridge to the next slide": one sentence that hands over to the next slide. Say it as you click.

### Canva change list (from your 19 Nov order)

Your Canva deck follows the 19 Nov order (`Running order by chapter`). Work down this list.

| 19 Nov # | Header | Action | New # |
|---|---|---|---|
| 1 | Title | keep | 1 |
| 2 | OCE Revisions | keep | 2 |
| 3 | Outline | **delete**; the hook question moves to the Part 1 divider | D1 |
| 4 | Divider, Ch. 1 | **replace** with the Part 1 divider | D1 |
| 5 | Why does it matter? | **change:** add the three kinds of engagement and where the study comes in; fix the two typos below | 3 |
| 6 | How is engagement detected from video? | **change:** the label chart moves to slide 18 | 4 |
| 7 | Which frames does the classifier see? | keep | 5 |
| 8 | What is still unknown? | **move** after Synthesis | 8 |
| 9 | Research Question | **change:** the revised question once Doc Jay approves it; add the general objective | 9 |
| 10 | Objectives | **split** into five slides, one per objective, each with its scope | 10–14 |
| 11 | Scope and Limitations | **hide** as a backup | B16 |
| 12 | Significance | keep (✂) | 15 |
| 13 | Divider, Ch. 2 | **delete** | |
| 14 | Related Works | **move** to Part 1; **change:** citations on every row; fix the text below | 6 |
| 15 | Synthesis | **move** to Part 1 | 7 |
| 16 | Divider, Ch. 3 | **delete** | |
| 17 | Working Definitions | **hide** as a backup | B15 |
| 18 | Position-Based vs. Content-Based Selection | **merge** into slide 20; its point is now made by slide 24 | 20, 24 |
| 19 | Conceptual Framework | keep | 16 |
| 20 | Divider, Ch. 4 | **replace** with the Part 3 divider | D3 |
| 21 | Research Design | keep | 17 |
| 22 | Data | **change** into the EngageNet slide | 18 |
| 23 | Feature Extraction | keep (✂) | 19 |
| 24 | Frame Selection Rules | **change:** the new `selection-rules.png`, with the groups | 20 |
| 25 | k-Changepoint | keep; **new** slide 21 goes before it | 22 |
| 26 | k-BOCPD | **replace** with new slides 23 and 24; the old figure becomes B19 | 23, 24 |
| 27 | Frame Combinations | keep; remove the caption under the figure (the figure has its own key); **new** slide 26 goes after it | 25 |
| 28 | Evaluation | keep | 27 |
| 29 | Interpretation of Outcomes | **hide** as a backup | B14 |
| 30 | Ethical Considerations | keep | 28 |
| 31 | Divider, Ch. 5 | **replace** with the Part 4 divider | D4 |
| 32 | Preliminary Work | **shorten** to 0:30 | 29 |
| 33 | Preliminary Results | keep; label it "ICCE 2026" | 30 |
| 34 | Tests Against SME | keep; label it "ICCE 2026" | 31 |
| 35 | From Gaps to Design | keep (✂) | 32 |
| 36 | Remaining Work | **change:** `remaining-work.png`; the full calendar becomes B17 | 33 |
| 37 | Back to the Question | keep | 34 |

**New slides to add:**
- the Part 2 divider;
- 10–14 (objectives);
- 18 (EngageNet; from the old Data slide);
- 21 (velocity steps);
- 23 (BOCPD run length);
- 24 (comparison);
- 26 (combination example).

**Text fixes seen in the recording (20 Nov):**
- **"Why does it matter?":**
  - "featues" should be "features";
  - "(Frederiks et al., 2004)" should be "(Fredricks et al., 2004)".
- **Related Works:**
  - The second column header reads "Excluded". It should name what the column shows, e.g. "What it means for this study".
  - "…is has not been examined…" should be "…has not been examined…".
  - The VLM row ("Can reliably detect basic emotions, however not for engagement detection") is stronger than §2.4. Say instead: "models that recognized basic emotions well confused engaged and distracted behavior; no evidence yet of reliable engagement classification for individual students".
- **Frame Combinations:** the caption under the figure repeats the figure's key. Delete it.

### Cite on slide (20 Nov)

Short form on the slide; the full reference is in the manuscript.
- **Two 2026 papers by Sityar & Azcarraga:** apacite labels them 2026a (ICCE) and 2026b (PERSUASIVE).
- **Slides 1, 2, 9, 16, 17, 32, 33 and 34** need no citation: they show your own design, plan or question.

| # | Citations |
|---|---|
| 3 | Fredricks et al., 2004 (the three kinds); D'Mello et al., 2017 (measured automatically) |
| 4 | CHED, 2020 (flexible learning); Gupta et al., 2016 (DAiSEE); Singh et al., 2023 (EngageNet labels) |
| 5 | Gupta et al., 2016 (57.9%); Selim et al., 2022 (67.5%); Whitehill et al., 2014; Korbar et al., 2019; Brkić et al., 2025 |
| 6 | One per row. 2.1: Whitehill et al., 2014 (r = 0.85). 2.2: Singh et al., 2023; Gupta et al., 2016. 2.3: Gupta et al., 2016; Selim et al., 2022. 2.4: Teotia et al., 2024; Goyal et al., 2026 (preprint). 2.5: Wang et al., 2016; Korbar et al., 2019; Tang et al., 2025; Brkić et al., 2025. 2.6: Resurreccion, 2024; Sityar & Azcarraga, 2026a. 2.7: Karpathy et al., 2014; Ng et al., 2015; Junejo et al., 2011 |
| 7 | Singh et al., 2023; Resurreccion, 2024; Sityar & Azcarraga, 2026a (these are inside `positioning.png`; nothing to add) |
| 8 | Resurreccion, 2024; Sityar & Azcarraga, 2026a |
| 10 | Lugaresi et al., 2019 (MediaPipe); Baltrušaitis et al., 2018 (OpenFace, left out) |
| 11 | Wang et al., 2016 (positional); Adams & MacKay, 2007 (BOCPD); Killick et al., 2012 (PELT, left out) |
| 12 | Wang et al., 2016 (frame differences); Junejo et al., 2011 (self-similarity) |
| 13 | Hochreiter & Schmidhuber, 1997; Cortes & Vapnik, 1995; Breiman, 2001; Chawla et al., 2002 (SMOTE) |
| 14 | McNemar, 1947; Holm, 1979; Lakens, 2017 |
| 15 | Brkić et al., 2025; Tang et al., 2025 |
| 18 | Singh et al., 2023 |
| 19 | Lugaresi et al., 2019 (MediaPipe); Qin et al., 2020 (background removal) |
| 20 | Wang et al., 2016 (positional); Truong et al., 2020; Adams & MacKay, 2007 |
| 21 | Truong et al., 2020 (velocity as the simplest window-sliding changepoint). Eq. 4.1 itself is your own formula (B1) |
| 22 | Truong et al., 2020 |
| 23 | Adams & MacKay, 2007 |
| 24 | Adams & MacKay, 2007; Truong et al., 2020 |
| 25 | Wang et al., 2016; Junejo et al., 2011; Hochreiter & Schmidhuber, 1997 |
| 26 | Wang et al., 2016 (frame differences); Junejo et al., 2011 (self-similarity) |
| 27 | McNemar, 1947; Holm, 1979; Efron & Tibshirani, 1993; Lakens, 2017; Chicco & Jurman, 2020 (MCC) |
| 28 | Singh et al., 2023 (user agreement); Republic Act No. 10173 (2012) |
| 29 | Sityar & Azcarraga, 2026b (PERSUASIVE); Carandang et al., 2026 (TENCON); Sityar & Azcarraga, 2026a (ICCE) |
| 30, 31 | Sityar & Azcarraga, 2026a |

### New and changed slides (20 Nov)

**Slide 3. "Engagement has three kinds; video shows mainly the behavioral one, which is what this study detects"** (§1.1, first paragraph; §3.1–3.2) · 1:00. *Replaces Background 1 and the definitions line of the working-definitions slide.*
- **On the slide:** two columns, plus a bottom line.
  - **What engagement is:** a student's involvement in a learning activity (Fredricks et al., 2004), in three kinds:
    - behavioral: participation, attention, effort;
    - emotional: reactions such as interest or boredom;
    - cognitive: investment in understanding, and regulating one's own learning.

    It is not fixed: it responds to the task and the support a teacher gives.
  - **How it is measured:** traditionally by self-reports, teacher ratings and observation; automatically, from signals such as facial expressions and eye movements, at a finer time scale (D'Mello et al., 2017).
  - **Bottom line, "Where this study comes in":** observer-rated engagement from video. That is mainly the behavioral kind, with visible signs of the emotional kind. The cognitive kind is not visible.
- **Say:**
  - Engagement changes during a lesson, which is one reason to measure it.
  - Explain the three kinds in one breath each, then say which one video can show.
  - Doc Jay's framing works as an opener: knowing when a student starts to disengage is what lets support come at the right time.
- **Don't say:**
  - that the study measures what students feel or think;
  - that it will tell teachers when to step in. §1.4 says only that reliable detection *could* help.
- **Source:** §1.1 (first paragraph); §3.1 (Student engagement); §3.2 (last paragraph).

**Slide 6. Related works: what changes on 20 Nov.** The 19 Nov spec ("Review") still applies. Two changes:
- the citations from the "Cite on slide" table, one per row;
- the text fixes above.

  The full table is B18.

**Slide 9. "Research questions and general objective"** · 0:45. *Replaces spec 5.*
- **On the slide:**
  - **The two research questions** (revised 22 Nov, word for word from §1.1):
    1. How does content-based frame selection compare with position-based and random selection in classifying observer-rated student engagement at equal frame budgets, and how does this comparison vary with the frame budget and the classifier?
    2. How much does representing the order and change of the selected frames add to engagement classification, compared with averaging them?
  - **Below it, the general objective,** word for word from §1.2: "to determine whether selecting the frames of a video clip by their content improves the classification of observer-rated student engagement compared with selecting them by their position in the clip."
- **Say:** the two things earlier comparisons couldn't separate:
  - the rule from the number of frames;
  - content-based selection from chance.

  Then: the next five slides take one specific objective each, with what it covers and what it leaves out.
- **Source:** §1.1, §1.2.

**Slides 10–14. One slide per specific objective** · 0:25 each. *Replaces spec 6, and spec 7 in the main deck.*
- **Layout (each slide):**
  - the header "Objective n";
  - the objective in the statement bar, word for word from §1.2, dropping only the leading "To";
  - below it, two columns, **Covers** and **Leaves out**.
- **Contents:** from the §1.3 paragraph tagged with that objective.

| # | Objective (§1.2) | Covers | Leaves out |
|---|---|---|---|
| 10 | 1. "Extract facial and upper-body pose features from the EngageNet video clips" | MediaPipe: 478 face landmarks, 52 blendshapes, 8 upper-body keypoints, 1,518 values per frame; the same features in every condition; valid frames only (face found, face and body consistent); video only | Other feature sets, e.g. OpenFace action units (whether the findings hold with them is not tested); audio, interaction data, quiz answers |
| 11 | 2. "Characterize content-based, position-based, and random frame selection techniques by their effect on engagement classification" | Five rules: SME and positional (position), random (control, five draws), k-Changepoint and k-BOCPD (content); k = 3, 5, 7 (SME at 3 only), so 13 conditions; the same clips in every condition | Every frame (dense sampling); learning which frames to use (attention over all frames); other changepoint methods such as PELT |
| 12 | 3. "Evaluate techniques for representing the temporal aspect of the selected frames, such as their order and how they change, when the frames are combined into a single input for engagement detection" | MLP, SVM, RF: mean (baseline), concatenation, mean + change, mean + self-similarity; LSTM: averaging or attention; each compared with the mean | Frame timing and unselected frames (so the rules stay comparable); other learned sequence representations |
| 13 | 4. "Implement and evaluate various machine learning classifiers for detecting student engagement from the selected frames" | LSTM, MLP, SVM, Random Forest, with the same untuned settings everywhere; one binary task, Highly-Engaged vs. the rest (3,740 vs. 4,139 training clips); macro F1, accuracy, MCC on the subject-independent test split | The four-level task; Not-Engaged as its own task (still reported: how often it is predicted as Highly-Engaged); end-to-end deep networks; vision-language models (reviewed, not tested) |
| 14 | 5. "Determine the best-performing combination of frame selection technique, number of frames, frame combination technique, and classifier" | Chosen on validation macro F1, then reported once on test; differences tested clip by clip (McNemar, Holm), over five seeds or draws; equivalence within ±2 points | Conclusions beyond this dataset, task, feature set and classifiers; "reliable" only if it holds in all five versions; observer-rated engagement only, not what students felt |

- **Say:** one sentence for each column. Don't read the cells.
- **Source:** §1.2; §1.3 (the paragraphs headed Data preparation, Frame selection, Task and classifiers, Vision-language models, Evaluation). The general limits (EngageNet only, not Filipino learners, no classroom system, no demographic comparison) are on the hidden B16.
- **If asked:** Q3 or B10 (Not-Engaged); Q2 or B6 (VLMs); B12 (MediaPipe); Q15 (scope of objective 3).

**Slide 18. "EngageNet: 127 adults, recorded by webcam in the wild, rated by three observers"** (§1.3, §4.2; Singh et al., 2023) · 1:00. *Replaces the 19 Nov Data slide; takes `label-split.png` from slide 4.*
- **On the slide:** a fact panel on the left, `label-split.png` on the right.

  | | |
  |---|---|
  | Participants | 127 adults, aged 18–37: 83 male, 44 female |
  | Task | Watched three lecture videos of about 5 minutes each, and answered questions after each |
  | Setting | In the wild: by webcam, in computer labs, dorm rooms and open spaces |
  | Clips | About 11,300 clips of 10 seconds |
  | Labels | Four levels, from three observers (weighted κ 0.73–0.79), rated from gaze, head pose and facial expression |
  | Split | Official, subject-independent: 91 / 11 / 26 participants (training / validation / test) |
  | Task in this study | Highly-Engaged vs. levels 0–2; training split 3,740 vs. 4,139 clips |

- **Say:**
  - "In the wild" means lighting, backgrounds and cameras vary. That is closer to real online learning, and harder.
  - The labels describe what observers saw.
  - Highly-Engaged is about half of every split, which is why the binary task is close to balanced.
- **Don't say:**
  - "students": the paper says participants, aged 18–37;
  - that the data represent Filipino learners. That is a stated limitation (§1.3).
- **Numbers:**
  - 83/44, the task and the setting are from Singh et al. (2023), §3.1–3.2.1. 83/44 is also added to §1.3 (20 Nov).
  - 91 is counted from the file names. Singh et al. report 90, and the source of the difference is not known.
  - The κ values are from Table 2.1.
- **If asked:** B2 (threshold 3), B11 (common clip set), Q1 (why EngageNet).

**Slide 20. "Position-based rules pick frames by where they are; content-based rules by what happens in them"** · 1:00. *Spec 13, with the new figure and the merged two-kinds cards.*
- **Visual:** `selection-rules.png`, now grouped: Position-based (SME, Positional), Control: chance (Random), Content-based (k-Changepoint, k-BOCPD), with a line between the groups (Doc Jay, 15:27).
- **Say:** spec 13's points. Then the glance:
  - a position-based rule may miss a brief cue between its frames;
  - the two content-based rules look for different moments: the fastest movement, or the start of a lasting change.

  The next four slides show how each one finds them.
- **Source:** §4.4; Algorithm 5.1; §3.4–3.5.

**Slide 21. "k-Changepoint: velocity is how far the landmarks move between two frames, after removing the movement of the whole face"** (Eq. 4.1) · 1:15. *New; Doc Jay's main comment.*
- **Visual:** `velocity-steps.png`. Six schematic landmarks; MediaPipe tracks 478.
- **Say, step by step:**
  1. Each valid frame gives 478 landmark positions, x and y.
  2. Center each frame by subtracting its mean position. A camera shift, or the student sliding in the chair, then doesn't count as movement.
  3. For each landmark, measure how far it moved between the two frames.
  4. Square these distances, add them, and take the square root: that is v_t (Eq. 4.1). Here it is 0.51. Without step 2 it would be 2.44, because the whole-face shift would swamp the two landmarks that really moved.
  5. Repeat for every pair of consecutive frames. This gives the velocity curve on the next slide.
- **The answer to "how does it know it found something?"** It doesn't decide that a change happened. It ranks moments by how fast the face moves and keeps the k fastest.
- **Source:** §4.4 (Eq. 4.1); B1.

**Slide 23. "k-BOCPD tracks how long the face has stayed put, and scores a frame by the chance that a new stretch began there"** (Eq. 4.2) · 1:15. *New; Doc Jay's main comment.*
- **Visual:** `bocpd-run-length.png`. It shows the forward pass on the made-up signal of `bocpd-score.png`.
- **Say, step by step:**
  1. **Signal:** the landmark positions, reduced within the clip to three numbers per frame (the first three principal components), scaled by the first one's standard deviation.
  2. **Segments:** stretches where these numbers vary around a usual value. The value and its spread are learned from the segment's own frames, starting from a weak guess (the prior).
  3. **The run length** is how many frames the current segment has lasted. At every new frame there are two possibilities: the segment continues (run length + 1), or a new one starts (back to 1). Each is weighted by how well the new frame fits, and by the hazard of 1/20, which allows a new segment about every 20 frames. The shading is the result.
  4. **The score of frame t** is the probability that the run length is 7 at frame t + 6, that is, that a segment began at t and has lasted 7 frames. Here, frame 25 scores 0.58.
  5. It is also run backward and the two averaged. Peaks must be at least 7 frames apart, and the top k are kept.
- **Point at the figure:**
  - the diagonal: the face stays put;
  - the quick turn: the long run dips, then recovers;
  - the lasting change at 25: a new diagonal starts from 1 and takes over.
- **Don't say:** that BOCPD is better. It is untested on EngageNet.
- **Source:** §4.4 (Eq. 4.2); §3.5; study guide §11. If asked about settings: study guide §11.6, and "Be ready", question 5 below.

**Slide 24. "On the same clip, velocity peaks keep the fastest movements; k-BOCPD keeps where the face moves and stays"** · 1:00. *New; answers "what is the difference?"*
- **Visual:** `content-rules-compare.png`. Made-up signal, 70 frames, k = 3.
- **Say:**
  - Velocity peaks keep 11, 36 and 50: the two glances and the biggest lasting move.
  - k-BOCPD keeps 22, 35 and 60: the three lasting moves. The glances score low, because the frames after them fit the old segment again.
  - Velocity is not blind to lasting changes. It ranks by speed, so a big glance outranks a smaller lasting move.
  - Which matters for engagement is open. Glancing away is one of the cues observers describe for Not-Engaged clips (§3.1), so the brief moments may carry information. That is what family 4 (12 comparisons) tests.
- **Don't say:** that glances are noise.
- **Source:** §3.5, §4.4, §4.6.

**Slide 26. "Change says how much each feature moved between frames; self-similarity says which frames look alike"** · 1:00. *New; Doc Jay, 24:45.*
- **Visual:** `combination-example.png`. Made-up numbers: 3 frames, 4 features (really 1,518), already standardized.
- **Say:**
  - Mean: the average of each feature.
  - Change: the size of each step between consecutive frames, averaged feature by feature. Frame 3's big step shows up as 1.05.
  - Self-similarity: the cosine of each pair of frames. 0.93 means frames 1 and 2 are alike; −0.72 and −0.73 mean frame 3 differs, as a glance away would.
  - Each is placed after the mean. Mean + change has 8 values here and 3,036 in the study. Mean + self-similarity has 7 here and 1,521 at k = 3.
  - Why standardize first: raw coordinates are all positive, so almost every cosine would be close to 1.
- **Don't say** (from the run-through, 24:17): that self-similarity uses the top three principal components. It uses all 1,518 standardized features of each frame. The principal components belong to k-BOCPD's signal.
- **Source:** §4.5; §3.6.

**Slide 33. "Remaining work: November 2026 to the final defense in March 2027"** · 0:30. *Spec 20, with a new figure.*
- **Visual:** `remaining-work.png`. Only the Planned rows of Table 5.4; the full calendar is B17.
- **Say:** the steps in order, from spec 20's list. Doc Jay (31:03): what matters is the work still to do.

### Be ready (20 Nov)

Doc Jay: "be ready on the details," especially the changepoint method. Thirty-second answers:

1. **"How does velocity-peak selection find a change?"**
   - It doesn't test whether a change happened.
   - For each pair of consecutive frames, it measures how far the 478 landmarks moved after removing whole-face movement (Eq. 4.1).
   - It smooths that over five frames, and keeps the k highest peaks at least seven frames apart.
   - So "change" here means the fastest movement. That is why the manuscript calls it velocity-peak selection, the simplest case of window-sliding changepoint detection (Truong et al., 2020; B1).
2. **"How does BOCPD decide that a change has started?"**
   - It keeps a probability for every possible run length: how long the current segment has lasted.
   - Each new frame either continues the segment or starts a new one, weighted by how well it fits and by the hazard.
   - The score of a frame is the probability that a segment began there and lasted seven frames.
   - A frame is chosen if its score is among the k highest peaks. There is no yes/no threshold.
3. **"What is the difference between them?"**
   - Velocity peaks: the moments of fastest movement, including a glance away and back.
   - k-BOCPD: the moments where the face moves and stays.
   - Comparing them (family 4) tests which kind of moment carries more information about engagement.
4. **"Why center the landmarks?"** So that moving the whole face, as with a camera shift or leaning, doesn't count. On slide 21, centering turns 2.44 into 0.51.
5. **"Why a hazard of 1/20, a prior, a 50-frame cap, and 7 frames?"**
   - All were fixed in advance and not tuned.
   - 1/20 means a segment lasts about 20 scanned frames, about 1.3 seconds. A 150-frame clip then expects about seven changes, as many as the largest k.
   - Seven frames matches the seven-frame minimum gap between peaks.
   - The prior is weak, so a few real frames override it.
6. **"Why standardize before the cosine?"**
   - Raw landmark coordinates are all positive and change little, so almost every cosine would be close to 1.
   - Standardizing uses the training split's mean and standard deviation only.
7. **"Is Eq. 4.1 from a paper?"** It is your own formula; see B1.

---

## Slide specs added 19 Nov

These are still used, except where a 20 Nov spec above replaces them. For example, Background 1 became slide 3, and the Data slide became slide 18.


**Outline: "Outline: one question, followed through the five chapters"** · 0:15 *(removed 20 Nov: the hook question moved to the Part 1 divider)*
- **On the slide:** the hook question, then the five chapters, each with the part of the question it answers.
- **Say:** ask the question out loud, then say the talk answers it one chapter at a time. The preliminary results come in Chapter 5, after the design they led to.

**Chapter dividers** · 0:05 each *(replaced 20 Nov by the four part dividers)*
- **On the slide:** the chapter's question (table above), its sections, and the five-step bar. Read the question and move on.

**Background 1: "Engagement responds to the task and the teacher's support, which is one reason to measure it"** (§1.1, first paragraph) · 0:45 *(replaced 20 Nov by slide 3)*
- **On the slide:** two columns.
  - What it is: involvement in a learning activity; behavioral, emotional and cognitive (Fredricks et al., 2004); not fixed, it responds to the task and the support a teacher gives.
  - How it is measured: traditionally by self-reports, teacher ratings and observation; automatically by models that infer it from signals such as facial expressions and eye movements, at a finer time scale than questionnaires (D'Mello et al., 2017).
- **Don't say:** that the study measures what students feel. That distinction is in Chapter 3.

**Background 2: "In video-based learning, the webcam is the sensor and observers' ratings are the labels"** (§1.1, second paragraph) · 0:45 *(slide 4 on 20 Nov; `label-split.png` and its table moved to slide 18)*
- **On the slide:**
  - CHED (2020) flexible learning, including online delivery;
  - the webcam is available, cheaper and less intrusive than physiological devices;
  - EngageNet's three observers per 10-second clip, rating from gaze, head pose and facial expression.
- **Visual (19 Nov):** `label-split.png`, on the right. Proportional bars show the share of each level in all splits, training, validation and test. The levels run light to dark blue, and a dashed line marks 50%.

  | | Clips | Not-Engaged | Barely-engaged | Engaged | Highly-Engaged |
  |---|---|---|---|---|---|
  | All splits | 11,206 | 18.2% | 12.3% | 21.0% | 48.6% |
  | Training | 7,879 | 18.4% | 13.1% | 21.0% | 47.5% |
  | Validation | 1,071 | 12.3% | 9.1% | 25.5% | 53.1% |
  | Test | 2,256 | 20.3% | 10.9% | 18.6% | 50.3% |

  The counts are Table 5.3 by subtraction (training: 1,446 / 1,035 / 1,658 / 3,740) and match the official label files. The "All splits" row equals §2.2's 18.16 / 12.3 / 20.97 / 48.57%.
- **On the left, under the bullets:** "What observers looked for":
  - Not-Engaged: often glances away; appears disinterested;
  - Barely-engaged: fidgeting;
  - Highly-Engaged: "glued to the screen".
  The descriptions are from §3.1 and §3.3; Engaged has none in the manuscript.
- **Say:** a classifier trained on these labels learns to reproduce what observers saw. Highly-Engaged is about half of every split, so Highly-Engaged vs. the rest is close to 50/50. The cues are brief; they come back.
- **Don't say:** that the splits have the same distribution. Not-Engaged ranges from 12.3% (validation) to 20.3% (test).

**Background 3: "A clip has over 100 frames, and which few reach the classifier has rarely been tested"** (§1.1, third paragraph) · 0:45. *Replaces spec 3. Slide 5 on 20 Nov.*
- **On the slide:**
  - DAiSEE 57.9% → 67.5% from features and networks;
  - most approaches use every frame or a fixed subsample;
  - when only a few frames are kept, which ones may matter (Whitehill et al., 2014; the selection rule changes results in video understanding).
- **Visual:** the glance strip. 24 cells; amber at 9–11 (the glance); green at 5, 13 and 21 (three evenly spaced frames, which miss it). The caption says it is made up and ends with "Would frames chosen by what happens in them do better?"
- **Don't say:** that evenly spaced frames always miss such cues.

**Background 4: "Two earlier comparisons of selection rules could not show why one rule did better"** (§1.1, third and fourth paragraphs) · 0:45 *(slide 8 on 20 Nov, after Related works and Synthesis)*
- **On the slide:**
  - two cards: Resurreccion (2024), DAiSEE; the preliminary study (2026), EngageNet;
  - the two confounds: the rule or the number of frames? better than chance?;
  - the problem statement of §1.1 as the last line.
- **Say:** the details of the preliminary study come at the end, in Part 4.

**Working title: "Significance: evidence on a design choice that is usually fixed without testing"** (§1.4) · 0:30 *(slide 15 on 20 Nov, ✂)*
- **On the slide:** whether content-based, position-based, or either beats chance at equal budgets; fast movement vs. lasting change; whether order and change add to the average; the reusable protocol (common clip set, paired tests over seeds and draws, equivalence margin, rules fixed in advance); the best configuration, within this dataset and task; relevance to VLMs, which also receive only a few frames.
- **Say:** the protocol answers the single-seed result that reversed in other seeds. The number of frames kept also sets the extraction cost, because the second pass runs once for each selected frame. Not a classroom tool.
- **Don't say:** that the study will help instructors detect disengagement. §1.4 says only that reliable detection *could* help.

**Working title: "The review narrows from engagement detection to how frames are used"** (§2.1–2.7) · 1:00 *(slide 6 on 20 Nov; add the citations and text fixes above)*
- **On the slide:** a table, one row per section, with what each means for this study:
  - 2.1: webcam video alone is the practical case; clip labels can be predicted from the average of frame labels (r = 0.85).
  - 2.2: EngageNet has 127 participants and three annotators (weighted κ 0.73–0.79), a subject-independent split, and labels less skewed than DAiSEE's.
  - 2.3: gains came from features and networks (DAiSEE 57.9% → 67.5%); each paper fixes how frames reach the model.
  - 2.4: there is no evidence yet of reliable zero-shot engagement classification for individual students; VLMs are not tested here.
  - 2.5: content-based selection can beat even coverage, but no rule is best for every task.
  - 2.6: most works use every frame or a fixed subsample; two studies compare rules, both at three frames.
  - 2.7: whether order and change add to the average is unsettled, and not examined at small frame budgets.
- **Say:** one line per row. 2.4 is OCE revision R2 (details on B6).
- **Don't say:** that frame selection has never been studied. It has, in video understanding (§2.5).
- **Source:** §2.1–§2.7, Tables 2.1–2.4.

**Working title: "Working definitions: engagement is what observers rated from visible behavior"** (§3.1–3.3) · 0:45 *(moved to backup B15 on 20 Nov; its definitions line is now on slide 3)*
- **On the slide:** a table of six of the 14 terms in §3.1:
  - student engagement;
  - observer-rated engagement;
  - position-based selection and content-based selection;
  - frame budget k;
  - temporal representation.
  Below it, one line: video shows mainly behavioral engagement, with visible signs of emotional engagement; cognitive engagement is not visible.
- **Say:** this is OCE revision R1. Affect, emotion and academic emotion are defined to keep them apart from engagement. The features describe what observers could see: facial movement (52 blendshapes, 478 landmarks), gaze (8 of the blendshapes), and posture (8 upper-body keypoints). A facial configuration is not read as a specific emotion (Barrett et al., 2019).
- **Source:** §3.1–§3.3.

**Working title: "Position-based rules cover the clip; the two content-based rules look for different moments"** (§3.4–3.5) · 0:45 *(merged on 20 Nov into slides 20 and 24)*
- **On the slide:** three cards.
  - Even coverage (Temporal Segment Networks): with 3–7 of 100+ frames, brief cues can be missed.
  - Velocity peaks, the simplest case of window sliding: more likely to catch a glance away, but also speaking or shifting position.
  - BOCPD, which tracks how long the current segment has lasted: a glance away and back gives weak evidence; a move that stays gives strong evidence.
  - Under the cards: which kind of moment carries engagement information, and whether either beats random selection, is what the study tests.
- **Say:** the settings come in Chapter 4.
- **Don't say:** that BOCPD is better. It is untested on EngageNet.
- **Source:** §3.4, §3.5.

**Working title: "Conceptual framework: what varies and what is held constant"** (§3.9) · 0:45 *(slide 16 on 20 Nov)*
- **Visual:** `conceptual-framework.png`
- **On the slide:**
  - independent: the selection rule and k, the frame combination, the classifier;
  - dependent: macro F1, accuracy, MCC;
  - held constant: dataset and split, features, task, classifier settings, training, seeds;
  - the expectation: if the fastest moments match the cues observers used, content-based beats position-based and random selection; if not, it does no better than random.
- **Say:** for k-BOCPD, if lasting changes mattered more to observers, k-BOCPD should beat velocity peaks. Table 4.3 lists how each pattern will be read. §3.6–3.8 come up with the methods in Chapter 4.
- **Source:** §3.9, Figure 3.1.

**✂ Working title: "Data: the official EngageNet split, one binary task, one common clip set"** (§4.2) · 0:45 *(replaced 20 Nov by slide 18, which keeps these points in its notes)*
- **On the slide:**
  - the split table (Table 4.2, official columns). Participants, labeled clips and SNP clips: training 91, 7,983, 104; validation 11, 1,071, 0; test 26, 2,257, 1;
  - the task: Highly-Engaged (level 3) vs. levels 0–2;
  - the full training split: 3,740 vs. 4,139 clips;
  - the common clip set.
- **Say:**
  - 91 is counted from the file names; Singh et al. report 90, and the source of the difference is not known.
  - The preliminary study used part of the training split and no SMOTE, so its numbers are not directly comparable.
  - Comparisons within the proposed study are unaffected.
- **Source:** §4.2, Table 4.2. If asked: B2, B11, Q9.

**Working title: "Which few frames should a classifier see? The study compares content, position and chance at equal budgets"** (closing; eyebrow "Back to the question") · 0:20 *(slide 34)*
- **On the slide,** what the study will show (§2.8):
  - whether content beats position;
  - whether either beats an arbitrary choice, and how much the number of frames matters;
  - whether a brief movement, such as a glance, or a lasting change marks the more useful frames;
  - whether order and change add to the average.
  - Then "Thank you."
- **Say:** close the loop with the glance. Evenly spaced frames can miss it; the study measures whether frames chosen by content do better, and whether that beats chance. Leave this slide up during questions.

---

## Figures

| File | Slide (20 Nov order) | Made from |
|---|---|---|
| `positioning.png` | 7 | Table 2.5 |
| `conceptual-framework.png` | 16 | Figure 3.1 |
| `design.png` | 17 | Table 4.1, §4.5 |
| `label-split.png` | 18 (moved from 4) | Table 5.3 by subtraction, checked against `data/labels/` (19 Nov) |
| `pipeline.png` | 19 | Figure 4.1, §1.3 |
| `selection-rules.png` | 20 | §4.4; frames for n = 20, k = 3; grouped into position-based, control, content-based (20 Nov) |
| `velocity-steps.png` | 21 (new) | Eq. 4.1 on six schematic landmarks, made-up positions; arithmetic printed by `charts.py` |
| `velocity-peaks.png` | 22 | made-up signal, labeled as such |
| `bocpd-run-length.png` | 23 (new) | run-length probabilities of the forward pass on the `bocpd-score.png` signal; §4.4 settings |
| `content-rules-compare.png` | 24 (new) | one made-up signal under both content rules, k = 3 |
| `frame-combinations.png` | 25 | §4.5 |
| `combination-example.png` | 26 (new) | made-up numbers, 3 frames × 4 features; checked with a script |
| `prelim-macro-f1.png` | 30 | Table 5.1 |
| `prelim-vs-sme.png` | 31 | Table 5.2 |
| `remaining-work.png` | 33 (new) | Table 5.4, Planned rows |
| `class-balance.png` | B2 | Table 5.3 |
| `interpretation.png` | B14 (was main) | Table 4.3 |
| `calendar.png` | B17 (was main) | Table 5.4 |
| `bocpd-score.png` | B19 (was main) | made-up signal, labeled as such; §4.4 settings |

To rebuild after a change, run from the repo root:

```
conda run -n thesis-engagenet python -I proposal-defense/figures/src/charts.py
conda run -n thesis-engagenet python -I proposal-defense/figures/src/build_tex.py
```

---

## Main slides

These are numbered as specs; the order you present them in is the running order above.
- **20 Nov:** the running order table says which slide each spec became. Specs 5, 6, 7, 14b and 18 were replaced or moved; their notes say where.

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

### 3. *(Replaced on 19 Nov by Background 3, under "New slides"; kept here for its sources and Q&A pointers.)* Working title: "Classifiers see only a few frames of each clip, and which frames is rarely tested" · 1:00
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

### 4. Working title *(retitled 19 Nov, because Background 4 now states the problem)*: "Only this study compares the rules at three matched frame budgets and against a random control" · 0:30
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
- **20 Nov:** replaced by slide 9 (research question and general objective).
- **On the slide (superseded 22 Nov; see slide 9):** the two research questions, word for word from §1.1.
- **Say:** the two things earlier comparisons couldn't separate:
  - the rule from the number of frames;
  - content-based selection from chance.
- **Visual:** none. The conceptual framework now has its own slide in Chapter 3 (19 Nov).
- **Source:** §1.1, §2.8.

### 6. Working title: "One general and five specific objectives" · 1:00
- **20 Nov:** replaced by slides 10–14, one per objective; the general objective moved to slide 9.
- **On the slide:** the general objective, plus the five specific objectives, shortened without changing their meaning:
  1. extract features;
  2. characterize the selection techniques;
  3. evaluate temporal representations;
  4. implement and evaluate the classifiers;
  5. find the best-performing combination.
- **Say:** objectives 3 and 5 were added at Dr. Azcarraga's request (13 Nov).
- **Source:** §1.2.
- **If asked:** Q15: "Doesn't adding temporal representations broaden the scope again?"

### 7. Working title *(redone 19 Nov, because it was hard to read at a glance)*: "Within each classifier, only the frames and how they are combined change. Everything else is held fixed." · 0:45
- **20 Nov:** hidden as backup B16 (Doc Jay, 37:06). Its rows are now split by objective on slides 10–14.
- **On the slide:** a table with one row per decision. "Included" is in blue and "Left out" in gray, side by side:

  | | Included | Left out |
  |---|---|---|
  | Data | EngageNet and its official split | Other datasets; audio |
  | Task | Highly-Engaged vs. all other clips | The four-level task; Not-Engaged on its own |
  | Frames | 3, 5 or 7 frames per clip, by five rules | Every frame; learning which frames to use |
  | Features | The same MediaPipe face and pose features | Other features, e.g. OpenFace action units |
  | Classifiers | Four classifiers, same settings, no tuning | End-to-end networks; vision-language models |
  | Purpose | Comparing frame selection rules | A classroom tool; demographic comparisons |

  The bottom line is the limitation: conclusions hold for this dataset, task, feature set and set of classifiers, and for observer-rated engagement only.
- The split sizes (91 / 11 / 26 participants) and 1,518 values per frame moved to the speaker notes and the §4.2 data slide.
- **Say:** pick two rows; don't read every cell.
- **Say:** Not-Engaged stays in the negative class for three reasons:
  - one task keeps the study focused;
  - the preliminary results exist only for this task;
  - a second task would double the 254 comparisons.

  How often Not-Engaged clips are predicted as Highly-Engaged is still reported.
- **Source:** §1.3.
- **If asked:**
  - Q3 or B10: Not-Engaged.
  - Q2 or B6: VLMs.
  - B12: MediaPipe vs. OpenFace.
  - Q1: why EngageNet.

### 8. ✂ Working title: "Preliminary work: two DAiSEE papers, then the preliminary study on EngageNet" · 1:00 *(papers folded in, 18 Nov)*
- **20 Nov:** slide 29, no longer ✂, but shortened to 0:30. Doc Jay (27:35): pass through it; it shows the panel you published three papers, so no specifics are needed. Showing the DAiSEE work is fine: you were exploring which dataset to use. Cite as in the "Cite on slide" table.
- **On the slide:** three cards.
  - **PERSUASIVE 2026 (published):** SME sampling, feature sets, per-frame vs. change features, binarization thresholds on DAiSEE. Kept: SME as the reference rule; threshold 3.
  - **TENCON 2026 (accepted for publication):** quantum vs. classical classifiers on DAiSEE; three frames per clip by BOCPD; one selection rule only. Kept: BOCPD, now tested against other rules.
  - **ICCE 2026 (accepted for presentation):**
    - EngageNet, threshold 3;
    - SME (k = 3) vs. k-Changepoint (k = 3, 5, 7);
    - LSTM, MLP, SVM, Random Forest;
    - 2,719 / 867 / 2,005 clips (training / validation / test);
    - neural networks: five seeds.
- **Source for the papers:** §5.1.1; Appendix B. Your TENCON role is in study guide §10.3, item 5.
- **Say:** three differences from the proposed study:
  - only part of the training split;
  - no SMOTE;
  - the MLP, SVM and Random Forest got only the mean of the frames.
- **Source:** §5.1 (second paragraph); Table 4.2.
- **If asked:** Q9: why only part of the training split.

### 9. Working title: "Every classifier had its highest macro F1 with three velocity-peak frames" · 1:00
- **20 Nov:** slide 30. Say that these results are from the ICCE paper (Sityar & Azcarraga, 2026a), and put that on the slide.
- **One point:** the direction was consistent across classifiers. Whether it is reliable is the next slide.
- **Visual:** `prelim-macro-f1.png`
- **Say:**
  - Best: SVM with 3-Changepoint, 0.701 macro F1 (0.7017 accuracy).
  - Classifiers differed more than conditions did. The SVM was 8.9 to 12.0 accuracy points above the Random Forest, while no condition changed a classifier's accuracy by more than 4.8 points.
  - LSTM and MLP values are means over five seeds.
- **Don't say:** "3-Changepoint is better". This slide shows the highest means, not a test.
- **Source:** Table 5.1; §5.1.

### 10. Working title: "Only the Random Forest improved significantly over SME" · 1:00
- **20 Nov:** slide 31; also from the ICCE paper.
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
- **20 Nov:** slide 32, ✂.
- **On the slide:** a two-column table (gap → change):

  | Gap | Change |
  |---|---|
  | position-based rule only at k = 3 | positional selection at 3, 5, 7 |
  | no random baseline | random selection, five draws |
  | frame budgets not compared | test family 5: k = 3 vs. 5 vs. 7 |
  | neural tests on a single seed | five seeds or draws; reliable only if significant in all five |
  | MLP, SVM, RF got only the mean | three temporal representations |

- **Source:** §5.1 (last paragraph); §4.1, §4.4, §4.5, §4.6.

### 12. Working title: "Thirteen selection conditions, each run with four classifiers" · 1:15
- **20 Nov:** slide 17.
- **Visual:** `design.png`
- **Say:**
  - Four rules × three budgets, plus SME at k = 3, gives thirteen conditions. SME is kept to link to the preliminary study.
  - Two of the rules are content-based: velocity peaks (from the preliminary study) and k-BOCPD (new).
  - Within each condition, the frames are combined four ways for the MLP, SVM and Random Forest, and two ways for the LSTM.
  - Dataset, split, features, task and classifier settings are the same everywhere, so conditions differ only in which frames are used and how they are combined.
- **Source:** §4.1, Table 4.1, §4.5.
- **If asked:**
  - Q7: why 3, 5, 7.
  - Q6: why a random baseline.

### 13. Working title: "On one clip, the five rules pick different frames" · 1:00
- **20 Nov:** slide 20, with the grouped figure; see "Slide 20" under the 20 Nov specs.
- **Visual:** `selection-rules.png`
- **Say:**
  - SME: first, middle, last.
  - Positional: the centre of each of k equal parts (from Temporal Segment Networks).
  - Random: uniform draws, seeds 42–46. The draws are nested, so a larger budget only adds frames.
  - k-Changepoint: the frames at the k highest velocity peaks.
  - k-BOCPD: the frames where a lasting change begins. It needs 7 valid frames on each side, so on this 20-frame example it keeps only one frame. Real clips have up to 150.
  - At k = 3, SME vs. positional tests whether the first and last frames matter (family 6).
  - Tell the audience that the random and content-based frames on the slide are an example.
- **Source:** §4.4; Algorithm 5.1.
- **If asked:** B3 (Algorithm 5.1).

### 14. ✂ Working title: "k-Changepoint keeps the frames where the face moves fastest" · 1:00
- **20 Nov:** slide 22, no longer ✂. Slide 21 now explains the computation, so here say only the smoothing, the 7-frame gap and the top k.
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
  - Q12 and B7: why two content rules; PELT.

### 14b. ✂ Working title: "k-BOCPD keeps the frames where a lasting change begins" · 1:00 *(added 15 Nov)*
- **20 Nov:** replaced by slides 23 (run length and score) and 24 (the comparison). `bocpd-score.png` is now backup B19.
- **Visual:** `bocpd-score.png`. Say it is a made-up signal.
- **On the slide:** the idea in words. The face's landmark positions, reduced to 3 components within the clip, are split into segments of stable behavior. The score of a frame is the probability that a new segment begins there, judged 7 frames later.
- **Say:**
  - Velocity peaks find fast movement. A quick turn and back makes a peak even though nothing lasts.
  - BOCPD finds where the face moves *and stays*: frames 25 and 44 on the slide score high, and the quick turn scores low.
  - The budget is always filled, so the third frame here is the quick turn, at a low score.
  - It's run forward and backward and the two scores averaged, with run lengths capped at 50 frames. Run forward only, it favored the start of the clip in my synthetic check.
  - All settings (hazard 1/20, prior, cap, 7 frames) are fixed in advance and not tuned.
- **Source:** §4.4 (Eq. 4.2), §3.5. Study guide §11.
- **If asked:** study guide §11.6 (settings, backward pass, 3 components, power).

### 15. ✂ Working title: "Every clip goes through the same pipeline; only the highlighted steps change" · 1:00
- **20 Nov:** slide 19, ✂. **Don't say** "the clips that aren't valid are removed" (run-through, 18:11). Frames without a detected face are dropped. A clip leaves only the common clip set, under the stated conditions, e.g. fewer than 14 valid frames under k-BOCPD.
- **Visual:** `pipeline.png`
- **Say:**
  - First pass, on every second frame: face and pose, the validity check, and the landmark positions and velocity that the two content rules use.
  - Selection.
  - Second pass, on the selected frames only: background removed; 1,518 values per frame (1,434 landmark coordinates, 52 blendshapes, 32 pose values).
  - Then the frames are combined and passed to a classifier.
  - SMOTE balances the training split only.
- **Source:** §1.3 (Data preparation), §4.3, Figure 4.1.
- **If asked:**
  - B12: MediaPipe.
  - B5: SMOTE.

### 16. Working title: "Four ways to combine the selected frames, and two readouts for the LSTM" · 1:15
- **20 Nov:** slide 25. Slide 26 now works through mean + change and mean + self-similarity on numbers. **Don't say** that self-similarity takes the top three principal components (run-through, 24:17).
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

### 17. Working title: "Conditions are compared clip by clip, in 254 comparisons fixed in advance" · 1:00
- **20 Nov:** slide 27.
- **On the slide:**
  - **Metrics:** macro F1 (primary), accuracy, MCC.
  - **Tests:** exact McNemar tests, with Holm–Bonferroni correction within each family.
  - **Families** (a small table you build):

    | Family | Comparisons |
    |---|---|
    | content vs. position (both content rules) | 24 |
    | content vs. chance (both content rules) | 24 |
    | position vs. chance | 12 |
    | velocity peaks vs. BOCPD | 12 |
    | frame budget | 48 |
    | clip boundaries | 4 |
    | temporal representation | 130 |
    | **total** | **254** |

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
- **20 Nov:** **moved to backup B14** (Doc Jay, 25:49: too much for the main talk). If asked how results will be read, say "I have a slide on that" and show it.
- **Visual:** `interpretation.png`
- **Say:**
  - This answers R4 in advance. For example, if velocity peaks ≈ random, you will not claim that velocity peaks carry engagement information.
  - The second block reads the two content rules against each other: lasting change vs. fast movement.
  - Temporal representations: for each one and each classifier, replicability analysis (Dror et al., 2017) estimates in how many of the 13 conditions it beats the mean. It "improves on the mean" if that count is at least 7 in every version, and it is never shown to be worse. The count is a 95% lower bound and is valid even though the conditions share clips.
- **If asked "why 7?":** more than half, i.e. most conditions; it's a choice fixed in advance. What the method adds is a known error rate for the count (study guide §12).
- **Check before the defense:** this rule replaced the old D25 rule on 15 Nov (D51). Mention it to Dr. Azcarraga along with the fifth rule.
- **Source:** Table 4.3; §4.6.5 (Eq. 4.3).

### 19. Working title: "Pre-existing data, used under the EngageNet user agreement and the Data Privacy Act" · 0:45
- **20 Nov:** slide 28.
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

### 20. Working title: "Remaining work: November 2026 to the final defense in March 2027" · 0:30 *(changed 19 Nov)*
- **20 Nov:** slide 33, with `remaining-work.png` (Planned rows only). The full calendar is backup B17.
- **Visual:** `calendar.png`. Point only at the Planned rows.
- **Remaining steps** (keywords on the slide, from §5.2.1, in order): new rules (positional, random, k-BOCPD); extraction for all 13 conditions; common clip set, with exclusions reported; frame combinations and LSTM attention; training with SMOTE, five seeds; 254 comparisons and the best configuration; final manuscript and defense.
- The contributions that were on this slide moved to the §1.4 slide in Chapter 1. The thanks moved to the closing summary slide.
- **Source:** §5.2.1, Table 5.4.

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
- If asked how many training runs: 590. This is **your own count, not stated in the manuscript**:
  - LSTM (2 readouts) and MLP (4 combinations) × 13 conditions × 5 seeds = 390;
  - SVM and RF (4 combinations each) × (10 fixed conditions + 3 random × 5 draws) = 200.

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

### B7. Why two content rules, and why not PELT *(rewritten 15 Nov)*
- Velocity peaks (kept from the preliminary study) find fast movement; BOCPD finds the beginnings of lasting changes. Comparing them tests which kind of moment carries more information (family 4).
- Velocity peaks keep the pilot evidence, so the main question doesn't depend on BOCPD's untested settings.
- PELT is not used: like BOCPD, it looks for lasting changes. The study compares two definitions of content, not every changepoint method.
- **Source:** §1.3, §3.5, §4.4. Study guide Q12, §11.

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
- The three reasons it isn't a separate task (as in spec 7, and on slide 13).
- For every condition, the study reports the share of Not-Engaged, Barely-engaged and Engaged clips predicted as Highly-Engaged.
- Threshold 1 is left for future work.
- **Source:** §1.3, §4.6.1, §5.2.3. Study guide Q3.

### B11. Common clip set
- Every condition is scored on the same clips. Without this, a difference could come from scoring different clips rather than from selecting different frames.
- Preliminary study: 2,719 / 867 / 2,005 clips.
- **Source:** §4.2.3.

### B12. MediaPipe rather than OpenFace action units
- MediaPipe gives both the landmarks that the two content rules need and the classifier features.
- Blendshapes have not been shown to work better than action units, and results with action units are not tested. This is stated as a limitation.
- **Source:** §1.3, §3.3.

### B13. Conceptual framework *(moved to the main deck on 19 Nov as the §3.9 slide; no longer a backup)*
- **Visual:** `conceptual-framework.png`
- Independent variables: the selection rule and k, the frame combination, the classifier.
- Dependent variable: macro F1, accuracy, MCC.
- Everything else is held constant.
- **Source:** §3.9, Figure 3.1.


### B14. Interpretation of outcomes *(moved from the main deck, 20 Nov)*
- **Visual:** `interpretation.png`. Notes as in spec 18.

### B15. Working definitions *(moved from the main deck, 20 Nov)*
- The 19 Nov spec "Working definitions", or a screenshot of the §3.1 definitions list. It is the evidence for R1 if asked.

### B16. Scope and limitations, general *(hidden, 20 Nov)*
- Spec 7's table. Add the general limits:
  - EngageNet only, so the results may not carry over to Filipino learners or other datasets;
  - pre-existing data only;
  - no classroom system;
  - no comparison across demographic groups;
  - processing time measured on your computer only.
- **Source:** §1.3 (Data and participants, Exclusions).

### B17. Full calendar *(was slide 36 on 19 Nov)*
- **Visual:** `calendar.png` (Table 5.4).

### B18. Related works in full
- A screenshot of Table 2.4 from `main.pdf`, with its citations (Doc Jay, 50:55: "screenshot it, put it on a hidden slide, just in case they want to ask").
- It has no participant data, so a screenshot is fine.

### B19. k-BOCPD on the example signal, both directions
- **Visual:** `bocpd-score.png`. Spec 14b's notes still apply.

### B20. OCE slides on the algorithms *(Doc Jay, 51:19: "be ready; they had more detail")*
- **From** `oral-comprehensive-exam/Affective Computing in Education – OCE.pdf`:
  - page 42: frame selection methods, from every frame to three;
  - pages 43–44: OCE backups B18–B19, frame selection methods 1 of 2 and 2 of 2;
  - page 46: OCE backup B20, changepoint methods and trade-offs (PELT, binary segmentation, BOCPD).
- **Check each one against the current manuscript before you reuse it.**
  - **Leave out page 45** ("Find the change points: PELT or BOCPD"). The study now uses velocity peaks and k-BOCPD, not PELT. If you keep it, caption it "OCE version, 29 Oct".
  - **Page 41** says a 10-second clip has about 300 frames. That is all frames at 30 fps. The study scans every second frame, so it has up to 150 valid frames.

---

## Before you present

- [ ] Every title matches what its slide shows.
- [ ] Every number on a slide appears in this file or in the manuscript at the cited place.
- [ ] No frame, face, or still from EngageNet on any slide.
- [ ] Timed once out loud. If you're over time, cut the ✂ slides first.
- [ ] The interpretation slide's rule (spec 18, now backup B14; D51, replicability analysis; it replaced D25 on 15 Nov) has been mentioned to Dr. Azcarraga.
- [ ] The research questions on slide 9 match §1.1 word for word, and Doc Jay has seen the 22 Nov wording.
- [ ] Every claim has its citation (see "Cite on slide").
- [ ] The 20 Nov text fixes are done ("featues", "Frederiks", the "Excluded" header, "is has", the VLM row).
- [ ] You can give the seven "Be ready" answers out loud without notes.
- [ ] Export the deck to PDF (in Canva: Share → Download → PDF Standard) into `proposal-defense/`, so it can be reviewed against the manuscript.
