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
- **Done (block 1, 2026-11-27):** `runner.level1(..., workers=1, cap=None)`: the chunks' paths are drawn in the serial order, then one unit per (chunk, schedule) goes through `pmap` (3 units per chunk: 3 at quick size, 30 per grid point at final size; the brief's "chunks" alone would give one unit at quick, since `CHUNK` = 1,000). The seed key is the chunk, never the worker. The cap store is module state, so a forked unit records into its own copy: each unit records into a local store and the records are merged into `cap` in (chunk, schedule) order, the first standing, as in the serial run (`run.py` passes `workers=w, cap=cap`; 120 lines). `accept.sh` passes `--workers W` to both `quick` runs, W = min(cores, (MemTotal GB - 2) // 3) and logs it; the workflow has no other `run.py` call (smoke and convergence run through pytest), so it is unchanged. Budget rows: `runner.py` 368 and `test_pool.py` 103 in `architecture.md` (totals 6,518 and 4,446). Tests: level 1 byte-identical at workers 1, 2, 3 (real model, 3 chunks), and a unit that meets a shortfall in a forked worker reaches the caller's store, first chunk first. `tests/model/model_v3` 413 passed (incl. `test_legacy_digest`, `test_budget`).
- **Memory (measured):** one level 1 unit (household, 1,000 paths) peaks at 3.0 GB (the `pool.py` text says about 2 GB: not corrected here, outside Touches). On this 8 GB machine two workers at 1,000 paths were OOM-killed in 2 of 5 attempts (`BrokenProcessPool`; cgroup kill, 3.0 GB anon each), so the cap above leaves 2 GB for the parent and gives 1 worker here and 4 on a 16 GB, 4-core runner.
- **Level 1, 3 schedules, 1,000 paths, this machine (`NPY_DISABLE_CPU_FEATURES=X86_V4`, one run each, a fresh process per worker count):** workers 1 327 s, workers 2 217 s (1.51x), workers 0 (= 2 cores) 216 s; digests identical.
- **Next:** the `quick` before and after on one date; ledger row and `run-cost.md` section; the Actions 4-core figure is for the author (command in the report).
- **Resume:** `git checkout brief/154c-level-1-parallel`.
- **State:** block 1 pushed; timing and byte comparison running.
<!-- progress:end -->
