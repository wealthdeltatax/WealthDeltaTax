# Speed-up ledger

One row per merged speed-up lever (rules: `project/agents/reference/code/speedup.md`). Append-only: on a conflict take upstream and add your row again. Times are best-of-two wall seconds from `model/studies/run-cost/bench.py` unless the machine column says otherwise; `ratio` is after / before; `identical` is the result of `bench.py compare` (and the `quick` output file for the byte check).

| brief | lever | case | before | after | ratio | identical | machine |
|---|---|---|---:|---:|---:|---|---|
| 150c | none: the unoptimised baseline | eval_hh_20 (one household evaluation, 20 paths) | 8.9 s | 8.9 s | 1.00 | n/a | 2 cores, 150c session, CPU not recorded; 150c timing.py, not bench.py |
| 150c | none: the unoptimised baseline | eval_leg_20 | 2.9 s | 2.9 s | 1.00 | n/a | as above |
| 150c | none: the unoptimised baseline | tornado_1sched_20 (11 evaluations, serial) | 74.4 s | 74.4 s | 1.00 | n/a | as above (speedup.py) |
| 150c | workers = 2 | tornado_1sched_20 | 74.4 s | 42.4 s | 0.57 | yes (to the last digit) | as above (speedup.py) |
| 150c | none: the unoptimised baseline | level1_1sched_1000 (household) | 74 s | 74 s | 1.00 | n/a | as above |
| 150c | none: the unoptimised baseline | root_1_20 (O1e root, bracket check only, 2 evaluations) | 16.4 s | 16.4 s | 1.00 | n/a | as above |
| 154c | level 1 through `pmap` (units of chunk x schedule), `--workers` | level1_3sched_1000 (household, workers 1 to 2) | 327 s | 217 s | 1.51 | yes at workers 1, 2, 3 (test); `quick` at workers 1 byte-equal to main; smoke equal except the recorded `workers` field | 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`; not bench.py; `quick` serial 2,319 s to 2,412 s (unit path about 4% dearer) |
| 180c | numba-compiled `household_step` and `apply_payment` (spike, off by default, not adopted) | eval_hh_20 (household, 20 paths) | 9.35 s | 8.08 s | 0.86 | yes (hash equal; one evaluation at 200 paths 26.0 s to 22.2 s, also equal) | Xeon 2.30 GHz, 2 cores, 8 GB, numpy 2.5.3, numba 0.68.1, `NPY_DISABLE_CPU_FEATURES=X86_V4`; ab harness, not bench.py; see kernel-spike.md |
| 186c | feasibility map runs only the OF1 group (`evaluate(only=)`) | whole quick map (50 paths, household, workers 1) | 328.7 s | 61.5 s | 0.19 | yes (map points and OF1 byte-equal; test on both arms; `quick` output equal but for `run_date`, see the brief) | 2 cores, `NPY_DISABLE_CPU_FEATURES=X86_V4`, `map_only.py`, best of 1 |

## Actions timing, brief 177c (hosted 4-core runner, 15 GB, `--workers 4`, `NPY_DISABLE_CPU_FEATURES=X86_V4`, branch `brief/177-quick-budget`, never `--final`)

| run id | CPU | `quick` wall | eval_hh_20 | eval_leg_20 | root_1_20 |
|---|---|---:|---:|---:|---:|
| 46065482351 | Intel Xeon 6975P-C | 975 s | 9.90 s | 2.31 s | 19.60 s |
| 46065485244 | AMD EPYC 9V74 | 954 s | 11.66 s | 2.67 s | 23.31 s |
| 46065488130 | AMD EPYC 7763 | 1335 s | 17.97 s | 4.10 s | 35.95 s |

Median 975 s; slowest 1335 s. Budget `QUICK_BUDGET_S` = 1670 s (slowest plus 25%; the brief's rule, median plus 25%, gives 1219 s, which the EPYC 7763 run would fail). All three are over the author's target of 10 minutes (600 s) by 1.6 to 2.2 times. The Xeon 8573C named in the brief did not come up in these three runs.
| 178c | `--parts level1,map` (skips the tornado and O1e) | quick, five points, workers 1 (`quick_headlines`; bench.py not merged, wall time of `run.main`) | about 2,350 s (full `quick`, 151c/154c session figure, not re-timed) | 1,875 s | 1.25 | yes: default smoke byte-identical (`cmp`); every id a partial smoke ran equals the full smoke's | 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`; target 3 to 5 min not met; Actions figure is the author's |

## Profile after 154c, brief 179c (measurement; no lever)

| brief | lever | case | before | after | ratio | identical | machine |
|---|---|---|---:|---:|---:|---|---|
| 179c | none: re-profile | `quick` serial, split by part | 1,942 s (level 1 1,465, tornado 352, map 59, roots 61) | 1,942 s | 1.00 | n/a | 2 cores, 8 GB, X86_V4, one run, not bench.py |
| 179c | workers 0 (2 cores) | `quick` | 1,942 s | 1,210 s | 0.62 | not checked (measurement only) | as above |

Level 1 is array-bound (9% fixed time, 1.4x the floor at 1,000 paths); tornado, map and roots are call-bound (3.5 to 4.1x the floor). See `profile-after-154c.md`.
| 152c | one year loop for the household arm (`burden.Tap` fed by `revenue.run_lines`) | one `core_run` plus headlines, household, 1,000 paths, 2 cores, best of 2 | 18.25 s | 11.0 s | 0.60 | yes (full household evaluation hash equal on both trees, 3 schedules; flows byte-equal to `line_flows`; `quick` output equal but for `run_date`, see the brief) | 20 paths 1.97 to 1.14 s; 200 paths 4.97 to 2.79 s |
