"""
test_wdt_style.py — Tests for wdt_style.py
===========================================
Tests verify:
  1. All constants have correct values (matching their predecessor sources)
  2. apply_style() sets rcParams correctly
  3. save_fig() creates a real file and closes the figure
  4. Colour palette internal consistency

Run with:
    python test_wdt_style.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wdt_style as S

# ── test runner ──────────────────────────────────────────────────────────────
_PASS = 0
_FAIL = 0


def check(label: str, got, expected):
    global _PASS, _FAIL
    if got == expected:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL  {label}")
        print(f"        got:      {got!r}")
        print(f"        expected: {expected!r}")


def check_true(label: str, condition: bool):
    check(label, condition, True)


def section(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. DPI constants
# ─────────────────────────────────────────────────────────────────────────────

section("DPI constants")

check("DPI_SCREEN", S.DPI_SCREEN, 150)
check("DPI_PRINT",  S.DPI_PRINT,  300)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Figure size constants — values and types
# ─────────────────────────────────────────────────────────────────────────────

section("Figure size constants")

# Check type and basic geometry
for name, val, expected_w, expected_h in [
    ('FIG_SINGLE',   S.FIG_SINGLE,   9,  5.5),
    ('FIG_SINGLE_W', S.FIG_SINGLE_W, 10, 5.5),
    ('FIG_WIDE',     S.FIG_WIDE,     13, 6),
    ('FIG_WIDE_L',   S.FIG_WIDE_L,   14, 6),
    ('FIG_PAIR',     S.FIG_PAIR,     14, 5.5),
    ('FIG_PAIR_T',   S.FIG_PAIR_T,   14, 6.5),
    ('FIG_PAIR_XW',  S.FIG_PAIR_XW,  16, 5.5),
    ('FIG_QUAD',     S.FIG_QUAD,     14, 9),
    ('FIG_QUAD_T',   S.FIG_QUAD_T,   13, 9),
    ('FIG_QUAD_XL',  S.FIG_QUAD_XL,  14, 10),
]:
    check_true(f"{name} is tuple", isinstance(val, tuple))
    check(f"{name} width",  val[0], expected_w)
    check(f"{name} height", val[1], expected_h)

# Verify the figsize constants cover the values used in the codebase
# (9, 5.5) — most VAL_S single panels
check("FSIZE compat FIG_SINGLE", S.FIG_SINGLE, (9, 5.5))
# (14, 9) — most VAL_S 2×2 grids
check("quad grid size", S.FIG_QUAD, (14, 9))


# ─────────────────────────────────────────────────────────────────────────────
# 3. Colour palette — declaration strategies
# ─────────────────────────────────────────────────────────────────────────────

section("Colour palette — declaration strategies")

# C_UNDER — must match 5_6.UNDER_COLS exactly
UNDER_COLS_ORIGINAL = ['#b30000', '#d73027', '#f46d43', '#fdae61']
check("C_UNDER length", len(S.C_UNDER), 4)
check("C_UNDER values", S.C_UNDER, UNDER_COLS_ORIGINAL)

# C_HONEST — must match 5_6.HONEST_COL
check("C_HONEST", S.C_HONEST, '#1a1a1a')

# C_OVER — must match 5_6.OVER_COLS
OVER_COLS_ORIGINAL = ['#4393c3', '#2166ac', '#053061', '#313695']
check("C_OVER length", len(S.C_OVER), 4)
check("C_OVER values", S.C_OVER, OVER_COLS_ORIGINAL)

# C_OVER_LIGHT — must match 5_6._FIG07_OVER_COLS
OVER_LIGHT_ORIGINAL = ['#74add1', '#4393c3', '#2166ac', '#053061']
check("C_OVER_LIGHT length", len(S.C_OVER_LIGHT), 4)
check("C_OVER_LIGHT values", S.C_OVER_LIGHT, OVER_LIGHT_ORIGINAL)

# All colour strings start with '#' and are 7 chars
for cname, cval in [
    ('C_HONEST', S.C_HONEST),
    ('C_GRID', S.C_GRID),
    ('C_ANNOTATION', S.C_ANNOTATION),
    ('C_DARK', S.C_DARK),
]:
    check_true(f"{cname} format", cval.startswith('#') and len(cval) == 7)

for col in S.C_UNDER + S.C_OVER + S.C_OVER_LIGHT:
    check_true(f"colour {col} format", col.startswith('#') and len(col) == 7)


# ─────────────────────────────────────────────────────────────────────────────
# 4. Colour palette — SWF / RATES
# ─────────────────────────────────────────────────────────────────────────────

section("Colour palette — SWF/RATES")

# Must match 16_7 constants exactly
check("C_SSM",      S.C_SSM,      '#4e79a7')
check("C_TCM",      S.C_TCM,      '#f28e2b')
check("C_LRR",      S.C_LRR,      '#59a14f')
check("C_SURPLUS",  S.C_SURPLUS,  '#9467bd')
check("C_BASELINE", S.C_BASELINE, '#e15759')


# ─────────────────────────────────────────────────────────────────────────────
# 5. PARAM_COLOURS dict
# ─────────────────────────────────────────────────────────────────────────────

section("PARAM_COLOURS dict")

# Must match 16_7.PARAM_COLOURS exactly
PARAM_COLOURS_ORIGINAL = {
    'tau_0': '#4e79a7',
    'tau_m': '#f28e2b',
    'k':     '#59a14f',
    'W_min': '#9467bd',
}
check("PARAM_COLOURS keys",   set(S.PARAM_COLOURS.keys()), set(PARAM_COLOURS_ORIGINAL.keys()))
check("PARAM_COLOURS tau_0",  S.PARAM_COLOURS['tau_0'], '#4e79a7')
check("PARAM_COLOURS tau_m",  S.PARAM_COLOURS['tau_m'], '#f28e2b')
check("PARAM_COLOURS k",      S.PARAM_COLOURS['k'],     '#59a14f')
check("PARAM_COLOURS W_min",  S.PARAM_COLOURS['W_min'], '#9467bd')

# Verify tau_0 matches C_SSM (shared colour, both are blue)
check("tau_0 == C_SSM", S.PARAM_COLOURS['tau_0'], S.C_SSM)
check("tau_0 == C_TAU0", S.PARAM_COLOURS['tau_0'], S.C_TAU0)


# ─────────────────────────────────────────────────────────────────────────────
# 6. CYCLE_BUCKETS
# ─────────────────────────────────────────────────────────────────────────────

section("CYCLE_BUCKETS")

ORIGINAL = [
    ('Post-war growth 1947–59', 1947, 1959, '#4e79a7'),
    ('Long boom 1960–79',       1960, 1979, '#f28e2b'),
    ('Liberalisation 1980–99',  1980, 1999, '#59a14f'),
    ('Crisis decade 2000–19',   2000, 2019, '#e15759'),
]

check("CYCLE_BUCKETS length", len(S.CYCLE_BUCKETS), 4)
for i, (orig, got) in enumerate(zip(ORIGINAL, S.CYCLE_BUCKETS)):
    check(f"bucket {i} label",    got[0], orig[0])
    check(f"bucket {i} yr_from",  got[1], orig[1])
    check(f"bucket {i} yr_to",    got[2], orig[2])
    check(f"bucket {i} colour",   got[3], orig[3])

# Year ranges must be contiguous and non-overlapping
years = [(b[1], b[2]) for b in S.CYCLE_BUCKETS]
for i in range(len(years) - 1):
    check_true(f"bucket {i} ends before {i+1} starts",
               years[i][1] < years[i+1][0])

# Colours must match SWF colours (they share the palette)
check("bucket 0 = C_SSM",      S.CYCLE_BUCKETS[0][3], S.C_SSM)
check("bucket 1 = C_TCM",      S.CYCLE_BUCKETS[1][3], S.C_TCM)
check("bucket 2 = C_LRR",      S.CYCLE_BUCKETS[2][3], S.C_LRR)
check("bucket 3 = C_BASELINE", S.CYCLE_BUCKETS[3][3], S.C_BASELINE)


# ─────────────────────────────────────────────────────────────────────────────
# 7. apply_style — rcParams set correctly
# ─────────────────────────────────────────────────────────────────────────────

section("apply_style — rcParams")

import matplotlib
matplotlib.use('Agg')   # non-interactive backend for tests
import matplotlib.pyplot as plt

# With grid
S.apply_style(grid=True)
check("grid=True axes.grid",      plt.rcParams['axes.grid'],       True)
check("grid=True grid.color",     plt.rcParams['grid.color'],      S.C_GRID)
check("grid=True grid.linewidth", plt.rcParams['grid.linewidth'],  0.6)
check("font.family",              plt.rcParams['font.family'],     ['DejaVu Sans'])
check("axes.spines.top",          plt.rcParams['axes.spines.top'], False)
check("axes.spines.right",        plt.rcParams['axes.spines.right'], False)
check("figure.facecolor",         plt.rcParams['figure.facecolor'], 'white')
check("axes.facecolor",           plt.rcParams['axes.facecolor'],   'white')

# Without grid
S.apply_style(grid=False)
check("grid=False axes.grid", plt.rcParams['axes.grid'], False)
# Base params still set
check("nogrid font still set", plt.rcParams['font.family'], ['DejaVu Sans'])

# Shorthands
S.apply_style_grid()
check("apply_style_grid sets grid", plt.rcParams['axes.grid'], True)

S.apply_style_nogrid()
check("apply_style_nogrid clears grid", plt.rcParams['axes.grid'], False)


# ─────────────────────────────────────────────────────────────────────────────
# 8. save_fig — file I/O
# ─────────────────────────────────────────────────────────────────────────────

section("save_fig — file I/O")

import matplotlib.pyplot as plt

with tempfile.TemporaryDirectory() as tmp:
    # Basic save
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot([1, 2], [3, 4])
    path = Path(tmp) / 'test_fig.png'
    returned = S.save_fig(fig, path, verbose=False)

    check("save_fig creates file",  path.exists(),  True)
    check("save_fig returns path",  returned,       path)
    check("file is non-empty",      path.stat().st_size > 0, True)

    # Figure should be closed after save — creating a new one should work
    fig2, ax2 = plt.subplots()
    ax2.plot([1], [1])
    path2 = Path(tmp) / 'sub' / 'dir' / 'fig2.png'
    S.save_fig(fig2, path2, verbose=False)
    check("save_fig creates parent dirs", path2.exists(), True)

    # DPI parameter respected — higher DPI → larger file
    fig3a, ax3a = plt.subplots(figsize=(4, 3))
    ax3a.plot([1, 2], [3, 4])
    path3a = Path(tmp) / 'lo_dpi.png'
    S.save_fig(fig3a, path3a, dpi=72, verbose=False)

    fig3b, ax3b = plt.subplots(figsize=(4, 3))
    ax3b.plot([1, 2], [3, 4])
    path3b = Path(tmp) / 'hi_dpi.png'
    S.save_fig(fig3b, path3b, dpi=300, verbose=False)

    check("higher DPI → larger file",
          path3b.stat().st_size > path3a.stat().st_size, True)

    # Verify figure is closed (plt.get_fignums() returns open figures)
    open_before = len(plt.get_fignums())
    fig4, _ = plt.subplots()
    open_mid = len(plt.get_fignums())
    S.save_fig(fig4, Path(tmp) / 'tmp4.png', verbose=False)
    open_after = len(plt.get_fignums())
    check("figure opened before save", open_mid, open_before + 1)
    check("figure closed after save",  open_after, open_before)

plt.close('all')


# ─────────────────────────────────────────────────────────────────────────────
# 9. Palette internal consistency
# ─────────────────────────────────────────────────────────────────────────────

section("Palette internal consistency")

# PARAM_COLOURS values match individual C_ constants
check("C_TAU0 == C_SSM",    S.C_TAU0, S.C_SSM)
check("C_TAUM == C_TCM",    S.C_TAUM, S.C_TCM)
check("C_K    == C_LRR",    S.C_K,    S.C_LRR)
check("C_WMIN == C_SURPLUS", S.C_WMIN, S.C_SURPLUS)

# C_DARK is the same as C_HONEST (both near-black #1a1a1a)
check("C_DARK == C_HONEST", S.C_DARK, S.C_HONEST)

# C_UNDER and C_OVER have no colours in common (reds vs blues)
under_set = set(S.C_UNDER)
over_set  = set(S.C_OVER)
check_true("C_UNDER ∩ C_OVER = ∅", len(under_set & over_set) == 0)

# All named colours are valid hex strings
all_named = [
    S.C_SSM, S.C_TCM, S.C_LRR, S.C_SURPLUS, S.C_BASELINE,
    S.C_TAU0, S.C_TAUM, S.C_K, S.C_WMIN,
    S.C_GRID, S.C_ANNOTATION, S.C_DARK, S.C_HONEST,
]
for col in all_named:
    check_true(f"{col} is valid hex", col.startswith('#') and len(col) == 7)
    int(col[1:], 16)   # raises if not valid hex — test will error not fail


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

print(f"\n{'═' * 60}")
print(f"  Results: {_PASS} passed, {_FAIL} failed")
print(f"{'═' * 60}")

if _FAIL > 0:
    sys.exit(1)
