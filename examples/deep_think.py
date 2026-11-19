import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

W, H = 1414, 804          # canvas in pixels; coordinates are pixels from top-left
PT = 0.72                 # 1 px = 0.72 pt at dpi=100
BG, INK, MUTED = "#f8f9fb", "#202124", "#80868b"
C = {"dt": "#2b52db", "pro": "#3d8ef8", "25": "#a3d2fd", "other": "#e3e5e8"}
BASE, BW, PITCH = 622, 62, 68

models = ["Gemini\n3 Deep Think", "Gemini\n3 Pro", "Gemini\n2.5 Pro", "Claude Sonnet\n4.5", "GPT-5\nPro", "GPT-5.1"]
colors = ["dt", "pro", "25", "other", "other", "other"]
panels = [  # (bar start x, title, subtitle, labels, values, px per %, hatched first bar)
    (40,  "Humanity’s Last Exam", "Reasoning & knowledge",   ["41%", "37.5%", "21.6%", "13.7%", "30.7%", "26.5%"], 5.97, False),
    (506, "GPQA Diamond",         "Scientific knowledge",    ["93.8%", "91.9%", "86.4%", "83.4%", "88.4%", "88.1%"], 2.96, False),
    (962, "ARC-AGI-2",            "Visual reasoning puzzles", ["45.1%", "31.1%", "4.9%", "13.6%", "15.8%", "17.6%"], 6.28, True),
]

plt.rcParams.update({"text.parse_math": False, "hatch.linewidth": 0.9,
                     "font.family": ["Google Sans", "Helvetica Neue", "DejaVu Sans"]})
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")

def text(x, y, s, px, color=INK, **kw):
    ax.text(x, y, s, fontsize=px * PT, color=color, va="center", ha=kw.pop("ha", "center"), **kw)

def rbox(x, y, w, h, r, fc, **kw):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r, fc=fc,
                                boxstyle=f"round,pad={r},rounding_size={r}", **kw))

def pill(cx, cy, w):
    rbox(cx - w / 2, cy - 11, w, 22, 6, "white", ec="#dadce0", lw=0.8)

text(707, 101, "Gemini 3 Deep Think", 37, weight=500)

for x0, title, sub, labels, scale, hatched in panels:
    cx = x0 + (5 * PITCH + BW) / 2
    text(cx, 218, title, 24, weight=500)
    text(cx, 244, sub, 17.5, MUTED)
    if hatched:  # legend pill: solid swatch + hatched swatch
        pill(cx, 274, 148)
        rbox(cx - 66, 269, 18, 11, 2, INK, lw=0)
        text(cx - 44, 274.5, "Tools off", 9.5, ha="left")
        rbox(cx + 6, 269, 18, 11, 0.1, "none", ec=INK, lw=0, hatch="//////")
        text(cx + 28, 274.5, "Tools on", 9.5, ha="left")
    else:
        pill(cx, 273, 55)
        text(cx, 273.5, "Tools off", 9.5)

    for i, (name, lab, c) in enumerate(zip(models, labels, colors)):
        x, h = x0 + i * PITCH, float(lab[:-1]) * scale
        if hatched and i == 0:  # light fill + dark diagonal hatch
            rbox(x, BASE - h, BW, h + 8, 5, "#8d9ef2", ec=C["dt"], lw=0, hatch="//////")
            rbox(x, BASE - h, BW, h + 8, 5, "none", ec=C["dt"], lw=1)
        else:
            rbox(x, BASE - h, BW, h + 8, 5, C[c], lw=0)
        text(x + BW / 2, BASE - h - 17, lab, 15.5, weight=500)
        ax.text(x + BW / 2, 630, name, fontsize=11.2 * PT, color=INK, ha="center", va="top", linespacing=1.15)
    ax.add_patch(Rectangle((x0 - 2, BASE), 6 * PITCH, 10, fc=BG, lw=0, zorder=5))  # square bar bottoms

ax.plot([40, 1366], [701, 701], color="#dadce0", lw=1)
text(42, 750, "Methodology: deepmind.google/models/evals-methodology/gemini-3-pro", 14.5, MUTED, ha="left")


fig.savefig("deep_think.png", dpi=200, facecolor=BG)
