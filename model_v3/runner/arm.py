"""
arm.py -- the hooks that carry the household's year through the kernel's five sites (model v3, brief 114c, kernel-wiring-design 3.2 and 3.6)
============================================================================================================================================
Layer 3.6: numpy and core/household.py; the runner builds a hook and passes it down through revenue.run_lines, burden.line_flows and support.wdt_run in the place of `c`.
A hook has `pre(book, t, g) -> (g_N, x)` (the growth rate and the signed flow share of the year: legacy returns g and -c), `post(book, fl)` (after
settlement) and one method for each site that read `c`: `grown` (revenue.run_lines, wealth after growth and flow), `gain` (revenue.identity, the accrued gain
rate) and `free` (burden.free_path, the untaxed growth factor). `LegacyHook(c)` does exactly what `c` did, operation for operation (bit equal);
the comparators' `support.system_run` stay legacy in this wiring (design 3.6, site 5).
Brief 117c (W5a): `line_state` builds the household arm's state of the 14 lines (class balances, income, saving and accrual shares) from the pack's decile composition and the register
(convention A; no file read here, every number arrives as an argument), `returns` applies the debt rule, and `HouseholdHook` runs the household year with no WDT (T = 0).
"""

import numpy as np

from model_v3.core import household as hh

CLASSES = ('property', 'net_financial', 'physical', 'pension')
TAKES_D10 = ('D10a', 'D10b', 'RL3', 'RL2', 'RL1')                  # the tail lines take D10's class mix (labelled an assumption, design 2.2)


class LegacyHook:
    """The legacy arm: every class grows at g, then a share c is consumed, W(1 + g)(1 - c)."""

    def __init__(self, c):
        self.c = c

    def pre(self, book, t, g):
        return g, -self.c

    def post(self, book, fl):
        """Nothing after settlement."""

    def grown(self, W0, g):
        return W0 * (1.0 + g) * (1.0 - self.c)

    def gain(self, g):
        return np.maximum((1.0 + g) * (1.0 - self.c) - 1.0, 0.0)

    def free(self, g):
        return (1.0 + g) * (1.0 - self.c)


def line_state(base, comp, reg, sav, scale=1.0):
    """The household arm's state of the base's lines, arrays of one entry per line (millions of pounds per adult; income a year): `pos` class -> balance (wealth times the line's decile
    share of the pack's `decile_composition` rows `comp`, debt netted inside the classes, so D1 keeps its negative shares), `income` (the band mean I-D9 per adult, D1 to D3 the low bound of
    I-D9a, tail lines the D10 mean, times `scale`, the B.6g factor, off at 1.0), `sav` (the non-pension saving ratio of income, a scenario value) and `acc` (the pension accrual share of income, I-D1k)."""
    mix = {(r['decile'], r['class']): r['value'] / 100 for r in comp}
    dec = ['D10' if x in TAKES_D10 else x for x in base.labels]
    inc = np.where(np.isnan(base.income), reg['I-D9a'].low / reg['I-D4h'].central / 1e6, base.income)
    n = len(base.labels)
    return dict(pos={k: base.wealth * np.array([mix[d, k] for d in dec]) for k in CLASSES}, income=inc * scale, sav=np.full(n, float(sav)), acc=np.full(n, reg['I-D1k'].central / 100))


def returns(pos, g):
    """The year's holding gains by class `g` (class -> rate) with the debt rule: a negative property or net financial balance earns 0% real (a labelled assumption; the debt rate range is unset)."""
    return {k: (np.where(pos[k] < 0, 0.0, v) if k in ('property', 'net_financial') else np.asarray(v, float)) for k, v in g.items()}
