# Model v1: inventory and mechanism (brief 001c, stage A)

Audit of `model_v1/` (published URL `/model/`). Read-only: no model file was edited and no model script (`run_all`, any `*_core.py main`, any table or chart script) was run. Date: 2026-11-15, repo at `7377c47` (main). Stage B (errors) is not started: where this note meets a fault it records the fact and leaves the register status to stage B.

How evidence is marked: **[code]** read in the named file and function; **[run]** short Python snippet run from the shell with `PYTHONDONTWRITEBYTECODE=1`, nothing written into the repo (`git status` clean afterwards); **[json]** read from a tracked file in `model_v1/OUTPUTS/`.

## 1. Headline facts

1. v1 is 21 Python modules, 18,136 lines (`wc -l`), plus `WDT_Params.toml` (554 lines), `run_all.bat` (47), `WDT_Model_Reference.md` (629) and four test scripts (1,683 lines).
2. **v1 cannot run as shipped.** Six code files import `rates_core`, but the module is `rates_core1.py`: `wdt_analytics.py:99`, `sweeps_core.py:68`, `8_2_RATES_tables.py:51`, `8_3_RATES_charts.py:55`, `16_3_SWEEPS_R_tables.py:26`, `16_4_SWEEPS_R_charts.py:33` **[run]** (each raises `ModuleNotFoundError: No module named 'rates_core'`). `run_all.bat` also names `rates_core.py` and `sweeeps_core.py` (typo), neither of which exists. Of the 16 entries in `run_all.bat`, 8 cannot start (section 2.3). Present on `main` before this audit; `docs/brief-suggestions.md` already logs it for `wdt_analytics`.
3. v1 never reads `jst_r6.json` (1.7 MB in the folder) **[code]** (grep for `jst` in all `*.py`: no hits). The historical return series is hardcoded in `WDT_Params.toml` `[returns]` (73 values, 1947 to 2019).
4. The cores `wdt_core`, `val_core`, `rates_core1`, `wfr_core`, `ldw_core` import cleanly; `wdt_fmt`, `wdt_md`, `wdt_style` import cleanly **[run]**.
5. Only four paper sources embed model PNGs by filename (papers 5, 8, 9, 19). 65 of the 84 tracked PNGs are referenced; 19 are not; 6 names embedded in paper 19 do not match any tracked file (section 5).
6. Tests cover only the helper modules (`wdt_fmt`, `wdt_md`, `wdt_style`, `wdt_analytics`). No test exists for `wdt_core`, `val_core`, `rates_core1`, `sweeps_core`, `wfr_core` or `ldw_core`. 320 assertions pass; the fourth test file cannot import (section 7).

## 2. Inventory

Order of dependence: base modules, then cores, then output scripts. "Imports" lists project modules only (from `ast` plus the `import rates_core` lines the parser cannot resolve).

### 2.1 Modules

