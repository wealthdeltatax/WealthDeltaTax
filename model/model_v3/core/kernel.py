"""
kernel.py -- the route-settlement kernel (model v3, ported from model_v2/wdt_kernel.py)
=======================================================================================
One implementation of the per-line yearly mechanics of the routes, vectorised over a line axis (shape (n,);
a scalar run is n = 1). The runner folds paths into the line axis, so n = lines x paths and the growth input
is a (T, n) matrix:

    growth -> consumption -> declared price -> verification -> ONE assessment on total declared W
    -> allocation of the tax / refund across routes -> settlement per route -> death and heir

LAYER (R4)
----------
L1. Imports numpy and the standard library only; no project module, not even schedule.py. The rate schedule
arrives as a callable rate_fn(x) -> tau, called with declared wealth divided by the index factor. No file is
read and nothing runs at import (R8).

CONVENTIONS (R6)
----------------
Arithmetic basis: growth g is the arithmetic return of one year, V -> V (1 + g); the caller supplies it.
Pounds are millions. + means family -> state in every flow.
Refund = tau x loss (C1 item 9): a fall in declared wealth is refunded at the marginal rate on an equivalent
gain, L = rate x delta for either sign. (v2 multiplied a loss by W_new / W_prev; v3 does not.) The rate is
read at the new declared wealth, as in v2.
Envelope resets at death (C1 item 10): the refund envelopes E_cash, EC, uo and the income envelope reset at
death, as in v2. The cumulative payer record (paid, refunded, lost_refund) is a lifetime record and does not.
The heir is taxed on the receipt as a delta from zero (the only heir rule; v2's 'fresh_entrant' is dropped).
Cumulative state per line (C1 item 5): book.paid is the sum of credited pounds that reached the state as tax
(in kind, in cash, or from external income); book.refunded the sum paid back; book.lost_refund the refund
that a cap held back. A refund that only cancels a deferred balance (lien, Route D accrual) is neither.

WHAT IT OWNS
------------
Settlement (D4a): A, B and D settle in cash-equivalent units at the true price; C settles in kind at the
declared price; B has three payment modes (D4b):
    sale    units sold at the true price (default pro-rata sale of holdings)
    lien    the tax is added to a deferred balance LB accruing at r_def, settled by sale at death and at the
            horizon; declared wealth is net of LB
    income  paid from external income up to the year's allowance, the shortfall by sale
Refunds (D5), capped by what was paid. C: units paid (uo), plus value paid under c_cap = 'units_and_value'.
A / B / D: the pooled cash envelope E_cash and the state's stake. Route D accrues liability and settles at the
true price at a voluntary reset, at death and at the horizon.
Verification (D6): independent hazards lam_C and lam_D; death verifies Route C with certainty (death_verify).
A Route D reset is an action the caller passes (reset_D), not a clock.

WHAT IT DOES NOT OWN
--------------------
Strategies (what alpha_C and alpha_D are each year), the ledger, the fund, the levy, the population, the
verdict tests: they stay in the callers.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

ZERO_TOL = 1e-9   # |x| below it is zero in a count or share (171c): the rounding noise of a zero-in-theory value is at most 1e-12, a real value is at least 1e-9


def neg(x):
    """x < 0 beyond ZERO_TOL (nan is False). The one test for a share or count of negatives."""
    return np.asarray(x) < -ZERO_TOL


def pos(x):
    """x > 0 beyond ZERO_TOL (nan is False). The one test for a share or count of payers."""
    return np.asarray(x) > ZERO_TOL


ROUTES = ('A', 'B', 'C', 'D', 'Cv')       # allocation order matters: E_cash and EC are pooled
B_MODES = ('sale', 'lien', 'income')
C_CAPS = ('units', 'units_and_value')
_INK = ('C', 'Cv')                        # routes paid in kind, each with its own units-paid cap


def _arr(x, n):
    a = np.asarray(x, dtype=float)
    return np.broadcast_to(a, (n,)).copy() if a.shape != (n,) else a.copy()


def _div(a, b):
    """a / b where b > 0, else 0 (no warning)."""
    b = np.asarray(b, dtype=float)
    return np.where(b > 0.0, a / np.where(b > 0.0, b, 1.0), 0.0)


# ─────────────────────────────────────────────────────────────
# FLOWS: what one operation moved
# ─────────────────────────────────────────────────────────────

@dataclass
class Flows:
    """Per-line results of one operation. value / credited / units are signed: + = family -> state.
    value is TRUE value moved, credited is the tax in credited pounds, units the units moved."""
    n: int
    value: dict = field(default_factory=dict)
    credited: dict = field(default_factory=dict)
    units: dict = field(default_factory=dict)
    income: np.ndarray = None            # net external income paid to the state (income mode)
    rate: np.ndarray = None
    delta: np.ndarray = None
    L: np.ndarray = None                 # total tax (+) or refund (-) assessed, credited pounds
    growth_family: dict = field(default_factory=dict)
    growth_state: dict = field(default_factory=dict)
    consumed: dict = field(default_factory=dict)       # true value of units sold to consume
    verify_family: np.ndarray = None     # units moved C -> Cv, family and state
    verify_state: np.ndarray = None

    def __post_init__(self):
        if self.income is None:
            self.income = np.zeros(self.n)

    def add(self, r, value=0.0, credited=0.0, units=0.0):
        for d, v in ((self.value, value), (self.credited, credited), (self.units, units)):
            d[r] = d.get(r, 0.0) + v


# ─────────────────────────────────────────────────────────────
# BOOK: the state of n lines
# ─────────────────────────────────────────────────────────────

class Book:
    """
    State of n family lines over the routes in `routes`.

    V0      dict route -> initial value of that route (share x V0), scalar or length n. 'Cv' is added
            automatically (value = that of C, no units) when has_cv.
    alpha0  dict {'C': .., 'D': ..} initial declared ratios (default 1).
    inc_allow  external income available to the WDT per year at t = 0 (income_cap x income_ratio x V0), grows with idx.
    paid, refunded, lost_refund  the cumulative payer record per line (see the module docstring).
    """

    def __init__(self, n, V0, alpha0=None, has_cv=False, b_mode='sale', c_cap='units', verify_down='allow',
                 r_def=0.0, inc_allow=0.0):
        if b_mode not in B_MODES:
            raise ValueError(f'b_mode must be one of {B_MODES}, got {b_mode!r}')
        if c_cap not in C_CAPS:
            raise ValueError(f'c_cap must be one of {C_CAPS}, got {c_cap!r}')
        if verify_down not in ('allow', 'reset'):
            raise ValueError(f"verify_down must be 'allow' or 'reset', got {verify_down!r}")
        if r_def <= -1.0:
            raise ValueError(f'r_def must be > -1, got {r_def!r}')
        self.n = n
        base = [r for r in ROUTES[:4] if r in V0 and np.any(np.asarray(V0[r]) > 0.0)]
        if not base:
            raise ValueError('no route has a positive value')
        if has_cv and 'C' not in base:
            raise ValueError('verification needs Route C')
        self.routes = base + (['Cv'] if has_cv else [])
        self.b_mode, self.c_cap, self.verify_down = b_mode, c_cap, verify_down
        self.r_def = float(r_def)
        self.inc_allow = _arr(inc_allow, n)
        a0 = {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0, 'Cv': 1.0}
        a0.update(alpha0 or {})
        self.R = {}
        for r in self.routes:
            if r == 'Cv':
                v0 = _arr(V0['C'], n)
                self.R[r] = dict(V=v0, f=np.zeros(n), s=np.zeros(n), sold=np.zeros(n), tot=np.zeros(n),
                                 dd=v0.copy(), Wp=np.zeros(n), ppu=v0.copy())
                continue
            v0 = _arr(V0[r], n)
            dd = _arr(a0[r], n) * v0
            self.R[r] = dict(V=v0, f=np.ones(n), s=np.zeros(n), sold=np.zeros(n), tot=np.ones(n),
                             dd=dd, Wp=dd.copy(), ppu=dd.copy())
        z = lambda: np.zeros(n)
        self.E_cash, self.A_D, self.EC = z(), z(), z()
        self.uo = {'C': z(), 'Cv': z()}
        self.LB, self.LBp = z(), z()
        self.inc_left, self.inc_paid, self.inc_total = z(), z(), z()
        self.state_cash = z()
        self.lost_refund, self.unpaid_D, self.unpaid_B = z(), z(), z()
        self.paid, self.refunded = z(), z()
        self.ledger = None                 # household arm (120c): per line, the state's stake by class, kept by revenue.run_lines; None (the legacy arm) leaves the stake as units
        self.pen, self.penp = z(), z()     # the pension: a class balance in the assessed base, never a unit (it is not sold), and its value at the last assessment
        self.vD = z()                      # share of Route D already auctioned at the true price (hazard lam_D)
        self.cap_cb = None                 # household arm (133c): a callback (book, excess) that carries the tax a route cannot pay as a lien; None (the default) records it in unpaid_B

    # ── readouts ─────────────────────────────────────────────
    def family_true(self):
        return sum(x['f'] * x['V'] for x in self.R.values())

    def state_true(self):
        return sum(x['s'] * x['V'] for x in self.R.values()) + self.state_cash if self.ledger is None else sum(self.ledger.values())

    def declared(self):
        return {r: x['f'] * x['dd'] for r, x in self.R.items()}

    def check(self):
        """Worst-case invariant errors (should all be ~0 / non-negative)."""
        out = {'units': 0.0, 'min_E_cash': float(self.E_cash.min()), 'min_A_D': float(self.A_D.min()),
               'min_EC': float(self.EC.min()), 'min_state_units': 0.0, 'min_uo': 0.0, 'uo_excess': 0.0}
        for r, x in self.R.items():
            out['units'] = max(out['units'], float(np.abs(x['f'] + x['s'] + x['sold'] - x['tot']).max()))
            out['min_state_units'] = min(out['min_state_units'], float(x['s'].min()))
        for r in _INK:
            if r in self.R:
                out['min_uo'] = min(out['min_uo'], float(self.uo[r].min()))
                out['uo_excess'] = max(out['uo_excess'], float((self.uo[r] - self.R[r]['s']).max()))
        return out


# ─────────────────────────────────────────────────────────────
# PRIMITIVES
# ─────────────────────────────────────────────────────────────

def _move(book, fl, r, units):
    """units > 0 family -> state, < 0 state -> family. Records value and units. Returns true value moved."""
    x = book.R[r]
    x['f'] = x['f'] - units
    x['s'] = x['s'] + units
    val = units * x['V']
    fl.add(r, value=val, units=units)
    return val


def _credit(book, fl, r, c):
    """Record credited pounds c (+ tax reaching the state, - refund paid back) in the flow and the payer record."""
    fl.add(r, credited=c)
    book.paid = book.paid + np.maximum(c, 0.0)
    book.refunded = book.refunded + np.maximum(-c, 0.0)


def _refund_cash(book, fl, r, rest):
    """Refund `rest` (>= 0) to the family in units at the true price: capped by the pooled cash envelope and the state's stake."""
    x = book.R[r]
    stake = x['s'] * x['V']
    if book.ledger is not None:                                                    # the ledger's value of the route's stake: the route's share of the state's units value (120c)
        tot = sum(y['s'] * y['V'] for y in book.R.values())
        stake = np.where(tot > 0, sum(book.ledger.values()) * stake / np.where(tot > 0, tot, 1.0), 0.0)
    val = np.minimum(np.minimum(rest, book.E_cash), stake)
    book.lost_refund = book.lost_refund + (rest - val)
    u = _div(val, x['V'])
    _move(book, fl, r, -u)
    book.E_cash = book.E_cash - val
    _credit(book, fl, r, -val)


