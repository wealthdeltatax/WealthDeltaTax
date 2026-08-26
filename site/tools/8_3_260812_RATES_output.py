"""
WDT Rates and Revenue — Output Driver
=======================================
Imports rates_model and produces all outputs:
  • Dated Markdown report  (7_5_YYMMDD_WDT_Rates_Revenue_Output.md)
  • Seven figures saved as PNG

Usage
-----
  python3 rates_output.py [params.toml] [output_dir]

  params.toml   defaults to 7_4_260807_WDT_Rates_and_Revenue_Params.toml
                in the same directory as this script.
  output_dir    defaults to ./OUTPUTS/

Figures produced
----------------
  rates_fig_01_sweep_breakeven_coverage.png
      Start-year sweep scatter: LRR breakeven year and TCM coverage ratio.

  rates_fig_02_revenue_concentration_heatmap.png
      Revenue concentration heatmap: cohort share of total revenue (%).

  rates_fig_03_terminal_wealth_by_tier.png
      Terminal net worth at year N by growth tier, upper brackets only.

  rates_fig_04_srr_lrr_trajectory.png
      SRR and LRR reserve trajectories over the capitalisation window.

  rates_fig_05_coverage_by_cycle.png
      TCM coverage ratio distribution by economic cycle (box plots).

  rates_fig_06_burden_matrix_heatmap.png
      Two-panel heatmap: annual wealth burden (% net worth) and effective
      rate on gains (% annual gain), 4 tiers × 10 brackets.

  rates_fig_07_ssm_tcm_coverage_range.png
      Per-start-year coverage range: SSM floor and TCM ceiling connected
      as a band, coloured by economic cycle, 100% reference line.

  rates_fig_08_loss_year_mechanics.png        [NEW]
      Loss-year mechanics: year-by-year gross tax and symmetric refund
      for the 95th percentile bracket, Good tier, 2006 scenario, years
      1–10 (calendar 2006–2015). 2008 crash year highlighted.

  rates_fig_09_phase_two_transition.png       [NEW]
      LRR trajectory over the full 71-year window. Pre-fill accumulation,
      then two post-fill paths: zero-governance depletion (modelled) and
      illustrative rate-recalibration line growing at the UK budget rate.
"""

import sys
import math
import datetime
from pathlib import Path

import rates_model as model

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.ticker
    import numpy as np
    _MPL = True
except ImportError:
    _MPL = False

DEFAULT_PARAMS = Path(__file__).parent / '260812_WDT_Params.toml'
OUTPUT_DIR     = Path(__file__).parent / 'OUTPUTS/RATES'

CYCLE_BUCKETS_CHART = [
    ('Post-war growth 1947–59',  1947, 1959, '#4e79a7'),
    ('Long boom 1960–79',        1960, 1979, '#f28e2b'),
    ('Liberalisation 1980–99',   1980, 1999, '#59a14f'),
    ('Crisis decade 2000–19',    2000, 2019, '#e15759'),
]


# ─────────────────────────────────────────────────────────────
# MARKDOWN HELPERS
# ─────────────────────────────────────────────────────────────

def _fmt_gbp(v, threshold=0.5):
    """Format a £/yr value; suppress near-zero values."""
    return '£—' if abs(v) < threshold else f'£{v:,.0f}'


def _fmt_m(v, threshold=0.0005):
    """Format a £m/yr revenue value; suppress near-zero."""
    return '£—' if abs(v) < threshold else f'£{v:,.0f}'


# ─────────────────────────────────────────────────────────────
# MARKDOWN REPORT
# ─────────────────────────────────────────────────────────────

