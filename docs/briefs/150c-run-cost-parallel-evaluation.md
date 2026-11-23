# 150: Run cost: time the household run and parallelise the evaluations

- **Status:** ready (after 057c block 3; can start the timing block now)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 057c (blocks 1 to 2 on its branch), 124c, 128c (merged)
- **Read (block 0: the first two only):** (1) the 057c entry "A full household run is hours to days" in `docs/brief-suggestions.md` (on the 057c branch until it merges) and `docs/briefs/057c-v3-12-run-script-and-acceptance.md`; (2) `docs/agents/code.md`. Later: `model_v3/runner/sweeps.py` (`breakeven_return`, O1e); `model_v3/runner/runner.py`; `model_v3/run.py` (on the 057c branch); any pool or N7 timing code under `model_v3/` (search `pool`).

## Goal
One household evaluation at 20 paths takes 4.9 s (legacy 1.8 s); O1e (break-even return) costs three schedules x (1 + N2) roots x about 13 evaluations, about 7,800 evaluations per point at N2 200, over five points, before the tornado. Make the first official run feasible: the author ruled **break-even at one point (`median_mid`), the other points get the cheap outputs**, and the evaluations run in parallel. This brief measures and then parallelises; it does not change what any output means.

## Decisions (author, 2026-11-23)
- The household arm will run at **10 death phases** (139c wiring, ruled after 149c); time one evaluation and the smoke at 6, 10 and 30 phases in block 1 so the projection uses 10 (149c: 10 phases cost about 1.7 times the 6-phase run).
- O1e only at `median_mid`; the other four points carry the outputs that do not need the root search, and the file says so (a stated marker, not a number): the manifest change is 057c's, this brief only makes the run cheap.
- Outputs must be unchanged by parallelism: same seeds, same results to the last digit, serial and parallel byte-identical.
- No change to model economics, the register or any kernel code.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: timing.** Time one evaluation and one O1e root at 20 and 200 paths on both arms, the whole smoke run and the cost split by output group (a table in `docs/model-v3/run-cost.md`); project a full run at one-point O1e. Push.
- **Block 2: parallel.** Evaluate the independent units (schedules, roots, grid points) in a process pool, with a switch and a worker count; tests: serial and parallel byte-identical on a small run. Push.
- **Block 3: measure and report.** Speed-up by worker count, the projected full-run time on this machine, the projected time on a larger one; any remaining bottleneck. Change report; push; stop.
**Stop rule.** A kernel or model change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/sweeps.py`, `model_v3/runner/runner.py`, `model_v3/run.py` only for the pool switch (coordinate with 057c: its file), a new `model_v3/runner/pool.py` if none exists, tests, `docs/model-v3/run-cost.md`. Not `core/`, `arm.py`, the register, the pack or the manifest.

## Acceptance criteria
- Serial and parallel results byte-identical (checked by the test); all suites pass; `test_legacy_digest` unchanged.
- `run-cost.md` has the timing tables and the projection.

## Out of scope
The manifest change that marks O1e as one-point (057c), the feasibility rule, the tornado design, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/150-run-cost origin/brief/150-run-cost`
- **State:** ready; not started (after 057c block 3 for the merge)
<!-- progress:end -->
