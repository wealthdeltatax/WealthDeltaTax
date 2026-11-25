# 044: Reorganise the repository into a vertical tree

- **Status:** umbrella and R1 (inventory) of the reorganisation, combined with 009c on 2026-11-24 and split into briefs 009c, 160c to 164c; ready now; Agent 2
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** nothing open (009c merged); the author's answers of 2026-11-24 (below). `docs/restructure/file-layout.md` is the 2026-11-18 design; where this brief differs, this brief wins
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
data/        every dataset: uk-wealth-tables (097r, 098r, 129r sources), rates (was Rates Data), jst (one jst_r6.json), wid, country-packs/GBR, input-register (inputs.json)
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

## Programme (author, 2026-11-24: combined with 009c, then split)
Sequential start, one parallel pair, sequential finish. Each stage is its own brief; the guru merges each to `main` (in the order they finish) and the next waits on it.

| step | brief | agent | depends on | does |
|---|---|---|---|---|
| R0 | 009c (merged) | 2 | none | retire `model_v1`, `model_v2`, `audit_d0`; keep the three data files v3 reads |
| R1 | 044c (this brief) | 2 | none (009c merged) | inventory only (below); the author and guru review it |
| R2 | 160c | 4 | 044c R1 | `data/`, `literature/`, `research/`: datasets, PDFs, notes; duplicates removed |
| R3 | 161c | 5 | 044c R1 | `website/`, `tests/website/`, `papers/legacy/` |
| R4 | 162c | 6 | 160c, 161c | `model/`, model-side `data/` and registry, `tests/model/`, `model/tools`, `model/studies` |
| R5 | 163c | 6 | 162c | `model-specs/` and `results/` from `docs/model-v3/` |
| R6 | 164c | 3 | 163c | `project/`, skills, final sweep, the acceptance of the whole move |

R2 and R3 run in parallel on different trees. Each rewrites only the references to the paths it moved; the shared files (`AGENTS.md`, `.gitignore`, STATUS, OVERVIEW) are left to R6 except for lines that would break the other stage's checks. The second of the two to merge rebases on `main`. R4 to R6 run one after another because they share the manifest, the tests and the `quick` byte check. `151c` and the rest of the speed-up work follow R6.

## How each stage proves it broke nothing (author concern, 2026-11-24)
No stage runs the 44-minute `quick` run or the 17-minute smoke run. Three cheap tiers instead; R1 builds the tools and takes the pre-move baseline once, before any move.
1. **Static, seconds, every commit.** The reference script (no old path left), the duplicate-name script, `check_agent_docs.py`, `python -m compileall`, an import of every module, and `pytest --collect-only` for each suite (an import or path error shows at collection).
2. **Path-rewrite proof, seconds.** `project/restructure/path_rewrite_proof.py`: for every file changed since the pre-move commit it applies the old-to-new path map (and the R3 renames) to the old content and compares with the new content; any other difference is reported as a non-path change. Pure renames must show as 100% similar (`git diff -M100%`). This is the check that nothing but paths changed.
3. **Tripwire, under 3 minutes.** `project/restructure/move_tripwire.py` records, before the move (R1, baseline file `move-tripwire-baseline.json`), the hashes of: the `inputs.json` bytes, the legacy digest test result, a rebuild of the GBR pack compared with the committed pack, and a household evaluation at 20 paths for `median_mid` and `min_mid` under both fund settings (the headline arrays M1a, M2 and P6 and the list of output ids; seeded, deterministic). After each stage it recomputes and compares; any difference stops the stage. It must run in under 3 minutes on one process.
4. **Suites, in the background.** The test suites (about 10 minutes in all: model 7 to 9, the rest under 2) run in the background while the agent writes the report; a stage is not pushed as green until they finish, but the agent is not waiting on an hour-long run.
5. **The full `quick` byte comparison, once, only if 057c has merged** (it is paused; otherwise skipped and said so, the tiers above carry the move). After R5 (specs and results) and at the end of R6, run in the background or overnight by the author or an agent with nothing else to do; it confirms the tiers above and blocks only the closing of the programme, not the individual stage merges.