def write_output_md(p, py_ssm, py_tcm, tcm_N, sweep_extremals, stats,
                    tcm_pf_cov=None, ssm_pf_cov=None,
                    pf_avg_budget=None, pf_years=0,
                    total_post_fill_rev=None,
                    output_dir=None):
    """
    Write a self-contained Markdown run report.

    Sections
    --------
    1.  Active parameters
    2.  SSM results — active scenario
    3.  TCM results — N periods
        3a  Net worth at start and year N
        3b  Net per taxpayer per year (capitalisation window)
        3c  Annual wealth burden
        3d  Effective rate on gains
        3e  Average annual net tax (lifetime)
        3f  Population distribution
        3g  Tax collected per year (capitalisation window)
        3h  Cohort proportion of total tax paid
        3i  Revenue by tier
    4.  Start-year sweep
    5.  Statistical pass
    """
    run_date = datetime.date.today().strftime('%y%m%d')
    meta     = p.get('meta', {})
    scenario = meta.get('scenario_label', 'unknown')
    fname    = f"7_5_{run_date}_WDT_Rates_Revenue_Output.md"
    out_dir  = Path(output_dir) if output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / fname

    lines = []
    A = lines.append

    diffs    = [t['differential'] for t in p['tiers']]
    tlabels  = [f"{t['differential']:+.2%} ({t['label']})" for t in p['tiers']]
    blabels  = [b['label'] for b in p['brackets']]
    tweights = [t['weight'] for t in p['tiers']]

    # ── header ────────────────────────────────────────────────
    A('# WDT Rates and Revenue — Model Output')
    A('')
    A(f'**Run date:** {datetime.date.today().isoformat()}  ')
    A(f'**Scenario:** {scenario}  ')
    A(f'**Model version:** {meta.get("version", "v6")}  ')
    A(f'**Parameters file:** `{DEFAULT_PARAMS.name}`  ')
    A('')

    # ── 1. Active parameters ──────────────────────────────────
    A('## 1. Active Parameters')
    A('')
    A('| Parameter | Value |')
    A('|---|---|')
    A(f'| $\tau_0$ (floor rate) | {p["tau_0"]:.0%} |')
    A(f'| $\tau_m$ (ceiling rate) | {p["tau_m"]:.0%} |')
    A(f'| k (steepness, per £m) | {p["k"]} |')
    A(f'| W_min (£m) | £{p["W_min"]}m |')
    A(f'| SRR capitalisation ratio | {p["srr_ratio"]}× |')
    A(f'| LRR floor (years of expenditure) | {p["lrr_years"]} years |')
    A(f'| Budget base (£b) | £{p["budget_base"]:,.1f}b |')
    A(f'| Budget growth (p.a.) | {p["budget_growth"]:.2%} |')
    A(f'| Historical mean return | {p["hist_mean"]:.2%} |')
    A('')
    A('**Growth tiers:**')
    A('')
    A('| Tier | Weight | Differential | Implied return |')
    A('|---|---|---|---|')
    for t in p['tiers']:
        implied = p['hist_mean'] + t['differential']
        A(f'| {t["label"]} | {t["weight"]:.0%} | {t["differential"]:+.2%} | {implied:.2%} |')
    A('')

    # ── 2. SSM summary ────────────────────────────────────────
    A('## 2. SSM Results — Active Scenario')
    A('')
    py_srr_fill = next((r for r in py_ssm
                        if r['srr_target'] > 0
                        and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)
    py_breach   = next((r for r in py_ssm if r['lrr_balance'] < 0), None)
    py_min_lrr  = min(r['lrr_balance'] for r in py_ssm)

    srr_fill_yr  = py_srr_fill['year'] if py_srr_fill else '—'
    lrr_fill_yr  = py_lrr_fill['year'] if py_lrr_fill else '—'
    srr_at_lrr   = f'£{py_lrr_fill["srr_balance"]:,.0f}b' if py_lrr_fill else '—'
    lrr_surp     = (f'£{(py_lrr_fill["lrr_balance"] - py_lrr_fill["lrr_target"]):,.0f}b'
                    if py_lrr_fill else '—')
    breach_yr    = py_breach['year'] if py_breach else 'no breach'
    gap          = (py_breach['year'] - py_lrr_fill['year']
                    if (py_breach and py_lrr_fill) else '—')
    budget_at_lrr = f'£{py_lrr_fill["budget"]:,.0f}b' if py_lrr_fill else '—'

    A('| Metric | Value |')
    A('|---|---|')
    A(f'| SRR fill year | {srr_fill_yr} |')
    A(f'| LRR breakeven year | {lrr_fill_yr} |')
    A(f'| Annual expenditure at LRR breakeven (£b) | {budget_at_lrr} |')
    A(f'| SRR balance at LRR breakeven (£b) | {srr_at_lrr} |')
    A(f'| LRR surplus at breakeven (£b) | {lrr_surp} |')
    A(f'| LRR first breach year | {breach_yr} |')
    A(f'| LRR breach lag (years) | {gap} |')
    A(f'| Minimum LRR balance in window (£b) | £{py_min_lrr:,.0f}b |')
    if ssm_pf_cov is not None:
        A(f'| Capitalisation window (years) | {pf_years} |')
        A(f'| Avg expenditure — capitalisation window (£b/yr) | £{pf_avg_budget:,.1f}b |')
        A(f'| **SSM coverage ratio** | **{ssm_pf_cov:.1%}** |')
        A('')
        A('*SSM coverage ratio: average annual SSM net income over the capitalisation window '
          '(SRR fill to LRR breakeven) divided by average annual expenditure over the same '
          'window. The SSM applies uniform historical returns across the population '
          '(correlated-shock assumption); TCM coverage appears in §3.*')
    A('')

    # ── 3. TCM matrices ───────────────────────────────────────
    A(f'## 3. TCM Results — N={tcm_N} periods')
    A('')

    # 3a. Net worth
    A('### 3a. Net worth — start ($V_0$) and year N (£m)')
    A('')
    A('*$V_0$ is the bracket mean wealth (£m) at entry, identical across tiers within a '
      'bracket. V_N is the true wealth (before tax settlement) at the end of period N '
      'for a representative taxpayer, varying by tier due to persistent return '
      'differentials. Figures are for a single representative taxpayer; they do not '
      'reflect aggregate portfolio wealth.*')
    A('')
    header = '| Net worth (£m) |' + ''.join(f' {b} |' for b in blabels)
    sep    = '|---|' + '---|' * len(blabels)
    A(header); A(sep)
    A('| **$V_0$ (start, all tiers)** |'
      + ''.join(f' £{b["V0_m"]:,.3f}m |' for b in p['brackets']))
    for i, diff in enumerate(diffs):
        vals = [r['V_at_N'] for r in py_tcm[diff]]
        A(f'| **V_N {tlabels[i]}** |' + ''.join(f' £{v:,.2f}m |' for v in vals))
    A('')

    # 3b. Net per taxpayer — capitalisation window
    A('### 3b. Net per taxpayer per year — capitalisation window average (£/yr)')
    A('')
    A('*Average annual net tax per representative taxpayer over the capitalisation '
      'window (SRR fill year to LRR breakeven year). Zeros suppressed.*')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['post_fill_net_gbp'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {_fmt_gbp(v)} |' for v in vals))
    A('')

    # 3c. Annual wealth burden
    A('### 3c. Annual wealth burden (tax as % of net worth)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['wealth_burden'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {v:.2%} |' for v in vals))
    A('')

    # 3d. Effective rate on gains
    A('### 3d. Effective rate on gains (tax as % of annual gain)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['eff_rate'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {v:.1%} |' for v in vals))
    A('')

    # 3e. Lifetime average net tax
    A('### 3e. Average annual net tax per taxpayer — lifetime average (£/yr)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['avg_net_gbp'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {_fmt_gbp(v)} |' for v in vals))
    A('')

    # 3f. Population distribution
    A('### 3f. Population distribution (taxpayers per bracket per tier)')
    A('')
    A('*Cell population = bracket population × tier weight. '
      'Bracket population is constant within a bracket across tiers.*')
    A('')
    A('| Tier (weight) \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        pop_vals = [r['cell_pop'] for r in py_tcm[diff]]
        A(f'| {tweights[i]:.0%} ({p["tiers"][i]["label"]}) |'
          + ''.join(f' {int(round(v)):,} |' for v in pop_vals))
    A('')

    # 3g. Tax collected per year — capitalisation window
    A('### 3g. Tax collected per year — capitalisation window average (£m/yr)')
    A('')
    A('*Average annual revenue per bracket-tier cell over the capitalisation window. '
      'Row total is the sum across all brackets for that tier. '
      'Column total is the sum across all tiers for that bracket. '
      'Grand total is in the bottom-right cell.*')
    A('')
    A('| Tier (weight) \\ Bracket |' + ''.join(f' {b} |' for b in blabels) + ' **Row total** |')
    A('|---|' + '---|' * len(blabels) + '---|')

    col_totals  = [0.0] * len(blabels)
    grand_total = 0.0
    for i, diff in enumerate(diffs):
        rev_vals  = [r['post_fill_revenue_m'] for r in py_tcm[diff]]
        row_total = sum(rev_vals)
        grand_total += row_total
        for j, v in enumerate(rev_vals):
            col_totals[j] += v
        A(f'| {tweights[i]:.0%} ({p["tiers"][i]["label"]}) |'
          + ''.join(f' {_fmt_m(v)} |' for v in rev_vals)
          + f' **£{row_total:,.1f}m** |')
    A('| **Column total** |'
      + ''.join(f' **£{v:,.1f}m** |' for v in col_totals)
      + f' **£{grand_total:,.1f}m** |')
    A('')
    A('*Row totals in £b/yr:*')
    A('')
    A('| Tier (weight) | £b/yr |')
    A('|---|---|')
    for i, diff in enumerate(diffs):
        row_b = sum(r['post_fill_revenue_m'] for r in py_tcm[diff]) / 1000
        A(f'| {tweights[i]:.0%} ({p["tiers"][i]["label"]}) | £{row_b:,.2f}b |')
    A(f'| **Grand total** | **£{grand_total / 1000:,.2f}b** |')
    A('')

    # 3h. Cohort proportion
    A('### 3h. Cohort proportion of total tax paid (%)')
    A('')
    A('*Each cell\'s capitalisation-window revenue as a percentage of the grand total. '
      'Row total is the tier\'s share; column total is the bracket\'s share across all tiers.*')
    A('')
    A('| Tier (weight) \\ Bracket |' + ''.join(f' {b} |' for b in blabels) + ' **Row total** |')
    A('|---|' + '---|' * len(blabels) + '---|')

    col_prop_totals = [0.0] * len(blabels)
    for i, diff in enumerate(diffs):
        rev_vals      = [r['post_fill_revenue_m'] for r in py_tcm[diff]]
        row_pct_total = 0.0
        cell_pcts     = []
        for j, v in enumerate(rev_vals):
            pct_val = (v / grand_total * 100) if grand_total > 0 else 0.0
            cell_pcts.append(pct_val)
            col_prop_totals[j] += pct_val
            row_pct_total      += pct_val
        A(f'| {tweights[i]:.0%} ({p["tiers"][i]["label"]}) |'
          + ''.join(f' {v:.1f}% |' for v in cell_pcts)
          + f' **{row_pct_total:.1f}%** |')
    A('| **Column total** |'
      + ''.join(f' **{v:.1f}%** |' for v in col_prop_totals)
      + ' **100.0%** |')
    A('')

    # 3i. Revenue by tier
    A('### 3i. Revenue by tier (£b/yr)')
    A('')
    A('| Tier | Lifetime avg (£b/yr) | Capitalisation window avg (£b/yr) |')
    A('|---|---|---|')
    total_rev = 0.0
    for i, diff in enumerate(diffs):
        subtotal    = sum(r['revenue_m']           for r in py_tcm[diff]) / 1000
        pf_subtotal = sum(r['post_fill_revenue_m'] for r in py_tcm[diff]) / 1000
        total_rev  += subtotal
        A(f'| {tlabels[i]} | £{subtotal:,.1f}b | £{pf_subtotal:,.1f}b |')
    if total_post_fill_rev is not None:
        A(f'| **Total** | **£{total_rev:,.1f}b** | **£{total_post_fill_rev:,.1f}b** |')
    else:
        A(f'| **Total** | **£{total_rev:,.1f}b** | — |')
    A('')
    if py_lrr_fill:
        A('*TCM horizon N is derived from the SSM LRR breakeven year, not the TOML snapshot_N.*')
        A('')
        A('**TCM coverage ratio:**')
        A('')
        if tcm_pf_cov is not None and pf_avg_budget is not None:
            A('| Metric | Value |')
            A('|---|---|')
            A(f'| Avg revenue — capitalisation window (£b/yr) | £{total_post_fill_rev:,.1f}b |')
            A(f'| Avg expenditure — capitalisation window (£b/yr) | £{pf_avg_budget:,.1f}b |')
            A(f'| Capitalisation window (years) | {pf_years} |')
            A(f'| **TCM coverage ratio** | **{tcm_pf_cov:.1%}** |')
            A('')
            A('*TCM coverage ratio: average annual TCM revenue over the capitalisation window '
              'divided by average annual expenditure over the same window. The TCM applies '
              'heterogeneous tier differentials to the actual historical return series, '
              'producing higher revenue than the SSM\'s uniform-return assumption. The SSM '
              'coverage ratio (solvency/stress-test perspective) appears in §2.*')
            A('')
        else:
            A('*TCM coverage not available — LRR fill not reached within modelling window.*')
        A('')

    # ── 4. Sweep ──────────────────────────────────────────────
    A('## 4. Start-Year Sweep')
    A('')
    A(f'All figures at $\tau_0$={p["tau_0"]:.0%}, $\tau_m$={p["tau_m"]:.0%}, '
      f'k={p["k"]}, W_min=£{p["W_min"]}m.')
    A('')

    if sweep_extremals:
        A('### Extremals — three dimensions')
        A('')
        A('| Dimension | Start year | LRR breakeven | LRR surplus (£b) '
          '| LRR breach lag | Peak LRR deficit (£b) |')
        A('|---|---|---|---|---|---|')
        for dim_label, r in [
            ('Speed — slowest LRR breakeven',    sweep_extremals.get('worst_speed')),
            ('Speed — fastest LRR breakeven',    sweep_extremals.get('best_speed')),
            ('Safety — thinnest surplus',        sweep_extremals.get('worst_margin')),
            ('Safety — largest surplus',         sweep_extremals.get('best_margin')),
            ('Durability — shortest breach lag', sweep_extremals.get('worst_durable')),
            ('Durability — longest breach lag',  sweep_extremals.get('best_durable')),
        ]:
            if r is None:
                A(f'| {dim_label} | — | — | — | — | — |')
            else:
                lag_str = (f'{r["years_fill_to_breach"]} years'
                           if r['years_fill_to_breach'] is not None else 'no breach')
                A(f'| {dim_label} | {r["calendar_year"]} | {r["lrr_fill_year"]} | '
                  f'£{r["lrr_surplus_at_fill"]:,.0f}b | {lag_str} | '
                  f'£{r["max_lrr_breach"]:,.0f}b |')
        A('')
        nb = sweep_extremals.get('nobreach_count', 0)
        if nb:
            A(f'*{nb} start years produce no LRR breach within the 71-year modelling window.*')
            A('')

        scenario_start = p.get('scenario_start_year')
        all_rows = sweep_extremals.get('all', [])
        A(f'### Full sweep table (all {len(all_rows)} calendar years)')
        A('')
        A('| Start | SRR fill | LRR breakeven | LRR surplus (£b) | SRR at breakeven (£b) '
          '| LRR breach | Breach lag | Peak LRR deficit (£b) | SRR breach | SRR deficit (£b) '
          '| LRR at SRR breach (£b) | SRR breach covered | SSM coverage | TCM coverage |')
        A('|:---:|:---:|:---:|---:|---:|:---:|:---:|---:|:---:|---:|---:|:---:|---:|---:|')

        for r in all_rows:
            def _c(v): return str(v) if v is not None else '—'
            lrr_s  = (f'{r["lrr_surplus_at_fill"]:,.0f}'
                      if r['lrr_fill_year'] is not None else '—')
            srr_l  = (f'{r["srr_balance_at_lrr_fill"]:,.0f}'
                      if r['lrr_fill_year'] is not None else '—')
            lrr_ab = (f'{r["lrr_bal_at_srr_breach"]:,.0f}'
                      if r['lrr_bal_at_srr_breach'] is not None else '—')
            ssm_str = (f'{r["ssm_post_fill_coverage"]:.1%}'
                       if r.get('ssm_post_fill_coverage') is not None else '—')
            tcm_str = (f'{r["tcm_post_fill_coverage"]:.1%}'
                       if r.get('tcm_post_fill_coverage') is not None else '—')
            cov = ('YES' if r['srr_breach_covered'] is True
                   else ('NO' if r['srr_breach_covered'] is False else '—'))
            yr  = r['calendar_year']
            bold = scenario_start and yr == scenario_start
            b = '**' if bold else ''
            A(f'| {b}{yr}{b} | {b}{_c(r["srr_fill_year"])}{b} | '
              f'{b}{_c(r["lrr_fill_year"])}{b} | {b}{lrr_s}{b} | {b}{srr_l}{b} | '
              f'{b}{_c(r["lrr_breach_year"])}{b} | {b}{_c(r["years_fill_to_breach"])}{b} | '
              f'{b}{r["max_lrr_breach"]:,.0f}{b} | {b}{_c(r["srr_breach_year"])}{b} | '
              f'{b}{r["srr_breach_magnitude"]:,.0f}{b} | {b}{lrr_ab}{b} | '
              f'{b}{cov}{b} | {b}{ssm_str}{b} | {b}{tcm_str}{b} |')

        A('')
        A('*Active scenario shown in bold. SRR breach covered: LRR balance at SRR breach year '
          '≥ SRR deficit. Peak LRR deficit: worst LRR balance in the 71-year window under the '
          'zero-governance assumption. Coverage ratios: capitalisation window averages '
          '(SRR fill to LRR breakeven).*')
        A('')

    # ── 5. Statistical pass ───────────────────────────────────
    A('## 5. Statistical Pass — P(success) Across Economic Cycles')
    A('')
    A('**Success definition:** LRR fills within the 71-year window AND '
      '(SRR never breaches OR SRR breach is fully covered by LRR balance at time of breach).')
    A('')
    if stats:
        ov = stats['overall']
        A(f'### Overall (all {ov["n_total"]} start years)')
        A('')
        A('| Metric | Value |')
        A('|---|---|')
        A(f'| Success rate | {ov["success_rate"]:.1f}% ({ov["n_success"]}/{ov["n_total"]}) |')
        A(f'| LRR fills | {ov["lrr_fill_rate"]:.1f}% ({ov["n_lrr_fills"]}/{ov["n_total"]}) |')
        A(f'| SRR breaches | {ov["srr_breach_rate"]:.1f}% ({ov["n_srr_breach"]}/{ov["n_total"]}) |')
        cb = stats['covered_breakdown']
        A(f'| — of which covered | {ov["n_srr_covered"]} |')
        A(f'| — of which uncovered | {ov["n_srr_uncovered"]} |')
        A(f'| No SRR breach | {cb["no_srr_breach"]} |')
        A('')
        A('### By economic cycle')
        A('')
        A('| Period | N | Success% | LRR fill% |')
        A('|---|:---:|:---:|:---:|')
        for b in stats['by_bucket']:
            A(f'| {b["label"]} | {b["n"]} | {b["success_rate"]:.1f}% | {b["lrr_fill_rate"]:.1f}% |')
        A('')
        A('### Key metric distributions')
        A('')
        A('| Metric | N | Min | Median | Mean | Max |')
        A('|---|:---:|---:|---:|---:|---:|')
        dist_rows = [
            ('lrr_fill_year',          'LRR breakeven year',            lambda v: f'{v:,.0f}'),
            ('srr_fill_year',          'SRR fill year',                 lambda v: f'{v:,.0f}'),
            ('lrr_surplus_at_fill',    'LRR surplus at breakeven (£b)', lambda v: f'{v:,.0f}'),
            ('years_fill_to_breach',   'LRR breach lag (yrs)',          lambda v: f'{v:,.0f}'),
            ('max_lrr_breach',         'Peak LRR deficit (£b)',         lambda v: f'{v:,.0f}'),
            ('srr_breach_magnitude',   'SRR deficit at breach (£b)',    lambda v: f'{v:,.0f}'),
            ('ssm_post_fill_coverage', 'SSM coverage ratio',            lambda v: f'{v:.1%}'),
            ('tcm_post_fill_coverage', 'TCM coverage ratio',            lambda v: f'{v:.1%}'),
        ]
        for key, label, fmt_fn in dist_rows:
            d = stats['distributions'][key]
            def _f(v, fn=fmt_fn): return fn(v) if v is not None else '—'
            A(f'| {label} | {d["n"]} | {_f(d["min"])} | {_f(d["median"])} '
              f'| {_f(d["mean"])} | {_f(d["max"])} |')
        A('')

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    return out_path


# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────

def _apply_base_style():
    plt.rcParams.update({
        'font.family':       'serif',
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'axes.grid':         True,
        'grid.alpha':        0.3,
        'grid.linestyle':    '--',
        'figure.dpi':        300,
    })


def _save(fig, output_dir, name):
    path = Path(output_dir) / name
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {name}')
    return path


# ─────────────────────────────────────────────────────────────
# FIGURES 01–05  (unchanged from 7_3)
# ─────────────────────────────────────────────────────────────

def _fig01_sweep_breakeven_coverage(p, sweep_results, output_dir):
    """Fig 01 — Start-year sweep scatter: breakeven year and TCM coverage."""
    _apply_base_style()
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    active_year = p['scenario_start_year']

    for label, yr_from, yr_to, colour in CYCLE_BUCKETS_CHART:
        bucket = [r for r in sweep_results
                  if yr_from <= r['calendar_year'] <= yr_to
                  and r['calendar_year'] != active_year]
        if not bucket:
            continue
        years    = [r['calendar_year'] for r in bucket]
        breakevn = [r['lrr_fill_year'] for r in bucket]
        coverage = [r['tcm_post_fill_coverage'] * 100
                    if r['tcm_post_fill_coverage'] is not None else None
                    for r in bucket]
        ax1.scatter(years, breakevn, color=colour, s=40, alpha=0.8, label=label, zorder=3)
        cov_pairs = [(y, c) for y, c in zip(years, coverage) if c is not None]
        if cov_pairs:
            cy, cc = zip(*cov_pairs)
            ax2.scatter(cy, cc, color=colour, s=40, alpha=0.4, marker='^', zorder=3)

    active = next((r for r in sweep_results if r['calendar_year'] == active_year), None)
    if active:
        ax1.scatter([active_year], [active['lrr_fill_year']],
                    color='black', s=120, zorder=5, marker='D',
                    label=f'{active_year} (active scenario)')
        if active['tcm_post_fill_coverage'] is not None:
            ax2.scatter([active_year], [active['tcm_post_fill_coverage'] * 100],
                        color='black', s=120, zorder=5, marker='^')

    # Ensure the right axis has headroom above the observed TCM maximum
    all_tcm = [r['tcm_post_fill_coverage'] * 100
               for r in sweep_results
               if r.get('tcm_post_fill_coverage') is not None]
    if all_tcm:
        ax2.set_ylim(0, max(all_tcm) * 1.10)

    ax1.set_xlabel('Start year', fontsize=11)
    ax1.set_ylabel('LRR breakeven year', fontsize=11)
    ax2.set_ylabel('TCM coverage ratio (%)', fontsize=11)
    ax1.set_title(
        'Start-year sweep: LRR breakeven and TCM coverage ratio\n'
        'Circles = breakeven year (left axis)  |  Triangles = TCM coverage (right axis)',
        fontsize=11, pad=12)
    handles = [mpatches.Patch(color=c, label=l) for l, _, _, c in CYCLE_BUCKETS_CHART]
    handles.append(plt.Line2D([0], [0], marker='D', color='black', linestyle='None',
                               markersize=8, label=f'{active_year} (active scenario)'))
    ax1.legend(handles=handles, fontsize=9, loc='upper left')
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_01_sweep_breakeven_coverage.png')


def _fig02_revenue_concentration_heatmap(p, py_tcm, output_dir):
    """Fig 02 — Revenue concentration heatmap (cohort share %)."""
    _apply_base_style()
    diffs   = [t['differential'] for t in p['tiers']]
    tlabels = [f"{t['differential']:+.2%}\n({t['label']})" for t in p['tiers']]
    blabels = [b['label'] for b in p['brackets']]
    grand_total = sum(r['post_fill_revenue_m'] for d in diffs for r in py_tcm[d])
    matrix = np.zeros((len(diffs), len(blabels)))
    for i, diff in enumerate(diffs):
        for j, r in enumerate(py_tcm[diff]):
            matrix[i, j] = (r['post_fill_revenue_m'] / grand_total * 100
                            if grand_total > 0 else 0.0)
    fig, ax = plt.subplots(figsize=(13, 4))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    ax.set_xticks(range(len(blabels))); ax.set_xticklabels(blabels, fontsize=9)
    ax.set_yticks(range(len(diffs)));   ax.set_yticklabels(tlabels, fontsize=9)
    ax.set_xlabel('Wealth percentile bracket', fontsize=10)
    ax.set_ylabel('Growth tier', fontsize=10)
    ax.set_title('Revenue concentration: cohort share of total capitalisation-window revenue (%)\n'
                 'RATES.A §B.3h  |  Revenue dip at 90th pct reflects population-weight step: '
                 'bracket population halves at 90th percentile boundary',
                 fontsize=9, pad=12)
    for i in range(len(diffs)):
        for j in range(len(blabels)):
            val = matrix[i, j]
            ax.text(j, i, f'{val:.1f}%', ha='center', va='center',
                    fontsize=8, color='white' if val > 6 else 'black', fontweight='bold')
    fig.colorbar(im, ax=ax, shrink=0.8).set_label('Share of total revenue (%)', fontsize=9)
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_02_revenue_concentration_heatmap.png')


def _fig03_terminal_wealth_by_tier(p, py_tcm, tcm_N, output_dir):
    """Fig 03 — Terminal net worth by tier, upper brackets, log scale."""
    _apply_base_style()
    diffs      = [t['differential'] for t in p['tiers']]
    tlabels    = [f"{t['label']} ({t['differential']:+.2%})" for t in p['tiers']]
    tier_cols  = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759']
    upper_idx  = list(range(4, 10))
    upper_lbl  = [p['brackets'][i]['label'] for i in upper_idx]
    v0_vals    = [p['brackets'][i]['V0_m']  for i in upper_idx]
    fig, ax    = plt.subplots(figsize=(13, 6))
    n_series   = len(diffs) + 1
    width      = 0.12
    x          = np.arange(len(upper_idx))
    offsets    = np.linspace(-(n_series - 1) / 2 * width,
                              (n_series - 1) / 2 * width, n_series)
    ax.bar(x + offsets[0], v0_vals, width=width, color='#bab0ac',
           label='$V_0$ (starting wealth)', zorder=3)
    for k, diff in enumerate(diffs):
        vn_vals = [py_tcm[diff][i]['V_at_N'] for i in upper_idx]
        ax.bar(x + offsets[k + 1], vn_vals, width=width,
               color=tier_cols[k], label=tlabels[k], zorder=3)
    ax.set_yscale('log')
    ax.set_xticks(x); ax.set_xticklabels(upper_lbl, fontsize=10)
    ax.set_xlabel('Wealth percentile bracket', fontsize=11)
    ax.set_ylabel('Wealth (£m, log scale)', fontsize=11)
    ax.set_title(
        f'Terminal net worth at year N={tcm_N}: $V_0$ (starting) and V_N (pre-settlement) by tier\n'
        'RATES.A §B.3a — WDT paid throughout; compounding base intact',
        fontsize=11, pad=12)
    ax.legend(fontsize=9, loc='upper left')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}m'))
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_03_terminal_wealth_by_tier.png')


