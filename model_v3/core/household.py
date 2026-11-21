"""Brief 108c: one household step, advancing one cell's positions by one year. A pure function, not called by the kernel, runner or revenue code.

Conventions (104r section 3, author rulings of 2026-11-21):
  A  credit the holding gain only; saving carries the retained yield once (dNW/NW = s + g_h). The recommended mode.
  B  credit total return (yield + gain) and take the yield out of saving; the same dNW, kept as an equivalence check.
  legacy  every class grows at the total return then loses the consumption share: W(1+r)(1-c), the kernel's grow_and_consume rule.
Crediting the total return and also leaving the yield in saving counts it twice; the identity below catches it (the tests build that case).

Account (real pounds of the pack's CPI basis):  dNW = S + CG + TR + O - T_WDT, checked to 1e-9 on every call.
  S = Y_L + Y_P - I_D - T_C - C; CG = holding gains on every asset class + the real erosion of debt at the expenditure deflator;
  the wedge between the two deflators is reported as its own entry of CG. O is an input residual, never solved. TR is fixed at 0.
Positions are plain numbers or arrays in a dict by class; the special classes are 'pension' (illiquid until a withdrawal flow) and 'debt' (a liability, positive).
Saving that is not pension accrual lands in the `sink` class; the WDT payment falls on the non-pension asset classes by `source_weights`
(default: pro rata to their value), never on pension. The function reads no pack and no register; the cell is a label only.
"""
from __future__ import annotations

import numpy as np

MODES = ('A', 'B', 'legacy')
FIXED = ('pension', 'debt')


def _ratio(a, b):
    return np.where(b > 0, a / np.where(b > 0, b, 1.0), np.inf)


def household_step(cell, pos, flows, rets, defl, convention, T_WDT=0.0, source_weights=None, sink='financial', fin=None, TR=0.0, O=0.0):
    """pos: class -> opening value. flows: Y_L, Y_P, I_D, T_C, C and the pension flows pen_in (contributions plus retained fund income, an aggregate scenario input) and pen_out
    (withdrawal); for legacy, 'c' (the consumption share). rets: 'g' class -> real holding gain rate, 'y' class -> yield rate (used by B only); for legacy 'r'.
    defl: 'cpi', 'hfce'. fin: the classes counted as net financial wealth in the liquidity diagnostic (default: the sink). Returns (pos1, acct)."""
    if convention not in MODES:
        raise ValueError(f'convention must be one of {MODES}, got {convention!r}')
    if np.any(np.asarray(TR) != 0):
        raise ValueError('TR is fixed at 0 in the first implementation')
    p = {k: np.asarray(v, float) for k, v in pos.items()}
    assets = [k for k in p if k != 'debt']
    if sink not in p or sink in FIXED:
        raise ValueError(f'the sink must be a non-pension asset class in pos, got {sink!r}')
    T = np.asarray(T_WDT, float)
    f = lambda k: np.asarray(flows.get(k, 0.0), float)
    nw0 = sum(p[k] for k in assets) - p.get('debt', 0.0)
    if convention == 'legacy':
        r, c = np.asarray(rets['r'], float), f('c')
        q = {k: (1.0 - c) * (p[k] * (1.0 + r)) for k in assets}
        S, CG, wedge = -c * (1.0 + r) * sum(p[k] for k in assets), r * sum(p[k] for k in assets), 0.0 * nw0
        q['debt'] = p.get('debt', 0.0)
    else:
        g, y = rets['g'], rets.get('y', {})
        gain = lambda k: np.asarray(g.get(k, 0.0), float)
        D, hfce, cpi = p.get('debt', 0.0), np.asarray(defl['hfce'], float), np.asarray(defl['cpi'], float)
        S = f('Y_L') + f('Y_P') - f('I_D') - f('T_C') - f('C')
        ero, wedge = hfce * D, (hfce - cpi) * D
        CG = sum(gain(k) * p[k] for k in assets) + ero
        yl = {k: (np.asarray(y.get(k, 0.0), float) * p[k] if convention == 'B' else 0.0 * p[k]) for k in assets}
        q = {k: p[k] * (1.0 + gain(k)) + yl[k] for k in assets}
        q['pension'] = q.get('pension', 0.0) + f('pen_in') - yl.get('pension', 0.0) - f('pen_out')
        q[sink] = q[sink] + S - f('pen_in') + f('pen_out') - sum(yl[k] for k in assets if k != 'pension') + np.asarray(O, float)
        q['debt'] = D - ero
    pay_pool = [k for k in assets if k not in FIXED]
    w = {k: (q[k] if source_weights is None else np.asarray(source_weights.get(k, 0.0), float)) for k in pay_pool}
    if source_weights is not None and set(source_weights) - set(pay_pool):
        raise ValueError('the payment cannot fall on pension, debt or a class not in pos')
    tot = sum(w.values())
    share = {k: _ratio(w[k], tot) * (tot > 0) for k in pay_pool}
    for k in pay_pool:
        q[k] = q[k] - T * share[k]
    nonpen, fin_w = sum(q[k] for k in pay_pool) + T, sum(q[k] for k in (fin or (sink,))) + T * sum(share[k] for k in (fin or (sink,)))
    if np.any(T > nonpen + 1e-12):
        raise ValueError('the payment exceeds non-pension wealth; pension is never sold')
    dnw = sum(q[k] for k in assets) - q['debt'] - nw0
    acct = dict(cell=cell, dNW=dnw, S=S, CG=CG, CG_wedge=wedge, TR=0.0 * dnw, O=np.asarray(O, float) * (convention != 'legacy'), T_WDT=T,
                pay_over_fin=_ratio(T, fin_w), pay_over_nonpension=_ratio(T, nonpen), pay_exceeds_fin=T > fin_w, shares=share)
    gap = dnw - (S + CG + acct['TR'] + acct['O'] - T)
    if np.any(np.abs(gap) > 1e-9):
        raise ValueError(f'the account does not close: dNW minus its flows is {gap}')
    return q, acct