def _cap(book, Lp, hold):
    """A payment Lp (credited pounds) capped at what the line holds on its route; the excess beyond 1e-9 is recorded in unpaid_B, never raised, or, when the hook supplies `book.cap_cb`, handed to it (133c). Returns the payment."""
    pay = np.where(Lp > hold + 1e-9, np.maximum(hold, 0.0), Lp)
    if book.cap_cb is None:
        book.unpaid_B = book.unpaid_B + (Lp - pay)
    else:
        book.cap_cb(book, Lp - pay)
    return pay


def shortfall_lines(book):
    """How many lines have a payment shortfall (unpaid_B > 0): a tax the line could not pay from its non-pension wealth. Zero when the model is right."""
    return int(np.count_nonzero(book.unpaid_B > 0.0))


def _route_tax(book, fl, r, Lr):
    """Settle route r's share Lr of the year's tax (+) or refund (-)."""
    x = book.R[r]
    Lp = np.where(Lr > 0.0, Lr, 0.0)
    Ln = np.where(Lr < 0.0, -Lr, 0.0)
    if r == 'B' and book.b_mode == 'lien':
        book.LB = book.LB + Lp
        red = np.minimum(Ln, book.LB)
        book.LB = book.LB - red
        _refund_cash(book, fl, r, Ln - red)
    elif r == 'B' and book.b_mode == 'income':
        pay = np.minimum(Lp, book.inc_left)
        book.inc_left = book.inc_left - pay
        book.inc_paid = book.inc_paid + pay
        book.inc_total = book.inc_total + pay
        book.paid = book.paid + pay
        fl.income = fl.income + pay
        short = _cap(book, Lp - pay, x['f'] * x['V'])
        _move(book, fl, r, _div(short, x['V']))
        book.E_cash = book.E_cash + short
        _credit(book, fl, r, short)
        ret = np.minimum(Ln, book.inc_paid)
        fl.income = fl.income - ret
        book.inc_paid = book.inc_paid - ret
        book.refunded = book.refunded + ret
        _refund_cash(book, fl, r, Ln - ret)
    elif r in ('A', 'B'):
        Lp = _cap(book, Lp, x['f'] * x['V'])
        _move(book, fl, r, _div(Lp, x['V']))
        book.E_cash = book.E_cash + Lp
        _credit(book, fl, r, Lp)
        _refund_cash(book, fl, r, Ln)
    elif r in _INK:
        Lp = _cap(book, Lp, x['f'] * x['dd'])
        u_pay = _div(Lp, x['dd'])
        val = _move(book, fl, r, u_pay)
        book.uo[r] = book.uo[r] + u_pay
        book.EC = book.EC + val
        _credit(book, fl, r, Lp)
        cap_u = _div(book.EC, x['V']) if book.c_cap == 'units_and_value' else np.full(book.n, np.inf)
        u_ref = np.minimum(np.minimum(_div(Ln, x['dd']), book.uo[r]), np.minimum(x['s'], cap_u))
        u_ref = np.maximum(u_ref, 0.0)
        book.lost_refund = book.lost_refund + (Ln - u_ref * x['dd'])
        val = _move(book, fl, r, -u_ref)
        book.uo[r] = book.uo[r] - u_ref
        book.EC = book.EC + val
        _credit(book, fl, r, -u_ref * x['dd'])
    else:  # D: liability accrues; a refund cancels it first
        book.A_D = book.A_D + Lp
        red = np.minimum(Ln, book.A_D)
        book.A_D = book.A_D - red
        _refund_cash(book, fl, r, Ln - red)


