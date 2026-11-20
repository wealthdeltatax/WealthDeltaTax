"""Brief 084c: the output groups are named in one place, an empty group changes no number, and `samples` refuses a bad or doubled id."""
from types import SimpleNamespace as NS

import numpy as np
import pytest

from model_v3.core import returns as rt
from model_v3.runner import groups as G, runner as R
from test_runner import SPEC, ctx, level1, lv, out, tier1  # noqa: F401  (the fixtures)

PIN = 'ce75c164e99d70ca1088daa095a6335aa8bdfc63b5edbf5b8b9315f41a6c46cc'     # digest of 055c's Samples: seed 7, 40 paths, chunks of 20, SPEC
GROUP = lambda name, ids=(), cells=None: NS(NAME=name, IDS=ids, per_path=lambda raw, again: {}, cells=lambda e: cells or {})


def test_the_four_groups_are_named_explicitly_and_follow_the_interface():
    assert [m.NAME for m in G.GROUPS] == ['revenue', 'burden', 'support', 'sweeps']
    assert all(m.IDS == () and m.cells({}) == {} and m.per_path(None, None) == {} for m in G.GROUPS)


@pytest.mark.parametrize('m', G.GROUPS, ids=lambda m: m.NAME)
def test_an_empty_group_changes_no_number(m, ctx, monkeypatch):
    monkeypatch.setattr(R, 'GROUPS', (m,))
    assert R.digest(level1(ctx, 7)[0]) == PIN                  # the same bytes as before the split, for the same seed
    assert m.NAME in R.evaluate(ctx, ctx.centre, SPEC, R.paths(np.zeros((100, 3)), 4.7, 8.2, 0.3), np.full((100, 3), 0.015))


def test_again_reruns_the_core_with_a_changed_spec_once(ctx, monkeypatch):
    seen = []
    monkeypatch.setattr(R, 'GROUPS', (NS(NAME='x', IDS=(), per_path=lambda raw, again: seen.append((again({}) is again({}), again({'ratio': 1.0}) is again({'ratio': 1.0}),
                                                              again({'ratio': 1.0}).spec['ratio'])) or {}, cells=lambda e: {}),))
    R.evaluate(ctx, ctx.centre, SPEC, R.paths(np.zeros((100, 2)), 4.7, 8.2, 0.3), np.full((100, 2), 0.015))
    assert seen == [(True, True, 1.0)]


def test_samples_puts_the_schedule_in_front_and_refuses_a_bad_or_doubled_id(ctx, monkeypatch):
    base = R.evaluate(ctx, ctx.centre, SPEC, R.paths(np.zeros((100, 2)), 4.7, 8.2, 0.3), np.full((100, 2), 0.015))
    cell = {'OP1': {('short', (), None): np.zeros(2)}}
    monkeypatch.setattr(R, 'GROUPS', (GROUP('x', ('OP1',), cell),))
    base['x'] = {}
    assert list(R.samples({'S': base}, ctx.ids)['OP1']) == [('S', 'short', (), None)]
    for groups, why in (((GROUP('x', ('OP1',), cell), GROUP('y', ('OP1',), cell)), 'returned by'), ((GROUP('x', ('OP1',), {'ZZ9': {}}),), 'not in the manifest'),
                        ((GROUP('x', (), cell),), 'IDS')):
        monkeypatch.setattr(R, 'GROUPS', groups)
        with pytest.raises(R.RunnerError, match=why):
            R.samples({'S': {**base, 'y': {}}}, ctx.ids)
    with pytest.raises(R.RunnerError, match='manifest'):
        R.samples({'S': base}, {'O1'})
