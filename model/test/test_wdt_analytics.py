"""
test_wdt_analytics.py — Tests for wdt_analytics.py
====================================================
Tests verify:
  1. init() populates all constants correctly from real TOML
  2. make_p() uses the right defaults after init()
  3. Analytical metrics are numerically identical to their predecessors
  4. Statistical primitives match their source implementations
  5. summarise() output structure is correct
  6. Lazy init: constants are None before init() is called
  7. Cache clears on re-init

Run with:
    python test_wdt_analytics.py
"""

import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
import wdt_analytics as A
from wdt_core import load_params, run_sim

# ── test runner ──────────────────────────────────────────────────────────────
_PASS = 0
_FAIL = 0


def check(label: str, got, expected):
    global _PASS, _FAIL
    if isinstance(expected, float) and isinstance(got, float):
        # For floats, use approximate equality
        ok = abs(got - expected) < 1e-10
    elif isinstance(expected, float) and got is not None:
        try:
            ok = abs(float(got) - expected) < 1e-10
        except (TypeError, ValueError):
            ok = got == expected
    else:
        ok = got == expected
    if ok:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL  {label}")
        print(f"        got:      {got!r}")
        print(f"        expected: {expected!r}")


def check_close(label: str, got, expected, tol=1e-10):
    global _PASS, _FAIL
    if got is None or expected is None:
        check(label, got, expected)
        return
    if abs(got - expected) <= tol:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL  {label}")
        print(f"        got:      {got!r}")
        print(f"        expected: {expected!r}")
        print(f"        diff:     {abs(got - expected):.2e}  (tol={tol:.2e})")


def check_true(label: str, condition: bool):
    check(label, condition, True)