def _fig04_srr_lrr_trajectory(p, py_ssm, output_dir):
    """Fig 04 — SRR and LRR trajectories over the capitalisation window."""
    _apply_base_style()
    lrr_fill_yr = next((r['year'] for r in py_ssm if r.get('lrr_filled')), len(py_ssm))
    ssm_clip    = [r for r in py_ssm if r['year'] <= lrr_fill_yr]
    years       = [r['year']        for r in ssm_clip]
    srr_bal     = [r['srr_balance'] for r in ssm_clip]
    lrr_bal     = [r['lrr_balance'] for r in ssm_clip]
    srr_tgt     = [r['srr_target']  for r in ssm_clip]
    lrr_tgt     = [r['lrr_target']  for r in ssm_clip]
    srr_fill    = next((r['year'] for r in ssm_clip
                        if r['srr_target'] > 0
                        and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(years, srr_bal, color='#4e79a7', linewidth=2, label='SRR balance')
    ax.plot(years, srr_tgt, color='#4e79a7', linewidth=1, linestyle='--',
            alpha=0.6, label='SRR target')
    ax.plot(years, lrr_bal, color='#f28e2b', linewidth=2, label='LRR balance')
    ax.plot(years, lrr_tgt, color='#f28e2b', linewidth=1, linestyle='--',
            alpha=0.6, label='LRR target')
    y_max = max(max(lrr_bal), max(lrr_tgt), max(srr_bal))
    if srr_fill:
        ax.axvline(srr_fill, color='#4e79a7', linestyle=':', alpha=0.8)
        ax.text(srr_fill + 0.4, y_max * 0.92, f'SRR fill\nyr {srr_fill}',
                fontsize=8, color='#4e79a7', va='top')
    ax.axvline(lrr_fill_yr, color='#f28e2b', linestyle=':', alpha=0.8)
    ax.text(lrr_fill_yr - 5, y_max * 0.75, f'LRR fill\nyr {lrr_fill_yr}',
            fontsize=8, color='#f28e2b', va='top')

    # Annotate the 2008 crash plateau: the return at simulation year 3 is −5.78%
    # (calendar 2008 in the 2006 scenario). The LRR accumulation visibly flattens here.
    crash_sim_yr = 3   # simulation year corresponding to calendar 2008
    if crash_sim_yr <= lrr_fill_yr:
        lrr_at_crash = next(
            (r['lrr_balance'] for r in ssm_clip if r['year'] == crash_sim_yr), None)
        if lrr_at_crash is not None:
            ax.annotate(
                '2008 crash\n(−5.78% return)',
                xy=(crash_sim_yr, lrr_at_crash),
                xytext=(crash_sim_yr + 3, lrr_at_crash + y_max * 0.06),
                fontsize=7.5, color='#555555',
                arrowprops=dict(arrowstyle='->', color='#555555', lw=0.8))

    ax.set_xlabel('Year from launch', fontsize=11)
    ax.set_ylabel('Reserve balance (£b)', fontsize=11)
    ax.set_title(
        f'SRR and LRR reserve trajectories — {p["scenario_start_year"]} Balanced scenario\n'
        f'Capitalisation window (years 1–{lrr_fill_yr}) '
        f'| Solid = balance  |  Dashed = target',
        fontsize=11, pad=12)
    ax.legend(fontsize=9, loc='upper left')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_04_srr_lrr_trajectory.png')


def _fig05_coverage_by_cycle(sweep_results, output_dir):
    """Fig 05 — TCM coverage ratio distribution by economic cycle (box plots)."""
    _apply_base_style()
    cycle_data, cycle_labels, cycle_cols = [], [], []
    for label, yr_from, yr_to, colour in CYCLE_BUCKETS_CHART:
        vals = [r['tcm_post_fill_coverage'] * 100
                for r in sweep_results
                if yr_from <= r['calendar_year'] <= yr_to
                and r['tcm_post_fill_coverage'] is not None]
        if vals:
            cycle_data.append(vals); cycle_labels.append(label); cycle_cols.append(colour)
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(cycle_data, patch_artist=True, notch=False,
                    medianprops=dict(color='black', linewidth=2))
    for patch, colour in zip(bp['boxes'], cycle_cols):
        patch.set_facecolor(colour); patch.set_alpha(0.7)
    ax.axhline(100, color='black', linestyle='--', linewidth=1,
               alpha=0.5, label='100% expenditure coverage')
    ax.set_xticklabels(cycle_labels, fontsize=9)
    ax.set_ylabel('TCM coverage ratio (%)', fontsize=11)
    ax.set_title(
        'TCM coverage ratio distribution by economic cycle  |  All 73 start years — Balanced parameters\n'
        'TCM coverage pairs with SSM coverage floor (see Fig 07)  |  '
        'Liberalisation outlier ~107%: 1982 start year',
        fontsize=9, pad=12)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_05_coverage_by_cycle.png')


# ─────────────────────────────────────────────────────────────
# FIGURES 06–07  (new)
# ─────────────────────────────────────────────────────────────

def _fig06_burden_matrix_heatmap(p, py_tcm, output_dir):
    """
    Fig 06 — Two-panel burden matrix heatmap.

    Left panel:  annual wealth burden (tax as % of net worth).
    Right panel: effective rate on gains (tax as % of annual gain).
    Both are 4-tier × 10-bracket grids.

    Visual argument: values are low across nearly the entire grid;
    the gradient runs tier-to-tier, not bracket-to-bracket.
    """
    _apply_base_style()
    diffs   = [t['differential'] for t in p['tiers']]
    tlabels = [f"{t['differential']:+.2%}\n({t['label']})" for t in p['tiers']]
    blabels = [b['label'] for b in p['brackets']]
    n_tiers = len(diffs)
    n_bkts  = len(blabels)

    burden_matrix = np.zeros((n_tiers, n_bkts))
    effrate_matrix = np.zeros((n_tiers, n_bkts))
    for i, diff in enumerate(diffs):
        for j, r in enumerate(py_tcm[diff]):
            burden_matrix[i, j]  = r['wealth_burden'] * 100
            effrate_matrix[i, j] = r['eff_rate']      * 100

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(18, 4),
                                      gridspec_kw={'wspace': 0.35})

    for ax, matrix, title, cmap, unit in [
        (ax_l, burden_matrix,  'Annual wealth burden\n(tax as % of net worth)',
         'Blues', '%'),
        (ax_r, effrate_matrix, 'Effective rate on gains\n(tax as % of annual gain)',
         'Oranges', '%'),
    ]:
        im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0)
        ax.set_xticks(range(n_bkts))
        ax.set_xticklabels(blabels, fontsize=8, rotation=40, ha='right')
        ax.set_yticks(range(n_tiers)); ax.set_yticklabels(tlabels, fontsize=8)
        ax.set_xlabel('Wealth percentile bracket', fontsize=9)
        ax.set_ylabel('Growth tier', fontsize=9)
        ax.set_title(title, fontsize=10, pad=10)
        threshold = matrix.max() * 0.55
        for ii in range(n_tiers):
            for jj in range(n_bkts):
                val = matrix[ii, jj]
                txt_col = 'white' if val > threshold else 'black'
                ax.text(jj, ii, f'{val:.2f}{unit}', ha='center', va='center',
                        fontsize=7, color=txt_col)
        cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
        cb.set_label(unit, fontsize=8)

    fig.suptitle(
        'Individual burden matrices — 2006 Balanced scenario, N=34\n'
        'RATES.A §B.3c (left) and §B.3d (right)  |  '
        '0.00% = genuine zero liability (exemption threshold + refund offset); not missing data',
        fontsize=9, y=1.03)
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_06_burden_matrix_heatmap.png')


