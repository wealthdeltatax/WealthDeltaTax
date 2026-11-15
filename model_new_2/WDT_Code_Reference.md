# WDT Code Reference: TOML, wdt_core, valgen_core, rates_core

How the code works and what it assumes. No results.

## 1. Layering

```
WDT_Params.toml  ->  wdt_core.py  ->  {valgen,rates}_core.py  ->  JSON  ->  tables / charts
```

- TOML holds every model input. `wdt_core` loads it and holds everything more than one core needs. Cores simulate and write JSON. Presentation only reads JSON.
- `valgen_core` imports `wdt_core`, `wdt_kernel`, `wdt_jst` and `wdt_fmt`. `rates_core` imports `wdt_core`, `wdt_kernel`, `wdt_jst` and `wdt_fmt`. Cores do not import each other, and presentation never imports a core.
- `wdt_kernel` is the shared route-settlement kernel (D12). `wdt_jst` loads the JST history and builds loop windows and the real basis inputs.
- Outputs: `OUTPUTS/VAL/valgen_data.json` and `OUTPUTS/RATES/rates_data.json`.
- Money is £m in `wdt_core` and `valgen`. `rates_core` works in units of GDP per capita at window start (y0), with revenue as a share of GDP.

## 2. WDT_Params.toml

The single source of truth. Parsed in `wdt_core.load_params` (full) or `load_rates_params` (only `[rates]`, `[rules]`, `[meta]`).

| Section | Contents |
|:---|:---|
| `[meta]`, `[output]` | Version, scenario label, chart flag. |
| Retired (D11) | `[rate]`, `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]`, `[[brackets]]` are gone. The rate design is `[rates.defaults]` / `[rates.scenarios.*]` (VAL picks one with `[val_gen] rate_scenario`); the fund is sized by `ms`, `ml` in `[rates.defaults]`; return tiers are `[rates.cohorts.*]`. |
| `[rho]` | State-side discount rate: base and sweep (real). |
| `[route_b]`, `[income]`, `[verification]`, `[archetypes.*]` | Route B payment mode (sale, lien, income), deferral rate, external income caps and ratios, lambda_C / lambda_D, the five route-mix archetypes. Read by both cores. |
| `[val]` | Single-life VAL: `V0_m`, `rho`, `N_demo` (=30, the holding period `N_val`), and figure grids. |
| `[val_gen]` | Generational model: `T`, `G`, route shares, consumption, voluntary-reset sensitivity (`reset_sens`), lambda grids, strategy grids, test tolerances, hec/dmg/uos settings. Required: `rate_scenario` and `basis` (`jst` derives `g_real` and `index_rate` from JST; `manual` needs both as numbers). |
| `[val_gen.hlc]` | HLC calibration (D1d): `average_stock_rate` (net payers), `top_stock_rate` (top 0.1%), source scenario, stamp. `placeholder = true` makes valgen skip the HLC pair. Regenerate with `test/print_hlc_calibration.py --write` after a RATES run. valgen reads no RATES output. |
| `[sweep]` | Shared analytical grids. `g_offsets` (pp around `g_real`) become `g_vals = g_real + offsets` in `with_val_basis`. The `*_canon`, `rates_*_sweep` and `wfr_*` keys are retired. |
| `[synthetic_scenario]` | Sine-wave growth stress test. |
| `[names.val.*]` | Acronym register: kind, name, legacy id. |
| `[rates]` | Everything for `rates_core` (below). |
| `[rules]` | Named rule sets `base` and `candidate`, keyed `c_cap/verify_down/dauc`. |

### `[rates]` subsections
- `defaults`: baseline config. Each `[rates.scenarios.NAME]` overrides only the keys it names, and unknown keys raise at load.
- `levy`, `levy_calibration`: the CORP levy and its calibration.
- `dist`, `dist.advani`: wealth distribution constants.
- `cohorts.*`: return heterogeneity.
- `schedules.*`: rate ladders.
- `replacement` (with `legs.*` and `income_by_wealth`): tax-replacement inputs.
- `closure`, `representativeness`, `run`, `figures`, `flags`, `eras`, `extras`.

