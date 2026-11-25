# The public ledger of the household arm

Brief 120c (W6). Not switched on: the default arm stays legacy and nothing here moves a legacy number.

## What it is
A ledger of the state's holdings by class, per path and year, replacing the state's single stake and the fund's bare cash recursion. Its classes are property, net financial, physical and a safe asset; the pension is not a class. It exists so that what the households pay and what the state receives tie by class, path and year.

## Units
Billions of pounds, real, on the pack's CPI basis (millions of pounds per adult times the thousands of adults of the base). Balances are market value, closing the year. A refund is a negative receipt.

## The recursion
For each class k, path and year t:

    L_k(t) = L_k(t-1) (1 + g_k) + receipts_k(t) - payout_k(t)        L_k(0) = 0

- **Receipts.** Every WDT payment a household makes (the year's tax, refunds, the assessment a death triggers, the heir's, a deferred balance settled, Route D settled) enters in the paying line's non-pension class mix at the time of payment, true value. The corporate levy enters as cash: `safe_share` (I-D14f) of it in the safe asset, the rest as net financial.
- **Returns.** The class return is the household's holding gain `g_k` (scenario ranges I-D1h to I-D1j). The safe asset's return is an input of `revenue.revenue` (`safe`); the identity table sets it to the net financial return, a stand-in, because no safe return is wired yet.
- **Payout.** `fund()` keeps its reserve rules (target, fill, failure events); the payout it decides comes out of the classes pro rata to their balances. `fund()` reads balance and return from the ledger: `rr = sum_k L_k g_k / L`.
- **State stake.** `Book.state_true` returns the ledger value under the household arm; under the legacy arm it is the old cash recursion, unchanged.

## Identities (tested to 1e-9)
1. Households' payments, weighted over the lines and phases, equal the ledger's WDT receipts, per path and year (`test_ledger.py`).
2. `dL_k = receipts_k + return_k - payout_k` for each class, per path and year; the classes sum to the fund balance `S` and the payouts to `R`.
3. Death and horizon payments are made in the year they occur (`HouseholdHook.reconcile` runs after each death step and after the terminal settlement, inside `revenue.run_lines`); the payment-shortfall record `unpaid_B` is zero in the production path.

`ledger_table.py` (this folder's `household-arm-account/`) writes `ledger_table.csv`: for years 1, 10, 30 and 100, receipts, return, payout and closing balance by class, and the two residuals (`res_pay`, households' payments minus ledger WDT receipts; `res_dL`, the largest class residual of identity 2). At the centre grid point of the stored digest (tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5), the B.6g income scale, six death phases, deaths every 30 years, the horizon settled in year 100, and the three saving values of the 118c/119c account (min, median, max of the ONS non-pension saving ratio, none called central), both residuals are below 2e-12 and `unpaid_B` is 0 in every year. At the centre `safe_share` is 0, so the safe class holds nothing and the levy sits in net financial.

## What it does not do
- **No price response to a sale.** A household that pays by selling an asset moves no price: the counterparty is outside the modelled sectors.
- **The pension is not a ledger class.** It stays in the assessed base and outside every payment source and every ledger class.
- **The levy is cash.** It enters under `safe_share` and the rest as net financial.
- **No result.** No revenue, fund-fill or burden figure is produced or reviewed in this note or the table; they wait for the arm switch and the withheld outputs (W7).
- **No safe-asset return, saving gradient, pension withdrawal or comparators** (out of scope for W6).
