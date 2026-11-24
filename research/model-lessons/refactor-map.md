> Legacy reference for the v1 and v2 models, kept as input for the model v3 refactor (brief 001). Not a rule source. Do not read unless a brief says so.

# Refactor map

Where things are going. Decisions made by the user: **`wdt_analytics` is dissolved into
the correct files; cores never import each other; JSON naming is made consistent;
VAL and SWEEPS script numbering is updated; LDW is paper 21; the synthetic-scenario
mess is a refactor item.** Everything else here is my proposal from reading the code
and is marked *(proposal)*. Confirm judgement calls with the user before doing them.

Contents: 1 Target dependency graph · 2 The shared engine must move to `wdt_core` ·
3 Dissolving `wdt_analytics` · 4 JSON I/O and paths · 5 JSON names and layout ·
6 Script renames · 7 Synthetic scenario · 8 Step order · 9 Regression method

---

## 1. Target dependency graph

```
WDT_Params.toml
   ▲
wdt_core ◄──────────────┬───────────┬───────────┬───────────┬──────────┐
   ▲                    │           │           │           │          │
   │               val_core   rates_core   sweeps_core   wfr_core   ldw_core      (no arrows between cores)
   │                    │           │           │           │          │
   │                  val_data   rates_data  sweeps_{v,r}_data  wfr_data  ldw_data
   │                    ▼           ▼           ▼           ▼          ▼
   └────────── {n}_{m}_{CODE}_tables / _charts  ◄── wdt_fmt, wdt_style, wdt_md
```

Presentation imports `wdt_core` (for `load_json`, `load_params`, `tau`, path helpers),
`wdt_fmt`, `wdt_style`, `wdt_md`. Never a `*_core`, never another presentation script.
`wdt_fmt`, `wdt_style`, `wdt_md` import no project module.

## 2. The shared engine must move into `wdt_core`

`sweeps_core` is the biggest violator: it calls the RATES start-year sweep
(`rates_core.run_start_year_sweep`, via `wdt_analytics.run_param_sweep`),
`rates_core.run_single_scenario` (g sweep, synthetic sweeps) and
`rates_core.tcm_burden_sweep`, each under parameter overrides. It must recompute, so it
can't just read RATES JSON. The only way to satisfy "cores don't import each other" is
to move the fund-model engine down into `wdt_core`:

| Move from `rates_core` to `wdt_core` | Notes |
|:---|:---|
| `_post_fill_step` | already pure |
| `_compute_coverage_windows` | fix the `3.0 * budget_base` → `lrr_years` bug as a *separate* step after the move |
| `run_ssm` + `_ssm_stripped` | consolidate into one implementation (flag for detail vs sweep) |
| `_tcm_marginal_net`, `_tcm_coverage_windows`, `run_tcm` | |
| `run_start_year_sweep`, `_rotate_returns`, `run_single_scenario` | |
| `tcm_burden_sweep`, `_weighted_quantiles` | removes the unused copy in `16_4` too |
| `validate_params` | `16_4` and `rates_core` both use it |
| `COVERAGE_WINDOWS` | → TOML, read via `p` |
| `median`, `mean`, `success` (from `wdt_fmt`) | circular-import reason disappears once the engine is in `wdt_core` |

Stays in `rates_core`: RATES-specific orchestration (`build_rates_output`), extremals
(`report_start_year_sweep`), `run_scenario_profiles`, `compute_statistics`, console
`report_*`, the RATES JSON assembly. `wdt_core` is already large and this makes it much larger:
**ask the user** whether they want to accept that or split it (e.g. a second base
module). The stated hierarchy has one base file, so don't split unprompted.
Also fold the four copies of the capitalisation logic (`_ssm_lrr_fill_year`, `run_ssm`,
`_ssm_stripped`, `_tcm_coverage_windows`) into one shared helper *after* the move, verifying identical output.

## 3. Dissolving `wdt_analytics`

