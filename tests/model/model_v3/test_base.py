"""Tests B1 to B6 of architecture.md 6.2 for core/base.py (briefs 051c and 073c), on the UK pack and the register. No number is typed: each is read from the pack, the register or levers.json."""
import copy
import dataclasses
import json
import re
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs
from model_v3.core import pack as pk

ROOT = Path(__file__).parents[3]
RATIOS = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())['axes']['threshold_ratio']


@pytest.fixture(scope='module')
def env():
    pack, reg = pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
    return pack, reg, bs.build_base(pack, reg, RATIOS[1])


def cell(pack, v, b):
    return pk.lookup(pack, 'wealth_distribution', variable=v, band=b)[0]['value']


def test_b1_band_shares_partition_and_equal_the_pack_totals(env):
    pack, reg, b = env
    total = cell(pack, 'wealth_total', 'all')
    s1, extra = (reg[bs.IDS['tail'][k]].central / 100 for k in ('s1', 'extra'))
    assert b.weights.sum() == pytest.approx(1, abs=1e-12) and (b.weights > 0).all()
    assert b.wealth_bn.sum() == pytest.approx(total * (1 + extra), rel=1e-12)                        # the survey total plus the missing wealth (073c)
    assert b.households_k.sum() == pytest.approx(cell(pack, 'households', 'all'), rel=1e-12)
    dec = np.array([cell(pack, 'wealth_total', f'D{i}') for i in range(1, 11)])
    assert np.allclose(b.wealth_bn[:9], dec[:9] * total / dec.sum(), rtol=1e-12, atol=0)             # the survey body is unchanged
    assert b.wealth_bn[9] + s1 * total == pytest.approx(dec[9] * total / dec.sum(), rel=1e-12)       # D10a and the survey top 1% make D10
    assert b.wealth_to_gdp == pytest.approx(total * (1 + extra) / cell(pack, 'gdp', 'all'))
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
    assert list(b.V0) == list(bs.ROUTES) and all(v.shape == (len(bs.LABELS),) for v in b.V0.values())
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


def test_b6_the_tail_follows_the_register(env):
    pack, reg, b = env
    g = {k: reg[i].central for k, i in bs.IDS['tail'].items()}
    total, n = cell(pack, 'wealth_total', 'all'), int(g['n'])
    assert len(bs.LABELS) == 14 and b.labels[-3:] == bs.TIERS
    assert b.adults_k[-3:].sum() * 1e3 == pytest.approx(n, rel=1e-12)                                   # the tier members sum to the list
    assert b.wealth_bn[-3:].sum() == pytest.approx(g['list_bn'], rel=1e-12)                             # and the tiers to the list total
    pareto = lambda lo, hi: g['list_bn'] * ((hi / n) ** (1 - 1 / g['alpha']) - (lo / n) ** (1 - 1 / g['alpha']))
    ranks = [0] + [round(f * n) for f in (g['cut1'] / 100, g['cut2'] / 100, 1)]
    assert np.allclose(b.wealth_bn[-3:], [pareto(lo, hi) for lo, hi in list(zip(ranks, ranks[1:]))[::-1]], rtol=1e-12, atol=0)
    top1 = b.wealth_bn[10:].sum()                                                                       # the top 1% after the addition
    assert (top1 - g['extra'] / 100 * total) / total == pytest.approx(g['s1'] / 100, rel=1e-12)          # I-D4d is the survey's share of the survey total, as in v2
    assert b.wealth_bn[10] == pytest.approx(top1 - g['list_bn'], rel=1e-12)                             # the list is inside the top 1%, not on top of it
    assert b.households_k[10:].sum() == pytest.approx(0.1 * b.households_k[9:].sum(), rel=1e-12)       # the top 1% of D10's households, split into D10b and the list


def test_b6_v2s_own_constants_reproduce_v2s_tiers_by_hand():
    # v2 (WDT_Params.toml [rates.dist.advani]): survey 14,400bn, top 10% 51%, top 1% 18%, 5% extra, 1,000 entries, 700bn, alpha 1.5, cuts 1%, 10%, 100%.
    t = bs.tail(14400, 0.51 * 14400, 0.18, 0.05, 1000, 700, 1.5, [0.01, 0.1, 1.0])
    assert list(t['tier_n']) == [900, 90, 10]                                                           # ranks 10, 100, 1000
    # b = 1 - 1/1.5 = 1/3; 0.1^(1/3) = 0.4641589, 0.01^(1/3) = 0.2154435: 700 x (1 - 0.4641589), 700 x (0.4641589 - 0.2154435), 700 x 0.2154435
    assert t['tier_bn'] == pytest.approx([375.0888, 174.0998, 150.8104], abs=1e-3) and t['tier_bn'].sum() == pytest.approx(700)
    assert t['d10a_bn'] == pytest.approx(0.33 * 14400)                                                  # 90th to 99th percentile: (0.51 - 0.18) x 14,400 = 4,752
    assert t['d10b_bn'] == pytest.approx(0.18 * 14400 + 0.05 * 14400 - 700)                             # top 1% 3,312 less the list = 2,612
    assert t['total_bn'] == pytest.approx(15120)                                                        # 14,400 x 1.05


@pytest.mark.parametrize('kw,match', [(dict(alpha=1), 'alpha'), (dict(list_bn=1e9), 'exceeds the top 1%'), (dict(cuts=[0.1, 0.1, 1.0]), 'ranks'),
                                      (dict(cuts=[0.5, 1.0]), 'tiers'), (dict(s1=0.6), 'top 10%')])
def test_b6_a_tail_that_does_not_hold_fails(kw, match):
    args = dict(total_bn=14400, d10_bn=7344, s1=0.18, extra=0.05, n=1000, list_bn=700, alpha=1.5, cuts=[0.01, 0.1, 1.0])
    with pytest.raises(bs.BaseError, match=match):
        bs.tail(**{**args, **kw})


def test_b6_base_py_keeps_no_v2_constant():
    assert not re.search(r'\b(0\.18|0\.51|700|1000)\b', (ROOT / 'model' / 'model_v3' / 'core' / 'base.py').read_text())
