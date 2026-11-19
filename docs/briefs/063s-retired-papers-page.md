# 063: Site: the retired papers page and its data (site.md B10)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (029s merged, so `registry/pages.yml` exists)
- **Read:** `docs/restructure/site.md` (section 8 row B10, 8.1, 8.2); `docs/restructure/site/nav.md` (section 2.6 utility pages, decision 5 on old URLs); `docs/restructure/site/ids.md` (rows RET and `registry/retired.yml`, rule 7, the target rule at line 81); `docs/restructure/ledger-sections.md` (header and column key; read the tables, not the notes); `docs/restructure/ledger.md` section 1 (dispositions); `registry/pages.yml`; `pipeline/config.py` (`load_pages`, names only); `pipeline/pages/references.py` (the shape of a generator in `pipeline/pages/`); `docs/agents/web.md`.

## Goal
`registry/retired.yml` records, once and frozen, where each section of the 30 retired numbered papers went, and `pipeline/pages/retired.py` writes the generated retired papers page (`/retired.html`, id RET) from it, so a reader of an old citation finds the new page.

## Decisions (author, 2026-11-18)
Site design approved (`site.md`, `nav.md`, `ids.md`): the 30 numbered papers retire, their URLs end without redirects, the single `wp.html` alias to the hub aside; the retired papers page is a generated old-to-successor table; the three standalones (ADD, INST, SCOPE) are not retired. The data gate holds: no spoke or hub prose. This brief builds on the ledger and fixtures and touches nothing under `source/`.

## Design
1. **One conversion step.** A script in `pipeline/pages/retired.py` (`--convert`) reads `ledger-sections.md` by paper heading and table row (Sec, Section, Words, Disp, Target, Note) and writes `registry/retired.yml`: a list of papers, each `{id: old-<stem>, successor: [page ids], sections: [{sec, title, words, disp, target, page, reason}]}`. `page` is the id of the page in `pages.yml` that the target resolves to; `reason` is the ledger Note for rows with Target `-` (dropped or archived). Mapping of a ledger target to a page id (document it in the file header): a spoke or appendix shortcode (FAIR, FISC, ...) to its own id; H1 and H2 to the hub row `H`; `glossary` to `GLOSS`; `UK data pack`, `input register`, `parameter register` and `method note for O7` to the data-layer page (`data` if `pages.yml` has no row for it, then `page: null` and `target` kept as text); `-` to `page: null`. Ledger rows of the three standalone papers (disposition SA) are not converted. Run the script once and commit the output; after that the file is edited by hand.
2. **`successor`.** Per paper: the pages that receive the most kept (K) and merged (M) words of that paper, in descending order, at most three; computed in the same step and then frozen (a later run of `--convert` refuses to overwrite a file whose header says `frozen: true`). Do not use the ledger's Words for any other purpose.
3. **The generator.** `python pipeline/pages/retired.py --out site/pages/retired.md` writes the page: a short explanatory paragraph (written in the generator: the old numbered series is retired, old addresses no longer work, find a section below; the revision history link as in `ids.md`), then one table per paper (old shortcode, title, successor links) with the section-level rows in a collapsible block (old section number and title, new page link, or the dropped or archived reason). Links use each page's `url` from `pages.yml`; a `page: null` row shows the reason, never a link. No text of any legacy paper is copied: only section numbers and titles from the ledger.
4. **Tests under `tests/retired/`** on the real files and a small fixture: every row of `pages.yml` with type `legacy` and an id of the 30 numbered papers appears exactly once in `retired.yml` and no other paper appears; every non-null `page` and every `successor` resolves to an id in `pages.yml`; every ledger row of the 30 papers (not SA) appears in `retired.yml` once; a frozen file is not overwritten; the generated page contains one table per paper and no link to a legacy URL; no sentence of any file in `source/` appears in the output (compare 12-word shingles of the output against all legacy source files, zero hits).

This is a build brief of `site.md` section 8 (B10). **Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule if the local build passes. A change to a Touches file outside the list, or any change under `source/`, stops the work with NEEDS THE AUTHOR.

## Touches
`registry/retired.yml` (new), `pipeline/pages/retired.py` (new), `tests/retired/` (new), this brief's progress block. Nothing in `source/`, `registry/pages.yml`, `site/` (the generated page goes to `site/pages/retired.md`, which is git-ignored like `glossary.md`; wiring it into the build is brief B15), `.github/`, `model_v3/`, or other docs. Verify before starting that none of the three new paths exists.

