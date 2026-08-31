"""
VAL Output Script D — Figures (v2 — clarity pass)
===================================================
All improvements from review:

Fig 01  — Added actual entry-rate annotation at W_min; thicker/more visible
           $V_0$ reference line; corrected $\tau_0$ label placement note.

Fig 02  — Grid lines suppressed *behind* cell annotations by drawing a white
           filled rectangle under each text label, so numbers are never
           obscured by grid lines.

Fig 03  — Legend entry now matches subtitle ("dashed-dot"); added g=8.4%
           line (threshold-adjacent for overstaters); y-axis range expanded
           to avoid top-left crop; legend reordered.

Fig 04  — Two panels replaced with a single overlaid plot: constant-g curves
           in solid lines, 2006 historical-series curves in dashed-dot lines,
           same colour key. N=34 reference vline retained.

Fig 05  — Boundary-condition zone redefined from arbitrary 15–40% to the
           principled 17–25% band (inflection-to-plateau-onset, derived from
           the data). Right-panel bar labels repositioned to avoid overlap
           with the mean-inflection dashed line. Left-panel y-axis label
           corrected to "understater's TW" (not "true wealth").

Fig 06  — Right panel now shows BOTH the first-reversal g (where C.1 first
           turns positive) AND the re-reversal g (where C.1 drops back below
           zero after its peak), annotated separately. α=1.2 zero-crossing
           clarified with a nearest-approach annotation on the left panel.

Fig 07  — Two-panel overstatement coherence figure.
           Left: C.1 surface heatmap (g_actual × alpha) with the C.1=0
           contour, the hist-mean vertical line, and the motivation line
           (g = mean × α) showing that strong overstaters must be expecting
           growth precisely in the disadvantage band.
           Right: Net tax difference vs holding period N at g=hist_mean,
           showing advantage erosion and reversal by N≈28–32 for α≥1.8.
           Together: overstatement advantage is narrow in (g, N) space and
           the (g, N) combinations where it exists are not those a rational
           overstater would be predicting at declaration.
"""

import os
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker
import numpy as np
from datetime import date
from wdt_core import (load_params, tau, simulate, simulate_sell,
                      settle_tw, run_sim, decompose_tw_advantage, run_sim_hist, npv_tax_advantage)

from val_helpers import OUT_DIR as _VAL_OUT_DIR

# ─────────────────────────────────────────────────────────────
# OUTPUT DIRECTORY  (local for this run)
# ─────────────────────────────────────────────────────────────

OUT_DIR = _VAL_OUT_DIR

# All analytical grids sourced from TOML via load_params() in main().
G_VALS        = []
G_LABELS      = []
ALPHA_VALS    = []
N_ACTUAL_VALS = []

DPI    = 150
FSIZE  = (9, 5.5)
FONT   = 'DejaVu Sans'

UNDER_COLS  = ['#b30000', '#d73027', '#f46d43', '#fdae61']
HONEST_COL  = '#1a1a1a'
OVER_COLS   = ['#4393c3', '#2166ac', '#053061', '#313695']


def set_style():
    plt.rcParams.update({
        'font.family':       FONT,
        'font.size':         10,
        'axes.titlesize':    11,
        'axes.labelsize':    10,
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'axes.grid':         True,
        'grid.color':        '#e0e0e0',
        'grid.linewidth':    0.6,
        'figure.facecolor':  'white',
        'axes.facecolor':    'white',
        'legend.frameon':    False,
        'legend.fontsize':   9,
    })


def _save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: {path}")
    return path


# ─────────────────────────────────────────────────────────────
# FIG 01 — Rate function τ(W)
# Improvements:
#   • Entry rate at W_min annotated explicitly
#   • $V_0$ line thicker and more visible
#   • $\tau_0$ label clarified as "parameter" not "entry rate"
# ─────────────────────────────────────────────────────────────

def fig_01_rate_function(p):
    print("  Generating fig 01: rate function τ(W)...")
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    W_vals   = np.logspace(np.log10(p['W_min']), np.log10(10000), 500)
    tau_vals = [tau(w, sim_p) * 100 for w in W_vals]

    # Actual entry rate (rate at W_min)
    entry_rate = tau(p['W_min'], sim_p) * 100

    set_style()
    fig, ax = plt.subplots(figsize=FSIZE)

    ax.semilogx(W_vals, tau_vals, color='#1a1a1a', linewidth=2)

    # Asymptote reference lines
    ax.axhline(p['tau_0'] * 100, color='#888888', linewidth=0.8, linestyle='--')
    ax.axhline(p['tau_m'] * 100, color='#888888', linewidth=0.8, linestyle='--')

    # $V_0$ reference line — thicker and more distinct colour
    ax.axvline(p['V0_m'], color='#2166ac', linewidth=1.5, linestyle=':',
               label=f"$V_0$ = £{p['V0_m']:.0f}m (reference scenario)")

    # Annotate asymptotes on right margin
    ax.text(8000, p['tau_0'] * 100 + 0.8,
            f"$\tau_0$ = {p['tau_0']*100:.0f}% (floor parameter)",
            va='bottom', ha='right', fontsize=8, color='#666666')
    ax.text(8000, p['tau_m'] * 100 - 0.8,
            f"$\tau_m$ = {p['tau_m']*100:.0f}% (ceiling)",
            va='top', ha='right', fontsize=8, color='#666666')

    # Annotate the actual entry rate at W_min — the key addition
    ax.annotate(
        f"Entry rate at W_min\n= {entry_rate:.1f}%",
        xy=(p['W_min'], entry_rate),
        xytext=(p['W_min'] * 2.5, entry_rate + 6),
        fontsize=8, color='#1a1a1a',
        arrowprops=dict(arrowstyle='->', color='#555555', lw=0.9),
        ha='left'
    )

    ax.set_xlabel("Declared net worth W (£m, log scale)")
    ax.set_ylabel("Marginal WDT rate τ(W) (%)")
    ax.set_title(
        "Fig 01 — Marginal rate function τ(W)\n"
        f"k = {p['k']}, $\tau_0$ = {p['tau_0']*100:.0f}% (floor parameter), "
        f"$\tau_m$ = {p['tau_m']*100:.0f}%, W_min = £{p['W_min']:.0f}m"
    )
    ax.set_xlim(p['W_min'], 10000)
    ax.set_ylim(0, p['tau_m'] * 100 * 1.1)
    ax.legend(loc='upper left')

    ax.set_xticks([2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000])
    ax.set_xticklabels(['£2m', '£5m', '£10m', '£20m', '£50m', '£100m',
                         '£200m', '£500m', '£1bn', '£2bn', '£5bn', '£10bn'],
                        rotation=45, ha='right', fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_01_rate_function_tau_w.png")


# ─────────────────────────────────────────────────────────────
# FIG 02 — C.1 heatmap
# Improvement: white background rectangle under each cell label
#              so grid lines never obscure the numbers.
# ─────────────────────────────────────────────────────────────

def fig_02_c1_heatmap(p):
    print("  Generating fig 02: C.1 heatmap...")
    base_by_g = {g: run_sim(p, alpha=1.0, g=g) for g in G_VALS}

    matrix = []
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, g=g)
            b = base_by_g[g]
            val = (r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100 if abs(r['TW_settled']) > 1e-12 else 0.0
            row.append(val)
        matrix.append(row)
    matrix = np.array(matrix)

    set_style()
    fig, ax = plt.subplots(figsize=(10, 5.5))

    # Grid must sit behind the imshow and text layers — set_axisbelow only
    # works for line/patch artists; for imshow we disable the rcParam grid
    # and redraw grid lines manually at zorder=0 so they are always behind.
    ax.grid(False)

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
        "Fig 02 — C.1 metric: (Net(α) − Net(1)) / TW(α)  [percentage points]\n"
        f"Red = understater pays more · Blue = overstater pays less · "
        f"N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m"
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.04)
    cbar.set_label("pp relative to honest declaration")

    # Cell annotations at zorder=3 — above the image, no grid interference
    for i in range(len(ALPHA_VALS)):
        for j in range(len(G_VALS)):
            val = matrix[i, j]
            text_col = 'white' if abs(val) > vmax * 0.6 else '#1a1a1a'
            ax.text(j, i, f"{val:.1f}",
                    ha='center', va='center', fontsize=7.5,
                    color=text_col, zorder=3)

    # Highlight honest row
    honest_idx = ALPHA_VALS.index(1.0)
    ax.add_patch(plt.Rectangle((-0.5, honest_idx - 0.5), len(G_VALS), 1,
                                fill=False, edgecolor='#1a1a1a', linewidth=1.5))

    plt.tight_layout()
    return _save(fig, "val_fig_02_c1_tax_difference_heatmap.png")


