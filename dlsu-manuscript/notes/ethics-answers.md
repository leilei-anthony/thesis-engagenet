# Answers for the Research Ethics Forms (Appendix A)

Updated 16 Nov 2026 (second version).

**The forms are now your Word files in `ethics-forms/filled/`.** They replace the template PDFs:

| File | What it is | Pages |
| :-- | :-- | --: |
| `sityar-ethics-review-form.docx` | Research/Project Ethics Review Form (ver. Oct2024c). The current version of the clearance form for proposals. | 4 |
| `sityar-general-ethics-checklist.docx` | General Research Ethics Checklist | 3 |
| `sityar-checklist-a.docx` | Checklist A (Human Participants) | 7 |

**How Appendix A uses them**
- Appendix A includes the PDF of each file, exported with Word.
- Your versions from before my edits are in `ethics-forms/filled/before-claude/`.
- **If you edit a form:**
  1. Edit the `.docx` in Word.
  2. Save it as PDF under the same name (File → Save As → PDF).
  3. Rebuild `main.pdf`.

Your decisions (16 Nov):
- no conflict of interest;
- the preliminary processing (June to July 2026) is disclosed;
- the smoke test runs only after approval.

---

## 1. Ethics Review Form: what I filled in

**Header**
- I left your entries alone except for two typos:
  - "Master of **of** Science" became "Master of Science";
  - the end date "Apr 30, **2026**" became "Apr 30, **2027**". It was earlier than the start date.
- **[Check]** The name reads "Sityar, Lester Anthony Jr. Hill". If Hill is your middle name, the usual order is "Sityar, Lester Anthony Hill Jr.".

**PROTOCOL table.** The middle column is the answer, and the right column is the reference document with page numbers.
- **Proposal pages** are the printed page numbers in `main.pdf`.
- **Checklist A pages** are those of `sityar-checklist-a.pdf`, where the pre-existing-data section is on pages 6–7.

| Row | Answer (summary) | Reference |
| :-- | :-- | :-- |
| Target participants | (Your wording, 16 Nov) Existing recordings of the 127 adults (18 to 37) in EngageNet, filmed by webcam while watching instructional videos. | Checklist A, pp. 1 and 6–7; Proposal §4.2.1, p. 34; Singh et al. (2023), §3 |
| Data to be used / collected | (Your wording, 16 Nov) No new data. About 11,300 ten-second EngageNet clips with their observer-assigned engagement levels. | Checklist A, pp. 1 and 6–7; Proposal §4.2, p. 34; §4.3, p. 37 |
| Brief procedure | Offline, and only after approval: (1) scan frames and keep those with a face; (2) choose 3/5/7 frames per rule; (3) remove the background and compute features; (4) train four classifiers and test them on unseen clips; (5) compare the rules with statistical tests. | Proposal §§4.3–4.6, pp. 37–47; Algorithms 5.1–5.2, pp. 57–58; Checklist A, p. 1 |
| Potential risks | No physical or psychological risk (no contact). (1) Identification through faces or landmark coordinates; (2) breach of the dataset licence; (3) misuse of results to judge individual students. | Proposal §4.7, pp. 47–48; Checklist A, pp. 6–7 |
| Terms of use / licensing | EngageNet Dataset User Agreement: academic, non-commercial; signed 19 June 2026, with Dr. Azcarraga as additional researcher; its restrictions listed. RA 10173. Tools, run locally: MediaPipe and OpenCV (Apache 2.0), rembg and ONNX Runtime (MIT), PyTorch and scikit-learn (BSD-3-Clause). | EngageNet Dataset User Agreement (attached); Proposal §4.7, p. 47 |
| Safeguards | (1) Local storage only, out of version control, never shared; (2) originals never altered; (3) no images of participants anywhere; (4) aggregate reporting only; (5) no clip sent to any online or AI service; (6) no processing, including code tests, until approval. | Proposal §4.7, pp. 47–48; §1.3, p. 5; Checklist A, p. 1 |
| Other concerns | (1) The earlier processing is disclosed; (2) consent: the dataset paper says consent was requested for the scope of usage; the information statement "is being requested" from the owners; (3) demographic differences are not evaluated, and the classifiers are not for decisions about individuals. | Proposal §4.7, p. 48; §5.1.2, p. 51; Table 5.4, p. 56; Singh et al. (2023), §3.1 |