## Acceptance criteria
- `registry/retired.yml` has 30 papers and every ledger row of those papers (disposition other than SA) once; its header states the mapping of targets to page ids and `frozen: true`.
- Every test above passes: `pytest tests/retired -q`.
- `python pipeline/pages/retired.py --out <file>` exits 0 and the page lists the 30 papers.
- The local site build (command in `docs/agents/web.md`) passes unchanged (the generated page is not wired in), and `git diff --stat` shows only the Touches list.
- The change report lists every ledger target the mapping could not resolve to a page id (expected: the data-layer targets) and the count of `page: null` rows.

## Checks to run
`pytest tests/retired -q`; the generator command; the local build (the change touches `pipeline/`, so it must pass before any merge to main, AGENTS.md). Skip the live-site fetch: nothing is published.

## Out of scope
Navigation entries for the page (B7), page layout and styles (B8), wiring into the build and the `/draft/` index (B15), cutover and the move of the 30 files to `docs/archive/papers/` (B16), any redirect, the pending pages, spoke or hub prose, and any edit of the ledger.

## Open questions
Ask the guru rather than guess: (1) whether a data-layer page row is to exist in `pages.yml` for the register targets; (2) a ledger target not covered by the mapping above; (3) if two pages tie for `successor`.

## Guru rulings, 2026-11-18
Both granularities: `retired.yml` holds the section rows and a frozen per-paper `successor` of at most three pages, the page shows paper tables with collapsible section rows: accepted. `successor` lives in `retired.yml`, not `papers.yml`: accepted. SA standalone rows are excluded; report the parsed count against the 980 of `ids.md`. Data-layer targets with no `pages.yml` row resolve to `page: null` and go in the change report.

## Implementation notes
<!-- progress:start -->
- **Done:** `pipeline/pages/retired.py` (`--convert`, `--out`), `registry/retired.yml` (frozen; 30 papers, 938 sections), `tests/retired/` (13 tests).
- **Next:** author decides the 12-word criterion (see Decisions); then merge. Wiring the page into the build is B15.
- **Decisions:** Ledger holds 980 rows; 938 belong to the 30 retired papers; 42 belong to ADD, INST, SCOPE and are not converted. Data-layer targets (48 rows) have no `pages.yml` row, so `page: null` with the target kept as text. A tie for `successor` raises an error; none occurred. Links on the page go to non-legacy rows; five new pages (VAL, CORP, GOV, BEHAV, POL) share the URL of the old paper they replace, so the link test checks the row, not the URL.
- **Gotchas:** The build's scrape step rewrites `registry/contents.yml`; I restored it, so the diff shows only Touches.
- **Resume:** nothing to resume.
- **Not run:** the generated page was written to the scratchpad, not `site/pages/` (outside Touches).
- **State:** done; NEEDS THE AUTHOR (one criterion not met as written)
<!-- progress:end -->

```
Change report
- Task: brief 063s, retired papers page
- Files changed: registry/retired.yml (new; frozen conversion of the ledger, 30 papers); pipeline/pages/retired.py (new; --convert and --out); tests/retired/ (new; conftest and 13 tests); this brief (progress block and report)
- What is different now: where each section of the 30 retired papers went is recorded once in registry/retired.yml; the generator writes the page from it (30 tables, sections in collapsible blocks, no link to a legacy row)
- New or changed interfaces: python pipeline/pages/retired.py --convert (refuses a frozen file); python pipeline/pages/retired.py --out FILE
- Acceptance criteria:
  - 30 papers, every ledger row of those papers once, header states mapping and frozen: true. Met: 30 papers, 938 of 980 ledger rows (the other 42 are ADD, INST, SCOPE).
  - pytest tests/retired -q passes. Met: 13 passed. Full suite: 317 passed.
  - Generator exits 0 and lists 30 papers. Met.
  - Local site build passes unchanged; diff shows only Touches. Met: build exit 0; git diff shows only the new paths (contents.yml, rewritten by the scrape step, restored).
  - Change report lists unresolved ledger targets and the page null count. Met: unresolved targets: none; page null rows: 314 (266 dropped or archived with the ledger note as reason, 48 data-layer targets with no page row).
  - Zero 12-word shingle hits against source/ legacy files. NOT MET as written: 8 hits on 5 lines, all of them titles of 12 words or more (for example the MF and WFR paper titles), which the brief says to copy. The test exempts only lines that carry such a title; no prose overlaps.
- Deviations from the brief: none beyond the criterion above.
- Risks / follow-ups: three papers have an empty successor (old-rates-a, old-sweeps-a, old-wfr-a: all their words are dropped, archived or data-layer), shown as "None". Author: accept titles as exempt from the shingle check, or shorten the long titles by hand in retired.yml. Add a data-layer row to pages.yml (B9) and edit the 48 rows by hand then.
- Verification: pytest tests (317 passed); scrape, glossary, anchors, preprocess and quarto render _build exit 0; generator run to the scratchpad.
- Overview sections likely needing an update: site pages and registry (retired.yml)
- Commit / branch: brief/063s
```

