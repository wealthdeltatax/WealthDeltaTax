"""Tests B1 to B5 of architecture.md 6.2 for core/base.py (brief 051c), on the UK pack and the register. No number is typed: each is read from the pack, the register or levers.json."""
import copy
import dataclasses
import json
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs
from model_v3.core import pack as pk

ROOT = Path(__file__).parents[2]
RATIOS = json.loads((ROOT / 'model_v3' / 'levers.json').read_text())['axes']['threshold_ratio']


@pytest.fixture(scope='module')
def env():
    pack, reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
    return pack, reg, bs.build_base(pack, reg, RATIOS[1])


def cell(pack, v, b):
    return pk.lookup(pack, 'wealth_distribution', variable=v, band=b)[0]['value']


def test_b1_band_shares_partition_and_equal_the_pack_totals(env):
    pack, _, b = env
    assert b.weights.sum() == pytest.approx(1, abs=1e-12) and (b.weights > 0).all()
    assert b.wealth_bn.sum() == pytest.approx(cell(pack, 'wealth_total', 'all'), rel=1e-12)
    assert b.households_k.sum() == pytest.approx(cell(pack, 'households', 'all'), rel=1e-12)
    dec = np.array([cell(pack, 'wealth_total', f'D{i}') for i in range(1, 11)])
    got = np.r_[b.wealth_bn[:9], b.wealth_bn[9:].sum()]
    assert np.allclose(got / got.sum(), dec / dec.sum(), rtol=0, atol=1e-12)
    tail = {r['series']: r['value'] for r in pk.lookup(pack, 'wealth_tail', year=max(r['year'] for r in pack.tables['wealth_tail']))}
    assert b.wealth_bn[10] / b.wealth_bn[9:].sum() == pytest.approx(tail['wid_top1'] / tail['wid_top10'], rel=1e-12)   # the split is the tail ratio
    assert b.wealth_to_gdp == pytest.approx(cell(pack, 'wealth_total', 'all') / cell(pack, 'gdp', 'all'))
    assert b.labels == bs.LABELS and b.G == 30


def test_b1_a_band_that_does_not_partition_fails(env):
    pack, reg, _ = env
    bad = copy.deepcopy(pack)
    next(r for r in bad.tables['wealth_distribution'] if r['variable'] == 'wealth_total' and r['band'] == 'D3')['value'] += 100
    with pytest.raises(bs.BaseError, match='partition'):
        bs.build_base(bad, reg, RATIOS[1])


@pytest.mark.parametrize('ratio', RATIOS)
def test_b2_w_min_is_the_lever_ratio_times_the_pack_median(env, ratio):
    pack, reg, _ = env
    assert bs.build_base(pack, reg, ratio).w_min == pytest.approx(ratio * cell(pack, 'median_house_price', 'all') / 1e6, rel=1e-12) == bs.w_min(pack, ratio)
    with pytest.raises(bs.BaseError):
        bs.w_min(pack, 0)


def test_b3_the_routes_sum_to_line_value_in_the_register_mix(env):
    _, reg, b = env
    assert list(b.V0) == list(bs.ROUTES) and all(v.shape == (11,) for v in b.V0.values())
    assert np.allclose(sum(b.V0.values()), b.wealth, rtol=1e-12, atol=0)
    for r, i in bs.IDS['route'].items():
        assert np.allclose(b.V0[r] / b.wealth, reg[i].central / 100, rtol=1e-12, atol=0)
    assert np.allclose(b.V0['A'] * b.adults_k, b.wealth_bn * reg[bs.IDS['route']['A']].central / 100, rtol=1e-12, atol=0)   # millions of pounds per adult x thousand adults = billions of pounds


def test_b3_a_route_mix_that_does_not_sum_to_100_fails(env):
    pack, reg, _ = env
    i = bs.IDS['route']['A']
    with pytest.raises(bs.BaseError, match='sum to 100'):
        bs.build_base(pack, {**reg, i: dataclasses.replace(reg[i], central=reg[i].central + 1)}, RATIOS[1])


def test_b4_income_and_liquid_assets_are_non_negative_and_ordered(env):
    _, _, b = env
    for x in (b.income, b.liquid, b.wealth):
        assert (x[np.isfinite(x)] >= 0).all()
    ok = np.isfinite(b.liquid)
    assert (np.diff(b.liquid[ok]) >= 0).all() and (np.diff(b.wealth) > 0).all()
    for v in b.income_deciles.values():
        assert len(v) == 10 and (v >= 0).all() and (np.diff(v) > 0).all()
    assert (b.liquid[ok] <= b.wealth[ok]).all()


def test_b4_a_payer_line_without_income_fails_and_a_non_payer_line_stays_nan(env):
    pack, reg, b = env
    assert np.isnan(b.income[:3]).all() and np.isfinite(b.income[3:]).all()   # below W_min: no source, not filled
    with pytest.raises(bs.BaseError, match='no source'):
        bs.build_base(pack, reg, 0.05)


def test_b5_two_builds_are_the_same(env):
    pack, reg, b = env
    c = bs.build_base(pack, reg, RATIOS[1])
    for f in dataclasses.fields(b):
        x, y = getattr(b, f.name), getattr(c, f.name)
        if isinstance(x, dict):
            assert all(np.array_equal(x[k], y[k], equal_nan=True) for k in x)
        elif isinstance(x, np.ndarray):
            assert np.array_equal(x, y, equal_nan=True)
        else:
            assert x == y
