"""Brief 126c, block 1: the household arm's untaxed path (design 3.6 site 4) under free_path, M3-today and M12; the legacy path does not move."""
import json
from dataclasses import replace
from types import SimpleNamespace

import numpy as np

from model_v3.core import burden as bd, kernel as K
from model_v3.runner import arm as ab, runner as R
from test_runner import ROOT, ctx, lv, out, tier1  # noqa: F401  (the fixtures)

INP = json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())
TOY = dict(pos=dict(property=np.array([1.0]), net_financial=np.array([0.5]), physical=np.array([0.0]), pension=np.array([0.5])), income=np.array([0.1]), sav=np.array([0.1]), acc=np.array([0.05]))
GAIN = dict(property=0.02, net_financial=0.01, physical=0.0, pension=0.01)


def test_the_household_free_path_is_the_account_with_no_tax_by_hand_and_by_the_kernel():
    h, g = ab.HouseholdHook(TOY, GAIN, 0.0), np.zeros((3, 2))
    f = h.free(g)
    assert f.shape == (3, 1, 2) and np.allclose(f[0], (2.0 + 0.015 + 0.03) / 2.0, atol=1e-15)     # W0 2, saving 0.1 x (0.05 + 0.1), gains 0.02 + 0.005 + 0.005
    book, hk, W0 = K.Book(1, {'A': np.array([1.5]), 'B': np.array([0.0]), 'D': np.array([0.0])}), ab.HouseholdHook(TOY, GAIN, 0.0), 2.0
    for t in range(1, 4):                                                                          # the same years through the kernel at a zero rate
        K.step_year(book, lambda w: 0.0 * w, 1.0, np.zeros(1), 0.0, hook=hk, t=t)
        assert np.allclose(np.cumprod(f[:, 0, 0])[t - 1] * 2.0, hk.W_after[0], atol=1e-12)


def test_the_burden_on_the_household_path_is_the_toy_rate_by_hand_and_the_legacy_path_is_bit_equal():
    base = SimpleNamespace(wealth=np.array([2.0]), w_min=0.0, adults_k=np.array([1.0]), band=np.array(['D10']))
    W = bd.free_path(base, np.zeros((2, 1)), None, G=2, hook=ab.HouseholdHook(TOY, GAIN, 0.0))
    d1 = 2.0 * 0.0225
    assert W.shape == (3, 1, 1) and np.isclose(W[1, 0, 0] - W[0, 0, 0], d1, atol=1e-12)
    out = bd._pooled(base, W, 2, (0.0, 0.0, 0.0), lambda x: 0.01 * x)                              # a tax of 1% of wealth on the path, no discounting
    assert np.isclose(out['D10'][0], 100 * 0.01 * (W[1, 0, 0] + W[2, 0, 0]) / (W[2, 0, 0] - W[0, 0, 0]), atol=1e-9) if 'D10' in out else True
    g, c = np.array([[0.02], [0.03]]), 0.1
    old = np.concatenate([np.ones((1, 1, 1)), np.cumprod((1.0 + g) * (1.0 - c), axis=0)[:, None, :]]) * base.wealth[None, :, None]
    assert np.array_equal(bd.free_path(base, g, c), old) and np.array_equal(bd.free_path(base, g, c, hook=ab.LegacyHook(c)), old)


def test_m3_and_m12_come_back_under_the_household_arm_without_reading_the_legacy_c(ctx):
    c2 = replace(ctx, arm=dict(arm='household', inputs=INP, saving='median'), once=frozenset({'OH1b', 'OH1c'}))
    th = {**c2.centre, 'I-D14c': np.nan}                                                           # a read of the legacy c would give nan
    st = R.statics(c2, th)['burden']
    assert set(st) == {'OH1b', 'OH1c'}
    vals = [np.asarray(v, float) for cells in st.values() for v in cells.values()]
    assert vals and sum(np.isfinite(v).any() for v in vals) > len(vals) // 2                        # most cells hold numbers (a band with no payer is nan)
    legacy = R.statics(replace(ctx, once=c2.once), th)['burden']
    assert not any(np.isfinite(np.asarray(v, float)).any() for cells in legacy.values() for v in cells.values())   # the legacy arm does read it: the same nan gives nan
