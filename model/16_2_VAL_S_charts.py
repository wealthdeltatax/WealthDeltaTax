import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

from wdt_core import load_params, tau
from wdt_fmt import out_dir, ensure_dir
from wdt_style import (apply_style, apply_style_nogrid, save_fig,
                        FIG_SINGLE, FIG_QUAD)
from wdt_analytics import init, draw_c1_heatmap
import wdt_analytics as _A

_OUT   = out_dir('SWEEPS_V')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'
V0_COLS = ['#2166ac', '#d73027', '#7b2d8b', '#4dac26']

def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)

def _save(fig, name):
    return save_fig(fig, _OUT / name)

def _v0_labels():
    return [f'V₀=£{v:.0f}m' + (' (canonical)' if v == _A.CANON_V0 else '')
            for v in _A.V0_VALS]


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


def _save(fig, name):
    return save_fig(fig, _OUT / name)


"""
VAL.S Output Script 1 — Rate Function Parameter Sweeps
========================================================
Generates figures for 2 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  2.1  τ₀ sweep   2.2  τ_m sweep   2.3  k sweep   2.4  W_min sweep
"""

# ── Shared heatmap 4-panel builder ────────────────────────────────────────────

def _heatmap_4panel(matrices, param_vals, canon_val, labels, suptitle, fname):
    """
    Render a 2×2 grid of C.1 heatmaps, one per parameter value.
    Uses draw_c1_heatmap() for each panel; adds a shared colourbar.
    """
    apply_style_nogrid()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD)
    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, mat_list, val, label in zip(axes.flat, matrices, param_vals, labels):
        mat = np.array(mat_list)
        bold = (val == canon_val)
        im = draw_c1_heatmap(ax, mat, title=label)
        ax.title.set_fontweight('bold' if bold else 'normal')

    cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cbar_ax)
    cbar_ax.set_ylabel('C.1 (pp)  +red = understater pays more  −blue = overstater pays less',
                        fontsize=8)
    fig.suptitle(suptitle, fontsize=10, y=1.01)
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    _save(fig, fname)


# ── 3.1  τ₀ sweep ────────────────────────────────────────────────────────────

def fig_3_1a_tau0_heatmaps(d):
    labels = [f'τ₀ = {v*100:.0f}%' + (' (canonical)' if v == _A.CANON_TAU0 else '')
              for v in _A.TAU0_VALS]
    _heatmap_4panel(
        d['val_s']['tau0_c1_matrices'], _A.TAU0_VALS, _A.CANON_TAU0, labels,
        suptitle=(
            'Figure 3.1a — C.1 advantage landscape across τ₀ values\n'
            f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, '
            f'V₀=£{_A.CANON_V0:.0f}m  ·  Bold panel = canonical'
        ),
        fname='SWEEPS_v_fig_3_1a_tau0_heatmaps.png',
    )


def fig_3_1b_tau0_n_crossings(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    tau0_fine = d['val_s']['tau0_fine']
    ls   = {1.5: '-', 1.8: '--', 2.0: '-.'}
    cols = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}
    for alpha in _A.OVER_ALPHAS:
        crossings = d['val_s']['tau0_n_crossings'][str(alpha)]
        ax.plot([t * 100 for t in tau0_fine], crossings,
                color=cols[alpha], linestyle=ls[alpha],
                linewidth=2, marker='o', markersize=5, label=f'α = {alpha}')
    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':',
               label=f'N = {_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_TAU0 * 100, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_TAU0 * 100 + 0.3, ax.get_ylim()[0] + 1,
            f'τ₀ = {_A.CANON_TAU0*100:.0f}% (canonical)', fontsize=7.5, color='#666666')
    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('N at which overstater first pays more than honest')
    ax.set_title(
        f'Figure 3.1b — N-crossing thresholds by τ₀\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(8, 33)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_3_1b_tau0_n_crossings.png')


