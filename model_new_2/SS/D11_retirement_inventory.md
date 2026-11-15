# D11 retirement inventory

Scope: readers of the retiring keys in the files provided (`wdt_core.py`, `valgen_core.py`, `rates_core.py`, `WDT_Params.toml` as described in the Code Reference, `apply_basis_change.py`, `wdt_jst.py`). Downstream scripts (WFR, VAL.A, SWEEPS, VAL.S, RATES.S, `module5_sweeps.py`, `print_val_real_inputs.py`, `rates_test.py`) were **not provided**. Anything said about them below is inferred from comments in `wdt_core` and is marked *(inferred)*.

Status key: **LIVE** = something in the provided code still needs it to run. **DEAD** = only the legacy SSM or nothing reads it.

---

## 1. Headline

1. **`rates_core.py` reads none of the retiring keys.** It loads through `load_rates_params`, which parses only `[rates]`, `[rules]`, `[meta]` and the Phase 2 blocks. RATES is already D11-clean.
2. **`valgen_core.py` has three live ties:**
   - `p['g']` is `hist_mean` from `[tcm]` whenever `[val_gen] g_real` is unset.
   - `_ir()` and `with_val_basis` fall back to `[budget] budget_growth`.
   - `_bridge` uses `p['returns']` through `run_sim_hist`.
   
   Items 1–2 of the plan (real basis, JST replay) are what cut these.
3. **Everything else is held up only by `wdt_core.load_params`.** It hard-reads `raw['swf']`, `['budget']`, `['returns']`, `['tcm']`, `['tiers']`, `['brackets']` and runs the whole legacy SSM at every load (71 years × 10 brackets) just to set `N_fill`. Removing a TOML block before patching `load_params` gives a `KeyError` in valgen.
4. **Do not retire `[sweep]` wholesale.** `alpha_vals`, `g_vals` and `n_actual_vals` are read live by valgen (`_bridge`, `_life_results`, strategies, grids). Only the `*_canon` keys, the `rates_*_sweep` keys and the `wfr_*` keys retire.
5. **Name collision to protect:** `[rates.defaults].tiers` (cohort return tiers, read in `run_window` as `cfg['tiers']`) is *not* the legacy `[[tiers]]` block. Leave it alone.

---

## 2. Key by key

