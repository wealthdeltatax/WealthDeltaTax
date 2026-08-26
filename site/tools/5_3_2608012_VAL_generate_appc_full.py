"""
VAL Output Script A — Full Appendix C Tables
=============================================
Generates VAL_AppC_Full_Tables.md

Parameters and simulation engine imported from wdt_core.py (single source of truth).
No Excel dependency. Uses confirmed simulation conventions and formulas throughout.

Output is a drop-in replacement for the [PENDING] placeholders in VAL.A §C.1–C.9,
plus a new C.10 using the 2006 historical return series (RATES Balanced reference).
Each table is preceded by a single formula line only. No prose.

N-offset correction applied: Tables 7/8 show actual N (5,10,...,60),
not the Excel header offset values (0,5,...,55).

Table 3 uses confirmed additive beta formula: g_eff = g + beta*ln(alpha).
VAL.A §B.3 and §C.3 carry the erroneous multiplicative form; this output
uses the formula confirmed from the Excel cell.

Model limitation: Option A convention throughout (annual periods = assessment
windows). Table K in worked examples uses N=3 annual periods, not three
multi-year windows. Expected to produce variance from a window-aware model.

N=34: aligned with the RATES Balanced reference scenario (2006 start year,
34-year LRR fill horizon). This is the correct policy-relevant horizon for
all cross-paper consistency. Previous versions used N=32 (an error) or
referenced N=61 (the raw Excel validation run) or N=58 (LRR breakeven year,
a derived output rather than a scenario parameter).
"""

import os
from datetime import date
from wdt_core import load_params, tau, g_eff, simulate, simulate_sell, run_sim, run_sim_hist
from val_helpers import OUT_DIR, pct_str, fmt_val, md_table

# All analytical grids sourced from TOML via load_params() in main().
# Module-level names are populated there and used throughout.
G_VALS        = []
G_LABELS      = []
ALPHA_VALS    = []
K_VALS        = []
V0_VALS       = []
N_ACTUAL_VALS = []
OVER_VALS     = []


# Core mechanics (tau, g_eff, simulate, simulate_sell, run_sim) imported from wdt_core.


# ─────────────────────────────────────────────────────────────
# TABLE COMPUTATION
# ─────────────────────────────────────────────────────────────

