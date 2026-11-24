# Doc Jay's comments on the defense slides (20 Nov 2026)

These come from the Zoom recording of the 20 Nov meeting, a run-through of your Canva deck.

**How this list was made**
- **Transcription:** the audio was transcribed locally with Whisper (large-v3). Comments are paraphrased in English from the Taglish. Timestamps refer to the recording.
- **What the recording covers:** your slides run from 00:00 to 32:16. The second presentation runs from 32:16 to the end. A few comments from that part were addressed to you too ("ganun din si Lester"), or apply to both of you. Those are marked *(2nd talk)*.
- **The transcript itself** is not in the repo.

---

## 1. The main comment

**Explain the changepoint algorithm technically** (29:04–30:56, repeated as the summary at 31:56).

What Doc Jay asked for:
- **Show how it is computed.** The graph alone is "too general". Show the math, "as simple as you can": what is compared between frames, and how the method decides it has found a change. "Be creative on how you will explain."
- **Why it matters:** the method is new to most people, and it is the highlight of the study, so the panel may ask about it. "Better na panigurado ka" (better to be sure), so that you don't go blank at the defense.
- **Apply this to both content rules,** since you present them as a pair. Two follow-ups during the meeting point the same way:
  - 19:39: "be ready: how do we say it found a change?" You answered: the velocity of the centered facial landmarks.
  - 21:54: "what is the difference between k-BOCPD and k-Changepoint? You have to be ready." You answered with the glance-away example.

## 2. Structure of the talk

| When | Comment | What to change |
| :-- | :-- | :-- |
| 00:21–02:36 | You don't have to follow the order of the manuscript. Tell it as a story, like the background in Chapter 1: general domain → specific domain → related works → gaps → problem statement → objectives. Scope and limitations come with the objectives. The end of the related works should be the gap. | Reorder the deck. This replaces the chapter-by-chapter order of 19 Nov. |
| 03:45–05:04 | No need to present the theoretical framework. Mention each concept, such as changepoint detection, when it comes up in the methodology. The details are in the document. | Drop the separate theory section. Introduce concepts where they are used. |
| 05:09 | "Why does it matter?" can be your first slide. | Put it right after the title, and the OCE-revisions slide if you keep it. |
| 13:23–13:41 | Working definitions: you said you would define terms as they come up, and Doc Jay found them self-explanatory. | Fold the definitions into the slides where each term first appears. |
| 13:49–14:09 | Don't forget the definition of engagement. Emphasize how the three kinds differ (behavioral, emotional, cognitive) and where your study comes in. | Keep one engagement slide that says which kind observer ratings capture. |

## 3. Slide by slide

| When | Slide | Comment | What to change |
| :-- | :-- | :-- | :-- |
| 02:52–03:43, 06:12–07:01 | All, especially the EngageNet slide | Cite every statement or idea you can, so the panel doesn't think it came from you. Example: EngageNet → Singh et al. (2023). Also cite who used an approach before when you adopt it in the methodology. | Add short citations on the slides. |
| 08:30–09:15, 35:02–35:21 *(2nd talk)* | Research question | A research question must not be answerable by yes or no. Use "how", "in what ways", and so on. Split it if needed. Send Doc Jay the revised question offline. | Revise and send. A draft is in §6. The manuscript has the same wording (Ch. 1, end of the research problem; §4.1 opening). |
| 10:09–10:51 | Objectives | The objectives must match the manuscript word for word ("ito yung contract nyo", this is your contract). The only allowed change is dropping the leading "To". | Your slide already does this, so leave it as it is. |
| 11:13–11:49, 37:06–37:20 *(2nd talk)* | Scope and limitations | Give the scope and limitations per objective, for example one slide per objective with what you will and won't do. Example: objective 1 extracts face and upper-body pose features, from MediaPipe only. Keep the general scope slide, but you can hide it. | Map the scope to the objectives. Hide the general slide. |
| 11:54–12:30 | Significance | Fine to mention, including the VLM point. | No change. |
| 14:12–15:12, 17:24–18:00 | EngageNet | Give it a dedicated slide that shows the panel "the nature of the data": the labels, the number of people, how many male and female, the task, and the setup (controlled or in the wild). | New slide. See §5 for what the manuscript already has. |
| 15:27–16:27 | Comparison of the rules | Add a line or divider that separates the position-based rules from the content-based ones. The position-based rules are clear, but the two content-based rules were not well explained. | Add the divider. The fix for the content rules is §1. |
| 24:42–25:06 | Frame combinations | Mean + change and mean + self-similarity were hard for Doc Jay to understand: "Would you be able to come up with a slide … visualization for explaining" these two specifically. | Add a visual for these two. See also §4, first item. |
| 25:49–26:56 | Interpretation rules (the outcome table) | It has too much in it. Hide it as a backup. If the panel asks, say "I have a slide comparing … I can show it." | Move it to the backup slides. |
| 27:35–28:34 | Preliminary work (the three papers) | Just pass through it. It shows the panel you published three papers, so no specifics are needed. Showing the DAiSEE work is fine: you were exploring which dataset to use. With a result, you can say which paper it is from. | Keep it short. |
| 31:03–31:47 | Remaining work (calendar) | The full calendar isn't needed, because it is in the document. What matters is the work still to do. You said you would mention just that part. | Show or speak to the Planned rows only. *(My reading: a still from 31:12 shows the calendar; the screen share lagged behind your words.)* |
| 50:31–51:07 *(2nd talk)* | Related-works table | Put citations on the summary table so the panel sees who did what. A longer table can be a screenshot on a hidden backup slide, "just in case they want to ask". | Add citations. A screenshot of Table 2.4 can go in the backup slides. |
| 51:19–51:43 *(2nd talk)* | Backup | Keep your OCE slides on the algorithms ready, since they had more detail and the panel may go back to them. | Add them to the backup slides. |
| 51:57 *(2nd talk)* | — | "We don't know what can be asked, so just be ready on the details." | — |

