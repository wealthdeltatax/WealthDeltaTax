"""Brief 132c: the pension-secured lien. Pure functions (core/pension_lien.py) and the hook's settlement at death and the horizon."""
from pathlib import Path

import json
from dataclasses import replace

import numpy as np

from model_v3.core import kernel as K, pension_lien as pl
from model_v3.runner import arm
from tests.model.model_v3.test_household_tax import GAIN, RATE, ST, book_for, run

Q = lambda p, n, f: {'property': np.array(p, float), 'net_financial': np.array(n, float), 'physical': np.array(f, float)}


def test_accrue_and_add_follow_the_deferral_rate():
    assert np.allclose(pl.accrue([1.0, 2.0], 0.03), [1.03, 2.06]) and np.allclose(pl.add([1.0], 0.5), [1.5])


def test_settle_pays_from_the_classes_pro_rata_then_draws_on_the_pension_then_reports_the_rest():
    q = Q([0.3, 0.3, -0.1, 0.3], [0.1, 0.1, 0.0, 0.1], [0.0, 0.0, 0.0, 0.0])
    q1, pen1, paid, d, rest = pl.settle(q, np.array([0.2, 0.6, 0.5, 2.0]), np.array([1.0, 1.0, 1.0, 1.0]))
    assert np.allclose(d, [0.0, 0.2, 0.5, 1.0]) and np.allclose(rest, [0.0, 0.0, 0.0, 0.6])        # a line in debt pays nothing from the classes; the draw stops at the pension
    assert np.allclose(pen1, 1.0 - d) and np.allclose(sum(paid.values()), [0.2, 0.6, 0.5, 1.4])
    assert np.allclose(q1['property'], [0.15, 0.0, -0.1, 0.0]) and np.allclose(q1['net_financial'], [0.05, 0.0, 0.0, 0.0])
    assert np.allclose(paid['property'][2], 0.5) and np.allclose(paid['net_financial'][2], 0.0)       # no positive balance: the draw is received in the first class


def test_hook_settlement_pays_classes_then_pension_keeps_i1_and_the_receipts_tie():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    h.q = {**h.q, 'property': np.full(14, 0.2), 'net_financial': np.full(14, 0.1), 'physical': np.zeros(14), 'pension': np.full(14, 1.0)}
    h.PL, h.rcv = np.full(14, 0.5), {k: np.zeros(14) for k in arm.CLASSES[:3]}
    fam = book.family_true()
    f = (0.3 - 0.5) / fam
    for x in book.R.values():
        x.update({k: x[k] * f for k in ('V', 'dd', 'Wp', 'ppu')})
    book.pen = book.penp = h.q['pension'].copy()
    h._check(book)
    u0 = book.unpaid_B.copy()
    h.settle(book)
    assert np.allclose(h.q['pension'], 0.8) and np.allclose(h.PL, 0.0) and np.allclose(sum(h.q[k] for k in arm.CLASSES[:3]), 0.0)
    assert np.allclose(book.family_true(), 0.0) and np.allclose(book.pen, 0.8) and (book.unpaid_B == u0).all()
    assert np.allclose(sum(sum(v) for v in h.rcv.values()), 0.5 * 14) and np.allclose(h.set_p, 0.2) and np.allclose(h.set_c, 0.3)


def test_hook_settlement_that_the_pension_cannot_cover_is_written_off_in_the_ledger_not_left_unpaid():
    """138c, limited recourse: the state collects up to the pension; the remainder is the ledger's write-off, so the lien never exceeds the pension and unpaid_B does not move."""
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    book = book_for(ST)
    K.step_year(book, RATE, 1.0, np.zeros(14), 0.0, hook=h, t=1)
    h.q = {**h.q, 'property': np.full(14, 0.2), 'net_financial': np.full(14, 0.1), 'physical': np.zeros(14), 'pension': np.full(14, 0.1)}
    h.PL, h.wo, h.set_c, h.set_p = np.full(14, 0.5), np.zeros(14), 0.0, 0.0
    f = (0.3 - 0.5) / book.family_true()
    for x in book.R.values():
        x.update({k: x[k] * f for k in ('V', 'dd', 'Wp', 'ppu')})
    book.pen = book.penp = h.q['pension'].copy()
    u0 = book.unpaid_B.copy()
    h.settle(book)
    L = h.lien()
    assert np.allclose(h.PL, 0.0) and np.allclose(h.wo, 0.1) and np.allclose(book.unpaid_B, u0) and np.allclose(h.q['pension'], 0.0) and np.allclose(h.unpaid, 0.0)
    assert np.allclose(0.5 - L['settled'] - L['wo'], L['bal'])                                      # the write-off ties the ledger's balance: opening - settled - written off = closing


