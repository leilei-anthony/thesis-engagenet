# Summary of Revisions: OCE Panel Report (29 Oct 2026) to Thesis Proposal

The panel's wording below is quoted from the OCE Panel Report (version 7OCT2026; chair Dr. Thomas James Z. Tiam-Lee).

Use this for the proposal defense, either as a slide or as a handout. Section numbers refer to the 5 Nov 2026 draft; re-check them after your revisions.

## Required revisions

| # | Panel's wording | What was done | Where |
| :-- | :--- | :--- | :--- |
| R1 | "Establish working definitions for important concepts relevant to your study (e.g., affect, engagement)." | Twelve working definitions, conceptual and operational. *Affect* is used in the narrow core-affect sense (Russell, 2003), separated from *emotion* and *engagement*. Engagement follows Fredricks et al. (2004); its operational definition is the observer-rated EngageNet label, with the limit that it measures perceived, not felt, states (Barrett et al., 2019). | §3.1; used consistently in Ch. 1–4 |
| R2 | "Consider adding references on the use of generative AI (MLLM or VLM) in classifying engagement." | A dedicated section and comparison table of six VLM/MLLM works: emotion (Emotion-LLaMA), academic emotion (CLIP-CAER; Wang et al.), and engagement (Teotia et al.; Goyal et al.; Vedernikov et al.). Preprints are labeled as such. The section explains why VLMs are reviewed but not tested: unreliable zero-shot engagement results, dataset license terms, and scope. It also notes that the study's question applies to them, because VLMs also receive only a few frames. | §2.4; §1.3 (Vision-language models); §1.4 |
| R3 | "Ensure that the selection of papers and the discussion flow is intentionally designed to introduce and position the study." | Chapter 2 is a funnel: detection in general, then datasets, models, VLMs, frame selection in video understanding, and frame use in engagement. Each section ends with the gap it leaves. §2.7 compares the study directly with the closest prior work (Table 2.5) and states the gap. | Ch. 2, esp. §2.6–2.7 |
| R4 | "Tone down the sweeping conclusions that are not supported by the data." | Every headline claim of the preliminary study was audited against the data (`notes/claim-audit.md`). Only the revised wording appears in the manuscript; for example, "significant only for the Random Forest", not "every architecture improved". Interpretations of the planned results are fixed in advance (Table 4.3), and a difference counts as reliable only if it holds in all five seeds or draws. | §4.6, §5.1; Ch. 1 problem statement |

## Rubric comments

| Panel's comment | What was done | Where |
| :--- | :--- | :--- |
| "The scope seems to be very broad, and would benefit from a tighter narrative that narrows into the specific study." | One question (content vs. position vs. random frame selection at equal budgets), one dataset, one binary task, fixed features and classifier settings. The background follows the inverted pyramid down to the research question. Exclusions are stated explicitly. | §1.1, §1.3 |
| "Look into more reputable publications and key papers and datasets relevant to the task." | The datasets compared are DAiSEE, EngageWild, EngageNet, CMOSE, and RAER. Sources are now mostly journals (IEEE TAC, ACM CSUR, ACM TiiS, Applied Intelligence) and major venues (ICCV, CVPR, NeurIPS, ECCV, ICMI). Preprints are labeled in the text. | Table 2.1; Ch. 2 |
| "Over-reliance on AI-generated slides." | Each section was taught to and reviewed by the proponent before approval. An AI-use disclosure is being discussed with the adviser. | `notes/ai-disclosure-draft.md` |
| "Going into more detail into the references and materials." | A must-read list with the sections to read for each core paper. | `notes/study-guide.md`, `notes/literature-matrix.md` |
| Suggested reading: Zhao et al., ICCV 2025 | Reviewed as a dataset (RAER) and as a VLM-based method (CLIP-CAER). The text explains why it labels academic emotion rather than engagement levels and is therefore not used. | §2.2, §2.4 |

## Other changes since the OCE

- **Design.** Positional and random selection added at 3, 5, and 7 frames, which separates the effect of the selection rule from the frame budget and from chance. **Pending Dr. Azcarraga's confirmation.**
- **Data.** All 91 training participants will be used. The preliminary study used 32 because the download was incomplete.
- **Title** changed to "Position-Based versus Content-Based Frame Selection for Detecting Student Engagement in Video-Based Learning".
- **Terminology.** The "*k*-Changepoint" name is kept but explained as velocity-peak selection, a minimal case of window-sliding changepoint detection (§3.5). PELT and BOCPD, which were shown at the OCE, are named as not used (§1.3, §3.5).
- **Training.** SMOTE balances the training data in every condition (§4.5).
- **Reporting.** Two descriptive additions: processing time per condition, and how often Not-Engaged, Barely-engaged and Engaged clips are predicted as Highly-Engaged (§4.6.1).
- **Objectives (adviser, 13 Nov).** The objectives are rewritten as broad goals: one general objective and five specific objectives, with the details moved to Scope and Limitations (§1.2–1.3). Two objectives were added at the adviser's request:
  - assessing how the temporal aspect of the selected frames is represented: mean vs. concatenation, change, and self-similarity, plus the LSTM readouts (§2.7, §3.6, §4.5);
  - identifying the best-performing configuration, chosen on the validation split (§4.6.6).

  The research question still concerns frame selection. The new comparisons need no new data or feature extraction, and they form their own test family (§4.6.2), so the frame-selection tests are unaffected.
- **Preliminary study.** Cited as accepted for publication (Sityar & Azcarraga, 2026). Its tables are marked as adapted from the paper, and the manuscript states where its interpretation is narrower than the paper's (§5.1).
- **Chapter 5 (adviser, 14 Nov).** A new chapter, "Preliminary Results and Future Work". It holds:
  - the preliminary results (§5.1);
  - the remaining steps of the thesis (§5.2.1);
  - frame selection and the training and evaluation procedure, as algorithms (§5.2.2);
  - why the binary task uses threshold 3, with class sizes for thresholds 1 to 3 (§5.2.3);
  - the calendar, a table from MSLABS1 (May 2025) to the final defense in late March 2027, with one bullet per term or month (§5.3, Table 5.4).

  §1.3 also gains a "Data preparation" paragraph on how each clip, and its selected frames, become one classifier input.
