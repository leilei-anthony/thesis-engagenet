# ICCE 2026 talk: notes for the presenter

**Slot:** short paper, 10 minutes plus 5 minutes of Q&A ([guidelines](https://icce2026.csse.canterbury.ac.nz/paper-and-poster-presentation-guidelines/)).

**Deck:** `sityar-icce2026.pptx`, built on the official ICCE template. The spoken script and a "Reminders" list are in each slide's speaker notes. `sityar-icce2026.pdf` is the copy for the USB stick.

**Status:** this is a first draft by Claude. Reword it into your own voice before you send it to Doc Jay (due 21 Nov).

## Files

| File | What it is |
|---|---|
| `ICCE-2026-Presentation-Slide-Template.pptx` | The official template, unchanged |
| `sityar-icce2026.pptx` / `.pdf` | The deck: 13 main slides, a references slide, and backups B1–B6 (slides 15–20) |
| `build_deck.py` | Builds the first draft from the template. After you edit the .pptx by hand, don't re-run it: it would overwrite your edits |
| `figures/src/charts.py` | Builds the six figures. Result numbers come from `paper.tex` Tables 1–2 |

**To rebuild** (from the repo root):
- **Figures:** `conda run -n thesis-engagenet python -I paper/icce-presentation/figures/src/charts.py`
- **Deck:** `python paper/icce-presentation/build_deck.py`. This needs base Anaconda, because python-pptx isn't in the project env.

## Running order and timing

The script is 1,050 words, about 8:45 at 120 words a minute. That leaves about a minute for pauses and clicks.

| # | Slide | Point | Script |
|---|---|---|---|
| 1 | Title | Who, and what the talk is about | 0:20 |
| 2 | Detecting engagement … starts with choosing a few frames | Why it matters; the hook question | 0:50 |
| 3 | Frames are usually picked by position … | Position vs. content; the gap; two "how" questions | 0:55 |
| 4 | Four sampling strategies × four classifiers on EngageNet | Design, data, task, split (32 of 91), tests | 0:55 |
| 5 | Each selected frame becomes 1,518 MediaPipe features | Two-pass pipeline; three feature families | 0:35 |
| 6 | k-Changepoint, step 1 | The velocity computation, step by step | 0:55 |
| 7 | k-Changepoint, step 2 | Smoothing, peaks, k highest; SME on the same clip | 0:40 |
| 8 | Every classifier had its highest mean macro F1 with three changepoint frames | Best: SVM + 3-CP, 0.701; these are means | 0:45 |
| 9 | Only the Random Forest's gain over SME was significant | McNemar + Holm; the LSTM seed artefact; no capacity claim | 0:55 |
| 10 | No classifier improved beyond three changepoint frames | k = 5, 7 never above k = 3; not tested | 0:35 |
| 11 | What the results suggest | Three takeaways; classroom use | 0:40 |
| 12 | Limits, and what my thesis study adds | Each limit and its fix | 0:40 |
| 13 | Thank you | Questions | 0:05 |

**If you run long,** shorten slide 5 to one sentence ("each frame becomes 1,518 MediaPipe numbers") and skip the left column on slide 2. That saves about 40 seconds.

## Where the talk differs from the printed paper

The numbers are the same. Some of the paper's readings go further than the data supports, so the talk uses the narrower wording from `dlsu-manuscript/notes/claim-audit.md`. If someone has the proceedings open and asks, say: "The numbers are the same. Since submitting, I've read them more carefully, and some of the paper's wording was stronger than the data supports."

| The paper says | The talk says | Audit |
|---|---|---|
| "the SVM gains least" | Gains at k = 3: RF +4.79, SVM +1.70, MLP +1.05, LSTM −0.15. The SVM gains second most | E1 |
| 7-Changepoint extraction is "a 7.8% increase" | Not on the slides. If asked: about 35% longer on a 10-video sample (8.4 s vs. 6.0–6.2 s per clip). The 7.8% average included one corrupted video | E2 |
| "about 0.9 s per selected frame" | Not used | E3 |
| "minimum separation of seven frames" | 7 *scanned* frames = 14 video frames, about 0.5 s | E6 |
| "the 32-subject training split" | 32 of the 91 training participants | E7 |
| "Every architecture reached its best macro F1 under 3-Changepoint" | Highest *mean* macro F1; significant only for the Random Forest | B1 |
| "performance declined as further frames were added" | No model improved beyond k = 3; only the SVM declined clearly; not tested | B2, B3 |
| The benefit "depends on model capacity" | Largest gain in the weakest model; four classifiers can't show why | B4 |
| Sampling "warrants deliberate tuning" | Should be reported and compared, not fixed by default | B5 |
| "six-fold" seed variance; "improves reproducibility" | Backup B3 only: a ratio of SDs (5.9), weaker at k = 5 and 7, not true for the MLP at k = 7 | B6 |
| Extra frames capture "blinks or camera jitter" | Not used. Extra peaks are smaller movements by construction | B7 |
| The pattern matches Brkić et al. (2025) | Not used | B8, B9 |
| Brow movement is "the strongest single signal" | Backup B5 only: Random Forest Gini importance; not evidence about behavior | B10 |
| "the classifiers converge on similar underlying signal" | Not used | B11 |
| Engagement signals feed "agentic AI systems" | Not on the slides. See Q12 | B13 |
| Engagement is "a well-established predictor" | "associated with achievement" | C1 |
| Korbar et al. select frames | Korbar et al. sample salient *clips* | C5 |

## Likely questions, with short answers

Say these your way. Each one points to the backup slide, if there is one.

**Q1. Why binary? Why threshold 3?**
We split Highly-Engaged from the other three levels. In the label files, threshold 3 is the closest to balanced: about 52% of training clips fall below it, against 18% and 32% for thresholds 1 and 2. In our training data that was 1,375 against 1,344. Highly-Engaged is also the level that's easiest to act on. The four-level problem is still open.
*(Shares from the manuscript's Table 5.3, official training labels.)*

**Q2. Why only compare against SME? What about uniform segments or random frames?**
That's the main limit of this study. SME was the baseline from our earlier work. The thesis adds evenly spaced and random frames at three, five and seven, so content and position are compared at the same frame budget. *(Slide 12.)*

**Q3. You used default hyperparameters. Couldn't tuning change everything?**
It could change each classifier's level. Here, though, the comparison is between sampling strategies *within* each classifier, with everything else held fixed. Still, a tuned model might care less about which frames it gets, so I'd treat this as a result at default settings. *(B4.)*

**Q4. How does 0.70 compare with the EngageNet baselines?**
The two can't be compared directly. The EngageNet baselines are four-class, trained on the full training split, with different features and segment sampling. Ours is binary and trained on 32 participants. Matching their setup is on the list.

**Q5. Why would facial movement mark the useful frames?**
I'm not claiming the peaks are "engagement moments". Velocity is just a cheap signal that says where the face changes most. The question is whether those frames carry more for the classifier than fixed positions. For the Random Forest they did. For the other three, the difference wasn't significant.

**Q6. Why did the Random Forest benefit the most?**
We don't know. It was the weakest model and gained the most. But the SVM, the strongest, gained second most, so it doesn't line up neatly with strength. With four classifiers, I can't separate capacity from everything else that differs between them.

**Q7. Why wasn't the LSTM better than the MLP?**
It only sees three to seven frames, with a mean readout and default settings. That's a very short sequence. I wouldn't read it as a verdict on sequence models.

**Q8. Why McNemar instead of comparing F1 scores?**
Every condition was tested on the same 2,005 clips, so predictions pair up clip by clip. McNemar tests whether one condition gets right the clips the other gets wrong more often than chance. Holm corrects for the several comparisons. One weakness: for the neural models it used one seed's predictions, and that's how the LSTM result at k = 5 came up. *(B2.)*

**Q9. Why only 32 of the 91 training participants?**
Those were the training videos we had at the time. Validation and test are complete. The thesis uses all 91. *(B6.)*

**Q10. How much slower is changepoint extraction?**
On a 10-video sample, seven peaks took about 35% longer per clip than SME or three peaks: 8.4 seconds against 6.0 to 6.2. The paper says 7.8%. That average included one video with corrupted metadata, so the 35% is the right figure.

**Q11. What about privacy? Are you showing students' faces?**
No. The slides use made-up signals and diagrams only. EngageNet was used under its end-user license agreement. The features are landmark coordinates and scores, not images.

**Q12. Your paper mentions agentic AI. How would this be used?**
That's a possible use, and we didn't test it. At about 0.70 macro F1, I'd keep a teacher in the loop and treat the estimate as a hint, not a trigger.

**Q13. Did oversampling matter?**
The results are without oversampling. The training data was already close to balanced, and SMOTE made no material difference in our checks.

**Q14. Are blendshapes action units?**
Not exactly. They're MediaPipe's continuous scores for facial movements, like "brow outer up". They're close in spirit to action units, but not coded the way FACS codes them.

## Rehearsal

- [ ] Reword the slides and notes into your own voice, then check that no number changed.
- [ ] Do two timed run-throughs out loud. Aim for 9:00 to 9:30. Slides 6 and 9 are where people run long.
- [ ] Practice slide 6 at the whiteboard without the slide: center, distance, combine, repeat.
- [ ] Practice jumping to a backup and back. In Slide Show, type the number and press Enter: B1 = 15, B2 = 16, B3 = 17, B4 = 18, B5 = 19, B6 = 20. These assume the backup divider stays deleted.
- [ ] Practice Q1, Q2, Q6 and Q10 out loud.

## On the day (from the guidelines)

- [ ] Bring your own laptop, plus an HDMI adapter if it needs one. A venue laptop is available if needed.
- [ ] Put the PDF on a USB stick. The PDF embeds its fonts, so it looks right on any machine.
- [ ] Check in with your Session Chair before the session.
- [ ] Set up and test in the room before your session: presenter view, notes visible, slide numbers.
- [ ] Use the .pptx on your own laptop: the title fonts and Aptos match there. Use the PDF if you're on the venue laptop.
