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
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/123-fl-horizon origin/brief/123-fl-horizon`
- **State:** ready; not started
<!-- progress:end -->