## R1: inventory and checks (this brief's own work; no moves)
Three deliverables, written to `docs/restructure` and `pipeline` before the move: (1) `file-layout-map.md` and `pipeline/path_refs.py`; (2) the checks above, `path_rewrite_proof.py` and `move_tripwire.py`, with the baseline file, taken at the merged state of 009c; (3) the review table. The map holds: for every tracked file or folder its old path, new path and, under R3, new name; the duplicate report (byte-identical, same name different); every file that references an old path (file, line); the depth-based path list (hazard 1); the local-only list (hazard 4); the files the rules cannot settle, each with the default above. **Checkpoint: the guru and author review the table before 160c and 161c start.**

## Touches
R1 writes the map and the script only; nothing moves. The stage briefs name their own Touches.

## Acceptance criteria (the whole programme, checked at R6)
- Root holds only README.md, AGENTS.md, CNAME, robots.txt, .gitignore, .gitattributes and the folders `.github`, `.claude`, `data`, `literature`, `research`, `model`, `model-specs`, `results`, `papers`, `website`, `tests`, `project`.
- No file name appears twice outside the R3 exceptions (a script lists any); no byte-identical duplicate remains; one dataset type, one PDF type, one notes type, one results type per branch.
- The reference script finds no old path outside archived briefs and decisions; the depth-based path list is empty or every entry verified.
- After each stage the static checks, the path-rewrite proof, the tripwire, the test suites, the gate checker and `check_agent_docs.py` pass (R5 excepted, listed); the full `quick` output is byte-identical once, after R5, and again at R6; moves are `git mv`.
- The change reports list the local-only files to move by hand, every skill line changed and every red check.

## Checks to run
The tiers above: reference and duplicate scripts, `compileall`, collection, `path_rewrite_proof.py`, `move_tripwire.py`, the suites (one `pytest` run per suite folder, in the background), the local Quarto build, `check_gate.py --all`.

## Out of scope
Changing file contents except paths and the R3 renames; history rewriting and LFS; the Actions workflow (after R6); rewriting any paper; the speed-up briefs.

## Open questions
None for R1. At its checkpoint: the call on every file the rules cannot settle and the default homes above.

