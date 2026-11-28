# Re-profile after 151c, 154c and 186c (brief 179c)

Measurement only; no model code changed. Machine: 2 cores, 8 GB, Intel Xeon (2.3 GHz class), numpy 2.5.3, `NPY_DISABLE_CPU_FEATURES=X86_V4`, main `ee8a9df` (151c, 154c, 186c, 177c merged), household arm, median_mid, spec tau_0 0.04, tau_m 0.5, k_ln 0.5, ratio 1.0. Script: `model/studies/run-cost/profile_after_154c.py` (`scale`, `prof`, `floor`, `split`); raw JSON in `profile-after-154c/`. cProfile slows a run about 1.3 to 1.4 times (12.8 s profiled against 9.0 s plain at 20 paths).

## Verdict
**Decision-table row, by weight: "large-array work dominates", for level 1, which is 75% of a `quick` run.** At 1,000 paths the arrays hold 14,000 elements, the part of `core_run` that does not scale with the data is 9% (1.4 s of 15.7 s), and the run costs 1.4 times the floor of its visible numpy calls, not more than 3 times. A compiled year loop (180c) does not address that. The other 24% of `quick` (tornado, map, O1e roots, run at 20 to 50 paths) is the call-overhead case: 66 to 83% fixed time, 3.5 to 4.1 times the floor, all wrapped calls on arrays under 1,000 elements at 20 paths. For that part the table's second row applies (redundant calls are visible: 1.03 million `asarray` and 536,000 `builtins.sum` calls in one evaluation), so 152c first, then re-measure. No single function dominates: the largest own-time share at 1,000 paths is `builtins.sum`, 12%.

## 1. Where the time goes, `quick`, serial and 2 cores (one run each, not best of two: a run takes 32 minutes)
`quick` = 5 grid points, level 1 3 schedules x 1,000 paths, tornado and map at 50 paths, O1e once. Wall seconds by wrapping the run script's own calls (`split`); the guru's figures are the brief's estimates.

