# Speed-up ledger

One row per merged lever (brief, lever, before, after, ratio, identical, machine). Append-only; on a conflict take upstream and re-add your row. 176c creates the rules and `bench.py`; this file was started by 154c because the ledger did not exist yet when it ran.

| brief | lever | before | after | ratio | identical | machine |
|---|---|---:|---:|---:|---|---|
| 154c | level 1 through `pmap` (units of chunk x schedule), `--workers` in `accept.sh` | level 1, 3 schedules, 1,000 paths: 327 s (workers 1) | 217 s (workers 2) | 1.51x on 2 cores (3 units on 2 workers); `quick` serial 2,319 s to 2,412 s (the unit path costs nothing measurable) | level 1 at workers 1, 2, 3 (test) and 2 at 1,000 paths (digest); `quick` at workers 1 byte-equal to main's; smoke at workers 1 and 2 equal except the recorded `workers` field | 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4` |
