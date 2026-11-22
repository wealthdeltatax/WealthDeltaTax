# 120 (W6): The public ledger by class, with death and terminal payments reconciled in the year

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 119c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 3.5 and the W6 row of section 4; (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`HouseholdHook.pre`, `post`, `reconcile`, `account`); `model_v3/core/revenue.py` (`run_lines`, `fund`, `revenue`, `identity`); `model_v3/core/kernel.py` (`state_true`, the refund cap); `tests/model_v3/test_household_tax.py`.

## Goal
One public ledger by class replaces the state's stake and the fund's bare cash recursion, so household payments and public receipts tie by class, path and year. Payments that a death or the terminal settlement move are paid in the year they happen, not at the next year's opening. Not switched on: the default arm stays legacy.

## Decisions (author, 2026-11-22)
- Ledger: `L[k]` per class (property, net financial, physical, plus the safe asset), per path and year, market value; `L_t+1 = L_t (1 + g_k) + receipts_k - payout_k`. The pension is not a ledger class. WDT receipts enter in the paying line's non-pension class mix at the time of payment; the corporate levy enters as cash under `safe_share` (Q10, as today). Class returns are the household's `g_k` (scenario ranges, I-D1h to I-D1j).
- `fund()` keeps its reserve rules; its balance and return are read from the ledger (`rr = sum_k L_k g_k / L`); `revenue.py` stops passing the bare path `g`; `state_true` returns the ledger value. Under the legacy arm nothing moves (digest gate).
- **Reconcile in the year.** `HouseholdHook.reconcile` runs immediately after a death step and after `settle_terminal`, not at the next year's `pre`. 118c found `run_lines` does not call it after the terminal settlement, so a final-year death or horizon payment has no later year to be caught in. This is an acceptance requirement.
- The pension stays in the assessed base and outside every payment source; refunds reconcile with household balances (refund cap reads the ledger class value of that route's stake).
- No price response to a sale (the counterparty is outside the modelled sectors). No revenue, fund or burden headline is produced or reviewed here: the author reads the ledger identity table.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: reconcile in the year.** Call `hook.reconcile` after the death step and after `settle_terminal` inside `revenue.run_lines` (name the exact sites). Tests: a death in the **last simulation year**; the terminal settlement; all six phases (`n_phase=6`); `unpaid_B` zero in the production path (`run_lines`), not only in the account script. `test_legacy_digest` unchanged. Push.
- **Block 2: the ledger.** Class receipts out of the hook (per year, by class, true value; the hook is built by the runner and passed down, so `revenue.py` imports no `runner`), the ledger recursion in `revenue.py`, `fund()` reading balance and return from it, `state_true` reading it, the refund cap's stake term. Keep layering (R4): the ledger takes arrays, not the hook. Push.
- **Block 3: the tying tests and the identity table.** Per path and year: `sum over lines of weight x T_WDT = ledger receipts` and `dL = receipts + return - payout` to 1e-9; all six phases; refunds; a final-year death. A script `docs/model-v3/household-arm-account/ledger_table.py` writing `ledger_table.csv` (per year in {1, 10, 30, 100}: receipts by class, return, payout, closing balance by class, the two residuals) and a note `docs/model-v3/public-ledger.md`: what the ledger is, units, the identities, what it does not do. **No revenue, fund-fill or burden headline.** Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/core/revenue.py` (+60), `model_v3/core/kernel.py` (`state_true`, +5), `model_v3/runner/arm.py` (class receipts out of the hook; budget 160, name any raise), `model_v3/runner/runner.py` only if it must pass the hook's receipts down (stays 360; report any raise), tests (`test_revenue.py`, `test_household_tax.py`, a new ledger test file), `docs/model-v3/household-arm-account/ledger_table.py` and CSV, `docs/model-v3/public-ledger.md`, `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not `burden.py` (`free_path` unchanged), `support.py`, the `out_*` files, the register, the pack, or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block; all suites pass (pre-existing failures reported as on main).
- Household payments equal ledger receipts per path and year, by class, to 1e-9; `dL = receipts + return - payout` to 1e-9; all six phases and a last-year death covered.
- Death and terminal payments are made in the year they occur (the tests would fail under the old next-year catch-up).
- `unpaid_B` is zero in the production path in every test, or the non-zero case is reported as a model error with its inputs.
- Pension is in the assessed base and never in a payment or ledger class; refunds reconcile.
- Layering R4 test passes; diff within Touches; budgets held.

## Checks to run
`test_legacy_digest` after each block; v3 suites in the background (never piped); the ledger script with summary lines only on screen; `python -I pipeline/check_agent_docs.py`.

## Out of scope
The arm switch, withheld outputs (W7), comparators, pension withdrawal, saving gradient, validation, any revenue or fund result, a price response to sales.

## Open questions
How the hook hands class receipts to `revenue.py` without an upward import (agent states the interface and why).

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout brief/120-w6-public-ledger`
- **State:** ready; not started
<!-- progress:end -->