## R1 checkpoint rulings (author, 2026-11-24)
The map's 13 review cases are settled as the map's defaults, with these changes. The map files, the RULES table in `pipeline/path_refs.py` and the review table are regenerated to match (**R1 round 2, the agent's next block**); the regenerated map is then the authority for 160c to 164c.
1. **Case 3, research outputs.** The derived tables and scripts of the parameter-map notes (099r to 104r, 131r, 145r, 146r) go to `research/tables/<NNNr-slug>/` and `research/scripts/`, not `results/` and `model/studies/`. `results/` holds model run outputs only; `model/` only model code. Source-table folders 097r, 098r and 129r still go to `data/uk-wealth-tables/`.
2. **Case 8, bibliography.** `references.bib`, `internal.json` and `bib_to_json.py`'s output `references.json` go to `literature/` (flat, unique names); the script `bib_to_json.py` goes with the website build scripts and reads them from there. Every other registry file follows the map (`inputs.json`, `inputs-display.yml`, `metrics.json` to `data/input-register/`; the rest to `website/registry/`).
3. **Case 13, pinned files.** The four stale citations (`registry/inputs.json` line 568, `legacy_digest.json` line 3, the pack `manifest.json` line 104, `internal.json` line 2, now in `literature/`) keep their bytes. `path_refs.py --check` allow-lists exactly these lines; they are refreshed at the next real re-pin of the register. Rewriting any other line of a pinned file is stop-and-report.
4. **The other defaults stand, with four changes:** (a) `check_agent_docs`, `build_skills`, `path_refs` go to `project/tools/` (not `project/housekeeping/`); (b) the five agent guides become `agent-code.md`, `agent-guru.md`, `agent-research.md`, `agent-web.md`, `agent-writing.md` (R6 rewrites the skills and every active reader); (c) tests follow the code they test: `tests/model`, `tests/website`, `tests/project` (the `hooks` suite is split by what each test file tests); (d) `INDEX.md` becomes `readable-copies-index.md` (it differs from Quarto's `index.md` only by case); the pack's own `source/jst_r6.json` stays as an exempt loader file, and Quarto's `index.md` and `index.qmd` are exempt as tool-mandated.
The R3 name exceptions gain: `index.md` and `index.qmd` (Quarto), the pack's `jst_r6.json`.

## Implementation notes
<!-- progress:start -->
- **Done:** R1 round 2: `RULES` in `pipeline/path_refs.py` follows the checkpoint rulings; the four map files are regenerated (1104 files, all flag S, 77 renames, 7 duplicates); the review table shows all 13 cases settled with the ruling stated. Earlier: R1 (inventory, `path_rewrite_proof.py`, `move_tripwire.py`, baseline taken at 817dccc).
- **Next:** the guru merges R1; then 160c and 161c (parallel) read the regenerated map as their authority.
- **Decisions:** the 097r, 098r extractor scripts go to `research/scripts/` with the other research scripts (the ruling names only 099r to 146r; flagged in case 3). The four `docs/restructure/` map files and `path_refs.py` go to `project/restructure/` and `project/tools/` (the two new CSVs were missing from the restructure rule and fell to `website/notes/`; fixed). `--check` allow-lists the four pinned lines by file, line and token, and matches the file at its old or new path.
- **Gotchas:** the tripwire needs a full-history clone (shallow gives `FAIL pack`; logged in the friction log). `path_refs.py --check` still exits 1 because nothing has moved; it prints no pinned line. The hooks suite splits into `tests/website/hooks/` (5 tests, conftest, fixtures), `tests/project/tools/` (build_skills, check_agent_docs) and `tests/model/tools/` (run_suites); `run_suites.py` and the hooks conftest find suites and fixtures by path, so 162c and 164c rewrite them.
- **Resume:** `python pipeline/path_refs.py --map`; a stage runs `python docs/restructure/path_rewrite_proof.py --base <pre-stage commit> --head HEAD` and `python docs/restructure/move_tripwire.py`.
- **Not run:** the full `quick` byte comparison (057c not merged); the local Quarto build and the test suites (nothing moved, no code changed).
- **State:** R1 round 2 done, awaiting merge (`brief/044-inventory`, pushed once).
<!-- progress:end -->

Change report
- Task: 044c R1, inventory and checks (no file moved, no content changed)
- Files changed (all new): `pipeline/path_refs.py` (map, reference, depth and local-only finders, reference check); `docs/restructure/file-layout-map.md` (review table, rule table, duplicates, renames, pinned files, depth, local-only, Windows length); `file-layout-map.csv`, `file-layout-references.csv`, `file-layout-depth.csv` (per-file, per-line data); `path_rewrite_proof.py`; `move_tripwire.py`; `move-tripwire-baseline.json`; this brief's notes
- What is different now: the whole move is specified file by file: 1096 files (384 settled, 712 default), 78 R3 renames, 8 R4 duplicates; 2,471 lines in 330 files name an old path; 472 lines build a path from their own location; 13 local-only files listed with their new homes
- New or changed interfaces: `python pipeline/path_refs.py --map|--refs|--depth|--dups|--local|--check|--new OLD`; `python docs/restructure/path_rewrite_proof.py --base C [--head H] [--allow F] [--show N]`; `python docs/restructure/move_tripwire.py [--baseline] [--only a,b]`
- Acceptance criteria: map covers every tracked file, no unmapped file, no repeated new name outside the exemptions: met. Reference, depth and local-only lists: met. Proof script: met, exercised on a full simulated move (not in the repo). Tripwire under 3 minutes with baseline at the merged 009c state: met (79 s; legacy digest, inputs.json bytes, pack rebuild byte-identical, household evaluation at 20 paths for median and min, safe and market). Review table for the checkpoint: met (13 cases)
- Deviations from the brief: the proof's folder rewriting only applies where every file of a folder moves by one rule; split folders (`docs/model-v3`, `pipeline`, `registry`) are rewritten per file, so a line naming such a folder is reported as `changed` for the stage to settle by hand
- Risks / follow-ups: case 13 (pinned files naming old paths) needs the author; the default homes (712 files) stay open until the checkpoint; the tag `legacy-models-2026-11` is still to be pushed by the author (proxy 403)
- Instruction friction: none new in this task (the pytest-per-directory `conftest.py` clash was logged earlier)
- Verification: `check_agent_docs.py` clean; `compileall` clean; all 10 suites pass on the branch (model_v3 408 passed in 6:32; layout 40 skipped as before); tripwire PASS twice; proof run at HEAD (nothing moved) shows 1079 pending, 0 changed
- Overview sections likely needing an update: none until a stage moves files (the guru updates the layout section at R6)
- Commit / branch: see the pushed head of `brief/044-inventory`; not merged (R1 needs the author and guru review at the checkpoint)

Change report (R1 round 2)
- Task: 044c R1 round 2, regenerate the file-layout map to the author's checkpoint rulings (nothing moved)
- Files changed: `pipeline/path_refs.py` (RULES, exempt names, pinned-line allow-list, search exclusions); `docs/restructure/file-layout-map.md`, `file-layout-map.csv`, `file-layout-references.csv`, `file-layout-depth.csv` (regenerated); this brief's progress block; `docs/agents/friction-log.md` (one entry)
- What is different now: all 13 review cases settled. Research tables and scripts go to `research/tables/<NNNr-slug>/` and `research/scripts/`; `references.bib`, `internal.json`, `references.json` to `literature/`; `check_agent_docs`, `build_skills`, `path_refs` to `project/tools/`; guides to `project/agents/agent-*.md`; tests to `tests/model`, `tests/website`, `tests/project` (hooks suite split); `INDEX.md` to `readable-copies-index.md`; `index.md`, `index.qmd` and the pack's `jst_r6.json` exempt (the pack copy is no longer a duplicate: 7 duplicates, was 8). 1104 files, 77 renames, 2599 old-path lines in 333 files
- New or changed interfaces: `path_refs.py --check` skips exactly the four pinned lines (`PINNED_ALLOWED`); the four generated map files are no longer searched for old paths (they held 5,600 of the earlier 8,208 hits)
- Acceptance criteria: map covers every tracked file, no name collision outside the exemptions, four pinned lines allow-listed and no other pinned line named: met. Proof on a scratch worktree with the new map: PASS (477 moved, 620 path-only, 7 removed, 0 changed, 0 added, 0 name collisions); worktree deleted. Tripwire equals `move-tripwire-baseline.json` (80 s); baseline not retaken
- Deviations from the brief: two small additions the rulings did not name: `file-layout-references.csv` and `file-layout-depth.csv` go to `project/restructure/`; the 097r and 098r extractor scripts go to `research/scripts/`
- Risks / follow-ups: `run_suites.py` and the hooks conftest depend on the old suite paths (162c, 164c); `path_refs.py --check` exits 1 until the stages have moved the files; the tripwire needs full git history
- Instruction friction: one entry in `docs/agents/friction-log.md` (tripwire fails in a shallow clone)
- Verification: `check_agent_docs.py` clean; `path_refs.py --map` and `--check` run; proof PASS; tripwire PASS after deepening the clone; suites not run (no code or test changed)
- Overview sections likely needing an update: none until a stage moves files
- Commit / branch: `brief/044-inventory`, pushed once; not merged (the guru merges R1)
