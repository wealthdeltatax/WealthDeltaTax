"""
WDT Rate Parameter Sensitivity Sweep — Charts
===============================================
Loads all sweep and burden data from OUTPUTS/sweep_cache.json (produced
by 16_0_compute.py) and produces ten publication-quality PNG figures.

Figures produced:
  sweep_fig_01  τ_0 sensitivity — 4-panel
  sweep_fig_02  τ_m sensitivity — 4-panel
  sweep_fig_03  k sensitivity   — 4-panel (log x-axis)
  sweep_fig_04  W_min sensitivity — 4-panel
  sweep_fig_05  Rate function shapes — 4-panel across all parameters
  sweep_fig_06  Relative sensitivity synthesis
  sweep_fig_07  srr_ratio sensitivity — 4-panel (SWF sizing)
  sweep_fig_08  lrr_years sensitivity — 4-panel (SWF sizing)
  sweep_fig_09  Coverage fan — SSM 5yr to TCM 50yr across all rate parameters
  sweep_fig_10  LRR failure year — SWF sizing sweeps srr_ratio and lrr_years
"""

import json
import math
from pathlib import Path
from copy import deepcopy

from wdt_analytics import (
    model, DEFAULT_PARAMS, init, HEADLINE_WINDOW,
)
from wdt_core import load_params, synthetic_returns
from wdt_fmt import fmt_pct1, out_dir, ensure_dir
from wdt_style import (apply_style, save_fig,
                        C_SSM, C_TCM, C_LRR, C_SURPLUS, C_BASELINE,
                        PARAM_COLOURS)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

OUTPUT_DIR = out_dir('RATES_S')
_CACHE     = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load_cache():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


# ── Sweep grids and baseline — populated from p_base in main() ───────────────
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


# _tcm_burden_sweep was moved to 16_0_compute.py; burden data is loaded from cache.


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
            across all 4-tier × 10-bracket cells at fixed N=p_base['tcm_N'].

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

        # One set of quantile labels only (ax1/blue); colour distinguishes series.
        ax1.text(rx, wb_med[-1],  'median',   color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_q75[-1],  '75th pct', color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_q25[-1],  '25th pct', color=C_WB, va='top',    **_lkw)
        ax1.text(rx, wb_max[-1],  'max',       color=C_WB, va='bottom', **_lkw)
        ax1.text(rx, wb_min[-1],  'min',       color=C_WB, va='top',    **_lkw)

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
        f'All cohorts, fixed N={p_base["tcm_N"]}  |  '
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
    ax.set_yscale('log')
    ax.legend(fontsize=9, loc='upper left',
              title=f'Parameter  (solid = SSM {HEADLINE_WINDOW}yr, dashed = TCM {HEADLINE_WINDOW}yr)',
              title_fontsize=8)
    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_09_coverage_fan.png')


# ── FIGURE 10: LRR failure year for SWF sweeps ───────────────────────────────