| Retiring item | Where it is read (provided files) | Status | Decision | Replacement |
|:--|:--|:--|:--|:--|
| `[returns]` values, `series_base_year` → `p['returns']`, `canonical_returns`, `returns_meta` | `wdt_core._ssm_marginals`; `wdt_core.run_sim_hist`; `valgen._bridge` (historical half: `p['returns'][:n]`, `run_sim_hist`) | LIVE (bridge only) | **Re-derive** | JST real return series. The bridge can take a JST UK series passed explicitly (`run_sim_hist(dict(p, returns=series), …)`) instead of the canonical array. D1/D1a. |
| `[tcm] hist_mean` → `p['hist_mean']` → `p['g']` | `wdt_core` (`p['g']`, `sweep.g_canon`, `synthetic_scenario.mu` default); `valgen` everywhere through `p['g']` | **LIVE, main tie** | **Re-derive** | `[val_gen] g_real` (JST-derived real g). Make it required, not optional, so a nominal `g` can never silently return. |
| `[tcm] scenario_start_year` (rotates `[returns]`) | `wdt_core.load_params`; `valgen.main` writes `meta.scenario_start_year` | LIVE (meta only) | **Archive** | Superseded by `wdt_jst.loop_windows`. Drop the meta field. |
| `[tcm] snapshot_N`, `canonical_N` → `tcm_N`, `p['tcm']` | `load_params` (`N_fill` fallback, `p['tcm']` view) | DEAD in provided code | **Archive** | None. `p['tcm']` is for the WFR pipeline *(inferred)*. |
| `[budget] budget_growth` | `valgen._ir` fallback; `wdt_core.with_val_basis` fallback; `_ssm_lrr_fill_year` | **LIVE, second tie** | **Re-derive** | `[val_gen] index_rate` = JST real GDP/head growth (plan 3.1.2). Make required. |
| `[budget] budget_base` | `_ssm_lrr_fill_year` only | DEAD | **Archive** | None. RATES uses expenditure/GDP from JST. |
| `[swf] srr_ratio`, `lrr_years` | `_ssm_lrr_fill_year` only | DEAD | **Archive** | Already replaced: `ms`, `ml` in `[rates.defaults]`, read by `run_fund`. Note the rules differ (legacy: target on mean cumulative net; new: trailing mean `A_t`), so the legacy numbers do not reproduce. |
| `[[tiers]]` → `p['tiers']` | none in provided code | DEAD | **Archive** | `[rates.cohorts.*]`. |
| `[[brackets]]` → `p['brackets']` | `_ssm_marginals` only | DEAD | **Archive** | `build_dist` cells in RATES. |
| `N_fill`, `p['N']` | `load_params` sets them; `valgen._validate` writes `report['N_fill']`; `valgen.main` writes `meta.N_fill`; `_require_N` error text | LIVE (meta only) | **Archive** | Per-window `fill_year` in the RATES JSON. Any quoted "N_fill = 19" is a D10 restatement. |
| Legacy SSM: `_ssm_marginals`, `_ssm_lrr_fill_year`, and the call in `load_params` | `load_params` | LIVE (called at every load) | **Archive** | `run_fund`. Removing the call is a free speed-up for every valgen start. |
| `[rate]` canon → `p['tau_0','tau_m','k','W_min']`, `p['rate']` | `rate_params`, `tau`, `valgen` via `with_rate_scenario` | LIVE when `rate_scenario = ''` | **Re-derive** | Rate design comes only from `[val_gen] rate_scenario` (baseline `gain_ladder`, D2). Make `rate_scenario` required. `p['rate']` view is for WFR *(inferred)*. |
| `[sweep]` `*_canon` keys | `load_params` builds them; no reader in provided code | DEAD | **Archive** | None. |
| `[sweep]` `alpha_vals`, `g_vals`, `n_actual_vals`, others | valgen, widely | **LIVE** | **Keep** | Move to `[val_gen]` at the D6 rewrite if you want `[sweep]` gone. |
| `[sweep]` `rates_*_sweep`, `wfr_*` | none in provided code | DEAD here | **Archive with RATES.S / WFR** *(inferred owners)* | RATES scenario overrides cover the RATES ones. |
| `[synthetic_scenario]` | `load_params` only; `synthetic_returns` | DEAD in provided code | **Archive** | None. Plan 3.3 already lists its stale comments. |
| `p['alpha']`, `p['beta']`, `g_eff` | `run_sim` | DEAD | **Archive** | None. |

---

## 3. Legacy functions in `wdt_core` that follow the keys

What valgen still imports from the legacy block: `simulate`, `run_pair`, `run_sim_hist`, `settle_tw_flows`, `tau`, `rate_params`, `with_rate_scenario`, `with_val_basis`, `BASIS_CONVENTION`.

- **Only `run_sim_hist` needs `[returns]`.** `run_pair`, `simulate`, `settle_tw_flows` need none of the retiring keys, so they can stay for now.
- **What they guard:** the P1 bridge (`_bridge`, `run_life` vs legacy to 1e-9) and `_p2_validate` (`single_life_equals_legacy_simulate`). Archiving them removes those guards.
- **Options:**
  1. Keep the single-life Route C block (`simulate`, `simulate_sell`, `settle_tw*`, `run_pair*`, `npv_tax*`) in `wdt_core` until D9 is built, then move it to `wdt_legacy_v7.py`. **Recommended.**
  2. Archive now and freeze the bridge numbers as golden values. This loses a live check during the rewrite.
