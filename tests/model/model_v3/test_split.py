"""Tests for out/split.py (brief 183c stage A): the partial encoding, the draw slices, the header and the refusals, on synthetic partials. No model is run."""
import json
import math
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import pack as pk
from model_v3.out import split as sp
from model_v3.runner import runner as R

ROOT = Path(__file__).parents[3]
COMMON = dict(size='smoke', seed=1, arm='household', n1=50, n2p=20, n2=5, tol=0.01, points=['median_mid', 'max_mid'], schedules=['S_low', 'S_central', 'S_high'], batch=2,
              git_sha='a' * 40, inputs={'manifest': 'm'}, numerics={'NPY_DISABLE_CPU_FEATURES': 'X86_V4', 'numpy': '2.5.3', 'probe': 'p'})


def partial(unit, plan_sha=None, draws='d1', body=None, **over):
    kind = unit['kind']
    h = sp.header(kind, unit, {**COMMON, **over}, plan_sha256=plan_sha, draws_sha256=draws if kind.startswith('o1e') else None)
    return {'header': h, 'body': body or {'x': sp.enc([0.1, float('nan')])}}


def run_files(**over):
    """A complete set for COMMON: plan, 2 points, the point roots and 3 schedules x 3 batches of draws (0:2, 2:4, 4:5)."""
    plan = sp.dumps(partial(sp.unit('plan'), **over))
    ph = sp.sha256(plan)
    us = [sp.unit('point', point=p) for p in COMMON['points']] + [sp.unit('o1e-point')] + [sp.unit('o1e', schedule=s, a=a, b=min(a + 2, 5)) for s in COMMON['schedules'] for a in (0, 2, 4)]
    return [('plan.json', plan)] + [(f'{sp.uid({"unit": u})}.json', sp.dumps(partial(u, plan_sha=ph, **over))) for u in us]


def test_floats_cross_exactly_in_hex_including_nan_inf_and_numpy():
    xs = [0.1, -0.0, 5e-324, 1.7976931348623157e308, math.pi, float('inf'), -float('inf'), np.float64(2.0) / 3]
    back = sp.dec(json.loads(sp.dumps({'v': sp.enc(xs)})))['v']
    assert [x.hex() for x in back] == [float(x).hex() for x in xs] and math.isnan(sp.dec(sp.enc(float('nan'))))
    assert sp.dec(sp.enc({'a': (1.5, [2.5])})) == {'a': [1.5, [2.5]]}


def test_bytes_are_stable_and_a_bare_nan_is_refused():
    p = partial(sp.unit('point', point='median_mid'), plan_sha='x')
    assert sp.dumps(p) == sp.dumps(json.loads(sp.dumps(p).decode())) and sp.dumps(p).endswith(b'}\n')
    with pytest.raises(sp.SplitError, match='non-finite'):
        sp.dumps({'x': float('nan')})


def test_draw_slices_concatenate_to_the_full_table_and_a_short_call_is_a_different_table():
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'),
                    json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text()), ['I-D5a', 'I-D4a', 'I-D9h'], [])
    full = R.draw_theta(np.random.default_rng(3), ctx, ctx.tier1, 7)
    parts = [sp.slice_draws(full, a, b) for a, b in ((0, 3), (3, 5), (5, 7))]
    assert all(np.array_equal(np.concatenate([p[k] for p in parts]), full[k]) for k in full)
    assert sp.draws_sha(full) == sp.draws_sha({k: np.array(v) for k, v in full.items()}) and sp.draws_sha(full) != sp.draws_sha(R.draw_theta(np.random.default_rng(4), ctx, ctx.tier1, 7))
    short = R.draw_theta(np.random.default_rng(3), ctx, ctx.tier1, 3)
    assert any(not np.array_equal(short[k], full[k][:3]) for k in full)     # never compute a shard's draws with n = b - a


def test_a_complete_set_checks_in_canonical_order_whatever_the_order_given():
    files = run_files()
    got = sp.check(files)
    assert list(got) == sp.expected(COMMON | {}) == ['plan', 'point:median_mid', 'point:max_mid', 'o1e-point'] + [f'o1e:{s}:{a}:{b}' for s in COMMON['schedules'] for a, b in ((0, 2), (2, 4), (4, 5))]
    assert list(sp.check(files[::-1])) == list(got) and list(sp.check(files + files[3:5])) == list(got)       # a duplicate with the same bytes is one unit