def fig_3_1c_tau0_tolerant_zone(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    tau0_fine = d['val_s']['tau0_fine']
    pct       = [t * 100 for t in tau0_fine]
    tzone     = d['val_s']['tau0_tzone']
    los = [row[0] for row in tzone]
    his = [row[1] for row in tzone]
    ax.fill_between(pct, los, his, alpha=0.15, color='#4393c3',
                    label='Tolerant zone (|C.1| < 2pp)')
    ax.plot(pct, los, color='#2166ac', linewidth=1.5, label='α_low boundary')
    ax.plot(pct, his, color='#d73027', linewidth=1.5, label='α_high boundary')
    ax.axhline(1.0, color='#888888', linewidth=0.8, linestyle='--', label='Honest (α = 1.0)')
    ax.axvline(_A.CANON_TAU0 * 100, color='#888888', linewidth=0.9, linestyle=':',
               label=f'Canonical τ₀ = {_A.CANON_TAU0*100:.0f}%')
    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('Declaration ratio α')
    ax.set_title(
        f'Figure 3.1c — Tolerant zone (|C.1| < {_A.TZONE_THRESHOLD*100:.0f}pp) boundaries by τ₀\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(5, 44)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_3_1c_tau0_tolerant_zone.png')


# ── 2.2  τ_m sweep ───────────────────────────────────────────────────────────

def fig_4_1a_taum_heatmaps(d):
    labels = [f'τ_m = {v*100:.0f}%' + (' (canonical)' if v == _A.CANON_TAUM else '')
              for v in _A.TAUM_VALS]
    _heatmap_4panel(
        d['val_s']['taum_c1_matrices'], _A.TAUM_VALS, _A.CANON_TAUM, labels,
        suptitle=(
            'Figure 3.1a — C.1 advantage landscape across τ_m values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, '
            f'V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='SWEEPS_v_fig_4_1a_taum_heatmaps.png',
    )


def fig_4_1b_taum_penalty_plateaus(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    under_alphas = [0.1, 0.2, 0.5, 0.8]
    cols = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    ls_by_taum = {0.50: ':', 0.60: '--', 0.70: '-', 0.80: '-.'}
    plateaus_data = d['val_s']['taum_penalty_plateaus']
    for tau_m, ls in ls_by_taum.items():
        plateaus = [plateaus_data[f'{tau_m:.2f}'][f'{alpha:.1f}']
                    for alpha in under_alphas]
        ax.plot([a * 100 for a in under_alphas], plateaus,
                linestyle=ls, linewidth=2, marker='o', markersize=5,
                label=f'τ_m = {tau_m*100:.0f}%' + (' (canonical)' if tau_m == _A.CANON_TAUM else ''))
    ax.set_xlabel('Declaration ratio α (understatement region)')
    ax.set_ylabel('Plateau ceiling of C.1 (pp)')
    ax.set_title(
        f'Figure 4.1b — Understater penalty plateau ceiling by α and τ_m\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, g sweep 18–40%'
    )
    ax.legend(); ax.set_xlim(5, 85)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_4_1b_taum_penalty_plateaus.png')


def fig_4_1c_taum_n_crossings(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    taum_fine = d['val_s']['taum_fine']
    ls   = {1.5: '-', 1.8: '--', 2.0: '-.'}
    cols = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}
    for alpha in _A.OVER_ALPHAS:
        crossings = d['val_s']['taum_n_crossings'][str(alpha)]
        ax.plot([t * 100 for t in taum_fine], crossings,
                color=cols[alpha], linestyle=ls[alpha],
                linewidth=2, marker='o', markersize=5, label=f'α = {alpha}')
    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':',
               label=f'N = {_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_TAUM * 100, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_TAUM * 100 + 0.5, ax.get_ylim()[0] + 1,
            f'τ_m = {_A.CANON_TAUM*100:.0f}% (canonical)', fontsize=7.5, color='#666666')
    ax.set_xlabel('Ceiling rate τ_m (%)')
    ax.set_ylabel('N at crossing (overstater first pays more than honest)')
    ax.set_title(
        f'Figure 4.1c — N-crossing thresholds by τ_m\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_4_1c_taum_n_crossings.png')


# ── 2.3  k sweep ─────────────────────────────────────────────────────────────

def fig_5_k_rate_curves(p):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    W_vals = np.logspace(np.log10(_A.CANON_WMIN), np.log10(5000), 400)
    k_labels = [f'k = {v}' + (' (canonical)' if v == _A.CANON_K else '') for v in _A.K_VALS]
    k_cols   = ['#2166ac', '#4dac26', '#d73027', '#7b2d8b']
    # Only show the first four K_VALS for clarity (matching original)
    for k_val, label, col in zip(_A.K_VALS[:4], k_labels[:4], k_cols):
        tau_vals = [tau(w, {'tau_0': _A.CANON_TAU0, 'tau_m': _A.CANON_TAUM,
                             'k': k_val, 'W_min': _A.CANON_WMIN}) * 100
                    for w in W_vals]
        lw = 2.2 if k_val == _A.CANON_K else 1.6
        ax.semilogx(W_vals, tau_vals, linewidth=lw, label=label,
                    linestyle='-' if k_val == _A.CANON_K else '--', color=col)
    ax.axvline(_A.CANON_V0, color='#888888', linewidth=1.0, linestyle=':',
               label=f'V₀=£{_A.CANON_V0:.0f}m')
    ax.axhline(_A.CANON_TAU0 * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.axhline(_A.CANON_TAUM * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Figure 5a — Rate curve τ(W) across k values\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, W_min=£{_A.CANON_WMIN:.0f}m'
    )
    ax.set_xlim(_A.CANON_WMIN, 5000)
    ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.12)
    ax.legend(loc='upper left')
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                        '£200m', '£500m', '£1bn', '£2bn', '£5bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_5_k_rate_curves.png')


def fig_5_1a_k_heatmaps(d):
    labels = [f'k = {v}' + (' (canonical)' if v == _A.CANON_K else '')
              for v in _A.K_VALS]
    _heatmap_4panel(
        d['val_s']['k_c1_matrices'][:4], _A.K_VALS[:4], _A.CANON_K, labels[:4],
        suptitle=(
            'Figure 5.1a — C.1 advantage landscape across k values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
            f'N={_A.CANON_N}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='SWEEPS_v_fig_5_1a_k_heatmaps.png',
    )


def fig_5_1c_k_bracket_penalty(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    k_fine     = d['val_s']['k_fine']
    v0_points  = [20.0, 100.0, 500.0]
    cols       = ['#2166ac', '#d73027', '#7b2d8b']
    for v0, col in zip(v0_points, cols):
        c1_vals = d['val_s']['k_bracket_penalty'][f'{v0:.0f}']
        ax.plot(k_fine, c1_vals, color=col, linewidth=2, label=f'V₀=£{v0:.0f}m')
    ax.axhline(0, color='#888888', linewidth=0.8, linestyle='--', label='Honest baseline')
    ax.axvline(_A.CANON_K, color='#888888', linewidth=0.9, linestyle=':',
               label=f'Canonical k={_A.CANON_K}')
    ax.set_xlabel('k (steepness parameter)')
    ax.set_ylabel('C.1 at α=1.8 (pp)  — negative = overstater advantage')
    ax.set_title(
        f'Figure 5.1c — Bracket penalty for α=1.8 by k and V₀\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, N={_A.CANON_N}, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_5_1c_k_bracket_penalty.png')


# ── 2.4  W_min sweep ─────────────────────────────────────────────────────────

def fig_6_wmin_rate_curves(p):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    W_vals    = np.logspace(np.log10(0.5), np.log10(5000), 600)
    wmin_cols = ['#2166ac', '#d73027', '#7b2d8b', '#4dac26']
    for w_min, col in zip(_A.WMIN_VALS[:4], wmin_cols):
        label = f'W_min=£{w_min:.0f}m' + (' (canonical)' if w_min == _A.CANON_WMIN else '')
        tau_vals = [tau(w, {'tau_0': _A.CANON_TAU0, 'tau_m': _A.CANON_TAUM,
                             'k': _A.CANON_K, 'W_min': w_min}) * 100
                    for w in W_vals]
        lw = 2.2 if w_min == _A.CANON_WMIN else 1.6
        ax.semilogx(W_vals, tau_vals, color=col, linewidth=lw, label=label,
                    linestyle='-' if w_min == _A.CANON_WMIN else '--')
        ax.axvline(w_min, color=col, linewidth=0.8, linestyle=':', alpha=0.5)
    ax.axvline(_A.CANON_V0, color='#888888', linewidth=1.0, linestyle=':',
               label=f'V₀=£{_A.CANON_V0:.0f}m')
    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Figure 6 — Rate curve τ(W) across W_min values\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}'
    )
    ax.set_xlim(0.5, 5000); ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.12)
    ax.legend(loc='upper left')
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    ax.set_xticklabels(['£1m', '£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                        '£200m', '£500m', '£1bn', '£2bn', '£5bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_6_wmin_rate_curves.png')


def fig_6_1a_wmin_heatmaps(d):
    labels = [f'W_min=£{v:.0f}m' + (' (canonical)' if v == _A.CANON_WMIN else '')
              for v in _A.WMIN_VALS]
    _heatmap_4panel(
        d['val_s']['wmin_c1_matrices'][:4], _A.WMIN_VALS[:4], _A.CANON_WMIN, labels[:4],
        suptitle=(
            'Figure 6.1a — C.1 advantage landscape across W_min values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
            f'N={_A.CANON_N}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='SWEEPS_v_fig_6_1a_wmin_heatmaps.png',
    )


def fig_6_1b_wmin_n_crossings(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    wmin_fine = d['val_s']['wmin_fine']
    ls   = {1.5: '-', 1.8: '--', 2.0: '-.'}
    cols = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}
    for alpha in _A.OVER_ALPHAS:
        crossings = d['val_s']['wmin_n_crossings'][str(alpha)]
        ax.plot(wmin_fine, crossings, color=cols[alpha], linestyle=ls[alpha],
                linewidth=2, marker='o', markersize=4, label=f'α = {alpha}')
    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':',
               label=f'N={_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_WMIN, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_WMIN + 0.15, ax.get_ylim()[0] + 1,
            f'W_min=£{_A.CANON_WMIN:.0f}m (canonical)', fontsize=7.5, color='#666666')
    ax.axvline(_A.CANON_V0, color='#cccccc', linewidth=0.8, linestyle='--',
               label=f'V₀=£{_A.CANON_V0:.0f}m')
    ax.set_xlabel('Entry threshold W_min (£m)')
    ax.set_ylabel('N at which overstater first pays more than honest')
    ax.set_title(
        f'Figure 6.1b — N-crossing thresholds by W_min\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
        f'V₀=£{_A.CANON_V0:.0f}m, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(0.5, 11)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_6_1b_wmin_n_crossings.png')


# ── Main ──────────────────────────────────────────────────────────────────────
"""
VAL.S Output Script 2 — Horizon and Wealth-Level Sweeps
=========================================================
Generates figures for 3 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  3.1  N sweep (holding period)
  3.2  V₀ sweep (entry wealth level)
"""

# ── 3.1  N sweep ─────────────────────────────────────────────────────────────

def fig_2_2a_n_crossing_annotated(d):
    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    N_sweep = d['val_s']['n_sweep']
    cols    = ['#4393c3', '#2166ac', '#053061']
    ls      = ['-', '--', '-.']

    # Left: net tax difference trajectory
    for alpha, col, style in zip(_A.OVER_ALPHAS, cols, ls):
        diffs = d['val_s']['n_diffs'][str(alpha)]
        ax1.plot(N_sweep, diffs, color=col, linestyle=style, linewidth=2, label=f'α={alpha}')
    ax1.axhline(0, color='#333333', linewidth=1.2, label='Honest (zero line)')
    ax1.axvline(_A.CANON_N, color='#888888', linewidth=1.0, linestyle=':',
                label=f'N={_A.CANON_N} (RATES ref)')
    ax1.set_xlabel('Holding period N (years)')
    ax1.set_ylabel('Net(α) − Net(honest)  [£m]\n− = overstater pays less')
    ax1.set_ylim(-5, 20)
    ax1.set_title(f'Overstater net-tax advantage by N\ng={_A.CANON_G*100:.1f}% (canonical)')
    ax1.legend(fontsize=8); ax1.set_xlim(5, 35)

    # Right: bar chart of crossing N
    crossing_ns = [d['val_s']['n_crossing_vals'][str(a)] for a in _A.OVER_ALPHAS]
    bars = ax2.bar(range(len(_A.OVER_ALPHAS)),
                   [cn if cn is not None else 0 for cn in crossing_ns],
                   color=cols, edgecolor='white', width=0.5)
    ax2.axhline(_A.CANON_N, color='#888888', linewidth=1.5, linestyle='--',
                label=f'N={_A.CANON_N} (RATES ref)')
    for bar, alpha, nc in zip(bars, _A.OVER_ALPHAS, crossing_ns):
        if nc is not None:
            ax2.text(bar.get_x() + bar.get_width() / 2, nc + 0.8,
                     f'N≈{nc:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax2.text(bar.get_x() + bar.get_width() / 2, 3, 'no\ncrossing',
                     ha='center', va='bottom', fontsize=8, color='#666666')
    ax2.set_xticks(range(len(_A.OVER_ALPHAS)))
    ax2.set_xticklabels([f'α={a}' for a in _A.OVER_ALPHAS])
    ax2.set_ylabel('N at first crossing')
    ax2.set_title(f'N-crossing thresholds\ng={_A.CANON_G*100:.1f}%')
    ax2.legend(); ax2.set_ylim(0, 70)

    fig.suptitle(
        f'Figure 2.2a — Overstater advantage erosion and N-crossing thresholds\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
        f'V₀=£{_A.CANON_V0:.0f}m',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_2_2a_n_crossing_annotated.png')


def fig_2_3_n_understater_panels(d):
    apply_style()
    under_cols = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    g_fine     = d['val_s']['g_fine']
    labels     = [f'N={n}' + (' (canonical)' if n == _A.CANON_N else '')
                  for n in _A.N_PANEL_VALS]
    fig, axes  = plt.subplots(2, 2, figsize=FIG_QUAD)
 
    # Compute shared y-axis limits across all panels for direct comparison
    all_vals = []
    for n in _A.N_PANEL_VALS:
        c1_data = d['val_s']['n_understater_c1'][str(n)]
        for alpha in _A.UNDER_ALPHAS:
            all_vals.extend(c1_data[str(alpha)])
    y_lo = min(all_vals)
    y_hi = max(all_vals)
    y_pad = (y_hi - y_lo) * 0.08
    shared_ylim = (y_lo - y_pad, y_hi + y_pad)
 
    for ax, n, label in zip(axes.flat, _A.N_PANEL_VALS, labels):
        c1_data = d['val_s']['n_understater_c1'][str(n)]
        for alpha, col in zip(_A.UNDER_ALPHAS, under_cols):
            ax.plot([gv * 100 for gv in g_fine], c1_data[str(alpha)],
                    color=col, linewidth=1.8, label=f'α={alpha}')
        ax.axhline(0, color='#1a1a1a', linewidth=0.8, linestyle=':')
        ax.axvline(_A.CANON_G * 100, color='#888888', linewidth=0.8, linestyle='--')
        ax.text(_A.CANON_G * 100 + 0.2, shared_ylim[0] + y_pad * 2,
                f'g={_A.CANON_G*100:.1f}%', fontsize=7.5, color='#666666')
        ax.set_xlabel('g (%)')
        ax.set_ylabel('C.1 (pp)')
        ax.set_title(label, fontsize=10,
                     fontweight='bold' if n == _A.CANON_N else 'normal')
        ax.set_xlim(0, 35); ax.set_ylim(*shared_ylim); ax.legend(fontsize=7.5)
 
    fig.suptitle(
        'Figure 2.3 — Understater penalty profile across holding periods\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_2_3_n_understater_panels.png')


def fig_2_2b_n_tolerant_zone(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    n_fine = d['val_s']['n_fine']
    tzone  = d['val_s']['n_tzone']
    los = [row[0] for row in tzone]
    his = [row[1] for row in tzone]
    ax.fill_between(n_fine, los, his, alpha=0.20, color='#4393c3',
                    label='Tolerant zone (|C.1| < 2pp)')
    ax.plot(n_fine, los, color='#2166ac', linewidth=1.5, label='α_low boundary')
    ax.plot(n_fine, his, color='#d73027', linewidth=1.5, label='α_high boundary')
    ax.axhline(0.8, color='#888888', linewidth=0.8, linestyle=':',
               label='α=0.8 (VAL.A lower)')
    ax.axhline(1.5, color='#888888', linewidth=0.8, linestyle='--',
               label='α=1.5 (VAL.A upper)')
    ax.axhline(1.0, color='#555555', linewidth=0.8, label='Honest (α=1.0)')
    ax.axvline(_A.CANON_N, color='#aaaaaa', linewidth=1.0, linestyle=':',
               label=f'N={_A.CANON_N} (RATES ref)')
    ax.set_xlabel('Holding period N (years)')
    ax.set_ylabel('Declaration ratio α')
    ax.set_title(
        f'Figure 2.2b — Tolerant zone stability across N\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=7.5); ax.set_xlim(5, 65); ax.set_ylim(0.1, 4.5)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_2_2b_n_tolerant_zone.png')


# ── 3.2  V₀ sweep ────────────────────────────────────────────────────────────

def fig_11b_v0_c1_curves(d):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    alpha_fine = d['val_s']['alpha_fine']
    ls_map     = {5.0: ':', 20.0: '-', 100.0: '--', 500.0: '-.'}
    for v0, label, col in zip(_A.V0_VALS[:4], _v0_labels()[:4], V0_COLS):
        c1_vals = d['val_s']['v0_c1_curves'][f'{v0:.0f}']
        lw = 2.2 if v0 == _A.CANON_V0 else 1.6
        ax.plot([a * 100 for a in alpha_fine], c1_vals,
                color=col, linewidth=lw, linestyle=ls_map.get(v0, '-'), label=label)
    ax.axhline(0, color='#888888', linewidth=0.9, linestyle='--', label='Honest baseline')
    ax.axvline(100, color='#888888', linewidth=0.8, linestyle=':', label='α=1.0 (honest)')
    ax.axvspan(10, 100, alpha=0.03, color='#d73027')
    ax.axvspan(100, 200, alpha=0.03, color='#4393c3')
    ax.set_xlabel('Declaration ratio α (%)  — 100% = honest')
    ax.set_ylabel('C.1 (pp)  +positive = pays more than honest')
    ax.set_title(
        f'Figure 11b — C.1 incentive structure by V₀ entry wealth\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=8); ax.set_xlim(10, 200); ax.set_ylim(-25, 30)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_11b_v0_c1_curves.png')


def fig_11a_v0_entry_rate(p):
    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)
    W_range = np.logspace(np.log10(_A.CANON_WMIN), np.log10(2000), 500)
    sim_p = {'tau_0': _A.CANON_TAU0, 'tau_m': _A.CANON_TAUM,
             'k': _A.CANON_K, 'W_min': _A.CANON_WMIN}
    tau_vals = [tau(w, sim_p) * 100 for w in W_range]
    ax.semilogx(W_range, tau_vals, color='#1a1a1a', linewidth=2, label='τ(W)')
    ax.axhline(_A.CANON_TAU0 * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.axhline(_A.CANON_TAUM * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    for v0, label, col in zip(_A.V0_VALS[:4], _v0_labels()[:4], V0_COLS):
        rate = tau(v0, sim_p) * 100
        ax.plot(v0, rate, 'o', color=col, markersize=9, zorder=5)
        ax.annotate(f'{label}\nτ={rate:.1f}%', xy=(v0, rate),
                    xytext=(v0 * 1.6, rate + 3 if rate < 50 else rate - 5),
                    fontsize=7.5, color=col,
                    arrowprops=dict(arrowstyle='->', color=col, lw=0.8))
    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Figure 11a — Entry rate τ(V₀) at four wealth levels\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, W_min=£{_A.CANON_WMIN:.0f}m'
    )
    ax.set_xlim(_A.CANON_WMIN, 2000); ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.15)
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m',
                        '£100m', '£200m', '£500m', '£1bn', '£2bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_11a_v0_entry_rate.png')


def fig_11c_v0_heatmaps(d):
    _heatmap_4panel_nogrid(
        d['val_s']['v0_c1_matrices'][:4], _A.V0_VALS[:4], _A.CANON_V0,
        _v0_labels()[:4],
        suptitle=(
            'Figure 11c — C.1 advantage landscape across V₀ wealth levels\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
            f'k={_A.CANON_K}, N={_A.CANON_N}  ·  Bold = canonical'
        ),
        fname='SWEEPS_v_fig_11c_v0_heatmaps.png',
    )


def _heatmap_4panel_nogrid(matrices, param_vals, canon_val, labels, suptitle, fname):
    """Shared 2×2 heatmap grid (nogrid style) for V₀ panels."""
    apply_style_nogrid()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD)
    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    for ax, mat_list, val, label in zip(axes.flat, matrices, param_vals, labels):
        mat  = np.array(mat_list)
        bold = (val == canon_val)
        draw_c1_heatmap(ax, mat, title=label)
        ax.title.set_fontweight('bold' if bold else 'normal')
    cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
    fig.colorbar(plt.cm.ScalarMappable(
        norm=norm, cmap='RdBu_r'), cax=cbar_ax)
    cbar_ax.set_ylabel('C.1 (pp)', fontsize=8)
    fig.suptitle(suptitle, fontsize=10, y=1.01)
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save_fig(fig, _OUT / fname)

"""
VAL.S Output Script 3 — Parameter Interaction Surfaces
========================================================
Generates figures for 4 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  4.1  τ₀ × N joint surface — N-crossing threshold for α=2.0
  4.2  k × V₀ joint surface — bracket penalty for α=1.8
  4.3  Governing Council calibration summary
"""

# ── 4.1  τ₀ × N surface ─────────────────────────────────────────────────────

def fig_3_1d_tau0_n_surface(d):
    apply_style_nogrid()
    tau0_grid   = d['val_s']['tau0_n_surface_tau0_grid']
    n_ceil_grid = d['val_s']['tau0_n_surface_nceil_grid']
    # Restore nan from None
    surface = np.array(
        [[v if v is not None else np.nan for v in row]
         for row in d['val_s']['tau0_n_surface']],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(11, 7))
    cmap = plt.cm.RdYlGn_r.copy()
    cmap.set_bad(color='#cccccc')
    masked = np.ma.masked_invalid(surface)
    ax.imshow(masked, aspect='auto', cmap=cmap, vmin=5, vmax=65,
              extent=[tau0_grid[0] * 100 - 1.5, tau0_grid[-1] * 100 + 1.5,
                      n_ceil_grid[-1] + 2.5,     n_ceil_grid[0] - 2.5])

    for i, n_ceil in enumerate(n_ceil_grid):
        for j, tau_0 in enumerate(tau0_grid):
            val = surface[i, j]
            if not np.isnan(val):
                ax.text(tau_0 * 100, n_ceil, f'{val:.0f}',
                        ha='center', va='center', fontsize=7,
                        color='white' if val < 25 or val > 55 else '#1a1a1a')
            else:
                ax.text(tau_0 * 100, n_ceil, '—', ha='center', va='center',
                        fontsize=7, color='#888888')

    ax.axvline(_A.CANON_TAU0 * 100, color='#1a1a1a', linewidth=1.5, linestyle='--',
               label=f'Canonical τ₀={_A.CANON_TAU0*100:.0f}%')
    ax.axhline(_A.CANON_N, color='#1a1a1a', linewidth=1.5, linestyle=':',
               label=f'RATES N={_A.CANON_N}')

    norm = mcolors.Normalize(vmin=5, vmax=65)
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax,
                 fraction=0.04, pad=0.02).set_label(
        'N-crossing threshold for α=2.0  (grey = no crossing)', fontsize=8)

    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('Maximum holding period (N sweep ceiling, years)')
    ax.set_title(
        'Figure 3.1d — Joint surface: N-crossing for α=2.0 across (τ₀, N)\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%\n'
        'Green = early crossing  ·  Red = late  ·  Grey = never',
        fontsize=9
    )
    ax.legend(fontsize=8)
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_3_1d_tau0_n_surface.png')


