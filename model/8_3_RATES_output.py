"""
WDT Rates and Revenue — Output Driver  (v8)
=============================================
Imports rates_model and produces all outputs:
  • Dated Markdown report  (7_5_YYMMDD_WDT_Rates_Revenue_Output.md)
  • Nine figures saved as PNG

Usage
-----
  python3 8_3_260812_RATES_output.py [params.toml] [output_dir]

  params.toml   defaults to WDT_Params.toml in the same directory.
  output_dir    defaults to ./OUTPUTS/RATES/

v8 mechanics changes (rates_model.py):
  - Post-fill uses 5-step priority mechanic (replaces old surplus→LRR pass)
  - New failure conditions: lrr_failure_year, srr_failure_year
  - Coverage fractions tracked in four windows: 5, 10, 20, 50 years
  - TCM runs its own independent post-fill loop
  - Success redefined: LRR fills AND lrr_failure_year is None
  - Retired: lrr_breach_year, years_fill_to_breach, max_lrr_breach,
             srr_breach_covered, ssm/tcm_post_fill_coverage (old single value)
  - Extremals: Speed, Margin, Durability (50yr SSM cov), Resilience (LRR fail)

Figures produced
----------------
  rates_fig_01_sweep_breakeven_coverage.png
      Start-year sweep scatter: LRR breakeven year and 10yr TCM coverage.

  rates_fig_02_revenue_concentration_heatmap.png
      Revenue concentration heatmap: cohort share of total revenue (%).

  rates_fig_03_terminal_wealth_by_tier.png
      Terminal net worth at year N by growth tier, upper brackets only.

  rates_fig_04_srr_lrr_trajectory.png
      SRR and LRR reserve trajectories over the capitalisation window.

  rates_fig_05_coverage_by_cycle.png
      SSM 10yr coverage distribution by economic cycle (box plots, v8).

  rates_fig_06_burden_matrix_heatmap.png
      Two-panel heatmap: annual wealth burden (% net worth) and effective
      rate on gains (% annual gain), 4 tiers × 10 brackets.

  rates_fig_07_ssm_tcm_coverage_range.png
      Per-start-year 10yr coverage range: SSM floor and TCM ceiling as a
      band, coloured by economic cycle, 100% reference line.

  rates_fig_08_loss_year_mechanics.png
      Loss-year mechanics: year-by-year gross tax and symmetric refund
      for the 95th percentile bracket, Good tier, 2006 scenario, years
      1–10 (calendar 2006–2015). 2008 crash year highlighted.

  rates_fig_09_phase_two_transition.png
      LRR trajectory over the full 71-year window. Pre-fill accumulation,
      then two post-fill paths: zero-governance depletion (modelled) and
      illustrative rate-recalibration line growing at the UK budget rate.
"""

import sys
import math
import datetime
from pathlib import Path

import rates_model as model

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker
import numpy as np

from wdt_core import simulate, simulate_sell_year
from wdt_fmt import fmt_gbp_yr, out_dir
from wdt_style import (apply_style, save_fig, CYCLE_BUCKETS,
                        C_SSM, C_TCM, C_LRR, C_BASELINE, C_ANNOTATION)

DEFAULT_PARAMS = Path(__file__).parent / 'WDT_Params.toml'
OUTPUT_DIR     = out_dir('RATES')

# Alias for all internal call sites — unchanged
CYCLE_BUCKETS_CHART = CYCLE_BUCKETS


# ─────────────────────────────────────────────────────────────
# MARKDOWN HELPERS
# ─────────────────────────────────────────────────────────────

# Aliases for wdt_fmt functions — all internal call sites unchanged
_fmt_gbp = fmt_gbp_yr   # fmt_gbp_yr(v, threshold=0.5) → '£12,345' or '£—'
# _fmt_m: original had no 'm' suffix (column header supplies the unit)
_fmt_m   = lambda v, threshold=0.0005: '£—' if abs(v) < threshold else f'£{v:,.0f}'


# ─────────────────────────────────────────────────────────────
# MARKDOWN REPORT
# ─────────────────────────────────────────────────────────────

