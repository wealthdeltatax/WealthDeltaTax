# 044: Reorganise the repository into a vertical tree

- **Status:** rewritten twice on 2026-11-24 (second time: by type of thing, unique names); ready once 057c, 148c and 009c have merged; Agent 3, alone on the repository (no other branch open while it moves files)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 057c, 148c and 009c merged and no other branch open; the author's answers of 2026-11-24 (below). `docs/restructure/file-layout.md` is the 2026-11-18 design; where this brief differs, this brief wins
- **Read:** `docs/restructure/file-layout.md` (the whole design); `.github/workflows/deploy.yml`; `site/_quarto.yml`; `docs/agents/code.md`.

## Goal
Sort every tracked file by the **type of thing it is**, into folders a layperson can find from the names alone, with no repeated file names and no type of thing split across branches. Every reference is rewritten. No number the model produces changes.

## Rules (author, 2026-11-24)
- **R1 Plain names.** Each folder is named for what it holds, in plain words; a reader should find the right area from file and folder names without opening anything.
- **R2 One type, one branch.** Datasets live in one branch, PDFs in one, research notes in one, model code in one, model run outputs in one, tests in one, briefs in one, skills in one. State (open or done) is a subfolder of the type, not a second branch.
- **R3 Unique, descriptive file names.** A file name is not repeated anywhere in the tree and says what the file is (`f1-phases06-safe-grid.csv`, not `f1_safe_grid.csv` inside a phase folder; no `report.md`, `tables.md`, `check.py`). Exceptions only: `conftest.py`, `__init__.py`, `SKILL.md`, `README.md`, files a loader reads by a fixed name (the country pack's own files) and the test fixtures that deliberately mirror them (under `tests/**/fixtures/`). A generic name is renamed with every reader rewritten.
- **R4 Duplicates.** Byte-identical copies (checked by hash) are reduced to one; same-name files that differ are renamed by R3. Code copies in `model_v1` and `model_v2` go with 009c, not here.
- **R5 Old papers.** The legacy papers are legacy: they move to `papers/legacy/`. The author accepts that the site build and the page and gate tests that read them may fail until the papers are rewritten from the hub and spokes; the agent still repairs paths first, changes no paper content, and lists each red check in the stage report.

Earlier rulings still hold: the model keeps its import name (`model/model_v3`, no package rename); the skill sources are rewritten in 044c and the guru then proposes the account skill edits; moves are `git mv`.

## Target tree
```
README.md  AGENTS.md  CNAME  robots.txt  .gitignore  .gitattributes   files tools need at root
.github/  .claude/                                                    stay (paths inside rewritten)
data/        every dataset: uk-wealth-tables (097r, 098r, 129r sources), rates (was Rates Data), jst (one jst_r6.json), wid, country-pack-GBR, input-register (inputs.json)
literature/  the PDFs only, and readable/ (converted reading copies of them)
research/    notes (the NNNr notes and derivations), hypotheses, model-audit, model-lessons, scaffold audit
model/       code only: model_v3/ (v1, v2 until 009c retires them), tools/ (build_inputs, build_metrics, validate_outputs, run scripts), studies/ (the driver scripts that make results)
model-specs/ what the model is meant to do: architecture, acceptance, metrics, outputs manifest, input-register docs, country-pack spec, drivers, design notes
results/     every model run output, one folder per study (death-phases, feasibility-map, household-arm-lien, ...), each holding its report and its csv files
papers/      legacy/ (the old papers), later the hub and spokes
website/     site/, build scripts (the web part of pipeline), page registry (pages, glossary, crosslinks, references), site notes
tests/       model/ and website/ (one folder per suite)
project/     STATUS.md, OVERVIEW.md, START_HERE.md, decisions.md, todo.md, lane-plan.html, briefs/ (open, done), agents/, skills/ (the .skill files), housekeeping/, restructure/, notes/ (the loose plans)
```
A study's report goes with its csv in `results/`; a document that says what the model should do goes in `model-specs/`; the script that makes the study goes in `model/studies/`. Guru defaults for the cases the rules cannot settle (open at the L1 checkpoint): `docs/EVAL_PLAN.md`, `VAL_*` to `research/`; `wdt-site-architecture.md` to `website/`; `wdt-jel-codes.md` to `research/`; `docs/agents/reference/code/patch-kit` stays with `project/agents/`; `model_v2/wid_out` and `audit_d0` to `data/` unless 009c removes them.

## Hazards
1. **Depth-based paths.** `Path(__file__).parents[n]`, `..` joins and relative includes break silently when a folder gets deeper or shallower; L1 lists every `__file__`, `parents[`, `os.path`, relative include, `.bat` and YAML path with the change it needs.
2. **Gate hash and digest.** `inputs.json` is hashed for the gate; `test_legacy_digest` pins results. Moves keep bytes; after each stage both are unchanged (the hash of `inputs.json`, the digest test).
3. **Renames read by code.** Generic names are renamed under R3: every reader (code, manifest, test, doc) is rewritten in the same commit; the pack's own files are exempt.
4. **Windows.** `Research` to `literature` is a different name, but `Rates Data` has a space and `docs/research/data` paths are long (check the 260 character limit); `.bat` files and the PowerShell commands in `docs/housekeeping/` are rewritten.
5. **Local-only files.** Ignored files do not move with `git mv`: the 097r workbooks (`boe-nmg-*.xlsx`, `nbs.xlsx`, `ukea2026q2.xlsx`), `.quarto`, `_build`, `scratch/`, `pdfs/`, `print/`. The change report lists each with its old and new path for the author to move by hand; `.gitignore` is rewritten.
6. **Docs checks.** `check_agent_docs.py` rejects path-like tokens that do not exist; active briefs, `AGENTS.md`, `project/agents/*`, STATUS, OVERVIEW, START_HERE and READMEs are rewritten to new paths. Archived briefs and decision history are not edited; `file-layout-map.md` carries the old-to-new table.
7. **Skills.** `.claude/skills/*`, the `.skill` files (built by `build_skills.py`) and the account skills name repo paths; the repo copies are rewritten and rebuilt, and every changed line is listed in the report.
8. **Run commands.** `accept.sh`, the smoke and `quick` commands and the planned Actions workflow: the first two are rewritten, the workflow is written after the move.
9. **Large files and history.** `.git` is about 576 MB. No history rewrite and no LFS here (a later question); duplicate removal (R4) only shrinks the next checkout.
10. **Briefs in flight.** None may be open: every other branch is merged or closed before L1, and the guru merges each stage to `main` before the next starts.

## Design
One stage per session; each ends with a push of the branch and a green check (except R5's allowance); the guru merges to `main` before the next stage.
- **L1: inventory (no moves).** `project/restructure/file-layout-map.md` and `pipeline/path_refs.py` (moved with the web scripts later): for every tracked file or folder, old path, new path and, under R3, new name; the duplicate report (byte-identical, same name different); every file that references an old path (file, line); the depth-based path list; the local-only list; the files the rules cannot settle, each with the default. **Checkpoint: the guru and author review the table before L2.**
- **L2: datasets, literature, research.** `Research/` PDFs and the 129r PDFs to `literature/`; their converted copies to `literature/readable/`; `docs/research/data` and `Rates Data` to `data/` by source; the notes, hypotheses, audits and lessons to `research/`; remove byte duplicates (hash-checked, listed); rename generic names. Check: reference script clean for these; hooks and data tests pass.
- **L3: project and skills.** `docs/` to `project/` (STATUS, OVERVIEW, START_HERE, decisions, briefs open and done, agents, lane plan, housekeeping, restructure, loose notes), `Tools/` to `project/skills/`; rewrite `.claude/skills`, `AGENTS.md`, agents docs, README and active briefs; rebuild the `.skill` files. Check: `check_agent_docs.py` passes; the skill change list is in the report.
- **L4: model code and its inputs.** `model_v1`, `model_v2`, `model_v3` into `model/`, the model-side pipeline scripts to `model/tools/`, the driver scripts to `model/studies/`, the country pack to `data/country-pack-GBR/`, `inputs.json` and the model-side registry files to `data/input-register/`, the model tests to `tests/model/`; rewrite imports, config, manifest, test paths and `accept.sh`. Check: all model tests pass; the legacy digest and the `inputs.json` hash unchanged; a `quick` run (the 057c command) reproduces the pre-move `quick` reference file byte for byte.
- **L5: model specs and results.** `docs/model-v3/` split by type: specifications to `model-specs/`, reports and csv to `results/<study>/` with R3 names (phase and fund in the file name where a study repeats them); rewrite every reader (the manifest, tests, docs). Check: all suites pass; the output manifest unchanged but for paths; the `quick` byte comparison again.
- **L6: website.** `site`, the web side of `pipeline`, the web registry and the web tests into `website/` and `tests/website/`; update `deploy.yml`, `_quarto.yml`, `.gitignore`, `check_gate.py`, `pages.yml`, the `.bat` files. Check: the build and web suites as far as R5 allows; gate checker output unchanged for pages not in `papers/`; CNAME and robots at the published root.
- **L7: old papers.** `source/` to `papers/legacy/`; repair paths; list red checks (R5). Not a gate.

## Touches
Every tracked path (archived briefs and decision history are not edited); by stage as above.

## Acceptance criteria
- Root holds only README.md, AGENTS.md, CNAME, robots.txt, .gitignore, .gitattributes and the folders `.github`, `.claude`, `data`, `literature`, `research`, `model`, `model-specs`, `results`, `papers`, `website`, `tests`, `project`.
- No file name appears twice outside the R3 exceptions (a script lists any); no byte-identical duplicate remains; one dataset type, one PDF type, one notes type, one results type per branch (the L1 table, checked at the end).
- The reference script finds no old path outside archived briefs and decisions; the depth-based path list is empty or every entry verified.
- After each stage the test suites, the gate checker and `check_agent_docs.py` pass (R5 excepted, listed); after L4 and L5 the `quick` output is byte-identical; moves are `git mv` (renames show in `git diff -M --stat`).
- The change report lists the local-only files to move by hand, every skill line changed and every red check.

## Checks to run
The reference script and the duplicate script, the suites (one `pytest` run per suite folder, in the background), the local Quarto build, `check_gate.py --all`, the legacy digest, the `quick` byte comparison.

## Out of scope
Changing file contents except paths and the renames of R3; deleting `model_v1` or `model_v2` (009c); editing archived briefs; history rewriting and LFS; the Actions workflow; rewriting any paper.

## Open questions
None for L1. At the L1 checkpoint: the call on every file the rules cannot settle and the default homes above.

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
