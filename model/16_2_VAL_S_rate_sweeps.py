"""
VAL.S Output Script 1 — Rate Function Parameter Sweeps
========================================================
Generates figures for §2 of VAL.S:
  §2.1  τ₀ sweep  (entry rate floor)
  §2.2  τ_m sweep (asymptotic ceiling)
  §2.3  k sweep   (steepness parameter)
  §2.4  W_min sweep (entry-wealth threshold)

Canonical reference:  τ₀=20%, τ_m=70%, k=0.001, W_min=£2m, N=34, g=10.45%, V₀=£20m
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
from wdt_style import apply_style, save_fig, FIG_SINGLE, FIG_QUAD, C_ANNOTATION
import wdt_analytics as _A
from wdt_analytics import (init, make_p, run_sim_p, c1, c1_matrix,
                            n_crossing, tolerant_zone_bounds)

_OUT = out_dir('VAL_S')

# Aliases — all internal call sites unchanged
set_style = apply_style


def save(fig, name):
    return save_fig(fig, _OUT / name)


# Module-scope label/colour lists — populated in main() after init()
TAU0_LABELS = []
TAUM_LABELS = []
K_LABELS    = []
WMIN_LABELS = []
TAU0_COLS   = ['#2166ac', '#4dac26', '#d73027', '#7b2d8b']
K_COLS      = ['#2166ac', '#4dac26', '#d73027', '#7b2d8b']
WMIN_COLS   = ['#2166ac', '#d73027', '#7b2d8b', '#4dac26']

# ─────────────────────────────────────────────────────────────
# §2.1  τ₀ SWEEP
# ─────────────────────────────────────────────────────────────


def fig_tau0_heatmaps():
    """4-panel C.1 heatmap grid across τ₀ values."""
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, tau_0, label in zip(axes, _A.TAU0_VALS, TAU0_LABELS):
        p = make_p(tau_0=tau_0)
        mat = c1_matrix(p)
        ax.grid(False)
        im = ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
        ax.set_xticks(range(len(_A.G_VALS)))
        ax.set_xticklabels(_A.G_LABELS, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(_A.ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in _A.ALPHA_VALS])
        ax.set_xlabel('g', fontsize=8)
        ax.set_ylabel('α', fontsize=8)
        ax.set_title(label, fontsize=10, fontweight='bold' if tau_0 == _A.CANON_TAU0 else 'normal')
        # Cell annotations
        for i in range(len(_A.ALPHA_VALS)):
            for j in range(len(_A.G_VALS)):
                v = mat[i, j]
                col = 'white' if abs(v) > vmax * 0.6 else '#1a1a1a'
                ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=6, color=col, zorder=3)
        # Highlight honest row
        hon = _A.ALPHA_VALS.index(1.0)
        ax.add_patch(plt.Rectangle((-0.5, hon - 0.5), len(_A.G_VALS), 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=1.5))

    cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cbar_ax)
    cbar_ax.set_ylabel('C.1 (pp)  +red = understater pays more  −blue = overstater pays less', fontsize=8)

    fig.suptitle(
        'Fig S2.1a — C.1 advantage landscape across τ₀ values\n'
        f'τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}, N = {_A.CANON_N}, V₀ = £{_A.CANON_V0:.0f}m  ·  '
        'Bold panel = canonical',
        fontsize=10, y=1.01
    )
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save(fig, 'val_s_fig_s2_1a_tau0_heatmaps.png')


def fig_tau0_n_crossings():
    """N-crossing thresholds for overstaters as a function of τ₀."""
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ls_by_alpha = {1.5: '-', 1.8: '--', 2.0: '-.'}
    col_by_alpha = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}

    for alpha in _A.OVER_ALPHAS:
        crossings = []
        for tau_0 in _A.TAU0_VALS:
            p = make_p(tau_0=tau_0)
            nc = n_crossing(p, alpha)
            crossings.append(nc if nc is not None else float('nan'))
        ax.plot(
            [t * 100 for t in _A.TAU0_VALS], crossings,
            color=col_by_alpha[alpha], linestyle=ls_by_alpha[alpha],
            linewidth=2, marker='o', markersize=5,
            label=f'α = {alpha}'
        )

    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':', label=f'N = {_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_TAU0 * 100, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_TAU0 * 100 + 0.3, ax.get_ylim()[0] + 1, f'τ₀ = {_A.CANON_TAU0*100:.0f}% (canonical)',
            fontsize=7.5, color='#666666')

    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('N at which overstater first pays more than honest')
    ax.set_title(
        f'Fig S2.1b — N-crossing thresholds by τ₀\n'
        f'τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}, V₀ = £{_A.CANON_V0:.0f}m, g = {_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    ax.set_xlim(8, 33)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_1b_tau0_n_crossings.png')


def fig_tau0_tolerant_zone():
    """Tolerant-zone width (α range where |C.1| < 2pp) as a function of τ₀."""
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    tau0_fine = [t / 100 for t in range(5, 45, 1)]
    widths = []
    los = []
    his = []
    for tau_0 in tau0_fine:
        p = make_p(tau_0=tau_0)
        lo, hi = tolerant_zone_bounds(p)
        if lo is not None and hi is not None:
            widths.append(hi - lo)
            los.append(lo)
            his.append(hi)
        else:
            widths.append(float('nan'))
            los.append(float('nan'))
            his.append(float('nan'))

    pct = [t * 100 for t in tau0_fine]
    ax.fill_between(pct, los, his, alpha=0.15, color='#4393c3', label='Tolerant zone (|C.1| < 2pp)')
    ax.plot(pct, los, color='#2166ac', linewidth=1.5, label='α_low boundary')
    ax.plot(pct, his, color='#d73027', linewidth=1.5, label='α_high boundary')
    ax.axhline(1.0, color='#888888', linewidth=0.8, linestyle='--', label='Honest (α = 1.0)')
    ax.axvline(_A.CANON_TAU0 * 100, color='#888888', linewidth=0.9, linestyle=':', label=f'Canonical τ₀ = {_A.CANON_TAU0*100:.0f}%')

    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('Declaration ratio α')
    ax.set_title(
        f'Fig S2.1c — Tolerant zone (|C.1| < {_A.TZONE_THRESHOLD*100:.0f}pp) boundaries by τ₀\n'
        f'τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}, N = {_A.CANON_N}, g = {_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    ax.set_xlim(5, 44)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_1c_tau0_tolerant_zone.png')


# ─────────────────────────────────────────────────────────────
# §2.2  τ_m SWEEP
# ─────────────────────────────────────────────────────────────


def fig_taum_heatmaps():
    """4-panel C.1 heatmap grid across τ_m values."""
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, tau_m, label in zip(axes, _A.TAUM_VALS, TAUM_LABELS):
        p = make_p(tau_m=tau_m)
        mat = c1_matrix(p)
        ax.grid(False)
        im = ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
        ax.set_xticks(range(len(_A.G_VALS)))
        ax.set_xticklabels(_A.G_LABELS, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(_A.ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in _A.ALPHA_VALS])
        ax.set_xlabel('g', fontsize=8)
        ax.set_ylabel('α', fontsize=8)
        ax.set_title(label, fontsize=10, fontweight='bold' if tau_m == _A.CANON_TAUM else 'normal')
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
        'Fig S2.2a — C.1 advantage landscape across τ_m values\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, k = {_A.CANON_K}, N = {_A.CANON_N}, V₀ = £{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10, y=1.01
    )
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save(fig, 'val_s_fig_s2_2a_taum_heatmaps.png')


def fig_taum_penalty_plateaus():
    """Understater penalty plateau ceiling by α as a function of τ_m."""
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    under_alphas = [0.1, 0.2, 0.5, 0.8]
    cols = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    ls_by_taum = {0.50: ':', 0.60: '--', 0.70: '-', 0.80: '-.'}

    # For each (tau_m, alpha), find the plateau ceiling:
    # max C.1 across g = 17%–40% (post-inflection plateau region)
    g_plateau_range = [g / 100 for g in range(18, 41)]

    for tau_m, ls in ls_by_taum.items():
        p = make_p(tau_m=tau_m)
        plateaus = []
        for alpha in under_alphas:
            vals = [c1(p, alpha, g_val) * 100 for g_val in g_plateau_range]
            plateaus.append(max(vals))
        ax.plot(
            [a * 100 for a in under_alphas], plateaus,
            linestyle=ls, linewidth=2, marker='o', markersize=5,
            label=f'τ_m = {tau_m*100:.0f}%' + (' (canonical)' if tau_m == _A.CANON_TAUM else '')
        )

    ax.set_xlabel('Declaration ratio α (understatement region)')
    ax.set_ylabel('Plateau ceiling of C.1 (pp) — peak penalty as % of understater TW')
    ax.set_title(
        f'Fig S2.2b — Understater penalty plateau ceiling by α and τ_m\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, k = {_A.CANON_K}, N = {_A.CANON_N}, g sweep 18–40%'
    )
    ax.legend()
    ax.set_xlim(5, 85)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_2b_taum_penalty_plateaus.png')


def fig_taum_n_crossings():
    """N-crossing thresholds for aggressive overstaters as a function of τ_m."""
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ls_by_alpha = {1.5: '-', 1.8: '--', 2.0: '-.'}
    col_by_alpha = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}
    taum_fine = [t / 100 for t in range(40, 85, 5)]

    for alpha in _A.OVER_ALPHAS:
        crossings = []
        for tau_m in taum_fine:
            p = make_p(tau_m=tau_m)
            nc = n_crossing(p, alpha)
            crossings.append(nc if nc is not None else float('nan'))
        ax.plot(
            [t * 100 for t in taum_fine], crossings,
            color=col_by_alpha[alpha], linestyle=ls_by_alpha[alpha],
            linewidth=2, marker='o', markersize=5,
            label=f'α = {alpha}'
        )

    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':', label=f'N = {_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_TAUM * 100, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_TAUM * 100 + 0.5, ax.get_ylim()[0] + 1,
            f'τ_m = {_A.CANON_TAUM*100:.0f}% (canonical)', fontsize=7.5, color='#666666')

    ax.set_xlabel('Ceiling rate τ_m (%)')
    ax.set_ylabel('N at crossing (overstater first pays more than honest)')
    ax.set_title(
        f'Fig S2.2c — N-crossing thresholds by τ_m\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, k = {_A.CANON_K}, V₀ = £{_A.CANON_V0:.0f}m, g = {_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_2c_taum_n_crossings.png')


# ─────────────────────────────────────────────────────────────
# §2.3  k SWEEP
# ─────────────────────────────────────────────────────────────



def fig_k_rate_curves():
    """Rate curve τ(W) overlaid for each k value."""
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    W_vals = np.logspace(np.log10(_A.CANON_WMIN), np.log10(5000), 400)

    for k_val, label, col in zip(_A.K_VALS, K_LABELS, K_COLS):
        p = make_p(k=k_val)
        tau_vals = [tau(w, p) * 100 for w in W_vals]
        lw = 2.2 if k_val == _A.CANON_K else 1.6
        ax.semilogx(W_vals, tau_vals, color=col, linewidth=lw,
                    label=label, linestyle='-' if k_val == _A.CANON_K else '--')

    ax.axvline(_A.CANON_V0, color='#888888', linewidth=1.0, linestyle=':', label=f'V₀ = £{_A.CANON_V0:.0f}m (reference)')
    ax.axhline(_A.CANON_TAU0 * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.axhline(_A.CANON_TAUM * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.text(4000, _A.CANON_TAU0 * 100 + 0.8, f'τ₀ = {_A.CANON_TAU0*100:.0f}%', fontsize=8, color='#888888', ha='right')
    ax.text(4000, _A.CANON_TAUM * 100 - 0.8, f'τ_m = {_A.CANON_TAUM*100:.0f}%', fontsize=8, color='#888888', ha='right', va='top')

    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Fig S2.3a — Rate curve τ(W) across k values\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, W_min = £{_A.CANON_WMIN:.0f}m'
    )
    ax.set_xlim(_A.CANON_WMIN, 5000)
    ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.12)
    ax.legend(loc='upper left')
    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                        '£200m', '£500m', '£1bn', '£2bn', '£5bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_3a_k_rate_curves.png')


def fig_k_heatmaps():
    """4-panel C.1 heatmap grid across k values."""
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, k_val, label in zip(axes, _A.K_VALS, K_LABELS):
        p = make_p(k=k_val)
        mat = c1_matrix(p)
        ax.grid(False)
        ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
        ax.set_xticks(range(len(_A.G_VALS)))
        ax.set_xticklabels(_A.G_LABELS, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(_A.ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in _A.ALPHA_VALS])
        ax.set_xlabel('g', fontsize=8)
        ax.set_ylabel('α', fontsize=8)
        ax.set_title(label, fontsize=10, fontweight='bold' if k_val == _A.CANON_K else 'normal')
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
        'Fig S2.3b — C.1 advantage landscape across k values\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, N = {_A.CANON_N}, V₀ = £{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10, y=1.01
    )
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save(fig, 'val_s_fig_s2_3b_k_heatmaps.png')


def fig_k_bracket_penalty():
    """
    Effective bracket penalty from overstatement (α = 1.8) at W = {£20m, £100m, £500m}
    as a function of k.  Penalty = C.1(α=1.8, g=10.45%) at that V₀.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    V0_points = [20.0, 100.0, 500.0]
    cols = ['#2166ac', '#d73027', '#7b2d8b']
    k_fine = [k / 10000 for k in range(1, 55)]   # 0.0001 to 0.0054

    for V0, col in zip(V0_points, cols):
        c1_vals = []
        for k_val in k_fine:
            p = make_p(k=k_val, V0_m=V0)
            c1_vals.append(c1(p, alpha=1.8, g=_A.CANON_G) * 100)
        ax.plot(k_fine, c1_vals, color=col, linewidth=2,
                label=f'V₀ = £{V0:.0f}m')

    ax.axhline(0, color='#888888', linewidth=0.8, linestyle='--', label='Honest baseline (C.1 = 0)')
    ax.axvline(_A.CANON_K, color='#888888', linewidth=0.9, linestyle=':',
               label=f'Canonical k = {_A.CANON_K}')

    ax.set_xlabel('k (steepness parameter)')
    ax.set_ylabel('C.1 at α = 1.8 (pp)  — negative = overstater advantage')
    ax.set_title(
        f'Fig S2.3c — Bracket penalty for α = 1.8 by k and V₀\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, N = {_A.CANON_N}, g = {_A.CANON_G*100:.1f}%  ·  '
        'Positive = overstater pays more than honest'
    )
    ax.legend()
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_3c_k_bracket_penalty.png')


