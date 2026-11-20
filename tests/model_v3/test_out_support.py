"""Brief 087c: the support group fills O7, OD1, OW1, OW2, OW3, OM1 and OS1 in Samples."""
import numpy as np
import pytest

from model_v3.runner import out_support as S, runner as R
from test_runner import SPEC, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

P = 4
G = lambda: (R.paths(np.random.default_rng(5).standard_normal((100, P)), 4.7, 8.2, 0.3), np.full((100, P), 0.015))


@pytest.fixture(scope='module')
def ev(ctx):
    return R.evaluate(ctx, ctx.centre, SPEC, *G(), seq=np.random.SeedSequence(3), key=(0,))


@pytest.fixture(scope='module')
def cells(ev):
    return S.cells(ev['support'])


def test_every_id_has_one_cell_per_manifest_vocabulary(cells, out):
    by = {o['id']: o for o in out['outputs']}
    assert set(cells) == set(S.IDS) and all(i in by for i in cells)
    n = {'O7': 1, 'OD1': 16, 'OW1': 20, 'OW2': 9, 'OW3': 5 * 3 + 5, 'OM1': 9, 'OS1': 3}
    assert {i: len(c) for i, c in cells.items()} == n
    assert {k[1] for k in cells['OD1']} == {(('alpha_grid', a),) for a in by['OD1']['by']['alpha_grid']}
    assert {k[2] for k in cells['OW3']} == {'M15a', 'M15b'} and {k[0] for k in cells['OW3'] if k[2] == 'M15b'} == {'transition'}


def test_shapes_follow_the_summary_forms(cells):
    assert all(v.shape == (3,) for i in ('O7', 'OD1') for v in cells[i].values())            # point_and_range: [point, lo, hi]
    assert all(v.shape == (P,) for i in ('OW1', 'OW2', 'OW3', 'OM1') for v in cells[i].values())   # one entry per path


def test_the_zone_contains_alpha_one_and_c1_is_zero_there(ev, cells):
    z, c = ev['support']['decl']['zone'], ev['support']['decl']['M7c']
    assert np.all(z['lo'] <= 1.0) and np.all(z['hi'] >= 1.0) and np.all(c['a100'] == 0.0)
    assert cells['O7'][('single', (), None)][1] <= 1.0 <= cells['O7'][('single', (), None)][2]


def test_m9_is_m1_less_x_and_the_cap_outputs_are_sane(cells):
    m = {(k[0], k[2]): v for k, v in cells['OM1'].items()}
    for h in S.HZ:
        np.testing.assert_allclose(m[h, 'M9'], m[h, 'M1'] - m[h, 'X'], atol=1e-12)
    a = np.concatenate([v for k, v in cells['OW3'].items() if k[2] == 'M15a'])
    b = cells['OW3'][('transition', (('entry_year', 'value_per_cohort'), ('wealth_band', 'overall')), 'M15b')]
    assert np.nanmin(a) >= 0 and np.nanmax(a) <= 100 + 1e-9 and np.nanmin(b) >= 0


def test_welfare_is_a_cost_and_chunks_repeat_one_value(cells):
    w = cells['OW1']
    f = [v for v in w.values() if np.isfinite(v).all()]
    assert len(f) == 16 and all(v.max() <= 1e-9 and np.ptp(v) == 0 for v in f)     # D4_5 has no payer at launch: nan, as in O2
    o = {dict(k[1])['tax_system']: v[0] for k, v in w.items() if dict(k[1])['wealth_band'] == 'overall'}
    assert o['wdt'] > o['stock_wealth_tax']
    assert all(np.ptp(v) == 0 for v in cells['OW2'].values())


def test_capitalisation_changes_m1_through_the_routes_and_is_zero_off(ctx, ev):
    s1 = {k[1][0][1]: v for k, v in S.cells(ev['support'])['OS1'].items()}
    assert set(s1) == {'m1', 'm2', 'payer_count'} and np.isfinite(s1['m1']).all() and s1['m1'][0] != 0
    b = R.shaped(ctx, ctx.centre, SPEC['ratio'])
    assert np.array_equal(S.grow(b, 1.0).wealth, b.wealth) and np.allclose(sum(S.grow(b, 1.1).V0.values()), 1.1 * b.wealth)


def test_the_group_is_reproducible_by_chunk(ctx, ev):
    again = R.evaluate(ctx, ctx.centre, SPEC, *G(), seq=np.random.SeedSequence(3), key=(0,))['support']
    assert np.array_equal(again['lock']['pct50']['y10'], ev['support']['lock']['pct50']['y10'])
