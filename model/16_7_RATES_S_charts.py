"""
WDT Rate Parameter Sensitivity Sweep — Charts
===============================================
Companion to 16_6_260813_RATES_S_tables.py.  Re-runs the same sweeps
and produces eight publication-quality PNG figures.

Figures produced:
  sweep_fig_01  τ_0 sensitivity — 4-panel
  sweep_fig_02  τ_m sensitivity — 4-panel
  sweep_fig_03  k sensitivity   — 4-panel (log x-axis)
  sweep_fig_04  W_min sensitivity — 4-panel
  sweep_fig_05  Rate function shapes — 4-panel across all parameters
  sweep_fig_06  Relative sensitivity synthesis
  sweep_fig_07  srr_ratio sensitivity — 4-panel (SWF sizing)
  sweep_fig_08  lrr_years sensitivity — 4-panel (SWF sizing)
  sweep_fig_09  Coverage fan — SSM 5yr to TCM 50yr across all rate parameters [NEW v8]
  sweep_fig_10  LRR failure year — SWF sizing sweeps srr_ratio and lrr_years [NEW v8]

v8 changes:
  Panel [0,0] axis titles now show HEADLINE_WINDOW (default 10yr).
  Coverage fan (Fig 09) shows full temporal profile: outer band SSM 5yr–TCM 50yr,
  inner band SSM HW–TCM HW, for all four rate parameters on one normalised axis.
  Failure year (Fig 10) shows LRR failure year distribution across SWF sweeps;
  exercises the v8 failure mechanics and shows post-fill buffer margin.
  Change HEADLINE_WINDOW in wdt_analytics.py to update all labels simultaneously.

Shared infrastructure (path resolution, statistical helpers, sweep
runner) comes from rates_s_helpers.py.

USAGE
  python3 16_7_260813_RATES_S_charts.py [params.toml] [output_dir]
"""

import sys
import math
import datetime
from pathlib import Path
from copy import deepcopy

from wdt_analytics import (
    model, DEFAULT_PARAMS,
    run_param_sweep, median, mean, success, summarise, HEADLINE_WINDOW,
)
from wdt_fmt import fmt_pct1, out_dir
from wdt_style import (apply_style, save_fig,
                        C_SSM, C_TCM, C_LRR, C_SURPLUS, C_BASELINE,
                        PARAM_COLOURS)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OUTPUT_DIR = out_dir('RATES_S')

# ── Sweep grids and baseline — populated from TOML in main() ─────────────────
BASELINE        = {}
SWEEP_TAU_0     = []
SWEEP_TAU_M     = []
SWEEP_K         = []
SWEEP_WMIN      = []
SWEEP_SRR_RATIO = []
SWEEP_LRR_YEARS = []

# ── Style and save helpers ────────────────────────────────────────────────────

# Aliases — all internal call sites unchanged
_base_style = apply_style


def _save(fig, output_dir, name):
    return save_fig(fig, Path(output_dir) / name)


def _pct(v):
    return v * 100 if v is not None else None


def _baseline_x(values, baseline):
    """Return the x-position (index or value) closest to the baseline."""
    return min(range(len(values)), key=lambda i: abs(values[i] - baseline))


# ── Figure helpers ────────────────────────────────────────────────────────────

def _extract_series(sweep_results, key, transform=None):
    """Extract a list of (value, dist_dict) pairs, skipping skipped entries."""
    xs, mins, medians, means, maxs = [], [], [], [], []
    for r in sweep_results:
        if r['skipped'] or r['summary'] is None:
            continue
        d = r['summary'][key]
        if d['median'] is None:
            continue
        v = r['value']
        t = transform if transform else (lambda x: x)
        xs.append(t(v))
        mins.append(d['min'])
        medians.append(d['median'])
        means.append(d['mean'])
        maxs.append(d['max'])
    return xs, mins, medians, means, maxs


def _extract_wc(sweep_results, key):
    """Extract worst-case 2006 values, one per sweep point."""
    xs, ys = [], []
    for r in sweep_results:
        if r['skipped'] or r['summary'] is None:
            continue
        wc = r['summary']['worst_case_2006']
        if wc is None:
            continue
        val = wc.get(key)
        if val is not None:
            xs.append(r['value'])
            ys.append(val)
    return xs, ys


def _weighted_quantiles(vals, weights, quantiles):
    """
    Compute weighted quantiles for a list of (value, weight) pairs.

    vals      : list of floats
    weights   : list of floats (same length; need not sum to 1)
    quantiles : list of floats in [0, 1]

    Returns a list of interpolated quantile values, one per entry in quantiles.
    Uses the midpoint-of-bin cumulative weight convention: each observation is
    assigned the cumulative weight at the *centre* of its probability mass
    (i.e. cum_before + 0.5 * w_i / total).  This recovers intuitive results
    for uniform weights (median of {1,2,3,4,5} = 3).  Linear interpolation
    between adjacent observations for quantiles falling between bin centres.
    """
    if not vals:
        return [None] * len(quantiles)
    pairs = sorted(zip(vals, weights), key=lambda x: x[0])
    sv, sw = zip(*pairs)
    total  = sum(sw)
    # Midpoint cumulative weight for each observation
    cum    = 0.0
    cum_w  = []
    for w in sw:
        cum_w.append(cum + 0.5 * w / total)
        cum += w / total
    results = []
    for q in quantiles:
        if q <= cum_w[0]:
            results.append(sv[0])
            continue
        if q >= cum_w[-1]:
            results.append(sv[-1])
            continue
        for i in range(1, len(cum_w)):
            if cum_w[i] >= q:
                span_w = cum_w[i] - cum_w[i - 1]
                frac   = (q - cum_w[i - 1]) / span_w if span_w > 0 else 0.0
                results.append(sv[i - 1] + frac * (sv[i] - sv[i - 1]))
                break
    return results


