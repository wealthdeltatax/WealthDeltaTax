"""
wdt_fmt.py — WDT Unified Formatting Utilities
==============================================
Single source of truth for all number, currency, and string formatting
used across VAL, VAL.S, RATES, and RATES.S output scripts.

Replaces
--------
  val_helpers.py          fm(), fp(), pct_str(), fmt_val(), eff_rate()
  rates_s_helpers.py      fmt_pct(), fmt_f(), baseline_marker(), dist_row()
  8_3 (local)             _fmt_gbp(), _fmt_m()

Public API
----------
Percentage formatting
  fmt_pct(v, dp=2)            fraction → "12.34%";  None → "—"
  fmt_pct1(v)                 shorthand for fmt_pct(v, dp=1)
  fmt_pct0(v)                 shorthand for fmt_pct(v, dp=0)

Currency formatting
  fmt_gbp_m(v, dp=3)          £m value  → "£12.345m";  None → "—"
  fmt_gbp_b(v, dp=1)          £b value  → "£12.3b";    None → "—"
  fmt_gbp_yr(v, threshold=0.5)  £/yr value, suppress near-zero → "£12,345" or "£—"
  fmt_rev_m(v, threshold=5e-4)  £m/yr revenue, suppress near-zero → "£12,345m" or "£—"

Float formatting
  fmt_f(v, spec='.1f')        float with format spec; None → "—"
  fmt_f0(v)                   shorthand for fmt_f(v, '0f')  (integer display)
  fmt_f2(v)                   shorthand for fmt_f(v, '.2f')
  fmt_f4(v)                   shorthand for fmt_f(v, '.4f')

Effective rate (convenience)
  eff_rate(sim_result)        Net_settled / TW_settled; 0.0 if degenerate

Distribution row formatting
  dist_row(d, fmt_fn)         "min / med / mean / max" from a dist dict
  baseline_marker(v, bv)      " ◄" if v ≈ bv else ""

Date
  today_iso()                 ISO date string for today

Output path helpers
  out_dir(subdir)             project_root / OUTPUTS / subdir  (Path)
  ensure_dir(path)            mkdir -p; returns path unchanged

Design notes
------------
- Every function that accepts a numeric value also accepts None and
  returns "—" (em-dash) in that case, making it safe to use with
  dict.get() results that may be absent.
- The two pct defaults (2dp for VAL, 1dp for RATES.S) are preserved
  as the dp= parameter; callers that previously used the 1dp default
  of rates_s_helpers.fmt_pct should pass dp=1 explicitly, or use
  the fmt_pct1 shorthand.
- fmt_gbp_m replaces both fm() and the inline £{v:.3f}m patterns.
  fp() is replaced by fmt_pct(v, dp=2).
- No matplotlib dependency; no wdt_core dependency. This module is
  safe to import anywhere without side effects.
"""

import datetime
from pathlib import Path

# ─── project root ────────────────────────────────────────────────────────────
# Resolve once at import time. All other path helpers are derived from this.
_ROOT = Path(__file__).parent


# ─────────────────────────────────────────────────────────────────────────────
# PERCENTAGE FORMATTING
# ─────────────────────────────────────────────────────────────────────────────

def fmt_pct(v, dp: int = 2) -> str:
    """
    Format a fraction (0.0–1.0) as a percentage string.

    Parameters
    ----------
    v  : float | None   fraction; None returns "—"
    dp : int            decimal places (default 2)

    Returns
    -------
    str   e.g. "12.34%" or "—"

    Migration notes
    ---------------
    Replaces val_helpers.pct_str(v, decimals=2)      → fmt_pct(v, dp=2)
    Replaces val_helpers.fp(v, dp=2)                 → fmt_pct(v, dp=2)
    Replaces rates_s_helpers.fmt_pct(v, decimals=1)  → fmt_pct(v, dp=1)
    """
    if v is None:
        return '—'
    return f'{v * 100:.{dp}f}%'


def fmt_pct1(v) -> str:
    """fmt_pct(v, dp=1) — shorthand used in RATES.S sweep tables."""
    return fmt_pct(v, dp=1)


def fmt_pct0(v) -> str:
    """fmt_pct(v, dp=0) — shorthand for whole-number percentages."""
    return fmt_pct(v, dp=0)


# ─────────────────────────────────────────────────────────────────────────────
# CURRENCY FORMATTING
# ─────────────────────────────────────────────────────────────────────────────

def fmt_gbp_m(v, dp: int = 3) -> str:
    """
    Format a value denominated in £ millions.

    Parameters
    ----------
    v  : float | None   value in £m; None returns "—"
    dp : int            decimal places (default 3)

    Returns
    -------
    str   e.g. "£12.345m" or "—"

    Migration notes
    ---------------
    Replaces val_helpers.fm(v, dp=3)   → fmt_gbp_m(v, dp=3)
    Replaces inline f'£{v:.3f}m' patterns throughout output scripts.
    """
    if v is None:
        return '—'
    return f'£{v:.{dp}f}m'


def fmt_gbp_b(v, dp: int = 1) -> str:
    """
    Format a value denominated in £ billions.

    Parameters
    ----------
    v  : float | None   value in £b; None returns "—"
    dp : int            decimal places (default 1)

    Returns
    -------
    str   e.g. "£12.3b" or "—"
    """
    if v is None:
        return '—'
    return f'£{v:.{dp}f}b'


