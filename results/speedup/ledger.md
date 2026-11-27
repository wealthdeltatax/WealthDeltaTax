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
