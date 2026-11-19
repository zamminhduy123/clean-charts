import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# (name, k1, k10, k15, palette)
data = [
    ("Gemini 4 Neon",     0.0, 0.0, 0.0,  "blue"),
    ("Gemini 4 Carbon",   0.0, 0.0, 0.0,  "blue"),
    ("Gemini 4 Hydrogen", 0.0, 0.0, 0.0,  "blue"),
    ("Gemini 4 Argon",    0.5, 0.6, 0.7,  "blue"),
    ("Claude Opus 5.5",   0.2, 0.7, 1.0,  "orange"),
    ("GPT-6.2 Sol",       0.2, 1.6, 2.3,  "green"),
    ("GPT-6.2 Astra",     0.2, 1.8, 2.4,  "green"),
    ("Claude Sonnet 5.5", 0.3, 2.7, 3.4,  "orange"),
    ("Claude Fable 5.2",  0.3, 2.9, 4.1,  "orange"),
    ("Muse Spark 1.3",    1.4, 5.9, 6.8,  "red"),
    ("GPT-6.1 Terra",     1.0, 6.3, 7.3,  "green"),
    ("GPT-6 Luna",        5.5, 25.0, 28.7, "green"),
]
# (k1, k10, k15) shades
pal = {
    "blue":   ("#1a56c4", "#8ab4f8", "#d2e3fc"),
    "orange": ("#cf5a0c", "#f2c97d", "#fcebcb"),
    "green":  ("#0a7f4f", "#d6f5d2", "#f0fbec"),
    "red":    ("#ef5350", "#f9d3de", "#fdeef2"),
}

plt.rcParams["font.family"] = ["Google Sans", "Helvetica Neue", "Arial", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(20, 9.6), dpi=100)
fig.subplots_adjust(left=0.12, right=0.89, top=0.78, bottom=0.25)

w = 0.62
for i, (name, k1, k10, k15, p) in enumerate(data):
    c1, c10, c15 = pal[p]
    x = i - w / 2
    if k15 == 0:  # zero bars: thin colored line
        ax.plot([x, x + w], [0.03, 0.03], color=c1, lw=3, solid_capstyle="round", zorder=3)
    else:
        for lo, hi, c in [(0, k1, c1), (k1, k10, c10), (k10, k15, c15)]:
            ax.add_patch(Rectangle((x, lo), w, hi - lo, color=c, lw=0, zorder=2))
        ax.add_patch(Rectangle((x, 0), w, k15, fill=False, ec="#3c4043", lw=1.3, zorder=3))
    ax.text(i, k15 + 0.6, f"{k15:.1f}%", ha="center", va="bottom", fontsize=17, color="#3c4043")

# star above best model
ax.plot(0, 4.6, marker=(4, 1, 0), ms=26, color="black", zorder=4)

ax.set_xlim(-0.55, len(data) - 0.45)
ax.set_ylim(0, 30.5)
ax.set_yticks([0, 10, 20, 30])
ax.tick_params(axis="y", length=0, labelsize=13, labelcolor="#5f6368", pad=10)
ax.tick_params(axis="x", length=0, pad=8)
ax.set_xticks(range(len(data)))
ax.set_xticklabels([d[0] for d in data], rotation=45, ha="right",
                   rotation_mode="anchor", fontsize=16, color="#202124")
ax.set_ylabel("Score (%)", fontsize=15, labelpad=18)
ax.grid(axis="y", color="#e8eaed", lw=1, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color("#3c4043")
ax.spines["bottom"].set_color("#3c4043")
ax.spines["left"].set_bounds(0, 35)
ax.set_ylim(0, 35)
ax.set_yticks([0, 10, 20, 30])

# legend (dots)
for x, c, lbl in [(0.42, "#202124", "K= 1"), (0.47, "#9aa0a6", "K= 10"), (0.522, "#e8eaed", "K= 15")]:
    fig.text(x, 0.725, "●", color=c, fontsize=32, ha="center", va="center")
    fig.text(x + 0.012, 0.727, lbl, fontsize=13, va="center", color="#202124")

fig.text(0.49, 0.865, "Gray Swan IPI", ha="center", fontsize=24, color="#202124")
fig.text(0.49, 0.825, "Attack success rate at k attempts • The number above each bar is "
         "attack success rate for k=15 attempts", ha="center", fontsize=17, color="#3c4043")
fig.text(0.49, 0.79, "Lower is better", ha="center", fontsize=15, weight="bold", color="#3c4043")
fig.text(0.49, 0.025, "Methodology: deepmind.google/models/evals-methodology/gemini-4-neon",
         ha="center", fontsize=12, color="#3c4043")

fig.savefig("gray_swan_ipi.png", facecolor="white")
