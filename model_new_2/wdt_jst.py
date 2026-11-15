"""
wdt_jst.py — JST window loader and real-basis inputs
=====================================================
Refactor plan, Phase 1 items 1 and 2 (decisions D1, D1a, D1b).

Item 1: one place decides which windows a country's JST history yields, so VAL and RATES
read the same sample. Replaces the no-wrap rule in rates_core.valid_windows() once wired
in (not yet wired: rates_core and valgen_core are unchanged).

Item 2: the real return g_real and the real GDP-per-head index index_rate that VAL reads
from [val_gen] (D1: everything real, no nominal series). real_basis_inputs() derives both
from the raw JST record, the same data RATES uses. Not yet wired to the TOML.

RULES (D1b, item 1)
  * A window is T consecutive USABLE years of one country (usable = every required
    column non-null). The series wraps: the last usable year is followed by the first.
  * Every result is reported twice: full loop (wrap = True) and contiguous-only
    (wrap = False, no seam crossed). Use `contiguous` to select the second.
  * Windows that repeat years (T longer than the usable series, as for PRT and BEL at
    T = 100) are KEPT and flagged `repeat`. They are not excluded.
  * `wraps` marks a window that crosses the seam. A calendar gap inside the usable
    years also counts as a break for `contiguous`.

PUBLIC API
  usable_years(d, cols)            ordered list of usable calendar years of a panel
  loop_windows(years, T, wrap)     list of window dicts (see below)
  window_frame(d, win)             panel rows for one window, in window order
  window_summary(windows)          counts for the effective-window table (T = 100)
  real_basis_inputs(J, iso, years) {g_real, index_rate, n, first, last} from the raw JST JSON

WINDOW DICT
  start      first calendar year of the window (as listed in the usable series)
  pos        positions into the usable series, length T (repeats possible)
  years      calendar years at those positions, length T
  wraps      True if the window crosses the seam
  repeat     True if T > number of usable years (some years appear twice)
  contiguous True if not wraps and no calendar gap inside the window

REAL BASIS (item 2)
  g_real      geometric mean REAL capital return: (1 + capital_tr) / (1 + CPI inflation) - 1
  index_rate  geometric mean REAL GDP-per-head growth: (gdp/pop) growth deflated by CPI
  Both use years where the input and the prior year's CPI, GDP and population are present.
  Geometric means, so the constant g reproduces the compounded path over the sample.
  Pass `years` to restrict to a window (e.g. the years of one loop window).
"""

import json
import math
from pathlib import Path


def usable_years(d, cols):
    """Ordered list of calendar years in panel `d` where every column in `cols` is non-null."""
    ok = d[list(cols)].notna().all(axis=1)
    return [int(y) for y in d.index[ok.to_numpy()]]


def loop_windows(years, T, wrap=True):
    """
    Windows of length T over the usable series `years` (ascending calendar years).

    wrap = True : every start position is valid; windows that run past the end continue
                  from the first usable year (the seam). This is the headline (D1b).
    wrap = False: only windows that fit inside the series (contiguous-only check).

    Returns a list of window dicts (see module docstring). Empty if T < 1 or no years.
    """
    n = len(years)
    T = int(T)
    if n == 0 or T < 1:
        return []
    starts = range(n) if wrap else range(0, n - T + 1)
    repeat = T > n
    out = []
    for i in starts:
        pos = [(i + k) % n for k in range(T)]
        yrs = [years[p] for p in pos]
        seam = (i + T) > n
        gap = any(yrs[k + 1] - yrs[k] != 1 for k in range(T - 1))
        out.append({
            'start': years[i],
            'pos': pos,
            'years': yrs,
            'wraps': bool(seam),
            'repeat': bool(repeat),
            'contiguous': bool((not seam) and (not gap)),
        })
    return out


def window_frame(d, win):
    """Panel rows for one window (from `loop_windows`), in window order. Repeated years repeat."""
    rows = d.loc[win['years']].copy()        # index is calendar years and unique in the panel
    rows.index = range(len(rows))            # window time: 0 .. T-1
    return rows


def window_summary(windows):
    """
    Counts for the effective-window table. Keys:
      total       all windows in the loop
      contiguous  windows that cross no seam and have no calendar gap
      wraps       windows that cross the seam
      repeat      windows with repeated years (flagged, kept)
      repeat_share  share of windows with repeated years
    """
    n = len(windows)
    cont = sum(w['contiguous'] for w in windows)
    wr = sum(w['wraps'] for w in windows)
    rp = sum(w['repeat'] for w in windows)
    return {
        'total': n,
        'contiguous': int(cont),
        'wraps': int(wr),
        'repeat': int(rp),
        'repeat_share': (rp / n) if n else float('nan'),
    }


# ─────────────────────────────────────────────────────────────
# REAL BASIS (item 2)
# ─────────────────────────────────────────────────────────────

def _jst_series(J, iso, var):
    """{year: value} for one JST country and variable, None values dropped."""
    c = J['countries'][iso]
    return {int(y): float(v) for y, v in zip(c['years'], c['series'][var]) if v is not None}