# ─────────────────────────────────────────────────────────────
# THE ASSESSMENT
# ─────────────────────────────────────────────────────────────

def assess(book, rate_fn, idx, Wn=None, Wp=None):
    """
    One assessment on TOTAL declared wealth (D7), then the tax / refund is allocated across routes by the
    positive-delta (tax) or negative-delta (refund) shares (D21). L = rate x delta for either sign: a loss is
    refunded at tau x loss (C1 item 9), capped by what was paid (per route, in _route_tax).

    Wn, Wp   dict route -> declared value now / at the last assessment (default: f x dd, and the stored Wp). The pension (`book.pen`, `book.penp`) is added to W_new and W_prev.
    Returns Flows with rate, delta and L (+ tax, - refund) per line. Does NOT rebase: call rebase() after
    (the post-settlement basis).
    """
    R, n = book.R, book.n
    Wn = Wn if Wn is not None else {r: R[r]['f'] * R[r]['dd'] for r in book.routes}
    Wp = Wp if Wp is not None else {r: R[r]['Wp'].copy() for r in book.routes}
    lien = book.b_mode == 'lien' and 'B' in R
    adj_n = book.LB if lien else 0.0
    adj_p = book.LBp if lien else 0.0
    W_new = np.maximum(sum(Wn[r] for r in book.routes) + book.pen - adj_n, 0.0)
    W_prev = np.maximum(sum(Wp[r] for r in book.routes) + book.penp - adj_p, 0.0)
    rate = np.asarray(rate_fn(W_new / idx), dtype=float)
    delta = W_new - W_prev
    d = {r: Wn[r] - Wp[r] for r in book.routes}
    if lien:
        d['B'] = d['B'] - (adj_n - adj_p)
    up = delta > 0.0
    down = delta < 0.0
    L = rate * delta
    w = {r: np.where(up, np.maximum(d[r], 0.0), np.where(down, np.maximum(-d[r], 0.0), 0.0)) for r in book.routes}
    tot = sum(w.values())
    fb = (tot <= 0.0) & (delta != 0.0) & ((book.pen != 0.0) | (book.penp != 0.0))     # the pension moved the base and no route did: settle by route value shares
    if np.any(fb):
        w = {r: np.where(fb, np.maximum(Wn[r], 0.0), w[r]) for r in book.routes}
        tot = sum(w.values())
    fl = Flows(n, rate=rate, delta=delta, L=L)
    for r in book.routes:                           # ROUTES order: pooled E_cash / EC depend on it
        Lr = L * _div(w[r], tot)
        if np.any(Lr != 0.0):
            _route_tax(book, fl, r, Lr)
    book.LBp = book.LB.copy()
    book.state_cash = book.state_cash + fl.income
    return fl


