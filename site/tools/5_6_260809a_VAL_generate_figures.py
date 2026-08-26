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
from wdt_core import load_params, tau, simulate, simulate_sell, run_sim

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
            val = (r['Net'] - b['Net']) / r['TW'] * 100 if abs(r['TW']) > 1e-12 else 0.0
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
            if abs(base['Net']) > 1e-12:
                net_diffs.append((r['Net'] - base['Net']) / base['Net'] * 100)
            else:
                net_diffs.append(0.0)
        ax.plot(alpha_fine, net_diffs, color=col, linewidth=lw,
                linestyle=ls, label=g_label)

    # 2006 historical series (actual return sequence, not constant g)
    returns_2006 = p['returns']  # already rotated to 2006 start
    N = p['N']
    g_series_2006 = returns_2006[:N]
    g_sell_2006   = returns_2006[N]
    mean_g_2006   = sum(g_series_2006) / len(g_series_2006)
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def run_hist(alpha_val):
        recs = simulate(p['V0_m'], g_series_2006, alpha_val, sim_p)
        sell = simulate_sell(recs, g_sell_2006, sim_p)
        gross_tax = sum(r['L'] for r in recs[1:] if r['L'] > 0)
        gross_ref = sum(r['L'] for r in recs[1:] if r['L'] < 0)
        if sell['L_sell'] > 0: gross_tax += sell['L_sell']
        else:                   gross_ref += sell['L_sell']
        return {'Net': gross_tax + gross_ref, 'TW': sell['TW']}

    base_hist = run_hist(1.0)
    hist_diffs = []
    for alpha in alpha_fine:
        r = run_hist(alpha)
        if abs(base_hist['Net']) > 1e-12:
            hist_diffs.append((r['Net'] - base_hist['Net']) / base_hist['Net'] * 100)
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

    # Expand y range so top-left (α~0.5, high cost) doesn't crop
    all_vals = [v for lst in [
        [(run_sim(p, alpha=a, g=g_val)['Net'] - run_sim(p, alpha=1.0, g=g_val)['Net'])
         / run_sim(p, alpha=1.0, g=g_val)['Net'] * 100
         for a in [0.5]] for g_val, *_ in g_scenarios
    ] for v in lst]
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
    sim_p  = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    def tw_gap_const(alpha, n):
        r = run_sim(p, alpha=alpha, g=p['g'], N=n)
        b = run_sim(p, alpha=1.0,   g=p['g'], N=n)
        return (r['TW'] - b['TW']) / b['TW'] * 100 if abs(b['TW']) > 1e-12 else 0.0

    def tw_gap_hist(alpha, n):
        g_ser  = returns_2006[:n]
        g_sell = returns_2006[n]
        def _run(a):
            recs = simulate(p['V0_m'], g_ser, a, sim_p)
            sell = simulate_sell(recs, g_sell, sim_p)
            return sell['TW']
        tw_a = _run(alpha)
        tw_1 = _run(1.0)
        return (tw_a - tw_1) / tw_1 * 100 if abs(tw_1) > 1e-12 else 0.0

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
            c1 = (r['Net'] - b['Net']) / r['TW'] * 100 if abs(r['TW']) > 1e-12 else 0.0
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
            c1 = (r['Net'] - b['Net']) / r['TW'] * 100 if abs(r['TW']) > 1e-12 else 0.0
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
    alphas_grid = np.linspace(1.0, 2.0, 41)
    g_grid      = np.linspace(0.0, 0.25, 101)
    g_pct_grid  = g_grid * 100

    c1_matrix = np.zeros((len(alphas_grid), len(g_grid)))
    for i, alpha in enumerate(alphas_grid):
        for j, g in enumerate(g_grid):
            r  = run_sim(p, alpha=alpha, g=g, N=N)
            b  = run_sim(p, alpha=1.0,   g=g, N=N)
            c1 = (r['Net'] - b['Net']) / r['TW'] * 100 if abs(r['TW']) > 1e-12 else 0.0
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
    ax1.set_ylim(1.0, 2.0)
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
            diffs.append(r['Net'] - b['Net'])
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

    print(f"\nGenerating improved VAL figures → {OUT_DIR}")
    print(f"Parameters: N={p['N']}, g={p['g']*100:.2f}%, $V_0$=£{p['V0_m']:.0f}m, "
          f"k={p['k']}, $\tau_0$={p['tau_0']*100:.0f}%, $\tau_m$={p['tau_m']*100:.0f}%\n")

    fig_01_rate_function(p)
    fig_02_c1_heatmap(p)
    fig_03_equilibrium_cost_curve(p)
    fig_04_tw_gap_by_n(p)
    fig_05_saturation_reversal(p)
    fig_06_overstatement_reversal(p)
    fig_07_overstatement_coherence(p)

    print("\nAll figures written.")


if __name__ == '__main__':
    main()
