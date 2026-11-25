"""Brief 138c block 2: the fund_return switch. `safe` (the default) is byte-identical to the run without the key; `market` credits the fund at the path's market return and says so in the label."""
import importlib.util
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from model_v3.runner import runner as R, switches as sw

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'model' / 'studies' / 'household-arm-run' / 'run_grid.py'


@pytest.fixture(scope='module')
def runs():
    spec = importlib.util.spec_from_file_location('run_grid_sw', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ctx, inp = mod.A.setup()
    g = np.vstack([np.full((R.T // 2, 3), 0.0474), np.full((R.T - R.T // 2, 3), -0.03)]) + np.array([0.0, 0.01, -0.01])
    c0 = mod.point_ctx(ctx, inp, 'median_mid')
    out = {}
    for name, extra in (('default', {}), ('safe', dict(fund_return='safe')), ('market', dict(fund_return='market'))):
        c = replace(c0, arm={**c0.arm, **extra})
        out[name] = R.core_run(c, c.centre, mod.A.SPEC, g, np.full(g.shape, c.gdp_g))
    return out, g


def test_safe_is_byte_identical_to_the_run_without_the_switch(runs):
    r, _ = runs
    assert r['safe'].arm == r['default'].arm and 'fund_return' not in r['default'].arm['scenario']
    for k in ('M1', 'M1c', 'S_gdp', 'P6'):
        a, b = r['default'].r[k], r['safe'].r[k]
        assert all(np.array_equal(a[x], b[x]) for x in a) if isinstance(a, dict) else np.array_equal(a, b)


def test_market_credits_the_fund_at_the_paths_market_return_and_is_labelled(runs):
    r, g = runs
    led = r['market'].run['ledger']
    assert all(np.array_equal(v, g) for v in led['rk'].values()) and r['market'].arm['scenario']['fund_return'] == 'market' and 'market return' in r['market'].arm['safe_return']
    assert not np.allclose(r['safe'].run['ledger']['rk']['net_financial'], g)                           # the stand-in is the net financial class return
    assert not np.array_equal(r['market'].r['S_gdp'], r['safe'].r['S_gdp']) and (r['market'].r['S_gdp'][9] > r['safe'].r['S_gdp'][9]).all()
    f = r['market'].r['fund']
    d = np.diff(np.vstack([np.zeros((1, g.shape[1])), f['L']['net_financial']]), axis=0) if isinstance(f['L'], dict) else None
    assert d is None or np.abs(d - (f['rc']['net_financial'] + f['ret']['net_financial'] - f['pay']['net_financial'])).max() < 1e-9      # the fund's own ledger closes


def test_an_unknown_setting_raises():
    with pytest.raises(ValueError, match='fund_return'):
        sw.fund_return(dict(fund_return='high'))
