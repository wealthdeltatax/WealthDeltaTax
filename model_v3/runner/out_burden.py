"""
out_burden.py -- output group: burden, non-payer savings and the comparators (model v3, brief 086c)
===================================================================================================
Interface: see groups.py. Layer L4 (conftest LAYER): imports numpy and core/burden.py only. No file is read and nothing runs at import (R8); no country or tax is named (R11).

BUILT (the metric each id reads, all from `Raw`, no new maths)
O2d   burden.m2d(raw.fl, lo, hi): M2 with the death flows. They are in `raw.fl` (the burden run keeps `death`, `full` or not), so `again` is not used.
O2b, O2c   burden.m2b / m2c (all net WDT, burden.py's default): the cell is the share of payers above each cut-off; the payer mean is not in the manifest.
O4b   burden.m4(...)['M4b'], by income decile, at the horizon's last year; O4a's inputs (`raw.r['P5']`, `raw.inc`, `raw.base.income_deciles`).
OL1   burden.m4c on that M4b and the income deciles.

NOT BUILT: O5, O6, O8, OH1b, OH1b2, OH1c, DH1c. Their core functions (m5, m6, m8, m3_today, m11, m12, dh1c) take the register or the pack, and
`per_path(raw, again)` is given neither (`Raw` holds the base, not `pack` or `reg`). Reported to the guru as an interface question (brief 086c).
"""

import numpy as np

from model_v3.core import burden as bd

NAME = 'burden'
IDS = ('O2d', 'O2b', 'O2c', 'O4b', 'OL1')
HORIZONS = ('transition', 'short', 'long')
BANDS = ('overall', 'D4_5', 'D6_7', 'D8_9', 'D10')


def per_path(raw, env, again):
    """Per-path arrays: {'M2d'|'M4b'|'OL1': {horizon: {key: (P,)}}, 'M2b'|'M2c': {horizon: {band: {'share_5': (P,)...}}}}."""
    if raw is None:
        return {}
    gate = lambda k, v: np.where(raw.ok, v, np.nan) if k == 'short' else v
    deep = lambda k, d: {a: (deep(k, b) if isinstance(b, dict) else gate(k, b)) for a, b in d.items()}
    bill, income = raw.base.income_deciles['total_tax'], raw.base.income_deciles['gross_income']
    out = {x: {} for x in ('M2d', 'M2b', 'M2c', 'M4b', 'M4c')}
    for k in HORIZONS:
        lo, hi, fl = raw.lo[k], raw.hi[k], raw.fl
        m4b = bd.m4(raw.r['P5'], hi, raw.inc, bill, income)['M4b']
        out['M2d'][k], out['M2b'][k], out['M2c'][k] = (deep(k, f) for f in (bd.m2d(fl, lo, hi), bd.m2b(fl, lo, hi), bd.m2c(fl, lo, hi)))
        out['M4b'][k], out['M4c'][k] = deep(k, m4b), deep(k, bd.m4c(m4b, income))
    return out


def cells(e):
    """{id: {(horizon, by, line): array}}; `by` is a sorted tuple of (name, value)."""
    if not e:
        return {}
    out = {i: {} for i in IDS}
    for k in HORIZONS:
        for b in BANDS:
            out['O2d'][k, (('wealth_band', b),), None] = e['M2d'][k][b]
            for oid, m, dim, cuts in (('O2b', 'M2b', 'cutoff_pct_of_income', bd.CUT_INCOME), ('O2c', 'M2c', 'cutoff_pct_of_liquid_assets', bd.CUT_LIQUID)):
                for c in cuts:
                    out[oid][k, tuple(sorted((('wealth_band', b), (dim, c)))), None] = e[m][k][b][f'share_{c}']
        for d in ('overall', *bd.DECILES):
            out['O4b'][k, (('income_decile', d),), None] = e['M4b'][k][d]
        for p in bd.REF_DECILE:
            out['OL1'][k, (('reference_worker', p),), None] = e['M4c'][k][p]
    return out