def rebase(book):
    """Post-settlement basis: the last declared value becomes f x dd."""
    for x in book.R.values():
        x['Wp'] = x['f'] * x['dd']
        x['ppu'] = x['dd'].copy()
    book.penp = book.pen.copy()


# ─────────────────────────────────────────────────────────────
# YEARLY OPERATIONS
# ─────────────────────────────────────────────────────────────

def grow_and_consume(book, g, consumption, share=None):
    """Growth of every route at g (scalar or per line), then consumption (units sold). `share`, when given, is the signed flow share x of the family's
    units in place of `consumption` (c = -x): a negative x sells units as consumption does, a positive x buys units (sold falls). Returns Flows with
    growth_family / growth_state / consumed (true values)."""
    fl = Flows(book.n)
    g = _arr(g, book.n)
    c = _arr(consumption, book.n) if share is None else -_arr(share, book.n)
    for r in book.routes:
        x = book.R[r]
        Vn = x['V'] * (1.0 + g)
        fl.growth_family[r] = x['f'] * (Vn - x['V'])
        fl.growth_state[r] = x['s'] * (Vn - x['V'])
        x['V'] = Vn
        cu = x['f'] * c
        fl.consumed[r] = cu * Vn
        x['f'] = x['f'] - cu
        x['sold'] = x['sold'] + cu
    return fl


