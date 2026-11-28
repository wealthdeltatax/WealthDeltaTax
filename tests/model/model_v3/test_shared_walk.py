"""Brief 152c: under the household arm the years are walked once (the ledger's walk feeds the burden's line flows through `burden.Tap`); the flows are those of the burden's own walk (`burden.line_flows`), to the last byte."""
import json
from dataclasses import replace

import numpy as np
import pytest

from model_v3.core import burden as bd
from model_v3.runner import arm as ab, runner as R, switches as sw
from test_heads_only import EPS, INP, SPECS
from test_pool import raw
from test_runner import ctx, lv, out, tier1  # noqa: F401  (the fixtures)


@pytest.mark.parametrize('spec', SPECS)
def test_the_household_flows_from_the_shared_walk_equal_the_burdens_own_walk_byte_for_byte(ctx, spec):
    cp, seen = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median', regime='mid')), []
    orig = R.core_run
    R.core_run = lambda *a, **k: seen.append((a, orig(*a, **k))) or seen[-1][1]
    try:
        R.make_ev(cp, EPS, heads=True)(spec)
    finally:
        R.core_run = orig
    (_, theta, _, g, gdp_g), rw = seen[0][0][:5], seen[0][1]
    ar = ab.build(cp.arm, cp, theta, rw.base, g, gdp_g)
    own = bd.line_flows(rw.base, rw.rate, g, gdp_g, ar.c, hook=ar.make(), **{**R.env_of(cp, theta).lam, **sw.phase_kw(cp.arm)})
    assert raw(rw.fl) == raw(own)
