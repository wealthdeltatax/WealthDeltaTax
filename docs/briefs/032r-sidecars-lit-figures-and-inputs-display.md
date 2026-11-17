# 032: Research: sidecar data for literature figures and input display (site.md B12)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none
- **Read:** `docs/restructure/site/hooks.md` sections 4.3, 4.5, 11 (questions 8 and 9) and 10; `docs/model-v3/inputs.md` (row format; every row's unit and Low, Central, High cells); `registry/references.bib` and `registry/references.json` (keys only); `docs/agents/research.md` and `docs/agents/reference/research/`.

## Goal
Provide the two data files the hook resolver needs and the register does not hold: the published figures that spokes quote from the literature, and a display unit and decimals for every register row.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap.

## Design
1. `registry/inputs-display.yml`: one entry for each of the 269 register rows: `id`, `unit` (a unit tag from `outputs.yml` `unit_tags` or a new tag proposed in the file), `decimals`, `display_unit` text (for example "% of GDP"), and `scale` if the value must be multiplied for display. Derive from the row's own unit text; flag rows whose unit is ambiguous in a `note`.
2. `registry/lit-figures.yml`: entries `<bibkey>:<slug>` with `value`, `unit`, `quoted_as` (the exact figure in the source), `page` or `table`, and `access_date`, for published numbers the old papers quote (ledger rows flagged `Y` or `P` with a literature source, and every register row whose source is a published study). Candidates come from `docs/restructure/ledger-sections.md` and `inputs.md`. The bib key must exist in `registry/references.bib`; where it does not, list the missing keys in the file's header comment and do not invent them. Only figures actually used; the author is reworking the references to exactly what is used.
3. A check script run with `python -I`: every `inputs-display.yml` id is in the register and vice versa; every `lit-figures.yml` bib key exists.

## Touches
`registry/lit-figures.yml` (new), `registry/inputs-display.yml` (new), this brief's progress block. Nothing in `docs/model-v3/inputs.md`, `registry/references.bib`, `source/`, `pipeline/`.

## Acceptance criteria
- `inputs-display.yml` covers all 269 rows with a unit tag and decimals; ambiguous rows are noted.
- Every `lit-figures.yml` entry cites a held source with the figure as quoted; none is from memory.
- The check script passes.
- `git diff --stat` shows only the Touches list.

## Checks to run
The check script; re-read five `quoted_as` figures against their sources.

## Out of scope
Choosing values, editing the register or the bibliography, the resolver.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
