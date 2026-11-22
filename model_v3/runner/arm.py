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

    def gain(self, g, run=None):
        return np.maximum((1.0 + g) * (1.0 - self.c) - 1.0, 0.0)

    def free(self, g):
        return (1.0 + g) * (1.0 - self.c)


def line_state(base, comp, reg, sav, scale=1.0):
    """The household arm's state of the base's lines, arrays of one entry per line (millions of pounds per adult; income a year): `pos` class -> balance (wealth times the line's decile
    share of the pack's `decile_composition` rows `comp`, normalised to sum to 1; debt netted inside the classes, so D1 keeps its negative shares), `income` (the band mean I-D9 per adult, D1 to D3 the low bound of
    I-D9a, tail lines the D10 mean, times `scale`, the B.6g factor, off at 1.0), `sav` (the non-pension saving ratio of income, a scenario value) and `acc` (the pension accrual share of income, I-D1k)."""
    mix = {(r['decile'], r['class']): r['value'] for r in comp}
    dec = ['D10' if x in TAKES_D10 else x for x in base.labels]
    tot = {d: sum(mix[d, k] for k in CLASSES) for d in set(dec)}                                          # the printed shares are rounded: normalised so the classes sum to the wealth
    inc = np.where(np.isnan(base.income), reg['I-D9a'].low / reg['I-D4h'].central / 1e6, base.income)
    n = len(base.labels)
    return dict(pos={k: base.wealth * np.array([mix[d, k] / tot[d] for d in dec]) for k in CLASSES}, income=inc * scale, sav=np.full(n, float(sav)), acc=np.full(n, reg['I-D1k'].central / 100))


def returns(pos, g):
    """The year's holding gains by class `g` (class -> rate) with the debt rule: a negative property or net financial balance earns 0% real (a labelled assumption; the debt rate range is unset)."""
    return {k: (np.where(pos[k] < 0, 0.0, v) if k in ('property', 'net_financial') else np.asarray(v, float)) for k, v in g.items()}


class HouseholdHook:
    """The household arm, untaxed (W5a): each year's growth and flow of every line from household_step (convention A, T_WDT = 0) on class balances. `state` is line_state's dict (arrays per line, tiled over
    the book's paths), `gain` the scenario holding gain by class, `growth` income growth a year. `c` given: the legacy rule on the classes (every class grows at g, a share c is consumed) while the book runs
    the legacy path, bit for bit as LegacyHook. A new book (each phase) restarts from the opening balances: its route values are rescaled to the non-pension total N and `pen` set, so every line holds units."""

    def __init__(self, state, gain, growth=0.0, c=None):
        self.st, self.gn, self.gr, self.c, self.book, self.W_after = state, gain, growth, c, None, None

    def _n(self, q):
        return sum(q[k] for k in (CLASSES if self.c is not None else CLASSES[:3]))              # the legacy arm sells every class; here pension is a balance beside the units

    def _start(self, book):
        t = lambda v: np.tile(np.asarray(v, float), book.n // len(self.st['income']))
        self.q, self.book = {**{k: t(v) for k, v in self.st['pos'].items()}, 'debt': np.zeros(book.n)}, book
        self.inc, self.sav, self.acc = t(self.st['income']), t(self.st['sav']), t(self.st['acc'])
        if self.c is None:
            if np.any(self._n(self.q) <= 0):
                raise ValueError('a line has no non-pension wealth, so no route units: the household arm cannot start')
            f = self._n(self.q) / book.family_true()
            for x in book.R.values():
                x.update({k: x[k] * f for k in ('V', 'dd', 'Wp', 'ppu')})
            book.pen = book.penp = self.q['pension'].copy()

    def pre(self, book, t, g):
        if book is not self.book:
            self._start(book)
        inc, N0, defl = self.inc * (1.0 + self.gr) ** (t - 1), self._n(self.q), dict(cpi=0.0, hfce=0.0)
        if self.c is not None:
            self.q1, _ = hh.household_step('arm', self.q, dict(c=self.c), dict(r=g), defl, 'legacy', sink='net_financial')
            self.W_after = sum(self.q1[k] for k in CLASSES)
            return g, -self.c
        gn = returns(self.q, self.gn)
        self.q1, _ = hh.household_step('arm', self.q, dict(Y_L=inc * (1.0 + self.acc), C=(1.0 - self.sav) * inc, pen_in=self.acc * inc), dict(g=gn), defl, 'A', sink='net_financial', source_weights=dict(property=1.0))
        g_n = sum(np.asarray(gn[k]) * self.q[k] for k in CLASSES[:3]) / N0
        book.pen, self.W_after = self.q1['pension'], sum(self.q1[k] for k in CLASSES)
        return g_n, self._n(self.q1) / (N0 * (1.0 + g_n)) - 1.0                                     # growth then the flow reach the household's closing non-pension total exactly (I1)

    def post(self, book, fl):
        if np.any(np.abs(sum(fl.value.values()) if fl.value else 0.0) > 1e-12):
            raise ValueError('the untaxed household arm moves no value to the state: the rate must be zero (the taxed arm is W5b)')
        self.q, N = self.q1, self._n(self.q1)
        if np.any(np.abs(book.family_true() - N) > 1e-9 * np.maximum(1.0, np.abs(N))):
            raise ValueError('I1 fails: the book\'s family value is not the class total')

    def grown(self, W0, g):
        return self.W_after

    def gain(self, g, run):
        """The accrued gain rate I3 reads: the run's recorded gain the rate applies to over its rate-weighted wealth, so that eps x gain x wbase is the sum over lines of rate x pre-tax change."""
        return run['wgain'] / np.where(run['wtau'] > 0, run['wtau'], np.nan)

    def free(self, g):
        raise ValueError('the untaxed path of site 4 (M3, M12) stays legacy under the household arm: withheld until the comparator brief')
