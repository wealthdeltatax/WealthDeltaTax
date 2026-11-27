# 183: Build the split final run and the exact merge

- **Status:** stage A ready now (new `split.py` and its tests only; do not edit `run.py`, `runner.py` or the workflow); stages B onward wait for 154c and 178c
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 182c (design), 154c and 178c (both change `run.py`; build on top of them, not beside them)
- **Read:** `results/split-run/design.md` (the stage plan at its end); `model/model_v3/run.py`; the design's named seams; `tests/model/model_v3/test_smoke.py`

## Goal
Build what 182c designed: partial files from `run.py`, a merge module, a matrix job and a merge job in the workflow. A split run at smoke size merges to a file byte-identical to the unsplit run.

## Design
The stages are the design note's. Each stage ends with a push and its cheapest check; the stop rule: if the merged file differs from the unsplit one in a single byte at smoke size, stop and report the first differing cell, do not patch the comparison.

## Touches
Completed from 182c; expected: `model/model_v3/run.py` (partial output switch), a new `model/model_v3/merge.py` (or `out/merge.py`) with its LAYER row, `tests/model/model_v3/` (merge tests, the split-equals-unsplit test), `.github/workflows/model-checks.yml` (the `run_final_size` jobs; reviewer: web), `model-specs/architecture.md` (budget rows), `results/speedup/ledger.md` is not touched (this is not a speed-up).

## Acceptance criteria
- Smoke size: split, merge, byte-identical to unsplit, in two batch orders and with one shard rerun (test).
- A mismatched header (seed, numerics setting, SHA) is refused by the merge with a message (test).
- One Actions run of the split jobs at `quick` size end to end, merged file validates and equals the unsplit `quick` file; run id and wall time reported.
- No run uses `--final`; all suites and the tripwire pass.

## Out of scope
The final-size run itself (181c); any speed-up.

## Open questions
From 182c.

## Implementation notes
<!-- progress:start -->
- **Done:** stage A. `model/model_v3/out/split.py` (hex-float encoding, header, draw slice and hash, `expected` units, `check` with its refusals) and `tests/model/model_v3/test_split.py` (17 tests, no model run). LAYER row `out/split: 5`; budget rows in `architecture.md` (code 140, tests 130; totals 6,650 and 4,548). Pushed on `brief/183-split-run`.
- **Next:** stage B (needs 154c and 178c merged: it edits `run.py`; build on top of them). Not started.
- **Resume:** none.
- **State:** stage A done; not merged.
<!-- progress:end -->

## Author answers on the 182c design (2026-11-27)
- Q1: **the `final` preset uses 200 O1e draws** (`SIZES['final']`, one number in `run.py`, changed in this brief; `quick` and `smoke` keep their draws). The workflow's final-size jobs assume 200.
- Q2 to Q7: proposals accepted as written in `results/split-run/design.md` (guru reading, labelled for challenge): stop writing `workers` into the output file (confirm the validator does not read it); measure the `cap` loss in pool workers at smoke and report; batch size 25 draws (20 if calibration says so); no level 1 cache in the merge; no per-point level 1 sharding here; the proof job is a manual dispatch input `run_split_proof`.

## Change report, stage A
`out/split.py` (133 lines) and `test_split.py` (120 lines). The test file is `test_split.py`, not the design's `test_split_run.py`: `test_budget` pairs `split.py` with `test_split.py`. The unit list and header follow the design (`COMMON` fields compared; `unit` and `workers` not; `plan_sha256` among the non-plan units; `draws_sha256` among the o1e units). `check` refuses: wrong schema or header fields, a differing common field (named, with both units), a missing or unexpected unit (a gap or an overlap in the batch ranges shows as both), two partials of one unit with different bytes, another plan, differing draws hashes. The draw test uses the real `draw_theta`: slices concatenate to the full table, and a call with `n = b - a` is shown to differ. Not touched: `run.py`, `runner.py`, the workflow.
Checks after `git clean -fdx`: gate (real-repository test deselected, as in 170c) 16, data 97, tools 5, project 22, website suites pass (layout 40 skipped), model_v3 426 passed in 901 s, agent documents exit 0, tripwire PASS.
