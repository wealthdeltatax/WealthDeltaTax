"""
wdt_analytics.py — WDT Unified Analytical Metrics and Sweep Infrastructure
===========================================================================
Single source of truth for the analytical primitives, statistical helpers,
cached simulation wrapper, canonical grid constants, and parameter sweep
runner used across VAL.S and RATES.S output scripts.

Replaces
--------
  val_s_helpers.py      _run_sim_cached(), run_sim_p(), make_p(),
                        c1(), c1_matrix(), n_crossing(),
                        tolerant_zone_bounds(), tolerant_zone_width(),
                        understater_plateau(), draw_c1_heatmap(),
                        all CANON_* and grid constants
  rates_s_helpers.py    median(), mean(), success(), summarise(),
                        run_param_sweep(),
                        model (re-export), DEFAULT_PARAMS (re-export)

Public API
----------
Initialisation
  init(p)               populate module-level grid constants from a loaded
                        params dict; call once in main() before using any
                        constant.  Safe to call multiple times (idempotent).

Re-exports (for drop-in migration)
  model                 rates_model module
  DEFAULT_PARAMS        Path to the default TOML file

Canonical parameter dict
  make_p(...)           build a minimal 7-key dict for run_sim_p()

Cached simulation
  run_sim_p(p, alpha, g, N=None)   LRU-cached run_sim for make_p() dicts

Analytical metrics
  c1(p, alpha, g, N=None)          C.1 incentive metric (fraction)
  c1_matrix(p, ...)                C.1 matrix [alpha × g] in pp
  n_crossing(p, alpha, g, N_sweep) first N where overstater crosses honest
  tolerant_zone_bounds(p, ...)     (lo, hi) alpha of |C.1| < threshold
  tolerant_zone_width(p, ...)      hi - lo, or 0.0
  understater_plateau(p, ...)      max C.1 (pp) in plateau zone

Heatmap helper
  draw_c1_heatmap(ax, mat, ...)    render a C.1 heatmap onto an axes

Statistical primitives
  median(vals)          weighted median (None-safe)
  mean(vals)            arithmetic mean  (None-safe)
  success(r)            True if run fills LRR and handles SRR breach

Sweep summariser
  summarise(sweep_results)         distribution dict from a full sweep

Sweep runner
  run_param_sweep(p_base, param_name, values, label=None)

Module-level grid constants (populated by init())
  CANON_TAU0, CANON_TAUM, CANON_K, CANON_N, CANON_V0, CANON_G, CANON_WMIN
  TZONE_THRESHOLD
  G_VALS, G_LABELS, ALPHA_VALS, OVER_ALPHAS, UNDER_ALPHAS
  N_SWEEP, N_PANEL_VALS, TAU0_VALS, TAUM_VALS, K_VALS, WMIN_VALS, V0_VALS

Design notes
------------
Lazy initialisation
  val_s_helpers ran load_params() at import time (line 34), which in turn
  runs the full SSM to derive N.  This made every `from val_s_helpers import *`
  expensive and surprising.  wdt_analytics defers this: the module-level
  constants are None until init(p) is called.  Each output script's main()
  calls load_params() once, then passes the result to init().

  The only cost: any constant used before init() will be None and will
  raise a clear error at the call site.  This is better than a hidden
  multi-second side effect on import.

No matplotlib at import time
  draw_c1_heatmap() imports matplotlib lazily to keep this module safe
  in non-plotting contexts.

rates_model re-export
  16_6 and 16_7 import `model` from rates_s_helpers.  We re-export it
  here so migration is a single import-line change.  DEFAULT_PARAMS is
  likewise re-exported.
"""

from __future__ import annotations

import functools
import math
from copy import deepcopy
from pathlib import Path
from typing import List, Optional, Sequence

import numpy as np

from wdt_core import load_params as _core_load_params, run_sim, tau

# ── rates_model re-export ────────────────────────────────────────────────────
# Imported here so 16_6/16_7 can replace `from rates_s_helpers import model`
# with `from wdt_analytics import model`.
import rates_model as model

