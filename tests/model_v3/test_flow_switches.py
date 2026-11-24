"""Brief 148c, block 1: pension_withdrawal and heir_floor. Off, nothing moves; on, the draw is a transfer inside the base (I1, the account identity, total wealth) and the floor leaves the heir's share."""
import numpy as np
import pytest

from model_v3.core import kernel as K, pension_lien as pl
from model_v3.runner import arm, flow_switches as fsw
from test_runner import ctx, lv, out, tier1  # noqa: F401  (the fixtures)

POS = dict(property=np.array([0.04, 0.04]), net_financial=np.array([0.01, 0.01]), physical=np.array([0.0, 0.0]), pension=np.array([5.0, 5.0]))
ST = dict(pos=POS, income=np.array([0.0, 0.0]), sav=np.array([0.0, 0.0]), acc=np.array([0.0, 0.0]))
GAIN = dict(property=0.0, net_financial=0.03, physical=0.0, pension=0.03)


def run(a, years=3, rates=(0.0, 0.0, 0.0), wd=None, r_def=0.0, pension=5.0):
    st = {**ST, 'pos': {**POS, 'pension': np.full(2, pension)}, **({} if wd is None else {'wd': np.array(wd)})}
    h = fsw.hook(a, arm.HouseholdHook)(st, GAIN, 0.0)
    book = K.Book(2, {'A': np.array([0.05, 0.05])}, r_def=r_def)
    for t in range(1, years + 1):
        K.step_year(book, lambda w, r=rates[t - 1]: r + 0.0 * w, 1.0, np.zeros(2), 0.0, hook=h, t=t)
    return h, book


def test_off_returns_the_class_and_the_state_and_label_untouched():
    st, lab = dict(pos=1), dict(scenario={'saving': 'median'})
    assert fsw.hook({}, arm.HouseholdHook) is arm.HouseholdHook and fsw.hook(dict(pension_withdrawal='off', heir_floor=0), arm.HouseholdHook) is arm.HouseholdHook
    s2, l2 = fsw.scenario({}, None, st, lab, None)
    assert s2 is st and l2 is lab
    assert np.array_equal(pl.settle({'a': np.array([1.0])}, np.array([3.0]), np.array([5.0]))[3], pl.settle({'a': np.array([1.0])}, np.array([3.0]), np.array([5.0]), 0.0)[3])


def test_bad_settings_raise():
    for k, v in (('pension_withdrawal', 'some'), ('heir_floor', 10)):
        with pytest.raises(ValueError, match=k):
            fsw.hook({k: v}, arm.HouseholdHook)


def test_a_draw_moves_the_pension_into_net_financial_and_total_wealth_is_unchanged():
    base, _ = run({}, 3)
    h, book = run(dict(pension_withdrawal='mid'), 3, wd=[0.02, 0.0])                                 # line 0 draws 2% of its opening pension a year, line 1 none
    q0, q = base.q, h.q
    tot = lambda x: sum(x[k] for k in arm.CLASSES)
    assert np.allclose(tot(q), tot(q0), atol=1e-12) and np.allclose(q['pension'][1], q0['pension'][1], atol=0) and q['pension'][0] < q0['pension'][0]
    d = q0['pension'][0] - q['pension'][0]
    assert d > 0.1 and np.isclose(q['net_financial'][0] - q0['net_financial'][0], d, atol=1e-9) and np.isclose(book.pen[0], q['pension'][0] - h.PK[0], atol=1e-12)
    a = h.account()
    assert np.abs(a['residual']).max() < 1e-9 and a['withdrawn'][0] > 0 and a['withdrawn'][1] == 0 and np.isclose(a['dNW'][0], base.account()['dNW'][0], atol=1e-12)