def write_output_md(p, py_ssm, py_tcm, tcm_N, sweep_extremals, stats,
                    tcm_win=None,
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
    _out     = Path(output_dir) if output_dir else OUTPUT_DIR
    _out.mkdir(parents=True, exist_ok=True)
    out_path = _out / fname

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

    # ── B.1 Active parameters ─────────────────────────────────
    A('## B.1 Active Parameters')
    A('')
    A('| Parameter | Value |')
    A('|---|---|')
    A(f'| $\\tau_0$ (floor rate) | {p["tau_0"]:.0%} |')
    A(f'| $\\tau_m$ (ceiling rate) | {p["tau_m"]:.0%} |')
    A(f'| $k$ (steepness, per £m) | {p["k"]} |')
    A(f'| $W_{{min}}$ (£m) | £{p["W_min"]}m |')
    A(f'| SRR capitalisation ratio | {p["srr_ratio"]}× |')
    A(f'| LRR floor (years of expenditure) | {p["lrr_years"]} years |')
    A(f'| Budget base (£b) | £{p["budget_base"]:,.1f}b |')
    A(f'| Budget growth (p.a). | {p["budget_growth"]:.2%} |')
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

    # ── B.2 SSM summary ───────────────────────────────────────
    A('## B.2 SSM Results — Active Scenario')
    A('')
    # Extract summary fields from the last SSM row (run_ssm attaches them there)
    ssm_last     = py_ssm[-1]
    py_lrr_fill  = next((r for r in py_ssm if r.get('lrr_filled')), None)

    srr_fill_yr   = ssm_last.get('srr_fill_year', '—')
    lrr_fill_yr   = ssm_last.get('lrr_fill_year', '—')
    lrr_fail_yr   = ssm_last.get('lrr_failure_year')
    srr_fail_yr   = ssm_last.get('srr_failure_year')
    fail_gap      = ssm_last.get('lrr_srr_failure_gap')
    srr_at_lrr    = (f'£{py_lrr_fill["srr_balance"]:,.0f}b' if py_lrr_fill else '—')
    lrr_surp      = (f'£{(py_lrr_fill["lrr_balance"] - py_lrr_fill["lrr_target"]):,.0f}b'
                     if py_lrr_fill else '—')
    budget_at_lrr = f'£{py_lrr_fill["budget"]:,.0f}b' if py_lrr_fill else '—'

    def _fv(v, suffix=''):
        return f'{v}{suffix}' if v is not None else '—'

    A('| Metric | Value |')
    A('|---|---|')
    A(f'| SRR fill year | {_fv(srr_fill_yr)} |')
    A(f'| LRR breakeven year | {_fv(lrr_fill_yr)} |')
    A(f'| Annual expenditure at LRR breakeven (£b) | {budget_at_lrr} |')
    A(f'| SRR balance at LRR breakeven (£b) | {srr_at_lrr} |')
    A(f'| LRR surplus at breakeven (£b) | {lrr_surp} |')
    A(f'| LRR failure year | {_fv(lrr_fail_yr, " (buffer exhausted)")} |'
      if lrr_fail_yr else '| LRR failure year | no failure within 71-year window |')
    A(f'| SRR failure year | {_fv(srr_fail_yr, " (refund guarantee broken)")} |'
      if srr_fail_yr else '| SRR failure year | no failure within 71-year window |')
    A(f'| LRR→SRR failure gap (years) | {_fv(fail_gap)} |')
    A('')

    # Coverage windows table
    A('**SSM Step-5 coverage fraction by window (average % of annual expenditure '
      'available for labour tax relief):**')
    A('')
    A('| Window | SSM coverage | Zero-coverage years | Min LRR balance (£b) '
      '| Years LRR below floor |')
    A('|---|---:|---:|---:|---:|')
    from rates_model import COVERAGE_WINDOWS
    for W in COVERAGE_WINDOWS:
        cov   = ssm_last.get(f'ssm_cov_{W}')
        zcov  = ssm_last.get(f'ssm_zero_cov_years_{W}')
        mlrr  = ssm_last.get(f'ssm_min_lrr_bal_{W}')
        bloor = ssm_last.get(f'ssm_lrr_below_floor_years_{W}')
        cov_s  = f'{cov:.1%}' if cov is not None else '—'
        zcov_s = str(zcov) if zcov is not None else '—'
        mlrr_s = f'£{mlrr:,.0f}b' if mlrr is not None else '—'
        bloor_s = str(bloor) if bloor is not None else '—'
        A(f'| {W} years | {cov_s} | {zcov_s} | {mlrr_s} | {bloor_s} |')
    A('')
    A('*SSM applies uniform historical returns across the population (correlated-shock '
      'assumption — worst-case floor). Coverage fraction = Step-5 remainder / annual '
      'expenditure; zero in any year where LRR or SRR balance hits zero. TCM coverage '
      '(heterogeneous-tier ceiling) appears in §B.3.*')
    A('')

    # ── B.3 TCM matrices ──────────────────────────────────────
    A(f'## B.3 TCM Results — N={tcm_N} periods')
    A('')

    # B.3.1 Net worth
    A('### B.3.1 Net worth — start ($V_0$) and year N (£m)')
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

    # B.3.2 Net per taxpayer — capitalisation window
    A('### B.3.2 Net per taxpayer per year — capitalisation window average (£/yr)')
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

    # B.3.3 Annual wealth burden
    A('### B.3.3 Annual wealth burden (tax as % of net worth)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['wealth_burden'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {v:.2%} |' for v in vals))
    A('')

    # B.3.4 Effective rate on gains
    A('### B.3.4 Effective rate on gains (tax as % of annual gain)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['eff_rate'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {v:.1%} |' for v in vals))
    A('')

    # B.3.5 Lifetime average net tax
    A('### B.3.5 Average annual net tax per taxpayer — lifetime average (£/yr)')
    A('')
    A('| Tier \\ Bracket |' + ''.join(f' {b} |' for b in blabels))
    A('|---|' + '---|' * len(blabels))
    for i, diff in enumerate(diffs):
        vals = [r['avg_net_gbp'] for r in py_tcm[diff]]
        A(f'| {tlabels[i]} |' + ''.join(f' {_fmt_gbp(v)} |' for v in vals))
    A('')

    # B.3.6 Population distribution
    A('### B.3.6 Population distribution (taxpayers per bracket per tier)')
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

    # B.3.7 Tax collected per year — capitalisation window
    A('### B.3.7 Tax collected per year — capitalisation window average (£m/yr)')
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

    # B.3.8 Cohort proportion
    A('### B.3.8 Cohort proportion of total tax paid (%)')
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

    # B.3.9 Revenue by tier
    A('### B.3.9 Revenue by tier (£b/yr)')
    A('')
    A('| Tier | Lifetime avg (£b/yr) | Capitalisation window avg (£b/yr) |')
    A('|---|---|---|')
    total_rev = 0.0
    for i, diff in enumerate(diffs):
        subtotal    = sum(r['revenue_m']           for r in py_tcm[diff]) / 1000
        pf_subtotal = sum(r['post_fill_revenue_m'] for r in py_tcm[diff]) / 1000
        total_rev  += subtotal
        A(f'| {tlabels[i]} | £{subtotal:,.1f}b | £{pf_subtotal:,.1f}b |')
    total_pf_rev = sum(
        sum(r['post_fill_revenue_m'] for r in py_tcm[t['differential']]) / 1000
        for t in p['tiers']
    )
    A(f'| **Total** | **£{total_rev:,.1f}b** | **£{total_pf_rev:,.1f}b** |')
    A('')
    if py_lrr_fill:
        A('*TCM horizon N is derived from the SSM LRR breakeven year, not the TOML snapshot_N.*')
        A('')
        A('**TCM Step-5 coverage fraction by window:**')
        A('')
        A('| Window | TCM coverage | TCM failure year (LRR) | TCM failure year (SRR) |')
        A('|---|---:|---:|---:|')
        for W in COVERAGE_WINDOWS:
            cov   = tcm_win.get(f'tcm_cov_{W}') if tcm_win else None
            cov_s = f'{cov:.1%}' if cov is not None else '—'
            A(f'| {W} years | {cov_s} | '
              f'{tcm_win.get("tcm_lrr_failure_year", "—") if tcm_win else "—"} | '
              f'{tcm_win.get("tcm_srr_failure_year", "—") if tcm_win else "—"} |')
        A('')
        A('*TCM applies heterogeneous tier differentials to the actual historical return '
          'series, producing higher revenue than the SSM uniform-return assumption. The SSM '
          'forms the solvency/stress-test floor; the TCM ceiling bounds the plausible range. '
          'TCM and SSM run independent SRR/LRR balance trackers.*')
        A('')

    # ── B.4 Sweep ─────────────────────────────────────────────
    A('## B.4 Start-Year Sweep')
    A('')
    A(f'All figures at $\\tau_0$={p["tau_0"]:.0%}, $\\tau_m$={p["tau_m"]:.0%}, '
      f'k={p["k"]}, $W_{{min}}$=£{p["W_min"]}m.')
    A('')

    if sweep_extremals:
        A('### B.4.1 Extremals — four dimensions')
        A('')
        A('| Dimension | Start year | LRR breakeven | LRR surplus (£b) '
          '| LRR failure year | SRR failure year | SSM cov 50yr |')
        A('|---|:---:|:---:|---:|:---:|:---:|---:|')
        for dim_label, r in [
            ('Speed — slowest LRR fill',         sweep_extremals.get('worst_speed')),
            ('Speed — fastest LRR fill',         sweep_extremals.get('best_speed')),
            ('Margin — thinnest surplus',        sweep_extremals.get('worst_margin')),
            ('Margin — largest surplus',         sweep_extremals.get('best_margin')),
            ('Durability — lowest 50yr SSMcov',  sweep_extremals.get('worst_durable')),
            ('Durability — highest 50yr SSMcov', sweep_extremals.get('best_durable')),
            ('Resilience — earliest LRR failure',sweep_extremals.get('worst_resilient')),
            ('Resilience — latest/no LRR failure',sweep_extremals.get('best_resilient')),
        ]:
            if r is None:
                A(f'| {dim_label} | — | — | — | — | — | — |')
            else:
                lf   = str(r.get('lrr_failure_year')) if r.get('lrr_failure_year') else 'none'
                sf   = str(r.get('srr_failure_year')) if r.get('srr_failure_year') else 'none'
                c50  = (f'{r["ssm_cov_50"]:.1%}' if r.get('ssm_cov_50') is not None else '—')
                surp = (f'£{r["lrr_surplus_at_fill"]:,.0f}b'
                        if r.get('lrr_fill_year') is not None else '—')
                A(f'| {dim_label} | {r["calendar_year"]} | {r.get("lrr_fill_year", "—")} | '
                  f'{surp} | {lf} | {sf} | {c50} |')
        A('')
        nofail = sum(1 for r in sweep_extremals.get('all', [])
                     if r.get('lrr_failure_year') is None and r.get('lrr_fill_year') is not None)
        if nofail:
            A(f'*{nofail} start years produce no LRR failure within the 71-year modelling window.*')
            A('')

        scenario_start = p.get('scenario_start_year')
        all_rows = sweep_extremals.get('all', [])
        A(f'### B.4.2 Full sweep table (all {len(all_rows)} calendar years)')
        A('')
        A('| Start | SRR fill | LRR fill | LRR surplus (£b) | LRR failure | SRR failure '
          '| gap | SSMcov5 | SSMcov10 | SSMcov20 | SSMcov50 | TCMcov10 | TCMcov50 |')
        A('|:---:|:---:|:---:|---:|:---:|:---:|:---:|---:|---:|---:|---:|---:|---:|')

        for r in all_rows:
            def _c(v): return str(v) if v is not None else '—'
            def _p(v): return f'{v:.1%}' if v is not None else '—'
            lrr_s = (f'{r["lrr_surplus_at_fill"]:,.0f}'
                     if r.get('lrr_fill_year') is not None else '—')
            yr   = r['calendar_year']
            bold = scenario_start and yr == scenario_start
            b    = '**' if bold else ''
            A(f'| {b}{yr}{b} | {b}{_c(r.get("srr_fill_year"))}{b} | '
              f'{b}{_c(r.get("lrr_fill_year"))}{b} | {b}{lrr_s}{b} | '
              f'{b}{_c(r.get("lrr_failure_year"))}{b} | '
              f'{b}{_c(r.get("srr_failure_year"))}{b} | '
              f'{b}{_c(r.get("lrr_srr_failure_gap"))}{b} | '
              f'{b}{_p(r.get("ssm_cov_5"))}{b} | '
              f'{b}{_p(r.get("ssm_cov_10"))}{b} | '
              f'{b}{_p(r.get("ssm_cov_20"))}{b} | '
              f'{b}{_p(r.get("ssm_cov_50"))}{b} | '
              f'{b}{_p(r.get("tcm_cov_10"))}{b} | '
              f'{b}{_p(r.get("tcm_cov_50"))}{b} |')

        A('')
        A('*Active scenario shown in bold. Coverage fractions = Step-5 remainder / annual '
          'expenditure, averaged over each window. Zero in failure years drags the average. '
          'LRR failure: buffer exhausted (lrr_bal = 0). SRR failure: refund guarantee broken '
          '(srr_bal = 0). Gap: years between LRR and SRR failure. SSM = correlated-shock '
          'floor; TCM = heterogeneous-tier ceiling.*')
        A('')

    # ── B.5 Statistical pass ──────────────────────────────────
    A('## B.5 Statistical Pass — P(success) Across Economic Cycles')
    A('')
    A('**Success definition (v8):** LRR fills within the 71-year window AND '
      'LRR never fails (lrr_failure_year is None).')
    A('')
    if stats:
        ov = stats['overall']
        A(f'### B.5.1 Overall (all {ov["n_total"]} start years)')
        A('')
        A('| Metric | Value |')
        A('|---|---|')
        A(f'| Success rate | {ov["success_rate"]:.1f}% ({ov["n_success"]}/{ov["n_total"]}) |')
        A(f'| LRR fills | {ov["lrr_fill_rate"]:.1f}% ({ov["n_lrr_fills"]}/{ov["n_total"]}) |')
        A(f'| LRR failures | {ov["lrr_failure_rate"]:.1f}% '
          f'({ov["n_lrr_failure"]}/{ov["n_total"]}) |')
        A(f'| SRR failures | {ov["srr_failure_rate"]:.1f}% '
          f'({ov["n_srr_failure"]}/{ov["n_total"]}) |')
        A('')
        A('### B.5.2 By economic cycle')
        A('')
        A('| Period | N | Success% | LRR fill% |')
        A('|---|:---:|:---:|:---:|')
        for b in stats['by_bucket']:
            A(f'| {b["label"]} | {b["n"]} | {b["success_rate"]:.1f}% '
              f'| {b["lrr_fill_rate"]:.1f}% |')
        A('')
        A('### B.5.3 Key metric distributions')
        A('')
        A('| Metric | N | Min | Median | Mean | Max |')
        A('|---|:---:|---:|---:|---:|---:|')

        def _fv2(v, fmt): return fmt(v) if v is not None else '—'

        dist_rows_int = [
            ('lrr_fill_year',       'LRR breakeven year'),
            ('srr_fill_year',       'SRR fill year'),
            ('lrr_failure_year',    'LRR failure year'),
            ('srr_failure_year',    'SRR failure year'),
            ('lrr_srr_failure_gap', 'LRR→SRR failure gap (yrs)'),
        ]
        for key, label in dist_rows_int:
            d = stats['distributions'].get(key, {})
            fi = lambda v: f'{v:,.0f}'
            A(f'| {label} | {d.get("n", 0)} | {_fv2(d.get("min"), fi)} '
              f'| {_fv2(d.get("median"), fi)} | {_fv2(d.get("mean"), fi)} '
              f'| {_fv2(d.get("max"), fi)} |')

        A(f'| LRR surplus at breakeven (£b) | '
          f'{stats["distributions"]["lrr_surplus_at_fill"].get("n", 0)} | '
          f'{_fv2(stats["distributions"]["lrr_surplus_at_fill"].get("min"), lambda v: f"{v:,.0f}")} | '
          f'{_fv2(stats["distributions"]["lrr_surplus_at_fill"].get("median"), lambda v: f"{v:,.0f}")} | '
          f'{_fv2(stats["distributions"]["lrr_surplus_at_fill"].get("mean"), lambda v: f"{v:,.0f}")} | '
          f'{_fv2(stats["distributions"]["lrr_surplus_at_fill"].get("max"), lambda v: f"{v:,.0f}")} |')

        fp = lambda v: f'{v:.1%}'
        for W in COVERAGE_WINDOWS:
            for prefix, label_pfx in [('ssm', 'SSM'), ('tcm', 'TCM')]:
                key = f'{prefix}_cov_{W}'
                d   = stats['distributions'].get(key, {})
                A(f'| {label_pfx} coverage {W}yr avg | {d.get("n", 0)} | '
                  f'{_fv2(d.get("min"), fp)} | {_fv2(d.get("median"), fp)} | '
                  f'{_fv2(d.get("mean"), fp)} | {_fv2(d.get("max"), fp)} |')
        A('')
        A('*Coverage fractions: Step-5 remainder / annual expenditure, '
          'averaged over each window length. Zero in any failure year. '
          'SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.*')
        A('')

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    return out_path


