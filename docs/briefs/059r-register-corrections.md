# 059: Apply the register corrections found by the source check (043r)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (043r is merged)
- **Read:** `docs/model-v3/source-map.md` section 3 (the 12 discrepancies) and section 2; `docs/model-v3/inputs.md` rows I-D6c, I-D6j, I-M6l, I-D4d, I-D4e, I-D5a to I-D5d, I-D10a, I-D10b, I-M5a to I-M5c, I-M8b, I-D6a and the rows citing S23 and S38; `registry/inputs-display.yml` and `registry/lit-figures.yml` for the same ids; `pipeline/build_inputs.py` (how `registry/inputs.json` is made); `docs/model-v3/drivers.md` D6.

## Goal
The register agrees with the held sources: the wrong figures are corrected, the page notes are exact, and every correction is visible in one list, with no other row touched.

## Decisions (author, 2026-11-18)
- **S22 (discrepancy 1):** the central workers' share of corporation tax is **51%**, as the held ifo WP 241 says (PDF pp. 5, 6, 19; "about half" p. 3). The 40% was the capital share. Rows I-D6c and I-D6j change accordingly; the owners and consumers shares, the variants and the low and high are re-derived by the row's own rule and shown.
- **S37 (discrepancy 2):** I-M6l's figures (11, 35, 45) are replaced with the figures in the held OxREP article by Advani, Hughson and Summers: mean effective rate 42% against a 47% headline for £3m or more of income, and almost a quarter of that group paying no more than 12% (PDF p. 3, and whatever else the article prints for the same group). The row's name, band and unit are rechecked against what the article measures; if the article's measure differs from the row's label, relabel the row and say so.
- Discrepancies 3 to 7, 9 and 10 are applied as the section says (page numbers to the held copy, with printed page and the version note; S16 magnitude note; S24 title; S30 page; S23 now checkable; S38 note that the held file is the full report).
- **Not in this brief:** `Hasen2017` and the reference list (the author's later rework); discrepancies 11 and 12 (no change needed).

## Design
1. Apply the S22 and S37 changes to `docs/model-v3/inputs.md` (value, low, high, note, source cell), then the other register edits; keep the `(J)` flags as they are unless a change makes a row derived or observed (say which).
2. Regenerate `registry/inputs.json` with `pipeline/build_inputs.py`; update `registry/inputs-display.yml` and `registry/lit-figures.yml` for every row changed (page, value, `verified`).
3. In `source-map.md` section 3, mark each of the 12 items `applied`, `no change` or `author` with the commit's row ids; add a section 6 listing every row edited, old value and new value.
4. Find what else depends on the two corrected values (grep `40%`, `I-D6c`, `I-D6j`, `I-M6l` in `docs/model-v3/`, `docs/restructure/` and `registry/`): list them in the change report; do not edit them (the guru decides which need a rerun, for example the tornado).

## Touches
`docs/model-v3/inputs.md`, `registry/inputs.json` (regenerated), `registry/inputs-display.yml`, `registry/lit-figures.yml`, `docs/model-v3/source-map.md`, this brief's progress block.

## Acceptance criteria
- The register still has 274 rows and the same (J) count except where a change is reported; `python pipeline/build_inputs.py` exits 0 and `registry/inputs.json` matches `inputs.md` (script check).
- I-D6c, I-D6j: the arithmetic of the 51% split is shown in the note and re-derives the stated low, central and high.
- I-M6l's figures each match the held article's text by page (script pattern check as in 043r).
- `pytest tests/data -q` and `pytest tests/gate -q` pass (separate commands); `python -I` load of `lit-figures.yml` returns all entries.
- Every edit appears in section 6 of `source-map.md`; `git diff --stat` is limited to the Touches list.

## Checks to run
The commands above. Skip the site build (no site file touched).

## Out of scope
Any figure from memory (read the held PDFs only); `references.bib`; the model, the tornado, drivers.md; new sources.

## Open questions
Ask, do not guess: if the S37 article cannot support any figure for the row's measure, mark the row pending with no figure and report it.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
