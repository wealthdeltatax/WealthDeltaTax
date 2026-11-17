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
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
