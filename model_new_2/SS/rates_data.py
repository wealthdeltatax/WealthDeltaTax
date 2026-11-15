"""
rates_data.py — RATES rebuild, data layer
==========================================
Loads the JST Macrohistory JSON (jst_r6.json) and produces per-country
annual panels in REAL terms for the sweep.  No modelling here; this module
only answers "what history do we have, in what units, and where is it usable".

PROVENANCE NOTE
---------------
The 73-value series in the legacy WDT_Params.toml (labelled "UK equity total
return") is JST `capital_tr` for GBR 1947-2019, NOMINAL, matching to 4 d.p. in
73/73 years.  It is the JST total-wealth return (housing, equity, bonds, bills),
not an equity series, and it is nominal.  The rebuild uses the same concept
in REAL terms.

PRINCIPLES
----------
* Raw JSON is never modified.  All transforms happen here, in code.
* Returns are converted to real terms with the country's own CPI.
* Nothing is silently dropped.  Suspect years are FLAGGED (see flag_years)
  and the sweep decides, by explicit policy, whether to exclude them.
* Windows that lack enough contiguous data are reported as censored,
  never quietly discarded.

PUBLIC API
----------
  load_jst(path)                      -> dict   (parsed JSON)
  countries(J)                        -> list[str] ISO codes
  panel(J, iso)                       -> DataFrame indexed by year
  flag_years(df, thresholds)          -> DataFrame[bool] of suspect-year flags
  contiguous_runs(mask)               -> list[(start, end)] inclusive
  valid_windows(df, cols, length)     -> list[start_year]  windows fully valid
  coverage_table(J, cols, length)     -> DataFrame summary per country
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_JSON = Path(__file__).parent / 'jst_r6.json'

# Columns the sweep needs.  capital_tr is the primary wealth-return concept.
RETURN_COLS = ['capital_tr', 'eq_tr', 'housing_tr', 'risky_tr', 'safe_tr',
               'bond_tr', 'eq_capgain']
FISCAL_COLS = ['gdp', 'expenditure', 'revenue', 'cpi', 'pop']


def load_jst(path=None):
    with open(Path(path) if path else DEFAULT_JSON, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def countries(J):
    return sorted(J['countries'])


def _series(J, iso, var):
    c = J['countries'][iso]
    return pd.Series([np.nan if v is None else v for v in c['series'][var]],
                     index=pd.Index(c['years'], name='year'), dtype=float)


def panel(J, iso):
    """
    Per-country annual panel.

    Columns
    -------
    infl                 CPI inflation, year on year (fraction)
    <ret>                nominal return (fraction), for each of RETURN_COLS
    <ret>_real           real return = (1+r)/(1+infl) - 1
    gdp, expenditure, revenue   nominal, local currency (as in JST)
    exp_gdp              expenditure / gdp  (dimensionless)
    gdp_pc, gpc, gpc_real  GDP per capita level, nominal growth, real growth
    rev_gdp              revenue / gdp
    pop                  population (thousands)

    Note on units: expenditure and gdp share currency and scale within a
    country, so exp_gdp is unit-safe.  Levels are NOT comparable across
    countries and the sweep must work in ratios to GDP.
    """
    d = pd.DataFrame({v: _series(J, iso, v)
                      for v in RETURN_COLS + FISCAL_COLS})
    d['infl'] = d['cpi'].pct_change()
    for r in RETURN_COLS:
        d[f'{r}_real'] = (1.0 + d[r]) / (1.0 + d['infl']) - 1.0
    d['exp_gdp'] = d['expenditure'] / d['gdp']
    d['rev_gdp'] = d['revenue'] / d['gdp']
    # GDP per capita (nominal, local units; pop is in thousands so levels are
    # only meaningful as ratios / growth rates)
    d['gdp_pc']   = d['gdp'] / d['pop']
    d['gpc']      = d['gdp_pc'].pct_change()
    d['gpc_real'] = (1.0 + d['gpc']) / (1.0 + d['infl']) - 1.0
    return d


# ─────────────────────────────────────────────────────────────
# SUSPECT-YEAR FLAGS
# ─────────────────────────────────────────────────────────────

DEFAULT_FLAG_THRESHOLDS = {
    # real capital_tr outside this band is flagged for manual review.
    'real_return_lo': -0.40,
    'real_return_hi':  0.60,
    # inflation above this is flagged (hyperinflation / reform territory).
    'infl_hi': 0.50,
}


def flag_years(d, thresholds=None):
    """
    Return a boolean DataFrame of suspect-year flags.  Flags are
    diagnostics, not exclusions.  The sweep's sample policy decides what to
    do with them.
    """
    t = {**DEFAULT_FLAG_THRESHOLDS, **(thresholds or {})}
    r = d['capital_tr_real']
    f = pd.DataFrame(index=d.index)
    f['extreme_real_return'] = (r < t['real_return_lo']) | (r > t['real_return_hi'])
    f['high_inflation']      = d['infl'] > t['infl_hi']
    f['any'] = f.any(axis=1)
    return f


# ─────────────────────────────────────────────────────────────
# CONTIGUOUS-WINDOW LOGIC
# ─────────────────────────────────────────────────────────────

def contiguous_runs(mask):
    """Inclusive (start_year, end_year) runs where boolean Series `mask` is True
    and years are consecutive."""
    runs, start, prev = [], None, None
    for yr, ok in mask.items():
        if ok and start is None:
            start = yr
        if ok:
            prev = yr
        if (not ok) and start is not None:
            runs.append((start, prev)); start = None
    if start is not None:
        runs.append((start, prev))
    return runs


def valid_windows(d, cols, length, exclude=None):
    """
    Start years s such that every column in `cols` is non-null for every
    year in [s, s+length-1], and (optionally) no year in that span is True in
    the boolean Series `exclude`.
    """
    ok = d[cols].notna().all(axis=1)
    if exclude is not None:
        ok = ok & ~exclude.reindex(d.index).fillna(False)
    starts = []
    ys = list(d.index)
    okv = ok.to_dict()
    ys_set = set(ys)
    for s in ys:
        span = range(s, s + length)
        if all((y in ys_set) and okv.get(y, False) for y in span):
            starts.append(s)
    return starts


MODEL_COLS = ['capital_tr_real', 'safe_tr_real', 'risky_tr_real',
              'exp_gdp', 'infl', 'gpc', 'gpc_real']


def coverage_table(J, length=40, cols=None, exclude_flags=False):
    """Per-country availability of usable windows of a given length."""
    cols = cols or MODEL_COLS
    rows = []
    for iso in countries(J):
        d = panel(J, iso)
        ex = flag_years(d)['any'] if exclude_flags else None
        w = valid_windows(d, cols, length, exclude=ex)
        ok = d[cols].notna().all(axis=1)
        runs = contiguous_runs(ok)
        longest = max(runs, key=lambda r: r[1] - r[0]) if runs else None
        rows.append({
            'iso': iso,
            'model_cols_first': int(d.index[ok][0]) if ok.any() else None,
            'longest_run': (f'{longest[0]}-{longest[1]} ({longest[1]-longest[0]+1}y)'
                            if longest else None),
            'n_windows': len(w),
            'first_start': w[0] if w else None,
            'last_start': w[-1] if w else None,
        })
    return pd.DataFrame(rows)
