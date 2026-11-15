# 010: Rename the model folders to model_v1 and model_v2

- **Status:** ready (after 006c)
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 006c (so the deletions happen at the old paths). Order: after 003s, which also edits the deploy workflow.
- **Read:** `pipeline/preprocess.py` (lines 140 to 190), `pipeline/transforms.py` (lines 55 to 70), `pipeline/tools.py`, `site/_quarto.yml`, `site/tools/taxpayer_calc.html`, `site/pages/calculator_index.md`, `.github/workflows/deploy.yml`.

## Goal
Name the folders for what they are: `model/` becomes `model_v1/` and `model_new_2/` becomes `model_v2/`, without breaking the live site.

## Decisions (author, 2026-11-15)
- `model_new_2` is to be called `model_v2` and the first `model` folder `model_v1`; both are replaced by a model v3 later, so this is housekeeping, not a redesign.

## Design
Triage found:
- `model_new_2/` has no references from outside its own folder except docs (`OVERVIEW.md`, briefs): rename with `git mv model_new_2 model_v2`.
- `model/` is read by the site build: `pipeline/preprocess.py` copies `model/` runtime files and `model/OUTPUTS/` figures into `_build/`, `pipeline/transforms.py` and `pipeline/tools.py` mention the paths, `site/_quarto.yml` lists `model/wdt_core.py`, `model/ldw_core.py`, `model/WDT_Params.toml` as resources, and `site/tools/taxpayer_calc.html` fetches `/model/wdt_core.py` and `/model/WDT_Params.toml` in the browser. `_quarto.yml` also lists `model/rates_model.py`, which no longer exists (now `rates_core1.py`).
- Recommended: rename the source folder to `model_v1/` and change only the source side. The published URL stays `/model/...`: `preprocess.py` reads from `model_v1/` and still writes `_build/model/`, so the calculator pages and `_quarto.yml` resources keep working. Fix the stale `rates_model.py` entry only if the build confirms it is unused; otherwise leave it and report.
- Update the docs that name the old folders (`OVERVIEW.md` through the guru, `README.md`, `AGENTS.md`, `docs/agents/code.md`, `docs/agents/reference/code/conventions.md`, `docs/agents/reference/code/patch-and-test.md`, `docs/wdt-site-architecture.md`). Leave the briefs' history as written.
- Do not rename any file inside the folders.

## Touches
`model/` (renamed), `model_new_2/` (renamed), `pipeline/preprocess.py`, `pipeline/transforms.py` and `pipeline/tools.py` (paths and comments), the docs above.

## Stages
- A: rename `model_new_2` to `model_v2` and fix the docs that name it. Checkpoint: branch pushed; check: `grep -rn model_new_2` finds only briefs and decisions.
- B: rename `model` to `model_v1`, change `preprocess.py` and comments, build locally. Checkpoint: branch pushed, local build passes; check: the built site still contains `_site/model/` calculator pages and the figures count equals the count before.

## Acceptance criteria
- `git ls-files | grep -E '^(model|model_new_2)/'` is empty.
- The site build output is the same set of files as before (compare `find _site -type f | sort` before and after), and the GitHub Action on `main` is green after the merge.
- `/model/wdt_core.py` and `/model/WDT_Params.toml` are still published.

## Checks to run
Local `pipeline/build_and_render.bat` before and after, and the file-list diff. The Action does not run on branches, so merge only after the local build matches, then watch the Action on `main` and revert if it fails (`AGENTS.md` Auto-merge).

## Out of scope
Changing the published URLs, renaming scripts, any change to model code.

## Open questions
- Keep the published URL `/model/` (default) or move it to `/model_v1/`? The second would break any external links to the calculators. Use the default; this is not a stop condition for auto-merge.

## Implementation notes
<!-- progress:start -->
Change report
- Task: 010s rename model folders
- Files changed: `model_new_2/` to `model_v2/` and `model/` to `model_v1/` (git mv, no file renamed inside); `pipeline/config.py`, `pipeline/preprocess.py`, `pipeline/transforms.py` (source-side path and comments); `README.md`, `START_HERE.md`, `AGENTS.md`, `docs/agents/code.md`, `docs/agents/reference/code/conventions.md`, `docs/agents/reference/code/patch-and-test.md`, `docs/wdt-site-architecture.md` (folder names)
- What is different now: the build reads `model_v1/` and still writes `_build/model/`, so published URLs are unchanged.
- New or changed interfaces: none for the site. Local scripts and `run_all.bat` now live under `model_v1/`.
- Acceptance criteria: (1) `git ls-files | grep -E '^(model|model_new_2)/'` is empty: met (0). (2) `find _site -type f | sort` before and after the rename: identical, 157 files; figures 95 before and after: met. The Action on `main` after the merge: see State. (3) `/model/wdt_core.py` and `/model/WDT_Params.toml` still in `_site/model/`: met.
- Deviations from the brief: `OVERVIEW.md` and `STATUS.md` not edited (guru owns them); `docs/lane-plan.html`, audit docs, briefs and `decisions.md` left as written.
- Risks / follow-ups: `site/_quarto.yml` still lists `model/rates_model.py`. The build confirms it is not published (`_site/model/` has no such file), but `site/tools/revenue_calc.html` still fetches it, so the revenue calculator probably fails (architecture doc Issue 16). Left alone as the brief says: needs a decision. `OVERVIEW.md` and `docs/lane-plan.html` still say `model/` and `model_new_2/`.
- Verification: full local build (`preprocess.py` and `quarto render _build`, Linux) on `main` before and after, same file list; `build_and_render.bat` itself not run (Windows).
- Overview sections likely needing an update: section 2 directory map (`model/` to `model_v1/`, `model_new_2/` to `model_v2/`), section 4, section 6.
- Decisions: published URL stays `/model/` (the brief's default).
- Commit / branch: brief/010-rename-model-folders
- Merged by the author's instruction ("006c is merged, merge yours too", 2026-11-15 21:23). Keep live until the author retires it.
<!-- progress:end -->