def test_withdrawal_composes_with_the_lien_and_raises_the_capacity_to_pay():
    h0, _ = run({}, 1, rates=(0.5,))
    h, book = run(dict(pension_withdrawal='high'), 1, rates=(4.0,), wd=[0.03, 0.03])
    h4, _ = run({}, 1, rates=(4.0,))
    a = h.account()
    assert np.abs(a['residual']).max() < 1e-9 and K.shortfall_lines(book) == 0                          # I1 is checked inside the hook each year: a failure raises
    assert h0.PL.min() > 0 and h.PL.min() > 0 and (h.PL < h4.PL).all() and np.allclose(h.lien()['bal'], h.PL, atol=0)   # the draw gives the units more to pay with, so less is carried as a lien
    assert (run(dict(pension_withdrawal='high'), 1, rates=(0.5,), wd=[0.03, 0.03])[0].PL == 0).all()  # and a small tax is paid in full


def test_the_heir_floor_leaves_a_share_of_the_pension_and_writes_the_rest_off():
    kw = dict(years=1, rates=(200.0,), pension=0.1)                                                            # a lien far above the pension: the draw takes the pension, the rest is written off (138c)
    h0, b0 = run({}, **kw)
    pl0, pen = h0.PL[0], h0.q['pension'][0]
    h0.settle(b0)
    assert np.isclose(h0.set_p[0], pen) and np.isclose(h0.wo[0], pl0 - pen) and h0.q['pension'][0] == 0
    for pct in (25, 50):
        h, b = run(dict(heir_floor=pct), **kw)
        h.settle(b)
        keep = pct / 100 * pen
        assert np.isclose(h.set_p[0], pen - keep, atol=1e-12) and np.isclose(h.q['pension'][0], keep, atol=1e-12) and h.PL[0] == 0
        assert np.isclose(h.wo[0], pl0 - (pen - keep), atol=1e-9) and h.lien()['wo'][0] == h.wo[0]            # what the floor leaves is written off and reported in the ledger's column


def test_through_core_run_off_is_byte_identical_and_on_keeps_the_identities(ctx, monkeypatch):
    import json
    from dataclasses import replace
    from test_arm_switch import INP, PATHS, SPEC
    from model_v3.runner import runner as R
    seen, orig = [], arm.HouseholdHook.post

    def spy(self, book, fl):
        orig(self, book, fl)
        seen.append(np.abs(self.account()['residual']).max())

    monkeypatch.setattr(arm.HouseholdHook, 'post', spy)
    run_ = lambda **k: R.core_run(replace(ctx, arm=dict(arm='household', inputs=INP, saving='median', **k)), ctx.centre, SPEC, *PATHS)
    base, off = run_(), run_(pension_withdrawal='off', heir_floor=0)
    assert all(np.array_equal(base.run[k], off.run[k]) for k in ('tax', 'death_tax', 'heir', 'refund')) and base.arm == off.arm
    on = run_(pension_withdrawal='high', heir_floor=50)
    assert on.arm['scenario']['pension_withdrawal']['setting'] == 'high' and on.arm['scenario']['heir_floor']['pct'] == 50 and 'pension_withdrawal' not in base.arm['scenario']
    assert max(seen) < 1e-9 and not np.array_equal(base.run['tax'], on.run['tax'])


def test_gdp_paths_off_returns_the_array_and_bad_settings_raise():
    g = np.full((5, 3), 0.0157)
    assert fsw.gdp('legacy', {}, g, g, None) is g and fsw.gdp(dict(arm='household'), {}, g, g, None) is g and fsw.gdp(dict(gdp_paths='off'), {}, g, g, None) is g
    with pytest.raises(ValueError, match='gdp_paths'):
        fsw.gdp_paths(dict(gdp_paths='x'))
    assert issubclass(fsw.hook(dict(gdp_paths='indep'), arm.HouseholdHook), arm.HouseholdHook)                 # built without a path (the comparators' arm): the fixed income growth


