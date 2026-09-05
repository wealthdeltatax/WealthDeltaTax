# WDT Output Pipeline — Model Reference

This document describes the Python simulation and output pipeline for the Wealth Delta Tax (WDT) model. It is the reference for maintaining, extending, and debugging the codebase. It covers the computational architecture, the individual simulation mechanics, the output pipeline structure, the parameter system, and the known issues and conventions that have accumulated over the project's history.

**Current model version: v8.** See §11 for a complete changelog from v7.

---

## 1. Architecture overview

The codebase has two layers that are kept deliberately separate.

**The computational layer** consists of two files: `wdt_core.py` and `rates_model.py`. These contain all simulation logic and no output logic. They have no matplotlib dependency. They can be imported, tested, and reasoned about without producing any files.

**The output layer** consists of four infrastructure modules (`wdt_fmt.py`, `wdt_md.py`, `wdt_style.py`, `wdt_analytics.py`) and ten output scripts. The output scripts call into both the computational layer and the infrastructure modules to produce the actual figures and tables.

The single source of truth for all parameters is `260812_WDT_Params.toml`. Nothing is hardcoded in the Python files that belongs in the TOML.

```
260812_WDT_Params.toml
        │
        ▼
  wdt_core.load_params()          ← TOML → unified params dict p
        │
        ├── wdt_core.py           ← rate function, simulation engine, NPV
        └── rates_model.py        ← SSM, TCM, start-year sweep
                │
                ▼
        output scripts (5_3, 5_4, 5_6, 8_3, 16_2–16_7)
                │
                ├── wdt_fmt.py    ← number → string formatting
                ├── wdt_md.py     ← markdown table and document assembly
                ├── wdt_style.py  ← matplotlib style, colours, figure saving
                └── wdt_analytics.py ← C.1 metric, sweep runner, statistics
```

---

## 2. The parameter system

### 2.1 Loading

All scripts call `wdt_core.load_params(toml_path=None)`. This reads the TOML, rotates the return series to the scenario start year, runs the minimal SSM to derive `p['N']` (the LRR fill year), and returns a unified dict `p` used everywhere.

`p['N']` is **computed**, not read from the TOML. It is the year at which the LRR fills under the active scenario. This means changing any rate or SWF parameter can change `N` automatically on the next run. The TOML field `snapshot_N` is a fallback only, used if the SSM fails to fill within 71 periods.

### 2.2 Key parameters

| Key | TOML section | Description |
|:---|:---|:---|
| `tau_0` | `[rate]` | Floor marginal rate at W = W_min (fraction) |
| `tau_m` | `[rate]` | Asymptotic ceiling rate (fraction) |
| `k` | `[rate]` | Steepness of logistic climb (per £m) |
| `W_min` | `[rate]` | Entry-point wealth; below this τ = 0 (£m) |
| `srr_ratio` | `[swf]` | SRR target = ratio × (cumulative net income / N) |
| `lrr_years` | `[swf]` | LRR target = lrr_years × prevailing expenditure |
| `budget_base` | `[budget]` | OBR total managed expenditure base year (£b) |
| `budget_growth` | `[budget]` | Nominal expenditure growth rate (fraction p.a.) |
| `returns` | `[returns]` | 73 annual UK equity returns, 1947–2019 (fraction) |
| `scenario_start_year` | `[tcm]` | Calendar year at which the active scenario begins |
| `hist_mean` | `[tcm]` | Population-weighted mean return (fraction) |
| `tiers` | `[[tiers]]` | Array of growth tier dicts (label, weight, differential) |
| `brackets` | `[[brackets]]` | Array of wealth bracket dicts (label, N_pop, V0_m) |

### 2.3 Derived fields added by load_params()

| Key | Description |
|:---|:---|
| `p['N']` | LRR fill year (SSM-derived; the primary simulation horizon) |
| `p['returns']` | Canonical series rotated to scenario_start_year |
| `p['canonical_returns']` | Unrotated series (used by the sweep) |
| `p['g']` | Alias for hist_mean |
| `p['V0_m']` | VAL reference entry wealth (from `[val]`) |
| `p['rho']` | Discount rate for NPV calculations (from `[val]`) |
| `p['sweep']` | Fully parsed analytical grid constants (all `[sweep]` keys) |

### 2.4 The sweep dict

`p['sweep']` contains all canonical reference values and analytical grid constants used by the VAL.S sensitivity scripts. The VAL.S scripts access these via `wdt_analytics` after calling `init(p)`. The key ones:

- `CANON_TAU0/TAUM/K/N/V0/G/WMIN` — reference point for all single-parameter sweeps
- `G_VALS`, `ALPHA_VALS` — the C.1 heatmap grid
- `TAU0_VALS`, `TAUM_VALS`, `K_VALS`, `WMIN_VALS` — panel sweep values
- `N_SWEEP` — full list for N-crossing detection (range 5–65)
- `tzone_threshold` — |C.1| below which declaration error is "negligible" (default 2pp)

---

## 3. The rate function

The WDT marginal rate is a logistic function of declared wealth W:

```
τ(W) = τ_m / (1 + ((τ_m - τ_0) / τ_0) × exp(-k × (W - W_min)))
τ(W) = 0    if W < W_min
```

Implemented in `wdt_core.tau(W_m, p)`.

Key properties:
- τ(W_min) = τ_0 exactly (the floor)
- τ(∞) → τ_m asymptotically (the ceiling, never reached)
- k controls how steeply the rate climbs from τ_0 toward τ_m
- W_min is a rate design parameter, not a population boundary — all UK adults are in the taxable population regardless of W_min; brackets below W_min simply have zero liability

**Known documentation error:** `rates_model.py` docstring writes the denominator coefficient as `(1-τ_0)/τ_0`. The correct formula, as implemented in `wdt_core.tau()`, uses `(τ_m - τ_0)/τ_0`. The implementation is correct; only the docstring is wrong.

---

## 4. The Route C simulation

Route C is the equity-transfer settlement route. The taxpayer transfers fractional equity to the state each period rather than paying cash. This is the settlement mechanism used in all VAL and VAL.S analysis.

### 4.1 Holding period: simulate()

`wdt_core.simulate(V0_m, g_series, alpha, p)` → list of N+1 record dicts

Each period t:
1. True value grows: `V_t = V_{t-1} × (1 + g_t)`
2. Declared wealth: `W_t = f × α × V_t`  (f is the retained equity fraction)
3. Delta: `Δ = W_t - W_{t-1}`
4. Tax: `L = max(-cum, τ(W_t) × Δ)` if Δ > 0 or cum > 0, else 0  (lifetime cap)
5. Equity fraction: `q = L / W_t`; `f' = f × (1 - q)`
6. Cumulative: `cum += L`

The `alpha` parameter is the declaration ratio. `alpha = 1.0` is honest declaration. `alpha < 1.0` understates; `alpha > 1.0` overstates. The declared wealth is always `f × alpha × V`, so alpha is applied relative to the current retained fraction, not to the original value.

Record fields per period: `t, V, W, f, cum, L, rate, delta, q`

### 4.2 Terminal sell year: simulate_sell()

`wdt_core.simulate_sell(sim, g_next, p)` → dict

At liquidation, **alpha drops out entirely**:

```
W_sell = f_N × V_sell        (not f_N × α × V_sell)
```

The taxpayer receives their retained equity fraction of true sale proceeds. For overstaters, the prior declared basis (`f_N × α × V_N`) typically exceeds `W_sell`, generating a negative delta and a sell-year refund. This is the key mechanism by which overstatement is self-limiting — the inflated basis creates a larger refund liability at sale.

The sell-year tax is also lifetime-capped: `L_sell = max(-cum_N, τ(W_sell) × δ_sell)`.

### 4.3 Post-sale settlement: settle_tw()

`wdt_core.settle_tw(sell_result, p)` → (TW_settled, net_settle_tax, n_iter)

After liquidation there is a residual oscillation: the sell-year refund creates a new basis gap which generates a small tax in the following period, which creates another small basis gap, and so on. `settle_tw` iterates this to convergence (tolerance 1e-10, max 2000 iterations — in practice always converges in a handful of steps).

`TW_settled` is the **primary output metric** for terminal net worth. The naive `TW = W_sell - L_sell` (the raw sell-year figure) is retained in the output dict for backward compatibility only and should not be used for analysis.

`Net_settled = TTP + Refunds + net_settle_tax` is the **primary output metric** for total lifetime tax.

### 4.4 Convenience runners

`run_sim(p_in, alpha, beta, N, g)` — constant-g simulation with settle_tw applied. Returns the full output dict including `TW_settled`, `Net_settled`, `records`, `sell`, etc.

`run_sim_hist(p_in, alpha, N)` — uses `p['returns']` as the g_series instead of a constant g. Also returns `g_mean`.

### 4.5 The beta (signalling) parameter

`wdt_core.g_eff(g, alpha, beta)` implements an exploratory signalling adjustment:

```
g_eff = g + β × ln(α)
```

A positive β means overstatement partially self-fulfils by contributing to confidence formation, increasing true growth. This is not empirically calibrated and is used only in the §C.3 exploratory extension. **VAL.A §B.3 documents this incorrectly as a multiplicative formula** — the implementation uses the additive form shown above, which was confirmed from the original Excel cell.

---

## 5. The C.1 metric

The C.1 metric is the primary incentive-alignment measure used throughout VAL and VAL.S:

```
C.1(α) = (Net_settled(α) − Net_settled(1)) / TW_settled(α)
```

Positive = α pays more net tax than honest declaration (understater penalty).
Negative = α pays less net tax than honest declaration (overstater advantage).

Implemented in `wdt_analytics.c1(p, alpha, g, N)`.

The α = 1.0 row is always exactly zero by construction.

### 5.1 The tolerant zone

The tolerant zone is the α band where |C.1| < threshold (default 2pp). Declaration errors in this band produce negligible incentive distortion — neither meaningful penalty nor meaningful saving. Analysed in VAL.S §2–§4 across all parameter sweeps.