def _swf_stress_margins(sw_srr_ratio, sw_lrr_years, output_dir):
    """
    Figure 10 — SWF stress margins across srr_ratio and lrr_years sweeps.

    2×2 panel layout:
      [0,0]  Zero-coverage years (10yr window, 2006 worst case) vs srr_ratio
      [0,1]  Zero-coverage years (10yr window, 2006 worst case) vs lrr_years
      [1,0]  Min LRR balance at fill (2006 worst case, £b) vs srr_ratio
      [1,1]  Min LRR balance at fill (2006 worst case, £b) vs lrr_years

    Zero-coverage years = years in the post-fill window where cov_frac = 0,
    meaning WDT revenue does not fully cover Step-5 expenditure and the LRR
    buffer must absorb the shortfall.  The LRR exists precisely for this
    purpose; the question is whether the buffer is sized adequately.

    No failure occurs at Balanced parameters because the LRR buffer is never
    exhausted — this figure shows the stress margin (how much headroom exists)
    rather than a binary failure indicator.  If the 2006 worst case still shows
    zero-coverage years, those are years the LRR absorbs; the min LRR balance
    panel confirms the buffer was never drained.

    Distribution bands (min/max across 73 start years) are shown where the
    cache provides the full distribution via zero_cov_W keys; otherwise the
    2006 worst-case single value is plotted as a point series.
    """
    _base_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(
        'Fig 10 — SWF stress margins: zero-coverage years and LRR buffer headroom\n'
        'Zero-coverage years = years post-fill where WDT net revenue < Step-5 expenditure '
        '(LRR absorbs shortfall)\n'
        'No LRR buffer exhaustion occurs at Balanced parameters across all 73 start years',
        fontsize=10, y=1.02,
    )

    W = 10   # headline coverage window for zero-cov metric
    C_ZCOV  = '#e15759'   # red — stress signal
    C_HDROOM = C_LRR      # reuse LRR colour for headroom/balance

    srr_bl = BASELINE.get('srr_ratio', 3.0)
    lrr_bl = BASELINE.get('lrr_years', 3.0)

    def _zero_cov_series(sweep_results, window):
        """Extract zero-cov-year series from summary, using dist if available."""
        xs, meds, mins_, maxs_ = [], [], [], []
        key_dist = f'zero_cov_{window}'
        key_wc   = f'ssm_zero_cov_years_{window}'
        for r in sweep_results:
            if r['skipped'] or r['summary'] is None:
                continue
            s = r['summary']
            if key_dist in s and s[key_dist]['n'] > 0:
                d = s[key_dist]
                xs.append(r['value'])
                meds.append(d['median'])
                mins_.append(d['min'])
                maxs_.append(d['max'])
            elif s.get('worst_case_2006') and s['worst_case_2006'].get(key_wc) is not None:
                v = s['worst_case_2006'][key_wc]
                xs.append(r['value'])
                meds.append(v)
                mins_.append(v)
                maxs_.append(v)
        return xs, meds, mins_, maxs_

    def _min_lrr_series(sweep_results):
        """Extract min LRR balance at fill from worst_case_2006 (£b)."""
        xs, ys = [], []
        for r in sweep_results:
            if r['skipped'] or r['summary'] is None:
                continue
            wc = r['summary'].get('worst_case_2006')
            if wc and wc.get('lrr_surplus_at_fill') is not None:
                xs.append(r['value'])
                ys.append(wc['lrr_surplus_at_fill'])
        return xs, ys

    # ── Row 0: zero-coverage years ──────────────────────────────────────────
    for col, (sweep, baseline_v, xlabel, title) in enumerate([
        (sw_srr_ratio, srr_bl, 'srr_ratio (×)',
         f'Zero-coverage years ({W}yr window)\nvs SRR capitalisation ratio'),
        (sw_lrr_years, lrr_bl, 'lrr_years (years)',
         f'Zero-coverage years ({W}yr window)\nvs LRR floor'),
    ]):
        ax = axes[0, col]
        xs, meds, mins_, maxs_ = _zero_cov_series(sweep, W)
        if xs:
            has_band = any(lo != hi for lo, hi in zip(mins_, maxs_))
            if has_band:
                _shade_band(ax, xs, mins_, maxs_, C_ZCOV, alpha=0.18)
            ax.plot(xs, meds, color=C_ZCOV, linewidth=2.2,
                    marker='o', markersize=5, zorder=3,
                    label=f'Zero-cov yrs {W}yr'
                          + (' (median)' if has_band else ' (2006 worst case)'))
            if has_band:
                ax.fill_between(xs, mins_, maxs_, color=C_ZCOV, alpha=0.10, linewidth=0)
        _mark_baseline(ax, baseline_v)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(f'Zero-coverage years ({W}yr window)', fontsize=10)
        ax.set_title(title, fontsize=10)
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        ax.legend(fontsize=8)
        # Annotate what zero-cov years mean
        ax.text(0.02, 0.97,
                'Each zero-cov year drains the LRR buffer;\nsee lower panels for buffer size.',
                transform=ax.transAxes, fontsize=7, va='top', color='#555555',
                style='italic')

    # ── Row 1: min LRR balance at fill ──────────────────────────────────────
    for col, (sweep, baseline_v, xlabel, title) in enumerate([
        (sw_srr_ratio, srr_bl, 'srr_ratio (×)',
         'LRR surplus at fill (£b, 2006 worst case)\nvs SRR capitalisation ratio'),
        (sw_lrr_years, lrr_bl, 'lrr_years (years)',
         'LRR surplus at fill (£b, 2006 worst case)\nvs LRR floor'),
    ]):
        ax = axes[1, col]
        xs, ys = _min_lrr_series(sweep)
        if xs:
            ax.plot(xs, ys, color=C_HDROOM, linewidth=2.2,
                    marker='o', markersize=5, zorder=3,
                    label='LRR surplus at fill — 2006 (£b)')
            ax.fill_between(xs, 0, ys, color=C_HDROOM, alpha=0.12, linewidth=0)
        _mark_baseline(ax, baseline_v)
        ax.axhline(0, color='#333333', linewidth=0.8, linestyle='--', alpha=0.5)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel('LRR surplus at fill (£b)', fontsize=10)
        ax.set_title(title, fontsize=10)
        ax.legend(fontsize=8)

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_10_swf_stress_margins.png')


