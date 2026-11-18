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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
