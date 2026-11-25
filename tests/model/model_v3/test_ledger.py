"""Brief 120c (W6): the public ledger by class ties to the household's payments per path and year, with deaths, the horizon, refunds and six phases."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, kernel as K, pack as pk, revenue as rv, schedule as S
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[3]
PACK, REG = pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
ST = arm.line_state(BASE, PACK.tables['decile_composition'], REG, 0.0101)
GAIN = dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094)
FALL = dict(GAIN, property=-0.09, net_financial=-0.06)                                       # a falling market: refunds
RATE = S.rate_function(k=0.01, tau_0=0.05, tau_m=0.50, W_min=BASE.w_min)
KS = ('property', 'net_financial', 'physical', 'safe')


class Tally(arm.HouseholdHook):
    """Adds up the value every payment moves (billions), by year: the household side of the tie."""

    def __init__(self, *a, n_phase=1, **k):
        super().__init__(*a, **k)
        self.w, self.paid, self.t = BASE.weights / n_phase, {}, 0

    def pre(self, book, t, g):
        self.t = t
        return super().pre(book, t, g)

    def _pay(self, q, T):
        self.paid[self.t] = self.paid.get(self.t, 0.0) + (self.w[None, :] * np.asarray(T, float).reshape(-1, 14)).sum(axis=1) * BASE.adults_k.sum()
        return super()._pay(q, T)


def build(years, G, n_phase, gain=GAIN, P=2, safe_share=0.3):
    h = Tally(ST, gain, 0.0157, n_phase=n_phase)
    g = np.zeros((years, P))
    run = rv.run_lines(BASE, RATE, g, np.full((years, P), 0.0157), 0.0, G=G, n_phase=n_phase, hook=h)
    return h, run, rv.revenue(run, 2000.0, 0.3, {'x': 1.0}, g, 40.0, 0.0, safe=np.full((years, P), 0.005), safe_share=safe_share)


CASES = [(9, 4, 1, GAIN), (13, 6, 6, GAIN), (13, 6, 6, FALL), (6, 5, 1, GAIN)]            # the last: a death in the year before the last


@pytest.mark.parametrize('years, G, n_phase, gain', CASES)
def test_household_payments_equal_ledger_receipts_per_path_and_year(years, G, n_phase, gain):
    h, run, o = build(years, G, n_phase, gain)
    wdt = run['tax'] + run['refund'] + run['death_tax'] + run['heir'] + run['death_B'] + run['death_D']
    rc = sum(run['ledger']['rc'].values())
    assert np.abs(rc - wdt).max() < 1e-9 and np.abs(np.array([h.paid[t] for t in range(1, years + 1)]) - wdt).max() < 1e-9 and np.abs(wdt).max() > 0
    assert np.abs(o['fund']['rc']['safe'] - 0.3 * 0.003 * run['gdp_index'] * 2000.0).max() < 1e-9 and np.abs(sum(o['fund']['rc'].values()) - (wdt + 0.003 * run['gdp_index'] * 2000.0)).max() < 1e-9


@pytest.mark.parametrize('years, G, n_phase, gain', CASES)
def test_the_ledger_identity_dL_equals_receipts_plus_return_minus_payout_by_class(years, G, n_phase, gain):
    _, run, o = build(years, G, n_phase, gain)
    f = o['fund']
    for k in KS:
        L = f['L'][k]
        dL = np.diff(np.vstack([np.zeros((1, L.shape[1])), L]), axis=0)
        assert np.abs(dL - (f['rc'][k] + f['ret'][k] - f['pay'][k])).max() < 1e-9
    assert np.abs(sum(f['L'].values()) - f['S']).max() < 1e-9 and np.abs(sum(f['pay'].values()) - f['R']).max() < 1e-9
    assert np.abs(f['L']['physical']).max() >= 0 and 'pension' not in f['L'] and 'pension' not in run['ledger']['rc']


def test_refunds_are_in_the_ledger_and_reconcile_with_the_households():
    h, run, o = build(13, 6, 6, FALL)
    assert run['refund'].min() < 0 and np.abs(sum(run['ledger']['rc'].values()) - (run['tax'] + run['refund'] + run['death_tax'] + run['heir'] + run['death_B'] + run['death_D'])).max() < 1e-9


def test_the_state_stake_reads_the_ledger_and_the_legacy_stake_is_unchanged(monkeypatch):
    books, orig = [], K.Book
    monkeypatch.setattr(K, 'Book', lambda *a, **k: books.append(orig(*a, **k)) or books[-1])
    build(9, 4, 1)
    b = books[0]
    assert np.allclose(b.state_true(), sum(b.ledger.values())) and (b.state_true() > 0).any() and all(K.shortfall_lines(x) == 0 and (x.unpaid_B == 0).all() for x in books)
    leg = orig(3, {'A': np.ones(3)})
    assert leg.ledger is None and np.array_equal(leg.state_true(), leg.state_cash)


def test_the_ledger_pays_out_pro_rata_and_the_identity_holds_when_the_fund_is_filled():
    T, P = 40, 3
    rng = np.random.default_rng(5)
    rc = {k: rng.uniform(0.5, 1.5, (T, P)) * s for k, s in zip(KS, (1.0, 2.0, 0.5, 0.5))}
    rk = {k: rng.normal(m, 0.04, (T, P)) for k, m in zip(KS, (0.02, 0.01, 0.0, 0.004))}
    f = rv.fund(sum(rc.values()), np.full((T, P), 0.3), None, ms=1.0, ml=1.0, a_window=3, led=dict(rc=rc, rk=rk))
    assert f['R'].max() > 0 and (f['fill'] > 0).all()
    for k in KS:
        L = f['L'][k]
        assert np.abs(np.diff(np.vstack([np.zeros((1, P)), L]), axis=0) - (rc[k] + f['ret'][k] - f['pay'][k])).max() < 1e-9
    assert np.abs(sum(f['pay'].values()) - f['R']).max() < 1e-9 and np.abs(sum(f['L'].values()) - f['S']).max() < 1e-9
    Sp = np.vstack([np.zeros((1, P)), f['S'][:-1]])
    assert np.abs(Sp * f['rr'] - sum(f['ret'].values())).max() < 1e-9
