"""
flow_switches.py -- three labelled scenario switches on the household arm's flows (model v3, brief 148c)
=========================================================================================================
Layer 3.55: numpy only (no project import); `arm.build` calls `scenario` and `hook`. Each is a scenario axis, off by default, never a central case, and off leaves every output byte for byte as it was
(`hook` returns the class itself, `scenario` returns the state and label it was given). The arm dict names the setting. No register row (a later brief): the numbers below are named and labelled here.

`pension_withdrawal` (`off`, `low`, `mid`, `high`; 145r): each year a share of the opening pension balance moves into net financial wealth. 145r gives a rate by wealth half for the retired stage only (the
not retired stage is `unset`: no draw). The model's lines are wealth bands, not stages, so a line's rate is the retired share of its band's persons (the pack's `cell_weights`) times the half's rate: the
band's retired persons draw at the stage rate, the rest not at all (a labelled approximation: the pension is not split by stage in the pack). The draw is a transfer inside the base: total wealth is unchanged,
the pension stays in the kernel's assessed base while held (`book.pen`), the units of the non-pension routes rise by the draw. Evidence class `proxy` (a different asset, a 1920-34 cohort); `low` is a floor.

`heir_floor` (0, 25, 50, in percent of the pension; author ruling 2026-11-23): the share of the pension balance that the lien's settlement draw cannot take. The base case, 0, is the uncapped draw. The settlement
is at a death and at the horizon (the hook cannot tell them apart without a kernel change: at the horizon the lien is settled as at a death); what the floor leaves unpaid is written off, and the ledger reports it
as its `wo` (the same column as the limited-recourse write-off of 138c).

`gdp_paths` (`off`, `indep`, `hist`; 146r, author rulings 2026-11-23): per-path real GDP growth per head, `gdp_g + d` with `d` a zero-mean AR(1) (marginal SD 2.68 points, the full sample; lag-1 0.28) whose
innovation is correlated with the market return's by RHO: 0 (`indep`, "growth risk only") or 0.37 (`hist`, "growth and market risk, correlated"). Zero deviation is today's fixed growth (the mean is not moved).
Household income follows the path (saving and accrual ratios stay fixed); the property and physical gains, the saving and accrual ratios and the market process itself do not move. The comparators of M13 run on
fixed scenario rates, per line and not per path, so `arm.withheld` withholds what reads them under `gdp_paths` (as under `market_paths`); the untaxed path (`free`: M3, M12) follows the GDP path. The postwar SD
1.93 is a noted alternative, not built. `gdp` is called from `runner.evaluate`, which makes the array every core run reads (the GDP index, W_min, the household's income).
"""
import numpy as np

WITHDRAWAL = ('off', 'low', 'mid', 'high')
HALF = {'D1-3': 'bottom', 'D4-5': 'bottom', 'D6-7': 'top', 'D8-9': 'top', 'D10': 'top'}                   # 145r section 4: the halves, by pack band (an assumption: halves are by total household wealth)
RATE = {'bottom': dict(low=0.0, mid=0.7, high=2.9), 'top': dict(low=0.8, mid=2.4, high=4.1)}            # % of the opening pension balance a year, retired stage, real (145r: IFS BN236, ELSA net financial wealth, pp. 11 and 13)
FLOORS = (0, 25, 50)
CLASS = 'proxy (mid and high; low in the bottom half is the zero floor, a scenario value); the not retired stage is unset and does not draw'
GDP = ('off', 'indep', 'hist')
RHO = {'indep': 0.0, 'hist': 0.37}                                                                        # same-year correlation with the market return (146r section 5: A scenario, B derived, 95% interval 0.20 to 0.51)
SD, PHI = 0.0268, 0.28                                                                                    # marginal SD of the growth deviation (fraction; 2.68 points, 117 years, derived) and its lag-1 (SE about 0.09)
MARKET = ('I-D1a', 'I-D1b', 'I-D1b2')                                                                     # the market process's mean and sd (percent) and lag-1: runner.RET (the runner is above this layer)
GDP_LABEL = {'indep': 'growth risk only', 'hist': 'growth and market risk, correlated'}
NONPEN = ('property', 'net_financial', 'physical', 'pension')
HEIR = 'the lien settlement draw at a death and at the horizon cannot take this share of the pension; the rest is written off and reported in the ledger (wo)'


