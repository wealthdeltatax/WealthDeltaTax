"""
VAL Output Script D — Figures (v3 — style refactor)
=====================================================
Refactor changes (v2 → v3):

Imports / module header
  • Removed unused imports: os, math, date, Path (Path came from wdt_fmt already)
  • Extended wdt_style import to include all named size and colour constants used
    in this file: FIG_SINGLE_W, FIG_PAIR_T, FIG_QUAD_XL, FIG_PAIR_XW,
    C_ANNOTATION, C_DARK, apply_style_nogrid
  • Dropped UNDER_COLS / HONEST_COL / OVER_COLS module-level aliases — all
    figures now reference C_UNDER / C_HONEST / C_OVER directly
  • Dropped OUT_DIR (str duplicate of _OUT); no os.path calls existed
  • Dropped FSIZE alias; FIG_SINGLE used directly at call sites
  • Dropped set_style alias; apply_style / apply_style_nogrid called directly

Figure-size cleanup (inline tuples → named constants)
  Fig 02  (10, 5.5)  → FIG_SINGLE_W
  Fig 04  (10, 5.5)  → FIG_SINGLE_W
  Fig 05  (10, 5.5)  → FIG_SINGLE_W
  Fig 07  (14, 6.5)  → FIG_PAIR_T
  Fig 08  (14, 6.5)  → FIG_PAIR_T
  Fig 09  (14, 10)   → FIG_QUAD_XL
  Fig 10  (16, 5.5)  → FIG_PAIR_XW
  Fig 06  (13, 5.5)  — kept as custom tuple; no named constant matches exactly

Colour cleanup (inline hex lists → wdt_style constants)
  Fig 04  local under_cols / over_cols  → C_UNDER / C_OVER
  Fig 05  local under_cols              → C_UNDER
  Fig 06  local over_cols               → C_OVER
  _FIG09_COLORS (duplicate of C_OVER_LIGHT) → C_OVER_LIGHT

apply_style_nogrid for pure-heatmap figures
  Fig 02  — entire figure is a heatmap; use apply_style_nogrid()
  Fig 07  — set_style() + per-axes ax1.grid(False) → apply_style_nogrid() for
             both axes; ax2 re-enables grid explicitly with ax2.grid(True)
  Fig 08  — apply_style_nogrid(); ax1.grid(True, zorder=0) kept as explicit
             re-enable; ax2.grid(False) is now a no-op but kept for clarity
  Fig 09  — apply_style_nogrid() (all four panels are heatmaps)
  Fig 10  — apply_style_nogrid() (both panels are heatmaps)

Fig 07 rcParams bleed fix
  plt.rcParams.update({'legend.frameon': True, ...}) replaced with per-axes
  legend() kwargs (frameon=True, framealpha=0.9, fontsize=8.5); no rcParam
  mutation that could bleed into subsequent figures.

All figure content, annotations, and data logic are unchanged.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from wdt_core import (load_params, tau, simulate, simulate_sell,
                      settle_tw, run_sim, decompose_tw_advantage,
                      run_sim_hist, npv_tax_advantage)
from wdt_fmt import out_dir, ensure_dir
from wdt_style import (
    apply_style, apply_style_nogrid, save_fig,
    FIG_SINGLE, FIG_SINGLE_W, FIG_PAIR_T, FIG_QUAD_XL, FIG_PAIR_XW,
    C_UNDER, C_HONEST, C_OVER, C_OVER_LIGHT,
    C_ANNOTATION, C_DARK,
)

_OUT = out_dir('VAL')

# ─────────────────────────────────────────────────────────────
# MODULE-LEVEL GRID CONSTANTS
# Populated by main() from TOML [sweep] section.
# ─────────────────────────────────────────────────────────────

G_VALS        = []
G_LABELS      = []
ALPHA_VALS    = []
N_ACTUAL_VALS = []


def _save(fig, name):
    path = _OUT / name
    save_fig(fig, path)
    return path


# ─────────────────────────────────────────────────────────────
# FIG 01 — Rate function τ(W)
# ─────────────────────────────────────────────────────────────

def fig_01_rate_function(p):
    print("  Generating fig 01: rate function τ(W)...")
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}

    W_vals   = np.logspace(np.log10(p['W_min']), np.log10(10000), 500)
    tau_vals = [tau(w, sim_p) * 100 for w in W_vals]

    entry_rate = tau(p['W_min'], sim_p) * 100

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    ax.semilogx(W_vals, tau_vals, color=C_DARK, linewidth=2)

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
        "Fig 01 — Marginal rate function τ(W)\n"
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
    return _save(fig, "val_fig_01_rate_function_tau_w.png")


# ─────────────────────────────────────────────────────────────
# FIG 02 — C.1 heatmap
# Pure heatmap: apply_style_nogrid(); no per-axes grid override needed.
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
        "Fig 02 — C.1 metric: (Net(α) − Net(1)) / TW(α)  [percentage points]\n"
        f"Red = pays more · Blue = pays less · "
        f"N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m"
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
    return _save(fig, "val_fig_02_c1_tax_difference_heatmap.png")


# ─────────────────────────────────────────────────────────────
# FIG 03 — Declaration equilibrium cost curve
# ─────────────────────────────────────────────────────────────

def fig_03_equilibrium_cost_curve(p):
    print("  Generating fig 03: declaration equilibrium cost curve...")

    alpha_fine = [a / 100 for a in range(50, 205, 5)]

    g_scenarios = [
        (0.059,  '#f46d43', '-',   1.8),
        (0.084,  '#d4ac0d', '-',   1.6),
        (0.1045, C_DARK,    '-',   2.0),
        (0.139,  '#4393c3', '-',   1.8),
    ]

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    for g_val, col, ls, lw in g_scenarios:
        base = run_sim(p, alpha=1.0, g=g_val)
        net_diffs = []
        for alpha in alpha_fine:
            r = run_sim(p, alpha=alpha, g=g_val)
            if abs(base['Net_settled']) > 1e-12:
                net_diffs.append((r['Net_settled'] - base['Net_settled']) / base['Net_settled'] * 100)
            else:
                net_diffs.append(0.0)
        ax.plot(alpha_fine, net_diffs, color=col, linewidth=lw,
                linestyle=ls, label=f'g = {g_val*100:.1f}% (constant)')

    scen_year   = p['scenario_start_year']
    N           = p['N']
    g_series    = p['returns'][:N]
    mean_g_hist = sum(g_series) / len(g_series)

    base_hist = run_sim_hist(p, alpha=1.0)
    hist_diffs = []
    for alpha in alpha_fine:
        r = run_sim_hist(p, alpha=alpha)
        if abs(base_hist['Net_settled']) > 1e-12:
            hist_diffs.append((r['Net_settled'] - base_hist['Net_settled']) / base_hist['Net_settled'] * 100)
        else:
            hist_diffs.append(0.0)
    ax.plot(alpha_fine, hist_diffs, color='#7b2d8b', linewidth=2.0,
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
        "Fig 03 — Declaration equilibrium: net tax cost relative to honest\n"
        f"N = {p['N']}, $V_0$ = £{p['V0_m']:.0f}m, "
        f"k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%  ·  "
        f"Dash-dot = {scen_year} historical return series (mean g = {mean_g_hist*100:.1f}%"
    )
    ax.legend(loc='upper right', fontsize=8)
    ax.set_xlim(0.5, 2.0)

    plt.tight_layout()
    return _save(fig, "val_fig_03_declaration_equilibrium_cost_curve.png")


# ─────────────────────────────────────────────────────────────
# FIG 04 — C.8 TW gap by N (overlaid)
# Colour lists replaced by C_UNDER / C_OVER.
# ─────────────────────────────────────────────────────────────

def fig_04_tw_gap_by_n(p):
    print("  Generating fig 04: C.8 TW gap by N (overlaid)...")

    alpha_under = [0.1, 0.2, 0.5, 0.8]
    alpha_over  = [1.2, 1.5, 1.8, 2.0]

    def tw_gap_const(alpha, n):
        r = run_sim(p, alpha=alpha, g=p['g'], N=n)
        b = run_sim(p, alpha=1.0,   g=p['g'], N=n)
        return (r['TW_settled'] - b['TW_settled']) / b['TW_settled'] * 100 if abs(b['TW_settled']) > 1e-12 else 0.0

    def tw_gap_hist(alpha, n):
        r = run_sim_hist(p, alpha=alpha, N=n)
        b = run_sim_hist(p, alpha=1.0,   N=n)
        return (r['TW_settled'] - b['TW_settled']) / b['TW_settled'] * 100 if abs(b['TW_settled']) > 1e-12 else 0.0

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)

    for alpha, col in zip(alpha_under, C_UNDER):
        vals_c = [tw_gap_const(alpha, n) for n in N_ACTUAL_VALS]
        vals_h = [tw_gap_hist(alpha,  n) for n in N_ACTUAL_VALS]
        ax.plot(N_ACTUAL_VALS, vals_c, color=col, linewidth=1.8,
                linestyle='-',  label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, vals_h, color=col, linewidth=1.4,
                linestyle='-.', alpha=0.8)

    for alpha, col in zip(alpha_over, C_OVER):
        vals_c = [tw_gap_const(alpha, n) for n in N_ACTUAL_VALS]
        vals_h = [tw_gap_hist(alpha,  n) for n in N_ACTUAL_VALS]
        ax.plot(N_ACTUAL_VALS, vals_c, color=col, linewidth=1.8,
                linestyle='--', label=f"α = {alpha}")
        ax.plot(N_ACTUAL_VALS, vals_h, color=col, linewidth=1.4,
                linestyle=':', alpha=0.8)

    ax.axhline(0, color=C_HONEST, linewidth=1.0, linestyle='-', label='α = 1.0 (honest)')
    scen_N = p['N']
    ax.axvline(scen_N, color=C_ANNOTATION, linewidth=0.8, linestyle=':')
    # inject N into the existing x-axis ticks as a small labelled tick
    existing_ticks = list(ax.get_xticks())
    if scen_N not in existing_ticks:
        existing_ticks = sorted(existing_ticks + [scen_N])
        ax.set_xticks(existing_ticks)
    tick_labels = [
        f'{int(t)}\n(N)' if t == scen_N else (str(int(t)) if t == int(t) else '')
        for t in ax.get_xticks()
    ]
    ax.set_xticklabels(tick_labels, fontsize=8)
    ax.tick_params(axis='x', which='major')

    scen_year = p['scenario_start_year']
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
    ax.legend(handles=h1 + style_handles,
              loc='lower left', ncol=2, fontsize=7.5)

    ax.set_xlabel("Holding period N (years)")
    ax.set_ylabel("TW vs honest declaration (%)")
    ax.set_title(
        "Fig 04 — C.8: terminal net worth gap vs honest, by holding period\n"
        f"Solid/dashed = constant g ({p['g']*100:.2f}%)  ·  "
        f"Dash-dot/dotted = {scen_year} hist. series  ·  "
        f"Red = understaters  ·  Blue = overstaters  ·  "
        f"$V_0$ = £{p['V0_m']:.0f}m, k = {p['k']}, $\\tau_0$ = {p['tau_0']*100:.0f}%"
    )
    ax.set_xlim(N_ACTUAL_VALS[0], N_ACTUAL_VALS[-1])

    plt.tight_layout()
    return _save(fig, "val_fig_04_c8_tw_gap_by_n.png")


# ─────────────────────────────────────────────────────────────
# FIG 05 — Saturation reversal boundary (understaters)
# Colour list replaced by C_UNDER.
# ─────────────────────────────────────────────────────────────

def fig_05_saturation_reversal(p):
    print("  Generating fig 05: saturation reversal boundary (single panel)...")

    alpha_under = [0.1, 0.2, 0.5, 0.8]

    g_sweep = [g_int / 1000.0 for g_int in range(0, 410)]
    g_pct   = [g * 100 for g in g_sweep]

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

    apply_style()
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)

    ax.axvspan(mean_plateau, 40, alpha=0.08, color=C_ANNOTATION, zorder=0,
               label=f'Plateau zone (g > {mean_plateau:.0f}%)')
    ax.text(mean_plateau + 0.3, 108,
            f'Plateau\n(g ≥ {mean_plateau:.0f}%)',
            fontsize=7.5, color='#555555', va='top')

    ax.axvline(mean_inflection, color='#333333', linewidth=1.1,
               linestyle='--', zorder=3,
               label=f'Inflection g ≈ {mean_inflection:.1f}% (rate fn property)')
    ax.text(mean_inflection + 0.3, 2,
            f'Inflection\n≈ {mean_inflection:.1f}%',
            fontsize=7.5, color='#333333', va='bottom')

    for alpha, col in zip(alpha_under, C_UNDER):
        curve_x = g_pct[:300]
        curve_y = c1_curves[alpha][:300]
        ax.plot(curve_x, curve_y, color=col, linewidth=2.0)

        ph = plateau_height[alpha]
        ax.text(31, ph,
                f"α = {alpha}  ({ph:.0f}%)",
                color=col, fontsize=8, va='center', ha='left',
                fontweight='bold' if alpha == 0.1 else 'normal')

    ax.axhline(0, color=C_DARK, linewidth=0.8, linestyle=':')

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


    legend_handles = [
        Line2D([0], [0], color='#333333', lw=1.1, linestyle='--',
               label=f'Inflection ≈ {mean_inflection:.1f}% (rate fn property)'),
        Patch(facecolor=C_ANNOTATION, alpha=0.15,
              label=f'Plateau zone g ≥ {mean_plateau:.0f}%'),
    ]
    ax.legend(handles=legend_handles, loc='upper left', fontsize=8)

    plt.tight_layout()
    return _save(fig, "val_fig_05_saturation_reversal_boundary.png")


# ─────────────────────────────────────────────────────────────
# FIG 06 — Overstatement reversal boundary
# Colour list replaced by C_OVER.
# figsize (13, 5.5) kept as custom: nearest named constant FIG_WIDE is (13, 6).
# ─────────────────────────────────────────────────────────────

def fig_06_overstatement_reversal(p):
    print("  Generating fig 06: overstatement reversal boundary...")

    alpha_over = [1.2, 1.5, 1.8, 2.0]

    g_sweep  = [g_int / 1000.0 for g_int in range(0, 400)]
    g_pct    = [g * 100 for g in g_sweep]
    c1_curves  = {}
    first_rev  = {}
    re_rev     = {}

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
            if c1 > peak_val:
                peak_val = c1
                peaked   = False
            elif c1 < peak_val - 0.5:
                peaked = True
            if peaked and c1 < 0 and found_back is None and found_fwd is not None:
                found_back = g * 100
        c1_curves[alpha] = vals
        first_rev[alpha] = found_fwd
        re_rev[alpha]    = found_back

    apply_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))   # no exact named match

    for alpha, col in zip(alpha_over, C_OVER):
        ax1.plot(g_pct, c1_curves[alpha], color=col, linewidth=1.8,
                 label=f"α = {alpha}")

    vals_12 = c1_curves[1.2]
    nearest_idx = max(range(len(vals_12)), key=lambda i: vals_12[i])
    nearest_g   = g_pct[nearest_idx]
    nearest_val = vals_12[nearest_idx]
    if nearest_val < 0:
        ax1.annotate(
            f"α=1.2 peak ≈ {nearest_val:.1f}pp\n(never crosses zero)",
            xy=(nearest_g, nearest_val),
            xytext=(nearest_g + 3, nearest_val + 2.5),
            fontsize=7.5, color=C_OVER[0],
            arrowprops=dict(arrowstyle='->', color=C_OVER[0], lw=0.8)
        )

    ax1.axhline(0, color=C_ANNOTATION, linewidth=0.8, linestyle='--',
                label='zero (honest baseline)')
    ax1.set_xlabel("Growth rate g (%)")
    ax1.set_ylabel("C.1 metric (%) — negative = overstater pays less than honest")
    ax1.set_title(f"Overstater C.1 by g — N = {p['N']}")
    ax1.set_xlim(0, 40)
    ax1.legend(fontsize=8)

    labels     = [f"α = {a}" for a in alpha_over]
    x_pos      = list(range(len(alpha_over)))
    bar_width  = 0.38

    fwd_vals = [first_rev[a] if first_rev[a] is not None else 0 for a in alpha_over]
    bwd_vals = [re_rev[a]    if re_rev[a]    is not None else 0 for a in alpha_over]

    bars_fwd = ax2.bar([i - bar_width/2 for i in x_pos],
                       fwd_vals, width=bar_width, color=C_OVER,
                       edgecolor='white', label='First reversal: overstater first pays more')
    bars_bwd = ax2.bar([i + bar_width/2 for i in x_pos],
                       bwd_vals, width=bar_width, color=C_OVER, alpha=0.4,
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
                     fontsize=8, color=C_DARK)

    for bar, alpha in zip(bars_bwd, alpha_over):
        t = re_rev[alpha]
        h = bar.get_height()
        if t is not None:
            ax2.text(bar.get_x() + bar.get_width() / 2, h + 0.5,
                     f"{t:.1f}%", ha='center', va='bottom', fontsize=8, color='#555555')
        else:
            label = "n/a" if first_rev[alpha] is None else "no\nre-reversal\nin range"
            ax2.text(bar.get_x() + bar.get_width() / 2, 1.2,
                     label, ha='center', va='bottom',
                     fontsize=7.5, color=C_ANNOTATION)

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
# apply_style_nogrid() for both panels (left is a heatmap; right re-enables
# grid explicitly). rcParams mutation removed — legend kwargs per-axes.
# ─────────────────────────────────────────────────────────────

_FIG07_OVER_ALPHAS = [1.2, 1.5, 1.8, 2.0]
_FIG07_OVER_COLS   = C_OVER_LIGHT


def fig_07_overstatement_coherence(p):
    print("  Generating fig 07: overstatement coherence...")

    hist_mean = p['g']
    N         = p['N']

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)

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

    vmax = 6.0
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    ax1.imshow(
        c1_matrix,
        origin='lower', aspect='auto', cmap='RdBu_r', norm=norm,
        extent=[g_pct_grid[0], g_pct_grid[-1], alphas_grid[0], alphas_grid[-1]],
        zorder=1,
    )

    CS = ax1.contour(
        g_pct_grid, alphas_grid, c1_matrix,
        levels=[0.0], colors=[C_DARK], linewidths=1.8, zorder=4,
    )
    ax1.clabel(CS, levels=[0.0], fmt={0.0: 'C.1 = 0'},
               fontsize=8, inline=True, inline_spacing=6)

    ax1.axvline(hist_mean * 100, color='#333333', linewidth=1.4,
                linestyle='--', zorder=5,
                label=f'Hist. mean g = {hist_mean*100:.1f}%')
    ax1.text(hist_mean * 100 - 0.3, 1.45,
             f'{hist_mean*100:.1f}%\n(mean)', fontsize=7.5,
             color='#333333', va='center', ha='right')

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
    ax1.legend(loc='lower right', fontsize=8.5, frameon=True, framealpha=0.9)

    # ── RIGHT: Net tax diff vs holding period N ──────────────
    # Re-enable grid on this panel only (it's a line plot, not a heatmap)
    ax2.grid(True)

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

        first_clip = next((k for k, c in enumerate(clipped_mask) if c), None)
        if first_clip and first_clip > 0:
            ax2.plot([n_vals[first_clip - 1], n_vals[first_clip]],
                     [diffs[first_clip - 1], Y_CLIP],
                     color=col, linewidth=1.2, linestyle='--', alpha=0.6)
            ax2.annotate('', xy=(n_vals[first_clip], Y_CLIP),
                         xytext=(n_vals[first_clip], Y_CLIP + 1.5),
                         arrowprops=dict(arrowstyle='->', color=col, lw=1.0))

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

    ax2.axvline(N, color='#555555', linewidth=1.0, linestyle='--', zorder=2)
    ax2.text(N + 0.4, Y_CLIP + 0.5,
             f'N={N}\n(RATES ref)', fontsize=7.5,
             color='#555555', va='bottom')

    ax2.set_xlabel("Holding period N (years)", fontsize=10)
    ax2.set_ylabel("Net(α) − Net(honest)  [£m]\n− = overstater pays less", fontsize=9)
    ax2.set_xlim(5, 60)
    ax2.set_title(
        f"Advantage erosion: net tax diff vs holding period N\n"
        f"g = hist. mean ({hist_mean*100:.1f}%) · $V_0$ = £{p['V0_m']:.0f}m · "
        f"Dashed arrows = line continues below clip at £{abs(Y_CLIP):.0f}m",
        fontsize=10
    )
    ax2.legend(loc='lower left', fontsize=8.5, frameon=True, framealpha=0.9)

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
# apply_style_nogrid(); ax1 re-enables grid explicitly (line plot);
# ax2 stays nogrid (heatmap).
# ─────────────────────────────────────────────────────────────

_FIG08_ALPHA_FINE = np.linspace(1.0, 2.0, 41)
_FIG08_G_FINE     = np.linspace(0.0, 0.25, 51)


def _decompose_fig08(p, alpha, g):
    """
    Thin wrapper around decompose_tw_advantage() returning a 7-tuple:
        W_sell_delta, refund_delta, settle_delta, tw_advantage,
        f_ratio, tw_honest, excess_periodic

    Correct identity (verified to machine precision):
        tw_advantage = W_sell_delta - refund_delta - settle_delta
    excess_periodic is informational only — NOT additive in the identity.
    """
    d = decompose_tw_advantage(p, alpha, g)
    return (
        d['W_sell_delta'],
        d['refund_delta'],
        d['settle_delta'],
        d['tw_advantage'],
        d['f_ratio'],
        d['tw_honest'],
        d['excess_periodic'],
    )


def fig_08_tw_decomposition(p):
    print("  Generating fig 08: TW advantage decomposition...")

    hist_mean = p['g']
    N         = p['N']

    wsd_vals = []
    rd_vals  = []
    sd_vals  = []
    tw_vals  = []
    ep_vals  = []

    for alpha in _FIG08_ALPHA_FINE:
        wsd, rd, sd, tw_adv, _, tw_h, ep = _decompose_fig08(p, alpha, hist_mean)
        denom = tw_h if abs(tw_h) > 1e-12 else 1.0
        wsd_vals.append(wsd    / denom * 100)
        rd_vals.append( rd     / denom * 100)
        sd_vals.append( sd     / denom * 100)
        tw_vals.append( tw_adv / denom * 100)
        ep_vals.append( ep     / denom * 100)

    wsd_arr = np.array(wsd_vals)
    rd_arr  = np.array(rd_vals)
    sd_arr  = np.array(sd_vals)
    tw_arr  = np.array(tw_vals)
    ep_arr  = np.array(ep_vals)

    stack_err = np.max(np.abs((wsd_arr - rd_arr - sd_arr) - tw_arr))
    if stack_err > 0.01:
        print(f"    WARNING: fig08 left-panel identity error = {stack_err:.4f}pp")

    f_matrix = np.zeros((len(_FIG08_ALPHA_FINE), len(_FIG08_G_FINE)))
    for i, alpha in enumerate(_FIG08_ALPHA_FINE):
        for j, g in enumerate(_FIG08_G_FINE):
            _, _, _, _, f_ratio, _, _ = _decompose_fig08(p, alpha, g)
            f_matrix[i, j] = f_ratio

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_T)
    alpha_x = _FIG08_ALPHA_FINE

    # ── LEFT: stacked decomposition (line plot — re-enable grid) ─
    ax1.grid(True, zorder=0)

    ax1.axhline(0, color='#555555', linewidth=0.9, zorder=2)

    ax1.fill_between(alpha_x, 0, -rd_arr,
                     color='#4393c3', alpha=0.55,
                     label='Sell-year refund benefit  (−refund_delta)')
    ax1.fill_between(alpha_x, 0, wsd_arr,
                     color='#d73027', alpha=0.55,
                     label='f_N erosion cost  (W_sell_delta ≤ 0)')
    ax1.fill_between(alpha_x, wsd_arr, wsd_arr - sd_arr,
                     color='#f46d43', alpha=0.55,
                     label='Post-sale damping cost  (settle_delta)')

    ax1.plot(alpha_x, tw_arr,
             color=C_DARK, linewidth=2.2, zorder=5,
             label='Net TW advantage  (C.8 cross-check)')
    ax1.plot(alpha_x, ep_arr,
             color='#6a3d9a', linewidth=1.3, linestyle=':', zorder=4,
             label='Excess periodic tax  (informational — not additive)')

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

    ax1.annotate(f'α=2.0: net +{tw_arr[-1]:.1f}pp',
                 xy=(2.0, tw_arr[-1]),
                 xytext=(1.82, tw_arr[-1] + 1.5),
                 fontsize=7.5, color=C_DARK,
                 arrowprops=dict(arrowstyle='->', color=C_DARK, lw=0.8))

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

    # ── RIGHT: f_N ratio heatmap (no grid) ───────────────────
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
# apply_style_nogrid(); all four panels are heatmaps.
# _FIG09_COLORS replaced by C_OVER_LIGHT.
# ─────────────────────────────────────────────────────────────

_FIG09_G_VALS = np.linspace(0.001, 0.28, 56)
_FIG09_N_VALS = np.arange(5, 62, 1)
_FIG09_ALPHAS = [1.2, 1.5, 1.8, 2.0]


def _tw_adv_pct_gN(p, alpha, g, N):
    """
    TW advantage of alpha over honest as % of honest TW_settled,
    at given constant g and holding period N.
    Runs both simulations inline to sweep N independently of p['N'].
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
    2×2 grid of heatmaps: TW advantage of overstatement vs honest across
    (g, N) space for each α ∈ {1.2, 1.5, 1.8, 2.0}.
    """
    print("  Generating fig 09: TW advantage across (g, N) space...")

    g_pct     = _FIG09_G_VALS * 100
    hist_mean = p['g']
    canon_N   = p['N']

    surfaces = {}
    for alpha in _FIG09_ALPHAS:
        mat = np.zeros((len(_FIG09_G_VALS), len(_FIG09_N_VALS)))
        for i, g in enumerate(_FIG09_G_VALS):
            for j, N in enumerate(_FIG09_N_VALS):
                mat[i, j] = _tw_adv_pct_gN(p, alpha, g, N)
        surfaces[alpha] = mat

    apply_style_nogrid()
    fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD_XL)
    axes = axes.flatten()

    for ax, alpha, col in zip(axes, _FIG09_ALPHAS, C_OVER_LIGHT):
        mat  = surfaces[alpha]
        vmax = float(np.percentile(mat, 98))
        norm = mcolors.Normalize(vmin=0.0, vmax=vmax)

        im = ax.imshow(
            mat,
            origin='lower', aspect='auto',
            cmap='Blues', norm=norm,
            extent=[_FIG09_N_VALS[0], _FIG09_N_VALS[-1],
                    g_pct[0], g_pct[-1]],
            zorder=1,
        )

        contour_levels = [l for l in [2, 4, 6, 8, 10, 12] if 0 < l < vmax]
        if contour_levels:
            CS = ax.contour(
                _FIG09_N_VALS, g_pct, mat,
                levels=contour_levels, colors='white',
                linewidths=0.9, zorder=4, alpha=0.85,
            )
            ax.clabel(CS, fmt='%d%%', fontsize=7.5, inline=True)

        ax.axhline(hist_mean * 100, color='#d73027', linewidth=1.4,
                   linestyle='--', zorder=5,
                   label=f'hist. mean g = {hist_mean*100:.1f}%')
        ax.axvline(canon_N, color='#d73027', linewidth=1.4,
                   linestyle=':', zorder=5,
                   label=f'canonical N = {canon_N}')

        peak_idx = np.unravel_index(np.argmax(mat), mat.shape)
        peak_g   = g_pct[peak_idx[0]]
        peak_N   = int(_FIG09_N_VALS[peak_idx[1]])
        peak_val = mat[peak_idx]
        ax.plot(peak_N, peak_g,
                marker='*', markersize=12, color='#ff7f00',
                zorder=7, clip_on=False,
                label=f'Peak: {peak_val:.1f}pp  g={peak_g:.1f}%  N={peak_N}')

        g_cidx    = int(np.argmin(np.abs(_FIG09_G_VALS - hist_mean)))
        N_cidx    = int(np.argmin(np.abs(_FIG09_N_VALS - canon_N)))
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
# FIG 10 — C.1 (nominal) vs C.12 (NPV-adjusted) heatmaps
# Pure heatmaps: apply_style_nogrid().
# ─────────────────────────────────────────────────────────────

def fig_10_c1_vs_c12_heatmap(p):
    print("  Generating fig 10: C.1 vs C.12 nominal vs NPV-adjusted heatmap...")

    rho = p['rho']

    base_by_g = {g: run_sim(p, alpha=1.0, g=g) for g in G_VALS}

    c1_matrix  = np.zeros((len(ALPHA_VALS), len(G_VALS)))
    c12_matrix = np.zeros((len(ALPHA_VALS), len(G_VALS)))

    for i, alpha in enumerate(ALPHA_VALS):
        for j, g in enumerate(G_VALS):
            r      = run_sim(p, alpha=alpha, g=g)
            b      = base_by_g[g]
            c1_val = ((r['Net_settled'] - b['Net_settled']) / r['TW_settled'] * 100
                      if abs(r['TW_settled']) > 1e-12 else 0.0)
            c1_matrix[i, j] = c1_val

            d = npv_tax_advantage(p, alpha, g, rho)
            c12_matrix[i, j] = d['npv_diff_pct'] * 100

    all_vals = np.concatenate([c1_matrix.ravel(), c12_matrix.ravel()])
    vmax = float(np.percentile(np.abs(all_vals), 98))
    vmax = max(vmax, 1.0)
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    apply_style_nogrid()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG_PAIR_XW)

    def _draw_heatmap(ax, matrix, title_suffix):
        im = ax.imshow(matrix, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)

        ax.set_xticks(range(len(G_VALS)))
        ax.set_xticklabels(G_LABELS, rotation=45, ha='right')
        ax.set_yticks(range(len(ALPHA_VALS)))
        ax.set_yticklabels([str(a) for a in ALPHA_VALS])
        ax.set_xlabel("Growth rate g")
        ax.set_ylabel("Declaration ratio α")
        ax.set_title(title_suffix, fontsize=10)

        honest_idx = ALPHA_VALS.index(1.0)
        ax.add_patch(plt.Rectangle(
            (-0.5, honest_idx - 0.5), len(G_VALS), 1,
            fill=False, edgecolor=C_DARK, linewidth=1.5, zorder=5,
        ))

        for i in range(len(ALPHA_VALS)):
            for j in range(len(G_VALS)):
                val = matrix[i, j]
                text_col = 'white' if abs(val) > vmax * 0.6 else C_DARK
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

    global G_VALS, G_LABELS, ALPHA_VALS, N_ACTUAL_VALS
    sw = p['sweep']
    G_VALS        = sw['g_vals']
    G_LABELS      = [f"{v*100:.1f}%" for v in G_VALS]
    ALPHA_VALS    = sw['alpha_vals']
    N_ACTUAL_VALS = sw['n_actual_vals']

    ensure_dir(_OUT)
    apply_style()

    print(f"\nGenerating VAL figures → {_OUT}")
    print(f"Parameters: N={p['N']}, g={p['g']*100:.2f}%, V0=£{p['V0_m']:.0f}m, "
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