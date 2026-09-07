"""
VAL.S Output Script 2 — Horizon and Wealth-Level Sweeps
=========================================================
Generates figures for §3 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  §3.1  N sweep (holding period)
  §3.2  V₀ sweep (entry wealth level)
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from wdt_core import load_params, tau
from wdt_fmt import out_dir, ensure_dir
from wdt_style import apply_style, apply_style_nogrid, save_fig, FIG_SINGLE, FIG_QUAD
from wdt_analytics import init, draw_c1_heatmap
import wdt_analytics as _A

_OUT   = out_dir('VAL_S')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


def _save(fig, name):
    return save_fig(fig, _OUT / name)


def _v0_labels():
    return [f'V₀=£{v:.0f}m' + (' (canonical)' if v == _A.CANON_V0 else '')
            for v in _A.V0_VALS]


V0_COLS = ['#2166ac', '#d73027', '#7b2d8b', '#4dac26']


# ── §3.1  N sweep ─────────────────────────────────────────────────────────────

def fig_n_crossing_annotated(d):
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
    ax1.set_title(f'Overstater net-tax advantage by N\ng={_A.CANON_G*100:.1f}% (canonical)')
    ax1.legend(fontsize=8); ax1.set_xlim(5, 65)

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
        f'Fig S3.1a — Overstater advantage erosion and N-crossing thresholds\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, '
        f'V₀=£{_A.CANON_V0:.0f}m',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'val_s_fig_s3_1a_n_crossing_annotated.png')


def fig_n_understater_panels(d):
    apply_style()
    under_cols = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    g_fine     = d['val_s']['g_fine']
    labels     = [f'N={n}' + (' (canonical)' if n == _A.CANON_N else '')
                  for n in _A.N_PANEL_VALS]
    fig, axes  = plt.subplots(2, 2, figsize=FIG_QUAD)

    for ax, n, label in zip(axes.flat, _A.N_PANEL_VALS, labels):
        c1_data = d['val_s']['n_understater_c1'][str(n)]
        for alpha, col in zip(_A.UNDER_ALPHAS, under_cols):
            ax.plot([gv * 100 for gv in g_fine], c1_data[str(alpha)],
                    color=col, linewidth=1.8, label=f'α={alpha}')
        ax.axhline(0, color='#1a1a1a', linewidth=0.8, linestyle=':')
        ax.axvline(_A.CANON_G * 100, color='#888888', linewidth=0.8, linestyle='--')
        ax.text(_A.CANON_G * 100 + 0.2, 2, f'g={_A.CANON_G*100:.1f}%',
                fontsize=7.5, color='#666666')
        ax.set_xlabel('g (%)')
        ax.set_ylabel('C.1 (pp)')
        ax.set_title(label, fontsize=10,
                     fontweight='bold' if n == _A.CANON_N else 'normal')
        ax.set_xlim(0, 35); ax.legend(fontsize=7.5)

    fig.suptitle(
        'Fig S3.1b — Understater penalty profile across holding periods\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'val_s_fig_s3_1b_n_understater_panels.png')


def fig_n_tolerant_zone(d):
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
        f'Fig S3.1c — Tolerant zone stability across N\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=7.5); ax.set_xlim(5, 65); ax.set_ylim(0.5, 2.2)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s3_1c_n_tolerant_zone.png')


# ── §3.2  V₀ sweep ────────────────────────────────────────────────────────────

def fig_v0_c1_curves(d):
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
        f'Fig S3.2a — C.1 incentive structure by V₀ entry wealth\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=8); ax.set_xlim(10, 200); ax.set_ylim(-25, 30)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s3_2a_v0_c1_curves.png')


def fig_v0_entry_rate(p):
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
        f'Fig S3.2b — Entry rate τ(V₀) at four wealth levels\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, W_min=£{_A.CANON_WMIN:.0f}m'
    )
    ax.set_xlim(_A.CANON_WMIN, 2000); ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.15)
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m',
                        '£100m', '£200m', '£500m', '£1bn', '£2bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s3_2b_v0_entry_rate.png')


def fig_v0_heatmaps(d):
    _heatmap_4panel_nogrid(
        d['val_s']['v0_c1_matrices'][:4], _A.V0_VALS[:4], _A.CANON_V0,
        _v0_labels()[:4],
        suptitle=(
            'Fig S3.2c — C.1 advantage landscape across V₀ wealth levels\n'
            f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
            f'k={_A.CANON_K}, N={_A.CANON_N}  ·  Bold = canonical'
        ),
        fname='val_s_fig_s3_2c_v0_heatmaps.png',
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    p = load_params()
    init(p)
    ensure_dir(_OUT)
    d = _load()

    print('VAL.S Script 2 — horizon and wealth-level sweeps (from cache)')

    print('\n§3.1  N sweep...')
    fig_n_crossing_annotated(d)
    fig_n_understater_panels(d)
    fig_n_tolerant_zone(d)

    print('\n§3.2  V₀ sweep...')
    fig_v0_c1_curves(d)
    fig_v0_entry_rate(p)
    fig_v0_heatmaps(d)

    print(f'\nScript 2 complete. Figures in {_OUT}')


if __name__ == '__main__':
    main()