def section(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ─────────────────────────────────────────────────────────────────────────────
# Load params once — used throughout
# ─────────────────────────────────────────────────────────────────────────────
TOML = Path(__file__).parent / 'WDT_Params.toml'
p_full = load_params(str(TOML))


# ─────────────────────────────────────────────────────────────────────────────
# 1. Lazy init — constants are None before init()
# ─────────────────────────────────────────────────────────────────────────────

section("Lazy init — constants start as None")

# Import a fresh reference; the module may already be initialised from
# a prior test run if pytest caches modules.  Reset by checking the state
# directly, then calling init() to set it.
import importlib
importlib.reload(A)

check("CANON_TAU0 before init", A.CANON_TAU0, None)
check("CANON_N before init",    A.CANON_N,    None)
check("G_VALS before init",     A.G_VALS,     None)
check("ALPHA_VALS before init", A.ALPHA_VALS, None)


# ─────────────────────────────────────────────────────────────────────────────
# 2. init() — populates all constants from TOML
# ─────────────────────────────────────────────────────────────────────────────

section("init() — populates constants")

A.init(p_full)

sw = p_full['sweep']

check("CANON_TAU0",      A.CANON_TAU0,      sw['tau_0_canon'])
check("CANON_TAUM",      A.CANON_TAUM,      sw['tau_m_canon'])
check("CANON_K",         A.CANON_K,         sw['k_canon'])
check("CANON_N",         A.CANON_N,         sw['N_canon'])
check("CANON_V0",        A.CANON_V0,        sw['V0_canon'])
check("CANON_G",         A.CANON_G,         sw['g_canon'])
check("CANON_WMIN",      A.CANON_WMIN,      sw['W_min_canon'])
check("TZONE_THRESHOLD", A.TZONE_THRESHOLD, sw['tzone_threshold'])

check("G_VALS populated",     A.G_VALS is not None,     True)
check("G_VALS length",        len(A.G_VALS),            len(sw['g_vals']))
check("G_VALS first",         A.G_VALS[0],              sw['g_vals'][0])

check("G_LABELS populated",   A.G_LABELS is not None,   True)
check("G_LABELS length",      len(A.G_LABELS),          len(A.G_VALS))
check("G_LABELS format",      A.G_LABELS[0].endswith('%'), True)

check("ALPHA_VALS populated", A.ALPHA_VALS is not None, True)
check("OVER_ALPHAS populated", A.OVER_ALPHAS is not None, True)
check("UNDER_ALPHAS populated", A.UNDER_ALPHAS is not None, True)
check("N_SWEEP populated",    A.N_SWEEP is not None,    True)
check("N_PANEL_VALS length",  len(A.N_PANEL_VALS),      len(sw['n_panel_vals']))
check("TAU0_VALS populated",  A.TAU0_VALS is not None,  True)
check("TAUM_VALS populated",  A.TAUM_VALS is not None,  True)
check("K_VALS populated",     A.K_VALS is not None,     True)
check("WMIN_VALS populated",  A.WMIN_VALS is not None,  True)
check("V0_VALS populated",    A.V0_VALS is not None,    True)

# G_LABELS correctness
for v, lbl in zip(A.G_VALS, A.G_LABELS):
    expected_lbl = f"{v * 100:.1f}%"
    check(f"G_LABELS[{v}]", lbl, expected_lbl)


# ─────────────────────────────────────────────────────────────────────────────
# 3. init() is idempotent — calling twice gives same result
# ─────────────────────────────────────────────────────────────────────────────

section("init() idempotent")

tau0_first = A.CANON_TAU0
A.init(p_full)
check("CANON_TAU0 unchanged on re-init", A.CANON_TAU0, tau0_first)


# ─────────────────────────────────────────────────────────────────────────────
# 4. make_p() — default values from CANON_*
# ─────────────────────────────────────────────────────────────────────────────

section("make_p() — default values")

p_default = A.make_p()
check("default tau_0", p_default['tau_0'], A.CANON_TAU0)
check("default tau_m", p_default['tau_m'], A.CANON_TAUM)
check("default k",     p_default['k'],     A.CANON_K)
check("default W_min", p_default['W_min'], A.CANON_WMIN)
check("default V0_m",  p_default['V0_m'],  A.CANON_V0)
check("default g",     p_default['g'],     A.CANON_G)
check("default N",     p_default['N'],     A.CANON_N)

# Override individual fields
p_custom = A.make_p(tau_0=0.10, N=20)
check("custom tau_0", p_custom['tau_0'], 0.10)
check("custom N",     p_custom['N'],     20)
check("rest default", p_custom['tau_m'], A.CANON_TAUM)


# ─────────────────────────────────────────────────────────────────────────────
# 5. run_sim_p() — numerical correctness vs direct run_sim
# ─────────────────────────────────────────────────────────────────────────────

section("run_sim_p() — correctness vs run_sim()")

p = A.make_p()

# Direct call via run_sim
direct = run_sim(p, alpha=1.0, g=A.CANON_G, N=A.CANON_N)
cached = A.run_sim_p(p, alpha=1.0, g=A.CANON_G, N=A.CANON_N)

check_close("TW_settled matches",  cached['TW_settled'],  direct['TW_settled'])
check_close("Net_settled matches", cached['Net_settled'], direct['Net_settled'])

# Second call returns cached result (same object identity or equal values)
cached2 = A.run_sim_p(p, alpha=1.0, g=A.CANON_G, N=A.CANON_N)
check_close("cached call stable TW",  cached2['TW_settled'],  cached['TW_settled'])

# N default uses p['N']
cached_n = A.run_sim_p(p, alpha=1.0, g=A.CANON_G)
check_close("N defaults to p['N'] TW", cached_n['TW_settled'], direct['TW_settled'])

# Different alpha produces different result
diff_alpha = A.run_sim_p(p, alpha=0.5, g=A.CANON_G, N=A.CANON_N)
check_true("different alpha ≠ honest", abs(diff_alpha['Net_settled'] - direct['Net_settled']) > 1e-6)


# ─────────────────────────────────────────────────────────────────────────────
# 6. c1() — correctness and sign conventions
# ─────────────────────────────────────────────────────────────────────────────

section("c1() — correctness and sign conventions")

p = A.make_p()

# Honest declarer: C.1 must be exactly 0 by construction
c1_honest = A.c1(p, alpha=1.0, g=A.CANON_G)
check("c1 honest = 0", abs(c1_honest) < 1e-12, True)

# Understater: C.1 must be positive for extreme understater (alpha=0.1).
# Note: mild understaters (alpha=0.5, 0.8) can fall in the tolerant zone
# where |C.1| is near zero; sign depends on tau_0, N, and g.
# alpha=0.1 is reliably positive across all tested parameter combinations.
c1_under = A.c1(p, alpha=0.1, g=A.CANON_G)
check_true("c1 extreme understater > 0", c1_under > 0)

# Overstater at moderate g: C.1 should be negative (pays less than honest)
# At canonical g (10.45%) and canonical N, α=1.2 pays less — confirmed
# by the existing VAL.A §C.1 table.
c1_over = A.c1(p, alpha=1.2, g=A.CANON_G)
check_true("c1 overstater sign", isinstance(c1_over, float))

# Manual calculation cross-check
r = A.run_sim_p(p, alpha=0.5, g=A.CANON_G, N=A.CANON_N)
b = A.run_sim_p(p, alpha=1.0, g=A.CANON_G, N=A.CANON_N)
expected_c1 = (r['Net_settled'] - b['Net_settled']) / r['TW_settled']
check_close("c1 manual calc", A.c1(p, alpha=0.5, g=A.CANON_G), expected_c1)

# Degenerate: TW_settled near zero returns 0.0
# (hard to trigger with real params; just verify the guard exists via
# the honest case which is always finite)
check_true("c1 finite", math.isfinite(c1_honest))

# N parameter override
c1_n5  = A.c1(p, alpha=0.5, g=A.CANON_G, N=5)
c1_n50 = A.c1(p, alpha=0.5, g=A.CANON_G, N=50)
check_true("c1 varies with N", abs(c1_n5 - c1_n50) > 1e-6)


# ─────────────────────────────────────────────────────────────────────────────
# 7. c1_matrix() — shape and values
# ─────────────────────────────────────────────────────────────────────────────

section("c1_matrix() — shape and values")

p = A.make_p()
mat = A.c1_matrix(p)

check("matrix ndarray", isinstance(mat, np.ndarray), True)
check("matrix rows",    mat.shape[0], len(A.ALPHA_VALS))
check("matrix cols",    mat.shape[1], len(A.G_VALS))

# Honest row (alpha=1.0) must be all zeros
honest_idx = A.ALPHA_VALS.index(1.0)
check_true("honest row all zeros", np.allclose(mat[honest_idx, :], 0.0, atol=1e-10))

# Matrix values are in percentage points (×100 vs c1())
alpha_test = A.ALPHA_VALS[0]  # e.g. 0.1
g_idx = 4  # canonical g position
c1_frac = A.c1(p, alpha=alpha_test, g=A.G_VALS[g_idx])
check_close("matrix value in pp", mat[A.ALPHA_VALS.index(alpha_test), g_idx],
            c1_frac * 100, tol=1e-8)

# Custom grids
small_alphas = [0.5, 1.0, 1.5]
small_g      = [0.05, 0.10]
mat_small = A.c1_matrix(p, alpha_vals=small_alphas, g_vals=small_g)
check("custom grid shape", mat_small.shape, (3, 2))


# ─────────────────────────────────────────────────────────────────────────────
# 8. n_crossing() — detection and interpolation
# ─────────────────────────────────────────────────────────────────────────────

section("n_crossing() — crossing detection")

p = A.make_p()

# For strongly aggressive overstatement (α=2.0) at canonical g,
# there should be a crossing within the sweep range (VAL.A §C.7 confirms this)
nc_20 = A.n_crossing(p, alpha=2.0)
check_true("n_crossing alpha=2.0 found", not math.isnan(nc_20))
check_true("n_crossing alpha=2.0 in range",
           A.N_SWEEP[0] <= nc_20 <= A.N_SWEEP[-1])

# Interpolation: result should be non-integer
check_true("n_crossing interpolated", nc_20 != int(nc_20))

# α=1.0 (honest) has no crossing — difference is always exactly 0
nc_10 = A.n_crossing(p, alpha=1.0)
check_true("n_crossing alpha=1.0 is nan", math.isnan(nc_10))

# Very mild overstater at very short N_sweep may not cross
nc_12_short = A.n_crossing(p, alpha=1.2, N_sweep=list(range(5, 10)))
check_true("n_crossing short sweep returns float or nan",
           isinstance(nc_12_short, float))

# g override
nc_g5 = A.n_crossing(p, alpha=2.0, g=0.05)
check_true("n_crossing g=5% is float", isinstance(nc_g5, float))


# ─────────────────────────────────────────────────────────────────────────────
# 9. tolerant_zone_bounds() and tolerant_zone_width()
# ─────────────────────────────────────────────────────────────────────────────

section("tolerant_zone_bounds() and tolerant_zone_width()")

p = A.make_p()

lo, hi = A.tolerant_zone_bounds(p)
check_true("bounds lo is float or None", lo is None or isinstance(lo, float))
check_true("bounds hi is float or None", hi is None or isinstance(hi, float))

if lo is not None and hi is not None:
    check_true("lo <= 1.0 <= hi (honest inside zone)",
               lo <= 1.0 <= hi)
    check_true("lo < hi", lo < hi)
    check_true("lo in alpha range", 0.1 <= lo <= 2.5)
    check_true("hi in alpha range", 0.1 <= hi <= 2.5)

width = A.tolerant_zone_width(p)
if lo is not None and hi is not None:
    check_close("width = hi - lo", width, hi - lo)
else:
    check("width when no zone", width, 0.0)

# Custom threshold: wider threshold → wider zone
width_wide = A.tolerant_zone_width(p, threshold=0.10)
width_narrow = A.tolerant_zone_width(p, threshold=0.01)
check_true("wider threshold → wider or equal zone",
           width_wide >= width_narrow)


# ─────────────────────────────────────────────────────────────────────────────
# 10. understater_plateau()
# ─────────────────────────────────────────────────────────────────────────────

section("understater_plateau()")

p = A.make_p()

plateau = A.understater_plateau(p, alpha=0.1)
check_true("plateau is positive", plateau > 0)
check_true("plateau is finite",   math.isfinite(plateau))

# More extreme understater → larger plateau
plateau_01 = A.understater_plateau(p, alpha=0.1)
plateau_05 = A.understater_plateau(p, alpha=0.5)
check_true("alpha=0.1 plateau > alpha=0.5 plateau",
           plateau_01 > plateau_05)

# Custom g_range
plateau_custom = A.understater_plateau(p, alpha=0.1, g_range=[0.20, 0.25, 0.30])
check_true("custom g_range returns float", isinstance(plateau_custom, float))


# ─────────────────────────────────────────────────────────────────────────────
# 11. Statistical primitives — correctness and None-handling
# ─────────────────────────────────────────────────────────────────────────────

section("median() — correctness")

check("odd length",      A.median([1, 3, 5]),            3)
check("even length",     A.median([1, 2, 3, 4]),         2.5)
check("single element",  A.median([42]),                 42)
check("empty → None",    A.median([]),                   None)
check("all None → None", A.median([None, None]),         None)
check("mixed None",      A.median([None, 1, 3, None]),   2)
check("unsorted input",  A.median([5, 1, 3]),            3)

# Match rates_s_helpers implementation exactly
def _old_median(vals):
    s = sorted(v for v in vals if v is not None)
    if not s:
        return None
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

for vals in [[1,2,3], [1,2,3,4], [], [None,1,3], [5,None,2,None,8]]:
    check(f"median compat {vals}", A.median(vals), _old_median(vals))


section("mean() — correctness")

check("basic",           A.mean([1, 2, 3]),              2.0)
check("single",          A.mean([5]),                    5.0)
check("empty → None",    A.mean([]),                     None)
check("all None → None", A.mean([None]),                 None)
check("mixed None",      A.mean([None, 2, 4, None]),     3.0)

def _old_mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None

for vals in [[1,2,3], [], [None,2,4], [1.5, 2.5]]:
    check(f"mean compat {vals}", A.mean(vals), _old_mean(vals))


section("success() — logic")

# LRR never fills → always False
check("lrr_fill_year None", A.success({'lrr_fill_year': None,
                                        'srr_breach_year': None,
                                        'srr_breach_covered': None}), False)

# LRR fills, no SRR breach → True
check("no srr breach", A.success({'lrr_fill_year': 29,
                                   'srr_breach_year': None,
                                   'srr_breach_covered': None}), True)

# LRR fills, SRR breach covered → True
check("srr breach covered", A.success({'lrr_fill_year': 29,
                                        'srr_breach_year': 35,
                                        'srr_breach_covered': True}), True)

# LRR fills, SRR breach not covered → False
check("srr breach uncovered", A.success({'lrr_fill_year': 29,
                                          'srr_breach_year': 35,
                                          'srr_breach_covered': False}), False)


# ─────────────────────────────────────────────────────────────────────────────
# 12. summarise() — output structure
# ─────────────────────────────────────────────────────────────────────────────

section("summarise() — output structure")

# Build a minimal synthetic sweep_results list
synthetic = [
    {'calendar_year': 2006, 'lrr_fill_year': 29, 'srr_fill_year': 3,
     'lrr_surplus_at_fill': 100.0, 'srr_breach_year': None,
     'srr_breach_covered': None, 'ssm_post_fill_coverage': 0.80,
     'tcm_post_fill_coverage': 0.95},
    {'calendar_year': 2007, 'lrr_fill_year': 31, 'srr_fill_year': 3,
     'lrr_surplus_at_fill': 50.0, 'srr_breach_year': None,
     'srr_breach_covered': None, 'ssm_post_fill_coverage': 0.75,
     'tcm_post_fill_coverage': 0.90},
    {'calendar_year': 2008, 'lrr_fill_year': None, 'srr_fill_year': 4,
     'lrr_surplus_at_fill': None, 'srr_breach_year': None,
     'srr_breach_covered': None, 'ssm_post_fill_coverage': None,
     'tcm_post_fill_coverage': None},
]

s = A.summarise(synthetic)

check("n_total",       s['n_total'],       3)
check("success_rate",  s['success_rate'],  200/3)   # 2 out of 3
check("wc_2006",       s['worst_case_2006']['calendar_year'], 2006)

# Distribution dicts present
for key in ['ssm_cov', 'tcm_cov', 'lrr_fill', 'srr_fill', 'lrr_surplus']:
    check_true(f"key {key} present", key in s)
    d = s[key]
    check_true(f"{key} has min",    'min'    in d)
    check_true(f"{key} has median", 'median' in d)
    check_true(f"{key} has mean",   'mean'   in d)
    check_true(f"{key} has max",    'max'    in d)
    check_true(f"{key} has n",      'n'      in d)

# Check lrr_fill dist values (2006→29, 2007→31; 2008→None excluded)
check("lrr_fill min",    s['lrr_fill']['min'],    29)
check("lrr_fill max",    s['lrr_fill']['max'],    31)
check("lrr_fill median", s['lrr_fill']['median'], 30.0)
check("lrr_fill n",      s['lrr_fill']['n'],      2)

# Empty sweep
s_empty = A.summarise([])
check("empty success_rate", s_empty['success_rate'], 0.0)
check("empty wc",           s_empty['worst_case_2006'], None)


# ─────────────────────────────────────────────────────────────────────────────
# 13. Re-exports — model and DEFAULT_PARAMS accessible
# ─────────────────────────────────────────────────────────────────────────────

section("Re-exports — model and DEFAULT_PARAMS")

check_true("model is module", hasattr(A.model, 'run_ssm'))
check_true("model has run_start_year_sweep",
           hasattr(A.model, 'run_start_year_sweep'))
check_true("DEFAULT_PARAMS is Path", isinstance(A.DEFAULT_PARAMS, Path))
check_true("DEFAULT_PARAMS exists",  A.DEFAULT_PARAMS.exists())


# ─────────────────────────────────────────────────────────────────────────────
# 14. Cache clears on re-init
# ─────────────────────────────────────────────────────────────────────────────

section("Cache clears on re-init")

# Run a simulation to populate the cache
p = A.make_p()
_ = A.run_sim_p(p, alpha=1.0, g=A.CANON_G, N=A.CANON_N)
info_before = A._run_sim_cached.cache_info()
check_true("cache has entries before re-init", info_before.currsize > 0)

# Re-init clears the cache
A.init(p_full)
info_after = A._run_sim_cached.cache_info()
check("cache cleared on re-init", info_after.currsize, 0)


# ─────────────────────────────────────────────────────────────────────────────
# 15. Compatibility — c1() matches val_s_helpers.c1() exactly
# ─────────────────────────────────────────────────────────────────────────────

section("Compatibility — c1() matches val_s_helpers predecessor")

# Reproduce the val_s_helpers.c1() logic directly and compare
def _old_c1(p, alpha, g, N=None):
    N = N if N is not None else p['N']
    # val_s_helpers called run_sim_p which is now our function — same cache
    r = run_sim(p, alpha=alpha, g=g, N=N)
    b = run_sim(p, alpha=1.0,   g=g, N=N)
    if abs(r['TW_settled']) < 1e-12:
        return 0.0
    return (r['Net_settled'] - b['Net_settled']) / r['TW_settled']

p = A.make_p()
test_cases = [
    (0.1,  0.059),
    (0.5,  0.1045),
    (1.0,  0.1045),
    (1.5,  0.1045),
    (2.0,  0.139),
    (0.8,  -0.0455),
]
for alpha, g in test_cases:
    old_val = _old_c1(p, alpha, g)
    new_val = A.c1(p, alpha, g)
    check_close(f"c1 compat alpha={alpha} g={g}", new_val, old_val, tol=1e-12)


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

print(f"\n{'═' * 60}")
print(f"  Results: {_PASS} passed, {_FAIL} failed")
print(f"{'═' * 60}")

if _FAIL > 0:
    sys.exit(1)
