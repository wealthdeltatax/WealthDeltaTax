"""
wdt_style.py — WDT Unified Figure Style and Colour Palette
===========================================================
Single source of truth for all matplotlib configuration, colour constants,
figure-size constants, and figure-saving logic used across VAL, VAL.S,
RATES, and RATES.S output scripts.

Replaces
--------
  val_s_helpers.py       _STYLE_BASE, set_style(), set_style_nogrid(), save_fig()
  5_6_VAL_figures.py     set_style(), _save(), DPI, FONT, FSIZE,
                         UNDER_COLS, HONEST_COL, OVER_COLS
  8_3_RATES_output.py    _apply_base_style(), _save(), CYCLE_BUCKETS_CHART
  16_7_RATES_S_charts.py _base_style(), _save(), C_SSM/TCM/LRR/SURPLUS/BASELINE,
                         PARAM_COLOURS

Public API
----------
Style
  apply_style(grid=True)       set rcParams; grid=False for heatmaps
  apply_style_grid()           shorthand — with grid
  apply_style_nogrid()         shorthand — without grid (heatmaps / imshow)

Saving
  save_fig(fig, path)          save at DPI_PRINT, close, print path; returns Path

Figure sizes (width, height in inches)
  FIG_SINGLE    (9, 5.5)       single-panel line/scatter
  FIG_SINGLE_W  (10, 5.5)     single-panel, slightly wider
  FIG_WIDE      (13, 6)        wide single-panel (RATES)
  FIG_WIDE_L    (14, 6)        wide single-panel, large
  FIG_PAIR      (14, 5.5)      two panels side by side
  FIG_PAIR_T    (14, 6.5)      two panels, taller
  FIG_PAIR_XW   (16, 5.5)     two panels, extra-wide
  FIG_QUAD      (14, 9)        2×2 panel grid
  FIG_QUAD_T    (13, 9)        2×2 panel grid, slightly narrower
  FIG_QUAD_XL   (14, 10)      2×2 panel grid, tall

DPI
  DPI_SCREEN    150            screen preview / VAL_S figures
  DPI_PRINT     300            publication output (canonical; all save_fig calls)

Colours — declaration strategies
  C_UNDER       list of 4 reds (most→least extreme understatement)
  C_HONEST      near-black (honest declarer reference lines)
  C_OVER        list of 4 blues (least→most extreme overstatement)
  C_OVER_LIGHT  list of 4 light blues (used in fig 07 / fig 09)

Colours — SWF / RATES model outputs
  C_SSM         blue   (#4e79a7) — SSM correlated-shock floor
  C_TCM         amber  (#f28e2b) — TCM heterogeneity ceiling
  C_LRR         green  (#59a14f) — LRR fill year / accumulation
  C_SURPLUS     purple (#9467bd) — LRR surplus
  C_BASELINE    red    (#e15759) — baseline parameter marker

Colours — rate parameters (sweep figures)
  C_TAU0        blue   (#4e79a7)
  C_TAUM        amber  (#f28e2b)
  C_K           green  (#59a14f)
  C_WMIN        purple (#9467bd)
  PARAM_COLOURS dict   {'tau_0': C_TAU0, 'tau_m': C_TAUM, ...}

Colours — misc
  C_GRID        light grey (#e0e0e0) — grid lines
  C_ANNOTATION  mid-grey   (#888888) — reference lines, text
  C_DARK        near-black (#1a1a1a) — primary axis text, outlines

Cycle buckets (RATES start-year sweep)
  CYCLE_BUCKETS  list of (label, yr_from, yr_to, colour)

Design notes
------------
Canonical DPI for all saved output is DPI_PRINT (300).  The old code had
150 in val_s_helpers (screen preview) and 300 in 8_3/16_7 (print).  We
normalise to 300 everywhere — this is the one intentional visual change.
Scripts that previously called save at 150 dpi will now save at 300 dpi;
files will be larger but sharper.  If you want 150-dpi previews, pass
dpi=DPI_SCREEN to matplotlib directly before calling save_fig is not needed —
save_fig always writes the print-quality file.

The font is unified to 'DejaVu Sans'.  The old 8_3 and 16_7 used 'serif',
which mapped to a platform-dependent font.  'DejaVu Sans' is the matplotlib
default and is always available.

No matplotlib import at module level — matplotlib is imported lazily inside
apply_style() so this module is safe to import in non-plotting contexts
(e.g. when running only the markdown output path).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# DPI CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

DPI_SCREEN: int = 150   # quick screen preview
DPI_PRINT:  int = 300   # canonical save DPI (all save_fig() calls)


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE SIZE CONSTANTS  (width, height) in inches
# ─────────────────────────────────────────────────────────────────────────────

FIG_SINGLE:  Tuple[float, float] = (9,  5.5)   # single-panel line/scatter
FIG_SINGLE_W: Tuple[float, float] = (10, 5.5)  # single-panel, slightly wider
FIG_WIDE:    Tuple[float, float] = (13, 6)      # wide single-panel (RATES)
FIG_WIDE_L:  Tuple[float, float] = (14, 6)      # wide single-panel, large
FIG_PAIR:    Tuple[float, float] = (14, 5.5)    # two panels side by side
FIG_PAIR_T:  Tuple[float, float] = (14, 6.5)   # two panels, taller
FIG_PAIR_XW: Tuple[float, float] = (16, 5.5)   # two panels, extra-wide
FIG_QUAD:    Tuple[float, float] = (14, 9)      # 2×2 panel grid
FIG_QUAD_T:  Tuple[float, float] = (13, 9)      # 2×2 panel grid, narrower
FIG_QUAD_XL: Tuple[float, float] = (14, 10)    # 2×2 panel grid, tall


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE — declaration strategies
# ─────────────────────────────────────────────────────────────────────────────

# Understater reds: most extreme (α=0.1) → least extreme (α=0.8)
C_UNDER: List[str] = ['#b30000', '#d73027', '#f46d43', '#fdae61']

# Honest declarer reference colour
C_HONEST: str = '#1a1a1a'

# Overstater blues: least extreme (α=1.2) → most extreme (α=2.0)
C_OVER: List[str] = ['#4393c3', '#2166ac', '#053061', '#313695']

# Light blues — used in fig 07/09 for the overstater surface panels
C_OVER_LIGHT: List[str] = ['#74add1', '#4393c3', '#2166ac', '#053061']


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE — SWF / RATES model outputs
# ─────────────────────────────────────────────────────────────────────────────

C_SSM:     str = '#4e79a7'   # blue   — SSM correlated-shock floor
C_TCM:     str = '#f28e2b'   # amber  — TCM heterogeneity ceiling
C_LRR:     str = '#59a14f'   # green  — LRR fill year / accumulation
C_SURPLUS: str = '#9467bd'   # purple — LRR surplus
C_BASELINE: str = '#e15759'  # red    — baseline parameter marker / crash


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE — rate parameter sweep (16_7 / RATES_S)
# ─────────────────────────────────────────────────────────────────────────────

C_TAU0: str = '#4e79a7'   # same blue as SSM — τ₀ parameter
C_TAUM: str = '#f28e2b'   # same amber as TCM — τ_m parameter
C_K:    str = '#59a14f'   # same green as LRR — k parameter
C_WMIN: str = '#9467bd'   # same purple as surplus — W_min parameter

PARAM_COLOURS: dict = {
    'tau_0': C_TAU0,
    'tau_m': C_TAUM,
    'k':     C_K,
    'W_min': C_WMIN,
}


# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE — miscellaneous
# ─────────────────────────────────────────────────────────────────────────────

C_GRID:       str = '#e0e0e0'   # grid lines
C_ANNOTATION: str = '#888888'   # reference lines, secondary text
C_DARK:       str = '#1a1a1a'   # primary axis text, outlines


# ─────────────────────────────────────────────────────────────────────────────
# CYCLE BUCKETS — RATES start-year sweep colouring
# ─────────────────────────────────────────────────────────────────────────────

# Each entry: (label, year_from, year_to, colour_hex)
# Colours match the RATES figures — blue/amber/green/red per era.
CYCLE_BUCKETS: List[Tuple[str, int, int, str]] = [
    ('Post-war growth 1947–59', 1947, 1959, C_SSM),      # blue
    ('Long boom 1960–79',       1960, 1979, C_TCM),      # amber
    ('Liberalisation 1980–99',  1980, 1999, C_LRR),      # green
    ('Crisis decade 2000–19',   2000, 2019, C_BASELINE), # red
]


# ─────────────────────────────────────────────────────────────────────────────
# STYLE APPLICATION
# ─────────────────────────────────────────────────────────────────────────────

# Canonical rcParams shared by all figure types
_BASE_PARAMS: dict = {
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

_GRID_PARAMS: dict = {
    'axes.grid':      True,
    'grid.color':     C_GRID,
    'grid.linewidth': 0.6,
    'grid.alpha':     1.0,
    'grid.linestyle': '-',
}

_NOGRID_PARAMS: dict = {
    'axes.grid': False,
}


def apply_style(grid: bool = True) -> None:
    """
    Apply the canonical WDT figure style to matplotlib rcParams.

    Parameters
    ----------
    grid : bool   True (default) = light grid; False = no grid (for heatmaps)

    Call this at the start of every figure function, before creating axes.

    Migration notes
    ---------------
    val_s_helpers.set_style()          → apply_style(grid=True)
    val_s_helpers.set_style_nogrid()   → apply_style(grid=False)
    5_6.set_style()                    → apply_style(grid=True)
    8_3._apply_base_style()            → apply_style(grid=True)
    16_7._base_style()                 → apply_style(grid=True)
    16_4: set_style = set_style_nogrid → apply_style(grid=False)

    Font change: 8_3 and 16_7 used 'serif' (platform-dependent).
    All scripts now use 'DejaVu Sans' (always available in matplotlib).

    Grid change: 8_3 used grid.alpha=0.3, grid.linestyle='--'.
                 16_7 used grid.alpha=0.25, grid.linestyle='--'.
                 Unified to alpha=1.0, linestyle='-', color='#e0e0e0'
                 which is visually equivalent at the lighter colour.
    """
    import matplotlib.pyplot as plt
    params = {**_BASE_PARAMS}
    if grid:
        params.update(_GRID_PARAMS)
    else:
        params.update(_NOGRID_PARAMS)
    plt.rcParams.update(params)


def apply_style_grid() -> None:
    """apply_style(grid=True) — standard line/scatter/bar figures."""
    apply_style(grid=True)


def apply_style_nogrid() -> None:
    """apply_style(grid=False) — heatmaps and imshow figures."""
    apply_style(grid=False)


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE SAVING
# ─────────────────────────────────────────────────────────────────────────────

def save_fig(fig, path: Path, dpi: int = DPI_PRINT, verbose: bool = True) -> Path:
    """
    Save a matplotlib figure, close it, and optionally print the path.

    Parameters
    ----------
    fig     : matplotlib.figure.Figure
    path    : Path   full destination path including filename and extension
    dpi     : int    resolution (default DPI_PRINT = 300)
    verbose : bool   if True, prints "  Saved: {path}" (default True)

    Returns
    -------
    Path   the path written to

    The parent directory is created automatically if it does not exist.

    Migration notes
    ---------------
    val_s_helpers.save_fig(fig, name, out_dir=None)
        → save_fig(fig, out_dir('VAL_S') / name)
          [DPI changes from 150 → 300]

    5_6._save(fig, name)
        → save_fig(fig, out_dir('VAL') / name)
          [DPI unchanged: was 150; now 300 — intentional normalisation]

    8_3._save(fig, output_dir, name)
        → save_fig(fig, Path(output_dir) / name)
          [DPI unchanged: was 300]

    16_7._save(fig, output_dir, name)
        → save_fig(fig, Path(output_dir) / name)
          [DPI unchanged: was 300]

    Call sites in 16_2/16_3/16_4 that do:
        save = save_fig
        save(fig, 'filename.png')
    become:
        from wdt_style import save_fig
        from wdt_fmt import out_dir
        _OUT = out_dir('VAL_S')
        save_fig(fig, _OUT / 'filename.png')
    """
    import matplotlib.pyplot as plt
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    if verbose:
        print(f'  Saved: {path}')
    return path
