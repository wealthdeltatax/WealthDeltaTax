This is a planning document rather than a coding task, so let me work through the full set of changes systematically.

---

## Change Plan: Post-Settlement Integration

### Conceptual summary

The introduction of `TW_settled` and `Net_settled` in `wdt_core.py` propagates through three layers: (1) the simulation helpers and runners that call `run_sim()`; (2) the output scripts that generate appendix tables and figures; (3) the paper prose and mathematical specification in VAL.A. Each layer has a different kind of change required.

---

## Layer 1 — Python helper and runner files

### `val_s_helpers.py`

The C.1 metric is currently defined as `(Net(α) − Net(1)) / TW(α)`. Both components change:

- Replace `r['Net']` → `r['Net_settled']` throughout
- Replace `r['TW']` → `r['TW_settled']` throughout
- This affects `c1()`, `c1_matrix()`, `n_crossing()`, `tolerant_zone_bounds()`, `tolerant_zone_width()`, `understater_plateau()`, and `run_sim_p()` / `_run_sim_cached()`
- The cached runner `_run_sim_cached()` currently caches on the tuple of parameters — it should also cache `TW_settled` and `Net_settled`, not just the old `Net` and `TW`. Since `settle_tw()` is deterministic, the lru_cache still works correctly; no change to the caching mechanism itself is needed, but the returned dict keys change
- The `draw_c1_heatmap()` function is passed `mat` values already computed, so no change there — but the callers computing `mat` need to use `Net_settled` and `TW_settled`

### `val_helpers.py`

- `eff_rate()` currently computes `r['Net'] / r['TW']`. Change to `r['Net_settled'] / r['TW_settled']`
- No other substantive changes needed here

### `wdt_core.py` (the `run_sim_p()` wrapper in `val_s_helpers`)

Already handled by the core change. The wrapper just calls `run_sim()` and returns its dict, so downstream consumers automatically get the new keys if they use them.

---

## Layer 2 — Output generation scripts

### General principle for all output scripts

Every place a script computes a metric from `run_sim()` results, the mapping is:

| Old | New |
|---|---|
| `r['TW']` in any ratio or comparison | `r['TW_settled']` |
| `r['Net']` in any ratio or comparison | `r['Net_settled']` |
| `r['TTP'] / r['TW']` (effective rate) | `r['TTP'] / r['TW_settled']` or `r['Net_settled'] / r['TW_settled']` depending on context |

The old keys remain in the dict for backward compatibility but should not appear in any output-facing computation.

### `5_3_2608012_VAL_generate_appc_full.py` (Appendix C tables)

**Metric changes:**
- C.1: formula denominator changes from `TW(α)` to `TW_settled(α)`. The numerator `Net(α) − Net(1)` changes to `Net_settled(α) − Net_settled(1)`
- C.2: `Net(α)/TW(α) − Net(1)/TW(1)` → settled equivalents throughout
- C.3 (beta extension): same — use settled metrics; note that the beta extension operates within the holding period, so the settlement correction applies on top
- C.4: `TTP(α=1) / TW(α=1)` — TTP is a holding-period quantity and stays unchanged; denominator changes to `TW_settled(α=1)`
- C.5: `(TW(α,k) − TW(1,k)) / TW(1,k)` → settled equivalents
- C.6: `TW(α) / TW(1)` in negative-g scenarios → settled equivalents
- C.7: `(Net(α,N) − Net(1,N)) / Net(1,N)` → settled equivalents
- C.8: `(TW(α,N) − TW(1,N)) / TW(1,N)` → settled equivalents
- C.9: TW and Net columns → settled equivalents
- C.10: TW, Net, effective rate columns → settled equivalents

