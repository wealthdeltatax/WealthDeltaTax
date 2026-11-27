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
| 186c | feasibility map runs only the OF1 group (`evaluate(only=)`) | whole quick map (50 paths, household, workers 1) | 328.7 s | 61.5 s | 0.19 | yes (map points and OF1 byte-equal; test on both arms; `quick` output equal but for `run_date`, see the brief) | 2 cores, `NPY_DISABLE_CPU_FEATURES=X86_V4`, `map_only.py`, best of 1 |