| Symbol | Destination | Why / note |
|:---|:---|:---|
| `DEFAULT_PARAMS` | delete | `wdt_core._DEFAULT_TOML` exists |
| `CANON_*`, `G_VALS`, `ALPHA_VALS`, … and `init(p)` | delete | read `p['sweep'][…]` directly; presentation reads the grids/canon values from the JSON `meta` (`sweeps_core` already stores most of them) |
| `HEADLINE_WINDOW` | TOML (e.g. `[sweep] headline_window = 10`) | consumed via `p`, stamped in JSON `meta` |
| `make_p`, `_run_sim_cached`, `run_sim_p` | `sweeps_core` | sole consumer; consider replacing `make_p` with `{**p, …}` overrides |
| `c1` | **delete**, use `run_pair(...)['net_pct']` | fixes the two-denominator problem; **behaviour change**: VAL.S numbers shift for α ≠ 1. Do as its own step |
| `c1_matrix`, `n_crossing`, `tolerant_zone_bounds`, `tolerant_zone_width`, `understater_plateau` | `sweeps_core` | sole consumer; `16_1` B.8.5 currently calls `n_crossing` live, so cache that result in the JSON |
| `draw_c1_heatmap` | `wdt_style` | chart code; keep matplotlib lazy |
| `median`, `mean`, `success` re-exports | `wdt_core` (see §2) | |
| `summarise`, `_summarise_single`, `_series_long_enough` | `sweeps_core` | sole consumer |
| `run_param_sweep`, `run_g_sweep`, `run_synthetic_sweep` | `sweeps_core` | call the engine now in `wdt_core` |
| unused `_core_load_params` import | delete | |

Callers to update: `sweeps_core` (all of it), `16_1`, `16_2`, `16_3`, `16_4`
(`init`, `_A.CANON_*`, `draw_c1_heatmap`, `HEADLINE_WINDOW`, `DEFAULT_PARAMS`), and
the infrastructure test file `test_wdt_analytics.py`, which should split across
the destinations.

## 4. JSON I/O and paths *(proposal)*

In `wdt_core`:

- `save_json(path, data)`: one sanitiser (numpy → plain, NaN/inf → `None`, float keys →
  strings), `indent=2`, `allow_nan=False`, creates parent dirs, prints path and size.
  Replaces `val_core._to_json_safe`, `rates_core._sanitise`/`save_rates_output`,
  `sweeps_core._jsonify`, `wfr_core._sanitise`.
- `load_json(path)` plus one `rekey_float(d)` helper (replaces `_rekey_float` in `5_3` and
  `_decode_tcm` in `rates_core`); the loaders `load_val_data` / `load_rates_output` go
  away, and `sweeps` / `wfr` presentation stops opening files by hand.
- Path helpers: `out_dir(code)`, `json_path(code)`, `tables_dir(code)`, `charts_dir(code)`
  (all creating nothing until asked). They live in `wdt_core` because cores need them and
  `wdt_fmt` must stay a leaf; `wdt_fmt.out_dir` and `ensure_dir` call sites then move
  (`ensure_dir` can stay in `wdt_fmt` or move; trivial). `wfr_core`'s own
  `TOML_PATH`/`OUTPUT_ROOT`/`module_output_dir` are deleted.

## 5. JSON names and layout

| Code | Today | Target |
|:---|:---|:---|
| VAL | `OUTPUTS/VAL/val_data.json` | `OUTPUTS/VAL/val_data.json` (unchanged) |
| RATES | `OUTPUTS/RATES/rates_output.json` | `OUTPUTS/RATES/rates_data.json` |
| WFR | `OUTPUTS/WFR/wfr_results.json` | `OUTPUTS/WFR/wfr_data.json` |
| SWEEPS | `OUTPUTS/sweep_cache.json` (`val_s`, `rates_s` keys) | split: `OUTPUTS/SWEEPS_V/sweeps_v_data.json`, `OUTPUTS/SWEEPS_R/sweeps_r_data.json` |
| LDW | none | `OUTPUTS/LDW/ldw_data.json` (core writes JSON; markdown moves to `21_2_LDW_tables.py`) |

All JSON gets a uniform `meta`: `code`, `generated`, `model_version`,
`scenario_start_year`, `N_val`, `N_fill`, parameter snapshot (and for sweeps the grids and
canonical values presentation needs). `rates_output.json` is flat today; wrap it.
Markdown → `tables/`, PNG → `charts/`. Pattern `{code}_data.json` is *(proposal)*; the
user only said names must be consistent.

Downstream: the Quarto/site paths and `.qmd` includes likely point at current
locations. Ask the user to check before moving output files.

## 6. Script renames

Pattern `{paper#}_{seq}_{CODE}_{tables|charts}.py`, `_2` = tables, `_3` = charts
(RATES/WFR already follow it). Paper numbers: VAL 5, RATES 8, SWEEPS 16, WFR 19, LDW 21.