**Formatting / numbering alignment with the paper:**
- Table labels should match VAL.A §C exactly: "Table C.1", "Table C.2" etc. — check current script output against the paper's table numbering
- The header note "Validation status: 0 FAILs" should be updated to reflect the new settlement methodology and note the version change
- The `N=29` annotation in table headers should remain (it's the RATES reference horizon, not changed)
- The `g=10.45%` annotation should remain
- All formula lines in the script's markdown output should use settled notation: `Net_settled(α)` and `TW_settled(α)`

### `5_4_260807_VAL_generate_worked_examples.py` (VAL.B figures)

- Update `run_sim()` calls to read `Net_settled` and `TW_settled` for all output metrics
- The "Total lifetime WDT (Net)" rows in tables J.1, K.1, N.1 should use `Net_settled`
- The "Terminal net worth (TW)" rows should use `TW_settled`
- "TW vs honest" and "Net vs honest" comparisons should use settled values throughout
- Effective rate calculation (`r['Net'] / r['TW']`) → settled
- The "Key mechanism" prose sections quote specific £m figures — these will shift slightly and should be regenerated from the updated model

### `5_5_60807_VAL_generate_illustrative.py` (illustrative claims)

- All `eff_rate(r)` calls → `r['Net_settled'] / r['TW_settled']`
- All strategy comparison table cells using `r['TW']` and `r['Net']` → settled
- The saturation reversal boundary search (section 3) uses C.1 — update to settled metric
- The indifference horizon table (section 5) uses `Net` — update to `Net_settled`
- The refund protection section (section 4) uses `TW` ratio — update to `TW_settled`
- Section 6 (rate profile) is unchanged — it uses `tau()` directly, no simulation

### `5_6_260809a_VAL_generate_figures.py` (VAL figures)

- `fig_02_c1_heatmap()`: the inline computation `(r['Net'] - b['Net']) / r['TW'] * 100` → settled
- `fig_03_equilibrium_cost_curve()`: `(r['Net'] - base['Net']) / base['Net'] * 100` → settled
- `fig_04_tw_gap_by_n()`: `(r['TW'] - b['TW']) / b['TW'] * 100` → settled
- `fig_05_saturation_reversal()`: C.1 computation inline → settled
- `fig_06_overstatement_reversal()`: C.1 computation inline → settled
- `fig_07_overstatement_coherence()`: both panels — C.1 surface and net tax difference — use `r['Net']` directly; the right panel uses `r['Net'] - b['Net']` which should become `r['Net_settled'] - b['Net_settled']`
- The `run_hist()` closure inside `fig_03` constructs its own `{'Net': ..., 'TW': ...}` dict manually from `simulate()` and `simulate_sell()` — this needs to call `settle_tw()` and add `Net_settled` and `TW_settled` to the manually-constructed result, or be refactored to call `run_sim_hist()` instead

### `16_2_260812b_VAL_S_rate_sweeps.py`

All C.1 computations delegate to `val_s_helpers.c1()` — once that helper is updated, these figures regenerate correctly with no further changes needed. The figure titles and axis labels do not reference `TW` or `Net` directly, so no label changes required.

### `16_3_260812a_VAL_S_horizon_sweeps.py`

Same as 16_2 — delegates to `val_s_helpers`. No direct changes needed beyond the helper update.

### `16_4_260812b_VAL_S_interactions.py`

Same delegation pattern. `tolerant_zone_width()` and `understater_plateau()` are called from `val_s_helpers` — once updated there, this script regenerates correctly.

### `16_5_260812b_VAL_S_assemble.py`

- Section A.4 (N sweep): the inline computation `c1_val = (r['Net'] - b['Net']) / r['TW']` → settled; `eff = r['Net'] / r['TW']` → settled. All other sections delegate to `c1()` from helpers.
- Section A.6 (τ₀ × N surface): delegates to `n_crossing()` from helpers — no direct change
- Section A.7 (k × V₀ surface): delegates to `c1()` from helpers — no direct change
- The consistency check at the bottom uses `c1()` — no direct change, updates automatically

**Formatting / numbering alignment:**
- Section labels `A.1` through `A.9` should match VAL.A appendix section numbering exactly — verify against the paper's §A–§G structure
- The figure index (section A.9) references figure filenames — these are unchanged
- The metadata header should note the model version change and settlement methodology

### `8_3_260812_RATES_output.py` (RATES.A output)

The RATES model uses `run_ssm()` and `run_tcm()` from `rates_model.py`, which call `simulate()` and `simulate_sell()` directly (not `run_sim()`). These functions return individual cell results without TW or Net in the same sense — the RATES model aggregates marginal cohort flows, not individual lifetime outcomes.

**Consequently**: RATES output does not directly use `TW_settled` or `Net_settled`. The RATES model is internally consistent and does not need substantive changes for the settlement fix.

However, the `run_tcm()` function in `rates_model.py` computes `eff_rate` and `wealth_burden` for individual bracket/tier cells using `TW` from `simulate_sell()` — specifically:
```python
TW = (W_sell - L_sell / tau_sell) if (tau_sell > 0.0 and L_sell > 0.0) else W_sell
```
This is a different TW definition (used for burden analysis, not lifetime settlement), and is intentionally left as-is — it measures the asset's value net of the sell-year tax event for burden analysis purposes, not the post-settlement cash position. Document this distinction clearly in the RATES.A output header.

### `16_6_260813_RATES_S_tables.py` and `16_7_260813_RATES_S_charts.py`

Same as RATES output — these sweep `rates_model.run_start_year_sweep()`, which does not use `run_sim()`. No changes needed to the computation. The tables and figures are already correctly specified.

---

## Layer 3 — VAL.A paper: mathematical specification updates

### §B.2.1 — Simulation algorithm (the most important fix)

The current text says for `Δ_t < 0`:
> `f_t = f_{t-1}`

This contradicts §A.4.2 Step 7, which correctly states `f_t = f_{t-1} × (1 − q_t)` for all signs of `q_t`. The code matches §A.4.2. Fix §B.2.1 to read:

> If `Δ_t < 0` (negative delta — refund period):
> `R_t = τ(W_t) × |Δ_t|` (subject to lifetime cap as in equation A.4.5)
> `q_t = L_t / W_t` (negative, since L_t is negative)  
> `f_t = f_{t-1} × (1 − q_t)` (retained fraction increases as state returns equity)

### §B.2.2 — Sell-year algorithm

The current text states `W_{N+1} = f_N × V_N` (no growth step). The correct formula per §A.4.4 and the code is `V_sell = V_N × (1 + g_sell)`, then `W_{N+1} = f_N × V_sell`. Fix §B.2.2 to include the sell-year growth step explicitly.

### §B.2 — New subsection: Post-sale settlement

Add a new subsection §B.2.3 after §B.2.2 describing the settlement procedure:

> **§B.2.3 Post-sale settlement**
>
> After the sell event, the mechanism does not terminate. The taxpayer holds cash `C_0 = W_sell − L_sell`. Modelling the simplifying assumption that they hold this cash with no further growth, each subsequent period produces:
>
> `delta_s = C_s − C_{s-1}` (where `C_{-1} = W_sell`)  
> `L_s = τ(C_s) × delta_s` (subject to lifetime cap)  
> `C_{s+1} = C_s − L_s`
>
> The series converges because `|τ| < 1` everywhere. At canonical parameters, convergence to `|L_s| < 10^{-10}` requires approximately 15 iterations.
>
> **TW_settled** is the value of `C_s` at convergence.  
> **Net_settled** is `Net + Σ L_s` across all settlement periods.
>
> The correction is directionally symmetric: understaters receive partial refunds during settlement (positive correction to TW), while overstaters pay additional tax (negative correction to TW). At canonical parameters the correction ranges from approximately +3% for severe understaters (α=0.1) to −2% for aggressive overstaters (α=2.0).

### §A.2 (Main Findings) — update to findings 4 and 5

**Finding 4** currently states the plateau is N-invariant and that aggressive overstatement is self-limiting. This remains correct. Add: the TW advantage cap is tighter than naive accounting suggests — post-settlement, the overstater's TW advantage at α=2.0 is approximately 12% above honest (rather than 14% naive), and their Net_settled is approximately 16% above the honest Net_settled (they pay more, not less, in net lifetime tax). The contemporaneous growth-corridor mechanism and the temporal N-crossing mechanism remain unchanged.

**Finding 5** currently states "the stable equilibrium zone is mild overstatement, not honest declaration." This can now be stated more precisely: mild overstatement (α ≈ 1.2–1.5) retains a TW_settled advantage and a Net_settled advantage (pays less total lifetime tax) relative to honest declaration, and this advantage is forecast-independent across the full tested growth range. Aggressive overstatement (α ≥ 1.8) has a TW_settled advantage but a Net_settled *disadvantage* — it retains more wealth but pays more total lifetime tax. This is a meaningful distinction: the mechanism collects more total tax from aggressive overstaters than from honest declarers, even though their terminal wealth is higher. The "advantage" of aggressive overstatement is purely a timing and composition effect, not a total-burden reduction.

### §C series — table header updates

Every table in §C that references the metric formula needs:
- `Net(α)` → `Net_settled(α)` in formula lines
- `TW(α)` → `TW_settled(α)` in formula lines  
- "Validation status" note updated to reflect v2 methodology
- Brief footnote: "TW_settled and Net_settled include post-sale settlement periods. See §B.2.3."

### §A.4 (Multi-Period Incentive Model) — notation table

Add `TW_settled` and `Net_settled` to the notation table in §A.4.1, defined as the converged values after the post-sale settlement procedure in §B.2.3.

### §A.5.6 (Cost functions and indifference conditions)

The table summarising propositions 1–6 should note that the indifference boundaries `α_low` and `α_high` are defined relative to `Net_settled`, not `Net`. This potentially shifts the boundary values slightly and should be recomputed from the updated tables.

---

## Summary of what is and isn't changing

**What changes substantially**: All TW and Net metrics reported in VAL.A §C tables, VAL.B worked example figures, VAL illustrative claims, and the five VAL figures. The changes are directionally consistent — understater penalties decrease slightly, overstater advantages decrease slightly — and the overall qualitative picture is preserved. The new Net_settled metric adds an important new dimension: aggressive overstaters pay *more* total lifetime tax than honest declarers, which is a cleaner statement of mechanism integrity than the C.1 metric alone.

**What does not change**: The RATES and RATES.S outputs — these use a different simulation path (SSM/TCM marginal cohort model) that does not pass through `run_sim()`. The VAL.S sweep figures change only insofar as C.1 values shift slightly; the qualitative patterns (heatmap structure, tolerant zone, N-crossing thresholds) are robust to the settlement correction. The rate function, the grandfathering logic, the must-transfer rule, and all Route D mechanics are unchanged.

**What resolves from the VAL observations**: The two concrete specification discrepancies (§B refund equity treatment, §B sell-year growth) are now corrected in the paper. The "settled TW" question is resolved with a named methodology. The reviewer's concern about TW rising monotonically with α is partially addressed — Net_settled reverses for aggressive overstaters, providing a cleaner mechanism-integrity claim even if TW_settled remains monotone.