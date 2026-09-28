"""
VAL Output Script D — Figures (v4 — data-driven)
=================================================
All simulation data is loaded from OUTPUTS/VAL/val_data.json
(produced by val_core.py). No wdt_core simulation calls here.

To regenerate output:
    python val_core.py          # run simulations
    python 5_4_VAL_charts.py   # render figures

If val_data.json is current you can re-run this script alone to
adjust figure formatting without re-running simulations.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from val_core import load_val_data
from wdt_fmt import out_dir, ensure_dir
from wdt_style import (
    apply_style, apply_style_nogrid, save_fig,
    FIG_SINGLE, FIG_SINGLE_W, FIG_PAIR_T, FIG_QUAD_XL, FIG_PAIR_XW,
    C_UNDER, C_HONEST, C_OVER, C_OVER_LIGHT,
    C_ANNOTATION, C_DARK,
)

_OUT = out_dir('VAL')


def _save(fig, name):
    return save_fig(fig, _OUT / name)


# ─────────────────────────────────────────────────────────────
# FIG 05 — Rate function τ(W)
# ─────────────────────────────────────────────────────────────

def fig_5_rate_function(data: dict):
    print("  Generating fig 05: rate function τ(W)...")
    p  = data['params']
    cd = data['charts']['fig_5_rate_function']

    W_vals   = cd['w_vals']
    tau_vals = cd['tau_vals']
    entry_rate = tau_vals[0] * 100   # τ at W_min (first point)

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    ax.semilogx(W_vals, [t * 100 for t in tau_vals], color=C_DARK, linewidth=2)

    ax.axhline(p['tau_0'] * 100, color=C_ANNOTATION, linewidth=0.8, linestyle='--')
    ax.axhline(p['tau_m'] * 100, color=C_ANNOTATION, linewidth=0.8, linestyle='--')

    ax.axvline(p['V0_m'], color='#2166ac', linewidth=1.5, linestyle=':',
               label=f"$V_0$ = £{p['V0_m']:.0f}m (reference scenario)")

    ax.text(8000, p['tau_0'] * 100 + 0.8,
            f"$\\tau_0$ = {p['tau_0']*100:.0f}% (floor parameter)",
            va='bottom', ha='right', fontsize=8, color='#666666')
    ax.text(8000, p['tau_m'] * 100 + 2.2,
            f"$\\tau_m$ = {p['tau_m']*100:.0f}% (ceiling)",
            va='top', ha='right', fontsize=8, color='#666666')

    ax.annotate(
        f"Entry rate at W_min\n= {entry_rate:.1f}%",
        xy=(p['W_min'], entry_rate),
        xytext=(p['W_min'] * 2.5, entry_rate + 6),
        fontsize=8, color=C_DARK,
        arrowprops=dict(arrowstyle='->', color='#555555', lw=0.9),
        ha='left'
    )

    ax.set_xlabel("Declared net worth W (£m, log scale)")
    ax.set_ylabel("Marginal WDT rate τ(W) (%)")
    ax.set_title(
        "Figure 5 - Marginal rate function τ(W)\n"
        f"k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}% (floor parameter), "
        f"$\\tau_m$ = {p['tau_m']*100:.0f}%, W_min = £{p['W_min']:.0f}m"
    )
    ax.set_xlim(p['W_min'], 10000)
    ax.set_ylim(0, p['tau_m'] * 100 * 1.1)
    ax.legend(loc='upper left')

    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                         '£200m', '£500m', '£1bn', '£2bn', '£5bn', '£10bn'],
                        rotation=45, ha='right', fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_5_rate_function_tau_w.png")


# ─────────────────────────────────────────────────────────────
# FIG 5.2a — C.1 heatmap
# ─────────────────────────────────────────────────────────────

def fig_5_2a_c1_heatmap(data: dict):
    print("  Generating fig 5.2a: C.1 heatmap...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_5_2a_c1_heatmap']

    G_VALS    = grids['g_vals']
    G_LABELS  = grids['g_labels']
    ALPHA_VALS = grids['alpha_vals']
    matrix = np.array(cd['matrix'])   # [alpha × g] in pp

    apply_style_nogrid()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)

    vmax = min(max(abs(matrix.min()), abs(matrix.max())), 25)
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    im   = ax.imshow(matrix, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)

    ax.set_xticks(range(len(G_VALS)))
    ax.set_xticklabels(G_LABELS, rotation=45, ha='right')
    ax.set_yticks(range(len(ALPHA_VALS)))
    ax.set_yticklabels([str(a) for a in ALPHA_VALS])
    ax.set_xlabel("Growth rate g")
    ax.set_ylabel("Declaration ratio α")
    ax.set_title(
        "Figure 5.2a - C.1 metric: (Net(α) − Net(1)) / TW(α)  [percentage points]\n"
        f"Red = pays more · Blue = pays less · "
        f"N = {p['N_demo']}, $V_0$ = £{p['V0_m']:.0f}m"
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("pp relative to honest declaration")

    for i in range(len(ALPHA_VALS)):
        for j in range(len(G_VALS)):
            val = matrix[i, j]
            text_col = 'white' if abs(val) > vmax * 0.6 else C_DARK
            ax.text(j, i, f"{val:.1f}",
                    ha='center', va='center', fontsize=7.5,
                    color=text_col, zorder=3)

    honest_idx = ALPHA_VALS.index(1.0)
    ax.add_patch(plt.Rectangle((-0.5, honest_idx - 0.5), len(G_VALS), 1,
                                fill=False, edgecolor=C_DARK, linewidth=1.5))

    plt.tight_layout()
    return _save(fig, "val_fig_5_2a_c1_tax_difference_heatmap.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1b — Declaration equilibrium cost curve
# ─────────────────────────────────────────────────────────────

def fig_7_1b_equilibrium_cost_curve(data: dict):
    print("  Generating fig 7.1b: declaration equilibrium cost curve...")
    p  = data['params']
    cd = data['charts']['fig_7_1b_equilibrium_cost_curve']

    alpha_fine  = cd['alpha_fine']
    g_scenarios = cd['g_scenarios']
    cost_by_g   = cd['cost_by_g']
    hist_cost   = cd['hist_cost']
    mean_g_hist = cd['mean_g_hist']

    g_colours = {0.059: '#f46d43', 0.084: '#d4ac0d', 0.1045: C_DARK, 0.139: '#4393c3'}

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    for g_val in g_scenarios:
        col = g_colours.get(g_val, '#888888')
        ax.plot(alpha_fine, cost_by_g[str(g_val)], color=col, linewidth=1.8,
                linestyle='-', label=f'g = {g_val*100:.1f}% (constant)')

    scen_year = data['meta']['scenario_start_year']
    N         = p['N_demo']
    ax.plot(alpha_fine, hist_cost, color='#7b2d8b', linewidth=2.0,
            linestyle='-.', label=f'{scen_year} hist. series (mean g = {mean_g_hist*100:.1f}%, N = {N})')

    ax.axhline(0, color=C_ANNOTATION, linewidth=0.8, linestyle='--')
    ax.axvline(1.0, color=C_ANNOTATION, linewidth=0.8, linestyle=':')
    ax.text(1.02, 18, 'α = 1.0\n(honest)', fontsize=8, color='#666666', va='top')
    ax.axvspan(0.5, 1.0, alpha=0.04, color='#d73027')
    ax.axvspan(1.0, 2.0, alpha=0.04, color='#4393c3')

    ax.set_ylim(bottom=-20, top=25)
    ax.set_xlabel("Declaration ratio α  (α < 1 = understatement, α > 1 = overstatement)")
    ax.set_ylabel("Net tax vs honest declaration (%)")
    ax.set_title(
        "Figure 7.1b - Declaration equilibrium: net tax cost relative to honest\n"
        f"N = {N}, $V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%"
    )
    ax.legend(loc='upper right', fontsize=8)
    ax.set_xlim(0.5, 2.0)

    plt.tight_layout()
    return _save(fig, "val_fig_7_1b_declaration_equilibrium_cost_curve.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.2a — C.8 TW gap by N
# ─────────────────────────────────────────────────────────────

def fig_7_2a_tw_gap_by_n(data: dict):
    print("  Generating fig 7.2a: C.8 TW gap by N (overlaid)...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_2a_tw_gap_by_n']

    N_ACTUAL_VALS = grids['n_actual_vals']
    alpha_under   = grids['alpha_under']
    alpha_over    = grids['alpha_over']

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)

    for alpha, col in zip(alpha_under, C_UNDER):
        ax.plot(N_ACTUAL_VALS, cd['const_under'][str(alpha)], color=col,
                linewidth=1.8, linestyle='-',  label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, cd['hist_under'][str(alpha)],  color=col,
                linewidth=1.4, linestyle='-.', alpha=0.8)

    for alpha, col in zip(alpha_over, C_OVER):
        ax.plot(N_ACTUAL_VALS, cd['const_over'][str(alpha)], color=col,
                linewidth=1.8, linestyle='--', label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, cd['hist_over'][str(alpha)],  color=col,
                linewidth=1.4, linestyle=':',  alpha=0.8)

    ax.axhline(0, color=C_HONEST, linewidth=1.0, linestyle='-', label='α = 1.0 (honest)')
    scen_N = p['N_demo']
    ax.axvline(scen_N, color=C_ANNOTATION, linewidth=0.8, linestyle=':')

    existing_ticks = sorted(set(list(ax.get_xticks()) + [scen_N]))
    ax.set_xticks(existing_ticks)
    tick_labels = [
        f'{int(t)}\n(N)' if t == scen_N else (str(int(t)) if t == int(t) else '')
        for t in ax.get_xticks()
    ]
    ax.set_xticklabels(tick_labels, fontsize=8)

    scen_year = data['meta']['scenario_start_year']
    style_handles = [
        Line2D([0], [0], color='#555555', lw=1.8, linestyle='-',
               label=f'Solid = constant g ({p["g"]*100:.2f}%)'),
        Line2D([0], [0], color='#555555', lw=1.4, linestyle='-.',
               label=f'Dash-dot = {scen_year} hist. series (understaters)'),
        Line2D([0], [0], color='#555555', lw=1.8, linestyle='--',
               label=f'Dashed = constant g ({p["g"]*100:.2f}%) (overstaters)'),
        Line2D([0], [0], color='#555555', lw=1.4, linestyle=':',
               label=f'Dotted = {scen_year} hist. series (overstaters)'),
    ]
    h1, l1 = ax.get_legend_handles_labels()
    ax.legend(handles=h1 + style_handles, loc='lower left', ncol=2, fontsize=7.5)

    ax.set_xlabel("Holding period N (years)")
    ax.set_ylabel("TW vs honest declaration (%)")
    ax.set_title(
        "Figure 7.2a - Terminal Net Worth Gap vs Honest, by holding period\n"
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%"
    )
    ax.set_xlim(N_ACTUAL_VALS[0], N_ACTUAL_VALS[-1])

    plt.tight_layout()
    return _save(fig, "val_fig_7_2a_c8_tw_gap_by_n.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.2b — Saturation reversal boundary (understaters)
# ─────────────────────────────────────────────────────────────

def fig_7_2b_saturation_reversal(data: dict):
    print("  Generating fig 7.2b: saturation reversal boundary...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_2b_saturation_reversal']

    alpha_under = grids['alpha_under']
    g_pct       = cd['g_pct']
    c1_curves   = {float(k): v for k, v in cd['c1_curves'].items()}

    # Derive inflection / plateau from the stored curves
    cutoff_idx = int(50 / 0.1)   # index at g = 50%
    inflection_g  = {}
    plateau_onset = {}
    plateau_height = {}
    for alpha in alpha_under:
        vals  = c1_curves[alpha]
        deriv = [vals[i+1] - vals[i] for i in range(len(vals) - 1)]
        peak_idx = max(range(len(deriv)), key=lambda i: deriv[i])
        inflection_g[alpha] = g_pct[peak_idx]
        onset = None
        for i in range(peak_idx, min(len(deriv), 400)):
            if deriv[i] < 0.05:
                onset = g_pct[i]
                break
        plateau_onset[alpha]  = onset if onset is not None else 40.0
        plateau_height[alpha] = max(vals)

    mean_inflection = sum(inflection_g[a]  for a in alpha_under) / len(alpha_under)
    mean_plateau    = sum(plateau_onset[a] for a in alpha_under) / len(alpha_under)
    y_max = max(max(c1_curves[a][:cutoff_idx]) for a in alpha_under)

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ax.set_xlim(0, 50)

    ax.axvspan(mean_plateau, 50, alpha=0.08, color=C_ANNOTATION, zorder=0,
               label=f'Plateau zone (g > {mean_plateau:.0f}%)')
    ax.text(mean_plateau + 1, y_max * 1.05, f'Plateau\n(g ≥ {mean_plateau:.0f}%)',
            fontsize=7.5, color='#555555', va='top')

    ax.axvline(mean_inflection, color='#333333', linewidth=1.1, linestyle='--', zorder=3,
               label=f'Inflection g ≈ {mean_inflection:.1f}%')
    ax.text(mean_inflection + 1, 2, f'Inflection\n≈ {mean_inflection:.1f}%',
            fontsize=7.5, color='#333333', va='bottom')

    for alpha, col in zip(alpha_under, C_UNDER):
        ax.plot(g_pct, c1_curves[alpha], color=col, linewidth=2.0)
        ph       = plateau_height[alpha]
        x_label  = ax.get_xlim()[1] * 0.82
        ax.text(x_label, ph,
                f"α = {alpha}  (plateau ≈ {ph:.0f}%)",
                color=col, fontsize=8, va='center', ha='left',
                fontweight='bold' if alpha == 0.1 else 'normal')

    ax.axhline(0, color=C_DARK, linewidth=0.8, linestyle=':')
    ax.set_xlabel("Growth rate g (%)")
    ax.set_ylabel("Excess tax burden (understater vs honest)\nas % of understater's TW(α)")
    ax.set_title(
        f"Figure 7.2b - Understater penalty structure: inflection and plateau (N = {p['N_demo']}, $V_0$ = £{p['V0_m']:.0f}m)\n"
        f"k = {p['k']}"
    )
    ax.set_ylim(-5, y_max * 1.12)

    legend_handles = [
        Line2D([0], [0], color='#333333', lw=1.1, linestyle='--',
               label=f'Inflection ≈ {mean_inflection:.1f}%'),
        Patch(facecolor=C_ANNOTATION, alpha=0.15,
              label=f'Plateau zone g ≥ {mean_plateau:.0f}%'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_7_2b_saturation_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.2c — Overstatement reversal boundary
# ─────────────────────────────────────────────────────────────

def fig_7_2c_overstatement_reversal(data: dict):
    print("  Generating fig 7.2c: overstatement reversal boundary...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_2c_overstatement_reversal']

    alpha_over  = grids['alpha_over']
    g_pct       = cd['g_pct']
    c1_curves   = {float(k): v for k, v in cd['c1_curves'].items()}

    # First-reversal g values (first g where C.1 > 0)
    first_rev = {}
    for alpha in alpha_over:
        vals = c1_curves[alpha]
        for i, (g, v) in enumerate(zip(g_pct, vals)):
            if v > 0:
                first_rev[alpha] = g
                break
        else:
            first_rev[alpha] = None

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)

    for alpha, col in zip(alpha_over, C_OVER):
        ax.plot(g_pct, c1_curves[alpha], color=col, linewidth=1.8, label=f"α = {alpha}")

    # α=1.2 nearest-approach annotation
    vals_12     = c1_curves[1.2]
    nearest_idx = max(range(len(vals_12)), key=lambda i: vals_12[i])
    nearest_g   = g_pct[nearest_idx]
    nearest_val = vals_12[nearest_idx]
    if nearest_val < 0:
        ax.annotate(
            f"α=1.2 peak ≈ {nearest_val:.1f}pp\n(never crosses zero)",
            xy=(nearest_g, nearest_val),
            xytext=(nearest_g + 3, nearest_val + 2.5),
            fontsize=7.5, color=C_OVER[0],
            arrowprops=dict(arrowstyle='->', color=C_OVER[0], lw=0.8)
        )

    y_lo = ax.get_ylim()[0]
    for idx, (alpha, col) in enumerate(zip(alpha_over, C_OVER)):
        t = first_rev[alpha]
        if t is not None:
            ax.axvline(t, color=col, linewidth=0.8, linestyle=':', alpha=0.6)
            ax.text(t + 0.3, y_lo * (0.95 - idx * 0.15),
                    f'{t:.1f}%', fontsize=7.5, color=col, va='bottom')

    ax.axhline(0, color=C_ANNOTATION, linewidth=0.8, linestyle='--',
               label='zero (honest baseline)')
    ax.axvline(p['g'] * 100, color=C_DARK, linewidth=1.0, linestyle=':',
               label=f"hist. mean g = {p['g']*100:.1f}%")

    ax.set_xlabel("Growth rate g (%)")
    ax.set_ylabel("C.1 metric (pp)")
    ax.set_title(
        f"Figure 7.3 - Overstater C.1 by growth rate\n"
        f"N = {p['N_demo']}, $V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%"
    )
    ax.set_xlim(0, 40)
    ax.legend(fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_7_3_overstatement_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1a — Overstatement coherence
# ─────────────────────────────────────────────────────────────

def fig_7_1a_overstatement_coherence(data: dict):
    print("  Generating fig 7.1a: overstatement coherence...")
    p   = data['params']
    cd  = data['charts']['fig_7_1a_overstatement_coherence']

    alphas_grid  = cd['alphas_grid']
    g_grid       = cd['g_grid']
    c1_mat       = np.array(cd['c1_matrix'])    # [alpha × g] in pp
    n_right      = cd['n_right']
    net_diffs    = {float(k): v for k, v in cd['net_diffs'].items()}
    hist_mean    = cd['hist_mean']
    N_ssm        = cd['N_ssm']
    g_pct_grid   = [g * 100 for g in g_grid]
    over_alphas  = [1.2, 1.5, 1.8, 2.0]

    # Compute zero-crossings from right-panel net diffs
    crossings = {}
    for alpha in over_alphas:
        diffs = net_diffs[alpha]
        cross = []
        for k in range(len(diffs) - 1):
            if diffs[k] * diffs[k + 1] < 0:
                n_cross = n_right[k] + (0 - diffs[k]) / (diffs[k + 1] - diffs[k])
                cross.append(n_cross)
        crossings[alpha] = cross

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)

    # ── LEFT: C.1 surface heatmap ────────────────────────────
    vmax = 10.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    ax1.imshow(
        c1_mat, origin='lower', aspect='auto', cmap='RdBu_r', norm=norm,
        extent=[g_pct_grid[0], g_pct_grid[-1], alphas_grid[0], alphas_grid[-1]],
        zorder=1,
    )
    CS = ax1.contour(g_pct_grid, alphas_grid, c1_mat,
                     levels=[0.0], colors=[C_DARK], linewidths=1.8, zorder=4)
    ax1.clabel(CS, levels=[0.0], fmt={0.0: 'C.1 = 0'}, fontsize=8, inline=True)
    CS_band = ax1.contour(g_pct_grid, alphas_grid, c1_mat,
                          levels=[-1.0, 1.0], colors=[C_ANNOTATION, C_ANNOTATION],
                          linewidths=1.0, linestyles='--', zorder=3, alpha=0.7)
    ax1.clabel(CS_band, levels=[-1.0, 1.0],
               fmt={-1.0: '−1pp', 1.0: '+1pp'}, fontsize=7, inline=True)
    ax1.axvline(hist_mean * 100, color='#333333', linewidth=1.4, linestyle='--', zorder=5,
                label=f'Hist. mean g = {hist_mean*100:.1f}%')
    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'),
                        ax=ax1, fraction=0.035, pad=0.03, shrink=0.85)
    cbar.set_label('C.1 (pp)', fontsize=8)
    ax1.set_xlabel("Actual growth rate g (%)", fontsize=10)
    ax1.set_ylabel("Declaration ratio α", fontsize=10)
    ax1.set_title("Advantage landscape: C.1 by (g_actual, α)", fontsize=10)
    ax1.set_xlim(0, 40)
    ax1.set_ylim(0.1, 2.0)
    ax1.legend(loc='lower right', fontsize=8.5, frameon=True, framealpha=0.9)

    # ── RIGHT: Net tax diff vs N ──────────────────────────────
    ax2.grid(True)
    Y_CLIP = -3.0; Y_HI = 40.0
    ax2.set_ylim(Y_CLIP, Y_HI)
    ax2.axhline(0, color='#333333', linewidth=1.2, linestyle='-', zorder=3,
                label='α = 1.0 honest (zero line)')
    ax2.axhspan(Y_CLIP, 0,    alpha=0.04, color='#2166ac', zorder=0)
    ax2.axhspan(0,      Y_HI, alpha=0.04, color='#d73027', zorder=0)
    for alpha, col in zip(over_alphas, C_OVER_LIGHT):
        ax2.plot(n_right, net_diffs[alpha], color=col, linewidth=2.0, label=f'α = {alpha}')
    for idx, (alpha, col) in enumerate(zip(over_alphas, C_OVER_LIGHT)):
        for n_cross in crossings[alpha]:
            ax2.axvline(n_cross, color=col, linewidth=0.8, linestyle=':', alpha=0.6)
            ax2.text(n_cross + 0.3, Y_HI * (0.55 - idx * 0.07),
                     f'α={alpha}, N≈{n_cross:.0f}', fontsize=7.5, color=col, va='top')
    ax2.axvline(N_ssm, color='#555555', linewidth=1.0, linestyle='--', zorder=2)
    ax2.text(N_ssm + 0.4, Y_CLIP + 0.5, f'N={N_ssm}\n(RATES ref)', fontsize=7.5,
             color='#555555', va='bottom')
    ax2.set_xlabel("Holding period N (years)", fontsize=10)
    ax2.set_ylabel("Net(α) − Net(honest)  [£m]", fontsize=9)
    ax2.set_xlim(5, 60)
    ax2.set_title(
        f"Advantage erosion: net tax diff vs holding period N\n"
        f"g = hist. mean ({hist_mean*100:.1f}%) · $V_0$ = £{p['V0_m']:.0f}m",
        fontsize=10
    )
    ax2.legend(loc='upper left', fontsize=8.5, frameon=True, framealpha=0.9)

    cross_strs = ', '.join(
        f'α={a}: N≈{crossings[a][0]:.0f}'
        for a in over_alphas if crossings[a]
    )
    fig.suptitle(
        "Figure 7.1a - Overstatement: the advantage is real but narrow\n"
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%\n"
        f"Zero crossings: {cross_strs if cross_strs else 'none in range'}",
        fontsize=10, y=1.01
    )

    plt.tight_layout()
    return _save(fig, "val_fig_7_1a_overstatement_coherence.png")


# ─────────────────────────────────────────────────────────────
# FIG 5.2b — TW advantage decomposition
# ─────────────────────────────────────────────────────────────

def fig_5_2b_tw_decomposition(data: dict):
    print("  Generating fig 5.2b: TW advantage decomposition...")
    p   = data['params']
    cd  = data['charts']['fig_5_2b_tw_decomposition']

    alpha_x = np.array(cd['alpha_over_fine'])
    g_decomp = np.array(cd['g_decomp'])
    wsd_arr = np.array(cd['wsd'])
    rd_arr  = np.array(cd['rd'])
    sd_arr  = np.array(cd['sd'])
    tw_arr  = np.array(cd['tw'])
    ep_arr  = np.array(cd['ep'])
    f_matrix = np.array(cd['f_matrix'])   # [alpha × g]
    hist_mean = p['g']
    N         = p['N_demo']

    stack_err = np.max(np.abs((wsd_arr - rd_arr - sd_arr) - tw_arr))
    if stack_err > 0.01:
        print(f"    WARNING: fig08 left-panel identity error = {stack_err:.4f}pp")

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)

    # LEFT: stacked decomposition
    ax1.grid(True, zorder=0)
    ax1.axhline(0, color='#555555', linewidth=0.9, zorder=2)
    ax1.fill_between(alpha_x, 0, -rd_arr,  color='#4393c3', alpha=0.55, label='Sell-year refund benefit')
    ax1.fill_between(alpha_x, 0,  wsd_arr, color='#d73027', alpha=0.55, label='f_N erosion cost')
    ax1.fill_between(alpha_x, wsd_arr, wsd_arr - sd_arr,
                     color='#f46d43', alpha=0.55, label='Post-sale damping cost')
    ax1.plot(alpha_x, tw_arr, color=C_DARK, linewidth=2.2, zorder=5, label='Net TW advantage')
    ax1.plot(alpha_x, ep_arr, color='#6a3d9a', linewidth=1.3, linestyle=':', zorder=4,
             label='Excess periodic tax (informational)')
    for k in range(len(tw_arr) - 1):
        if tw_arr[k] * tw_arr[k + 1] < 0:
            a_cross = (alpha_x[k]
                       + (0 - tw_arr[k]) / (tw_arr[k + 1] - tw_arr[k])
                       * (alpha_x[k + 1] - alpha_x[k]))
            ax1.axvline(a_cross, color='#333333', linewidth=1.0, linestyle='--', zorder=4)
            ax1.text(a_cross + 0.01, tw_arr.max() * 0.8,
                     f'TW adv = 0\na~{a_cross:.2f}', fontsize=7.5, color='#333333')
    ax1.set_xlabel("Declaration ratio α", fontsize=10)
    ax1.set_ylabel("As % of honest TW_settled", fontsize=10)
    ax1.set_title(
        f"Left: TW advantage — corrected decomposition\n"
        f"g = {hist_mean*100:.1f}%  ·  N = {N}  ·  V₀ = £{p['V0_m']:.0f}m",
        fontsize=9.5
    )
    ax1.set_xlim(1.0, 2.0)
    ax1.legend(loc='upper left', fontsize=8)

    # RIGHT: f_N ratio heatmap
    g_pct = g_decomp * 100
    norm  = mcolors.Normalize(vmin=f_matrix.min(), vmax=1.0)
    im = ax2.imshow(f_matrix, origin='lower', aspect='auto', cmap='Blues_r', norm=norm,
                    extent=[g_pct[0], g_pct[-1], alpha_x[0], alpha_x[-1]], zorder=1)
    CS95 = ax2.contour(g_pct, alpha_x, f_matrix, levels=[0.95],
                       colors=['#d73027'], linewidths=1.6, zorder=4)
    ax2.clabel(CS95, fmt={0.95: 'f ratio = 0.95'}, fontsize=8, inline=True)
    CS90 = ax2.contour(g_pct, alpha_x, f_matrix, levels=[0.90],
                       colors=['#7f0000'], linewidths=1.4, linestyles='--', zorder=4)
    ax2.clabel(CS90, fmt={0.90: 'f ratio = 0.90'}, fontsize=8, inline=True)
    ax2.axvline(hist_mean * 100, color='#333333', linewidth=1.4, linestyle='--', zorder=5,
                label=f'g = hist. mean ({hist_mean*100:.1f}%)')
    cbar = fig.colorbar(im, ax=ax2, fraction=0.035, pad=0.03, shrink=0.85)
    cbar.set_label('f_N(alpha) / f_N(1)', fontsize=8)
    ax2.set_xlabel("Actual growth rate g (%)", fontsize=10)
    ax2.set_ylabel("Declaration ratio (alpha)", fontsize=10)
    ax2.set_title("Right: Retained equity fraction ratio f_N(alpha) / f_N(1)", fontsize=10)
    ax2.legend(loc='upper left', fontsize=8, framealpha=0.9)

    fig.suptitle("Figure 5.2b - Overstater TW advantage: mechanism and dilution cost",
                 fontsize=9.5, y=1.02)
    plt.tight_layout()
    return _save(fig, "val_fig_5_2b_tw_decomposition.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1c — TW advantage across (g, N) space
# ─────────────────────────────────────────────────────────────

def fig_7_1c_tw_advantage_gN_surface(data: dict):
    print("  Generating fig 7.1c: TW advantage (g, N) surface...")
    p   = data['params']
    cd  = data['charts']['fig_7_1c_tw_advantage_gN_surface']

    g_surf  = cd['g_surf']
    n_surf  = cd['n_surf']
    g_pct   = [g * 100 for g in g_surf]
    hist_mean = p['g']
    canon_N   = p['N']
    over_alphas = [1.2, 1.5, 1.8, 2.0]

    apply_style_nogrid()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD_XL)
    axes = axes.flatten()

    for ax, alpha, col in zip(axes, over_alphas, C_OVER_LIGHT):
        mat  = np.array(cd['surfaces'][str(alpha)])   # [g × N]
        vmax = float(np.percentile(mat, 98))
        norm = mcolors.Normalize(vmin=0.0, vmax=vmax)

        im = ax.imshow(mat, origin='lower', aspect='auto', cmap='Blues', norm=norm,
                       extent=[n_surf[0], n_surf[-1], g_pct[0], g_pct[-1]], zorder=1)

        contour_levels = [l for l in [2, 4, 6, 8, 10, 12] if 0 < l < vmax]
        if contour_levels:
            CS = ax.contour(n_surf, g_pct, mat, levels=contour_levels,
                            colors='white', linewidths=0.9, zorder=4, alpha=0.85)
            ax.clabel(CS, fmt='%d%%', fontsize=7.5, inline=True)

        ax.axhline(hist_mean * 100, color='#d73027', linewidth=1.4, linestyle='--', zorder=5,
                   label=f'hist. mean g = {hist_mean*100:.1f}%')
        ax.axvline(canon_N, color='#d73027', linewidth=1.4, linestyle=':', zorder=5,
                   label=f'canonical N = {canon_N}')

        peak_idx  = np.unravel_index(np.argmax(mat), mat.shape)
        peak_g    = g_pct[peak_idx[0]]
        peak_N    = int(n_surf[peak_idx[1]])
        peak_val  = mat[peak_idx]
        ax.plot(peak_N, peak_g, marker='*', markersize=12, color='#ff7f00',
                zorder=7, clip_on=False,
                label=f'Peak: {peak_val:.1f}pp  g={peak_g:.1f}%  N={peak_N}')

        g_cidx    = int(np.argmin(np.abs(np.array(g_surf) - hist_mean)))
        N_cidx    = int(np.argmin(np.abs(np.array(n_surf) - canon_N)))
        canon_val = mat[g_cidx, N_cidx]
        ax.plot(canon_N, hist_mean * 100, marker='o', markersize=7,
                color='#d73027', zorder=6, clip_on=False)
        ax.annotate(f'{canon_val:.1f}pp',
                    xy=(canon_N, hist_mean * 100),
                    xytext=(canon_N + 3, hist_mean * 100 + 1.5),
                    fontsize=7.5, color='#d73027',
                    arrowprops=dict(arrowstyle='->', color='#d73027', lw=0.8))

        cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, shrink=0.85)
        cbar.set_label('TW advantage vs honest (%)', fontsize=8)
        ax.set_xlabel("Holding period N (years)", fontsize=9)
        ax.set_ylabel("Actual growth rate g (%)", fontsize=9)
        ax.set_title(f"α = {alpha}", fontsize=9.5)
        ax.set_xlim(n_surf[0], n_surf[-1])
        ax.set_ylim(g_pct[0], g_pct[-1])
        ax.legend(loc='upper right', fontsize=7.5, framealpha=0.92, frameon=True)

    fig.suptitle(
        "Figure 7.1c - TW advantage of overstatement across (g, N) space\n"
        f"$V_0$ = £{p['V0_m']:.0f}m  ·  k = {p['k']}",
        fontsize=9.5, y=1.02,
    )
    plt.tight_layout()
    return _save(fig, "val_fig_7_1c_tw_advantage_gN_surface.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1d — C.12 NPV heatmap
# ─────────────────────────────────────────────────────────────

def fig_7_1d_c1_vs_c12_heatmap(data: dict):
    print("  Generating fig 7.1d: C.12 heatmap...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_1d_c12_heatmap']

    G_VALS    = grids['g_vals']
    G_LABELS  = grids['g_labels']
    ALPHA_VALS = grids['alpha_vals']
    c12_mat   = np.array(cd['matrix'])
    rho       = cd['rho']

    vmax = min(max(abs(c12_mat.min()), abs(c12_mat.max())), 25)
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    apply_style_nogrid()
    fig, ax = plt.subplots(1, 1, figsize=FIG_SINGLE_W)

    im = ax.imshow(c12_mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
    ax.set_xticks(range(len(G_VALS)))
    ax.set_xticklabels(G_LABELS, rotation=45, ha='right')
    ax.set_yticks(range(len(ALPHA_VALS)))
    ax.set_yticklabels([str(a) for a in ALPHA_VALS])
    ax.set_xlabel("Growth rate g")
    ax.set_ylabel("Declaration ratio α")
    ax.set_title(
        f"C.12 — NPV-adjusted tax difference: (NPV_tax(α) − NPV_tax(1)) / TW_settled(1)  [pp]\n"
        f"ρ = {rho*100:.0f}%,  N = {p['N_demo']},  $V_0$ = £{p['V0_m']:.0f}m,  k = {p['k']}"
    )

    honest_idx = ALPHA_VALS.index(1.0)
    ax.add_patch(plt.Rectangle((-0.5, honest_idx - 0.5), len(G_VALS), 1,
                                fill=False, edgecolor=C_DARK, linewidth=1.5, zorder=5))

    for i in range(len(ALPHA_VALS)):
        for j in range(len(G_VALS)):
            val = c12_mat[i, j]
            text_col = 'white' if abs(val) > vmax * 0.6 else C_DARK
            ax.text(j, i, f"{val:.1f}", ha='center', va='center',
                    fontsize=7.5, color=text_col, zorder=3)

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("pp relative to honest declaration\n", fontsize=8)

    fig.suptitle(
        f"Figure 7.1d - NPV-adjusted tax difference (ρ = {rho*100:.0f}%)",
        fontsize=10,
    )
    plt.tight_layout()
    return _save(fig, "val_fig_7_1d_c1_vs_c12_nominal_vs_npv.png")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("5_4_VAL_charts.py — loading val_data.json...")
    data = load_val_data()
    print(f"Data loaded. Generated: {data['meta']['generated']}")
    p = data['params']
    print(f"Parameters: k={p['k']}, N={p['N']}, N_demo={p['N_demo']}, "
          f"g={p['g']:.4f}, V0=£{p['V0_m']:.0f}m")

    ensure_dir(_OUT)

    print(f"\nGenerating VAL figures → {_OUT}")
    fig_5_rate_function(data)
    fig_5_2a_c1_heatmap(data)
    fig_7_1b_equilibrium_cost_curve(data)
    fig_7_2a_tw_gap_by_n(data)
    fig_7_2b_saturation_reversal(data)
    fig_7_2c_overstatement_reversal(data)
    fig_7_1a_overstatement_coherence(data)
    fig_5_2b_tw_decomposition(data)
    fig_7_1c_tw_advantage_gN_surface(data)
    fig_7_1d_c1_vs_c12_heatmap(data)

    print("\nAll figures written.")


if __name__ == '__main__':
    main()