| Module | Lines | Role | Imports (project) | Reads | Writes |
|:---|---:|:---|:---|:---|:---|
| `wdt_core.py` | 1,248 | Shared mechanics: rate function `tau`, Route C `simulate`, `simulate_sell`, `settle_tw`, metrics `run_pair`, fund helpers `_ssm_marginals`, `_ssm_lrr_fill_year`, `load_params` | none | `WDT_Params.toml` via `tomllib` (`load_params`, line 1063) | nothing |
| `wdt_fmt.py` | 416 | Number formatting, `out_dir`, stats helpers `median`, `mean`, `success` | none | n/a | n/a |
| `wdt_md.py` | 532 | Markdown assembly: `md_table`, `pct_table`, `key_value_table`, `MdDoc` | none | n/a | n/a |
| `wdt_style.py` | 319 | Figure style, colours, `save_fig` | none | n/a | n/a |
| `val_core.py` | 1,161 | VAL runner: tables C.1 to C.12, chart series, worked examples, validation | `wdt_core`, `wdt_fmt` | TOML | `OUTPUTS/VAL/val_data.json` (`main`) |
| `rates_core1.py` | 1,709 | RATES: fund model SSM, taxpayer cohort model TCM, 73-start-year sweep, statistics | `wdt_core`, `wdt_fmt` | TOML | `OUTPUTS/RATES/rates_output.json` (`main`) |
| `wdt_analytics.py` | 999 | Sweep infrastructure and C.1 metric: `c1`, `c1_matrix`, `n_crossing`, `summarise`, `run_param_sweep`, `run_g_sweep`, `run_synthetic_sweep`, `draw_c1_heatmap` | `wdt_core`, `wdt_fmt`, `rates_core` (broken) | n/a | n/a |
| `sweeps_core.py` | 419 | SWEEPS runner: VAL.S and RATES.S pre-computation | `wdt_analytics`, `wdt_core`, `wdt_fmt`, `rates_core` (broken) | TOML | `OUTPUTS/sweep_cache.json` (`main`) |
| `wfr_core.py` | 1,635 | WFR welfare comparison: five modules (tax systems, progressive complications, CGT lock-in, heterogeneous tiers, sweeps) | `wdt_core`, `wdt_fmt` | TOML | `OUTPUTS/WFR/wfr_results.json` (`main`) |
| `ldw_core.py` | 530 | LDW purchasing-power calculator and its tables; income tax, NIC, VAT, energy figures hardcoded | `wdt_fmt`, `wdt_md` | nothing | `OUTPUTS/LDW/ldw_tables.md` |
| `5_3_VAL_tables.py` | 858 | VAL appendix C tables | `val_core`, `wdt_fmt`, `wdt_md` | `val_data.json` | `VAL_AppC_Full_Tables.md` |
| `5_4_VAL_charts.py` | 1,042 | VAL figures (14 PNG) | `val_core`, `wdt_fmt`, `wdt_style` | `val_data.json` | `val_fig_*.png` |
| `5_5_VAL_generate_worked_examples.py` | 478 | VAL worked-example figures | `val_core`, `wdt_fmt` | `val_data.json` | `VAL_Worked_Examples_Figures.md` |
| `8_2_RATES_tables.py` | 935 | RATES tables | `wdt_fmt`, `wdt_md`, `rates_core` (broken) | `rates_output.json` | `7_5_WDT_Rates_Revenue_Output.md` |
| `8_3_RATES_charts.py` | 859 | RATES figures (9 PNG names in code, 10 tracked) | `wdt_core`, `wdt_fmt`, `wdt_style`, `rates_core` (broken) | `rates_output.json` | `rates_fig_*.png` |
| `16_1_SWEEPS_V_tables.py` | 312 | SWEEPS.V tables | `wdt_analytics`, `wdt_core`, `wdt_fmt`, `wdt_md` | `sweep_cache.json` | `SWEEPS_V_Appendix_Tables.md` |
| `16_2_SWEEPS_V_charts.py` | 829 | SWEEPS.V figures (21 PNG) | `wdt_analytics`, `wdt_core`, `wdt_fmt`, `wdt_style` | `sweep_cache.json` | `SWEEPS_v_fig_*.png` |
| `16_3_SWEEPS_R_tables.py` | 402 | SWEEPS.R tables | `wdt_analytics`, `wdt_core`, `wdt_fmt`, `wdt_md`, `8_2` (importlib), `rates_core` (broken) | `sweep_cache.json` | `RATES_S_Appendix_Tables.md` |
| `16_4_SWEEPS_R_charts.py` | 1,253 | SWEEPS.R figures (12 PNG) | `wdt_analytics`, `wdt_core`, `wdt_fmt`, `wdt_style`, `rates_core` (broken) | `sweep_cache.json` | `sweeps_r_fig_*.png` |
| `19_2_WFR_tables.py` | 1,058 | WFR appendix tables | `wdt_fmt`, `wdt_md` | `wfr_results.json` | `WFR_appendix_tables.md` |
| `19_3_WFR_charts.py` | 1,142 | WFR figures (27 PNG) | `wdt_fmt`, `wdt_style` | `wfr_results.json` | `wfr_fig_*.png` in `OUTPUTS/WFR/charts/` |

Other files in the folder: `WDT_Params.toml` (inputs), `jst_r6.json` (not read by v1), `run_all.bat`, `WDT_Model_Reference.md` (names `rates_model.py` 11 times; the module is now `rates_core1.py`), `test/` (four scripts), `OUTPUTS/` (95 tracked files, 32 MB, generated).

