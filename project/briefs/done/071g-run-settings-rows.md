# 071: Add the run settings the revenue stage reads to the input register

- **Status:** done, merged 2026-11-19
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none (068g and 069r are merged)
- **Read:** `docs/model-v3/inputs.md` (conventions, as 068g followed them: ids, `(J)`, Coverage, Source); the blocker note on branch `brief/052-revenue` (progress block); `docs/model-v3/judgement-decisions.md`; `model_v2/WDT_Params.toml` lines 195 to 220 (`lambda_vals`, `lambda_base`, `c_share_vals`), 700 to 740 (the fund and `valgen` defaults), 1130 to 1230 (the sensitivity blocks for `c`, `a_window`, `safe_share`, `horizon`), 1620 to 1626 (`[verification]`); `docs/model-v3/drivers.md` (D7, D8, D16 if present); `pipeline/build_inputs.py`; `registry/inputs-display.yml`; the archived brief `docs/archive/briefs/068g-route-mix-rows.md` for the steps it followed.

## Goal
The register holds every setting the revenue and fund stage (052c) reads that is not in the pack, so `core/revenue.py` reads them from `registry/inputs.json` and invents nothing.

## Decisions (author and guru, 2026-11-19)
- All rows are judgement rows `(J)` pending in `judgement-decisions.md` (gate G3), each saying plainly that its source is the v2 default or sensitivity grid and is a framing value, not an estimate, as v2's own comments say.
- **Verification hazard** (the author chose 5% central): `lambda_C` central 5, low 0, high 10 (% per year), the yearly chance that a self-declared Route C asset is verified; `lambda_D` central 5, low 0, high 10, the corrective-auction hazard on Route D (v2 couples it to `lambda_C` when 0; here two rows, same values). The identity test I1 sets its own values to v2's reference scenario in the test, not from these rows.
- **Consumption** `c`, the consumption share of net worth each year: central 3.5 (v2 `valgen` D16, `c_mode` fixed), low 0.5, high 5 (the v2 sensitivity values 0.5, 2, 5 bound it; take the end values and say so). A stationary mode is not a row.
- **Fund settings:** `a_window` (trailing years for the mean refund) central 5, low 3, high 10; `horizon` (years after the long reserve fills over which coverage is measured) central 10, low 5, high 15; `safe_share` (share of the fund held in the safe asset) central 0, low 0, high 1.0 (v2 sensitivities 0.5 and 1.0); `exp_ref_year` the year of the reference expenditure over GDP, text or integer, 2019, no range.
- **Levy base:** no new row. M1b reads the register's I-D7a (% of GDP, 2.77 / 2.82 / 2.88) as a constant share of GDP; v2's per-window derivation from the equity price return is not ported. State this in each of I-D7a's Coverage cell and in `drivers.md` D7 (one sentence).
- **Not rows:** Route B deferral rate and the income cap (they act only in the `lien` and `income` modes, unused under `sale`, I-D13e); the short and long reserve multiples (I-D8a, already present).

## Design
1. Add the rows following the register's conventions (choose the family and ids, report them); the five fund and consumption rows each carry low, central and high satisfying the ordering rule except where noted.
2. Add the rows to `judgement-decisions.md` (pending); update the register header counts.
3. Regenerate `registry/inputs.json` (`python pipeline/build_inputs.py`), add `registry/inputs-display.yml` entries, regenerate the page cards (`python pipeline/page_cards.py`) and the data fixture (`python tests/data/make_fixture.py`) if the data tests embed the register; update the pinned row-count tests in `tests/data/` (they pin the register counts).
4. Report whether `tests/model_v3/` pins the register count (P9 reads it from `inputs.md`; do not edit those tests).

## Touches
`docs/model-v3/inputs.md`, `docs/model-v3/judgement-decisions.md`, `docs/model-v3/drivers.md` (D7 one sentence), `registry/inputs.json` (regenerated), `registry/inputs-display.yml`, `docs/restructure/pages/` (regenerated), `tests/data/` (count pins, regenerated fixture), this brief's progress block.

## Acceptance criteria
- Seven new rows: `lambda_C`, `lambda_D`, `c`, `a_window`, `horizon`, `safe_share`, `exp_ref_year`; the I-D7a Coverage note; register header counts correct.
- `python pipeline/build_inputs.py` exit 0; `pytest tests/data`, `tests/gate`, `tests/cards`, `tests/model_v3` pass (separate commands).
- `git diff --stat` limited to Touches.

## Checks to run
The commands above.

## Out of scope
The model, the pack, any other register row.

## Open questions
None. If a convention forbids an integer-valued row, say so and propose the form.

## Implementation notes
<!-- progress:start -->
- **Done:** family D14 (run settings, tier 2), seven `(J)` rows in `inputs.md`: I-D14a `lambda_C` 0/5/10 % per year, I-D14b `lambda_D` 0/5/10, I-D14c consumption `c` 0.5/3.5/5 % of net worth per year (end values of v2's 0.5, 2, 5), I-D14d `a_window` 3/5/10 years, I-D14e `horizon` 5/10/15 years, I-D14f `safe_share` 0/0/100 % of fund, I-D14g `exp_ref_year` 2019/2019/2019. Each cites the v2 `WDT_Params.toml` line. I-D7a Coverage notes that M1b reads it as a constant share of GDP and v2's per-window derivation is not ported; one sentence added to `drivers.md` D7. Added to `judgement-decisions.md` (pending); counts now 287 rows and 103 `(J)`; display entries; `inputs.json`, fixture regenerated (cards unchanged); pins 280 to 287 in `tests/data/test_build_inputs.py`.
- **Next:** the author decides the seven rows at gate G3; 052c reads them from `registry/inputs.json`.
- **Decisions:** one family D14, ids a to g. `safe_share` stored as a percentage (0/0/100) to match the other share rows, not the brief's fraction 1.0; the row's unit says "% of fund". `exp_ref_year` is an integer row with unit tag `count` (no `year` tag exists) and repeats 2019. Hazard rows use the tag `pct_per_year`.
- **Gotchas:** `build_inputs` prints one old warning (I-H2a10 cites SN3), not from this brief. `tests/model_v3/` does not pin the register count: P9 reads it from `inputs.md` and passes at 287.
- **Resume:** none; merged.
- **Not run:** site build.
- **State:** merged to main.
<!-- progress:end -->
