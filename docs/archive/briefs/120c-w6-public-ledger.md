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
- **Done:** blocks 0 to 3. Block 1: `revenue.run_lines` calls `hook.reconcile` after each death step and, under the household arm, settles the terminal D and B and reconciles in the last year. Block 2: `hook.receipts()` and `class_returns()` (carried in `run['ledger']`, read by `revenue()`; no runner change), `fund(led=)`, `Book.ledger`, `state_true`, the refund cap's stake; `tests/model_v3/test_ledger.py` (11 tests). Block 3: `docs/model-v3/household-arm-account/ledger_table.py` and `ledger_table.csv` (3 saving values x years 1, 10, 30, 100; 12 rows), `docs/model-v3/public-ledger.md`. Suites 10 of 10 passed (305 in model_v3, `test_legacy_digest` unchanged); `check_agent_docs` exit 0.
- **Next:** review, then squash-merge (the author's). W7 (the arm switch and withheld outputs) reads the ledger; a safe-asset return is still to be wired.
- **Decisions:** the identity table runs the production path (`run_lines` with six phases, then `revenue.revenue`) at the account script's centre grid point and income scale (it imports `account_table.setup`, `SPEC`, `SHOW`); the safe asset earns the net financial class return in the table (no safe return is wired; at the centre `safe_share` is 0 so it holds nothing); `res_pay` compares the households' weighted payments with the WDT receipts (the levy excluded).
- **Gotchas:** a death never falls in the last simulation year by design (`run_lines` deaths need `t < T`; year T is the terminal settlement), so "a death in the last year" is the terminal settlement plus a death in the last-but-one year (`test_a_death_in_the_last_but_one_year...`, `test_deaths_and_the_horizon_are_paid_in_the_year_in_the_production_path`, `CASES` in `test_ledger.py`).
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout brief/120-w6-public-ledger`
- **State:** done; not merged (squash-merge is the author's after review)

Change report
- Task: brief 120c (W6), the public ledger by class, death and terminal payments reconciled in the year; block 3 (identity table, note, report)
- Files changed (whole brief): `model_v3/core/revenue.py`, `kernel.py` (`state_true`, the refund cap stake, the ledger), `model_v3/runner/arm.py` (`reconcile`, `receipts`, `class_returns`), `tests/model_v3/test_ledger.py` (new), `test_household_tax.py`, `docs/model-v3/household-arm-account/ledger_table.py` and `.csv` (new), `docs/model-v3/public-ledger.md` (new), `docs/model-v3/architecture.md` (budget rows), this brief
- What is different now: under the household arm the state's holdings are a ledger by class (property, net financial, physical, safe) and household payments tie to its receipts per path and year; deaths and the horizon are paid in their year. The default arm is legacy and unchanged.
- New or changed interfaces: `hook.receipts()`, `hook.class_returns()`, `hook.reconcile(book)` called inside `run_lines`; `run['ledger']` (`rc` by class); `fund(..., led=)`; `Book.ledger`; `revenue()` reads `run['ledger']` and the safe returns `safe`.
- Acceptance criteria: `test_legacy_digest` passes unchanged and all suites pass: met (10 of 10 suites; data, cards and hooks now pass as well). Payments equal ledger receipts and `dL = receipts + return - payout` to 1e-9, six phases and refunds covered: met (`test_ledger.py`; in the table both residuals are at most 1.4e-12). Death and terminal payments paid in their year: met (`test_household_tax.py`, nothing left for the next year's `pre`). `unpaid_B` zero in the production path: met (asserted on the production books in `test_ledger.py` and `test_household_tax.py`; 0 in the table's three runs, 0 shortfall lines). Pension in the base, never a class: met (`'pension' not in` the ledger). R4 and budgets: met (`test_rules`, `test_budget` pass). Diff within Touches: met.
- Deviations from the brief: a death in the last simulation year does not exist (deaths need `t < T`; year T is the terminal settlement), so that case is the terminal settlement and a death in the last-but-one year; `arm.py` is 171 lines against the 180 of its budget row in `architecture.md` (the 160 in the progress block was the brief's figure; the row was raised, as the brief allowed by "name any raise"); `runner.py` untouched.
- Risks / follow-ups: the table's safe-asset return is a stand-in (net financial return) and `safe_share` is 0 at the centre, so the safe class is empty there; production `core_run` passes no `safe` series, so W7 must supply one before the arm is switched on.
- Instruction friction: none
- Verification: `python pipeline/run_suites.py` (10 of 10 passed, run in the background to a file); `python -I docs/model-v3/household-arm-account/ledger_table.py` (summary lines: max |res_pay| 1.8e-12, max |res_dL| 1.4e-12, unpaid_B 0, shortfall lines 0); `python -I pipeline/check_agent_docs.py` exit 0.
- Overview sections likely needing an update: none
- Commit / branch: `brief/120-w6-public-ledger`; not merged
<!-- progress:end -->
