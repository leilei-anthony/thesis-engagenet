"""Build the ICCE 2026 talk from the official template (first draft only).

Run from the repo root with the base Anaconda Python, which has python-pptx
(the thesis-engagenet env does not):
    python paper/icce-presentation/build_deck.py

Input:  ICCE-2026-Presentation-Slide-Template.pptx (official, unchanged) and figures/*.png
        (from figures/src/charts.py).
Output: sityar-icce2026.pptx

Every result number comes from paper/paper.tex (Tables 1-2, Sections 2-3). The readings follow
dlsu-manuscript/notes/claim-audit.md, which is narrower than the printed paper (see talk-notes.md).
Once the deck is edited by hand in PowerPoint, edit the .pptx directly; re-running this overwrites it.
"""
import copy
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "ICCE-2026-Presentation-Slide-Template.pptx"
OUT = HERE / "sityar-icce2026.pptx"
FIG = HERE / "figures"

# ---------------------------------------------------------------- colors
NAVY = RGBColor(0x00, 0x20, 0x68)      # ICCE logo navy
RED = RGBColor(0xC7, 0x12, 0x2F)       # ICCE red (layout text); used sparingly
INK = RGBColor(0x1A, 0x1A, 0x1A)
INK2 = RGBColor(0x4A, 0x49, 0x46)
MUTED = RGBColor(0x6B, 0x6A, 0x66)     # citations; 5:1 on white
CARD = RGBColor(0xF4, 0xF4, 0xF4)      # the template's own light gray
LINE = RGBColor(0xC3, 0xC2, 0xB7)
FRAME = RGBColor(0xD3, 0xD3, 0xD3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SME_C = RGBColor(0xEB, 0x68, 0x34)
CP_C = {3: RGBColor(0x10, 0x42, 0x81), 5: RGBColor(0x2A, 0x78, 0xD6), 7: RGBColor(0x6D, 0xA7, 0xEC)}

# ---------------------------------------------------------------- geometry (inches)
LM, CW = 0.92, 11.5                    # the template's title left edge and width
RM = LM + CW
TOP = 1.62                             # content starts below the title block
SPLIT_X = 9.45                         # right-hand panel next to an 8.3 in figure

prs = Presentation(str(TEMPLATE))
LAYOUT = {l.name: l for l in prs.slide_layouts}

# drop the template's six sample slides
for sld_id in list(prs.slides._sldIdLst):
    prs.part.drop_rel(sld_id.rId)
    prs.slides._sldIdLst.remove(sld_id)


# ---------------------------------------------------------------- helpers
def I(v):
    return Inches(v)


def add_slide_number(slide):
    """Copy the layout's slide-number placeholder onto the slide, so the number shows."""
    for ph in slide.slide_layout.placeholders:
        if ph.placeholder_format.type == PP_PLACEHOLDER.SLIDE_NUMBER:
            el = copy.deepcopy(ph._element)
            el.find(".//" + qn("p:cNvPr")).set("id", str(slide.shapes._next_shape_id))
            slide.shapes._spTree.append(el)
            return


def set_notes(slide, script, reminders=()):
    text = script.strip()
    if reminders:
        text += "\n\nReminders:\n" + "\n".join(f"- {r}" for r in reminders)
    slide.notes_slide.notes_text_frame.text = text


def style_run(run, size=None, bold=None, italic=None, color=None):
    f = run.font
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color


def bulletize(p, indent=0.22, char="•"):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(indent)))
    pPr.set("indent", str(-Inches(indent)))
    etree.SubElement(pPr, qn("a:buFont"), typeface="Arial")
    etree.SubElement(pPr, qn("a:buChar"), char=char)


def fill_tf(tf, paras, size=16, color=INK, align=None, space_after=6, line_spacing=None):
    """paras: list of paragraphs; a paragraph is a str, or a dict with 'runs' (list of str or
    (text, opts)), and optional 'bullet', 'size', 'space_after', 'align', 'color'."""
    first = True
    for para in paras:
        if isinstance(para, str):
            para = {"runs": [para]}
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(para.get("space_after", space_after))
        if line_spacing:
            p.line_spacing = line_spacing
        if para.get("align", align) is not None:
            p.alignment = para.get("align", align)
        for item in para["runs"]:
            text, opts = (item, {}) if isinstance(item, str) else item
            r = p.add_run()
            r.text = text
            style_run(r, size=opts.get("size", para.get("size", size)), bold=opts.get("bold", False),
                      italic=opts.get("italic"), color=opts.get("color", para.get("color", color)))
        if para.get("bullet"):
            bulletize(p)
    return tf


