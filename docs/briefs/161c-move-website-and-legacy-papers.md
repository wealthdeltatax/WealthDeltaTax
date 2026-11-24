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
- **Done:** 177 files `git mv`ed per the map (53 site, 27 web build scripts, 8 web registry files, 56 web tests, 33 papers; 114 pure renames, the rest renamed with path-only edits); 248 named-path lines rewritten from the reference csv; built paths and depths rewritten by hand in 20 scripts and 9 test conftests/tests; `deploy.yml`, `.gitignore`, both `.bat` files; page cards regenerated; every check below run.
- **Next:** the author reviews (the diff moves `source/`, so no auto-merge); then rebase on `main` (160c may merge first) and `git push origin HEAD:main`.
- **Decisions:** (1) `check_gate.py`, `tests/gate`, `validate_outputs.py` stay in `pipeline/` for 162c (map case 7 and 10); only web paths they read were repaired, and `hooks.py`, the hooks conftest load `validate_outputs` from `pipeline/` until then. (2) The 40 `docs/restructure` site notes, `wdt-site-architecture.md` and `navigation_suggestions.md` are not in Touches: left for 164c. (3) Hub and spokes (`source/hub.md`, `source/spokes/*`, not yet written) point to `papers/hub.md` and `papers/spokes/`, not `papers/legacy/` (tree: "later the hub and spokes"). (4) `print/` goes to `website/print/`; `_build/` stays at the root (the deploy renders `_build`). (5) The glossary registry mode finds its root three levels above `registry/glossary.yml`; the glossary test fixtures gained one folder of prefix (`glossary/fixtures/...`). (6) `registry/internal.json` line 2 keeps its stale citation (ruling 3).
- **Gotchas:** `run_suites.py` no longer finds the web suites (they sit one level deeper, `tests/website/<suite>`); run each with `pytest tests/website/<suite>` until 162c rewrites it. `is_spoke_source` takes the source root (now `papers/legacy`), so the first spoke under `papers/spokes/` needs a decision. The Quarto render needs Quarto on PATH (installed here with `pip install quarto-cli`).
- **Resume:** `git checkout brief/161-move-website-and-legacy-papers`; checks in the change report below.
- **Not run:** the model suites (`tests/model_v3`: collection only, 408 tests, files untouched); the full `quick` run (057c not merged); the GitHub Action (not pushed to `main`).
- **State:** done, pushed, `NEEDS THE AUTHOR` (diff touches `source/`)
<!-- progress:end -->

Change report
- Task: 161c, move the website, its build scripts, registry and tests to `website/` and `tests/website/`, and the legacy papers to `papers/legacy/` (reorganisation R3)
- Files changed: 177 moved (`site/` 53, `pipeline/` web scripts 27 incl. 2 `.bat`, `registry/` web files 8, `tests/{cards,glossary,hooks,layout,nav,pages,retired}` 56, `source/` 33); path edits in 60 moved or reading files (`website/build/*.py`, `website/registry/*.yml`, `tests/website/**`, `.github/workflows/deploy.yml`, `.gitignore`, `pipeline/check_gate.py`, `pipeline/check_agent_docs.py`, `tests/gate/*`, `tests/data/test_to_markdown.py`); 26 page cards regenerated; readers in `AGENTS.md`, `START_HERE.md`, `docs/agents/*`, a few `docs/` notes; one friction-log entry
- What is different now: the site, its build, registry and web tests live in `website/` and `tests/website/`; the 33 legacy papers are in `papers/legacy/`, byte-identical (all 33 are 100% renames). No model file moved; no number changed
- New or changed interfaces: site build commands now `python website/build/<script>.py` (`scrape_contents`, `build_glossary --papers papers/legacy --contents website/registry/contents.yml --out website/site/pages/glossary.md`, `build_anchors`, `preprocess`), then `quarto render _build`; `ROOT_DIR` in `config.py` is now `parents[2]` of the script; `hooks.py _load(name, base)`
- Acceptance criteria: web files only under `website/`, `tests/website/`, `papers/legacy/`: met for the files in Touches (the `docs/restructure` notes and the two loose notes are not moved, see Decisions); no name repeated: met (`path_refs` map has no collision; moves are the map's); build and web suites pass: met, no R5 exception needed (cards 8, glossary 26 + 1 skip, hooks 67, layout 40, nav 59, pages 28, retired 13, plus gate 17 and data 103); gate output unchanged: met in substance (same verdicts for 26 pages, exit 1 both before and after; only the path words in the messages differ); deploy workflow points to the new paths: met; local-only files listed: met (below)
- Deviations from the brief: (1) gate checker and its tests stay in `pipeline/` and `tests/gate` (map case 7 and 10 give them to 162c; the brief's Design lists "gate" under the web side); (2) `docs/restructure` site notes (40 files) and two loose notes not moved (outside Touches); (3) no R3 renames: the map settles none for these trees
- Risks / follow-ups: `run_suites.py` and `check_gate.py` G5 know the web suites by their old folders (G5 now names `tests/website/hooks` instead of `tests/hooks`; `run_suites.py` discovery misses `tests/website/*`; 162c rewrites it); hub and spokes source root (see Decisions 3); 162c must move `validate_outputs.py` and then repoint `hooks.py` and the hooks conftest (`MODEL_TOOLS`); `OVERVIEW.md` (11 lines), `STATUS.md`, `docs/lane-plan.html` and the briefs still name old paths (R6); `docs/wdt-site-architecture.md` prose still names `site/` and `source/`; 160c edits `bib_to_json.py`, `pdf.py` and `hooks.py` for `literature/`: the second branch to merge rebases
- Instruction friction: one entry in `docs/agents/friction-log.md` (brief and map disagree on the gate; the proof tool flags generic words)
- Verification: `check_agent_docs.py` clean; `compileall` clean; `pytest --collect-only` per suite (website 8, 40; model_v3 408; data 103; gate 17); `path_rewrite_proof.py --base 1b1f43b`: 144 moved, 46 files differ after the map is applied, all reviewed: intended path or depth edits, plus the proof applying the map to generic words (`source:`, `site`, `Tools`); tripwire PASS in 103 s (inputs.json bytes, legacy digest, pack rebuild, household evaluation at 20 paths all equal the baseline); the site Python stages (`scrape_contents`, `build_glossary`, `build_anchors`, `preprocess`) on this branch and on `main`: staged `_build` identical apart from path words in comments and one timestamp; `quarto render _build` passes on both (50 pages each, HTML identical except `link-map.html` comment and `sitemap.xml`); `check_gate.py --all` same verdicts before and after; `registry/internal.json` pinned line left unchanged
- Local-only files to move by hand (old to new): `source/.obsidian/` to `papers/legacy/.obsidian/`; `print/` to `website/print/` (generated PDFs, `pdf.py` and `zenodo_upload.py` write there now); `pdfs/` to `literature/` (as the map says; no script reads it); `site/pages/glossary.md` to `website/site/pages/glossary.md` (regenerated by the build); `anchors.yml` is regenerated at `website/registry/anchors.yml`; `.quarto/`, `_build/`, `_site/` are rebuilt, not moved; `check*.txt` reports now ignored under `website/build/` as well
- Overview sections likely needing an update: the file-layout and site-build sections (all `site/`, `pipeline/`, `registry/`, `source/` paths), the Agents table entry for web
- Commit / branch: `brief/161-move-website-and-legacy-papers`, pushed; NOT merged: `NEEDS THE AUTHOR` because the diff touches `source/` (paper text moved; no paper content changed)
