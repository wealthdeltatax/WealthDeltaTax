"""Brief 110c block 1: the cell inputs partition the pack, the band income mean is kept, the gaps are reported."""
import pytest

import numpy as np

from model_v3.core import kernel as kn, pack as pk
from model_v3.runner import cell_baseline as cb
from conftest import REPO

PACK = pk.load_pack(REPO / 'model_v3' / 'pack' / 'GBR')
REG = pk.load_register(REPO / 'registry' / 'inputs.json')
close = lambda a, b, t=1e-9: abs(a - b) <= t * max(1.0, abs(b))


def test_ten_cells_and_the_pack_totals():
    cells = cb.build_cells(PACK, REG)
    assert [c['cell'] for c in cells] == [f'{b}|{s}' for b in cb.BANDS for s in cb.STAGES]
    assert sum(c['persons'] for c in cells) == sum(r['persons'] for r in PACK.tables['cell_weights'])
    deciles = sum(r['value'] for r in PACK.tables['wealth_distribution'] if r['variable'] == 'wealth_total' and r['band'] != 'all')
    assert close(sum(c['wealth'] for c in cells), deciles) and close(sum(sum(c['pos'].values()) for c in cells), deciles)
    assert close(sum(c['households_k'] for c in cells), 26991.0)


def test_class_shares_follow_the_band_composition():
    for c in cb.build_cells(PACK, REG):
        assert close(sum(c['pos'].values()), c['wealth'])
    d45 = next(c for c in cb.build_cells(PACK, REG) if c['cell'] == 'D4-5|retired')
    assert close(d45['pos']['property'] / d45['wealth'], 37.5 / 100.1)


@pytest.mark.parametrize('f', [0.4, 0.6, 0.8])
def test_band_mean_income_is_kept_and_retired_is_the_fraction(f):
    cells = {c['cell']: c for c in cb.build_cells(PACK, REG, retired_fraction=f)}
    for b, i in cb.INCOME_ID.items():
        hh = cells[f'{b}|retired']['households_k'] + cells[f'{b}|not retired']['households_k']
        tot = cells[f'{b}|retired']['income'] + cells[f'{b}|not retired']['income']
        assert close(tot * 1e9 / (hh * 1e3), REG[i].central)
        assert close(cells[f'{b}|retired']['income_per_hh'], f * cells[f'{b}|not retired']['income_per_hh'])


def test_lowest_band_takes_the_d4_5_low_bound():
    assert cb.band_income(REG, 'D1-3') == REG['I-D9a'].low == 40200.0
    assert cb.band_income(REG, 'D1-3', 'high') == 40200.0 and cb.band_income(REG, 'D10', 'high') == REG['I-D9d'].high


def test_retired_fraction_out_of_range_fails():
    with pytest.raises(ValueError, match='retired_fraction'):
        cb.build_cells(PACK, REG, retired_fraction=0.0)


def test_reconcile_reports_the_gaps_and_is_deterministic():
    cells = cb.build_cells(PACK, REG)
    a, b = cb.reconcile(cells, PACK, 1883.195, 100.0), cb.reconcile(cb.build_cells(PACK, REG), PACK, 1883.195, 100.0)
    assert a == b and close(a['wealth_cells'], a['wealth_deciles']) and close(a['income_cells'] / 1883.195 - 1, a['income_gap_pct'] / 100)
    assert a['persons'] == sum(r['persons'] for r in PACK.tables['cell_weights'])


def test_scaling_hits_the_target_and_keeps_proportions():
    cells = cb.build_cells(PACK, REG)
    s = cb.scale_income(cells, 1883.195)
    assert close(sum(c['income'] for c in s), 1883.195) and close(sum(c['wealth'] for c in s), sum(c['wealth'] for c in cells))
    assert close(s[2]['income'] / s[0]['income'], cells[2]['income'] / cells[0]['income'])
    assert close(s[1]['income_per_hh'] / s[0]['income_per_hh'], cells[1]['income_per_hh'] / cells[0]['income_per_hh'])


SC = dict(arm='new', s=0.0713, g=dict(property=0.0265, equity=0.0, financial=0.052, physical=0.0, pension=0.052), y=dict(property=0.038), pen=0.0112, gdp_g=0.0182, r=0.0474, c=0.035)
CELLS = cb.scale_income(cb.build_cells(PACK, REG), 1801.414)


def test_identity_closes_every_year_in_a_and_b_and_they_agree():
    a, b = cb.run_cells(CELLS, SC, 100, 'A'), cb.run_cells(CELLS, SC, 100, 'B')
    assert max(r['resid'] for r in a + b) < 1e-9 and len(a) == 1010
    assert max(abs(x['dNW'] - y['dNW']) for x, y in zip(a, b) if x['year'] == 1) < 1e-9   # one step: the same dNW; later years differ in where the yield sits


def test_legacy_arm_equals_the_kernels_growth_and_consumption():
    rows = cb.run_cells(CELLS, dict(SC, arm='legacy'), 100)
    book = kn.Book(10, {'A': np.array([c['wealth'] for c in CELLS])})
    for t in range(1, 101):
        kn.grow_and_consume(book, SC['r'], SC['c'])
        assert np.allclose([r['nw'] for r in rows if r['year'] == t], book.family_true(), rtol=1e-12, atol=0)


def test_run_is_deterministic_and_aggregate_has_every_band():
    a, b = cb.run_cells(CELLS, SC), cb.run_cells(CELLS, SC)
    assert a == b
    g = cb.aggregate(a, (0, 10, 100), 2211.48, 0.0182)
    assert [r['year'] for r in g] == [0, 10, 100] and abs(g[0]['wealth_over_gdp_index'] - 1) < 1e-12
    assert abs(sum(v for k, v in g[2].items() if k.startswith('share_')) - 1) < 1e-12
