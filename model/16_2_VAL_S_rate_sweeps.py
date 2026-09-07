"""
VAL.S Output Script 1 — Rate Function Parameter Sweeps
========================================================
Generates figures for §2 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  §2.1  τ₀ sweep   §2.2  τ_m sweep   §2.3  k sweep   §2.4  W_min sweep
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from wdt_core import load_params, tau
from wdt_fmt import out_dir, ensure_dir
from wdt_style import (apply_style, apply_style_nogrid, save_fig,
                        FIG_SINGLE, FIG_QUAD, C_UNDER)
from wdt_analytics import init, draw_c1_heatmap
import wdt_analytics as _A

_OUT   = out_dir('VAL_S')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


def _save(fig, name):
    return save_fig(fig, _OUT / name)


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


# ── §2.1  τ₀ sweep ────────────────────────────────────────────────────────────

def fig_tau0_heatmaps(d):
    labels = [f'τ₀ = {v*100:.0f}%' + (' (canonical)' if v == _A.CANON_TAU0 else '')
              for v in _A.TAU0_VALS]
    _heatmap_4panel(
        d['val_s']['tau0_c1_matrices'], _A.TAU0_VALS, _A.CANON_TAU0, labels,
        suptitle=(
            'Fig S2.1a — C.1 advantage landscape across τ₀ values\n'
            f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, '
            f'V₀=£{_A.CANON_V0:.0f}m  ·  Bold panel = canonical'
        ),
        fname='val_s_fig_s2_1a_tau0_heatmaps.png',
    )


def fig_tau0_n_crossings(d):
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
        f'Fig S2.1b — N-crossing thresholds by τ₀\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(8, 33)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_1b_tau0_n_crossings.png')


def fig_tau0_tolerant_zone(d):
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
        f'Fig S2.1c — Tolerant zone (|C.1| < {_A.TZONE_THRESHOLD*100:.0f}pp) boundaries by τ₀\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(5, 44)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_1c_tau0_tolerant_zone.png')


# ── §2.2  τ_m sweep ───────────────────────────────────────────────────────────

def fig_taum_heatmaps(d):
    labels = [f'τ_m = {v*100:.0f}%' + (' (canonical)' if v == _A.CANON_TAUM else '')
              for v in _A.TAUM_VALS]
    _heatmap_4panel(
        d['val_s']['taum_c1_matrices'], _A.TAUM_VALS, _A.CANON_TAUM, labels,
        suptitle=(
            'Fig S2.2a — C.1 advantage landscape across τ_m values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, '
            f'V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='val_s_fig_s2_2a_taum_heatmaps.png',
    )


def fig_taum_penalty_plateaus(d):
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
        f'Fig S2.2b — Understater penalty plateau ceiling by α and τ_m\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, g sweep 18–40%'
    )
    ax.legend(); ax.set_xlim(5, 85)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_2b_taum_penalty_plateaus.png')


def fig_taum_n_crossings(d):
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
        f'Fig S2.2c — N-crossing thresholds by τ_m\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_2c_taum_n_crossings.png')


# ── §2.3  k sweep ─────────────────────────────────────────────────────────────

def fig_k_rate_curves(p):
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
        f'Fig S2.3a — Rate curve τ(W) across k values\n'
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
    _save(fig, 'val_s_fig_s2_3a_k_rate_curves.png')


def fig_k_heatmaps(d):
    labels = [f'k = {v}' + (' (canonical)' if v == _A.CANON_K else '')
              for v in _A.K_VALS]
    _heatmap_4panel(
        d['val_s']['k_c1_matrices'][:4], _A.K_VALS[:4], _A.CANON_K, labels[:4],
        suptitle=(
            'Fig S2.3b — C.1 advantage landscape across k values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
            f'N={_A.CANON_N}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='val_s_fig_s2_3b_k_heatmaps.png',
    )


def fig_k_bracket_penalty(d):
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
        f'Fig S2.3c — Bracket penalty for α=1.8 by k and V₀\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, N={_A.CANON_N}, '
        f'g={_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_3c_k_bracket_penalty.png')


# ── §2.4  W_min sweep ─────────────────────────────────────────────────────────

def fig_wmin_rate_curves(p):
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
        f'Fig S2.4a — Rate curve τ(W) across W_min values\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}'
    )
    ax.set_xlim(0.5, 5000); ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.12)
    ax.legend(loc='upper left')
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    ax.set_xticklabels(['£1m', '£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                        '£200m', '£500m', '£1bn', '£2bn', '£5bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_4a_wmin_rate_curves.png')


def fig_wmin_heatmaps(d):
    labels = [f'W_min=£{v:.0f}m' + (' (canonical)' if v == _A.CANON_WMIN else '')
              for v in _A.WMIN_VALS]
    _heatmap_4panel(
        d['val_s']['wmin_c1_matrices'][:4], _A.WMIN_VALS[:4], _A.CANON_WMIN, labels[:4],
        suptitle=(
            'Fig S2.4b — C.1 advantage landscape across W_min values\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
            f'N={_A.CANON_N}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical'
        ),
        fname='val_s_fig_s2_4b_wmin_heatmaps.png',
    )


def fig_wmin_n_crossings(d):
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
        f'Fig S2.4c — N-crossing thresholds by W_min\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
        f'V₀=£{_A.CANON_V0:.0f}m, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(); ax.set_xlim(0.5, 11)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s2_4c_wmin_n_crossings.png')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    p = load_params()
    init(p)
    ensure_dir(_OUT)
    d = _load()

    print('VAL.S Script 1 — rate function parameter sweeps (from cache)')

    print('\n§2.1  τ₀ sweep...')
    fig_tau0_heatmaps(d)
    fig_tau0_n_crossings(d)
    fig_tau0_tolerant_zone(d)

    print('\n§2.2  τ_m sweep...')
    fig_taum_heatmaps(d)
    fig_taum_penalty_plateaus(d)
    fig_taum_n_crossings(d)

    print('\n§2.3  k sweep...')
    fig_k_rate_curves(p)
    fig_k_heatmaps(d)
    fig_k_bracket_penalty(d)

    print('\n§2.4  W_min sweep...')
    fig_wmin_rate_curves(p)
    fig_wmin_heatmaps(d)
    fig_wmin_n_crossings(d)

    print(f'\nScript 1 complete. Figures in {_OUT}')


if __name__ == '__main__':
    main()