def _tcm_burden_sweep(p_base, param_key, values):
    """
    For each parameter value in `values`, run run_tcm() at fixed N=p_base['N']
    and N_fill=1 (lifetime averages over the full N-year window), then compute
    population-weighted quantiles of wealth_burden and eff_rate across all
    4-tier × 10-bracket cells.

    Returns a list of dicts, one per non-skipped value:
      {
        'value'  : float,
        'x_raw'  : float (same as value, for log-transform at call site),
        'wb_min' : float,  'wb_q25': float, 'wb_med': float,
        'wb_q75' : float,  'wb_max': float,   # wealth_burden, fraction
        'er_min' : float,  'er_q25': float, 'er_med': float,
        'er_q75' : float,  'er_max': float,   # eff_rate, fraction
      }

    Cells where wealth_burden == 0.0 (taxpayer below W_min threshold) are
    included as genuine zeros — they represent no-liability cells and
    correctly drag the lower quantiles toward zero when W_min is high.
    """
    N = p_base['N']
    results = []
    for v in values:
        p = deepcopy(p_base)
        p[param_key] = v
        if p['tau_0'] >= p['tau_m'] or p['W_min'] < 0:
            continue
        try:
            tcm = model.run_tcm(p, N=N, N_fill=1)
        except Exception:
            continue

        wb_vals, er_vals, pops = [], [], []
        for tier in p['tiers']:
            diff = tier['differential']
            for cell in tcm[diff]:
                wb_vals.append(cell['wealth_burden'])
                er_vals.append(cell['eff_rate'])
                pops.append(cell['cell_pop'])

        wb_q = _weighted_quantiles(wb_vals, pops, [0.0, 0.25, 0.50, 0.75, 1.0])
        er_q = _weighted_quantiles(er_vals, pops, [0.0, 0.25, 0.50, 0.75, 1.0])

        results.append({
            'value':  v,
            'x_raw':  v,
            'wb_min': wb_q[0], 'wb_q25': wb_q[1], 'wb_med': wb_q[2],
            'wb_q75': wb_q[3], 'wb_max': wb_q[4],
            'er_min': er_q[0], 'er_q25': er_q[1], 'er_med': er_q[2],
            'er_q75': er_q[3], 'er_max': er_q[4],
        })

    return results


def _shade_band(ax, xs, mins, maxs, color, alpha=0.15):
    ax.fill_between(xs, mins, maxs, color=color, alpha=alpha, linewidth=0)


def _plot_median_band(ax, xs, mins, medians, maxs, color, label, lw=2):
    ax.plot(xs, medians, color=color, linewidth=lw, label=label, zorder=3)
    _shade_band(ax, xs, mins, maxs, color)


def _mark_baseline(ax, baseline_x_val):
    """Draw a vertical baseline marker."""
    ax.axvline(baseline_x_val, color=C_BASELINE, linewidth=1.0,
               linestyle=':', alpha=0.8, zorder=2)


def _pct_formatter(x, pos):
    return f'{x:.0f}%'


# ── FIGURE 1-4: per-parameter 4-panel sensitivity ────────────────────────────

