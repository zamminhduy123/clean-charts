# Pie, doughnut, area, scatter, radar in the Google launch-chart grammar.
# No Google reference exists for these types: they apply the same rules
# (blue hero / grey others, Google Sans, direct labels instead of legends,
# muted subtitle, methodology footer). All data below is ILLUSTRATIVE.
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import numpy as np
import matplotlib.pyplot as plt
from gstyle import *

setup()
OUT = os.path.dirname(os.path.abspath(__file__))
FOOT = "Illustrative data • Methodology: example.com/evals"
HERO = "Gemini 4 Neon"
OTHERS_GREYS = [GREY_MID, GREY_DARK, GREY_LIGHT, GREY_DARKER]


def new_fig(title, subtitle, polar=False):
    fig = plt.figure(figsize=(9, 6.75), dpi=100)
    ax = fig.add_axes([0.1, 0.17, 0.8, 0.62], polar=polar)
    header(fig, title, subtitle, y=0.93)
    footer(fig, FOOT, y=0.035)
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=200, facecolor="white")
    plt.close(fig)


# ---- pie: hero slice blue, rest greys, white gaps, direct labels (no legend) ----
def pie():
    names = [HERO, "Claude Opus 5.5", "GPT-6.2 Sol", "Other"]
    vals = [42, 27, 21, 10]
    colors = [BLUE] + OTHERS_GREYS[:3]
    fig, ax = new_fig("Win share in head-to-head tasks", "Share of 1,200 tasks • Higher is better")
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(edgecolor="white", linewidth=3))
    for w, n, v in zip(wedges, names, vals):
        a = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = 1.18 * np.cos(a), 1.18 * np.sin(a)
        ha = "left" if x > 0 else "right"
        c = BLUE_HI if n == HERO else INK
        ax.text(x, y + 0.06, f"{v}%", ha=ha, va="center", fontsize=15, weight=500, color=c)
        ax.text(x, y - 0.08, n, ha=ha, va="center", fontsize=11, color=c if n == HERO else INK2)
    ax.set_aspect("equal")
    save(fig, "pie.png")


# ---- doughnut: same, plus the hero number in the hole ----
def doughnut():
    names = [HERO, "Claude Opus 5.5", "GPT-6.2 Sol", "Other"]
    vals = [42, 27, 21, 10]
    colors = [BLUE] + OTHERS_GREYS[:3]
    fig, ax = new_fig("Win share in head-to-head tasks", "Share of 1,200 tasks • Higher is better")
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.32, edgecolor="white", linewidth=3))
    ax.text(0, 0.07, "42%", ha="center", va="center", fontsize=34, weight=500, color=BLUE_HI)
    ax.text(0, -0.17, HERO, ha="center", va="center", fontsize=12, color=INK2)
    for w, n, v in list(zip(wedges, names, vals))[1:]:
        a = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = 1.15 * np.cos(a), 1.15 * np.sin(a)
        ha = "left" if x > 0 else "right"
        ax.text(x, y, f"{n}  {v}%", ha=ha, va="center", fontsize=11, color=INK2)
    ax.set_aspect("equal")
    save(fig, "doughnut.png")


# ---- area: hero filled blue, others grey lines; labels at line ends ----
def area():
    x = np.arange(0, 13)
    series = {HERO: 30 + 32 * (1 - np.exp(-x / 4)),
              "Claude Opus 5.5": 28 + 26 * (1 - np.exp(-x / 5)),
              "GPT-6.2 Sol": 25 + 24 * (1 - np.exp(-x / 6))}
    fig, ax = new_fig("Accuracy vs. thinking budget", "Pass@1 • Higher is better")
    for (n, y), c in zip(reversed(series.items()), [GREY_MID, GREY_DARK, BLUE]):
        hero = n == HERO
        ax.fill_between(x, y, color=c, alpha=0.18 if hero else 0.0, lw=0, zorder=1)
        ax.plot(x, y, color=c, lw=2.8 if hero else 2.2, zorder=3, solid_capstyle="round")
        ax.text(x[-1] + 0.25, y[-1], n, va="center", fontsize=11, weight=500 if hero else 400,
                color=BLUE_HI if hero else INK2)
    ax.set_xlim(0, 12); ax.set_ylim(0, 70)
    ax.set_xticks(range(0, 13, 2), [f"{v}k" for v in range(0, 13, 2)])
    style_axes(ax)
    ax.set_xlabel("Thinking tokens", fontsize=11, color=INK, labelpad=8)
    ax.set_position([0.1, 0.17, 0.66, 0.62])  # room for end labels
    save(fig, "area.png")


