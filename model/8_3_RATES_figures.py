"""
WDT Rates and Revenue — Figures  (v8)
======================================
Produces all nine RATES PNG figures:

    OUTPUTS/RATES/rates_fig_01_sweep_breakeven_coverage.png
    OUTPUTS/RATES/rates_fig_02_revenue_concentration_heatmap.png
    OUTPUTS/RATES/rates_fig_03_terminal_wealth_by_tier.png
    OUTPUTS/RATES/rates_fig_04_srr_lrr_trajectory.png
    OUTPUTS/RATES/rates_fig_05_coverage_by_cycle.png
    OUTPUTS/RATES/rates_fig_06_burden_matrix_heatmap.png
    OUTPUTS/RATES/rates_fig_07_ssm_tcm_coverage_range.png
    OUTPUTS/RATES/rates_fig_08_loss_year_mechanics.png
    OUTPUTS/RATES/rates_fig_09_phase_two_transition.png

Figure inventory
----------------
  01  Start-year sweep scatter: LRR breakeven year and 10yr TCM coverage.
  02  Revenue concentration heatmap: cohort share of total revenue (%).
  03  Terminal net worth at year N by growth tier, upper brackets only.
  04  SRR and LRR reserve trajectories over the capitalisation window.
  05  SSM 10yr coverage distribution by economic cycle (box plots, v8).
  06  Two-panel burden matrix: annual wealth burden and effective rate
      on gains, 4 tiers × 10 brackets.
  07  Per-start-year 10yr SSM/TCM coverage range band, coloured by cycle.
  08  Loss-year mechanics: symmetric refund in the worst return year,
      95th percentile bracket, Good tier.
  09  Phase Two stress profile: LRR balance vs target + Step-5 coverage
      fraction, full 71-year window, two stacked panels.

Usage
-----
  python3 8_3_RATES_figures.py [params.toml] [output_dir]

  params.toml  defaults to WDT_Params.toml in the same directory.
  output_dir   defaults to ./OUTPUTS/RATES/

Can also be imported and called directly:

    from 8_3_RATES_figures import generate_figures
    generate_figures(p, py_ssm, py_tcm, sweep_results, tcm_N=N)
"""

import sys
from pathlib import Path

import rates_model as model
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker
import numpy as np

from wdt_core import simulate
from wdt_fmt import ensure_dir, out_dir
from wdt_style import (
    apply_style, save_fig,
    FIG_WIDE,
    C_SSM, C_TCM, C_LRR, C_BASELINE, C_ANNOTATION,
    CYCLE_BUCKETS,
)

DEFAULT_PARAMS = Path(__file__).parent / 'WDT_Params.toml'
_OUT           = out_dir('RATES')

# Figure sizes used in this script.
# Three figures use FIG_WIDE (13, 6) exactly; the others are bespoke RATES
# sizes not yet in wdt_style — defined here as named constants.
_FIG_SWEEP    = (12, 6)   # figs 01, 08 — sweep/loss year with twin axes
_FIG_HEAT_WIDE= (13, 4)   # fig 02 — wide shallow heatmap
_FIG_BOX      = (10, 6)   # fig 05 — box plot, fewer x categories
_FIG_BURDEN   = (18, 5)   # fig 06 — two-panel burden matrix, very wide
_FIG_STACK    = (13, 8)   # fig 09 — two stacked panels

# Colour aliases reused across multiple figures
_C_NEUTRAL    = '#555555'   # reference lines, annotation text
_C_DARK       = '#333333'   # contour labels, axis grid references
_C_CRASH      = '#c03020'   # crash year annotation (red-brown)
_C_TIER_GREY  = '#bab0ac'   # V0 (starting wealth) bars in fig 03
_C_ZONE_AMBER = '#f28e2b'   # below-floor shading in fig 09 (= C_TCM)
_C_ZONE_RED   = '#e15759'   # zero-coverage bars in fig 09 (= C_BASELINE)


# ─────────────────────────────────────────────────────────────
# PUBLIC ENTRY POINT
# ─────────────────────────────────────────────────────────────