# ─────────────────────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────────────────────

# Style and save aliases — all internal call sites unchanged
_apply_base_style = apply_style


def _save(fig, output_dir, name):
    path = Path(output_dir) / name
    save_fig(fig, path)
    return path


# ─────────────────────────────────────────────────────────────
# FIGURES 01–05  (unchanged from 7_3)
# ─────────────────────────────────────────────────────────────

def _fig01_sweep_breakeven_coverage(p, sweep_results, output_dir):
    """Fig 01 — Start-year sweep scatter: breakeven year and 10yr TCM coverage."""
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
        breakevn = [r.get('lrr_fill_year') for r in bucket]
        coverage = [r['tcm_cov_10'] * 100
                    if r.get('tcm_cov_10') is not None else None
                    for r in bucket]
        ax1.scatter(years, breakevn, color=colour, s=40, alpha=0.8, label=label, zorder=3)
        cov_pairs = [(y, c) for y, c in zip(years, coverage) if c is not None]
        if cov_pairs:
            cy, cc = zip(*cov_pairs)
            ax2.scatter(cy, cc, color=colour, s=40, alpha=0.4, marker='^', zorder=3)

    active = next((r for r in sweep_results if r['calendar_year'] == active_year), None)
    if active:
        ax1.scatter([active_year], [active.get('lrr_fill_year')],
                    color='black', s=120, zorder=5, marker='D',
                    label=f'{active_year} (active scenario)')
        if active.get('tcm_cov_10') is not None:
            ax2.scatter([active_year], [active['tcm_cov_10'] * 100],
                        color='black', s=120, zorder=5, marker='^')

    all_tcm = [r['tcm_cov_10'] * 100
               for r in sweep_results if r.get('tcm_cov_10') is not None]
    all_lrr = [r['lrr_fill_year'] for r in sweep_results
               if r.get('lrr_fill_year') is not None]

    # ── set both axes explicitly so gridlines align ───────────────────────────
    # Fix ax1 range, compute clean ticks, then derive ax2 ticks at the same
    # fractional positions.  N_TICKS controls density on both axes together.
    N_TICKS = 6
    ax1_lo = 0
    ax1_hi = max(all_lrr) * 1.15 if all_lrr else 40
    ax2_lo = 0
    ax2_hi = max(all_tcm) * 1.10 if all_tcm else 400

    ax1.set_ylim(ax1_lo, ax1_hi)
    ax2.set_ylim(ax2_lo, ax2_hi)
    ax2.axhline(100, color='black', linewidth=0.9, linestyle='--', alpha=0.5,
            label='100% TCM coverage')

    # Evenly spaced fractions 0..1, then map onto each axis
    fractions = [i / (N_TICKS - 1) for i in range(N_TICKS)]
    ax1_ticks = [ax1_lo + f * (ax1_hi - ax1_lo) for f in fractions]
    ax2_ticks = [ax2_lo + f * (ax2_hi - ax2_lo) for f in fractions]

    ax1.set_yticks(ax1_ticks)
    ax1.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}')
    )
    ax2.set_yticks(ax2_ticks)
    ax2.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%')
    )
    # ─────────────────────────────────────────────────────────────────────────

    ax1.set_xlabel('Start year', fontsize=11)
    ax1.set_ylabel('LRR breakeven year', fontsize=11)
    ax2.set_ylabel('TCM 10yr coverage (%)', fontsize=11)
    ax1.set_title(
        'Start-year sweep: LRR breakeven and 10yr TCM coverage\n'
        'Circles = breakeven year (left axis)  |  Triangles = TCM 10yr coverage (right axis)',
        fontsize=11, pad=12)
    handles = [mpatches.Patch(color=c, label=l) for l, _, _, c in CYCLE_BUCKETS_CHART]
    handles.append(plt.Line2D([0], [0], marker='D', color='black', linestyle='None',
                               markersize=8, label=f'{active_year} (active scenario)'))
    handles.append(plt.Line2D([0], [0], color='black', linestyle='--',
                           alpha=0.5, linewidth=0.9, label='100% TCM coverage'))
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
    ax.grid(False)
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
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(3))
    y_max = max(max(lrr_bal), max(lrr_tgt), max(srr_bal))
    if srr_fill:
        ax.axvline(srr_fill, color='#4e79a7', linestyle=':', alpha=0.8)
        ax.text(srr_fill + 0.4, y_max * 0.92, f'SRR fill\nyr {srr_fill}',
                fontsize=8, color='#4e79a7', va='top')
    ax.axvline(lrr_fill_yr, color='#f28e2b', linestyle=':', alpha=0.8)
    ax.text(lrr_fill_yr - 1, y_max * 0.75, f'LRR fill\nyr {lrr_fill_yr}',
            fontsize=8, color='#f28e2b', va='top')

    # ── dynamically annotate the worst return year within the capitalisation window ──
    # Find the simulation year with the most negative return (the clearest visible
    # plateau/dip in LRR accumulation). Only annotate if it's genuinely negative.
    worst_row = min(
        (r for r in ssm_clip if r['year'] >= 1),
        key=lambda r: r['g'],
    )
    if worst_row['g'] < 0:
        crash_sim_yr   = worst_row['year']
        crash_cal_yr   = p['scenario_start_year'] + crash_sim_yr - 1
        crash_return   = worst_row['g'] * 100
        srr_at_crash   = worst_row['srr_balance']
        ax.annotate(
            f'{crash_cal_yr} crash\n({crash_return:+.2f}% return)',
            xy=(crash_sim_yr, srr_at_crash),
            xytext=(crash_sim_yr + 3, srr_at_crash + y_max * -0.06),
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
    """Fig 05 — SSM 10yr coverage distribution by economic cycle (box plots, v8)."""
    _apply_base_style()
    cycle_data, cycle_labels, cycle_cols = [], [], []
    for label, yr_from, yr_to, colour in CYCLE_BUCKETS_CHART:
        vals = [r['ssm_cov_10'] * 100
                for r in sweep_results
                if yr_from <= r['calendar_year'] <= yr_to
                and r.get('ssm_cov_10') is not None]
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
    ax.set_ylabel('SSM 10yr coverage (%)', fontsize=11)
    ax.set_title(
        'SSM 10yr coverage distribution by economic cycle  |  All 73 start years — Balanced parameters\n'
        'SSM = correlated-shock floor; pairs with TCM ceiling (see Fig 07)  |  '
        '5-step post-fill priority mechanic (v8)',
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

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(18, 5),
                                      gridspec_kw={'wspace': 0.35})

    for ax, matrix, title, cmap, unit in [
        (ax_l, burden_matrix,  'Annual wealth burden\n(tax as % of net worth)',
         'Blues', '%'),
        (ax_r, effrate_matrix, 'Effective rate on gains\n(tax as % of annual gain)',
         'Oranges', '%'),
    ]:
        im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0)
        ax.grid(False)
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
        f'Individual burden matrices — {p["scenario_start_year"]} Balanced scenario, N={p["N"]}\n'
        'RATES.A §B.3c (left) and §B.3d (right)  |  '
        '0.00% = genuine zero liability (exemption threshold + refund offset); not missing data',
        fontsize=9, y=1.06)
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
                  and r.get('ssm_cov_10') is not None
                  and r.get('tcm_cov_10') is not None]
        for r in bucket:
            yr  = r['calendar_year']
            ssm = r['ssm_cov_10'] * 100
            tcm = r['tcm_cov_10'] * 100
            ax.plot([yr, yr], [ssm, tcm], color=colour, alpha=0.5, linewidth=1.2)
            ax.scatter(yr, ssm, color=colour, s=30, alpha=0.8, zorder=4,
                       marker='o', linewidths=0)
            ax.scatter(yr, tcm, color=colour, s=30, alpha=0.8, zorder=4,
                       marker='^', linewidths=0)

    # Active scenario
    active = next((r for r in sweep_results if r['calendar_year'] == active_year), None)
    if active and active.get('ssm_cov_10') is not None and active.get('tcm_cov_10') is not None:
        ssm_a = active['ssm_cov_10'] * 100
        tcm_a = active['tcm_cov_10'] * 100
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
    ax.set_ylabel('10yr coverage fraction (%)', fontsize=11)
    ax.set_title(
        'SSM/TCM 10yr coverage range by start year\n'
        'Circles = SSM floor (correlated-shock)  |  Triangles = TCM ceiling (persistent heterogeneity)  |  '
        '5-step post-fill priority mechanic (v8)',
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
    Fig 08 — Loss-year mechanics: symmetric refund in the worst return year
    within the first 10 simulation years.
    """
    _apply_base_style()

    # ── bracket and tier selection ────────────────────────────────────────────
    # 95th percentile bracket by label
    bracket_95_idx = next(
        (i for i, b in enumerate(p['brackets']) if b['label'] == '95%'), None)
    if bracket_95_idx is None:
        # fallback: bracket closest to 95th percentile by index
        bracket_95_idx = min(len(p['brackets']) - 1, 5)
    b95 = p['brackets'][bracket_95_idx]

    # Good tier: positive differential closest to zero (most conservative growth tier)
    pos_tiers = [t for t in p['tiers'] if t['differential'] > 0]
    good_tier = min(pos_tiers, key=lambda t: t['differential']) if pos_tiers else p['tiers'][-1]
    good_diff = good_tier['differential']

    # ── simulation ───────────────────────────────────────────────────────────
    N       = p['N']
    returns = p['returns']
    g_series = [returns[t] + good_diff for t in range(1, N + 1)]
    g_sell   = returns[N + 1] + good_diff
    sim      = simulate(b95['V0_m'], g_series, alpha=1.0, p=p)

    # ── display window: first 10 years (or N if shorter) ─────────────────────
    window_end  = min(10, N)
    window_years = list(range(1, window_end + 1))
    cal_start    = p['scenario_start_year']
    sim_year_labels = [str(cal_start + t - 1) for t in window_years]

    # ── find worst return year within the window ──────────────────────────────
    worst_t       = min(window_years, key=lambda t: returns[t])
    crash_sim_yr  = worst_t
    crash_cal_yr  = cal_start + crash_sim_yr - 1
    crash_return_pct = returns[crash_sim_yr] * 100
    crash_x       = crash_sim_yr - 1   # 0-indexed position in bar chart

    # ── tax / refund series ───────────────────────────────────────────────────
    gross_tax    = [max(0.0, sim[t]['L']) * 1e6 for t in window_years]
    gross_refund = [min(0.0, sim[t]['L']) * 1e6 for t in window_years]
    cum_net      = []
    running = 0.0
    for t in window_years:
        running += sim[t]['L'] * 1e6
        cum_net.append(running)

    # ── plot ──────────────────────────────────────────────────────────────────
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    x     = np.arange(len(window_years))
    bar_w = 0.55

    # Highlight crash year
    ax1.axvspan(crash_x - 0.45, crash_x + 0.45, color='#fee8e8', zorder=1, alpha=0.9)

    ax1.bar(x, gross_tax,    width=bar_w, color='#4e79a7', alpha=0.85,
            label='Gross tax paid (gain year)', zorder=3)
    ax1.bar(x, gross_refund, width=bar_w, color='#e15759', alpha=0.85,
            label='Symmetric refund received (loss year)', zorder=3)

    ax2.plot(x, cum_net, color='#333333', linewidth=2, linestyle='-',
             marker='o', markersize=5, zorder=5, label='Cumulative net tax (right axis)')
    ax2.axhline(0, color='#333333', linewidth=0.6, linestyle=':', alpha=0.5)

    # Crash year annotation — only if the worst year has a negative return
    if crash_return_pct < 0:
        ax1.annotate(
            f'Calendar {crash_cal_yr}\n'
            f'Return: {crash_return_pct:+.2f}%\n'
            f'Refund fires at τ(W)',
            xy=(crash_x, gross_refund[crash_x]),
            xytext=(crash_x + 1.2, gross_refund[crash_x] - abs(gross_refund[crash_x]) * -0.4),
            fontsize=8, color='#c0392b',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.9))

    # ── align gridlines between left and right y-axes ────────────────────────
    N_TICKS = 6

    # ax1 range: symmetric around zero so tax bars and refund bars both show cleanly
    ax1_abs = max(max(gross_tax), abs(min(gross_refund))) * 1.25
    ax1_lo, ax1_hi = -ax1_abs, ax1_abs

    # ax2 range: cumulative net — find natural bounds with some headroom
    ax2_abs = max(abs(min(cum_net)), abs(max(cum_net))) * 1.25
    ax2_lo  = min(cum_net) * 1.25 if min(cum_net) < 0 else -ax2_abs * 0.1
    ax2_hi  = max(cum_net) * 1.25

    ax1.set_ylim(ax1_lo, ax1_hi)
    ax2.set_ylim(ax2_lo, ax2_hi)

    fractions  = [i / (N_TICKS - 1) for i in range(N_TICKS)]
    ax1_ticks  = [ax1_lo + f * (ax1_hi - ax1_lo) for f in fractions]
    ax2_ticks  = [ax2_lo + f * (ax2_hi - ax2_lo) for f in fractions]

    ax1.set_yticks(ax1_ticks)
    ax1.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}'))
    ax2.set_yticks(ax2_ticks)
    ax2.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}'))
    # ─────────────────────────────────────────────────────────────────────────

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

    crash_note = (f'Red shading = {crash_cal_yr} crash year ({crash_return_pct:+.2f}%)'
                  if crash_return_pct < 0 else 'No negative return year in display window')

    fig.suptitle(
        f'Loss-year mechanics: symmetric refund in the worst return year\n'
        f'95th percentile bracket ($V_0$ = £{b95["V0_m"]:.3f}m), '
        f'{good_tier["label"]} tier ({good_diff * 100:+.2f}pp), '
        f'{cal_start} Balanced scenario — simulation years 1–{window_end}\n'
        f'{crash_note}  |  Refund is bounded by cumulative net tax paid '
        f'(lifetime contribution envelope)',
        fontsize=9, y=1.01)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=8.5, loc='upper left')

    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_08_loss_year_mechanics.png')


def _fig09_phase_two_transition(p, py_ssm, output_dir):
    """
    Fig 09 — Phase Two transition: LRR stress zones across the full 71-year window.

    Two stacked panels (shared x-axis):

    Top panel — LRR balance vs target (linear scale):
      - Orange line: LRR balance accumulating during capitalisation phase.
      - Red line:    LRR balance post-fill (zero-governance, modelled output).
      - Grey dashed: LRR target (3× annual expenditure, growing at budget_growth).
      - Green shading: balance above target (healthy buffer).
      - Amber shading: balance below target but above zero (stressed — LRR below
        floor but refund guarantee not yet broken).
      - Vertical dashed: LRR fill year.

    Bottom panel — Step-5 coverage fraction (linear scale):
      - Blue bars:  positive coverage years (Step-5 surplus / annual expenditure).
      - Red bars:   zero-coverage years (cov_frac == 0.0 post-fill).
      - 100% reference line.

    The two panels together make the model's honesty argument explicit:
    100% solvency success does not mean 100% coverage every year — it means
    the LRR never hits zero, but it can and does dip below its floor target,
    and coverage can be zero in those years.
    """
    _apply_base_style()

    lrr_fill_yr = next((r['year'] for r in py_ssm if r.get('lrr_filled')), None)
    if lrr_fill_yr is None:
        print('  Fig 09 skipped: LRR did not fill within modelling window.')
        return None

    years   = [r['year']        for r in py_ssm]
    lrr_bal = [r['lrr_balance'] for r in py_ssm]
    lrr_tgt = [r['lrr_target']  for r in py_ssm]
    cov_frac = [r['cov_frac']   for r in py_ssm]   # 0.0 during capitalisation
    returns_g = [r['g']         for r in py_ssm]

    # ── derived zone masks (post-fill only) ──────────────────────────────────
    post_years = [y for y in years if y > lrr_fill_yr]
    post_bal   = [lrr_bal[i] for i, y in enumerate(years) if y > lrr_fill_yr]
    post_tgt   = [lrr_tgt[i] for i, y in enumerate(years) if y > lrr_fill_yr]
    post_cov   = [cov_frac[i] for i, y in enumerate(years) if y > lrr_fill_yr]

    # Identify years below floor (bal < target) and zero-coverage years
    below_floor_years = [y for y, b, t in zip(post_years, post_bal, post_tgt) if b < t]
    zero_cov_years    = [y for y, c in zip(post_years, post_cov) if c == 0.0]

    # ── summary stats for title ───────────────────────────────────────────────
    n_below_floor = len(below_floor_years)
    n_zero_cov    = len(zero_cov_years)
    min_bal       = min(post_bal) if post_bal else 0.0
    max_cov_pct   = max(c * 100 for c in post_cov) if post_cov else 0.0

    # ── figure layout: 2 panels, shared x-axis ───────────────────────────────
    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(13, 8),
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1.4], 'hspace': 0.08}
    )

    # ═══════════════════════════════════════════════════════════════
    # TOP PANEL — LRR balance vs target
    # ═══════════════════════════════════════════════════════════════

    # Shading zones (post-fill only, between balance and target)
    # Green where balance >= target, amber where 0 < balance < target
    py_arr  = np.array(post_years,  dtype=float)
    pb_arr  = np.array(post_bal,    dtype=float)
    pt_arr  = np.array(post_tgt,    dtype=float)

    # Shade only the gap where balance dips below the floor target
    ax_top.fill_between(
        py_arr, pb_arr, pt_arr,
        where=(pb_arr < pt_arr),
        interpolate=True,
        color='#f28e2b', alpha=0.45, linewidth=0,
        label='Below floor (stressed, not failed)',
    )

    # LRR target line
    ax_top.plot(years, lrr_tgt, color='#888888', linewidth=1.4, linestyle='--',
                alpha=0.8, label='LRR floor target (3× annual expenditure)')

    # Pre-fill balance (capitalisation phase)
    pre_years_plot = [y for y in years if y <= lrr_fill_yr]
    pre_bal_plot   = [lrr_bal[i] for i, y in enumerate(years) if y <= lrr_fill_yr]
    ax_top.plot(pre_years_plot, pre_bal_plot, color='#f28e2b', linewidth=2.2,
                label='LRR balance — capitalisation phase')

    # Post-fill balance (zero-governance modelled output)
    # Include lrr_fill_yr as the join point
    post_all_years = [y for y in years if y >= lrr_fill_yr]
    post_all_bal   = [lrr_bal[i] for i, y in enumerate(years) if y >= lrr_fill_yr]
    ax_top.plot(post_all_years, post_all_bal, color='#e15759', linewidth=2.2,
                label='LRR balance — post-fill (zero-governance)')

    # LRR fill vertical
    ax_top.axvline(lrr_fill_yr, color='#555555', linestyle=':', linewidth=1.3, alpha=0.9)
    ax_top.text(lrr_fill_yr + 0.6, max(lrr_tgt) * 1.05,
                f'LRR fill\n(yr {lrr_fill_yr})',
                fontsize=8, color='#555555', va='top')

    ax_top.set_ylabel('LRR balance (£b)', fontsize=10)
    ax_top.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))
    ax_top.legend(fontsize=8.5, loc='upper left')

    # Annotate minimum balance (shows the model never hits zero)
    min_yr = post_years[post_bal.index(min_bal)]
    ax_top.annotate(
        f'Min balance\n£{min_bal:,.0f}b\n(yr {min_yr})',
        xy=(min_yr, min_bal),
        xytext=(min_yr + 3, min_bal + (max(lrr_tgt) * 0.08)),
        fontsize=7.5, color='#c03020',
        arrowprops=dict(arrowstyle='->', color='#c03020', lw=0.8),
    )

    # ═══════════════════════════════════════════════════════════════
    # BOTTOM PANEL — Step-5 coverage fraction
    # ═══════════════════════════════════════════════════════════════

    post_budget   = [r['budget'] for r in py_ssm if r['year'] > lrr_fill_yr]
    post_surplus_b = [c * b for c, b in zip(post_cov, post_budget)]

    # Draw bars for all years (zero-coverage bars are zero height — invisible)
    ax_bot.bar(post_years, post_surplus_b, width=0.8,
            color='#4e79a7', alpha=0.85, zorder=3)

    # Zero-coverage years: red column shading + triangle marker at baseline
    for y, c in zip(post_years, post_cov):
        if c == 0.0:
            ax_bot.axvspan(y - 0.4, y + 0.4, color='#e15759', alpha=0.35,
                        zorder=2, linewidth=0)
            ax_bot.scatter(y, 1.0, marker='v', color='#e15759', s=40,
                            zorder=5, clip_on=False)

    # 100% coverage reference = annual expenditure in £b
    ax_bot.plot(post_years, post_budget, color='black', linewidth=0.9,
                linestyle='--', alpha=0.5, label='Annual expenditure (= 100% coverage)')

    ax_bot.axvline(lrr_fill_yr, color='#555555', linestyle=':', linewidth=1.3, alpha=0.9)
    ax_bot.set_xlabel('Year from launch', fontsize=10)
    ax_bot.set_yscale('log')
    ax_bot.set_ylim(bottom=1.0)   # £1b floor — anything below this is effectively zero
    ax_bot.set_ylabel('Step-5 surplus\n(£b/yr)', fontsize=9)
    ax_bot.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b')
    )

    # Legend
    blue_patch = mpatches.Patch(color='#4e79a7', alpha=0.85, label='Labour-relief surplus (£b)')
    red_patch  = mpatches.Patch(color='#e15759', alpha=0.35,
                                label=f'Zero coverage ({n_zero_cov} years — all surplus consumed by Steps 1–4)')
    ax_bot.legend(
        handles=[blue_patch, red_patch,
                plt.Line2D([0], [0], color='black', linestyle='--',
                            alpha=0.5, label='Annual expenditure (100% reference)')],
        fontsize=8, loc='upper left',
    )

    # ── shared title ─────────────────────────────────────────────────────────
    scenario_yr = p['scenario_start_year']
    fig.suptitle(
        f'Phase Two stress profile — full 71-year window, {scenario_yr} Balanced scenario\n'
        f'Top: LRR balance vs 3× floor target  |  '
        f'Amber shading = {n_below_floor} years below floor (stressed, not failed)  |  '
        f'Min balance £{min_bal:,.0f}b (never zero)\n'
        f'Bottom: Step-5 labour-relief surplus (£b)  |  '
        f'Red bars = {n_zero_cov} zero-coverage years  |  '
        f'Dashed line = annual expenditure; bars above it = coverage > 100%  |  '
        f'Growth in later decades reflects compounding wealth base, not a modelling error',
        fontsize=8.5, y=1.01,
    )

    plt.tight_layout()
    return _save(fig, output_dir, 'rates_fig_09_phase_two_transition.png')

# ─────────────────────────────────────────────────────────────
# GENERATE ALL CHARTS
# ─────────────────────────────────────────────────────────────

def generate_charts(p, py_ssm, py_tcm, sweep_results, output_dir=None, tcm_N=None):
    """
    Generate all nine RATES figures and save to output_dir.

    Figures 01–07: core model outputs (sweep, revenue, burden, reserves, coverage).
    Figure 08: loss-year mechanics — symmetric refund in the 2008 crash.
    Figure 09: Phase Two transition — LRR trajectory beyond LRR fill.
    """
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

    # ── TCM (bracket×tier output table) ───────────────────────
    print(f'\nRunning TCM (N={ssm_lrr_N}, N_fill={ssm_srr_N}, '
          f'{len(p["brackets"])} brackets × {len(p["tiers"])} tiers)...')
    py_tcm = model.run_tcm(p, N=ssm_lrr_N, N_fill=ssm_srr_N)

    total_rev = sum(
        sum(r['revenue_m'] for r in py_tcm[t['differential']]) / 1000
        for t in p['tiers']
    )
    print(f'  Lifetime-avg revenue: £{total_rev:,.1f}b/yr')

    # TCM coverage windows (independent SRR/LRR loop)
    print('  Computing TCM coverage windows...')
    from rates_model import _tcm_coverage_windows, COVERAGE_WINDOWS
    tcm_win = _tcm_coverage_windows(p, ssm_lrr_N, ssm_srr_N) if py_lrr_fill else None

    # SSM coverage windows (from run_ssm last-row summary fields)
    ssm_last = py_ssm[-1]
    if py_lrr_fill:
        print('  SSM coverage windows:')
        for W in COVERAGE_WINDOWS:
            v = ssm_last.get(f'ssm_cov_{W}')
            print(f'    ssm_cov_{W}: {"—" if v is None else f"{v:.1%}"}')
        if tcm_win:
            print('  TCM coverage windows:')
            for W in COVERAGE_WINDOWS:
                v = tcm_win.get(f'tcm_cov_{W}')
                print(f'    tcm_cov_{W}: {"—" if v is None else f"{v:.1%}"}')
        lrr_fail = ssm_last.get('lrr_failure_year')
        srr_fail = ssm_last.get('srr_failure_year')
        print(f'  LRR failure year: {lrr_fail if lrr_fail else "none"}')
        print(f'  SRR failure year: {srr_fail if srr_fail else "none"}')

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
    _out = Path(output_dir) if output_dir else OUTPUT_DIR
    _out.mkdir(parents=True, exist_ok=True)

    print('\nWriting output report...')
    out_path = write_output_md(
        p, py_ssm, py_tcm, ssm_lrr_N, sweep_extremals, stats,
        tcm_win=tcm_win,
        output_dir=_out,
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
    if py_lrr_fill:
        for W in [10, 50]:
            sv = ssm_last.get(f'ssm_cov_{W}')
            tv = tcm_win.get(f'tcm_cov_{W}') if tcm_win else None
            ss = f'{sv:.1%}' if sv is not None else '—'
            ts = f'{tv:.1%}' if tv is not None else '—'
            print(f'  SSM/TCM cov {W}yr:              {ss} / {ts}')
        lf = ssm_last.get('lrr_failure_year')
        print(f'  LRR failure year:              {lf if lf else "none"}')
    ov = stats['overall']
    print(f'  Success rate:     {ov["success_rate"]:.1f}%  '
          f'({ov["n_success"]}/{ov["n_total"]} start years)')
    ws = sweep_extremals.get('worst_speed')
    bs = sweep_extremals.get('best_speed')
    print(f'  Sweep speed:      worst={ws["calendar_year"] if ws else "—"} '
          f'(N={ws["lrr_fill_year"] if ws else "—"})  '
          f'best={bs["calendar_year"] if bs else "—"} '
          f'(N={bs["lrr_fill_year"] if bs else "—"})')
    wd = sweep_extremals.get('worst_durable')
    bd = sweep_extremals.get('best_durable')
    if wd:
        print(f'  Durability:       worst={wd["calendar_year"]} '
              f'(SSMcov50={wd.get("ssm_cov_50", 0):.1%})  '
              f'best={bd["calendar_year"] if bd else "—"} '
              f'(SSMcov50={bd.get("ssm_cov_50", 0):.1%})')
    print(f'  Output:           {out_path.name}')
    print('\nDone.')


if __name__ == '__main__':
    main()
