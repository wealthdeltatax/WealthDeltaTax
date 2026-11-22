# 119: Tail lines: pension held as an absolute cap, then rerun the account table

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 118c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-account.md` (the shortfall section only); (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`line_state`, `TAKES_D10`); `docs/research/data/102r/band_composition_by_pack_band.csv` (D10 rows, last round); `docs/model-v3/inputs.md` rows I-D1h to I-D1k (for format); `docs/model-v3/household-arm-account/account_table.py`.

## Goal
Stop the tail lines holding an impossible pension. 118c gave D10a, D10b, RL3, RL2 and RL1 the D10 class **shares**, so RL1 (about £40bn per adult) holds 37% of its wealth (about £15bn) as pension. Pension is never sold, so by year 69 the other classes are exhausted and the richest three lines cannot pay (`unpaid_B`). Cap the pension at an absolute amount, move the rest into the other classes, and rerun the account table.

## Decisions (author, 2026-11-22)
- The tail lines' pension balance is an **absolute amount per adult, real, equal to the D10 mean pension per adult** (observed: WAS Round 8, April 2020 to March 2022, D10 pension share of D10 wealth times D10 mean wealth, divided to a per-adult basis the way the pack does for wealth). It is a cap: a tail line whose proportional pension is below the cap keeps the proportional amount.
- Wealth the cap displaces goes to property, net financial and physical pro rata to D10's mix among those three classes.
- This is a **labelled scenario, not a measurement**. The author wants future readers to inspect and challenge it with better data. The label says what it is (the D10 mean, a ceiling on tail pensions), why (no held distribution of pension wealth; no UKDS licence), and what would replace it (the p90 or p99 of private pension wealth, or a lifetime-allowance-based figure, from an ONS pension-wealth-by-percentile table). The replacement is a one-value change.
- No other change to settlement. Pension stays never sold, illiquid, inside the base. The shortfall alarm stays: if it still fires after the cap, report it and stop; do not change the settlement rule.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block pushed.
- **Block 1: the cap.** In `line_state` (or a helper in `core/household.py` if arm.py cannot take it), set the tail lines' pension to min(proportional pension, cap), with the cap derived from the committed D10 row, and redistribute the displacement as above. Tests: the pension of RL1 to RL3 equals the cap; each line's total wealth is unchanged; classes sum to the line's wealth; lines below D10 and the legacy arm are bit-for-bit unchanged; `test_legacy_digest` passes unchanged. Push.
- **Block 2: the register row and the labels.** One new row **I-D1l** in `docs/model-v3/inputs.md` and the register (class `scenario`, source and basis above, the challenge note, no central value beyond the one D10-mean value the register format demands, marked as a mid-point label). Update the gate hash the way 105c to 107c did and report that you did. Add the label to `decisions.md` and one line to STATUS. Push.
- **Block 3: rerun the table.** Rerun `account_table.py` unchanged in method. Write the new note section in `household-arm-account.md` (replace the shortfall section): the shortfall count, the pension share by tail line at year 1, 30 and 100, and the rows for RL1 to RL3 that were blank at year 100. If the alarm still fires, give the year, the line and the class balances, and stop. **No revenue, fund or burden number.** Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print only summary lines; suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 140; raise to 160 if the cap needs it and say so, or put the helper in `core/household.py`), `tests/model_v3/test_household_hook.py` or `test_household_tax.py` (additions), `docs/model-v3/inputs.md`, the register file and its gate hash (`registry/inputs.json`), `docs/decisions.md`, `STATUS.md`, `docs/model-v3/household-arm-account.md`, `docs/model-v3/household-arm-account/` (rerun CSV), `docs/model-v3/architecture.md` (budget rows only). Name any further file before editing it. Not the kernel, `revenue.py`, the pack, `runner.py`, the `out_*` files, the legacy digest fixture.

## Acceptance criteria
- `test_legacy_digest` passes unchanged after every block; all suites pass (pre-existing data, cards and hooks failures reported as on main).
- Tail lines hold pension equal to min(proportional, cap); wealth per line unchanged; I1 and the account identity hold to 1e-9 with tax on.
- I-D1l is in `inputs.md` and the register with the label and challenge note; the gate hash is updated and reported.
- Rerun table: `shortfall_lines` empty, or the exact remaining case reported without changing the settlement rule; year-100 rows present for all 14 lines if empty.
- Diff within Touches; no upward import.

## Checks to run
`test_legacy_digest` after each block; v3 suites in the background (never piped); the account script with summary lines only on screen; `python -I pipeline/check_agent_docs.py`.

## Out of scope
Any change to the pension settlement rule, a p90 or p99 figure (not held; named as the replacement only), per-line pension heterogeneity within D10, the arm switch, comparators, any revenue or fund result.

## Open questions
Whether D10a and D10b (near the D10 mean) are affected at all by the cap: the agent reports the pension share before and after for all five tail lines.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout brief/119-tail-pension-cap`
- **State:** ready; not started
<!-- progress:end -->
