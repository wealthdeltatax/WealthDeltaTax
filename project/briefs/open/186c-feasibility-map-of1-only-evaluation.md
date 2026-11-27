# 186: Feasibility map by an OF1-only evaluation

- **Status:** hold; ready after 154c merges
- **Agent:** 5
- **Needs:** 154c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-27
- **Depends on:** 151c (merged: `heads`), 154c (both change `runner/runner.py`, at its 360-line budget; do not edit it in parallel), 176c (bench; soft)
- **Read:** `model/model_v3/runner/runner.py` (`evaluate`, `make_ev`, `GROUPS`); `model/model_v3/runner/out_sweeps.py` (`per_path`, the OF1 group); `model/model_v3/runner/sweeps.py` (`feasibility`, `grid`); `results/run-cost/run-cost.md` ("Headline-only evaluation (151c)": the map is about 15% of what is left of a `quick` run)

## Goal
The feasibility map evaluates every point of the lever grid with the full evaluator and reads only `e['sweeps']['of1']`: per path `p3`, `M2` and `M4a` for each margin and horizon. Every other group's `per_path`, and the extra `core_run` calls behind them (`again`), are computed and thrown away. 151c cut the same waste from the tornado and the roots (5.49x); the map was left because `heads` stops before the OF1 group. Run only the OF1 group for the map. The map is on the path of every run, including the 178c fast loop (the named schedules come from it), so it sets a floor on the loop.

## Decisions (author, 2026-11-27)
Cheaper map approved with moving the kernel spike ahead, to keep the 10-minute `quick` target. Byte-identical lever.

## Design
1. `evaluate` (and `make_ev`) take a group selector, for example `only=('sweeps',)` or the group's `NAME`; the default (all groups) is unchanged. The headlines are still returned. `feasibility` passes the selector. `of1`'s group is the only one run; `again` stays as it is (the OF1 group asks for `core_run` variants; count them: if it needs more than the base run, say so).
2. **Check first that the groups are independent.** If any other group draws from `env.rng` before the OF1 group, skipping it would change the OF1 stream. State from the code (file and line) that none does, and test byte equality of `e['sweeps']['of1']` selected against the full evaluator on both arms, 20 paths and the `quick` map, as `test_heads_only.py` does.
3. Time before and after with `bench.py` if merged, else `timing.py`: one map point, the whole `quick` map, workers 1 and 0; and the `quick_headlines` case once 178c lands.
4. If `evaluate` growth breaks the `runner.py` budget, move a function out (say which) or raise the budget row in `architecture.md` and say so.

## Touches
`model/model_v3/runner/runner.py`, `model/model_v3/runner/sweeps.py`, `tests/model/model_v3/` (equality test), `model-specs/architecture.md` (budget rows only), `results/run-cost/run-cost.md` (a section), `results/speedup/ledger.md` (one row).

## Acceptance criteria
- Selected-group `of1` byte-identical to the full evaluator on both arms (test); the `quick` output file byte-equal to a before-file made on the same machine with the same numerics setting, `run_date` excluded as 176c does; all suites and the tripwire pass.
- Map time before and after, measured, against the guess (about 330 s of a `quick` run on 2 cores, to under 100 s); if the saving is under 2x, say why (the base `core_run` dominates) and what remains.

## Out of scope
Changing the grid, the rules (`TOLS`, `MARGINS`) or `choose`; the kernel (180c); any change to a number.

## Open questions
None for the author.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** hold
<!-- progress:end -->