def _four_panel(sweep_results, param_label, baseline_v, x_label,
                p_base=None, is_log=False, output_dir=None, fname=None,
                burden_data=None):
    """
    Generic 4-panel sensitivity figure for one swept parameter.

    Panels:
      [0,0] SSM & TCM coverage — median + min/max band
      [0,1] LRR fill year — median + min/max band
      [1,0] LRR surplus at fill — median + min/max band
      [1,1] Taxpayer burden distribution — population-weighted quantiles of
            wealth_burden (left y-axis, %) and eff_rate (right y-axis, %)
            across all 4-tier × 10-bracket cells at fixed N=p_base['N'].

    burden_data : list of dicts from _tcm_burden_sweep(), one per parameter
                  value.  If None the panel is left blank.
    """
    _base_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        f'Parameter sensitivity: {param_label}\n'
        f'Shaded band = min–max across 73 historical start years  |  '
        f'Line = median  |  Baseline marked in red',
        fontsize=11, y=1.01
    )

    # — Build x arrays —
    valid = [r for r in sweep_results if not r['skipped'] and r['summary'] is not None]
    xs_raw = [r['value'] for r in valid]
    xs = [math.log10(v) for v in xs_raw] if is_log else xs_raw
    base_x = math.log10(baseline_v) if is_log else baseline_v

    # — Panel [0,0]: SSM & TCM coverage —
    ax = axes[0, 0]
    ssm_xs, ssm_mins, ssm_meds, _, ssm_maxs = _extract_series(sweep_results, 'ssm_cov', transform=math.log10 if is_log else None)
    tcm_xs, tcm_mins, tcm_meds, _, tcm_maxs = _extract_series(sweep_results, 'tcm_cov', transform=math.log10 if is_log else None)

    ssm_meds_pct = [v * 100 for v in ssm_meds]
    ssm_mins_pct = [v * 100 for v in ssm_mins]
    ssm_maxs_pct = [v * 100 for v in ssm_maxs]
    tcm_meds_pct = [v * 100 for v in tcm_meds]
    tcm_mins_pct = [v * 100 for v in tcm_mins]
    tcm_maxs_pct = [v * 100 for v in tcm_maxs]

    _plot_median_band(ax, ssm_xs, ssm_mins_pct, ssm_meds_pct, ssm_maxs_pct,
                      C_SSM, f'SSM {HEADLINE_WINDOW}yr coverage (correlated-shock floor)')
    _plot_median_band(ax, tcm_xs, tcm_mins_pct, tcm_meds_pct, tcm_maxs_pct,
                      C_TCM, f'TCM {HEADLINE_WINDOW}yr coverage (heterogeneity ceiling)')
    ax.axhline(100, color='black', linewidth=0.8, linestyle='--', alpha=0.5,
               label='100% expenditure coverage')
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('Coverage fraction (%)', fontsize=10)
    ax.set_title(f'SSM & TCM {HEADLINE_WINDOW}yr coverage\n(Step-5 avg, post-fill)', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pct_formatter))
    ax.legend(fontsize=8, loc='upper left')
    if is_log:
        _set_log_xticks(ax, xs_raw)

    # — Panel [0,1]: LRR fill year —
    ax = axes[0, 1]
    lrr_xs, lrr_mins, lrr_meds, _, lrr_maxs = _extract_series(sweep_results, 'lrr_fill', transform=math.log10 if is_log else None)
    _plot_median_band(ax, lrr_xs, lrr_mins, lrr_meds, lrr_maxs, C_LRR,
                      'LRR fill year (median)')
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('Year from launch', fontsize=10)
    ax.set_title('LRR fill year\n(transition speed)', fontsize=10)
    ax.legend(fontsize=8)
    if is_log:
        _set_log_xticks(ax, xs_raw)

    # — Panel [1,0]: LRR surplus at fill —
    ax = axes[1, 0]
    sur_xs, sur_mins, sur_meds, _, sur_maxs = _extract_series(sweep_results, 'lrr_surplus', transform=math.log10 if is_log else None)
    _plot_median_band(ax, sur_xs, sur_mins, sur_meds, sur_maxs, C_SURPLUS,
                      'LRR surplus at fill (median)')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.4)
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('LRR surplus (£b)', fontsize=10)
    ax.set_title('LRR surplus at fill\n(safety margin above floor)', fontsize=10)
    ax.legend(fontsize=8)
    if is_log:
        _set_log_xticks(ax, xs_raw)

    # — Panel [1,1]: taxpayer burden distribution —
    ax1 = axes[1, 1]
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    C_WB = '#4e79a7'   # blue  — wealth burden (left axis)
    C_ER = '#e15759'   # red   — effective rate on gains (right axis)

    if burden_data:
        bd_xs_raw = [d['x_raw'] for d in burden_data]
        bd_xs     = [math.log10(v) for v in bd_xs_raw] if is_log else bd_xs_raw

        wb_min = [d['wb_min'] * 100 for d in burden_data]
        wb_q25 = [d['wb_q25'] * 100 for d in burden_data]
        wb_med = [d['wb_med'] * 100 for d in burden_data]
        wb_q75 = [d['wb_q75'] * 100 for d in burden_data]
        wb_max = [d['wb_max'] * 100 for d in burden_data]

        er_min = [d['er_min'] * 100 for d in burden_data]
        er_q25 = [d['er_q25'] * 100 for d in burden_data]
        er_med = [d['er_med'] * 100 for d in burden_data]
        er_q75 = [d['er_q75'] * 100 for d in burden_data]
        er_max = [d['er_max'] * 100 for d in burden_data]

        # Wealth burden — left axis
        ax1.fill_between(bd_xs, wb_min, wb_max,
                         color=C_WB, alpha=0.10, linewidth=0)
        ax1.fill_between(bd_xs, wb_q25, wb_q75,
                         color=C_WB, alpha=0.25, linewidth=0)
        ax1.plot(bd_xs, wb_med, color=C_WB, linewidth=2.0, zorder=3)

        # Effective rate on gains — right axis
        ax2.fill_between(bd_xs, er_min, er_max,
                         color=C_ER, alpha=0.10, linewidth=0)
        ax2.fill_between(bd_xs, er_q25, er_q75,
                         color=C_ER, alpha=0.25, linewidth=0)
        ax2.plot(bd_xs, er_med, color=C_ER, linewidth=2.0, zorder=3)

        # Band labels — right-edge text, placed just inside the final x value
        # so they never collide with the data bands of the other panels.
        # ax1 (left/blue) labels sit on wb values; ax2 (right/red) on er values.
        # A tight white bbox makes each label legible regardless of overlap.
        rx = bd_xs[-1]   # rightmost x position
        _lkw = dict(ha='right', fontsize=7.5, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.15', fc='white',
                              ec='none', alpha=0.75))

        ax1.text(rx, wb_med[-1],  'median',    color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_q75[-1],  '75th pct',  color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_q25[-1],  '25th pct',  color=C_WB, va='top',    **_lkw)
        ax1.text(rx, wb_max[-1],  'max',        color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_min[-1],  'min',        color=C_WB, va='top',    **_lkw)

        ax2.text(rx, er_med[-1],  'median',    color=C_ER, va='top',    **_lkw)
        ax2.text(rx, er_q75[-1],  '75th pct',  color=C_ER, va='top',    **_lkw)
        ax2.text(rx, er_q25[-1],  '25th pct',  color=C_ER, va='bottom', **_lkw)
        ax2.text(rx, er_max[-1],  'max',        color=C_ER, va='top',    **_lkw)
        ax2.text(rx, er_min[-1],  'min',        color=C_ER, va='bottom', **_lkw)

        if is_log:
            _set_log_xticks(ax1, bd_xs_raw)

    _mark_baseline(ax1, base_x)
    ax1.set_xlabel(x_label, fontsize=10)
    ax1.set_ylabel('Annual wealth burden — avg tax / net worth (%)',
                   fontsize=9, color=C_WB)
    ax2.set_ylabel('Effective rate on gains — net tax / TW (%)',
                   fontsize=9, color=C_ER)
    ax1.tick_params(axis='y', labelcolor=C_WB)
    ax2.tick_params(axis='y', labelcolor=C_ER)
    # Wealth burden: 3 decimal places (values are in the 0.001–1% range)
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v:.3f}%'))
    # Effective rate: 1 decimal place (values in the 1–30% range)
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v:.1f}%'))
    ax1.set_title(
        f'Taxpayer burden — population-weighted distribution\n'
        f'All cohorts, fixed N={p_base["N"]}  |  '
        f'Bands: min–max (outer) and 25th–75th percentile (inner)',
        fontsize=9)

    plt.tight_layout()
    return _save(fig, output_dir, fname)


