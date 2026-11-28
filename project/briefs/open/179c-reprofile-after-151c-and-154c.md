# 179: Re-profile after 151c and 154c, and decide what is left

- **Status:** review; branch `brief/179-reprofile`, change report below
- **Agent:** 3
- **Needs:** 151c, 154c, 176c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 151c, 154c, 176c
- **Read:** `results/run-cost/run-cost.md`; `results/speedup/ledger.md`; `model-specs/computational-architecture-hypothesis.md` (Scenarios A to C); `model/model_v3/core/kernel.py` (the year loop), `model/model_v3/runner/runner.py` (`core_run`); `model/studies/run-cost/bench.py`

## Goal
The guru's split of a `quick` run (level 1 about 1,100 s, tornado about 1,900 s, map about 240 s, roots about 300 s) is an estimate, and the claim that `core_run` is call overhead in many small array operations is a hypothesis. Measure both on the code after 151c and 154c, then say which lever is next. Measurement only; no model change.

## Design
1. **Where the time goes.** The `quick` run split by part (level 1, map, tornado, O1e), serial and at workers 0, on this machine, best of 2.
2. **Inside `core_run`.** `cProfile` (and `perf`-style sampling if available) of one household evaluation at 20 and 200 paths: top 20 functions by own time, number of numpy calls per simulated year, median array size per call, share of time in calls on arrays under 1,000 elements, time in Python bytecode outside numpy.
3. **Call-overhead test.** For the hot year-loop body, estimate the floor: the same operations on the same sizes in one tight timing loop. If the real time is more than 3 times that floor, call overhead dominates.
4. **Decision table, written before measuring:**

| finding | next |
|---|---|
| over 50% of `core_run` in calls on arrays under 1,000 elements, and more than 3 times the floor | compiled year loop: 180c |
| the same, and many redundant operations visible (same product computed twice, copies) | numpy restructure first (152c), then re-measure |
| large-array work dominates | vectorisation or memory layout; kernel compile will not help; write a brief for the top function |
| `again` runs or welfare solves still large | a second headline-only style cut, from the profile |

5. Update the projections in `results/run-cost/run-cost.md`: `quick` and the final run, serial, 2 workers, 4 workers, 14 workers, each labelled measured or estimated.

## Touches
`results/speedup/profile-after-154c.md` (new), `results/run-cost/run-cost.md` (projection section), `model/studies/run-cost/` (profile script), `results/speedup/ledger.md`. Not model code.

## Acceptance criteria
- Both tables filled with measured numbers; the decision table's row named and the reason given with the numbers.
- The guru's estimate and the measurement side by side; any part off by more than 30% is flagged.

## Out of scope
Any code change to the model, including cheap fixes found on the way: write them as `project/brief-suggestions.md` entries.

## Open questions
None for the author.

## Implementation notes
<!-- progress:start -->
- **Done:** all five items measured and written up; `profile-after-154c.md`, projections in `run-cost.md`, ledger rows, suggestion entry.
- **Next:** author reads the change report.
- **Resume:** nothing to resume.
- **State:** done
<!-- progress:end -->

## Change report
- **What changed:** `model/studies/run-cost/profile_after_154c.py` (new); `results/speedup/profile-after-154c.md` and `profile-after-154c/` raw JSON (new); `run-cost.md` new projection section; `ledger.md` two rows; `project/brief-suggestions.md` one entry. No model code.
- **Result:** `quick` is 1,942 s serial and 1,210 s on 2 cores. Level 1 is 75% of it. Level 1 is array-bound (9% fixed time, 1.4x the floor at 1,000 paths): decision-table row 3, no compile. Tornado, map and roots (24%) are call-bound (3.5 to 4.1x the floor, 100% of calls under 1,000 elements at 20 paths) with visible redundancy: row 2, 152c first. Estimates off by more than 30%: level 1 (+33%), tornado (-81%), map (-76%), roots (-80%); the last three predate 151c and 186c.
- **Caveats:** one `quick` run per setting (32 and 20 minutes), not best of two. The floor counts visible numpy calls only (operators uncounted), so it is a lower bound. 4-worker `quick` figure is from Actions (177c); 14-worker and every final-size figure is estimated.
- **Author questions:** none.