def fmt_gbp_yr(v, threshold: float = 0.5) -> str:
    """
    Format an annual £/taxpayer value; suppress near-zero cells.

    Near-zero cells represent taxpayers below the W_min threshold who have
    zero liability; displaying "£0" would be misleading, so we suppress.

    Parameters
    ----------
    v         : float   value in £/yr
    threshold : float   values with |v| < threshold render as "£—" (default 0.5)

    Returns
    -------
    str   e.g. "£12,345" or "£—"

    Migration notes
    ---------------
    Replaces 8_3._fmt_gbp(v, threshold=0.5)
    """
    if abs(v) < threshold:
        return '£—'
    return f'£{v:,.0f}'


def fmt_rev_m(v, threshold: float = 5e-4) -> str:
    """
    Format a revenue value in £m/yr; suppress near-zero cells.

    Parameters
    ----------
    v         : float   value in £m/yr
    threshold : float   values with |v| < threshold render as "£—" (default 5e-4)

    Returns
    -------
    str   e.g. "£1,234m" or "£—"

    Migration notes
    ---------------
    Replaces 8_3._fmt_m(v, threshold=0.0005)
    """
    if abs(v) < threshold:
        return '£—'
    return f'£{v:,.0f}m'


# ─────────────────────────────────────────────────────────────────────────────
# FLOAT FORMATTING
# ─────────────────────────────────────────────────────────────────────────────

def fmt_f(v, spec: str = '.1f') -> str:
    """
    Format a float with an arbitrary format spec; None → "—".

    Parameters
    ----------
    v    : float | None
    spec : str          Python format spec string (default '.1f')

    Returns
    -------
    str   e.g. "12.3" or "—"

    Migration notes
    ---------------
    Replaces rates_s_helpers.fmt_f(v, fmt='.1f')
    Call sites using fmt_f(v, ".0f") should use fmt_f0(v).
    """
    if v is None:
        return '—'
    return f'{v:{spec}}'


def fmt_f0(v) -> str:
    """fmt_f(v, '.0f') — integer display, no decimal point."""
    return fmt_f(v, '.0f')


def fmt_f2(v) -> str:
    """fmt_f(v, '.2f') — two decimal places."""
    return fmt_f(v, '.2f')


def fmt_f4(v) -> str:
    """fmt_f(v, '.4f') — four decimal places (f_N ratios, etc.)."""
    return fmt_f(v, '.4f')


# ─────────────────────────────────────────────────────────────────────────────
# EFFECTIVE RATE CONVENIENCE
# ─────────────────────────────────────────────────────────────────────────────

def eff_rate(sim_result: dict) -> float:
    """
    Compute effective lifetime tax rate from a run_sim() result dict.

    Returns Net_settled / TW_settled, or 0.0 if TW_settled is degenerate.

    Migration notes
    ---------------
    Replaces val_helpers.eff_rate(r)
    Also replaces the inline pattern used in 5_3:
        r['Net_settled'] / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0
    """
    tw = sim_result.get('TW_settled', 0.0)
    if abs(tw) < 1e-12:
        return 0.0
    return sim_result['Net_settled'] / tw


# ─────────────────────────────────────────────────────────────────────────────
# DISTRIBUTION ROW FORMATTING
# ─────────────────────────────────────────────────────────────────────────────

def dist_row(d: dict, fmt_fn) -> str:
    """
    Format a distribution dict as a "min / median / mean / max" string.

    Parameters
    ----------
    d      : dict   must contain keys 'min', 'median', 'mean', 'max'
    fmt_fn : callable   applied to each value; should handle None → "—"

    Returns
    -------
    str   e.g. "3.1% / 5.2% / 5.4% / 8.7%"

    Migration notes
    ---------------
    Replaces rates_s_helpers.dist_row(d, fmt_fn) — identical signature.
    """
    return (
        f"{fmt_fn(d['min'])} / {fmt_fn(d['median'])} / "
        f"{fmt_fn(d['mean'])} / {fmt_fn(d['max'])}"
    )


def baseline_marker(v: float, baseline_v: float, tol: float = 1e-9) -> str:
    """
    Return " ◄" if v is within tol of baseline_v, else "".

    Used in sweep tables to mark the baseline parameter value.

    Migration notes
    ---------------
    Replaces rates_s_helpers.baseline_marker(v, baseline_v, tol=1e-9) — identical.
    """
    return ' ◄' if abs(v - baseline_v) < tol else ''


# ─────────────────────────────────────────────────────────────────────────────
# DATE
# ─────────────────────────────────────────────────────────────────────────────

def today_iso() -> str:
    """Return today's date as an ISO string, e.g. '2026-08-13'."""
    return datetime.date.today().isoformat()


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT PATH HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def out_dir(subdir: str) -> Path:
    """
    Return the canonical output directory for a given subdirectory name.

    The root is always the directory containing this file (the project root).
    The returned path is not created automatically — call ensure_dir() first.

    Parameters
    ----------
    subdir : str   e.g. 'VAL', 'VAL_S', 'RATES', 'RATES_S'

    Returns
    -------
    Path   e.g. /mnt/project/OUTPUTS/VAL

    Migration notes
    ---------------
    Replaces val_helpers.OUT_DIR         → out_dir('VAL')
    Replaces val_s_helpers.OUT_DIR       → out_dir('VAL_S')
    Replaces rates_s_helpers.OUT_DIR_*   → out_dir('RATES_S')
    Replaces 8_3.OUTPUT_DIR             → out_dir('RATES')
    """
    return _ROOT / 'OUTPUTS' / subdir


def ensure_dir(path: Path) -> Path:
    """
    Create path (and all parents) if it does not exist.

    Returns path unchanged so it can be used inline:
        p = ensure_dir(out_dir('VAL')) / 'output.md'

    Migration notes
    ---------------
    Replaces os.makedirs(OUT_DIR, exist_ok=True) calls in each main().
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
