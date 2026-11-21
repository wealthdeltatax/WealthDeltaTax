# 108: The household step function (pure function, not wired in)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 104r (merged), 106c (merged)
- **Read:** `docs/research/104r-parameter-map-design.md` sections 3 and 5.1 (conventions, worked cases, the proposed signature); `docs/research/data/104r/conventions_worked.py` and its CSVs (the worked household whose dNW is 54 on both sides; reproduce it as a test); `docs/model-v3/household-flow-plan.md`; `docs/model-v3/architecture.md` 5.1 (layers) and the budgets block; `docs/agents/code.md` ("Adding or filling a model module", "Layer check"); `model_v3/core/kernel.py` `grow_and_consume` (line ~324) and `model_v3/runner/runner.py` where I-D14c is read.

## Goal
One new pure function, `household_step`, that advances one cell's positions by one year under convention A, with a `legacy` mode that reproduces the existing `W[t+1] = W[t](1+g)(1-c)` rule exactly. It is not called by the kernel, runner or revenue code in this brief; no existing digest may move.

## Decisions (author, 2026-11-21)
- Convention A: credit the holding gain; saving carries the retained yield once (`dNW/NW = s + g_h` in aggregate form). Convention B (credit total return, consume the yield) is a second mode used only as an equivalence check. Counting the yield twice is wrong and must be a failing test.
- Pension is in the base on the WAS SCAPE stock basis and is illiquid until drawn; its accrual is one labelled aggregate scenario input, with no rate on the stock.
- Physical wealth is a separate class inside the base; pension, physical and net financial returns are labelled scenario inputs, never defaults.
- Two deflators: CPI for returns and numeraire, the expenditure deflator for liability erosion; the wedge is its own line in the account.
- `O` is reported, not forced to zero. `TR` is an argument fixed at 0. The legacy 3.5% is the `legacy` mode only.
- Settlement (author, replaces the earlier net-financial-only ruling): the existing kernel routes; the payment is taken pro rata across the non-pension classes; pension is never sold; Route D keeps its lien. The function takes `T_WDT` as an input (default 0) and an optional `source_weights` over classes (default: price-weighted pro rata over property, net financial and physical, pension weight 0); it reports the liquidity diagnostic (payment over net financial wealth, payment over non-pension wealth, and a flag where payment exceeds net financial wealth).

## Design
1. `model_v3/core/household.py` with `household_step(cell, pos, flows, rets, defl, convention) -> (pos1, acct)` as in 104r 5.1 (names may adjust; report each change). Classes: property, net financial, physical, pension, debt. Inputs are plain numbers or arrays; no pack or register reads inside the function.
2. `acct` has `dNW`, `S`, `CG` (with the erosion wedge as its own entry), `TR`, `O`, `T_WDT`, and the identity `dNW = S + CG + TR + O - T_WDT` holds to 1e-9; `O` is an input residual, not solved.
3. `legacy` mode: given wealth and I-D14c it returns exactly the kernel's `W*(1+g)*(1-c)`; test it against `kernel.grow_and_consume` on the same inputs (bit-equal).
4. No-double-counting tests: the 104r worked household gives 54 in A and in B; a deliberately wrong convention (yield counted in saving and in the return) gives 90 and must be caught by a test that asserts the identity against an independent calculation.
5. Illiquid pension and settlement: the pension is not available to `T_WDT` or consumption until a `withdrawal` flow; a test shows this. With `T_WDT` > 0 the payment falls pro rata on the non-pension classes (test: shares match the class weights; the identity still holds with `T_WDT` as one negative line), and the liquidity diagnostic fields are returned in `acct`.
6. Registration: a LAYER row for `household` in `tests/model_v3/conftest.py`; a budget row in `architecture.md`; new tests in `tests/model_v3/test_household.py` and the `test_groups.py` rows the 104r note lists. Choose the layer from architecture.md 5.1 so that `household` imports nothing above it; report the choice.

## Touches
`model_v3/core/household.py` (new), `tests/model_v3/test_household.py` (new), `tests/model_v3/conftest.py` (LAYER row), `tests/model_v3/test_groups.py` (only if needed), `docs/model-v3/architecture.md` (budget row and a short section). Nothing else; in particular not `kernel.py`, `runner.py`, `revenue.py`, `burden.py`, the pack or the register.

## Acceptance criteria
- `household_step` exists with the modes `A`, `B`, `legacy`; identity holds per call to 1e-9.
- The 104r worked household reproduces (54 and 54); the double-count variant is caught.
- `legacy` is bit-equal to `grow_and_consume` on a grid of inputs; all existing v3 digests and suites unchanged.
- Registration done; budget respected.
- Diff limited to Touches.

## Checks to run
v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
Wiring into the kernel or runner, the public ledger, pack inputs, scenario values, the lien and route logic (they stay in the kernel), tax, any register or paper edit.

## Open questions
Layer placement; whether `cell` needs more than band and stage in the signature.

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
