# 133: Carry the tax the kernel cannot collect as a lien (the median_high case)

- **Status:** draft (needs the author's choice of design in Decisions before release)
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 132c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-lien.md` ("Not carried"); (2) `docs/agents/code.md`. Later: `model_v3/core/kernel.py` (`_cap` line 225, the route payments 250 to 280, `settle_B` 454, `step_year`); `model_v3/core/pension_lien.py`; `model_v3/runner/arm.py` (`pre`, `_pay`, `settle`); `docs/model-v3/household-arm-i1-floor.md`.

## Goal
At `median_high` the tax on pension gains takes all the non-pension wealth of nine lines (D1 to D10b, years 70 to 97). The kernel caps each payment at the line's route units and records the excess in `unpaid_B`, so the household hook never sees an unpaid amount and 132c's lien cannot arise (3,000 shortfall lines, unchanged). Carry that excess as a lien so the account closes without a shortfall alarm.

## Decisions (author, 2026-11-22; the design choice is open)
- Same rule as 132c: the unpaid tax is deferred, accrues at `r_def`, is a receivable of the public ledger, and is settled at death and at the horizon (classes, then the one-off pension draw). Nothing is tuned.
- **Choice for the author:** (a) the kernel keeps the excess in a book-level lien `PL` netted from the family value (the lien lives in the kernel, the hook reads it); or (b) `_cap` returns the excess to a callback the hook supplies, so the lien stays in `pension_lien.py` and the kernel has one new call. The guru leans to (b): one lien implementation, a smaller kernel change. The agent states the rule it used if the author has not chosen.

## Blocks (one push each)
- **Block 0:** progress block pushed.
- **Block 1:** the kernel change behind a flag that defaults to today's behaviour, so the legacy digest and every passing point are unchanged. Tests: a toy line whose units run out (excess carried, accrues, settles), the legacy digest unchanged.
- **Block 2:** the hook and ledger use it; `median_high` rerun (20 paths) with the 132c checks; note `docs/model-v3/household-arm-lien.md` updated, not a new file. **No headline number.**
**Stop rule.** If the change alters any legacy number, stop and report the case. After two blocks or a quarter of the budget left, push and list the rest.

## Touches
`model_v3/core/kernel.py` (the cap and the flag), `model_v3/core/pension_lien.py`, `model_v3/runner/arm.py` (calls), `model_v3/core/revenue.py` only if the ledger needs it, tests, `docs/model-v3/household-arm-lien.md`, `docs/model-v3/household-arm-run/` (labelled rerun CSVs), `architecture.md` (budget rows). Name any further file before editing it. Not the register, the pack or the manifest.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; the three passing points and the account CSVs byte-identical.
- At `median_high`: I1, the account identity (1e-9) and the ledger ties hold; `shortfall_lines` and `unpaid_B` are reported before and after; the remaining cases, if any, are listed with balances.
- The floor alarm of 127c (lines with zero units) is reported separately: it is a different failure and this brief does not remove it.

## Out of scope
The deferral rate (134r), the heir's share of the pension, the 127c floor alarm, per-path returns (128c), any headline number.

## Open questions
The design choice above; where the kernel's own pension is read from for the settlement draw (the agent states it).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** none
- **State:** draft; not started
<!-- progress:end -->
