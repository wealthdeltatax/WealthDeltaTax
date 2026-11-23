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


def scenario(a, ctx, st, label):
    """(state, label) with the opening pension stock times the basis multiplier (1.00: unchanged) and the scenario values stated in the run record."""
    m = pension_multiplier(a, ctx)
    st = st if m == 1.0 else {**st, 'pos': {**st['pos'], 'pension': st['pos']['pension'] * m}}
    new = dict(lien_rate=lien_rate(a, ctx), lien_rate_point=a.get('lien_rate', 'central'), pension_basis=a.get('pension_basis', 'ons'), pension_multiplier=m, housing_gain=housing_gain(ctx), death_phases=N_PHASE)
    return st, {**label, 'scenario': {**label['scenario'], **new}}
