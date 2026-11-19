"""Tests R1 to R7 of architecture.md 6.2 for core/returns.py (brief 050c), on the UK pack and the register."""
import json
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import pack as pk
from model_v3.core import returns as rt

ROOT = Path(__file__).parents[2]
PIN = {'n': 117, 'arithmetic': 4.742, 'geometric': 4.420, 'sd': 8.219, 'lag1': 0.303}   # R1, re-derived on the pack series (sample ends 2019): n is unchanged
IDS = {'mean': 'I-D1a', 'sd': 'I-D1b', 'phi': 'I-D1b2'}


@pytest.fixture(scope='module')
def data():
    reg = pk.load_register(ROOT / 'registry' / 'inputs.json')
    years, r = rt.real_series(pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'))
    return years, r, rt.sample_stats(r), {k: reg[i] for k, i in IDS.items()}


def test_r1_sample_statistics_are_pinned_and_agree_with_the_register(data):
    years, _, st, rows = data
    assert years[0] == 1896 and years[-1] == 2019 and not {*range(1940, 1947)} & set(years)
    for k, v in PIN.items():
        assert st[k] == pytest.approx(v, abs=0.001)
    assert abs(st['arithmetic'] - rows['mean'].central) < 0.005 and abs(st['sd'] - rows['sd'].central) < 0.005 and abs(st['lag1'] - rows['phi'].central) < 0.005
    assert round(st['n_eff']) == 63


def test_r2_generator_reproduces_its_inputs_at_100000_paths(data):
    _, _, st, _ = data
    g = rt.ar1_paths(rt.streams()['level1_paths'], st['arithmetic'], st['sd'], st['lag1'], 100, 100_000) * 100
    assert abs(g.mean() - st['arithmetic']) < 0.05 and abs(g.std() - st['sd']) < 0.05
    assert abs((((g[:-1] - g.mean()) * (g[1:] - g.mean())).mean() / g.var()) - st['lag1']) < 0.02
    assert abs(g[0].mean() - st['arithmetic']) < 0.1 and abs(g[0].std() - st['sd']) < 0.1   # stationary start


def test_r3_same_seed_same_array_different_seed_different(data):
    _, _, st, _ = data
    a, b, c = (rt.ar1_paths(rt.streams(s)['level1_paths'], st['arithmetic'], st['sd'], st['lag1'], 20, 50) for s in (1, 1, 2))
    assert np.array_equal(a, b) and not np.array_equal(a, c)
    assert list(rt.streams()) == list(rt.STREAMS) and len(set(map(id, rt.streams().values()))) == 5
    s = rt.streams()
    assert s['level1_paths'].random() != s['level2_draws'].random()


def test_r4_bootstrap_mean_and_sd_within_0_1_of_the_sample(data):
    years, r, st, _ = data
    g = rt.block_bootstrap(rt.streams()['bootstrap_check'], years, r, 100, 20_000, 3) * 100
    assert abs(g.mean() - st['arithmetic']) < 0.1 and abs(g.std() - st['sd']) < 0.1
    g = rt.block_bootstrap(rt.streams()['bootstrap_check'], np.array([1, 2, 3, 10, 11]), np.array([0., 1, 2, 100, 101]), 50, 20_000, 3)
    after2 = g[1:][g[:-1] == 0.02]   # a block ending at year 3 wraps to year 1, not on to year 10: only a fresh block start reaches 100
    assert (after2 == 1.0).mean() < 0.2 < (after2 == 0.0).mean()


def test_r5_level2_band_reproduces_the_register_range(data):
    rows = data[3]
    d = rt.level2_draw(rt.streams()['level2_draws'], rows, 100_000)
    for k, row in rows.items():
        assert np.percentile(d[k], 10) == pytest.approx(row.low, abs=0.02) and np.percentile(d[k], 90) == pytest.approx(row.high, abs=0.02)
        assert abs(np.median(d[k]) - row.central) < 0.02


def test_r6_loop_windows_self_test():
    ys = list(range(1900, 1910))
    loop, flat = rt.loop_windows(ys, 4), rt.loop_windows(ys, 4, wrap=False)
    assert (len(loop), len(flat), sum(w['wraps'] for w in loop)) == (10, 7, 3) and not any(w['repeat'] for w in loop)
    assert loop[-1]['years'] == [1909, 1900, 1901, 1902] and loop[-1]['wraps'] and not loop[-1]['contiguous'] and all(w['contiguous'] for w in flat)
    assert all(w['repeat'] for w in rt.loop_windows(ys[:3], 5)) and rt.loop_windows([], 3) == []


def test_r6_the_real_series_has_117_windows_of_which_the_gap_breaks_some(data):
    w = rt.loop_windows([int(y) for y in data[0]], 100)
    assert len(w) == 117 and sum(x['wraps'] for x in w) == 99 and not any(x['contiguous'] for x in w)


def test_r7_nothing_is_clipped():
    rng = rt.streams()['level1_paths']
    with pytest.raises(ValueError, match='-100%'):
        rt.ar1_paths(rng, 5.0, 60.0, 0.3, 100, 2_000)
    with pytest.raises(ValueError):
        rt.ar1_paths(rng, 5.0, 8.0, 1.0, 10, 10)
    bad = {k: pk.Row('x', 0.1, 0.2, 5.0, '', False) for k in ('mean', 'sd', 'phi')}
    with pytest.raises(ValueError, match='not clipped'):
        rt.level2_draw(rng, bad, 1000)


def test_the_normal_quantile_is_accurate():
    from statistics import NormalDist
    u = np.array([1e-6, 0.001, 0.02, 0.1, 0.5, 0.9, 0.99, 1 - 1e-6])
    assert np.abs(rt._ppf(u) - [NormalDist().inv_cdf(x) for x in u]).max() < 1e-7