# Default TOML path — mirrors rates_s_helpers.DEFAULT_PARAMS resolution
DEFAULT_PARAMS: Path = Path(__file__).parent / 'WDT_Params.toml'


# ─────────────────────────────────────────────────────────────────────────────
# MODULE-LEVEL GRID CONSTANTS
# All start as None; populated by init(p).
# ─────────────────────────────────────────────────────────────────────────────

CANON_TAU0:      Optional[float] = None
CANON_TAUM:      Optional[float] = None
CANON_K:         Optional[float] = None
CANON_N:         Optional[int]   = None
CANON_V0:        Optional[float] = None
CANON_G:         Optional[float] = None
CANON_WMIN:      Optional[float] = None
TZONE_THRESHOLD: Optional[float] = None

G_VALS:       Optional[List[float]] = None
G_LABELS:     Optional[List[str]]   = None
ALPHA_VALS:   Optional[List[float]] = None
OVER_ALPHAS:  Optional[List[float]] = None
UNDER_ALPHAS: Optional[List[float]] = None
N_SWEEP:      Optional[List[int]]   = None
N_PANEL_VALS: Optional[List[int]]   = None
TAU0_VALS:    Optional[List[float]] = None
TAUM_VALS:    Optional[List[float]] = None
K_VALS:       Optional[List[float]] = None
WMIN_VALS:    Optional[List[float]] = None
V0_VALS:      Optional[List[float]] = None


# ─────────────────────────────────────────────────────────────────────────────
# INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────

def init(p: dict) -> None:
    """
    Populate all module-level grid constants from a loaded params dict.

    Parameters
    ----------
    p : dict   result of wdt_core.load_params() or rates_model.load_params()

    Call once in main() after loading parameters:

        p = load_params()
        wdt_analytics.init(p)

    Safe to call multiple times — subsequent calls overwrite the previous
    values, which is useful when testing with different TOML files.

    Migration notes
    ---------------
    val_s_helpers populated these at import time via:
        _P  = load_params()
        _SW = _P['sweep']
        CANON_TAU0 = _SW['tau_0_canon']
        ...
    The new pattern moves this to main() and is explicit.

    16_4 and 16_5 had their own `_P = load_params()` at module scope;
    those calls are replaced by init(p) in main().
    """
    global CANON_TAU0, CANON_TAUM, CANON_K, CANON_N, CANON_V0, CANON_G
    global CANON_WMIN, TZONE_THRESHOLD
    global G_VALS, G_LABELS, ALPHA_VALS, OVER_ALPHAS, UNDER_ALPHAS
    global N_SWEEP, N_PANEL_VALS, TAU0_VALS, TAUM_VALS, K_VALS, WMIN_VALS, V0_VALS

    sw = p['sweep']

    CANON_TAU0      = sw['tau_0_canon']
    CANON_TAUM      = sw['tau_m_canon']
    CANON_K         = sw['k_canon']
    CANON_N         = sw['N_canon']
    CANON_V0        = sw['V0_canon']
    CANON_G         = sw['g_canon']
    CANON_WMIN      = sw['W_min_canon']
    TZONE_THRESHOLD = sw['tzone_threshold']

    G_VALS       = sw['g_vals']
    G_LABELS     = [f"{v * 100:.1f}%" for v in G_VALS]
    ALPHA_VALS   = sw['alpha_vals']
    OVER_ALPHAS  = sw['over_alphas']
    UNDER_ALPHAS = sw['under_alphas']
    N_SWEEP      = sw['n_sweep']
    N_PANEL_VALS = sw['n_panel_vals']
    TAU0_VALS    = sw['tau0_panel_vals']
    TAUM_VALS    = sw['taum_panel_vals']
    K_VALS       = sw['k_panel_vals']
    WMIN_VALS    = sw['wmin_panel_vals']
    V0_VALS      = sw['v0_sweep_vals']

    # Reset the simulation cache whenever parameters are re-initialised,
    # since make_p() defaults will have changed.
    _run_sim_cached.cache_clear()