### 5.2 The N-crossing threshold

For overstaters, C.1 is initially negative (advantage) but reverses sign at some holding period N — the point at which the accumulated f_N dilution and the damping of the sell-year refund overcome the refund benefit. This crossing N is tracked by `wdt_analytics.n_crossing(p, alpha, g, N_sweep)`.

At canonical parameters, aggressive overstaters (α ≥ 1.8) cross within the RATES reference holding period N.

### 5.3 The TW advantage decomposition (C.11)

`wdt_core.decompose_tw_advantage(p, alpha, g)` splits the TW_settled(α) − TW_settled(1) advantage into three additive terms verified to machine precision:

```
tw_advantage = W_sell_delta − refund_delta − settle_delta
```

- `W_sell_delta` ≤ 0: f_N erosion reduces sell-year declared value
- `refund_delta` ≤ 0: overstater receives larger sell-year refund
- `settle_delta` ≥ 0: post-sale damping taxes back part of the refund

**Excess periodic tax is NOT additive in this identity.** It is returned as an informational field only. An earlier version of Fig 08 used excess_periodic incorrectly in the decomposition; this has been corrected.

---

## 6. The SSM (Sovereign Wealth Fund Solvency Model)

`rates_model.run_ssm(p, max_N=71)` → list of year dicts

The SSM applies the historical return series uniformly across the entire taxable population (correlated-shock assumption — the worst-case floor for revenue). It tracks:

- **SRR (Short-term Refund Reserve):** the buffer guaranteeing individual refunds. Target = `srr_ratio × (cumulative net income / N)`.
- **LRR (Long-term Revenue Reserve):** the fund that eventually replaces conventional taxation. Target = `lrr_years × prevailing government expenditure`.

### 6.1 Capitalisation phase (years 1 to lrr_fill_year)

Year-by-year logic, unchanged from v7:
1. Compute marginal net revenue (the increment from extending the cohort model by one more year)
2. Add net to SRR up to target; any surplus flows to LRR
3. Once LRR reaches its floor target, the capitalisation phase ends

`p['N']` is derived from the year the LRR first fills. This is computed at `load_params()` time by the internal `_ssm_lrr_fill_year()` function using the active scenario's rotated return series.

### 6.2 Post-fill phase — 5-step priority mechanic (v8)

Each year t after `lrr_fill_year`, in strict priority order:

**Step 1 — SRR from income:**
```
srr_contrib = min(max(net_t, 0), max(0, srr_target_t − srr_bal))
srr_bal += srr_contrib;  remainder = net_t − srr_contrib
```

**Step 2 — LRR floor maintenance from remainder:**
```
lrr_contrib = min(max(remainder, 0), max(0, lrr_target_t − lrr_bal))
lrr_bal += lrr_contrib;  remainder −= lrr_contrib
```

**Step 3 — LRR covers remaining SRR deficit:**
```
srr_still_short = max(0, srr_target_t − srr_bal)
lrr_to_srr = min(lrr_bal, srr_still_short)
lrr_bal −= lrr_to_srr;  srr_bal += lrr_to_srr
→ record lrr_failure_year when lrr_bal hits 0
→ record srr_failure_year when srr_bal hits 0
```

**Step 4 — Surplus above SRR target tops up LRR toward floor:**
```
if srr_bal >= srr_target_t and remainder > 0:
    lrr_topup = min(remainder, max(0, lrr_target_t − lrr_bal))
    lrr_bal += lrr_topup;  remainder −= lrr_topup
```

**Step 5 — Labour tax relief (coverage fraction):**
```
cov_frac_t = max(0, remainder) / budget_t
```
Set to 0 if either failure condition has been reached in any prior year (including the current year). Zero in failure years drags the window average down.

The priority ordering means SRR credibility is defended before LRR maintenance, and LRR maintenance before labour relief — matching the constitutional priority structure of the WDT.

### 6.3 Failure conditions (v8)

Two distinct failure modes, always ordered LRR → SRR:

- **`lrr_failure_year`**: first t where `lrr_bal` reaches 0. The political buffer is exhausted; any further SRR deficit has no backstop. This is the primary failure signal.
- **`srr_failure_year`**: first t where `srr_bal` reaches 0. The refund guarantee itself is mechanically broken. Always follows `lrr_failure_year` if both occur.

The gap between `lrr_failure_year` and `srr_failure_year` (if both occur) is `lrr_srr_failure_gap` — how long the system limps after buffer exhaustion before the refund guarantee breaks.

At Balanced parameters, `lrr_failure_year` is None for all 73 historical start years. The failure mechanics are live but untriggered at the recommended calibration.

### 6.4 Coverage windows (v8)

For W in {5, 10, 20, 50}, `run_ssm` and `_ssm_stripped` compute:

| Key | Description |
|:---|:---|
| `ssm_cov_W` | Average `cov_frac_t` over post-fill years 1..W |
| `ssm_zero_cov_years_W` | Count of zero-coverage years in window |
| `ssm_min_lrr_bal_W` | Minimum LRR balance in window (£b) |
| `ssm_lrr_below_floor_years_W` | Years LRR balance was below its floor in window |

