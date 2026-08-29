"""
val_s_helpers.py — Shared helpers for VAL.S output scripts
===========================================================
Single source of truth for the analytical primitives, canonical constants,
matplotlib style, and caching layer shared across:

  16_2  VAL_S_rate_sweeps.py
  16_3  VAL_S_horizon_sweeps.py
  16_4  VAL_S_interactions.py
  16_5  VAL_S_assemble.py

Import everything needed with:
    from val_s_helpers import *

or selectively:
    from val_s_helpers import make_p, c1, n_crossing, set_style, save_fig
"""

import os
import math
import functools
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from wdt_core import load_params, run_sim, tau

# ─────────────────────────────────────────────────────────────
# CANONICAL CONSTANTS — sourced from TOML once at import time
# ─────────────────────────────────────────────────────────────

_P  = load_params()
_SW = _P['sweep']

CANON_TAU0 = _SW['tau_0_canon']
CANON_TAUM = _SW['tau_m_canon']
CANON_K    = _SW['k_canon']
CANON_N    = _SW['N_canon']
CANON_V0   = _SW['V0_canon']
CANON_G    = _SW['g_canon']
CANON_WMIN = _SW['W_min_canon']

G_VALS       = _SW['g_vals']
G_LABELS     = [f"{v*100:.1f}%" for v in G_VALS]
ALPHA_VALS   = _SW['alpha_vals']
OVER_ALPHAS  = _SW['over_alphas']
UNDER_ALPHAS = _SW['under_alphas']
N_SWEEP      = _SW['n_sweep']          # full list e.g. range(5,66)
TZONE_THRESHOLD = _SW['tzone_threshold']

# Panel sweep values used at module scope in specific scripts
TAU0_VALS    = _SW['tau0_panel_vals']
TAUM_VALS    = _SW['taum_panel_vals']
K_VALS       = _SW['k_panel_vals']
WMIN_VALS    = _SW['wmin_panel_vals']
V0_VALS      = _SW['v0_sweep_vals']
N_PANEL_VALS = _SW['n_panel_vals']

# Shared output directory for all VAL.S figure/table outputs
OUT_DIR = os.path.join(os.path.dirname(__file__), 'OUTPUTS', 'VAL_S')


# ─────────────────────────────────────────────────────────────
# CACHED RUN_SIM — avoids recomputing the same (p, alpha, g, N) tuple
#
# Cache key: flatten the seven make_p() fields + alpha + g + N into a
# hashable tuple.  Only works cleanly because make_p() output has a
# fixed, known set of numeric keys.  Full p dicts from load_params()
# are not cached here (they carry returns lists etc.); use run_sim()
# directly for those.
# ─────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=8192)
def _run_sim_cached(tau_0, tau_m, k, W_min, V0_m, g_param, N_param,
                    alpha, g, N):
    """
    Cached thin wrapper around run_sim().
    Only accepts scalar numeric params — suitable for make_p() dicts.
    """
    p = {
        'tau_0': tau_0, 'tau_m': tau_m, 'k': k,
        'W_min': W_min, 'V0_m': V0_m, 'g': g_param, 'N': N_param,
    }
    return run_sim(p, alpha=alpha, g=g, N=N)


def run_sim_p(p, alpha, g, N=None):
    """
    Cached run_sim for make_p()-style dicts (seven fixed numeric keys).
    Falls back to uncached run_sim for any other dict shape.
    """
    N = N if N is not None else p['N']
    try:
        return _run_sim_cached(
            p['tau_0'], p['tau_m'], p['k'], p['W_min'],
            p['V0_m'], p['g'], p['N'],
            alpha, g, N,
        )
    except (KeyError, TypeError):
        return run_sim(p, alpha=alpha, g=g, N=N)


# ─────────────────────────────────────────────────────────────
# CANONICAL PARAMETER DICT FACTORY
# ─────────────────────────────────────────────────────────────

def make_p(tau_0=CANON_TAU0, tau_m=CANON_TAUM, k=CANON_K,
           W_min=CANON_WMIN, V0_m=CANON_V0, g=CANON_G, N=CANON_N):
    """Return a minimal parameter dict suitable for run_sim_p()."""
    return {
        'tau_0': tau_0, 'tau_m': tau_m, 'k': k,
        'W_min': W_min, 'V0_m': V0_m, 'g': g, 'N': N,
    }


# ─────────────────────────────────────────────────────────────
# ANALYTICAL METRICS
# ─────────────────────────────────────────────────────────────

def c1(p, alpha, g, N=None):
    """
    C.1 metric: (Net_settled(α) − Net_settled(1)) / TW_settled(α).
    Positive = α pays more net tax than honest; negative = pays less.
    Uses settled values to account for post-sale tax/refund oscillation.
    """
    N = N if N is not None else p['N']
    r = run_sim_p(p, alpha=alpha, g=g, N=N)
    b = run_sim_p(p, alpha=1.0,   g=g, N=N)
    if abs(r['TW_settled']) < 1e-12:
        return 0.0
    return (r['Net_settled'] - b['Net_settled']) / r['TW_settled']


def c1_matrix(p, alpha_vals=None, g_vals=None):
    """
    Compute C.1 matrix [alpha × g] in percentage points.
    Defaults to the canonical ALPHA_VALS × G_VALS grid.
    """
    if alpha_vals is None:
        alpha_vals = ALPHA_VALS
    if g_vals is None:
        g_vals = G_VALS
    mat = np.zeros((len(alpha_vals), len(g_vals)))
    for i, alpha in enumerate(alpha_vals):
        for j, g_val in enumerate(g_vals):
            mat[i, j] = c1(p, alpha, g_val) * 100
    return mat