# ─────────────────────────────────────────────────────────────────────────────
# CANONICAL PARAMETER DICT FACTORY
# ─────────────────────────────────────────────────────────────────────────────

def make_p(
    tau_0=None, tau_m=None, k=None,
    W_min=None, V0_m=None, g=None, N=None,
) -> dict:
    """
    Build a minimal 7-key parameter dict suitable for run_sim_p().

    Unspecified arguments default to the CANON_* module-level values,
    which must have been populated by init() first.

    Migration notes
    ---------------
    val_s_helpers.make_p(**kwargs)  →  make_p(**kwargs)
    Identical signature and behaviour; the only change is that the
    defaults now come from module-level constants set by init() rather
    than from closure over the import-time load.
    """
    return {
        'tau_0': tau_0 if tau_0 is not None else CANON_TAU0,
        'tau_m': tau_m if tau_m is not None else CANON_TAUM,
        'k':     k     if k     is not None else CANON_K,
        'W_min': W_min if W_min is not None else CANON_WMIN,
        'V0_m':  V0_m  if V0_m  is not None else CANON_V0,
        'g':     g     if g     is not None else CANON_G,
        'N':     N     if N     is not None else CANON_N,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CACHED SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=8192)
def _run_sim_cached(
    tau_0, tau_m, k, W_min, V0_m, g_param, N_param,
    alpha, g, N,
):
    """
    LRU-cached run_sim for scalar numeric parameters.

    Cache key is the full tuple of all nine numeric inputs, which is
    hashable. Only suitable for make_p()-style dicts with seven fixed
    numeric keys. Full load_params() dicts (with returns lists etc.)
    must use run_sim() directly.

    Migration notes
    ---------------
    Identical to val_s_helpers._run_sim_cached — same cache key structure,
    same maxsize, same fallback pattern in run_sim_p().
    """
    p = {
        'tau_0': tau_0, 'tau_m': tau_m, 'k': k,
        'W_min': W_min, 'V0_m': V0_m, 'g': g_param, 'N': N_param,
    }
    return run_sim(p, alpha=alpha, g=g, N=N)


def run_sim_p(p: dict, alpha: float, g: float, N: Optional[int] = None):
    """
    Cached run_sim for make_p()-style dicts.

    Falls back to uncached run_sim() for any dict that lacks the seven
    expected numeric keys (e.g. a full load_params() dict).

    Parameters
    ----------
    p     : dict    make_p()-style dict with keys tau_0, tau_m, k,
                    W_min, V0_m, g, N
    alpha : float   declaration ratio
    g     : float   constant growth rate for this run
    N     : int     holding period; defaults to p['N']

    Migration notes
    ---------------
    val_s_helpers.run_sim_p(p, alpha, g, N=None)  →  run_sim_p(p, alpha, g, N)
    Identical signature and behaviour.
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


# ─────────────────────────────────────────────────────────────────────────────
# ANALYTICAL METRICS
# ─────────────────────────────────────────────────────────────────────────────

def c1(p: dict, alpha: float, g: float, N: Optional[int] = None) -> float:
    """
    C.1 incentive metric: (Net_settled(α) − Net_settled(1)) / TW_settled(α).

    Positive = α pays more net tax than honest (understater penalty).
    Negative = α pays less net tax than honest (overstater advantage).

    Uses TW_settled and Net_settled (post-sale oscillation corrected)
    throughout, matching VAL.A §C conventions.

    Parameters
    ----------
    p     : dict    make_p()-style parameter dict
    alpha : float   declaration ratio
    g     : float   constant growth rate
    N     : int     holding period; defaults to p['N']

    Returns
    -------
    float   C.1 as a fraction (multiply by 100 for percentage points)

    Migration notes
    ---------------
    val_s_helpers.c1(p, alpha, g, N=None)  →  c1(p, alpha, g, N)
    Identical signature and behaviour.
    """
    N = N if N is not None else p['N']
    r = run_sim_p(p, alpha=alpha, g=g, N=N)
    b = run_sim_p(p, alpha=1.0,   g=g, N=N)
    if abs(r['TW_settled']) < 1e-12:
        return 0.0
    return (r['Net_settled'] - b['Net_settled']) / r['TW_settled']


def c1_matrix(
    p: dict,
    alpha_vals: Optional[Sequence[float]] = None,
    g_vals: Optional[Sequence[float]] = None,
) -> np.ndarray:
    """
    Compute C.1 matrix [alpha × g] in percentage points.

    Parameters
    ----------
    p          : dict    make_p()-style parameter dict
    alpha_vals : list    row values; defaults to module-level ALPHA_VALS
    g_vals     : list    column values; defaults to module-level G_VALS

    Returns
    -------
    np.ndarray  shape (len(alpha_vals), len(g_vals)), values in pp

    Migration notes
    ---------------
    val_s_helpers.c1_matrix(p, alpha_vals, g_vals)  →  c1_matrix(p, ...)
    Identical signature and behaviour; defaults now require init() first.
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