These are attached to each year-dict in `run_ssm` output and to each row in `run_start_year_sweep` output. All keys are prefixed `ssm_` to avoid collision with TCM keys.

### 6.5 Retired v7 metrics

The following keys from v7 no longer appear in any output dict:

| Retired key | Replaced by |
|:---|:---|
| `lrr_breach_year` | `lrr_failure_year` |
| `years_fill_to_breach` | `lrr_srr_failure_gap` |
| `max_lrr_breach` | `ssm_min_lrr_bal_W` (per window) |
| `srr_breach_year` | `srr_failure_year` |
| `srr_breach_covered` | retired — superseded by failure ordering guarantee |
| `srr_breach_magnitude` | retired |
| `lrr_bal_at_srr_breach` | retired |
| `ssm_post_fill_coverage` | `ssm_cov_W` (per window) |
| `tcm_post_fill_coverage` | `tcm_cov_W` (per window) |

Any code reading these keys will silently return None or raise KeyError. Search the codebase for these strings before upgrading dependent scripts.

---

## 7. The TCM (Taxpayer Cohort Model)

### 7.1 Bracket×tier snapshot: run_tcm()

`rates_model.run_tcm(p, N, N_fill)` → dict keyed by tier differential

The TCM disaggregates by wealth bracket and growth tier, applying persistent return differentials sourced from Fagereng et al. (2020). It uses the actual historical return series plus tier differential, rather than the uniform correlated-shock assumption of the SSM. This function produces the detailed per-bracket output table for the B.3 markdown sections. It is a snapshot at horizon N, not the source of coverage fractions (those come from `_tcm_coverage_windows`).

Per bracket-tier cell output: `label, N_pop, cell_pop, V0_m, V_at_N, TW, avg_net_gbp, wealth_burden, eff_rate, revenue_m, post_fill_net_m, post_fill_revenue_m, post_fill_net_gbp`.

### 7.2 TCM coverage windows: _tcm_coverage_windows() (v8)

`rates_model._tcm_coverage_windows(p, lrr_N, srr_N)` → dict

The TCM now runs its own **independent** year-by-year priority loop from 1 to 71, using `_tcm_marginal_net()` at each year to compute aggregate net revenue across all tier×bracket cells. It maintains completely separate SRR and LRR balance trackers from the SSM and applies the same 5-step priority mechanic. This produces:

- `tcm_cov_W` for W in {5, 10, 20, 50} — TCM coverage fractions by window
- `tcm_lrr_failure_year` — first year the TCM's own LRR balance hits 0 (or None)
- `tcm_srr_failure_year` — first year the TCM's own SRR balance hits 0 (or None)

The TCM produces higher revenue than the SSM because heterogeneous tier returns are less correlated than the SSM's uniform shock. The SSM forms the solvency/stress-test floor; the TCM forms the persistent-heterogeneity ceiling. Together they bracket the plausible revenue range.

**Key design note:** `_tcm_coverage_windows` is called by `run_start_year_sweep` for every start year and by `8_3_260812_RATES_output.main()` for the active scenario. Only `tcm_cov_W` keys are propagated into the per-row sweep dict; the auxiliary TCM keys (`tcm_lrr_failure_year` etc.) are available from the dict returned by `_tcm_coverage_windows` directly but are not stored in the sweep row.

### 7.3 Window alignment

The SSM and TCM coverage windows are deliberately independent — the SSM uses the uniform-return cohort marginal approach; the TCM uses per-tier simulations with `_tcm_marginal_net`. They share the same 5-step priority logic via `_post_fill_step`, which is a pure function called identically by both.

---

## 8. The start-year sweep

`rates_model.run_start_year_sweep(p)` → list of 73 result dicts

For each of the 73 calendar start years (1947–2019), the function:
1. Rotates the canonical returns series to that start year
2. Runs `_ssm_stripped` (optimised SSM) to get all v8 solvency and coverage metrics
3. Runs `_tcm_coverage_windows` using the SSM-derived LRR fill year
4. Merges `tcm_cov_W` keys into the row dict

Each row contains all SSM metrics (with `ssm_` prefix on coverage keys), all `tcm_cov_W` keys, and the v8 failure fields.

### 8.1 Success definition (v8)

Success = LRR fills within the 71-year modelling window AND `lrr_failure_year` is None.

The v7 definition (LRR fills AND SRR breach is covered by LRR) is retired. The v8 definition is stricter on the buffer side — any post-fill LRR exhaustion is a failure regardless of whether the SRR subsequently fails.

### 8.2 Extremal dimensions (v8)

`rates_model.report_start_year_sweep` identifies extremals across four dimensions:

| Dimension | Worst | Best |
|:---|:---|:---|
| Speed | Slowest LRR fill year | Fastest LRR fill year |
| Margin | Thinnest LRR surplus at fill | Largest LRR surplus at fill |
| Durability | Lowest 50yr SSM coverage fraction | Highest 50yr SSM coverage fraction |
| Resilience | Earliest LRR failure year | Latest/no LRR failure year |

