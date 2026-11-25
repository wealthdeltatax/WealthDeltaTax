"""Brief 136c: the helpers and the stored table of model/studies/household-vs-legacy/flows.py (diagnosis only, no model change)."""
import csv
import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
HVL = ROOT / 'docs' / 'model-v3' / 'household-vs-legacy'


def rows():
    return list(csv.DictReader(open(HVL / 'flows.csv')))


def test_phases_averages_the_six_death_phases_of_a_line():
    spec = importlib.util.spec_from_file_location('hvl_flows', ROOT / 'model' / 'studies' / 'household-vs-legacy' / 'flows.py')
    sys.path[:0] = [str(ROOT), str(ROOT / 'model' / 'studies' / 'household-arm-account'), str(ROOT / 'model' / 'studies' / 'household-arm-run')]
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    x = np.arange(6 * 3 * 14, dtype=float).reshape(6 * 3, 14)
    out = m.phases(x)
    assert out.shape == (3, 14) and np.allclose(out[1, 2], np.mean([x[p * 3 + 1, 2] for p in range(6)]))


def test_the_legacy_rows_depreciate_at_the_arms_own_c_and_the_household_account_closes():
    r = rows()
    assert {x['arm'] for x in r} == {'legacy', 'household'} and {x['point'] for x in r} == {'all', 'median_mid', 'max_mid', 'median_low'}
    assert max(abs(float(x['c_eq_pre_tax']) - 0.035) for x in r if x['arm'] == 'legacy') < 1e-9               # W(1 + g)(1 - c), c = I-D14c, before tax
    assert max(abs(float(x['resid_share'])) for x in r if x['arm'] == 'household') < 1e-9
    assert all(np.isnan(float(x['S_share'])) for x in r if x['arm'] == 'legacy')                                 # the legacy arm has no saving account


def test_every_row_carries_its_scenario_label():
    assert all(x['label'] for x in rows())


def decomp():
    d = {}
    for r in csv.DictReader(open(HVL / 'decomp.csv')):
        d[(r['case'], r['output'], r['horizon'], r['band'], r['term'])] = float(r['value'])
    return d


def test_the_decomposition_reproduces_the_124c_values_in_every_case_that_has_them():
    d = decomp()
    pairs = [(k, v, d[k[:4] + ('reported_124c',)]) for k, v in d.items() if k[4] == 'value' and k[:4] + ('reported_124c',) in d and np.isfinite(v)]
    assert len(pairs) > 100 and max(abs(v - w) / max(abs(w), 1e-9) for _, v, w in pairs) < 1e-9


def test_the_ratio_to_legacy_is_exactly_base_ratio_times_rate_ratio_on_the_common_ground():
    d = decomp()
    on_common = [(k, v) for k, v in d.items() if k[0].endswith('/ common:legacy') and k[4] == 'ratio_interaction' and np.isfinite(v)]
    assert len(on_common) > 20 and max(abs(v - 1.0) for _, v in on_common) < 1e-9
    stoch = [v for k, v in d.items() if k[0].endswith('/ stoch:legacy') and k[4] == 'ratio_interaction' and np.isfinite(v)]
    assert stoch and all(0.2 < v < 5 for v in stoch)                                                    # the error of means of terms on the legacy arm's own paths is reported, and bounded