### TOML conventions
- An optional setting is "off" by omission. TOML has no null.
- Placeholders and judgments are flagged in comments. Examples: `employer_share`, `income_by_wealth`, `f_inc`, `brg_tol`, `hec_phi`, taxpayer-count curves.
- **One rate design.** The baseline is the gain ladder (D2). Logistic schedules survive only as comparison scenarios (`logistic_ref` and others).
- **Real basis only.** There is no nominal `g`. `p['g_real']` and `p['index_rate']` exist only after `with_val_basis`; `load_params` does not set them.

## 3. wdt_core.py

Shared base layer. Its simulation mechanics are single-life Route C.

### Rate functions
- `tau(W, p)` is the scalar rate. `rate_vec(x, rp)` and `tau_vec` are the vectorised twins. Rate is 0 below `W_min`.
- Three schedules:
  - `logistic`: `tau_m / (1 + ((tau_m - tau_0)/tau_0) e^{-k(W-W_min)})`.
  - `logistic_ln`: same, in ln(W/W_min), with k dimensionless.
  - `ladder`: statutory anchors `[(W, tau)]`, linear in ln W, flat beyond the ends.
- `ladder_to_tau` converts target effective rates to the statutory rate on the delta. The target applies to an accumulator earning `r_ref` and consuming `c_ref`.
  - stock: `s/(r-c)`.
  - gain: `G r/(r-c)`.
  - delta: unchanged.
- `fit_k` is a closed-form k putting a logistic through a ladder's top anchor.
- `rate_params(p)` builds the dict `tau` reads. `rate_spec_from_scenario` and `with_rate_scenario` let VAL take its rate design from a `[rates.scenarios]` entry (one source for RATES and VAL).
- `with_val_basis` puts VAL on the real basis: `basis = "jst"` derives `g_real` (geometric-mean real capital return) and `index_rate` (real GDP/head growth) from the JST history of `[rates].uk_iso` (`jst_basis`); `"manual"` takes both from `[val_gen]`. It sets `p['g_real']`, `p['index_rate']`, `p['val_basis']` and `p['sweep']['g_vals']`.

### Rule sets
`parse_rule("c_cap/verify_down/dauc")`, with defaults `units/allow/off`.
- `c_cap`: `units` or `units_and_value`. The value cap stops a Route C refund exceeding the value paid.
- `verify_down`: `allow` or `reset`. `reset` means correcting your own overstatement is a basis reset with no refund.
- `dauc`: `off` or `on`. `on` applies the corrective auction to Route D too.

### Route C simulation (single life)
- `simulate(V0, g_series, alpha, p)` runs the holding years. Declared wealth is `W = f * alpha * V`, where `f` is the family's unit fraction.
  - Tax `L = tau(W) * delta` is paid in kind as fraction `q = L/W`, so `f <- f(1-q)`.
  - Refunds are capped by cumulative tax paid (`-cum`).
- `simulate_sell` is the sale year. `alpha` drops out at liquidation (`W_sell = f_N * V_sell`), and a prior overstated basis can produce a negative delta and a refund.
- `settle_tw` / `settle_tw_flows` iterate the post-sale tax/refund oscillation to convergence.
- Convenience runners:
  - `run_sim` (constant g) and `run_sim_hist` (historical series).
  - `run_pair`, `run_pair_rhos`, `breakeven_rho`.
  - `decompose_tw_advantage` (C.11) and `npv_tax_advantage` (C.12).
  - The declared-path variants.
- **Primary metrics:** `TW_settled` and `Net_settled`. Bare `TW` is legacy.
- **Comparison metrics:** all expressed as fractions of the honest `TW_settled(1)`, with the sign convention `+` = pays more tax, except `tw_gap` where `+` = retains more.
  - `net_pct`, `tw_gap`, `tw_cost`, and `pv_pct`.
  - `pv_pct` values each payment at the true value surrendered (`L/alpha` in the holding period, cash at sale).
- `g_eff = g + beta ln(alpha)` is additive. VAL.A §B.3 states it wrongly.
- **N is never implicit.** `_require_N` raises if `N` is missing. `N_val` (30) is the taxpayer holding period. The SSM fill year `N_fill` and the alias `p['N']` are retired (D11); the fund fills inside each RATES window (`fill_year` in the JSON).