def n_crossing(p, alpha, g=None, N_sweep=None):
    """
    First N at which overstater Net > honest Net (interpolated).
    Returns np.nan if no crossing found within N_sweep.

    g defaults to CANON_G.  N_sweep defaults to the canonical list.
    """
    if g is None:
        g = CANON_G
    if N_sweep is None:
        N_sweep = N_SWEEP
    diffs = []
    for n in N_sweep:
        r = run_sim_p(p, alpha=alpha, g=g, N=n)
        b = run_sim_p(p, alpha=1.0,   g=g, N=n)
        diffs.append(r['Net_settled'] - b['Net_settled'])
    for i in range(len(diffs) - 1):
        if diffs[i] < 0 and diffs[i + 1] >= 0:
            frac = -diffs[i] / (diffs[i + 1] - diffs[i])
            return N_sweep[i] + frac
    return np.nan


def tolerant_zone_bounds(p, g=None, threshold=None):
    """
    Returns (lo, hi) alpha of the |C.1| < threshold zone, or (None, None).
    Sweeps alpha 0.10 → 2.50 in steps of 0.05.
    """
    if g is None:
        g = CANON_G
    if threshold is None:
        threshold = TZONE_THRESHOLD
    alphas = [a / 100 for a in range(10, 251, 5)]
    c1_vals = [c1(p, a, g) for a in alphas]
    lo = hi = None
    for a, v in zip(alphas, c1_vals):
        if abs(v) < threshold:
            if lo is None:
                lo = a
            hi = a
    return lo, hi


def tolerant_zone_width(p, g=None, threshold=None):
    """
    Width (hi − lo) of the |C.1| < threshold zone.
    Returns 0.0 if no zone found.
    """
    lo, hi = tolerant_zone_bounds(p, g=g, threshold=threshold)
    if lo is not None and hi is not None:
        return hi - lo
    return 0.0


def understater_plateau(p, alpha=0.1, g_range=None):
    """
    Max C.1 (in pp) in the plateau zone (g > 17%) for a given understater α.
    """
    if g_range is None:
        g_range = [gv / 100 for gv in range(18, 41)]
    return max(c1(p, alpha, gv) * 100 for gv in g_range)


# ─────────────────────────────────────────────────────────────
# MATPLOTLIB STYLE AND FIGURE SAVING
#
# Two style presets:
#   set_style()        — standard style with grid (most sweep figures)
#   set_style_nogrid() — no grid (heatmaps: 16_4 interactions)
# ─────────────────────────────────────────────────────────────

_STYLE_BASE = {
    'font.family':       'DejaVu Sans',
    'font.size':         9,
    'axes.titlesize':    10,
    'axes.labelsize':    9,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
    'legend.frameon':    False,
    'legend.fontsize':   8,
}

def set_style():
    """Standard sweep-figure style with a light grid."""
    plt.rcParams.update({
        **_STYLE_BASE,
        'axes.grid':    True,
        'grid.color':   '#e0e0e0',
        'grid.linewidth': 0.6,
    })


def set_style_nogrid():
    """Heatmap style — grid disabled (avoids lines over imshow cells)."""
    plt.rcParams.update({
        **_STYLE_BASE,
        'axes.grid': False,
    })


def save_fig(fig, name, out_dir=None):
    """
    Save fig to out_dir/name at 150 dpi, close it, and print the path.
    out_dir defaults to the shared VAL_S OUT_DIR.
    """
    if out_dir is None:
        out_dir = OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  Saved: {path}')
    return path


# ─────────────────────────────────────────────────────────────
# SHARED HEATMAP HELPER
# ─────────────────────────────────────────────────────────────

def draw_c1_heatmap(ax, mat, alpha_vals=None, g_labels=None,
                    vmax=30.0, title='', bold_alpha=1.0):
    """
    Render a C.1 heatmap (in pp) onto ax.  Returns the imshow object.

    mat        — 2-D array [alpha × g] in pp
    alpha_vals — row labels (default ALPHA_VALS)
    g_labels   — column labels (default G_LABELS)
    vmax       — symmetric colour scale ±vmax
    title      — axes title
    bold_alpha — the alpha value whose row gets a border box
    """
    if alpha_vals is None:
        alpha_vals = ALPHA_VALS
    if g_labels is None:
        g_labels = G_LABELS
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)
    ax.grid(False)
    im = ax.imshow(mat, aspect='auto', cmap='RdBu_r', norm=norm, zorder=2)
    ax.set_xticks(range(len(g_labels)))
    ax.set_xticklabels(g_labels, rotation=45, ha='right', fontsize=7)
    ax.set_yticks(range(len(alpha_vals)))
    ax.set_yticklabels([str(a) for a in alpha_vals])
    ax.set_xlabel('g', fontsize=8)
    ax.set_ylabel('α', fontsize=8)
    ax.set_title(title, fontsize=10)
    # Cell annotations
    for i in range(len(alpha_vals)):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            col = 'white' if abs(v) > vmax * 0.6 else '#1a1a1a'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                    fontsize=6, color=col, zorder=3)
    # Highlight the honest row
    if bold_alpha in alpha_vals:
        hon = list(alpha_vals).index(bold_alpha)
        ax.add_patch(plt.Rectangle((-0.5, hon - 0.5), len(g_labels), 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=1.5))
    return im
