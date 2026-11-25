"""Brief 110c: the untaxed baseline of the ten cells (five pack bands by retired or not), run with household_step under convention A or legacy. Standalone: the kernel,
runner and revenue code do not import it, and it models no tax, no withdrawal from pension, no transition between cells and no death.

Units. Wealth and income are per household in thousands of the pack's pounds (UNIT) (wealth_total in billions over households in thousands; the income rows of the register are per household
per year), so a cell's weight is its number of households: the band's households (a tenth per decile) split by the person shares of cell_weights, a person-based proxy.
Cell wealth per household is the band mean for both stages and its classes are the shares of band_composition (debt is netted inside them, so the debt class is 0);
a cell's income per household is the band mean, the retired fraction of it for the retired. Nothing is rescaled to match a national total.
Saving is one uniform ratio of the cell's income (non-pension), with the pension accrual a share of the cell's income added to saving and to the pension class (111c; the share of opening
net worth of 110c grew with wealth). `scaled` multiplies every cell's income by one factor so the households' total is a stated national total; band proportions and the retired split stay.
Income grows with real GDP per head. Returns are real; the holding gain is credited, the retained yield is inside saving (convention A).
"""
from __future__ import annotations

import numpy as np

from model_v3.core import household as hh, pack as pk

CLASSES = ('property', 'net_financial', 'physical', 'pension')
BANDS = {'D1-3': (1, 2, 3), 'D4-5': (4, 5), 'D6-7': (6, 7), 'D8-9': (8, 9), 'D10': (10,)}
UNIT = 1e3                                                           # money is carried in thousands of pounds per household, so the identity check of household_step (1e-9, absolute) is not at the mercy of rounding
INCOME = {'D1-3': 'I-D9a', 'D4-5': 'I-D9a', 'D6-7': 'I-D9b', 'D8-9': 'I-D9c', 'D10': 'I-D9d'}


def cell_table(pack, reg, retired):
    """The ten cells: households (a count), income per household per year, positions per household by class. D1-3 takes the low bound of the D4-5 income row."""
    one = lambda var, d: pk.lookup(pack, 'wealth_distribution', variable=var, band=f'D{d}')[0]['value']
    persons = {(r['band'], r['stage']): r['persons'] for r in pack.tables['cell_weights']}
    share = {(r['band'], r['class']): r['value'] / 100 for r in pack.tables['band_composition']}
    out = []
    for band, ds in BANDS.items():
        hh_b, wealth = 1e3 * sum(one('households', d) for d in ds), 1e9 * sum(one('wealth_total', d) for d in ds)
        wealth = wealth / UNIT
        row = reg[INCOME[band]]
        inc = row.low if band == 'D1-3' else row.central
        for stage in ('not retired', 'retired'):
            n = hh_b * persons[band, stage] / (persons[band, 'not retired'] + persons[band, 'retired'])
            pos = {c: wealth / hh_b * share[band, c] for c in CLASSES}
            out.append(dict(cell=f'{band}|{stage}', band=band, stage=stage, households=n, income=inc / UNIT * (retired if stage == 'retired' else 1.0), pos=dict(pos, debt=0.0)))
    return out


def scaled(cells, total):
    """The cells with every income multiplied by one factor so that households times income equals `total` (pounds). Returns the cells and the factor."""
    k = total / UNIT / sum(c['households'] * c['income'] for c in cells)
    return [dict(c, income=c['income'] * k) for c in cells], k


def run_cell(cell, years, sav, accrual, growth, rets, convention='A', c=0.0):
    """Advance one cell `years` years; `accrual` is a share of the cell's income. rets: A and B, dict(g=class -> gain, y=class -> yield); legacy, dict(r=total return) with c the consumption share. Returns one
    (year, positions after, account) row per year, year 1 to `years`, and the opening positions as year 0 are the caller's."""
    pos, rows = {k: np.asarray(v, float) for k, v in cell['pos'].items()}, []
    for t in range(years):
        nw = sum(pos[k] for k in CLASSES)
        inc = cell['income'] * (1.0 + growth) ** t
        P = accrual * inc
        flows = dict(c=c) if convention == 'legacy' else dict(Y_L=inc + P, C=(1.0 - sav) * inc, pen_in=P)
        pos, acct = hh.household_step(cell['cell'], pos, flows, rets, dict(cpi=0.0, hfce=0.0), convention, sink='net_financial', source_weights=dict(property=1.0))
        rows.append((t + 1, pos, dict(acct, income=inc, nw_open=nw)))
    return rows
