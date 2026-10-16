"""
VAL Output Script D — Figures (v5 — data-driven, N-consistent, Net | TW side by side)
=====================================================================================
All simulation data is loaded from OUTPUTS/VAL/val_data.json
(produced by val_core.py v2+). No wdt_core simulation calls here.

v5 changes vs v4
  * Every heatmap / curve figure shows BOTH metrics side by side, both divided by
    the same denominator, TW_settled(1) (honest terminal wealth):
        Net  = (Net(a) - Net(1)) / TW(1)      + = pays more
        TW   = -(TW(a) - TW(1)) / TW(1)       + = retains less   ("TW cost")
    Same sign convention, same colour scale: red = worse for the declarer.
  * Fig 7.1d adds a third panel, PV of true-value payments (corrected C.12).
  * The canonical holding period is N_val (= 30). The SSM fill year N_fill (19)
    appears only as a labelled reference line in Fig 7.1a.
  * Every figure asserts that the data N stamp equals N_val.

To regenerate output:
    python val_core.py          # run simulations
    python 5_4_VAL_charts.py   # render figures
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

NET_LABEL = "Net tax vs honest  (Net(α) − Net(1)) / TW(1)   [+ = pays more]"
TW_LABEL  = "TW cost vs honest  −(TW(α) − TW(1)) / TW(1)   [+ = retains less]"
PV_LABEL  = "PV of true-value payments vs honest / TW(1)   [+ = pays more]"


def _save(fig, name):
    return save_fig(fig, _OUT / name)


def _n_val(p):
    return p.get('N_val', p['N_demo'])


def _check_stamp(cd, p, name):
    """Fail loudly if a figure's data was produced at a different N."""
    n = cd.get('N')
    if isinstance(n, int) and n != _n_val(p):
        raise SystemExit(f"{name}: data N stamp {n} != N_val {_n_val(p)}. Re-run val_core.py.")


def _heat(ax, mat, g_labels, alphas, norm, title, cmap='RdBu_r', fs=7.0):
    """Annotated (alpha x g) heatmap with the honest row boxed."""
    im = ax.imshow(mat, aspect='auto', cmap=cmap, norm=norm, zorder=2)
    ax.set_xticks(range(len(g_labels)))
    ax.set_xticklabels(g_labels, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(alphas)))
    ax.set_yticklabels([str(a) for a in alphas], fontsize=8)
    ax.set_xlabel("Growth rate g")
    ax.set_title(title, fontsize=8.5)
    vmax = norm.vmax
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            ax.text(j, i, f"{v:.1f}", ha='center', va='center', fontsize=fs,
                    color='white' if abs(v) > vmax * 0.6 else C_DARK, zorder=3)
    hi = alphas.index(1.0)
    ax.add_patch(plt.Rectangle((-0.5, hi - 0.5), mat.shape[1], 1,
                               fill=False, edgecolor=C_DARK, linewidth=1.5, zorder=5))
    return im


def _shared_norm(*mats, cap=25.0):
    vmax = min(max(float(np.max(np.abs(m))) for m in mats), cap)
    return mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)


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
# FIG 5.2a — C.1 heatmap: Net | TW side by side
# ─────────────────────────────────────────────────────────────