### 2.2 Dependency order

```
WDT_Params.toml ─► wdt_core ─► val_core ──► val_data.json ──► 5_3, 5_4, 5_5
                       │  └──► rates_core1 ► rates_output.json ► 8_2, 8_3
                       │  └──► wfr_core ───► wfr_results.json ► 19_2, 19_3
                       └─► wdt_analytics ─► sweeps_core ─► sweep_cache.json ─► 16_1 .. 16_4
                           (also imports rates_core)   (also imports rates_core)
ldw_core (no core import; writes its own markdown)
wdt_fmt, wdt_md, wdt_style: leaves used by cores and output scripts
```

Core-to-core imports exist: `wdt_analytics` and `sweeps_core` import the RATES module (`tcm_burden_sweep`, `run_start_year_sweep`, `run_single_scenario` are called through them). Output scripts import cores: `5_3`, `5_4`, `5_5` import `val_core`; `8_2`, `8_3`, `16_3`, `16_4` import `rates_core`; `16_3` imports `8_2` by `importlib`. The refactor map treats these as targets to remove; this note records only that they exist.

### 2.3 Run status by entry in `run_all.bat` [run, import only]

Each numbered script was loaded with `importlib` without calling `main`; each core was imported by name.

| Entry | Result |
|:---|:---|
| `val_core.py`, `wfr_core.py`, `ldw_core.py` | imports ok |
| `5_3`, `5_4`, `5_5`, `19_2`, `19_3` | imports ok |
| `rates_core.py` | file does not exist (the module is `rates_core1.py`) |
| `sweeeps_core.py` | file does not exist (typo; the real file `sweeps_core.py` also fails on `rates_core`) |
| `8_2`, `8_3`, `16_3`, `16_4` | `ModuleNotFoundError: rates_core` (direct import) |
| `16_1`, `16_2` | `ModuleNotFoundError: rates_core` (through `wdt_analytics`) |

Net: 8 of 16 entries cannot start today (`rates_core.py`, `sweeeps_core.py`, `8_2`, `8_3`, `16_1`, `16_2`, `16_3`, `16_4`). Whether the 8 that import would run to completion was not tested.

## 3. Inputs

- `WDT_Params.toml` v7, dated 2026-09-08 (`[meta]`). Sections and size: `[meta]`, `[output]`, `[rate]`, `[swf]`, `[budget]`, `[returns]` (99 lines, 73 values), `[tcm]` (27), `[[tiers]]` x4, `[[brackets]]` x10, `[val]` (92), `[sweep]` (137), `[synthetic_scenario]`. `[meta] excel_checker` points at a frozen Excel file used only for validation.
- Canonical values after `load_params()` **[run]**: tau_0 0.15, tau_m 0.70, k 0.001, W_min 2.0 (£m), `N_val` 30, `N_fill` 19 (also `N` = 19), rho 0.05, `srr_ratio` 3.0, `lrr_years` 3.0, `budget_base` 1157.4, `budget_growth` 0.0451, `returns` length 73. `load_params()` took 0.05 s.
- `jst_r6.json`: not read by any v1 file.

## 4. Outputs and the papers

Tracked `model_v1/OUTPUTS/`: 95 files. JSON: `VAL/val_data.json` 4.8 MB (generated 2026-09-30), `RATES/rates_output.json` 0.2 MB (run_date 2026-09-28), `WFR/wfr_results.json` 0.3 MB, `sweep_cache.json` 1.0 MB (generated 2026-09-28). All four predate the 2026-11-15 folder work; their contents were not regenerated.

| Folder | PNG | Markdown | JSON |
|:---|---:|---:|---:|
| `VAL` | 14 | 2 | 1 |
| `RATES` | 10 | 1 | 1 |
| `SWEEPS_V` | 21 | 1 | 0 |
| `SWEEPS_R` | 12 | 1 | 0 |
| `WFR` (`charts/`) | 27 | 1 | 1 |
| `LDW` | 0 | 1 | 0 |
| root | 0 | 0 | 1 (`sweep_cache.json`) |