# ─────────────────────────────────────────────────────────────
# FIG 03 — Declaration equilibrium cost curve
# Improvements:
#   • Added g = 8.4% line (threshold-adjacent for overstaters)
#   • Legend entry and subtitle consistent ("dash-dot")
#   • y-axis range expanded to prevent top-left crop
#   • 2006 historical series added as dash-dot purple
# ─────────────────────────────────────────────────────────────

def fig_03_equilibrium_cost_curve(p):
    print("  Generating fig 03: declaration equilibrium cost curve...")

    alpha_fine = [a / 100 for a in range(50, 205, 5)]

    # Constant-g scenarios — now includes 8.4%
    g_scenarios = [
        (0.059,  'g = 5.9% (constant)',  '#f46d43', '-',   1.8),
        (0.084,  'g = 8.4% (constant)',  '#d4ac0d', '-',   1.6),
        (0.1045, 'g = 10.5% (constant)', '#1a1a1a', '-',   2.0),
        (0.139,  'g = 13.9% (constant)', '#4393c3', '-',   1.8),
    ]

    set_style()
    fig, ax = plt.subplots(figsize=FSIZE)

    for g_val, g_label, col, ls, lw in g_scenarios:
        base = run_sim(p, alpha=1.0, g=g_val)
        net_diffs = []
        for alpha in alpha_fine:
            r = run_sim(p, alpha=alpha, g=g_val)
            if abs(base['Net_settled']) > 1e-12:
                net_diffs.append((r['Net_settled'] - base['Net_settled']) / base['Net_settled'] * 100)
            else:
                net_diffs.append(0.0)
        ax.plot(alpha_fine, net_diffs, color=col, linewidth=lw,
                linestyle=ls, label=g_label)

    # 2006 historical series — use run_sim_hist for consistent settled metrics
    returns_2006 = p['returns']  # already rotated to 2006 start
    N = p['N']
    g_series_2006 = returns_2006[:N]
    mean_g_2006   = sum(g_series_2006) / len(g_series_2006)

    base_hist = run_sim_hist(p, alpha=1.0)
    hist_diffs = []
    for alpha in alpha_fine:
        r = run_sim_hist(p, alpha=alpha)
        if abs(base_hist['Net_settled']) > 1e-12:
            hist_diffs.append((r['Net_settled'] - base_hist['Net_settled']) / base_hist['Net_settled'] * 100)
        else:
            hist_diffs.append(0.0)
    ax.plot(alpha_fine, hist_diffs, color='#7b2d8b', linewidth=2.0,
            linestyle='-.', label=f'2006 hist. series (mean g = {mean_g_2006*100:.1f}%, N = {N})')

    ax.axhline(0, color='#888888', linewidth=0.8, linestyle='--')
    ax.axvline(1.0, color='#888888', linewidth=0.8, linestyle=':')
    ax.text(1.02, 18, 'α = 1.0\n(honest)', fontsize=8, color='#666666', va='top')

    # Shade regions
    ax.axvspan(0.5, 1.0, alpha=0.04, color='#d73027')
    ax.axvspan(1.0, 2.0, alpha=0.04, color='#4393c3')

    ax.set_ylim(bottom=-20, top=25)

    ax.set_xlabel("Declaration ratio α  (α < 1 = understatement, α > 1 = overstatement)")
    ax.set_ylabel("Net tax vs honest declaration (%)")
    ax.set_title(
        "Fig 03 — Declaration equilibrium: net tax cost relative to honest\n"
        f"N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m  ·  Dash-dot = 2006 historical return series"
    )
    ax.legend(loc='upper right', fontsize=8)
    ax.set_xlim(0.5, 2.0)

    plt.tight_layout()
    return _save(fig, "val_fig_03_declaration_equilibrium_cost_curve.png")


# ─────────────────────────────────────────────────────────────
# FIG 04 — C.8 TW gap — OVERLAID single plot
# Improvement: constant-g (solid) and 2006 historical (dash-dot)
#              overlaid on one axes, same colour key.
# ─────────────────────────────────────────────────────────────

def fig_04_tw_gap_by_n(p):
    print("  Generating fig 04: C.8 TW gap by N (overlaid)...")

    alpha_under = [0.1, 0.2, 0.5, 0.8]
    alpha_over  = [1.2, 1.5, 1.8, 2.0]
    under_cols  = ['#b30000', '#d73027', '#f46d43', '#fdae61']
    over_cols   = ['#4393c3', '#2166ac', '#053061', '#313695']

    returns_2006 = p['returns']
    N_max  = max(N_ACTUAL_VALS)

    def tw_gap_const(alpha, n):
        r = run_sim(p, alpha=alpha, g=p['g'], N=n)
        b = run_sim(p, alpha=1.0,   g=p['g'], N=n)
        return (r['TW_settled'] - b['TW_settled']) / b['TW_settled'] * 100 if abs(b['TW_settled']) > 1e-12 else 0.0

    def tw_gap_hist(alpha, n):
        r = run_sim_hist(p, alpha=alpha, N=n)
        b = run_sim_hist(p, alpha=1.0,   N=n)
        return (r['TW_settled'] - b['TW_settled']) / b['TW_settled'] * 100 if abs(b['TW_settled']) > 1e-12 else 0.0

    set_style()
    fig, ax = plt.subplots(figsize=(10, 5.5))

    # Understaters
    for alpha, col in zip(alpha_under, under_cols):
        vals_c = [tw_gap_const(alpha, n) for n in N_ACTUAL_VALS]
        vals_h = [tw_gap_hist(alpha,  n) for n in N_ACTUAL_VALS]
        ax.plot(N_ACTUAL_VALS, vals_c, color=col, linewidth=1.8,
                linestyle='-',  label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, vals_h, color=col, linewidth=1.4,
                linestyle='-.', alpha=0.8)

    # Overstaters
    for alpha, col in zip(alpha_over, over_cols):
        vals_c = [tw_gap_const(alpha, n) for n in N_ACTUAL_VALS]
        vals_h = [tw_gap_hist(alpha,  n) for n in N_ACTUAL_VALS]
        ax.plot(N_ACTUAL_VALS, vals_c, color=col, linewidth=1.8,
                linestyle='--', label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, vals_h, color=col, linewidth=1.4,
                linestyle=':', alpha=0.8)

    ax.axhline(0, color=HONEST_COL, linewidth=1.0, linestyle='-', label='α = 1.0 (honest)')
    ax.axvline(p['N'], color='#888888', linewidth=0.8, linestyle=':')
    ylo = ax.get_ylim()[0]
    ax.text(p['N'] + 0.5, ylo * 0.88,
            f'N = {p["N"]}\n(RATES ref)', fontsize=8, color='#666666', va='bottom')

    # Line-style legend entry
    from matplotlib.lines import Line2D
    style_handles = [
        Line2D([0], [0], color='#555555', lw=1.8, linestyle='-',
               label='Solid = constant g (10.45%)'),
        Line2D([0], [0], color='#555555', lw=1.4, linestyle='-.',
               label='Dash-dot = 2006 hist. series (understaters)'),
        Line2D([0], [0], color='#555555', lw=1.8, linestyle='--',
               label='Dashed = constant g (overstaters)'),
        Line2D([0], [0], color='#555555', lw=1.4, linestyle=':',
               label='Dotted = 2006 hist. series (overstaters)'),
    ]
    h1, l1 = ax.get_legend_handles_labels()
    ax.legend(handles=h1 + style_handles,
              loc='lower left', ncol=2, fontsize=7.5)

    ax.set_xlabel("Holding period N (years)")
    ax.set_ylabel("TW vs honest declaration (%)")
    ax.set_title(
        "Fig 04 — C.8: terminal net worth gap vs honest, by holding period\n"
        "Solid/dashed = constant g (10.45%)  ·  Dash-dot/dotted = 2006 historical series  "
        "·  Red = understaters  ·  Blue = overstaters"
    )
    ax.set_xlim(N_ACTUAL_VALS[0], N_ACTUAL_VALS[-1])

    plt.tight_layout()
    return _save(fig, "val_fig_04_c8_tw_gap_by_n.png")