# ─────────────────────────────────────────────────────────────
# §2.4  W_min SWEEP
# ─────────────────────────────────────────────────────────────



def fig_wmin_rate_curves():
    """
    Rate curve τ(W) overlaid for each W_min value.
    W_min shifts the onset of the logistic without altering τ₀, τ_m, or k,
    so all curves share the same shape but begin at different points on the
    wealth axis.  Below W_min, τ = 0.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    W_vals = np.logspace(np.log10(0.5), np.log10(5000), 600)

    for w_min, label, col in zip(_A.WMIN_VALS, WMIN_LABELS, WMIN_COLS):
        p = make_p(W_min=w_min)
        tau_vals = [tau(w, p) * 100 for w in W_vals]
        lw = 2.2 if w_min == _A.CANON_WMIN else 1.6
        ax.semilogx(W_vals, tau_vals, color=col, linewidth=lw,
                    label=label, linestyle='-' if w_min == _A.CANON_WMIN else '--')

    ax.axvline(_A.CANON_V0, color='#888888', linewidth=1.0, linestyle=':',
               label=f'V₀ = £{_A.CANON_V0:.0f}m (reference)')
    ax.axhline(_A.CANON_TAU0 * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.axhline(_A.CANON_TAUM * 100, color='#aaaaaa', linewidth=0.7, linestyle='--')
    ax.text(4000, _A.CANON_TAU0 * 100 + 0.8, f'τ₀ = {_A.CANON_TAU0*100:.0f}%',
            fontsize=8, color='#888888', ha='right')
    ax.text(4000, _A.CANON_TAUM * 100 - 0.8, f'τ_m = {_A.CANON_TAUM*100:.0f}%',
            fontsize=8, color='#888888', ha='right', va='top')

    # Annotate each W_min onset with a short vertical tick
    for w_min, col in zip(_A.WMIN_VALS, WMIN_COLS):
        ax.axvline(w_min, color=col, linewidth=0.8, linestyle=':', alpha=0.5)

    ax.set_xlabel('Declared net worth W (£m, log scale)')
    ax.set_ylabel('Marginal WDT rate τ(W) (%)')
    ax.set_title(
        f'Fig S2.4a — Rate curve τ(W) across W_min values\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}'
    )
    ax.set_xlim(0.5, 5000)
    ax.set_ylim(0, _A.CANON_TAUM * 100 * 1.12)
    ax.legend(loc='upper left')
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000])
    ax.set_xticklabels(['£1m', '£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                        '£200m', '£500m', '£1bn', '£2bn', '£5bn'],
                       rotation=45, ha='right', fontsize=7.5)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_4a_wmin_rate_curves.png')


def fig_wmin_heatmaps():
    """4-panel C.1 heatmap grid across W_min values."""
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    axes = axes.flatten()

    vmax = 30.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    for ax, w_min, label in zip(axes, _A.WMIN_VALS, WMIN_LABELS):
        p = make_p(W_min=w_min)
        mat = c1_matrix(p)
        ax.grid(False)
        ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
        ax.set_xticks(range(len(_A.G_VALS)))
        ax.set_xticklabels(_A.G_LABELS, rotation=45, ha='right', fontsize=7)
        ax.set_yticks(range(len(_A.ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in _A.ALPHA_VALS])
        ax.set_xlabel('g', fontsize=8)
        ax.set_ylabel('α', fontsize=8)
        ax.set_title(label, fontsize=10,
                     fontweight='bold' if w_min == _A.CANON_WMIN else 'normal')
        for i in range(len(_A.ALPHA_VALS)):
            for j in range(len(_A.G_VALS)):
                v = mat[i, j]
                col = 'white' if abs(v) > vmax * 0.6 else '#1a1a1a'
                ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                        fontsize=6, color=col, zorder=3)
        hon = _A.ALPHA_VALS.index(1.0)
        ax.add_patch(plt.Rectangle((-0.5, hon - 0.5), len(_A.G_VALS), 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=1.5))

    cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'), cax=cbar_ax)
    cbar_ax.set_ylabel('C.1 (pp)', fontsize=8)

    fig.suptitle(
        'Fig S2.4b — C.1 advantage landscape across W_min values\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}, '
        f'N = {_A.CANON_N}, V₀ = £{_A.CANON_V0:.0f}m  ·  Bold = canonical',
        fontsize=10, y=1.01
    )
    plt.tight_layout(rect=[0, 0, 0.91, 1])
    save(fig, 'val_s_fig_s2_4b_wmin_heatmaps.png')


def fig_wmin_n_crossings():
    """
    N-crossing thresholds for α ∈ {1.5, 1.8, 2.0} as a function of W_min.
    W_min controls the entry point of the rate function; a higher W_min means
    the effective rate at V₀ = £20m is lower, which changes the speed at which
    overstatement becomes self-defeating.
    """
    set_style()
    fig, ax = plt.subplots(figsize=(9, 5.5))

    ls_by_alpha = {1.5: '-', 1.8: '--', 2.0: '-.'}
    col_by_alpha = {1.5: '#4393c3', 1.8: '#2166ac', 2.0: '#053061'}
    wmin_fine = [w / 10 for w in range(5, 110, 5)]   # £0.5m to £10.5m in steps of £0.5m

    for alpha in _A.OVER_ALPHAS:
        crossings = []
        for w_min in wmin_fine:
            p = make_p(W_min=w_min)
            nc = n_crossing(p, alpha)
            crossings.append(nc if nc is not None else float('nan'))
        ax.plot(
            wmin_fine, crossings,
            color=col_by_alpha[alpha], linestyle=ls_by_alpha[alpha],
            linewidth=2, marker='o', markersize=4,
            label=f'α = {alpha}'
        )

    ax.axhline(_A.CANON_N, color='#888888', linewidth=0.9, linestyle=':',
               label=f'N = {_A.CANON_N} (RATES ref)')
    ax.axvline(_A.CANON_WMIN, color='#888888', linewidth=0.9, linestyle=':')
    ax.text(_A.CANON_WMIN + 0.15, ax.get_ylim()[0] + 1,
            f'W_min = £{_A.CANON_WMIN:.0f}m (canonical)', fontsize=7.5, color='#666666')
    ax.axvline(_A.CANON_V0, color='#cccccc', linewidth=0.8, linestyle='--',
               label=f'V₀ = £{_A.CANON_V0:.0f}m (reference wealth)')

    ax.set_xlabel('Entry threshold W_min (£m)')
    ax.set_ylabel('N at which overstater first pays more than honest')
    ax.set_title(
        f'Fig S2.4c — N-crossing thresholds by W_min\n'
        f'τ₀ = {_A.CANON_TAU0*100:.0f}%, τ_m = {_A.CANON_TAUM*100:.0f}%, k = {_A.CANON_K}, '
        f'V₀ = £{_A.CANON_V0:.0f}m, g = {_A.CANON_G*100:.1f}%'
    )
    ax.legend()
    ax.set_xlim(0.5, 11)
    plt.tight_layout()
    save(fig, 'val_s_fig_s2_4c_wmin_n_crossings.png')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    init(p)

    print('VAL.S Script 1: rate function parameter sweeps')
    print(f'Canonical (from TOML): τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
          f'k={_A.CANON_K}, W_min=£{_A.CANON_WMIN:.0f}m, N={_A.CANON_N}, '
          f'V₀=£{_A.CANON_V0:.0f}m, g={_A.CANON_G*100:.2f}%')

    # Populate module-scope label lists (require init() first)
    global TAU0_LABELS, TAUM_LABELS, K_LABELS, WMIN_LABELS
    TAU0_LABELS = [f'τ₀ = {v*100:.0f}%'   + (' (canonical)' if v == _A.CANON_TAU0 else '') for v in _A.TAU0_VALS]
    TAUM_LABELS = [f'τ_m = {v*100:.0f}%'  + (' (canonical)' if v == _A.CANON_TAUM else '') for v in _A.TAUM_VALS]
    K_LABELS    = [f'k = {v}'              + (' (canonical)' if v == _A.CANON_K    else '') for v in _A.K_VALS]
    WMIN_LABELS = [f'W_min = £{v:.0f}m'   + (' (canonical)' if v == _A.CANON_WMIN else '') for v in _A.WMIN_VALS]

    ensure_dir(_OUT)

    print('\n§2.1  τ₀ sweep...')
    fig_tau0_heatmaps()
    fig_tau0_n_crossings()
    fig_tau0_tolerant_zone()

    print('\n§2.2  τ_m sweep...')
    fig_taum_heatmaps()
    fig_taum_penalty_plateaus()
    fig_taum_n_crossings()

    print('\n§2.3  k sweep...')
    fig_k_rate_curves()
    fig_k_heatmaps()
    fig_k_bracket_penalty()

    print('\n§2.4  W_min sweep...')
    fig_wmin_rate_curves()
    fig_wmin_heatmaps()
    fig_wmin_n_crossings()

    print(f'\nScript 1 complete. Figures in {_OUT}')


if __name__ == '__main__':
    main()
