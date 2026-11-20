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

NOT BUILT, each for a manifest or design gap, not a missing function (brief 086c): O5, O6, O8 have neither `by` nor `lines` in the manifest, so one cell cannot hold the
five comparators (or the reforms); OH1b and OH1c are once-not-per-schedule but need a threshold ratio (a swept lever, no central one) and a set of paths.
"""

import numpy as np

from model_v3.core import burden as bd

NAME = 'burden'
IDS = ('O2d', 'O2b', 'O2c', 'O4b', 'OL1', 'OH1b2', 'DH1c')
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
    return out


def cells(e):
    """{id: {(horizon, by, line): array}}; `by` is a sorted tuple of (name, value)."""
    if not e:
        return {}
    out = {i: {} for i in IDS}
    out['OH1b2']['single', (), None] = e['OH1b2']
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
        for p in bd.REF_DECILE:
            out['OL1'][k, (('reference_worker', p),), None] = e['M4c'][k][p]
    return out
