# 123: The burden run's line flows include the horizon settlement

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 121c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-outputs.md` (the `fl` gap paragraph and the O2/O4a rows); (2) `docs/agents/code.md`. Later: `model_v3/core/burden.py` (`line_flows`), `model_v3/core/revenue.py` (`run_lines`, terminal settlement), `model_v3/runner/runner.py` (`core_run`), `tests/model_v3/test_arm_switch.py`.

## Goal
Under the household arm the burden run's line flows (`fl`) miss the horizon settlement of year T (about £639bn at the account's centre point), while M1 and the ledger include it, so M2, M2b to M2d and M4a are built on a different base. Make `fl` and `run_lines` agree in every year, with the settlement in year T. The legacy arm must not move.

## Decisions (author, 2026-11-22)
- The household arm is the one that changes; `test_legacy_digest` stays bit equal.
- Do not change the settlement rule (existing routes, pro rata from non-pension classes, `unpaid_B` alarm).

## Blocks
- **Block 0:** progress block pushed.
- **Block 1: find and fix.** Show where `line_flows` stops short of `run_lines` in year T under the household hook and make them equal; a test that the burden and the revenue receipts agree in all years including T, at two grid points, six phases. Report whether M2b to M2d are affected. Change report; push; stop.
**Stop rule.** If the fix needs a kernel change, stop and report it. Suites in the background, never piped.

## Touches
`model_v3/core/burden.py`, `tests/model_v3/` (additions), `docs/model-v3/household-arm-outputs.md` (the O2, O2b to O2d and O4a rows), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel, `revenue.py` beyond a bug fix (report it), the register, or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass.
- Burden and revenue receipts agree in every year including T under the household arm (test).
- The output-list note no longer says "known gap" for the fixed ids.

## Out of scope
Comparators, new outputs, any revenue or burden number for the author.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 and 1. Found: under the household hook `burden.line_flows` stepped the kernel to year T but never ran `settle_terminal`, which `revenue.run_lines` runs (Route D and B at the horizon, then `hook.reconcile`); the gap was in year T only (639.32 at the account's point, saving median). Fixed in `burden.line_flows` (5 lines, household arm only, the settlement counts with the death flows as `run_lines` classes it). Test: burden and revenue receipts equal in all 100 years, six phases, saving min and median. Suites: data 94, gate 17, hooks 87, model_v3 311 all pass; `test_legacy_digest` unchanged; check_agent_docs exit 0.
- **Next:** none for this brief; the comparators brief is the next household-arm step.
- **Decisions:** the terminal flows are added to `death` (as in `run_lines`: death_B, death_D), so M2 in life excludes them and M2b, M2c, M2d include them.
- **Gotchas:** the 121c note listed M4a with the gap; M4a reads `P5` and the pack deciles, not `fl`, so it was never affected (corrected in the note).
- **Resume:** none.
- **Not run:** two grid points are two saving values at the account's schedule, not a wider grid.
- **State:** done; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 123c, the burden run's line flows include the horizon settlement
- Files changed: model_v3/core/burden.py (line_flows, +4 lines); tests/model_v3/test_arm_switch.py (1 parametrised test, two cases); docs/model-v3/household-arm-outputs.md (O2, O2b to O2d, O4a rows and the fl paragraph); this brief
- What is different now: under the household arm fl and run_lines agree in every year including T; the legacy arm is untouched
- New or changed interfaces: none
- Acceptance criteria: test_legacy_digest unchanged and all suites pass (met); receipts agree in every year including T under the household arm (met, test: 100 years, six phases, saving min and median); the note no longer says known gap for the fixed ids (met)
- Deviations from the brief: none
- Risks / follow-ups: M2 in life leaves the settlement out by construction (it counts with the death flows); M2b, M2c, M2d now include it in windows that reach year T, so any household-arm M2b to M2d read before this fix was short; no number was published; the 121c note's claim that M4a was affected was wrong (M4a does not read fl)
- Instruction friction: none
- Verification: data 94, gate 17, hooks 87, model_v3 311 passed (background); check_agent_docs exit 0
- Overview sections likely needing an update: none
- Commit / branch: brief/123-fl-horizon, merged to main
```
