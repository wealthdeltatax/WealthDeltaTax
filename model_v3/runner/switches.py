"""
switches.py -- the household arm's labelled scenario switches (model v3, brief 138c)
=====================================================================================
Layer 3.6: numpy only; `arm.build` calls it. A switch is a scenario axis, never a central case, and its default leaves every output as it was. The arm dict names the setting.

`fund_return`: what the public fund earns. `safe` (default) is the household arm's stand-in, the net financial class return (a low case, no register row); `market` credits every class of the fund, and the
levy's safe share, at the year's market return of the path (the legacy arm's fund return), so P6, M1c and the long M1 net read as a range across both settings.

Brief 139c adds the register-read scenario values (all (J) rows, `inputs.md`): `lien_rate` (I-D1m, the one real deferral rate of the pension lien and the Route B lien; `low` 0, `central` 2 (default), `high` 3 % real), `pension_basis`
(I-D1n, the multiplier on the opening pension stock; `ons` 1.00 = the pack (default), `ifs` the row's central, `ifs_high` its high), and the household arm's 10 death phases (a numerical approximation, not a row; the legacy arm keeps 6).
The housing gain is read from I-D1o (central) in `arm.household_inputs`. `scenario` states each in the run record.
"""
import numpy as np

FUND = ('safe', 'market')
MARKET_LABEL = "the path's market return, like the legacy arm (a labelled scenario value: the fund_return axis, the high case)"


def fund_return(a):
    """The fund_return of an arm dict, checked."""
    v = a.get('fund_return', 'safe')
    if v not in FUND:
        raise ValueError(f"fund_return must be one of {FUND}, not {v!r}")
    return v


def fund(a, safe, label, g=None):
    """(safe, label) of the arm under its fund_return: `safe` is the household stand-in series function and `label` the run record; `market` replaces the safe series by the market return `g` (T, P) and says so in the label."""
    if fund_return(a) == 'safe' or g is None:
        return safe, label
    return (lambda T, P: np.asarray(g, float)[:T]), {**label, 'safe_return': MARKET_LABEL, 'scenario': {**label['scenario'], 'fund_return': 'market'}}


def hook(a, cls):
    """The hook class of the arm: `cls` itself under `safe`; under `market` a subclass that keeps each year's market return `g` (per line) of its book and gives it as the ledger's class returns (the household's own balances keep the scenario class returns)."""
    if fund_return(a) == 'safe':
        return cls

    class MarketFund(cls):
        def pre(self, book, t, g):
            self.mk = [] if book is not self.book else self.mk
            self.mk.append(np.asarray(g, float))
            return super().pre(book, t, g)

        def class_returns(self):
            return {k: self.mk[-1] for k in ('property', 'net_financial', 'physical')}

        def class_paths(self, T, P):
            m = np.array(self.mk)[:, ::len(self.st['income'])]
            return {k: m for k in ('property', 'net_financial', 'physical')}

    return MarketFund


TAIL = {'off': None, 'ast_low': (14.4, False), 'ast_high': (16.5, False), 'ast_low_e0': (14.4, True), 'ast_high_e0': (16.5, True)}   # top_tail (147c): the published top-1% share in percent (Advani, Summers and Tarrant 2025, pp. 1, 12) and whether I-D4e is taken as 0
POINTS = ('low', 'central', 'high')
BASIS = {'ons': 'low', 'ifs': 'central', 'ifs_high': 'high'}
N_PHASE = 10                                                  # the household arm's death phases (149c): a numerical approximation, the legacy arm keeps 6


def _arm(arm):
    return {'arm': arm} if isinstance(arm, str) else dict(arm)


def _row(a, key, ctx, row, pts, default):
    p = a.get(key, default)
    if p not in pts:
        raise ValueError(f"{key} must be one of {tuple(pts)}, not {p!r}")
    return getattr(ctx.reg[row], pts[p] if isinstance(pts, dict) else p)


def lien_rate(a, ctx):
    """The real deferral rate (a fraction) of the arm dict `a`: the I-D1m point named by `lien_rate` (default `central`)."""
    return _row(a, 'lien_rate', ctx, 'I-D1m', POINTS, 'central') / 100


def pension_multiplier(a, ctx):
    """The multiplier on the opening pension stock: the I-D1n point named by `pension_basis` (default `ons`, 1.00)."""
    return _row(a, 'pension_basis', ctx, 'I-D1n', BASIS, 'ons')


