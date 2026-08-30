"""
VAL Output Script D — Figures
==============================
Generates PNG figures for VAL.A and VAL.B.

Requires matplotlib and numpy. All figure files are written to:
  OUTPUTS/VAL/figures/

Figure inventory:

  Fig 08  — Two-panel TW advantage decomposition.
             Left: stacked area chart at g=hist_mean showing the three
             mechanical terms (excess periodic cost, sell-year refund
             benefit, post-sale damping) against alpha. Net TW advantage
             line confirms C.8. Right: f_N ratio heatmap across (alpha, g)
             with contours at 0.95 and 0.90 showing equity dilution cost.

Parameters from wdt_core.load_params() (single source of truth).
All monetary values in £m. LaTeX rendering disabled — plain text labels used.
"""

import os
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from wdt_core import load_params, decompose_tw_advantage
from val_helpers import OUT_DIR

FIGURE_DIR = str(Path(OUT_DIR) / 'figures')


# ─────────────────────────────────────────────────────────────
# SHARED STYLE HELPERS
# ─────────────────────────────────────────────────────────────

def set_style():
    """Apply consistent style to all figures."""
    plt.rcParams.update({
        'figure.facecolor':  'white',
        'axes.facecolor':    '#f8f8f8',
        'axes.edgecolor':    '#cccccc',
        'axes.grid':         True,
        'grid.color':        '#dddddd',
        'grid.linewidth':    0.7,
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'font.family':       'sans-serif',
        'font.size':         9,
        'axes.titlesize':    10,
        'axes.labelsize':    9,
        'xtick.labelsize':   8,
        'ytick.labelsize':   8,
        'legend.frameon':    True,
        'legend.framealpha': 0.85,
        'legend.fontsize':   8.5,
        'lines.linewidth':   1.8,
    })


def _save(fig, filename):
    """Save figure to FIGURE_DIR and return the output path."""
    os.makedirs(FIGURE_DIR, exist_ok=True)
    out = os.path.join(FIGURE_DIR, filename)
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"    Saved: {out}")
    return out


# ─────────────────────────────────────────────────────────────
# FIG 08 CONSTANTS AND HELPERS
# ─────────────────────────────────────────────────────────────

_FIG08_OVER_ALPHAS = [1.0, 1.2, 1.5, 1.8, 2.0]
_FIG08_ALPHA_FINE  = np.linspace(1.0, 2.0, 41)    # left panel x-axis
_FIG08_G_FINE      = np.linspace(0.0, 0.25, 51)   # right panel y-axis


def _decompose_fig08(p, alpha, g):
    """
    Thin wrapper around wdt_core.decompose_tw_advantage() that unpacks
    the result dict into the 6-tuple expected by fig_08_tw_decomposition():

        excess_periodic, refund_delta, settle_delta, tw_advantage, f_ratio, tw_honest

    All values in £m except f_ratio (dimensionless).
    """
    d = decompose_tw_advantage(p, alpha, g)
    return (
        d['excess_periodic'],
        d['refund_delta'],
        d['settle_delta'],
        d['tw_advantage'],
        d['f_ratio'],
        d['tw_honest'],
    )


# ─────────────────────────────────────────────────────────────
# FIG 08 — TW advantage decomposition
# ─────────────────────────────────────────────────────────────