def _set_log_xticks(ax, raw_values):
    """Set x-ticks to log10 positions with formatted labels."""
    log_vals = [math.log10(v) for v in raw_values]
    ax.set_xticks(log_vals)
    ax.set_xticklabels([f'{v:.4g}' for v in raw_values], rotation=35, ha='right', fontsize=8)


# ── FIGURES 7–8: SWF sizing parameter sensitivity (dual-milestone panel) ─────

def _four_panel_swf(sweep_results, param_label, baseline_v, x_label,
                    p_base=None, output_dir=None, fname=None):
    """
    4-panel sensitivity figure for SWF sizing parameters (srr_ratio, lrr_years).

    Panels [0,0], [0,1], [1,0] are identical to _four_panel().
    Panel [1,1] replaces the taxpayer-burden panel (which is flat for SWF sizing
    sweeps — the rate function is unchanged) with a dual-milestone panel showing:
      - SRR fill year (left axis, blue) — median + min/max band
      - LRR fill year (right axis, green) — median + min/max band
    This is the most informative panel for SWF sizing: it shows the two political
    milestones and how the gap between them changes with the swept parameter.
    """
    _base_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        f'SWF sizing sensitivity: {param_label}\n'
        f'Shaded band = min–max across 73 historical start years  |  '
        f'Line = median  |  Baseline marked in red  |  '
        f'Individual taxpayer burden is invariant across this sweep',
        fontsize=11, y=1.01
    )

    valid = [r for r in sweep_results if not r['skipped'] and r['summary'] is not None]
    xs_raw = [r['value'] for r in valid]
    xs     = xs_raw
    base_x = baseline_v

    # — Panel [0,0]: SSM & TCM coverage —
    ax = axes[0, 0]
    ssm_xs, ssm_mins, ssm_meds, _, ssm_maxs = _extract_series(sweep_results, 'ssm_cov')
    tcm_xs, tcm_mins, tcm_meds, _, tcm_maxs = _extract_series(sweep_results, 'tcm_cov')

    ssm_meds_pct = [v * 100 for v in ssm_meds]
    ssm_mins_pct = [v * 100 for v in ssm_mins]
    ssm_maxs_pct = [v * 100 for v in ssm_maxs]
    tcm_meds_pct = [v * 100 for v in tcm_meds]
    tcm_mins_pct = [v * 100 for v in tcm_mins]
    tcm_maxs_pct = [v * 100 for v in tcm_maxs]

    _plot_median_band(ax, ssm_xs, ssm_mins_pct, ssm_meds_pct, ssm_maxs_pct,
                      C_SSM, f'SSM {HEADLINE_WINDOW}yr coverage (correlated-shock floor)')
    _plot_median_band(ax, tcm_xs, tcm_mins_pct, tcm_meds_pct, tcm_maxs_pct,
                      C_TCM, f'TCM {HEADLINE_WINDOW}yr coverage (heterogeneity ceiling)')
    ax.axhline(100, color='black', linewidth=0.8, linestyle='--', alpha=0.5,
               label='100% expenditure coverage')
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('Coverage fraction (%)', fontsize=10)
    ax.set_title(f'SSM & TCM {HEADLINE_WINDOW}yr coverage\n(Step-5 avg, post-fill)', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pct_formatter))
    ax.legend(fontsize=8, loc='upper left')

    # — Panel [0,1]: LRR fill year —
    ax = axes[0, 1]
    lrr_xs, lrr_mins, lrr_meds, _, lrr_maxs = _extract_series(sweep_results, 'lrr_fill')
    _plot_median_band(ax, lrr_xs, lrr_mins, lrr_meds, lrr_maxs, C_LRR,
                      'LRR fill year (median)')
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('Year from launch', fontsize=10)
    ax.set_title('LRR fill year\n(transition speed)', fontsize=10)
    ax.legend(fontsize=8)

    # — Panel [1,0]: LRR surplus at fill —
    ax = axes[1, 0]
    sur_xs, sur_mins, sur_meds, _, sur_maxs = _extract_series(sweep_results, 'lrr_surplus')
    _plot_median_band(ax, sur_xs, sur_mins, sur_meds, sur_maxs, C_SURPLUS,
                      'LRR surplus at fill (median)')
    ax.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.4)
    _mark_baseline(ax, base_x)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel('LRR surplus (£b)', fontsize=10)
    ax.set_title('LRR surplus at fill\n(safety margin above floor)', fontsize=10)
    ax.legend(fontsize=8)

    # — Panel [1,1]: dual-milestone — SRR fill year (left) + LRR fill year (right) —
    # Both drawn on the same x-axis; the gap between the two lines is the
    # capitalisation window — the period during which the SRR is full but the LRR
    # has not yet reached its floor.  This is the politically critical window.
    ax1 = axes[1, 1]
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    C_SRR_FILL = '#4e79a7'   # blue  — SRR fill year (left axis)
    C_LRR_FILL = '#59a14f'   # green — LRR fill year (right axis)

    srr_xs, srr_f_mins, srr_f_meds, _, srr_f_maxs = _extract_series(sweep_results, 'srr_fill')
    lrr_f_xs, lrr_f_mins, lrr_f_meds, _, lrr_f_maxs = _extract_series(sweep_results, 'lrr_fill')

    if srr_xs:
        _shade_band(ax1, srr_xs, srr_f_mins, srr_f_maxs, C_SRR_FILL, alpha=0.15)
        ax1.plot(srr_xs, srr_f_meds, color=C_SRR_FILL, linewidth=2.0,
                 label='SRR fill year (median)', zorder=3)

    if lrr_f_xs:
        _shade_band(ax2, lrr_f_xs, lrr_f_mins, lrr_f_maxs, C_LRR_FILL, alpha=0.15)
        ax2.plot(lrr_f_xs, lrr_f_meds, color=C_LRR_FILL, linewidth=2.0,
                 label='LRR fill year (median)', zorder=3)

    _mark_baseline(ax1, base_x)
    ax1.set_xlabel(x_label, fontsize=10)
    ax1.set_ylabel('SRR fill year', fontsize=9, color=C_SRR_FILL)
    ax2.set_ylabel('LRR fill year', fontsize=9, color=C_LRR_FILL)
    ax1.tick_params(axis='y', labelcolor=C_SRR_FILL)
    ax2.tick_params(axis='y', labelcolor=C_LRR_FILL)
    ax1.set_title(
        'SRR fill year (left) vs LRR fill year (right)\n'
        'Gap between lines = capitalisation window (refund credible; Phase Two not yet viable)',
        fontsize=9)

    # Combined legend from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper left')

    plt.tight_layout()
    return _save(fig, output_dir, fname)


