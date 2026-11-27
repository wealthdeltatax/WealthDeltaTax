"""Brief 151c: the headline-only evaluator (`make_ev(..., heads=True)`) returns exactly the headline keys of the full evaluator, to the last byte, on both arms."""
import json
from dataclasses import replace

import numpy as np
import pytest

from model_v3.runner import runner as R
from test_pool import raw
from test_runner import ROOT, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

INP = json.loads((ROOT / 'results' / 'cell-baseline' / 'inputs_used.json').read_text())
SPECS = [dict(tau_0=0.04, tau_m=0.5, k_ln=0.5, ratio=1.0), dict(tau_0=0.04, tau_m=0.9, k_ln=1.0, ratio=0.5), dict(tau_0=0.02, tau_m=0.7, k_ln=2.0, ratio=0.75)]
HEADS = {'M1', 'M1a', 'M1b', 'M1c', 'M1d', 'M2', 'M4a', 'M3', 'neg', 'P3h', 'P1', 'P7b', 'fill', 'unfilled', 'long_T'}
EPS = np.random.default_rng(151).standard_normal((R.T, 12))


@pytest.mark.parametrize('arm', ['legacy', 'household'])
def test_headline_only_equals_the_headline_keys_of_the_full_evaluator_byte_for_byte(ctx, arm):
    cp = ctx if arm == 'legacy' else replace(ctx, arm=dict(arm='household', inputs=INP, saving='median', regime='mid'))
    full, heads = R.make_ev(cp, EPS), R.make_ev(cp, EPS, heads=True)
    overrides = [{}, {R.RET['mean']: ctx.centre[R.RET['mean']] + 1.0}, {R.RET['sd']: ctx.centre[R.RET['sd']] * 1.2}]
    for spec in SPECS:
        for over in overrides:
            f, h = full(spec, over), heads(spec, over)
            assert set(h) == HEADS <= set(f) and set(f) - HEADS                      # no group result comes back; the full evaluator still has them
            assert all(raw(h[k]) == raw(f[k]) for k in HEADS), [k for k in HEADS if raw(h[k]) != raw(f[k])]
    g = np.full((R.T, 3), 0.012)                                                     # paths given instead of innovations
    assert all(raw(heads(SPECS[0], None, g)[k]) == raw(full(SPECS[0], None, g)[k]) for k in HEADS)


def test_the_default_evaluator_is_unchanged(ctx):
    assert R.make_ev(ctx, EPS)(SPECS[0]).keys() > HEADS


@pytest.mark.parametrize('arm', ['legacy', 'household'])
def test_the_sweeps_group_only_equals_the_full_evaluators_of1_and_headlines_byte_for_byte(ctx, arm):
    """186c: the feasibility map runs `only=('sweeps',)`; its OF1 result and the headlines are those of the full evaluator (the groups draw from their own named streams)."""
    cp = ctx if arm == 'legacy' else replace(ctx, arm=dict(arm='household', inputs=INP, saving='median', regime='mid'))
    full, part = R.make_ev(cp, EPS), R.make_ev(cp, EPS, only=('sweeps',))
    for spec in SPECS:
        f, p = full(spec), part(spec)
        assert set(p) == HEADS | {'sweeps'} and set(f) > set(p)                      # the other groups are not run
        assert raw(p['sweeps']) == raw(f['sweeps']) and all(raw(p[k]) == raw(f[k]) for k in HEADS)
