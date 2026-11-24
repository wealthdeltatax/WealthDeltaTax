> Legacy reference for the v1 and v2 models, kept as input for the model v3 refactor (brief 001). Not a rule source. Do not read unless a brief says so.

# WDT model mechanics

What the model computes and how the key numbers are defined. Derived from the code as
audited, which supersedes the older `WDT_Model_Reference.md` where they differ.

Contents: 1 Rate function · 2 Route C simulation · 3 Metrics · 4 Fund model (SSM) ·
5 TCM · 6 Start-year sweep · 7 N conventions · 8 Function contracts

---

## 1. Rate function

`wdt_core.tau(W_m, p)`:

```
τ(W) = τ_m / (1 + ((τ_m − τ_0)/τ_0) · exp(−k (W − W_min)))     W ≥ W_min
τ(W) = 0                                                       W < W_min
```

`τ(W_min) = τ_0` exactly; `τ → τ_m` asymptotically. `W_min` is a rate-design parameter,
not a population boundary: every adult is in the taxable population, brackets below
`W_min` simply owe nothing. Wherever a docstring writes `(1−τ_0)/τ_0`, it is wrong.

## 2. Route C simulation (`wdt_core`)

Taxpayer settles in kind: each year they surrender equity fraction `q = L/W`.

`simulate(V0_m, g_series, alpha, p)` → records `t=0..N`, each with
`t, V, W, f, cum, L, rate, delta, q`. Per year:
`V ← V(1+g)`; `W = f·α·V`; `Δ = W − W_prev`; `L = max(−cum, τ(W)·Δ)` if `Δ>0 or cum>0`
else 0 (lifetime envelope: refunds capped at cumulative net tax paid); `q = L/W`;
`f ← f(1−q)`; `cum += L`. Negative `L` is a refund.

`simulate_sell(sim, g_next, p)`: at liquidation **α drops out**: `W_sell = f_N·V_sell`.
For overstaters the prior declared basis exceeds `W_sell`, giving a sell-year refund;
this is the self-limiting mechanism. Sell-year `L` is also envelope-capped.

`settle_tw` / `settle_tw_flows`: iterate the post-sale tax/refund oscillation to
convergence (tol 1e-10). Returns `TW_settled`, `net_settle_tax`, and (flows variant)
the per-period flows needed for PV.

`run_sim` (constant g, optional β) and `run_sim_hist` (uses `p['returns'][:N]`, sell
year `returns[N]`) return: `TW` (naive, legacy), `TW_settled`, `TTP`, `Refunds`,
`Net` (holding period only, legacy), `Net_settled`, `records`, `sell`, plus `g_use` or
`g_mean`. **Use `TW_settled` and `Net_settled`.**

β signalling: `g_eff = g + β·ln(α)` (additive; not calibrated; §C.3 exploratory only).

## 3. Metrics

`run_pair(p, alpha, g, N)` is the canonical comparison. All are fractions of the
**same denominator, `TW_settled(1)`**:

| Key | Definition | Sign |
|:---|:---|:---|
| `net_pct` | (Net_settled(α) − Net_settled(1)) / TW(1) | + = pays more net tax (this is C.1) |
| `tw_gap` | (TW(α) − TW(1)) / TW(1) | + = retains more wealth (C.5/C.8) |
| `tw_cost` | −tw_gap | + = worse off, same sign as `net_pct` |
| `pv_pct` | (PVtrue(α) − PVtrue(1)) / TW(1) | + = pays more in PV (C.12, corrected) |
| `pv_declared_pct` | legacy C.12 (discounts credited L) | audit only |

**C.1 has two live definitions.** `wdt_core.run_pair`/`val_core` use the `TW(1)`
denominator (post-refactor). `wdt_analytics.c1()` still divides by `TW_settled(α)`
(pre-refactor), and several table/figure texts still say `/TW(α)`. They give
different numbers for α ≠ 1. See drift register §B.

