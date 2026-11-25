"""
out_revenue.py -- output group: revenue lines and the fund (model v3, brief 085c)
================================================================================
Interface: see groups.py. Fills O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1 from revenue.py's result `raw.r` (revenue.revenue); no value is computed here that the core
does not give, except B1b and B1c as a percent: over each window, the entries or exits over the payers of the year before (a ratio of sums; the core keeps the counts, and metrics.md B1b
gives the percent form the manifest asks for).
Metric to core: O1d M1e (r['M1e'] by retired tax, window mean over each horizon as M1), OP1 P1, OP3 P3, OP4 P4_ratio (the first year below zero is text, not a cell),
OP5 P5 (column of the tax, 0 = never retired), OP6 P6 by year, OR1 P7a and P7b (one value over all years after the fill; P7a is 0 or 1 per path, P7b is nan where no year
follows a fill), OB1 B1a to B1d read from `again({'ratio': r}, full=True)`, the only run that keeps the payer record, each at its own fill year's windows.
The retired taxes' names are the keys of `env.ctx.rec` (pack and lever file), never written here (R11).
"""

import numpy as np

from model_v3.core import revenue as rv

NAME = 'revenue'
IDS = ('O1d', 'OP1', 'OP3', 'OP4', 'OP5', 'OP6', 'OR1', 'OB1')
RATIOS = {'r025': 0.25, 'r050': 0.5, 'r100': 1.0}       # OB1's `by.w_min` labels and the threshold ratios of the base they name


def _win(x, raw, w, k):
    """Ratio of sums of the (T, P) share x over the horizon k's window, weighted by w; the short window is nan where the reserve never fills, as headlines."""
    v = rv.window_mean(x, w, raw.lo[k], raw.hi[k])
    return np.where(raw.ok, v, np.nan) if k == 'short' else v


def _prev(x):
    """The year before, year 1 repeating its own start (the launch payers)."""
    return np.vstack([x[:1], x[:-1]])


def per_path(raw, env, again):
    """Per-path arrays: leaves are (P,) arrays, the structure is in the keys (see the module note)."""
    r, taxes = raw.r, list(env.ctx.rec)
    out = {'M1e': {t: {k: _win(r['M1e'][t], raw, r['gdp'], k) for k in raw.lo} for t in taxes},
           'P1': r['P1'], 'P3': r['P3'], 'P4': r['P4_ratio'], 'P5': {t: r['P5'][:, i] for i, t in enumerate(taxes)}, 'P6': dict(r['P6']),
           'P7a': r['P7a'].astype(float), 'P7b': np.where(np.isfinite(r['P7b']), r['P7b'], np.nan), 'B1': {}}
    for lab, ratio in RATIOS.items():
        a = again({'ratio': ratio}, full=True)
        run, gdp, flat = a.run, a.r['gdp'], np.ones_like(a.r['gdp'])
        rate = lambda x, k: 100 * _win(x, a, flat, k) / np.where(_win(_prev(run['payers']), a, flat, k) > 0, _win(_prev(run['payers']), a, flat, k), np.nan)
        out['B1'][lab] = {'B1a': {k: _win(a.r['B1a'], a, flat, k) for k in a.lo}, 'B1d': {k: _win(a.r['B1d'], a, gdp, k) for k in a.lo},
                          'B1b': {k: rate(run['entries'], k) for k in a.lo}, 'B1c': {k: rate(run['exits'], k) for k in a.lo}}
    return out


def cells(e):
    """{output id: {(horizon, by, line): array}} from this group's per-path results of one schedule."""
    one = lambda x: {('single', (), None): x}
    return {'O1d': {(k, (('per', t),), None): v for t, hs in e['M1e'].items() for k, v in hs.items()},
            'OP1': one(e['P1']), 'OP3': one(e['P3']), 'OP4': one(e['P4']),
            'OP5': {('single', (('per', t),), None): v for t, v in e['P5'].items()},
            'OP6': {('single', (('year', y),), None): v for y, v in e['P6'].items()},
            'OR1': {('single', (), ln): e[ln] for ln in ('P7a', 'P7b')},
            'OB1': {(k, (('w_min', lab),), ln): v for lab, lns in e['B1'].items() for ln, hs in lns.items() for k, v in hs.items()}}