Mapping by filename, from image embeds in `source/*.md` (basename match; paper sources are being rewritten, so this is a snapshot):

| Output set | Paper | Embeds found | Notes |
|:---|:---|---:|:---|
| `val_fig_*` (VAL charts) | 5 Valuing Wealth | 10 | 14 generated; `val_fig_7_4`, `7_5`, `7_6`, `7_7` not embedded |
| `rates_fig_*` | 8 Rates and Revenue | 9 | 10 generated; `rates_fig_4a_loss_year_mechanics.png` not embedded |
| `SWEEPS_v_fig_*`, `sweeps_r_fig_*` | 9 Parameter Sweeps | 33 | 33 generated, all 33 embedded |
| `wfr_fig_*` | 19 Taxpayer Welfare | 19 | 27 generated; 13 matched; 14 not matched (list below); 6 embeds match no tracked file |
| Markdown tables (`VAL_AppC_Full_Tables.md`, `VAL_Worked_Examples_Figures.md`, `7_5_WDT_Rates_Revenue_Output.md`, `SWEEPS_V_Appendix_Tables.md`, `RATES_S_Appendix_Tables.md`, `WFR_appendix_tables.md`, `ldw_tables.md`) | 5a/5b, 8a, 9a, 19a, 21 | not machine-linked | no paper source names these files; the tables are pasted or transcribed by hand. Which appendix table comes from which file is not recorded in code or registry |

Totals: 84 PNG generated, 65 matched by an embed, 19 generated but not embedded, 71 distinct embeds, 6 embeds with no tracked file: `wfr_fig_4_1e_combined_gamma1`, `wfr_fig_4_1f_combined_gamma2`, `wfr_fig_4_1g_combined_gamma2` (no code in `19_3_WFR_charts.py` produces them: grep for `4_1e`, `4_1f`, `4_1g`, `combined_gamma` finds nothing), and `wfr_fig_fig_4_5_3b_taum`, `..._3c_k`, `..._3d_wmin` (doubled `fig_` prefix; the generated files are `wfr_fig_4_5_3b_taum.png`, `3c_k`, `3d_wmin`).

The 14 WFR PNGs with no matching embed: `3_1a_cew_by_gamma`, `3_2_variance`, `4_1a_rate_function`, `4_1b_flat_vs_progressive`, `4_1c_leverage`, `4_1d_asymmetry`, `4_2_2b_sensitivity_gain`, `4_5_1a_revenue_target`, `4_5_1b_w0_sensitivity`, `4_5_2a_start_year_distribution`, `4_5_2b_timeseries`, `4_5_3b_taum`, `4_5_3c_k`, `4_5_3d_wmin` (the last three are the files the doubled-prefix embeds below probably intend). The 19 unmatched PNGs are these 14, the four VAL files and the one RATES file above (14 + 4 + 1).

Figure numbers in captions follow the pre-2026 paper numbering (script prefix 16 for sweeps, 5 for VAL). The papers now number SWEEPS as 9; the author has said old numbers do not matter, so this is recorded but not treated as a fault.

## 5. Mechanism

Stated against the papers: `site/pages/Project-Map.md` sections VAL, RATES, SWEEPS, WFR, LDW. Each statement is checked in code; numbers are from short runs.

### 5.1 Shared mechanics: `wdt_core` (feeds VAL, SWEEPS.V, WFR, RATES)