C.12 (corrected): PV at rate ρ of tax valued at true value surrendered: holding-period
flows `L_t/α` (in-kind at declared price), sell year `L_sell` (cash), post-sale settle
flows (cash). The old version discounted credited `L` and so undercounted understater
payments by 1/α, manufacturing a "deferral gain".

C.11 decomposition (`decompose_tw_advantage`), exact to machine precision:

```
TW_settled(α) − TW_settled(1) = W_sell_delta − refund_delta − settle_delta
```
`W_sell_delta ≤ 0` (f_N erosion), `refund_delta ≤ 0` (bigger sell-year refund),
`settle_delta ≥ 0` (post-sale taxing-back). `excess_periodic` is informational and is
**not** additive in the identity.

Other analytics (`wdt_analytics`): tolerant zone = α band where |C.1| < `tzone_threshold`
(2pp); `n_crossing` = first N where an overstater's Net exceeds honest's (interpolated;
NaN if none); `understater_plateau` = max C.1 over g ≈ 18–40%.

## 4. Fund model: SSM (`rates_core.run_ssm`, `wdt_core._ssm_marginals`)

The SSM applies the historical return series uniformly to the whole population
(correlated shock: the revenue **floor**). `_ssm_marginals(p, max_N=71)` computes
cohort marginal net revenue per year (£b) by differencing cumulative bracket
simulations (`× b['N'] / 1000`).

Balances: SRR (refund reserve) target = `srr_ratio × (cum_net / N)`; LRR (long-run
reserve) target = `lrr_years × budget_t`, `budget_t = budget_base·(1+budget_growth)^(N−1)`.

**Capitalisation (year 1 → LRR fill):** income fills SRR to target; surplus flows to
LRR; phase ends when `lrr_bal ≥ lrr_target`. `N_fill` = that year. The fast path
`_ssm_lrr_fill_year` duplicates this logic for `load_params`; change both together.

**Post-fill, `_post_fill_step` (pure; shared by SSM and TCM), strict priority:**
1. Income → SRR up to target.
2. Remainder → LRR up to floor.
3. LRR covers remaining SRR shortfall. Record `lrr_failure_year` when LRR hits 0,
   `srr_failure_year` when SRR hits 0 (LRR failure always precedes SRR failure).
4. If SRR at target, remaining surplus tops LRR toward floor.
5. `cov_frac = max(0, remainder)/budget_t`, forced to 0 once either failure has occurred
   (including the current year).

**Coverage windows** for W ∈ {5,10,20,50} (`COVERAGE_WINDOWS`): mean `cov_frac` over
post-fill years 1..W → `ssm_cov_W`, plus `ssm_zero_cov_years_W`, `ssm_min_lrr_bal_W`,
`ssm_lrr_below_floor_years_W`. Years beyond the 71-year run carry the last value
forward (approximation). Headline window = `wdt_analytics.HEADLINE_WINDOW` (10); the
`ssm_cov` / `tcm_cov` aliases in `summarise()` follow it.

**Success (v8)** = LRR fills within the window **and** `lrr_failure_year is None`
(`wdt_fmt.success`). v7's "breach" keys are retired (`lrr_breach_year`,
`srr_breach_covered`, `ssm_post_fill_coverage`, …); any code still reading them gets
`None`.

## 5. TCM (`rates_core.run_tcm`, `_tcm_coverage_windows`)

Disaggregates by 10 wealth brackets × 4 growth tiers (Poor/Ok/Good/Great;
differentials from Fagereng et al. 2020; weights and differentials in TOML; weighted
mean differential ≈ 0). Uses the actual return series plus tier differential, so
returns are heterogeneous: the revenue **ceiling** relative to the SSM floor.

- `run_tcm(p, N, N_fill)`: per bracket×tier snapshot at horizon N (feeds the B.3
  tables: `V_at_N, TW_settled, avg_net_gbp, wealth_burden, eff_rate,
  income_tax_rate, revenue_m, post_fill_*`). `income_tax_rate = total_net_settled /
  (TW_settled − V0)`, `None` if gain ≤ 0.
