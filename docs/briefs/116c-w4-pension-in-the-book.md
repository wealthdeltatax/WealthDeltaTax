# 116 (W4): Pension in the book, and the payment half of the household step

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 115c, 114c, 113c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/kernel-wiring-design.md` sections 2.5, 3.3, 3.4 and the W4 row of section 4; (2) `docs/agents/code.md`. Later, by block: `model_v3/core/kernel.py` (`Book`, `assess` at line 275, `_route_tax`, `_move`, `_div`, `unpaid_B` at 159, `check()`); `model_v3/core/household.py` (lines 55 to 75: the payment code) and `tests/model_v3/test_household.py`.

## Goal
Add the pension as a balance beside the book's units, assessed but never sold, and split the payment half out of `household_step` as a pure function, so W5 can call it per line. With `pen = 0` (the default) every result is bit-equal to today; the stored legacy digest proves it.

## Decisions (author, 2026-11-22)
- Pension is in the assessed base (`W_new`, `W_prev`) and is never a unit that can be sold: option P1 of 112r (a class balance `pen` per line, with `penp` at the last assessment).
- The payment is taken pro rata from the non-pension classes (settlement by the existing routes). A payment above non-pension wealth is **capped at it and the excess is reported as `unpaid_B`**; the author's reading is that this cannot occur if the model is right (WDT is a tax at a marginal rate below 1 on the change in net worth), so a non-zero count in a standard run is a **model alarm**: report it, do not hide it.
- Negative net positions and their return rule are W5's, not here.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: pension in the book.** `Book.pen` and `Book.penp` (zeros by default, per line); `assess` adds `pen` to `W_new` and `penp` to `W_prev`; `rebase` sets `penp = pen`. Route weights `w[r]` use route deltas only; add the **fallback** the design names: when every route delta is non-positive while the total delta is positive (pension grew, units did not), allocate the tax by route value shares, so no tax is lost to `_div`. Tests: with `pen = penp = 0` the books equal the old code to 0.0 (and `test_legacy_digest` passes); with a positive pension delta and non-positive route deltas the allocated `sum_r L_r` equals `L` exactly and the route deltas stay non-positive; a case where pension falls is refunded as a loss at the rate (existing C1 rule). Push.
- **Block 2: `apply_payment`.** Extract the payment lines of `household_step` (`household.py` about 60 to 67) into a pure `apply_payment(q, T, source_weights)` that reduces the non-pension classes pro rata, adds the lien to debt and closes `dNW = S + CG + TR + O - T_WDT`; `household_step` calls it. Existing `test_household.py` tests pass unchanged; add tests for the pension never being reduced and for the shares. Push.
- **Block 3: the shortfall.** State what the book already does when a sale route needs more than the line holds (`_div` and the holdings cap) and make the excess visible: `unpaid_B` is set and a small helper returns its count per run; tests for a payment above non-pension wealth (capped, excess reported, not raised). Report whether any existing run has a non-zero `unpaid_B` today (expected zero). Registration, budget rows, change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and write Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/core/kernel.py` (about +20, budget 660: about 595 after), `model_v3/core/household.py` (about +25 of 120), `tests/model_v3/test_kernel.py` or a new `test_pension_book.py`, `tests/model_v3/test_household.py` (additions only), `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not the register, the pack, the runner, `revenue.py`, `burden.py`, `support.py` or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block (bit equal, `pen = 0`); all existing suites pass (pre-existing data, cards and hooks failures reported as on main).
- Assessment allocation with a pension delta: `sum_r L_r = L` exactly; no tax lost; losses refunded as before.
- `apply_payment` is pure and `household_step` results are unchanged to 0.0; pension never reduced by a payment.
- A payment above non-pension wealth is capped and reported, never raised; the report states whether any current run triggers it.
- `kernel.py` within 660, `household.py` within 120, no upward import (R4); diff limited to Touches.

## Checks to run
`test_legacy_digest` after each block (about 2 minutes); v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
The household hook, class returns, the debt return rule, income and saving flows, the ledger, the arm switch (W5 to W7), any register or pack change.

## Open questions
Whether the route-value fallback should weight by route value or by units (agent reports the choice and why).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and fetch line, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
