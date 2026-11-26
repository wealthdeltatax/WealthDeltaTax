# 151: Headline-only evaluation for the tornado and the O1e roots

- **Status:** draft (provisional; released after 044c, and only with the `quick` byte-reference file in hand)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 057c (the `quick` run size and its reference file), 150c (merged, the timing scripts), 044c (the file move; all paths below are pre-move and are rewritten by it)
- **Read (block 0: the first two only):** (1) `results/run-cost/run-cost.md` ("Cost by part", "What is left"); (2) `project/agents/agent-code.md`. Later: `model/model_v3/runner/runner.py` (`core_run` 197, `headlines` 220, `evaluate` 235, `make_ev` 257); `model/model_v3/runner/sweeps.py` (`headline`, `tornado` 86, `breakeven_return` about 125); `model/model_v3/runner/pool.py`; `model/studies/run-cost/timing.py`; `model-specs/computational-architecture-hypothesis.md` (Scenario A).

## Goal
Make the tornado and the O1e roots several times cheaper without changing a number. Today every evaluation they call runs `core_run` five times (one base, and the `again` runs the output groups ask for) and the support group's welfare solves, although the tornado reads only the headlines M1, M2 and M3 and an O1e root reads only `['M1']['short']`. Those two steps are over 90% of a full run. The guru's profile (2026-11-23, household arm, 400 paths) puts the work in many small array operations, so skipping whole evaluations saves more than speeding up any one of them.

## Decisions (author, 2026-11-23)
- Option 1 of the guru's speed-up list goes first and alone: a headline-only evaluation. The author liked the whole list; options 2 to 4 below are not part of this brief.
- Byte-identical. The model, the register, the kernel, `arm.py` and the manifest do not change. Level 1 and every full evaluation (the groups, OB1, OM1, OS1, welfare) stay as they are.
- Follow-up briefs, each written only after this one's measurement: **152c** one year loop shared by burden and ledger under the household arm (touches `arm.py` and the wiring); **153c** fewer evaluations per O1e root (secant or Brent, bracket from the previous root), which is not byte-identical, so it carries its own tolerance rule and needs the author's sign-off; **154c** level 1 chunks through `pmap`; then stacked class arrays and selective Numba on whatever the profile still shows. Rust and Julia (Scenarios B and C of the hypothesis) stay on hold until these are measured.

## Design
1. A switch on the evaluator (`make_ev(..., heads_only=True)`, or a second factory; the agent says which and why): it calls `core_run` once and `headlines`, and returns the headline keys exactly as `evaluate` does, with no group results. Default off, so every existing caller is unchanged.
2. `sweeps.tornado` and `sweeps.breakeven_return` use it, and `run.py` (057c's file) passes it for them. The feasibility map's evaluations keep the full evaluator unless the agent shows the map reads headlines only.
3. Read the callers first and list every key each one reads (`headline()`, `HEADS`, the O1e lambda). If any caller reads a group result, it stays on the full evaluator and the brief says so.
4. A test that the headline-only result equals `evaluate`'s headline keys to the last byte (floats by hex, arrays by buffer, as `test_pool.py` does), on both arms, at least three specs and two input overrides.

## Blocks (one push each; `project/agents/agent-code.md`)
- **Block 0:** progress block pushed.
- **Block 1:** the switch and its test; `test_legacy_digest` unchanged.
- **Block 2:** the callers use it; the `quick` run reproduces the reference file byte for byte; timing before and after (tornado, one schedule; one O1e root; the `quick` run), best of two, on this machine, in `results/run-cost/run-cost.md` as a new section, with the profile top ten before and after.
- **Block 3:** the note: what the measurement says about 152c to 154c (which is now the largest share), and an updated projection of the full run.
**Stop rule.** If any caller reads a group result, or the byte comparison fails once, stop and report the case; do not loosen the comparison. After three blocks or a quarter of the budget left, push and list the rest.

## Touches
`model/model_v3/runner/runner.py` (the switch; the file is at its 360-line budget, so the agent either moves a function out or raises the budget row in `architecture.md` and says which), `model/model_v3/runner/sweeps.py`, `model_v3/run.py`, `tests/model/model_v3/` (a new `test_heads_only.py`; `conftest.py` LAYER row and `test_groups.py` if the layer table needs a row), `results/run-cost/run-cost.md` (a section), `model-specs/architecture.md` (budget rows only), the `quick` timing script. Name any further file before editing it. Not the kernel, `arm.py`, the register, the pack or the manifest.

## Acceptance criteria
- The headline-only result is byte-identical to the full evaluator's headline keys on both arms (test).
- The `quick` output file is byte-identical to the reference taken before 009c and 044c; `test_legacy_digest` and all suites pass.
- Timings before and after are reported with the machine, path count and spec, for the tornado, one root and the `quick` run; the saving is stated as measured, against the guru's estimate of 3 to 5x, and if it is under 2x the note says why and what remains.
- `git diff --stat` limited to Touches.

## Out of scope
Any change to a number, to the root-finding method, to the arm code or to the kernel; parallelising level 1; Numba, Rust, Julia; reducing the sizes of the run (paths, draws).

## Open questions
None for the author. The agent states which of the two designs in step 1 it used.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0 (after 044c merges)
- **Resume:** none
- **State:** draft; not started
<!-- progress:end -->
