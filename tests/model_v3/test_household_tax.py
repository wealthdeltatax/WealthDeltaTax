"""Brief 118c (W5b): the taxed household hook. The value the kernel moves to the state is paid from the non-pension classes (block 1); deaths and the horizon (block 2)."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, kernel as K, pack as pk, revenue as rv, schedule as S
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[2]
PACK, REG = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
ST = arm.line_state(BASE, PACK.tables['decile_composition'], REG, 0.0101)
GAIN = dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094)
RATE = S.rate_function(k=0.01, tau_0=0.05, tau_m=0.50, W_min=BASE.w_min)


def book_for(st, paths=1, **kw):
    tot = np.tile(sum(st['pos'].values()), paths)
    return K.Book(paths * 14, {'A': 0.4 * tot, 'B': 0.3 * tot, 'D': 0.3 * tot}, **kw)


def run(hook, years, paths=1, G=0, **kw):
    """The kernel's taxed years, deaths every G years, the horizon settled: yields (t, kind, book, account) after each step, hook.reconcile applied after every settlement."""
    book, n = book_for(hook.st, paths, **kw), paths * 14
    for t in range(1, years + 1):
        K.step_year(book, RATE, 1.0, np.zeros(n), 0.0, hook=hook, t=t)
        yield t, 'year', book, hook.account()
        if G and t % G == 0 and t < years:
            K.step_death(book, RATE, 1.0)
            hook.reconcile(book)
            yield t, 'death', book, hook.account()
    K.settle_terminal(book)
    hook.reconcile(book)
    yield years, 'end', book, hook.account()


def test_the_account_closes_in_every_line_and_year_with_tax_on_and_i1_holds():
    h, paid = arm.HouseholdHook(ST, GAIN, 0.0157), 0.0
    for t, kind, book, a in run(h, 12):
        assert np.abs(a['residual']).max() < 1e-9 and (a['unpaid'] == 0).all() and K.shortfall_lines(book) == 0
        assert np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9 and (book.pen == h.q['pension']).all()
        paid += a['T_WDT'].sum()
    assert paid > 0


def test_the_payment_follows_the_class_weights_and_never_touches_pension():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 3):
        T, w = a['T_WDT'], {k: np.maximum(h.q1[k], 0.0) for k in arm.CLASSES[:3]}
        for k in arm.CLASSES[:3]:
            assert np.abs((h.q1[k] - h.q[k]) - T * w[k] / sum(w.values())).max() < 1e-9
        assert (h.q['pension'] == h.q1['pension']).all()
    assert T.max() > 0


def test_the_payment_ratios_are_over_the_pre_payment_balances_and_zero_when_nothing_is_paid():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 4):
        T, nonpen = a['T_WDT'], sum(h.q1[k] for k in arm.CLASSES[:3])
        assert np.allclose(a['pay_over_nonpension'][T > 0], (T / nonpen)[T > 0]) and np.allclose(a['pay_over_fin'][T > 0], (T / h.q1['net_financial'])[T > 0]) and (a['pay_over_fin'][T == 0] == 0).all()


def test_i3_closes_over_several_taxed_years():
    g, gg = np.zeros((6, 3)), np.full((6, 3), 0.0157)
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    out = rv.run_lines(BASE, RATE, g, gg, 0.0, hook=h, n_phase=1)
    assert out['assessed'].min() > 0 and rv.identity(out, g, 0.0, h)['assessed'].max() < 1e-9


@pytest.mark.parametrize('mode', ['sale', 'lien'])
def test_deaths_and_the_horizon_settle_and_the_account_closes(mode):
    h, last = arm.HouseholdHook(ST, GAIN, 0.0157), None
    for t, kind, book, a in run(h, 9, G=4, b_mode=mode):
        assert np.abs(a['residual']).max() < 1e-9 and (a['unpaid'] == 0).all() and K.shortfall_lines(book) == 0 and np.abs(book.family_true() - sum(h.q[k] for k in arm.CLASSES[:3])).max() < 1e-9
        last = a
    assert (book.LB == 0).all() and (book.A_D == 0).all() and (h.q['pension'] == book.pen).all()