def fig_5_2a_c1_heatmap(data: dict):
    print("  Generating fig 5.2a: C.1 heatmaps (Net | TW cost)...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_5_2a_c1_heatmap']
    _check_stamp(cd, p, 'fig 5.2a')

    G_LABELS   = grids['g_labels']
    ALPHA_VALS = grids['alpha_vals']
    m_net = np.array(cd['matrix_net'])
    m_tw  = np.array(cd['matrix_tw_cost'])
    norm  = _shared_norm(m_net, m_tw)

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6), sharey=True)
    _heat(ax1, m_net, G_LABELS, ALPHA_VALS, norm, "Left: " + NET_LABEL)
    im = _heat(ax2, m_tw, G_LABELS, ALPHA_VALS, norm, "Right: " + TW_LABEL)
    ax1.set_ylabel("Declaration ratio α")
    cbar = fig.colorbar(im, ax=[ax1, ax2], fraction=0.02, pad=0.02)
    cbar.set_label("pp of honest TW(1)   (red = worse for declarer)")

    fig.suptitle(
        "Figure 5.2a - Cost of mis-declaration: net tax paid and terminal wealth, same denominator\n"
        f"Common scale · N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']}",
        fontsize=10)
    return _save(fig, "val_fig_5_2a_c1_tax_difference_heatmap.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1b — Declaration equilibrium cost curves: Net | TW
# ─────────────────────────────────────────────────────────────

def fig_7_1b_equilibrium_cost_curve(data: dict):
    print("  Generating fig 7.1b: declaration equilibrium cost curves (Net | TW)...")
    p  = data['params']
    cd = data['charts']['fig_7_1b_equilibrium_cost_curve']
    _check_stamp(cd, p, 'fig 7.1b')

    alpha_fine  = cd['alpha_fine']
    g_scenarios = cd['g_scenarios']
    net_by_g    = cd.get('net_pct_by_g', cd['cost_by_g'])
    tw_by_g     = cd['tw_cost_by_g']
    hist_net    = cd.get('hist_net_pct', cd['hist_cost'])
    hist_tw     = cd['hist_tw_cost']
    mean_g_hist = cd['mean_g_hist']
    N           = _n_val(p)
    scen_year   = data['meta']['scenario_start_year']

    g_colours = {0.059: '#f46d43', 0.084: '#d4ac0d', 0.1045: C_DARK, 0.139: '#4393c3'}

    apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.4), sharey=True)
    for ax, by_g, hist, ttl in ((axes[0], net_by_g, hist_net, "Left: " + NET_LABEL),
                                (axes[1], tw_by_g,  hist_tw,  "Right: " + TW_LABEL)):
        for g_val in g_scenarios:
            ax.plot(alpha_fine, by_g[str(g_val)], color=g_colours.get(g_val, '#888888'),
                    linewidth=1.8, label=f'g = {g_val*100:.1f}% (constant)')
        ax.plot(alpha_fine, hist, color='#7b2d8b', linewidth=2.0, linestyle='-.',
                label=f'{scen_year} hist. series (mean g = {mean_g_hist*100:.1f}%)')
        ax.axhline(0, color=C_ANNOTATION, linewidth=0.8, linestyle='--')
        ax.axvline(1.0, color=C_ANNOTATION, linewidth=0.8, linestyle=':')
        ax.axvspan(0.5, 1.0, alpha=0.04, color='#d73027')
        ax.axvspan(1.0, 2.0, alpha=0.04, color='#4393c3')
        ax.set_xlim(0.5, 2.0)
        ax.set_xlabel("Declaration ratio α  (α < 1 = understatement, α > 1 = overstatement)")
        ax.set_title(ttl, fontsize=8.5)
    axes[0].set_ylabel("% of honest TW(1)   (+ = worse for declarer)")
    lo = min(min(min(v) for v in net_by_g.values()), min(min(v) for v in tw_by_g.values()), -5)
    hi = max(max(max(v) for v in net_by_g.values()), max(max(v) for v in tw_by_g.values()))
    axes[0].set_ylim(max(lo * 1.1, -60), min(hi * 1.1, 60))
    axes[0].legend(loc='upper right', fontsize=8)

    fig.suptitle(
        "Figure 7.1b - Declaration equilibrium: net tax and terminal wealth relative to honest\n"
        f"N = {N}, $V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%",
        fontsize=10)
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
    scen_N = _n_val(p)
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
    ax.set_ylabel("TW(α) vs honest TW(1)  (%)   [+ = retains more]")
    ax.set_title(
        "Figure 7.2a - Terminal Net Worth Gap vs Honest, by holding period\n"
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%"
    )
    ax.set_xlim(N_ACTUAL_VALS[0], N_ACTUAL_VALS[-1])

    plt.tight_layout()
    return _save(fig, "val_fig_7_2a_c8_tw_gap_by_n.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.2b — Saturation reversal boundary (understaters): Net | TW
# ─────────────────────────────────────────────────────────────

def fig_7_2b_saturation_reversal(data: dict):
    print("  Generating fig 7.2b: saturation reversal boundary (Net | TW)...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_2b_saturation_reversal']
    _check_stamp(cd, p, 'fig 7.2b')

    alpha_under = grids['alpha_under']
    g_pct       = cd['g_pct']
    net_curves  = {float(k): v for k, v in cd['c1_curves'].items()}
    tw_curves   = {float(k): v for k, v in cd['tw_cost_curves'].items()}

    # Derive inflection / plateau from the stored NET curves
    cutoff_idx = int(50 / 0.1)   # index at g = 50%
    inflection_g, plateau_onset, plateau_height = {}, {}, {}
    for alpha in alpha_under:
        vals  = net_curves[alpha]
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
    y_max_n = max(max(net_curves[a][:cutoff_idx]) for a in alpha_under)
    y_max_t = max(max(tw_curves[a][:cutoff_idx]) for a in alpha_under)
    y_min_t = min(min(tw_curves[a][:cutoff_idx]) for a in alpha_under)
    y_max   = max(y_max_n, y_max_t)

    apply_style()
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6), sharey=True)

    for a_ax in (ax, ax2):
        a_ax.set_xlim(0, 50)
        a_ax.axhline(0, color=C_DARK, linewidth=0.8, linestyle=':')
        a_ax.set_xlabel("Growth rate g (%)")

    ax.axvspan(mean_plateau, 50, alpha=0.08, color=C_ANNOTATION, zorder=0)
    ax.axvline(mean_inflection, color='#333333', linewidth=1.1, linestyle='--', zorder=3)
    for alpha, col in zip(alpha_under, C_UNDER):
        ax.plot(g_pct, net_curves[alpha], color=col, linewidth=2.0)
        ph = plateau_height[alpha]
        ax.text(41, ph, f"α = {alpha} (peak ≈ {ph:.0f}%)", color=col, fontsize=7.5,
                va='center', ha='left', fontweight='bold' if alpha == 0.1 else 'normal')
    ax.legend(handles=[
        Line2D([0], [0], color='#333333', lw=1.1, linestyle='--',
               label=f'Mean net-curve inflection ≈ {mean_inflection:.1f}%'),
        Patch(facecolor=C_ANNOTATION, alpha=0.15,
              label=f'Net-curve plateau zone g ≥ {mean_plateau:.0f}%')],
        loc='upper left', fontsize=8)
    ax.set_ylabel("% of honest TW(1)   (+ = worse for declarer)")
    ax.set_title("Left: " + NET_LABEL, fontsize=8.5)

    for alpha, col in zip(alpha_under, C_UNDER):
        ax2.plot(g_pct, tw_curves[alpha], color=col, linewidth=2.0, label=f"α = {alpha}")
    ax2.legend(loc='upper left', fontsize=8)
    ax2.set_title("Right: " + TW_LABEL, fontsize=8.5)

    span = y_max - min(y_min_t, 0)
    ax.set_ylim(min(y_min_t, 0) - 0.05 * span, y_max + 0.12 * span)

    fig.suptitle(
        f"Figure 7.2b - Understater penalty structure (N = {_n_val(p)}, "
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']})\n"
        "Both panels divided by honest TW(1). The metrics diverge at high g: for the deepest "
        "understaters the net-tax penalty stays positive while the TW cost turns negative (retains more).",
        fontsize=9.5)
    plt.tight_layout()
    return _save(fig, "val_fig_7_2b_saturation_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.2c — Overstatement reversal boundary: Net | TW
# ─────────────────────────────────────────────────────────────

def fig_7_2c_overstatement_reversal(data: dict):
    print("  Generating fig 7.2c: overstatement reversal boundary (Net | TW)...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_2c_overstatement_reversal']
    _check_stamp(cd, p, 'fig 7.2c')

    alpha_over = grids['alpha_over']
    g_pct      = cd['g_pct']
    net_curves = {float(k): v for k, v in cd['c1_curves'].items()}
    tw_curves  = {float(k): v for k, v in cd['tw_cost_curves'].items()}

    first_rev = {}
    for alpha in alpha_over:
        first_rev[alpha] = next((g for g, v in zip(g_pct, net_curves[alpha]) if v > 0), None)

    apply_style()
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.4))

    for alpha, col in zip(alpha_over, C_OVER):
        ax.plot(g_pct, net_curves[alpha], color=col, linewidth=1.8, label=f"α = {alpha}")
        ax2.plot(g_pct, tw_curves[alpha], color=col, linewidth=1.8, label=f"α = {alpha}")

    vals_12 = net_curves[alpha_over[0]]
    nearest_idx = max(range(len(vals_12)), key=lambda i: vals_12[i])
    if vals_12[nearest_idx] < 0:
        ax.annotate(
            f"α={alpha_over[0]} peak ≈ {vals_12[nearest_idx]:.1f}pp\n(never crosses zero)",
            xy=(g_pct[nearest_idx], vals_12[nearest_idx]),
            xytext=(g_pct[nearest_idx] + 3, vals_12[nearest_idx] + 2.5),
            fontsize=7.5, color=C_OVER[0],
            arrowprops=dict(arrowstyle='->', color=C_OVER[0], lw=0.8))
    y_lo = ax.get_ylim()[0]
    for idx, (alpha, col) in enumerate(zip(alpha_over, C_OVER)):
        t = first_rev[alpha]
        if t is not None:
            ax.axvline(t, color=col, linewidth=0.8, linestyle=':', alpha=0.6)
            ax.text(t + 0.3, y_lo * (0.95 - idx * 0.15), f'{t:.1f}%',
                    fontsize=7.5, color=col, va='bottom')

    for a_ax, ttl in ((ax, "Left: " + NET_LABEL), (ax2, "Right: " + TW_LABEL)):
        a_ax.axhline(0, color=C_ANNOTATION, linewidth=0.8, linestyle='--')
        a_ax.axvline(p['g'] * 100, color=C_DARK, linewidth=1.0, linestyle=':',
                     label=f"hist. mean g = {p['g']*100:.1f}%")
        a_ax.set_xlabel("Growth rate g (%)")
        a_ax.set_ylabel("% of honest TW(1)")
        a_ax.set_title(ttl, fontsize=8.5)
        a_ax.set_xlim(0, 40)
        a_ax.legend(fontsize=8)

    fig.suptitle(
        f"Figure 7.3 - Overstater: net tax and terminal wealth by growth rate\n"
        f"N = {_n_val(p)}, $V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%",
        fontsize=10)
    plt.tight_layout()
    return _save(fig, "val_fig_7_3_overstatement_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1a — Overstatement coherence: Net | TW | net-diff vs N
# ─────────────────────────────────────────────────────────────

def fig_7_1a_overstatement_coherence(data: dict):
    print("  Generating fig 7.1a: overstatement coherence (Net | TW | vs N)...")
    p   = data['params']
    cd  = data['charts']['fig_7_1a_overstatement_coherence']
    _check_stamp(cd, p, 'fig 7.1a')

    alphas_grid = cd['alphas_grid']
    g_grid      = cd['g_grid']
    m_net       = np.array(cd['matrix_net'])
    m_tw        = np.array(cd['matrix_tw_cost'])
    n_right     = cd['n_right']
    net_diffs   = {float(k): v for k, v in cd['net_diffs'].items()}
    hist_mean   = cd['hist_mean']
    N_val       = cd.get('N_val', _n_val(p))
    N_fill      = cd.get('N_fill', cd.get('N_ssm'))
    g_pct_grid  = [g * 100 for g in g_grid]
    over_alphas = [1.2, 1.5, 1.8, 2.0]

    crossings = {}
    for alpha in over_alphas:
        diffs = net_diffs[alpha]
        cross = []
        for k in range(len(diffs) - 1):
            if diffs[k] * diffs[k + 1] < 0:
                cross.append(n_right[k] + (0 - diffs[k]) / (diffs[k + 1] - diffs[k]))
        crossings[alpha] = cross

    apply_style_nogrid()
    fig = plt.figure(figsize=(20.0, 5.8))
    gs  = fig.add_gridspec(1, 5, width_ratios=[1, 1, 0.04, 0.3, 1.15], wspace=0.28)
    ax1 = fig.add_subplot(gs[0]); ax3 = fig.add_subplot(gs[1], sharey=ax1)
    cax = fig.add_subplot(gs[2]); ax2 = fig.add_subplot(gs[4])

    vmax = 10.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    ext  = [g_pct_grid[0], g_pct_grid[-1], alphas_grid[0], alphas_grid[-1]]
    for a_ax, mat, ttl in ((ax1, m_net, "Net tax:  (Net(α) − Net(1)) / TW(1)"),
                           (ax3, m_tw,  "TW cost:  −(TW(α) − TW(1)) / TW(1)")):
        a_ax.imshow(mat, origin='lower', aspect='auto', cmap='RdBu_r', norm=norm,
                    extent=ext, zorder=1)
        CS = a_ax.contour(g_pct_grid, alphas_grid, mat, levels=[0.0],
                          colors=[C_DARK], linewidths=1.8, zorder=4)
        try:
            a_ax.clabel(CS, levels=[0.0], fmt={0.0: '= 0'}, fontsize=8, inline=True)
        except Exception:
            pass
        a_ax.axvline(hist_mean * 100, color='#333333', linewidth=1.4, linestyle='--', zorder=5,
                     label=f'Hist. mean g = {hist_mean*100:.1f}%')
        a_ax.set_xlabel("Actual growth rate g (%)", fontsize=10)
        a_ax.set_title(ttl, fontsize=10)
        a_ax.set_xlim(0, 40)
        a_ax.set_ylim(0.1, 2.0)
    ax1.set_ylabel("Declaration ratio α", fontsize=10)
    ax1.legend(loc='lower right', fontsize=8.5, frameon=True, framealpha=0.9)
    cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'),
                        cax=cax)
    cbar.set_label('pp of honest TW(1)  (red = worse for declarer)', fontsize=8)

    ax2.grid(True)
    Y_CLIP = -3.0; Y_HI = 40.0
    ax2.set_ylim(Y_CLIP, Y_HI)
    ax2.axhline(0, color='#333333', linewidth=1.2, zorder=3, label='α = 1.0 honest (zero line)')
    ax2.axhspan(Y_CLIP, 0,    alpha=0.04, color='#2166ac', zorder=0)
    ax2.axhspan(0,      Y_HI, alpha=0.04, color='#d73027', zorder=0)
    for alpha, col in zip(over_alphas, C_OVER_LIGHT):
        ax2.plot(n_right, net_diffs[alpha], color=col, linewidth=2.0, label=f'α = {alpha}')
    for idx, (alpha, col) in enumerate(zip(over_alphas, C_OVER_LIGHT)):
        for n_cross in crossings[alpha]:
            ax2.axvline(n_cross, color=col, linewidth=0.8, linestyle=':', alpha=0.6)
            ax2.text(n_cross + 0.3, Y_HI * (0.55 - idx * 0.07),
                     f'α={alpha}, N≈{n_cross:.0f}', fontsize=7.5, color=col, va='top')
    ax2.axvline(N_val, color='#d73027', linewidth=1.2, linestyle=':', zorder=2)
    ax2.text(N_val + 0.4, Y_CLIP + 0.4, f'N={N_val} (canonical)', fontsize=7.5,
             color='#d73027', va='bottom')
    if N_fill is not None:
        ax2.axvline(N_fill, color='#555555', linewidth=1.0, linestyle='--', zorder=2)
        ax2.text(N_fill + 0.4, Y_CLIP + 0.5, f'N={N_fill}\n(SSM fill year;\nreference only)',
                 fontsize=7.5, color='#555555', va='bottom')
    ax2.set_xlabel("Holding period N (years)", fontsize=10)
    ax2.set_ylabel("Net(α) − Net(honest)  [£m]", fontsize=9, labelpad=6)
    ax2.set_xlim(5, 60)
    ax2.set_title(f"Net tax diff vs holding period N\n"
                  f"g = hist. mean ({hist_mean*100:.1f}%) · $V_0$ = £{p['V0_m']:.0f}m", fontsize=10)
    ax2.legend(loc='upper left', fontsize=8.5, frameon=True, framealpha=0.9)

    cross_strs = ', '.join(f'α={a}: N≈{crossings[a][0]:.0f}' for a in over_alphas if crossings[a])
    fig.suptitle(
        "Figure 7.1a - Overstatement: net tax and terminal wealth, side by side\n"
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%, N = {N_val}   |   "
        f"Net-tax zero crossings vs N: {cross_strs if cross_strs else 'none in range'}",
        fontsize=10, y=1.02)
    return _save(fig, "val_fig_7_1a_overstatement_coherence.png")


