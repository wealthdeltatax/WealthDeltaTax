# 163: Split the model documents into specs and results (reorganisation R5)

- **Status:** done, merged 2026-11-25
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 162c merged
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `model-specs/outputs.yml` and its readers; `docs/restructure/rehearsal-report.md` (the 162c and 163c sections)

## Goal
`docs/model-v3/` (188 files) is split by type: what the model should do goes to `model-specs/`; every run report and its csv go to `results/<study>/` with unique names.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- Specifications (architecture, acceptance, metrics, the outputs manifest `outputs.yml`, input-register docs, country-pack spec, drivers, design notes, `what-we-know`) to `model-specs/`.
- Reports and csv of each study (death-phases, feasibility-map, household-arm-run, -validation, -lien, -paths, f1-diagnostic, f1-household, cell-baseline, tornado, returns, run-cost, wealth-ratio-diagnostic, of1-ck1, and the others) to `results/<study>/`, each file renamed under R3 so no name repeats (phase, fund and variant in the name: `f1-phases06-safe-grid.csv`). Every reader (manifest, tests, drivers in `model/studies/`, docs) rewritten.
- Rule of thumb for the call on each file: a document that says what the model is meant to do is a spec; a file that reports what a run produced is a result; the script that makes it is a study driver (already moved).
- Check: the 044c tiers; the output manifest unchanged but for paths. At the end, one full `quick` run in the background (44 minutes) compared byte for byte with the pre-move reference; it blocks closing the programme, not this merge.

## Added from the rehearsal (165c, 2026-11-25)
- Only three pinned lines reach this stage (`inputs.md` line 145, the `outputs.yml` shortcodes comment, the `inputs.md` readers); they keep their old text (162c lists them); nothing else in `model-specs/` or `results/` is read by code beyond depth and constructed paths.
- A study folder that holds both a driver and its outputs is split: the driver is in `model/studies/<study>` (162c), the reports and csv go to `results/<study>/`. A variable or `sys.path` line naming the old folder cannot be rewritten as one path: `sys.path` means the code folder; `VAR / 'file'` becomes that file's own new path. Check every driver for output paths it writes.
- Use `git clean -fdx` before the stage's final run; throwaway trees built by tests keep their paths.
- The 163c section of `rehearsal-fixes.patch` is a guide only (it is built on the pre-160c tree).

## Touches
`docs/model-v3/` (all), `model/studies/` (paths), tests and docs that read them.

## Acceptance criteria
- `model-specs/` holds only specifications and `results/` only run outputs; no name repeated in either.
- Suites and `check_agent_docs.py` pass; manifest unchanged but for paths; tripwire and path-rewrite proof clean; the `quick` comparison reported when it finishes.

## Out of scope
Changing any number or text except paths and R3 names; project documents and skills (164c).

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:** 198 files of `docs/model-v3/` moved by `path_refs.py --apply --only docs/model-v3/` on a scratch clone and merged back: 189 by map (170 pure renames, 15 path-only edits, 4 R4 duplicates removed) plus 8 files the map lacks (the 166c `reserve-diagnostic` csv and report) to `results/reserve-diagnostic/`; `model-specs/` 26 entries, `results/` 18 studies. 65 constructed `ROOT / 'docs' / 'model-v3' / ...` paths in `model/studies`, `model/tools`, `model/model_v3/pack/build_gbr.py` (line 24) and the tests rewritten. `docs/model-v3/` is gone.
- **Next:** author merges; 164c (project, skills, final sweep) follows; the `quick` byte comparison (44 min) still blocks closing the programme, not this merge.
- **Decisions:** `--only PREFIX` added to `path_refs.py --apply` and to `path_rewrite_proof.py` (a stage scope; no check weakened). `PINNED_ALLOWED` follows the two pinned spec files to `model-specs/` and drops `build_gbr.py` line 24 (code, now names `results/`). The 166c files have no map row: placed by the study rule (`results/reserve-diagnostic/`); the guru adds rows.
- **Gotchas:** the apply rewrites the pinned tokens inside `path_refs.py` and the candidate lists of `move_tripwire.py`: both restored by hand. A shallow clone fails the tripwire pack check.
- **Resume:** `bash` of the scratch recipe is in the suggestions entry; nothing left to do in this stage.
- **Not run:** the `quick` byte comparison; Quarto build; `layout` (40 skipped as in the baseline).
- **State:** done, awaiting merge.
<!-- progress:end -->


Change report
- Task: 163c split `docs/model-v3/` into `model-specs/` and `results/<study>/`
- Files changed: 194 renames and 4 removals (R4) from `docs/model-v3/`; 101 files edited (readers in `model/studies`, `model/tools`, `tests/model`, research notes, briefs, STATUS and agent docs: paths only); `pipeline/path_refs.py` (`--only`, pinned list), `docs/restructure/path_rewrite_proof.py` (`--only`); friction log, brief suggestions
- What is different now: specifications live in `model-specs/` (26 entries), every run report and csv in `results/<study>/` (18 studies); `docs/model-v3/` no longer exists
- New or changed interfaces: `path_refs.py --apply ROOT --only PREFIX`; `path_rewrite_proof.py --only PREFIX`
- Acceptance criteria: only specs in `model-specs/`, only run outputs in `results/`, no repeated name in either (met: checked for duplicate file names across both); suites pass (met: model data 103, gate 17, tools 5, model_v3 408, website 201 passed 41 skipped, hooks 16); `check_agent_docs.py` clean (met); tripwire PASS (met); proof on the stage: 170 moved, 15 path-only, 4 removed, 1 changed (`model-specs/inputs.md` line 145, the declared pinned line), 8 added (the 166c files, no map row); manifest unchanged but for paths (met: tripwire evaluation hashes equal); `quick` comparison not yet run (blocks closing the programme, not this merge)
- Deviations from the brief: scope options added to two tools; the 166c files placed by rule
- Risks / follow-ups: `docs/lane-plan.html` line 273 and the briefs 044c/163c still name `docs/model-v3/` (they describe the move; the guru updates); the map needs rows for the 8 added files
- Instruction friction: one entry added
- Verification: tripwire, tests above, proof, `--check` filtered to this stage (24 remaining tokens named `model-v3`, all pinned, prose of the move, or archive file names that contain "model-v3"), a markdown link scan (91 broken links, identical to before the move)
- Overview sections likely needing an update: the file-layout section of OVERVIEW.md (model-specs, results)
- Commit / branch: see push, `brief/163c-move-model-specs-and-results`
