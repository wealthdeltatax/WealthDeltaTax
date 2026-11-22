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
- **Done:** blocks 0 to 3 (below). `model_v3` 272 passed incl. `test_legacy_digest` unchanged; `data`, `cards`, `hooks` fail exactly as on main (5, 1, 1 tests; same names, checked on a clean `origin/main`); `check_agent_docs` clean.
- **Next:** W5 (the household hook) calls `apply_payment` per line and sets `book.pen`.
- **Decisions:** (1) the fallback allocates by the route's declared value, not by units: a unit of C is declared at `alpha_C x V`, of A at `V`, so units of different routes are not comparable, and the tax is a share of assessed value. It fires only where the line has a non-zero pension, `tot = 0` and `delta != 0`, so `pen = penp = 0` is bit equal; it covers a pension fall with routes not down (a refund) as well as a rise. `sum_r L_r = L` holds to 1e-12 relative. (2) `apply_payment(q, T, source_weights=None, lien=0.0)`: the `lien` argument is mine, the brief's text asks the function to add the lien to debt and the signature named none; default 0.0 changes nothing. (3) `household_step` still raises on a payment above non-pension wealth (its existing tests require it), now from `apply_payment`'s `unpaid`; the pure function itself caps and reports.
- **Gotchas:** (1) **The design note was wrong on one point: the sale routes did not cap at holdings.** `_div` only guards a zero divisor; in `_route_tax` the A, B (and income-mode short) and C/Cv payments moved `Lp / V` units whatever the line held, so `f` could go negative (only the death and horizon settlement `settle_B` capped, and set `unpaid_B`). Without a pension this cannot bind (`L <= delta <= declared value held`), so no legacy run moves; with a pension delta it can. Block 3 added `_cap` (excess beyond 1e-9 goes to `unpaid_B`, the payment is capped at `f x V` or, for C, `f x dd`) and `shortfall_lines(book)`. Route D accrues a liability, not a sale, so it is not capped. (2) A line with pension and no route value gets nothing from the fallback (`tot` stays 0): its tax is not taken, and it is not counted in `unpaid_B` either (no route asked for it); W5 must give such a line units or treat it. (3) `check()` has no minimum-family-units entry; a negative `f` would not have shown there.
- **Resume:** none.
- **Not run:** nothing named by the brief.
- **State:** done; merged to main; ready to retire.

### Change report
```
Change report
- Task: 116c (W4): pension in the book, and the payment half of the household step
- Files changed: model_v3/core/kernel.py (Book.pen, penp; assess; rebase; _cap and shortfall_lines; 574 to 594 lines of 660); model_v3/core/household.py (apply_payment; 77 to 89 of 120); tests/model_v3/test_pension_book.py (new, 9 tests, 78 lines); tests/model_v3/test_household.py (two tests added); this brief
- What is different now: a line can carry a pension balance that is assessed and never sold; the tax on a pension rise or the refund on a fall is settled over the routes by declared value when no route moved; a sale route never pays more than the line holds and the excess is counted in unpaid_B; the payment half of the household step is a pure function
- New or changed interfaces: Book.pen, Book.penp; kernel.shortfall_lines(book); household.apply_payment(q, T, source_weights=None, lien=0.0) -> (q1, share, unpaid)
- Acceptance criteria: test_legacy_digest passes unchanged after each block (bit equal at pen = 0; run after blocks 1 and 3, and in the full v3 run); all suites pass but data (5), cards (1), hooks (1), identical on clean main; sum_r L_r = L to 1e-12 relative with route deltas non-positive (test), a pension fall is refunded as a loss at the rate (test); apply_payment pure, pension never reduced, household_step bit equal to the old code on 356 random cases across modes, T and weights, and raising the same error in the 4 cases that raised (scratch comparison against origin/main's file, not committed); a payment above holdings capped and reported, never raised (A, B, C tests); no standard run triggers it today: 90 books over 5 schedules, full and not, 60 paths each, max unpaid_B 0.0, 0 lines with a shortfall; kernel 594 of 660, household 89 of 120, no upward import (R4 passes); diff inside Touches
- Deviations from the brief: (1) block 3 changed `_route_tax` (cap in the A, B, income-short and C branches), not only a report: the brief assumed the book already capped; it did not (gotcha 1); a bit-stable cap, 0 effect without a pension. (2) `apply_payment` has a `lien` argument. (3) the architecture.md budget rows are unchanged (no row needs to move: kernel 594 under 660, household 89 under 120); `test_pension_book.py` has no row of its own (the budget check maps only `test_<module>.py`)
- Risks / follow-ups: the design note kernel-wiring-design 3.4 says the sale routes cap at holdings; it should say they now do, and that `check()` does not report negative family units. A pension-only line (no route value) pays nothing and is not flagged: W5 to handle. Open question answered: route value, not units (decision 1)
- Instruction friction: none
- Verification: pytest tests/model_v3 272 passed (includes test_legacy_digest, test_budget, rules); run_suites all: data, cards, hooks fail as on main; check_agent_docs clean; scratch comparison and the unpaid_B measurement not committed
- Overview sections likely needing an update: model v3 build status (W4 built)
- Commit / branch: brief/116-work, merged to main by fast-forward; brief 116c merged, ready to retire
```
<!-- progress:end -->