# ── Main ──────────────────────────────────────────────────────────────────────

# ── FIGURE 11: g sensitivity ──────────────────────────────────────────────────

def _g_sensitivity(sweep_results, output_dir):
    """
    Figure 11 — Deterministic g sweep: LRR fill year and coverage vs growth rate.

    2-panel figure:
      Left:  LRR fill year vs g.  Shows how transition speed varies with the
             underlying economic growth rate.  Lower g → slower fill because
             the WDT revenue base compounds more slowly.
      Right: SSM and TCM headline-window coverage vs g.  Shows the post-fill
             fiscal headroom as a function of growth.

    Unlike the historical start-year sweeps, each point here is a single
    deterministic run with a constant g series — no distribution band.
    """
    _base_style()
    fig, (ax_fill, ax_cov) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        'Fig 11 — Constant-g sensitivity: LRR fill year and coverage\n'
        'Each point = one deterministic SSM run with g applied uniformly. '
        'No start-year distribution.',
        fontsize=11, y=1.01,
    )

    fill_valid = [r for r in sweep_results
                  if not r['skipped']
                  and r['summary']
                  and r['summary'].get('lrr_fill', {}).get('median') is not None]
    cov_valid = [r for r in sweep_results
                 if not r['skipped']
                 and r['summary']
                 and r['summary'].get('ssm_cov', {}).get('median') is not None
                 and r['summary'].get('tcm_cov', {}).get('median') is not None]

    # Left: LRR fill year
    xs_fill   = [r['value'] * 100 for r in fill_valid]
    lrr_fills = [r['summary']['lrr_fill']['median'] for r in fill_valid]
    
    ax_fill.plot(xs_fill, lrr_fills, color=C_LRR, linewidth=2.2,
                 marker='o', markersize=6, zorder=3)
    _mark_baseline(ax_fill, BASELINE.get('hist_mean',
                   fill_valid[0]['value'] * 100 if fill_valid else 10) * 100 / 100 * 100)
    ax_fill.set_xlabel('Growth rate g (%)', fontsize=10)
    ax_fill.set_ylabel('LRR fill year', fontsize=10)
    ax_fill.set_title('LRR fill year\n(transition speed vs growth rate)', fontsize=10)

    # Annotate hist_mean
    hist_mean = BASELINE.get('hist_mean', None)
    if hist_mean:
        ax_fill.axvline(hist_mean * 100, color=C_BASELINE, linewidth=1.0,
                        linestyle=':', label=f'hist_mean = {hist_mean:.2%}')
        ax_fill.legend(fontsize=8)

    # Right: SSM and TCM coverage
    xs_cov = [r['value'] * 100 for r in cov_valid]
    ssm_cov = [r['summary']['ssm_cov']['median'] * 100 for r in cov_valid]
    tcm_cov = [r['summary']['tcm_cov']['median'] * 100 for r in cov_valid]
    ax_cov.plot(xs_cov, ssm_cov, color=C_SSM, linewidth=2.2, marker='o', markersize=5,
                label=f'SSM {HEADLINE_WINDOW}yr (correlated-shock floor)')
    ax_cov.plot(xs_cov, tcm_cov, color=C_TCM, linewidth=2.2, marker='o', markersize=5,
                label=f'TCM {HEADLINE_WINDOW}yr (heterogeneity ceiling)')
    ax_cov.axhline(100, color='black', linewidth=0.8, linestyle='--', alpha=0.5,
                   label='100% expenditure coverage')
    if hist_mean:
        ax_cov.axvline(hist_mean * 100, color=C_BASELINE, linewidth=1.0, linestyle=':')
    ax_cov.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax_cov.set_xlabel('Growth rate g (%)', fontsize=10)
    ax_cov.set_ylabel(f'Coverage fraction (%)', fontsize=10)
    ax_cov.set_title(f'SSM & TCM {HEADLINE_WINDOW}yr coverage\n(post-fill, Step-5 avg)',
                     fontsize=10)
    ax_cov.legend(fontsize=8, loc='upper left')

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_11_g_sensitivity.png')


