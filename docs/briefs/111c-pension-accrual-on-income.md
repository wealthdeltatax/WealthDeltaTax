# 111: Base the pension accrual on income and rerun the untaxed baseline

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 110c (merged)
- **Read (first block: the first two only):** (1) `docs/model-v3/cell-baseline.md` ("What came out", "Inputs, as used", "Limits"); (2) `docs/research/data/101r/` derivations of D.8 (`derived_ons_flows.csv` columns `D8_over_B6g` and `D8_over_open_NW`, or their names there) and register row F-10 in `docs/research/data/103r/parameter_register.csv`. Later, by block: row I-D1k in `docs/model-v3/inputs.md`; `model_v3/core/cells.py`, `tests/model_v3/test_cells.py`; `docs/model-v3/cell-baseline/cell_baseline.py`; `pipeline/build_inputs.py`; `docs/agents/code.md`.

## Goal
Make the pension accrual follow income, not wealth, and rerun the untaxed baseline, so the path is no longer set by an accrual label that grows with wealth (110c: mid-point 1.12% of opening net worth was 2.7 times today's ONS D.8, and 1.12 of the 1.22 points of saving).

## Decisions (author, 2026-11-22)
- Accrual is a share of income: D.8 over B.6g, applied to cell income. Held series 1998 to 2025: min 3.0%, median 7.3%, max 9.7%; 2024 4.8%.
- **No mid-point label for this row.** The central is the observed value in the income base year (2024, 4.8% of B.6g; recompute from the 101r derivation and state the exact figure), shown as an observed latest year, with the 1998 to 2025 min and max as the range. This ties the accrual to today's flow instead of an average of a falling series.
- The earlier ruling on the income gap applies again, because the accrual is now an income share: scale every cell's income by one factor to the B.6g total (2024, matching the I-D9 income level; state the year and any price adjustment), keeping band proportions and the retired split; label the run aggregate-constrained; keep the unscaled run as a sensitivity. 110c did not apply it (it reconciled to 2021 and reported an 11% gap).
- Everything else in 110c stands (ETB retired fraction 0.4386, regimes, saving ratio, convention A, no tax).

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** progress block and the skeleton of a new section "Rerun with the accrual on income" in `docs/model-v3/cell-baseline.md` (pending). Read only the first two Read items.
- **Block 1: the row.** Redefine I-D1k in `inputs.md` to the income basis (unit % of B.6g; low and high the 1998 to 2025 min and max; central the 2024 value, labelled observed latest year, not a mid-point; the median as reference text); regenerate `registry/inputs.json`; adjust the row-count and any pins; keep the old basis in a dated note. Anything that quotes I-D1k (grep) is listed and updated. Tests; push.
- **Block 2: the module.** `cells.py` takes the accrual as a share of cell income (income scaled as ruled); account lines unchanged (accrual still counts as saving into the pension class); tests, including that the realised accrual in year 1 equals the share times B.6g within rounding. Push.
- **Block 3: the rerun.** The 15 runs of 110c under the new basis (accrual at low, observed, high in place of the two sensitivities), the unscaled sensitivity, B and legacy; CSVs; summary lines only on screen. Push.
- **Block 4: findings.** Update the note: what changed against 110c, what now sets the path, the limits; set State; change report; push; stop.
**Stop rule.** After three blocks, or when a quarter of the budget is left, write from what exists, push, list the rest under Next and stop.

## Touches
`docs/model-v3/inputs.md` (I-D1k only, counts), `registry/inputs.json` (generated), `registry/inputs-display.yml` if the display entry needs the new unit, `tests/data/test_build_inputs.py` only if a count moves, `model_v3/core/cells.py`, `tests/model_v3/test_cells.py`, `docs/model-v3/cell-baseline.md`, `docs/model-v3/cell-baseline/`. Name any further file before editing it. Nothing in the kernel, runner, revenue, pack or the other register rows.

## Acceptance criteria
- I-D1k on the income basis with exact figures; registry regenerated; suites pass (pre-existing data and hooks failures reported as on main); existing digests unchanged.
- Identity residual below 1e-9 in every year of every run; legacy arm still equals `grow_and_consume`.
- Year-1 aggregate accrual equals the stated share of B.6g (2024) within rounding.
- The note reports every run and what now drives the path; no input tuned; any odd result (negative wealth) reported with inputs.
- Diff limited to Touches.

## Checks to run
`python -I pipeline/build_inputs.py`; v3, data and hooks suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
Pension withdrawal or drawdown, transitions, a saving gradient, WDT, wiring, validation, any other register row.

## Open questions
Whether D.8 over B.6g (which counts employer contributions and benefit accrual) is the right base for a household pension that is never drawn here (agent states the limit; the author rules later).

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 (skeleton); block 1: I-D1k on the income basis (D8_share_of_B6g: 3.01 / 4.83 / 9.74, central the observed 2024 value 0.048267, median 7.30 reference), registry regenerated, display unit updated; count 297 and judgement 112 unchanged; data 5 and hooks 1 failures as on main.
- **Next:** block 2, the module (cells.py accrual on income, income scaled to B.6g 2024).
- **Decisions:** the row quotes: STATUS.md and docs/decisions.md still describe the old basis (guru-owned, not edited); cell-baseline.md 110c text and cell_baseline.py still use it until blocks 3 and 4.
- **Gotchas:** none.
- **Resume:** branch `brief/111-accrual-income`; `git fetch origin brief/111-accrual-income && git checkout brief/111-accrual-income`; last block pushed 1; first action: block 2.
- **Not run:**
- **State:** in progress; block 1 pushed
<!-- progress:end -->