def real_basis_inputs(J, iso, years=None):
    """
    Real-basis inputs for one country from the raw JST JSON J (as loaded by rates_core.load_jst).

    years : optional iterable of calendar years to restrict to (e.g. one window's years).
            A year is used only if its own and the prior year's CPI, GDP and population
            are present, and its capital return is present.

    Returns a dict:
      g_real       geometric mean real capital return over the used years
      index_rate   geometric mean real GDP-per-head growth over the used years
      n            number of years used
      first, last  first and last year used
    Raises ValueError if no year qualifies.
    """
    ret = _jst_series(J, iso, 'capital_tr')
    cpi = _jst_series(J, iso, 'cpi')
    gdp = _jst_series(J, iso, 'gdp')
    pop = _jst_series(J, iso, 'pop')
    keep = set(years) if years is not None else None

    real_r, real_g, used = [], [], []
    for y in sorted(ret):
        if keep is not None and y not in keep:
            continue
        if not all((y in s and (y - 1) in s) for s in (cpi, gdp, pop)):
            continue
        infl = cpi[y] / cpi[y - 1] - 1.0
        gpc = (gdp[y] / pop[y]) / (gdp[y - 1] / pop[y - 1]) - 1.0
        real_r.append((1.0 + ret[y]) / (1.0 + infl) - 1.0)
        real_g.append((1.0 + gpc) / (1.0 + infl) - 1.0)
        used.append(y)

    if not used:
        raise ValueError(f'real_basis_inputs: no usable years for {iso}')
    gm = lambda xs: math.exp(sum(math.log(1.0 + x) for x in xs) / len(xs)) - 1.0
    return {
        'g_real': gm(real_r),
        'index_rate': gm(real_g),
        'n': len(used),
        'first': used[0],
        'last': used[-1],
    }


_HERE = Path(__file__).resolve().parent
# [rates].jst_path is "looked up in the RATES folder, then in Model/" (TOML comment)
_JST_DIRS = [_HERE / 'RATES', _HERE, _HERE.parent]
_JST_CACHE = {}


def load_jst(name, dirs=None):
    """
    Parse the JST JSON `name`, looked up in each directory of `dirs` in order (default: Model/RATES, Model/, its parent).
    The parsed dict is cached per resolved file and shared: callers must treat it as read-only.
    Raises FileNotFoundError listing what was tried. The one JST loader for VAL and RATES.
    """
    tried = []
    for d in (_JST_DIRS if dirs is None else dirs):
        path = Path(d) / name
        tried.append(str(path))
        if path.exists():
            key = str(path.resolve())
            if key not in _JST_CACHE:
                with open(path, 'r', encoding='utf-8') as fh:
                    _JST_CACHE[key] = json.load(fh)
            return _JST_CACHE[key]
    raise FileNotFoundError(f'JST file not found; tried {tried}')


def real_return_series(J, iso):
    """
    {year: REAL capital return} for one JST country: (1 + capital_tr) / (1 + CPI inflation) - 1, for every year in which the return
    and this year's and the prior year's CPI are present. The series VAL replays (D1a); window rules are loop_windows on its sorted years.
    """
    ret = _jst_series(J, iso, 'capital_tr')
    cpi = _jst_series(J, iso, 'cpi')
    return {y: (1.0 + r) / (cpi[y] / cpi[y - 1]) - 1.0 for y, r in sorted(ret.items()) if y in cpi and (y - 1) in cpi}


if __name__ == '__main__':
    # Self-tests on synthetic data. Run: python wdt_jst.py
    ys = list(range(1900, 1910))             # 10 usable years
    w_loop = loop_windows(ys, T=4, wrap=True)
    w_cont = loop_windows(ys, T=4, wrap=False)
    assert len(w_loop) == 10 and len(w_cont) == 7
    assert sum(w['wraps'] for w in w_loop) == 3            # starts 1907, 1908, 1909 cross the seam
    assert all(not w['repeat'] for w in w_loop)
    last = w_loop[-1]                                       # start 1909: 1909, 1900, 1901, 1902
    assert last['years'] == [1909, 1900, 1901, 1902] and last['wraps'] and not last['contiguous']
    assert all(w['contiguous'] for w in w_cont)
    rep = loop_windows(ys[:3], T=5, wrap=True)              # T > n: repeats
    assert all(w['repeat'] for w in rep)

    # real basis, synthetic: capital return 10% a year, CPI +2%, GDP +5%, population flat.
    # real return = 1.10 / 1.02 - 1; GDP/head nominal = 1.05, real = 1.05 / 1.02 - 1.
    yrs = list(range(2000, 2006))
    J = {'countries': {'XXX': {
        'years': yrs,
        'series': {
            'capital_tr': [0.10] * 6,
            'cpi': [1.02 ** k for k in range(6)],
            'gdp': [1.05 ** k for k in range(6)],
            'pop': [1.0] * 6,
        }}}}
    out = real_basis_inputs(J, 'XXX')
    assert abs(out['g_real'] - (1.10 / 1.02 - 1.0)) < 1e-12, out
    assert abs(out['index_rate'] - (1.05 / 1.02 - 1.0)) < 1e-12, out
    assert out['n'] == 5 and out['first'] == 2001 and out['last'] == 2005   # 2000 has no prior year
    sub = real_basis_inputs(J, 'XXX', years=[2002, 2003])
    assert sub['n'] == 2 and sub['first'] == 2002
    rs = real_return_series(J, 'XXX')
    assert sorted(rs) == [2001, 2002, 2003, 2004, 2005] and abs(rs[2003] - (1.10 / 1.02 - 1.0)) < 1e-12, rs
    print('wdt_jst self-tests ok:', window_summary(w_loop))
