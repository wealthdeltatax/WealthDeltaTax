> Legacy reference for the v1 and v2 models, kept as input for the model v3 refactor (brief 001). Not a rule source. Do not read unless a brief says so.

# Drift register

Places where the code departs from the conventions in `conventions.md` or from its own
documentation. Compiled from a read-through of the files uploaded on 2026-09-30 (cores,
presentation scripts, infrastructure modules, TOML, `run_all.bat`, `WDT_Model_Reference.md`).
It was a read-through, not an execution: nothing here was run. Items marked *(verify)*
should be confirmed by running before fixing.

The user expects this list to be long and incomplete; the codebase is mid-refactor. Use
it to (a) avoid rediscovering items, (b) choose what to fix when asked to "clean up",
(c) recognise which drift is new. When an item is fixed, tell the user so they can
strike it from this file (the skill folder is read-only in-session, so updates need a
re-package).

Contents: A Hardcoded values · B Numerics and consistency · C Layering and duplication ·
D Layout and naming · E Stale documentation · F Suggested order

---

## A. Hardcoded values that belong in the TOML

| Where | What |
|:---|:---|
| `rates_core` | `max_N = 71` (several places), `COVERAGE_WINDOWS = [5,10,20,50]`, `burden_N=30` default in `build_rates_output` (should be `p['N_val']`), `assert len(returns) == 73`, `CYCLE_BUCKETS`/stats buckets (also duplicated in `wdt_style`) |
| `sweeps_core` | fine grids (`tau0_fine range(5,45)`, `taum_fine`, `k_fine`, `wmin_fine`), `v0_points [20,100,500]`, `g_plateau 18–40%`, `under_alphas` redefined locally, calibration `variants` dict with literal values and labels |
| `val_core` | Example parameters §J–§N (V0, g, N, alphas; `0.944` soft-reset ratio; `0.02` auction cost), chart grids (`g_scenarios`, alpha/g fine grids, heatmap grids, surface ranges, `n_right range(5,61)`, `[1.2,1.5,1.8,2.0]`) |
| `wfr_core` | `W0_NORM`, `TARGET_ET`, `GAMMA_VALS`/`GAMMA_CEN` (TOML has `wfr_gamma_vals` too), `tau_cgt 0.24`, `V_ref 10`, gain ratio 0.5, `T=5`, tier→bracket map (`Poor→95%` …), Sweep C `W0_vals [10,30,100]`, leverage grid, `W0` multiples, `range(base_yr, base_yr+73)` |
| `ldw_core` | All 2025/26 income-tax and NIC bands/rates, VAT share, energy baseline/reduction, `_PAPER_SALARIES`; no `load_params` at all |
| `5_5`, `5_3`, `19_3`, `19_2`, `8_3` | Numbers typed into text: "£20.000m/£16.000m/£10.000m", "g = 7%, N = 5, τ = 15%", "+3.45pp / £2.86m / −4.55pp / £139.6m" (corner labels), "E[T]=2%", "£2m threshold", canonical marker `2000`, "73 start years", "71-year", "Balanced scenario" |
| `rates_core._compute_coverage_windows` | `3.0 * budget_base` for the extended LRR target: should be `lrr_years`; wrong whenever `lrr_years ≠ 3` (affects below-floor counts in extension years only) |

## B. Numerics and consistency

1. **C.1 has two denominators.** `wdt_core.run_pair` / `val_core` divide by `TW_settled(1)`;
   `wdt_analytics.c1()` (used by VAL.S via `sweeps_core`) still divides by `TW_settled(α)`.
   Figure/table text in `5_3` and `5_4` still says `/TW(α)`. VAL and VAL.S "C.1" are
   therefore not the same metric for α ≠ 1. Needs a decision, then one implementation.
2. **`5_4` reads legacy keys.** `val_core` now ships `matrix_net`, `matrix_tw_cost`,
   `matrix_pv` but `5_4` still reads `matrix` / `c1_matrix` / `surfaces`, so the new
   common-denominator views are never plotted. Legacy keys happen to hold net (and, for
   fig 7.1d, corrected PV) so nothing crashes; titles are what's stale.
3. **`5_3` prose is stale.** C.12 "Metric" still describes `Σ L_t/(1+ρ)^t` (the retired
   version); the C.11 "Purpose" paragraph lists excess periodic tax as one of three
   summands, contradicting the corrected identity in the next paragraph. Footer says
   "Python model v1.0" while `val_core` meta says v1.1.