- **Unused by anything provided** (archive candidates): `declared_path`, `simulate_declared`, `run_declared`, `run_declared_pair`, `npv_true_declared`, `breakeven_rho`, `decompose_tw_advantage`, `npv_tax_advantage`, `run_pair_rhos`, `npv_tax_declared`, `synthetic_returns`, `g_eff`, `run_sim`. Callers may exist in VAL.A / VAL.S / SWEEPS *(not provided)*.

---

## 4. Other findings

1. **`apply_basis_change.py` is a spent one-off.** Its `WDT_CORE` list targets `simulate`, `simulate_declared` and `settle_tw_flows`. Once those move to `wdt_legacy_v7.py` its snippets stop matching (`found 0 times` raises). The provided cores already contain the patched text. Run it once with `--check` to confirm every line says "already applied", then archive it at the tag.
2. **`kernel_test.py` parity test imports `valgen_core` and `wdt_core`.** It calls `load_params`, so it breaks if the TOML blocks go before `load_params` is patched. Order matters (section 5).
3. **Stale text:**
   - `wdt_core._ssm_marginals` docstring says `rates_core.run_ssm()` calls it; `rates_core` no longer has `run_ssm`.
   - The Code Reference notes `tcm_burden_sweep` / `run_tcm` in an old `rates_core`; neither exists now.
   - A comment in `load_params` says WFR reads `p['returns']['array']`; the code stores it at `p['returns_meta']['array']`.
   - `[rates].valgen_dir` is parsed by `_parse_rates` but not read by `rates_core`. Check the presentation scripts before deleting it.
   - Code Reference §2 warns that `[rate]` and `[sweep]` canon differ (30/90 vs 15/70). That mismatch disappears with D2.
4. **Output fields that change.** valgen JSON `meta.N_fill` and `meta.scenario_start_year`, and `meta.params` (dumps all of `[val_gen]`, including `reset_interval` and `death_waiver` until D6). Downstream readers of those fields are unknown.
5. **`[val_gen]` D6 keys** (`reset_interval`, `reset_sens`, `death_waiver`) are not D11 but are read widely: `run_family3`, `_ctx`, `_strategies` (`yrs_to_reset`), `_p3_validate`, `_p5_opts`, `main`, `_route_d_examples`. They go in the plan item 6 valgen rewrite, not this retirement.

---

## 5. Order of operations

1. **Items 1–3 land first** (user's patch): D2 ladder baseline, `g_real` / `index_rate` live in `[val_gen]`, JST replay, `[rho]`. After this, `p['g']`, `budget_growth` and `hist_mean` have no live reader.
2. **Patch `load_params`:** make the retiring blocks optional (`raw.get`), drop the SSM call, `N_fill`, `p['N']`, `p['tcm']`, `p['returns_meta']`, and require `g_real`, `index_rate` and `rate_scenario`. Re-run valgen and `kernel_test.py` to confirm nothing else broke.
3. **Re-point the bridge** at a JST series (section 2, `[returns]` row).
4. **Delete the TOML blocks:** `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]`, `[[brackets]]`, `[rate]`, the `*_canon`, `rates_*_sweep`, `wfr_*` keys, `[synthetic_scenario]`.
5. **Remove the dead code** from `wdt_core` (`_ssm_*`, `load_params` sections, unused legacy runners). Move the single-life block to `wdt_legacy_v7.py` after D9.
6. **Tag `legacy-v7` before step 2.** This is Phase 0 and everything above assumes it.
7. **Clean the downstream scripts** once they are available (the WFR, SWEEPS, VAL.A, VAL.S, RATES.S group).

---

## 6. Needed from the user to finish

- The downstream scripts, or a grep for `p\['(swf|tiers|brackets|budget|tcm|returns|rate|hist_mean|N_fill|N)'\]` and `\['sweep'\]\['(rates|wfr)_` across the repo. That list is the remaining half of the inventory.
- Confirmation of which of the unused legacy runners (section 3) are called from the downstream scripts.
- Whether `p['g']` as a name should survive. Items 1–2 may rename it (for example `g_real`).