| part | serial | share | 2 cores (workers 0) | speed-up | guru's estimate | measured against estimate |
|---|---:|---:|---:|---:|---:|---|
| level 1 (5 points) | 1,465 s | 75.4% | 964 s | 1.52x | about 1,100 s | **+33%, flagged** |
| tornado (5 points) | 352 s | 18.1% | 180 s | 1.96x | about 1,900 s | **-81%, flagged** (the estimate predates 151c's headline-only evaluator) |
| feasibility map (once) | 59 s | 3.0% | 30 s | 1.94x | about 240 s | **-76%, flagged** (predates 186c) |
| O1e roots (once) | 61 s | 3.1% | 31 s | 1.96x | about 300 s | **-80%, flagged** (predates 151c) |
| everything else (assembly, I/O) | 4 s | 0.2% | 0 | | | |
| **total** | **1,942 s (32 min)** | | **1,210 s (20 min)** | 1.60x | about 3,540 s | |

Level 1 is the one part that did not fall since the estimate: it rose by a third (one run each; the 154c note had 287 s per point, 1,437 s for five). With 2 cores the three units per point leave one core idle a third of the time, which is why level 1 gives 1.52x and the rest 1.9 to 2.0x (154c's note). On 4 cores in Actions the same `quick` took 954 s (EPYC 9V74), 975 s (Xeon 6975P-C) and 1,335 s (EPYC 7763) (177c, run ids in the ledger).

## 2. Inside `core_run` (profile of one full evaluation = 5 `core_run`s plus the output groups)
`kernel.step_year` is called 10,161 times in one evaluation (2,032 per `core_run`). Arrays hold 14 elements per path: 280 at 20 paths, 2,800 at 200, 14,000 at 1,000.

| | 20 paths | 200 paths | 1,000 paths |
|---|---:|---:|---:|
| plain wall, full evaluation | 9.0 s | 24.0 s | 93.7 s |
| profiled own time in all functions | 12.7 s | 31.9 s | 117.0 s |
| own time in builtin (C) functions | 2.3 s (18%) | 5.9 s (18%) | 20.9 s (18%) |
| of which numpy functions | 0.7 s | 2.0 s | 6.6 s |
| own time in Python code, including numpy operators (`+`, `*`, `>`: not visible to cProfile) | 10.4 s (82%) | 26.0 s (82%) | 96.1 s (82%) |
| numpy function calls (visible) per simulated year | 202 | 202 | 202 |
| wrapped numpy calls (where, asarray, maximum, ...) | 3.58 million | 3.58 million | 3.58 million |
| median array size of those calls | 280 | 2,800 | 14,000 |
| share of wrapped calls on arrays under 1,000 elements | 100% | 28% | 27% |

The 27 to 28% under 1,000 are scalar and 14-element calls (`asarray` of a small list, 1.03 million of them) at every size. The calls and the 82% share are the same at every size: the work in Python is a fixed cost per year, and only the array work grows.

Top own-time functions (profiled, seconds; all three sizes have the same list in a flat order):

| function | calls | 20 paths | 200 paths | 1,000 paths |
|---|---:|---:|---:|---:|
| `builtins.sum` | 536,453 | 1.38 | 3.53 | 13.84 |
| `household.apply_payment` | 45,373 | 1.15 | 2.25 | 5.83 |
| `kernel._div` | 148,674 | 0.61 | 1.39 | 5.56 |
| `kernel.assess` | 10,827 | 0.59 | 1.47 | 5.13 |
| `arm._restart` | 10,130 | 0.51 | 1.46 | 5.08 |
| `kernel._route_tax` | 52,346 | 0.53 | 1.31 | 5.01 |
| `household.household_step` | 17,540 | 0.77 | 1.40 | 3.70 |
| `arm.pre` | 10,130 | 0.37 | 0.99 | 3.46 |

At 1,000 paths `burden.m2` (18 calls, 5.7 s) and `burden._cash` (6 calls, 5.1 s) join the list: they are per-year loops of their own.

## 3. Call-overhead test
Two tests, both on the real model.

**(a) Time that does not scale with the data.** `core_run` and the full evaluation timed at 20, 50, 100, 200, 500 and 1,000 paths (best of 2), straight-line fit t = fixed + per_path x paths (`scale.json`; the fit misses a point by up to 9 to 11%, so the shares are approximate):

| | fixed | per path | fixed share at 20 / 50 / 200 / 1,000 paths |
|---|---:|---:|---|
| `core_run` | 1.39 s | 14.2 ms | 83% / 66% / 33% / 9% |
| headline-only evaluation | 1.42 s | 14.0 ms | 84% / 67% / 34% / 9% |
| full evaluation | 6.59 s | 84.9 ms | 80% / 61% / 28% / 7% |

**(b) The same operations in a tight loop** (`floor.json`, `floor2.json`): time per call at these sizes, microseconds: `where` 1.3 (280), 3.2 (2,800), 43 (14,000); `maximum` 0.6, 1.4, 4.8; `add` 0.4, 1.3, 5.7; `sum` 0.4, 0.9, 2.9; `asarray` 0.04. The floor of the evaluation is the wrapped-call counts of section 2 times these:

| paths | floor of the wrapped calls | plain evaluation | ratio |
|---|---:|---:|---:|
| 20 | 2.5 s | 9.0 s | 3.5 |
| 200 | 5.9 s | 24.0 s | 4.1 |
| 1,000 | about 67 s | 93.7 s | 1.4 |

The floor counts the visible calls only (the operators `+`, `*` are not counted, and my `where` floor includes its comparison), so it is a floor on the calls, and the ratio is an upper bound for how much of the rest is overhead; the direction does not depend on it. **The 3x line from the brief is crossed at 20 and 200 paths and not at 1,000.**

## 4. The decision table, filled
| finding | measured here | row |
|---|---|---|
| over 50% of `core_run` in calls on arrays under 1,000 elements, and more than 3x the floor | true at 20 paths (100%, 3.5x), at 200 paths (the arrays are 2,800 but 4.1x); **false at 1,000 paths, where level 1 and the final run spend their time (27%, 1.4x)** | compiled loop (180c): applies to the tornado, map and roots only, 24% of `quick`; 180c measured 1.16x for the cheap part and stopped |
| the same, and redundant operations visible | 1.03 million `asarray` and 536,000 `builtins.sum` calls per evaluation (about 100 each per simulated year); 202 visible numpy calls per year | numpy restructure first (152c), then re-measure: applies to the 24% |
| large-array work dominates | 9% fixed time and 1.4x the floor at 1,000 paths; level 1 is 75% of `quick` | **vectorisation or memory layout; a kernel compile will not help; a brief for the top function** (`builtins.sum`, 12% of own time at 1,000 paths) |
| `again` runs or welfare solves still large | the full evaluation is 5.9x one `core_run` (93.7 s against 15.7 s at 1,000 paths); level 1 runs it | a headline-only level 1 is not possible (level 1 reads the groups); the `again` runs are already the grouping unit |

## 5. What this says for the next lever
1. Level 1 at 1,000-path chunks is array-bound, so neither a compile (180c) nor 152c (which removes redundant calls) cuts the bulk of it; 152c helps the 24% that runs at 20 to 50 paths.
2. The array cost is the number and size of the `where`, `maximum` and `sum` calls on 14,000-element arrays: 3.58 million wrapped calls per evaluation whatever the size. Fewer passes over the data (fusing the `where` chains, `float32` where the pins allow, a layout with the paths axis contiguous) is the lever; each needs its own byte-identity or tolerance proof (171c).
3. Workers are the lever already pulled: level 1 on 4 cores is 3 units per point and cannot use more than 3; at final size 30 units per point.
4. Suggestions (not done here, as the brief says): `project/brief-suggestions.md`, entry "179c: level 1 is array-bound".

## 6. Caveats
- One `quick` run each, serial and 2 cores (32 and 20 minutes); no repeat, so a 5% difference between the two is not evidence.
- cProfile does not see operator ufunc calls; the 82% "Python" share includes them. The floor test is the answer to how much of it is overhead.
- The micro-timings (`floor`) were taken while another run used the second core, 1 to 2% effect on microsecond figures at most.
- `scale` at 500 and 1,000 paths on the full evaluator used about 5 GB; at 1,000 paths one run was alone on the machine.