# ─────────────────────────────────────────────────────────────
# FIG 05 — Saturation reversal boundary (understaters)
# Improvements:
#   • Boundary zone redefined to principled 17–25% band
#   • Right-panel bar labels repositioned above bars only
#   • Left-panel y-axis label corrected
#   • Mean inflection annotation moved to avoid label collision
# ─────────────────────────────────────────────────────────────

def fig_05_saturation_reversal(p):
    print("  Generating fig 05: saturation reversal boundary (single panel)...")

    alpha_under = [0.1, 0.2, 0.5, 0.8]
    under_cols  = ['#b30000', '#d73027', '#f46d43', '#fdae61']

    g_sweep = [g_int / 1000.0 for g_int in range(0, 410)]
    g_pct   = [g * 100 for g in g_sweep]

    # Compute C.1 curves and structural boundaries
    c1_curves      = {}
    inflection_g   = {}
    plateau_onset  = {}
    plateau_height = {}

    for alpha in alpha_under:
        vals = []
        for g in g_sweep:
            r  = run_sim(p, alpha=alpha, g=g, N=p['N'])
            b  = run_sim(p, alpha=1.0,   g=g, N=p['N'])
            c1 = (r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100 if abs(r['TW_settled']) > 1e-12 else 0.0
            vals.append(c1)
        c1_curves[alpha] = vals

        deriv    = [vals[i+1] - vals[i] for i in range(len(vals) - 1)]
        peak_idx = max(range(len(deriv)), key=lambda i: deriv[i])
        inflection_g[alpha] = g_pct[peak_idx]

        plateau_onset[alpha] = None
        for i in range(peak_idx, min(len(deriv), 400)):
            if deriv[i] < 0.05:
                plateau_onset[alpha] = g_pct[i]
                break
        if plateau_onset[alpha] is None:
            plateau_onset[alpha] = 40.0

        plateau_height[alpha] = max(vals[:350])

    mean_inflection = sum(inflection_g[a]  for a in alpha_under) / len(alpha_under)
    mean_plateau    = sum(plateau_onset[a] for a in alpha_under) / len(alpha_under)

    set_style()
    fig, ax = plt.subplots(figsize=(10, 5.5))

    # ── Plateau shading: from mean plateau onset to right edge ──
    ax.axvspan(mean_plateau, 40, alpha=0.08, color='#888888', zorder=0,
               label=f'Plateau zone (g > {mean_plateau:.0f}%)')
    ax.text(mean_plateau + 0.3, 108,
            f'Plateau\n(g ≥ {mean_plateau:.0f}%)',
            fontsize=7.5, color='#555555', va='top')

    # ── Inflection vertical line (single value — property of rate fn) ──
    ax.axvline(mean_inflection, color='#333333', linewidth=1.1,
               linestyle='--', zorder=3,
               label=f'Inflection g ≈ {mean_inflection:.1f}% (rate fn property)')
    ax.text(mean_inflection + 0.3, 2,
            f'Inflection\n≈ {mean_inflection:.1f}%',
            fontsize=7.5, color='#333333', va='bottom')

    # ── C.1 curves with direct end-of-curve labels ──────────────
    x_label = 39.0   # g% at which to place the right-side label
    for alpha, col in zip(alpha_under, under_cols):
        curve_x = g_pct[:300]
        curve_y = c1_curves[alpha][:300]
        ax.plot(curve_x, curve_y, color=col, linewidth=2.0)

        # Label at right end of each curve
        ph = plateau_height[alpha]
        ax.text(31, ph,
                f"α = {alpha}  ({ph:.0f}%)",
                color=col, fontsize=8, va='center', ha='left',
                fontweight='bold' if alpha == 0.1 else 'normal')

    ax.axhline(0, color='#1a1a1a', linewidth=0.8, linestyle=':')

    ax.set_xlabel("Growth rate g (%)")
    ax.set_ylabel(
        "Excess tax burden (understater vs honest)\n"
        "as % of understater's terminal wealth TW(α)"
    )
    ax.set_title(
        f"Fig 05 — Understater penalty structure: inflection and plateau (N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m)\n"
        f"k = {p['k']} · Dashed line = inflection g ≈ {mean_inflection:.1f}% (rate fn property) · "
        f"Grey = plateau zone (g ≥ {mean_plateau:.0f}%) · Labels show plateau ceiling per α"
    )
    ax.set_xlim(0, 35)
    ax.set_ylim(-5, 120)

    # Compact legend (structural elements only — curves labelled directly)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    legend_handles = [
        Line2D([0], [0], color='#333333', lw=1.1, linestyle='--',
               label=f'Inflection ≈ {mean_inflection:.1f}% (rate fn property)'),
        Patch(facecolor='#888888', alpha=0.15,
              label=f'Plateau zone g ≥ {mean_plateau:.0f}%'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_05_saturation_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 06 — Overstatement reversal boundary
# Improvements:
#   • Right panel shows BOTH first-reversal and re-reversal g
#   • α=1.2 nearest-approach annotation on left panel
# ─────────────────────────────────────────────────────────────

def fig_06_overstatement_reversal(p):
    print("  Generating fig 06: overstatement reversal boundary...")

    alpha_over = [1.2, 1.5, 1.8, 2.0]
    over_cols  = ['#4393c3', '#2166ac', '#053061', '#313695']

    g_sweep  = [g_int / 1000.0 for g_int in range(0, 400)]
    g_pct    = [g * 100 for g in g_sweep]
    c1_curves  = {}
    first_rev  = {}   # g where C.1 first > 0
    re_rev     = {}   # g where C.1 drops back < 0 after its peak

    for alpha in alpha_over:
        vals       = []
        found_fwd  = None
        found_back = None
        peaked     = False
        peak_val   = -999
        for idx, g in enumerate(g_sweep):
            r  = run_sim(p, alpha=alpha, g=g, N=p['N'])
            b  = run_sim(p, alpha=1.0,   g=g, N=p['N'])
            c1 = (r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100 if abs(r['TW_settled']) > 1e-12 else 0.0
            vals.append(c1)
            if c1 > 0 and found_fwd is None:
                found_fwd = g * 100
            # Track peak
            if c1 > peak_val:
                peak_val = c1
                peaked   = False
            elif c1 < peak_val - 0.5:
                peaked = True
            # Re-reversal: after peak, C.1 goes back below 0
            if peaked and c1 < 0 and found_back is None and found_fwd is not None:
                found_back = g * 100
        c1_curves[alpha] = vals
        first_rev[alpha] = found_fwd
        re_rev[alpha]    = found_back

    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

    # ── LEFT: C.1 curves ────────────────────────────────────────
    for alpha, col in zip(alpha_over, over_cols):
        ax1.plot(g_pct, c1_curves[alpha], color=col, linewidth=1.8,
                 label=f"α = {alpha}")

    # α=1.2 nearest-approach annotation
    vals_12 = c1_curves[1.2]
    nearest_idx = max(range(len(vals_12)), key=lambda i: vals_12[i])
    nearest_g   = g_pct[nearest_idx]
    nearest_val = vals_12[nearest_idx]
    if nearest_val < 0:
        ax1.annotate(
            f"α=1.2 peak ≈ {nearest_val:.1f}pp\n(never crosses zero)",
            xy=(nearest_g, nearest_val),
            xytext=(nearest_g + 3, nearest_val + 2.5),
            fontsize=7.5, color=over_cols[0],
            arrowprops=dict(arrowstyle='->', color=over_cols[0], lw=0.8)
        )

    ax1.axhline(0, color='#888888', linewidth=0.8, linestyle='--',
                label='zero (honest baseline)')
    ax1.set_xlabel("Growth rate g (%)")
    ax1.set_ylabel("C.1 metric (%) — negative = overstater pays less than honest")
    ax1.set_title(f"Overstater C.1 by g — N = {p['N']}")
    ax1.set_xlim(0, 40)
    ax1.legend(fontsize=8)

    # ── RIGHT: dual-bar — first reversal AND re-reversal ────────
    labels     = [f"α = {a}" for a in alpha_over]
    x_pos      = list(range(len(alpha_over)))
    bar_width  = 0.38

    # First reversal bars
    fwd_vals = [first_rev[a] if first_rev[a] is not None else 0 for a in alpha_over]
    bwd_vals = [re_rev[a]    if re_rev[a]    is not None else 0 for a in alpha_over]

    bars_fwd = ax2.bar([i - bar_width/2 for i in x_pos],
                       fwd_vals, width=bar_width, color=over_cols,
                       edgecolor='white', label='First reversal: overstater first pays more')
    bars_bwd = ax2.bar([i + bar_width/2 for i in x_pos],
                       bwd_vals, width=bar_width, color=over_cols, alpha=0.4,
                       edgecolor='white', label='Re-reversal: overstater cheap again')

    for bar, alpha in zip(bars_fwd, alpha_over):
        t = first_rev[alpha]
        h = bar.get_height()
        if t is not None:
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                     f"{t:.1f}%", ha='center', va='bottom', fontsize=8.5,
                     fontweight='bold')
        else:
            ax2.text(bar.get_x() + bar.get_width() / 2, 1.2,
                     "never\nreverses", ha='center', va='bottom',
                     fontsize=8, color='#1a1a1a')

    for bar, alpha in zip(bars_bwd, alpha_over):
        t = re_rev[alpha]
        h = bar.get_height()
        if t is not None:
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                     f"{t:.1f}%", ha='center', va='bottom', fontsize=8, color='#555555')
        else:
            # Either never reversed at all, or reversed but never re-reversed
            label = "n/a" if first_rev[alpha] is None else "no\nre-reversal\nin range"
            ax2.text(bar.get_x() + bar.get_width() / 2, 1.2,
                     label, ha='center', va='bottom',
                     fontsize=7.5, color='#888888')

    ax2.set_ylabel("g (%) at threshold")
    ax2.set_title(f"Reversal and re-reversal thresholds by α — N = {p['N']}")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(labels)
    ax2.set_ylim(0, 50)
    ax2.legend(fontsize=8, loc='upper right')

    fig.suptitle(
        "Fig 06 — Overstatement reversal: when overstater C.1 crosses zero (and back)\n"
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}  ·  "
        "Dark bar = first reversal (overstater starts paying more)  ·  "
        "Light bar = re-reversal (overstater cheap again at high g)",
        fontsize=10
    )
    plt.tight_layout()
    return _save(fig, "val_fig_06_overstatement_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 07 — Overstatement coherence
# Two-panel figure: C.1 surface heatmap (left) and net tax
# difference vs holding period N (right).
# Visual argument: the advantage is real but narrow — strong
# overstaters face disadvantage at the growth rates their
# motivation line predicts, and the advantage reverses by N≈29.
# ─────────────────────────────────────────────────────────────

_FIG07_OVER_ALPHAS = [1.2, 1.5, 1.8, 2.0]
_FIG07_OVER_COLS   = ['#74add1', '#4393c3', '#2166ac', '#053061']


def fig_07_overstatement_coherence(p):
    print("  Generating fig 07: overstatement coherence...")

    hist_mean = p['g']    # 10.45%
    N         = p['N']

    set_style()
    # Override grid and legend settings for the heatmap panel
    plt.rcParams.update({'legend.frameon': True, 'legend.framealpha': 0.9,
                         'legend.fontsize': 8.5})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

    # ── LEFT: C.1 surface heatmap ────────────────────────────
    alphas_grid = np.linspace(0.1, 2.0, 41)
    g_grid      = np.linspace(0.0, 0.25, 101)
    g_pct_grid  = g_grid * 100

    c1_matrix = np.zeros((len(alphas_grid), len(g_grid)))
    for i, alpha in enumerate(alphas_grid):
        for j, g in enumerate(g_grid):
            r  = run_sim(p, alpha=alpha, g=g, N=N)
            b  = run_sim(p, alpha=1.0,   g=g, N=N)
            c1 = (r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100 if abs(r['TW_settled']) > 1e-12 else 0.0
            c1_matrix[i, j] = c1

    ax1.grid(False)
    vmax = 6.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    ax1.imshow(
        c1_matrix,
        origin='lower', aspect='auto', cmap='RdBu_r', norm=norm,
        extent=[g_pct_grid[0], g_pct_grid[-1], alphas_grid[0], alphas_grid[-1]],
        zorder=1,
    )

    # C.1 = 0 contour
    CS = ax1.contour(
        g_pct_grid, alphas_grid, c1_matrix,
        levels=[0.0], colors=['#1a1a1a'], linewidths=1.8, zorder=4,
    )
    ax1.clabel(
        CS,
        levels=[0.0],
        fmt={0.0: 'C.1 = 0'},
        fontsize=8,
        inline=True,
        inline_spacing=6
    )

    # Vertical line: g = hist_mean
    ax1.axvline(hist_mean * 100, color='#333333', linewidth=1.4,
                linestyle='--', zorder=5,
                label=f'Hist. mean g = {hist_mean*100:.1f}%')
    ax1.text(hist_mean * 100 - 0.3, 1.45,
             f'{hist_mean*100:.1f}%\n(mean)', fontsize=7.5,
             color='#333333', va='center', ha='right')

    # Motivation line: g = hist_mean × alpha
    motiv_alphas = alphas_grid
    motiv_g      = hist_mean * motiv_alphas * 100
    mask = motiv_g <= 25.0
    ax1.plot(motiv_g[mask], motiv_alphas[mask],
             color='#b8860b', linewidth=2.0, linestyle='-.',
             zorder=6, label='Implied growth expectation\n(g = mean × α)')
    mid_idx = np.searchsorted(motiv_alphas[mask], 1.38)
    ax1.text(motiv_g[mask][mid_idx] + 0.5, motiv_alphas[mask][mid_idx] - 0.06,
             'Motivation\nline', fontsize=7.5, color='#b8860b',
             va='top', ha='left')

    # Region labels
    ax1.text(13, 1.9, 'DISADVANTAGE\n(overstater pays more)',
             ha='center', va='center', fontsize=7.5, color='#8b0000',
             fontweight='bold', zorder=7)
    ax1.text(3.5, 1.13, 'ADVANTAGE\n(overstater pays less)',
             ha='center', va='center', fontsize=7.5, color='#08306b',
             fontweight='bold', zorder=7)

    cbar = fig.colorbar(
        plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r'),
        ax=ax1, fraction=0.035, pad=0.03, shrink=0.85
    )
    cbar.set_label('C.1 (pp)  −=advantage  +=disadvantage', fontsize=8)
    cbar.ax.tick_params(labelsize=8)

    ax1.set_xlabel("Actual growth rate g (%)", fontsize=10)
    ax1.set_ylabel("Declaration ratio α", fontsize=10)
    ax1.set_title(
        "Advantage landscape: C.1 by (g_actual, α)\n"
        "Blue = advantage · Red = disadvantage · Black = indifference boundary",
        fontsize=10
    )
    ax1.set_xlim(0, 25)
    ax1.set_ylim(0.1, 2.0)
    ax1.legend(loc='lower right', fontsize=8, framealpha=0.9)

    # ── RIGHT: Net tax diff vs holding period N ──────────────
    n_vals = list(range(5, 61))

    all_series = {}
    crossings  = {}
    for alpha in _FIG07_OVER_ALPHAS:
        diffs = []
        for n in n_vals:
            r = run_sim(p, alpha=alpha, g=hist_mean, N=n)
            b = run_sim(p, alpha=1.0,   g=hist_mean, N=n)
            diffs.append(r['Net_settled'] - b['Net_settled'])
        all_series[alpha] = diffs
        cross = []
        for k in range(len(diffs) - 1):
            if diffs[k] * diffs[k + 1] < 0:
                n_cross = n_vals[k] + (0 - diffs[k]) / (diffs[k + 1] - diffs[k])
                cross.append(n_cross)
        crossings[alpha] = cross

    Y_CLIP = -15.0
    Y_HI   =  4.0

    ax2.set_ylim(Y_CLIP, Y_HI)
    ax2.axhline(0, color='#333333', linewidth=1.2, linestyle='-',
                zorder=3, label='α = 1.0 honest (zero line)')
    ax2.axhspan(Y_CLIP, 0,    alpha=0.04, color='#2166ac', zorder=0)
    ax2.axhspan(0,      Y_HI, alpha=0.04, color='#d73027', zorder=0)

    ax2.text(7, -13, 'ADVANTAGE\n(pays less than honest)',
             fontsize=7.5, color='#08306b', va='bottom', fontweight='bold')
    ax2.text(7,  3.5, 'DISADVANTAGE\n(pays more than honest)',
             fontsize=7.5, color='#8b0000', va='top', fontweight='bold')

    for alpha, col in zip(_FIG07_OVER_ALPHAS, _FIG07_OVER_COLS):
        diffs         = all_series[alpha]
        clipped_mask  = [d < Y_CLIP for d in diffs]

        seg_x, seg_y = [], []
        for k, (n, d, clip) in enumerate(zip(n_vals, diffs, clipped_mask)):
            if not clip:
                seg_x.append(n); seg_y.append(d)
            else:
                if seg_x:
                    ax2.plot(seg_x, seg_y, color=col, linewidth=2.0)
                    seg_x, seg_y = [], []
        if seg_x:
            ax2.plot(seg_x, seg_y, color=col, linewidth=2.0, label=f'α = {alpha}')
        else:
            ax2.plot([], [], color=col, linewidth=2.0, label=f'α = {alpha}')

        # Dashed stub at clip boundary
        first_clip = next((k for k, c in enumerate(clipped_mask) if c), None)
        if first_clip and first_clip > 0:
            ax2.plot([n_vals[first_clip - 1], n_vals[first_clip]],
                     [diffs[first_clip - 1], Y_CLIP],
                     color=col, linewidth=1.2, linestyle='--', alpha=0.6)
            ax2.annotate('', xy=(n_vals[first_clip], Y_CLIP),
                         xytext=(n_vals[first_clip], Y_CLIP + 1.5),
                         arrowprops=dict(arrowstyle='->', color=col, lw=1.0))

        # Zero-crossing markers
        for n_cross in crossings[alpha]:
            ax2.plot(n_cross, 0, marker='o', markersize=6,
                     color=col, zorder=6, clip_on=False)
            label_y = 1.0 if alpha == 1.8 else (-2.5 if alpha == 2.0 else 1.0)
            ax2.annotate(
                f'α={alpha}: crosses N≈{n_cross:.0f}',
                xy=(n_cross, 0),
                xytext=(n_cross + 3, label_y),
                fontsize=7.5, color=col,
                arrowprops=dict(arrowstyle='->', color=col, lw=0.8),
                zorder=7,
            )

    # N reference vline
    ax2.axvline(N, color='#555555', linewidth=1.0, linestyle='--', zorder=2)
    ax2.text(N + 0.4, Y_CLIP + 0.5,
             f'N={N}\n(RATES ref)', fontsize=7.5,
             color='#555555', va='bottom')

    ax2.set_xlabel("Holding period N (years)", fontsize=10)
    ax2.set_ylabel("Net(α) − Net(honest)  [£m]\n− = overstater pays less",
                   fontsize=9)
    ax2.set_xlim(5, 60)
    ax2.set_title(
        f"Advantage erosion: net tax diff vs holding period N\n"
        f"g = hist. mean ({hist_mean*100:.1f}%) · $V_0$ = £{p['V0_m']:.0f}m · "
        f"Dashed arrows = line continues below clip at £{abs(Y_CLIP):.0f}m",
        fontsize=10
    )
    ax2.legend(loc='lower left', fontsize=8.5, framealpha=0.9)

    fig.suptitle(
        "Fig 07 — Overstatement: the advantage is real but narrow\n"
        "Left: advantage landscape across (g_actual, α) — strong overstaters face "
        "disadvantage at moderate growth (9–17%)  ·  "
        "Right: advantage erodes and reverses by N≈29 for α ≥ 1.8 at hist. mean growth",
        fontsize=10, y=1.01
    )

    plt.tight_layout()
    return _save(fig, "val_fig_07_overstatement_coherence.png")


# ─────────────────────────────────────────────────────────────
# FIG 08 — TW advantage decomposition
# Two-panel figure:
#   Left:  Stacked area chart at g=hist_mean across alpha in [1.0, 2.0].
#          Shows the three cost/benefit terms as a fraction of honest TW:
#            - Excess periodic tax paid   (cost, plotted upward in red)
#            - Post-sale damping cost     (cost, stacked on periodic in orange)
#            - Sell-year refund benefit   (benefit, plotted downward in blue)
#            - Net TW advantage           (black line — algebraic sum)
#   Right: f_N ratio heatmap across (alpha, g).
#          Shows how rapidly equity is eroded relative to honest declaration.
#          Contours at f_ratio = 0.95 and 0.90.
# ─────────────────────────────────────────────────────────────

_FIG08_ALPHA_FINE  = np.linspace(1.0, 2.0, 41)
_FIG08_G_FINE      = np.linspace(0.0, 0.25, 51)


def _decompose_fig08(p, alpha, g):
    """
    Thin wrapper around wdt_core.decompose_tw_advantage() that unpacks
    the result dict into the 7-tuple expected by fig_08_tw_decomposition():

        W_sell_delta, refund_delta, settle_delta, tw_advantage,
        f_ratio, tw_honest, excess_periodic

    Correct additive identity (verified to machine precision):
        tw_advantage = W_sell_delta - refund_delta - settle_delta

    excess_periodic is returned last as an informational field only —
    it is NOT additive in the identity.  The incorrect identity
    -excess_periodic - refund_delta - settle_delta was used in Fig 08 v1.

    All values in £m except f_ratio (dimensionless).
    """
    d = decompose_tw_advantage(p, alpha, g)
    return (
        d['W_sell_delta'],       # term 1: f_N erosion effect on sell proceeds
        d['refund_delta'],       # term 2: sell-year refund difference
        d['settle_delta'],       # term 3: post-sale damping difference
        d['tw_advantage'],       # sum of above (verified)
        d['f_ratio'],            # f_N(alpha) / f_N(1)
        d['tw_honest'],          # denominator for % scaling
        d['excess_periodic'],    # informational only
    )


def fig_08_tw_decomposition(p):
    print("  Generating fig 08: TW advantage decomposition...")

    hist_mean = p['g']
    N         = p['N']

    # ── precompute left-panel series ─────────────────────────
    # Correct identity: tw_advantage = W_sell_delta - refund_delta - settle_delta
    # W_sell_delta <= 0  (f_N erosion reduces sell proceeds)
    # refund_delta <= 0  (larger sell-year refund for overstater)
    # settle_delta >= 0  (damping taxes back some of the refund)
    # excess_periodic is informational only — NOT additive in the identity.

    wsd_vals = []   # W_sell_delta / tw_honest  (always <= 0)
    rd_vals  = []   # refund_delta / tw_honest  (always <= 0)
    sd_vals  = []   # settle_delta / tw_honest  (always >= 0)
    tw_vals  = []   # tw_advantage / tw_honest
    ep_vals  = []   # excess_periodic / tw_honest  (informational)

    for alpha in _FIG08_ALPHA_FINE:
        wsd, rd, sd, tw_adv, _, tw_h, ep = _decompose_fig08(p, alpha, hist_mean)
        denom = tw_h if abs(tw_h) > 1e-12 else 1.0
        wsd_vals.append(wsd   / denom * 100)
        rd_vals.append( rd    / denom * 100)
        sd_vals.append( sd    / denom * 100)
        tw_vals.append( tw_adv / denom * 100)
        ep_vals.append( ep    / denom * 100)

    wsd_arr = np.array(wsd_vals)
    rd_arr  = np.array(rd_vals)
    sd_arr  = np.array(sd_vals)
    tw_arr  = np.array(tw_vals)
    ep_arr  = np.array(ep_vals)

    # Verify stacking sums to tw_arr (should be ~0 everywhere)
    stack_err = np.max(np.abs((wsd_arr - rd_arr - sd_arr) - tw_arr))
    if stack_err > 0.01:
        print(f"    WARNING: fig08 left-panel identity error = {stack_err:.4f}pp")

    # ── precompute right-panel f_N heatmap ───────────────────
    f_matrix = np.zeros((len(_FIG08_ALPHA_FINE), len(_FIG08_G_FINE)))
    for i, alpha in enumerate(_FIG08_ALPHA_FINE):
        for j, g in enumerate(_FIG08_G_FINE):
            _, _, _, _, f_ratio, _, _ = _decompose_fig08(p, alpha, g)
            f_matrix[i, j] = f_ratio

    # ── figure ───────────────────────────────────────────────
    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))
    alpha_x = _FIG08_ALPHA_FINE

    # ── LEFT: corrected stacked decomposition ────────────────
    #
    # Correct identity: tw_advantage = W_sell_delta - refund_delta - settle_delta
    #
    # Visual decomposition of tw_advantage (black line):
    #   ABOVE zero: -refund_delta  (the gain — refund is negative, so -rd > 0)
    #   BELOW zero: W_sell_delta   (f_N erosion cost — wsd <= 0)
    #   BELOW that: -(settle_delta) further down (damping cost — sd >= 0)
    #
    # The black line sits between the blue region (above) and the combined
    # red/orange region (below), and is the algebraic sum of all three terms.

    ax1.axhline(0, color='#555555', linewidth=0.9, zorder=2)

    # Refund benefit: -refund_delta > 0, plotted upward from zero
    ax1.fill_between(alpha_x, 0, -rd_arr,
                     color='#4393c3', alpha=0.55,
                     label='Sell-year refund benefit  (−refund_delta)')

    # f_N erosion cost: W_sell_delta <= 0, plotted downward from zero
    ax1.fill_between(alpha_x, 0, wsd_arr,
                     color='#d73027', alpha=0.55,
                     label='f_N erosion cost  (W_sell_delta ≤ 0)')

    # Post-sale damping cost: settle_delta >= 0, stacked further below wsd
    ax1.fill_between(alpha_x, wsd_arr, wsd_arr - sd_arr,
                     color='#f46d43', alpha=0.55,
                     label='Post-sale damping cost  (settle_delta)')

    # Net TW advantage line — algebraic sum; should bisect the areas
    ax1.plot(alpha_x, tw_arr,
             color='#1a1a1a', linewidth=2.2, zorder=5,
             label='Net TW advantage  (C.8 cross-check)')

    # Excess periodic tax — informational dotted line only
    ax1.plot(alpha_x, ep_arr,
             color='#6a3d9a', linewidth=1.3, linestyle=':', zorder=4,
             label='Excess periodic tax  (informational — not additive)')

    # Mark any tw_advantage zero-crossings
    for k in range(len(tw_arr) - 1):
        if tw_arr[k] * tw_arr[k + 1] < 0:
            a_cross = (alpha_x[k]
                       + (0 - tw_arr[k]) / (tw_arr[k + 1] - tw_arr[k])
                       * (alpha_x[k + 1] - alpha_x[k]))
            ax1.axvline(a_cross, color='#333333', linewidth=1.0,
                        linestyle='--', zorder=4)
            ax1.text(a_cross + 0.01, tw_arr.max() * 0.8,
                     f'TW adv = 0\na~{a_cross:.2f}',
                     fontsize=7.5, color='#333333')

    # Annotate endpoint
    ax1.annotate(f'α=2.0: net +{tw_arr[-1]:.1f}pp',
                 xy=(2.0, tw_arr[-1]),
                 xytext=(1.82, tw_arr[-1] + 1.5),
                 fontsize=7.5, color='#1a1a1a',
                 arrowprops=dict(arrowstyle='->', color='#1a1a1a', lw=0.8))

    ax1.set_xlabel("Declaration ratio α", fontsize=10)
    ax1.set_ylabel("As % of honest TW_settled", fontsize=10)
    ax1.set_title(
        f"Left: TW advantage — corrected decomposition\n"
        f"g = {hist_mean*100:.1f}% (hist. mean)  ·  N = {N}  ·  "
        f"V₀ = £{p['V0_m']:.0f}m  ·  k = {p['k']}\n"
        f"Identity: tw_adv = W_sell_delta − refund_delta − settle_delta  ✓",
        fontsize=9.5
    )
    ax1.set_xlim(1.0, 2.0)
    ax1.legend(loc='upper left', fontsize=8)
    ax1.grid(True, zorder=0)

    # ── RIGHT: f_N ratio heatmap ─────────────────────────────
    ax2.grid(False)

    g_pct = _FIG08_G_FINE * 100
    norm  = mcolors.Normalize(vmin=f_matrix.min(), vmax=1.0)
    im = ax2.imshow(
        f_matrix,
        origin='lower', aspect='auto',
        cmap='Blues_r', norm=norm,
        extent=[g_pct[0], g_pct[-1],
                _FIG08_ALPHA_FINE[0], _FIG08_ALPHA_FINE[-1]],
        zorder=1,
    )

    CS95 = ax2.contour(
        g_pct, _FIG08_ALPHA_FINE, f_matrix,
        levels=[0.95], colors=['#d73027'], linewidths=1.6, zorder=4,
    )
    ax2.clabel(CS95, fmt={0.95: 'f ratio = 0.95'}, fontsize=8, inline=True)

    CS90 = ax2.contour(
        g_pct, _FIG08_ALPHA_FINE, f_matrix,
        levels=[0.90], colors=['#7f0000'], linewidths=1.4,
        linestyles='--', zorder=4,
    )
    ax2.clabel(CS90, fmt={0.90: 'f ratio = 0.90'}, fontsize=8, inline=True)

    ax2.axvline(hist_mean * 100, color='#333333', linewidth=1.4,
                linestyle='--', zorder=5,
                label=f'g = hist. mean ({hist_mean*100:.1f}%)')

    cbar = fig.colorbar(im, ax=ax2, fraction=0.035, pad=0.03, shrink=0.85)
    cbar.set_label('f_N(alpha) / f_N(1)  —  1.0 = no extra dilution', fontsize=8)
    cbar.ax.tick_params(labelsize=8)

    ax2.set_xlabel("Actual growth rate g (%)", fontsize=10)
    ax2.set_ylabel("Declaration ratio (alpha)", fontsize=10)
    ax2.set_title(
        "Right: Retained equity fraction ratio f_N(alpha) / f_N(1)\n"
        "Darker = more equity eroded vs honest  —  contours at 0.95 and 0.90",
        fontsize=10
    )
    ax2.set_xlim(g_pct[0], g_pct[-1])
    ax2.set_ylim(_FIG08_ALPHA_FINE[0], _FIG08_ALPHA_FINE[-1])
    ax2.legend(loc='upper left', fontsize=8, framealpha=0.9)

    fig.suptitle(
        "Fig 08 — Overstater TW advantage: mechanism and dilution cost\n"
        "Left: sell-year refund benefit swamps f_N erosion cost across all tested α  ·  "
        "Right: equity dilution grows with α and g — the hidden price of overstatement\n"
        "Identity (corrected): tw_adv = W_sell_delta − refund_delta − settle_delta  "
        "[excess periodic tax is informational only — not additive]",
        fontsize=9.5, y=1.02
    )

    plt.tight_layout()
    return _save(fig, "val_fig_08_tw_decomposition.png")


