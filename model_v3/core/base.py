"""
base.py -- the wealth and payer base (model v3, stage V3-6)
===========================================================
Layer L2 (architecture.md 5.1). Imports numpy and core/pack.py only. Rewritten from the specification (rates_core.py 408 to 599),
not ported. No file is read and nothing runs at import (R8). No country appears here (R11): the pack and the register arrive as arguments.

LINES AND UNITS (R6)
--------------------
A line is a representative adult. There are eleven: wealth deciles D1 to D9, then D10 split in two by the tail table (D10a, the 90th
to 99th percentile, 90% of D10's households; D10b, the top 1%, 10%). The top 1%'s share of D10's wealth is the pack's top 1% share over
its top 10% share in the latest year both are given: a ratio of two adult-basis WID shares applied to the household-basis D10, which is
the base's one cross-basis step and is stated, not hidden. Pounds are in millions per adult (the kernel's unit); `adults_k` is thousands of
adults, so V0 x adults_k is billions of pounds. Wealth by decile and households come from the pack; adults per household is one register number
for every line. W_min is the lever ratio times the pack's median house price per adult.

WHAT IS NOT HERE
----------------
Behaviour (a level 2 draw, V3-10), the cohort return tiers, the Route B payment mode (a kernel argument), and any non-payer income
decile share (M4a, V3-8). Income and liquid assets exist only where a source gives them: wealth bands D4 and above. A line at or above
W_min with no income or liquid assets raises; below W_min they stay nan, never filled.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

G = 30                                                                        # generation length in years (C1, metrics.md)
ROUTES = ('A', 'B', 'C', 'D')
IDS = {'adults': 'I-D4h', 'route': dict(zip(ROUTES, ('I-D13a', 'I-D13b', 'I-D13c', 'I-D13d'))),
       'income': {'D4-5': 'I-D9a', 'D6-7': 'I-D9b', 'D8-9': 'I-D9c', 'D10': 'I-D9d'}}   # register rows: income is pounds per household a year
BANDS = {'D4': 'D4-5', 'D5': 'D4-5', 'D6': 'D6-7', 'D7': 'D6-7', 'D8': 'D8-9', 'D9': 'D8-9', 'D10a': 'D10', 'D10b': 'D10'}
LABELS = tuple(f'D{i}' for i in range(1, 10)) + ('D10a', 'D10b')
TOP_SHARE = 0.10                                                              # the top 1% is a tenth of D10's households


class BaseError(ValueError):
    """The base cannot be built, or a band does not partition."""


@dataclass(frozen=True)
class Base:
    labels: tuple              # line labels, bottom to top
    band: tuple                # the pack band each line takes its income and liquid assets from ('' if none)
    households_k: np.ndarray   # thousands of households in the line
    adults_k: np.ndarray       # thousands of adults in the line
    weights: np.ndarray        # share of all adults, sums to 1
    wealth_bn: np.ndarray      # billions of pounds held by the line, sums to the pack's total
    V0: dict                   # route -> millions of pounds per adult, n lines; the routes sum to `wealth`
    wealth: np.ndarray         # millions of pounds per adult
    income: np.ndarray         # millions of pounds per adult per year, nan where no source
    liquid: np.ndarray         # millions of pounds per adult, nan where no source
    w_min: float               # millions of pounds per adult
    wealth_to_gdp: float
    income_deciles: dict       # 'gross_income', 'total_tax': arrays of pounds per household a year, income decile 1 to 10 (M4a, M4b)
    G: int = G


def _cell(pack, dataset, **where):
    rows = [r for r in pack.tables[dataset] if all(r[k] == v for k, v in where.items())]
    if len(rows) != 1:
        raise BaseError(f'{dataset} {where}: {len(rows)} rows, one expected')
    return rows[0]['value']


def _reg(reg, i):
    if i not in reg or reg[i].central is None:
        raise BaseError(f'register row {i} is missing or has no central value')
    return reg[i].central


def w_min(pack, ratio):
    """The threshold, millions of pounds per adult: the lever ratio times the pack's median house price per adult."""
    if not ratio > 0:
        raise BaseError(f'the threshold ratio must be positive, got {ratio!r}')
    return ratio * _cell(pack, 'wealth_distribution', variable='median_house_price', band='all') / 1e6


