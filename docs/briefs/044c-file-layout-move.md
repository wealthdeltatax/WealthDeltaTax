# 044: Reorganise the repository into a vertical tree

- **Status:** rewritten 2026-11-24 after the author's four answers; ready once 057c, 148c and 009c have merged; Agent 3, alone on the repository (no other branch open while it moves files)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 057c, 148c and 009c merged and no other branch open; the author's answers of 2026-11-24 (below). `docs/restructure/file-layout.md` is the 2026-11-18 design; where this brief differs, this brief wins
- **Read:** `docs/restructure/file-layout.md` (the whole design); `.github/workflows/deploy.yml`; `site/_quarto.yml`; `docs/agents/code.md`.

## Goal
Move every tracked file into five areas (model, research, web, docs, root files tools need) with every reference rewritten, so each folder holds only its own level. Nothing about any number the model produces changes.

## Author decisions
- 2026-11-18: five areas; old papers to `docs/archive/papers/` only once the hub and spokes have replaced them; STATUS, OVERVIEW and START_HERE into `docs/`.
- 2026-11-24: (1) the model keeps its import name: `model/model_v1`, `model/model_v2`, `model/model_v3` (no package rename). (2) One research area with four subfolders (below); `docs/model-audit/` and `docs/audit/` go to `docs/archive/` (the audit is done). (3) `registry/` and `pipeline/` are split by owner: what the model or its tools read goes under `model/`, what the site reads goes under `web/`. (4) The skill sources are rewritten in 044c (repo copies and the `.skill` files); the guru then proposes the matching edits to the account skills for the author to save.
- Guru defaults, open to override at the L1 checkpoint: `docs/model-v3/` (design record and run outputs, 188 files) moves to `model/docs/model_v3/`; model tests (`tests/model_v3`, `tests/data`) move to `model/tests/`, page, gate, cards, glossary, hooks, layout, nav, pages and retired tests move to `web/tests/`; `Rates Data/` becomes `model/data/rates/` (no space in the name).

## Target tree
```
README.md  AGENTS.md  CNAME  robots.txt  .gitignore  .gitattributes   root files tools need
.github/  .claude/                                                    stay (paths inside rewritten)
model/    model_v1/  model_v2/  model_v3/   data/rates/   registry/ (inputs, metrics, what the model reads)   tools/ (build_inputs, build_metrics, validate_outputs, run scripts)   tests/   docs/model_v3/
research/ sources/ (Research/ PDFs)   notes/ (docs/research NNNr notes)   data/ (docs/research/data)   readable/ (docs/research/readable)   hypotheses/ (docs/hypotheses)
web/      site/  pipeline/ (site build, gate, hooks, checks)   registry/ (pages, glossary, crosslinks, references)   tests/   source/ (the old papers, stays live until L6)
docs/     STATUS.md OVERVIEW.md START_HERE.md  briefs/ agents/ archive/ (gains model-audit, audit)  decisions.md  todo.md  restructure/  housekeeping/  model-lessons/  skills/ (Tools/ .skill files)  lane-plan.html and the other loose notes (EVAL_PLAN, VAL_*, navigation_suggestions, wdt-*) into docs/notes/
```
Every folder's top level is a short list of subfolders and at most a README.

## Hazards the old brief did not name
1. **Depth-based paths.** `Path(__file__).parents[n]`, `..` joins and relative includes break silently when a folder gets deeper; the reference script (name-based) cannot see them. L1 lists every `__file__`, `parents[`, `os.path`, `..`/ relative include and `.bat`/YAML path, with the depth change it needs.
2. **Gate hash and digest.** `registry/inputs.json` is hashed for the gate, and `test_legacy_digest` pins results. Moves are `git mv` with identical bytes; after each stage the hash of `inputs.json` and the digest test are unchanged.
3. **Windows.** The author works on Windows: `Research/` to `research/` is a case-only rename (do it through a temporary name in two commits); `Rates Data` has a space; paths under `research/data` are long (check the 260 character limit); `.bat` files and PowerShell commands in `docs/housekeeping/` are rewritten.
4. **Local-only files.** Ignored files do not move with `git mv`: the 097r workbooks (`boe-nmg-*.xlsx`, `nbs.xlsx`, `ukea2026q2.xlsx`), `.quarto`, `_build`, `scratch/`, `pdfs/`, `print/`. The change report lists each one with its old and new path so the author moves them by hand, and `.gitignore` is rewritten to the new paths.
5. **Docs checks.** `check_agent_docs.py` rejects path-like tokens that do not exist; active briefs, `AGENTS.md`, `docs/agents/*`, STATUS, OVERVIEW and START_HERE are rewritten to new paths; archived briefs and `docs/decisions.md` history are not edited (a note at the top of `file-layout-map.md` gives the old-to-new table).
6. **Skills.** `.claude/skills/*`, `docs/skills/*.skill` (built by `build_skills.py`) and the account skills name repo paths. The repo copies are rewritten and rebuilt; the change report lists every changed line so the guru can propose the account edits.
7. **Run commands.** `accept.sh`, the smoke and `quick` commands (`python -I -c "import sys; sys.path.insert(0, '.')..."`) and the planned Actions workflow for big runs: the first is rewritten, the workflow is written after the move (not before).
8. **Large files and history.** `.git` is about 576 MB (`research/data` 211 MB, model_v2 dumps 151 MB until 009c). Moves keep history (`git mv`; `git diff -M --stat` shows renames); no rewriting of history, no LFS here (a later question).

