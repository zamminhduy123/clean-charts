import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

W, H = 1200, 675          # canvas in pixels; all coordinates below are pixels from top-left
PT = 0.72                 # 1 px = 0.72 pt at dpi=100
BLUE, GREY, INK, MUTED = "#1f57d6", "#dfe1e5", "#202124", "#5f6368"

models = ["Gemini 4 Carbon", "Claude Fable 5.2", "Claude Opus 5.5", "GPT-6 Astra"]
panels = [  # (panel x, title, subtitle, values, px per unit, value format)
    (62,  "Quality",       "Climb WSR · higher is better", [54.3, 56.6, 53.0, 50.2],     4.245, "{:.1f}%"),
    (615, "Cost per task", "USD · lower is better",        [5.63, 35.28, 10.29, 6.15],  6.35,  "${:.2f}"),
]

plt.rcParams["text.parse_math"] = False
plt.rcParams["font.family"] = ["Google Sans", "Helvetica Neue", "Arial", "DejaVu Sans"]
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")

def text(x, y, s, px, color=INK, **kw):
    ax.text(x, y, s, fontsize=px * PT, color=color, va="center", **kw)

def rbox(x, y, w, h, r, color):
    ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r, color=color, lw=0,
                                boxstyle=f"round,pad={r},rounding_size={r}"))

text(600, 40, "Multimodal Knowledge Agent (MKA) Eval", 25, ha="center")
text(600, 81, "Gemini 4 Carbon delivers frontier quality at much lower cost", 37,
     ha="center", weight=500)

for px0, title, sub, vals, scale, fmt in panels:
    rbox(px0, 233, 524, 283, 18, "#f8f9fa")
    text(px0 + 28, 271, title, 22)
    text(px0 + 28, 295, sub, 12.5, MUTED)
    bar_x = px0 + 170
    for i, (name, v) in enumerate(zip(models, vals)):
        y = 334 + 42 * i
        c, tc = (BLUE, BLUE) if i == 0 else (GREY, INK)
        text(px0 + 28, y, name, 15, tc)
        w = v * scale
        rbox(bar_x, y - 12.5, w, 25, 4, c)
        text(bar_x + w + 9, y, fmt.format(v), 15, tc)

text(600, 647, "Methodology: MKA split from Artificial Analysis. Stirrup harness. Score is Climb WSR. "
     "All models at standard list price, including Gemini 4 Carbon at $4 / $20 per 1M tokens.",
     10.5, "#9aa0a6", ha="center")


fig.savefig("mka_eval.png", dpi=200, facecolor="white")