def declare(book, alpha_C, alpha_D, lam_D=0.0, reset_D=False):
    """
    Set the declared price per unit of each route for this year. A, B, Cv at the true price; C at alpha_C x V;
    D at alpha_D x V, except that a share vD has been auctioned at the true price (hazard lam_D) and that a
    reset year declares the true price. Returns D_excl (the auction correction) per line.
    """
    n = book.n
    for r in book.routes:
        x = book.R[r]
        if r == 'D':
            continue
        a = _arr(alpha_C, n) if r == 'C' else 1.0
        x['dd'] = a * x['V']
    D_excl = np.zeros(n)
    if 'D' in book.R:
        x = book.R['D']
        aD = _arr(alpha_D, n)
        v_prev = book.vD
        v_new = 1.0 - (1.0 - lam_D) * (1.0 - v_prev)
        dd_nr = x['V'] * (1.0 + (aD - 1.0) * (1.0 - v_prev))
        dd_act = x['V'].copy() if reset_D else x['V'] * (1.0 + (aD - 1.0) * (1.0 - v_new))
        x['dd'] = dd_act
        D_excl = x['f'] * (dd_act - dd_nr)
        book.vD = v_new
    return D_excl


def verify_C(book, lam):
    """
    Expected-value verification of Route C (D6): a share lam of the unverified C units, the family's and the
    state's, moves to the verified tranche Cv, declared at the true price. The prior declared value and the
    units paid move with the units, so the correction shows up as a delta in the next assessment.
    With verify_down = 'reset', correcting an own overstatement carries no write-down credit for the price excess.
    Returns Flows with verify_family / verify_state (units moved).
    """
    C, Cv = book.R['C'], book.R['Cv']
    lam = _arr(lam, book.n)
    mf, ms = lam * C['f'], lam * C['s']
    C['f'] = C['f'] - mf
    C['s'] = C['s'] - ms
    Cv['f'] = Cv['f'] + mf
    Cv['s'] = Cv['s'] + ms
    C['tot'] = C['tot'] - (mf + ms)
    Cv['tot'] = Cv['tot'] + (mf + ms)
    moved_wp = lam * C['Wp']
    C['Wp'] = C['Wp'] - moved_wp
    adj = moved_wp
    if book.verify_down == 'reset':
        adj = moved_wp - mf * np.maximum(0.0, C['ppu'] - C['V'])
    Cv['Wp'] = Cv['Wp'] + adj
    moved_uo = lam * book.uo['C']
    book.uo['C'] = book.uo['C'] - moved_uo
    book.uo['Cv'] = book.uo['Cv'] + moved_uo
    fl = Flows(book.n)
    fl.verify_family, fl.verify_state = mf, ms
    return fl


