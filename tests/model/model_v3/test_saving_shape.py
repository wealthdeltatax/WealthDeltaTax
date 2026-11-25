"""Brief 147c block 2: the `saving_shape` switch. `flat` (default) leaves the state and label unchanged; `mild` and `steep` give the saving ratio by line the 145r offsets, income-weighted to a mean of zero, so aggregate saving equals `flat`'s at every flat value;
the offsets match the 145r table; I1, the account identity and the ledger ties hold in a short run."""
import csv
import importlib.util
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import yaml

from model_v3.runner import arm as ab, runner as R, switches as sw

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'model' / 'studies' / 'household-arm-run' / 'run_grid.py'
TABLE = ROOT / 'research' / 'tables' / '145r-saving-shapes-and-withdrawal-range' / 'saving_shapes.csv'


@pytest.fixture(scope='module')
def grid():
    spec = importlib.util.spec_from_file_location('run_grid_147s', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ctx, inp = mod.A.setup()
    return mod, ctx, inp


def state(grid, name='median', **x):
    mod, ctx, inp = grid
    c = replace(mod.point_ctx(ctx, inp, 'median_mid'), arm={**mod.point_ctx(ctx, inp, 'median_mid').arm, 'saving': name, **x})
    b = R.shaped(c, c.centre, mod.A.SPEC['ratio'])
    a = ab.build(c.arm, c, c.centre, b)
    return a.make().st, a.label['scenario'], b


def floor_report(grid, name='median', **x):
    mod, ctx, inp = grid
    c = mod.point_ctx(ctx, inp, 'median_mid')
    c = replace(c, arm={**c.arm, 'saving': name, **x})
    return ab.build(c.arm, c, c.centre, R.shaped(c, c.centre, mod.A.SPEC['ratio'])).make().floor_report


def test_flat_is_the_default_and_leaves_the_state_and_label_unchanged(grid):
    s0, l0, _ = state(grid)
    s1, l1, _ = state(grid, saving_shape='flat')
    assert np.array_equal(s0['sav'], s1['sav']) and l0 == l1 and 'saving_shape' not in l0


@pytest.mark.parametrize('name', ['min', 'median', 'max'])
@pytest.mark.parametrize('shape', ['mild', 'steep'])
def test_aggregate_saving_equals_flat_at_every_flat_value(grid, name, shape):
    s0, _, b = state(grid, name)
    s, lab, _ = state(grid, name, saving_shape=shape)
    w, rep = s0['income'] * b.adults_k, floor_report(grid, name, saving_shape=shape)
    assert abs((w * s['sav']).sum() - (w * s0['sav']).sum() - rep['saving_added_pts'] / 100 * w.sum()) < 1e-12 * w.sum() and lab['saving_shape'] == shape and 'saving_floor' in lab   # equal to flat's where no line is floored; flat's plus the dissaving the floor removes otherwise
    assert (rep['lines_floored'] == 0) == (rep['saving_added_pts'] == 0.0)
    assert all(np.array_equal(s[k], s0[k]) for k in ('income', 'acc')) and all(np.array_equal(s['pos'][k], s0['pos'][k]) for k in s0['pos'])


@pytest.mark.parametrize('shape', ['mild', 'steep'])
def test_the_offsets_match_the_145r_table(grid, shape):
    s0, _, b = state(grid)
    s, _, _ = state(grid, saving_shape=shape)
    rows = {r['line']: float(r['delta_pp']) for r in csv.DictReader(open(TABLE)) if r['shape'] == shape}
    got, want, lam = 100 * (s['sav'] - s0['sav']), np.array([rows[x] for x in b.labels]), floor_report(grid, saving_shape=shape)['lam']
    assert np.allclose(got[lam == 1], want[lam == 1], atol=1e-3)                                 # unfloored lines carry the 145r offset
    assert np.all(got[lam < 1] > want[lam < 1] - 1e-9) and np.all(got[lam < 1] <= 1e-9)             # a floored line's offset is limited, not reversed


def test_mild_lowers_only_the_two_lowest_lines_relative_to_the_rest_and_steep_rises_with_rank(grid):
    s0, _, b = state(grid)
    m, _, _ = state(grid, saving_shape='mild')
    t, _, _ = state(grid, saving_shape='steep')
    d = m['sav'] - s0['sav']
    assert d[0] == d[1] < 0 and np.allclose(d[2:], d[2]) and d[2] > 0
    assert np.all(np.diff((t['sav'])[2:]) >= -1e-15) and t['sav'][-1] > t['sav'][2]


def test_an_unknown_shape_raises(grid):
    with pytest.raises(ValueError, match='saving_shape'):
        state(grid, saving_shape='tilted')


@pytest.mark.parametrize('point, shape', [('median_mid', 'mild'), ('max_mid', 'steep')])
def test_a_short_run_holds_i1_the_account_identity_and_the_ledger_ties(grid, point, shape):
    """Only cells that complete: six of the ten non-flat cells at the five points stop in M13 (CRRA utility needs positive terminal wealth: D1 and D2 dissave to a negative balance), see the 147c note."""
    mod, ctx, inp = grid
    c = mod.point_ctx(ctx, inp, point)
    man = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    _, k = mod.run_point(replace(c, arm={**c.arm, 'saving_shape': shape}), inp, point, man, 4, 4)
    assert k['error'] == '' and k['i1'].startswith('held') and k['account_residual_max'] < 1e-9 and k['ledger_tie_max'] < 1e-9 and k['unpaid_max'] < 1e-9


def test_floored_and_unfloored_agree_where_no_line_hits_zero(grid):
    rep = floor_report(grid, 'max', saving_shape='steep')
    s0, _, b = state(grid, 'max')
    s, _, _ = state(grid, 'max', saving_shape='steep')
    assert rep['lines_floored'] == 0 and rep['saving_added_pts'] == 0.0 and np.all(rep['lam'] == 1.0)
    w = s0['income'] * b.adults_k
    assert abs((w * s['sav']).sum() - (w * s0['sav']).sum()) < 1e-12 * w.sum()


def test_the_floor_keeps_wealth_at_or_above_zero_and_the_floored_cell_completes(grid):
    mod, ctx, inp = grid
    rep = floor_report(grid, 'min', saving_shape='steep')
    assert rep['lines_floored'] >= 1 and rep['saving_added_pts'] > 0 and np.all((0 <= rep['lam']) & (rep['lam'] <= 1))
    c = mod.point_ctx(ctx, inp, 'min_mid')
    man = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    _, k = mod.run_point(replace(c, arm={**c.arm, 'saving_shape': 'steep'}), inp, 'min_mid', man, 4, 4)
    assert k['error'] == '' and k['i1'].startswith('held') and k['account_residual_max'] < 1e-9 and k['ledger_tie_max'] < 1e-9