### Retired legacy and what stays
The SSM (`_ssm_marginals`, `_ssm_lrr_fill_year`) and the readers of `[swf]`, `[budget]`, `[returns]`, `[tcm]`, `[[tiers]]`, `[[brackets]]` are deleted, so `load_params` is instant. Kept until the D9 bridge is signed off (then moved to `wdt_legacy_v7.py`): the single-life Route C block (`simulate`, `run_pair`, `run_sim_hist`, `settle_tw_flows` and relatives, `run_sim`, `g_eff`, `synthetic_returns`). `run_sim_hist` takes its series as `p['returns']`; valgen's bridge passes a JST real series explicitly.

### wdt_kernel (D12)
The shared route-settlement kernel. Routes A, B, C, D plus the verified tranche Cv. Route B pays by `sale`, `lien` (deferred balance at `r_def`, settled at death) or `income` (external income up to the cap, shortfall sold). Route C caps are `units` or `units_and_value`. Refund is the ratio mirror (D5). lambda_C and lambda_D are independent; death verifies C; a voluntary reset is an action, not a rule. `step_year` and `step_death` operate on a `Book`; `step_death` has no line mask, so `rates_core` cuts sub-books (`_sub_book`, `_write_back`). Unit tests: `kernel_test.py`; parity with both cores: `bridge_test.py`.

