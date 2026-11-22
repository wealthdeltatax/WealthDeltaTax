# 127: I1 at the class floor: reconcile the class book with the kernel's family value

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 124c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-run.md` (the Checks section and Odd item 7); (2) `docs/agents/code.md`. Later: `docs/model-v3/household-arm-run/run_grid.py` and `checks.csv`; `model_v3/runner/arm.py` (`HouseholdHook.pre`, `post`, `reconcile`, the I1 check and the 0%-real debt floor); `model_v3/core/household.py` (`household_step`, `apply_payment`); `model_v3/core/kernel.py` (where the family value is floored at 0).

## Goal
Two grid points of 124c raise I1 before any output exists: `min_mid` (threshold ratio 0.25, line D5, year 78: non-pension class total -0.0012, net financial -0.1329, against a family value floored at 0) and `median_high` (ratios 0.25 and 0.5, line D10a, years 70 and 97: non-pension classes 0.0015, pension 6.45). Make a line whose non-pension classes are exhausted **report** through the model's alarms (`unpaid_B`, shortfall lines) instead of raising, and find out which of the two cases is a bookkeeping disagreement and which is economics.

## Decisions (author, 2026-11-22)
- **Fix the class floor only.** No change to household behaviour, asset economics, the pension rule (never sold, illiquid, inside the base) or the settlement rule. The failures stay visible as alarms for the author to rule on; no result is tuned to make a check pass.
- The three passing grid points and the 14-line account at the three saving values must be **byte-identical** before and after (their CSVs). If the fix moves any of them, stop and report.
- Pension gains continue above the opening cap; this brief does not add a running cap or withdrawal.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: diagnose.** For each failing point, locate the first year the class total and the kernel's family value disagree, and say which rule is responsible (the kernel floors a negative family value at 0 while the class book goes slightly negative; the 0% real debt floor; a payment capped at non-pension wealth). Write the finding as a two-case table in the note (point, line, year, class balances, kernel value, rule responsible, bookkeeping or economics) before changing code. Push.
- **Block 2: the fix and tests.** Make the book and the kernel agree at the floor (in `arm.py` or `household.py`, say which and why; a kernel change is a stop-and-report), so an exhausted line is capped and `unpaid_B` or the shortfall alarm records it. Tests: a toy line driven to exhaustion (I1 holds, the alarm is recorded, no raise); the three passing points and the account CSVs byte-identical; `test_legacy_digest` unchanged. Push.
- **Block 3: rerun and note.** Rerun the two failed grid points through `run_grid.py` (1,000 paths is not needed; the arm has no spread: use 20) and report their checks. Write `docs/model-v3/household-arm-i1-floor.md`: the diagnosis, the fix, the two points' results (checks, and whether the alarm now fires and where). **No headline number.** Change report; push; stop.
**Stop rule.** If the diagnosis shows the failure is economics (a line whose non-pension wealth is genuinely exhausted by tax on pension gains) rather than bookkeeping, make the alarm report it, do not change any rule, and say so plainly. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 245, now FULL: any addition needs a raise or a move into `core/household.py`; name it), `model_v3/core/household.py` (budget 120), tests (`test_household_tax.py`, `test_run_grid.py`), `docs/model-v3/household-arm-i1-floor.md` (new), `docs/model-v3/household-arm-run/` (rerun of the two points, labelled), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel (stop and report), `revenue.py`, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; the three passing grid points and the account CSVs byte-identical.
- No raise at `min_mid` and `median_high`; each failing line is reported through an alarm with point, line, year and balances.
- The note says, per case, bookkeeping or economics, with the evidence.

## Out of scope
Pension withdrawal, a running pension cap, per-path returns, any change to the settlement or pension rules, validation, headline numbers.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3; branch pushed for review (do not merge)
- **Next:** none; the author rules on the alarms (see the note)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/127-i1-class-floor origin/brief/127-i1-class-floor`
- **State:** done, awaiting review
<!-- progress:end -->