def generate_figures(p, py_ssm, py_tcm, sweep_results,
                     output_dir=None, tcm_N=None):
    """
    Generate all nine RATES figures and save to output_dir.

    Parameters
    ----------
    p            : dict   loaded params (wdt_core.load_params())
    py_ssm       : list   run_ssm() result
    py_tcm       : dict   run_tcm() result (keyed by tier differential)
    sweep_results: list   run_start_year_sweep() result
    output_dir   : Path   override; defaults to OUTPUTS/RATES/
    tcm_N        : int    TCM horizon (SSM LRR fill year); needed for fig 03
    """
    out = ensure_dir(Path(output_dir) if output_dir else _OUT)
    if tcm_N is None:
        py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)
        tcm_N = p['tcm_N']

    print('\nGenerating RATES figures...')
    _fig01(p, sweep_results, out)
    _fig02(p, py_tcm, out)
    _fig03(p, py_tcm, tcm_N, out)
    _fig04(p, py_ssm, out)
    _fig05(sweep_results, out)
    _fig06(p, py_tcm, out)
    _fig07(p, sweep_results, out)
    _fig08(p, py_tcm, out)
    _fig09(p, py_ssm, out)
    print('  All figures complete.')


# ─────────────────────────────────────────────────────────────
# SHARED SAVE HELPER
# ─────────────────────────────────────────────────────────────

def _save(fig, out_dir, name):
    return save_fig(fig, Path(out_dir) / name)


# ─────────────────────────────────────────────────────────────
# FIG 01 — Start-year sweep scatter
# ─────────────────────────────────────────────────────────────

def _fig01(p, sweep_results, out_dir):
    """Scatter: LRR breakeven year (left axis) and 10yr TCM coverage (right axis)."""
    apply_style()
    fig, ax1 = plt.subplots(figsize=_FIG_SWEEP)
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    active_year = p['scenario_start_year']

    for label, yr_from, yr_to, colour in CYCLE_BUCKETS:
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
        ax1.scatter(years, breakevn, color=colour, s=40, alpha=0.8,
                    label=label, zorder=3)
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

    all_lrr = [r['lrr_fill_year'] for r in sweep_results
               if r.get('lrr_fill_year') is not None]
    all_tcm = [r['tcm_cov_10'] * 100
               for r in sweep_results if r.get('tcm_cov_10') is not None]

    N_TICKS = 6
    ax1_lo, ax1_hi = 0, max(all_lrr) * 1.15 if all_lrr else 40
    ax2_lo, ax2_hi = 0, max(all_tcm) * 1.10 if all_tcm else 400
    ax1.set_ylim(ax1_lo, ax1_hi)
    ax2.set_ylim(ax2_lo, ax2_hi)
    ax2.axhline(100, color='black', linewidth=0.9, linestyle='--',
                alpha=0.5, label='100% TCM coverage')

    fracs = [i / (N_TICKS - 1) for i in range(N_TICKS)]
    ax1.set_yticks([ax1_lo + f * (ax1_hi - ax1_lo) for f in fracs])
    ax1.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}'))
    ax2.set_yticks([ax2_lo + f * (ax2_hi - ax2_lo) for f in fracs])
    ax2.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))

    ax1.set_xlabel('Start year', fontsize=11)
    ax1.set_ylabel('LRR breakeven year', fontsize=11)
    ax2.set_ylabel('TCM 10yr coverage (%)', fontsize=11)
    ax1.set_title(
        'Start-year sweep: LRR breakeven and 10yr TCM coverage\n'
        'Circles = breakeven year (left axis)  |  '
        'Triangles = TCM 10yr coverage (right axis)',
        fontsize=11, pad=12)

    handles = [mpatches.Patch(color=c, label=l) for l, _, _, c in CYCLE_BUCKETS]
    handles.append(plt.Line2D([0], [0], marker='D', color='black',
                              linestyle='None', markersize=8,
                              label=f'{active_year} (active scenario)'))
    handles.append(plt.Line2D([0], [0], color='black', linestyle='--',
                              alpha=0.5, linewidth=0.9, label='100% TCM coverage'))
    ax1.legend(handles=handles, fontsize=9, loc='upper left')
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_01_sweep_breakeven_coverage.png')