@pytest.mark.parametrize('v', ['indep', 'hist'])
def test_the_gdp_process_has_the_stated_moments_and_correlation(v):
    from model_v3.runner import runner as R
    T, P, th = 100, 40000, dict(zip(fsw.MARKET, (4.74, 8.22, 0.30)))
    g = R.paths(np.random.default_rng(3).standard_normal((T, P)), *th.values())
    base = np.full((T, P), 0.0157039)
    out = fsw.gdp(dict(gdp_paths=v), th, g, base, lambda name: np.random.default_rng(4))
    d = out - base
    assert abs(out.mean() - 0.0157039) < 4e-4 and abs(d.std() - fsw.SD) < 5e-4 and abs(np.corrcoef(d[1:].ravel(), d[:-1].ravel())[0, 1] - fsw.PHI) < 0.01      # mean, marginal SD, lag-1
    assert abs(np.corrcoef(d.ravel(), g.ravel())[0, 1] - 0.9996 * fsw.RHO[v]) < 0.01                                                                        # 146r: same-year correlation = innovation correlation x 0.9996
    assert np.array_equal(out, fsw.gdp(dict(gdp_paths=v), th, g, base, lambda name: np.random.default_rng(4)))                                               # the same seed, the same paths


@pytest.mark.parametrize('v', ['indep', 'hist'])
def test_gdp_paths_through_core_run_keep_the_identities_and_income_follows_the_path(ctx, monkeypatch, v):
    from dataclasses import replace
    from test_arm_switch import INP, SPEC
    from model_v3.runner import runner as R
    seen, orig = [], arm.HouseholdHook.post

    def spy(self, book, fl):
        orig(self, book, fl)
        seen.append((np.abs(self.account()['residual']).max(), np.abs(self.account()['S']).max()))

    monkeypatch.setattr(arm.HouseholdHook, 'post', spy)
    g = R.paths(np.random.default_rng(5).standard_normal((100, 6)), 4.74, 8.22, 0.30)
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median', gdp_paths=v))
    ev = R.evaluate(c2, c2.centre, SPEC, g, np.full(g.shape, ctx.gdp_g), seq=None, key=())
    raw = R.core_run(c2, c2.centre, SPEC, g, fsw.gdp(c2.arm, c2.centre, g, np.full(g.shape, ctx.gdp_g), lambda n: np.random.default_rng(1)))
    assert raw.arm['scenario']['gdp_paths']['setting'] == v and raw.gdp_g.std(axis=1).min() > 0 and max(r for r, _ in seen) < 1e-9
    wdt = sum(raw.run[k] for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D'))
    assert np.abs(sum(raw.run['ledger']['rc'].values()) - wdt).max() < 1e-9 and np.isfinite(ev['M1']['short']).any()
    assert not np.allclose(raw.run['gdp_index'][:, 0], raw.run['gdp_index'][:, 1]) and raw.run['gdp_index'][-1].std() > 0                          # the GDP index differs by path
    from model_v3.runner import arm as ab
    assert ab.withheld(raw.arm)['OW1'] == 'legacy_only'


def test_the_household_income_follows_each_paths_gdp_index():
    gdp = np.array([[0.10, -0.05], [0.20, 0.0], [0.0, 0.0]])                                                   # (T, P): two paths, three years
    st = {**ST, 'income': np.array([1.0, 2.0]), 'sav': np.array([0.5, 0.5])}
    h = fsw.hook(dict(gdp_paths='indep'), arm.HouseholdHook, gdp, arm.returns)(st, GAIN, 0.0)
    book = K.Book(4, {'A': np.full(4, 0.05)})                                                                 # lines of a path side by side: [l0 p0, l1 p0, l0 p1, l1 p1]
    for t in (1, 2, 3):
        K.step_year(book, lambda w: 0.0 * w, 1.0, np.zeros(4), 0.0, hook=h, t=t)
        idx = np.array([1.0, 1.1, 1.32][t - 1]), np.array([1.0, 0.95, 0.95][t - 1])
        want = 0.5 * np.array([1.0, 2.0, 1.0, 2.0]) * np.repeat([idx[0], idx[1]], 2)
        assert np.allclose(h.account()['S'], want, atol=1e-12) and np.abs(h.account()['residual']).max() < 1e-9
    assert np.isclose(h.gr, 0.0)                                                                              # the scalar growth is restored after each year
