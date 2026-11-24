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
"""
import numpy as np

WITHDRAWAL = ('off', 'low', 'mid', 'high')
HALF = {'D1-3': 'bottom', 'D4-5': 'bottom', 'D6-7': 'top', 'D8-9': 'top', 'D10': 'top'}                   # 145r section 4: the halves, by pack band (an assumption: halves are by total household wealth)
RATE = {'bottom': dict(low=0.0, mid=0.7, high=2.9), 'top': dict(low=0.8, mid=2.4, high=4.1)}            # % of the opening pension balance a year, retired stage, real (145r: IFS BN236, ELSA net financial wealth, pp. 11 and 13)
FLOORS = (0, 25, 50)
CLASS = 'proxy (mid and high; low in the bottom half is the zero floor, a scenario value); the not retired stage is unset and does not draw'
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
    w, f, new = withdrawal(a), heir_floor(a), {}
    if w != 'off':
        wd = line_rates(w, base, ctx.pack)
        st = {**st, 'wd': wd}
        new['pension_withdrawal'] = dict(setting=w, rates_pct={h: RATE[h][w] for h in RATE}, retired_share=retired_share(ctx.pack), evidence=CLASS,
                                         rule='a line draws the retired share of its band times the half\'s rate, of its opening pension, into net financial wealth; total wealth is unchanged; a scenario, not a forecast')
    if f:
        new['heir_floor'] = dict(pct=f, rule=HEIR)
    return st, ({**label, 'scenario': {**label['scenario'], **new}} if new else label)


def hook(a, cls):
    """`cls` itself with both switches off; else a subclass: `_year` moves the draw (the account, the identity and I1 see a transfer between classes), `settle` leaves the heir's share of the pension."""
    w, f = withdrawal(a), heir_floor(a)
    if w == 'off' and not f:
        return cls

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

    return Flow
