#!/usr/bin/env python3
"""
rates_engine_test.py -- S2 checks for the kernel-based RATES engine (rates_core.run_lines / run_cohorts / _route_plan / _verification).
No JST file needed. Run from the RATES folder:   python rates_engine_test.py        (exit 0 = all pass)
For legacy parity (sale mode) run rates_core.pre_s2 against the patched file on the real JST: see parity_check() at the bottom (--parity).
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import rates_core as rc            # noqa: E402

RP = {'tau_0': 0.3, 'tau_m': 0.9, 'k': 0.005, 'wmin': 0.0}
ARCH = {'a': dict(V0_m=0.4, A=0.3, B=0.6, C=0.05, D=0.05), 'b': dict(V0_m=8.0, A=0.1, B=0.1, C=0.7, D=0.1),
        'c': dict(V0_m=50.0, A=0.5, B=0.2, C=0.1, D=0.2)}
P = {'archetypes': ARCH, 'route_b': {'payment_mode': 'sale', 'sovereign_real_rate': 0.015, 'deferral_spread': 0.01, 'r_def': 0.025},
     'income': {'cap': 1.0, 'default_ratio': 0.0, 'by_archetype': {'a': 0.08, 'b': 0.02, 'c': 0.005}},
     'verification': {'lambda_C': 0.0, 'lambda_D': 0.0, 'death_verifies': False}}
CAL = {'V0': np.array([0.4, 1.0, 8.0, 20.0, 50.0, 400.0]), 'y_ref_gbp_m': 1.0, 'share': np.array([.5, .3, .1, .05, .04, .01]),
       'band_id': np.array([0, 0, 1, 1, 2, 2]), 'bands': {'adult_share': [0, 0, 0], 'edges_gbp_m': [1.0, 25.0]}}
fails = []


def check(name, ok, info=''):
    print(f"  {'ok  ' if ok else 'FAIL'} {name} {info}")
    if not ok:
        fails.append(name)


def cfg(**kw):
    return {'route_b_mode': None, 'route_mix': 'none', 'route_mix_weights': {}, 'deferral_spread': None, 'income_cap': None,
            'rule_set': 'candidate', 'lam_C': 'toml', 'lam_D': 'toml', 'death_verify': 'toml', **kw}


def run(g, V0, ph=None, plan=None, ver=None, c=0.035, c_cap='units', G=30, idx=None, heir_rule='delta'):
    n = len(V0)
    idx = np.ones(len(g)) if idx is None else idx
    return rc.run_lines(np.asarray(g, float), idx, np.asarray(V0, float), np.full(n, 1.0 / n), np.arange(n), n,
                        None if ph is None else np.asarray(ph), G, c, RP, heir_rule=heir_rule, c_cap=c_cap, plan=plan, ver=ver)


def plan_of(mode='sale', **shares):
    n = len(next(iter(shares.values())))
    return {'shares': {k: np.asarray(v, float) for k, v in shares.items()}, 'mode': mode, 'r_def': 0.025, 'cap': 1.0, 'income': np.zeros(n)}


def test_mixture():
    print('route mixture')
    for mix, kw in (('wealth', {}), ('blend', {'route_mix_weights': {'a': .5, 'c': .5}}), ('b', {})):
        r = rc._route_plan(cfg(route_mix=mix, **kw), CAL, P)
        S = np.column_stack([r['cell']['shares'][k] for k in rc._ABCD])
        check(f'{mix}: shares sum to 1 in every cell', np.allclose(S.sum(1), 1.0))
    r = rc._route_plan(cfg(route_mix='b'), CAL, P)
    check('pure archetype: same shares in every cell', all(np.allclose(r['cell']['shares'][k], ARCH['b'][k]) for k in rc._ABCD))
    r = rc._route_plan(cfg(route_mix='blend', route_mix_weights={'a': .5, 'c': .5}), CAL, P)
    check('blend = weighted archetypes', np.allclose(r['cell']['shares']['B'], .5 * .6 + .5 * .2))
    r = rc._route_plan(cfg(route_mix='wealth'), CAL, P)
    check('wealth: archetype shares exactly at their V0_m anchors', all(abs(r['cell']['shares'][k][CAL['V0'].tolist().index(8.0)] - ARCH['b'][k]) < 1e-12 for k in rc._ABCD))
    check("none + sale: no plan (everything in kind, the earlier numbers)", rc._route_plan(cfg(), CAL, P)['cell'] is None)
    for bad in (dict(route_mix='blend', route_mix_weights={'a': .5}), dict(route_mix='nope'), dict(route_b_mode='x')):
        try:
            rc._route_plan(cfg(**bad), CAL, P)
            check(f'rejects {bad}', False)
        except ValueError:
            check(f'rejects {bad}', True)


def test_baseline_identity():
    print('sale / all-in-kind identity')
    g = np.full(60, 0.05)
    a = run(g, [2.0, 8.0, 40.0], ph=[5, 12, 20])
    b = run(g, [2.0, 8.0, 40.0], ph=[5, 12, 20], plan=plan_of(C=[1, 1, 1]))
    check('plan None == shares {C: 1}', all(np.array_equal(a[k], b[k]) for k in ('tax', 'refund', 'heir', 'wealth', 'stake')))
    check('no route D / lien / income when all in kind', not (a['dsettle'].any() or a['accr_d_out'].any() or a['lien'].any() or a['income'].any()))


def test_route_d():
    print('route D accrues, settles at death')
    g = np.full(60, 0.05)
    nd = run(g, [20.0], ph=None, plan=plan_of(D=[1.0]))
    check('no deaths: nothing settled, liability accrues (a receivable, not a receipt)', nd['dsettle'].sum() == 0 and nd['accr_d_out'][-1] > 0 and nd['tax'].sum() == 0)
    d = run(g, [20.0], ph=[20], plan=plan_of(D=[1.0]), heir_rule='fresh')
    k = 19
    check('death at 20 (heir untaxed): settled that year, receivable cleared', d['dsettle'][k] > 0 and d['accr_d_out'][k] < 1e-12)
    check('settled at death ~ accrued just before (growth of one year, same order)', 0.9 < d['dsettle'][k] / d['accr_d_out'][k - 1] < 1.3, f"({d['dsettle'][k]:.4f} vs prior receivable {d['accr_d_out'][k - 1]:.4f})")
    dh = run(g, [20.0], ph=[20], plan=plan_of(D=[1.0]))
    check('death at 20 (heir taxed): the heir\'s influx opens a new Route D liability', dh['dsettle'][k] > 0 and dh['accr_d_out'][k] > 0 and dh['tax'].sum() == 0)


def test_death_mask():
    print('a death hits only its own lines')
    g = np.full(60, 0.05)
    both = run(g, [5.0, 5.0], ph=[10, 25], plan=plan_of('lien', B=[.5, .5], C=[.5, .5]))
    one = run(g, [5.0, 5.0], ph=[10, 25], plan=plan_of('lien', B=[.5, .5], C=[.5, .5]))
    alone = run(g, [5.0], ph=[25], plan=plan_of('lien', B=[.5], C=[.5]))
    # weights are 1/n: line 2 alone has weight 1, so compare per-line values
    check('line unaffected by the other line\'s death', np.allclose(both['wealth_by_bracket'][:, 1], alone['wealth_by_bracket'][:, 0] / 2.0, rtol=1e-12))
    check('deterministic', np.array_equal(both['tax'], one['tax']))


def test_lambda_passthrough():
    print('verification pass-through (honest lines)')
    rng = np.random.default_rng(4)
    g = rng.normal(0.04, 0.15, 60)                         # price falls included
    pl = plan_of(C=[.5, .5, .5], D=[.5, .5, .5])
    z = run(g, [3.0, 10.0, 40.0], ph=[7, 15, 22], plan=pl, ver={'lam_C': 0.0, 'lam_D': 0.0, 'verify_down': 'allow'})
    a = run(g, [3.0, 10.0, 40.0], ph=[7, 15, 22], plan=pl, ver={'lam_C': 0.05, 'lam_D': 0.05, 'verify_down': 'allow'})
    check("verify_down 'allow': lambda changes nothing for an honest line", all(np.allclose(z[k], a[k], rtol=1e-9, atol=1e-12) for k in ('tax', 'refund', 'heir', 'dsettle', 'wealth')))
    r = run(g, [3.0, 10.0, 40.0], ph=[7, 15, 22], plan=pl, ver={'lam_C': 0.05, 'lam_D': 0.05, 'verify_down': 'reset'})
    pay_z = z['tax'].sum() + z['refund'].sum() + z['dsettle'].sum() + z['heir'].sum()
    pay_r = r['tax'].sum() + r['refund'].sum() + r['dsettle'].sum() + r['heir'].sum()
    check("verify_down 'reset': an honest holder pays at least as much (no write-down credit)", pay_r >= pay_z - 1e-12, f'({pay_r:.5f} vs {pay_z:.5f})')


def test_income():
    print('route B income mode')
    g = np.full(60, 0.05)
    pl = {'shares': {'B': np.array([.5]), 'C': np.array([.5])}, 'mode': 'income', 'r_def': 0.025, 'cap': 0.5, 'income': np.array([0.01])}
    r = run(g, [10.0], plan=pl)
    allow = 0.5 * 0.01 * 10.0
    check('income paid each year <= cap x ratio x V0 (index 1)', (r['income_gross_b'].sum(axis=1) <= allow + 1e-12).all())
    check('income paid is part of tax (counted once)', r['income'].sum() > 0 and r['tax'].sum() >= r['income'].sum() - 1e-12)
    full = {**pl, 'cap': 1.0}
    r2 = run(g, [10.0], plan=full)
    check('higher cap: more income, less sold', r2['income'].sum() >= r['income'].sum())


def test_finite():
    print('numerics')
    g = np.r_[np.full(30, 0.3), np.full(30, -0.6), np.full(40, 0.05)]
    r = run(g, [2.0, 30.0], ph=[3, 30], plan=plan_of('lien', A=[.1, .1], B=[.3, .3], C=[.3, .3], D=[.3, .3]), c_cap='units_and_value')
    check('finite through a crash', all(np.isfinite(r[k]).all() for k in ('tax', 'refund', 'heir', 'wealth', 'lien_out', 'accr_d_out')))


def parity_check(legacy_path, scenarios=('gain_ladder', 'gl_rb_sale', 'gain_ladder_rule_base', 'heir_fresh', 'cohort_central', 'gl_top6_1'), stride=20):
    """Sale-mode parity on the real JST: the pre-S2 file vs this one, every legacy key of each scenario block (cfg excluded) to 1e-9 relative."""
    import math
    import wdt_core as wc
    spec = importlib.util.spec_from_file_location('rc_legacy', legacy_path)
    leg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(leg)
    p = wc.load_rates_params(None)
    J = rc.load_jst(p['rates']['jst_path'])

    def diff(a, b, path=''):
        out = []
        if isinstance(a, dict) and isinstance(b, dict):
            for k in a:
                if k in b and k != 'cfg':
                    out += diff(a[k], b[k], f'{path}/{k}')
        elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b):
            for i, (x, y) in enumerate(zip(a, b)):
                out += diff(x, y, f'{path}[{i}]')
        elif isinstance(a, float) and isinstance(b, float):
            if not (math.isnan(a) and math.isnan(b)) and abs(a - b) > 1e-9 * max(1.0, abs(a)):
                out.append((path, a, b))
        elif not isinstance(a, (dict, list, tuple)) and a != b:
            out.append((path, a, b))
        return out
    for n in scenarios:
        d = diff(wc.json_safe(leg.run_scenario(J, p, n, stride=stride, verbose=False)), wc.json_safe(rc.run_scenario(J, p, n, stride=stride, verbose=False)))
        check(f'parity {n}', not d, f'({len(d)} diffs; first {d[:2]})')


if __name__ == '__main__':
    for t in (test_mixture, test_baseline_identity, test_route_d, test_death_mask, test_lambda_passthrough, test_income, test_finite):
        t()
    if '--parity' in sys.argv:
        parity_check(sys.argv[sys.argv.index('--parity') + 1])
    print('\nALL PASS' if not fails else f'\nFAILED: {fails}')
    sys.exit(1 if fails else 0)
