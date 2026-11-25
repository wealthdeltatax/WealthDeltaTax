"""The recorded v2 run at logistic_ln_ref (brief 078c): the fixture is complete and agrees with itself. v2 is not run or imported here."""

import json
from pathlib import Path

import numpy as np
import pytest

FIXTURE = Path(__file__).parent / 'fixtures' / 'v2_logistic_ln_ref.json'


@pytest.fixture(scope='module')
def ref():
    return json.loads(FIXTURE.read_text())


def test_windows_and_headline(ref):
    w = ref['windows']
    assert len(w) == ref['headline']['n_windows'] == 117
    assert len({r['start'] for r in w}) == 117 and not any(r['censored'] for r in w)
    x = np.array([r['wdt_gdp_h'] for r in w])
    assert abs(100 * x.mean() - ref['headline']['wdt_gdp_h_mean_pct_of_gdp']) < 1e-9
    assert abs(100 * np.median(x) - ref['headline']['wdt_gdp_h_median_pct_of_gdp']) < 1e-9
    assert round(ref['headline']['wdt_gdp_h_mean_pct_of_gdp'], 2) == 7.34        # the recorded headline is the mean; the median is 6.59
    assert round(ref['headline']['wdt_gdp_h_median_pct_of_gdp'], 2) == 6.59


def test_distribution_table(ref):
    c = ref['calibration']
    assert len(c['cells']) == c['n_cells'] == 41
    assert abs(sum(x['wealth_bn'] for x in c['cells']) - c['total_bn']) < 1e-6
    assert abs(sum(x['adult_share'] for x in c['cells']) - 1) < 1e-9
    assert all(abs(x['adult_share'] * c['n_adults'] * x['mean_gbp_m'] / 1e3 - x['wealth_bn']) < 1e-6 * max(1, x['wealth_bn']) for x in c['cells'])
    assert abs(c['wmin_gbp_m'] - c['wmin_house_ratio'] * c['house_median_gbp_m']) < 1e-12
    assert round(c['wealth_to_gdp'], 6) == round(c['total_bn'] / c['gdp_bn'], 6)


def test_series_and_provenance(ref):
    g = ref['gpc_real']
    assert len(g['years']) == len(g['values']) and g['years'][-1] - g['years'][0] == len(g['years']) - 1
    assert ref['settings']['cfg']['schedule'] == 'logistic_ln' and ref['settings']['cfg']['c'] == 0.035
    assert len(ref['settings']['toml_sha256']) == 64 and ref['_meta']['command'] and ref['_meta']['repo_commit']
