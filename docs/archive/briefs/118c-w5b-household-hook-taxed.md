# 118 (W5b): The household hook, taxed, and the per-line account table

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 117c, 116c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 3.2 (steps 3 to 6), 3.4, 3.8 and the W5 row of section 4; (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`HouseholdHook`, its `post` and the `post` raise on value moving to the state); `model_v3/core/household.py` (`apply_payment`); `model_v3/core/kernel.py` (`step_year`, `_move`, `settle_B`, `settle_D`, `shortfall_lines`); `model_v3/core/revenue.py` (`run_lines`, `identity`); `tests/model_v3/test_household_hook.py`; `tests/model_v3/test_legacy_digest.py` (to pick the schedule).

## Goal
Let the household hook carry a WDT payment: the value the kernel moves to the state comes out of the line's non-pension classes pro rata, I1 holds after payment, and the deaths and the horizon settle correctly. Then produce the per-line account table the author reviews. Not switched on: the default arm stays legacy and nothing selects the hook outside tests and the table script.

## Decisions (author, 2026-11-22)
- Settlement by the existing routes; the payment is taken pro rata from the non-pension classes through `apply_payment`; pension is never sold; Route D keeps its lien.
- A payment above non-pension wealth is capped and reported (`unpaid_B`); it is a **model alarm**, expected zero. The table reports the count; a non-zero count is reported as an error in the model, not as a result.
- The author reviews a **per-line account table, no revenue or fund headline** (112r W5 review point). Saving is the three-value scenario axis (min, median, max); no value is called central.
- The `out_*` call sites that still pass `c` (`out_support.py:57,82,105`, `out_burden.py:77-79`) are **not** touched here: W7 withholds those outputs under the household arm.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: payment through the hook.** `HouseholdHook.post` accepts value moved to the state: for each line the true value moved (`fl.value`) is the payment `T`; call `apply_payment` on the line's class balances, set the closing positions, and recheck I1 (units equal N, pension equals the pension balance). Tests: the account identity `dNW = S + CG + TR + O - T_WDT` closes to 1e-9 for every line and year with tax on; payment shares follow the class weights; pension untouched; the I3 identity (`revenue.identity`) holds over several taxed years, not one. Push.
- **Block 2: deaths and the horizon.** The generation step and the horizon settlement (`settle_B`, `settle_D`, the lien settled by pro rata sale) under the hook: the settled amounts leave the non-pension classes pro rata and the account still closes; tests for a death year and the last year, with Route B in lien mode and Route D. Report whether `shortfall_lines` is empty in every test run. Push.
- **Block 3: the account table.** A script (`docs/model-v3/household-arm-account/account_table.py`, run with the repo's clean-room flags) running the centre grid point of the stored digest under the taxed household arm, for 14 lines at the three saving values, writing `account_table.csv` (line, saving value, year in {1, 10, 30, 100}: `dNW`, `S`, `CG`, `T_WDT`, `unpaid_B`, payment over net financial wealth, payment over non-pension wealth, the identity residual) and the note `docs/model-v3/household-arm-account.md`: the table for the author (headline: one row per line and saving value for years 1 and 30), the units, the schedule used, what each column means, the shortfall count, and plain statements of anything odd (negative wealth, a payment share above 1). **No revenue, fund or burden number anywhere in the note.** Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists, write the note from what exists and list the rest under Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/runner/arm.py`, `model_v3/core/household.py` only if a bug is found (report it), `tests/model_v3/test_household_hook.py` (additions) and a new test file if needed, `docs/model-v3/household-arm-account/` (new script and CSV), `docs/model-v3/household-arm-account.md` (new), `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not the kernel's tax code, `revenue.py` beyond a bug fix (report it), the register, the pack, `runner.py`, the `out_*` files, or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block; all suites pass (pre-existing data, cards and hooks failures reported as on main).
- With tax on: I1 and the account identity hold to 1e-9 in every line and year tested; the I3 identity holds over several years; deaths and the horizon close; `unpaid_B` is zero in every test, or the non-zero case is reported as a model error with its inputs.
- The account table covers 14 lines by three saving values at years 1, 10, 30 and 100, with the columns above and the identity residuals; the note contains no revenue or fund number.
- `arm.py` within 140; no upward import (R4); diff limited to Touches.

## Checks to run
`test_legacy_digest` after each block; v3 suites in the background (never piped); the account script with summary lines only on screen; `python -I pipeline/check_agent_docs.py`.

## Out of scope
The arm switch, withheld outputs, the `out_*` sites, the public ledger, comparators, a saving gradient, withdrawal, validation, any register or pack edit, any revenue or fund result.

## Open questions
Whether the death step needs a separate path for the pension (the balance passes to the next generation unchanged: agent states what it does and why).

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3. Block 1 and 2: `HouseholdHook.post` pays the value moved to the state (`fl.value`) from the non-pension classes (`apply_payment`, pro rata to the positive balances, pension never sold), rechecks I1; `reconcile(book)` pays value the kernel moves outside `post` (death tax, settle_D/settle_B, heir tax, horizon). Block 3: `household-arm-account/account_table.py`, `account_table.csv`, note `household-arm-account.md`.
- **Next:** NEEDS THE AUTHOR: the account table shows a payment shortfall (a model error) in the three richest lines at year 69 (see the report). Not merged.
- **Decisions:** payment weights are max(balance, 0); settlement value is the gap between the class total and the book's family value (`reconcile`); no separate pension path at death (balance in `book.pen`, passes unchanged); the table runs each line alone and stops a line at its first shortfall (the hook cannot carry a line with no non-pension wealth); incomes scaled by the B.6g factor 1.3733 as in 111c.
- **Gotchas:** `arm.py` 139 of 140 lines; arm test budget 210 to 330 (`test_household_tax.py`, architecture.md rows and totals). `revenue.run_lines` does not call `reconcile` after `settle_terminal` (outside Touches).
- **Resume:** `git fetch origin && git checkout brief/118-w5b-taxed-hook`; last block pushed: 3; waiting on the author's ruling on the shortfall.
- **Not run:** `check_gate.py --all` (fails on main already).
- **State:** blocks done, branch pushed, not merged, NEEDS THE AUTHOR
<!-- progress:end -->

```
Change report
- Task: brief 118c (W5b), the household hook with the WDT payment, and the per-line account table
- Files changed: model_v3/runner/arm.py (post pays the value moved to the state; reconcile; account; 139/140 lines); tests/model_v3/test_household_tax.py (new, 77 lines); tests/model_v3/test_household_hook.py (the W5b refusal test dropped); docs/model-v3/household-arm-account/account_table.py and account_table.csv (new); docs/model-v3/household-arm-account.md (new note); docs/model-v3/architecture.md (arm tests budget 330, totals, a paragraph); this brief
- What is different now: the household arm can run with the tax on: each line's payment is taken pro rata from its positive non-pension classes, pension is never sold, I1 and the account identity hold to 1e-9 in every tested year, deaths and the horizon settle through `reconcile`. The default arm is still legacy.
- New or changed interfaces: HouseholdHook.reconcile(book), HouseholdHook.account(); the post of a household hook no longer refuses a taxed year
- Acceptance criteria: test_legacy_digest passes unchanged (met; inside the model_v3 suite); all suites pass except the failures already on main (met: data 5, cards 1, hooks 1); I1 and the account identity hold to 1e-9 with tax on (met, largest residual 5e-12 in the table, 12 taxed years, deaths and horizon in tests); I3 identity over several years (met, six taxed years); deaths and horizon close (met in the tests); unpaid_B zero in every test (met in the tests; NOT met in the table run: see below); table covers 14 lines x 3 saving values x years 1, 10, 30, 100 with residuals and no revenue/fund number (met, except 9 year-100 rows blank by the stop below); arm.py <= 140 (139); no upward import (met); diff within Touches (met; one further file named: tests/model_v3/test_household_tax.py)
- Deviations from the brief: the table runs each line alone and stops a line at its first shortfall (the hook cannot carry a line with no non-pension wealth), so RL3, RL2 and RL1 have no year-100 rows; incomes in the table carry the B.6g factor 1.3733 (the 111c labelled run); arm test budget raised to 330
- Risks / follow-ups: MODEL ERROR for the author: at the centre grid point the three richest lines (RL3, RL2, RL1) cannot pay their tax from non-pension wealth in year 69 under all three saving values (unpaid_B 1.6, 13.3 and 107.7 millions per adult at the median saving); the kernel taxes the delta of wealth with the pension in it, the payment comes only from non-pension wealth, and the death years take 62% of it. The pension rule (design 3.8) or the schedule decides what to do; nothing was changed. The hook stops there (no route units). revenue.run_lines does not call reconcile after settle_terminal. The 087c grow() V0-scaling deviation is still unconfirmed.
- Instruction friction: none
- Verification: test_legacy_digest, budget, rules, arm and hook tests pass; `run_suites.py` 7 of 10 suites pass (model_v3 289 passed; data, cards, hooks fail as on main); check_agent_docs exit 0; account script run on screen shows summary lines only
- Overview sections likely needing an update: model v3 status (W5b done except the shortfall ruling), architecture 6.1
- Commit / branch: see git log, brief/118-w5b-taxed-hook
```
