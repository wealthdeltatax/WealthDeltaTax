# 044: Reorganise the repository into a vertical tree

- **Status:** parked (starts after the model v3 build; the guru releases it)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** the v3 build briefs (040g D2) merged; the author's decision on `docs/restructure/file-layout.md` section 3
- **Read:** `docs/restructure/file-layout.md` (the whole design); `.github/workflows/deploy.yml`; `site/_quarto.yml`; `docs/agents/code.md`.

## Goal
Move the files into the tree of `file-layout.md` with every reference rewritten, so root holds only what tools need and each folder holds only its own level.

## Decisions (author, 2026-11-18)
Five areas (model, research, web, docs; root files only where tools require). Old papers go to `docs/archive/papers/`. STATUS, OVERVIEW and START_HERE go into `docs/`. The move happens after the v3 build.

## Design
Stages, one session each, each ending in a push and a green check.
- **L1: inventory.** `docs/restructure/file-layout-map.md` and a script `web/pipeline/path_refs.py` (or `pipeline/path_refs.py` before the move): the old-to-new path table for every tracked top-level item, and every tracked file that references an old path (file, line). Checkpoint: pushed; check: the script reports the counts of `file-layout.md` section 4 or explains each difference.
- **L2: research and docs.** `Research/`, `docs/research/` to `research/`; `Tools/` to `docs/skills/`; STATUS, OVERVIEW, START_HERE into `docs/`; rewrite references. Check: the reference script reports none of these old paths; the unit tests pass.
- **L3: model.** `model_v1`, `model_v2`, `model_v3`, `Rates Data` into `model/`; rewrite imports, config and test paths. Check: v3 acceptance command from `acceptance.md` exits 0 (provisional run allowed); v2 tests pass.
- **L4: web.** `site`, `pipeline`, `registry`, `tests` into `web/`; update `deploy.yml`, `_quarto.yml` paths, `.gitignore`, `check_gate.py`, `pages.yml`. Check: full local site build; gate checker output unchanged; all test suites pass; `/model/` URL and CNAME, robots reach the build output.
- **L5: papers and deploy.** Only when the guru confirms the hub and spokes have replaced the old papers: `source/` to `docs/archive/papers/`, the live content to its new home. Check: the deployed site is identical in page list.

## Touches
Every tracked path outside `docs/archive/` and the generated outputs; by stage as above.

## Acceptance criteria
- Root holds only README.md, AGENTS.md, CNAME, robots.txt, .gitignore and the folders `.github`, `.claude`, `model`, `research`, `web`, `docs`.
- The reference script finds no old path anywhere outside `docs/archive/`.
- Site build, deploy dry run, gate checker, and every test suite pass after each stage.
- No history lost: moves are `git mv` (rename detection shows in `git diff -M --stat`).

## Checks to run
The reference script, `pytest` for each suite, the local Quarto build, `python web/pipeline/check_gate.py --all`.

## Out of scope
Changing any file's content other than paths; deleting `model_v1`/`model_v2` (that is 009c); editing archived briefs.

## Open questions
The three points of `file-layout.md` section 3 (papers' live home, `model-v3` docs, tests). Ask the guru before L2.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** parked; not started
<!-- progress:end -->
