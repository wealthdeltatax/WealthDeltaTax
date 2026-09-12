Yes — and it's worth being precise about what kind of information is lost, because it's not all the same thing.

**What the 4-tier structure captures well**

The Fagereng return differentials (Poor −4.55pp through Great +3.45pp) are the analytically important dimension for the welfare comparison. The differential is what drives the D-M risk-sharing result, the progressive incidence, and the concentration path. Four tiers span the distribution of return heterogeneity adequately for those questions.

**What's genuinely missing by collapsing 10 brackets to 4**

Three distinct things:

*1. Within-tier wealth variation at the entry margin.*
The 95th percentile (£2.86m) and 99th percentile (£7.14m) are both mapped to a single "Ok" return differential (−2.05pp). But an agent at £2.86m is right at `W_min = £2m` and sits near the τ₀ = 15% floor of the logistic, while an agent at £7.14m is well into the rising part of the curve at maybe 20–25%. The progressive rate function means their effective tax rates differ materially — collapsing them loses that within-tier rate variation.

*2. Population-weighted revenue estimates.*
Each bracket has a real `N_pop`. The aggregate revenue calculation in `run_tier_comparison` uses `pop_share × W0` per tier, but those shares (10/30/40/20%) are Fagereng-derived, not ONS-derived. The actual UK taxable population is heavily skewed: the 95th–99th percentile bracket has ~1.4 million people, the 99.9th has ~62,000, and the 99.99%+ has ~700. Revenue is dominated by the middle brackets by headcount, but by the top brackets by wealth. That interaction is invisible in the current model.

*3. The bottom of the taxable population (90th–95th percentile, £1.63m).*
These are below `W_min = £2m` and therefore currently pay zero WDT. They are the marginal non-taxpayers — the people closest to the entry threshold who would be most affected by a change in `W_min`. The model says nothing about them.

**What you'd get by adding all 10 brackets**

For points 1 and 2, running all 10 brackets through the welfare comparison — each with its actual `V0_m`, `N_pop`, and an assigned Fagereng differential — would give a population-weighted aggregate welfare cost and a revenue estimate that's anchored in real headcount data rather than assumed shares. The four-bracket-below-threshold group (50th–80th) produces no WDT and can be dropped, leaving 6 taxable brackets (90th through 99.99%+).

For point 3, the 90th–95th bracket is genuinely in scope: at £1.63m it's below the current `W_min = £2m`, so they contribute nothing and receive nothing. But if `W_min` were lowered to £1m in a sensitivity run, they'd enter. Knowing their wealth and headcount is useful for that.

**The practical question**

The Fagereng differential assignment is the awkward part. You have 6 taxable brackets but only 4 differentials, and the literature doesn't give you bracket-level differentials — it gives you quartile-level ones. The most defensible approach would be to assign by wealth rank: bottom two taxable brackets (90th, 95th) → Poor differential; next two (99th, 99.9th) → Ok/Good; top two (99.99th, 99.99%+) → Great. That's a judgement call but a transparent one.

**Verdict**

The current model is fine for the welfare ranking and the D-M structural questions — those results won't change materially. What's missing is a credible population-weighted revenue figure and a proper accounting of within-tier rate variation for the progressive schedule. If either of those matters for the paper's claims — and the progressive incidence section probably does depend on them — it's worth adding. It's a contained change: replace the 4 tiers with 6 taxable brackets, assign differentials by a declared mapping, pull `N_pop` from TOML to compute proper population weights, and rerun. The chart would need updating but the new heatmap structure handles arbitrary row counts fine.

Do you want to make that extension?

Let me read the current state of the files carefully before writing anything.Good. Now I have the complete picture. Let me work out the full design before writing a line of code.

**The 6 taxable brackets** (at or above W_min = £2m):

| Bracket | N_pop | V0_m | Below W_min? | Fagereng differential |
|---|---|---|---|---|
| 90% | 3,460,000 | £1.63m | Yes — £1.63m < £2m | Poor (−4.55pp) |
| 95% | 2,768,000 | £2.86m | No | Poor (−4.55pp) |
| 99% | 622,800 | £7.14m | No | Ok (−2.05pp) |
| 99.9% | 62,280 | £19.85m | No | Good (+0.95pp) |
| 99.99% | 6,228 | £53.38m | No | Great (+3.45pp) |
| 99.99%+ | 692 | £139.6m | No | Great (+3.45pp) |