4. **`8_2.write_report` uses undefined `model`** (`model.run_tcm`) when `py_tcm_burden`
   is None. `NameError`. The JSON path always supplies it so it hasn't fired. *(verify)*
5. **Burden sweep N.** `rates_core.tcm_burden_sweep` runs `run_tcm(p, N=p_base['N'],
   N_fill=1)`, i.e. `N_fill` (≈19), not the canonical burden horizon 30; `16_4` titles
   it "fixed N={p_base['tcm_N']}" (the fallback snapshot, 30). Title and computation
   disagree, and both disagree with the N convention. *(verify which N is intended)*
6. **Two rate-function implementations.** `wfr_core.ProgressiveRateFunction.rate` returns
   0 for `W <= W_min`; `wdt_core.tau` returns 0 only for `W < W_min` (value `τ_0` at
   exactly `W_min`). Also `effective_rate` uses a midpoint approximation, unlike Route C.
   WFR should use `wdt_core.tau` or document the deliberate difference.
7. **Stale "canonical" marker.** `sweeps_core` calibration variants label `τ₀=20% (canon)`
   and `16_2.fig_7_1` marks that bar by index; TOML canonical τ₀ is 15%.
8. **Synthetic scenario is tangled (user: its own refactor).** TOML `mu = 0.07`,
   `amplitude = 0.08` but comments (TOML, `16_4`) say μ = 2%, A = 4%, g ∈ [−2%, +6%];
   actual range ≈ −1% to +15%. Fallback literals in `sweeps_core`, `wdt_analytics`, `16_3`
   disagree with the TOML. Don't pick a side in passing; see `refactor-map.md` §7.
9. **`val_core._to_json_safe` doesn't null NaN/inf** but dumps with `allow_nan=False`,
   so any NaN raises. The other three sanitisers do null them.
10. **Fixed-N assumptions in `val_core._validate`**: requires `N_val ∈ n_actual_vals`
    and `p['g'] ∈ g_vals`; fails loudly if the TOML grids change. Probably fine, but
    document.
11. **`16_1` simulates.** Sections B.4, B.5, B.8.5 call `run_sim` / `n_crossing` though the
    docstring says everything comes from cache; B.9 ("figure index") is announced in
    `main()` but no function exists.
12. **`8_3.fig_4`** runs `simulate()` itself (presentation simulating) and has an unused
    `g_sell`; `fig_7_3b` legend label is missing a `)` and the suptitle ends with a dangling
    `|`.
