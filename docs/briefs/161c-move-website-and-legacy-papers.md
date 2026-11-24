# 161: Move the website and the legacy papers (reorganisation R3)

- **Status:** ready (044c R1 merged and settled); Agent 5; runs in parallel with 160c; the authority is `docs/restructure/file-layout-map.md` and its csv
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 044c R1 merged and reviewed; no other branch touching these paths
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `.github/workflows/deploy.yml`; `site/_quarto.yml`

## Goal
The website, its build scripts, its registry and tests are in `website/` and `tests/website/`; the legacy papers are in `papers/legacy/`.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `site/`, the web side of `pipeline/` (site build, gate, hooks, checks, `.bat` files), the web registry (pages, glossary, crosslinks, references, routing) and the web tests (cards, glossary, hooks, layout, nav, pages, retired, gate) to `website/` and `tests/website/`. The model-side pipeline scripts (`build_inputs`, `build_metrics`, `validate_outputs`) and `registry/inputs.json` and `metrics.json` stay for 162c; where a script is shared, the L1 table decides.
- `source/` to `papers/legacy/`. R5: the site build and the page and gate tests that read the papers may fail; repair paths first, change no paper content, list every red check. The legacy calculators and figures already lost their model assets in 009c.
- Update `deploy.yml`, `_quarto.yml`, `.gitignore` lines for `_build`, `.quarto`, `pdfs`, `print`, `check_gate.py`, `pages.yml`, the `.bat` files; CNAME and robots reach the published root.
- Names: rename generic names under R3 (for example `site/pages/research.md`) with every reader rewritten.
- Check: the local build and web suites as far as R5 allows; gate checker output unchanged for pages outside `papers/`; model suites untouched.

## Touches
`site/`, `pipeline/` (web side), `registry/` (web side), `tests/` (web suites), `source/`, `.github/workflows/deploy.yml`, `.gitignore`, `CNAME`/`robots.txt` wiring, readers of those paths.

## Acceptance criteria
- Web files only under `website/`, `tests/website/`, `papers/legacy/`; no name repeated.
- Build and web suites pass except those R5 lists; gate output unchanged outside the papers; deploy workflow points to the new paths.
- Local-only files listed.

## Out of scope
The model, datasets, research, skills and the shared files; rewriting any paper.

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:** block 0: branch from `origin/main` (1b1f43b); scope read from `file-layout-map.csv`: 218 rows land in my trees (53 site, 27 web build scripts, 8 web registry files, 56 web tests, 33 papers, 40 notes, 1 architecture note).
- **Next:** block 1 `git mv` per map; block 2 reference and depth rewrites; block 3 checks; block 4 report.
- **Decisions:** (1) `check_gate.py` and `tests/gate` go to `model/` in the map (162c), so they stay put here; I only repair the web paths they read. (2) The 40 `docs/restructure` notes and `wdt-site-architecture.md` are not in this brief's Touches; left for 164c, flagged. (3) `registry/references.bib`, `internal.json` go to `literature/` (160c), so `bib_to_json.py` reads them from there only after 160c merges.
- **Gotchas:** clone is shallow; the tripwire needs full history.
- **Resume:** `git checkout brief/161-move-website-and-legacy-papers`; `python pipeline/path_refs.py --check`.
- **Not run:** everything (nothing moved yet).
- **State:** block 0 done
<!-- progress:end -->