def verified_share(book):
    """Share of Route C units (family and state) that has moved to the verified tranche."""
    if 'Cv' not in book.R:
        return np.zeros(book.n)
    C, Cv = book.R['C'], book.R['Cv']
    tot = C['f'] + C['s'] + Cv['f'] + Cv['s']
    return _div(Cv['f'] + Cv['s'], tot)


def settle_D(book, in_kind_declared=False):
    """Settle accrued Route D liability in units, at the true price (or the declared price). Returns Flows."""
    fl = Flows(book.n)
    if 'D' not in book.R:
        return fl
    x = book.R['D']
    price = x['dd'] if in_kind_declared else x['V']
    units = np.minimum(_div(book.A_D, price), x['f'])
    units = np.where(book.A_D > 0.0, units, 0.0)
    val = _move(book, fl, 'D', units)
    cred = units * price
    book.E_cash = book.E_cash + val
    book.unpaid_D = book.unpaid_D + np.where(book.A_D > 0.0, book.A_D - cred, 0.0)
    book.A_D = np.zeros(book.n)
    _credit(book, fl, 'D', cred)
    return fl


def settle_B(book):
    """Lien mode: settle the deferred balance by selling Route B units at the true price (death, horizon)."""
    fl = Flows(book.n)
    if 'B' not in book.R or book.b_mode != 'lien':
        book.LBp = book.LB.copy()
        return fl
    x = book.R['B']
    has = book.LB > 0.0
    units = np.where(has, np.minimum(_div(book.LB, x['V']), x['f']), 0.0)
    val = _move(book, fl, 'B', units)
    book.E_cash = book.E_cash + val
    book.unpaid_B = book.unpaid_B + np.where(has, book.LB - val, 0.0)
    _credit(book, fl, 'B', val)
    book.LB = np.zeros(book.n)
    book.LBp = np.zeros(book.n)
    return fl