# ─────────────────────────────────────────────────────────────
# FIG 02 — Revenue concentration heatmap
# ─────────────────────────────────────────────────────────────

def _fig02(p, py_tcm, out_dir):
    """Heatmap of cohort share of capitalisation-window revenue (%)."""
    apply_style()
    diffs   = [t['differential'] for t in p['tiers']]
    tlabels = [f"{t['differential']:+.2%}\n({t['label']})" for t in p['tiers']]
    blabels = [b['label'] for b in p['brackets']]

    grand_total = sum(r['post_fill_revenue_m'] for d in diffs for r in py_tcm[d])
    matrix = np.zeros((len(diffs), len(blabels)))
    for i, diff in enumerate(diffs):
        for j, r in enumerate(py_tcm[diff]):
            matrix[i, j] = (r['post_fill_revenue_m'] / grand_total * 100
                            if grand_total > 0 else 0.0)

    fig, ax = plt.subplots(figsize=_FIG_HEAT_WIDE)
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    ax.grid(False)
    ax.set_xticks(range(len(blabels))); ax.set_xticklabels(blabels, fontsize=9)
    ax.set_yticks(range(len(diffs)));   ax.set_yticklabels(tlabels, fontsize=9)
    ax.set_xlabel('Wealth percentile bracket', fontsize=10)
    ax.set_ylabel('Growth tier', fontsize=10)
    ax.set_title(
        'Revenue concentration: cohort share of total capitalisation-window revenue (%)\n'
        'RATES.A §B.3.8  |  Revenue dip at 90th pct reflects population-weight step: '
        'bracket population halves at 90th percentile boundary',
        fontsize=9, pad=12)
    for i in range(len(diffs)):
        for j in range(len(blabels)):
            val = matrix[i, j]
            ax.text(j, i, f'{val:.1f}%', ha='center', va='center', fontsize=8,
                    color='white' if val > 6 else 'black', fontweight='bold')
    fig.colorbar(im, ax=ax, shrink=0.8).set_label('Share of total revenue (%)', fontsize=9)
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_02_revenue_concentration_heatmap.png')


# ─────────────────────────────────────────────────────────────
# FIG 03 — Terminal wealth by tier
# ─────────────────────────────────────────────────────────────

def _fig03(p, py_tcm, tcm_N, out_dir):
    """Bar chart of V0 and V_N for upper brackets by growth tier (log scale)."""
    apply_style()
    diffs     = [t['differential'] for t in p['tiers']]
    tlabels   = [f"{t['label']} ({t['differential']:+.2%})" for t in p['tiers']]
    tier_cols = [C_SSM, C_TCM, C_LRR, C_BASELINE]
    upper_idx = list(range(4, 10))
    upper_lbl = [p['brackets'][i]['label'] for i in upper_idx]
    v0_vals   = [p['brackets'][i]['V0_m']  for i in upper_idx]

    fig, ax = plt.subplots(figsize=FIG_WIDE)
    n_series = len(diffs) + 1
    width    = 0.12
    x        = np.arange(len(upper_idx))
    offsets  = np.linspace(-(n_series - 1) / 2 * width,
                            (n_series - 1) / 2 * width, n_series)

    ax.bar(x + offsets[0], v0_vals, width=width, color=_C_TIER_GREY,
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
        f'Terminal net worth at year N={tcm_N}: $V_0$ (starting) and '
        f'V_N (pre-settlement) by tier\n'
        'RATES.A §B.3.1 — WDT paid throughout; compounding base intact',
        fontsize=11, pad=12)
    ax.legend(fontsize=9, loc='upper left')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}m'))
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_03_terminal_wealth_by_tier.png')


# ─────────────────────────────────────────────────────────────
# FIG 04 — SRR/LRR reserve trajectories
# ─────────────────────────────────────────────────────────────

