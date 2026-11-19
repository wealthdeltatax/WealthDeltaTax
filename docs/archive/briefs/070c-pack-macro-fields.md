# 070: Add the macro series the revenue stage needs to the UK pack

- **Status:** done
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
- **Done:** `returns.csv` gains `gdp_pc` (JST `rgdpmad`, 1870 to 2019, 150 rows, all positive); `public_expenditure.csv` holds one `total` row (2019, 36.82). Builder extended (201 lines, under 230) and run twice, byte-identical; `pack_sha256` now a9d8312678f423f7978de1857a67ece80f88ce0c39f514aef01832e6282c31be. Loader: `gdp_pc` in the schema (float, nullable, > 0); `public_expenditure.pct_gdp` strictly between 0 and 100; a non-empty file needs a `total` row. `core/pack.py` stays at 340 lines (the receipts check became a lambda in CROSS). ZZZ fixture: `gdp_pc` column added (2000 blank, then 1010 to 1090) and a `total` row (40.0, 2025-26); its pin is 339cb47401dc...ccefde9c. country-pack.md 3.1, 3.7 and the section 4 table updated. Tests P11 and P12 (6 tests) in the new `test_pack_macro.py`.
- **Field list 052c can rely on:**
  - `returns.csv`, column `gdp_pc`: real GDP per head, a level, JST `rgdpmad` as published (the repo's description: Maddison, 1990 USD; the held file has no unit label), years 1870 to 2019, no gaps, 2019 = 26341.025966. Growth is the model's to derive.
  - `public_expenditure.csv`, row `function=total`, `fiscal_year=2019` (calendar year), `pct_gdp=36.82` (percent), `gbp_bn` empty, `basis=outturn`. Source: JSTdatasetR6.xlsx Sheet1, GBR row 1510, `expenditure` 830.452 over `gdp` 2255.283.
  - Cross-check, not stored: PSS_May_2024_TES_UPDATED.xlsx, Data_for_charts, Total Managed Expenditure over Nominal GDP = 39.58 for 2019-20 (888.4 / 2244.5) and 39.48 for 2018-19 (858.2 / 2173.7). The 2.8-point gap is definition (JST general government expenditure against TME) and fiscal against calendar year.
- **Next:** 052c.
- **Decisions:** `gdp_pc` is `rgdpmad` (the JST per-head level in dollars) not `rgdpbarro` (an index) nor `gdp / pop` (nominal, what v2 derived). The `total` check is "a non-empty file needs a total row", because the manifest declares no reference year; so the fixture got a `total` row (the brief's second option). `gbp_bn` left empty: the JST description says millions but the GBR values are billions. The builder asserts every `rgdpmad` year and the 2019 expenditure equal the xlsx cells, so the json copy and the sheet cannot drift. `public_expenditure` is now `cite-only` (JST) and its `retrieved` is 2026-09-30.
- **Gotchas:** `pct_gdp` on `public_expenditure` is now exclusive of 0 and 100 (was inclusive). Fixture `returns.csv` has a 7th column, so P3's cell-count test now expects 6 cells. P11 and P12 are in `tests/model_v3/test_pack_macro.py`, a file outside Touches, because `test_pack.py` is at its 240-line budget (same as 067c's `test_pack_base.py`). The unit of `gdp_pc` is unconfirmed (see the description note).
- **Resume:** nothing.
- **Not run:** none of the named checks was skipped. Also run: tests/hooks and tests/cards (75 passed).
- **State:** done; merged to main. Results: tests/model_v3 134 passed, tests/data 84, tests/gate 17. `git diff --stat`: only Touches plus the new test file; the other five CSVs and levers.json are unchanged.
<!-- progress:end -->
