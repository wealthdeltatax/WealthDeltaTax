"""Brief 147c block 1: the `top_tail` switch. Off (default) leaves the household state byte-identical; on, D10b is scaled to the published top-1% share with the Rich List tiers fixed and the removed non-pension wealth given to D10a, so total wealth
and the top-decile share are unchanged (the `_e0` settings also take the missing wealth I-D4e off); the pension stays; I1, the account identity and the ledger ties hold in a short run."""
import importlib.util
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import yaml

from model_v3.runner import arm as ab, runner as R, switches as sw

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'model' / 'studies' / 'household-arm-run' / 'run_grid.py'
SHARE = {'ast_low': 0.144, 'ast_high': 0.165, 'ast_low_e0': 0.144, 'ast_high_e0': 0.165}


@pytest.fixture(scope='module')
def grid():
    spec = importlib.util.spec_from_file_location('run_grid_147', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ctx, inp = mod.A.setup()
    return mod, mod.point_ctx(ctx, inp, 'median_mid'), inp


def with_arm(c, **x):
    return replace(c, arm={**c.arm, **x})


def state(grid, **x):
    mod, c, _ = grid
    b = R.shaped(c, c.centre, mod.A.SPEC['ratio'])
    a = ab.build(with_arm(c, **x).arm, c, c.centre, b)
    return a.make().st, a.label['scenario'], b


def tot(st, b):
    W = sum(st['pos'].values()) * b.adults_k
    L = list(b.labels)
    return W, L, [L.index(x) for x in ('RL3', 'RL2', 'RL1')]


def test_off_is_the_default_and_leaves_the_state_and_label_unchanged(grid):
    s0, l0, _ = state(grid)
    s1, l1, _ = state(grid, top_tail='off')
    assert all(np.array_equal(s0['pos'][k], s1['pos'][k]) for k in s0['pos']) and l0 == l1 and 'top_tail' not in l0


@pytest.mark.parametrize('v', ['ast_low', 'ast_high'])
def test_the_top_one_percent_hits_the_published_share_with_total_and_top_decile_held(grid, v):
    s0, _, b = state(grid)
    s, lab, _ = state(grid, top_tail=v)
    W0, L, rl = tot(s0, b)
    W, *_ = tot(s, b)
    ia, ib = L.index('D10a'), L.index('D10b')
    top1 = lambda w: (w[ib] + w[rl].sum()) / w.sum()
    assert abs(top1(W) - SHARE[v]) < 1e-9 and top1(W0) > SHARE['ast_high']
    assert abs(W.sum() - W0.sum()) < 1e-6 and abs((W[ia] + W[ib] + W[rl].sum()) - (W0[ia] + W0[ib] + W0[rl].sum())) < 1e-6
    assert np.allclose(W[rl], W0[rl]) and np.allclose(np.delete(W, [ia, ib]), np.delete(W0, [ia, ib]))
    assert np.array_equal(s['pos']['pension'], s0['pos']['pension']) and all(s['pos'][k][ib] > 0 for k in s['pos'])
    assert lab['top_tail'] == v and abs(lab['wealth_moved_bn'] - (W0[ib] + W0[rl].sum() - SHARE[v] * W0.sum())) < 1e-6      # 146r's amounts (1,069bn and 770bn) are on the unshaped pack; the arm's stock carries the launch loss


@pytest.mark.parametrize('v', ['ast_low_e0', 'ast_high_e0'])
def test_the_e0_settings_take_the_missing_wealth_off_and_scale_to_the_survey_total(grid, v):
    s0, _, b = state(grid)
    s, lab, _ = state(grid, top_tail=v)
    W0, L, rl = tot(s0, b)
    W, *_ = tot(s, b)
    ia, ib = L.index('D10a'), L.index('D10b')
    top0 = W0[ib] + W0[rl].sum()
    drop = top0 * 0.05 / (0.18 + 0.05)                                                                 # I-D4e 5% and I-D4d 18%: the missing wealth inside the top 1%
    assert abs(W.sum() - (W0.sum() - drop)) < 1e-6 and abs((W[ib] + W[rl].sum()) / W.sum() - SHARE[v]) < 1e-9
    assert abs((W[ia] + W[ib] + W[rl].sum()) - (W0[ia] + W0[ib] + W0[rl].sum() - drop)) < 1e-6          # the top decile loses only the missing wealth


def test_an_unknown_setting_or_one_that_would_raise_the_top_raises(grid):
    with pytest.raises(ValueError, match='top_tail'):
        state(grid, top_tail='high')


@pytest.mark.parametrize('v', ['ast_low', 'ast_high_e0'])
def test_a_short_run_holds_i1_the_account_identity_and_the_ledger_ties(grid, v):
    mod, c, inp = grid
    man = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    _, k = mod.run_point(with_arm(c, top_tail=v), inp, 'median_mid', man, 4, 4)
    assert k['error'] == '' and k['i1'].startswith('held') and k['account_residual_max'] < 1e-9 and k['ledger_tie_max'] < 1e-9 and k['unpaid_max'] < 1e-9