- **Rate function** `tau(W_m, p)`: logistic, `tau_m / (1 + ((tau_m - tau_0)/tau_0) * exp(-k (W - W_min)))` for `W >= W_min`, zero below [code, lines 140 to 152]. Matches RATES §4 in the Project Map. Check [run]: `tau(2.0) = 0.150000` (equals tau_0), `tau(2.0 - 1e-9) = 0`, `tau(1e5) = 0.7000`.
- **Route C simulation** `simulate(V0_m, g_series, alpha, p)` [code, 241 to 287]: each year `V` grows by `g`; declared wealth `W = f * alpha * V`; tax `L = max(-cum, tau(W) * (W - W_prev))` when the delta is positive or cumulative net tax `cum` is positive, else 0; the taxpayer surrenders equity fraction `q = L / W`, so `f <- f (1 - q)`. Refunds are capped at lifetime cumulative tax paid (the "envelope"). This is the in-kind settlement of VAL §4 Route C with the loss refund of the whole paper series.
- **Sell year** `simulate_sell` [code, 294 to 338]: at liquidation alpha drops out (`W_sell = f_N * V_sell`), so an overstater's prior declared basis exceeds `W_sell` and receives a sell-year refund (the self-limiting mechanism of VAL §7).
- **Post-sale settlement** `settle_tw`, `settle_tw_flows` [code, 176 to 234]: iterate the tax/refund oscillation until `|delta|` and `|cum|` are under 1e-10 (max 2000 iterations); returns `TW_settled`, net settlement tax and the flows.
- **Comparison metrics** `run_pair(p, alpha, g, N)` [code, 736 to 763]: `net_pct`, `tw_gap`, `tw_cost`, `pv_pct` all divided by `TW_settled(1)`. `N` must be passed explicitly (`_require_N`, line 123).
- Check [run] at canonical parameters, `g = 10.45%`, `N = 30`: `run_pair(alpha=1.0)` gives 0 on all three metrics; `alpha = 1.5`: `net_pct = +0.009345`, `tw_gap = +0.058455`, `pv_pct = -0.014155`; `alpha = 0.5`: `net_pct = -0.000529`, `tw_gap = -0.061059`, `pv_pct = +0.014729`. The sign pattern (overstater retains more wealth, but pays less in present value) agrees with the VAL §7.1/§7.3 statement that nominal mild-overstatement advantage does not survive NPV adjustment.
- **C.11 decomposition** `decompose_tw_advantage` [code, 802 to 868]: check [run] at `alpha = 1.5, g = 10.45%, N = 30`: `W_sell_delta = -4.0058`, `refund_delta = -24.6958`, `settle_delta = +3.9188`, `tw_advantage = 16.7713` (£m); `W_sell_delta - refund_delta - settle_delta - tw_advantage = 1.6e-13`, so the identity holds to rounding; the function reports `identity_error = 0.0`.

### 5.2 VAL: `val_core` (paper 5, appendices 5a/5b)

`main` [code, 1082 to 1156] builds grids from `[val]` and `[sweep]`, then computes in order: tables C.1 to C.12 (`_compute_tables`), chart series (`_compute_charts`), discount-rate sweep and tolerance zone (`_compute_rho_data`), declaration under uncertainty by Monte Carlo (`_compute_uncertainty`), worked examples (`_compute_examples`), and `_validate`, then writes `val_data.json`. All simulation goes through `wdt_core.run_pair` and friends. Metadata in the tracked JSON: model string "Python v1.1 standalone", convention "TW_settled / Net_settled; common TW(1) denominator; explicit N", scenario start year 2000.

### 5.3 RATES: `rates_core1` (paper 8)

Fund model (SSM, `run_ssm`, `_post_fill_step`) runs the cohort marginal revenue series year by year (N = 1 to 71) through the reserve rules, using `p['returns']`, the 1947 to 2019 UK return series (per `research/model-lessons/mechanics.md`, uniform across the population, so it is the revenue floor; not re-derived here); the taxpayer cohort model (TCM, `run_tcm`, `_tcm_coverage_windows`) splits 10 wealth brackets by 4 growth tiers (`[[brackets]]`, `[[tiers]]`). `run_start_year_sweep` rotates the series over 73 start years. `main` writes `rates_output.json`.
Checks [run] against RATES claims in the Project Map: `run_start_year_sweep` returned 73 rows in 9.5 s; `srr_fill_year` takes the single value 3 across all 73 start years; `lrr_fill_year` has min 7, median 13, max 29; 0 rows have an LRR failure year; `wdt_core._ssm_lrr_fill_year` gives 19 for the 2000 scenario. These agree with RATES §2 (SRR year 3 invariant, 100% success, LRR breakeven 7 to 29, median 13, 2000 breakeven 19).

### 5.4 SWEEPS: `wdt_analytics` and `sweeps_core` (paper 9)