def n_crossing(
    p: dict,
    alpha: float,
    g: Optional[float] = None,
    N_sweep: Optional[Sequence[int]] = None,
) -> float:
    """
    First N at which overstater Net_settled > honest Net_settled.

    Uses linear interpolation between the two N values that straddle the
    zero crossing.  Returns np.nan if no crossing found in N_sweep.

    Parameters
    ----------
    p       : dict    make_p()-style parameter dict
    alpha   : float   overstater declaration ratio (should be > 1.0)
    g       : float   growth rate; defaults to CANON_G
    N_sweep : list    holding periods to test; defaults to module N_SWEEP

    Returns
    -------
    float   interpolated crossing N, or np.nan

    Migration notes
    ---------------
    val_s_helpers.n_crossing(p, alpha, g, N_sweep)  →  n_crossing(p, alpha, ...)
    Identical behaviour; defaults require init() first.
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
            span = diffs[i + 1] - diffs[i]
            frac = -diffs[i] / span if span != 0 else 0.0
            return N_sweep[i] + frac
    return np.nan


def tolerant_zone_bounds(
    p: dict,
    g: Optional[float] = None,
    threshold: Optional[float] = None,
) -> tuple:
    """
    Return (lo, hi) alpha of the tolerant zone where |C.1| < threshold.

    The tolerant zone is the α range in which declaration error is small
    enough that it produces negligible incentive distortion — neither a
    meaningful penalty (understater) nor a meaningful saving (overstater).

    Sweeps α from 0.10 to 2.50 in steps of 0.05.

    Parameters
    ----------
    p         : dict    make_p()-style parameter dict
    g         : float   growth rate; defaults to CANON_G
    threshold : float   |C.1| threshold in fractions; defaults to TZONE_THRESHOLD

    Returns
    -------
    (lo, hi) : (float, float) or (None, None) if no zone found

    Migration notes
    ---------------
    val_s_helpers.tolerant_zone_bounds(p, g, threshold)  →  identical signature.
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


def tolerant_zone_width(
    p: dict,
    g: Optional[float] = None,
    threshold: Optional[float] = None,
) -> float:
    """
    Width (hi − lo) of the tolerant zone, or 0.0 if none found.

    Migration notes
    ---------------
    val_s_helpers.tolerant_zone_width(p, g, threshold)  →  identical signature.
    """
    lo, hi = tolerant_zone_bounds(p, g=g, threshold=threshold)
    if lo is not None and hi is not None:
        return hi - lo
    return 0.0


def understater_plateau(
    p: dict,
    alpha: float = 0.1,
    g_range: Optional[Sequence[float]] = None,
) -> float:
    """
    Maximum C.1 (in percentage points) in the plateau zone for an understater.

    The plateau zone is roughly g > 17%, where the progressive rate function
    saturates and further growth no longer increases the C.1 penalty.

    Parameters
    ----------
    p       : dict    make_p()-style parameter dict
    alpha   : float   understater declaration ratio (default 0.1)
    g_range : list    growth rates to sweep; defaults to 18%–40% in 1% steps

    Returns
    -------
    float   maximum C.1 in percentage points over the plateau range

    Migration notes
    ---------------
    val_s_helpers.understater_plateau(p, alpha, g_range)  →  identical signature.
    """
    if g_range is None:
        g_range = [gv / 100 for gv in range(18, 41)]
    return max(c1(p, alpha, gv) * 100 for gv in g_range)