def _fig07_ssm_tcm_coverage_range(p, sweep_results, output_dir):
    """
    Fig 07 — SSM/TCM coverage range plot.

    For each of the 73 start years, a vertical line segment runs from
    the SSM coverage (floor, circle) to the TCM coverage (ceiling,
    triangle), coloured by economic cycle.  A horizontal 100% reference
    line is drawn.  The active scenario is highlighted in black.

    Visual argument: the SSM–TCM band stays well above zero across all
    start years and all economic cycles; the two ratios bracket the
    plausible revenue range rather than being point estimates.
    """
    _apply_base_style()
    active_year = p['scenario_start_year']

    fig, ax = plt.subplots(figsize=(13, 6))

    for label, yr_from, yr_to, colour in CYCLE_BUCKETS_CHART:
        bucket = [r for r in sweep_results
                  if yr_from <= r['calendar_year'] <= yr_to
                  and r['calendar_year'] != active_year
                  and r.get('ssm_post_fill_coverage') is not None
                  and r.get('tcm_post_fill_coverage') is not None]
        for r in bucket:
            yr  = r['calendar_year']
            ssm = r['ssm_post_fill_coverage'] * 100
            tcm = r['tcm_post_fill_coverage'] * 100
            ax.plot([yr, yr], [ssm, tcm], color=colour, alpha=0.5, linewidth=1.2)
            ax.scatter(yr, ssm, color=colour, s=30, alpha=0.8, zorder=4,
                       marker='o', linewidths=0)
            ax.scatter(yr, tcm, color=colour, s=30, alpha=0.8, zorder=4,
                       marker='^', linewidths=0)

    # Active scenario
    active = next((r for r in sweep_results if r['calendar_year'] == active_year), None)
    if active and active.get('ssm_post_fill_coverage') and active.get('tcm_post_fill_coverage'):
        ssm_a = active['ssm_post_fill_coverage'] * 100
        tcm_a = active['tcm_post_fill_coverage'] * 100
        ax.plot([active_year, active_year], [ssm_a, tcm_a],
                color='black', linewidth=2.0, zorder=6)
        ax.scatter(active_year, ssm_a, color='black', s=80, zorder=7, marker='o')
        ax.scatter(active_year, tcm_a, color='black', s=80, zorder=7, marker='^')
        ax.annotate(f'{active_year}\nSSM {ssm_a:.1f}%\nTCM {tcm_a:.1f}%',
                    xy=(active_year, (ssm_a + tcm_a) / 2),
                    xytext=(active_year + 3, (ssm_a + tcm_a) / 2),
                    fontsize=8, color='black',
                    arrowprops=dict(arrowstyle='->', color='black', lw=0.8))

    ax.axhline(100, color='black', linestyle='--', linewidth=1,
               alpha=0.5, label='100% expenditure coverage')

    ax.set_xlabel('Start year', fontsize=11)
    ax.set_ylabel('Coverage ratio (%)', fontsize=11)
    ax.set_title(
        'SSM/TCM coverage range by start year\n'
        'Circles = SSM floor (correlated-shock)  |  Triangles = TCM ceiling (persistent heterogeneity)  |  '
        'Wider bands in high-mean-return eras: tier differentials compound faster when mean growth is high',
        fontsize=9, pad=12)

    handles = [mpatches.Patch(color=c, label=l) for l, _, _, c in CYCLE_BUCKETS_CHART]
    handles += [
        plt.Line2D([0], [0], marker='o', color='grey', linestyle='None',
                   markersize=7, label='SSM coverage (floor)'),
        plt.Line2D([0], [0], marker='^', color='grey', linestyle='None',
                   markersize=7, label='TCM coverage (ceiling)'),
        plt.Line2D([0], [0], color='black', linewidth=2,
                   label=f'{active_year} (active scenario)'),
    ]
    ax.legend(handles=handles, fontsize=8, loc='upper right')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_07_ssm_tcm_coverage_range.png')


