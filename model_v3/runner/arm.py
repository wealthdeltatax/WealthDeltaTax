"""
arm.py -- the hooks that carry the household's year through the kernel's five sites (model v3, brief 114c, kernel-wiring-design 3.2 and 3.6)
============================================================================================================================================
Layer 3.6: numpy and core/household.py; the runner builds a hook and passes it down through revenue.run_lines, burden.line_flows and support.wdt_run in the place of `c`.
A hook has `pre(book, t, g) -> (g_N, x)`, `post(book, fl)`, `reconcile(book)` (value a death or the horizon moved, paid in the year, 120c), the flag `household` (the arm settles Route D and B in the last
year and keeps the public ledger, `receipts`, `class_returns`) and the site methods `grown`, `gain` and `free` (the places that read `c`). `LegacyHook(c)` does exactly what `c` did (bit equal); the comparators' `support.system_run` stay legacy (design 3.6).
`line_state` (117c, 119c: the tail pension ceiling `cap`) builds the 14 lines' class balances, income, saving and accrual from the pack and register, `returns` applies the debt rule,
and `HouseholdHook` runs the household year (convention A), paying the WDT from the non-pension classes.
"""

from dataclasses import dataclass

import numpy as np

from model_v3.core import household as hh, pension_lien as pl

CLASSES = ('property', 'net_financial', 'physical', 'pension')
PROPERTY_GAIN = 0.016455                                                                            # F-20: the JST housing holding gain, all years (cell_baseline.py); a scenario value, not a register row
WITHHELD = {}                                                                                       # outputs that read the legacy c and have no base on the account: none since 126c (M3, M12, M13, M15 and M9 are on it)


WITHHELD_BY = {}                                                                                     # an output kept without some by-values: none since 126c (the tornado's M3 head returned)


def withheld(label):
    """{output id: 'legacy_only' (the whole id) or {dimension: {value: 'legacy_only'}} (part of it)} for a run label: the household arm withholds what reads the legacy c (never a number); the legacy arm withholds none."""
    if label['arm'] != 'legacy' and (label.get('scenario') or {}).get('market_paths'):                  # the comparators run on fixed scenario rates: not like for like with the WDT on paths (128c)
        return {**dict.fromkeys(WITHHELD, 'legacy_only'), **WITHHELD_BY, 'OW1': 'legacy_only'}
    return {} if label['arm'] == 'legacy' else {**dict.fromkeys(WITHHELD, 'legacy_only'), **WITHHELD_BY}


TAKES_D10 = ('D10a', 'D10b', 'RL3', 'RL2', 'RL1')                  # the tail lines take D10's class mix (labelled an assumption, design 2.2)