# ─────────────────────────────────────────────────────────────────────────────
# HEATMAP HELPER
# ─────────────────────────────────────────────────────────────────────────────

def draw_c1_heatmap(
    ax,
    mat: np.ndarray,
    alpha_vals: Optional[Sequence[float]] = None,
    g_labels: Optional[Sequence[str]] = None,
    vmax: float = 30.0,
    title: str = '',
    bold_alpha: float = 1.0,
):
    """
    Render a C.1 heatmap (in pp) onto a matplotlib axes object.

    Parameters
    ----------
    ax         : matplotlib.axes.Axes
    mat        : np.ndarray   [alpha × g] in percentage points
    alpha_vals : list         row labels; defaults to ALPHA_VALS
    g_labels   : list         column labels; defaults to G_LABELS
    vmax       : float        symmetric colour scale ±vmax (default 30)
    title      : str          axes title
    bold_alpha : float        the alpha row to highlight with a border box

    Returns
    -------
    imshow object (for use with fig.colorbar())

    Migration notes
    ---------------
    val_s_helpers.draw_c1_heatmap(ax, mat, ...)  →  identical signature.
    Defaults require init() first.
    """
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt

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

    for i in range(len(alpha_vals)):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            col = 'white' if abs(v) > vmax * 0.6 else '#1a1a1a'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                    fontsize=6, color=col, zorder=3)

    if bold_alpha in alpha_vals:
        hon = list(alpha_vals).index(bold_alpha)
        ax.add_patch(plt.Rectangle(
            (-0.5, hon - 0.5), len(g_labels), 1,
            fill=False, edgecolor='#1a1a1a', linewidth=1.5,
        ))
    return im


# ─────────────────────────────────────────────────────────────────────────────
# STATISTICAL PRIMITIVES
# ─────────────────────────────────────────────────────────────────────────────

def median(vals) -> Optional[float]:
    """
    Median of a sequence, ignoring None values.

    Returns None if the filtered sequence is empty.

    Migration notes
    ---------------
    rates_s_helpers.median(vals)  →  median(vals)  — identical.
    rates_model._median(vals)     →  median(vals)  — identical behaviour,
                                      now public and accessible.
    """
    s = sorted(v for v in vals if v is not None)
    if not s:
        return None
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def mean(vals) -> Optional[float]:
    """
    Arithmetic mean of a sequence, ignoring None values.

    Returns None if the filtered sequence is empty.

    Migration notes
    ---------------
    rates_s_helpers.mean(vals)  →  mean(vals)  — identical.
    rates_model._mean(vals)     →  mean(vals)  — identical behaviour.
    """
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def success(r: dict) -> bool:
    """
    Return True if a sweep result row represents a 'successful' scenario.

    Success (v8) = LRR fills within the modelling window AND LRR never
    fails (lrr_failure_year is None).  The older v7 definition used
    srr_breach_year / srr_breach_covered, which are retired in v8.

    Parameters
    ----------
    r : dict   one row from run_start_year_sweep() results

    Migration notes
    ---------------
    rates_s_helpers.success(r)  →  success(r)
    rates_model._success(r)     →  success(r)
    v8: srr_breach_year / srr_breach_covered replaced by lrr_failure_year.
    """
    return (r.get('lrr_fill_year') is not None and
            r.get('lrr_failure_year') is None)


# ─────────────────────────────────────────────────────────────────────────────
# COVERAGE WINDOW HEADLINE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────