def test_no_lien_in_a_line_that_never_needs_it_and_the_pension_is_reduced_only_at_settlement():
    h = arm.HouseholdHook(ST, GAIN, 0.0157)
    for t, kind, book, a in run(h, 12, G=6):
        assert (a['PL'] == 0).all() and (a['lien_new'] == 0).all() and (np.asarray(a['settled_pension']) == 0).all() and np.abs(a['residual']).max() < 1e-9
        assert (book.pen == h.q['pension']).all() and K.shortfall_lines(book) == 0


def test_the_public_ledger_carries_the_lien_as_a_receivable_in_all_six_phases_and_the_terminal_year():
    from model_v3.core import base as bs, pack as pk, revenue as rv, schedule as sc
    root = Path(__file__).resolve().parents[3]
    pack, reg = pk.load_pack(root / 'data' / 'country-packs' / 'GBR'), pk.load_register(root / 'data' / 'input-register' / 'inputs.json')
    inp = json.loads((root / 'results' / 'cell-baseline' / 'inputs_used.json').read_text())
    b0, y = bs.build_base(pack, reg, 0.25), inp['yreg']['mid']
    k = np.where(b0.wealth >= b0.w_min, 1.0 - reg['I-D5a'].central / 100.0, 1.0)                                                                  # the runner's shaped base: the behavioural loss at launch
    base = replace(b0, wealth=b0.wealth * k, wealth_bn=b0.wealth_bn * k, V0={r: v * k for r, v in b0.V0.items()})
    gain = dict(property=0.016455, net_financial=inp['regimes']['mid'] - y, physical=0.0, pension=inp['regimes']['mid'] - y)
    st = arm.line_state(base, pack.tables['decile_composition'], reg, inp['sav']['min'], scale=inp['income_scale'], cap=reg['I-D1l'].central)          # the 127c point min_mid at the lower threshold ratio: D4 runs out of non-pension wealth
    rate, T, P = sc.rate_function(1, 0.04, 0.7, base.w_min, 'logistic_ln'), 100, 1
    run = rv.run_lines(base, rate, np.zeros((T, P)), np.full((T, P), inp['g']), reg['I-D14c'].central / 100, G=30, n_phase=6, hook=arm.HouseholdHook(st, gain, inp['g']), lam_C=reg['I-D14a'].central / 100, lam_D=reg['I-D14b'].central / 100)
    rec, wdt = run['ledger']['rec'], run['tax'] + run['refund'] + run['death_tax'] + run['heir'] + run['death_B'] + run['death_D']
    o = rv.revenue(run, 2000.0, 0.3, {'x': 1.0}, np.zeros((T, P)), 40.0, 0.0, safe=np.full((T, P), 0.005), safe_share=0.3)
    assert rec['new'].sum() > 0 and rec['settled'][-1, 0] > 0 and (rec['settled'][:T - 1, 0] > 0).sum() >= 2 and np.abs(rec['wo']).max() == 0 and rec['bal'][-1, 0] < 1e-9     # settled at deaths and in the terminal year
    assert np.abs(np.diff(np.vstack([np.zeros((1, P)), rec['bal']]), axis=0) - (rec['new'] + rec['accr'] - rec['settled'] - rec['wo'])).max() < 1e-9                 # the receivable's own recursion
    assert np.abs(sum(run['ledger']['rc'].values()) + rec['new'] - rec['xnew'] - rec['settled'] - wdt).max() < 1e-9                                    # receipts exclude the lien and include its settlement
    f = o['fund']
    for k, L in f['L'].items():
        assert np.abs(np.diff(np.vstack([np.zeros((1, P)), L]), axis=0) - (f['rc'][k] + f['ret'][k] - f['pay'][k])).max() < 1e-9      # dL = receipts + return - payout with the receivable apart
    assert np.abs(sum(f['rc'].values()) - (wdt - (rec['new'] - rec['xnew']) + rec['settled'] + 0.003 * run['gdp_index'] * 2000.0)).max() < 1e-9 and f['rec'] is rec
