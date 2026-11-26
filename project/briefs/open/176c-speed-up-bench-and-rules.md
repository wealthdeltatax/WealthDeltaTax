# 176: Speed-up bench and the rules every speed-up follows

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** none (runs alongside 151c and 171c; disjoint files)
- **Read:** `results/run-cost/run-cost.md` ("One evaluation", "Level 1 and O1e roots"); `model/studies/run-cost/timing.py` and `speedup.py`; `project/agents/reference/code/conventions.md`; `tests/model/model_v3/accept.sh` (steps 5 and 6)

## Goal
Optimising is a discipline (author, 2026-11-26). Give every speed-up brief one script that measures before and after and proves the numbers did not move, and one short rule file saying how a speed-up is proposed, measured and accepted. Without it each brief invents its own timing and its own byte check.

## Decisions (author, 2026-11-26)
- A `quick` run under 10 minutes is the working target for the many-variable-changes loop; a final-size run may take long, best on GitHub Actions.
- Every speed-up carries either a byte-identical proof or a tolerance rule the author signs off, written before measuring.

## Design
1. **`model/studies/run-cost/bench.py`.** One command: `python -I model/studies/run-cost/bench.py run --out FILE [--cases a,b]`. Cases (named, fixed specs and seeds): `eval_hh_20` (one household evaluation, 20 paths), `eval_leg_20`, `tornado_1sched_20`, `root_1_20` (one O1e root), `level1_1sched_1000`, `quick_headlines` (once 178c lands), `quick_full`. The small cases finish in under 3 minutes in total, so a developer can run them after every change; `quick_full` runs only when asked.
2. **Record per case:** best of 2 wall seconds; a result hash (floats by hex, arrays by buffer, as `tests/model/model_v3/test_pool.py` does); and a header with CPU model, cores, memory, numpy version, `NPY_DISABLE_CPU_FEATURES`, git SHA, worker count.
3. **`bench.py compare A B`:** per case the time ratio and `identical: yes/no`; refuses to compare files with different numerics settings or CPU model unless `--force`, and says so.
4. **Rules file `project/agents/reference/code/speedup.md`** (at most 40 lines), one link added to `project/agents/agent-code.md`:
   - profile first, then pick the lever; one lever per brief;
   - before and after from `bench.py` on the same machine and numerics setting, best of two, header recorded;
   - the proof is written before measuring: byte-identical (`compare` says yes on every case and the `quick` output file is byte-equal), or a tolerance rule signed off by the author with its adoption bar;
   - report measured against the brief's estimate; if the gain is under the bar, say so and keep or revert as the brief says;
   - a non-byte-identical lever lands only after 171c, and moves the pins in its own commit;
   - a slowdown is a failure: the `quick` time budget (177c) is checked on Actions.
5. **Ledger `results/speedup/ledger.md`:** one row per merged lever (brief, lever, before, after, ratio, identical, machine). Append-only; on a conflict take upstream and re-add your row.

## Touches
`model/studies/run-cost/bench.py` (new), `model/studies/run-cost/README` line if one exists, `project/agents/reference/code/speedup.md` (new), `project/agents/agent-code.md` (one link), `results/speedup/ledger.md` (new, seeded with the 150c figures as the first rows: the unoptimised baseline), `tests/project/tools/` or `tests/model/` for a test that `compare` flags a one-bit change. Not the model, `run.py`, `runner.py`, the workflow or the pins.

## Acceptance criteria
- `bench.py run` twice on one machine: every hash identical, times within 15% (report the spread).
- A test: `compare` reports `identical: no` when one float is changed by one bit and refuses mismatched numerics headers.
- The small cases total under 3 minutes on this 2-core machine (report the figure).
- `speedup.py` rules file within 40 lines; `check_agent_docs.py` exit 0.

## Checks to run
The new test; `python model/tools/run_suites.py tools` and `project` suites; `python project/tools/check_agent_docs.py`.

## Out of scope
Any model change; the budget check on Actions (177c); the `--parts` switch (178c).

## Open questions
None for the author.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** ready; not started
<!-- progress:end -->
