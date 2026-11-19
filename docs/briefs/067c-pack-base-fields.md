# 067: Extend the UK pack with what the wealth and payer base needs

- **Status:** ready once the author has uploaded the ONS housing affordability file (see Depends)
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** 048c (merged), 066c (manifest rulings; they touch `build_gbr.py` and `manifest.json`, so run 067c after 066c merges); **the author uploads the ONS bulletin or dataset "Housing affordability in England and Wales: 2025" (median house price, England, £300,000, year ending Sept 2025) to `Research/`**; the guru then sets this brief to ready.
- **Read:** `docs/model-v3/country-pack.md` section 3.2 including the 2026-11-19 addition; `docs/briefs/051c-v3-6-wealth-and-payer-base.md` (the blocker note on branch `brief/051-base`, `git show origin/brief/051-base:docs/briefs/051c-v3-6-wealth-and-payer-base.md`) for the field list; `model_v3/pack/build_gbr.py`; `model_v3/core/pack.py` (enum at line 38, checks `_x_wealth`); `model_v2/RATES/rates_core.py` lines 408 to 599 as specification only; `Rates Data/totalwealthtables.xlsx` (WAS Tables 2.2, 2.5, 2.9), `Rates Data/financialwealthtables.xlsx`, the OBR and ONS sheets in `Rates Data/`, `docs/model-v3/inputs.md` rows I-D4a to I-D4f, I-D9*.

## Goal
`pack/GBR/wealth_distribution.csv` carries every number from outside the register that `core/base.py` needs, so the base can be built from the pack and register alone: wealth in pounds and adult and household counts by band, the median house price, and GDP.