# ── 4.2  k × V₀ surface ─────────────────────────────────────────────────────

def fig_5_1b_k_v0_surface(d):
    apply_style_nogrid()
    k_grid  = d['val_s']['k_v0_surface_k_grid']
    v0_grid = d['val_s']['k_v0_surface_v0_grid']
    surface = np.array(d['val_s']['k_v0_surface'])

    fig, ax = plt.subplots(figsize=(10, 7))
    vbound = max(abs(surface.min()), abs(surface.max()))
    norm   = mcolors.TwoSlopeNorm(vmin=-vbound, vcenter=0, vmax=vbound)
    im     = ax.imshow(surface, aspect='auto', cmap='RdBu_r', norm=norm)

    for i in range(len(k_grid)):
        for j in range(len(v0_grid)):
            v   = surface[i, j]
            col = 'white' if abs(v) > vbound * 0.5 else '#1a1a1a'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=8, color=col)

    ax.set_xticks(range(len(v0_grid)))
    ax.set_xticklabels([f'£{v:.0f}m' for v in v0_grid])
    ax.set_yticks(range(len(k_grid)))
    ax.set_yticklabels([str(k) for k in k_grid])
    ax.set_xlabel('Entry wealth V₀ (£m)')
    ax.set_ylabel('Steepness parameter k')

    # Canonical cell border
    can_k  = k_grid.index(_A.CANON_K)  if _A.CANON_K  in k_grid  else None
    can_v0 = v0_grid.index(_A.CANON_V0) if _A.CANON_V0 in v0_grid else None
    if can_k is not None and can_v0 is not None:
        ax.add_patch(plt.Rectangle((can_v0 - 0.5, can_k - 0.5), 1, 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=2.5,
                                   label='Canonical cell'))
    ax.legend(fontsize=8, loc='upper left')
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).set_label(
        'C.1 (pp) at α=1.8  — negative = overstater pays less', fontsize=8)
    ax.set_title(
        'Figure 5.1b — Joint surface: bracket penalty (C.1) for α=1.8 across (k, V₀)\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%\n'
        'Red = overstater pays more  ·  Blue = overstater pays less  ·  Bold = canonical',
        fontsize=9
    )
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_5_1b_k_v0_surface.png')


