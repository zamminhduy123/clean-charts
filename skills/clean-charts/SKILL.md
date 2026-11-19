---
name: clean-charts
description: Draw clean, publication-ready benchmark and comparison charts in the style of AI model-launch posts (Google / DeepMind Gemini blogs, model cards) with Python + matplotlib - bar charts, stacked pass@k bars, cost-vs-quality lines, scatter with Pareto frontier, pie, doughnut, area, radar and slide layouts. Use whenever the user wants a chart that "looks like Google's", wants to recreate or clone a chart from a screenshot, or asks for clean model-vs-model benchmark charts (scores, cost per task, attack success rate, "higher is better") for a launch post, slide deck, paper or README - even if they never say "Google" but show a chart in that look (Google Sans, blue hero bars, grey competitors, value labels on top, methodology footer).
license: MIT
compatibility: Python 3 with matplotlib; fonttools only for the optional Google Sans install.
metadata:
  version: "1.0.0"
  repository: https://github.com/zamminhduy123/clean-charts
---

# Clean charts (model-launch style)

Google's launch charts look consistent because they follow a small, strict grammar. Learn the grammar, reuse the helpers in `scripts/gstyle.py`, start from the closest worked example in `examples/`, render, look at the PNG, fix, repeat.

## Setup (once per machine)

1. Check the font: `python3 -c "import matplotlib.font_manager as f; print(any(x.name=='Google Sans' for x in f.fontManager.ttflist))"`.
2. If `False`, tell the user you are installing Google Sans (OFL licence, from github.com/google/fonts) and run `python3 <skill>/scripts/install_font.py` (needs `fonttools`). It writes static Regular/Medium/Bold files, because matplotlib cannot select weights from a variable font.
3. A `findfont: Failed to find font weight 500` warning is harmless: it comes from the fallback fonts in the family list. Only investigate if the rendered text visibly is not Google Sans.

## Workflow

1. **Pick the archetype** (table below) and copy that example as the starting script. Import helpers with `sys.path.insert(0, "<skill>/scripts"); from gstyle import *`, then call `setup()`.
2. **Put data at the top** as a plain list or dict, so the user can edit numbers without touching drawing code.
3. **Render at `dpi=200`** to get crisp 2× PNGs, then **Read the PNG and inspect it**. Check for overlapping labels, clipped text, a title that collides with the legend, and the footer touching the axis labels. Fix and re-render; one or two passes are normal.
4. **When recreating a screenshot**, first read the image and measure pixel positions (title y, plot box, bar x/width, label rows). Build on a canvas of the same pixel size (`canvas(W, H)`) so the measurements transfer directly. Derive bar scale from two bars (px per unit) rather than guessing. Use printed values exactly, and estimate unlabeled segments from pixel heights, telling the user which numbers are estimates.
5. Report the script path, the PNG path, and what differs from the reference.

| Archetype | When | Start from |
|---|---|---|
| Outlined bars on axes | single metric, 4–10 models, "Score (%)" axis. **Most common.** | `examples/exploitgym.py` |
| Stacked k-attempt bars | pass@k / attack success at k=1,10,15; one bar = nested segments | `examples/gray_swan.py` |
| Cost vs. score lines | quality vs. price frontier, effort levels (Low/Med/High) | `examples/aa_index.py` |
| Slide with panels + horizontal bars | headline claim + 2 side-by-side metric cards | `examples/mka_eval.py` |
| Multi-panel rounded bars, no axes | 2–3 benchmarks side by side on one slide | `examples/deep_think.py` |
| Pie / doughnut / area / scatter / radar | shares, trends over a budget, cost-vs-quality points, capability profiles | `examples/more_types.py` (one function each) |

The last row has no Google reference: it applies the same grammar to new chart types. Its rules are a blue hero with grey others, white 3px gaps between slices, direct labels instead of legends where possible, the hero's number in the doughnut hole, only the hero area filled, a dashed `FAINT` Pareto frontier on scatter, and the hero drawn last on radar with a light fill. If the user supplies a real Google reference for one of these types, follow the reference over these rules.