**Your edits (16 Nov, after mine):** you shortened the Target participants and Data rows, put Doc Jay's name on the adviser signature line, and the form now fits on 3 pages.

**Panel's decision boxes:** the template drew them as "€", a font artifact. They now show as ☐. Everything below PROTOCOL (the panel's comments, decision, justification and signatures) is for the panel.

**Facts behind the answers**
- **Licences:** checked in the installed packages' metadata.
- **Proposal page numbers:** taken from `main.toc` and the PDF.
- **EngageNet facts:** from the paper (arXiv 2302.00431) and the signed agreement.

---

## 2. Checklist A: what I added

- **Source of data:** ✔ item 2 (pre-existing data). Neither item had been checked.
- **Page 6, dataset:** "EngageNet (Singh et al., 2023, ICMI '23): about 11,300 ten-second webcam clips of 127 participants, labeled with four engagement levels".
- **Page 6, approval authority** (under your ✔ No): "EngageNet dataset licensors (A. Dhall and M. Singh), through the EngageNet Dataset User Agreement signed 19 June 2026 (attached)".

**Your other answers were already complete.** These are publicly available? No; collected for this study? No; sensitive data? No; identifiers? Yes, Indirect; new data? No.

**I did not change these. Please look at them:**
1. **The description (page 1)** now reads "…Results are reported and no image of a participant appears in any document." It looks as if "only in aggregate," was dropped. Suggested: "Results are reported only in aggregate, and no image of a participant appears in any document."
2. **The new-data-only section (page 2)** has "Online and through recommended Experts" in the recruitment row. You collect no new data, so this row should be empty.
3. **Clipped text on page 2** ("ou checked this item…"): this comes from the template itself; your original file shows it too. Leave it, or fix the indentation in Word if you like.

---

## 3. General Ethics Checklist: complete as you filled it

**Update 16 Nov (late):** you replaced it with a new version, `sityar-general-ethics-checklist.pdf`, exported from Google Docs. There is no Word file for it any more, so edit it in Google Docs and export it again under the same name.

**Answers**
- Yes: human participants (1.A–1.C No); documents not in the public domain; secondary data needing permission.
- No: animals, wildlife, infectious agents, toxic substances.
- [✔] No conflict of interest.

**Note:** the two "Yes" answers on non-public documents and secondary data ask for "certification that permission … was granted". The signed EngageNet agreement is that certification, so attach it.

---

## 4. E-mail to the EngageNet authors (you send it)

The Ethics Review Form says the participant information statement "is being requested". Send this **before** you submit, or change the wording.

**To:** Dr. Abhinav Dhall. Use the contact on the EngageNet page linked in the user agreement.

**Subject:** EngageNet: participant information statement for an ethics review

> Dear Dr. Dhall,
>
> I am a BS-MS Computer Science student at De La Salle University, Manila, working under Dr. Judith Azcarraga. We obtained access to EngageNet through your request form and signed the EngageNet Dataset User Agreement on 19 June 2026.
>
> Our university's research ethics committee asks for the information given to participants when the data were collected, that is, the consent form or information sheet. Your paper notes that participants' consent was requested for the scope of usage of the data (Singh et al., 2023, Section 3.1). Would you be able to share a copy of that form or sheet, or a short statement of what participants agreed to? It will be used only for the ethics review.
>
> Thank you very much.
>
> Sincerely,
> Lester Anthony Sityar Jr.
> De La Salle University, Manila

---

## 5. Before you submit

1. Fix or confirm the items flagged in §1 (name order) and §2 (items 1 and 2). Then re-export those PDFs from Word.
2. Send the e-mail in §4.
3. Attach these to the submission. **Update 16 Nov:** you also put the signed user agreement in Appendix A. It is included from `EULA_EngageNet_signed-flat.pdf`, a copy whose typed entries are flattened into the page, because LaTeX drops PDF annotations:
   - the signed user agreement (`docs/EULA_EngageNet_signed.pdf`);
   - the information statement once received, or until then a one-page note quoting Singh et al. (2023), §3.1.
4. Signatures: the adviser and panel sign the Ethics Review Form at or after the defense. Sign wherever the checklists ask for your signature.
5. Run nothing on the clips, including the smoke test, until the review approves the study.