The 90th percentile (£1.63m) is below W_min — it's a marginal non-taxpayer. I'll include it with a flag so the model can show it pays zero WDT, which is informative for the entry-margin discussion. The 50th–80th percentiles (all under £1.11m) are far below threshold and add nothing — exclude them.

**Differential assignment** — declared mapping, transparent:
- 90%, 95% → Poor (−4.55pp): lowest-return bracket, just at/below entry
- 99% → Ok (−2.05pp): mid-range taxable
- 99.9% → Good (+0.95pp): upper taxable range
- 99.99%, 99.99%+ → Great (+3.45pp): top two brackets, both well into the ceiling of the logistic

**Population weights** — replace the Fagereng `weight` field with `N_pop`-derived weights *within the 6 taxable brackets*. The Fagereng weights (10/30/40/20%) described the full population share; we now want weights among the taxable population only, derived from actual headcount.

Total N across 6 brackets: 3,460,000 + 2,768,000 + 622,800 + 62,280 + 6,228 + 692 = 6,920,000.

| Bracket | N_pop | Pop share |
|---|---|---|
| 90% | 3,460,000 | 50.0% |
| 95% | 2,768,000 | 40.0% |
| 99% | 622,800 | 9.0% |
| 99.9% | 62,280 | 0.90% |
| 99.99% | 6,228 | 0.090% |
| 99.99%+ | 692 | 0.010% |

This is now empirically grounded — headcount from ONS/WAS.

**Structural changes needed:**

1. `AgentTier` — add `below_threshold: bool` flag; the 90th bracket gets this set True and is handled as a zero-tax bracket in welfare computations
2. `build_tiers` → replaced by `build_brackets_as_tiers` (or rename `build_tiers` to use brackets directly) — reads all 6 taxable brackets from TOML, assigns differentials and pop weights from N_pop
3. `run_tier_comparison` — needs to handle `below_threshold` brackets gracefully: skip the revenue solver for them (tau doesn't apply), record CEW=0, ET=0
4. `chart_tier_cew` — 6 columns now instead of 4; heatmap already handles arbitrary column count
5. `print_tier_table` — 6 columns
6. `welfare_tables.py` — `table_wfr10`, `table_wfr11`, `table_wfr13` now have 6 bracket columns

The Fagereng `[[tiers]]` in the TOML stay as-is — they're the return differential library. The bracket-to-differential mapping is declared in code (a lookup dict), not in the TOML. That keeps the TOML clean and the mapping auditable.Important observation: the 90% and 95% brackets together are 90% of the taxable population by headcount. The pop-weighted mean W0 is £2.84m — heavily pulled down by the two large low-wealth brackets. This is exactly the right picture: most WDT taxpayers are near the entry threshold, and the ultra-wealthy tail is tiny by headcount but huge by wealth. The model now reflects that.

One more thing to check — what the aggregate revenue target looks like when weighted by wealth rather than headcount, since that's what the solver uses:The 90th bracket (below W_min, zero WDT) holds 28.7% of aggregate wealth among the near-threshold population. That's a meaningful number for the paper — it shows how much wealth sits just below the entry point. Now I have everything I need. Let me write the changes.Good. I now have a complete picture. The changes needed are:

1. **`AgentTier`** — add `bracket_label`, `N_pop`, `below_threshold` fields
2. **`build_tiers`** → rewritten as `build_brackets_as_tiers` (keep `build_tiers` as an alias for backward compat) — reads 6 taxable brackets, assigns differentials and N_pop-derived pop weights
3. **`_solve_aggregate_rate`** — skip `below_threshold` brackets (they pay zero tax, contribute nothing to revenue)
4. **`run_tier_comparison`** — for `below_threshold` brackets, set all CEW/ET to zero without calling the solver
5. **`chart_tier_cew`** — 6 brackets, new TIER_COLOURS for the 2 new ones; heatmap already handles arbitrary columns
6. **`chart_concentration_path`** — ratio now "99.99%+ / 90%" instead of "Great / Poor"; ax2 plot subset to avoid 12-line spaghetti
7. **`chart_envelope`** — 6 panels (2×3 grid instead of 2×2)
8. **`print_tier_table`**, **`print_envelope_summary`** — 6 columns
9. **`main()`** — update agg_taus lookup key from "Good" to "99.9%"; update concentration ratio print
10. **`welfare_tables.py`** — `table_wfr10`, `table_wfr11`, `table_wfr13` — 6 bracket columns