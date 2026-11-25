# 162: Move the model code and its inputs (reorganisation R4)

- **Status:** done, merged 2026-11-25
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 160c, 161c and 165c merged (done 2026-11-25); no other branch open
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `model/model_v3/pack/build_gbr.py`; `tests/model/model_v3/`; `model/tools/validate_outputs.py`; `docs/restructure/rehearsal-report.md` (the 162c section and the trap) and `docs/restructure/rehearsal-fixes.patch` (the `# ===== stage 162c` hunks, built on the pre-160c tree: use as a guide, not a patch to apply)

## Goal
The model is code only under `model/`; everything it reads is under `data/`; its tests are under `tests/model/`; and the tripwire equals its pre-move baseline.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `model_v3` to `model/model_v3` (import name kept); the model-side pipeline scripts (`build_inputs`, `build_metrics`, `validate_outputs`, `run_suites`, shared helpers per the L1 table) to `model/tools/`; the study drivers (`docs/model-v3/**/*.py`) to `model/studies/` with unique names.
- The country pack to `data/country-packs/GBR/` (its own file names stay); `data/input-register/inputs.json` and the model-side registry files to `data/input-register/`; the pack builder reads `data/jst/` and `data/wid/` (009c).
- The model tests (`tests/model/model_v3`, `tests/model/data`) to `tests/model/`.
- Rewrite imports, config, the manifest, test paths, `accept.sh`, the run commands; check every depth-based path (hazard 1).
- Checks: the 044c tiers (static, path-rewrite proof, tripwire against the R1 baseline, suites in the background); no `quick` run in this stage.

## Rulings from the rehearsal (165c, 2026-11-25)
- **Pack folder** is `data/country-packs/GBR/` (the loader needs folder name equal to the manifest country); the map is updated.
- **Pinned bytes stay unchanged** (the pack tree and `inputs.json` are hashed): `NOTICE.md`, the three NOTICE strings in `build_gbr.py`, the pack `manifest.json` strings, `inputs.md` line 145 (source of the pinned `inputs.json` line 568) and the `outputs.yml` shortcodes comment (hashed in `manifest_sha256`) keep their old text. The author allow-listed the NOTICE lines on 2026-11-25; add the rest to the tripwire's expected list in the same way, and list every such line in the report (stop-and-report if the tripwire needs more than an allow-list).
- **Shared rewriter in the proof:** `path_rewrite_proof.py` takes `path_refs.Rewriter(...).text` in place of its own regular expression (the rehearsal showed the two disagreed: 198 false changes). This is the one allowed change to a check in this programme; show before and after counts.
- **Throwaway trees in tests** (`run_suites` test, gate conftest f-strings) keep their own paths; the automatic rewrite must not touch them.
- **Before the stage's final run** use `git clean -fdx` or a fresh checkout: empty old folders hide missing paths.
- **Run commands** to be rewritten: see the `Resume` and `Gotchas` lines of the 165c progress block.

## Touches
`model_v3/`, `pipeline/` (model side), `registry/` (model side), `tests/model/model_v3/`, `tests/model/data/`, `docs/model-v3/**/*.py`, the pack, readers of those paths (docs, workflows).

## Acceptance criteria
- Tripwire equal to the baseline, path-rewrite proof clean, digest and gate hash unchanged, all model suites pass.
- No model file renamed except under R3; no number changed.
- Depth-based path list checked and empty; local-only files listed.