# ─────────────────────────────────────────────────────────────
# FIGURES 08–09  (new)
# ─────────────────────────────────────────────────────────────

def _fig08_loss_year_mechanics(p, py_tcm, output_dir):
    """
    Fig 08 — Loss-year mechanics: symmetric refund in the 2008 crash.

    Uses the 95th percentile bracket, Good tier (+0.95pp differential),
    within the 2006 Balanced scenario.  Simulation year 3 = calendar 2008
    (return −5.78% from the rotated 2006 series).

    Shows years 1–10 (calendar 2006–2015):
      - Bars: gross tax (positive, blue) and gross refund (negative, red)
        per simulation year.
      - Line: cumulative net tax paid to date (right axis), illustrating
        the lifetime contribution envelope.
      - Crash year annotated explicitly.
    """
    _apply_base_style()

    # Locate the 95th percentile bracket index and Good tier differential
    good_diff = next(t['differential'] for t in p['tiers'] if t['label'] == 'Good')
    bracket_95_idx = next(i for i, b in enumerate(p['brackets']) if b['label'] == '95%')
    b95 = p['brackets'][bracket_95_idx]

    # Run the full TCM simulation for this bracket/tier over N=34 periods
    # so we can extract year-by-year L values for years 1–10
    N = 34
    alpha  = 1.0
    returns = p['returns']
    g_series = [returns[t] + good_diff for t in range(1, N + 1)]
    g_sell   = returns[N + 1] + good_diff

    from wdt_core import simulate, simulate_sell_year
    sim = simulate(b95['V0_m'], g_series, alpha, p)

    # Window: simulation years 1–10 (calendar years 2006–2015)
    window_years = list(range(1, 11))
    sim_year_labels = [str(p['scenario_start_year'] + t - 1) for t in window_years]
    crash_sim_yr = 3   # simulation year 3 = calendar 2008

    gross_tax    = [max(0.0, sim[t]['L']) * 1e6 for t in window_years]   # £/yr
    gross_refund = [min(0.0, sim[t]['L']) * 1e6 for t in window_years]   # £/yr (negative)
    cum_net      = []
    running = 0.0
    for t in window_years:
        running += sim[t]['L'] * 1e6
        cum_net.append(running)

    crash_return_pct = returns[crash_sim_yr] * 100   # −5.78%

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    x = np.arange(len(window_years))
    bar_w = 0.55

    # Highlight crash year column background
    crash_x = crash_sim_yr - 1   # 0-indexed in window
    ax1.axvspan(crash_x - 0.45, crash_x + 0.45, color='#fee8e8', zorder=1, alpha=0.9)

    # Bars: gross tax (blue) and gross refund (red)
    ax1.bar(x, gross_tax,    width=bar_w, color='#4e79a7', alpha=0.85,
            label='Gross tax paid (gain year)', zorder=3)
    ax1.bar(x, gross_refund, width=bar_w, color='#e15759', alpha=0.85,
            label='Symmetric refund received (loss year)', zorder=3)

    # Cumulative net line on right axis
    ax2.plot(x, cum_net, color='#333333', linewidth=2, linestyle='-',
             marker='o', markersize=5, zorder=5, label='Cumulative net tax (right axis)')
    ax2.axhline(0, color='#333333', linewidth=0.6, linestyle=':', alpha=0.5)

    # Crash year annotations
    ax1.annotate(
        f'Calendar {p["scenario_start_year"] + crash_sim_yr - 1}\n'
        f'Return: {crash_return_pct:+.2f}%\n'
        f'Refund fires at τ(W)',
        xy=(crash_x, gross_refund[crash_x]),
        xytext=(crash_x + 1.2, gross_refund[crash_x] - abs(gross_refund[crash_x]) * 0.4),
        fontsize=8, color='#c0392b',
        arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.9))

    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [f'{lbl}\n(yr {t})' for lbl, t in zip(sim_year_labels, window_years)],
        fontsize=8.5)
    ax1.set_xlabel('Calendar year  (simulation year)', fontsize=10)
    ax1.set_ylabel('Annual tax / refund (£ per taxpayer)', fontsize=10)
    ax2.set_ylabel('Cumulative net tax paid (£ per taxpayer)', fontsize=10)

    ax1.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}'))
    ax2.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}'))

    fig.suptitle(
        f'Loss-year mechanics: symmetric refund in the 2008 crash\n'
        f'95th percentile bracket ($V_0$ = £{b95["V0_m"]:.3f}m), Good tier (+0.95pp), '
        f'2006 Balanced scenario — simulation years 1–10\n'
        f'Red shading = crash year  |  Refund is bounded by cumulative net tax paid '
        f'(lifetime contribution envelope)',
        fontsize=9, y=1.01)

    # Combined legend
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=8.5, loc='upper left')

    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_08_loss_year_mechanics.png')


