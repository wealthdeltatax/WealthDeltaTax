# 043: Map the uploaded research to the register's sources and add held figures

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (032r merged; all literature PDFs are now in `Research/`)
- **Read:** `docs/model-v3/inputs.md` (the source table S1 to S43 and every row that cites one); `registry/lit-figures.yml` (header and entries; it is the model to follow); `registry/inputs-display.yml`; `Research/` (file list); `docs/restructure/site/hooks.md` Q9 and the 032r rulings (lit-figures format).

## Goal
Every source the register cites is tied to the file held for it (or marked not held), every cited page is checked against the held copy, and the figures behind the register rows are entered in `registry/lit-figures.yml`, so the papers can quote them without re-reading the sources. Today only six ONS ETB figures are entered; the other literature was not held.

## Decisions (author, 2026-11-18)
- All literature PDFs the author could obtain are uploaded to `Research/`. The workspace cannot download PDFs, so do not try; for a source with no file, say not held.
- Reference-list rework is the author's later job. This brief does not edit `registry/references.bib` or `internal.json`.
- No figure from memory. A figure enters `lit-figures.yml` only when re-read in the held copy.

## Design
Two stages, one agent, each ending in a push.
- **M1: mapping.** Write `docs/model-v3/source-map.md`: one row per S-id S1 to S43: held file (path in `Research/` or `Rates Data/`) or `not held`; version note where the held file differs from the one the register cites (known: `wp-2017-241-fuest-peichl-siegloch-corporate-taxes.pdf` is the 2017 ifo WP 241, S22 cites the 2015 IZA DP 9606; `Adam et al. (IFS).pdf` is the Mirrlees Review preface, *Tax by Design* 2011, and matches no S-id; `R168-Revaluation-...pdf` is S38, IFS March 2020; `1475_5890.12286.pdf` is Advani, Bangham, Leslie 2021 in Fiscal Studies, S5 cites the CAGE WP 576; `Fiscal Studies - 2021 - Advani - Behavioural...pdf` is S13; `Accretion-Based Progressive Wealth Taxation.pdf` is Hasen 2017, check which S-id or paper cites it, if none say so; `report-g20.pdf` against S24; `Effects of taxes and benefits...pdf` against S23). For each held source: the register rows that cite it and the pages they cite. Also a proposed bib key per held source (`AuthorYear` style, matching `references.bib` where an entry exists, else marked proposed). Checkpoint: pushed file; check: 43 rows, every held PDF in `Research/` appears once.
- **M2: page check and figures.** For each held source, open the cited pages and compare each figure the register or `inputs-display.yml` takes from it. Record in `source-map.md` section 2: row id, figure as printed, page, `ok` or `differs` (say how). Enter in `registry/lit-figures.yml` each figure that a register row or ledger row uses, in the existing format (`<bibkey>:<slug>`, `value`, `unit`, `decimals`, `quoted_as`, `page`, `verified`), and update the header comment (coverage and the MISSING keys list). Checkpoint: pushed; check: `python pipeline/validate_outputs.py` and the 030c data tests still pass; `python -I` load of `registry/lit-figures.yml` returns every entry with all fields.

## Touches
`docs/model-v3/source-map.md` (new), `registry/lit-figures.yml`, this brief's progress block. If a register row's cited page or figure is wrong, do not edit `inputs.md`: list it in `source-map.md` section 3 for the guru.

## Acceptance criteria
- `source-map.md` has all 43 S-ids and every file in `Research/` (script check).
- Every `lit-figures.yml` entry has a page and a verified date; no figure without a held copy.
- Every discrepancy between a register figure and the held source is listed in section 3, none silently fixed.
- `git diff --stat` is limited to the Touches list.

## Checks to run
The two scripts above; the data tests (`pytest tests/data -q`). Skip the site build (no site file touched).

## Out of scope
Downloading anything; `references.bib`; `inputs.md`, `inputs.json` and `outputs.yml` edits; non-literature sources (ONS and HMRC data files, news items) beyond saying held or not held; reading beyond the cited pages.

## Open questions
Ask rather than guess: which S-id a held PDF belongs to when the match is not clear.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/model-v3/source-map.md` (43 S-ids, all 17 files of `Research/` and 7 of `Rates Data/` once, page check, 12 discrepancies) and `registry/lit-figures.yml` (67 entries: 6 ETB bulletin, 7 ETB workbook cells, 54 figures from S4, S5, S6, S13, S16, S17, S18, S22, S24, S25, S30; header lists 10 proposed bib keys). Script check: 54 of 54 figures matched by pattern on the named held page, 7 of 7 workbook cells; `python -I` load returns 67 entries with all fields; `pytest tests/data -q` 75 passed.
- **Next:** guru reads section 3 and decides the register edits (S22 workers' share, S37 figures, page notes); author reworks the reference list (10 proposed keys; `Hasen2017` points to the wrong work).
- **Decisions:** page = PDF page of the held file, printed page added where checked; version differences recorded, not corrected; ranges entered as two entries; no S37 or S38 figure entered (not in the held text).
- **Gotchas:** S22 held WP says 51% workers, register says 40% (the 40% in the WP is the capital share); S37's 35%/45%/11% are not in the article; S5 and S13 register pages are WP numbering; `Adam et al. (IFS).pdf` is the full 548-page *Tax by Design*, not a preface; bib `Hasen2017` is Richard Hasen, the papers mean David Hasen. `python pipeline/validate_outputs.py` needs a file argument; on `registry/metrics.json --fixture` it reports 3 errors, a file this brief did not touch (pre-existing).
- **Resume:** n/a
- **Not run:** site build (no site file touched); the check script is not committed (Touches).
- **State:** done, merged.
<<!-- progress:end -->