def _fig04(p, py_ssm, out_dir):
    """SRR and LRR balance vs target over the capitalisation window."""
    apply_style()
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

    fig, ax = plt.subplots(figsize=FIG_WIDE)
    ax.plot(years, srr_bal, color=C_SSM, linewidth=2, label='SRR balance')
    ax.plot(years, srr_tgt, color=C_SSM, linewidth=1, linestyle='--',
            alpha=0.6, label='SRR target')
    ax.plot(years, lrr_bal, color=C_TCM, linewidth=2, label='LRR balance')
    ax.plot(years, lrr_tgt, color=C_TCM, linewidth=1, linestyle='--',
            alpha=0.6, label='LRR target')
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(3))

    y_max = max(max(lrr_bal), max(lrr_tgt), max(srr_bal))
    if srr_fill:
        ax.axvline(srr_fill, color=C_SSM, linestyle=':', alpha=0.8)
        ax.text(srr_fill + 0.4, y_max * 0.92, f'SRR fill\nyr {srr_fill}',
                fontsize=8, color=C_SSM, va='top')
    ax.axvline(lrr_fill_yr, color=C_TCM, linestyle=':', alpha=0.8)
    ax.text(lrr_fill_yr - 1, y_max * 0.75, f'LRR fill\nyr {lrr_fill_yr}',
            fontsize=8, color=C_TCM, va='top')

    worst_row = min((r for r in ssm_clip if r['year'] >= 1), key=lambda r: r['g'])
    if worst_row['g'] < 0:
        crash_sim_yr = worst_row['year']
        crash_cal_yr = p['scenario_start_year'] + crash_sim_yr - 1
        crash_pct    = worst_row['g'] * 100
        srr_at_crash = worst_row['srr_balance']
        ax.annotate(
            f'{crash_cal_yr} crash\n({crash_pct:+.2f}% return)',
            xy=(crash_sim_yr, srr_at_crash),
            xytext=(crash_sim_yr + 3, srr_at_crash + y_max * -0.06),
            fontsize=7.5, color=C_ANNOTATION,
            arrowprops=dict(arrowstyle='->', color=C_ANNOTATION, lw=0.8))

    ax.set_xlabel('Year from launch', fontsize=11)
    ax.set_ylabel('Reserve balance (£b)', fontsize=11)
    ax.set_title(
        f'SRR and LRR reserve trajectories — {p["scenario_start_year"]} '
        f'Balanced scenario\n'
        f'Capitalisation window (years 1–{lrr_fill_yr}) '
        '| Solid = balance  |  Dashed = target',
        fontsize=11, pad=12)
    ax.legend(fontsize=9, loc='upper left')
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_04_srr_lrr_trajectory.png')


# ─────────────────────────────────────────────────────────────
# FIG 05 — Coverage by economic cycle
# ─────────────────────────────────────────────────────────────

def _fig05(sweep_results, out_dir):
    """Box plots of SSM 10yr coverage by economic cycle."""
    apply_style()
    cycle_data, cycle_labels, cycle_cols = [], [], []
    for label, yr_from, yr_to, colour in CYCLE_BUCKETS:
        vals = [r['ssm_cov_10'] * 100
                for r in sweep_results
                if yr_from <= r['calendar_year'] <= yr_to
                and r.get('ssm_cov_10') is not None]
        if vals:
            cycle_data.append(vals)
            cycle_labels.append(label)
            cycle_cols.append(colour)

    fig, ax = plt.subplots(figsize=_FIG_BOX)
    bp = ax.boxplot(cycle_data, patch_artist=True, notch=False,
                    medianprops=dict(color='black', linewidth=2))
    for patch, colour in zip(bp['boxes'], cycle_cols):
        patch.set_facecolor(colour); patch.set_alpha(0.7)
    ax.axhline(100, color='black', linestyle='--', linewidth=1,
               alpha=0.5, label='100% expenditure coverage')
    ax.set_xticklabels(cycle_labels, fontsize=9)
    ax.set_ylabel('SSM 10yr coverage (%)', fontsize=11)
    ax.set_title(
        'SSM 10yr coverage distribution by economic cycle  |  '
        'All 73 start years — Balanced parameters\n'
        'SSM = correlated-shock floor; pairs with TCM ceiling (see Fig 07)  |  '
        '5-step post-fill priority mechanic (v8)',
        fontsize=9, pad=12)
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_05_coverage_by_cycle.png')


