"""Brief 110c block 1: the cell inputs partition the pack, the band income mean is kept, the gaps are reported."""
import pytest

from model_v3.core import pack as pk
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