class LegacyHook:
    """The legacy arm: every class grows at g, then a share c is consumed, W(1 + g)(1 - c)."""

    household = False                                                                              # the legacy arm settles nothing at the horizon and keeps no ledger (revenue.run_lines)

    def __init__(self, c):
        self.c = c

    def reconcile(self, book):
        pass                                                                                       # the legacy rule pays no value from classes

    def pre(self, book, t, g):
        return g, -self.c

    def post(self, book, fl):
        pass                                                                                       # nothing after settlement

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

    def __init__(self, state, gain, growth=0.0, c=None, mu=None):
        self.st, self.gn, self.gr, self.c, self.book, self.W_after, self.mu, self.dv, self.gh = state, gain, growth, c, None, None, mu, None, []   # `mu` the market process's mean (fraction): given, net financial and pension deviate with the path's market return (128c)
        self.household = c is None                                                                # revenue.run_lines settles the horizon, reconciles it in the last year and keeps the ledger (120c)

    def _gn(self, g):
        """The year's class gains: the scenario rates; with `mu` (128c) net financial and pension add the path's deviation g - mu (loading 1), so the mean return is the scenario rate. Property and physical stay fixed."""
        if self.mu is None:
            return self.gn
        dev = np.asarray(g, float) - self.mu
        return {**self.gn, 'net_financial': self.gn['net_financial'] + dev, 'pension': self.gn['pension'] + dev}

    def _n(self, q):
        return sum(q[k] for k in (CLASSES if self.c is not None else CLASSES[:3]))              # the legacy arm sells every class; here pension is a balance beside the units

    def _start(self, book):
        t = lambda v: np.tile(np.asarray(v, float), book.n // len(self.st['income']))
        self.gh = []
        self.PL, self.PK = np.zeros(book.n), np.zeros(book.n)                                           # the pension-secured lien per line (132c) and its part the kernel's cap left unpaid (133c, netted from the kernel's pension, not its units)
        self.q, self.book, self.rcv = {**{k: t(v) for k, v in self.st['pos'].items()}, 'debt': np.zeros(book.n)}, book, {k: np.zeros(book.n) for k in CLASSES[:3]}
        self.inc, self.sav, self.acc = t(self.st['income']), t(self.st['sav']), t(self.st['acc'])
        if self.c is None:
            if np.any(self._n(self.q) <= 0):
                raise ValueError('a line has no non-pension wealth, so no route units: the household arm cannot start')
            f = self._n(self.q) / book.family_true()
            for x in book.R.values():
                x.update({k: x[k] * f for k in ('V', 'dd', 'Wp', 'ppu')})
            self.mix = {r: x['V'] / sum(y['V'] for k, y in book.R.items() if k != 'Cv') for r, x in book.R.items() if r != 'Cv'}      # the line's opening route mix, kept for a restart (137c)
            book.pen = book.penp = self.q['pension'].copy()
            book.cap_cb = self.carry                                                                    # the tax a route cannot pay is carried as a lien, not lost to unpaid_B (133c)

    def pre(self, book, t, g):
        self._start(book) if book is not self.book else self.reconcile(book)                       # value a reset moved after the last post is paid from the classes first (a death's, in the year)
        inc, N0, defl = self.inc * (1.0 + self.gr) ** (t - 1), self._n(self.q), dict(cpi=0.0, hfce=0.0)
        if self.c is not None:
            self.q1, _ = hh.household_step('arm', self.q, dict(c=self.c), dict(r=g), defl, 'legacy', sink='net_financial')
            self.W_after = sum(self.q1[k] for k in CLASSES)
            return g, -self.c
        gn = returns(self.q, self._gn(g))
        self.dv = None if self.mu is None else np.asarray(g, float) - self.mu
        self.gh.append(self.dv)
        self.q1, self.acct = self._year(self.q, inc, self.sav, self.acc, gn)
        PL0, PK0, self.PL, self.PK = self.PL, self.PK, pl.accrue(self.PL, book.r_def), pl.accrue(self.PK, book.r_def)    # the lien accrues at the kernel's deferral rate (132c); U = PL - PK is the part netted from the units
        self.nw0, self.T, self.unpaid, self.new, self.accr, self.set_c, self.set_p = sum(self.q[k] for k in CLASSES) - PL0, 0.0, 0 * PL0, 0.0, self.PL - PL0, 0.0, 0.0
        N1, N0, self.ex = self._n(self.q1), N0 - (PL0 - PK0), 0 * PL0
        dead = np.abs(N0) <= 1e-12                                                                 # the class floor (127c): a line whose units are all 0 cannot carry any flow (units grow multiplicatively), so it stays at 0; a line with negative wealth keeps its units
        self.wo = np.where(dead, self.PL - self.PK, 0.0)                                                      # a lien on a line with no units left is written off: the ledger reports it (132c)
        N1, self.PL = N1 - (self.PL - self.PK), self.PL - self.wo
        back = self._restart(book, dead & (N1 > 1e-12))                                              # 137c: a dead line whose year's saving is positive restarts from it (units = saving / price), so the floor does not fire
        self.fl = np.where(dead & ~back, -N1, 0.0)                                                  # what the floor added (+) or removed (-) in the year; an alarm, never tuned away
        for k in CLASSES[:3]:
            self.q1[k] = np.where(dead & ~back, 0.0, self.q1[k])
        book.unpaid_B = book.unpaid_B + np.abs(self.fl)                                             # recorded as the model's shortfall alarm (shortfall_lines counts it)
        N0 = np.where(dead, 1.0, N0)
        g_n = sum(np.asarray(gn[k]) * self.q[k] for k in CLASSES[:3]) / N0
        book.pen, self.W_after = self.q1['pension'] - self.PK, sum(self.q1[k] for k in CLASSES) - self.PL
        return g_n, (self._n(self.q1) - (self.PL - self.PK)) / (N0 * (1.0 + g_n)) - 1.0                                     # growth then the flow reach the household's closing non-pension total exactly (I1)

    def _restart(self, book, want):
        """The class floor's restart (137c; a labelled bookkeeping rule, no register input): the lines in `want` (no units, positive saving) get units again at the year's price, one number on every route so that the family value is 1,
        which `pre` takes as the opening value (N0 = 1) and its flow brings to the closing total. A route price that a rescale at N <= 0 left at 0 or below is first restored to the opening route mix (`self.mix`; Cv at C's). The units are bought (`sold` falls), so f + s + sold = tot holds. Returns `want`."""
        rt, cv = {r: x for r, x in book.R.items() if r != 'Cv'}, book.R.get('Cv')
        bad = want & (sum(x['V'] for x in rt.values()) <= 0.0)
        for r, x in rt.items():
            x['V'] = np.where(bad, self.mix[r], x['V'])
        p, kept = sum(x['V'] for x in rt.values()), 0.0 if cv is None else cv['f'] * np.where(bad, rt['C']['V'], cv['V'])      # Cv's units (the verified tranche of C) keep their value
        cv is None or cv.update(V=np.where(bad, rt['C']['V'], cv['V']))
        for x in rt.values():
            u = np.where(want, (1.0 - kept) / np.where(want, p, 1.0) - x['f'], 0.0)
            tg = (1.0 - kept) / np.where(want, p, 1.0)
            x['f'], x['sold'] = np.where(bad, tg, x['f'] + u), np.where(bad, x['tot'] - x['s'] - tg, x['sold'] - u)      # a wiped line's units can be huge (a rescale at a near-zero value) and f + u then loses the restart in rounding: its f is the target and its sold the identity's remainder (135c)
        return want

    def lien(self):
        """The public ledger's receivable (132c), by line: the lien balance at the close and the year's new, accrued, settled and written-off amounts (billions after weighting; the balance moves by new + accr - settled - wo); `xnew` is the part of `new` the kernel never moved (the cap's excess, 133c), which is not in the year's value paid."""
        return dict(bal=self.PL, new=self.new, accr=self.accr, settled=self.set_c + self.set_p, wo=self.wo, xnew=self.ex)

    def _year(self, q, inc, sav, acc, gn):
        """The household's year before any tax (convention A): the closing balances and the account of balances `q` with income `inc`, saving ratio `sav`, pension accrual `acc` and the holding gains `gn`."""
        return hh.household_step('arm', q, dict(Y_L=inc * (1.0 + acc), C=(1.0 - sav) * inc, pen_in=acc * inc), dict(g=gn), dict(cpi=0.0, hfce=0.0), 'A', sink='net_financial', source_weights=dict(property=1.0))

    def _pay(self, q, T):
        """The payment T (a line's value moved to the state, negative a refund) on the classes q, pro rata to the positive non-pension balances; pension is never sold. Adds to the year's T and unpaid."""
        w = {k: np.maximum(q[k], 0.0) for k in CLASSES[:3]}
        w['net_financial'] = np.where((sum(w.values()) <= 0.0) & (np.asarray(T) < 0), 1.0, w['net_financial'])      # a refund on a line with no positive non-pension balance goes to net financial (128c): a fall in the pension's value can refund a line the floor holds at 0; it raised I1 before
        q1, _, un = hh.apply_payment(q, T, w)
        self.T, self.new = self.T + T - un, self.new + un
        self.PL = pl.add(self.PL, un)                                                              # the kernel took the whole tax from the line's units (net of the lien): what the classes cannot pay is carried as a lien on the pension (132c)
        for k in CLASSES[:3]:
            self.rcv[k] = self.rcv[k] + q[k] - q1[k]                                              # the state's receipt by class: the value the line paid out of each
        return q1

    def receipts(self):
        """The true value the state received since the last call, by non-pension class, per line (millions of pounds per adult; a refund is negative): the public ledger's receipts (120c)."""
        out, self.rcv = self.rcv, {k: np.zeros_like(v) for k, v in self.rcv.items()}
        return out

    def class_returns(self):
        """The household's holding gain by non-pension class (scenario rates, I-D1h to I-D1j) in the year just run: the ledger's returns. With `mu`, net financial carries the path's deviation, per line and path (n,)."""
        r = {k: float(self.gn[k]) for k in CLASSES[:3]}
        return r if self.dv is None else {**r, 'net_financial': r['net_financial'] + self.dv}

    def class_paths(self, T, P):
        """The ledger's class returns by year and path, (T, P) each (128c): the scenario rate, plus the recorded deviation of the path (every line of a path carries the same one) for net financial."""
        out = {k: np.full((T, P), r) for k, r in {k: float(self.gn[k]) for k in CLASSES[:3]}.items()}
        if self.mu is not None:
            out['net_financial'] = out['net_financial'] + np.array(self.gh)[:, ::len(self.st['income'])]
        return out

    def carry(self, book, ex):
        """The kernel's cap callback (133c): the tax a route could not pay (`ex`, per line) is carried as a lien on the pension. It is netted from the kernel's pension, which the kernel reads at once and takes as the new basis at the end of the assessment; the units do not move."""
        self.PL, self.PK, self.new, self.ex, book.pen = self.PL + ex, self.PK + ex, self.new + ex, self.ex + ex, book.pen - ex

    def _check(self, book):
        N = self._n(self.q) - (0.0 if self.c is not None else self.PL - self.PK)                  # the family value is net of the lien's unit part
        if np.any(np.abs(book.family_true() - N) > np.maximum(1e-7, 1e-9 * np.abs(N))) or (self.c is None and np.any(np.abs(book.pen - (self.q['pension'] - self.PK)) > 1e-12)):
            raise ValueError("I1 fails: the book's family value is not the class total, or its pension is not the pension balance")

    def reconcile(self, book):
        """Value the kernel moved outside `post` (a death's tax, settlements, the heir's tax; the horizon's: call it after settle_terminal) is paid from the classes, in the year's account. Pension passes to the heir unchanged."""
        if self.c is not None:
            return
        gap = self._n(self.q) - (self.PL - self.PK) - book.family_true()
        self.q = self._pay(self.q, np.where(np.abs(gap) > 1e-12 * np.maximum(1.0, np.abs(self._n(self.q))), gap, 0.0))
        self._check(book)

    def settle(self, book):
        """Settle the lien at a death or the horizon (132c; revenue.run_lines calls it after `reconcile`): from the positive non-pension classes, then a one-off draw on the pension (the only time it is drawn); the kernel's family
        value, net of the lien, rises by the draw, so the route units are rescaled to it (as `_start` does). What the pension cannot cover is written off (limited recourse, 138c)."""
        if not np.any(self.PL):
            return                                                                                  # no lien, nothing moves (the account and the ledger of a line that never needed it are unchanged, bit for bit)
        q3 = {k: self.q[k] for k in CLASSES[:3]}
        q1, pen1, paid, d, rest = pl.settle(q3, self.PL, self.q['pension'])
        self.set_c, self.set_p = self.set_c + (self.PL - rest - d), self.set_p + d
        self.wo, self.PK = self.wo + rest, 0.0 * rest                                              # limited recourse (138c): the state collects up to the pension; what it cannot cover is written off in the ledger (a labelled cost), not left as unpaid_B
        self.q, self.PL = {**self.q, **q1, 'pension': pen1}, 0.0 * rest
        for k in CLASSES[:3]:
            self.rcv[k] = self.rcv[k] + paid[k]                                                    # the state's receipt by class, the draw in the classes' mix
        fam = book.family_true()
        f = np.where(fam != 0, (self._n(self.q) - (self.PL - self.PK)) / np.where(fam != 0, fam, 1.0), 1.0)
        for x in book.R.values():
            x.update({k: x[k] * f for k in ('V', 'dd', 'Wp', 'ppu')})
        book.pen = book.penp = pen1 - self.PK
        self._check(book)

    def post(self, book, fl):
        T = sum(fl.value.values()) if fl.value else 0.0
        if self.c is not None and np.any(np.abs(T) > 1e-12):
            raise ValueError('the legacy rule on classes moves no value to the state: the rate must be zero')
        self.q = self.q1 if self.c is not None else self._pay(self.q1, T)
        self._check(book)

    def account(self):
        """The last year's account by line: dNW (pension included), S, CG, T_WDT, unpaid (a model alarm), the payment over net financial and over non-pension wealth, and the residual dNW - (S + CG - T_WDT)."""
        q0, dnw = self.q1, sum(self.q[k] for k in CLASSES) - self.PL - self.nw0
        fin, nonpen = q0['net_financial'], sum(q0[k] for k in CLASSES[:3])
        return dict(dNW=dnw, S=self.acct['S'], CG=self.acct['CG'], T_WDT=self.T, unpaid=self.unpaid, pay_over_fin=np.where(self.T == 0, 0.0, hh._ratio(self.T, fin)), pay_over_nonpension=np.where(self.T == 0, 0.0, hh._ratio(self.T, nonpen)),
                    residual=dnw - (self.acct['S'] + self.acct['CG'] - self.T + self.fl - self.new - self.accr), floor=self.fl, PL=self.PL, lien_new=self.new, settled_classes=self.set_c, settled_pension=self.set_p)

    def system(self, kind, rate, G, payer):
        """A comparator tax on the account (126c, M13): terminal wealth (pension included) and the lifetime tax, both (L,), of the lines over G years under `kind` ('none'; 'stock_wealth_tax' on the opening net worth, pension included;
        'income_tax_gains' on the positive holding gain CG; 'consumption_tax' on the year's consumption C), paid from the non-pension classes like the WDT (what they cannot cover is not paid); lines outside `payer` pay nothing. Keeps no state."""
        q, paid, s = {**{k: np.asarray(v, float) for k, v in self.st['pos'].items()}, 'debt': np.zeros(len(self.st['income']))}, 0.0, self.st
        for t in range(G):
            inc = s['income'] * (1.0 + self.gr) ** t
            q1, a = self._year(q, inc, s['sav'], s['acc'], returns(q, self.gn))
            base = {'none': 0.0, 'stock_wealth_tax': sum(q[k] for k in CLASSES), 'income_tax_gains': np.maximum(a['CG'], 0.0), 'consumption_tax': (1.0 - s['sav']) * inc}[kind]
            q, _, un = hh.apply_payment(q1, rate * base * payer, {k: np.maximum(q1[k], 0.0) for k in CLASSES[:3]})
            paid = paid + rate * base * payer - un
        return sum(q[k] for k in CLASSES), paid + 0.0 * q['property']

    def consumption(self):                                                                          # the account's year-1 consumption C by line (millions of pounds per adult): the base of M9's leavers' spend (126c)
        return (1.0 - self.st['sav']) * self.st['income']

    def grown(self, W0, g):
        return self.W_after

    def gain(self, g, run):
        """The accrued gain rate I3 reads: the run's recorded gain the rate applies to over its rate-weighted wealth, so that eps x gain x wbase is the sum over lines of rate x pre-tax change."""
        return run['wgain'] / np.where(run['wtau'] > 0, run['wtau'], np.nan)

    def free(self, g):
        """The untaxed path of site 4 (M3, M12): each line's yearly growth factor of total wealth, pension included, (G, L, P), from the opening balances with T = 0 through the same household step (126c); the scenario rates are the same on every path."""
        q, out = {**{k: np.asarray(v, float) for k, v in self.st['pos'].items()}, 'debt': np.zeros(len(self.st['income']))}, []
        if self.mu is not None:                                                                  # per-path market returns (128c): each path carries its own state, (L, P)
            q = {k: np.repeat(v[:, None], g.shape[1], 1) for k, v in q.items()}
        for t in range(len(g)):
            q1, _ = self._year(q, (self.st['income'] * (1.0 + self.gr) ** t)[:, None] if self.mu is not None else self.st['income'] * (1.0 + self.gr) ** t, *((self.st[k][:, None] if self.mu is not None else self.st[k]) for k in ('sav', 'acc')), returns(q, self._gn(g[t])))
            w0, w1 = (sum(x[k] for k in CLASSES) for x in (q, q1))
            out, q = out + [np.where(w0 != 0, w1 / np.where(w0 != 0, w0, 1.0), 1.0)], q1
        return np.array(out) if self.mu is not None else np.broadcast_to(np.array(out)[:, :, None], (*np.shape(out), g.shape[1]))


def household_inputs(ctx, base, inp, sav, regime='mid'):
    """(state, gain, growth) of the household hook at one scenario grid point (121c; the 118c account script's setup, now one builder): `inp` the stored inputs (cell-baseline/inputs_used.json: the
    three saving values `sav`, the market `regimes` and their yields `yreg`, the B.6g `income_scale`, the income growth `g`), `sav` the non-pension saving ratio, `regime` the market regime; the class gains are the
    housing gain (PROPERTY_GAIN), the regime's real return less its yield for net financial and pension, and I-D1j for physical; the tail pension cap is I-D1l and the accrual I-D1k (both central)."""
    y, r = inp['yreg'][regime], inp['regimes'][regime]
    st = line_state(base, ctx.pack.tables['decile_composition'], ctx.reg, sav, scale=inp['income_scale'], cap=ctx.reg['I-D1l'].central)
    return st, dict(property=PROPERTY_GAIN, net_financial=r - y, physical=ctx.reg['I-D1j'].central / 100, pension=r - y), inp['g']


@dataclass(frozen=True)
class Arm:
    """What `core_run` needs of an arm: `name`, the legacy consumption share `c` (the sites that still read it), `make()` a fresh hook (the household hook keeps the year's state, one per kernel run), `safe(T, P)` the
    safe-asset return series of the public ledger (None under legacy) and `label`, the run record: the arm and, for the household arm, the scenario grid point it used."""
    name: str
    c: float
    make: object
    safe: object
    label: dict


def build(arm, ctx, theta, base, g=None):
    """The arm of a run (brief 121c): `arm` is 'legacy' or 'household' or a dict {'arm', 'inputs', 'saving', 'regime'} (`inputs` the stored inputs of `household_inputs`; saving 'min', 'median' or 'max', regime 'mid' by default; `paths`: true gives per-path market returns, 128c, scenario-labelled: market-return risk only). `g` the run's market paths (T, P), read for the safe asset.
    The household arm is scenario-labelled and never called central; its safe asset earns the net financial class return, a stand-in (no register row), stated in the label."""
    a, c = {'arm': arm} if isinstance(arm, str) else dict(arm), theta['I-D14c'] / 100
    if a['arm'] == 'legacy':
        return Arm('legacy', c, lambda: LegacyHook(c), lambda T, P: None, dict(arm='legacy'))
    if a['arm'] != 'household':
        raise ValueError(f"arm must be 'legacy' or 'household', not {a['arm']!r}")
    name, regime = a.get('saving', 'median'), a.get('regime', 'mid')
    st, gain, growth = household_inputs(ctx, base, a['inputs'], a['inputs']['sav'][name], regime)
    label = dict(arm='household', scenario=dict(saving=name, saving_ratio=a['inputs']['sav'][name], regime=regime, class_returns={k: gain[k] for k in CLASSES[:3]}, pension_accrual=ctx.reg['I-D1k'].central / 100,
                 tail_pension_cap=ctx.reg['I-D1l'].central, income_scale=a['inputs']['income_scale']), safe_return='the net financial class return (a stand-in: no register row)', central=False)
    mu = theta['I-D1a'] / 100 if a.get('paths') else None
    label['scenario']['market_paths'] = None if mu is None else 'market-return risk only: net financial and pension deviate with the path\'s market return (loading 1); property, physical, saving, income and GDP growth are scenario constants'
    safe = (lambda T, P: np.full((T, P), gain['net_financial'])) if mu is None or g is None else (lambda T, P: gain['net_financial'] + np.asarray(g, float)[:T] - mu)
    return Arm('household', c, lambda: HouseholdHook(st, gain, growth, mu=mu), safe, label)
