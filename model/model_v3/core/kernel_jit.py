"""Brief 180c, stage A (spike): compiled drop-ins for the two household functions the year loop calls most (household.household_step in convention A, household.apply_payment on the three non-pension classes).

Off by default and never imported by the numpy path. `install()` swaps them into `core.household` only when `WDT_KERNEL=numba`; a call that is not the arm's own shape falls back to the numpy function.
Each compiled function repeats the numpy expression order term by term (left to right, the zero terms kept), so the only operation that can differ in the last bit is none here: there is no exp, log or pow in them.
numba absent: `AVAILABLE` is False and `install()` does nothing. fastmath is off.
"""
import os

import numpy as np

try:
    import numba
    AVAILABLE = True
except ImportError:                                           # the spike is optional
    numba = None
    AVAILABLE = False

CACHE = True


def _jit(f):
    return numba.njit(cache=CACHE, fastmath=False)(f) if AVAILABLE else f


@_jit
def _year_A(p, nf, ph, pen, Y_L, C, pen_in, g_p, g_n, g_h, g_e):
    """Convention A, hfce = cpi = 0, no debt, sink net_financial, T = 0. Returns the closing balances, S, CG and the largest |gap| of the account identity."""
    n = p.shape[0]
    q_p, q_n, q_h, q_e = np.empty(n), np.empty(n), np.empty(n), np.empty(n)
    S, CG, gap = np.empty(n), np.empty(n), 0.0
    for i in range(n):
        s = Y_L[i] + 0.0 - 0.0 - 0.0 - C[i]
        cg = 0.0 + g_p[i] * p[i] + g_n[i] * nf[i] + g_h[i] * ph[i] + g_e[i] * pen[i] + 0.0
        z = 0.0 * p[i], 0.0 * nf[i], 0.0 * ph[i], 0.0 * pen[i]
        a, b, c, d = p[i] * (1.0 + g_p[i]) + z[0], nf[i] * (1.0 + g_n[i]) + z[1], ph[i] * (1.0 + g_h[i]) + z[2], pen[i] * (1.0 + g_e[i]) + z[3]
        d = d + pen_in[i] - z[3] - 0.0
        b = b + s - pen_in[i] + 0.0 - (0.0 + z[0] + z[1] + z[2]) + 0.0
        q_p[i], q_n[i], q_h[i], q_e[i], S[i], CG[i] = a, b, c, d, s, cg
        nw0 = p[i] + nf[i] + ph[i] + pen[i] - 0.0
        dnw = a + b + c + d - (0.0 - 0.0) - nw0
        gp = abs(dnw - (s + cg + 0.0 + 0.0 - 0.0))
        if gp > gap or np.isnan(gp):
            gap = gp
    return q_p, q_n, q_h, q_e, S, CG, gap


@_jit
def _pay(p, nf, ph, T, w_p, w_n, w_h):
    """apply_payment on the three classes with the weights the caller gives (the arm's `_pay`: the positive balances), lien 0. Returns the closing classes and `unpaid`."""
    n = p.shape[0]
    o_p, o_n, o_h, un = np.empty(n), np.empty(n), np.empty(n), np.empty(n)
    for i in range(n):
        tot = 0.0 + w_p[i] + w_n[i] + w_h[i]
        sh_p, sh_n, sh_h = (w_p[i] / tot, w_n[i] / tot, w_h[i] / tot) if tot > 0 else (0.0, 0.0, 0.0)
        cash = T[i] - 0.0
        s = 0.0 + p[i] + nf[i] + ph[i]
        u = cash - max(s, 0.0) if (cash > 0 and cash > s + 1e-12) else 0.0
        o_p[i], o_n[i], o_h[i], un[i] = p[i] - (cash - u) * sh_p, nf[i] - (cash - u) * sh_n, ph[i] - (cash - u) * sh_h, u
    return o_p, o_n, o_h, un


def _vec(x, n):
    a = np.asarray(x, dtype=np.float64)
    return a if a.shape == (n,) else np.broadcast_to(a, (n,))


def install():
    """Swap the compiled functions into core.household when WDT_KERNEL=numba and numba is present. Returns True when installed."""
    if os.environ.get('WDT_KERNEL') != 'numba' or not AVAILABLE:
        return False
    from model_v3.core import household as hh
    if getattr(hh, '_jit_installed', False):
        return True
    step0, pay0 = hh.household_step, hh.apply_payment

    def step(cell, pos, flows, rets, defl, convention, T_WDT=0.0, source_weights=None, sink='financial', fin=None, TR=0.0, O=0.0):
        keys = ('property', 'net_financial', 'physical', 'pension', 'debt')
        ok = (convention == 'A' and sink == 'net_financial' and fin is None and source_weights == {'property': 1.0} and not np.any(T_WDT) and not np.any(O) and not np.any(TR)
              and tuple(pos) == keys and not np.any(pos['debt']) and not np.any(defl['hfce']) and not np.any(defl['cpi'])
              and set(flows) == {'Y_L', 'C', 'pen_in'} and set(rets) == {'g'} and set(rets['g']) == set(keys[:4]))
        if not ok:
            return step0(cell, pos, flows, rets, defl, convention, T_WDT, source_weights, sink, fin, TR, O)
        n = np.shape(pos['property'])[0]
        v = lambda x: _vec(x, n)
        g = rets['g']
        a, b, c, d, S, CG, gap = _year_A(v(pos['property']), v(pos['net_financial']), v(pos['physical']), v(pos['pension']), v(flows['Y_L']), v(flows['C']), v(flows['pen_in']),
                                         v(g['property']), v(g['net_financial']), v(g['physical']), v(g['pension']))
        if gap > 1e-9 or gap != gap:
            raise ValueError(f'the account does not close: the largest gap is {gap}')
        return {'property': a, 'net_financial': b, 'physical': c, 'pension': d, 'debt': pos['debt'] - 0.0}, {'S': S, 'CG': CG}

    def pay(q, T, source_weights=None, lien=0.0):
        n = np.shape(q['property'])
        ok = (source_weights is not None and tuple(source_weights) == ('property', 'net_financial', 'physical') and tuple(q) == ('property', 'net_financial', 'physical', 'pension', 'debt')
              and len(n) == 1 and not np.any(lien) and np.shape(T) in ((), n))
        if not ok:
            return pay0(q, T, source_weights, lien)
        w = [_vec(source_weights[k], n[0]) for k in source_weights]
        o_p, o_n, o_h, un = _pay(_vec(q['property'], n[0]), _vec(q['net_financial'], n[0]), _vec(q['physical'], n[0]), _vec(T, n[0]), *w)
        return {'property': o_p, 'net_financial': o_n, 'physical': o_h, 'pension': q['pension'], 'debt': q['debt'] + lien}, None, un

    hh.household_step, hh.apply_payment, hh._jit_installed = step, pay, True
    return True