# ─────────────────────────────────────────────────────────────
# FIG 5.2b — TW advantage decomposition
# ─────────────────────────────────────────────────────────────

def fig_5_2b_tw_decomposition(data: dict):
    print("  Generating fig 5.2b: TW advantage decomposition...")
    p   = data['params']
    cd  = data['charts']['fig_5_2b_tw_decomposition']
    _check_stamp(cd, p, 'fig 5.2b')

    alpha_x  = np.array(cd['alpha_over_fine'])
    g_decomp = np.array(cd['g_decomp'])
    wsd_arr  = np.array(cd['wsd'])
    rd_arr   = np.array(cd['rd'])
    sd_arr   = np.array(cd['sd'])
    tw_arr   = np.array(cd['tw'])
    ep_arr   = np.array(cd['ep'])
    f_matrix = np.array(cd['f_matrix'])   # [alpha × g]
    hist_mean = p['g']
    N         = _n_val(p)

    stack_err = np.max(np.abs((wsd_arr - rd_arr - sd_arr) - tw_arr))
    if stack_err > 0.01:
        print(f"    WARNING: fig 5.2b left-panel identity error = {stack_err:.4f}pp")

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)

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
            a_cross = (alpha_x[k] + (0 - tw_arr[k]) / (tw_arr[k + 1] - tw_arr[k])
                       * (alpha_x[k + 1] - alpha_x[k]))
            ax1.axvline(a_cross, color='#333333', linewidth=1.0, linestyle='--', zorder=4)
            ax1.text(a_cross + 0.01, tw_arr.max() * 0.8,
                     f'TW adv = 0\na~{a_cross:.2f}', fontsize=7.5, color='#333333')
    ax1.set_xlabel("Declaration ratio α", fontsize=10)
    ax1.set_ylabel("As % of honest TW_settled", fontsize=10)
    ax1.set_title(
        f"Left: TW advantage — decomposition\n"
        f"g = {hist_mean*100:.1f}%  ·  N = {N}  ·  V₀ = £{p['V0_m']:.0f}m",
        fontsize=9.5)
    ax1.set_xlim(1.0, 2.0)
    ax1.legend(loc='upper left', fontsize=8)

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
# FIG 7.1c — (g, N) surfaces: TW advantage row + net-tax row
# ─────────────────────────────────────────────────────────────