## Design
One stage per session; each ends with a push of the branch and a green check; the guru merges to `main` before the next stage starts, so `main` is never half-moved while another branch exists.
- **L1: inventory and classification (no moves).** `docs/restructure/file-layout-map.md` and `pipeline/path_refs.py`: the old-to-new path for every tracked top-level item and every file under `pipeline/`, `registry/`, `tests/` (model side or web side, with the rule used: read by model code or model tools = model, else web); every tracked file that references an old path (file, line); the depth-based path list (hazard 1); the local-only list (hazard 4). **Checkpoint: the guru and author review the table before L2.**
- **L2: research.** `Research/` to `research/sources/`, `docs/research/` notes to `research/notes/`, its `data/` and `readable/` to `research/data/` and `research/readable/`, `docs/hypotheses/` to `research/hypotheses/`; `docs/model-audit/` and `docs/audit/` into `docs/archive/`. Check: reference script clean for these; hooks, data tests pass.
- **L3: docs and skills.** STATUS, OVERVIEW, START_HERE into `docs/`; loose notes into `docs/notes/`; `Tools/` to `docs/skills/`; rewrite `.claude/skills`, `AGENTS.md`, `docs/agents/*`, README and active briefs; rebuild the `.skill` files. Check: `check_agent_docs.py` passes; the skill change list is in the report.
- **L4: model.** `model_v1`, `model_v2`, `model_v3`, `Rates Data`, the model side of `registry/`, `pipeline/` and `tests/`, and `docs/model-v3/` into `model/`; rewrite imports, config, manifest and test paths and `accept.sh`. Check: all `model/tests` pass, the legacy digest and the `inputs.json` hash are unchanged, and a `quick` run (after the 057c command) reproduces the pre-move `quick` reference file byte for byte.
- **L5: web.** `site`, `source`, the web side of `pipeline`, `registry` and `tests` into `web/`; update `deploy.yml`, `_quarto.yml`, `.gitignore`, `check_gate.py`, `pages.yml`, the `.bat` files. Check: full local site build; gate checker output unchanged; every web test suite passes; the deploy dry run publishes the same page list, with `/model/`, CNAME and robots at the published root.
- **L6: old papers (conditional).** Only when the guru confirms the hub and spokes have replaced them: `web/source/` to `docs/archive/papers/`, live content to `web/content/`. Not started by default; the stage report says it was not run.

## Touches
Every tracked path outside `docs/archive/` (archived briefs and decision history are not edited) and the generated outputs; by stage as above.

## Acceptance criteria
- Root holds only README.md, AGENTS.md, CNAME, robots.txt, .gitignore, .gitattributes and the folders `.github`, `.claude`, `model`, `research`, `web`, `docs`.
- The reference script finds no old path outside `docs/archive/`; the depth-based path list is empty or every entry is verified.
- After each stage: all test suites, the gate checker and `check_agent_docs.py` pass; after L4 the model output is byte-identical to before; after L5 the built page list is identical.
- Moves are `git mv`; renames show in `git diff -M --stat`; no content changes except paths.
- The change report lists the local-only files to move by hand and every skill line changed.

## Checks to run
The reference script, the test suites (one `pytest` run per suite folder, in the background), the local Quarto build, `check_gate.py --all`, the legacy digest, the `quick` byte comparison (L4).

## Out of scope
Changing any file's content other than paths; deleting `model_v1` or `model_v2` (009c); editing archived briefs; history rewriting, LFS; the Actions workflow (after the move); the old papers' archive (L6, conditional).

## Open questions
None open for L1. At the L1 checkpoint: the model-side or web-side call for any file the rule cannot settle; the default homes for `docs/model-v3/` and the tests.

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