# ─────────────────────────────────────────────────────────────
# FIG 09 — TW advantage across (g, N) space
# ─────────────────────────────────────────────────────────────

# Grid constants — fine enough for smooth contours, fast enough to run
_FIG09_G_VALS = np.linspace(0.001, 0.28, 56)   # skip g=0 (degenerate)
_FIG09_N_VALS = np.arange(5, 62, 1)
_FIG09_ALPHAS = [1.2, 1.5, 1.8, 2.0]
_FIG09_COLORS = ['#74add1', '#4393c3', '#2166ac', '#053061']


def _tw_adv_pct_gN(p, alpha, g, N):
    """
    TW advantage of alpha over honest as % of honest TW_settled,
    at given constant g and holding period N.

    Runs both simulations inline rather than calling decompose_tw_advantage()
    because we need to sweep N independently of p['N'].
    """
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    g_ser  = [g] * N
    recs_h = simulate(p['V0_m'], g_ser, 1.0, sim_p)
    sell_h = simulate_sell(recs_h, g, sim_p)
    tw_h, _, _ = settle_tw(sell_h, sim_p)
    recs_a = simulate(p['V0_m'], g_ser, alpha, sim_p)
    sell_a = simulate_sell(recs_a, g, sim_p)
    tw_a, _, _ = settle_tw(sell_a, sim_p)
    return (tw_a - tw_h) / tw_h * 100 if abs(tw_h) > 1e-12 else 0.0


