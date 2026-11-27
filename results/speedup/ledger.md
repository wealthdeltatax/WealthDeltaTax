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

## Actions timing, brief 177c (hosted 4-core runner, 15 GB, `--workers 4`, `NPY_DISABLE_CPU_FEATURES=X86_V4`, branch `brief/177-quick-budget`, never `--final`)

| run id | CPU | `quick` wall | eval_hh_20 | eval_leg_20 | root_1_20 |
|---|---|---:|---:|---:|---:|
| 46065482351 | Intel Xeon 6975P-C | 975 s | 9.90 s | 2.31 s | 19.60 s |
| 46065485244 | AMD EPYC 9V74 | 954 s | 11.66 s | 2.67 s | 23.31 s |
| 46065488130 | AMD EPYC 7763 | 1335 s | 17.97 s | 4.10 s | 35.95 s |

Median 975 s; slowest 1335 s. Budget `QUICK_BUDGET_S` = 1670 s (slowest plus 25%; the brief's rule, median plus 25%, gives 1219 s, which the EPYC 7763 run would fail). All three are over the author's target of 10 minutes (600 s) by 1.6 to 2.2 times. The Xeon 8573C named in the brief did not come up in these three runs.
