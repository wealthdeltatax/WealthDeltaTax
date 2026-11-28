# 191: Compute each distinct scenario spec once

- **Status:** ready
- **Agent:** 2
- **Needs:** none
- **Length:** 1
- **Asks:** is S_low equal to S_central by design? If the scenario register meant them to differ, which parameter is missing
- **Author/date:** K. Ogata with the guru, 2026-11-28
- **Depends on:** none (152c touches the same evaluation path; if it merges first, build on it)
- **Read:** `results/speedup/root-methods.md` (the finding on S_low and S_central); `model-specs/` scenario register and `model/model_v3/inputs/` rows for the scenario points; `model/model_v3/runner/` (how level 1, the tornado and the O1e roots loop over scenario points); `project/agents/reference/code/speedup.md`

## Goal
In the `quick` run the S_low and S_central scenario specs are identical (466 of 466 level 1 cells byte-equal), yet level 1, the tornado and the roots compute both: 153c estimates about 600 s of 1,942 s. First settle whether that is right, then stop computing a repeated spec twice, with byte-identical output.

## Method
1. **Is it by design?** Read the scenario register and the spec that builds each scenario point. Say, for each of the 5 scenario points at `quick`, `final` and `smoke` size, which are equal as specs (compare the resolved spec, not the name). If S_low and S_central should differ and do not, that is a model finding: stop and report it to the author before changing anything (the `Asks` line); do not dedupe a register error.
2. **Dedupe:** key each evaluation by the resolved spec (a hash of the fields the run reads), compute once, and give every point that shares it the same result in its own place in the output. Level 1, the tornado, the roots and the map: wherever the loop runs over scenario points. The output must keep all five points, labelled as today.
3. Measure: the share of `quick` saved, at 1 and 2 workers, and the same at `final` size if the specs coincide there.
4. Housekeeping (small): `model/tools/bench.py` case `quick_headlines` still passes `--parts headlines`, which 178c replaced with `level1,map`; update it.

## Touches
`model/model_v3/runner/` (the loops over scenario points), `model/model_v3/run.py` if the plan needs it (the split run, 183c, makes the plan list units by point and scenario: dedupe must not change the unit list or the merged bytes), `model/tools/bench.py`, `tests/model/model_v3/`, `results/speedup/` (ledger row).

## Acceptance criteria
- `quick` and smoke outputs byte-identical to a same-setting before-file (`run_date` excluded), the split-run comparison still IDENTICAL, `fast` green on Actions.
- The decision on S_low and S_central written in the report with the evidence (the two resolved specs).
- Time saved at quick size measured on the hosted runner.

## Out of scope
Changing which scenarios exist; changing a scenario's values (author's call); the model.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