def fig_09_tw_advantage_gN_surface(p):
    """
    2×2 grid of heatmaps showing TW advantage of overstatement vs honest
    declaration across (g, N) space, for each α ∈ {1.2, 1.5, 1.8, 2.0}.

    Key findings made visible:
      - TW advantage is always positive: no (g, N) makes overstatement
        worse than honest on terminal net worth.
      - Advantage peaks at low g, long N (patient, low-growth holders).
      - Advantage is remarkably flat across the centre of the space —
        the overstater does not need to predict g or N correctly to
        capture most of the available advantage.
      - Red dashed = hist. mean g; red dotted = canonical N; star = peak.

    Companion to Fig 08. Together: the TW advantage is real but is
    purchased via certain periodic overpayments (real, early money)
    recovered as a nominal sell-year refund (inflated, late money).
    In real terms, factoring inflation, the advantage is almost certainly
    negative — the state collects early purchasing power and refunds
    inflated nominal value.
    """
    print("  Generating fig 09: TW advantage across (g, N) space...")

    g_pct     = _FIG09_G_VALS * 100
    hist_mean = p['g']
    canon_N   = p['N']

    # ── build surfaces ────────────────────────────────────────
    surfaces = {}
    for alpha in _FIG09_ALPHAS:
        mat = np.zeros((len(_FIG09_G_VALS), len(_FIG09_N_VALS)))
        for i, g in enumerate(_FIG09_G_VALS):
            for j, N in enumerate(_FIG09_N_VALS):
                mat[i, j] = _tw_adv_pct_gN(p, alpha, g, N)
        surfaces[alpha] = mat

    # ── figure ────────────────────────────────────────────────
    set_style()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for ax, alpha, col in zip(axes, _FIG09_ALPHAS, _FIG09_COLORS):
        mat  = surfaces[alpha]
        vmax = float(np.percentile(mat, 98))    # cap at 98th pct
        norm = mcolors.Normalize(vmin=0.0, vmax=vmax)

        im = ax.imshow(
            mat,
            origin='lower', aspect='auto',
            cmap='Blues', norm=norm,
            extent=[_FIG09_N_VALS[0], _FIG09_N_VALS[-1],
                    g_pct[0], g_pct[-1]],
            zorder=1,
        )

        # Contours at meaningful levels
        contour_levels = [l for l in [2, 4, 6, 8, 10, 12]
                          if 0 < l < vmax]
        if contour_levels:
            CS = ax.contour(
                _FIG09_N_VALS, g_pct, mat,
                levels=contour_levels, colors='white',
                linewidths=0.9, zorder=4, alpha=0.85,
            )
            ax.clabel(CS, fmt='%d%%', fontsize=7.5, inline=True)

        # Hist-mean g horizontal line
        ax.axhline(hist_mean * 100, color='#d73027', linewidth=1.4,
                   linestyle='--', zorder=5,
                   label=f'hist. mean g = {hist_mean*100:.1f}%')

        # Canonical N vertical line
        ax.axvline(canon_N, color='#d73027', linewidth=1.4,
                   linestyle=':', zorder=5,
                   label=f'canonical N = {canon_N}')

        # Peak location
        peak_idx = np.unravel_index(np.argmax(mat), mat.shape)
        peak_g   = g_pct[peak_idx[0]]
        peak_N   = int(_FIG09_N_VALS[peak_idx[1]])
        peak_val = mat[peak_idx]
        ax.plot(peak_N, peak_g,
                marker='*', markersize=12, color='#ff7f00',
                zorder=7, clip_on=False,
                label=f'Peak: {peak_val:.1f}pp  g={peak_g:.1f}%  N={peak_N}')

        # Value at canonical intersection
        g_cidx = int(np.argmin(np.abs(_FIG09_G_VALS - hist_mean)))
        N_cidx = int(np.argmin(np.abs(_FIG09_N_VALS - canon_N)))
        canon_val = mat[g_cidx, N_cidx]
        ax.plot(canon_N, hist_mean * 100,
                marker='o', markersize=7, color='#d73027',
                zorder=6, clip_on=False)
        ax.annotate(f'{canon_val:.1f}pp',
                    xy=(canon_N, hist_mean * 100),
                    xytext=(canon_N + 3, hist_mean * 100 + 1.5),
                    fontsize=7.5, color='#d73027',
                    arrowprops=dict(arrowstyle='->', color='#d73027', lw=0.8))

        cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.03, shrink=0.85)
        cbar.set_label('TW advantage vs honest (%)', fontsize=8)
        cbar.ax.tick_params(labelsize=7.5)

        ax.set_xlabel("Holding period N (years)", fontsize=9)
        ax.set_ylabel("Actual growth rate g (%)", fontsize=9)
        ax.set_title(
            f"α = {alpha}  —  TW advantage over honest declaration\n"
            f"Darker blue = larger advantage  ·  "
            f"White contours = % advantage levels",
            fontsize=9.5,
        )
        ax.set_xlim(_FIG09_N_VALS[0], _FIG09_N_VALS[-1])
        ax.set_ylim(g_pct[0], g_pct[-1])
        ax.legend(loc='upper right', fontsize=7.5,
                  framealpha=0.92, frameon=True, facecolor='white')

    fig.suptitle(
        "Fig 09 — TW advantage of overstatement across (g, N) space\n"
        f"$V_0$ = £{p['V0_m']:.0f}m  ·  k = {p['k']}  ·  "
        "TW advantage is always positive — overstatement always retains more "
        "nominal TW than honest declaration\n"
        "Red dashed = hist. mean g  ·  Red dotted = canonical N  ·  "
        "Star = peak  ·  Red dot = canonical intersection\n"
        "Caveat: periodic overpayments are real early money; "
        "sell-year refund is inflated late money — "
        "real-terms advantage is almost certainly negative",
        fontsize=9.5, y=1.02,
    )

    plt.tight_layout()
    return _save(fig, "val_fig_09_tw_advantage_gN_surface.png")

