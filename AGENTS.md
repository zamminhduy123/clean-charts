# AGENTS.md

Instructions for coding agents working on this repository (not for using the skill — see `skills/clean-charts/SKILL.md`).

## Commands
- Render every example (checks nothing is broken): `cd skills/clean-charts/examples && for f in *.py; do python3 "$f"; done`
- Validate plugin + marketplace manifests: `claude plugin validate ./`
- Downsize example PNGs before committing (keeps the repo small): `sips -Z 1400 skills/clean-charts/examples/*.png` (macOS) or `mogrify -resize 1400x1400 ...`

## Rules
- Keep `SKILL.md` under 500 lines; frontmatter `name` must stay `clean-charts` (matches its folder, Agent Skills spec).
- New chart type → add one example script + its PNG, a row in the SKILL.md archetype table, and a gallery cell in README.md.
- Shared drawing code goes in `scripts/gstyle.py`; examples import it via `sys.path`.
- No logos, brand marks or bundled font files. Never invent benchmark numbers in examples; mark illustrative data as such.
- Bump `version` in `.claude-plugin/plugin.json` and SKILL.md `metadata.version` together.
