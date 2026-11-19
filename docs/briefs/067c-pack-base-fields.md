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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** waiting for the author's upload
<!-- progress:end -->