def _tail_ratio(pack):
    """Share of the top 10%'s wealth held by the top 1%, from the latest year of the tail table that gives both."""
    t = {(r['series'], r['year']): r['value'] for r in pack.tables['wealth_tail']}
    ys = sorted({y for s, y in t if s == 'wid_top1'} & {y for s, y in t if s == 'wid_top10'})
    if not ys or not 0 < t['wid_top1', ys[-1]] < t['wid_top10', ys[-1]]:
        raise BaseError('wealth_tail: no year gives a top 1% share below the top 10% share')
    return t['wid_top1', ys[-1]] / t['wid_top10', ys[-1]]


def _share(pack, variable, band):
    rows = [r for r in pack.tables['wealth_distribution'] if r['variable'] == variable and r['band'] == band]
    return rows[0]['value'] / 100 if rows else float('nan')


def build_base(pack, register, ratio):
    """The payer base for one threshold ratio; two calls with the same arguments give equal arrays (B5)."""
    wd = lambda v, b: _cell(pack, 'wealth_distribution', variable=v, band=b)
    dec = [wd('wealth_total', f'D{i}') for i in range(1, 11)]
    total_bn, hh_all = wd('wealth_total', 'all'), wd('households', 'all')
    if abs(sum(dec) - total_bn) > max(0.5, 1e-4 * total_bn) or abs(sum(wd('households', f'D{i}') for i in range(1, 11)) - hh_all) > 0.5:
        raise BaseError('wealth_distribution: deciles D1 to D10 do not partition the printed total')
    top = _tail_ratio(pack)
    wealth_bn = np.array(dec[:9] + [dec[9] * (1 - top), dec[9] * top]) * total_bn / sum(dec)            # scaled so the lines sum to the total
    hh = np.array([wd('households', f'D{i}') for i in range(1, 10)] + [wd('households', 'D10') * (1 - TOP_SHARE), wd('households', 'D10') * TOP_SHARE])
    hh = hh * hh_all / hh.sum()
    per_hh = _reg(register, IDS['adults'])
    if not 1 <= per_hh <= 2:
        raise BaseError(f'adults per household {per_hh} is outside 1 to 2')
    adults = hh * per_hh
    wealth = wealth_bn / adults                                                                         # bn of pounds over thousand adults = millions of pounds per adult
    mix = {r: _reg(register, i) for r, i in IDS['route'].items()}
    if min(mix.values()) < 0 or abs(sum(mix.values()) - 100) > 1e-9:
        raise BaseError(f'the route mix {mix} does not sum to 100')
    band = tuple(BANDS.get(label, '') for label in LABELS)
    income = np.array([_reg(register, IDS['income'][b]) / per_hh / 1e6 if b else np.nan for b in band])
    liquid = np.array([_share(pack, 'net_financial_share', b) * w if b else np.nan for b, w in zip(band, wealth)])
    wm = w_min(pack, ratio)
    if (np.isnan(income) | np.isnan(liquid))[wealth >= wm].any():
        raise BaseError('a line at or above W_min has no income or liquid assets: no source gives them')
    hi = lambda v: np.array([_cell(pack, 'household_incidence', variable=v, group=f'D{i}', tax=None) for i in range(1, 11)], float)
    return Base(LABELS, band, hh, adults, adults / adults.sum(), wealth_bn, {r: wealth * s / 100 for r, s in mix.items()}, wealth, income, liquid,
                wm, total_bn / _cell(pack, 'wealth_distribution', variable='gdp', band='all'),
                {'gross_income': hi('gross_income'), 'total_tax': hi('total_tax')})
