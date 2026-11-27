# 176: Speed-up bench and the rules every speed-up follows

- **Status:** author; pushed on `brief/176c-speed-up-bench-and-rules`, not merged: the small bench cases total 5.2 min against the criterion of under 3 (all other criteria met). Guru recommends option (b) of its report: move `tornado_1sched_20` and `level1_1sched_1000` out of the default set
- **Agent:** 6
- **Needs:** none
- **Length:** 1
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
3. **`bench.py compare A B`:** per case the time ratio and `identical: yes/no`; output files are compared with the `run_date` line excluded (151c's two `quick` files differed only there, because the runs straddled midnight; `accept.sh --compare` has the same exposure, so the agent either excludes the line there too or pins it, and says which); refuses to compare files with different numerics settings or CPU model unless `--force`, and says so.
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
- **Done:** all blocks. After the author's ruling (2026-11-27, option 2) the default case set is eval_hh_20, eval_leg_20, root_1_20; tornado_1sched_20 and level1_1sched_1000 are on request.
- **Next:** guru retires the brief.
- **Resume:** none
- **State:** merged
<!-- progress:end -->

## Change report
```
Change report
- Task: 176c speed-up bench and the rules every speed-up follows
- Files changed: model/studies/run-cost/bench.py (new); tests/model/tools/test_bench.py (new, 7 tests); project/agents/reference/code/speedup.md (new, 21 lines); project/agents/agent-code.md (one line); results/speedup/ledger.md (new, seeded with 6 rows from 150c); friction log; this brief
- What is different now: `python -I model/studies/run-cost/bench.py run --out FILE` times the named cases (best of 2, header, result hashes) and `bench.py compare A B` says per case the time ratio and `identical: yes/no`, exits 1 on a difference and refuses files from a different CPU model, numpy version or numerics setting unless `--force`
- New or changed interfaces: bench.py run | compare | list; case names eval_hh_20, eval_leg_20, tornado_1sched_20, root_1_20, level1_1sched_1000 (small), quick_headlines (unavailable until the --parts switch of 178c, says so), quick_full (run.py --size quick, hash of outputs.json with the run date masked; default one rep)
- Acceptance criteria:
  - bench.py run twice, hashes identical (met: all 5 small cases identical), times within 15% (met: ratios 0.93 to 1.02; spread: eval_hh_20 13.7 and 12.8 s, eval_leg_20 3.0 and 3.0, tornado 150 and 143, root 26.6 and 24.7, level 1 130 and 129)
  - test that compare flags a one-bit change and refuses mismatched headers (met: test_bench.py, float and array, three header keys, forced, warning on cores, command line, date mask)
  - small cases total under 3 minutes: met after the author's ruling of 2026-11-27 (option 2): default set eval_hh_20, eval_leg_20, root_1_20, best times 12.6 + 3.0 + 25.9 = 41.5 s, a whole `run` 131 s with the warm-up and two reps; two default runs identical, ratios 0.95 to 1.02. First measurement with five cases was NOT MET: Best times of run 2 add to 312 s (5.2 min); a whole `run` including the warm-up call and the second rep takes 818 s (13.6 min). This machine is slower than in 150c (one household evaluation 12.8 s against 8.9 s; tornado of one schedule 143 s against 74 s), and with the 150c figures the five cases would add to about 176 s. Dominant cases: tornado_1sched_20 (143 s) and level1_1sched_1000 (129 s); without those two the three others total 40 s
  - rules file within 40 lines (met: 21); check_agent_docs.py exit 0 (met)
- Deviations from the brief: the checks `run_suites.py tools` and `project` do not exist as suites (no conftest.py): ran `python -m pytest tests/model/tools` (12 passed) and `tests/project` (22 passed) directly; quick_full not run (about an hour; not an acceptance criterion); `README` line: no README exists in run-cost
- Risks / follow-ups: quick_full and quick_headlines are written but unrun; the tornado and level 1 cases remain available with --cases; the ledger row for root_1_20 in 150c is the bracket-check root
- Instruction friction: one entry added (run_suites names; time criterion from another machine)
- Verification: bench run twice and compared (the table above); tests/model/tools 12 passed; tests/project 22 passed; check_agent_docs exit 0; the date-mask pattern matches the one `run_date` in results/057c-evidence/quick-q4/outputs.json
- Overview sections likely needing an update: none
- Commit / branch: brief/176c-speed-up-bench-and-rules; merged to main after the author's ruling; brief 176c merged, ready to retire
```
