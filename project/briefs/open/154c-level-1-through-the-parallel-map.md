# 154: Level 1 through the parallel map, and `--workers` in the Actions jobs

- **Status:** ready after 151c merges
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 151c (both change `runner.py`, which is at its 360-line budget; do not edit it in parallel). 176c helps (bench) but does not block.
- **Read:** `results/run-cost/run-cost.md` ("Parallel evaluation", "What is left" item 2); `model/model_v3/runner/pool.py`; `model/model_v3/runner/runner.py` (the level 1 fold over chunks of 1,000 paths); `model/model_v3/run.py` (`--workers`, `run_point`); `tests/model/model_v3/test_pool.py`; `tests/model/model_v3/accept.sh` line 21

## Goal
Level 1 is the serial floor of a run (about 1,100 s of a `quick` run on this machine, 3.1 h at final size) and the Actions accept job never passed `--workers`, so its two `quick` runs were single-core. Run level 1's independent chunks through `pmap` and pass `--workers 0` where the jobs run `run.py`. No number changes.

## Decisions (author, 2026-11-26)
Byte-identical lever; goes first with 151c. The 10-minute `quick` target is measured on a 4-core Actions runner and on this machine; the agent reports both.

## Design
1. Level 1 splits into chunks of 1,000 paths (30 per grid point at final size). Each chunk is independent given its seed stream; the fold that combines chunks stays in chunk order, so the result is the serial result. Send the chunks through `pmap(f, chunks, workers)`; `workers` 1 is the plain loop and stays the default for library callers.
2. Keep the seeds per chunk, not per worker: a result must not depend on the worker count. The test runs workers 1, 2 and 3 and compares to the last byte (floats by hex, arrays by buffer).
3. `run.py` passes `a.workers` to level 1. `accept.sh` calls `run.main([... '--workers', '0' ...])` for both `quick` runs; the workflow's other `run.py` calls do the same. Check memory: 2 GB per worker at 1,000 paths; the agent reads `free` and `nproc` from the Actions log (the 168c step logs `lscpu`) and caps `--workers 0` at what fits, saying how.
4. Time before and after with `bench.py` (176c) if merged, else `timing.py`: `level1_1sched_1000` and `quick_full`, workers 1 and 0, on this machine; then one Actions run of the accept job's first `quick` step for the 4-core figure.

## Touches
`model/model_v3/runner/runner.py` (move a function out or raise its budget row in `architecture.md` and say which), `model/model_v3/run.py`, `tests/model/model_v3/accept.sh`, `.github/workflows/model-checks.yml` (worker flags only; reviewer: web), `tests/model/model_v3/test_pool.py` (level 1 case), `model-specs/architecture.md` (budget rows only), `results/speedup/ledger.md` (one row), `results/run-cost/run-cost.md` (a section).

## Acceptance criteria
- Level 1 at workers 1, 2, 3 byte-identical (test); `quick` output byte-equal to a before-file made on the same machine with the same numerics setting; `test_legacy_digest` and all suites pass.
- Timings reported: `level1_1sched_1000` and `quick_full` on this machine, workers 1 and 0, against the estimate (1,100 s to about 300 s on 4 cores); one Actions figure with `nproc`.
- If the saving is under 1.5x on 2 cores, say why (memory, fork cost, chunk imbalance) and what remains.

## Out of scope
Changing chunk size or seeds; the tornado and roots (151c); the budget check (177c); `--parts` (178c).

## Open questions
None for the author.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** waiting for 151c
<!-- progress:end -->
