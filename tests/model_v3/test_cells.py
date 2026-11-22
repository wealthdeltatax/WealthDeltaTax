"""Brief 110c: the untaxed cell baseline. Ten cells, the identity in every year, the legacy arm equal to the kernel's, determinism."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import cells as ce, kernel as kn, pack as pk

ROOT = Path(__file__).resolve().parents[2]
PACK, REG = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
RETS = dict(g=dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094), y=dict(property=0.03758, net_financial=0.0426, physical=0.0, pension=0.0426))
CELLS = ce.cell_table(PACK, REG, 0.44)


def test_ten_cells_carry_the_pack_households_wealth_and_the_register_income():
    assert [c['cell'] for c in CELLS][:2] == ['D1-3|not retired', 'D1-3|retired'] and len(CELLS) == 10
    assert sum(c['households'] for c in CELLS) == pytest.approx(1e3 * 26991) and sum(c['households'] * sum(c['pos'].values()) for c in CELLS) * ce.UNIT / 1e9 == pytest.approx(13568.0, rel=1e-3)
    inc = {c['cell']: c['income'] * ce.UNIT for c in CELLS}
    assert inc['D1-3|not retired'] == REG['I-D9a'].low and inc['D6-7|not retired'] == REG['I-D9b'].central and inc['D10|retired'] == pytest.approx(0.44 * REG['I-D9d'].central)
    assert all(c['pos']['debt'] == 0.0 for c in CELLS)


@pytest.mark.parametrize('sav,acc', [(-0.026, 0.0041), (0.01, 0.0112), (0.135, 0.0184)])
def test_the_identity_holds_in_every_year_of_every_cell(sav, acc):
    for c in CELLS:
        rows, pos0 = ce.run_cell(c, 100, sav, acc, 0.0157, RETS), c['pos']
        before = sum(pos0[k] for k in ce.CLASSES)
        for t, pos, a in rows:
            after = sum(pos[k] for k in ce.CLASSES)
            assert abs((after - before) - (a['S'] + a['CG'] + a['O'] - a['T_WDT'])) < 1e-9 and abs(a['dNW'] - (after - before)) < 1e-9
            before = after


def test_the_legacy_arm_reproduces_the_kernels_legacy_path_on_the_same_cells():
    r, c = 0.0474, 0.035
    book = kn.Book(len(CELLS), {'A': np.array([sum(x['pos'][k] for k in ce.CLASSES) for x in CELLS])})
    paths = [ce.run_cell(x, 100, 0.0, 0.0, 0.0157, dict(r=r), 'legacy', c) for x in CELLS]
    for t in range(100):
        kn.grow_and_consume(book, r, c)
        assert np.allclose([sum(p[t][1][k] for k in ce.CLASSES) for p in paths], book.family_true(), rtol=1e-12, atol=0)


def test_a_run_is_deterministic():
    a = [ce.run_cell(c, 100, 0.01, 0.0112, 0.0157, RETS) for c in CELLS]
    b = [ce.run_cell(c, 100, 0.01, 0.0112, 0.0157, RETS) for c in CELLS]
    assert all(np.array_equal(x[1][k], y[1][k]) for ra, rb in zip(a, b) for x, y in zip(ra, rb) for k in ce.CLASSES)


def test_scaling_fixes_the_income_total_and_keeps_the_proportions():   # 111c
    sc, k = ce.scaled(CELLS, 1.8014e12)
    assert sum(c['households'] * c['income'] for c in sc) * ce.UNIT == pytest.approx(1.8014e12, rel=1e-12) and k > 1
    assert all(a['income'] / b['income'] == pytest.approx(k) and a['pos'] == b['pos'] and a['households'] == b['households'] for a, b in zip(sc, CELLS))
    assert sc[1]['income'] / sc[0]['income'] == pytest.approx(0.44)


def test_the_accrual_in_year_one_is_the_share_times_the_income_total():   # 111c
    sc, _ = ce.scaled(CELLS, 1.8014e12)
    accrual = sum(c['households'] * (ce.run_cell(c, 1, 0.0101, 0.0483, 0.0157, RETS)[0][2]['S'] - 0.0101 * c['income']) for c in sc) * ce.UNIT
    assert accrual == pytest.approx(0.0483 * 1.8014e12, rel=1e-9)

