"""
VAL.S Output Script 2 — Horizon and Wealth-Level Sweeps
=========================================================
Generates figures for §3 of VAL.S:
  §3.1  N sweep  (holding period)
  §3.2  V₀ sweep (entry wealth level)

Canonical reference:  τ₀=20%, τ_m=70%, k=0.001, N=34, g=10.45%, V₀=£20m
Outputs to: ./OUTPUTS/VAL_S/
All simulation via wdt_core.run_sim() with caching from val_s_helpers.
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from wdt_core import load_params, run_sim, tau
from wdt_fmt import out_dir, ensure_dir
from wdt_style import apply_style, save_fig
import wdt_analytics as _A
from wdt_analytics import (init, make_p, run_sim_p, c1,
                            n_crossing, tolerant_zone_bounds)

_OUT = out_dir('VAL_S')

# Aliases — all internal call sites unchanged
set_style = apply_style


def save(fig, name):
    return save_fig(fig, _OUT / name)


# Module-scope label/colour lists — populated in main() after init()
V0_LABELS = []
V0_COLS   = ['#2166ac', '#d73027', '#7b2d8b', '#4dac26']


# ─────────────────────────────────────────────────────────────
# §3.1  N SWEEP
# ─────────────────────────────────────────────────────────────

def fig_n_crossing_annotated():
    """
    N-crossing thresholds for α ∈ {1.5, 1.8, 2.0} at canonical parameters,
    shown on a timeline with the RATES reference N annotated.
    Also shows net-tax difference trajectory for each α.
    """
    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    p = make_p()
    N_sweep = list(range(5, 66))
    cols = ['#4393c3', '#2166ac', '#053061']
    ls   = ['-', '--', '-.']

    # Left: net tax difference by N for each overstater alpha
    for alpha, col, style in zip(_A.OVER_ALPHAS, cols, ls):
        diffs = []
        for n in N_sweep:
            r = run_sim(p, alpha=alpha, g=_A.CANON_G, N=n)
            b = run_sim(p, alpha=1.0,   g=_A.CANON_G, N=n)
            diffs.append(r['Net'] - b['Net'])
        ax1.plot(N_sweep, diffs, color=col, linestyle=style, linewidth=2, label=f'α = {alpha}')

    ax1.axhline(0, color='#333333', linewidth=1.2, linestyle='-', label='Honest (zero line)')
    ax1.axvline(_A.CANON_N, color='#888888', linewidth=1.0, linestyle=':',
                label=f'N = {_A.CANON_N} (RATES ref)')
    ax1.text(_A.CANON_N + 0.5, ax1.get_ylim()[0] * 0.85,
             f'N = {_A.CANON_N}', fontsize=8, color='#666666')
    ax1.fill_between(N_sweep, [0] * len(N_sweep), [min(0, d) for d in
                     [sum([run_sim(p, alpha=1.5, g=_A.CANON_G, N=n)['Net'] -
                           run_sim(p, alpha=1.0, g=_A.CANON_G, N=n)['Net'] for alpha in [1.5]])
                      for n in N_sweep]], alpha=0.05, color='#2166ac')
    ax1.set_xlabel('Holding period N (years)')
    ax1.set_ylabel('Net(α) − Net(honest)  [£m]\n− = overstater pays less')
    ax1.set_title(f'Overstater net-tax advantage by N\ng = {_A.CANON_G*100:.1f}% (canonical)')
    ax1.legend(fontsize=8)
    ax1.set_xlim(5, 65)

    # Right: bar chart of crossing N for each alpha
    crossing_ns = []
    for alpha in _A.OVER_ALPHAS:
        nc = n_crossing(p, alpha, N_sweep=N_sweep)
        crossing_ns.append(nc)

    x = range(len(_A.OVER_ALPHAS))
    bars = ax2.bar(x, [cn if cn is not None else 0 for cn in crossing_ns],
                   color=cols, edgecolor='white', width=0.5)
    ax2.axhline(_A.CANON_N, color='#888888', linewidth=1.5, linestyle='--',
                label=f'N = {_A.CANON_N} (RATES ref)')

    for bar, alpha, nc in zip(bars, _A.OVER_ALPHAS, crossing_ns):
        if nc is not None:
            ax2.text(bar.get_x() + bar.get_width() / 2, nc + 0.8,
                     f'N ≈ {nc:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        else:
            ax2.text(bar.get_x() + bar.get_width() / 2, 3,
                     'no\ncrossing\nin range', ha='center', va='bottom', fontsize=8, color='#666666')

    ax2.set_xticks(x)
    ax2.set_xticklabels([f'α = {a}' for a in _A.OVER_ALPHAS])
    ax2.set_ylabel('N at first crossing (overstater pays more than honest)')
    ax2.set_title(f'N-crossing thresholds\ng = {_A.CANON_G*100:.1f}%  ·  τ₀={_A.CANON_TAU0*100:.0f}%  ·  k={_A.CANON_K}')
    ax2.legend()
    ax2.set_ylim(0, 70)

    fig.suptitle(
        f'Fig S3.1a — Overstater advantage erosion and N-crossing thresholds\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m',
        fontsize=10
    )
    plt.tight_layout()
    save(fig, 'val_s_fig_s3_1a_n_crossing_annotated.png')


def fig_n_understater_panels():
    """
    Understater C.1 by g at N ∈ {10, 20, 34, 50} — 4-panel.
    Shows how penalty profile evolves with horizon.
    """
    set_style()
    N_VALS  = _A.N_PANEL_VALS
    N_LABEL = [f'N = {n}' + (' (canonical)' if n == _A.CANON_N else '') for n in N_VALS]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes = axes.flatten()

    under_cols = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    g_fine = [g / 1000 for g in range(0, 401)]

    for ax, n, label in zip(axes, N_VALS, N_LABEL):
        p = make_p(N=n)
        for alpha, col in zip(_A.UNDER_ALPHAS, under_cols):
            c1_vals = [c1(p, alpha, gv, N=n) * 100 for gv in g_fine]
            ax.plot([gv * 100 for gv in g_fine], c1_vals, color=col, linewidth=1.8, label=f'α = {alpha}')

        ax.axhline(0, color='#1a1a1a', linewidth=0.8, linestyle=':')
        ax.axvline(_A.CANON_G * 100, color='#888888', linewidth=0.8, linestyle='--')
        ax.text(_A.CANON_G * 100 + 0.2, 2, f'g = {_A.CANON_G*100:.1f}%', fontsize=7.5, color='#666666')
        ax.set_xlabel('g (%)')
        ax.set_ylabel('C.1 (pp)')
        ax.set_title(label, fontsize=10, fontweight='bold' if n == _A.CANON_N else 'normal')
        ax.set_xlim(0, 35)
        ax.legend(fontsize=7.5)

    fig.suptitle(
        'Fig S3.1b — Understater penalty profile across holding periods\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10
    )
    plt.tight_layout()
    save(fig, 'val_s_fig_s3_1b_n_understater_panels.png')


def fig_n_tolerant_zone():
    """
    Tolerant-zone bounds (|C.1| < 2pp) across N values at canonical g.
    Shows whether the α = 0.8–1.5 band is stable across N.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    n_fine = list(range(5, 66, 2))
    los, his = [], []
    for n in n_fine:
        p = make_p(N=n)
        lo, hi = tolerant_zone_bounds(p)
        los.append(lo if lo is not None else float('nan'))
        his.append(hi if hi is not None else float('nan'))

    ax.fill_between(n_fine, los, his, alpha=0.20, color='#4393c3', label='Tolerant zone (|C.1| < 2pp)')
    ax.plot(n_fine, los, color='#2166ac', linewidth=1.5, label='α_low boundary')
    ax.plot(n_fine, his, color='#d73027', linewidth=1.5, label='α_high boundary')
    ax.axhline(0.8, color='#888888', linewidth=0.8, linestyle=':', label='α = 0.8 (VAL.A tolerant zone lower)')
    ax.axhline(1.5, color='#888888', linewidth=0.8, linestyle='--', label='α = 1.5 (VAL.A tolerant zone upper)')
    ax.axhline(1.0, color='#555555', linewidth=0.8, linestyle='-', label='Honest (α = 1.0)')
    ax.axvline(_A.CANON_N, color='#aaaaaa', linewidth=1.0, linestyle=':',
               label=f'N = {_A.CANON_N} (RATES ref)')

    ax.set_xlabel('Holding period N (years)')
    ax.set_ylabel('Declaration ratio α')
    ax.set_title(
        f'Fig S3.1c — Tolerant zone (|C.1| < {_A.TZONE_THRESHOLD*100:.0f}pp) stability across N\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=7.5)
    ax.set_xlim(5, 65)
    ax.set_ylim(0.5, 2.2)
    plt.tight_layout()
    save(fig, 'val_s_fig_s3_1c_n_tolerant_zone.png')


# ─────────────────────────────────────────────────────────────
# §3.2  V₀ SWEEP
# ─────────────────────────────────────────────────────────────


def fig_v0_c1_curves():
    """
    C.1 by α at four V₀ levels overlaid, at canonical g.
    Shows how the incentive structure scales with wealth.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    alpha_fine = [a / 100 for a in range(10, 201, 5)]
    ls_map = {5.0: ':', 20.0: '-', 100.0: '--', 500.0: '-.'}

    for v0, label, col in zip(_A.V0_VALS, V0_LABELS, V0_COLS):
        p = make_p(V0_m=v0)
        c1_vals = [c1(p, a, _A.CANON_G) * 100 for a in alpha_fine]
        lw = 2.2 if v0 == _A.CANON_V0 else 1.6
        ax.plot([a * 100 for a in alpha_fine], c1_vals,
                color=col, linewidth=lw, linestyle=ls_map[v0],
                label=label)

    ax.axhline(0, color='#888888', linewidth=0.9, linestyle='--', label='Honest baseline')
    ax.axvline(100, color='#888888', linewidth=0.8, linestyle=':', label='α = 1.0 (honest)')

    # Shade understater / overstater regions lightly
    ax.axvspan(10, 100, alpha=0.03, color='#d73027')
    ax.axvspan(100, 200, alpha=0.03, color='#4393c3')

    ax.set_xlabel('Declaration ratio α (%)  — 100% = honest')
    ax.set_ylabel('C.1 (pp)  +positive = pays more than honest')
    ax.set_title(
        f'Fig S3.2a — C.1 incentive structure by V₀ entry wealth\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%'
    )
    ax.legend(fontsize=8)
    ax.set_xlim(10, 200)
    ax.set_ylim(-25, 30)
    plt.tight_layout()
    save(fig, 'val_s_fig_s3_2a_v0_c1_curves.png')


def fig_v0_entry_rate():
    """
    Entry rate τ(V₀) as a function of V₀, annotated with the four reference levels.
    Shows where on the rate curve each V₀ sits.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    p = make_p()
    W_range = np.logspace(np.log10(_A.CANON_WMIN), np.log10(2000), 500)
    tau_vals = [tau(w, p) * 100 for w in W_range]

    ax.semilogx(W_range, tau_vals, color='#1a1a1a', linewidth=2, label='τ(W)')
    ax.axhline(_A.CANON_TAU0 * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.axhline(_A.CANON_TAUM * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.text(1500, _A.CANON_TAU0 * 100 + 0.5, f'τ₀ = {_A.CANON_TAU0*100:.0f}%', fontsize=8, color='#888888', ha='right')
    ax.text(1500, _A.CANON_TAUM * 100 - 0.5, f'τ_m = {_A.CANON_TAUM*100:.0f}%', fontsize=8, color='#888888', ha='right', va='top')

    for v0, label, col in zip(_A.V0_VALS, V0_LABELS, V0_COLS):
        rate_at_v0 = tau(v0, p) * 100
        ax.plot(v0, rate_at_v0, 'o', color=col, markersize=9, zorder=5)
        ax.annotate(
            f'{label}\nτ = {rate_at_v0:.1f}%',
            xy=(v0, rate_at_v0),
            xytext=(v0 * 1.6, rate_at_v0 + 3 if rate_at_v0 < 50 else rate_at_v0 - 5),
            fontsize=7.5, color=col,
            arrowprops=dict(arrowstyle='->', color=col, lw=0.8)
        )

    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Fig S3.2b — Entry rate τ(V₀) at four wealth levels\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, W_min=£{_A.CANON_WMIN:.0f}m'
    )
    ax.set_xlim(_A.CANON_WMIN, 2000)
    ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.15)
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m', '£100m', '£200m', '£500m', '£1bn', '£2bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    save(fig, 'val_s_fig_s3_2b_v0_entry_rate.png')


def fig_v0_heatmaps():
    """
    2×2 C.1 heatmap grid across V₀ values — same format as rate-sweep heatmaps.
    """
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, v0, label in zip(axes, _A.V0_VALS, V0_LABELS):
        p = make_p(V0_m=v0)
        mat = np.zeros((len(_A.ALPHA_VALS), len(_A.G_VALS)))
        for i, alpha in enumerate(_A.ALPHA_VALS):
            for j, g_val in enumerate(_A.G_VALS):
                mat[i, j] = c1(p, alpha, g_val) * 100
        ax.grid(False)
        ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
        ax.set_xticks(range(len(_A.G_VALS)))
        ax.set_xticklabels(_A.G_LABELS, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(_A.ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in _A.ALPHA_VALS])
        ax.set_xlabel('g', fontsize=8)
        ax.set_ylabel('α', fontsize=8)
        ax.set_title(label, fontsize=10, fontweight='bold' if v0 == _A.CANON_V0 else 'normal')
        for i in range(len(_A.ALPHA_VALS)):
            for j in range(len(_A.G_VALS)):
                v = mat[i, j]
                col = 'white' if abs(v) > vmax * 0.6 else '#1a1a1a'
                ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=6, color=col, zorder=3)
        hon = _A.ALPHA_VALS.index(1.0)
        ax.add_patch(plt.Rectangle((-0.5, hon - 0.5), len(_A.G_VALS), 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=1.5))

    cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cbar_ax)
    cbar_ax.set_ylabel('C.1 (pp)', fontsize=8)

    fig.suptitle(
        'Fig S3.2c — C.1 advantage landscape across V₀ wealth levels\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}  ·  Bold = canonical',
        fontsize=10, y=1.01
    )
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save(fig, 'val_s_fig_s3_2c_v0_heatmaps.png')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    init(p)

    print('VAL.S Script 2: horizon and wealth-level sweeps')
    print(f'Canonical (from TOML): τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
          f'k={_A.CANON_K}, N={_A.CANON_N}, V₀=£{_A.CANON_V0:.0f}m, g={_A.CANON_G*100:.2f}%')

    global V0_LABELS
    V0_LABELS = [f'V₀ = £{v:.0f}m' + (' (canonical)' if v == _A.CANON_V0 else '')
                 for v in _A.V0_VALS]

    ensure_dir(_OUT)

    print('\n§3.1  N sweep...')
    fig_n_crossing_annotated()
    fig_n_understater_panels()
    fig_n_tolerant_zone()

    print('\n§3.2  V₀ sweep...')
    fig_v0_c1_curves()
    fig_v0_entry_rate()
    fig_v0_heatmaps()

    print(f'\nScript 2 complete. Figures in {_OUT}')


if __name__ == '__main__':
    main()
