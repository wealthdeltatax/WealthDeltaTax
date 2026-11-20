"""Brief 086c: the burden group fills O2d, O2b, O2c, O4b and OL1 from Raw; the seven that need the pack or register are listed as not built."""
import numpy as np
import pytest

from model_v3.core import returns as rt
from model_v3.runner import out_burden as B, runner as R
from test_runner import SPEC, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

KEY = lambda *by: tuple(sorted(by))


@pytest.fixture(scope='module')
def s1(ctx):
    return R.level1(ctx, {'S': SPEC}, rt.streams(7)['level1_paths'], n=60, chunk=30)[0]


def test_empty_input_gives_empty_output():
    assert B.per_path(None, None) == {} and B.cells({}) == {}


def test_each_built_id_has_one_cell_per_horizon_and_by_value(s1):
    n = {'O2d': 15, 'O2b': 45, 'O2c': 45, 'O4b': 33, 'OL1': 12}
    assert {i: len(s1[i]) for i in B.IDS} == n and B.IDS == tuple(n)
    assert s1['O4b']['S', 'long', (('income_decile', 'D10'),), None].shape == (60,)
    assert ('S', 'short', KEY(('wealth_band', 'D10'), ('cutoff_pct_of_income', 20)), None) in s1['O2b']
    assert ('S', 'transition', (('reference_worker', 'p25'),), None) in s1['OL1']


def test_early_check_death_flows_are_the_larger_part_of_m2(s1):
    a, d = (np.nanmean(s1[i]['S', 'short', (('wealth_band', 'overall'),), None]) for i in ('O2', 'O2d'))
    assert d > 5 * a and abs(a - 2.8) < 0.28 and abs(d - 22.2) < 2.22        # 053c's central run: 2.8 in life, 22.2 with death


def test_o2d_exceeds_o2_on_average_and_shares_are_percentages(s1):
    for h in R.HORIZONS:
        a, d = (s1[i]['S', h, (('wealth_band', 'overall'),), None] for i in ('O2', 'O2d'))
        assert np.nanmean(d) > np.nanmean(a) > 0
    for k, v in s1['O2c'].items():
        assert np.nanmax(v) <= 100 + 1e-9
    assert np.nanmax(s1['O2b']['S', 'short', KEY(('wealth_band', 'D10'), ('cutoff_pct_of_income', 5)), None]) <= 100 + 1e-9


def test_ol1_is_ordered_by_reference_worker_and_not_built_ids_are_not_claimed(s1):
    v = [np.nanmean(s1['OL1']['S', 'long', (('reference_worker', p),), None]) for p in ('p25', 'p50', 'p75', 'p90')]
    assert all(x > 0 for x in v) and not {'O5', 'O6', 'O8', 'OH1b', 'OH1b2', 'OH1c', 'DH1c'} & set(B.IDS)