# ── 4.3  Calibration summary ─────────────────────────────────────────────────

def fig_7_1_calibration_summary(d):
    apply_style()
    cal      = d['val_s']['calibration']
    labels   = list(cal.keys())
    tzone_w  = [cal[lbl]['tzone_width'] for lbl in labels]
    cross_ns = [cal[lbl]['n_crossing_1_8'] or 70.0 for lbl in labels]
    plateaus = [cal[lbl]['plateau_0_1'] for lbl in labels]

    group_cols   = ['#2166ac'] * 4 + ['#d73027'] * 4 + ['#7b2d8b'] * 4 + ['#1a7a2a'] * 4
    canon_flags  = [False, False, True, False,
                    False, False, True, False,
                    False, False, True, False,
                    False, True, False, False]
    x = range(len(labels))

    def _add_canon_borders(ax, heights):
        for xi, flag, ht in zip(x, canon_flags, heights):
            if flag:
                ax.add_patch(plt.Rectangle((xi - 0.35, 0), 0.7, ht + 0.5,
                                           fill=False, edgecolor='black', linewidth=2))

    fig, axes = plt.subplots(3, 1, figsize=(16, 12))

    axes[0].bar(x, [w * 100 for w in tzone_w], color=group_cols, edgecolor='white', width=0.7)
    _add_canon_borders(axes[0], [w * 100 for w in tzone_w])
    axes[0].set_ylabel('Tolerant-zone width (% of α range where |C.1| < 2pp)')
    axes[0].set_title('Tolerant-zone width', fontsize=9)
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels, fontsize=7.0)

    axes[1].bar(x, cross_ns, color=group_cols, edgecolor='white', width=0.7)
    axes[1].axhline(_A.CANON_N, color='#888888', linewidth=1.0, linestyle='--',
                    label=f'RATES N={_A.CANON_N}')
    _add_canon_borders(axes[1], cross_ns)
    axes[1].set_ylabel('N-crossing for α=1.8 (years)')
    axes[1].set_title('N-crossing threshold for aggressive overstatement (α=1.8)', fontsize=9)
    axes[1].set_xticks(x); axes[1].set_xticklabels(labels, fontsize=7.0)
    axes[1].legend(fontsize=7.5); axes[1].set_ylim(0, 80)

    axes[2].bar(x, plateaus, color=group_cols, edgecolor='white', width=0.7)
    _add_canon_borders(axes[2], plateaus)
    axes[2].set_ylabel('Understater plateau ceiling (pp) at α=0.1, g>17%')
    axes[2].set_title('Understater penalty plateau ceiling (α=0.1)', fontsize=9)
    axes[2].set_xticks(x); axes[2].set_xticklabels(labels, fontsize=7.0)

    legend_elements = [
        Patch(facecolor='#2166ac', label='τ₀ variants'),
        Patch(facecolor='#d73027', label='τ_m variants'),
        Patch(facecolor='#7b2d8b', label='k variants'),
        Patch(facecolor='#1a7a2a', label='W_min variants'),
    ]
    axes[0].legend(handles=legend_elements, loc='upper right', fontsize=7.5)

    fig.suptitle(
        'Figure 7.1 — Governing Council calibration summary\n'
        'How each rate-function parameter moves the three key mechanism boundaries\n'
        f'Bold borders = canonical  ·  N={_A.CANON_N}, V₀=£{int(_A.CANON_V0)}m, '
        f'g={_A.CANON_G*100:.1f}%',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'SWEEPS_v_fig_7_1_calibration_summary.png')


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    p = load_params()
    init(p)
    ensure_dir(_OUT)
    d = _load()

    print('\n3.1  N sweep...')
    fig_2_2a_n_crossing_annotated(d)
    fig_2_3_n_understater_panels(d)
    fig_2_2b_n_tolerant_zone(d)

    print('\n3.2  V₀ sweep...')
    fig_11b_v0_c1_curves(d)
    fig_11a_v0_entry_rate(p)
    fig_11c_v0_heatmaps(d)

    print('\n4.1  τ₀ × N surface...')
    fig_3_1d_tau0_n_surface(d)

    print('\n4.2  k × V₀ surface...')
    fig_5_1b_k_v0_surface(d)

    print('\n4.3  Calibration summary...')
    fig_7_1_calibration_summary(d)

    print('\n2.1  τ₀ sweep...')
    fig_3_1a_tau0_heatmaps(d)
    fig_3_1b_tau0_n_crossings(d)
    fig_3_1c_tau0_tolerant_zone(d)

    print('\n2.2  τ_m sweep...')
    fig_4_1a_taum_heatmaps(d)
    fig_4_1b_taum_penalty_plateaus(d)
    fig_4_1c_taum_n_crossings(d)

    print('\n2.3  k sweep...')
    fig_5_k_rate_curves(p)
    fig_5_1a_k_heatmaps(d)
    fig_5_1c_k_bracket_penalty(d)

    print('\n2.4  W_min sweep...')
    fig_6_wmin_rate_curves(p)
    fig_6_1a_wmin_heatmaps(d)
    fig_6_1b_wmin_n_crossings(d)

if __name__ == '__main__':
    main()