def _fig09_phase_two_transition(p, py_ssm, output_dir):
    """
    Fig 09 — Phase Two transition: LRR trajectory beyond LRR fill.

    Shows the full 71-year SSM window for the 2006 Balanced scenario,
    split at the LRR fill year (year 34).

    Pre-fill (years 1–34): LRR balance accumulating toward target.
    Post-fill, two paths:
      - Zero-governance (solid orange): LRR depletes as full annual
        expenditure is charged against it; no rate adjustments assumed.
        This is the modelled output from run_ssm(max_N=71).
      - Illustrative governance (dashed green): LRR balance at year 34
        grows at the UK budget growth rate (5.24% p.a.), representing
        the stylised outcome if rate recalibration keeps revenue pace
        with expenditure.  NOT a model output; explicitly labelled.

    The LRR target is also plotted to show how the expenditure hurdle
    grows throughout the window.
    """
    _apply_base_style()

    lrr_fill_yr = next((r['year'] for r in py_ssm if r.get('lrr_filled')), None)
    if lrr_fill_yr is None:
        print('  Fig 09 skipped: LRR did not fill within modelling window.')
        return None

    years      = [r['year']         for r in py_ssm]
    lrr_bal    = [r['lrr_balance']  for r in py_ssm]
    lrr_tgt    = [r['lrr_target']   for r in py_ssm]
    budget_g   = p['budget_growth']

    # Stylised governance line: start from LRR balance at fill year,
    # grow at budget_growth p.a. for each subsequent year
    lrr_bal_at_fill = next(r['lrr_balance'] for r in py_ssm if r['year'] == lrr_fill_yr)
    gov_years  = [yr for yr in years if yr >= lrr_fill_yr]
    gov_bal    = [lrr_bal_at_fill * (1 + budget_g) ** (yr - lrr_fill_yr)
                  for yr in gov_years]

    # ── split the zero-governance line at fill year for visual clarity ──
    pre_years  = [yr for yr in years if yr <= lrr_fill_yr]
    pre_bal    = [lrr_bal[i] for i, yr in enumerate(years) if yr <= lrr_fill_yr]
    post_years = [yr for yr in years if yr >= lrr_fill_yr]
    post_bal   = [lrr_bal[i] for i, yr in enumerate(years) if yr >= lrr_fill_yr]

    # ── breach detection before plotting ────────────────────────
    breach_yr = next((r['year'] for r in py_ssm
                      if r.get('lrr_filled') and r['lrr_balance'] < 0), None)

    # For log scale, clip the zero-governance post-fill line at a small
    # positive floor (£10b) just before it goes negative, so the depletion
    # path remains visible and the breach point can be annotated explicitly.
    LOG_FLOOR = 10.0   # £b — smallest value plotted on log axis
    post_bal_log = [max(v, LOG_FLOOR) for v in post_bal]
    # Truncate at the first year the true value drops below LOG_FLOOR
    first_below = next(
        (i for i, v in enumerate(post_bal) if v < LOG_FLOOR), len(post_bal))
    post_years_log = post_years[:first_below + 1]
    post_bal_log   = post_bal_log[:first_below + 1]

    # Pre-fill: all positive, safe for log
    pre_bal_log = [max(v, LOG_FLOOR) for v in pre_bal]
    # LRR target: all positive
    lrr_tgt_log = [max(v, LOG_FLOOR) for v in lrr_tgt]

    fig, ax = plt.subplots(figsize=(13, 6))

    # Log scale — straight line for constant-growth governance path
    ax.set_yscale('log')

    # LRR target (growing expenditure hurdle)
    ax.plot(years, lrr_tgt_log, color='#888888', linewidth=1.2, linestyle=':',
            alpha=0.7, label='LRR target (3× annual expenditure)')

    # Pre-fill LRR balance
    ax.plot(pre_years, pre_bal_log, color='#f28e2b', linewidth=2.2,
            label='LRR balance — capitalisation phase')

    # Post-fill zero-governance path (clipped at LOG_FLOOR)
    ax.plot(post_years_log, post_bal_log, color='#e15759', linewidth=2.2, linestyle='-',
            label='Post-fill: zero-governance (no rate adjustment)')

    # Post-fill stylised governance path — straight line on log scale confirms constant growth
    ax.plot(gov_years, gov_bal, color='#59a14f', linewidth=2.2, linestyle='--',
            label=f'Post-fill: illustrative (rate recalibration, +{budget_g:.2%} p.a.)')

    y_max = max(max(gov_bal), max(lrr_tgt_log)) * 2.0
    y_min = LOG_FLOOR * 0.5

    # LRR fill marker
    ax.axvline(lrr_fill_yr, color='#f28e2b', linestyle=':', linewidth=1.2, alpha=0.85)
    ax.text(lrr_fill_yr + 0.5, y_max * 0.35,
            f'LRR fill\n(yr {lrr_fill_yr})\nPhase Two\nviable',
            fontsize=8, color='#c07020', va='top')

    # Annotate the end-state of the zero-governance path
    last_zg_yr  = post_years_log[-1]
    last_zg_val = post_bal_log[-1]
    true_last_val = post_bal[len(post_years_log) - 1]

    if breach_yr:
        # Line clipped at LOG_FLOOR before breach — mark the clip point
        ax.scatter([last_zg_yr], [last_zg_val],
                   color='#e15759', s=60, zorder=6, marker='v')
        ax.annotate(
            f'LRR breaches zero\n(yr {breach_yr}, zero-governance)',
            xy=(last_zg_yr, last_zg_val),
            xytext=(last_zg_yr - 8, last_zg_val * 0.2),
            fontsize=7.5, color='#c03020',
            arrowprops=dict(arrowstyle='->', color='#c03020', lw=0.8))
    else:
        # No breach — mark year-71 endpoint only; narrative in title
        ax.scatter([last_zg_yr], [last_zg_val],
                   color='#e15759', s=50, zorder=6, marker='o')
    ax.set_xlim(0, max(years) + 1)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Year from launch', fontsize=11)
    ax.set_ylabel('LRR balance (£b, log scale)', fontsize=11)

    # In the 2006 scenario the zero-governance red line grows faster than
    # the illustrative governance green line because WDT revenue (compounding
    # on a large and growing wealth base) outpaces expenditure in the later
    # decades of the historical series. The governance line shows what happens
    # if the Governing Council redirects the surplus above the 3× floor
    # target toward the labour dividend rather than letting it accumulate.
    breach_note = (f'Red clipped at £{LOG_FLOOR:.0f}b floor where balance → 0'
                   if breach_yr else
                   'Red grows above green: WDT revenue outpaces expenditure in later decades; '
                   'green = surplus redirected to labour dividend per enumerated clause 6')
    ax.set_title(
        f'Phase Two transition — LRR trajectory beyond LRR fill, 2006 Balanced scenario\n'
        f'Orange = capitalisation phase  |  Red = zero-governance (no rate adjustment)  |  '
        f'Green dashed = illustrative governance (balance grows at {budget_g:.2%} p.a.; '
        f'surplus directed to labour relief)\n'
        f'{breach_note}  |  Illustrative path is NOT a model output',
        fontsize=8.0, pad=12)
    ax.legend(fontsize=8.5, loc='upper left')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))

    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_09_phase_two_transition.png')


