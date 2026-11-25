"""Brief 139c block 2: the arm reads the register's scenario rows. The lien rate (I-D1m) defaults to the register central and reaches the kernel's `r_def`; the housing gain (I-D1o) is the register central, equal to the old constant; the pension basis
(I-D1n) is off by default (`ons`, 1.00) and scales the opening pension stock only when switched on; the household arm runs 10 death phases and the legacy arm is untouched."""
import importlib.util
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from model_v3.runner import arm as ab, runner as R, switches as sw

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'docs' / 'model-v3' / 'household-arm-run' / 'run_grid.py'


@pytest.fixture(scope='module')
def grid():
    spec = importlib.util.spec_from_file_location('run_grid_139', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ctx, inp = mod.A.setup()
    return mod, mod.point_ctx(ctx, inp, 'median_mid')


def with_arm(c, **extra):
    return replace(c, arm={**c.arm, **extra})


def test_the_rows_hold_the_values_the_arm_reads(grid):
    _, c = grid
    m, n, o = (c.reg[i] for i in ('I-D1m', 'I-D1n', 'I-D1o'))
    assert (m.low, m.central, m.high) == (0.0, 2.0, 3.0) and (n.low, n.central, n.high) == (1.0, 1.96, 2.02)
    assert sw.housing_gain(c) == 0.016455 and o.low < o.central < o.high


def test_the_default_household_arm_reads_the_register_central_and_says_so(grid):
    mod, c = grid
    s = ab.build(c.arm, c, c.centre, R.shaped(c, c.centre, mod.A.SPEC['ratio'])).label['scenario']
    assert (s['lien_rate'], s['lien_rate_point'], s['pension_basis'], s['pension_multiplier'], s['death_phases'], s['housing_gain']) == (0.02, 'central', 'ons', 1.0, 10, 0.016455)
    assert R.env_of(c, c.centre).lam['r_def'] == 0.02 and sw.phase_kw(c.arm) == {'n_phase': 10}


@pytest.mark.parametrize('point, rate', [('low', 0.0), ('central', 0.02), ('high', 0.03)])
def test_the_lien_rate_switch_reaches_the_kernels_deferral_rate(grid, point, rate):
    _, c = grid
    assert R.env_of(with_arm(c, lien_rate=point), c.centre).lam['r_def'] == rate


def test_the_legacy_arm_gets_no_lien_rate_and_keeps_six_phases(grid):
    _, c = grid
    leg = replace(c, arm='legacy')
    assert sw.lien_kw(leg) == {} and sw.phase_kw('legacy') == {} and 'r_def' not in R.env_of(leg, leg.centre).lam


def test_the_pension_basis_scales_the_opening_pension_stock_only_when_switched_on(grid):
    mod, c = grid
    b = R.shaped(c, c.centre, mod.A.SPEC['ratio'])
    st = lambda **x: ab.build(with_arm(c, **x).arm, c, c.centre, b).make().st
    off, on, high = st(), st(pension_basis='ifs'), st(pension_basis='ifs_high')
    assert np.array_equal(off['pos']['pension'], st(pension_basis='ons')['pos']['pension'])
    assert np.allclose(on['pos']['pension'], off['pos']['pension'] * 1.96) and np.allclose(high['pos']['pension'], off['pos']['pension'] * 2.02)
    assert all(np.array_equal(on['pos'][k], off['pos'][k]) for k in ('property', 'net_financial', 'physical')) and np.array_equal(on['income'], off['income'])


@pytest.mark.parametrize('key, bad', [('lien_rate', 'zero'), ('pension_basis', 'gilt')])
def test_an_unknown_setting_raises(grid, key, bad):
    mod, c = grid
    with pytest.raises(ValueError, match=key):
        ab.build(with_arm(c, **{key: bad}).arm, c, c.centre, R.shaped(c, c.centre, mod.A.SPEC['ratio']))
