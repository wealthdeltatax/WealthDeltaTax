"""Brief 085c: the eight revenue-side outputs (O1d, OP1, OP3, OP4, OP5, OP6, OR1, OB1) in Samples for the named schedule."""
import json
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np
import pytest

from model_v3.core import revenue as rv
from model_v3.runner import out_revenue as M, runner as R
from test_runner import SPEC, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

HZ = ('transition', 'short', 'long')


@pytest.fixture(scope='module')
def run(ctx):
    g = R.paths(np.random.default_rng(5).standard_normal((100, 30)), 4.74, 8.2, 0.3)
    gg = np.full(g.shape, ctx.gdp_g)
    ev = R.evaluate(ctx, ctx.centre, SPEC, g, gg)
    return NS(ev=ev, s=R.samples({'S': ev}, ctx.ids, ctx.once), g=g, gg=gg)


def man(out, oid):
    return next(o for o in out['outputs'] if o['id'] == oid)


def test_each_id_has_one_cell_per_schedule_horizon_and_by_value_and_none_is_nan(run, out):
    want = {'O1d': 18, 'OP1': 1, 'OP3': 1, 'OP4': 1, 'OP5': 6, 'OP6': 4, 'OR1': 2, 'OB1': 36}
    assert set(M.IDS) == set(want)
    for oid, n in want.items():
        assert len(run.s[oid]) == n and all(k[0] == 'S' for k in run.s[oid]), oid
        assert not any(np.isnan(v).any() for v in run.s[oid].values()), oid      # central, every path fills: no nan


def test_the_cells_follow_the_manifest_lists(run, out, lv):
    cell = lambda oid, i: {dict(k[2])[i] if k[2] else None for k in run.s[oid]}
    assert cell('O1d', 'per') == set(man(out, 'O1d')['by']['per']) == cell('OP5', 'per')      # names come from the pack, not the code (R11)
    assert cell('OP6', 'year') == set(man(out, 'OP6')['by']['year'])
    assert cell('OB1', 'w_min') == set(man(out, 'OB1')['by']['w_min']) == set(M.RATIOS)
    assert sorted(M.RATIOS.values()) == lv['axes']['threshold_ratio'] and {k[3] for k in run.s['OB1']} == set(man(out, 'OB1')['lines'])
    assert {k[1] for k in run.s['O1d']} == set(HZ) and {k[1] for k in run.s['OP1']} == {'single'} == {k[1] for k in run.s['OR1']}


def test_op3_is_the_headline_p3_and_o1d_sums_to_the_retired_receipts(run):
    assert np.array_equal(run.s['OP3']['S', 'single', (), None], run.ev['P3h']['long'])
    for hz in HZ:
        total = sum(v for k, v in run.s['O1d'].items() if k[1] == hz)
        assert np.allclose(total, run.ev['M1d'][hz], atol=1e-9, equal_nan=True)


def test_ob1_reads_the_full_run_and_ob1_and_fund_ids_match_the_core(ctx, run):
    full = R.core_run(ctx, ctx.centre, SPEC, run.g, run.gg, full=True)                  # ratio 0.5 is r050
    b1a = run.s['OB1']['S', 'transition', (('w_min', 'r050'),), 'B1a']
    assert b1a.mean() > 1 and np.allclose(b1a, rv.window_mean(full.r['B1a'], np.ones((100, 30)), full.lo['transition'], full.hi['transition']))
    r = run.ev['revenue']
    assert np.array_equal(run.s['OP1']['S', 'single', (), None], run.ev['P1']) and np.array_equal(r['P4'], run.s['OP4']['S', 'single', (), None])
    assert np.array_equal(run.s['OP6']['S', 'single', (('year', 25),), None], r['P6'][25])
    assert np.array_equal(run.s['OR1']['S', 'single', (), 'P7b'], run.ev['P7b'])


def test_a_path_that_never_fills_gives_nan_in_the_short_window_only(ctx, run):
    zero = np.full((100, 4), -0.2)                                                          # a ruinous path: the reserve never fills
    e = R.evaluate(ctx, ctx.centre, SPEC, zero, np.full(zero.shape, ctx.gdp_g))['revenue']
    assert np.isnan(e['M1e'][next(iter(e['M1e']))]['short']).all() and not np.isnan(e['M1e'][next(iter(e['M1e']))]['long']).any()