def withdrawal(a):
    v = a.get('pension_withdrawal', 'off')
    if v not in WITHDRAWAL:
        raise ValueError(f"pension_withdrawal must be one of {WITHDRAWAL}, not {v!r}")
    return v


def heir_floor(a):
    v = a.get('heir_floor', 0)
    if v not in FLOORS:
        raise ValueError(f"heir_floor must be one of {FLOORS} (percent), not {v!r}")
    return v


def gdp_paths(a):
    v = a.get('gdp_paths', 'off')
    if v not in GDP:
        raise ValueError(f"gdp_paths must be one of {GDP}, not {v!r}")
    return v


def gdp(arm, theta, g, gdp_g, rng):
    """The (T, P) GDP-per-head growth of a run on the market paths `g` (T, P): `gdp_g` itself when `gdp_paths` is off (the same array, nothing moves), else `gdp_g + SD x`, with x a standard AR(1)
    (lag-1 PHI, stationary start) whose innovation is RHO times the market's (recovered from `g` at the draw's market mean, sd and lag-1, the recursion of `runner.paths`) plus an independent one from `rng('gdp_paths')`."""
    v = gdp_paths({'gdp_paths': 'off'} if isinstance(arm, str) else arm)
    if v == 'off':
        return gdp_g
    g, rho = np.asarray(g, float), RHO[v]
    w = np.sqrt(1 - rho * rho) * rng('gdp_paths').standard_normal(g.shape)
    if rho:
        m, sd, phi = (theta[i] for i in MARKET)
        x = (100 * g - m) / sd
        w = w + rho * np.concatenate([x[:1], (x[1:] - phi * x[:-1]) / np.sqrt(1 - phi * phi)])
    x = np.empty_like(w)
    x[0] = w[0]
    for t in range(1, len(w)):
        x[t] = PHI * x[t - 1] + np.sqrt(1 - PHI * PHI) * w[t]
    out = np.asarray(gdp_g, float) + SD * x
    if np.any(out <= -1.0):
        raise ValueError('gdp_paths: a path\'s growth is at or below -100%')
    return out


def retired_share(pack):
    """{band: share of the band's persons who are retired} from the pack's `cell_weights` (person-based proxy)."""
    n = {(r['band'], r['stage']): r['persons'] for r in pack.tables['cell_weights']}
    return {b: n[b, 'retired'] / (n[b, 'retired'] + n[b, 'not retired']) for b in HALF}


def line_rates(point, base, pack):
    """The share of the opening pension a line draws each year (fraction): the retired share of its band times the half's rate at `point`; D1 to D3 take band D1-3 (the base leaves their band empty), tail lines D10."""
    sh = retired_share(pack)
    return np.array([sh[b] * RATE[HALF[b]][point] / 100 for b in (x or 'D1-3' for x in base.band)])


def scenario(a, ctx, st, label, base):
    """(state, label) with the withdrawal rate by line in `st['wd']` (setting on) and both switches stated in the run record when on (a switch is stated only when on)."""
    w, f, new, v = withdrawal(a), heir_floor(a), {}, gdp_paths(a)
    if w != 'off':
        wd = line_rates(w, base, ctx.pack)
        st = {**st, 'wd': wd}
        new['pension_withdrawal'] = dict(setting=w, rates_pct={h: RATE[h][w] for h in RATE}, retired_share=retired_share(ctx.pack), evidence=CLASS,
                                         rule='a line draws the retired share of its band times the half\'s rate, of its opening pension, into net financial wealth; total wealth is unchanged; a scenario, not a forecast')
    if f:
        new['heir_floor'] = dict(pct=f, rule=HEIR)
    if v != 'off':
        new['gdp_paths'] = dict(setting=v, label=GDP_LABEL[v], mean='the pack constant (not moved)', sd_pts=100 * SD, lag1=PHI, corr_market=RHO[v], evidence='derived from one country\'s history (146r); not a forecast',
                                rule='household income follows the path; saving and accrual ratios, property and physical gains and the market process are unchanged; the M13 comparators stay on fixed rates and are withheld')
    return st, ({**label, 'scenario': {**label['scenario'], **new}} if new else label)