## Out of scope
Specs and results (163c); the website; skills and shared files.

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:** all of 162c on the branch (rebased on `main` fb2770b): `model/model_v3`, `model/tools`, `model/studies`, `data/country-packs/GBR`, `data/input-register`, `tests/model`; imports, depth lines, constructed paths, pinned lines, proof `Rewriter`, prose citations of `model_v3/`.
- **Next:** author review and merge; then 163c (specs and results) and 164c.
- **Decisions:** 163c and 164c rows stay put (held to identity): study drivers read and write their data at `docs/model-v3/<study>` through a `DATA` constant until 163c; `check_gate` default `model_v3/OUTPUTS/outputs.json` (generated, untracked, not in the map) left as is.
- **Gotchas:** `git clean -fdx` before the final run (done); 163c must rewrite the `DATA` chains and the `docs/model-v3/inputs.md`, `metrics.md`, `outputs.yml` readers.
- **Resume:** `git checkout brief/162-move-model-code-and-inputs`.
- **Not run:** `quick` (out of scope), `tests/website` and `tests/project` suites (collect-only passes, 791 tests), Quarto build.
- **State:** all blocks done, pushed

Change report
- Task: brief 162c, move the model code and its inputs (R4)
- Files changed: 159 renames and about 75 edited files: model code, tools and 38 study drivers under `model/`; pack under `data/country-packs/GBR/`; register under `data/input-register/`; tests under `tests/model/`; `path_refs.py` (rules, `PINNED_ALLOWED`), `path_rewrite_proof.py` (shared rewriter), `move_tripwire.py` (paths), `website/build/hooks.py` (register paths), `AGENTS.md`, `START_HERE.md`, `docs/agents/code.md` (`model/model_v3`).
- What is different now: the model is code only under `model/`; its data sit under `data/`; its tests under `tests/model/`. Import name `model_v3` kept; the import root is `model/`. No model file renamed except under R3; no number changed.
- New or changed interfaces: run `pytest tests/model/<suite>`; tools at `model/tools/*.py`; `run_suites.py` and `G5_TEST_DIRS` find both test layouts; study drivers at `model/studies/<study>/`.
- Acceptance criteria: tripwire PASS (inputs, legacy digest, pack rebuild byte-identical, 4 evaluation cases): met. Digest and gate hash unchanged: met (tripwire). Model suites: data 103, gate 17, tools 5, model_v3 408 passed, after `git clean -fdx`: met. `check_agent_docs.py` clean: met. Path-rewrite proof (stage map, base `origin/main`, 163c/164c rows held to identity): 504 moved, 40 path-only, 0 removed, 72 changed (the declared depth, import root and DATA edits, all path terms), before and after the Rewriter change identical; the proof still prints FAIL without an `--allow` list because it lists those 72 and the 499 files of earlier stages as "added": partly met, see risks. Depth list: every `parents[k]`, `.parent` chain, `HERE` and `DIR` of the moved files checked, compileall and collect-only pass; list of unresolved depth lines is empty.
- Deviations from the brief: pinned-line list is longer than the brief's (see below); the `--check` output is cut at 50 lines (hid the rest), not changed.
- Pinned lines kept with their old text (all allow-listed in `PINNED_ALLOWED`): `data/country-packs/GBR/NOTICE.md:13`, `model/model_v3/pack/build_gbr.py:24,193,217` (NOTICE and manifest strings), pack `manifest.json:104`, `docs/model-v3/inputs.md:145`, `docs/model-v3/outputs.yml:3` (shortcodes comment), plus the existing `inputs.json:568`, `legacy_digest.json:3`, `registry/internal.json:2`. The allow-list sufficed.
- Risks / follow-ups: (1) the proof has no `--allow` file for the 72 declared edits, so it does not print PASS by itself; (2) `check_gate` default `model_v3/OUTPUTS/outputs.json` is a generated untracked path, left; (3) `file-layout-map.md` still says "four" pinned lines; (4) the prose sweep of `pipeline/`, `tests/` and others stays with 164c; (5) 163c must move the `DATA` constants with the data.
- Instruction friction: `path_refs.py --check` truncates its output at 50 lines; the brief did not say where the proof's before and after counts come from (used a stage map).
- Verification: as in the criteria; not run: `quick`, `tests/website`, `tests/project`, Quarto build.
- Overview sections likely needing an update: the repository layout section (model and data paths).
- Commit / branch: branch `brief/162-move-model-code-and-inputs`.
<!-- progress:end -->