def fig_7_1c_tw_advantage_gN_surface(data: dict):
    print("  Generating fig 7.1c: (g, N) surfaces (TW row | Net row)...")
    p   = data['params']
    cd  = data['charts']['fig_7_1c_tw_advantage_gN_surface']

    g_surf  = cd['g_surf']
    n_surf  = cd['n_surf']
    g_pct   = [g * 100 for g in g_surf]
    hist_mean = p['g']
    canon_N   = _n_val(p)
    over_alphas = [1.2, 1.5, 1.8, 2.0]

    apply_style_nogrid()
    fig, axes = plt.subplots(2, 4, figsize=(20.0, 10.0))

    # Row 0: TW advantage (positive = retains more)
    for ax, alpha in zip(axes[0], over_alphas):
        mat  = np.array(cd['surfaces'][str(alpha)])   # [g × N]
        vmax = float(np.percentile(mat, 98))
        norm = mcolors.Normalize(vmin=0.0, vmax=vmax)
        im = ax.imshow(mat, origin='lower', aspect='auto', cmap='Blues', norm=norm,
                       extent=[n_surf[0], n_surf[-1], g_pct[0], g_pct[-1]], zorder=1)
        lv = [l for l in [0.5, 1, 1.5, 2, 3, 4, 6, 8, 10, 12] if 0 < l < vmax]
        if lv:
            CS = ax.contour(n_surf, g_pct, mat, levels=lv, colors='white',
                            linewidths=0.9, zorder=4, alpha=0.85)
            ax.clabel(CS, fmt='%g%%', fontsize=7.5, inline=True)
        ax.axhline(hist_mean * 100, color='#d73027', linewidth=1.2, linestyle='--', zorder=5)
        ax.axvline(canon_N, color='#d73027', linewidth=1.2, linestyle=':', zorder=5,
                   label=f'canonical N = {canon_N}')
        pi = np.unravel_index(np.argmax(mat), mat.shape)
        ax.plot(int(n_surf[pi[1]]), g_pct[pi[0]], marker='*', markersize=12,
                color='#ff7f00', zorder=7, clip_on=False,
                label=f'Peak {mat[pi]:.1f}pp (g={g_pct[pi[0]]:.1f}%, N={int(n_surf[pi[1]])})')
        gi = int(np.argmin(np.abs(np.array(g_surf) - hist_mean)))
        ni = int(np.argmin(np.abs(np.array(n_surf) - canon_N)))
        ax.plot(canon_N, hist_mean * 100, marker='o', markersize=7, color='#d73027',
                zorder=6, clip_on=False)
        ax.annotate(f'{mat[gi, ni]:.2f}pp', xy=(canon_N, hist_mean * 100),
                    xytext=(canon_N + 3, hist_mean * 100 + 1.5), fontsize=7.5, color='#d73027',
                    arrowprops=dict(arrowstyle='->', color='#d73027', lw=0.8))
        cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, shrink=0.85)
        cbar.set_label('TW(α) − TW(1), % of TW(1)   [+ = retains more]', fontsize=7.5)
        ax.set_title(f"α = {alpha}: terminal-wealth advantage", fontsize=9.5)
        ax.set_xlabel("Holding period N (years)", fontsize=9)
        ax.set_ylabel("Actual growth rate g (%)", fontsize=9)
        ax.set_xlim(n_surf[0], n_surf[-1]); ax.set_ylim(g_pct[0], g_pct[-1])
        ax.legend(loc='upper right', fontsize=7, framealpha=0.92)

    # Row 1: net-tax difference (positive = pays more), diverging, symmetric
    for ax, alpha in zip(axes[1], over_alphas):
        mat  = np.array(cd['surfaces_net'][str(alpha)])
        vmax = max(float(np.percentile(np.abs(mat), 98)), 1e-6)
        norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
        im = ax.imshow(mat, origin='lower', aspect='auto', cmap='RdBu_r', norm=norm,
                       extent=[n_surf[0], n_surf[-1], g_pct[0], g_pct[-1]], zorder=1)
        try:
            CS0 = ax.contour(n_surf, g_pct, mat, levels=[0.0], colors=[C_DARK],
                             linewidths=1.6, zorder=4)
            ax.clabel(CS0, fmt={0.0: 'Net = 0'}, fontsize=7.5, inline=True)
        except Exception:
            pass
        ax.axhline(hist_mean * 100, color='#333333', linewidth=1.2, linestyle='--', zorder=5)
        ax.axvline(canon_N, color='#333333', linewidth=1.2, linestyle=':', zorder=5)
        gi = int(np.argmin(np.abs(np.array(g_surf) - hist_mean)))
        ni = int(np.argmin(np.abs(np.array(n_surf) - canon_N)))
        ax.plot(canon_N, hist_mean * 100, marker='o', markersize=7, color=C_DARK,
                zorder=6, clip_on=False)
        ax.annotate(f'{mat[gi, ni]:+.2f}pp', xy=(canon_N, hist_mean * 100),
                    xytext=(canon_N + 3, hist_mean * 100 + 1.5), fontsize=7.5, color=C_DARK,
                    arrowprops=dict(arrowstyle='->', color=C_DARK, lw=0.8))
        cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, shrink=0.85)
        cbar.set_label('(Net(α) − Net(1)) / TW(1), pp   [+ = pays more]', fontsize=7.5)
        ax.set_title(f"α = {alpha}: net tax difference", fontsize=9.5)
        ax.set_xlabel("Holding period N (years)", fontsize=9)
        ax.set_ylabel("Actual growth rate g (%)", fontsize=9)
        ax.set_xlim(n_surf[0], n_surf[-1]); ax.set_ylim(g_pct[0], g_pct[-1])

    fig.suptitle(
        "Figure 7.1c - Overstatement across (g, N) space: terminal wealth (top) and net tax (bottom)\n"
        f"Both divided by honest TW(1) · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']} · "
        f"dashed = hist. mean g ({hist_mean*100:.1f}%), dotted = canonical N ({canon_N})",
        fontsize=10, y=1.0)
    plt.tight_layout()
    return _save(fig, "val_fig_7_1c_tw_advantage_gN_surface.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.1d — Net | TW cost | PV(true value) heatmaps
# ─────────────────────────────────────────────────────────────

def fig_7_1d_c1_vs_c12_heatmap(data: dict):
    print("  Generating fig 7.1d: Net | TW cost | PV heatmaps...")
    p       = data['params']
    grids   = data['grids']
    cd      = data['charts']['fig_7_1d_c12_heatmap']
    _check_stamp(cd, p, 'fig 7.1d')

    G_LABELS   = grids['g_labels']
    ALPHA_VALS = grids['alpha_vals']
    rho        = cd['rho']
    m_net = np.array(cd['matrix_net'])
    m_tw  = np.array(cd['matrix_tw_cost'])
    m_pv  = np.array(cd['matrix_pv'])
    norm  = _shared_norm(m_net, m_tw, m_pv)

    apply_style_nogrid()
    fig, axes = plt.subplots(1, 3, figsize=(20.0, 5.8), sharey=True)
    _heat(axes[0], m_net, G_LABELS, ALPHA_VALS, norm, "Net tax (undiscounted, credited £)", fs=6.5)
    _heat(axes[1], m_tw,  G_LABELS, ALPHA_VALS, norm, "TW cost (terminal wealth lost)", fs=6.5)
    im = _heat(axes[2], m_pv, G_LABELS, ALPHA_VALS, norm,
               f"C.12 PV of true-value payments (ρ = {rho*100:.0f}%)", fs=6.5)
    axes[0].set_ylabel("Declaration ratio α")
    cbar = fig.colorbar(im, ax=list(axes), fraction=0.015, pad=0.02)
    cbar.set_label("pp of honest TW(1)   (red = worse for declarer)", fontsize=8)

    fig.suptitle(
        "Figure 7.1d - Three views of the cost of mis-declaration, one denominator (honest TW(1)), one scale\n"
        f"N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']} · "
        "PV = holding-period payments at true value L/α + sale-year and post-sale cash, discounted at ρ",
        fontsize=10)
    return _save(fig, "val_fig_7_1d_c1_vs_c12_nominal_vs_npv.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.4 — State tolerance zone (PV revenue) and incentive alignment
# ─────────────────────────────────────────────────────────────

def _log_alpha_axis(ax, alphas):
    ax.set_yscale('log')
    ticks = [t for t in (0.1, 0.2, 0.5, 1, 2, 3, 5, 8) if alphas[0] * 0.999 <= t <= alphas[-1] * 1.001]
    ax.set_yticks(ticks); ax.set_yticklabels([str(t) for t in ticks])
    ax.minorticks_off()
    ax.set_ylim(alphas[0], alphas[-1])


def _mesh(ax, g, alphas, m, **kw):
    return ax.pcolormesh(g, alphas, m, shading='nearest', **kw)


def fig_7_4_tolerance_zone(data: dict):
    print("  Generating fig 7.4: revenue tolerance zone + incentive alignment...")
    p  = data['params']
    cd = data['charts']['fig_7_4_tolerance_zone']
    _check_stamp(cd, p, 'fig 7.4')

    alphas = np.array(cd['alphas']); g = np.array(cd['g_grid']) * 100.0
    rho_h  = cd['rho_headline']; tol = cd['tol_pp']; rhos = cd['rhos']
    pv   = np.array(cd['pv'][str(rho_h)])          # [alpha x g], pp of TW(1)
    tw   = np.array(cd['tw_gap'])                  # + = declarer retains more
    a_star = np.array(cd['alpha_star'])

    apply_style_nogrid()
    fig, axes = plt.subplots(1, 3, figsize=(20.0, 6.0),
                             gridspec_kw={'width_ratios': [1.05, 1.05, 1.0]})
    ax1, ax2, ax3 = axes

    # (a) PV revenue difference with tolerance zone
    vmax = 12.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    im = _mesh(ax1, g, alphas, pv, cmap='RdBu_r', norm=norm, zorder=1)
    ax1.contourf(g, alphas, pv, levels=[-tol, tol], colors='none', hatches=['///'], zorder=3)
    for lvl, ls, lw in ((0.0, '-', 1.8), (-tol, '--', 1.2), (tol, '--', 1.2)):
        CS = ax1.contour(g, alphas, pv, levels=[lvl], colors=[C_DARK], linewidths=lw,
                         linestyles=ls, zorder=4)
    ax1.plot(g, a_star, color='#ff7f00', linewidth=2.0, linestyle=':', zorder=6,
             label='Declarer TW-maximising α*(g)')
    ax1.axvline(p['g'] * 100, color='#333333', linewidth=1.2, linestyle='--', zorder=5,
                label=f"Hist. mean g = {p['g']*100:.1f}%")
    ax1.axhline(1.0, color=C_DARK, linewidth=1.4, zorder=5)
    cb = fig.colorbar(im, ax=ax1, fraction=0.04, pad=0.02, extend='both')
    cb.set_label("PV of true-value payments vs honest, pp of TW(1)\n(blue = state receives less)", fontsize=8)
    _log_alpha_axis(ax1, alphas)
    ax1.set_xlabel("Actual growth rate g (%)"); ax1.set_ylabel("Declaration ratio α (log scale)")
    ax1.set_title(f"(a) State revenue vs honest, ρ = {rho_h*100:.0f}%\n"
                  f"hatched = tolerance zone |Δ| ≤ {tol:.0f}pp", fontsize=9.5)
    ax1.legend(loc='lower right', fontsize=8, frameon=True, framealpha=0.92)

    # (b) alignment map
    cat = np.zeros_like(pv)
    cat[(tw > 0) & (pv >= -tol)] = 1
    cat[(tw > 0) & (pv < -tol)]  = 2
    cat[(tw <= 0)] = 0
    cmap = mcolors.ListedColormap(['#eeeeee', '#66c2a5', '#d73027'])
    _mesh(ax2, g, alphas, cat, cmap=cmap, vmin=0, vmax=2, zorder=1)
    ax2.contour(g, alphas, tw, levels=[0.0], colors=[C_DARK], linewidths=1.0, zorder=3)
    ax2.plot(g, a_star, color='#ff7f00', linewidth=2.0, linestyle=':', zorder=6)
    ax2.axvline(p['g'] * 100, color='#333333', linewidth=1.2, linestyle='--', zorder=5)
    ax2.axhline(1.0, color=C_DARK, linewidth=1.0, zorder=5)
    _log_alpha_axis(ax2, alphas)
    ax2.set_xlabel("Actual growth rate g (%)"); ax2.set_ylabel("Declaration ratio α (log scale)")
    ax2.set_title(f"(b) Do declarer and state interests coincide? (ρ = {rho_h*100:.0f}%)", fontsize=9.5)
    ax2.legend(handles=[
        Patch(facecolor='#66c2a5', label=f'Declarer gains TW, state within {tol:.0f}pp (aligned)'),
        Patch(facecolor='#d73027', label=f'Declarer gains TW, state loses > {tol:.0f}pp (conflict)'),
        Patch(facecolor='#eeeeee', label='Declarer loses TW (no incentive)')],
        loc='lower right', fontsize=7.5, frameon=True, framealpha=0.95)

    # (c) state outcome at the declarer's best response, by rho
    ax3.grid(True)
    cols = plt.cm.viridis(np.linspace(0.05, 0.92, len(rhos)))
    ax3.axhspan(-tol, tol, color='#66c2a5', alpha=0.18, zorder=0, label=f'Tolerance ±{tol:.0f}pp')
    for r, col in zip(rhos, cols):
        ax3.plot(g, cd['pv_at_star'][str(r)], color=col, linewidth=2.2 if r == rho_h else 1.2,
                 label=f"ρ = {r*100:.0f}%" + (" (headline)" if r == rho_h else ""))
    ax3.axhline(0, color=C_DARK, linewidth=0.9)
    ax3.axvline(p['g'] * 100, color='#333333', linewidth=1.0, linestyle='--')
    ax3.text(0.02, 0.02, f"α* = {a_star.max():.1f} (grid maximum) at every g > 0",
             transform=ax3.transAxes, fontsize=7.5, color='#555555', va='bottom')
    ax3.set_ylim(-60, 15)
    ax3.set_xlabel("Actual growth rate g (%)")
    ax3.set_ylabel("State PV revenue vs honest at α*(g), pp of TW(1)")
    ax3.set_title("(c) State outcome when the declarer maximises terminal wealth", fontsize=9.5)
    ax3.legend(loc='upper right', fontsize=7, ncol=3)

    fig.suptitle(
        "Figure 7.4 - Where the state need not care: PV revenue tolerance zone and incentive alignment\n"
        f"N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']} · α searched on "
        f"[{alphas[0]:.1f}, {alphas[-1]:.1f}]",
        fontsize=10, y=1.02)
    plt.tight_layout()
    return _save(fig, "val_fig_7_4_revenue_tolerance_zone.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.5 — Discount-rate sweep of the PV revenue metric
# ─────────────────────────────────────────────────────────────

def fig_7_5_rho_sweep(data: dict):
    print("  Generating fig 7.5: rho sweep of PV revenue metric...")
    p  = data['params']
    cd = data['charts']['fig_7_4_tolerance_zone']
    _check_stamp(cd, p, 'fig 7.5')

    alphas = np.array(cd['alphas']); g = np.array(cd['g_grid']) * 100.0
    rhos = [r for r in cd['rho_display'] if str(r) in cd['pv']]
    tol = cd['tol_pp']; rho_h = cd['rho_headline']
    vmax = 12.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    apply_style_nogrid()
    ncol = 3; nrow = int(np.ceil(len(rhos) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(17.0, 5.2 * nrow), sharex=True, sharey=True)
    axes = np.atleast_1d(axes).flatten()
    im = None
    for ax, r in zip(axes, rhos):
        m = np.array(cd['pv'][str(r)])
        im = _mesh(ax, g, alphas, m, cmap='RdBu_r', norm=norm, zorder=1)
        ax.contourf(g, alphas, m, levels=[-tol, tol], colors='none', hatches=['///'], zorder=3)
        ax.contour(g, alphas, m, levels=[0.0], colors=[C_DARK], linewidths=1.6, zorder=4)
        ax.contour(g, alphas, m, levels=[-tol, tol], colors=[C_DARK], linewidths=1.0,
                   linestyles='--', zorder=4)
        ax.axvline(p['g'] * 100, color='#333333', linewidth=1.1, linestyle='--', zorder=5)
        ax.axhline(1.0, color=C_DARK, linewidth=1.2, zorder=5)
        _log_alpha_axis(ax, alphas)
        sub = m[alphas > 1][:, g <= 25]
        ax.set_title(f"ρ = {r*100:.0f}%" + ("  (headline)" if r == rho_h else "") +
                     f"\nα > 1, g ≤ 25%: worst shortfall {sub.min():.1f}pp",
                     fontsize=9)
        ax.set_xlabel("Actual growth rate g (%)"); ax.set_ylabel("Declaration ratio α (log)")
    for ax in axes[len(rhos):]:
        ax.axis('off')
    cb = fig.colorbar(im, ax=list(axes), fraction=0.015, pad=0.02, extend='both')
    cb.set_label("PV of true-value payments vs honest, pp of TW(1)   (blue = state receives less)", fontsize=8)
    fig.suptitle(
        "Figure 7.5 - Discount-rate sensitivity of state revenue vs honest declaration\n"
        f"Hatched = tolerance zone |Δ| ≤ {tol:.0f}pp · solid = 0 · dashed = ±{tol:.0f}pp · "
        f"N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']}",
        fontsize=10)
    return _save(fig, "val_fig_7_5_rho_sweep.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.6 — Breakeven discount rate
# ─────────────────────────────────────────────────────────────

def fig_7_6_breakeven_rho(data: dict):
    print("  Generating fig 7.6: breakeven discount rate...")
    p  = data['params']
    cd = data['charts']['fig_7_4_tolerance_zone']
    _check_stamp(cd, p, 'fig 7.6')

    tol = cd['tol_pp']; rho_h = cd['rho_headline']
    be_g = np.array(cd['be_g']) * 100
    be_alphas = cd['be_alphas']

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6))
    cols = plt.cm.Reds(np.linspace(0.35, 0.95, len(be_alphas)))
    for a, col in zip(be_alphas, cols):
        ax1.plot(be_g, np.array(cd['be_rho'][str(a)]) * 100, color=col, linewidth=1.8, label=f"α = {a}")
    ax1.plot(be_g, g_line := be_g, color='#555555', linewidth=1.0, linestyle=':', label='ρ = g')
    ax1.axhline(rho_h * 100, color='#2166ac', linewidth=1.0, linestyle='--', label=f'headline ρ = {rho_h*100:.0f}%')
    ax1.axvline(p['g'] * 100, color='#333333', linewidth=1.0, linestyle='--')
    ax1.set_xlim(be_g[0], be_g[-1]); ax1.set_ylim(0, 25)
    ax1.set_xlabel("Actual growth rate g (%)")
    ax1.set_ylabel(f"Breakeven ρ (%) — state shortfall = {tol:.0f}pp of TW(1)")
    ax1.set_title("(a) Discount rate needed to keep overstatement inside the tolerance zone\n"
                  "(state within tolerance for ρ above the curve)", fontsize=9.5)
    ax1.legend(loc='upper left', fontsize=8)

    # (b) breakeven vs alpha at hist mean g, from the (alpha x g) grid via bisection on stored PV(rho)
    rhos = np.array(cd['rhos']); alphas = np.array(cd['alphas']); g = np.array(cd['g_grid']) * 100
    jh = int(np.argmin(abs(g - p['g'] * 100)))
    over = alphas > 1.0
    for r, col in zip(rhos, plt.cm.viridis(np.linspace(0.05, 0.92, len(rhos)))):
        pv = np.array(cd['pv'][str(r)])[over, jh]
        ax2.plot(alphas[over], pv, color=col, linewidth=2.0 if r == rho_h else 1.2,
                 label=f"ρ = {r*100:.0f}%")
    ax2.axhspan(-tol, tol, color='#66c2a5', alpha=0.18, label=f'Tolerance ±{tol:.0f}pp')
    ax2.axhline(0, color=C_DARK, linewidth=0.9)
    ax2.set_xscale('log')
    ax2.set_xticks([1.2, 1.5, 2, 3, 5]); ax2.set_xticklabels(['1.2', '1.5', '2', '3', '5'])
    ax2.minorticks_off()
    ax2.set_ylim(-45, 3)
    ax2.set_xlabel("Overstatement ratio α (log scale)")
    ax2.set_ylabel("State PV revenue vs honest, pp of TW(1)")
    ax2.set_title(f"(b) State shortfall by α at g = {g[jh]:.1f}%, one line per ρ", fontsize=9.5)
    ax2.legend(loc='lower left', fontsize=7, ncol=3)

    fig.suptitle("Figure 7.6 - Breakeven discount rate for the state tolerance zone\n"
                 f"N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']}", fontsize=10)
    plt.tight_layout()
    return _save(fig, "val_fig_7_6_breakeven_rho.png")


# ─────────────────────────────────────────────────────────────
# FIG 7.7 — Declaration under uncertainty (market reveals true value)
# ─────────────────────────────────────────────────────────────

def fig_7_7_uncertainty(data: dict):
    print("  Generating fig 7.7: declaration under uncertainty...")
    p  = data['params']
    cd = data['charts']['fig_7_7_uncertainty']
    _check_stamp(cd, p, 'fig 7.7')

    ms = np.array(cd['ms']); tol = cd['tol_pp']
    sigmas = cd['sigmas']; modes = cd['modes']
    titles = {'committed': "Committed path: D_t = m·V₀(1+g)^t, no market feedback",
              'lagged':    "Anchored: D_t = m·V_{t-1}(1+g), re-declared on last year's observed value"}
    scols = plt.cm.plasma(np.linspace(0.05, 0.8, len(sigmas)))

    def slab(sg):
        return "σ = 0 (deterministic)" if sg == 0 else (f"σ = {sg*100:.1f}%" + (" (historical)" if abs(sg - 0.083) < 1e-9 else ""))

    apply_style()
    fig, axes = plt.subplots(2, 3, figsize=(19.0, 10.0), sharex=True)
    for r, md in enumerate(modes):
        ax1, ax2, ax3 = axes[r]
        for sg, col in zip(sigmas, scols):
            st = cd['stats'][md][str(sg)]
            ax1.plot(ms, st['tw_mean'], color=col, linewidth=1.8, label=slab(sg))
            if sg > 0:
                ax1.plot(ms, st['tw_p05'], color=col, linewidth=1.1, linestyle='--')
            ax2.plot(ms, np.array(st['p_shortfall']) * 100, color=col, linewidth=1.8, label=slab(sg))
            ax3.plot(ms, np.array(st['p_tw_gain']) * 100, color=col, linewidth=1.8, label=slab(sg) + ": P(TW gain)")
            ax3.plot(ms, np.array(st['p_over_at_sale']) * 100, color=col, linewidth=1.1, linestyle=':')
        ax1.axhline(0, color=C_DARK, linewidth=0.9)
        ax1.set_ylim(-15, 100)
        ax1.set_ylabel("TW vs honest on the same path (% of honest TW)")
        ax1.set_title(f"{titles[md]}\nTW gain: mean (solid), 5th percentile (dashed)", fontsize=9)
        ax2.set_ylim(-2, 102)
        ax2.set_ylabel(f"P(state PV shortfall > {tol:.0f}pp of TW(1)) (%), ρ = {cd['rho_headline']*100:.0f}%")
        ax2.set_title("Probability the state is outside its tolerance zone", fontsize=9)
        ax3.set_ylim(-2, 102)
        ax3.set_ylabel("Probability (%)")
        ax3.set_title("P(declarer gains TW) solid · P(realised α_N > 1 at sale) dotted", fontsize=9)
        for ax in (ax1, ax2, ax3):
            ax.axvline(1.0, color='#555555', linewidth=0.9, linestyle=':')
            ax.set_xscale('log')
            ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 3, 5]); ax.set_xticklabels(['0.1', '0.2', '0.5', '1', '2', '3', '5'])
            ax.minorticks_off()
            if r == 1:
                ax.set_xlabel("Targeted declaration level m (declared ÷ expected value; log scale)")
        ax1.legend(loc='upper left', fontsize=8)

    fig.suptitle(
        "Figure 7.7 - Declaring without controlling the realised ratio: the market reveals true value\n"
        f"Lognormal annual returns, mean g = {cd['g']*100:.2f}% · {cd['paths']} paired paths per σ · "
        f"N = {_n_val(p)} · $V_0$ = £{p['V0_m']:.0f}m · k = {p['k']}",
        fontsize=10, y=1.0)
    plt.tight_layout()
    return _save(fig, "val_fig_7_7_declaration_under_uncertainty.png")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("5_4_VAL_charts.py — loading val_data.json...")
    data = load_val_data()
    print(f"Data loaded. Generated: {data['meta']['generated']}")
    p = data['params']
    print(f"Parameters: k={p['k']}, N_val={_n_val(p)} (canonical), "
          f"N_fill={p.get('N_fill','?')} (SSM fill, reference only), "
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
    fig_7_4_tolerance_zone(data)
    fig_7_5_rho_sweep(data)
    fig_7_6_breakeven_rho(data)
    fig_7_7_uncertainty(data)

    print("\nAll figures written.")


if __name__ == '__main__':
    main()
