# 183: Build the split final run and the exact merge

- **Status:** ready; stage A merged 2026-11-27, 178c merged 2026-11-28 (stage B onward)
- **Agent:** 4
- **Needs:** none
- **Length:** 2
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
- **Done:** stages A (merged), B, C (proof) and D (workflow), on `brief/183-split-run-b` (pushed, c5055c5 plus this report). Actions run 46132231508 (quick split, quick unsplit, cmp, proof, fast): all green. Stage E (calibration at final size) not run: see NEEDS THE AUTHOR.
- **Next:** author: read the report, say merge or not; then `fast` on two CPU kinds on main (stage C of 170c style), and decide stage E.
- **Resume:** none.
- **State:** not merged.
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

## Change report, stage A
`out/split.py` (133 lines) and `test_split.py` (120 lines). The test file is `test_split.py`, not the design's `test_split_run.py`: `test_budget` pairs `split.py` with `test_split.py`. The unit list and header follow the design (`COMMON` fields compared; `unit` and `workers` not; `plan_sha256` among the non-plan units; `draws_sha256` among the o1e units). `check` refuses: wrong schema or header fields, a differing common field (named, with both units), a missing or unexpected unit (a gap or an overlap in the batch ranges shows as both), two partials of one unit with different bytes, another plan, differing draws hashes. The draw test uses the real `draw_theta`: slices concatenate to the full table, and a call with `n = b - a` is shown to differ. Not touched: `run.py`, `runner.py`, the workflow.
Checks after `git clean -fdx`: gate (real-repository test deselected, as in 170c) 16, data 97, tools 5, project 22, website suites pass (layout 40 skipped), model_v3 426 passed in 901 s, agent documents exit 0, tripwire PASS.

## Change report, stages B to D
**Built.** `run.py` is now `setup`, `plan_unit`, `point_unit`, `o1e_unit`, `merge`; `--unit plan|point:P|o1e-point|o1e:S:A:B`, `--plan-file`, `--merge DIR`, `--batch` (25), `--run-date`. A run without those flags is plan, then every unit in the canonical order, then the merge, in one process, with the partials through the file encoding: one code path. `run_point` lost the O1e block (O1e is its own unit); `S.breakeven_return` got `point=False` for a batch of draws; `SIZES['final']` has 200 O1e draws (author, 2026-11-27; `quick` and `smoke` unchanged); `workers` is no longer written into the output file (the validator does not read it). Stage B hardening of `out/split.py`, all four, each with a test: missing header fields are `SplitError`; `enc` takes numpy integers and bools and `dumps` turns a `TypeError` into `SplitError`; a batch below 1 is refused where the plan is built and where it is read; a string starting `f:` or `e:` is escaped with `e:` and round-trips. `parts` joined the compared header fields (no O1e units when `o1e` is not in `--parts`). Plan body: `named` as a list of pairs, because JSON sorts dict keys and the named schedules must keep the order the plan chose them (found by the first smoke run: the header refused it).
**Checkpoint of stage B (refactor changed nothing).** The unsplit smoke file from the new code equals the one from `main` before the refactor, same day: identical after removing `workers` (375,538 and 375,521 bytes; the 17 bytes are `workers`).
**Proof, local (2 cores), `-m split`, smoke, two points, batches of 2:** 4 passed in 21 min. Merge equals the unsplit file byte for byte; the O1e units run in reverse order and one point unit run again give byte-identical partials and the same merge; a changed seed, numerics setting or commit in a partial, a missing unit, and an invocation with another seed are each refused with the field named and no output written (the script exits `merge refused: ...`). **Proof on Actions** (job 140939709525, Intel Xeon Platinum 8573C): green in about 21 min.
**Actions run 46132231508** (branch, dispatch, `run_split_quick` and `run_split_proof`; `run_accept` off): the split run at quick size, the unsplit quick run, `cmp`: **IDENTICAL**, byte for byte. The partials were made on four CPU models and the unsplit run on a fifth kind of job:
| job | wall | CPU |
|---|---:|---|
| plan | 40 s | AMD EPYC 9V45 |
| o1e-point | 49 s | AMD EPYC 9V45 |
| point median_mid | 220 s | AMD EPYC 7763 |
| point max_mid | 176 s | AMD EPYC 9V74 |
| point median_low | 244 s | Intel Xeon 8573C |
| point median_high | 208 s | AMD EPYC 7763 |
| point min_mid | 216 s | AMD EPYC 7763 |
| merge | 24 s | AMD EPYC 9V74 |
| unsplit quick run (4 workers) | 1,034 s | Intel Xeon 8573C |
| fast | 27.6 min | AMD EPYC 7763 |
The split run's critical path was about 6 min (plan 40 s, a point 4 min, merge 24 s, plus queueing) against 17 min unsplit. `fast` is green on the AMD EPYC 7763 (no AVX512). No job passes `--final`; a test (`test_no_workflow_step_passes_the_final_flag...`) keeps it so. `run_final_size` now runs the split run at `--size final` (not run here).
**cap loss in pool workers (author's request, measured at smoke and quick).** No difference can be shown: at smoke, `cap` is empty for the point unit, the point roots and one batch at workers 1 and 2; at quick, the tornado alone (level 1 off) at max_mid and median_high records nothing at workers 1, so nothing is lost at workers 2. The shortfall records of quick come from level 1 (serial). Not a proof of absence: a point where the tornado or a root hits a cap was not found.
**Budgets.** `run.py` 120 to 215 lines, `split.py` 160 (tests 170), totals 6,773 and 4,616, reasons in `architecture.md`. The proof test is `test_split_proof.py` (marker `split`; excluded from accept.sh step 1, the `fast` job and `acceptance.md` row 1). Docs: `agent-code.md` and `acceptance.md` paragraphs. Checks after `git clean -fdx`: gate (real-repository test deselected) 16, data 97, tools 12, project 40, website suites pass, model_v3 447 passed (not converge, not split), agent documents 0, tripwire PASS.
**Not done, NEEDS THE AUTHOR.** (1) Stage E, the calibration at final size (one point unit and one 25-draw batch, timed, to replace the 1.4 and 2.5 factors of the design): it is hours of runner time and the workflow has no way to run only some units; propose an input `split_units` (a list) in a follow-up, or run the whole final-size split (32 jobs) as 181c. (2) The 20-concurrent-job limit and the 4-worker speed-up are still the design's estimates. (3) The merge job needs `needs` success of every unit: a failed unit means rerunning that job from the Actions page ("Re-run failed jobs"), then the merge; not exercised here.
