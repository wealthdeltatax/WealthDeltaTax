# Compiled kernel spike (brief 180c): stage A result, stopped after A

**Verdict: stop. A compiled version of the numeric functions the year loop calls gives 1.16x at 20 paths and about 1.1x at 200, bit-identical. The brief's line is 2x (bar: 3x). Stages B and C are not run, as the brief says.**
What it would take to reach 3x is a different, larger piece of work than the brief's "hot year-loop body only"; section 3 says what, and asks the author.

Machine: Intel Xeon @ 2.30 GHz, 2 cores, 8 GB, numpy 2.5.3, numba 0.68.1, llvmlite 0.50.0, Python 3.13, `NPY_DISABLE_CPU_FEATURES=X86_V4`, workers 1. Branch started from main `8da93c2`.

## 1. Where the time goes (cProfile of `eval_hh_20`; 179c's profile has not landed, so this is the 10-minute one the brief allows)
One evaluation is five `core_run`s (one plus four `again` calls). Each runs the kernel year loop twice, in `burden.line_flows` and again in `revenue.run_lines` (household arm).
Cumulative, profiled run 13.4 s:

| part | cumulative s | share |
|---|---|---|
| `kernel.step_year` (10,161 calls, about 1 ms each) | 10.1 | 76% |
| of which the household hook `pre` / `post` | 4.1 / 0.9 | 37% |
| of which `kernel.assess` (10,827 calls) | 4.1 | 31% |
| `household_step` (17,540 calls) | 2.5 | 19% |
| `apply_payment` (45,373 calls) | 1.7 | 13% |
| `builtins.sum` (536,453 calls) | 2.0 | 15% |

The arrays are 20 to 280 lines long. The cost is Python call overhead (about 10 million function calls, 1 million `np.asarray`), not arithmetic: a year step is a tree of dict-of-array operations, hooks (`HouseholdHook.pre/post`), a Python closure for the rate (`rate_fn`), a `Flows` record of dicts, and validity checks.
The benchmark's configuration (measured by wrapping `step_year`): routes A, B, C, D and Cv (verification on), `b_mode` sale, `c_cap` units, `r_def` 0.02, the household hook, with the public-ledger book in `run_lines`. So a compiled loop for the household arm must cover declare, verify_C, assess and all five route settlements, the ledger branch of `_refund_cash`, the hook's pension-lien and floor-restart logic and the cap callback, not one function.

## 2. What was built and measured (stage A)
`model/model_v3/core/kernel_jit.py`: `@njit(cache=True, fastmath=False)` versions of `household_step` (convention A, the arm's shape) and `apply_payment` (the arm's `_pay`), two functions, 103 lines in the file. Installed into `core.household` only by `kernel_jit.install()` when `WDT_KERNEL=numba` and numba is importable; any call of another shape falls back to numpy. The numpy path is untouched and the module is not imported unless the switch is set. These two functions are the largest pure-array pieces of the loop; the rest is the object graph above.

| case (household arm) | numpy | numba | ratio | identical |
|---|---|---|---|---|
| `eval_hh_20`, best of 2 | 9.35 s | 8.08 s | 0.86 (1.16x) | yes (hash `059139aee5e6`) |
| one evaluation at 200 paths, best of 2 runs of one | 26.5 s, 26.0 s | 23.7 s, 22.2 s | 0.89, 0.86 (about 1.1x) | yes (hash `bdf1dfcdb3ad`) |

Bit equality is expected and found: the two functions have no `exp`, `log` or `pow`, and the compiled code repeats the numpy expression order term by term (zero terms kept). `tests/model/model_v3/test_kernel_jit.py` asks for bit equality (signed zeros included) on random inputs with negative balances; skipped when numba is absent.
`core_run` alone was not timed separately: `eval_hh_20` is five `core_run`s plus the output groups (about 11.7 of 13.4 s profiled is `core_run`), so the ratio on `core_run` alone would be a little higher, not near 2x.

Ceiling of this piece: the two functions are 4.2 of 13.4 profiled seconds (31%); making them free would give 1.45x; the 1.16x measured saves 1.3 s of the roughly 2.9 s these functions take unprofiled, so about half of the ceiling is lost to converting dicts to arrays and back on each call.

## 3. The adoption bar, point by point
1. At least 3x on `core_run` at 20 and 200 paths, household arm: **no** (1.16x and about 1.1x for the pieces that are cheap to compile). Whole-loop ceiling: `step_year` is 76% of the time, so a loop compiled end to end and costing nothing would give about 4.2x; 3x needs it to cost under 17% of today's time, with the remaining 24% (hooks around the loop, output groups) unchanged. That has not been shown to be reachable and is not what was built.
2. Cold compile under 60 s, warm cache load under 5 s: **yes for the prototype** (cold 0.6 s, warm 0.17 s for two small functions). A whole-loop kernel would compile for far longer; not measured. The cache on Actions was not tried (`actions/cache` on the numba cache dir; no workflow change made).
3. Works under `pmap` forked workers and `X86_V4`: **yes for the prototype** (a forked 2-process pool called the compiled function from a parent that had already compiled it; all runs above had `X86_V4` set). Not tried through `pmap` itself.
4. Every `quick` output within tolerance, 171c counts identical: **not run** (stage B is not reached). For the two compiled functions the result is bit-identical, so the tolerance question does not arise for them; it will for the `rate_fn` (`exp`/`log` in `logistic_ln`) in a whole-loop port.

Recommendation: do not adopt this prototype. 1.1x to 1.16x does not repay a second implementation of the arithmetic, a new dependency and a cache in CI.

## 4. For the author
The brief's Touches (kernel.py and kernel_jit.py) do not reach the hook (`runner/arm.py`, layer 3.6), which holds 37% of the loop. A compiled loop that reaches 3x has to take the hook's year, the assessment, the route settlements, the ledger and the rate function into one compiled body with array state in place of the `Book` dicts; the `Flows` record becomes arrays. It is a rewrite of about 1,000 lines (kernel.py's year step plus arm.py's hook plus the household functions) for one configuration, kept in step with the numpy path by a tolerance test, and I estimate it as several days of work (an estimate, not a measurement). Options:
- **A. Stop here** (recommended): the spike answers the question the brief asked; the profile shows the cost is Python call overhead on small arrays, which is the case a compiled body or a vectorised-over-paths restructure addresses, and a smaller lever first is to cut call count (for example fewer `sum` and `asarray` calls, one `Flows` per year).
- **B. Authorise the whole-loop port** as its own brief, with the file budget and `arm.py` in Touches, and then stages B and C on it.
- **C. Skip numba and go to stage C only** (Rust or Julia assessment, no code): a compiled language faces the same object-graph rewrite, so the cost estimate in B applies to it as well.

Open question (the tolerance): unchanged from the brief (1e-9 relative, counts identical); not exercised, since the compiled functions are bit-identical.
