# Speed-ups: how one is proposed, measured and accepted

A speed-up changes how long the model takes and must not change what it says. Every speed-up brief follows this file (brief 176c). The measuring tool is `model/studies/run-cost/bench.py`.

## Before any code
1. **Profile first, then pick the lever.** Time the case the lever targets (`bench.py list` names them; `model/studies/run-cost/timing.py --quick` splits an evaluation by part). A lever that touches under 5% of the measured time is not worth a brief.
2. **One lever per brief.** Two levers in one change cannot be told apart in the ledger or reverted separately.
3. **Write the proof before measuring.** Either (a) byte-identical: `bench.py compare` says `identical: yes` on every case, and the `quick` output file is byte-equal (case `quick_full`, run date masked); or (b) a tolerance rule the author has signed off, with its adoption bar, written in the brief. A change that is not byte-identical lands only after 171c, and it moves the pins (legacy digest, `test_groups`, tripwire baseline) in its own commit.

## Measuring
4. Before and after come from `bench.py run` on the same machine, the same numerics setting (`NPY_DISABLE_CPU_FEATURES=X86_V4`) and the same worker count. The default cases take two minutes (`bench.py list`); a lever that touches the tornado or level 1 adds `--cases tornado_1sched_20,level1_1sched_1000` (about 5 minutes more). Best of two (`quick_full` takes about an hour: best of one is allowed and is recorded as `reps: 1`). The header (CPU model, cores, memory, numpy, git SHA, workers) goes with the file.
5. `bench.py compare BEFORE AFTER` refuses files from a different CPU model, numpy version or numerics setting. `--force` overrides it; a forced comparison is not evidence of identity and is not reported as such.
6. Take the "before" file from the commit the branch started from, in the same session as the "after" file; never from a table in a note.

## Accepting
7. Report measured against the brief's estimate, case by case. If the gain is under the brief's bar, say so with the numbers and keep or revert as the brief says; do not retune the bar.
8. A slowdown on any case is a failure, even if another case got faster. The `quick` time budget (177c) is checked on Actions: the `speed` job (manual: "Run workflow", `run_speed`; and on pushes to `main` that touch `model/`) fails if `quick` takes longer than `QUICK_BUDGET_S` in the workflow; the bench numbers it prints do not gate.
9. On merge, add one row to `results/speedup/ledger.md`: brief, lever, before, after, ratio, identical, machine. The ledger is append-only; on a conflict take upstream and add your row again.

## What does not count as a proof
A passing test suite alone; a timing from another machine or numerics path; a hash of part of the result; a tolerance chosen after seeing the difference.