# ── FIGURE 5: rate function shapes ───────────────────────────────────────────

def _rate_function_shapes(p_base, output_dir):
    """
    Figure 5: 4-panel — τ(W) curve across the wealth range for each swept
    value of each parameter.  Uses a shared W axis 0–20 £m.
    """
    _base_style()
    from wdt_core import tau as _tau

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        'Rate function shape: τ(W) across the wealth range\n'
        'Each line = one parameter value; other three parameters held at Balanced baseline',
        fontsize=11, y=1.01
    )

    W_range = np.linspace(0, 5000, 500)

    configs = [
        (axes[0, 0], SWEEP_TAU_0, 'tau_0',
         'τ_0 (floor rate)', plt.cm.Blues,
         [f'{v:.0%}' for v in SWEEP_TAU_0]),
        (axes[0, 1], SWEEP_TAU_M, 'tau_m',
         'τ_m (ceiling rate)', plt.cm.Oranges,
         [f'{v:.0%}' for v in SWEEP_TAU_M]),
        (axes[1, 0], SWEEP_K, 'k',
         'k (steepness, per £m) — log-spaced', plt.cm.Greens,
         [f'{v:.4g}' for v in SWEEP_K]),
        (axes[1, 1], SWEEP_WMIN, 'W_min',
         'W_min (£m)', plt.cm.Purples,
         [f'£{v}m' for v in SWEEP_WMIN]),
    ]

    for ax, sweep_vals, param_key, title, cmap, labels in configs:
        n = len(sweep_vals)
        colours = [cmap(0.3 + 0.6 * i / max(n - 1, 1)) for i in range(n)]
        baseline_v = BASELINE[param_key]

        for i, (v, c, lbl) in enumerate(zip(sweep_vals, colours, labels)):
            p = deepcopy(p_base)
            p[param_key] = v
            rates = [_tau(w, p) * 100 for w in W_range]
            lw = 2.5 if abs(v - baseline_v) < 1e-9 else 1.2
            ls = '-' if abs(v - baseline_v) < 1e-9 else '-'
            alpha = 1.0 if abs(v - baseline_v) < 1e-9 else 0.65
            ax.plot(W_range, rates, color=c, linewidth=lw, alpha=alpha, label=lbl)

        ax.set_xlabel('Declared wealth W (£m)', fontsize=10)
        ax.set_ylabel('Marginal rate τ(W) (%)', fontsize=10)
        ax.set_title(title, fontsize=10)
        ax.set_xlim(0, 5000)
        ax.set_ylim(-2, 105)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pct_formatter))
        # Annotate baseline
        p_bl = deepcopy(p_base)
        rates_bl = [_tau(w, p_bl) * 100 for w in W_range]
        ax.plot(W_range, rates_bl, color=C_BASELINE, linewidth=2.0,
                linestyle='--', alpha=0.7, label=f'Baseline ({baseline_v})')
        ax.legend(fontsize=7, loc='lower right', ncol=2)

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_05_rate_function_shapes.png')


# ── FIGURE 6: relative sensitivity synthesis ─────────────────────────────────