### wdt_jst
`load_jst`, `real_return_series`, `real_basis_inputs`, and `loop_windows` (windows wrap within a country's series; a window that repeats years is flagged `repeat`, one that crosses the seam is not `contiguous`; every result is reported for the full loop and for contiguous windows).

### Tax replacement (RATES T17 to T22)
- Relief retires the taxes in `rp['retire']` in order: CGT, IHT, then corporation tax.
- The leftover is split by `employer_share`:
  - One common tax-free threshold X for income tax and employee NI.
  - A separate threshold X_e for employer NI.
- Liability grows from zero at the threshold. The higher-rate band moves up by the same amount. Everyone is counted, WDT payers included.
- Taxpayer-count curves `n_above` are placeholders. `calibrated_legs` rescales each leg's count curve (`count_scale`) so the leg raises its stated share of GDP.
- Cost of a threshold is the integral of the count curve times the rate. `solve_threshold` bisects for X, with a cap `x_cap_gbp`.
- Functions: `threshold_outcomes`, `person_saving`, `threshold_beneficiaries`.
- `band_net_position` gives per-adult net position by launch-wealth band.
  - It is read over the post-fill horizon, for windows where the fund fills.
  - The income profile is only a shape. It is rescaled so total saving equals what the solver says the relief buys.
  - It also produces the budget closure (sources vs uses).

### Other helpers
- JSON I/O: `json_safe`, `save_json`, `load_json`, `table_to_frame`.
- Reading stored scenarios: `scenario_headline`, `levy_headline`, `scenario_medians`, `of_ref`.
- `_parse_rates` validates the whole `[rates]` tree, including figure/scenario cross-references.

## 4. valgen_core.py

A family line on a double-entry ledger. It tests whether any declaration strategy beats honesty. Build steps P1 to P5 are nested, and each reduces to the previous at its off-switches.

### Ledger and checks
- Accounts hold true value. Every `post()` is a pure move, so the ledger sums to zero.
- Invariants checked each year:
  - `family_equity == f*V`.
  - `f + s + sold == 1`.
  - `0 <= u_out <= s`.
  - Conservation of family plus state value.
- Bridges to legacy (`wdt_core`) tolerance 1e-9.
- Plan fixtures (regression values) apply only at baseline parameters, and are skipped otherwise.

### Steps
- **P1 `run_life`:** one life, one route, sale at N. Reproduces the legacy results.
- **P2 / P2b `run_family`:** Route C only over horizon T, with a death every G years.
  - **Heir rule `delta` (default):** the heir's receipt is taxed as a delta from zero, in kind at `tau(W_heir)`.
  - **Heir rule `fresh_entrant`:** no tax on the receipt, and the basis equals the declared value of the stake.
  - **Envelope unit `real` (default):** the cap is the true value paid.
  - **Envelope unit `credited`:** the cap is the credited liability.
  - **Consumption (D16/D17):** a share of units is sold each year.
  - **Indexation:** `W_min` and k are indexed at `index_rate`.
  - **Refund rule `legacy`:** refund is `tau * delta / W_new`, capped by the envelope.
  - **Refund rule `ratio_mirror`:** refund is `tau(1 - W_new/W_prev)` of holdings, capped by units this individual paid.
- **P3 `run_family3` (and `run_batch`):** a ledger wrapper (`_LedgerHook`) around `wdt_kernel`; the kernel does the settlement. Four routes with shares of V0 (A/B/C/D).
  - **A/B:** professionally valued, so `alpha = 1`. They are paid in cash-equivalent units, with a pooled real-value refund cap.
  - **C:** self-declared fungible. Paid in kind at the declared price. Refund is in units, capped by units paid (and by value under `units_and_value`).
  - **D:** self-declared non-fungible. Liability accrues, and is settled in units at the true (auction) price at a reset or death. Under a waived death auction, settlement is in kind at the declared price.
  - **Assessment:** one assessment on total declared W, with the `ratio_mirror` refund `tau|delta| W_new/W_prev`. Tax or refund is then allocated across routes by positive-delta or negative-delta shares.
  - **Route D reset:** `reset_interval` and `death_waiver` are retired (they raise `TypeError`). A reset is a voluntary action in the strategy space (`reset_sens` cycles); death verifies Routes C and D with certainty.
  - **Family terminal wealth:** the sum of true route holdings at T, after settling outstanding Route D at the true price.
- **P4 verification hazard:** `lambda_C` and `lambda_D` are independent. Each year a share `lambda_C` of unverified Route C units (family and state) moves to a verified tranche `Cv`, declared at true value. This is an expected-value flow.
  - Verified share is `1-(1-lambda)^t`.
  - Lambda is a framing device. It is not calibrated, since the WDT changes the listing decision itself.
  - The corrective auction on D is an expected-value share `vD = 1-(1-lambda)^t` declared at the true price.
- **P5 strategy search (`_strategies`, `_p5_search`):** a library of declaration strategies. Honest is excluded.
  - Types: constant, first-gen-only, late deviation, correct-before-death, pre-reset deviation, reset gaming.
  - Targets: C, D or CD.
  - alpha is a number or a function of context (`gen`, `yrs_to_death`, `yrs_to_reset`).
  - The best response is a lower bound over the library.

### Verdicts (thresholds are placeholders in the TOML)
| Test | Meaning |
|:---|:---|
| BRG | Best-response gain at most `brg_tol`. |
| HSC | Honest family's cost from the rule in a one-year market fall at most `hsc_tol`. |
| SPT | Among gaining strategies, state PV within `state_tol`, at each rho in `[rho]` sweep (a sensitivity). |
| SST | Among gaining strategies, state terminal stake within `state_tol`. Discount-free: the PRIMARY state test (D1c). |

### Other analyses
- **Added by the refactor:** `_lam_D` couples lambda_D to lambda_C unless `[verification] lambda_D > 0`; lambda_C x lambda_D grid (`_p3_lambda_grid`); V0 sweep over the RATES bands (`_v0_sweep`); Route B archetypes and the breakeven deferral spread (`p6`); JST replay (`_p7_replay`, full loop and contiguous); rho sensitivity; HLC pair from `[val_gen.hlc]` (`_hlc_pair`); the legacy bridge now runs on a JST real series (`_bridge_series`).
- **Surfaces and grids:** growth by lambda surface (`_p5_growth_surface`), dominance grid DOMG (`_p5_dmg`), headline contrast by alpha (`_p5_headline`).
- **UOS** (`_p5_direction`): under- vs over-statement across Route C share (A absorbs the difference).
- **HEC** (`_p5_hec`): honest valuation error on C and D (lognormal AR(1) in logs, unbiased).
- **Conventional baseline:** a flat tax on declared value, calibrated to the same honest terminal wealth. No delta, refund or auction.
- **No-tax ceiling:** no strategy can leave the family richer than a no-tax run. Every best response is checked against it.
- **LIFE results:** single-life grids and worked examples via `run_life`. Route D worked examples L and M run through the family engine.

### Assumptions
- **Value path:** all routes grow at one g (route-specific g is not built).
- **Heir:** no pre-existing heir wealth. No gifts, no failed assets.
- **Objective:** terminal true net worth (consumption is a diagnostic only).
- **Honesty:** `alpha = 1` means no valuation bias. Honest bias is not modelled. A persistent discount is a constant `alpha_C < 1`.
- **Verification:** a Poisson-like hazard, independent of growth.

## 5. rates_core.py

Replays each country-history window (JST data, many countries) onto today's UK-calibrated wealth distribution and rate schedule. It tests robustness to macro history. It is not a forecast. It writes one JSON.

### Layers
- **L0 data:**
  - JST panels per country, with real returns deflated by country CPI.
  - Ratios to GDP so levels are unit-safe.
  - Suspect years flagged (diagnostic only unless `exclude_flagged`).
- **L1 distribution:** `advani`, `adjusted` or `survey`.
  - Survey body plus a fitted tail (ln w(q) quadratic in ln q) plus a named Rich List tier.
  - Cells ordered poorest to richest.
  - `body_split` can subdivide deciles using a monotone PCHIP Lorenz interpolation.
  - Non-monotone cell means are repaired by pooling adjacent violators.
- **L2 scenario:**
  - `calibrate` expresses wealth and rate parameters in y0 units.
  - `build_scenario` builds one window: data year `start+t-1` drives sim year t.
  - `wmin_pct`, `wmin_house_ratio`, `anchor_from` and ladders are resolved here.
  - `cohort_spec` demeans differentials by launch-wealth weights, so the wealth-weighted mean return stays at JST r. Cohorts move return between holders and add none.
- **L3 engine (`run_lines`, `run_cohorts`):** vectorised honest declaration (`alpha = 1`) across lines, settled through `wdt_kernel`. `_route_plan` gives each cell's A/B/C/D shares (archetype mixture by launch wealth, a blend, or one archetype), the Route B mode, `r_def`, income cap and income ratio; `_verification` gives lambda_C, lambda_D and death verification (pass-through: honest lines, so they bite only with `verify_down = reset` in price-fall years). Both are built once per scenario. A line is a bracket by tier by death-phase, weighted by population share. The fund counts settled cash only: a Route B lien and an accrued Route D liability are receivables (`lien_out`, `accr_d_out`). Yearly mechanics:
  1. Asset grows.
  2. Consumption `f *= 1-c`.
  3. Declared `W = fV`.
  4. Rate `tau(W/idx_t)`.
  5. Tax in kind if delta > 0. Refund in units if delta < 0, floored at units paid, and also at value paid under `units_and_value`.
  6. State units accumulate.
  7. Deaths at `ph, ph+G, ...`: the cap is cleared and the heir is taxed on the receipt as a delta from zero. The `fresh` rule is an ablation only.
- **L4 fund (`run_fund`):** the SRR/LRR rules.
  - **Trailing mean A_t:** `A_t` is the trailing mean of `max(net,0)`.
  - **Targets:** SRR is `ms*A_t`. Total is `(ms+ml)*A_t`.
  - **Fill:** fill occurs when `S_pre >= (ms+ml)A_t`.
  - **Committed relief:** after fill, committed relief is the trailing mean of surplus after upkeep, over `ml` years.
  - **Relief paid:** `R = min(R*, S_pre - SRR)`.
  - **Failure events:** unmet, ring, insolvent.
  - **Coverage:** coverage is relief over the `horizon` years after fill, over expenditure.
  - **Reference coverage:** `cov_ref` uses relief/GDP over that same window against a fixed reference expenditure/GDP (UK 2019 by default).
  - **Censoring:** windows that never fill, or fill too late, are censored. They are reported, not dropped.
  - **cov_ref_uncond:** counts censored windows as zero.
- **L5 sweep:** every JST loop window (`wdt_jst.loop_windows`, T = 100; wrap flagged, `contiguous` reported separately) for each index mode, with stride and country filters. Bootstrap block length is `block_years` = 100.
- **L6 output:** each named scenario becomes a JSON block. `validate` checks window counts sum across country, era, and slices.

### CORP levy
- It enters the fund and net receipts. It does not enter individual stock or gain rates, nor revenue-by-tier shares. It is paid by companies, not by the engine's adults.
- Two tiers:
  - `tau` on `f_inc` (unattributed).
  - `tau0` on `f_attr` (attributed non-native).
- Levy as share of GDP: `(tau f_inc + tau0 f_attr) * mc_gdp * max(0, nominal equity return) / (1 + nominal GDP growth)`. No refund in loss years.
- **Calibration:** the entry rate (`tau0` or a scale) is solved in closed form so the **median levy over all valid windows (nominal base)** equals the retired tax's GDP share.
  - It is floored at 0 and flagged `infeasible` if the unattributed tier alone overshoots.
  - The same rate is then applied to the real base, which is the conservative case.
  - Per scenario, `levy_cal_base` picks the base the rate is solved on.
- Every window runs the fund three times, once per levy case: `nominal`, `real` and `none`. Fund-dependent columns are stored as `<col>__<case>`.
- **Data requirement:** windows need nominal `eq_capgain` and GDP in every year. Otherwise the window is dropped from every scenario carrying the levy.

### Window outputs
- **Burden:** stock rate = net WDT / wealth. Gain rate = net WDT / `r*W_{t-1}`. Both are ratios of sums, so they are wealth-weighted. Computed for all, for payers, and for top-q cells. Heir receipts included.
- **Drift:** `drift = (wealth/GDP at end) / (launch)`. The stable band is `drift_band`.
- **Closure:** `base_multiple_needed = replaced_ref / net_gdp_mean`. Also `nonwdt_req_*`.
- **Zucman check:** annual stock rate of billionaire cells against a floor. A check, not a target.
- **Revenue by tier:** `revshare_band{i}` and `bands`.
- **Post-fill horizon columns** (`*_h`): years fill+1 to fill+horizon, per levy case.
  - They support T22 and F22.
  - Identity: `relief = wdt + levy + fund income - fund retention`, exact.
- **Concentration:** top-q share and wealth/GDP at launch and end.
- **Medians:** `medians` is over uncensored windows (right for relief and coverage). `medians_all` is over all windows (right for receipts, burden, drift). `country_median_*` weights countries equally.

### Representativeness
- **Slices:** pooled, focus countries, low-growth, low-inflation, today-like and eras (regime thresholds are judgments).
- **Block bootstrap of the median** with three resampling schemes: iid, country-period blocks, all-country period blocks.
  - `deff = var(block) / var(iid)`.
  - `n_eff = windows / max(deff, 1)`. The honest sample size, since 30-year windows overlap.

### CLI
`python rates_core.py [--quick] [--scenario a b] [--stride k] [--countries ...] [--fresh]`. Scenario results merge into the existing JSON unless `--fresh`.

### Assumptions and limits
- **Honest declaration:** `alpha = 1`. No behavioural response (migration, avoidance, restructuring).
- **Fixed cohort:** no new entrants beyond the six death-phase lines and heirs.
- **Valuation and anchors:** the wealth distribution is a 2016-18 snapshot (no time adjustment), and Pareto interpolation hides lumpiness.
- **Replay:** each country's history is applied to the UK calibration. Overlapping windows are autocorrelated.
- **Heterogeneity:** cohorts are persistent and carry across generations (a stylisation).
- **Basis:** default basis is real (CPI-deflated). The levy base is nominal by statute.
- **Reference denominators:** fixed JST UK 2019 expenditure/GDP and revenue/GDP.
- **Placeholders:** tax-replacement counts and shares, income-by-wealth profile, `f_inc`, `employer_share` and `house_median_gbp_m` need verification before quoting.

## 6. Running order

1. Edit the TOML.
2. Run `valgen_core.py` and `rates_core.py`. Each validates itself and writes its JSON.
3. Run the dependent tables and charts.
4. If you touch `wdt_core`, `wdt_kernel`, the TOML or the JST basis, re-run everything downstream. After a RATES run, refresh `[val_gen.hlc]` with `python test/print_hlc_calibration.py --write`, then re-run `valgen_core.py` (HLC pair).
5. Tests (Model/test): `kernel_test.py`, `bridge_test.py`, `rates_test.py`, `test_valgen_pairs.py`, `test_hlc_drift.py`; `diff_json.py` compares two JSON outputs.