# ─────────────────────────────────────────────────────────────
# FIG 06 — Burden matrix heatmap
# ─────────────────────────────────────────────────────────────

def _fig06(p, py_tcm, out_dir):
    """Two-panel heatmap: annual wealth burden and effective rate on gains."""
    apply_style()
    diffs   = [t['differential'] for t in p['tiers']]
    tlabels = [f"{t['differential']:+.2%}\n({t['label']})" for t in p['tiers']]
    blabels = [b['label'] for b in p['brackets']]
    n_tiers = len(diffs)
    n_bkts  = len(blabels)

    burden_matrix  = np.zeros((n_tiers, n_bkts))
    effrate_matrix = np.zeros((n_tiers, n_bkts))
    for i, diff in enumerate(diffs):
        for j, r in enumerate(py_tcm[diff]):
            burden_matrix[i, j]  = r['wealth_burden'] * 100
            effrate_matrix[i, j] = r['eff_rate']      * 100

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=_FIG_BURDEN,
                                      gridspec_kw={'wspace': 0.35})
    for ax, matrix, title, cmap in [
        (ax_l, burden_matrix,  'Annual wealth burden\n(tax as % of net worth)',  'Blues'),
        (ax_r, effrate_matrix, 'Effective rate on gains\n(tax as % of annual gain)', 'Oranges'),
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
                ax.text(jj, ii, f'{val:.2f}%', ha='center', va='center',
                        fontsize=7,
                        color='white' if val > threshold else 'black')
        cb = fig.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
        cb.set_label('%', fontsize=8)

    fig.suptitle(
        f'Individual burden matrices — {p["scenario_start_year"]} '
        f'Balanced scenario, N={p["tcm_N"]}\n'
        'RATES.A §B.3.3 (left) and §B.3.4 (right)  |  '
        '0.00% = genuine zero liability (exemption threshold + refund offset); '
        'not missing data',
        fontsize=9, y=1.06)
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_06_burden_matrix_heatmap.png')


# ─────────────────────────────────────────────────────────────
# FIG 07 — SSM/TCM coverage range
# ─────────────────────────────────────────────────────────────

def _fig07(p, sweep_results, out_dir):
    """Per-start-year SSM floor / TCM ceiling band, coloured by economic cycle."""
    apply_style()
    active_year = p['scenario_start_year']
    fig, ax = plt.subplots(figsize=FIG_WIDE)

    for label, yr_from, yr_to, colour in CYCLE_BUCKETS:
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

    active = next((r for r in sweep_results if r['calendar_year'] == active_year), None)
    if active and active.get('ssm_cov_10') and active.get('tcm_cov_10'):
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
        'Circles = SSM floor (correlated-shock)  |  '
        'Triangles = TCM ceiling (persistent heterogeneity)',
        fontsize=9, pad=12)

    handles = [mpatches.Patch(color=c, label=l) for l, _, _, c in CYCLE_BUCKETS]
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
    return _save(fig, out_dir, 'rates_fig_07_ssm_tcm_coverage_range.png')


# ─────────────────────────────────────────────────────────────
# FIG 08 — Loss-year mechanics
# ─────────────────────────────────────────────────────────────

