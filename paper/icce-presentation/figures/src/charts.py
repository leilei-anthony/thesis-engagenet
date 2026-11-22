"""Figures for the ICCE 2026 talk (white background, each sized to its slot on a 13.33 x 7.5 in slide).

Run from the repo root:
    conda run -n thesis-engagenet python -I paper/icce-presentation/figures/src/charts.py

Every result number is copied from the ICCE paper (paper/paper.tex):
    macro-f1.png            Table 1, macro F1 column
    vs-sme.png              Table 2 (accuracy difference from SME, Holm-corrected McNemar)
    frame-budget.png        Table 1, macro F1 at k = 3, 5, 7, shown as the change from k = 3
    seed-sd.png             Table 1, the +/- SD of accuracy over five seeds (LSTM, MLP)
The method figures use made-up positions and signals, labeled as such; no EngageNet data:
    velocity-steps.png      the velocity computation of Section 2.3, on six schematic landmarks
    sme-vs-changepoint.png  SME and 3-Changepoint picks on one made-up velocity curve

Adapted from proposal-defense/figures/src/charts.py (same palette, same signals), with the
captions changed for a talk about the paper itself. Wording follows dlsu-manuscript/notes/claim-audit.md.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.signal import find_peaks

OUT = Path(__file__).resolve().parents[1]

# Palette from the proposal-defense figures (validated with the dataviz validator on white)
SME = "#eb6834"                                   # orange: the position-based baseline
CP = {3: "#104281", 5: "#2a78d6", 7: "#6da7ec"}   # one blue, dark -> light as k grows (ordinal ramp)
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 14,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelcolor": INK2,
    "ytick.labelcolor": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})
DPI = 220
CLASSIFIERS = ["SVM", "MLP", "LSTM", "Random Forest"]   # top to bottom, by best macro F1
RULE_NAMES = ["SME", "3-Changepoint", "5-Changepoint", "7-Changepoint"]
RULE_COLORS = [SME, CP[3], CP[5], CP[7]]


def footnote(fig, text):
    fig.text(0.01, 0.015, text, ha="left", va="bottom", fontsize=11, color=MUTED)


def legend_top(ax, handles, ncol, fontsize=13):
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=ncol,
              frameon=False, fontsize=fontsize, handletextpad=0.4, columnspacing=1.2, borderaxespad=0)


def dot(color, filled=True, label=None):
    return Line2D([], [], linestyle="none", marker="o", markersize=11,
                  markerfacecolor=color if filled else "white", markeredgecolor=color,
                  markeredgewidth=2, label=label)


def minus(s):
    return s.replace("-", "−")


# ---------------------------------------------------------------- Table 1
F1 = {  # SME, 3-, 5-, 7-Changepoint (macro F1; LSTM and MLP are five-seed means)
    "LSTM": [0.6475, 0.6548, 0.6413, 0.6494],
    "MLP": [0.6497, 0.6617, 0.6471, 0.6445],
    "SVM": [0.6838, 0.7010, 0.6966, 0.6884],
    "Random Forest": [0.5307, 0.5904, 0.5612, 0.5610],
}
ACC_SD = {  # SD of accuracy over five seeds, SME, 3-, 5-, 7-Changepoint
    "LSTM": [0.0129, 0.0022, 0.0077, 0.0080],
    "MLP": [0.0096, 0.0047, 0.0045, 0.0121],
}


def macro_f1():
    fig, ax = plt.subplots(figsize=(8.3, 4.6))
    offsets = [0.27, 0.09, -0.09, -0.27]
    for row, clf in enumerate(CLASSIFIERS):
        y0 = len(CLASSIFIERS) - 1 - row
        for j, value in enumerate(F1[clf]):
            ax.scatter(value, y0 + offsets[j], s=110, color=RULE_COLORS[j], edgecolor="white",
                       linewidth=1.5, zorder=3)
        best = F1[clf][1]  # 3-Changepoint is the highest in every row (Table 1)
        ax.text(best + 0.004, y0 + offsets[1], f"{best:.3f}", va="center", fontsize=13, color=INK)
    ax.set_yticks(range(len(CLASSIFIERS)))
    ax.set_yticklabels(CLASSIFIERS[::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, len(CLASSIFIERS) - 0.4)
    ax.set_xlim(0.50, 0.73)
    ax.set_xticks(np.arange(0.50, 0.721, 0.05))
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Macro F1 on the test split")
    legend_top(ax, [dot(c, label=n) for c, n in zip(RULE_COLORS, RULE_NAMES)], ncol=4, fontsize=12)
    footnote(fig, "Test split, 2,005 clips. LSTM and MLP: mean of five seeds. Labeled: 3-Changepoint.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "macro-f1.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- Table 2
DIFF = {  # accuracy difference from SME in points, and significant after Holm correction
    "Random Forest": [(4.79, True), (2.59, True), (2.39, True)],
    "SVM": [(1.70, False), (1.25, False), (0.50, False)],
    "MLP": [(1.05, False), (-0.45, False), (-1.65, False)],
    "LSTM": [(-0.15, False), (-2.49, True), (-0.60, False)],
}


def vs_sme():
    fig, ax = plt.subplots(figsize=(8.3, 4.6))
    offsets = {3: 0.22, 5: 0.0, 7: -0.22}
    for row, clf in enumerate(CLASSIFIERS):
        y0 = len(CLASSIFIERS) - 1 - row
        for k, (value, sig) in zip((3, 5, 7), DIFF[clf]):
            y = y0 + offsets[k]
            ax.scatter(value, y, s=110, color=CP[k] if sig else "white", edgecolor=CP[k],
                       linewidth=2, zorder=3)
            if sig:
                label = minus(f"{value:+.2f}")
                if clf == "LSTM":
                    ax.text(value - 0.2, y, label + "†", va="center", ha="right", fontsize=13, color=INK)
                else:
                    ax.text(value + 0.2, y, label, va="center", ha="left", fontsize=13, color=INK)
    ax.axvline(0, color=BASELINE, linewidth=1.5, zorder=1)
    ax.set_yticks(range(len(CLASSIFIERS)))
    ax.set_yticklabels(CLASSIFIERS[::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, len(CLASSIFIERS) - 0.25)
    ax.set_xlim(-4, 6.3)
    ax.set_xticks(range(-4, 7, 2))
    ax.set_xticklabels([minus(f"{t:+d}") if t else "0" for t in range(-4, 7, 2)])
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Accuracy difference from SME (percentage points)")
    ax.text(0.15, 3.62, "changepoint better →", fontsize=12, color=MUTED, va="center")
    ax.text(-0.15, 3.62, "← SME better", fontsize=12, color=MUTED, va="center", ha="right")
    blank = Line2D([], [], linestyle="none", label=" ")
    # the legend fills column by column: row 1 = the three k values, row 2 = the fill key
    handles = [dot(CP[3], label="3-Changepoint"), dot(MUTED, True, "significant (Holm)"),
               dot(CP[5], label="5-Changepoint"), dot(MUTED, False, "not significant"),
               dot(CP[7], label="7-Changepoint"), blank]
    legend_top(ax, handles, ncol=3, fontsize=12)
    footnote(fig, "Exact McNemar tests on 2,005 test clips, Holm–Bonferroni corrected. LSTM and MLP: one seed's predictions.\n"
                  "† Reverses direction in three of five seeds.")
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    fig.savefig(OUT / "vs-sme.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- Table 1, k = 3 -> 5 -> 7
def frame_budget():
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ks = [3, 5, 7]
    label_y = {}
    for clf in CLASSIFIERS:
        base = F1[clf][1]
        delta = [100 * (F1[clf][j] - base) for j in (1, 2, 3)]
        ax.plot(ks, delta, color=INK2, linewidth=2, zorder=2)
        for k, d in zip(ks, delta):
            ax.scatter(k, d, s=95, color=CP[k], edgecolor="white", linewidth=1.5, zorder=3)
        label_y[clf] = delta[-1]
    for clf, y in label_y.items():
        ax.text(7.25, y, f"{clf}  {minus(f'{y:+.2f}')}", va="center", ha="left", fontsize=13, color=INK)
    ax.axhline(0, color=BASELINE, linewidth=1.5, zorder=1)
    ax.set_xlim(2.6, 9.4)
    ax.set_xticks(ks)
    ax.set_xticklabels(["k = 3", "k = 5", "k = 7"])
    ax.set_ylim(-3.5, 0.6)
    ax.set_yticks([-3, -2, -1, 0])
    ax.set_yticklabels([minus(f"{t:+d}") if t else "0" for t in [-3, -2, -1, 0]])
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Change in macro F1 from k = 3\n(points, ×100)")
    footnote(fig, "Changepoint conditions only. LSTM and MLP: mean of five seeds. Not tested for significance.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "frame-budget.png", dpi=DPI)
    plt.close(fig)


def seed_sd():
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2), sharey=True)
    x = np.arange(4)
    for ax, clf in zip(axes, ["LSTM", "MLP"]):
        vals = ACC_SD[clf]
        ax.bar(x, vals, 0.62, color=RULE_COLORS, edgecolor="white", linewidth=2, zorder=3)
        for xi, v in zip(x, vals):
            ax.text(xi, v + 0.0003, f"{v:.4f}", ha="center", va="bottom", fontsize=13, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels(["SME", "3-CP", "5-CP", "7-CP"])
        ax.tick_params(axis="x", length=0)
        ax.set_title(clf, loc="left", fontsize=15, color=INK)
        ax.yaxis.grid(True, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
    axes[0].set_ylim(0, 0.015)
    axes[0].set_ylabel("SD of accuracy, five seeds")
    footnote(fig, "From Table 1 of the paper. Each SD comes from only five seeds, so it is a rough estimate.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "seed-sd.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- made-up illustrations
def velocity_steps():
    """Section 2.3 step by step, on six schematic landmarks (MediaPipe tracks 478). Made-up positions."""
    p_t = np.array([[-1.0, 1.0], [1.0, 1.0], [0.0, 0.2], [-0.7, -0.8], [0.7, -0.8], [0.0, -1.5]])
    shift = np.array([0.9, 0.35])                  # the whole face moves, e.g. the student shifts in the chair
    own = np.zeros_like(p_t)
    own[1] = [0.0, 0.30]                           # landmark 2 moves on its own
    own[4] = [0.10, -0.40]                         # landmark 5 moves on its own
    p_t1 = p_t + shift + own
    c_t, c_t1 = p_t - p_t.mean(0), p_t1 - p_t1.mean(0)
    d = np.linalg.norm(c_t1 - c_t, axis=1)
    v = np.sqrt((d ** 2).sum())
    v_raw = np.sqrt((np.linalg.norm(p_t1 - p_t, axis=1) ** 2).sum())

    fig = plt.figure(figsize=(11.5, 4.45))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.3], wspace=0.06)
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    text_ax = fig.add_subplot(gs[0, 3])
    titles = ["1  Two frames in a row", "2  Center each frame", "3  How far each one moved"]
    for ax, title in zip(axes, titles):
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for side in ax.spines.values():
            side.set_visible(False)
        ax.set_title(title, loc="left", fontsize=13.5, color=INK, pad=6)

    def draw(ax, a, b):
        ax.scatter(a[:, 0], a[:, 1], s=95, facecolor="white", edgecolor=MUTED, linewidth=2, zorder=3)
        ax.scatter(b[:, 0], b[:, 1], s=95, color=CP[5], edgecolor="white", linewidth=1.5, zorder=4)

    a1, a2, a3 = axes
    draw(a1, p_t, p_t1)
    a1.annotate("", xy=p_t1.mean(0), xytext=p_t.mean(0),
                arrowprops=dict(arrowstyle="-|>", color=INK2, linewidth=1.5))
    a1.text(0.45, -2.5, "the whole face shifts,\nand two landmarks also move", ha="center", fontsize=12, color=INK2)
    a1.set_xlim(-1.7, 2.6); a1.set_ylim(-2.95, 2.0)

    draw(a2, c_t, c_t1)
    a2.scatter([0], [0], marker="+", s=150, color=INK2, linewidth=1.5, zorder=5)
    a2.text(0.2, -0.02, "mean", fontsize=11, color=MUTED, va="center")
    a2.text(0.0, -2.5, "subtract each frame's mean:\nthe shift is gone", ha="center", fontsize=12, color=INK2)
    a2.set_xlim(-2.15, 2.15); a2.set_ylim(-2.95, 2.0)

    for i, (a, b) in enumerate(zip(c_t, c_t1)):
        a3.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=CP[3], linewidth=1.6,
                                                        shrinkA=0, shrinkB=0))
        a3.scatter(*a, s=95, facecolor="white", edgecolor=MUTED, linewidth=2, zorder=3)
        dx = 0.18 if a[0] >= 0 else -0.18
        a3.text(a[0] + dx, a[1] + 0.05, f"$d_{i + 1}$ = {d[i]:.2f}", fontsize=11.5, color=INK,
                ha="left" if dx > 0 else "right", va="bottom")
    a3.text(0.0, -2.5, "the length of each arrow", ha="center", fontsize=12, color=INK2)
    a3.set_xlim(-2.15, 2.15); a3.set_ylim(-2.95, 2.0)

    text_ax.axis("off")
    terms = (" + ".join(f"{x:.2f}²" for x in d[:3]) + "\n    + " + " + ".join(f"{x:.2f}²" for x in d[3:]))
    lines = [
        (0.99, "4  Combine into one number", 13.5, INK),
        (0.83, r"$v_t = \sqrt{d_1^2 + d_2^2 + \cdots + d_{478}^2}$", 18, INK),
        (0.64, f"With these 6 landmarks:\n√({terms})\n= {v:.2f}", 11.5, INK2),
        (0.33, f"Without step 2 it would be {v_raw:.2f}:\nthe whole-face shift would hide\n"
               "the two landmarks that moved.", 11.5, INK2),
        (0.10, "5  Repeat for every pair of frames:\nthis gives the velocity curve.", 13.5, INK),
    ]
    for y, text, size, color in lines:
        text_ax.text(0.02, y, text, fontsize=size, color=color, va="top", ha="left", transform=text_ax.transAxes,
                     linespacing=1.35)

    handles = [dot(MUTED, filled=False, label="frame t"), dot(CP[5], label="frame t+1")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.998), ncol=2, frameon=False,
               fontsize=12.5, handletextpad=0.4, columnspacing=1.4)
    footnote(fig, "Schematic: 6 landmarks with made-up positions. MediaPipe tracks 478, each with x and y. "
                  "Not EngageNet data.")
    fig.subplots_adjust(left=0.01, right=0.995, top=0.85, bottom=0.07)
    fig.savefig(OUT / "velocity-steps.png", dpi=DPI)
    plt.close(fig)
    print("velocity-steps: d =", np.round(d, 2).tolist(), f"v = {v:.3f}", f"without centering = {v_raw:.3f}")


def sme_vs_changepoint():
    """One made-up clip of 40 valid frames: where SME and 3-Changepoint take their frames."""
    n = 40                                    # valid frames in the made-up clip
    t = np.arange(1, n)                       # v_t lies between valid frames t and t + 1
    rng = np.random.default_rng(7)
    raw = 0.12 + 0.03 * rng.random(n - 1)
    for centre, height in [(7, 0.95), (17, 0.70), (23, 0.50), (32, 0.85)]:
        raw += height * np.exp(-0.5 * ((t - centre) / 0.8) ** 2)
    raw[11] += 0.9                            # one jittery frame
    smooth = np.convolve(raw, np.ones(5) / 5, mode="same")   # as in get_landmark_velocity
    smooth = np.pad(smooth, (0, 1), mode="edge")              # one value per valid frame
    peaks, _ = find_peaks(smooth, distance=7)
    top = np.sort(peaks[np.argsort(smooth[peaks])[-3:]])
    frames = np.arange(1, n + 1)
    sme = [0, n // 2, n - 1]                  # first, middle (valid_indices[len // 2]) and last valid frame

    fig, ax = plt.subplots(figsize=(8.3, 4.6))
    ax.plot(t, raw, color=BASELINE, linewidth=1.4)
    ax.plot(frames, smooth, color=CP[5], linewidth=2.5)
    for p in top:
        ax.vlines(frames[p], 0, smooth[p], color=CP[3], linewidth=1.5, linestyle=(0, (3, 3)))
        ax.scatter(frames[p], smooth[p], s=120, color=CP[3], edgecolor="white", linewidth=1.5, zorder=5)
    for p in sme:
        ax.vlines(frames[p], 0, smooth[p], color=SME, linewidth=1.5, linestyle=(0, (3, 3)))
        ax.scatter(frames[p], smooth[p], s=120, color=SME, edgecolor="white", linewidth=1.5, marker="D", zorder=5)
    maxima, _ = find_peaks(smooth, prominence=0.05)
    others = [p for p in maxima if p not in top]
    for p in others:
        ax.scatter(frames[p], smooth[p], s=100, color="white", edgecolor=CP[5], linewidth=2, zorder=4)
    if others:
        p = others[0]
        ax.annotate("within 7 frames of a\nhigher peak: skipped", xy=(frames[p], smooth[p]),
                    xytext=(frames[p] + 1.5, smooth[p] + 0.42), fontsize=12, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    ax.annotate("one-frame jitter:\nsmoothed away", xy=(12, raw[11]), xytext=(13.3, 1.03),
                fontsize=12, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    ax.set_xlim(0, n + 1)
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Valid frame, in time order (every 2nd video frame)")
    ax.set_ylabel("Landmark velocity")
    handles = [Line2D([], [], color=BASELINE, linewidth=1.4, label="velocity"),
               Line2D([], [], color=CP[5], linewidth=2.5, label="smoothed (5 frames)"),
               dot(CP[3], label="3-Changepoint"),
               Line2D([], [], linestyle="none", marker="D", markersize=10, markerfacecolor=SME,
                      markeredgecolor=SME, label="SME")]
    legend_top(ax, handles, ncol=4, fontsize=12)
    footnote(fig, "Made-up signal, 40 valid frames, k = 3. Not EngageNet data.")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT / "sme-vs-changepoint.png", dpi=DPI)
    plt.close(fig)
    print("sme-vs-changepoint: changepoint frames", [int(frames[p]) for p in top],
          "| SME frames", [int(frames[p]) for p in sme], "| skipped peaks", [int(frames[p]) for p in others])


if __name__ == "__main__":
    macro_f1()
    vs_sme()
    frame_budget()
    seed_sd()
    velocity_steps()
    sme_vs_changepoint()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
