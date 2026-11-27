# 180: Compiled kernel spike (numba first)

- **Status:** done, stopped after stage A (author: stop), merged 2026-11-27 (report only; the prototype stays on branch `brief/180c-compiled-kernel-spike`)
- **Agent:** 6
- **Needs:** 176c
- **Length:** 1
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
- **Done:** stage A only (the brief's stop rule): profile of `eval_hh_20`, compiled `household_step` and `apply_payment` in `core/kernel_jit.py` behind `WDT_KERNEL=numba`, equality test, timings, report `results/speedup/kernel-spike.md`, ledger row. Result 1.16x at 20 paths, about 1.1x at 200, bit-identical. Under 2x, so stages B and C were not run.
- **Next:** the author chooses A (stop), B (a whole-loop port as its own brief, `arm.py` in Touches) or C (stage C assessment only); see section 4 of the report. 152c (one year loop shared by burden and ledger) attacks the same call overhead and is the cheaper first lever.
- **Resume:** branch `brief/180c-compiled-kernel-spike`; nothing to merge before the author's answer. The full `model_v3` suite (without `test_converge.py`) was still running when this was written; see Verification.
- **State:** needs the author
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 180c, compiled kernel spike (numba): stage A only, stopped under the 2x line as the brief says
- Files changed: model/model_v3/core/kernel_jit.py (new: compiled household_step and apply_payment, installed only under WDT_KERNEL=numba); tests/model/model_v3/test_kernel_jit.py (new: bit equality, skipped without numba); tests/model/model_v3/conftest.py (LAYER row); results/speedup/kernel-spike.md (report); results/speedup/ledger.md (one row); project/agents/friction-log.md, project/brief-suggestions.md; this brief.
- What is different now: numba is optional and off; nothing changes unless WDT_KERNEL=numba and numba is installed. Measured: 1.16x on eval_hh_20 (9.35 s to 8.08 s), about 1.1x at 200 paths, outputs bit-identical.
- New or changed interfaces: env switch WDT_KERNEL=numba (calls kernel_jit.install()); nothing is called by default. No workflow or pin change.
- Acceptance criteria: stage A figures with machine header: met (report sections 1 and 2). Adoption bar point by point: met for points 1 to 3 (no; yes for the prototype; yes for the prototype), point 4 not run because stage B is not reached after under 2x. Default path byte-identical: met by construction (no file the numpy path imports was changed; git diff is a LAYER row, a ledger row and new files); not shown by a quick run. All suites pass with WDT_KERNEL unset: NOT MET as a complete check: the model_v3 suite without test_converge.py was still running (91 tests passed, none failed, when I stopped waiting); test_converge.py not run; other suites not run.
- Deviations from the brief: the switch is in kernel_jit.install() on core.household, not in kernel.py, because the hook (runner/arm.py) is outside Touches and holds 37% of the loop; the timing harness was a scratch script, not bench.py (bench.py has no way to set the switch); no workflow spike job added (nothing to run in it).
- Risks / follow-ups: author decision A, B or C (report section 4). 152c is the cheaper lever on the same overhead. Estimates in the report (a whole-loop port of about 1,000 lines, several days) are estimates.
- Instruction friction: two entries added to project/agents/friction-log.md (suite run time; Touches left out arm.py).
- Verification: tests/model/model_v3/test_kernel_jit.py and test_groups.py pass (7); eval_hh_20 hash equal both ways; 200-path hash equal both ways; fork pool and cold/warm cache load timed; full model_v3 suite not completed (above).
- Overview sections likely needing an update: none until the author decides.
- Commit / branch: brief/180c-compiled-kernel-spike (pushed, not merged: NEEDS THE AUTHOR)
```