def _fig08(p, py_tcm, out_dir):
    """Symmetric refund in the worst return year, 95th pct bracket, Good tier."""
    apply_style()

    bracket_95_idx = next(
        (i for i, b in enumerate(p['brackets']) if b['label'] == '95%'),
        min(len(p['brackets']) - 1, 5))
    b95 = p['brackets'][bracket_95_idx]

    pos_tiers = [t for t in p['tiers'] if t['differential'] > 0]
    good_tier = min(pos_tiers, key=lambda t: t['differential']) if pos_tiers \
                else p['tiers'][-1]
    good_diff = good_tier['differential']

    N       = p['tcm_N']
    returns = p['returns']
    g_series = [returns[t] + good_diff for t in range(1, N + 1)]
    g_sell   = returns[N + 1] + good_diff
    sim      = simulate(b95['V0_m'], g_series, alpha=1.0, p=p)

    window_end       = min(10, N)
    window_years     = list(range(1, window_end + 1))
    cal_start        = p['scenario_start_year']
    sim_year_labels  = [str(cal_start + t - 1) for t in window_years]

    worst_t      = min(window_years, key=lambda t: returns[t])
    crash_x      = worst_t - 1
    crash_cal_yr = cal_start + worst_t - 1
    crash_pct    = returns[worst_t] * 100

    gross_tax    = [max(0.0, sim[t]['L']) * 1e6 for t in window_years]
    gross_refund = [min(0.0, sim[t]['L']) * 1e6 for t in window_years]
    cum_net      = []
    running = 0.0
    for t in window_years:
        running += sim[t]['L'] * 1e6
        cum_net.append(running)

    fig, ax1 = plt.subplots(figsize=_FIG_SWEEP)
    ax2 = ax1.twinx()
    ax2.spines['top'].set_visible(False)

    x = np.arange(len(window_years))
    ax1.axvspan(crash_x - 0.45, crash_x + 0.45, color='#fee8e8', zorder=1, alpha=0.9)
    ax1.bar(x, gross_tax,    width=0.55, color=C_SSM,      alpha=0.85,
            label='Gross tax paid (gain year)', zorder=3)
    ax1.bar(x, gross_refund, width=0.55, color=C_BASELINE, alpha=0.85,
            label='Symmetric refund received (loss year)', zorder=3)
    ax2.plot(x, cum_net, color=_C_DARK, linewidth=2, linestyle='-',
             marker='o', markersize=5, zorder=5,
             label='Cumulative net tax (right axis)')
    ax2.axhline(0, color=_C_DARK, linewidth=0.6, linestyle=':', alpha=0.5)

    if crash_pct < 0:
        ax1.annotate(
            f'Calendar {crash_cal_yr}\nReturn: {crash_pct:+.2f}%\nRefund fires at τ(W)',
            xy=(crash_x, gross_refund[crash_x]),
            xytext=(crash_x + 1.2,
                    gross_refund[crash_x] - abs(gross_refund[crash_x]) * -0.4),
            fontsize=8, color=_C_CRASH,
            arrowprops=dict(arrowstyle='->', color=_C_CRASH, lw=0.9))

    N_TICKS   = 6
    ax1_abs   = max(max(gross_tax), abs(min(gross_refund))) * 1.25
    ax1_lo, ax1_hi = -ax1_abs, ax1_abs
    ax2_abs   = max(abs(min(cum_net)), abs(max(cum_net))) * 1.25
    ax2_lo    = min(cum_net) * 1.25 if min(cum_net) < 0 else -ax2_abs * 0.1
    ax2_hi    = max(cum_net) * 1.25
    ax1.set_ylim(ax1_lo, ax1_hi)
    ax2.set_ylim(ax2_lo, ax2_hi)
    fracs = [i / (N_TICKS - 1) for i in range(N_TICKS)]
    ax1.set_yticks([ax1_lo + f * (ax1_hi - ax1_lo) for f in fracs])
    ax2.set_yticks([ax2_lo + f * (ax2_hi - ax2_lo) for f in fracs])
    for ax in (ax1, ax2):
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}'))

    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [f'{lbl}\n(yr {t})' for lbl, t in zip(sim_year_labels, window_years)],
        fontsize=8.5)
    ax1.set_xlabel('Calendar year  (simulation year)', fontsize=10)
    ax1.set_ylabel('Annual tax / refund (£ per taxpayer)', fontsize=10)
    ax2.set_ylabel('Cumulative net tax paid (£ per taxpayer)', fontsize=10)

    crash_note = (f'Red shading = {crash_cal_yr} crash year ({crash_pct:+.2f}%)'
                  if crash_pct < 0 else 'No negative return year in display window')
    fig.suptitle(
        f'Loss-year mechanics: symmetric refund in the worst return year\n'
        f'95th percentile bracket ($V_0$ = £{b95["V0_m"]:.3f}m), '
        f'{good_tier["label"]} tier ({good_diff * 100:+.2f}pp), '
        f'{cal_start} Balanced scenario — simulation years 1–{window_end}\n'
        f'{crash_note}  |  Refund is bounded by cumulative net tax paid '
        '(lifetime contribution envelope)',
        fontsize=9, y=1.01)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=8.5, loc='upper left')
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_08_loss_year_mechanics.png')