| Current | Target |
|:---|:---|
| `5_3_VAL_tables.py` | `5_2_VAL_tables.py` |
| `5_4_VAL_charts.py` | `5_3_VAL_charts.py` |
| `5_5_VAL_generate_worked_examples.py` | *(open)* fold into `5_2_VAL_tables.py` as a second output (`tables/VAL_Worked_Examples_Figures.md`), or keep a separate script with a name that still fits the pattern |
| `16_1_SWEEPS_V_tables.py` | `16_2_SWEEPS_V_tables.py` |
| `16_2_SWEEPS_V_charts.py` | `16_3_SWEEPS_V_charts.py` (it's three scripts concatenated; splitting is optional) |
| `16_3_SWEEPS_R_tables.py` | `16_2_SWEEPS_R_tables.py` |
| `16_4_SWEEPS_R_charts.py` | `16_3_SWEEPS_R_charts.py` |
| (tables inside `ldw_core.py`) | `21_2_LDW_tables.py` (+ `21_3_LDW_charts.py` if needed) |
| `8_2`, `8_3`, `19_2`, `19_3` | unchanged |

Cores stay unnumbered. A rename touches: `run_all.bat`, docstring self-names, the
import in `16_3` (which should disappear anyway), the Reference doc, and probably the
site. Figure file prefixes become lowercase `sweeps_v_fig_…` / `sweeps_r_fig_…`
(today `SWEEPS_v_fig_…`). Check with the user because the site may embed these names.

## 7. Synthetic scenario

The user flags this as its own refactor. Don't "fix" it in passing, and don't pick
between the TOML values and the comments. What's tangled:

- TOML `mu = 0.07`, `amplitude = 0.08` vs comments saying 2% / 4% / "−2% to +6%".
- Fallback defaults hardcoded in three more places that disagree with the TOML:
  `sweeps_core` (`mu` default `hist_mean`, amplitude `0.05`), `wdt_analytics.run_synthetic_sweep`
  (`0.1045`, `0.05`), `16_3` prose (`0.1045`, `0.05`).
- Series builder `synthetic_returns` in `wdt_core`; sweep in `wdt_analytics`; runner
  `run_single_scenario` in `rates_core`; extension helper `_series_long_enough` cyclically
  repeats series to 72+ entries (an approximation for non-periodic ones); `n=80` literal repeated.
- `p['synthetic_scenario']` is parsed but consumers use `.get(...)` with literal defaults.
- Plot code (`16_4.fig_7_5`) reads series, params and `ssm_full` from the cache.

Design it deliberately with the user: one TOML section as the only source, no fallback
literals, builder and runner both in `wdt_core`, sweep in `sweeps_core`, titles from data.

## 8. Suggested step order

0. Snapshot current JSON, tables and chart listings (§9).
1. Quick fixes: `sweeeps_core` typo in `run_all.bat`; `model` NameError in `8_2`.
2. `wdt_core`: `save_json` / `load_json` / `rekey_float` / path helpers. Switch cores
   over one at a time; JSON content should be byte-identical apart from name/location.
3. TOML: `headline_window`, coverage windows, any grids needed by the moves.
4. Move the engine into `wdt_core` (§2); update `rates_core` and its presentation scripts.
5. Dissolve `wdt_analytics` (§3); `sweeps_core` absorbs; `draw_c1_heatmap` → `wdt_style`.
   Check `sweeps_core` no longer imports `rates_core` or `wdt_analytics`.
6. C.1 denominator change (§3), as its own step; update text in `5_3`, `5_4`, `16_x`.
7. JSON names, `meta`, split sweeps, output subfolders; update loaders, `run_all.bat`.
8. Script renames (§6).
9. `ldw_core` into the pattern (TOML `[ldw]` → core → JSON → `21_2_LDW_tables.py`).
10. Hardcode sweep (drift register §A), then text literals in titles and captions.
11. Synthetic scenario redesign (§7).
12. Refresh `WDT_Model_Reference.md` and docstrings; update this skill's drift register.

## 9. Regression method

Pure moves must not change numbers. Before step 2 (and again before any step that
touches a core), copy `OUTPUTS/` to a dated snapshot. After a step: re-run the affected
core, then compare each JSON with the snapshot by loading both and checking numeric
equality (tolerance 1e-12) while ignoring `meta.generated`. Diff the generated markdown
as text. For charts, compare file lists and spot-check regenerated figures; PNG byte
equality isn't reliable. Any difference after a "pure move" is a bug in the move.
When a step is *meant* to change numbers (C.1, `burden_N`, `3.0 * budget_base`),
list the expected differences first and check the diff matches only those.