- `_tcm_coverage_windows`: independent year-by-year priority loop over 1..71 using
  `_tcm_marginal_net` (differenced cumulative sims), its own SRR/LRR balances, same
  `_post_fill_step`. Produces `tcm_cov_W` and TCM failure years. Only `tcm_cov_W` is
  merged into sweep rows.

## 6. Start-year sweep (`rates_core.run_start_year_sweep`)

For each of 73 calendar start years (1947–2019): rotate canonical returns, run
`_ssm_stripped` (same logic as `run_ssm`, trimmed), then `_tcm_coverage_windows` using
that year's SSM fill year. Extremals: Speed, Margin, Durability (50yr SSM coverage),
Resilience (LRR failure year; no-failure is best). `run_single_scenario(p, series)` runs
one deterministic series (constant-g, synthetic sine) instead of the sweep.
`sweeps_core` runs these under parameter overrides via `wdt_analytics.run_param_sweep`.

## 7. N conventions

| Name | Value | Meaning | Use for |
|:---|:---|:---|:---|
| `p['N_val']` (= `p['N_demo']`, `[val] N_demo`) | 30 | taxpayer holding period | all VAL tables/figs; RATES burden tables (`burden_N`) |
| `p['N_fill']` | derived (19 for 2000 start, τ₀=15%) | SSM LRR fill year | RATES capitalisation-window tables, TCM snapshot `tcm_N`; reference lines |
| `p['N']` | = `N_fill` | legacy alias | do not use in new code |
| `[tcm] snapshot_N` | 30 | fallback for `N_fill` if LRR never fills | nothing else |
| `[tcm] canonical_N`, `[sweep] N_canon` | 30 | duplicates of `N_demo` | compatibility |

Changing τ₀, τ_m, k, W_min, `srr_ratio`, `lrr_years`, the budget, or the scenario start
year can move `N_fill`. Re-run every core afterwards.

## 8. Function contracts (quick lookup)

`wdt_core`: `load_params(toml_path=None)`, `tau`, `g_eff`, `simulate`, `simulate_sell`
(alias `simulate_sell_year`), `settle_tw`, `settle_tw_flows`, `run_sim`, `run_sim_hist`,
`run_pair`, `npv_tax`, `npv_tax_declared` (legacy), `npv_tax_advantage`,
`decompose_tw_advantage`, `synthetic_returns`, `_ssm_marginals`, `_ssm_lrr_fill_year`.

`rates_core`: `load_params` (thin wrapper), `validate_params`, `run_ssm`, `run_tcm`,
`run_start_year_sweep`, `run_single_scenario`, `run_scenario_profiles`,
`compute_statistics`, `tcm_burden_sweep`, `build_rates_output` / `save_rates_output` /
`load_rates_output`.

`wdt_analytics` (after `init(p)`): `make_p`, `run_sim_p` (LRU-cached), `c1`, `c1_matrix`,
`n_crossing`, `tolerant_zone_bounds/width`, `understater_plateau`, `draw_c1_heatmap`,
`summarise`, `run_param_sweep`, `run_g_sweep`, `run_synthetic_sweep`.

`wdt_fmt`: `fmt_pct/pct0/pct1/pct4`, `fmt_gbp_m/b/yr`, `fmt_rev_m`, `fmt_f*`, `eff_rate`,
`dist_row`, `baseline_marker`, `median`, `mean`, `success`, `today_iso`, `out_dir`,
`ensure_dir`. (Stats helpers live here only to break a circular import.)

`wdt_md`: `md_table(headers, rows, col_fmt, fmt_fn)` (col 0 is `str()`, `fmt_fn` on
cols 1+), `pct_table`, `key_value_table`, `MdDoc` (`add`, `blank`, `add_block`,
`add_lines`, `h1–h4`, `caption`, `note`, `rule`, `table`, `table_block`, `render`,
`write`).

`wdt_style`: `apply_style(grid)`, `apply_style_nogrid`, `save_fig(fig, path, dpi=300)`,
FIG_* sizes, C_* colours, `PARAM_COLOURS`, `CYCLE_BUCKETS`.