## 4. Two things you said that need fixing

1. **Mean + self-similarity (24:17).** You said it takes the top three principal components, because using every value would give too many comparisons. That is not what the manuscript says (§4.5).
   - **What it does:** each cosine similarity uses all 1,518 standardized features of the two frames. The 3, 10 or 21 values are the number of frame pairs at k = 3, 5, 7.
   - **Where the top three principal components belong:** k-BOCPD's signal (§4.4).
   - **Why it matters:** Doc Jay already found this slide hard to follow, so expect a question here.
2. **The pipeline (18:11).** You said "removes the clips that aren't valid". What is removed is the **frames** with no detected face. A clip leaves only the common clip set, and only under the stated conditions, for example fewer than 14 valid frames under k-BOCPD.

## 5. For the EngageNet slide: what the manuscript already gives you

| Item | Value | Where in the manuscript |
| :-- | :-- | :-- |
| People | 127 adults, aged 18 to 37 | Ch. 1, scope |
| Task | Watching instructional videos, recorded by webcam | Ch. 1, scope |
| Setting | In the wild: computer labs, dormitory rooms, open spaces | Ch. 1; Table 2.1 |
| Clips | About 11,300, each 10 s long | Table 2.1 |
| Labels | Four engagement levels from three annotators, weighted κ 0.73–0.79 | Table 2.1 |
| Split | 91 / 11 / 26 participants (train / val / test), subject-independent | Ch. 1, §4.2 |

**Male/female counts (resolved 20 Nov):**
- Singh et al. (2023), §3.2.1: 83 male and 44 female.
- Also from that paper (§3.1–3.2.1): each participant watched three lecture videos of about 5 minutes and answered questions after each; recorded "in an unconstrained environment" (labs, dorm rooms, open spaces).
- "83 male and 44 female" is now in §1.3 of the manuscript too, so the slide's number traces to it.

## 6. Research questions: revised 22–23 Nov

**Done (22 Nov):** two "how" questions replace the yes/no ones. They are now in §1.1 and the opening of §4.1, and on slide 9. `main.pdf` was rebuilt.

**23 Nov (your edits):** the first question is split in two, and the temporal question now reads "What are the effects of…". There are three questions in all.

**Before** (both answerable by yes or no):
> Does content-based frame selection improve the classification of observer-rated student engagement over position-based and random selection at equal frame budgets, and does the answer depend on the frame budget and the classifier?

> The study therefore also asks whether representing the temporal aspect of the selected frames improves classification.

**Now:**
> 1. How does content-based frame selection compare with position-based and random selection in classifying observer-rated student engagement at equal frame budgets?
> 2. How does this comparison vary with the frame budget and the classifier?
> 3. What are the effects of representing the order and change of the selected frames on engagement classification, compared with averaging them?

**Why this wording:**
- **Doc Jay's own words:** "how", "in what ways".
- **No winner assumed:** the questions don't assume content-based selection wins. "No difference" or "position does better" is still an answer, and the equivalence tests are designed for exactly that case.
- **The second question was also yes/no.** It was the "also asks whether" sentence in §1.1, and it now has its own question.

**Not changed:** the objectives. Doc Jay called them your contract, and §1.2 still matches them word for word. The problem statement in §1.1 ("it is not known whether…") is a statement, not a question, so it stays.

**To do:** send Doc Jay the new wording, ideally with the revised `main.pdf` (§7).

## 7. To do (admin)

- [ ] **Sir Thomas:** follow up. Doc Jay already messaged him and got no reply yet. If there's still none by **21 Nov**, e-mail him again.
- [ ] **Send Doc Jay "the slides, yung sa ICC" by 21 Nov.** Whisper heard "ICC". Most likely the ICCE slides.
- [ ] **Send Doc Jay the revised research questions** (§6). They are already in the manuscript; ask for comments.
- [ ] **Next meeting:** next week. Doc Jay will send available times, being out of the country and with other defenses that week.