def hook(a, cls, gdp_g=None, returns=None):
    """`cls` itself with all three switches off; else a subclass: `_year` moves the pension draw (the account, the identity and I1 see a transfer between classes), `settle` leaves the heir's share of the pension,
    and with `gdp_paths` `pre` and `free` take the household's income along the path `gdp_g` (T, P) (`returns`: arm.returns, passed because this layer cannot import arm). An arm built without `gdp_g` (the comparators' and the statics' `env.arm`) keeps the fixed income growth."""
    w, f, v = withdrawal(a), heir_floor(a), gdp_paths(a)
    if w == 'off' and not f and v == 'off':
        return cls
    Y = None if v == 'off' or gdp_g is None else np.cumprod(1.0 + np.asarray(gdp_g, float), axis=0)

    class Flow(cls):
        keep = f / 100

        def _rates(self, like):
            wd = self.st.get('wd')
            if wd is None:
                return 0.0
            like = np.asarray(like)
            return wd[:, None] if like.ndim == 2 else np.tile(wd, like.size // wd.size)

        def _year(self, q, inc, sav, acc, gn):
            q1, acct = super()._year(q, inc, sav, acc, gn)
            d = self._rates(q['pension']) * np.maximum(q['pension'], 0.0)
            if np.any(d):
                q1 = {**q1, 'pension': q1['pension'] - d, 'net_financial': q1['net_financial'] + d}
            if q is self.q:
                self.drawn = d
            return q1, acct

        def account(self):
            a = super().account()
            return {**a, 'withdrawn': np.asarray(getattr(self, 'drawn', 0.0)) * np.ones_like(a['S'])} if w != 'off' else a

        def _ix(self, k):
            """The GDP index after k years, per path (the income's growth factor)."""
            return np.ones(Y.shape[1]) if k <= 0 else Y[k - 1]

        def pre(self, book, t, g):
            if Y is None:
                return super().pre(book, t, g)
            f_ = np.repeat(self._ix(t - 1), len(self.st['income']))                                    # the kernel folds a path's lines side by side
            if f_.size != book.n:
                raise ValueError(f'gdp_paths: the growth array has {Y.shape[1]} paths, the book {book.n} lines')
            g0, self.gr = self.gr, f_ ** (1.0 / max(t - 1, 1)) - 1.0                                   # (1 + gr) ** (t - 1) is the path's index at t - 1
            try:
                return super().pre(book, t, g)
            finally:
                self.gr = g0

        def free(self, g):
            if Y is None:
                return super().free(g)
            L, P = len(self.st['income']), np.shape(g)[1]
            q = {**{k: np.repeat(np.asarray(v_, float)[:, None], P, 1) for k, v_ in self.st['pos'].items()}, 'debt': np.zeros((L, P))}
            out = []
            for t in range(len(g)):
                q1, _ = self._year(q, self.st['income'][:, None] * self._ix(t)[None, :], self.st['sav'][:, None], self.st['acc'][:, None], returns(q, self._gn(g[t])))
                w0, w1 = (sum(x[k] for k in NONPEN) for x in (q, q1))
                out, q = out + [np.where(w0 != 0, w1 / np.where(w0 != 0, w0, 1.0), 1.0)], q1
            return np.array(out)

    return Flow
