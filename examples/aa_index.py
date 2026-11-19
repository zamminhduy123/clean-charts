import matplotlib.pyplot as plt

# name: (color, [(cost, score), ...])  — drawn in this order (later on top)
series = {
    "Claude Opus 5.5": ("#45474a", [(0.93, 35.1), (2.41, 48.1), (3.43, 52.1), (4.65, 54.1), (6.03, 57.1), (10.0, 59.1)]),
    "GPT-6.2 Sol":     ("#b3b8bf", [(0.12, 40.0), (0.35, 53.2), (0.5, 55.2), (0.6, 56.1), (0.95, 57.1)]),
    "Gemini 4 Carbon": ("#a8d1f7", [(4.65, 54.1), (5.2, 58.2), (7.75, 60.2)]),
    "Gemini 4 Neon":   ("#3b8bf0", [(0.69, 44.1), (1.86, 55.0), (3.7, 60.2), (6.42, 61.1)]),
}
legend_order = ["Gemini 4 Neon", "Gemini 4 Carbon", "Claude Opus 5.5", "GPT-6.2 Sol"]

plt.rcParams["font.family"] = ["Google Sans", "Helvetica Neue", "Arial", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(16.4, 10.4), dpi=100)
fig.subplots_adjust(left=0.11, right=0.81, top=0.745, bottom=0.165)

for name, (c, pts) in series.items():
    x, y = zip(*pts)
    ax.plot(x, y, color=c, lw=2.8, marker="o", ms=11, mfc=c, mec="#202124",
            mew=1.2, label=name, zorder=3, clip_on=False)

for label, (x, y) in zip(["Low", "Med", "High", "Xhigh"], series["Gemini 4 Neon"][1]):
    ax.annotate(label, (x, y), xytext=(0, 12), textcoords="offset points",
                ha="center", va="bottom", fontsize=14, color="#202124")

ax.set_xlim(0, 10)
ax.set_ylim(0, 70)
ax.set_xticks(range(0, 11, 2))
ax.set_yticks(range(0, 71, 10))
ax.margins(0)
ax.tick_params(length=0, labelsize=16, labelcolor="#3c4043", pad=12)
ax.grid(axis="y", color="#e8eaed", lw=1.2, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#202124")
    ax.spines[s].set_linewidth(1.3)
ax.set_xlabel("Cost per task ($)", fontsize=20, weight=500, labelpad=6, color="#202124")
ax.set_ylabel("AA Intelligence Index", fontsize=20, weight=500, labelpad=14, color="#202124")

leg = fig.legend([plt.Line2D([], [], ls="", marker="o", ms=19, color=series[n][0]) for n in legend_order],
                 legend_order, loc="center", bbox_to_anchor=(0.435, 0.825), ncol=4,
                 frameon=False, fontsize=18, handletextpad=0.4, columnspacing=1.4)

fig.text(0.435, 0.878, "AA Index v5.0.1", ha="center", fontsize=23, weight=500, color="#202124")
fig.text(0.435, 0.04, "Methodology: deepmind.google/models/evals-methodology/gemini-4-neon",
         ha="center", fontsize=13, color="#3c4043")

fig.savefig("aa_index.png", facecolor="white")