def test_zero_draws_needs_no_batches():
    files = run_files(n2=0)
    keep = [f for f in files if not f[0].startswith('o1e:')]
    assert list(sp.check(keep)) == ['plan', 'point:median_mid', 'point:max_mid', 'o1e-point']


@pytest.mark.parametrize('field, value', [('seed', 2), ('size', 'quick'), ('git_sha', 'b' * 40), ('numerics', {'NPY_DISABLE_CPU_FEATURES': '', 'numpy': '2.5.3', 'probe': 'p'}),
                                          ('inputs', {'manifest': 'other'}), ('n2', 6), ('points', ['max_mid'])])
def test_a_header_field_that_differs_is_refused_and_named(field, value):
    files = run_files()
    name, raw = files[3]
    p = sp.loads(raw); p['header'][field] = value
    with pytest.raises(sp.SplitError, match=f'header field {field}'):
        sp.check(files[:3] + [(name, sp.dumps(p))] + files[4:])


def test_missing_extra_duplicate_gap_and_overlap_are_refused():
    files = run_files()
    with pytest.raises(sp.SplitError, match='missing.*o1e:S_central:2:4'):
        sp.check([f for f in files if f[0] != 'o1e:S_central:2:4.json'])
    p = sp.loads(files[1][1]); p['body'] = {'x': 'changed'}
    with pytest.raises(sp.SplitError, match='differ'):
        sp.check(files + [('rerun.json', sp.dumps(p))])
    over = partial(sp.unit('o1e', schedule='S_low', a=0, b=3), plan_sha=sp.sha256(files[0][1]))
    with pytest.raises(sp.SplitError, match='unexpected'):
        sp.check(files + [('o.json', sp.dumps(over))])
    gap = [f for f in files if f[0] not in ('o1e:S_low:2:4.json',)] + [('g.json', sp.dumps(partial(sp.unit('o1e', schedule='S_low', a=3, b=4), plan_sha=sp.sha256(files[0][1]))))]
    with pytest.raises(sp.SplitError, match='missing'):
        sp.check(gap)
    with pytest.raises(sp.SplitError, match='no partial'):
        sp.check([])


def test_other_plan_other_draws_wrong_schema_and_bad_headers_are_refused():
    files = run_files()
    with pytest.raises(sp.SplitError, match='another plan'):
        sp.check([('plan.json', sp.dumps(partial(sp.unit('plan'), seed=1, tol=0.01) | {'body': {'x': 'other plan'}}))] + files[1:])
    other = sp.loads(files[-1][1]); other['header']['draws_sha256'] = 'd2'
    with pytest.raises(sp.SplitError, match='draws_sha256'):
        sp.check(files[:-1] + [(files[-1][0], sp.dumps(other))])
    old = sp.loads(files[2][1]); old['header']['schema'] = 'wdt-split-partial/0'
    with pytest.raises(sp.SplitError, match='schema'):
        sp.check(files[:2] + [(files[2][0], sp.dumps(old))] + files[3:])
    odd = sp.loads(files[2][1]); odd['header']['extra'] = 1
    with pytest.raises(sp.SplitError, match='header fields'):
        sp.check(files[:2] + [(files[2][0], sp.dumps(odd))] + files[3:])
    with pytest.raises(sp.SplitError):
        sp.header('o1e', sp.unit('o1e', schedule='S_low', a=0, b=2), COMMON)                  # an o1e unit without the hash of the draws
    with pytest.raises(sp.SplitError):
        sp.header('point', sp.unit('point', point='p'), {k: v for k, v in COMMON.items() if k != 'seed'}, plan_sha256='x')
    assert sp.header('point', sp.unit('point', point='p'), COMMON, workers=4, plan_sha256='x')['workers'] == 4


def test_workers_and_the_unit_are_not_compared():
    files = run_files()
    p = sp.loads(files[1][1]); p['header']['workers'] = 4
    assert list(sp.check(files[:1] + [(files[1][0], sp.dumps(p))] + files[2:]))[1] == 'point:median_mid'
