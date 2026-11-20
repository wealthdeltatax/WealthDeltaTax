"""
out_burden.py -- output group: burden, non-payer savings and the comparators (model v3, brief 086c)
===================================================================================================
Interface: see groups.py. Layer L4 (conftest LAYER): imports numpy and core/burden.py only. No file is read and nothing runs at import (R8); no country or tax is named (R11).

BUILT (the metric each id reads, all from `Raw`, no new maths)
O2d   burden.m2d(raw.fl, lo, hi): M2 with the death flows. They are in `raw.fl` (the burden run keeps `death`, `full` or not), so `again` is not used.
O2b, O2c   burden.m2b / m2c (all net WDT, burden.py's default): the cell is the share of payers above each cut-off; the payer mean is not in the manifest.
O4b   burden.m4(...)['M4b'], by income decile, at the horizon's last year; O4a's inputs (`raw.r['P5']`, `raw.inc`, `raw.base.income_deciles`).
OL1   burden.m4c on that M4b and the income deciles.

OH1b2 (M11)  burden.m11(env.ctx.reg), register row I-T1d; the manifest does not mark it once, so it is a per-schedule cell, the same value on every path.
DH1c  burden.dh1c(env.pack, retired taxes, ctx.mp['parts'], ctx.mp['payer_taxes'])['bill_pct_income'] by income decile and overall: the manifest has unit pct only,
      so the share of income, not pounds. It does not depend on paths: each cell is the same value on every path (the manifest does not mark it once).

O5    burden.m5(base wealth, adults, reg, m2_wdt): `burden` the comparator's burden (the same on every path, register rows only), `diff` against this schedule's M2 in
      life, `overall` band, per horizon. No with-death line (079g).
O6    burden.m6(reg): gains, estates, total by band, register rows I-M6a to I-M6i; the same on every path.
O8    burden.m8(...)['burden'], short only: revenue per path is the post-fill window mean of M1 times GDP (raw.r['M1'] x raw.r['gdp'], pounds bn; its share of GDP is the M1
      headline), shares from burden.reform_shares(env.pack); `diff` is that burden minus M2 in life (points). The non-payer saving form and the line-mean thresholds stay limits.
OH1b, OH1c  `static(env)`, once: 1000 paths from env.rng('burden.static') with returns.ar1_paths at env.theta (I-D1a, I-D1b, I-D1b2), base.build_base(pack, reg, 0.5) unshaped
      (see the test: shaping scales payer wealth and the two are ratios), burden.m3_today and burden.m12 (rates I-D11a to c, c I-D14c, register rows named in burden.py);
      the cause `exempt_law` is the manifest's `exempt_by_law`. The all-tax line of OH1b is a limit of the first run (053c).
"""

import numpy as np

from model_v3.core import base as bs, burden as bd, returns as rt, revenue as rv

NAME = 'burden'
IDS = ('O2d', 'O2b', 'O2c', 'O4b', 'OL1', 'OH1b2', 'DH1c', 'O5', 'O6', 'O8', 'OH1b', 'OH1c')
COMPARATORS, REFORMS, STATIC_PATHS, STATIC_RATIO = ('zucman', 'uk_minimum', 'union', 'green', 'once'), ('property', 'gains'), 1000, 0.5
HORIZONS = ('transition', 'short', 'long')
BANDS = ('overall', 'D4_5', 'D6_7', 'D8_9', 'D10')


