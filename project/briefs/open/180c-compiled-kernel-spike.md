# 180: Compiled kernel spike (numba first)

- **Status:** ready; stage A (speed) starts as soon as 176c has merged; moved ahead of 153c (author, 2026-11-27)
- **Agent:** 6
- **Needs:** 176c
- **Length:** 1
- **Row:** 180b | agent 6 | hold | needs 171c | length 1 | Kernel spike, stages B (bits) and C (assessment)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 176c (bench). Stage A does not wait for 179c: if its profile has landed, read it; if not, a 10-minute `cProfile` of `eval_hh_20` picks the function to jit, and stage A's own speed-up answers the call-overhead question (under 2x: stop). Stage B waits for 171c (zero tolerance), so a count that moves is real. The 153c brief waits for this spike's report.
- **Read:** `results/speedup/profile-after-154c.md`; `model/model_v3/core/kernel.py` (603 lines: read the year loop and its callers only); `model/model_v3/runner/runner.py` `core_run`; `model-specs/computational-architecture-hypothesis.md`; `model-specs/architecture.md` 5.1 (layers)

## Goal
Find out how much a compiled year loop buys and what it costs in bits, before anyone commits to it. The author wants the kernel rewrite explored and any further gain taken ("if I can get time down even further, even better"). A spike: measure and report; adoption is a separate brief, numbered after the report.

## Decisions (author, 2026-11-26)
Willing to try a compiled kernel. Not byte-identical to numpy is expected (the compiler's `exp`, `log` and `pow` differ); that is why it comes after 171c and the pins move once more.

## Known (guru, 2026-11-26)
`pip install --dry-run numba numpy==2.5.3` resolves (numba 0.68.1, llvmlite 0.50.0), so the pinned numpy need not change; `PIP_PINS` in the workflow would gain numba and llvmlite pins. Numba is not installed here or in the workflow today.

## Pre-registered adoption bar (written before measuring)
Recommend adoption only if all hold: (1) at least 3x on `core_run` at 20 and 200 paths, household arm; (2) cold compile under 60 s and a warm cache load under 5 s, and the cache works on Actions (`actions/cache` on the numba cache dir); (3) works under `pmap` forked workers and under `NPY_DISABLE_CPU_FEATURES=X86_V4`; (4) every output at `quick` within the tolerance rule below of the numpy result, with the 171c counts identical.
**Tolerance for the spike (proposal for the author):** floats within 1e-9 relative, counts identical after 171c's zero tolerance, flags and markers identical, p10 to p90 ranges within 1e-9 relative. Looser than that: report, do not adopt.

## Design (stages, one push each)
- **A (prototype).** Behind an environment switch `WDT_KERNEL=numba` (default off, numpy path untouched): the hot year-loop body only, `@njit(cache=True)`, `fastmath=False`, no change to the numpy path or its signature. Report: time of `core_run` and `eval_hh_20` before and after (`bench.py`), compile and warm times, lines of kernel moved.
- **B (bits).** Run `quick` both ways on one machine, same numerics setting; report per-output maximum relative and absolute differences and every count or flag that moved; list the operations that differ (`exp`, `log`, `pow`, sums) by testing each in isolation.
- **C (assessment, no code).** One page: what the gain per call overhead removed implies for Rust (PyO3, `maturin`) or Julia; build, CI and review cost of each against numba; a recommendation and the main alternative. Estimates labelled as such.
If stage A gives under 2x, stop after A and report why (array sizes too large, loop not the cost); do not go on to B and C.

## Touches
`model/model_v3/core/kernel.py` (switch and the jitted function; if the file budget is hit, a new `core/kernel_jit.py` with a LAYER row in `tests/model/model_v3/conftest.py` and `test_groups.py` as `agent-guru.md` says), `tests/model/model_v3/` (equality and tolerance tests, skipped when numba is absent), `.github/workflows/model-checks.yml` (spike job only, manual; reviewer: web), `results/speedup/kernel-spike.md`, `results/speedup/ledger.md`. No pin changes: the spike is off by default.

## Acceptance criteria
- Stage A figures and stage B differences reported with the machine header; the adoption bar answered point by point, yes or no with numbers.
- Default (numpy) path byte-identical to before; all suites pass with `WDT_KERNEL` unset.

## Out of scope
Making numba the default; moving the pins; Rust or Julia code; the workflow's regular jobs.

## Open questions
For the author: the spike tolerance above, or another.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
