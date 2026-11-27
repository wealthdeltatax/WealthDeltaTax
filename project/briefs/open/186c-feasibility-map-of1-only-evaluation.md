# 186: Feasibility map by an OF1-only evaluation

- **Status:** author; done on `brief/186-map-of1-only`, pushed, not merged; needs the author to merge
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
- **Done:** all of it (report below). **Next:** author merges. **State:** done
<!-- progress:end -->

```
Change report
- Task: 186c Feasibility map by an OF1-only evaluation
- Files changed: model/model_v3/runner/runner.py (`evaluate` and `make_ev` take `only=`, group names; default all; 368 lines, unchanged count); model/model_v3/run.py (the map's evaluator is built with `only=('sweeps',)`); tests/model/model_v3/test_heads_only.py (equality test, both arms); model/studies/run-cost/map_only.py (timing script, new); results/run-cost/run-cost.md (section); results/speedup/ledger.md (one row); this brief.
- What is different now: the feasibility map runs only the OF1 group, so it no longer computes the revenue, burden and support per-path results. Every number is unchanged.
- New or changed interfaces: `evaluate(..., only=None)`, `make_ev(..., only=None)`; none on the command line.
- Acceptance criteria: (1) selected-group `of1` byte-identical to the full evaluator on both arms: met (test, 3 specs each; also the headlines). (2) `quick` output equal to a before-file made with the same numerics setting, `run_date` excluded: met (Actions run 46069300028, before = main 8da93c2, after = this branch, forced path, 270,571 characters equal). (3) all suites and the tripwire pass: met (`fast` job, Actions run 46067095370, success; local: test_heads_only, test_of1, test_runner, test_budget pass). (4) map time before and after against the guess: met, 329 s to 62 s for the whole quick map on 2 cores, workers 1 (5.3x; 174 s to 33 s at workers 0), under the 100 s target; map points and OF1 byte-equal in every case (`map_only.py`).
- Deviations from the brief: the selector is passed where the map's evaluator is built (`run.py`), not inside `sweeps.feasibility`, which takes `ev` as an argument. The `quick_headlines` case was not timed (178c not read). Wall times of the two quick jobs on Actions (1,427 s before, 1,723 s after) are different hosted machines and not a measurement of the change.
- Risks / follow-ups: the OF1 group's independence rests on `Env.rng(name)` being keyed by group name; a group that draws from a shared stream would break the equality test, which would show it. Whole-run saving on a quiet 2-core machine was not measured (the map is about 15% of what is left of a quick run).
- Instruction friction: none beyond: a short sha is not accepted by `actions/checkout` as a ref (use the full sha).
- Verification: tests above; map timings in run-cost.md; the temporary workflow `186c-quick.yml` is removed in this commit.
- Overview sections likely needing an update: none
- Commit / branch: see the branch head, `brief/186-map-of1-only`
```