def per_path(raw, env, again):
    """Per-path arrays: {'M2d'|'M4b'|'OL1': {horizon: {key: (P,)}}, 'M2b'|'M2c': {horizon: {band: {'share_5': (P,)...}}}}."""
    if raw is None:
        return {}
    gate = lambda k, v: np.where(raw.ok, v, np.nan) if k == 'short' else v
    deep = lambda k, d: {a: (deep(k, b) if isinstance(b, dict) else gate(k, b)) for a, b in d.items()}
    bill, income = raw.base.income_deciles['total_tax'], raw.base.income_deciles['gross_income']
    ctx, out = env.ctx, {x: {} for x in ('M2d', 'M2b', 'M2c', 'M4b', 'M4c')}
    d = bd.dh1c(env.pack, list(ctx.rec), ctx.mp['parts'], ctx.mp['payer_taxes'])['bill_pct_income']
    out['DH1c'] = {'overall': 100 * bill.sum() / income.sum(), **dict(zip(bd.DECILES, d))}
    for k in HORIZONS:
        lo, hi, fl = raw.lo[k], raw.hi[k], raw.fl
        m4b = bd.m4(raw.r['P5'], hi, raw.inc, bill, income)['M4b']
        out['M2d'][k], out['M2b'][k], out['M2c'][k] = (deep(k, f) for f in (bd.m2d(fl, lo, hi), bd.m2b(fl, lo, hi), bd.m2c(fl, lo, hi)))
        out['M4b'][k], out['M4c'][k] = deep(k, m4b), deep(k, bd.m4c(m4b, income))
    out['DH1c'] = {k: np.full(len(raw.ok), v) for k, v in out['DH1c'].items()}
    out['OH1b2'] = np.full(len(raw.ok), bd.m11(ctx.reg))
    b, full = raw.base, lambda v: np.full(len(raw.ok), float(v))
    out['O6'] = {k: {ln: full(v) for ln, v in d.items()} for k, d in bd.m6(ctx.reg).items()}
    out['O5'], out['O8'] = {k: {} for k in HORIZONS}, {}
    for k in HORIZONS:
        m5 = bd.m5(b.wealth, b.adults_k, ctx.reg, bd.m2(raw.fl, raw.lo[k], raw.hi[k])['overall'])
        out['O5'][k] = {c: {'burden': full(m5[c]), 'diff': gate(k, m5[c + '_diff'])} for c in COMPARATORS}
    gdp1, lo, hi = np.ones_like(raw.r['gdp']), raw.lo['short'], raw.hi['short']
    rev = rv.window_mean(raw.r['M1'] * raw.r['gdp'], gdp1, lo, hi)
    sh, nan, m8 = bd.reform_shares(env.pack), np.full(len(raw.ok), np.nan), {}
    for r in REFORMS:          # a reform whose base has no share for a band where payers are (property below D6, at a low threshold ratio) has no value there: nan
        try:
            m8[r] = bd.m8(b.wealth, b.adults_k, b.band, b.w_min, np.where(rev > 0, rev, np.nan), {r: sh[r]})[r]
        except bd.BurdenError:
            m8[r] = {'burden': nan}
    m2s = bd.m2(raw.fl, lo, hi)['overall']
    out['O8'] = {r: {'burden': gate('short', m8[r]['burden']), 'diff': gate('short', m8[r]['burden'] - m2s)} for r in REFORMS}
    return out


def static(env):
    """OH1b and OH1c: once, single horizon, over STATIC_PATHS return paths at the inputs `env.theta` and the base at the reference ratio."""
    th, reg = env.theta, env.ctx.reg
    g = rt.ar1_paths(env.rng('burden.static'), th['I-D1a'], th['I-D1b'], th['I-D1b2'], bd.G, STATIC_PATHS)
    base, c, rates = bs.build_base(env.pack, reg, STATIC_RATIO), th['I-D14c'] / 100, tuple(th[i] for i in ('I-D11a', 'I-D11b', 'I-D11c'))
    m12 = bd.m12(base, g, c, reg, env.pack, rates)
    return {'OH1b': {('single', (('wealth_band', b),), None): v for b, v in bd.m3_today(base, g, c, reg, rates).items()},
            'OH1c': {('single', tuple(sorted((('wealth_band', b), ('cause', 'exempt_by_law' if ca == 'exempt_law' else ca)))), None): x
                     for b, d in m12.items() for ca, x in d.items()}}


def cells(e):
    """{id: {(horizon, by, line): array}}; `by` is a sorted tuple of (name, value)."""
    if not e:
        return {}
    out = {i: {} for i in IDS if i not in ('OH1b', 'OH1c')}
    out['OH1b2']['single', (), None] = e['OH1b2']
    out['O8'].update({('short', (('reform', r),), ln): v for r, d in e['O8'].items() for ln, v in d.items()})
    for k in HORIZONS:
        for b in BANDS:
            out['O2d'][k, (('wealth_band', b),), None] = e['M2d'][k][b]
            for oid, m, dim, cuts in (('O2b', 'M2b', 'cutoff_pct_of_income', bd.CUT_INCOME), ('O2c', 'M2c', 'cutoff_pct_of_liquid_assets', bd.CUT_LIQUID)):
                for c in cuts:
                    out[oid][k, tuple(sorted((('wealth_band', b), (dim, c)))), None] = e[m][k][b][f'share_{c}']
        for d in ('overall', *bd.DECILES):
            out['O4b'][k, (('income_decile', d),), None] = e['M4b'][k][d]
        for d in ('overall', *bd.DECILES):
            out['DH1c'][k, (('income_decile', d),), None] = e['DH1c'][d]
        out['O6'].update({(k, (('wealth_band', b),), ln): v for b, d in e['O6'].items() for ln, v in d.items()})
        out['O5'].update({(k, (('comparator', c),), ln): v for c, d in e['O5'][k].items() for ln, v in d.items()})
        for p in bd.REF_DECILE:
            out['OL1'][k, (('reference_worker', p),), None] = e['M4c'][k][p]
    return out