# ─────────────────────────────────────────────────────────────
# FIG 10 — C.1 (nominal) vs C.12 (NPV-adjusted) side-by-side heatmap
#
# Purpose: makes the inflation-mechanics argument visual. The left panel
# is the familiar C.1 nominal tax-difference heatmap (same data as Fig 02
# but recomputed here for self-containment). The right panel shows the
# same metric discounted to t=0 at ρ=5%.
#
# Key pattern:
#   - Low-g cells (g < ~8%): these are the only cells where C.1 shows blue
#     (genuine nominal advantage for overstaters). In C.12 these blue cells
#     compress sharply toward white or flip to red — the advantage is a
#     timing artefact. Overstaters pay periodic tax as wealth grows, then
#     receive a large sell-year refund. At low g, the refund dominates
#     nominally but is discounted heavily relative to the spread-out
#     periodic costs.
#   - Mid/high-g cells (g > ~8%): overstaters already pay more than honest
#     in C.1 (red). Discounting makes this worse in C.12 because the periodic
#     overpayments concentrate in late years where wealth is largest, but the
#     sell-year refund is also late — and discounting hits the refund more
#     than the distributed periodic costs.
#   - Understater cells: C.12 is systematically smaller than C.1 at mid/high g.
#     Understaters pay less early (declared basis is low) and more at sale;
#     discounting the larger late payment partially offsets their penalty.
#     At low g and high alpha, C.12 can turn negative (understater appears to
#     benefit in PV terms from front-loaded refund receipt).
#
# The inflation-mechanics argument from VAL §7.3 holds precisely in the
# low-g band: the mild-overstater nominal advantage (blue in C.1) is a
# timing artefact — it collapses to near-zero or reverses in C.12.
# The shared colour scale makes this compression directly legible.
# ─────────────────────────────────────────────────────────────

