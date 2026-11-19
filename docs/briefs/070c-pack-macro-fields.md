# 070: Add the macro series the revenue stage needs to the UK pack

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none (067c and 051c are merged)
- **Read:** the blocker note on branch `brief/052-revenue` (`git show origin/brief/052-revenue:docs/briefs/052c-v3-7-revenue-fund-identity.md`, progress block); `docs/model-v3/country-pack.md` sections 3.1 (returns) and 4 (public_expenditure); `model_v3/pack/build_gbr.py`; `model_v3/core/pack.py` (SCHEMA, `_x_returns`); `tests/model_v3/test_pack.py`; `Rates Data/JSTdatasetR6.xlsx`; `Rates Data/PSS_May_2024_TES_UPDATED.xlsx`; `model_v2/RATES/rates_core.py` lines 60 to 90, 158 to 210, 1109 to 1193 (specification only).

## Goal
The pack holds the two macro inputs 052c needs that no file in it carries: real GDP per head (to grow wealth and index W_min in real terms) and the reference expenditure over GDP (the denominator of relief coverage, P1, and the non-WDT requirement). Today `returns.csv` has returns and `cpi` only, and `public_expenditure.csv` is empty (header only).

## Decisions (author and guru, 2026-11-19)
- Real GDP per head enters `returns.csv` as one new column `gdp_pc` (real GDP per head, a level, the JST series in its published units), blank outside its span; the model derives growth from the level. `cpi` stays as it is. The country-pack.md 3.1 table gains the row; the loader's schema gains the column (nullable like the returns columns; no other loader change).
- The reference expenditure is one row in `public_expenditure.csv`: function `total`, `fiscal_year` the reference year (v2 used 2019, `exp_ref_year`), `pct_gdp` from a held file: JST government expenditure over GDP for the UK in 2019 if the JST file carries both, otherwise total managed expenditure over GDP from the held PSS sheet. Use JST first, because v2 did; say which in `NOTICE.md` and in the builder, and report the other source's value for the same year as a cross-check without storing it.
- Every value is read from a held sheet with its table and cell named; no number from memory. If a series is missing from the held files, stop and report; do not fill or interpolate.
- Not in this brief: consumption, verification hazards, fund settings (register rows, brief 071g); the levy base (the register's I-D7a, % of GDP, is used as it is).

## Design
1. Extend `build_gbr.py` (it may grow to about 230 lines; say so), rebuild once, rebuild again and confirm byte-identical output.
2. `core/pack.py`: schema gets `gdp_pc` in `returns` (float, nullable, > 0); `public_expenditure` row checks (`total` row present for the reference year, 0 < pct_gdp < 100).
3. `tests/model_v3/test_pack.py`: tests P11 (the new column has the JST span, positive, and its 2019 level equals the sheet's cell) and P12 (the `total` row exists and equals the sheet); update the pinned `pack_sha256`. All existing loader tests pass; the ZZZ fixture pack loads (the new column is nullable, the fixture may omit the `total` row only if the loader's check is conditional on the pack declaring a reference year; if not conditional, add the row to the fixture and say so).
4. Update `country-pack.md` sections 3.1 and 4 with the new column and row in the same commit.
5. Progress block ends with the field list 052c can rely on (file, column or row, unit, span).

## Touches
`model_v3/pack/build_gbr.py`, `model_v3/pack/GBR/` (`returns.csv`, `public_expenditure.csv`, `manifest.json`, `NOTICE.md`), `model_v3/core/pack.py` (schema and checks only), `tests/model_v3/test_pack.py`, the ZZZ fixture pack under `tests/model_v3/` if needed, `docs/model-v3/country-pack.md` (3.1 and 4 only), this brief's progress block.

## Acceptance criteria
- `gdp_pc` over the JST UK span in `returns.csv`; `public_expenditure.csv` holds the `total` row; both trace to named cells.
- `pytest tests/model_v3 -q` passes; second builder run byte-identical; `pack_sha256` updated.
- `git diff --stat` limited to Touches; other CSVs unchanged.

## Checks to run
`pytest tests/model_v3 -q`, `pytest tests/data -q`, `pytest tests/gate -q` (separate commands).

## Out of scope
`core/revenue.py`, the register, the base, `levers.json`.

## Open questions
Ask rather than guess: if JST carries expenditure but no GDP in pounds for 2019, say what it holds.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