## Decisions (author and guru, 2026-11-19)
- The author chose to extend the pack before building the base. The median house price comes from the uploaded ONS file (not from the register's number alone).
- New variables in `wealth_distribution.csv` (country-pack.md 3.2): `wealth_total` (`gbp_bn`), `households` and `adults` (`thousand`) by band D1 to D10 and `all`; `median_house_price` (`gbp`, band `all`, basis adult); `gdp` (`gbp_bn`, band `all`). Units `thousand` and `gbp` join the loader enum; no other format change.
- Every value is read from a held sheet or file with its table and cell named in `NOTICE.md` or the builder's comments; no number from memory. If a value cannot be read from a held file, stop and report which one; do not fill it.
- The route mix is not a pack item (it is register rows, brief 068g).

## Design
1. Extend `build_gbr.py` (it may grow to about 200 lines; say so) to read the new variables, rebuild the pack once, and run it a second time to confirm byte-identical output.
2. Add the two enum values to `core/pack.py` and any check the new rows need: `wealth_total` over D1 to D10 sums to `all` within rounding; `households` and `adults` likewise; `median_house_price` > 0; `gdp` > 0.
3. Add tests to `tests/model_v3/test_pack.py` (P10: the new variables exist, partition, and match the sheets' totals; update the pinned `pack_sha256`). The loader's other tests must pass unchanged.
4. Pack basis: the wealth year is the survey period the existing rows use (2020-22); GDP is for that period or the manifest `base_year`, whichever the pack's other rows use; state it.
5. Write in the progress block the final field list `base.py` can rely on (variable, bands, unit, basis, year), so 051c can start from it.

## Touches
`model_v3/pack/build_gbr.py`, `model_v3/pack/GBR/` (`wealth_distribution.csv`, `manifest.json`, `NOTICE.md`; no other CSV changes), `model_v3/core/pack.py` (enum and checks only), `tests/model_v3/test_pack.py`, this brief's progress block. Nothing in the other `core/` files, `levers.json`, `registry/`.

## Acceptance criteria
- The new variables are in the pack; every value traces to a held file and table; `pytest tests/model_v3 -q` passes; a second builder run is byte-identical; the pinned `pack_sha256` is updated.
- The ZZZ fixture pack still loads (the enum only grows).
- `git diff --stat` is limited to Touches; other CSVs unchanged.

## Checks to run
`pytest tests/model_v3 -q`, `pytest tests/data -q`, `pytest tests/gate -q` (separate commands).

## Out of scope
The base itself (051c), the route mix, register rows, the kernel.

## Open questions
Ask rather than guess: if the survey tables give households but not adults by decile, say what the held sheets give; do not derive adults from an assumed household size.

## Implementation notes
<!-- progress:start -->
- **Done:** `wealth_distribution.csv` has 24 new rows (15 to 39). Loader enum gains `thousand` and `gbp`; `_x_wealth` checks D1 to D10 against the printed `all` for `gbp_bn` and `thousand` groups (tolerance max(0.5, 1e-4 of all)) and requires `median_house_price` and `gdp` > 0. P10 in `tests/model_v3/test_pack_base.py`; `pack_sha256` pinned: 09d76ce7...2540. `build_gbr.py` is 188 lines (limit about 200). Second run byte-identical; levers.json and the other six CSVs unchanged.
- **Field list `base.py` can rely on** (all in `wealth_distribution.csv`):
  - `wealth_total`: bands D1 to D10 and `all`; `gbp_bn`; basis `household`; year `2020-22`. D values from WAS Table 2.2 block 1 (GBP million over 1000, 3 decimals), sum 13,567.89; `all` = Table 2.1 row 8 = 13,568.
  - `households`: bands D1 to D10 and `all`; `thousand`; basis `household`; year `2020-22`. `all` = 26,991 (Table 2.1 row 29); each decile 2,699.1 (total over ten, a decile holds a tenth of households by definition; no held table prints a count per decile).
  - `adults`: **not in the pack.** No held table gives adults by decile (Table 2.10 gives persons by seven wealth bands, whole-number percentages). 051c takes adults per household from a register row.
  - `median_house_price`: band `all`; `gbp`; basis `adult`; year `YE Sep 2025`; 300,000 (ONS bulletin, England, all dwellings; the existing-dwelling median in the HPSSA workbook is 297,000).
  - `gdp`: band `all`; `gbp_bn`; basis `household`; year `2020-22`; 2,211.48 = mean of FY 2020-21 (2,085.204) and FY 2021-22 (2,337.757), `Revenue composition spreadsheet.xlsx` sheet Total revenues column G, nominal as published (author, 2026-11-19: mean of the two years). The register's I-D4a uses 2,284 (calendar 2021, OECD via FRED, not held): the ratio is 13,568 / 2,211.48 = 6.14 against the register's 5.94.
- **Next:** 051c.
- **Decisions:** author 2026-11-19: adults out of the pack, GDP the mean of the two financial years, households per decile the total over ten. Median house price from the bulletin (all dwellings), not from the HPSSA workbook. `gdp` basis is `household` (the enum has only household and adult). The pack's price year in country-pack.md 3.2 says GDP is "the pack's price year"; the pack's other wealth rows are nominal 2020-22 as published, so GDP is on the survey period, as the brief's design item 4 allows.
- **Gotchas:** (1) `wealth_distribution.csv` is now `cite-only` in the manifest (most restrictive source: the GDP series is the IFS spreadsheet); it was `ogl-v3`. (2) `core/pack.py` is 340 lines, exactly at its budget; `test_pack.py` is exactly 240, so the P10 tests live in a new file `tests/model_v3/test_pack_base.py` (not in the brief's Touches). (3) The builder now needs `pdftotext` (it checks the bulletin sentence). (4) The register's I-D4a and I-D4b numbers are on £2,284bn and £300,000: I-D4a differs from the pack GDP (guru to decide whether the register or the pack moves).
- **Resume:** `python3 -B -I model_v3/pack/build_gbr.py`, `pytest tests/model_v3 -q`.
- **Not run:** none.
- **State:** done

```
Change report
- Task: 067c, UK pack base fields
- Files changed: model_v3/pack/build_gbr.py; model_v3/pack/GBR/{wealth_distribution.csv, manifest.json, NOTICE.md}; model_v3/core/pack.py; tests/model_v3/test_pack.py (the pin); tests/model_v3/test_pack_base.py (new); this brief
- What is different now: the pack carries wealth_total, households, median_house_price and gdp for the base
- New or changed interfaces: loader units `thousand` and `gbp`; partition and positivity checks in _x_wealth
- Acceptance criteria: new variables in the pack, each traced to a held file and cell (met, NOTICE); pytest tests/model_v3 118 passed; second builder run byte-identical (met); pin updated (met); ZZZ fixture loads (met); diff limited to Touches (one extra file, see Deviations), other CSVs unchanged (met)
- Deviations from the brief: adults not supplied (no held table, author's ruling); new test file; manifest licence for wealth_distribution is now cite-only
- Risks / follow-ups: register I-D4a (GDP 2,284 against 2,211.48); the cite-only licence of the file
- Verification: pytest model_v3 118, data 84, gate 17, hooks 67, cards 8 (separate runs); builder twice and diffed
- Overview sections likely needing an update: none
- Commit / branch: brief/067-pack-base-fields
```
<!-- progress:end -->
