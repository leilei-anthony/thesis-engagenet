"""Charts for the proposal defense slides (white background, sized for a 16:9 slide).

Run from the repo root:
    conda run -n thesis-engagenet python -I proposal-defense/figures/src/charts.py

Every number is copied from the manuscript:
    prelim-macro-f1.png   Table 5.1 (dlsu-manuscript/chapter_5.tex, tab:prelim-f1)
    prelim-vs-sme.png     Table 5.2 (tab:prelim-mcnemar)
    class-balance.png     Table 5.3 (tab:thresholds)
    label-split.png       Table 5.3 by subtraction (per-level counts), checked against data/labels/*
    velocity-peaks.png    a SYNTHETIC signal, labeled as such on the image; no EngageNet data
    bocpd-score.png       a SYNTHETIC signal, labeled as such on the image; no EngageNet data.
                          Its BOCPD code is a minimal illustration of Section 4.4 (D44-D47), not the
                          study implementation, which the proponent writes (docs/implementation-spec.md).
    velocity-steps.png    Equation 4.1 step by step on six SCHEMATIC landmarks with made-up positions (20 Nov)
    bocpd-run-length.png  the run-length probabilities behind Eq. 4.2, on the bocpd-score.png signal (20 Nov)
    content-rules-compare.png  one SYNTHETIC signal under both content rules (20 Nov)
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.signal import find_peaks

OUT = Path(__file__).resolve().parents[1]

# Palette (validated with the dataviz skill's validator on a white surface)
SME = "#eb6834"                                   # orange: the position-based baseline
CP = {3: "#104281", 5: "#2a78d6", 7: "#6da7ec"}   # one blue, dark -> light as k grows (ordinal ramp)
SPLITS = {"Training": "#2a78d6", "Validation": "#eb6834", "Test": "#1baf7a"}
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 15,
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


def footnote(fig, text):
    fig.text(0.01, 0.015, text, ha="left", va="bottom", fontsize=11, color=MUTED)


def legend_top(ax, handles, ncol):
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=ncol,
              frameon=False, fontsize=13, handletextpad=0.4, columnspacing=1.4, borderaxespad=0)


def dot(color, filled=True, label=None):
    return Line2D([], [], linestyle="none", marker="o", markersize=11,
                  markerfacecolor=color if filled else "white", markeredgecolor=color,
                  markeredgewidth=2, label=label)


# ---------------------------------------------------------------- Table 5.1
F1 = {  # SME, 3-, 5-, 7-Changepoint
    "LSTM": [0.6475, 0.6548, 0.6413, 0.6494],
    "MLP": [0.6497, 0.6617, 0.6471, 0.6445],
    "SVM": [0.6838, 0.7010, 0.6966, 0.6884],
    "Random Forest": [0.5307, 0.5904, 0.5612, 0.5610],
}


def prelim_macro_f1():
    fig, ax = plt.subplots(figsize=(10, 4.9))
    colors = [SME, CP[3], CP[5], CP[7]]
    names = ["SME", "3-Changepoint", "5-Changepoint", "7-Changepoint"]
    offsets = [0.27, 0.09, -0.09, -0.27]
    for row, clf in enumerate(CLASSIFIERS):
        y0 = len(CLASSIFIERS) - 1 - row
        for j, value in enumerate(F1[clf]):
            ax.scatter(value, y0 + offsets[j], s=120, color=colors[j], edgecolor="white",
                       linewidth=1.5, zorder=3)
        best = F1[clf][1]  # 3-Changepoint is the highest in every row (Table 5.1)
        ax.text(best + 0.0035, y0 + offsets[1], f"{best:.3f}", va="center", fontsize=13, color=INK)
    ax.set_yticks(range(len(CLASSIFIERS)))
    ax.set_yticklabels(CLASSIFIERS[::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, len(CLASSIFIERS) - 0.4)
    ax.set_xlim(0.50, 0.725)
    ax.set_xticks(np.arange(0.50, 0.721, 0.05))
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Macro F1 on the test split")
    legend_top(ax, [dot(c, label=n) for c, n in zip(colors, names)], ncol=4)
    footnote(fig, "Preliminary study, threshold 3, 2,005 test clips. LSTM and MLP: mean of five seeds. Values labeled: 3-Changepoint.\n"
                  "Adapted from Sityar & Azcarraga (2026).")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "prelim-macro-f1.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- Table 5.2
DIFF = {  # accuracy difference from SME in points, and significant after Holm correction
    "Random Forest": [(4.79, True), (2.59, True), (2.39, True)],
    "SVM": [(1.70, False), (1.25, False), (0.50, False)],
    "MLP": [(1.05, False), (-0.45, False), (-1.65, False)],
    "LSTM": [(-0.15, False), (-2.49, True), (-0.60, False)],
}


def prelim_vs_sme():
    fig, ax = plt.subplots(figsize=(10, 4.9))
    offsets = {3: 0.22, 5: 0.0, 7: -0.22}
    for row, clf in enumerate(CLASSIFIERS):
        y0 = len(CLASSIFIERS) - 1 - row
        for k, (value, sig) in zip((3, 5, 7), DIFF[clf]):
            y = y0 + offsets[k]
            ax.scatter(value, y, s=120, color=CP[k] if sig else "white", edgecolor=CP[k],
                       linewidth=2, zorder=3)
            if sig:
                label = f"{value:+.2f}".replace("-", "−")
                if clf == "LSTM":
                    ax.text(value - 0.18, y, label + "†", va="center", ha="right", fontsize=13, color=INK)
                else:
                    ax.text(value + 0.18, y, label, va="center", ha="left", fontsize=13, color=INK)
    ax.axvline(0, color=BASELINE, linewidth=1.5, zorder=1)
    ax.set_yticks(range(len(CLASSIFIERS)))
    ax.set_yticklabels(CLASSIFIERS[::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-0.6, len(CLASSIFIERS) - 0.4)
    ax.set_xlim(-4, 6)
    ax.set_xticks(range(-4, 7, 2))
    ax.set_xticklabels([f"{t:+d}".replace("-", "−") if t else "0" for t in range(-4, 7, 2)])
    ax.xaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Accuracy difference from SME (percentage points)")
    ax.text(0.15, -0.55, "changepoint better →", fontsize=12, color=MUTED, va="bottom")
    ax.text(-0.15, -0.55, "← SME better", fontsize=12, color=MUTED, va="bottom", ha="right")
    blank = Line2D([], [], linestyle="none", label=" ")
    # the legend fills column by column: row 1 = the three k values, row 2 = the fill key
    handles = [dot(CP[3], label="3-Changepoint"), dot(MUTED, True, "significant after Holm–Bonferroni"),
               dot(CP[5], label="5-Changepoint"), dot(MUTED, False, "not significant"),
               dot(CP[7], label="7-Changepoint"), blank]
    legend_top(ax, handles, ncol=3)
    for t in ax.get_legend().get_texts():
        t.set_fontsize(12)
    footnote(fig, "McNemar tests on 2,005 test clips, Holm–Bonferroni corrected; LSTM and MLP tests use seed 42.\n"
                  "† Reverses direction in three of five seeds. Adapted from Sityar & Azcarraga (2026).")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "prelim-vs-sme.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- Table 5.3
NEG = {  # share of clips below the threshold, %, for t = 1, 2, 3
    "Training": [18.4, 31.5, 52.5],
    "Validation": [12.3, 21.4, 46.9],
    "Test": [20.3, 31.2, 49.7],
}


def class_balance():
    fig, ax = plt.subplots(figsize=(10, 4.9))
    x = np.arange(3)
    width = 0.26
    for i, (split, values) in enumerate(NEG.items()):
        xs = x + (i - 1) * width
        ax.bar(xs, values, width, color=SPLITS[split], edgecolor="white", linewidth=2, label=split, zorder=3)
        for xi, v in zip(xs, values):
            ax.text(xi, v + 1.0, f"{v:.1f}%", ha="center", va="bottom", fontsize=12, color=INK, zorder=4,
                    bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    ax.axhline(50, color=INK2, linewidth=1.2, linestyle=(0, (5, 4)), zorder=2)
    ax.text(-0.45, 50.8, "balanced (50%)", fontsize=12, color=INK2, ha="left", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(["t = 1\nNot-Engaged vs. rest", "t = 2\nlevels 0–1 vs. 2–3",
                        "t = 3\nHighly-Engaged vs. rest"])
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 62)
    ax.set_yticks(range(0, 61, 10))
    ax.set_yticklabels([f"{t}%" for t in range(0, 61, 10)])
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.set_ylabel("Clips below the threshold")
    legend_top(ax, [plt.Rectangle((0, 0), 1, 1, color=c, label=s) for s, c in SPLITS.items()], ncol=3)
    footnote(fig, "Official EngageNet partition, SNP clips removed (7,879 training, 1,071 validation, "
                  "2,256 test clips). Counted from the official label files.")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "class-balance.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- label shares by split
LEVELS = ["Not-Engaged", "Barely-engaged", "Engaged", "Highly-Engaged"]
LEVEL_COLORS = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]  # ordinal blue ramp, steps 250/400/550/700 (validated)
LEVEL_TEXT = [INK, INK, "white", "white"]                     # by fill luminance
LEVEL_COUNTS = {  # clips per level, SNP removed: Table 5.3 by subtraction, checked against the label files
    "Training": [1446, 1035, 1658, 3740],
    "Validation": [132, 97, 273, 569],
    "Test": [457, 246, 419, 1134],
}


def label_split():
    rows = {"All splits": [sum(v) for v in zip(*LEVEL_COUNTS.values())], **LEVEL_COUNTS}
    fig, ax = plt.subplots(figsize=(8, 4.6))
    n = len(rows)
    for i, (name, counts) in enumerate(rows.items()):
        y = n - 1 - i
        total = sum(counts)
        left = 0.0
        for j, c in enumerate(counts):
            share = 100 * c / total
            ax.barh(y, share, left=left, height=0.62, color=LEVEL_COLORS[j], edgecolor="white", linewidth=2, zorder=3)
            ax.text(left + 0.9, y, f"{share:.1f}%", va="center", ha="left", fontsize=13, color=LEVEL_TEXT[j], zorder=4)
            left += share
        ax.text(-2, y + 0.12, name, ha="right", va="center", fontsize=14, color=INK,
                fontweight="bold" if name == "All splits" else "normal")
        ax.text(-2, y - 0.2, f"{total:,} clips", ha="right", va="center", fontsize=12, color=MUTED)
    # Behind the bars, so it shows between rows and never crosses a label.
    ax.axvline(50, color=INK2, linewidth=1.2, linestyle=(0, (5, 4)), zorder=2)
    ax.text(50, -0.52, "50%", ha="center", va="top", fontsize=12, color=INK2)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, n - 0.5)
    ax.axis("off")
    fig.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c, label=l) for l, c in zip(LEVELS, LEVEL_COLORS)],
               loc="upper left", bbox_to_anchor=(0.01, 0.995), ncol=4, frameon=False, fontsize=13,
               handletextpad=0.4, columnspacing=1.4, borderaxespad=0)
    footnote(fig, "Official EngageNet partition, SNP clips removed. Counted from the official label files (Table 5.3).")
    fig.subplots_adjust(left=0.17, right=0.99, top=0.88, bottom=0.14)
    fig.savefig(OUT / "label-split.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- synthetic illustration
def velocity_peaks():
    """Illustrates k-Changepoint selection (Section 4.4) on a made-up signal, k = 3."""
    n = 40                                    # valid frames in the made-up clip
    t = np.arange(1, n)                       # v_t lies between frames t and t + 1
    rng = np.random.default_rng(7)
    raw = 0.12 + 0.03 * rng.random(n - 1)
    for centre, height in [(7, 0.95), (17, 0.70), (23, 0.50), (32, 0.85)]:
        raw += height * np.exp(-0.5 * ((t - centre) / 0.8) ** 2)
    raw[11] += 0.9                            # one jittery frame (v_12)
    smooth = np.convolve(raw, np.ones(5) / 5, mode="same")   # as in get_landmark_velocity
    smooth = np.pad(smooth, (0, 1), mode="edge")              # one value per frame
    peaks, _ = find_peaks(smooth, distance=7)
    top = np.sort(peaks[np.argsort(smooth[peaks])[-3:]])
    frames = np.arange(1, n + 1)

    fig, ax = plt.subplots(figsize=(10, 4.6))
    ax.plot(t, raw, color=BASELINE, linewidth=1.5, label="velocity")
    ax.plot(frames, smooth, color=CP[5], linewidth=2.5, label="smoothed (5-frame average)")
    for p in top:
        ax.vlines(frames[p], 0, smooth[p], color=CP[3], linewidth=1.5, linestyle=(0, (3, 3)))
        ax.scatter(frames[p], smooth[p], s=130, color=CP[3], edgecolor="white", linewidth=1.5, zorder=4)
        ax.text(frames[p], smooth[p] + 0.06, f"frame {frames[p]}", ha="center", fontsize=13, color=INK)
    maxima, _ = find_peaks(smooth, prominence=0.05)          # every clear local maximum
    others = [p for p in maxima if p not in top]             # dropped by the 7-frame rule or not in the top 3
    for p in others:
        ax.scatter(frames[p], smooth[p], s=110, color="white", edgecolor=CP[5], linewidth=2, zorder=4)
    ax.annotate("one-frame jitter:\nflattened by smoothing", xy=(12, raw[11]), xytext=(13.5, 1.02),
                fontsize=12, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    if others:
        p = others[0]
        ax.annotate("peak within 7 frames of a\nhigher one: not selected", xy=(frames[p], smooth[p]),
                    xytext=(frames[p] + 2.0, smooth[p] + 0.32), fontsize=12, color=INK2,
                    arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    ax.set_xlim(0, n + 1)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Valid frame, in temporal order")
    ax.set_ylabel("Facial-landmark velocity")
    ax.yaxis.label.set_color(INK2)
    handles = [Line2D([], [], color=BASELINE, linewidth=1.5, label="velocity between consecutive frames"),
               Line2D([], [], color=CP[5], linewidth=2.5, label="smoothed"),
               dot(CP[3], label="3 highest peaks: selected frames")]
    legend_top(ax, handles, ncol=3)
    footnote(fig, "Illustration with a made-up signal (40 valid frames, k = 3); not EngageNet data.")
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(OUT / "velocity-peaks.png", dpi=DPI)
    plt.close(fig)
    print("velocity-peaks: selected frames", list(frames[top]), "| other peaks", [int(frames[p]) for p in others])


# Same colors as velocity-peaks.png (user's request, 20 Nov): the line in the mid blue, selected frames in
# the dark blue. The rule chips in other figures still mark k-BOCPD in pink.
BOCPD_COLOR = CP[5]
BOCPD_DARK = CP[3]


def _bocpd_forward(x, hazard=1 / 20, cap=50, lag=7, prior=(0.0, 1.0, 2.0, 1.0), return_post=False):
    """Score s_t = P(r_{t+lag-1} = lag | x_1..x_{t+lag-1}) for a 1-D signal (0-based t).
    Run length r = frames in the current segment, counting the current one. Illustration only.
    With return_post, also returns post[t, r] = P(run length r at frame t | frames up to t)."""
    from scipy.special import gammaln, logsumexp

    def logpred(v, mu, ka, al, be):
        nu, s2 = 2 * al, be * (ka + 1) / (al * ka)
        return (gammaln((nu + 1) / 2) - gammaln(nu / 2) - 0.5 * np.log(nu * np.pi * s2)
                - (nu + 1) / 2 * np.log1p((v - mu) ** 2 / (s2 * nu)))

    def update(mu, ka, al, be, v):
        return (ka * mu + v) / (ka + 1), ka + 1, al + 0.5, be + ka * (v - mu) ** 2 / (2 * (ka + 1))

    n = len(x)
    p0 = tuple(np.array([v]) for v in prior)
    stats, logpost = update(*p0, x[0]), np.array([0.0])
    post = np.zeros((n, n + 1))
    post[0, 1] = 1.0
    for t in range(1, n):
        grow = logpost + np.log(1 - hazard) + logpred(x[t], *stats)
        new = logsumexp(logpost) + np.log(hazard) + logpred(x[t], *p0)[0]
        logpost = np.concatenate([[new], grow])[:cap]
        stats = tuple(np.concatenate([a, b])[:cap] for a, b in zip(update(*p0, x[t]), update(*stats, x[t])))
        logpost -= logsumexp(logpost)
        post[t, 1:len(logpost) + 1] = np.exp(logpost)
    s = np.zeros(n)
    for t in range(1, n - lag + 1):
        s[t] = post[t + lag - 1, lag]
    return (s, post) if return_post else s


def _bocpd_signal():
    """The made-up one-component signal of bocpd-score.png and bocpd-run-length.png (60 valid frames)."""
    n = 60
    rng = np.random.default_rng(0)
    x = np.zeros(n)
    x[13:16] += 0.9            # frames 14-16: a quick head turn and back
    x[24:] += 1.0              # frame 25: the face moves and stays
    x[43:] -= 0.6              # frame 44: it moves again and stays
    x += rng.normal(0, 0.08, n)
    return x


def _bocpd_two_way(x, lag=7):
    """Forward and backward scores averaged, as in Section 4.4; frames without 7 valid frames on each
    side get no score (0)."""
    n = len(x)
    fwd = _bocpd_forward(x)
    bwd = np.roll(_bocpd_forward(x[::-1].copy())[::-1], 1)
    bwd[0] = 0
    s = (fwd + bwd) / 2
    s[:lag] = 0
    s[n - lag + 1:] = 0
    return s


def bocpd_score():
    """Illustrates k-BOCPD selection (Section 4.4) on a made-up one-component signal, k = 3."""
    lag = 7
    x = _bocpd_signal()
    n = len(x)
    s = _bocpd_two_way(x, lag)
    peaks, _ = find_peaks(s, distance=7)
    top = np.sort(peaks[np.argsort(s[peaks])[-3:]])
    frames = np.arange(1, n + 1)

    # Laid out like velocity-peaks.png: gray context line, one colored line, dark selected dots with
    # dashed drops, gray notes with leaders. Position and score are different quantities, so they keep
    # two stacked layers on one frame axis rather than sharing a y-axis.
    shown = s.copy()
    shown[:lag] = np.nan
    shown[n - lag + 1:] = np.nan                 # not scored: drawn as no line at all
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 5.0), sharex=True,
                                 gridspec_kw={"height_ratios": [0.75, 1], "hspace": 0.08})
    a1.plot(frames, x, color=BASELINE, linewidth=1.8)
    a1.annotate("quick turn and back", xy=(15, x[14]), xytext=(3, 1.3), fontsize=12, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a1.annotate("moves and stays", xy=(28, x[27]), xytext=(29.5, 1.42), fontsize=12, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a1.set_ylim(-0.35, 1.6)
    a1.spines["bottom"].set_visible(False)
    a1.tick_params(axis="x", length=0)
    a2.plot(frames, shown, color=BOCPD_COLOR, linewidth=2.5)
    low = top[np.argmin(s[top])]
    for p in top:
        a2.vlines(frames[p], 0, s[p], color=BOCPD_DARK, linewidth=1.5, linestyle=(0, (3, 3)))
        a1.axvline(frames[p], color=BOCPD_DARK, linewidth=1.2, linestyle=(0, (3, 3)), alpha=0.6)
        a2.scatter(frames[p], s[p], s=130, color=BOCPD_DARK, edgecolor="white", linewidth=1.5, zorder=4)
        if p == low:   # to the right, clear of the note's leader line on the left
            a2.text(frames[p] + 0.9, s[p] + 0.05, f"frame {frames[p]}", ha="left", fontsize=13, color=INK)
        else:
            a2.text(frames[p], s[p] + 0.06, f"frame {frames[p]}", ha="center", fontsize=13, color=INK)
    a2.annotate("quick turn: low score,\nkept only to fill k = 3", xy=(frames[low], s[low]),
                xytext=(frames[low] - 11.5, 0.42), fontsize=12, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a2.annotate("not scored: 7 frames\nneeded on each side", xy=(n - lag + 1, 0), xytext=(n + 0.8, 0.42),
                ha="right", fontsize=12, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a2.set_ylim(0, max(0.8, s.max() + 0.17))
    for ax in (a1, a2):
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.yaxis.label.set_color(INK2)
    a1.set_ylabel("Landmark\nposition")
    a2.set_ylabel("BOCPD score")
    a2.set_xlabel("Valid frame, in temporal order")
    a2.set_xlim(0, n + 1)
    a2.set_xticks(range(0, n + 1, 10))
    handles = [Line2D([], [], color=BASELINE, linewidth=1.8, label="landmark position (1st component)"),
               Line2D([], [], color=BOCPD_COLOR, linewidth=2.5, label="BOCPD score"),
               dot(BOCPD_DARK, label="3 highest peaks: selected frames")]
    legend_top(a1, handles, ncol=3)
    footnote(fig, "Illustration with a made-up signal (60 valid frames, one component, k = 3); not EngageNet data.")
    fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.18, hspace=0.08)
    fig.savefig(OUT / "bocpd-score.png", dpi=DPI)
    plt.close(fig)
    print("bocpd-score: selected frames", list(frames[top]), "scores", np.round(s[top], 2).tolist())


# ---------------------------------------------------------------- step-by-step explanations (20 Nov)
# Doc Jay asked for the computation behind the two content rules, "as simple as you can" (20 Nov).
BOCPD_LINE, BOCPD_DOT = "#D9628F", "#B0477A"   # the k-BOCPD pink, darkened to pass 3:1 on white (validated)


def velocity_steps():
    """Equation 4.1 step by step, on six schematic landmarks (MediaPipe tracks 478). Made-up positions."""
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

    fig = plt.figure(figsize=(13.5, 5.0))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.35], wspace=0.08)
    axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    text_ax = fig.add_subplot(gs[0, 3])
    titles = ["1  Landmarks in frames t and t+1", "2  Center each frame", "3  How far each landmark moved"]
    for ax, title in zip(axes, titles):
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for side in ax.spines.values():
            side.set_visible(False)
        ax.set_title(title, loc="left", fontsize=14, color=INK, pad=8)

    def draw(ax, a, b):
        ax.scatter(a[:, 0], a[:, 1], s=110, facecolor="white", edgecolor=MUTED, linewidth=2, zorder=3)
        ax.scatter(b[:, 0], b[:, 1], s=110, color=CP[5], edgecolor="white", linewidth=1.5, zorder=4)

    a1, a2, a3 = axes
    draw(a1, p_t, p_t1)
    a1.annotate("", xy=p_t1.mean(0), xytext=p_t.mean(0),
                arrowprops=dict(arrowstyle="-|>", color=INK2, linewidth=1.5))
    a1.text(0.5, -2.45, "the whole face shifts,\nand two landmarks also move", ha="center", fontsize=12, color=INK2)
    a1.set_xlim(-1.7, 2.6); a1.set_ylim(-2.9, 2.0)

    draw(a2, c_t, c_t1)
    a2.scatter([0], [0], marker="+", s=160, color=INK2, linewidth=1.5, zorder=5)
    a2.text(0.2, -0.02, "mean position", fontsize=11, color=MUTED, va="center")
    a2.text(0.0, -2.45, "subtract each frame's mean position:\nthe shift is gone", ha="center", fontsize=12,
            color=INK2)
    a2.set_xlim(-2.15, 2.15); a2.set_ylim(-2.9, 2.0)

    for i, (a, b) in enumerate(zip(c_t, c_t1)):
        a3.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=CP[3], linewidth=1.6,
                                                        shrinkA=0, shrinkB=0))
        a3.scatter(*a, s=110, facecolor="white", edgecolor=MUTED, linewidth=2, zorder=3)
        dx = 0.18 if a[0] >= 0 else -0.18
        a3.text(a[0] + dx, a[1] + 0.05, f"$d_{i + 1}$ = {d[i]:.2f}", fontsize=12, color=INK,
                ha="left" if dx > 0 else "right", va="bottom")
    a3.text(0.0, -2.45, "the length of each arrow", ha="center", fontsize=12, color=INK2)
    a3.set_xlim(-2.15, 2.15); a3.set_ylim(-2.9, 2.0)

    text_ax.axis("off")
    terms = " + ".join(f"{x:.2f}²" for x in d)
    lines = [
        (0.97, "4  Combine them into one number", 14, INK),
        (0.80, r"$v_t = \sqrt{d_1^2 + d_2^2 + \cdots + d_{478}^2}$", 19, INK),
        (0.64, f"Here, with 6 landmarks:\n√({terms})\n= {v:.2f}", 12.5, INK2),
        (0.38, f"Without step 2 it would be {v_raw:.2f}:\nthe shift of the whole face would hide\n"
               "the two landmarks that really moved.", 12.5, INK2),
        (0.13, "5  Repeat for every pair of consecutive\nframes: this gives the velocity curve.", 14, INK),
    ]
    for y, text, size, color in lines:
        text_ax.text(0.02, y, text, fontsize=size, color=color, va="top", ha="left", transform=text_ax.transAxes,
                     linespacing=1.35)

    handles = [dot(MUTED, filled=False, label="frame t"), dot(CP[5], label="frame t+1")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.995), ncol=2, frameon=False,
               fontsize=13, handletextpad=0.4, columnspacing=1.4)
    footnote(fig, "Schematic: 6 landmarks with made-up positions (MediaPipe tracks 478, each with x and y). "
                  "Not EngageNet data. Equation 4.1, Section 4.4.")
    fig.subplots_adjust(left=0.01, right=0.995, top=0.86, bottom=0.08)
    fig.savefig(OUT / "velocity-steps.png", dpi=DPI)
    plt.close(fig)
    print("velocity-steps: d =", np.round(d, 2).tolist(), f"v = {v:.3f}", f"without centering = {v_raw:.3f}")


def bocpd_run_length():
    """The run-length probabilities that k-BOCPD's score reads (Eq. 4.2), on the signal of bocpd-score.png."""
    from matplotlib.colors import LinearSegmentedColormap

    lag, rmax = 7, 36
    x = _bocpd_signal()
    n = len(x)
    _, post = _bocpd_forward(x, return_post=True)
    frames = np.arange(1, n + 1)
    grid = post[:, 1:rmax + 1].T                   # rows: run length 1..rmax; columns: frames
    cmap = LinearSegmentedColormap.from_list("seq", ["#ffffff", CP[7], CP[5], CP[3]])

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6.4), sharex=True,
                                 gridspec_kw={"height_ratios": [0.42, 1], "hspace": 0.08})
    a1.plot(frames, x, color=BASELINE, linewidth=1.8)
    a1.annotate("quick turn and back", xy=(15, x[14]), xytext=(3, 1.25), fontsize=12, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a1.annotate("moves and stays", xy=(27, x[26]), xytext=(29.5, 1.42), fontsize=12, color=INK2,
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a1.set_ylim(-0.35, 1.7)
    a1.set_yticks([])
    a1.set_ylabel("Landmark\nposition")
    for side in ("left", "bottom"):
        a1.spines[side].set_visible(False)
    a1.tick_params(axis="x", length=0)

    im = a2.imshow(grid, origin="lower", aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest",
                   extent=(0.5, n + 0.5, 0.5, rmax + 0.5))
    t_change, t_read = 25, 25 + lag - 1           # the score of frame 25 is read at frame 31
    score = post[t_read - 1, lag]
    a2.add_patch(plt.Rectangle((t_read - 0.5, lag - 0.5), 1, 1, fill=False, edgecolor=INK, linewidth=2, zorder=5))
    a2.annotate(f"score of frame {t_change}:\nP(run length = {lag} at frame {t_read}) = {score:.2f}",
                xy=(t_read + 0.5, lag + 0.5), xytext=(30.5, 29.5), fontsize=12, color=INK, va="bottom",
                arrowprops=dict(arrowstyle="-", color=INK2, linewidth=1))
    a2.annotate("run length grows by one\nwith every frame that fits", xy=(9, 9), xytext=(2, 24),
                fontsize=12, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a2.annotate("quick turn: the long run dips,\nthen recovers", xy=(16, 16), xytext=(13, 31.5),
                fontsize=12, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a2.annotate("lasting change: a new run\nstarts at 1 and takes over", xy=(28, 4), xytext=(41, 4),
                fontsize=12, color=INK2, va="center", arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a2.set_ylabel("Run length:\nframes since the\nsegment began")
    a2.set_xlabel("Valid frame, in temporal order")
    a2.set_xlim(0.5, n + 0.5)
    a2.set_xticks(range(0, n + 1, 10))
    a2.set_yticks([1, 10, 20, 30])
    for ax in (a1, a2):
        ax.yaxis.label.set_color(INK2)
    cax = fig.add_axes([0.80, 0.905, 0.17, 0.022])
    cb = fig.colorbar(im, cax=cax, orientation="horizontal", ticks=[0, 0.5, 1])
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=11, length=0)
    fig.text(0.79, 0.917, "probability", ha="right", va="center", fontsize=12, color=INK2)
    footnote(fig, "Made-up signal (60 valid frames, one component), not EngageNet data. Forward pass only; "
                  "k-BOCPD averages it with a backward pass.\nHazard 1/20, run lengths capped at 50 "
                  "(Section 4.4). Shading: the probability of each run length, given the frames so far.")
    fig.subplots_adjust(left=0.13, right=0.98, top=0.88, bottom=0.2)
    fig.savefig(OUT / "bocpd-run-length.png", dpi=DPI)
    plt.close(fig)
    print(f"bocpd-run-length: score of frame {t_change} (forward) = {score:.3f}; "
          f"most likely run length at frames 14-20:", [int(np.argmax(post[t])) for t in range(13, 20)])


def content_rules_compare():
    """One made-up clip under both content rules (k = 3): velocity peaks vs. the k-BOCPD score."""
    n, lag, k = 70, 7, 3
    rng = np.random.default_rng(3)
    x = np.zeros(n)
    x[11:13] += 1.4            # frames 12-13: a quick glance away and back
    x[49:51] -= 1.3            # frames 50-51: another quick glance
    x[21:] += 0.7              # frame 22: the face moves and stays
    x[34:] -= 0.75             # frame 35: it moves back and stays
    x[59:] += 0.6              # frame 60: it moves again and stays
    x += rng.normal(0, 0.07, n)
    frames = np.arange(1, n + 1)

    vel = np.abs(np.diff(x))                       # one component, so velocity is the size of the step
    smooth = np.pad(np.convolve(vel, np.ones(5) / 5, mode="same"), (0, 1), mode="edge")
    vp, _ = find_peaks(smooth, distance=7)
    v_top = np.sort(vp[np.argsort(smooth[vp])[-k:]])
    s = _bocpd_two_way(x, lag)
    bp, _ = find_peaks(s, distance=7)
    b_top = np.sort(bp[np.argsort(s[bp])[-k:]])

    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(10.5, 7.8), sharex=True,
                                     gridspec_kw={"height_ratios": [0.85, 1, 1], "hspace": 0.12})
    a1.plot(frames, x, color=BASELINE, linewidth=1.8)
    a1.text(14.3, 1.35, "glance away\nand back", fontsize=12, color=INK2, va="center")
    a1.text(52.3, -1.05, "glance away\nand back", fontsize=12, color=INK2, va="center")
    a1.annotate("moves and stays", xy=(28, x[27]), xytext=(28.5, 1.55), fontsize=12, color=INK2, ha="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, linewidth=1))
    a1.set_ylim(-1.6, 1.9)
    a1.set_ylabel("Landmark\nposition")

    def panel(ax, y, line_color, dot_color, top, name, label):
        shown = y.copy()
        ax.plot(frames, shown, color=line_color, linewidth=2.5)
        for p in top:
            ax.vlines(frames[p], 0, y[p], color=dot_color, linewidth=1.5, linestyle=(0, (3, 3)))
            ax.scatter(frames[p], y[p], s=130, color=dot_color, edgecolor="white", linewidth=1.5, zorder=4)
            ax.text(frames[p], y[p] + 0.09 * y.max(), f"{frames[p]}", ha="center", fontsize=13, color=INK)
            a1.axvline(frames[p], color=dot_color, linewidth=1.1, linestyle=(0, (3, 3)), alpha=0.55)
        ax.set_ylim(0, y.max() * 1.6)
        ax.text(0.995, 0.97, name, transform=ax.transAxes, ha="right", va="top", fontsize=13.5, color=INK,
                fontweight="bold")
        ax.text(0.995, 0.80, label, transform=ax.transAxes, ha="right", va="top", fontsize=12, color=INK2)

    panel(a2, smooth, CP[5], CP[3], v_top, "k-Changepoint: velocity peaks",
          "keeps the fastest movements, glances included")
    shown = s.copy()
    shown[:lag] = np.nan
    shown[n - lag + 1:] = np.nan
    panel(a3, np.nan_to_num(shown), BOCPD_LINE, BOCPD_DOT, b_top, "k-BOCPD: lasting changes",
          "keeps where the face moves and stays")
    a2.set_ylabel("Velocity")
    a3.set_ylabel("BOCPD score")
    a3.set_xlabel("Valid frame, in temporal order")
    a3.set_xlim(0, n + 1)
    for ax in (a1, a2, a3):
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.yaxis.label.set_color(INK2)
    for ax in (a1, a2):
        ax.tick_params(axis="x", length=0)
    footnote(fig, "Illustration with a made-up signal (70 valid frames, one component, k = 3); not EngageNet data. "
                  "Dashed lines: the frames each rule keeps.")
    fig.subplots_adjust(left=0.1, right=0.99, top=0.97, bottom=0.12)
    fig.savefig(OUT / "content-rules-compare.png", dpi=DPI)
    plt.close(fig)
    print("content-rules-compare: velocity peaks keep", list(frames[v_top]), np.round(smooth[v_top], 2).tolist(),
          "| k-BOCPD keeps", list(frames[b_top]), np.round(s[b_top], 2).tolist())


if __name__ == "__main__":
    prelim_macro_f1()
    prelim_vs_sme()
    class_balance()
    label_split()
    velocity_peaks()
    bocpd_score()
    velocity_steps()
    bocpd_run_length()
    content_rules_compare()
    print("written to", OUT)
