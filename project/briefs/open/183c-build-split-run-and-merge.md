# 183: Build the split final run and the exact merge

- **Status:** hold; stage A done and pushed on `brief/183-split-run` (`split.py`, 17 tests), not merged; stages B onward wait for 154c and 178c (they edit `run.py`)
- **Agent:** 4
- **Needs:** 183a, 154c, 178c
- **Length:** 2
- **Row:** 183a | agent 4 | review | needs none | length 1 | Split run, stage A: split.py (encode, decode, merge checks) and its tests
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
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->

## Stage B hardening (guru review of stage A, 2026-11-27)
Stage A meets its checkpoint (38 tests re-run green). Stage B makes these four changes to `out/split.py`, each with a test in `test_split.py`:
1. `check` raises `SplitError`, not a bare `KeyError`, for a header with no `kind`; also for any other missing header field.
2. `enc` handles numpy integer and bool scalars (as plain ints and bools) or raises `SplitError`; never a `TypeError` from `json`.
3. A `batch` of 0 or less is refused where the plan is built (`SplitError`, test).
4. A string that starts with `f:` is either forbidden in a body (`dumps` raises `SplitError`) or escaped on encode and unescaped on decode; pick one and test the round trip. No body writes such a string today.
Budget: `split.py` is 133 of 140 lines; raise the row in `architecture.md` if these need more, with the reason in the change report.

## Author answers on the 182c design (2026-11-27)
- Q1: **the `final` preset uses 200 O1e draws** (`SIZES['final']`, one number in `run.py`, changed in this brief; `quick` and `smoke` keep their draws). The workflow's final-size jobs assume 200.
- Q2 to Q7: proposals accepted as written in `results/split-run/design.md` (guru reading, labelled for challenge): stop writing `workers` into the output file (confirm the validator does not read it); measure the `cap` loss in pool workers at smoke and report; batch size 25 draws (20 if calibration says so); no level 1 cache in the merge; no per-point level 1 sharding here; the proof job is a manual dispatch input `run_split_proof`.