13. **Static claims in prose** (`16_3` reading notes: "0 failures at Balanced", "100%
    success") are not checked against the data.

## C. Layering and duplication

- Four JSON sanitisers: `val_core._to_json_safe`, `rates_core._sanitise`,
  `sweeps_core._jsonify`, `wfr_core._sanitise`. One `save_json/load_json` belongs in `wdt_core`.
- `_weighted_quantiles` is canonical in `rates_core`; `16_4` still has an unused copy.
- **Core-to-core imports (forbidden by decision):** `sweeps_core` imports `rates_core`
  (`tcm_burden_sweep`) and, through `wdt_analytics`, the RATES engine
  (`run_start_year_sweep`, `run_single_scenario`). `wdt_analytics` imports `rates_core`.
  Presentation also imports cores: `8_2`, `8_3`, `16_4` import `rates_core`; `5_x`
  import `val_core` for the loader.
- `wdt_analytics` (being dissolved, `refactor-map.md` §3) imports `rates_core`, hosts sweep runners (`run_param_sweep`,
  `run_g_sweep`, `run_synthetic_sweep`, `summarise`) that are core logic, and hosts
  `draw_c1_heatmap` that is chart code. It also has an unused import. `wdt_fmt` hosts
  `median/mean/success` (domain logic) only to dodge a circular import, which is a symptom.
- The capitalisation logic exists in four places: `_ssm_lrr_fill_year`, `run_ssm`,
  `_ssm_stripped`, `_tcm_coverage_windows`. `run_ssm` and `_ssm_stripped` are near-duplicates.
  Changing one silently desynchronises the others.
- `load_params` runs a full SSM marginal pass on every call, and every script calls it;
  `_ssm_marginals` is also recomputed in `run_ssm`. Slow; no caching.
- `wfr_core` defines its own `TOML_PATH`, `OUTPUT_ROOT`, `module_output_dir`, and a
  `load_params` wrapper instead of `wdt_fmt.out_dir` / `wdt_core.load_params`.
- Presentation imports: `16_3` imports `8_2` (via importlib; only `write_report`, which it
  doesn't use); `8_2` imports private `_tcm_coverage_windows`.
- `rates_core` mixes console reporting (`report_*`, `run_scenario_profiles`) into the
  core, and imports private `_ssm_marginals` from `wdt_core`.
- `16_2` is three scripts concatenated (mid-file docstrings, duplicate `_load`/`_save`).
  `16_4` uses module-level mutable state (`BASELINE`, `SWEEP_*`) populated in `main()`
  and prints the whole params dict.
- Presentation bypasses the shared style: `19_3` defines inline styling (`_style_ax`),
  inline palettes, and saves at `DPI_SCREEN` (150); `16_2` / `16_4` / `8_3` use inline
  hex and local figure sizes (`_FIG_*` in `8_3` are flagged "not yet in wdt_style").
- `5_3` and `5_5` build markdown with raw `lines.append`; `5_5` uses `date.today()`
  rather than `today_iso()`; `ldw_core` duplicates the `wdt_md` separator map.
- `sweeps_core` and `16_x` compute the cache path differently (`Path(__file__).parent`
  vs `out_dir('.').parent / 'OUTPUTS'`); the latter works only by path normalisation.

## D. Layout and naming

- Output layout: only `WFR` has `charts/`; nothing has `tables/`; `sweep_cache.json` is in
  `OUTPUTS/` root; `LDW` has no json/tables/charts. JSON names differ per paper
  (`val_data`, `rates_output`, `wfr_results`, `sweep_cache`).
- `run_all.bat` lists `sweeeps_core.py` (typo; file is `sweeps_core.py`), which stops the
  run at that step; and its comment references helper modules that no longer exist.
- Script numbering isn't uniform (VAL 3/4/5, SWEEPS 1–4; RATES and WFR already follow
  `_2` tables / `_3` charts). VAL and SWEEPS renumbering decided; LDW = paper 21
  (`21_2_LDW_tables.py`). Renames in `refactor-map.md` §6.
- Figure filenames/prefixes inconsistent (`val_fig_`, `rates_fig_`, `SWEEPS_v_fig_`,
  `sweeps_r_fig_`, `wfr_fig_`). Figure numbers in titles, function names and filenames
  disagree in places: `5_4` fig 7.2c titled "Figure 7.3"; `16_2` τ_m heatmaps titled
  "Figure 3.1a" (duplicate of the τ₀ one); `16_4` function names vs titles (8.3a/8.3b,
  7.x) vs docstring list (`sweep_fig_01…`); `8_3` docstring lists `rates_fig_01…` but files are
  `rates_fig_7_2_…` etc.
- `generate_charts` flag: parsed in `load_params` and set true in the TOML, but `8_3` no longer
  reads it.

## E. Stale documentation

- `WDT_Model_Reference.md`: `rates_model.py` (now `rates_core.py`); scripts `5_6`, `8_3_260812…`,
  `16_5–16_7` (now `5_4`/`5_5`, `8_2`/`8_3`, `16_1–16_4`); `p['N']` as the primary
  horizon (now `N_val` / `N_fill`); `FIGURE_REGISTRY` in `16_5` (no longer in the uploaded
  files); "ten output scripts"; 8_3 producing markdown (now `8_2`); `generate_charts` guard.
- Docstring self-names: `sweeps_core` ("16_0_compute.py"), `ldw_core` ("wdt_ldw.py"),
  `wfr_core` (output path `OUTPUTS/WFR/wfr/`), `16_x` ("16_0", "16_6", "16_7"),
  `16_3` generated-by string and "rates_model.py / wdt_core.py" mention.
- `WDT_Params.toml`: `[meta] version = "v7"`; comments reference `module5_sweeps.py`,
  "3.4.1–3.4.4", and `wfr_start_years_full` (not defined); `[sweep]` canonical block
  duplicates values from `[rate]`, `[val]`, `[tcm]`.
- Tests: `test_wdt_*.py` (480 tests per reference) weren't in the upload; the reference
  says `test_wdt_analytics` needs v8 updates (`success`, `summarise`).

## F. Order

The refactor order, with regression method, is in `refactor-map.md` §8–§9. In short:
quick fixes → shared JSON/path helpers → engine into `wdt_core` → dissolve
`wdt_analytics` → C.1 fix → output layout and JSON names → renames → LDW → hardcode
sweep → synthetic scenario → docs.
