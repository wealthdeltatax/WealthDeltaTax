"""Briefs 084c and 092c: the output groups are named in one place, get Env, an empty group changes no number, and `samples` refuses a bad or doubled id."""
from types import SimpleNamespace as NS

import numpy as np
import pytest

from model_v3.core import returns as rt
from model_v3.runner import groups as G, runner as R
from test_runner import SPEC, ctx, level1, lv, out, tier1  # noqa: F401  (the fixtures)

PIN = 'ce75c164e99d70ca1088daa095a6335aa8bdfc63b5edbf5b8b9315f41a6c46cc'     # 055c's Samples digest: seed 7, 40 paths, chunks of 20, SPEC
GROUP = lambda name, ids=(), cells=None, pp=lambda raw, env, again: {}, **kw: NS(NAME=name, IDS=ids, per_path=pp, cells=lambda e: cells or {}, **kw)
PATHS = lambda n=2: (R.paths(np.zeros((100, n)), 4.7, 8.2, 0.3), np.full((100, n), 0.015))
EV = lambda ctx, m, mp, **kw: (mp.setattr(R, 'GROUPS', (m,)), R.evaluate(ctx, ctx.centre, SPEC, *PATHS(), **kw))[1]


def test_the_four_groups_are_named_explicitly_and_follow_the_interface(out):
    assert [m.NAME for m in G.GROUPS] == ['revenue', 'burden', 'support', 'sweeps']
    ids = [i for m in G.GROUPS for i in m.IDS]            # manifest ids, no two groups share one
    assert set(ids) <= {o['id'] for o in out['outputs']} and len(ids) == len(set(ids)) and all(m.cells({}) == m.per_path(None, None, None) == {} for m in G.GROUPS)


def test_an_empty_group_changes_no_number(ctx, monkeypatch):
    monkeypatch.setattr(R, 'GROUPS', (GROUP('x'),))
    assert R.digest(level1(ctx, 7)[0]) == PIN and 'x' in R.evaluate(ctx, ctx.centre, SPEC, *PATHS(3))


def test_again_reruns_the_core_once_and_full_gives_the_receipts_of_run_lines(ctx, monkeypatch):
    seen = []
    pp = lambda raw, env, again: seen.append((again({}) is again({}), raw.r['B1a'].any(), again({}, full=True).r['B1a'].any(), again({}, full=True) is again({}, full=True))) or {}
    EV(ctx, GROUP('x', pp=pp), monkeypatch)
    assert seen == [(True, False, True, True)]


def test_env_rng_is_reproducible_and_distinct_by_chunk_and_name(ctx, monkeypatch):
    got, seq = [], rt.streams(7)['level1_paths'].bit_generator.seed_seq
    pp = lambda raw, env, again: got.append((env.ctx is ctx and env.pack is ctx.pack and sorted(env.lam) == ['lam_C', 'lam_D'], env.rng('a').random(3), env.rng('b').random(3))) or {}
    [EV(ctx, GROUP('x', pp=pp), monkeypatch, seq=seq, key=k) for k in ((0,), (0,), (1,))]
    a, b, c = got
    assert a[0] and np.array_equal(a[1], b[1]) and not np.array_equal(a[1], c[1]) and not np.array_equal(a[1], a[2])


def test_samples_puts_the_schedule_in_front_refuses_a_bad_or_doubled_id_and_stores_static_cells(ctx, monkeypatch):
    base = {**EV(ctx, GROUP('x'), monkeypatch), 'y': {}}
    cell = {'OP1': {('short', (), None): np.zeros(2)}}
    monkeypatch.setattr(R, 'GROUPS', (GROUP('x', ('OP1',), cell),))
    assert list(R.samples({'S': {**base, 'x': {}}}, ctx.ids)['OP1']) == [('S', 'short', (), None)]
    for groups, why in (((GROUP('x', ('OP1',), cell), GROUP('y', ('OP1',), cell)), 'returned by'), ((GROUP('x', ('OP1',), {'ZZ9': {}}),), 'not in the manifest'),
                        ((GROUP('x', (), cell),), 'IDS')):
        monkeypatch.setattr(R, 'GROUPS', groups)
        with pytest.raises(R.RunnerError, match=why):
            R.samples({'S': base}, ctx.ids)
    with pytest.raises(R.RunnerError, match='manifest'):
        R.samples({'S': base}, {'O1'})
    sc = {'OP1': {('single', (), None): np.ones(1)}}                                              # a static cell: schedule None, only for a once id
    monkeypatch.setattr(R, 'GROUPS', (GROUP('x', ('OP1',), static=lambda env: sc),))
    assert list(R.samples({'S': {**base, 'x': {}}}, ctx.ids, {'OP1'}, R.statics(ctx, ctx.centre))['OP1']) == [(None, 'single', (), None)]
    with pytest.raises(R.RunnerError, match='once_not_per_schedule'):
        R.samples({'S': {**base, 'x': {}}}, ctx.ids, frozenset(), R.statics(ctx, ctx.centre))