Durability replaces the v7 "breach lag" dimension. Resilience is new. At Balanced parameters, the Resilience worst case has no data (no failures), so only the best case (the no-failure start year with the fastest fill) is populated.

---

## 9. The output infrastructure modules

### 9.1 wdt_fmt.py — formatting

All number-to-string conversion. Import and call directly; no side effects.

| Function | Use |
|:---|:---|
| `fmt_pct(v, dp=2)` | Fraction → "12.34%"; None → "—" |
| `fmt_pct1(v)` | 1dp shorthand (RATES.S sweep tables) |
| `fmt_gbp_m(v, dp=3)` | "£12.345m" |
| `fmt_gbp_b(v, dp=1)` | "£12.3b" |
| `fmt_gbp_yr(v, threshold=0.5)` | £/yr with near-zero suppression |
| `fmt_f(v, spec='.1f')` | Generic float; None → "—" |
| `dist_row(d, fmt_fn)` | "min / med / mean / max" from dist dict |
| `baseline_marker(v, bv)` | " ◄" if v ≈ bv |
| `out_dir(subdir)` | project_root / OUTPUTS / subdir (Path) |
| `ensure_dir(path)` | mkdir -p; returns path |

**Note on `fmt_gbp_yr`:** This suppresses near-zero values with `'£—'`. The original `8_3._fmt_m` did the same but produced no `'m'` suffix (the column header supplied the unit). If reusing `fmt_rev_m` elsewhere, check whether the suffix is wanted.

### 9.2 wdt_md.py — document assembly

`md_table(headers, rows, col_fmt=None, fmt_fn=None)` — the single markdown table builder. `col_fmt` is a list of `LEFT`/`RIGHT`/`CENTER` per column (default all centre). `fmt_fn` is applied to cols 1+ only; col 0 is always `str()`. No hidden default formatter.

`pct_table(row_keys, col_labels, data, row_label, fmt_fn)` — VAL.A §C-style table where col 0 is bold. Direct replacement for the old `_build_pct_table`.

`MdDoc` — accumulates lines via `.add()`, renders via `.render()`, writes via `.write(path)`. Produces `'\n'.join(lines)` with no trailing newline, byte-identical to the original scripts' output.

### 9.3 wdt_style.py — figures

`apply_style(grid=True)` — sets canonical rcParams. Call at the start of every figure function. `grid=False` for heatmaps/imshow.

`save_fig(fig, path, dpi=300)` — saves at print quality, closes the figure, prints the path.

Colour constants: `C_UNDER` (4 reds), `C_HONEST`, `C_OVER` (4 blues), `C_OVER_LIGHT` (4 light blues), `C_SSM/TCM/LRR/SURPLUS/BASELINE`, `PARAM_COLOURS`, `CYCLE_BUCKETS`.

Figure size constants: `FIG_SINGLE (9, 5.5)`, `FIG_WIDE (13, 6)`, `FIG_PAIR (14, 5.5)`, `FIG_QUAD (14, 9)`, and variants.

The era colours in `CYCLE_BUCKETS` deliberately match the SWF palette (`C_SSM/TCM/LRR/BASELINE`). If you change one, consider whether the other should change too.

### 9.4 wdt_analytics.py — analytical metrics and sweep runner

Requires explicit initialisation: call `wdt_analytics.init(p)` in `main()` before using any constant.

**Critical:** import as `import wdt_analytics as _A` and access constants as `_A.CANON_TAU0` etc. Do NOT use `from wdt_analytics import CANON_TAU0`. Python's `from X import Y` captures the value at import time (which is `None`); `init()` updating the module global does not update the local binding. This is a known Python gotcha for modules with deferred initialisation. The exception is `HEADLINE_WINDOW`, which is a plain integer set at module level before `init()` is called, so it is safe to import directly.

**`HEADLINE_WINDOW`** (v8) — module-level integer constant (default 10). Controls which coverage window is used as the headline in table column headers, chart axis labels, and `run_param_sweep` progress output. The `ssm_cov` and `tcm_cov` aliases in the `summarise()` return dict always point at `ssm_cov_{HEADLINE_WINDOW}` and `tcm_cov_{HEADLINE_WINDOW}`. Change this single integer to switch the headline everywhere without touching any other code.

Key functions:
- `make_p(**kwargs)` — build a minimal 7-key dict for run_sim_p (uses CANON_* defaults)
- `run_sim_p(p, alpha, g, N)` — LRU-cached wrapper around run_sim (cache key = all 9 numeric inputs; cache clears on re-init)
- `c1(p, alpha, g, N)` — C.1 metric as fraction
- `c1_matrix(p, alpha_vals, g_vals)` — C.1 matrix in pp
- `n_crossing(p, alpha, g, N_sweep)` — interpolated crossing N (np.nan if not found)
- `tolerant_zone_bounds(p, g, threshold)` — (lo, hi) alpha
- `understater_plateau(p, alpha, g_range)` — max C.1 in pp over plateau zone
- `run_param_sweep(p_base, param_name, values, label)` — full 73-start-year sweep per value
- `success(r)` — v8 success predicate: LRR fills AND lrr_failure_year is None
- `summarise(sweep_results)` — per-window coverage dists plus failure dists (v8)