`sweeps_core.main` [code, 370 to 415] calls `init(p)`, then `_compute_val_s` (declaration incentives: C.1 matrices, N-crossing, tolerant zone, plateau, V0 and parameter sweeps; `wdt_core.run_sim`) and `_compute_rates_s` (fiscal sweeps: parameter, g and synthetic-sine sweeps through the RATES engine), and writes `sweep_cache.json` with keys `meta`, `val_s`, `rates_s`. The C.1 metric in `wdt_analytics.c1` divides by `TW_settled(alpha)` per its docstring [code, line 295], whereas `wdt_core.run_pair` divides by `TW_settled(1)`. Whether this changes published numbers is a stage B question and was not run.

### 5.5 WFR: `wfr_core` (paper 19)

Not a simulation of the tax code in `wdt_core`: it defines its own tax functions (`tax_consumption`, `tax_income`, `tax_cgt`, `tax_stock_wealth`, `tax_symmetric_flat`, `ProgressiveRateFunction`) and compares them by certainty-equivalent welfare at revenue equivalence (`solve_revenue_equivalent_rate`, Brent). Modules 1 to 5 correspond to WFR §3 (controlled baseline), §4.1 (progressive complications), §4.2 (CGT lock-in), §4.3 (heterogeneous tiers and concentration) and §4.5 (sweeps). CLI: `python wfr_core.py [--modules 1..5] [--out path]`. It imports `wdt_core` only for parameter loading (`load_params`) and defines its own output path.

### 5.6 LDW: `ldw_core` (paper 21)

Pure arithmetic on 2025/26 income tax, NIC, VAT and energy figures hardcoded in the module (`_income_tax`, `_employee_nics`, `_employer_nics`, `_vat_gain`, `_energy_gain`); no TOML, no simulation, no JSON. `ldw_calc` builds the purchasing-power picture for a salary; `ldw_tables` writes `OUTPUTS/LDW/ldw_tables.md`. Corresponds to LDW §2 and §4.

## 6. Output-script layer

Eleven numbered scripts read the JSON written by one core and write tables or figures; they hold no model logic except where noted: `8_3_RATES_charts.py` calls `wdt_core.simulate` itself (line 583), and `16_1_SWEEPS_V_tables.py` calls `wdt_core.run_sim` directly (lines 131 to 167) and imports `n_crossing` from `wdt_analytics` (line 18) instead of reading everything from `sweep_cache.json`. These are inventory facts; whether they count as errors is stage B.

## 7. Tests

Four standalone scripts, run as `python test_x.py` from `model_v1/test/` with `PYTHONPATH=..` (not pytest). Results [run]:

| Script | Lines | Result |
|:---|---:|:---|
| `test_wdt_fmt.py` | 318 | 107 passed, 0 failed |
| `test_wdt_md.py` | 489 | 82 passed, 0 failed |
| `test_wdt_style.py` | 322 | 131 passed, 0 failed |
| `test_wdt_analytics.py` | 554 | cannot start: `ModuleNotFoundError: rates_core` at `wdt_analytics.py:99` |

Not tested: `wdt_core` (tau, simulate, settle, run_pair, decompose), `val_core`, `rates_core1`, `sweeps_core`, `wfr_core`, `ldw_core`, all eleven output scripts. The mechanism checks in section 5 are therefore this audit's own snippets, not existing tests.

## 8. Not run, and why

- `run_all.bat`, any `*_core.py main`, any table or chart script: out of scope for the audit; several cannot start anyway.
- Any regeneration of `OUTPUTS/`: the tracked JSON, tables and figures are dated 2026-09-28 to 2026-09-30 and were read as is. Whether they match what the current code would produce was not tested.
- `jst_r6.json`: not opened (guide rule); no code reads it.
- Errors and the drift register: stage B.

## 9. Pointers for stage B (facts only, not statuses)

- `rates_core` name break (section 1.2) likely makes a large part of the drift register moot or unreproducible until fixed; stage B should decide how to treat register items that name `rates_core`.
- Two C.1 denominators (section 5.4) can be reproduced with a short snippet at stage B, as `run_pair` and `c1` are both callable.
- WFR paper embeds three figures the chart script cannot produce (section 4).