def _relative_sensitivity(all_sweeps, output_dir):
    """
    Figure 6: normalised sensitivity comparison.

    For each parameter, normalise the parameter value to [0,1] across its
    sweep range and plot:
      - TCM coverage median (left axis, %)
      - LRR fill year median (right axis, years)

    This makes the relative potency of each parameter immediately visible.
    One line per parameter per metric, all on the same axes.
    """
    _base_style()
    fig, (ax_cov, ax_lrr) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        'Relative parameter sensitivity: normalised parameter value (0–1) vs key metrics\n'
        'Each line = one parameter swept from its minimum to maximum value  |  '
        'Vertical dashed = Balanced baseline position',
        fontsize=11, y=1.01
    )

    param_meta = [
        ('tau_0', SWEEP_TAU_0, BASELINE['tau_0'], 'τ_0 (floor rate)',      PARAM_COLOURS['tau_0']),
        ('tau_m', SWEEP_TAU_M, BASELINE['tau_m'], 'τ_m (ceiling rate)',    PARAM_COLOURS['tau_m']),
        ('k',     SWEEP_K,     BASELINE['k'],     'k (steepness)',          PARAM_COLOURS['k']),
        ('W_min', SWEEP_WMIN,  BASELINE['W_min'], 'W_min (entry £m)',      PARAM_COLOURS['W_min']),
    ]

    for (param_key, sweep_vals, baseline_v, label, colour), sweep_results in \
            zip(param_meta, all_sweeps):

        valid = [r for r in sweep_results if not r['skipped'] and r['summary'] is not None]
        if not valid:
            continue

        raw_vals = [r['value'] for r in valid]
        vmin, vmax = min(raw_vals), max(raw_vals)

        # Normalise to [0,1]
        if vmax == vmin:
            continue
        norm = [(v - vmin) / (vmax - vmin) for v in raw_vals]

        tcm_meds = [r['summary']['tcm_cov']['median'] * 100 for r in valid]
        lrr_meds = [r['summary']['lrr_fill']['median'] for r in valid]

        baseline_norm = (baseline_v - vmin) / (vmax - vmin)

        # Coverage panel
        ax_cov.plot(norm, tcm_meds, color=colour, linewidth=2.0,
                    marker='o', markersize=4, label=label)
        ax_cov.axvline(baseline_norm, color=colour, linewidth=0.8,
                       linestyle=':', alpha=0.6)

        # LRR fill year panel
        ax_lrr.plot(norm, lrr_meds, color=colour, linewidth=2.0,
                    marker='o', markersize=4, label=label)
        ax_lrr.axvline(baseline_norm, color=colour, linewidth=0.8,
                       linestyle=':', alpha=0.6)

    ax_cov.axhline(100, color='black', linewidth=0.8, linestyle='--',
                   alpha=0.5, label='100% coverage')
    ax_cov.set_xlabel('Normalised parameter value (0 = min, 1 = max)', fontsize=10)
    ax_cov.set_ylabel(f'TCM {HEADLINE_WINDOW}yr coverage — median across 73 start years (%)',
                      fontsize=10)
    ax_cov.set_title(f'TCM {HEADLINE_WINDOW}yr coverage (median)\nvs normalised parameter value',
                     fontsize=10)
    ax_cov.yaxis.set_major_formatter(mticker.FuncFormatter(_pct_formatter))
    ax_cov.legend(fontsize=9)

    ax_lrr.set_xlabel('Normalised parameter value (0 = min, 1 = max)', fontsize=10)
    ax_lrr.set_ylabel('LRR fill year — median across 73 start years', fontsize=10)
    ax_lrr.set_title('LRR fill year (median)\nvs normalised parameter value', fontsize=10)
    ax_lrr.legend(fontsize=9)

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_06_relative_sensitivity.png')


# ── FIGURE 9: coverage fan ────────────────────────────────────────────────────

def _coverage_fan(all_sweeps, sweep_labels, sweep_colours, output_dir):
    """
    Figure 9 — Coverage fan: SSM 5yr to TCM 50yr across all four rate parameters.

    Normalised x-axis (0 = min, 1 = max parameter value), one colour per
    parameter.  Each parameter contributes two shaded bands:
      outer band: SSM 5yr (lower bound) to TCM 50yr (upper bound)
      inner band: SSM {HW}yr to TCM {HW}yr  (headline window)
    and two solid lines (SSM {HW}yr median, TCM {HW}yr median).

    This figure shows the temporal profile of the coverage promise across
    the full rate-parameter space in a single view: how wide the
    SSM–TCM range is, and whether it narrows or widens with the parameter.
    """
    _base_style()
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle(
        f'Coverage fan: SSM 5yr to TCM 50yr across rate parameters\n'
        f'Outer band = SSM 5yr–TCM 50yr  |  '
        f'Inner band = SSM {HEADLINE_WINDOW}yr–TCM {HEADLINE_WINDOW}yr  |  '
        f'Lines = SSM/TCM {HEADLINE_WINDOW}yr median  |  '
        f'Normalised x-axis: 0 = min value, 1 = max value for each parameter',
        fontsize=10, y=1.02,
    )

    for sweep_results, label, colour in zip(all_sweeps, sweep_labels, sweep_colours):
        valid = [r for r in sweep_results if not r['skipped'] and r['summary'] is not None]
        if not valid:
            continue

        raw_vals = [r['value'] for r in valid]
        vmin, vmax = min(raw_vals), max(raw_vals)
        if vmax == vmin:
            continue
        norm = [(v - vmin) / (vmax - vmin) for v in raw_vals]

        def _meds(key):
            return [r['summary'][key]['median'] * 100
                    for r in valid
                    if r['summary'].get(key, {}).get('median') is not None]

        ssm_5   = _meds('ssm_cov_5')
        tcm_50  = _meds('tcm_cov_50')
        ssm_hw  = _meds('ssm_cov')    # headline alias
        tcm_hw  = _meds('tcm_cov')    # headline alias

        # Guard: all series must be same length as norm
        if not all(len(s) == len(norm) for s in [ssm_5, tcm_50, ssm_hw, tcm_hw]):
            continue

        # Outer band: SSM 5yr floor to TCM 50yr ceiling
        ax.fill_between(norm, ssm_5, tcm_50,
                         color=colour, alpha=0.10, linewidth=0)
        # Inner band: SSM HW to TCM HW
        ax.fill_between(norm, ssm_hw, tcm_hw,
                         color=colour, alpha=0.22, linewidth=0)
        # Headline median lines
        ax.plot(norm, ssm_hw, color=colour, linewidth=1.8, linestyle='-',
                alpha=0.85)
        ax.plot(norm, tcm_hw, color=colour, linewidth=1.8, linestyle='--',
                alpha=0.85, label=label)

    ax.axhline(100, color='black', linewidth=0.9, linestyle='--',
               alpha=0.5, label='100% expenditure coverage')
    ax.set_xlabel('Normalised parameter value (0 = min, 1 = max)', fontsize=11)
    ax.set_ylabel('Coverage fraction (%)', fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_pct_formatter))
    ax.legend(fontsize=9, loc='upper left',
              title=f'Parameter  (solid = SSM {HEADLINE_WINDOW}yr, dashed = TCM {HEADLINE_WINDOW}yr)',
              title_fontsize=8)
    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_09_coverage_fan.png')


