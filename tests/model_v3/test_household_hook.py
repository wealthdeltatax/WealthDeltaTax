"""Brief 117c (W5a): the household arm's line state and its debt rule (block 1), the hook and its equivalence with cells.run_cell (blocks 2 and 3)."""
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import base as bs, pack as pk
from model_v3.runner import arm

ROOT = Path(__file__).resolve().parents[2]
PACK, REG = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
BASE = bs.build_base(PACK, REG, 1.0)
COMP = PACK.tables['decile_composition']
ST = arm.line_state(BASE, COMP, REG, 0.0101)
GAIN = dict(property=0.016455, net_financial=0.0094, physical=0.0, pension=0.0094)


def test_class_balances_sum_to_line_wealth_and_d1_keeps_its_negative_shares():
    assert all(a.shape == (14,) for a in (*ST['pos'].values(), ST['income'], ST['sav'], ST['acc']))
    assert np.allclose(sum(ST['pos'].values()), BASE.wealth, rtol=2e-4, atol=0)
    assert ST['pos']['property'][0] == pytest.approx(-0.0472 * BASE.wealth[0]) and ST['pos']['net_financial'][0] == pytest.approx(-1.0492 * BASE.wealth[0])


def test_tail_lines_carry_the_d10_mix_and_the_incomes_are_the_band_means():
    sh = {k: v / BASE.wealth for k, v in ST['pos'].items()}
    assert all(np.allclose(sh[k][9:], sh[k][9]) for k in sh) and sh['pension'][9] == pytest.approx(0.364) and sh['pension'][3] == pytest.approx(0.3614)
    per = REG['I-D4h'].central * 1e6
    assert ST['income'][0] == pytest.approx(REG['I-D9a'].low / per) and ST['income'][3] == pytest.approx(REG['I-D9a'].central / per) and ST['income'][13] == pytest.approx(REG['I-D9d'].central / per)
    assert np.allclose(arm.line_state(BASE, COMP, REG, 0.0101, scale=1.3733)['income'], 1.3733 * ST['income']) and ST['acc'][0] == REG['I-D1k'].central / 100 and (ST['sav'] == 0.0101).all()


def test_the_debt_rule_gives_a_negative_property_or_net_financial_balance_no_return():
    g = arm.returns(ST['pos'], GAIN)
    assert g['net_financial'][0] == 0.0 and g['property'][0] == 0.0 and (g['physical'] == 0.0).all()
    assert (g['net_financial'][ST['pos']['net_financial'] >= 0] == GAIN['net_financial']).all() and (g['pension'] == GAIN['pension']).all() and (g['property'][5:] == GAIN['property']).all()