def textbox(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, margin=0.0, name=None, **kw):
    tb = slide.shapes.add_textbox(I(x), I(y), I(w), I(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = I(margin)
    tf.margin_top = tf.margin_bottom = I(0.02)
    fill_tf(tf, paras, **kw)
    if name:
        tb.name = name
    return tb


def box(slide, x, y, w, h, fill=CARD, line=None, radius=0.06, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=None):
    s = slide.shapes.add_shape(shape, I(x), I(y), I(w), I(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    s.shadow.inherit = False
    s.text_frame.text = ""
    if name:
        s.name = name
    return s


def box_text(shape, paras, anchor=MSO_ANCHOR.MIDDLE, margin=0.14, **kw):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = I(margin)
    tf.margin_top = tf.margin_bottom = I(0.08)
    fill_tf(tf, paras, **kw)
    return shape


def arrow(slide, x1, y1, x2, y2, color=INK2, width=1.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, I(x1), I(y1), I(x2), I(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    etree.SubElement(ln, qn("a:tailEnd"), type="triangle", w="med", len="med")
    return c


def dot(slide, x, y, d, color, shape=MSO_SHAPE.OVAL):
    s = slide.shapes.add_shape(shape, I(x), I(y), I(d), I(d))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def picture(slide, name, x, y, w):
    return slide.shapes.add_picture(str(FIG / name), I(x), I(y), width=I(w))


def strip(slide, x, y, w, h, n, picks, pick_color, base=FRAME, bg=None, gap_ratio=0.35):
    """A row of n frames; the frames in `picks` are colored. Optional background band."""
    if bg is not None:
        box(slide, x - 0.12, y - 0.1, w + 0.24, h + 0.2, fill=bg, radius=0.12)
    fw = w / (n + (n - 1) * gap_ratio)
    for i in range(n):
        fx = x + i * fw * (1 + gap_ratio)
        r = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, I(fx), I(y), I(fw), I(h))
        r.fill.solid()
        r.fill.fore_color.rgb = pick_color if i in picks else base
        r.line.fill.background()
        r.shadow.inherit = False
    return [x + i * fw * (1 + gap_ratio) + fw / 2 for i in range(n)]


def content_slide(title):
    s = prs.slides.add_slide(LAYOUT["Title and Content"])
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 1:
            ph._element.getparent().remove(ph._element)
    t = s.shapes.title
    t.left, t.top, t.width, t.height = I(LM), I(0.4), I(CW), I(1.08)
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.clear()
    r = tf.paragraphs[0].add_run()
    r.text = title
    style_run(r, size=30, bold=True, color=NAVY)
    tf.paragraphs[0].line_spacing = 0.95
    return s


def table(slide, x, y, w, col_w, rows, header_fill=NAVY, size=14, row_h=0.4, bold_rows=(), muted_rows=(),
          align_right_cols=()):
    nr, nc = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nr, nc, I(x), I(y), I(w), I(row_h * nr))
    tbl = gf.table
    tbl.first_row = True
    tbl.horz_banding = False
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = I(cw)
    for i in range(nr):
        tbl.rows[i].height = I(row_h)
        for j in range(nc):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = I(0.08)
            cell.margin_top = cell.margin_bottom = I(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.fore_color.rgb = CARD if i % 2 == 0 else WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if j in align_right_cols else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(rows[i][j])
            style_run(r, size=size, bold=(i == 0 or i in bold_rows),
                      italic=(i in muted_rows) or None,
                      color=WHITE if i == 0 else (MUTED if i in muted_rows else INK))
    return tbl


def finish(slide, script, reminders=()):
    add_slide_number(slide)
    set_notes(slide, script, reminders)


# ================================================================= 1. Title
s = prs.slides.add_slide(LAYOUT["Title Slide-Editable Title_Sub-1"])
title_ph = s.placeholders[0]
title_ph.text_frame.text = "Temporal Sampling Strategies for Student Engagement Detection"
sub = s.placeholders[1]
sub.text_frame.text = "Lester Anthony H. Sityar & Judith Azcarraga"
for p in sub.text_frame.paragraphs:
    for r in p.runs:
        style_run(r, size=20)
textbox(s, 6.27, 5.62, 6.03, 0.75, [
    {"runs": [("De La Salle University, Philippines", {"size": 16, "color": INK2})], "align": PP_ALIGN.CENTER,
     "space_after": 2},
    {"runs": [("Short paper", {"size": 14, "color": MUTED})], "align": PP_ALIGN.CENTER},
])
finish(s, """
Hello, everyone. I'm Lester Sityar from De La Salle University in the Philippines. This is joint work with my adviser, Dr. Judith Azcarraga. It's about a small step in engagement detection that usually gets skipped over: how we pick the frames.
""", [
    "Keep this under 20 seconds. The session chair has already said the title.",
    "Short paper slot: 10 minutes, then 5 minutes of Q&A.",
])

# ================================================================= 2. Why
s = content_slide("Detecting engagement from webcam video starts with choosing a few frames")
textbox(s, LM, TOP + 0.1, 5.75, 3.4, [
    {"runs": [("Engagement is associated with achievement", {"bold": True})], "size": 19, "space_after": 2},
    {"runs": [("Fredricks et al., 2004", {"size": 13, "color": MUTED})], "space_after": 16},
    {"runs": [("Online and hybrid classes take away the teacher's view of the room", {"bold": True})], "size": 19,
     "space_after": 16},
    {"runs": [("Webcam datasets now exist", {"bold": True})], "size": 19, "space_after": 2},
    {"runs": [("DAiSEE (Gupta et al., 2016) · EngageNet (Singh et al., 2023)", {"size": 13, "color": MUTED})]},
])
textbox(s, LM, 5.25, 5.75, 1.2, [
    {"runs": [("If the model sees only a few frames, which ones should it see?", {"bold": True})], "size": 22,
     "color": RED},
])
# right: film strip -> features -> classifier
rx, rw = 7.15, 5.27
textbox(s, rx, TOP + 0.05, rw, 0.4, [{"runs": [("One 10-second clip: about 300 frames", {"size": 15, "color": INK2})]}])
centers = strip(s, rx, TOP + 0.62, rw, 0.55, 20, picks={3, 10, 16}, pick_color=WHITE,
                base=RGBColor(0x8A, 0x8A, 0x8A), bg=RGBColor(0x2B, 0x2B, 0x2B))
feat = box(s, rx + 0.6, 3.35, rw - 1.2, 0.72)
box_text(feat, [{"runs": [("Features from each selected frame", {"bold": True})], "align": PP_ALIGN.CENTER}], size=16)
for c in (centers[3], centers[10], centers[16]):
    arrow(s, c, TOP + 1.3, rx + rw / 2 + (c - (rx + rw / 2)) * 0.45, 3.33, color=INK2, width=1.5)
clf = box(s, rx + 0.6, 4.5, rw - 1.2, 0.72)
box_text(clf, [{"runs": [("Classifier", {"bold": True})], "align": PP_ALIGN.CENTER}], size=16)
arrow(s, rx + rw / 2, 4.08, rx + rw / 2, 4.48)
textbox(s, rx, 5.42, rw, 0.5, [{"runs": [("Highly engaged, or not?", {"size": 16, "color": INK2})],
                                "align": PP_ALIGN.CENTER}])
arrow(s, rx + rw / 2, 5.23, rx + rw / 2, 5.44)
finish(s, """
Engagement matters for learning. Students who are more engaged tend to do better in school. In online and hybrid classes, though, the teacher can't look around the room anymore. That's why people have been building ways to detect engagement from webcam video, and there are now datasets for it, like DAiSEE and EngageNet.

Here's the step I mean. A ten-second clip has about three hundred frames. Most pipelines don't use all of them. They pick a few, extract features from those, and then classify. So if the model only sees a few frames, which ones should it see?
""", [
    "Fredricks et al. (2004) report associations. Say 'tend to do better', not 'predicts' or 'causes' (audit C1).",
    "300 frames = 10 s at 30 fps.",
    "The diagram is schematic. Never show EngageNet frames or faces (user agreement).",
])

# ================================================================= 3. Position vs content
s = content_slide("Frames are usually picked by position, not by what happens in them")
cw2, gap = 5.55, 0.4
for k, (x, head, color, picks, items) in enumerate([
    (LM, "By position", SME_C, {0, 7, 15}, [
        [("Start-Middle-End (SME): ", {"bold": True}), "first, middle and last frame"],
        [("Equal segments: ", {"bold": True}), "DAiSEE and EngageNet baselines, after temporal segment networks"],
        [("Gupta et al., 2016; Singh et al., 2023; Wang et al., 2016", {"size": 12, "color": MUTED})],
    ]),
    (LM + cw2 + gap, "By content", CP_C[3], {2, 9, 12}, [
        [("Salient-clip sampling ", {"bold": True}), "helps in action recognition"],
        [("Changepoint detection ", {"bold": True}), "finds where a signal's statistics shift"],
        [("Korbar et al., 2019; Truong et al., 2020", {"size": 12, "color": MUTED})],
        [("Rarely compared for engagement", {"italic": True, "color": INK2})],
    ]),
]):
    box(s, x, TOP + 0.05, cw2, 3.35)
    dot(s, x + 0.25, TOP + 0.3, 0.24, color)
    textbox(s, x + 0.62, TOP + 0.2, cw2 - 0.8, 0.45, [{"runs": [(head, {"bold": True})], "size": 21}])
    strip(s, x + 0.3, TOP + 0.9, cw2 - 0.6, 0.42, 16, picks=picks, pick_color=color, base=FRAME)
    paras = [{"runs": items[0], "size": 16, "bullet": True, "space_after": 6},
             {"runs": items[1], "size": 16, "bullet": True, "space_after": 4},
             {"runs": items[2], "space_after": 8}]
    if len(items) > 3:
        paras.append({"runs": items[3], "size": 15})
    textbox(s, x + 0.3, TOP + 1.55, cw2 - 0.55, 1.75, paras)
q = box(s, LM, 5.2, CW, 1.3, fill=NAVY)
box_text(q, [
    {"runs": [("Our questions", {"bold": True, "size": 15, "color": RGBColor(0xC9, 0xD3, 0xEA)})], "space_after": 4},
    {"runs": [("1  How does content-based selection compare with SME across four classifiers?",
               {"color": WHITE})], "space_after": 2},
    {"runs": [("2  How does the number of selected frames change the result?", {"color": WHITE})]},
], anchor=MSO_ANCHOR.MIDDLE, margin=0.3, size=18)
finish(s, """
Most of the time, frames are picked by position. The simplest is Start-Middle-End, or SME: the first, middle, and last frame. Another is to cut the clip into equal segments. That's what the DAiSEE and EngageNet baselines do, and it comes from temporal segment networks.

The alternative is to pick frames by what happens in them. In action recognition, picking salient clips has helped. Changepoint detection is a family of methods for finding where a signal changes. For engagement, though, this hasn't really been compared with positional sampling.

So we asked two things. How does content-based selection compare with SME across different classifiers? And how does the number of frames change the result?
""", [
    "Korbar et al. (2019) sample salient clips, not single frames (audit C5). Don't call it frame selection.",
    "Say 'rarely compared', not 'never tested'.",
    "Wang et al. (2016) is TSN, where the segment idea comes from.",
])

# ================================================================= 4. Design and data
s = content_slide("Four sampling strategies × four classifiers on EngageNet")
gx, gy = LM, TOP + 0.1
label_w, cell_w, head_h, row_h = 2.15, 0.98, 0.5, 0.6
for j, name in enumerate(["LSTM", "MLP", "SVM", "Random\nForest"]):
    textbox(s, gx + label_w + j * cell_w, gy, cell_w, head_h,
            [{"runs": [(name, {"bold": True})], "size": 13, "align": PP_ALIGN.CENTER}],
            anchor=MSO_ANCHOR.BOTTOM)
for i, (name, color) in enumerate(zip(["SME", "3-Changepoint", "5-Changepoint", "7-Changepoint"],
                                      [SME_C, CP_C[3], CP_C[5], CP_C[7]])):
    ry = gy + head_h + 0.1 + i * row_h
    dot(s, gx, ry + 0.18, 0.22, color)
    textbox(s, gx + 0.32, ry + 0.08, label_w - 0.35, 0.42, [{"runs": [(name, {"bold": True})], "size": 15}],
            anchor=MSO_ANCHOR.MIDDLE)
    for j in range(4):
        cx0 = gx + label_w + j * cell_w + 0.08
        box(s, cx0, ry + 0.06, cell_w - 0.16, row_h - 0.12, fill=CARD, radius=0.15)
        dot(s, cx0 + (cell_w - 0.16) / 2 - 0.09, ry + 0.06 + (row_h - 0.12) / 2 - 0.09, 0.18, color)
grid_bottom = gy + head_h + 0.1 + 4 * row_h
textbox(s, gx, grid_bottom + 0.15, 6.2, 1.6, [
    {"runs": [("16 configurations, each trained and tested on the same clips", {"bold": True})], "size": 15,
     "space_after": 8},
    {"runs": ["Changepoint: the k highest peaks in facial-landmark velocity"], "size": 15, "space_after": 8},
    {"runs": ["All classifiers at library defaults, no tuning"], "size": 15},
])
fx, fw = 7.35, RM - 7.35
facts = [
    ("Data", [("EngageNet: ", {"bold": True}), "10-s webcam clips of 127 participants, four engagement levels, "
              "three expert annotators", ("  Singh et al., 2023", {"size": 12, "color": MUTED})]),
    ("Task", ["Highly-Engaged vs. the other three levels. Training: 1,344 vs. 1,375 clips"]),
    ("Split", ["Official, subject-independent. Training 2,719 clips from ", ("32 of the 91", {"bold": True}),
               " training participants; validation 867; test 2,005"]),
    ("Tests", ["Exact McNemar on paired test predictions, Holm-corrected. LSTM and MLP: five seeds"]),
]
yy = TOP + 0.05
for label, runs in facts:
    textbox(s, fx, yy, 1.0, 0.4, [{"runs": [(label, {"bold": True})], "size": 15, "color": NAVY}])
    textbox(s, fx + 1.0, yy, fw - 1.0, 1.1, [{"runs": runs, "size": 15}])
    yy += 1.18
finish(s, """
We crossed four sampling strategies with four classifiers. The strategies are SME, and changepoint selection keeping three, five, or seven frames. The classifiers are an LSTM, an MLP, an SVM, and a Random Forest, all at default settings. That's sixteen configurations.

The data is EngageNet. We made the labels binary: Highly-Engaged against the other three levels, which is close to balanced. The split is subject-independent, so nobody appears in both training and test. I should be upfront that training used thirty-two of the ninety-one training participants. That's what we had at the time.

Every configuration uses the same clips, so we can compare predictions clip by clip.
""", [
    "Clips: training 2,719, validation 867, test 2,005, after keeping only clips usable under all four strategies (backup B6).",
    "Training classes: 1,344 Highly-Engaged vs. 1,375 others.",
    "SVM and Random Forest are deterministic; LSTM and MLP are averaged over five seeds.",
    "Holm-Bonferroni within each family of tests.",
    "If asked why 32 of 91: those were the training videos available at the time. The thesis uses all 91.",
])

# ================================================================= 5. Pipeline
s = content_slide("Each selected frame becomes 1,518 MediaPipe features")
steps = [
    ("Clip", "10 s, about 300 frames", False),
    ("Pass 1", "Scan every 2nd frame; keep frames with a face and consistent shoulders", False),
    ("Select k frames", "SME or k‑Changepoint", True),
    ("Pass 2", "MediaPipe again, on the selected frames only", False),
    ("Classifier", "LSTM: frames in order\nMLP, SVM, RF: mean of the frames", False),
]
bw, bg_, by, bh = 2.05, (CW - 5 * 2.05) / 4, TOP + 0.15, 1.75
for i, (head, detail, hl) in enumerate(steps):
    bx = LM + i * (bw + bg_)
    b = box(s, bx, by, bw, bh, fill=NAVY if hl else CARD)
    box_text(b, [
        {"runs": [(head, {"bold": True})], "size": 17, "color": WHITE if hl else NAVY, "space_after": 6},
        {"runs": [detail], "size": 13, "color": WHITE if hl else INK},
    ], anchor=MSO_ANCHOR.TOP, margin=0.13)
    if i < 4:
        arrow(s, bx + bw + 0.03, by + bh / 2, bx + bw + bg_ - 0.03, by + bh / 2)
textbox(s, LM, 4.0, CW, 0.45, [{"runs": [("1,518 features per frame", {"bold": True}),
                                          ("   MediaPipe (Lugaresi et al., 2019)", {"size": 13, "color": MUTED})],
                                 "size": 19, "color": NAVY}])
cards = [
    ("52", "blendshape scores, similar to action units: brow raise, cheek squint, mouth corners"),
    ("1,434", "face-landmark values: 478 points × x, y, z"),
    ("32", "upper-body pose values: 8 keypoints × x, y, z, visibility"),
]
cwid = (CW - 2 * 0.3) / 3
for i, (num, desc) in enumerate(cards):
    cx = LM + i * (cwid + 0.3)
    c = box(s, cx, 4.55, cwid, 1.85)
    box_text(c, [
        {"runs": [(num, {"bold": True})], "size": 30, "color": NAVY, "space_after": 2},
        {"runs": [desc], "size": 14},
    ], anchor=MSO_ANCHOR.TOP, margin=0.2)
finish(s, """
Here's the pipeline. The first pass scans every second frame and keeps the valid ones, where a face is found and the shoulders look consistent. The rule picks k of those. The second pass runs MediaPipe again on just those frames. Each frame gives fifteen hundred eighteen numbers: blendshape scores, which are similar to action units, face landmarks, and upper-body pose. The LSTM sees the frames in order. The other three get the average.
""", [
    "52 + 1,434 + 32 = 1,518.",
    "Blendshapes are MediaPipe's continuous scores, not coder-assigned Action Units. Say 'similar to', not 'are'.",
    "Valid frame: a face is detected and shoulder visibility is consistent.",
    "LSTM: 64 units, then a 32-unit dense layer, mean over time steps (backup B4).",
])

# ================================================================= 6. Velocity
s = content_slide("k-Changepoint, step 1: one velocity value for each pair of frames")
picture(s, "velocity-steps.png", LM, TOP + 0.05, CW)
finish(s, """
So how does the changepoint rule find a change? It uses the face landmarks. Take two frames in a row. First, subtract each frame's mean position. If the whole head shifts, that cancels out. Then measure how far each landmark moved. Here, two landmarks moved and the rest barely did. Combine those distances into one number, the square root of the sum of squares. That's the velocity for this pair of frames. Without centering, this example would give 2.44 instead of 0.51, and the head shift would hide the two landmarks that really moved. Do this for every pair of frames and you get a velocity curve.
""", [
    "The velocity uses the x and y of all 478 face landmarks.",
    "Centering removes a shift of the whole face. It does not remove rotation or scale.",
    "Six landmarks with made-up positions; not EngageNet data.",
    "Changepoint detection framework: Truong et al. (2020). This is a simple peak-based version, not a full changepoint model.",
])

# ================================================================= 7. Peaks vs SME
s = content_slide("k-Changepoint, step 2: keep the k highest peaks, at least 7 frames apart")
picture(s, "sme-vs-changepoint.png", LM, TOP, 8.3)
px, pw = SPLIT_X, RM - SPLIT_X
textbox(s, px, TOP + 0.15, pw, 3.3, [
    {"runs": [("1  ", {"bold": True, "color": NAVY}), "Smooth over 5 frames"], "size": 15, "space_after": 10},
    {"runs": [("2  ", {"bold": True, "color": NAVY}), "Find peaks at least 7 scanned frames apart (about 0.5 s)"],
     "size": 15, "space_after": 10},
    {"runs": [("3  ", {"bold": True, "color": NAVY}), "Keep the k highest, back in time order"], "size": 15,
     "space_after": 10},
    {"runs": [("4  ", {"bold": True, "color": NAVY}), "k or fewer valid frames: keep them all"], "size": 15},
])
sme_card = box(s, px, 4.85, pw, 1.35)
dot(s, px + 0.18, 5.05, 0.2, SME_C, shape=MSO_SHAPE.DIAMOND)
textbox(s, px + 0.5, 4.95, pw - 0.6, 1.2, [
    {"runs": [("SME ignores the signal: ", {"bold": True}), "first, middle and last valid frame"], "size": 14},
])
finish(s, """
Next, we smooth the curve over five frames, so a one-frame jitter can't win. Then we find peaks that are at least seven scanned frames apart, about half a second. We keep the k highest and put them back in time order. If a clip has k valid frames or fewer, we keep them all.

Compare that with SME here. SME takes frames one, twenty-one, and forty, whatever happens in between. Three-Changepoint takes the three biggest movements.
""", [
    "7 scanned frames = 14 video frames, about 0.47 s at 30 fps (audit E6). The paper just says 'seven frames'.",
    "No height or prominence threshold: the k largest peaks are kept whatever their size.",
    "Made-up signal of 40 valid frames; not EngageNet data.",
    "Don't call the peaks 'engagement moments'. They are the largest facial movements.",
])

# ================================================================= 8. Macro F1
s = content_slide("Every classifier had its highest mean macro F1 with three changepoint frames")
picture(s, "macro-f1.png", LM, TOP, 8.3)
textbox(s, px, TOP + 0.2, pw, 1.9, [
    {"runs": [("0.701", {"bold": True})], "size": 48, "color": NAVY, "space_after": 0},
    {"runs": ["macro F1, SVM with 3‑Changepoint: best of the 16"], "size": 15, "color": INK2},
])
textbox(s, px, 3.75, pw, 2.4, [
    {"runs": [("Classifiers differed more than strategies", {"bold": True})], "size": 15, "space_after": 6},
    {"runs": ["SVM vs. Random Forest: 8.9 to 12.0 accuracy points"], "size": 14, "bullet": True, "space_after": 4},
    {"runs": ["Strategy, within a classifier: at most 4.8 points"], "size": 14, "bullet": True, "space_after": 12},
    {"runs": [("These are means. The tests come next.", {"italic": True})], "size": 14, "color": MUTED},
])
finish(s, """
Now the results. This is macro F1 on the test set. Orange is SME, and the blues are the changepoint versions. For every classifier, the darkest dot, three changepoints, is the highest. The best overall was the SVM with three changepoints, at 0.701.

Two things to keep in mind. These are means, not tests, and that's the next slide. Also, the classifiers differ more than the strategies do. The SVM beats the Random Forest by nine to twelve accuracy points. No strategy moved a classifier by more than about five.
""", [
    "Don't say '3-Changepoint is better'. This slide shows the highest means, not a test (audit B1).",
    "SVM with 3-Changepoint: macro F1 0.7010, accuracy 0.7017 (backup B1).",
    "LSTM and MLP values are means over five seeds.",
])

# ================================================================= 9. McNemar
s = content_slide("Only the Random Forest's gain over SME was significant")
picture(s, "vs-sme.png", LM, TOP, 8.3)
textbox(s, px, TOP + 0.2, pw, 1.6, [
    {"runs": [("+4.79", {"bold": True})], "size": 44, "color": NAVY, "space_after": 0},
    {"runs": ["accuracy points, Random Forest at k = 3 (p < 0.001)"], "size": 15, "color": INK2},
])
textbox(s, px, 3.55, pw, 2.8, [
    {"runs": ["SVM +1.70 (p = 0.082), MLP and LSTM: not significant"], "size": 14, "bullet": True,
     "space_after": 6},
    {"runs": ["LSTM −2.49 at k = 5: one seed, flips in 3 of 5 seeds"], "size": 14, "bullet": True,
     "space_after": 10},
    {"runs": [("Largest gain, weakest model. Four classifiers can't show whether that is about capacity.",
               {"bold": True})], "size": 14},
])
finish(s, """
So are these differences reliable? Each dot is the accuracy difference from SME, and the filled dots survived Holm correction. Only the Random Forest shows a reliable gain: almost five points with three changepoints, and it holds at five and seven. The SVM gained 1.7 points, but that wasn't significant, and neither neural model shows a reliable effect. The one filled LSTM dot comes from a single seed, and it flips direction in three of five seeds, so I don't read anything into it.

The largest gain went to the weakest model. That's interesting, but with only four classifiers we can't say it's about model capacity.
""", [
    "Random Forest: +4.79 at k = 3 (p < 0.001); +2.59 at k = 5 and +2.39 at k = 7 (p = 0.004 each).",
    "Gains at k = 3: RF +4.79, SVM +1.70, MLP +1.05, LSTM -0.15. Don't repeat the paper's 'SVM gains least'; it gains second most (audit E1).",
    "Don't say the benefit 'depends on model capacity' (audit B4).",
    "McNemar for LSTM and MLP uses one seed's predictions (backup B2).",
])

# ================================================================= 10. Frame budget
s = content_slide("No classifier improved beyond three changepoint frames")
picture(s, "frame-budget.png", LM, TOP, 7.4)
bx2, bw2 = 8.75, RM - 8.75
textbox(s, bx2, TOP + 0.25, bw2, 4.3, [
    {"runs": [("Never above k = 3", {"bold": True})], "size": 22, "color": NAVY, "space_after": 14},
    {"runs": ["SVM: 0.701 → 0.697 → 0.688, lower at each step"], "size": 15, "bullet": True,
     "space_after": 8},
    {"runs": ["MLP and Random Forest: changed by less than 0.003 from k = 5 to 7"], "size": 15, "bullet": True,
     "space_after": 8},
    {"runs": ["Extra peaks are smaller movements by construction"], "size": 15, "bullet": True,
     "space_after": 14},
    {"runs": [("Differences between k values were not tested.", {"italic": True})], "size": 14, "color": MUTED},
])
finish(s, """
What about the number of frames? This shows how macro F1 changes as we go from three to five to seven peaks. Nothing goes above zero, so no classifier got better with more frames. The SVM dropped at each step. For the MLP and the Random Forest, the change from five to seven was tiny. We didn't test these differences, so read this as a pattern, not a result.
""", [
    "Macro F1 at k = 3 / 5 / 7. SVM 0.701 / 0.697 / 0.688; MLP 0.662 / 0.647 / 0.645; RF 0.590 / 0.561 / 0.561; LSTM 0.655 / 0.641 / 0.649.",
    "Don't say the extra frames capture blinks or jitter (audit B7). Centering cancels head shake, and a blink moves few of the 478 landmarks.",
    "Only if asked about cost: 7-Changepoint took about 35% longer to extract than SME or 3-Changepoint on a 10-video sample (8.4 s vs. 6.0 to 6.2 s per clip). The paper's '7.8%' is wrong (audit E2).",
])

# ================================================================= 11. Takeaways
s = content_slide("What the results suggest")
tw, tg = (CW - 2 * 0.35) / 3, 0.35
takeaways = [
    "Every classifier had its highest mean macro F1 with 3-Changepoint. The gain over SME was significant only "
    "for the Random Forest.",
    "Keeping more than three velocity peaks did not improve any model.",
    "Frame selection should be reported and compared, not fixed by default.",
]
for i, t in enumerate(takeaways):
    c = box(s, LM + i * (tw + tg), TOP + 0.1, tw, 2.75)
    box_text(c, [
        {"runs": [(str(i + 1), {"bold": True})], "size": 32, "color": NAVY, "space_after": 4},
        {"runs": [t], "size": 17},
    ], anchor=MSO_ANCHOR.TOP, margin=0.25)
imp = box(s, LM, 4.85, CW, 1.5, fill=NAVY)
box_text(imp, [
    {"runs": [("For classrooms", {"bold": True, "size": 15, "color": RGBColor(0xC9, 0xD3, 0xEA)})],
     "space_after": 4},
    {"runs": [("At about 0.70 macro F1, an engagement estimate is a hint for the teacher, not an automatic trigger.",
               {"color": WHITE})]},
], anchor=MSO_ANCHOR.MIDDLE, margin=0.3, size=20)
finish(s, """
So, three takeaways. First, every classifier had its highest mean macro F1 with three changepoints, but the gain over SME was significant only for the Random Forest. Second, keeping more than three velocity peaks didn't help any model. Third, frame selection should be reported and compared, not left as a default nobody mentions.

For classrooms, a model at about 0.70 macro F1 shouldn't act on its own. I'd treat its output as a hint for the teacher, not an automatic trigger.
""", [
    "Takeaway 3 is a suggestion (audit B5). Don't say frame selection 'must be tuned'.",
    "The classroom point is our opinion (audit B14). Say 'I'd treat', not 'it should be'.",
])

# ================================================================= 12. Limits -> thesis
s = content_slide("Limits of this study, and what my thesis study adds")
rows = [
    ["This study", "Thesis study (planned)"],
    ["SME only at k = 3; no random control", "Position-based and random selection at k = 3, 5, 7"],
    ["32 of the 91 training participants", "All 91"],
    ["Neural-model tests on one seed's predictions", "A result must hold on all five seeds or draws"],
    ["MLP, SVM, Random Forest saw only the frame mean", "Also concatenation, change, and self-similarity"],
    ["One content rule (velocity peaks)", "Adds k-BOCPD (Adams & MacKay, 2007)"],
    ["Binary labels, one dataset", "Still open"],
]
table(s, LM, TOP + 0.15, CW, [5.3, 6.2], rows, size=16, row_h=0.6, muted_rows=(6,))
finish(s, """
This study has limits, and my thesis is designed around them. SME was only tested at three frames, and there was no random baseline, so the thesis adds positional and random selection at three, five, and seven. It uses all ninety-one training participants. A result has to hold on all five seeds, not just one. The other classifiers get more than the frame average. And there's a second content rule, k-BOCPD. Binary labels and a single dataset are still open.
""", [
    "Thesis design: 13 selection conditions (SME at k = 3; positional, random, k-Changepoint and k-BOCPD at k = 3, 5, 7).",
    "Temporal representations: concatenation, mean + change, mean + cosine self-similarity; LSTM: averaging vs. attention readout.",
    "k-BOCPD: Bayesian online changepoint detection on landmark positions (Adams & MacKay, 2007).",
    "Don't promise results or dates.",
])

# ================================================================= 13. Thank you
s = prs.slides.add_slide(LAYOUT["Title Slide-Editable Title_Sub-1"])
s.placeholders[0].text_frame.text = "Thank you"
s.placeholders[1].text_frame.text = "Questions are welcome"
textbox(s, 6.27, 5.65, 6.03, 0.7, [
    {"runs": [("lester_sityar@dlsu.edu.ph  ·  judith.azcarraga@dlsu.edu.ph", {"size": 14, "color": INK2})],
     "align": PP_ALIGN.CENTER},
])
finish(s, """
Thank you. I'm happy to take questions.
""", [
    "Backups: B1 full results, B2 McNemar table, B3 seed spread, B4 model settings, B5 feature importance, B6 common clip set.",
    "Q&A answers are in talk-notes.md.",
])

# ================================================================= 14. References
s = content_slide("References")
refs = [
    "Adams, R. P., & MacKay, D. J. C. (2007). Bayesian online changepoint detection. arXiv:0710.3742.",
    "Fredricks, J. A., Blumenfeld, P. C., & Paris, A. H. (2004). School engagement: Potential of the concept, state "
    "of the evidence. Review of Educational Research, 74(1), 59–109.",
    "Gupta, A., D'Cunha, A., Awasthi, K., & Balasubramanian, V. (2016). DAiSEE: Towards user engagement recognition "
    "in the wild. arXiv:1609.01885.",
    "Korbar, B., Tran, D., & Torresani, L. (2019). SCSampler: Sampling salient clips from video for efficient action "
    "recognition. ICCV.",
    "Lugaresi, C., et al. (2019). MediaPipe: A framework for building perception pipelines. arXiv:1906.08172.",
    "Singh, M., Hoque, X., Zeng, D., Wang, Y., Ikeda, K., & Dhall, A. (2023). Do I have your attention: A large scale "
    "engagement prediction dataset and baselines. ICMI '23, 174–182.",
    "Truong, C., Oudre, L., & Vayatis, N. (2020). Selective review of offline change point detection methods. "
    "Signal Processing, 167, 107299.",
    "Wang, L., et al. (2016). Temporal segment networks: Towards good practices for deep action recognition. "
    "ECCV, 20–36.",
]
tb = textbox(s, LM, TOP, CW, 4.9, [{"runs": [r], "size": 13, "space_after": 7} for r in refs])
for p in tb.text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(0.35)))
    pPr.set("indent", str(-Inches(0.35)))
finish(s, "Not presented. Leave it up during questions only if nobody needs a backup slide.")

# ================================================================= Backup divider
s = prs.slides.add_slide(LAYOUT["Section Header"])
s.shapes.title.text_frame.text = "Backup slides"
s.placeholders[1].text_frame.text = "For questions"
finish(s, "Backup slides start here. Jump to them only when a question needs one.")

# ================================================================= B1 full results
s = content_slide("B1. All 16 configurations (test split, 2,005 clips)")
res = [
    ["Sampling", "Model", "Accuracy", "Macro F1", "C0 F1", "C1 F1", "PCC", "MSE"],
    ["SME", "LSTM", "0.6480 ± 0.0129", "0.6475", "0.6526", "0.6424", "0.2983", "0.3520"],
    ["SME", "MLP", "0.6509 ± 0.0096", "0.6497", "0.6485", "0.6508", "0.3042", "0.3491"],
    ["SME", "SVM", "0.6848", "0.6838", "0.7013", "0.6663", "0.3754", "0.3152"],
    ["SME", "RF", "0.5651", "0.5307", "0.6578", "0.4036", "0.1705", "0.4349"],
    ["3-CP", "LSTM", "0.6553 ± 0.0022", "0.6548", "0.6511", "0.6585", "0.3113", "0.3447"],
    ["3-CP", "MLP", "0.6630 ± 0.0047", "0.6617", "0.6450", "0.6784", "0.3267", "0.3370"],
    ["3-CP", "SVM", "0.7017", "0.7010", "0.7163", "0.6856", "0.4090", "0.2983"],
    ["3-CP", "RF", "0.6130", "0.5904", "0.6866", "0.4941", "0.2700", "0.3870"],
    ["5-CP", "LSTM", "0.6454 ± 0.0077", "0.6413", "0.6143", "0.6683", "0.2945", "0.3546"],
    ["5-CP", "MLP", "0.6491 ± 0.0045", "0.6471", "0.6333", "0.6609", "0.3001", "0.3509"],
    ["5-CP", "SVM", "0.6973", "0.6966", "0.7111", "0.6820", "0.3995", "0.3027"],
    ["5-CP", "RF", "0.5910", "0.5612", "0.6756", "0.4467", "0.2290", "0.4090"],
    ["7-CP", "LSTM", "0.6520 ± 0.0080", "0.6494", "0.6336", "0.6652", "0.3068", "0.3480"],
    ["7-CP", "MLP", "0.6466 ± 0.0121", "0.6445", "0.6299", "0.6591", "0.2950", "0.3534"],
    ["7-CP", "SVM", "0.6898", "0.6884", "0.7091", "0.6677", "0.3871", "0.3102"],
    ["7-CP", "RF", "0.5890", "0.5610", "0.6720", "0.4499", "0.2213", "0.4110"],
]
table(s, LM, TOP - 0.05, CW, [1.1, 1.0, 2.2, 1.45, 1.45, 1.45, 1.4, 1.45], res, size=12, row_h=0.268,
      bold_rows=(7,), align_right_cols=(2, 3, 4, 5, 6, 7))
textbox(s, LM, 6.28, CW, 0.3, [{"runs": [
    "C0 = levels 0–2 pooled; C1 = Highly-Engaged. LSTM and MLP: mean ± SD over five seeds. Paper, Table 1."],
    "size": 11, "color": MUTED}])
finish(s, "Paper Table 1. The bold row is the best configuration.", [
    "Training times are in the paper's Table 1 (1.8 to 13.0 s); not shown here.",
])

# ================================================================= B2 McNemar table
s = content_slide("B2. Accuracy difference from SME, Holm-corrected McNemar p-values")
mc = [
    ["Model", "3-Changepoint", "5-Changepoint", "7-Changepoint"],
    ["Random Forest", "+4.79 (p < 0.001)*", "+2.59 (p = 0.004)*", "+2.39 (p = 0.004)*"],
    ["SVM", "+1.70 (p = 0.082)", "+1.25 (p = 0.209)", "+0.50 (p = 0.558)"],
    ["MLP", "+1.05 (p = 0.413)", "−0.45 (p = 0.611)", "−1.65 (p = 0.233)"],
    ["LSTM", "−0.15 (p = 0.890)", "−2.49 (p = 0.011)*†", "−0.60 (p = 0.751)"],
]
table(s, LM, TOP + 0.2, CW, [2.5, 3.0, 3.0, 3.0], mc, size=17, row_h=0.62)
textbox(s, LM, 5.0, CW, 1.2, [
    {"runs": ["Percentage points; positive favors changepoint. * Significant after Holm–Bonferroni within the family."],
     "size": 14, "color": INK2, "space_after": 4},
    {"runs": ["† McNemar uses one seed's predictions; this difference reverses sign in three of five seeds."],
     "size": 14, "color": INK2},
])
finish(s, "Paper Table 2.", [
    "Exact McNemar works because every condition is tested on the same 2,005 clips.",
    "The family here is each changepoint condition vs. SME within an architecture.",
])

# ================================================================= B3 seed spread
s = content_slide("B3. Spread across five seeds")
picture(s, "seed-sd.png", LM + 0.35, TOP, 10.8)
textbox(s, LM, 5.95, CW, 0.6, [{"runs": [
    "LSTM accuracy varied less with 3-Changepoint (SD 0.0022) than with SME (0.0129). The pattern was weaker at "
    "k = 5 and 7, and did not hold for the MLP at k = 7."], "size": 14, "color": INK2}])
finish(s, "If asked about stability across seeds.", [
    "The paper says 'six-fold variance'. 0.0129 / 0.0022 is about 5.9, a ratio of standard deviations; the variances differ about 34-fold (study guide Q14).",
    "Don't say content-based selection 'improves reproducibility' (audit B6).",
])

# ================================================================= B4 model settings
s = content_slide("B4. Model settings: library defaults, no hyperparameter search")
ms = [
    ["Model", "Input", "Settings"],
    ["LSTM", "Selected frames, in order", "64-unit LSTM → 32-unit dense; mean over time steps; five seeds"],
    ["MLP", "Mean of the selected frames", "Same widths as the LSTM; five seeds"],
    ["SVM", "Mean of the frames, standardized", "RBF kernel; deterministic"],
    ["Random Forest", "Mean of the frames", "100 unpruned trees; deterministic"],
]
table(s, LM, TOP + 0.2, CW, [2.3, 3.7, 5.5], ms, size=16, row_h=0.62)
textbox(s, LM, 5.0, CW, 1.0, [{"runs": [
    "The comparison is between architectures at default settings, not at their best-tuned settings."],
    "size": 15, "color": INK2}])
finish(s, "Paper Section 2.4.", [
    "With 3 to 7 frames, an LSTM has little sequence to model. Don't read 'LSTM no better than MLP' as a general verdict.",
])

# ================================================================= B5 feature importance
s = content_slide("B5. Random Forest feature importance (Gini), top 5")
fi = [
    ["Rank", "SME", "Gini", "3-Changepoint", "Gini"],
    ["1", "Brow outer up, right (blendshape)", "0.0127", "Brow outer up, right (blendshape)", "0.0149"],
    ["2", "Brow inner up (blendshape)", "0.0109", "Left wrist visibility (pose)", "0.0106"],
    ["3", "Left wrist visibility (pose)", "0.0074", "Brow inner up (blendshape)", "0.0090"],
    ["4", "Cheek squint, left (blendshape)", "0.0054", "Left hip visibility (pose)", "0.0077"],
    ["5", "Face landmark 138, x", "0.0048", "Right wrist, y (pose)", "0.0063"],
]
table(s, LM, TOP + 0.2, CW, [0.8, 4.1, 1.1, 4.4, 1.1], fi, size=15, row_h=0.56, align_right_cols=(2, 4))
textbox(s, LM, 5.25, CW, 1.1, [
    {"runs": ["Importance is spread thin: the top feature carries about 22 times its uniform share (1/1,518)."],
     "size": 14, "color": INK2, "space_after": 4},
    {"runs": ["Gini importance shows what this model used, not which behaviors indicate engagement."],
     "size": 14, "color": INK2},
])
finish(s, "Random Forest only, retrained on the common clip set.", [
    "Say 'in the Random Forest, the right outer-brow-raise blendshape had the highest importance under both' (audit B10).",
    "Wrist visibility may proxy hand movement or camera framing; it was not analyzed further.",
])

# ================================================================= B6 common clip set
s = content_slide("B6. Common clip set: the same clips in every condition")
cc = [
    ["Split", "Clips before", "Clips used"],
    ["Training", "2,825", "2,719"],
    ["Validation", "1,068", "867"],
    ["Test", "2,227", "2,005"],
]
table(s, LM, TOP + 0.2, 7.5, [2.5, 2.5, 2.5], cc, size=17, row_h=0.62, align_right_cols=(1, 2))
textbox(s, LM, 4.4, CW, 1.4, [
    {"runs": ["Every condition was restricted to the clips that all four strategies produced, so predictions can be "
              "paired clip by clip."], "size": 15, "color": INK2, "space_after": 6},
    {"runs": ["Training used 32 of EngageNet's 91 training participants."], "size": 15, "color": INK2},
])
finish(s, "If asked why the clip counts differ from EngageNet's.", [
    "Don't explain why clips dropped out. The cause wasn't logged (audit E5). The thesis logs every clip's extraction outcome.",
])

prs.save(str(OUT))
print("wrote", OUT.name, "with", len(prs.slides), "slides")