def fig_08_tw_decomposition(p):
    """
    Two-panel figure:

    LEFT — Stacked area chart at g = hist_mean across alpha in [1.0, 2.0].
    Shows the three cost/benefit terms as a fraction of honest TW:
      - Excess periodic tax paid   (cost, plotted upward in red)
      - Post-sale damping cost     (cost, stacked on periodic in orange)
      - Sell-year refund benefit   (benefit, plotted downward in blue)
      - Net TW advantage           (black line — algebraic sum)

    RIGHT — f_N ratio heatmap across (alpha, g).
    Shows how rapidly equity is eroded relative to honest declaration.
    Contours at f_ratio = 0.95 and 0.90.

    Together the panels answer: where does the TW advantage come from,
    and what is its mechanical cost?
    """
    print("  Generating Fig 08: TW advantage decomposition...")

    hist_mean = p['g']
    N         = p['N']

    # ── precompute left-panel series ─────────────────────────
    ep_vals = []   # excess periodic / tw_honest  (%)
    rd_vals = []   # refund delta    / tw_honest  (%)
    sd_vals = []   # settle delta    / tw_honest  (%)
    tw_vals = []   # tw advantage    / tw_honest  (%)

    for alpha in _FIG08_ALPHA_FINE:
        ep, rd, sd, tw_adv, _, tw_h = _decompose_fig08(p, alpha, hist_mean)
        denom = tw_h if abs(tw_h) > 1e-12 else 1.0
        ep_vals.append(ep    / denom * 100)
        rd_vals.append(rd    / denom * 100)
        sd_vals.append(sd    / denom * 100)
        tw_vals.append(tw_adv / denom * 100)

    ep_arr = np.array(ep_vals)
    rd_arr = np.array(rd_vals)
    sd_arr = np.array(sd_vals)
    tw_arr = np.array(tw_vals)

    # ── precompute right-panel f_N heatmap ───────────────────
    # shape: (len(alpha_fine), len(g_fine))
    f_matrix = np.zeros((len(_FIG08_ALPHA_FINE), len(_FIG08_G_FINE)))
    for i, alpha in enumerate(_FIG08_ALPHA_FINE):
        for j, g in enumerate(_FIG08_G_FINE):
            _, _, _, _, f_ratio, _ = _decompose_fig08(p, alpha, g)
            f_matrix[i, j] = f_ratio

    # ── figure ───────────────────────────────────────────────
    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))
    alpha_x = _FIG08_ALPHA_FINE

    # ── LEFT: stacked decomposition ──────────────────────────
    ax1.axhline(0, color='#555555', linewidth=0.9, zorder=2)

    # Costs above zero
    ax1.fill_between(alpha_x, 0, ep_arr,
                     color='#d73027', alpha=0.55,
                     label='Excess periodic tax paid')
    ax1.fill_between(alpha_x, ep_arr, ep_arr + sd_arr,
                     color='#f46d43', alpha=0.55,
                     label='Post-sale damping cost')

    # Benefit below zero
    ax1.fill_between(alpha_x, 0, rd_arr,
                     color='#4393c3', alpha=0.55,
                     label='Sell-year refund benefit')

    # Net TW advantage line
    ax1.plot(alpha_x, tw_arr,
             color='#1a1a1a', linewidth=2.2, zorder=5,
             label='Net TW advantage (C.8)')

    # Mark any zero-crossings
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
    ax1.text(alpha_x[-1] - 0.01, tw_arr[-1] + 0.3,
             f'a=2.0: {tw_arr[-1]:.1f}pp',
             fontsize=7.5, ha='right', color='#1a1a1a')

    ax1.set_xlabel("Declaration ratio (alpha)", fontsize=10)
    ax1.set_ylabel("As % of honest TW_settled", fontsize=10)
    ax1.set_title(
        f"Left: TW advantage decomposition\n"
        f"g = {hist_mean*100:.1f}% (hist. mean), N = {N}, "
        f"V0 = £{p['V0_m']:.0f}m, k = {p['k']}",
        fontsize=10
    )
    ax1.set_xlim(1.0, 2.0)
    ax1.legend(loc='upper left', fontsize=8.5)
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

    # f_ratio = 0.95 contour
    CS95 = ax2.contour(
        g_pct, _FIG08_ALPHA_FINE, f_matrix,
        levels=[0.95], colors=['#d73027'], linewidths=1.6, zorder=4,
    )
    ax2.clabel(CS95, fmt={0.95: 'f ratio = 0.95'}, fontsize=8, inline=True)

    # f_ratio = 0.90 contour
    CS90 = ax2.contour(
        g_pct, _FIG08_ALPHA_FINE, f_matrix,
        levels=[0.90], colors=['#7f0000'], linewidths=1.4,
        linestyles='--', zorder=4,
    )
    ax2.clabel(CS90, fmt={0.90: 'f ratio = 0.90'}, fontsize=8, inline=True)

    # hist_mean reference line
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
        "Left: sell-year refund benefit exceeds periodic cost across all tested alpha  "
        "Right: f_N erosion increases with both alpha and g — "
        "equity dilution is the hidden price of overstatement",
        fontsize=10, y=1.01
    )

    plt.tight_layout()
    return _save(fig, "val_fig_08_tw_decomposition.png")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    p = load_params()
    print(f"Parameters loaded: k={p['k']}, N={p['N']} (SSM-derived), g={p['g']:.4f}")
    print(f"Figure output directory: {FIGURE_DIR}")

    print("Fig 08: TW advantage decomposition...")
    fig_08_tw_decomposition(p)
    

    print("Done.")


if __name__ == '__main__':
    main()