# The headline coverage window (years) used in table column headers, chart
# axis labels, and run_param_sweep progress output.  All four windows
# (5, 10, 20, 50) are always computed and stored in the summary dict;
# this constant controls which one is aliased to the bare 'ssm_cov' /
# 'tcm_cov' keys that existing call sites in 16_6 and 16_7 read.
# Change this single integer to switch the headline everywhere.
HEADLINE_WINDOW: int = 10


# ─────────────────────────────────────────────────────────────────────────────
# SWEEP SUMMARISER
# ─────────────────────────────────────────────────────────────────────────────

def summarise(sweep_results: list) -> dict:
    """
    Summarise a run_start_year_sweep() result list into a statistics dict.

    Parameters
    ----------
    sweep_results : list   output of rates_model.run_start_year_sweep()

    Returns
    -------
    dict with keys:
      n_total          int    number of start years
      success_rate     float  percentage of successful scenarios (v8 definition)
      n_lrr_failure    int    count of start years where lrr_failure_year is not None

      ssm_cov          dist   alias for ssm_cov_{HEADLINE_WINDOW}  (backward compat)
      tcm_cov          dist   alias for tcm_cov_{HEADLINE_WINDOW}  (backward compat)
      ssm_cov_5        dist   SSM Step-5 coverage fraction, 5yr window
      ssm_cov_10       dist   SSM Step-5 coverage fraction, 10yr window
      ssm_cov_20       dist   SSM Step-5 coverage fraction, 20yr window
      ssm_cov_50       dist   SSM Step-5 coverage fraction, 50yr window
      tcm_cov_5  ..50  dist   TCM equivalents

      lrr_failure      dist   LRR failure year distribution
      srr_failure      dist   SRR failure year distribution
      lrr_fill         dist   LRR fill year distribution
      srr_fill         dist   SRR fill year distribution
      lrr_surplus      dist   LRR surplus at fill distribution
      worst_case_2006  dict   raw sweep row for calendar_year == 2006, or None

    Each dist dict has keys: min, median, mean, max, n.
    The 'ssm_cov' and 'tcm_cov' aliases allow existing 16_6 / 16_7 call
    sites to keep reading s['ssm_cov'] and s['tcm_cov'] unchanged while
    the full per-window data is available via the explicit keys.

    Migration notes
    ---------------
    rates_s_helpers.summarise(sweep_results)  →  summarise(sweep_results)
    Signature unchanged.  Return dict is a superset of the old structure:
    ssm_cov / tcm_cov are now aliases rather than direct dist computations,
    and point at HEADLINE_WINDOW rather than the retired single-value keys.
    """
    n_total       = len(sweep_results)
    n_success     = sum(1 for r in sweep_results if success(r))
    n_lrr_failure = sum(1 for r in sweep_results
                        if r.get('lrr_failure_year') is not None)

    def _dist(key):
        vals = [r[key] for r in sweep_results if r.get(key) is not None]
        if not vals:
            return {'min': None, 'median': None, 'mean': None, 'max': None, 'n': 0}
        return {
            'min':    min(vals),
            'median': median(vals),
            'mean':   mean(vals),
            'max':    max(vals),
            'n':      len(vals),
        }

    wc = next((r for r in sweep_results if r.get('calendar_year') == 2006), None)

    # Per-window dists for all four windows
    ssm_w = {W: _dist(f'ssm_cov_{W}') for W in (5, 10, 20, 50)}
    tcm_w = {W: _dist(f'tcm_cov_{W}') for W in (5, 10, 20, 50)}

    return {
        'n_total':         n_total,
        'success_rate':    100.0 * n_success / n_total if n_total else 0.0,
        'n_lrr_failure':   n_lrr_failure,
        # Headline aliases — point at HEADLINE_WINDOW; 16_6/16_7 read these
        'ssm_cov':         ssm_w[HEADLINE_WINDOW],
        'tcm_cov':         tcm_w[HEADLINE_WINDOW],
        # Full per-window dists
        'ssm_cov_5':       ssm_w[5],
        'ssm_cov_10':      ssm_w[10],
        'ssm_cov_20':      ssm_w[20],
        'ssm_cov_50':      ssm_w[50],
        'tcm_cov_5':       tcm_w[5],
        'tcm_cov_10':      tcm_w[10],
        'tcm_cov_20':      tcm_w[20],
        'tcm_cov_50':      tcm_w[50],
        # Failure year dists (v8)
        'lrr_failure':     _dist('lrr_failure_year'),
        'srr_failure':     _dist('srr_failure_year'),
        # Milestone dists (unchanged)
        'lrr_fill':        _dist('lrr_fill_year'),
        'srr_fill':        _dist('srr_fill_year'),
        'lrr_surplus':     _dist('lrr_surplus_at_fill'),
        'worst_case_2006': wc,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SWEEP RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_param_sweep(
    p_base: dict,
    param_name: str,
    values: Sequence,
    label: Optional[str] = None,
) -> list:
    """
    Run model.run_start_year_sweep() for each value, overriding one parameter.

    For each value in `values`, creates a deep copy of p_base, sets
    p_base[param_name] = value, validates the result, then runs the full
    73-start-year sweep and summarises it.

    Invalid combinations are skipped with a printed reason:
      - tau_0 >= tau_m  (rate function undefined)
      - W_min < 0       (negative entry threshold)
      - srr_ratio <= 0  (degenerate SRR sizing)
      - lrr_years <= 0  (degenerate LRR sizing)

    Parameters
    ----------
    p_base     : dict   base parameter dict from load_params()
    param_name : str    key in p_base to override
    values     : list   values to sweep
    label      : str    display label for progress output; defaults to param_name

    Returns
    -------
    list of dicts, one per value:
      {
        'value':       float,
        'label':       str,
        'summary':     dict | None,   (None if skipped)
        'skipped':     bool,
        'skip_reason': str | None,
      }

    Migration notes
    ---------------
    rates_s_helpers.run_param_sweep(p_base, param_name, values, label)
        →  run_param_sweep(p_base, param_name, values, label)
    Identical signature and output structure.
    The only internal change: summarise() is now this module's version
    rather than rates_s_helpers'.  Output is identical.
    """
    from wdt_fmt import fmt_pct1  # avoid circular at module level

    if label is None:
        label = param_name

    results = []
    for v in values:
        p = deepcopy(p_base)
        p[param_name] = v

        # ── validation guards ────────────────────────────────────────────────
        def _skip(reason):
            results.append({
                'value': v, 'label': label,
                'summary': None, 'skipped': True,
                'skip_reason': reason,
            })
            print(f"  [{label}={v:.5g}]  SKIPPED ({reason})")

        if p.get('tau_0', 0) >= p.get('tau_m', 1):
            _skip(f"τ_0={p['tau_0']:.2f} >= τ_m={p['tau_m']:.2f}")
            continue
        if p.get('W_min', 0) < 0:
            _skip(f"W_min={p['W_min']} < 0")
            continue
        if p.get('srr_ratio', 1) <= 0:
            _skip(f"srr_ratio={p['srr_ratio']} <= 0")
            continue
        if p.get('lrr_years', 1) <= 0:
            _skip(f"lrr_years={p['lrr_years']} <= 0")
            continue

        # ── run ──────────────────────────────────────────────────────────────
        print(f"  [{label}={v:.5g}]  sweeping...", end='', flush=True)
        sweep = model.run_start_year_sweep(p)
        s = summarise(sweep)
        results.append({
            'value': v, 'label': label,
            'summary': s, 'skipped': False, 'skip_reason': None,
        })
        n_fail = s['n_lrr_failure']
        print(
            f"  done  success={s['success_rate']:.0f}%  "
            f"SSMcov{HEADLINE_WINDOW}={fmt_pct1(s['ssm_cov']['median'])}  "
            f"TCMcov{HEADLINE_WINDOW}={fmt_pct1(s['tcm_cov']['median'])}  "
            f"LRR_med={s['lrr_fill']['median']}  "
            f"LRRfail={n_fail}/{s['n_total']}"
        )

    return results