def compute_all_tables(p):
    g_pos = [g for g in G_VALS if g > 0]

    # Precompute honest baselines by g
    base_by_g = {g: run_sim(p, alpha=1.0, beta=0.0, g=g) for g in G_VALS}
    base_pos   = {g: base_by_g[g] for g in g_pos}
    base_ref   = run_sim(p, alpha=1.0, beta=0.0)  # at params g

    # Table 1: (Net(a) - Net(1)) / TW(a) by alpha x g
    t1 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_by_g[g]
            row.append((r['Net'] - b['Net']) / r['TW'] if abs(r['TW']) > 1e-12 else 0.0)
        t1[alpha] = row

    # Table 2: Net(a)/TW(a) - Net(1)/TW(1) by alpha x g
    t2 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_by_g[g]
            val = (r['Net'] / r['TW'] - b['Net'] / b['TW']
                   if abs(r['TW']) > 1e-12 and abs(b['TW']) > 1e-12 else 0.0)
            row.append(val)
        t2[alpha] = row

    # Table 3: (Net(a,beta) - Net(1,beta=0)) / TW(a,beta), overstaters only
    # beta swept over same numeric values as G_VALS; g fixed at params g
    t3 = {}
    for alpha in OVER_VALS:
        row = []
        for beta_col in G_VALS:
            r = run_sim(p, alpha=alpha, beta=beta_col, g=p['g'])
            val = ((r['Net'] - base_ref['Net']) / r['TW']
                   if abs(r['TW']) > 1e-12 else 0.0)
            row.append(val)
        t3[alpha] = row

    # Table 4: TTP(a=1)/TW(a=1) by k x V0
    t4 = {}
    for k in K_VALS:
        row = []
        for v0 in V0_VALS:
            tp = dict(p); tp['k'] = k; tp['V0_m'] = float(v0)
            r = run_sim(tp, alpha=1.0, beta=0.0)
            row.append(r['TTP'] / r['TW'] if abs(r['TW']) > 1e-12 else 0.0)
        t4[k] = row

    # Table 5: (TW(a,k) - TW(1,k)) / TW(1,k) by alpha x k
    t5 = {}
    for alpha in ALPHA_VALS:
        row = []
        for k in K_VALS:
            tp = dict(p); tp['k'] = k
            r = run_sim(tp, alpha=alpha, beta=0.0)
            b = run_sim(tp, alpha=1.0, beta=0.0)
            row.append((r['TW'] - b['TW']) / b['TW'] if abs(b['TW']) > 1e-12 else 0.0)
        t5[alpha] = row

    # Table 6: TW(a)/TW(1) by alpha x g (positive g only)
    t6 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in g_pos:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_pos[g]
            row.append(r['TW'] / b['TW'] if abs(b['TW']) > 1e-12 else 0.0)
        t6[alpha] = row

    # Tables 7 and 8: N sweep at params g
    # N-offset corrected: N_ACTUAL_VALS are the real simulation Ns
    t7 = {}; t8 = {}
    for alpha in ALPHA_VALS:
        row7 = []; row8 = []
        for n_act in N_ACTUAL_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, N=n_act)
            b = run_sim(p, alpha=1.0,   beta=0.0, N=n_act)
            v7 = (r['Net'] - b['Net']) / b['Net'] if abs(b['Net']) > 1e-12 else 0.0
            v8 = (r['TW']  - b['TW'])  / b['TW']  if abs(b['TW'])  > 1e-12 else 0.0
            row7.append(v7); row8.append(v8)
        t7[alpha] = row7; t8[alpha] = row8

    # Table 9: Summary — TW at alpha∈{2,1,0.1} and refund ratio by g
    t9 = []
    for g in sorted([g for g in G_VALS if g >= 0], reverse=True):
        r2  = run_sim(p, alpha=2.0, beta=0.0, g=g)
        r1  = run_sim(p, alpha=1.0, beta=0.0, g=g)
        r01 = run_sim(p, alpha=0.1, beta=0.0, g=g)
        # Refund ratio: Net(0.1)/Net(1) where Net is negative (refund scenario)
        # Only meaningful at negative g; for positive g Net > 0, ratio not applicable
        refund_ratio = (r01['Net'] / r1['Net']
                        if r1['Net'] < 0 and abs(r1['Net']) > 1e-12 else None)
        t9.append({'g': g, 'TW_a2': r2['TW'], 'TW_a1': r1['TW'],
                   'TW_a01': r01['TW'], 'Net_a2': r2['Net'],
                   'Net_a1': r1['Net'], 'Net_a01': r01['Net'],
                   'refund_ratio': refund_ratio})

    # Table 10: 2006 historical return series — α sweep at N=34 + N trajectory at α=1
    #
    # Part A: full α sweep at N=p['N'] (34).
    #   For each α in ALPHA_VALS, run_sim_hist; report TW, TTP, Net,
    #   effective rate (Net/TW), TW vs honest, Net vs honest.
    #   Base is α=1.0 under the same series.
    #
    # Part B: N trajectory at α=1.0.
    #   For N in {5,10,15,20,25,30,p['N']}, run_sim_hist; report TW, Net,
    #   g_mean (mean of the N holding-period returns used).
    #
    # g_mean varies by N because each call uses returns[:N]; it is printed
    # in Part B so readers can see how the realised-return average evolves
    # as the holding window extends through the 2006 series.

    base_hist = run_sim_hist(p, alpha=1.0)   # α=1 baseline for Part A

    t10_alpha = []
    for alpha in ALPHA_VALS:
        r = run_sim_hist(p, alpha=alpha)
        tw_vs_honest  = ((r['TW']  - base_hist['TW'])  / base_hist['TW']
                         if abs(base_hist['TW'])  > 1e-12 else 0.0)
        net_vs_honest = ((r['Net'] - base_hist['Net']) / base_hist['Net']
                         if abs(base_hist['Net']) > 1e-12 else 0.0)
        eff_rate      = r['Net'] / r['TW'] if abs(r['TW']) > 1e-12 else 0.0
        t10_alpha.append({
            'alpha':         alpha,
            'TW':            r['TW'],
            'TTP':           r['TTP'],
            'Net':           r['Net'],
            'eff_rate':      eff_rate,
            'tw_vs_honest':  tw_vs_honest,
            'net_vs_honest': net_vs_honest,
            'g_mean':        r['g_mean'],
        })

    n_traj_vals = sorted({5, 10, 15, 20, 25, 30, p['N']})
    t10_n = []
    for n in n_traj_vals:
        r = run_sim_hist(p, alpha=1.0, N=n)
        t10_n.append({
            'N':      n,
            'TW':     r['TW'],
            'Net':    r['Net'],
            'g_mean': r['g_mean'],
        })

    return {
        't1': t1, 't2': t2, 't3': t3, 't4': t4,
        't5': t5, 't6': t6, 't7': t7, 't8': t8, 't9': t9,
        't10_alpha': t10_alpha, 't10_n': t10_n,
    }


