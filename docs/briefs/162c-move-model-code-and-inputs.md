# 162: Move the model code and its inputs (reorganisation R4)

- **Status:** draft; released after 161c (merged) and 165c (merged); Agent 6
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 160c, 161c and 165c merged (done 2026-11-25); no other branch open
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `model_v3/pack/build_gbr.py`; `tests/model_v3/`; `pipeline/validate_outputs.py`; `docs/restructure/rehearsal-report.md` (the 162c section and the trap) and `docs/restructure/rehearsal-fixes.patch` (the `# ===== stage 162c` hunks, built on the pre-160c tree: use as a guide, not a patch to apply)

## Goal
The model is code only under `model/`; everything it reads is under `data/`; its tests are under `tests/model/`; and the tripwire equals its pre-move baseline.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `model_v3` to `model/model_v3` (import name kept); the model-side pipeline scripts (`build_inputs`, `build_metrics`, `validate_outputs`, `run_suites`, shared helpers per the L1 table) to `model/tools/`; the study drivers (`docs/model-v3/**/*.py`) to `model/studies/` with unique names.
- The country pack to `data/country-packs/GBR/` (its own file names stay); `registry/inputs.json` and the model-side registry files to `data/input-register/`; the pack builder reads `data/jst/` and `data/wid/` (009c).
- The model tests (`tests/model_v3`, `tests/data`) to `tests/model/`.
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
`model_v3/`, `pipeline/` (model side), `registry/` (model side), `tests/model_v3/`, `tests/data/`, `docs/model-v3/**/*.py`, the pack, readers of those paths (docs, workflows).

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
- **Done:** claimed on 2026-11-25 (author asked for 162c; 167c, which would replace 162c to 164c, has no branch yet). Branch cut from `main` at 2386501.
- **Next:** work in a scratch copy of this clone (`path_refs.py --apply` refuses this repository): apply only the 162c rows (`model/`, `data/country-packs/`, `data/input-register/`, `tests/model/`), then the 162c hunks of the rehearsal patch as a guide, pinned lines, proof `Rewriter`, checks.
- **Decisions:** 163c and 164c rows stay put (their map rows are held to identity in the apply, so their old paths are not rewritten here).
- **Gotchas:** if Agent 6 starts 167c, one of the two must stop: both move the same tree.
- **Resume:** `git checkout brief/162-move-model-code-and-inputs`.
- **Not run:** everything.
- **State:** block 0 done
<!-- progress:end -->