def housing_gain(ctx):
    """The real housing holding gain (a fraction): the I-D1o central."""
    return ctx.reg['I-D1o'].central / 100


def lien_kw(ctx):
    """The book keywords the household arm adds to the run's `lam`: the lien deferral rate; none for the legacy arm."""
    a = _arm(ctx.arm)
    return dict(r_def=lien_rate(a, ctx)) if a['arm'] == 'household' else {}


def phase_kw(arm):
    """The death phases of the arm's burden and revenue runs: 10 for the household arm, none (the core default, 6) for the legacy arm."""
    return dict(n_phase=N_PHASE) if _arm(arm)['arm'] == 'household' else {}


def scenario(a, ctx, st, label, base):
    """(state, label) with the opening pension stock times the basis multiplier (1.00: unchanged), the `top_tail` stock (147c; off: unchanged) and the scenario values stated in the run record (a switch is stated only when on)."""
    m = pension_multiplier(a, ctx)
    st = st if m == 1.0 else {**st, 'pos': {**st['pos'], 'pension': st['pos']['pension'] * m}}
    st, tt = top_tail(a, ctx, st, base)
    new = dict(**(tt or {}), lien_rate=lien_rate(a, ctx), lien_rate_point=a.get('lien_rate', 'central'), pension_basis=a.get('pension_basis', 'ons'), pension_multiplier=m, housing_gain=housing_gain(ctx), death_phases=N_PHASE)
    return st, {**label, 'scenario': {**label['scenario'], **new}}


def top_tail(a, ctx, st, base):
    """(state, report) with the opening stock of D10b scaled to a published top-1% share (147c, 146r section 4): the setting of `top_tail` (default `off`: state unchanged, report None). The named-list tiers keep their stock (I-D4f); D10b loses non-pension wealth pro rata to its balances (its pension stays, capped);
    D10a gains the same non-pension wealth, so total wealth and the top-decile share are unchanged. The shares are of the arm's own opening stock (the base after the launch loss I-D5a on the payer lines, which the arm sees), not of the unshaped pack, so the moved amounts differ a little from 146r's. A `_e0` setting first takes the missing wealth (I-D4e) off D10b, so the total falls by it and the target share is of the survey total. The pack's top 1% is above the published range: the settings lower it. A labelled scenario, not fitted."""
    v = a.get('top_tail', 'off')
    if v not in TAIL:
        raise ValueError(f"top_tail must be one of {tuple(TAIL)}, not {v!r}")
    if TAIL[v] is None:
        return st, None
    share, e0 = TAIL[v][0] / 100, TAIL[v][1]
    L, n = list(base.labels), base.adults_k
    ib, ia, il = L.index('D10b'), L.index('D10a'), [L.index(x) for x in ('RL3', 'RL2', 'RL1')]
    np_, pos = ('property', 'net_financial', 'physical'), st['pos']
    W = sum(pos.values()) * n                                                                       # billions of pounds a line holds (millions per adult times thousand adults)
    T, rl = float(W.sum()), float(W[il].sum())
    s1, e = ctx.reg['I-D4d'].central / 100, ctx.reg['I-D4e'].central / 100
    drop = float((W[ib] + rl) * e / (s1 + e)) if e0 else 0.0                                         # the missing wealth in the arm's top 1% (the top 1% is I-D4d plus I-D4e of the survey total, both times the launch loss)
    T1 = T - drop
    new_b = share * T1 - rl
    to_a = float(W[ib]) - drop - new_b
    if new_b <= 0 or to_a < 0:
        raise ValueError(f"top_tail {v}: D10b would hold {new_b:.1f}bn and D10a gain {to_a:.1f}bn; the setting must lower the top-1% stock")
    mix = {k: pos[k][ib] / sum(pos[j][ib] for j in np_) for k in np_}                              # D10b's non-pension mix is D10's (the cap's displacement is pro rata to it)
    cut, add = (float(W[ib]) - new_b) / n[ib], to_a / n[ia]
    new = {k: pos[k].copy() for k in pos}
    for k in np_:
        new[k][ib] -= cut * mix[k]
        new[k][ia] += add * mix[k]
    if min(new[k][ib] for k in np_) < 0:
        raise ValueError(f"top_tail {v}: a class of D10b would go negative")
    return {**st, 'pos': new}, dict(top_tail=v, top1_share_target=share, wealth_moved_bn=to_a, wealth_removed_bn=drop, total_bn=T1)