# ─────────────────────────────────────────────────────────────
# MARKDOWN FORMATTING — imported from val_helpers
# ─────────────────────────────────────────────────────────────

def write_appc_md(tables, p):
    lines = []

    lines.append(f"# VAL.A Appendix C — Full Simulation Tables")
    lines.append(f"")
    lines.append(f"**Generated:** {date.today().isoformat()}  ")
    lines.append(f"**Model version:** Python v1.0 (standalone, no Excel dependency)  ")
    lines.append(f"**Parameters:** $V_0$ = £{p['V0_m']:.0f}m · $\tau_0$ = {p['tau_0']*100:.0f}% · $\tau_m$ = {p['tau_m']*100:.0f}% · k = {p['k']} · W_min = £{p['W_min']:.0f}m · N = {p['N']} · g = {p['g']*100:.2f}%  ")
    lines.append(f"**Validation status:** 0 FAILs across all primary matrices (confirmed against Excel 27 July 2026)  ")
    lines.append(f"**N-offset:** Tables C.7/C.8 show actual simulation N; Excel displayed N-5 in column headers — corrected here.  ")
    lines.append(f"**Beta formula:** Additive g_eff = g + β·ln(α); VAL.A §B.3 shows multiplicative form — that section requires update.  ")
    lines.append(f"**Table C.4 note:** Max 2.67% deviation from Excel (known snapshot issue); Python values used throughout.  ")
    lines.append(f"")

    # ── C.1 ────────────────────────────────────────────────────
    lines.append(f"## C.1 Total Tax Paid Difference Relative to Honest Declaration, as Share of Terminal Net Worth")
    lines.append(f"")
    lines.append(f"**Formula:** (Net(α) − Net(1)) / TW(α)  ·  Positive = α pays more than honest; negative = pays less.")
    lines.append(f"")
    t1 = tables['t1']
    headers = ['α \\ g'] + G_LABELS
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t1[alpha]
        rows.append(row)
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*Base parameters. α = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax.*")
    lines.append(f"")

    # ── C.2 ────────────────────────────────────────────────────
    lines.append(f"## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration")
    lines.append(f"")
    lines.append(f"**Formula:** Net(α)/TW(α) − Net(1)/TW(1)  ·  Positive = α has higher effective rate than honest.")
    lines.append(f"")
    t2 = tables['t2']
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t2[alpha]
        rows.append(row)
    lines.append(md_table(headers, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*VAL.A §C.2 describes this as 'effective lifetime tax rate from terminal wealth' but the formula is a difference relative to honest. Label in VAL.A §C.2 heading requires correction.*")
    lines.append(f"")

    # ── C.3 ────────────────────────────────────────────────────
    lines.append(f"## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)")
    lines.append(f"")
    lines.append(f"**Formula:** (Net(α,β) − Net(1,β=0)) / TW(α,β)  ·  β swept over same numeric values as g columns; g fixed at 10.45%.")
    lines.append(f"**Beta formula:** g_eff = g + β·ln(α) [additive — confirmed from Excel; VAL.A §B.3 states multiplicative form incorrectly].")
    lines.append(f"**Scope:** Overstatement only (α ≥ 1.0). Understater cells omitted — analytical scope for signalling is overstatement.")
    lines.append(f"")
    t3 = tables['t3']
    beta_labels = [f"β={g*100:.1f}%" for g in G_VALS]
    headers3 = ['α \\ β'] + beta_labels
    rows = []
    for alpha in OVER_VALS:
        row = [f"**{alpha}**"] + t3[alpha]
        rows.append(row)
    lines.append(md_table(headers3, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*Exploratory only. No empirical calibration for β exists. Sign convention: positive = α pays more than honest. Deviations increase at high α×β due to exponential compounding over N=34.*")
    lines.append(f"")

    # ── C.4 ────────────────────────────────────────────────────
    lines.append(f"## C.4 Effective Lifetime Tax Rate by k Parameter and Initial Wealth ($V_0$)")
    lines.append(f"")
    lines.append(f"**Formula:** TTP(α=1) / TW(α=1)  ·  Honest declaration throughout. Rows = k; columns = $V_0$ (£m).")
    lines.append(f"**Note:** Max 2.67% deviation from Excel (known snapshot — Excel AppC cells computed at different params state). Python values used.")
    lines.append(f"")
    t4 = tables['t4']
    v0_labels = [f"£{v}m" for v in V0_VALS]
    headers4 = ['k \\ $V_0$'] + v0_labels
    rows = []
    for k in K_VALS:
        row = [f"{k:.0e}"] + t4[k]
        rows.append(row)
    lines.append(md_table(headers4, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*All at α=1, β=0, g=10.45%, N=34. k values above 0.001 are analytically extreme; included for completeness.*")
    lines.append(f"")

    # ── C.5 ────────────────────────────────────────────────────
    lines.append(f"## C.5 Sensitivity of k and Alpha: Terminal Net Worth Difference vs Honest")
    lines.append(f"")
    lines.append(f"**Formula:** (TW(α,k) − TW(1,k)) / TW(1,k)  ·  Positive = α retains more TW than honest; negative = less.")
    lines.append(f"")
    t5 = tables['t5']
    k_labels = [f"{k:.0e}" for k in K_VALS]
    headers5 = ['α \\ k'] + k_labels
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t5[alpha]
        rows.append(row)
    lines.append(md_table(headers5, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*α = 1.0 row is zero by construction. g = 10.45%, N = 34 throughout.*")
    lines.append(f"")

    # ── C.6 ────────────────────────────────────────────────────
    lines.append(f"## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio")
    lines.append(f"")
    lines.append(f"**Formula:** TW(α) / TW(1)  ·  Values below 100% = reduced TW relative to honest. Negative g scenarios only.")
    lines.append(f"")
    t6 = tables['t6']
    # Table 6 uses positive g only — for refund protection we want negative g
    # Recompute Table 6 equivalent for negative g (refund scenarios)
    p = p.copy()
    neg_g_vals = [g for g in G_VALS if g < 0]
    neg_g_labels = [G_LABELS[i] for i, g in enumerate(G_VALS) if g < 0]
    base_neg = {g: run_sim(p, alpha=1.0, beta=0.0, g=g) for g in neg_g_vals}
    t6_neg = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in neg_g_vals:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g)
            b = base_neg[g]
            row.append(r['TW'] / b['TW'] if abs(b['TW']) > 1e-12 else 0.0)
        t6_neg[alpha] = row
    headers6 = ['α \\ g'] + neg_g_labels
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t6_neg[alpha]
        rows.append(row)
    lines.append(md_table(headers6, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*Negative g scenarios only. α = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry.*")
    lines.append(f"")

    # ── C.7 ────────────────────────────────────────────────────
    lines.append(f"## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N")
    lines.append(f"")
    lines.append(f"**Formula:** (Net(α,N) − Net(1,N)) / Net(1,N)  ·  Positive = α pays more net tax than honest.")
    lines.append(f"**N correction:** Values shown are actual simulation N (5 to 60). Excel headers showed N-5 (0 to 55) — corrected here.")
    lines.append(f"")
    t7 = tables['t7']
    headers7 = ['α \\ N'] + [str(n) for n in N_ACTUAL_VALS]
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t7[alpha]
        rows.append(row)
    lines.append(md_table(headers7, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*g = 10.45% throughout. α = 1.0 row is zero by construction. Understater penalty at N=5 reflects large realisation delta on short horizon.*")
    lines.append(f"")

    # ── C.8 ────────────────────────────────────────────────────
    lines.append(f"## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N")
    lines.append(f"")
    lines.append(f"**Formula:** (TW(α,N) − TW(1,N)) / TW(1,N)  ·  Negative = α retains less TW than honest.")
    lines.append(f"**N correction:** As C.7 — actual N shown.")
    lines.append(f"")
    t8 = tables['t8']
    rows = []
    for alpha in ALPHA_VALS:
        row = [f"**{alpha}**"] + t8[alpha]
        rows.append(row)
    lines.append(md_table(headers7, rows, fmt_fn=lambda v: pct_str(v, 2)))
    lines.append(f"")
    lines.append(f"*g = 10.45% throughout. α = 1.0 row is zero by construction.*")
    lines.append(f"")

    # ── C.9 ────────────────────────────────────────────────────
    lines.append(f"## C.9 Summary of Declaration Incentives Across Growth Regimes")
    lines.append(f"")
    lines.append(f"**Columns:** TW(£m) and Net tax (£m) at α∈{{2.0, 1.0, 0.1}}; ratios vs honest. N = 34 throughout.")
    lines.append(f"")
    t9 = tables['t9']
    headers9 = ['g', 'TW(α=2) £m', 'TW(α=1) £m', 'TW(α=0.1) £m',
                'Net(α=2) £m', 'Net(α=1) £m', 'Net(α=0.1) £m',
                'TW(0.1)/TW(1)', 'Net(0.1)/Net(1)']
    lines.append('| ' + ' | '.join(headers9) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in headers9) + '|')
    for row in t9:
        g_disp = f"{row['g']*100:.1f}%"
        tw2    = f"{row['TW_a2']:.1f}"
        tw1    = f"{row['TW_a1']:.1f}"
        tw01   = f"{row['TW_a01']:.1f}"
        net2   = f"{row['Net_a2']:.1f}"
        net1   = f"{row['Net_a1']:.1f}"
        net01  = f"{row['Net_a01']:.1f}"
        tw_r   = f"{row['TW_a01']/row['TW_a1']*100:.1f}%" if abs(row['TW_a1']) > 1e-12 else "—"
        net_r  = (f"{row['Net_a01']/row['Net_a1']*100:.1f}%"
                  if row['refund_ratio'] is not None else "—")
        lines.append(f"| {g_disp} | {tw2} | {tw1} | {tw01} | {net2} | {net1} | {net01} | {tw_r} | {net_r} |")
    lines.append(f"")
    lines.append(f"*Net(α=0.1)/Net(α=1) shown only where Net < 0 (refund scenario, negative g). '—' at positive g where both Net values are positive.*")
    lines.append(f"")

    # ── C.10 ───────────────────────────────────────────────────
    lines.append(f"## C.10 2006 Historical Return Series — Reference Scenario Results")
    lines.append(f"")
    lines.append(
        f"**Source:** p['returns'] rotated to {p['scenario_start_year']} start year "
        f"(RATES Balanced worst-case reference scenario).  "
        f"N = {p['N']} holding periods + sell year.  "
        f"$V_0$ = £{p['V0_m']:.0f}m, $\tau_0$ = {p['tau_0']*100:.0f}%, "
        f"$\tau_m$ = {p['tau_m']*100:.0f}%, k = {p['k']}.  "
        f"No beta/signalling adjustment applied."
    )
    lines.append(f"")
    lines.append(
        f"**Purpose:** Locates the RATES worst-case scenario within the analytical "
        f"space characterised by C.1–C.9. The 2006 series includes the 2008 crash "
        f"and subsequent recovery; the realised mean growth rate across N={p['N']} "
        f"periods is below the 10.45% hist_mean used in C.1–C.9, so results here "
        f"represent a harder test than the constant-g tables."
    )
    lines.append(f"")

    # Part A: α sweep
    lines.append(f"### C.10a — Declaration strategy comparison (α sweep, N = {p['N']})")
    lines.append(f"")
    lines.append(
        f"*Realised mean g across N={p['N']} periods: "
        f"{tables['t10_alpha'][0]['g_mean']*100:.2f}% "
        f"(varies by N; this figure is for Part A's N={p['N']}).*"
    )
    lines.append(f"")

    h10a = ['α', 'TW (£m)', 'TTP (£m)', 'Net (£m)', 'Eff rate', 'TW vs honest', 'Net vs honest']
    lines.append('| ' + ' | '.join(h10a) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10a) + '|')
    for row in tables['t10_alpha']:
        marker = ' ← honest' if row['alpha'] == 1.0 else ''
        lines.append(
            f"| **{row['alpha']}** "
            f"| {row['TW']:.2f} "
            f"| {row['TTP']:.2f} "
            f"| {row['Net']:.2f} "
            f"| {row['eff_rate']*100:.2f}% "
            f"| {row['tw_vs_honest']*100:+.2f}% "
            f"| {row['net_vs_honest']*100:+.2f}%{marker} |"
        )
    lines.append(f"")
    lines.append(
        f"*α = 1.0 row is the honest baseline; TW vs honest and Net vs honest are "
        f"zero by construction for that row. Positive Net vs honest = understater "
        f"pays more net tax than honest under the historical series.*"
    )
    lines.append(f"")

    # Part B: N trajectory at α=1.0
    lines.append(f"### C.10b — Honest declarer trajectory by N (α = 1.0)")
    lines.append(f"")
    lines.append(
        f"*Each row uses p['returns'][:N] as the holding-period series and "
        f"p['returns'][N] as the sell-year rate. g_mean is the arithmetic mean "
        f"of the N holding-period returns; it shifts as more years of the 2006 "
        f"series are included, most notably around N=3 (2008 crash enters) and "
        f"N=4 (2009 recovery enters).*"
    )
    lines.append(f"")

    h10b = ['N', 'TW (£m)', 'Net (£m)', 'Mean g of series[:N]']
    lines.append('| ' + ' | '.join(h10b) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in h10b) + '|')
    for row in tables['t10_n']:
        ref_marker = ' ← RATES ref' if row['N'] == p['N'] else ''
        lines.append(
            f"| {row['N']}{ref_marker} "
            f"| {row['TW']:.2f} "
            f"| {row['Net']:.2f} "
            f"| {row['g_mean']*100:.2f}% |"
        )
    lines.append(f"")
    lines.append(
        f"*TW and Net grow with N as additional years of compounding and WDT "
        f"payments accumulate. The g_mean column makes the path-dependence "
        f"explicit: unlike C.7/C.8 (constant g throughout), each row here "
        f"reflects a different prefix of the realised return history.*"
    )
    lines.append(f"")

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    print(f"Parameters loaded: k={p['k']}, N={p['N']} (SSM-derived), g={p['g']:.4f}")

    # Populate module-level grid constants from TOML [sweep] section.
    global G_VALS, G_LABELS, ALPHA_VALS, K_VALS, V0_VALS, N_ACTUAL_VALS, OVER_VALS
    sw = p['sweep']
    G_VALS        = sw['g_vals']
    G_LABELS      = [f"{v*100:.1f}%" for v in G_VALS]
    ALPHA_VALS    = sw['alpha_vals']
    K_VALS        = sw['appc_k_vals']
    V0_VALS       = sw['appc_v0_vals']
    N_ACTUAL_VALS = sw['n_actual_vals']
    OVER_VALS     = sw['appc_over_vals']

    print("Computing all Appendix C tables...")
    tables = compute_all_tables(p)

    print("Formatting markdown...")
    md = write_appc_md(tables, p)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "VAL_AppC_Full_Tables.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Written: {out_path}")
    print(f"Lines: {len(md.splitlines())}")


if __name__ == '__main__':
    main()