# ── FIGURE 10: LRR failure year for SWF sweeps ───────────────────────────────

def _failure_year_swf(sw_srr_ratio, sw_lrr_years, output_dir):
    """
    Figure 10 — LRR failure year distribution across SWF sizing sweeps.

    1×2 panel: one panel per SWF parameter (srr_ratio, lrr_years).
    X-axis = parameter value.  Y-axis = LRR failure year (median, min, max
    across the 73 historical start years that produce a failure).

    At Balanced parameters lrr_failure_year is None for all 73 start years,
    so n=0 in the dist and the series is absent — the panel renders cleanly
    as an empty plot with only the baseline marker and a "no failures at
    baseline" annotation.  As parameters stress the SWF, failure years
    appear and the series fills in from the right (most-stressed end).

    This figure exercises the v8 failure mechanics and shows the parameter
    margin available before the LRR buffer is exhausted post-fill.
    """
    _base_style()
    fig, (ax_srr, ax_lrr) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        'LRR failure year across SWF sizing parameters\n'
        'LRR failure = LRR buffer hits zero post-fill (refund guarantee at risk)\n'
        'Empty series at a parameter value = no LRR failure across all 73 start years',
        fontsize=10, y=1.02,
    )

    C_FAIL = '#e15759'   # red — failure year

    configs = [
        (ax_srr, sw_srr_ratio, BASELINE.get('srr_ratio', 3.0),
         'srr_ratio (×)', 'SRR capitalisation ratio'),
        (ax_lrr, sw_lrr_years, BASELINE.get('lrr_years', 3.0),
         'lrr_years (years)', 'LRR floor (years of expenditure)'),
    ]

    for ax, sweep_results, baseline_v, x_label, title in configs:
        xs_fail, meds, mins_, maxs_ = [], [], [], []

        for r in sweep_results:
            if r['skipped'] or r['summary'] is None:
                continue
            d = r['summary']['lrr_failure']
            if d['n'] == 0:
                continue   # no failures at this parameter value — skip point
            xs_fail.append(r['value'])
            meds.append(d['median'])
            mins_.append(d['min'])
            maxs_.append(d['max'])

        if xs_fail:
            _shade_band(ax, xs_fail, mins_, maxs_, C_FAIL, alpha=0.20)
            ax.plot(xs_fail, meds, color=C_FAIL, linewidth=2.2,
                    marker='o', markersize=5, zorder=3,
                    label='LRR failure year (median)')
            ax.fill_between(xs_fail, mins_, maxs_,
                            color=C_FAIL, alpha=0.12, linewidth=0)

        _mark_baseline(ax, baseline_v)

        # Annotate baseline if no failures there
        baseline_row = next(
            (r for r in sweep_results
             if not r['skipped'] and r['summary'] is not None
             and abs(r['value'] - baseline_v) < 1e-9),
            None,
        )
        if baseline_row and baseline_row['summary']['lrr_failure']['n'] == 0:
            y_mid = 50   # midpoint annotation
            ax.text(baseline_v, y_mid,
                    f'Baseline ({baseline_v})\nno LRR failures',
                    ha='center', va='center', fontsize=8,
                    color=C_BASELINE, style='italic',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white',
                              ec=C_BASELINE, alpha=0.8))

        ax.set_xlabel(x_label, fontsize=10)
        ax.set_ylabel('LRR failure year', fontsize=10)
        ax.set_title(f'{title}\nLRR failure year distribution', fontsize=10)
        ax.set_ylim(0, 75)
        if xs_fail:
            ax.legend(fontsize=8)

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_10_failure_years.png')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    toml_path  = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    effective_toml = toml_path or str(DEFAULT_PARAMS)
    print(f'Loading parameters from: {effective_toml}')
    p_base = model.load_params(effective_toml)
    model.validate_params(p_base)

    # Populate module-level BASELINE and sweep grids from TOML.
    global BASELINE, SWEEP_TAU_0, SWEEP_TAU_M, SWEEP_K, SWEEP_WMIN, \
           SWEEP_SRR_RATIO, SWEEP_LRR_YEARS
    sw = p_base['sweep']
    BASELINE = {
        'tau_0':     p_base['tau_0'],
        'tau_m':     p_base['tau_m'],
        'k':         p_base['k'],
        'W_min':     p_base['W_min'],
        'srr_ratio': p_base['srr_ratio'],
        'lrr_years': p_base['lrr_years'],
    }
    SWEEP_TAU_0     = sw['rates_tau_0_sweep']
    SWEEP_TAU_M     = sw['rates_tau_m_sweep']
    SWEEP_K         = sw['rates_k_sweep']
    SWEEP_WMIN      = sw['rates_wmin_sweep']
    SWEEP_SRR_RATIO = sw['rates_srr_ratio_sweep']
    SWEEP_LRR_YEARS = sw['rates_lrr_years_sweep']

    _out = Path(output_dir) if output_dir else OUTPUT_DIR
    _out.mkdir(parents=True, exist_ok=True)

    print(f'\nBaseline (from TOML): τ_0={p_base["tau_0"]:.0%}  τ_m={p_base["tau_m"]:.0%}  '
          f'k={p_base["k"]}  W_min=£{p_base["W_min"]}m  '
          f'srr_ratio={p_base["srr_ratio"]}×  lrr_years={p_base["lrr_years"]}\n')

    # ── Run sweeps ─────────────────────────────────────────────
    print('=' * 60)
    print('SWEEP 1/4: τ_0')
    print('=' * 60)
    sw_tau0 = run_param_sweep(p_base, 'tau_0', SWEEP_TAU_0)

    print('\n' + '=' * 60)
    print('SWEEP 2/4: τ_m')
    print('=' * 60)
    sw_taum = run_param_sweep(p_base, 'tau_m', SWEEP_TAU_M)

    print('\n' + '=' * 60)
    print('SWEEP 3/4: k (log-spaced)')
    print('=' * 60)
    sw_k = run_param_sweep(p_base, 'k', SWEEP_K)

    print('\n' + '=' * 60)
    print('SWEEP 4/4: W_min')
    print('=' * 60)
    sw_wmin = run_param_sweep(p_base, 'W_min', SWEEP_WMIN)

    print('\n' + '=' * 60)
    print('SWEEP 5/6: srr_ratio (SRR capitalisation ratio)')
    print('=' * 60)
    sw_srr_ratio = run_param_sweep(p_base, 'srr_ratio', SWEEP_SRR_RATIO)

    print('\n' + '=' * 60)
    print('SWEEP 6/6: lrr_years (LRR floor, years of expenditure)')
    print('=' * 60)
    sw_lrr_years = run_param_sweep(p_base, 'lrr_years', SWEEP_LRR_YEARS)

    # ── Compute taxpayer burden sweeps (cheap: one run_tcm per value) ──────────
    # Note: burden is invariant across srr_ratio and lrr_years sweeps — the rate
    # function is unchanged.  No burden sweep is computed for those two parameters;
    # their fourth panel uses the dual-milestone design instead.
    print('\nComputing taxpayer burden sweeps (fixed N={})...'.format(p_base['N']))
    burden_tau0 = _tcm_burden_sweep(p_base, 'tau_0', SWEEP_TAU_0)
    burden_taum = _tcm_burden_sweep(p_base, 'tau_m', SWEEP_TAU_M)
    burden_k    = _tcm_burden_sweep(p_base, 'k',     SWEEP_K)
    burden_wmin = _tcm_burden_sweep(p_base, 'W_min', SWEEP_WMIN)
    print('  Burden sweeps complete.')

    # ── Generate figures ───────────────────────────────────────
    print('\nGenerating figures...')

    _four_panel(
        sw_tau0,
        param_label='τ_0 (floor rate)',
        baseline_v=BASELINE['tau_0'],
        x_label='τ_0 (floor rate)',
        p_base=p_base,
        is_log=False,
        output_dir=_out,
        fname='sweep_fig_01_tau0_sensitivity.png',
        burden_data=burden_tau0,
    )

    _four_panel(
        sw_taum,
        param_label='τ_m (ceiling rate)',
        baseline_v=BASELINE['tau_m'],
        x_label='τ_m (ceiling rate)',
        p_base=p_base,
        is_log=False,
        output_dir=_out,
        fname='sweep_fig_02_taum_sensitivity.png',
        burden_data=burden_taum,
    )

    _four_panel(
        sw_k,
        param_label='k (steepness, per £m) — log x-axis',
        baseline_v=BASELINE['k'],
        x_label='k (log scale)',
        p_base=p_base,
        is_log=True,
        output_dir=_out,
        fname='sweep_fig_03_k_sensitivity.png',
        burden_data=burden_k,
    )

    _four_panel(
        sw_wmin,
        param_label='W_min (entry point, £m)',
        baseline_v=BASELINE['W_min'],
        x_label='W_min (£m)',
        p_base=p_base,
        is_log=False,
        output_dir=_out,
        fname='sweep_fig_04_wmin_sensitivity.png',
        burden_data=burden_wmin,
    )

    _rate_function_shapes(p_base, _out)

    _relative_sensitivity([sw_tau0, sw_taum, sw_k, sw_wmin], _out)

    _four_panel_swf(
        sw_srr_ratio,
        param_label='srr_ratio (SRR capitalisation ratio)',
        baseline_v=BASELINE['srr_ratio'],
        x_label='srr_ratio (×)',
        p_base=p_base,
        output_dir=_out,
        fname='sweep_fig_07_srr_ratio_sensitivity.png',
    )

    _four_panel_swf(
        sw_lrr_years,
        param_label='lrr_years (LRR floor, years of expenditure)',
        baseline_v=BASELINE['lrr_years'],
        x_label='lrr_years (years)',
        p_base=p_base,
        output_dir=_out,
        fname='sweep_fig_08_lrr_years_sensitivity.png',
    )

    _coverage_fan(
        all_sweeps   = [sw_tau0, sw_taum, sw_k, sw_wmin],
        sweep_labels = ['τ_0 (floor rate)', 'τ_m (ceiling rate)',
                        'k (steepness)', 'W_min (entry £m)'],
        sweep_colours= [PARAM_COLOURS['tau_0'], PARAM_COLOURS['tau_m'],
                        PARAM_COLOURS['k'],     PARAM_COLOURS['W_min']],
        output_dir=_out,
    )

    _failure_year_swf(sw_srr_ratio, sw_lrr_years, _out)

    print('\nAll figures complete.')


if __name__ == '__main__':
    main()