**`summarise()` return dict (v8):**

| Key | Description |
|:---|:---|
| `n_total` | Number of start years |
| `success_rate` | % successful under v8 definition |
| `n_lrr_failure` | Count of start years where lrr_failure_year is not None |
| `ssm_cov` | Alias → `ssm_cov_{HEADLINE_WINDOW}` dist |
| `tcm_cov` | Alias → `tcm_cov_{HEADLINE_WINDOW}` dist |
| `ssm_cov_5/10/20/50` | SSM coverage fraction dist per window |
| `tcm_cov_5/10/20/50` | TCM coverage fraction dist per window |
| `lrr_failure` | LRR failure year dist |
| `srr_failure` | SRR failure year dist |
| `lrr_fill` | LRR fill year dist |
| `srr_fill` | SRR fill year dist |
| `lrr_surplus` | LRR surplus at fill dist |
| `worst_case_2006` | Raw sweep row for calendar year 2006 (or None) |

The `ssm_cov` and `tcm_cov` aliases mean existing 16_6 and 16_7 call sites reading `s['ssm_cov']` and `s['tcm_cov']` continue to work unchanged as the headline window changes.

---

## 10. The output scripts

| Script | Produces | Description |
|:---|:---|:---|
| `5_3` | VAL_AppC_Full_Tables.md | Full VAL.A §C tables (C.1–C.12) |
| `5_4` | VAL_Worked_Examples_Figures.md | Worked examples §J–§N (VAL.B) |
| `5_6` | 10 VAL PNGs | All VAL.A figures (Figs 01–10) |
| `8_3` | RATES markdown + 9 PNGs | Full RATES output report and figures |
| `16_2` | 12 VAL_S PNGs | §2 rate function parameter sweeps |
| `16_3` | 6 VAL_S PNGs | §3 horizon and wealth-level sweeps |
| `16_4` | 3 VAL_S PNGs | §4 interaction surfaces |
| `16_5` | VAL_S_Appendix_Tables.md | Full VAL.S appendix tables (B.1–B.9) |
| `16_6` | RATES_S_Appendix_Tables.md | RATES.S parameter sweep tables (v8) |
| `16_7` | 10 RATES_S PNGs | RATES.S sensitivity sweep figures (v8) |

All scripts follow the same pattern:
```python
def main():
    p = load_params()
    init(p)           # wdt_analytics only; other modules need no init
    ensure_dir(_OUT)
    # ... domain logic ...
```

Output directories: `OUTPUTS/VAL`, `OUTPUTS/VAL_S`, `OUTPUTS/RATES`, `OUTPUTS/RATES_S`.

### 10.1 8_3 — RATES output report (v8)

The `write_output_md` signature changed in v8. The old `tcm_pf_cov`, `ssm_pf_cov`, `pf_avg_budget`, `pf_years`, `total_post_fill_rev` arguments are retired. The single new argument is `tcm_win` — the dict returned by `_tcm_coverage_windows(p, ssm_lrr_N, ssm_srr_N)`.

Report sections updated in v8:
- **B.2 SSM Results** — failure years (`lrr_failure_year`, `srr_failure_year`, `lrr_srr_failure_gap`) replace breach metrics; coverage window table replaces single coverage ratio
- **B.3.9 TCM coverage** — window table with four rows replaces single coverage ratio; `tcm_lrr_failure_year` and `tcm_srr_failure_year` reported
- **B.4.1 Extremals** — four dimensions (Speed, Margin, Durability, Resilience) replace three
- **B.4.2 Full sweep table** — 13 columns including `ssm_cov_5/10/20/50`, `tcm_cov_10/50`, failure years
- **B.5 Statistical pass** — v8 success definition; failure year distributions; per-window coverage distributions for all 8 window/model combinations

The nine figures are unchanged in structure. Figures 01, 05, and 07 now use `ssm_cov_10` / `tcm_cov_10` keys in place of the retired single-ratio keys.

### 10.2 16_6 — RATES.S tables (v8)

Summary table gains two new columns: `SSMcov50 (min/med)` for long-run trajectory, and `LRR fail n` for failure count. Worst-case 2006 table shows `LRR failure yr` in place of the retired `SRR breach covered`. Metrics glossary in B.1.3 updated throughout. Model version string updated to v8. Column headers embed `HEADLINE_WINDOW` so they update automatically when the constant changes.

### 10.3 16_7 — RATES.S charts (v8)

Panel [0,0] labels in `_four_panel` and `_four_panel_swf` now read `SSM {HW}yr coverage` and `TCM {HW}yr coverage` where HW = `HEADLINE_WINDOW`. The `_relative_sensitivity` y-axis label similarly updates. Two new figures added:

**`sweep_fig_09_coverage_fan.png`** — all four rate parameters on one normalised-x-axis chart. Two shaded bands per parameter: outer from SSM 5yr to TCM 50yr; inner from SSM HW to TCM HW. Shows the full temporal profile of the coverage promise across the rate-parameter space in a single view.

**`sweep_fig_10_failure_years.png`** — 1×2 panel, one per SWF sizing parameter (`srr_ratio`, `lrr_years`). Y-axis = LRR failure year (median, min, max across start years that produce a failure). At Balanced parameters renders with "no failures at baseline" annotations. Populates as SWF parameters are stressed. This is the figure that exercises the v8 failure mechanics and answers how much SWF slack exists before the post-fill buffer exhausts.

---

## 11. Known issues and conventions

### 11.1 Active conventions

**The FIGURE_REGISTRY in 16_5** is a manually maintained index of all 21 VAL.S figures with their axis descriptions written as strings. It must be kept in sync with the figure functions manually. It is built by `_build_figure_registry()` which is called in `main()` after `init(p)` — this is necessary because the registry's f-strings embed CANON_* values.

**The generate_charts flag in 8_3** is the only script with an opt-in charts guard: `p.get('generate_charts', False)` checked from the TOML `[output]` section. All other scripts always produce figures. Set `generate_charts = true` in `[output]` to enable RATES chart generation.

**N is computed, not configured.** `p['N']` is derived from the SSM at load time. After changing rate parameters or SWF sizing, re-run everything — the canonical N may have shifted, and all VAL.S sweep figures use `CANON_N` from the sweep dict, which is also derived from N.

**The beta mechanism is not calibrated.** The §C.3 tables use beta as a sensitivity parameter. The formula is additive (`g_eff = g + β ln(α)`), not multiplicative as incorrectly stated in VAL.A §B.3. Do not use the VAL.A §B.3 formula for any calculations.

**DPI is 300 everywhere** after the refactor. The pre-refactor VAL_S scripts produced 150-dpi figures; RATES produced 300-dpi figures. All are now 300. Reference checksums for pre-refactor VAL_S figures will not match.

**All monetary values are in £m** throughout `wdt_core` and the simulation engine. `rates_model` uses £b for aggregate SWF quantities (`× b['N'] / 1000.0`). `wdt_fmt` functions are named accordingly (`fmt_gbp_m`, `fmt_gbp_b`).

**Coverage key collision guard.** SSM and TCM coverage keys use distinct prefixes (`ssm_cov_W`, `tcm_cov_W`). The auxiliary SSM keys (`ssm_zero_cov_years_W`, `ssm_min_lrr_bal_W`, `ssm_lrr_below_floor_years_W`) use the same prefix. Never call `_compute_coverage_windows` without an explicit `prefix=` argument, and never merge SSM and TCM dicts directly into the same namespace without checking for collisions first.

**`rates_model.py` docstring error.** The `rates_model.py` module-level docstring correctly states `(τ_m - τ_0)/τ_0` but the inline docstring for `rates_model.validate_params` writes `(1-τ_0)/τ_0`. The implementation in `wdt_core.tau()` is correct. The inline docstring error is a pre-existing issue.

### 11.2 v8 changelog

The following changes were made in the v8 update (this session). `wdt_core.py` was not modified.

**`rates_model.py`** — complete rewrite of the SSM post-fill block and TCM. Key changes:

- `_post_fill_step()` — new pure function implementing the 5-step priority mechanic. Called identically by both SSM and TCM, ensuring they use exactly the same logic.
- `run_ssm()` — post-fill block replaced. Tracks `lrr_failure_year`, `srr_failure_year`, `post_fill_cov_fracs`, `post_fill_lrr_bals`, `post_fill_lrr_targets`. Calls `_compute_coverage_windows` to produce four window metrics per run.
- `_compute_coverage_windows()` — new function. All output keys fully prefixed (`ssm_cov_W`, `ssm_zero_cov_years_W`, etc.) to prevent collision when SSM and TCM outputs are merged into the same row dict.
- `_ssm_stripped()` — same post-fill logic as `run_ssm` in optimised form for the sweep.
- `_tcm_marginal_net()` — new function. Computes aggregate marginal TCM revenue at year N by differencing cumulative simulations at N and N-1.
- `_tcm_coverage_windows()` — new function. Runs a completely independent year-by-year priority loop using `_tcm_marginal_net`, with its own SRR/LRR trackers, producing `tcm_cov_W` and `tcm_lrr/srr_failure_year`.
- `run_tcm()` — retained for the bracket×tier snapshot table (B.3 report sections). No longer the source of coverage fractions.
- `run_start_year_sweep()` — now calls `_tcm_coverage_windows` per start year, merging `tcm_cov_W` keys into each row dict.
- `report_start_year_sweep()` — four extremal dimensions (Speed, Margin, Durability, Resilience). Sweep table columns updated to v8 keys.
- `compute_statistics()` — v8 success definition; failure year distributions; per-window coverage distributions.
- `report_statistics()` — updated for v8 metric names.
- `run_scenario_profiles()` — extremal dimension keys updated.