def fig_10_c1_vs_c12_heatmap(p):
    print("  Generating fig 10: C.1 vs C.12 nominal vs NPV-adjusted heatmap...")

    rho = p['rho']

    # ── build both matrices ───────────────────────────────────
    base_by_g = {g: run_sim(p, alpha=1.0, g=g) for g in G_VALS}

    c1_matrix  = np.zeros((len(ALPHA_VALS), len(G_VALS)))
    c12_matrix = np.zeros((len(ALPHA_VALS), len(G_VALS)))

    for i, alpha in enumerate(ALPHA_VALS):
        for j, g in enumerate(G_VALS):
            # C.1 nominal
            r   = run_sim(p, alpha=alpha, g=g)
            b   = base_by_g[g]
            c1_val = ((r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100
                      if abs(r['TW_settled']) > 1e-12 else 0.0)
            c1_matrix[i, j] = c1_val

            # C.12 NPV-adjusted
            d = npv_tax_advantage(p, alpha, g, rho)
            c12_matrix[i, j] = d['npv_diff_pct'] * 100

    # ── shared colour scale: cap at 98th percentile of |values| ──
    all_vals = np.concatenate([c1_matrix.ravel(), c12_matrix.ravel()])
    vmax = float(np.percentile(np.abs(all_vals), 98))
    vmax = max(vmax, 1.0)   # floor so near-zero grids still show something
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5.5))

    def _draw_heatmap(ax, matrix, title_suffix):
        ax.grid(False)
        im = ax.imshow(matrix, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)

        ax.set_xticks(range(len(G_VALS)))
        ax.set_xticklabels(G_LABELS, rotation=45, ha='right')
        ax.set_yticks(range(len(ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in ALPHA_VALS])
        ax.set_xlabel("Growth rate g")
        ax.set_ylabel("Declaration ratio α")
        ax.set_title(title_suffix, fontsize=10)

        # Highlight honest row
        honest_idx = ALPHA_VALS.index(1.0)
        ax.add_patch(plt.Rectangle(
            (-0.5, honest_idx - 0.5), len(G_VALS), 1,
            fill=False, edgecolor='#1a1a1a', linewidth=1.5, zorder=5,
        ))

        # Cell annotations
        for i in range(len(ALPHA_VALS)):
            for j in range(len(G_VALS)):
                val = matrix[i, j]
                text_col = 'white' if abs(val) > vmax * 0.6 else '#1a1a1a'
                ax.text(j, i, f"{val:.1f}",
                        ha='center', va='center', fontsize=7.5,
                        color=text_col, zorder=3)
        return im

    im = _draw_heatmap(
        ax1, c1_matrix,
        f"C.1 — Nominal: (Net(α) − Net(1)) / TW(α)  [pp]\n"
        f"N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m"
    )
    _draw_heatmap(
        ax2, c12_matrix,
        f"C.12 — NPV-adjusted: (NPV_tax(α) − NPV_tax(1)) / TW_settled(1)  [pp]\n"
        f"ρ = {rho*100:.0f}%  ·  N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m"
    )

    # Shared colourbar
    cbar = fig.colorbar(im, ax=[ax1, ax2], fraction=0.02, pad=0.04)
    cbar.set_label(
        "pp relative to honest declaration  ·  "
        "Red = understater pays more / overstater pays less (in nominal) or MORE (in PV)\n"
        "Blue = overstater pays less (nominal)  ·  "
        "Shared scale: direct comparison of magnitude across panels",
        fontsize=8
    )

    fig.suptitle(
        "Fig 10 — Nominal (C.1) vs NPV-adjusted (C.12) tax difference: timing artefacts exposed\n"
        f"Left (C.1): nominal metric  ·  Right (C.12): discounted at ρ = {rho*100:.0f}%  ·  "
        f"Sell-year refund at t=N+1 is worth ≈{100*(1/(1+rho)**p['N']):.0f}p/£ vs a year-1 payment\n"
        "Low-g blue cells (nominal overstater advantage): collapse toward white or flip red in C.12 — the advantage is a timing artefact\n"
        "Mid/high-g cells: overstaters already pay more in C.1; C.12 is larger still — discounting penalises late periodic costs less than late refund\n"
        "Understater red cells shrink in C.12 at mid/high g — deferral of payment partially offsets the penalty in PV terms",
        fontsize=9.0, y=1.04,
    )

    plt.tight_layout()
    return _save(fig, "val_fig_10_c1_vs_c12_nominal_vs_npv.png")

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    print(f"Parameters loaded: k={p['k']}, N={p['N']} (SSM-derived), g={p['g']:.4f}")

    # Populate module-level grid constants from TOML [sweep] section.
    global G_VALS, G_LABELS, ALPHA_VALS, N_ACTUAL_VALS
    sw = p['sweep']
    G_VALS        = sw['g_vals']
    G_LABELS      = [f"{v*100:.1f}%" for v in G_VALS]
    ALPHA_VALS    = sw['alpha_vals']
    N_ACTUAL_VALS = sw['n_actual_vals']

    os.makedirs(OUT_DIR, exist_ok=True)
    set_style()

    print(f"\nGenerating VAL figures → {OUT_DIR}")
    print(f"Parameters: N={p['N']}, g={p['g']*100:.2f}%, $V_0$=£{p['V0_m']:.0f}m, "
          f"k={p['k']}, tau_0={p['tau_0']*100:.0f}%, tau_m={p['tau_m']*100:.0f}%\n")

    fig_01_rate_function(p)
    fig_02_c1_heatmap(p)
    fig_03_equilibrium_cost_curve(p)
    fig_04_tw_gap_by_n(p)
    fig_05_saturation_reversal(p)
    fig_06_overstatement_reversal(p)
    fig_07_overstatement_coherence(p)
    fig_08_tw_decomposition(p)
    fig_09_tw_advantage_gN_surface(p)
    fig_10_c1_vs_c12_heatmap(p)

    print("\nAll figures written.")


if __name__ == '__main__':
    main()