# ─────────────────────────────────────────────────────────────
# A FULL YEAR AND A DEATH
# ─────────────────────────────────────────────────────────────

def step_year(book, rate_fn, idx, g, consumption, alpha_C=1.0, alpha_D=1.0, lam_C=0.0, lam_D=0.0, reset_D=False, hook=None, t=0):
    """
    One holding year. Returns a list of (kind, Flows): 'growth' (growth_family / growth_state / consumed),
    'verify', 'tax', 'reset_D'. idx is the index factor (1 + index_rate)^t for W_min and k.
    `hook` (None: the legacy kernel, growth g and consumption share `consumption`) is an object with pre(book, t, g) -> (g_N, x), the growth rate
    and the signed flow share the year uses, and post(book, fl), called with the year's assessment after settlement (kernel-wiring-design 3.2).
    """
    ops, share = [], None
    if hook is not None:
        g, share = hook.pre(book, t, g)
    book.LB = book.LB * (1.0 + book.r_def)                     # deferred balance accrues (lien)
    book.inc_left = book.inc_allow * idx                       # this year's income available to the WDT (income)
    ops.append(('growth', grow_and_consume(book, g, consumption, share)))
    D_excl = declare(book, alpha_C, alpha_D, lam_D, reset_D)
    if 'Cv' in book.R:
        ops.append(('verify', verify_C(book, lam_C)))
    Wn = book.declared()
    Wp = {r: book.R[r]['Wp'].copy() for r in book.routes}
    if book.verify_down == 'reset' and 'D' in book.R:
        m = (D_excl < 0.0) & (Wn['D'] < Wp['D'])
        Wp['D'] = np.where(m, Wp['D'] + np.maximum(D_excl, Wn['D'] - Wp['D']), Wp['D'])
    fl = assess(book, rate_fn, idx, Wn, Wp)
    ops.append(('tax', fl))
    rebase(book)
    if hook is not None:
        hook.post(book, fl)
    if reset_D:
        ops.append(('reset_D', settle_D(book)))
        if 'D' in book.R:                                      # a reset sells units: re-base Route D
            x = book.R['D']
            x['Wp'] = x['f'] * x['dd']
    return ops


def step_death(book, rate_fn, idx, death_verify=False):
    """
    Death of the holder, after the year's assessment. Death verifies Route C with certainty (D6) and holds a
    corrective auction on Route D (declared price -> true price); accrued D and any deferred B balance are
    settled; the heir starts with clean envelopes (C1 item 10) and is taxed on the receipt as a delta from zero.
    The cumulative payer record is kept. Returns a list of (kind, Flows).
    """
    ops = []
    n = book.n
    if death_verify and 'Cv' in book.R:
        ops.append(('verify_death', verify_C(book, 1.0)))
        ops.append(('tax_death_C', assess(book, rate_fn, idx)))
        rebase(book)
    if 'D' in book.R:
        x = book.R['D']
        dd_old = x['dd'].copy()
        x['dd'] = x['V'].copy()                                # the death auction reveals the true price
        Wn2 = book.declared()
        Wp2 = {r: book.R[r]['Wp'].copy() for r in book.routes}
        if book.verify_down == 'reset':
            m = Wn2['D'] < Wp2['D']
            Wp2['D'] = np.where(m, Wp2['D'] + np.maximum(x['f'] * (x['dd'] - dd_old), Wn2['D'] - Wp2['D']), Wp2['D'])
        ops.append(('tax_death', assess(book, rate_fn, idx, Wn2, Wp2)))
        rebase(book)
        ops.append(('death_D', settle_D(book)))
    ops.append(('death_B', settle_B(book)))
    book.uo = {'C': np.zeros(n), 'Cv': np.zeros(n)}
    book.EC = np.zeros(n)
    book.E_cash = np.zeros(n)
    book.inc_paid = np.zeros(n)                                # the heir: clean income envelope, a full year's income
    book.inc_left = book.inc_allow * idx
    Wn = book.declared()
    ops.append(('tax_heir', assess(book, rate_fn, idx, Wn, {r: np.zeros(n) for r in book.routes})))
    rebase(book)                                               # post-heir-tax basis
    return ops