# ---- scatter: cost vs score, hero blue, direct labels, dashed frontier ----
def scatter():
    pts = [(HERO, 1.8, 61), ("Gemini 4 Carbon", 0.6, 55), ("Claude Opus 5.5", 6.0, 59),
           ("GPT-6.2 Sol", 3.4, 57), ("Muse Wonder", 2.6, 48), ("DeepSeek-V4.1", 0.4, 46)]
    fig, ax = new_fig("Quality vs. cost", "AA Intelligence Index • Up and to the left is better")
    for n, c, s in pts:
        gem = n.startswith("Gemini")
        col = (BLUE if n == HERO else BLUE_LIGHT) if gem else GREY_MID
        ax.scatter(c, s, s=140, color=col, edgecolor=INK, linewidth=1, zorder=3)
        ax.annotate(n, (c, s), xytext=(10, 0), textcoords="offset points", va="center",
                    fontsize=11, weight=500 if n == HERO else 400, color=BLUE_HI if n == HERO else INK2)
    front = sorted([(c, s) for _, c, s in pts])
    best, fx, fy = -1, [], []
    for c, s in front:  # Pareto frontier: points that beat everything cheaper
        if s > best:
            best = s; fx.append(c); fy.append(s)
    ax.plot(fx, fy, ls=(0, (4, 3)), color=FAINT, lw=1.3, zorder=2)
    ax.set_xlim(0, 7); ax.set_ylim(40, 65)
    style_axes(ax, ylabel="AA Intelligence Index", pct_ticks=False)
    ax.grid(axis="x", color=GRID, lw=1)
    ax.xaxis.set_major_formatter(lambda v, _: f"${v:g}")
    ax.set_xlabel("Cost per task", fontsize=11, color=INK, labelpad=8)
    save(fig, "scatter.png")


# ---- radar: hero blue line + light fill on top, others grey outlines ----
def radar():
    axes_ = ["Coding", "Math", "Science", "Agents", "Vision", "Long context"]
    data = {"GPT-6.2 Sol": [74, 80, 78, 60, 66, 58],
            "Claude Opus 5.5": [80, 72, 75, 70, 60, 64],
            HERO: [78, 84, 82, 72, 80, 76]}
    ang = np.linspace(0, 2 * np.pi, len(axes_), endpoint=False)
    fig, ax = new_fig("Capability profile", "Normalised score per domain • Higher is better", polar=True)
    ax.set_position([0.25, 0.13, 0.5, 0.58])
    ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
    for (n, v), c in zip(data.items(), [GREY_MID, GREY_DARK, BLUE]):
        hero = n == HERO
        a, r = np.r_[ang, ang[0]], np.r_[v, v[0]]
        if hero:
            ax.fill(a, r, color=BLUE, alpha=0.15, zorder=2)
        ax.plot(a, r, color=c, lw=2.8 if hero else 2, zorder=3)
        ax.plot(ang, v, "o", ms=6, color=c, mec=INK, mew=0.8, zorder=4)
    ax.set_ylim(0, 100)
    ax.set_xticks(ang, axes_, fontsize=11.5, weight=500, color=INK)
    ax.set_yticks([25, 50, 75, 100], ["", "", "", ""])
    ax.grid(color=GRID, lw=1)
    ax.spines["polar"].set_color(DIVIDER)
    ax.tick_params(pad=10)
    for i, (n, c) in enumerate(zip(reversed(list(data)), [BLUE, GREY_DARK, GREY_MID])):
        fig.text(0.36 + i * 0.2 - (0.04 if i == 0 else 0), 0.825, "●", color=c, fontsize=16, ha="right", va="center")
        fig.text(0.365 + i * 0.2 - (0.04 if i == 0 else 0), 0.825, n, fontsize=11, va="center", color=INK)
    save(fig, "radar.png")


for f in (pie, doughnut, area, scatter, radar):
    f()