Each `.py` has a matching `.png` to show what "done" looks like. Look at it before you start.

## The style grammar

**Color carries the story, not the vendor.** The model being launched ("ours") is blue and everything else is neutral grey, so the eye goes straight to the hero.
- Blues: `BLUE_DEEP` #2b52db for the flagship or top tier, `BLUE` #3d8ef8 for the main model, `BLUE_LIGHT` #a3d2fd for the smaller sibling. A single highlighted item on a slide uses `BLUE_HI` #1f57d6, applied to its label and value text too.
- Greys for competitors: `GREY_LIGHT` #e3e5e8 (borderless style), or for outlined bars `GREY_PALE` #eef1f5, `GREY_MID` #b3b8bf and `GREY_DARK` #6b6d72. Varying the greys separates vendors without using a hue.
- Only the older stacked-k style uses vendor hue families (`VENDOR_SHADES`), with dark→pale shades for k=1→k=max.
- Hatching (`hatch="//////"` with a dark-blue edge) means a variant such as "tools on". Explain it in a small legend pill.

**Typography** is Google Sans throughout, in sentence case, never all-caps.
- Title: Medium (500), centred. Subtitle on the line below in regular `INK2`/`MUTED`, written as `Metric • Setting • Higher is better` with a bullet `•` separator. On slides, a muted eyebrow line sits above a large Medium headline that states the claim ("X delivers frontier quality at much lower cost").
- Value labels sit above bars in `INK2`, with the format matching the source (`41%`, `51.26%`, or dollars with cents). On borderless slide bars they are Medium weight.
- Model names go under bars, wrapped onto two lines at the family/version split (`Gemini 4\nNeon`, `Claude\nOpus 5.5`), in `INK`. An optional third muted line carries the harness or setting (`Claude Code`, `6h`, `No time cap`).
- The footer reads `Methodology: deepmind.google/models/evals-methodology/<model>` (or the user's own source) in small `INK2`/`FAINT`. It is centred under axes charts and left-aligned on slides.

**Axes, when present:** keep only the left and bottom spines (dark, ~1px), with no tick marks. Add light horizontal gridlines (`GRID` #e8eaed) behind the data, `%` y tick labels, `Score (%)` as the y label, and a plain white background. `style_axes()` sets all of this.

**Marks:**
- Outlined bars: 1px `INK` edge, slightly rounded joins, a small gap (width ≈ 0.9 of the slot).
- Slide bars: borderless, rounded top and square bottom (`bar()`), on a `BG_SLIDE` #f8f9fb background.
- Horizontal bars inside a `PANEL` #f8f9fa rounded card: fully rounded (`hbar()`).
- Lines: about 2.8px, round markers with a thin dark edge, and effort labels above the hero series' points.

**Slides only:** a light background, rounded cards, small white "pill" tags (`pill()`). Leave out logos and brand marks: they are trademarks, and the chart reads as Google-style without them.

**Order:** usually descending by score with the hero first. When recreating, keep the source's order exactly, even when the hero is not the highest — that is a deliberate editorial choice in the original.

## Gotchas (each one cost a re-render)

- A dollar sign in labels triggers mathtext: two of them in one label (a price range) render as math with the signs dropped. `setup()` sets `text.parse_math=False`; keep it.
- `bar()` gets square bottoms by painting a mask in `bg` under the baseline. Pass the real background colour, or a stripe appears.
- Long tick labels plus a muted third line plus the footer compete for vertical space. Leave about 0.19 of the figure height under the axes and check the render.
- Matplotlib cannot use variable-font weights. Use the static files from `install_font.py`.

## Data honesty

These charts are often recreations of published results or drafts for a real launch. Never invent benchmark numbers. Use the values the user gives or that are printed on the reference image, and clearly flag any values estimated from pixel heights.
