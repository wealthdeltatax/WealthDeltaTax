"""
base.py -- the wealth and payer base (model v3, stage V3-6)
===========================================================
Layer L2 (architecture.md 5.1). Imports numpy and core/pack.py only. Rewritten from the specification (rates_core.py 408 to 599),
not ported. No file is read and nothing runs at import (R8). No country appears here (R11): the pack and the register arrive as arguments.

LINES AND UNITS (R6)
--------------------
A line is a representative adult. There are fourteen: wealth deciles D1 to D9, then D10 split by `tail` (D10a, the 90th to 99th percentile;
D10b, the top 1% below the named list; RL3, RL2, RL1, the named list in three tiers, RL1 the richest). D10 holds 90% / 10% of D10's households
(D10a / the top 1%); the top 1% of adults is its D10b adults plus the named list members.

THE TAIL (brief 073c; v2's construction, rates_core.py `_build_advani`, rewritten, no v2 constant kept)
------------------------------------------------------------------------------------------------------
The survey total grows by the register's missing-wealth share (I-D4e), all of it at the top. The top 1% of the survey holds I-D4d of the survey
total; D10a is D10 less that (the survey's 90th to 99th percentile). The top 1% after the addition is that plus the missing wealth. The Rich
List (I-D4f, I-D4j members) is part of the top 1% (the list overlaps the survey, so it is not added): D10b is the top 1% less the list. The list
is split into tiers at the member-rank cuts (I-D4k, I-D4l and the whole list) by a Pareto tail: ranks lo to hi of n hold list x ((hi/n)^b - (lo/n)^b),
b = 1 - 1/alpha (I-D4i); a rank cut is round(fraction x n), Python's rounding. `wealth_bn` sums to the survey total times one plus the missing-wealth
share; `wealth_to_gdp` is that total over GDP (as v2's calibrate). The top 1% share I-D4d is a share of the survey total, as in v2.

Pounds are in millions per adult (the kernel's unit); `adults_k` is thousands of
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
       'income': {'D4-5': 'I-D9a', 'D6-7': 'I-D9b', 'D8-9': 'I-D9c', 'D10': 'I-D9d'},   # register rows: income is pounds per household a year
       'tail': dict(s1='I-D4d', extra='I-D4e', list_bn='I-D4f', alpha='I-D4i', n='I-D4j', cut1='I-D4k', cut2='I-D4l')}   # percent, percent, GBP bn, coefficient, count, percent of members
TIERS = ('RL3', 'RL2', 'RL1')
BANDS = {'D4': 'D4-5', 'D5': 'D4-5', 'D6': 'D6-7', 'D7': 'D6-7', 'D8': 'D8-9', 'D9': 'D8-9', **{k: 'D10' for k in ('D10a', 'D10b') + TIERS}}
LABELS = tuple(f'D{i}' for i in range(1, 10)) + ('D10a', 'D10b') + TIERS
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
    wealth_bn: np.ndarray      # billions of pounds held by the line, sums to the pack's total plus the missing wealth (I-D4e)
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


def tail(total_bn, d10_bn, s1, extra, n, list_bn, alpha, cuts):
    """The top of the distribution. Every constant is an argument (the model passes the register's; test I1 passes v2's own).
    total_bn the survey total, d10_bn the survey's top 10%, s1 the survey's top 1% share of the total, extra the missing-wealth share of the
    total, n the named list members, list_bn their total, alpha the Pareto coefficient, cuts the rising member-rank fractions ending in 1.
    Returns d10a_bn, d10b_bn, tier_bn and tier_n (ascending wealth: the poorest tier first), and total_bn after the addition."""
    if not (alpha > 1 and 0 < s1 < 1 and extra >= 0 and n >= 1 and list_bn > 0):
        raise BaseError('tail: need alpha > 1, 0 < top 1% share < 1, missing wealth >= 0, members >= 1 and a positive list total')
    ranks = [0] + [int(round(f * n)) for f in cuts]
    if ranks[-1] != n or any(b <= a for a, b in zip(ranks, ranks[1:])) or len(cuts) != len(TIERS):
        raise BaseError(f'tail: the cuts {list(cuts)} give ranks {ranks}, which must rise to {n} in {len(TIERS)} tiers')
    top1, b = s1 * total_bn + extra * total_bn, 1 - 1 / alpha
    d10a, d10b = d10_bn - s1 * total_bn, top1 - list_bn
    if d10a <= 0 or d10b <= 0:
        raise BaseError(f'tail: the top 10% {d10_bn:.1f}bn does not cover the top 1% share, or the named list {list_bn}bn exceeds the top 1% {top1:.1f}bn')
    pairs = list(zip(ranks, ranks[1:]))[::-1]
    return {'d10a_bn': d10a, 'd10b_bn': d10b, 'tier_bn': np.array([list_bn * ((hi / n) ** b - (lo / n) ** b) for lo, hi in pairs]),
            'tier_n': np.array([hi - lo for lo, hi in pairs], float), 'total_bn': total_bn * (1 + extra)}


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
    g = {k: _reg(register, i) for k, i in IDS['tail'].items()}
    t = tail(total_bn, dec[9] * total_bn / sum(dec), g['s1'] / 100, g['extra'] / 100, int(g['n']), g['list_bn'], g['alpha'], [g['cut1'] / 100, g['cut2'] / 100, 1.0])
    wealth_bn = np.array([d * total_bn / sum(dec) for d in dec[:9]] + [t['d10a_bn'], t['d10b_bn'], *t['tier_bn']])   # the survey deciles sum to the total; the tail adds the missing wealth
    hh = np.array([wd('households', f'D{i}') for i in range(1, 10)] + [wd('households', 'D10') * (1 - TOP_SHARE), wd('households', 'D10') * TOP_SHARE])
    hh = hh * hh_all / hh.sum()
    per_hh = _reg(register, IDS['adults'])
    if not 1 <= per_hh <= 2:
        raise BaseError(f'adults per household {per_hh} is outside 1 to 2')
    members = t['tier_n'] / 1e3 / per_hh                                                                # thousands of households: each member is one adult
    if hh[10] <= members.sum():
        raise BaseError(f'the {int(t["tier_n"].sum())} named list members exceed the top 1%')
    hh = np.r_[hh[:10], hh[10] - members.sum(), members]
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
                wm, t['total_bn'] / _cell(pack, 'wealth_distribution', variable='gdp', band='all'),
                {'gross_income': hi('gross_income'), 'total_tax': hi('total_tax')})
