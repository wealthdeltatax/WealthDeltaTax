# 132: Pension-secured lien for the tax a line cannot pay from non-pension wealth

- **Status:** ready (coordinate with 128c: both touch `arm.py` and the ledger; whichever merges second rebases)
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 127c (merged), 120c (ledger)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-i1-floor.md` (the fix and the two cases); (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`HouseholdHook.pre`, `post`, `_pay`, `reconcile`, `account`, the 127c floor); `model_v3/core/household.py` (`apply_payment`, `lien`); `model_v3/core/revenue.py` (the ledger recursion, `receipts`); `model_v3/core/kernel.py` (the Route B lien: `LB`, `r_def`, `settle_B`: read only, to reuse its rate and settlement points).

## Goal
127c made exhausted lines report instead of raising, but the cause is economic: at `median_high` the tax on pension gains takes all the non-pension wealth of nine lines (D1 to D10b) in years 70 to 97, and at `min_mid` dissaving plus tax exhausts D4 and D5. The author ruled (2026-11-22): **the unpaid tax is carried as a lien against the pension and settled later**. Pension stays inside the base and is never sold during life; it is drawn only to settle the lien.

## Decisions (author, 2026-11-22)
- **Lien.** The part of a year's WDT the non-pension classes cannot pay (today `unpaid`, taken as net financial debt in 127c) becomes a **pension-secured deferred balance** `PL` per line: it accrues at the same deferral rate `r_def` the Route B lien uses (the agent reads it; a scenario value, not invented; real 0.0 if the register sets none, said in the label), appears as debt in the account, and is **not** a receipt of the year.
- **Settlement.** `PL` is settled **at death and at the horizon**: first from the non-pension classes pro rata (as the existing settlement), then, for any remainder, by a **one-off draw on the pension** (the only time pension is drawn). Where even that is insufficient the remainder is `unpaid_B` and an alarm (expected zero).
- **Ledger.** The lien is a **receivable of the public ledger** (accrues at `r_def`); the year's receipts exclude it; settlement moves it into the receipts by class (the pension draw enters in the line's class mix at that time, like any payment). The 120c identities (payments equal receipts by class; `dL = receipts + return - payout`) hold with the receivable as a separate ledger line, to 1e-9.
- No other rule changes: the pension accrual, the I-D1l opening cap, the settlement of Routes A, B, C and D, and the legacy arm are untouched. Nothing is tuned.
- A line that never needs the lien records none, and the three passing grid points and the 14-line account CSVs stay **byte-identical**.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: the lien in the household account.** Pure functions in a new `model_v3/core/pension_lien.py` (accrue, add, settle against classes then pension; budget 80, row in `architecture.md`) so `arm.py` (budget 255, at 253) takes only the calls; the hook uses them in `_pay` (replacing the net-financial debt of 127c), in `pre` (accrual) and in the death and terminal settlement; `account()` reports `PL`. Tests: toy line driven to exhaustion (lien created, accrues, settles at death from classes, then pension, I1 and the account identity hold); a line that never needs it records none; pension never reduced in life; legacy bit equal. Push.
- **Block 2: the ledger.** Receivable line in the public ledger (`revenue.py`), year receipts exclude the lien, settlement enters by class; tests: the 120c ties with a lien present, a lien settled in the terminal year, all six phases. `test_legacy_digest` unchanged. Push.
- **Block 3: rerun and note.** Rerun the two points of 127c (`min_mid`, `median_high`, 20 paths; the arm has no spread) and the three passing points (must be byte-identical). `docs/model-v3/household-arm-lien.md`: where the lien arises (line, year, amount), its size against the line's pension and wealth, how long it is carried, how much settles from classes against pension, whether `unpaid_B` stays zero, and the checks. **No headline number.** If the lien is still unpaid at settlement for some line, report it plainly. Change report; push; stop.
**Stop rule.** If the settlement design needs a kernel change, stop and report it with the case. After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Suites in the background, never piped.

## Touches
`model_v3/core/pension_lien.py` (new), `model_v3/runner/arm.py` (calls only; name any raise), `model_v3/core/revenue.py` (the ledger receivable, +40), tests (`test_household_tax.py`, `test_ledger.py`, a new `test_pension_lien.py`), `docs/model-v3/household-arm-lien.md` (new), `docs/model-v3/household-arm-run/` (labelled rerun CSVs), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel (stop and report), the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; the three passing grid points and the account CSVs byte-identical.
- I1, the account identity (to 1e-9) and the ledger ties hold with a lien present, in all six phases and in the terminal year.
- `shortfall_lines` and `unpaid_B` at `min_mid` and `median_high` are reported after the change; the floor alarm of 127c no longer fires where the lien now carries the tax, or the remaining cases are listed with their balances.
- The pension is reduced only at lien settlement (a test).

## Out of scope
Pension withdrawal in life, a running pension cap, a saving gradient, per-path returns (128c), changing the base so pension is excluded, any headline number.

## Open questions
The deferral rate (read from the Route B lien; the agent states the value and its source); whether the settlement draw on the pension should be limited to what the heir would receive (the agent states the rule it used and why).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/132-pension-lien origin/brief/132-pension-lien`
- **State:** ready; not started
<!-- progress:end -->
