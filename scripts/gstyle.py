"""Helpers for Google / DeepMind-style benchmark charts (matplotlib).

Usage:
    import sys; sys.path.insert(0, "<skill>/scripts")
    from gstyle import *

Two ways to draw:
  * axes charts (bars / lines with real axes)  -> setup() then normal matplotlib + style_axes()
  * slide charts (panels, pills, free layout)  -> canvas(W, H) gives an axes in PIXEL coords
    (origin top-left, y down), then text()/rbox()/bar()/pill() with pixel sizes.
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle

# ---- palette (sampled from Google's published charts) ------------------------
INK, INK2, MUTED, FAINT = "#202124", "#3c4043", "#5f6368", "#9aa0a6"
GRID, DIVIDER = "#e8eaed", "#dadce0"
BG_WHITE, BG_SLIDE, PANEL = "#ffffff", "#f8f9fb", "#f8f9fa"

# Hero model ("ours") = blues; newest/flagship darkest-saturated.
BLUE_DEEP = "#2b52db"    # flagship / Deep Think
BLUE = "#3d8ef8"         # main Gemini model
BLUE_HI = "#1f57d6"      # single highlighted bar/text on slide charts
BLUE_LIGHT = "#a3d2fd"   # secondary / smaller Gemini model
# Competitors = neutral greys (newer style). Pick by rank/vendor, not meaning.
GREY_MID = "#b3b8bf"
GREY_LIGHT = "#e3e5e8"
GREY_PALE = "#eef1f5"    # use with a dark outline
GREY_DARK = "#6b6d72"
GREY_DARKER = "#45474a"
# Older multi-vendor style (stacked k-attempt bars): (dark, mid, pale) per vendor.
VENDOR_SHADES = {
    "gemini": ("#1a56c4", "#8ab4f8", "#d2e3fc"),
    "claude": ("#cf5a0c", "#f2c97d", "#fcebcb"),
    "gpt":    ("#0a7f4f", "#d6f5d2", "#f0fbec"),
    "other":  ("#ef5350", "#f9d3de", "#fdeef2"),
}

PT = 0.72  # 1 px = 0.72 pt when dpi=100 (canvas() uses dpi=100)


def has_google_sans():
    return any(f.name == "Google Sans" for f in fm.fontManager.ttflist)


def setup():
    """Global rcParams: Google Sans, no mathtext ($ is common in labels)."""
    if not has_google_sans():
        print("gstyle: Google Sans not found -> run scripts/install_font.py (falling back to Helvetica/Arial)")
    plt.rcParams.update({
        "font.family": ["Google Sans", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "text.parse_math": False,
        "hatch.linewidth": 0.9,
        "axes.edgecolor": INK,
        "text.color": INK,
    })


# ---- axes charts -------------------------------------------------------------
def style_axes(ax, ylabel="Score (%)", pct_ticks=True, grid=True):
    """Left+bottom dark spines, no tick marks, light horizontal grid behind data."""
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK)
        ax.spines[s].set_linewidth(1.1)
    ax.tick_params(length=0, labelsize=11, labelcolor=INK2, pad=8)
    if grid:
        ax.grid(axis="y", color=GRID, lw=1)
        ax.set_axisbelow(True)
    if pct_ticks:
        ax.yaxis.set_major_formatter(lambda v, _: f"{v:g}%")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=INK, labelpad=10)


def header(fig, title, subtitle=None, y=0.93, x=0.5):
    """Centered title (medium) + muted subtitle like 'Pass@1 • Higher is better'."""
    fig.text(x, y, title, ha="center", va="center", fontsize=17, weight=500, color=INK)
    if subtitle:
        fig.text(x, y - 0.045, subtitle, ha="center", va="center", fontsize=13, color=INK2)


def footer(fig, text="Methodology: deepmind.google/models/evals-methodology/<model>", y=0.035, x=0.5, ha="center"):
    fig.text(x, y, text, ha=ha, va="center", fontsize=8.5, color=INK2)


def value_labels(ax, xs, tops, labels, pad=1.0, size=12.5):
    """Value above each bar (pad in data units)."""
    for x, t, s in zip(xs, tops, labels):
        ax.text(x, t + pad, s, ha="center", va="bottom", fontsize=size, color=INK2)


# ---- pixel canvas (slide charts) ---------------------------------------------
def canvas(W=1200, H=675, bg=BG_WHITE):
    """Figure W x H px with an axes in pixel coords (0,0 top-left). Save with dpi=200 for 2x."""
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=bg)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
    return fig, ax


def text(ax, x, y, s, px, color=INK, ha="center", va="center", **kw):
    """Text with size in pixels (cap+descender height ~ px)."""
    return ax.text(x, y, s, fontsize=px * PT, color=color, ha=ha, va=va, **kw)


def rbox(ax, x, y, w, h, r, fc, **kw):
    """Rounded rectangle; (x, y) = top-left in pixel coords."""
    r = min(r, w / 2, h / 2)
    p = FancyBboxPatch((x + r, y + r), max(w - 2 * r, 1e-6), max(h - 2 * r, 1e-6), fc=fc,
                       boxstyle=f"round,pad={r},rounding_size={r}", **kw)
    ax.add_patch(p)
    return p


def bar(ax, x, base, w, h, fc, r=5, bg=BG_WHITE, outline=None, hatch=None):
    """Vertical bar with rounded TOP corners, square bottom, in pixel coords.
    Draws past the baseline then masks with `bg`, so `bg` must match the area under the baseline."""
    rbox(ax, x, base - h, w, h + r + 2, r, fc, lw=0, hatch=hatch, ec=outline or fc, zorder=2)
    if outline:
        rbox(ax, x, base - h, w, h + r + 2, r, "none", ec=outline, lw=1, zorder=2)
    ax.add_patch(Rectangle((x - 2, base), w + 4, r + 4, fc=bg, lw=0, zorder=3))


def hbar(ax, x, cy, w, h, fc, r=4):
    """Horizontal fully-rounded bar starting at x, vertically centred on cy."""
    rbox(ax, x, cy - h / 2, w, h, r, fc, lw=0)


def pill(ax, cx, cy, w, label=None, h=22, px=9.5):
    """Small white rounded tag with hairline border, e.g. 'Tools off'."""
    rbox(ax, cx - w / 2, cy - h / 2, w, h, 6, "white", ec=DIVIDER, lw=0.8)
    if label:
        text(ax, cx, cy + 0.5, label, px)