**`wdt_analytics.py`** — three targeted changes:

- `HEADLINE_WINDOW = 10` — new module-level constant. Controls the headline coverage window throughout all downstream output.
- `success(r)` — v8 definition: `lrr_fill_year is not None AND lrr_failure_year is None`. Retired `srr_breach_year` / `srr_breach_covered` reads.
- `summarise(sweep_results)` — returns a superset of the old structure. `ssm_cov` and `tcm_cov` are headline aliases; `ssm_cov_5/10/20/50` and `tcm_cov_5/10/20/50` are the full per-window dists; `lrr_failure` and `srr_failure` are new dist fields; `n_lrr_failure` is a direct count. Existing call sites reading `s['ssm_cov']` and `s['tcm_cov']` continue to work unchanged.
- `run_param_sweep` progress line — now prints `SSMcov{HW}`, `TCMcov{HW}`, and `LRRfail=N/73`.

**`8_3_260812_RATES_output.py`** — reporting updated throughout. `write_output_md` signature: old `tcm_pf_cov/ssm_pf_cov/pf_avg_budget/pf_years/total_post_fill_rev` arguments replaced by single `tcm_win` dict. B.2, B.3.9, B.4.1, B.4.2, B.5 all rewritten for v8 metrics. Figures 01, 05, 07 use `ssm_cov_10`/`tcm_cov_10` keys.

**`16_6_260813_RATES_S_tables.py`** — summary table gains `SSMcov50` and `LRR fail n` columns. Worst-case table shows `LRR failure yr` (not `SRR breach covered`). Metrics glossary rewritten. Model version string updated to v8. `HEADLINE_WINDOW` imported and embedded in column headers.

**`16_7_260813_RATES_S_charts.py`** — panel [0,0] axis titles updated for `HEADLINE_WINDOW`. `_relative_sensitivity` y-axis label updated. Two new figures: `sweep_fig_09_coverage_fan.png` and `sweep_fig_10_failure_years.png`. Figure count increases from 8 to 10.

---

## 12. Extending the model

### Adding a new output figure

1. Add a figure function to the appropriate output script following the pattern of existing functions
2. Call `apply_style()` or `apply_style_nogrid()` at the top
3. Use colour constants from `wdt_style` rather than inline hex strings
4. End with `save_fig(fig, _OUT / 'filename.png')`
5. If the figure belongs to the VAL.S suite, add an entry to `FIGURE_REGISTRY` in `_build_figure_registry()` in `16_5`

### Adding a new analytical metric

1. Add the function to `wdt_analytics.py` with a test in `test_wdt_analytics.py`
2. Import it in the relevant output script

### Adding a new TOML parameter

1. Add the key to the TOML with a comment
2. Add the parse line in `wdt_core.load_params()`
3. If it affects the sweep, add it to `p['sweep']` and expose it via `wdt_analytics.init()`
4. If it affects N (rate or SWF parameters), re-run all scripts and update `snapshot_N`

### Changing the headline coverage window

Change `HEADLINE_WINDOW` in `wdt_analytics.py`. This updates: `summarise()` aliases, `run_param_sweep` progress output, `16_6` column headers, `16_7` panel [0,0] axis titles and legend labels, `_relative_sensitivity` y-axis label. The TOML does not need to change. The underlying per-window data in all four windows is always computed regardless of which window is the headline.

### Changing a canonical parameter value

1. Update the TOML
2. Run `load_params()` and check the new `p['N']`
3. If N changed, update `snapshot_N` in the TOML, and note that all sweep figures will shift
4. Regenerate all outputs and check the FIGURE_REGISTRY parameter strings in `16_5` are still accurate

### Running the full pipeline

```
python 5_3_2608012_VAL_generate_appc_full.py
python 5_4_260807_VAL_generate_worked_examples.py
python 5_6_260809a_VAL_generate_figures.py
python 8_3_260812_RATES_output.py
python 16_2_260812b_VAL_S_rate_sweeps.py
python 16_3_260812a_VAL_S_horizon_sweeps.py
python 16_4_260812b_VAL_S_interactions.py
python 16_5_260812b_VAL_S_assemble.py
python 16_6_260813_RATES_S_tables.py
python 16_7_260813_RATES_S_charts.py
```

`run_all.bat` automates this on Windows. Scripts are independent and can be run individually; there are no inter-script dependencies.

### Testing the infrastructure modules

```
python test_wdt_fmt.py
python test_wdt_md.py
python test_wdt_style.py
python test_wdt_analytics.py
```

480 tests in total. These run quickly (under 30 seconds) except `test_wdt_analytics.py` which runs the simulation engine and takes a few seconds. Run these after any change to the four infrastructure modules before regenerating outputs.

**Note:** `test_wdt_analytics.py` tests for `success()` and `summarise()` will need updating for v8 — any test asserting on `srr_breach_covered` or `ssm_post_fill_coverage` will fail. Update those tests to use `lrr_failure_year` and `ssm_cov_{W}` keys respectively.
