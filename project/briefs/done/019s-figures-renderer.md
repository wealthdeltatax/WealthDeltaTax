# 019: Figure renderer and visual system

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 017s, 018s, 020w, 021s).
- **Read:** `docs/restructure/template.md` section 6a, `docs/model-v3/outputs.yml` (the `kind:` and `by:` values), and the `dataviz` skill guidance. Nothing else need be opened.

## Goal
Design how a figure block becomes a chart and its reference table, with one visual system across the series.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/figures.md`. Cover: the renderer choice and why (static SVG at build, or a chart library), kept light on the page; one palette and style for light and dark; how each `kind` (line, band, bar, dot, map, stack) is drawn; how a `p10_mean_p90` output draws the mean with a p10 to p90 band; how several schedules are drawn together; units and axis labels taken from the metric register; alt text and keyboard access; print and PDF output; the reference table beside each figure and its CSV; and a test list (one fixture per kind, drawn from fake data). For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/figures.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- Every `kind` in `outputs.yml` has a drawing rule.
- The rule for uncertainty bands and for the three schedules is stated and shown on a fixture description.
- The table and CSV come from the same data as the drawing, and the document says how that is guaranteed.
- Accessibility and print are covered.
- `git diff --stat` shows only the Touches list.

## Out of scope
Building the pipeline, writing spoke or hub prose, editing `template.md`, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/restructure/site/figures.md` written (renderer choice, palette and style, one-data-path guarantee, rules for six kinds, bands and three schedules, units, alt and keyboard, print, test list, 8 questions with proposed answers).
- **Next:** the guru merges the sibling files into `docs/restructure/site.md`.
- **State:** done; Q1 to Q8 answered by the author 2026-11-17, all as proposed; brief 019 merged, ready to retire
<!-- progress:end -->

Change report
- Task: brief 019s, figure renderer and visual system
- Files changed: `docs/restructure/site/figures.md` (new, the design); `docs/briefs/019s-figures-renderer.md` (this block)
- What is different now: a design for static-SVG figures at build with one shared stylesheet and script; one `FigureData` object feeding drawing, table and CSV with a build self-check; fixed drawing rules for line, band, bar, dot, stack and map; a default drawing kind for each manifest role (seven on `main`, three proposed); the interval rule for the three schedules; units, accessibility, print and a 12-fixture test list
- New or changed interfaces: none (design only); proposes `registry/figure-style.yml`, `/data/csv/<table id>.csv`, `/data/fig/<figure id>.svg`, and four optional figure-block fields (Q2)
- Acceptance criteria: every `kind` in `outputs.yml` has a drawing rule, met (section 6; seven values checked by grep against the file); band and three-schedule rule stated with a fixture description, met (sections 5.2, 5.3); table and CSV from the same data with the guarantee stated, met (section 4); accessibility and print covered, met (sections 8, 9); `git diff --stat` only the Touches list, met (see Verification)
- Deviations from the brief: the change report is pasted into Implementation notes outside the progress block, inside this brief file
- Risks / follow-ups: Q1 to Q8 need the author; the palette was validated against the `dataviz` default surfaces, not the site's real background (theme files not opened); the Quarto dark-mode selector is unconfirmed; the manifest's two meanings of `kind` and OP4's two units are manifest issues for the guru; nothing was rendered
- Verification: `validate_palette.js` run four times (ordinal light and dark, eight categorical slots light and dark, all pass); `kind` and `by` values in `docs/model-v3/outputs.yml` compared with section 6 by grep. Not run: any build, since nothing in `pipeline/`, `site/` or `registry/` changed
- Overview sections likely needing an update: none until the author answers
- Commit / branch: branch `brief/019-figures-renderer`; merged to `main` after the author answered Q1 to Q8