# ─────────────────────────────────────────────────────────────
# FIG 09 — Phase Two stress profile
# ─────────────────────────────────────────────────────────────

def _fig09(p, py_ssm, out_dir):
    """Two-panel: LRR balance vs target (top) + coverage fraction (bottom)."""
    apply_style()

    lrr_fill_yr = next((r['year'] for r in py_ssm if r.get('lrr_filled')), None)
    if lrr_fill_yr is None:
        print('  Fig 09 skipped: LRR did not fill within modelling window.')
        return None

    years    = [r['year']        for r in py_ssm]
    lrr_bal  = [r['lrr_balance'] for r in py_ssm]
    lrr_tgt  = [r['lrr_target']  for r in py_ssm]
    cov_frac = [r['cov_frac']    for r in py_ssm]

    post_years = [y for y in years if y > lrr_fill_yr]
    post_bal   = [lrr_bal[i] for i, y in enumerate(years) if y > lrr_fill_yr]
    post_tgt   = [lrr_tgt[i] for i, y in enumerate(years) if y > lrr_fill_yr]
    post_cov   = [cov_frac[i] for i, y in enumerate(years) if y > lrr_fill_yr]

    n_below_floor = sum(1 for b, t in zip(post_bal, post_tgt) if b < t)
    n_zero_cov    = sum(1 for c in post_cov if c == 0.0)
    min_bal       = min(post_bal) if post_bal else 0.0

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=_FIG_STACK, sharex=True,
        gridspec_kw={'height_ratios': [3, 1.4], 'hspace': 0.08})

    # ── top panel ────────────────────────────────────────────
    py_arr = np.array(post_years, dtype=float)
    pb_arr = np.array(post_bal,   dtype=float)
    pt_arr = np.array(post_tgt,   dtype=float)

    ax_top.fill_between(py_arr, pb_arr, pt_arr, where=(pb_arr < pt_arr),
                        interpolate=True, color=_C_ZONE_AMBER, alpha=0.45,
                        linewidth=0, label='Below floor (stressed, not failed)')
    ax_top.plot(years, lrr_tgt, color=C_ANNOTATION, linewidth=1.4, linestyle='--',
                alpha=0.8, label='LRR floor target (3× annual expenditure)')

    pre_y = [y for y in years if y <= lrr_fill_yr]
    pre_b = [lrr_bal[i] for i, y in enumerate(years) if y <= lrr_fill_yr]
    ax_top.plot(pre_y, pre_b, color=C_TCM, linewidth=2.2,
                label='LRR balance — capitalisation phase')

    post_all_y = [y for y in years if y >= lrr_fill_yr]
    post_all_b = [lrr_bal[i] for i, y in enumerate(years) if y >= lrr_fill_yr]
    ax_top.plot(post_all_y, post_all_b, color=C_BASELINE, linewidth=2.2,
                label='LRR balance — post-fill (zero-governance)')

    ax_top.axvline(lrr_fill_yr, color=_C_NEUTRAL, linestyle=':', linewidth=1.3, alpha=0.9)
    ax_top.text(lrr_fill_yr + 0.6, max(lrr_tgt) * 1.05,
                f'LRR fill\n(yr {lrr_fill_yr})', fontsize=8, color=_C_NEUTRAL, va='top')

    min_yr = post_years[post_bal.index(min_bal)]
    ax_top.annotate(
        f'Min balance\n£{min_bal:,.0f}b\n(yr {min_yr})',
        xy=(min_yr, min_bal),
        xytext=(min_yr + 3, min_bal + max(lrr_tgt) * 0.08),
        fontsize=7.5, color=_C_CRASH,
        arrowprops=dict(arrowstyle='->', color=_C_CRASH, lw=0.8))

    ax_top.set_ylabel('LRR balance (£b)', fontsize=10)
    ax_top.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))
    ax_top.legend(fontsize=8.5, loc='upper left')

    # ── bottom panel ─────────────────────────────────────────
    post_budget    = [r['budget']   for r in py_ssm if r['year'] > lrr_fill_yr]
    post_surplus_b = [c * b for c, b in zip(post_cov, post_budget)]

    ax_bot.bar(post_years, post_surplus_b, width=0.8,
               color=C_SSM, alpha=0.85, zorder=3)
    for y, c in zip(post_years, post_cov):
        if c == 0.0:
            ax_bot.axvspan(y - 0.4, y + 0.4, color=_C_ZONE_RED,
                           alpha=0.35, zorder=2, linewidth=0)
            ax_bot.scatter(y, 1.0, marker='v', color=_C_ZONE_RED,
                           s=40, zorder=5, clip_on=False)

    ax_bot.plot(post_years, post_budget, color='black', linewidth=0.9,
                linestyle='--', alpha=0.5,
                label='Annual expenditure (= 100% coverage)')
    ax_bot.axvline(lrr_fill_yr, color=_C_NEUTRAL, linestyle=':', linewidth=1.3, alpha=0.9)
    ax_bot.set_xlabel('Year from launch', fontsize=10)
    ax_bot.set_yscale('log')
    ax_bot.set_ylim(bottom=1.0)
    ax_bot.set_ylabel('Step-5 surplus\n(£b/yr)', fontsize=9)
    ax_bot.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f'£{v:,.0f}b'))

    blue_patch = mpatches.Patch(color=C_SSM, alpha=0.85,
                                label='Labour-relief surplus (£b)')
    red_patch  = mpatches.Patch(color=_C_ZONE_RED, alpha=0.35,
                                label=f'Zero coverage ({n_zero_cov} years')
    ax_bot.legend(
        handles=[blue_patch, red_patch,
                 plt.Line2D([0], [0], color='black', linestyle='--', alpha=0.5,
                            label='Annual expenditure (100% reference)')],
        fontsize=8, loc='upper left')

    scenario_yr = p['scenario_start_year']
    fig.suptitle(
        f'Phase Two stress profile — full 71-year window, {scenario_yr} Balanced scenario\n'
        f'Top: LRR balance vs 3× floor target  |  '
        f'Min balance £{min_bal:,.0f}b (never zero)\n'
        f'Red bars = {n_zero_cov} zero-coverage years  |  '
        f'Dashed line = annual expenditure; bars above it = coverage > 100%  |  ',
        fontsize=8.5, y=1.01)
    plt.tight_layout()
    return _save(fig, out_dir, 'rates_fig_09_phase_two_transition.png')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    toml_path  = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f'Loading parameters from: {toml_path or DEFAULT_PARAMS}')
    p = model.load_params(toml_path)
    model.validate_params(p)

    print('\nRunning SSM (active scenario, N=1..71)...')
    py_ssm = model.run_ssm(p, max_N=71)

    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)
    py_srr_fill = next((r for r in py_ssm
                        if r['srr_target'] > 0
                        and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
    ssm_lrr_N = py_lrr_fill['year'] if py_lrr_fill else p['tcm_N']
    ssm_srr_N = py_srr_fill['year'] if py_srr_fill else 1
    print(f"  LRR fill year: {ssm_lrr_N}")

    print(f'\nRunning TCM (N={ssm_lrr_N})...')
    py_tcm = model.run_tcm(p, N=ssm_lrr_N, N_fill=ssm_srr_N)

    print(f'\nRunning start-year sweep ({len(p["returns"])} calendar years)...')
    sweep = model.run_start_year_sweep(p)

    _out = ensure_dir(Path(output_dir) if output_dir else _OUT)
    generate_figures(p, py_ssm, py_tcm, sweep,
                     output_dir=_out, tcm_N=ssm_lrr_N)
    print('\nDone.')


if __name__ == '__main__':
    main()