def settle_terminal(book):
    """End of the horizon: settle Route D at the true price and the deferred B balance. Returns (kind, Flows) list."""
    return [('terminal_D', settle_D(book)), ('terminal_B', settle_B(book))]


# ─────────────────────────────────────────────────────────────
# DRIVER
# ─────────────────────────────────────────────────────────────

def run_lines(rate_fn, g_mat, V0, G=None, consumption=0.0, index_rate=0.0, alpha_C=1.0, alpha_D=1.0,
              lam_C=0.0, lam_D=0.0, death_verify=False, reset_years=(), n=None, collect=False, hook=None, **book_kw):
    """
    Run n lines over T years with deaths at G, 2G, ... < T. g_mat is the (T, n) growth matrix: row t - 1 is
    year t for every line. A (T,) or (T, 1) series is shared by all lines. alpha_C / alpha_D are numbers (or
    length-n arrays), or callables f(t, gen, yrs_to_death) -> number / array (the strategy hook). reset_years:
    years in which Route D is voluntarily reset. hook: see step_year (None, the legacy kernel). Returns the Book (and the list of (t, kind, Flows) if collect).
    """
    g_mat = np.asarray(g_mat, dtype=float)
    if g_mat.ndim == 1:
        g_mat = g_mat[:, None]
    if g_mat.ndim != 2:
        raise ValueError(f'g_mat must have shape (T, n), got {g_mat.shape}')
    T = g_mat.shape[0]
    n = n or max([np.size(v) for v in V0.values()] + [g_mat.shape[1]])
    if g_mat.shape[1] not in (1, n):
        raise ValueError(f'g_mat has {g_mat.shape[1]} columns for {n} lines')
    has_cv = (lam_C > 0.0 or death_verify) and 'C' in V0 and np.any(np.asarray(V0['C']) > 0.0)
    a0 = {'C': alpha_C(0, 0, T) if callable(alpha_C) else alpha_C,
          'D': alpha_D(0, 0, T) if callable(alpha_D) else alpha_D}
    book = Book(n, V0, alpha0=a0, has_cv=has_cv, **book_kw)
    log, gen = [], 0
    for t in range(1, T + 1):
        idx = (1.0 + index_rate) ** t
        if G:
            nd = -(-t // G) * G
            to_death = (nd - t) if nd < T else (T - t)
        else:
            to_death = T - t
        aC = alpha_C(t, gen, to_death) if callable(alpha_C) else alpha_C
        aD = alpha_D(t, gen, to_death) if callable(alpha_D) else alpha_D
        ops = step_year(book, rate_fn, idx, g_mat[t - 1], consumption, aC, aD, lam_C, lam_D, t in reset_years, hook, t)
        if collect:
            log += [(t, k, f) for k, f in ops]
        if G and t % G == 0 and t < T:
            gen += 1
            ops = step_death(book, rate_fn, idx, death_verify)
            if collect:
                log += [(t, k, f) for k, f in ops]
    ops = settle_terminal(book)
    if collect:
        log += [(T, k, f) for k, f in ops]
        return book, log
    return book
