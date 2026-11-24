# 162: Move the model code and its inputs (reorganisation R4)

- **Status:** draft; released after 160c and 161c have merged; Agent 6
- **Author/date:** K. Ogata with the guru, 2026-11-24
- **Depends on:** 160c and 161c merged; no other branch open
- **Read:** `docs/briefs/044c-file-layout-move.md` (rules, tree, hazards); `docs/restructure/file-layout-map.md` (the reviewed table from R1); `model_v3/pack/build_gbr.py`; `tests/model_v3/`; `pipeline/validate_outputs.py`

## Goal
The model is code only under `model/`; everything it reads is under `data/`; its tests are under `tests/model/`; and a `quick` run reproduces the pre-move reference byte for byte.

Rules, target tree and hazards: `docs/briefs/044c-file-layout-move.md` (R1 to R5, the tree, hazards 1 to 10); they apply here. One stage, one session, one push per block; any content change beyond paths and the R3 renames is stop-and-report; suites run in the background, never piped.

## Design
- `model_v3` to `model/model_v3` (import name kept); the model-side pipeline scripts (`build_inputs`, `build_metrics`, `validate_outputs`, `run_suites`, shared helpers per the L1 table) to `model/tools/`; the study drivers (`docs/model-v3/**/*.py`) to `model/studies/` with unique names.
- The country pack to `data/country-pack-GBR/` (its own file names stay); `registry/inputs.json` and the model-side registry files to `data/input-register/`; the pack builder reads `data/jst/` and `data/wid/` (009c).
- The model tests (`tests/model_v3`, `tests/data`) to `tests/model/`.
- Rewrite imports, config, the manifest, test paths, `accept.sh`, the run commands; check every depth-based path (hazard 1).
- Before any move, produce and keep the pre-move `quick` reference file (057c command); after the move the same command (new path) writes a byte-identical file; the legacy digest and the `inputs.json` hash are unchanged; model suites pass.

## Touches
`model_v3/`, `pipeline/` (model side), `registry/` (model side), `tests/model_v3/`, `tests/data/`, `docs/model-v3/**/*.py`, the pack, readers of those paths (docs, workflows).

## Acceptance criteria
- `quick` output byte-identical; digest and gate hash unchanged; all model suites pass.
- No model file renamed except under R3; no number changed.
- Depth-based path list checked and empty; local-only files listed.

## Out of scope
Specs and results (163c); the website; skills and shared files.

## Open questions
None; the agent flags any call the rules cannot settle.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** not started
<!-- progress:end -->