# ── FIGURE 12: synthetic scenario ─────────────────────────────────────────────

def _synthetic_scenario(amp_results, per_results, canonical_series,
                         syn_params, output_dir):
    """
    Figure 12 — Synthetic stress-test scenario: mu = inflation floor, A dips negative.

    Purpose: address the criticism that the WDT is not stress-tested under
    negative growth.  mu is set to 2% (UK CPI inflation floor) so the
    mean growth rate is barely positive.  Amplitude A then drives g negative
    for part of each cycle.  At canonical A = 4%, g oscillates between -2%
    and +6% — more adverse than any recorded decade of UK equity returns.

    2×2 panel layout:
      [0,0]  Canonical synthetic series shape (first 50 years), overlaid with
             multiple amplitude values to show the negative-growth excursions.
      [0,1]  Zero-coverage years (10yr window) vs amplitude A.
             Shows how many post-fill years the LRR buffer must absorb as
             the stress severity increases.
      [1,0]  LRR fill year vs period T (A fixed at canonical).
             Flat/near-flat line demonstrates cycle-length insensitivity.
      [1,1]  Per-year cov_frac trajectory post-fill for each amplitude value.
             x = years post-fill; y = cov_frac.  100% line = Governing Council
             recalibration trigger.  Shows the system recovering to steady-state
             coverage even after deep negative-growth years.
    """
    _base_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    mu_pct = syn_params['mu'] * 100
    A_pct  = syn_params['amplitude'] * 100
    T      = syn_params['period']
    fig.suptitle(
        r'Fig 12 — Synthetic stress-test: $g(t) = \mu + A \sin(2\pi t / T)$, '
        r'$\lambda = 0$'
        '\n'
        f'μ = {mu_pct:.0f}% (inflation floor)  |  '
        f'Canonical A = {A_pct:.0f}% (g oscillates {mu_pct - A_pct:.0f}% to {mu_pct + A_pct:.0f}%)  |  '
        f'T = {T:.0f} yr',
        fontsize=10, y=1.02,
    )

    # Colour ramp for amplitude values — darker = more stress
    AMP_COLOURS = [
        '#b2df8a', '#78c679', '#41ab5d', '#238b45',
        '#006d2c', '#00441b', '#1a1a1a', '#888888',
    ]

    amp_valid = [r for r in amp_results
                 if not r['skipped'] and r['summary']]

    # ── Panel [0,0]: canonical series shape with amplitude overlays ───────────
    ax = axes[0, 0]
    # Show multiple amplitude curves so the reader sees negative-growth excursions
    t_plot = list(range(min(50, len(canonical_series))))
    for idx, r in enumerate(amp_valid):
        raw = r['summary'].get('_raw', {})
        ssm_full = raw.get('ssm_full', [])
        if not ssm_full:
            continue
        g_series = [row['g'] * 100 for row in ssm_full[:50]]
        t_series = list(range(len(g_series)))
        A_val = r['value']
        color = AMP_COLOURS[idx % len(AMP_COLOURS)]
        lw    = 2.0 if abs(A_val - syn_params['amplitude']) < 1e-9 else 1.0
        label = f'A = {A_val:.0%}' + (' ◄ canonical' if lw == 2.0 else '')
        ax.plot(t_series, g_series, color=color, linewidth=lw,
                label=label, alpha=0.85)
    ax.axhline(mu_pct, color='#888888', linewidth=0.9, linestyle='--',
               label=f'μ = {mu_pct:.0f}%')
    ax.axhline(0, color='#333333', linewidth=0.7, linestyle=':',
               label='g = 0', alpha=0.7)
    ax.fill_between(t_plot,
                    [0] * len(t_plot),
                    [min(0, canonical_series[t] * 100) for t in t_plot],
                    color='#e15759', alpha=0.18, label='Negative growth region')
    ax.set_xlabel('Year t', fontsize=10)
    ax.set_ylabel('Growth rate g(t) (%)', fontsize=10)
    ax.set_title('Synthetic stress series — amplitude overlay\n'
                 '(red shading = negative growth years)', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.legend(fontsize=7, loc='upper right', ncol=2)

    # ── Panel [0,1]: zero-coverage years vs amplitude ────────────────────────
    ax = axes[0, 1]
    W = 10
    amp_xs_zcov, amp_zcov = [], []
    for r in amp_valid:
        s   = r['summary']
        raw = s.get('_raw', {})
        # Prefer aggregated distribution; fall back to single-run value from _raw;
        # final fallback: compute directly from ssm_full post-fill rows.
        dist = s.get(f'zero_cov_{W}')
        if dist and dist['n'] > 0:
            amp_xs_zcov.append(r['value'] * 100)
            amp_zcov.append(dist['median'])
        else:
            zc = raw.get(f'ssm_zero_cov_years_{W}')
            if zc is not None:
                amp_xs_zcov.append(r['value'] * 100)
                amp_zcov.append(zc)
            else:
                ssm_full = raw.get('ssm_full', [])
                fill_yr  = raw.get('lrr_fill_year')
                if ssm_full and fill_yr is not None:
                    post_window = [row for row in ssm_full
                                   if row['year'] > fill_yr][:W]
                    zc_computed = sum(1 for row in post_window
                                      if row.get('cov_frac', 1.0) == 0.0)
                    amp_xs_zcov.append(r['value'] * 100)
                    amp_zcov.append(zc_computed)
    if amp_xs_zcov:
        ax.bar(amp_xs_zcov, amp_zcov, width=0.8,
               color='#e15759', alpha=0.75, edgecolor='#333333', linewidth=0.5,
               label=f'Zero-cov years ({W}yr window)')
        ax.axvline(A_pct, color=C_BASELINE, linewidth=1.2, linestyle=':',
                   label=f'Canonical A = {A_pct:.0f}%')
    ax.set_xlabel('Amplitude A (%)', fontsize=10)
    ax.set_ylabel(f'Zero-coverage years ({W}yr window)', fontsize=10)
    ax.set_title('Years LRR buffer must absorb shortfall\nvs stress amplitude',
                 fontsize=10)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.legend(fontsize=8)
    ax.text(0.02, 0.97,
            'LRR exists to cover these years.\nBuffer sizing shown in Fig 10.',
            transform=ax.transAxes, fontsize=7, va='top',
            color='#555555', style='italic')

    # ── Panel [1,0]: LRR fill year vs period T ───────────────────────────────
    ax = axes[1, 0]
    per_valid = [r for r in per_results if not r['skipped'] and r['summary']
                 and r['summary'].get('lrr_fill', {}).get('median') is not None]
    if per_valid:
        per_xs   = [r['value'] for r in per_valid]
        per_fill = [r['summary']['lrr_fill']['median'] for r in per_valid]
        ax.plot(per_xs, per_fill, color=C_LRR, linewidth=2.2,
                marker='o', markersize=6)
        ax.axvline(T, color=C_BASELINE, linewidth=1.2, linestyle=':',
                   label=f'Canonical T = {T:.0f} yr')
        ax.set_ylim(0, max(per_fill) * 1.5)   # prevent line sitting at bottom edge
        ax.legend(fontsize=8)
    ax.set_xlabel('Period T (years)', fontsize=10)
    ax.set_ylabel('LRR fill year', fontsize=10)
    ax.set_title('LRR fill year vs cycle period\n'
                 '(A = canonical; near-flat = cycle-length insensitivity)', fontsize=10)

    # ── Panel [1,1]: per-year cov_frac trajectory post-fill ──────────────────
    ax = axes[1, 1]
    drew_any = False
    for idx, r in enumerate(amp_valid):
        raw      = r['summary'].get('_raw', {})
        ssm_full = raw.get('ssm_full', [])
        lrr_fill = raw.get('lrr_fill_year')
        if not ssm_full or lrr_fill is None:
            continue
        # Extract post-fill rows; x = years since fill, y = cov_frac %
        post = [(row['year'] - lrr_fill, row['cov_frac'] * 100)
                for row in ssm_full
                if row.get('lrr_filled') and row['year'] > lrr_fill
                and row.get('cov_frac') is not None]
        if not post:
            continue
        t_post   = list(t for t, _ in post)
        cov_post = list(c for _, c in post)
        A_val  = r['value']
        color  = AMP_COLOURS[idx % len(AMP_COLOURS)]
        lw     = 2.2 if abs(A_val - syn_params['amplitude']) < 1e-9 else 1.2
        label  = f'A = {A_val:.0%}' + (' ◄' if lw == 2.2 else '')
        ax.plot(t_post, cov_post, color=color, linewidth=lw, label=label, alpha=0.85)
        drew_any = True

    ax.axhline(100, color='black', linewidth=1.0, linestyle='--', alpha=0.6,
               label='100% expenditure coverage\n(Governing Council recalibration trigger)')
    if not drew_any:
        ax.text(0.5, 0.5, 'Regenerate cache with updated TOML\n(mu=2% stress-test scenario)',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=9, color='#888888', style='italic')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.set_xlabel('Years post-LRR fill', fontsize=10)
    ax.set_ylabel('Step-5 coverage fraction (%)', fontsize=10)
    ax.set_title('Coverage trajectory post-fill by amplitude\n'
                 '(x = years since LRR fill; 100% = recalibration trigger)', fontsize=10)
    ax.legend(fontsize=7, loc='upper left', ncol=2)

    plt.tight_layout()
    return _save(fig, output_dir, 'sweep_fig_12_synthetic_scenario.png')


def main():
    p_base = load_params()
    print(p_base)
    model.validate_params(p_base)
    init(p_base)

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

    _out = OUTPUT_DIR
    ensure_dir(_out)

    print(f'16_7 RATES_S charts — loading from cache')
    print(f'Baseline: τ_0={p_base["tau_0"]:.0%}  τ_m={p_base["tau_m"]:.0%}  '
          f'k={p_base["k"]}  W_min=£{p_base["W_min"]}m  '
          f'srr_ratio={p_base["srr_ratio"]}×  lrr_years={p_base["lrr_years"]}\n')

    # ── Load all pre-computed data from cache ─────────────────
    d = _load_cache()
    rs = d['rates_s']

    sw_tau0      = rs['rates_tau0_sweep']
    sw_taum      = rs['rates_taum_sweep']
    sw_k         = rs['rates_k_sweep']
    sw_wmin      = rs['rates_wmin_sweep']
    sw_srr_ratio = rs['rates_srr_sweep']
    sw_lrr_years = rs['rates_lrr_sweep']

    burden_tau0  = rs['burden_tau0']
    burden_taum  = rs['burden_taum']
    burden_k     = rs['burden_k']
    burden_wmin  = rs['burden_wmin']

    sw_g_sweep           = rs['rates_g_sweep']
    sw_amp_sweep         = rs['synthetic_amplitude_sweep']
    sw_per_sweep         = rs['synthetic_period_sweep']
    canonical_syn_series = rs['synthetic_canonical_series']
    syn_params           = rs['synthetic_params']

    # Store hist_mean in BASELINE for use by _g_sensitivity
    BASELINE['hist_mean'] = p_base['hist_mean']

    # ── Generate figures ──────────────────────────────────────
    print('Generating figures...')

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

    _swf_stress_margins(sw_srr_ratio, sw_lrr_years, _out)

    _g_sensitivity(sw_g_sweep, _out)

    _synthetic_scenario(sw_amp_sweep, sw_per_sweep,
                        canonical_syn_series, syn_params, _out)

    print('\nAll figures complete.')


if __name__ == '__main__':
    main()