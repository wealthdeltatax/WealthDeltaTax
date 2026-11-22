"""
arm.py -- the hooks that carry the household's year through the kernel's five sites (model v3, brief 114c, kernel-wiring-design 3.2 and 3.6)
============================================================================================================================================
Layer 3.6: numpy and core/household.py; the runner builds a hook and passes it down through revenue.run_lines, burden.line_flows and support.wdt_run in the place of `c`.
A hook has `pre(book, t, g) -> (g_N, x)` (the growth rate and the signed flow share of the year: legacy returns g and -c), `post(book, fl)` (after
settlement) and one method for each site that read `c`: `grown` (revenue.run_lines, wealth after growth and flow), `gain` (revenue.identity, the accrued gain
rate) and `free` (burden.free_path, the untaxed growth factor). `LegacyHook(c)` does exactly what `c` did, operation for operation (bit equal);
the comparators' `support.system_run` stay legacy in this wiring (design 3.6, site 5).
Brief 119c: `d10_pension` and `line_state`'s `cap` hold the tail lines' pension at the D10 mean (a labelled scenario ceiling, I-D1l).
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


def d10_pension(base, comp, wd):
    """The D10 mean pension per adult (millions of pounds, real), observed: D10's pension share of its class total (`comp`, normalised) times the survey's D10 wealth (`wd`, the pack's wealth_distribution rows, scaled to the printed total as build_base does) over D10's adults."""
    w = {r['band']: r['value'] for r in wd if r['variable'] == 'wealth_total'}
    return comp_share(comp, 'D10', 'pension') * w['D10'] * w['all'] / sum(w[f'D{i}'] for i in range(1, 11)) / base.adults_k[9:].sum()


def comp_share(comp, d, k):
    mix = {(r['decile'], r['class']): r['value'] for r in comp}
    return mix[d, k] / sum(mix[d, c] for c in CLASSES)


def line_state(base, comp, reg, sav, scale=1.0, cap=None):
    """The household arm's state of the base's lines, arrays of one entry per line (millions of pounds per adult; income a year): `pos` class -> balance (wealth times the line's decile
    share of the pack's `decile_composition` rows `comp`, normalised to sum to 1; debt netted inside the classes, so D1 keeps its negative shares), `income` (the band mean I-D9 per adult, D1 to D3 the low bound of
    I-D9a, tail lines the D10 mean, times `scale`, the B.6g factor, off at 1.0), `sav` (the non-pension saving ratio of income, a scenario value) and `acc` (the pension accrual share of income, I-D1k)."""
    mix = {(r['decile'], r['class']): r['value'] for r in comp}
    dec = ['D10' if x in TAKES_D10 else x for x in base.labels]
    tot = {d: sum(mix[d, k] for k in CLASSES) for d in set(dec)}                                          # the printed shares are rounded: normalised so the classes sum to the wealth
    inc = np.where(np.isnan(base.income), reg['I-D9a'].low / reg['I-D4h'].central / 1e6, base.income)
    n = len(base.labels)
    pos = {k: base.wealth * np.array([mix[d, k] / tot[d] for d in dec]) for k in CLASSES}
    if cap is not None:                                                                                    # brief 119c: the tail lines' pension is at most `cap` (I-D1l); the displaced wealth goes to the other three classes, pro rata to D10's mix
        tail = np.array([x in TAKES_D10 for x in base.labels])
        pen = np.where(tail, np.minimum(pos['pension'], cap), pos['pension'])
        out = pos['pension'] - pen
        rest = {k: mix['D10', k] / sum(mix['D10', j] for j in CLASSES[:3]) for k in CLASSES[:3]}
        pos = {**{k: pos[k] + out * rest[k] for k in CLASSES[:3]}, 'pension': pen}
    return dict(pos=pos, income=inc * scale, sav=np.full(n, float(sav)), acc=np.full(n, reg['I-D1k'].central / 100))


def returns(pos, g):
    """The year's holding gains by class `g` (class -> rate) with the debt rule: a negative property or net financial balance earns 0% real (a labelled assumption; the debt rate range is unset)."""
    return {k: (np.where(pos[k] < 0, 0.0, v) if k in ('property', 'net_financial') else np.asarray(v, float)) for k, v in g.items()}


class HouseholdHook:
    """The household arm (W5a untaxed, W5b taxed): each year's growth and flow of every line from household_step (convention A) on class balances, then the WDT the kernel moves to the state paid from the non-pension classes (`post`). `state` is line_state's dict (arrays per line, tiled over
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
        elif self.c is None:
            self.reconcile(book)                                                                     # value a death or reset moved after the last post is paid from the classes first
        inc, N0, defl = self.inc * (1.0 + self.gr) ** (t - 1), self._n(self.q), dict(cpi=0.0, hfce=0.0)
        if self.c is not None:
            self.q1, _ = hh.household_step('arm', self.q, dict(c=self.c), dict(r=g), defl, 'legacy', sink='net_financial')
            self.W_after = sum(self.q1[k] for k in CLASSES)
            return g, -self.c
        gn = returns(self.q, self.gn)
        self.q1, self.acct = hh.household_step('arm', self.q, dict(Y_L=inc * (1.0 + self.acc), C=(1.0 - self.sav) * inc, pen_in=self.acc * inc), dict(g=gn), defl, 'A', sink='net_financial', source_weights=dict(property=1.0))
        self.nw0, self.T, self.unpaid = sum(self.q[k] for k in CLASSES), 0.0, 0.0
        g_n = sum(np.asarray(gn[k]) * self.q[k] for k in CLASSES[:3]) / N0
        book.pen, self.W_after = self.q1['pension'], sum(self.q1[k] for k in CLASSES)
        return g_n, self._n(self.q1) / (N0 * (1.0 + g_n)) - 1.0                                     # growth then the flow reach the household's closing non-pension total exactly (I1)

    def _pay(self, q, T):
        """The payment T (a line's value moved to the state, negative a refund) on the classes q, pro rata to the positive non-pension balances; pension is never sold. Adds to the year's T and unpaid."""
        q1, _, un = hh.apply_payment(q, T, {k: np.maximum(q[k], 0.0) for k in CLASSES[:3]})
        self.T, self.unpaid = self.T + T - un, self.unpaid + un
        return q1

    def _check(self, book):
        N = self._n(self.q)
        if np.any(np.abs(book.family_true() - N) > 1e-9 * np.maximum(1.0, np.abs(N))) or (self.c is None and np.any(book.pen != self.q['pension'])):
            raise ValueError("I1 fails: the book's family value is not the class total, or its pension is not the pension balance")

    def reconcile(self, book):
        """Value the kernel moved outside `post` (a death's tax, settlements, the heir's tax; the horizon's: call it after settle_terminal) is paid from the classes, in the year's account. Pension passes to the heir unchanged."""
        gap = self._n(self.q) - book.family_true()
        self.q = self._pay(self.q, np.where(np.abs(gap) > 1e-12 * np.maximum(1.0, np.abs(self._n(self.q))), gap, 0.0))
        self._check(book)

    def post(self, book, fl):
        T = sum(fl.value.values()) if fl.value else 0.0
        if self.c is not None and np.any(np.abs(T) > 1e-12):
            raise ValueError('the legacy rule on classes moves no value to the state: the rate must be zero')
        self.q = self.q1 if self.c is not None else self._pay(self.q1, T)
        self._check(book)

    def account(self):
        """The last year's account by line: dNW (pension included), S, CG, T_WDT, unpaid (a model alarm), the payment over net financial and over non-pension wealth, and the residual dNW - (S + CG - T_WDT)."""
        q0, dnw = self.q1, sum(self.q[k] for k in CLASSES) - self.nw0
        fin, nonpen = q0['net_financial'], sum(q0[k] for k in CLASSES[:3])
        return dict(dNW=dnw, S=self.acct['S'], CG=self.acct['CG'], T_WDT=self.T, unpaid=self.unpaid, pay_over_fin=np.where(self.T == 0, 0.0, hh._ratio(self.T, fin)), pay_over_nonpension=np.where(self.T == 0, 0.0, hh._ratio(self.T, nonpen)),
                    residual=dnw - (self.acct['S'] + self.acct['CG'] - self.T))

    def grown(self, W0, g):
        return self.W_after

    def gain(self, g, run):
        """The accrued gain rate I3 reads: the run's recorded gain the rate applies to over its rate-weighted wealth, so that eps x gain x wbase is the sum over lines of rate x pre-tax change."""
        return run['wgain'] / np.where(run['wtau'] > 0, run['wtau'], np.nan)

    def free(self, g):
        raise ValueError('the untaxed path of site 4 (M3, M12) stays legacy under the household arm: withheld until the comparator brief')