# ─────────────────────────────────────────────────────────────
# GENERATE ALL CHARTS
# ─────────────────────────────────────────────────────────────

def generate_charts(p, py_ssm, py_tcm, sweep_results, output_dir=None, tcm_N=None):
    """
    Generate all nine RATES figures and save to output_dir.
    Skips gracefully if matplotlib is unavailable.

    Figures 01–07: core model outputs (sweep, revenue, burden, reserves, coverage).
    Figure 08: loss-year mechanics — symmetric refund in the 2008 crash.
    Figure 09: Phase Two transition — LRR trajectory beyond LRR fill.
    """
    if not _MPL:
        print('  Charts skipped: matplotlib not available.')
        return

    out = Path(output_dir) if output_dir else OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    print('\nGenerating figures...')
    _fig01_sweep_breakeven_coverage(p, sweep_results, out)
    _fig02_revenue_concentration_heatmap(p, py_tcm, out)
    _fig03_terminal_wealth_by_tier(p, py_tcm, tcm_N, out)
    _fig04_srr_lrr_trajectory(p, py_ssm, out)
    _fig05_coverage_by_cycle(sweep_results, out)
    _fig06_burden_matrix_heatmap(p, py_tcm, out)
    _fig07_ssm_tcm_coverage_range(p, sweep_results, out)
    _fig08_loss_year_mechanics(p, py_tcm, out)
    _fig09_phase_two_transition(p, py_ssm, out)
    print('  All figures complete.')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    toml_path  = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # ── load and validate ─────────────────────────────────────
    print(f'Loading parameters from: {toml_path or DEFAULT_PARAMS}')
    p = model.load_params(toml_path)
    model.validate_params(p)

    meta = p.get('meta', {})
    print()
    print('─' * 60)
    print('PARAMETERS')
    print('─' * 60)
    print(f"  scenario:     {meta.get('scenario_label', '—')}")
    print(f"  start year:   {p['scenario_start_year']}")
    print(f"  $\tau_0$={p['tau_0']:.0%}  $\tau_m$={p['tau_m']:.0%}  "
          f"k={p['k']}  W_min=£{p['W_min']}m")
    print(f"  SRR={p['srr_ratio']}×  LRR={p['lrr_years']} yrs")
    print(f"  budget £{p['budget_base']}b  growth {p['budget_growth']:.2%} p.a.")
    print(f"  returns: {len(p['returns'])} values rotated to {p['scenario_start_year']}")

    # ── SSM ───────────────────────────────────────────────────
    print('\nRunning SSM (active scenario, N=1..71)...')
    py_ssm = model.run_ssm(p, max_N=71)

    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)
    py_srr_fill = next((r for r in py_ssm
                        if r['srr_target'] > 0
                        and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
    ssm_lrr_N = py_lrr_fill['year'] if py_lrr_fill else p['tcm_N']
    ssm_srr_N = py_srr_fill['year'] if py_srr_fill else 1

    print(f"  SRR fill year: {py_srr_fill['year'] if py_srr_fill else '—'}")
    print(f"  LRR fill year: {ssm_lrr_N}  (used as TCM N)")
    if py_lrr_fill is None:
        print('  WARNING: LRR did not fill within 71-year window — '
              'TCM will use TOML snapshot_N')

    # ── TCM ───────────────────────────────────────────────────
    print(f'\nRunning TCM (N={ssm_lrr_N}, N_fill={ssm_srr_N}, '
          f'{len(p["brackets"])} brackets × {len(p["tiers"])} tiers)...')
    py_tcm = model.run_tcm(p, N=ssm_lrr_N, N_fill=ssm_srr_N)

    total_rev = sum(
        sum(r['revenue_m'] for r in py_tcm[t['differential']]) / 1000
        for t in p['tiers']
    )
    total_post_fill_rev = sum(
        sum(r['post_fill_revenue_m'] for r in py_tcm[t['differential']]) / 1000
        for t in p['tiers']
    )

    if py_lrr_fill:
        ssm_last      = py_ssm[-1]
        ssm_pf_cov    = ssm_last.get('ssm_post_fill_coverage')
        pf_avg_budget = ssm_last.get('post_fill_avg_budget_b')
        pf_years      = ssm_last.get('post_fill_years', 0)
        tcm_pf_cov    = (total_post_fill_rev / pf_avg_budget
                         if pf_avg_budget and pf_avg_budget > 0 else None)
        print(f'  Lifetime-avg revenue:          £{total_rev:,.1f}b/yr')
        print(f'  Cap. window avg revenue (TCM): £{total_post_fill_rev:,.1f}b/yr')
        if pf_avg_budget:
            print(f'  Cap. window avg expenditure:   £{pf_avg_budget:,.1f}b/yr  '
                  f'({pf_years} years)')
        if tcm_pf_cov  is not None: print(f'  TCM coverage ratio:            {tcm_pf_cov:.1%}')
        if ssm_pf_cov  is not None: print(f'  SSM coverage ratio:            {ssm_pf_cov:.1%}')
    else:
        tcm_pf_cov = ssm_pf_cov = pf_avg_budget = None
        pf_years = 0
        print(f'  Lifetime-avg revenue: £{total_rev:,.1f}b/yr')

    # ── sweep ─────────────────────────────────────────────────
    print(f'\nRunning start-year sweep ({len(p["returns"])} calendar years)...')
    sweep           = model.run_start_year_sweep(p)
    sweep_extremals = model.report_start_year_sweep(sweep, p)

    print('\nRunning extremal scenario profiles...')
    profiles = model.run_scenario_profiles(sweep_extremals, p)
    model.report_scenario_profiles(profiles, p)

    print('\nRunning statistical pass...')
    stats = model.compute_statistics(sweep)
    model.report_statistics(stats, p)

    # ── outputs ───────────────────────────────────────────────
    out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    print('\nWriting output report...')
    out_path = write_output_md(
        p, py_ssm, py_tcm, ssm_lrr_N, sweep_extremals, stats,
        tcm_pf_cov=tcm_pf_cov, ssm_pf_cov=ssm_pf_cov,
        pf_avg_budget=pf_avg_budget, pf_years=pf_years,
        total_post_fill_rev=total_post_fill_rev,
        output_dir=out_dir,
    )
    print(f'  Output written: {out_path}')

    if p.get('generate_charts', False):
        generate_charts(p, py_ssm, py_tcm, sweep,
                        output_dir=out_path.parent, tcm_N=ssm_lrr_N)

    # ── summary ───────────────────────────────────────────────
    print()
    print('=' * 60)
    print('SUMMARY')
    print('=' * 60)
    print(f"  Active scenario:  {meta.get('scenario_label', '—')} "
          f"(start {p['scenario_start_year']})")
    print(f'  SSM LRR breakeven:             N={ssm_lrr_N}')
    print(f'  TCM lifetime-avg revenue:      £{total_rev:,.1f}b/yr')
    if py_lrr_fill and tcm_pf_cov is not None:
        print(f'  TCM cap. window avg revenue:   £{total_post_fill_rev:,.1f}b/yr')
        print(f'  TCM coverage ratio:            {tcm_pf_cov:.1%}')
    if py_lrr_fill and ssm_pf_cov is not None:
        print(f'  SSM coverage ratio:            {ssm_pf_cov:.1%}')
    ov = stats['overall']
    print(f'  Success rate:     {ov["success_rate"]:.1f}%  '
          f'({ov["n_success"]}/{ov["n_total"]} start years)')
    ws = sweep_extremals['worst_speed']
    bs = sweep_extremals['best_speed']
    print(f'  Sweep speed:      worst={ws["calendar_year"] if ws else "—"} '
          f'(N={ws["lrr_fill_year"] if ws else "—"})  '
          f'best={bs["calendar_year"] if bs else "—"} '
          f'(N={bs["lrr_fill_year"] if bs else "—"})')
    print(f'  Output:           {out_path.name}')
    print('\nDone.')


if __name__ == '__main__':
    main()
