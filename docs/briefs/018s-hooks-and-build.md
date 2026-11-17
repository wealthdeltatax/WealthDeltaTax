# 018: Hook resolution, data interface and the Data block

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 017s, 019s, 020w, 021s).
- **Read:** `docs/restructure/template.md` (sections 4, 6 and 6a), `docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md` (summary forms and reading rules), `docs/model-v3/inputs.md` (row format), and `pipeline/` file names. Nothing else need be opened.

## Goal
Design how a hook becomes a value at build time: the file the model writes, the resolver, draft and release builds, and the generated Data block with its CSV reference tables.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/hooks.md`. Cover: the output data file (a schema with one entry per output id holding p10, mean, p90 or a point, per schedule, horizon and `by` key, with unit and rounding set by the metric register); where it lives and who writes it (the v3 run script, built later); how `{{i:}}` reads the input register (a generated data file from `inputs.md`) and `{{lit:}}` reads the reference database; how `{{ref:}}` numbers figures; the draft build (unresolved hooks render as `[[...]]`) and the release build (fails on any unresolved hook); the Data block generator, row by row from template section 6; reference tables as HTML and CSV; run metadata (manifest version, country pack, run date). Give one worked example from hook to rendered value to Data block row. For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/hooks.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- The data file schema is complete enough to write a validator, and is stated for the three summary forms in `outputs.yml`.
- Every hook form of template section 4 has a resolution rule and an error case.
- The worked example round-trips: hook, data entry, rendered text, Data block row.
- Where the schema needs a field the manifest lacks, it is listed as a question.
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
