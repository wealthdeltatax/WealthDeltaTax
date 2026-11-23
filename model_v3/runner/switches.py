"""
switches.py -- the household arm's labelled scenario switches (model v3, brief 138c)
=====================================================================================
Layer 3.6: numpy only; `arm.build` calls it. A switch is a scenario axis, never a central case, and its default leaves every output as it was. The arm dict names the setting.

`fund_return`: what the public fund earns. `safe` (default) is the household arm's stand-in, the net financial class return (a low case, no register row); `market` credits every class of the fund, and the
levy's safe share, at the year's market return of the path (the legacy arm's fund return), so P6, M1c and the long M1 net read as a range across both settings.
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
