"""W2-05  WDT_Params.toml D11 cleanup.  Apply together with W2-04 (W2-04 makes wdt_core stop reading these blocks).

 deleted   [swf] [budget] [returns] [tcm] [[tiers]] [[brackets]] (+ the retired-[rate] note)
           [sweep]: N_canon V0_canon g_canon, rates_*_sweep (incl. rates_g_sweep), wfr_*  (+ their doc comments)
 changed   [sweep] g_vals  ->  g_offsets (pp around g_real; wdt_core.with_val_basis builds g_vals = g_real + offsets)
           [synthetic_scenario] mu 0.07 -> 0.02 (the comment always said 2%); amplitude comment states the real range
           [val_gen] basis: "legacy" removed from the comment; index_wmin comment; stale N_fill comments
 kept      [rates.defaults].tiers (cohort return tiers: a different thing), the live [sweep] grids

 NOT touched (flagged): [meta] version = "v7"; [val] surface_table_g (nominal-era grid 5/8/10.45/15/20%);
 amplitude = 0.08 in [synthetic_scenario] (gives -6%..+10%, the old comment described 0.04).

Numbers: the g_vals grid moves (nominal 10.45% centre -> JST real g_real centre).  Synthetic scenario mu moves 7% -> 2%
(only synthetic_returns reads it).  Nothing in RATES moves.
"""
import re
from patchlib import Patch
P = Patch('W2-05', __doc__)
T = 'WDT_Params.toml'
S = re.S | re.M

# header N convention
P.regex(T, r"# N CONVENTION \(read this before touching any N value\)\n.*?# decompose_tw_advantage / npv_tax_advantage REQUIRE N to be passed explicitly\.\n",
        "# N CONVENTION: N_val = [val] N_demo = 30 is the taxpayer holding period (p['N_val']). The SSM fill year N_fill is retired (D11);\n"
        "# the fund fills inside each RATES window. run_sim / run_sim_hist / run_pair REQUIRE N to be passed explicitly.\n", count=1, flags=S)

# legacy blocks: from the [rate] banner to the [val] banner
P.regex(T, r"# ─+\n# \[rate\] — WDT logistic rate function parameters\n.*?(?=# ─+\n# \[val\] — VAL reference scenario parameters)",
        "# ─────────────────────────────────────────────────────────────\n"
        "# RETIRED (D11): [rate] (D2), [swf], [budget], [returns], [tcm], [[tiers]], [[brackets]].\n"
        "# Rate design  = [rates.defaults] / [rates.scenarios.*], picked for VAL by [val_gen] rate_scenario (baseline \"gain_ladder\").\n"
        "# Real basis   = [val_gen] basis (\"jst\": g_real and index_rate derived from the JST history).\n"
        "# Fund sizing  = ms, ml in [rates.defaults] (the fund fills inside each window; no SSM fill year).\n"
        "# Cohort tiers = [rates.cohorts.*].   Wealth cells = RATES build_dist.\n"
        "# The legacy tables are in the legacy-v7 tag.\n"
        "# ─────────────────────────────────────────────────────────────\n\n\n", count=1, flags=S)

# [sweep] doc comments
P.regex(T, r"# CANONICAL BASELINE\n# -+\n.*?(?=# ANALYSIS CONSTANTS)", "", count=1, flags=S)
P.replace(T, "# g_vals         : growth sweep used in C.1 heatmaps (VAL.A Data Tables order)\n",
          "# g_offsets      : growth sweep as offsets (pp, additive) around g_real; wdt_core.with_val_basis builds p['sweep']['g_vals'] = g_real + g_offsets\n")
P.regex(T, r"# RATES\.S SWEEP GRIDS\n# -+\n.*?(?=# ─+\n\[sweep\])", "", count=1, flags=S)
# [sweep] body
P.regex(T, r"# ── Canonical baseline ─+\n.*?(?=# ── Analysis constants)", "", count=1, flags=S)
P.regex(T, r"g_vals = \[\n  -0\.0455, 0\.00449, 0\.059, 0\.084, 0\.1045,\n   0\.114,  0\.139,   0\.1645, 0\.2045, 0\.2545,\n\]\n",
        "# offsets from g_real (the old nominal grid was 10.45% +/- the same steps); 0.0 is g_real itself\n"
        "g_offsets = [-0.15, -0.10, -0.0455, -0.0205, 0.0, 0.0095, 0.0345, 0.06, 0.10, 0.15]\n", count=1, flags=S)
P.regex(T, r"# ── RATES\.S sweep grids ─+\n.*?(?=# Synthetic scenario — linear trend)", "", count=1, flags=S)

# synthetic scenario
P.replace(T, "mu        = 0.07     # mean growth rate = UK CPI inflation floor (2%)", "mu        = 0.02     # mean growth rate = UK CPI inflation floor (2%)")
P.replace(T, "amplitude = 0.08     # canonical: g oscillates between -2% and +6%", "amplitude = 0.08     # with mu = 2%: g oscillates between -6% and +10% (0.04 would give -2% .. +6%)")

# stale comments
P.replace(T, "# index_wmin    : index W_min and k at [budget] budget_growth (D16).", "# index_wmin    : index W_min and k at the real index_rate (D16).")
P.replace(T, '#   "legacy" nominal hist_mean and [budget] budget_growth. Kept only until D11 retires them.\n', "#   (the nominal \"legacy\" basis is retired: D11)\n")
P.replace(T, "#   * The rebuild does not use N_fill / the old SSM: the fund fills dynamically\n#     inside each window (rates_core, fund layer).\n",
          "#   * The fund fills dynamically inside each window (rates_core, fund layer); there is no SSM fill year.\n")
P.regex(T, r"                # from p\['N_fill'\] \(the SSM-derived LRR fill year\), which is a fund\n                # mechanics output, not a taxpayer lifecycle parameter\.\n",
        "                # from the fund fill year, which is a RATES output, not a taxpayer lifecycle parameter.\n", count=1, flags=S)
P.run()
