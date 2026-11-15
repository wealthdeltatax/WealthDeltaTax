"""
test_rules_and_basis.py: checks for STEP 2. Run from the model folder (or --dir): python test_rules_and_basis.py

 1  parse_rule: defaults, full key, invalid parts raise; p['rules'] and valgen's rule constants agree
 2  rates_core.run_lines: c_cap='units' is the old behaviour (default == explicit); c_cap='units_and_value' never refunds more
    than the value paid, and equals valgen run_family3 (Route C only, same c_cap) after a market fall, under logistic and ladder
 3  the value cap actually binds after a fall (otherwise test 2 proves nothing)
 4  with_val_basis: legacy when g_real / index_rate are omitted; overrides when set; valgen meta/helper follow
 5  honest families are inert to verify_down and the auction (why RATES need only the c_cap part)
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--dir', default='.')
a = ap.parse_args()
base = Path(a.dir).resolve()


def _add_paths(base, modules):
    """Put the folder of every named module on sys.path, wherever it sits (the model folder, one level up, or any subfolder)."""
    roots = [base, base.parent]
    for m in modules:
        hits = []
        for r in roots:
            hits += [h for h in r.rglob(m + '.py') if not any(x.startswith('.') or x in ('OUTPUTS', '__pycache__') for x in h.parts)]
            if hits:
                break
        if not hits:
            raise SystemExit(f'{m}.py not found under {base} or {base.parent}; pass --dir with the folder that holds wdt_core.py')
        sys.path.insert(0, str(sorted(hits, key=lambda h: len(h.parts))[0].parent))


_add_paths(base, ('wdt_core', 'rates_core', 'valgen_core'))

import numpy as np

import wdt_core as wc
import rates_core as rc
import valgen_core as vc

FAILS = []


def check(name, ok, detail=''):
    print(f"{'PASS' if ok else 'FAIL'}  {name} {detail}")
    if not ok:
        FAILS.append(name)


p = wc.load_params()

# 1 ── rule parsing
check('parse_rule_defaults', wc.parse_rule('units') == {'c_cap': 'units', 'verify_down': 'allow', 'dauc': 'off'})
check('parse_rule_full', wc.parse_rule('units_and_value/reset/on') == {'c_cap': 'units_and_value', 'verify_down': 'reset', 'dauc': 'on'})
bad = 0
for k in ('x', 'units/x', 'units/allow/x', 'units/allow/off/extra'):
    try:
        wc.parse_rule(k)
    except ValueError:
        bad += 1
check('parse_rule_invalid_raises', bad == 4, f'{bad} of 4')
check('rules_in_both_loaders', wc.resolve_rule(p, 'candidate') == wc.resolve_rule(wc.load_rates_params(), 'candidate'))
check('valgen_constants_match_toml_rules',
      wc.parse_rule(vc._BASE_RULE) == wc.resolve_rule(p, 'base') and wc.parse_rule(vc._CANDIDATE_RULE) == wc.resolve_rule(p, 'candidate'))
check('rates_default_rule_resolves', wc.resolve_rule(wc.load_rates_params(), wc.load_rates_params()['rates']['defaults']['rule_set'])['c_cap']
      in ('units', 'units_and_value'))

# 2 ── engines
T, G = 100, 30
ir, V0, g0 = vc._ir(p), p['V0_m'], p['g']
idx = (1.0 + ir) ** np.arange(1, T + 1)
fall = [g0] * T
fall[19], fall[20] = -0.5, 0.3                   # a genuine one-year market fall at year 20, then a rebound
# (name, consumption, return path). High consumption drives W down while the price rises, so refunds are of units paid at
# LOWER prices: that is where a value cap can bind. A fall alone does not (units paid earlier were paid at higher prices).
SCEN = [('fall', 0.035, fall), ('high_consumption', 0.20, [g0] * T), ('high_consumption_slow_growth', 0.12, [0.05] * T)]


def vec(q):
    out = {'tau_0': q['tau_0'], 'tau_m': q['tau_m'], 'k': q['k'], 'wmin': q['W_min'], 'schedule': q.get('schedule', 'logistic')}
    if 'ladder' in q:
        out['ladder'] = q['ladder']
    return out


def rates_run(q, cap, ser, c):
    return rc.run_lines(np.array(ser), idx, np.array([V0]), np.array([1.0]), np.array([0]), 1, np.array([G]), G, c, vec(q),
                        heir_rule='delta', c_cap=cap)


gaps = {}
for n in ('', 'gain_ladder'):
    q = wc.with_rate_scenario(p, n)
    d0 = rc.run_lines(np.array(fall), idx, np.array([V0]), np.array([1.0]), np.array([0]), 1, np.array([G]), G, 0.035, vec(q))
    d1 = rates_run(q, 'units', fall, 0.035)
    same = all(np.array_equal(d0[k], d1[k]) for k in ('tax', 'refund', 'heir', 'stake', 'wealth'))
    check(f'units_is_default_behaviour[{n or "legacy"}]', same)
    for sname, c, ser in SCEN:
        for cap in ('units', 'units_and_value'):
            v = vc.run_family3(q, 1.0, 1.0, ser, G, 'delta', consumption=c, index_rate=ir, shares={'C': 1.0}, c_cap=cap)
            r = rates_run(q, cap, ser, c)
            rel = abs(r['wealth'][-1] - v['family_true_T']) / v['family_true_T']
            check(f'rates_equals_valgen_C_only[{n or "legacy"},{sname},{cap}]', rel < 1e-9, f'rel diff={rel:.1e}')
        gaps[(n or 'legacy', sname)] = (rates_run(q, 'units_and_value', ser, c)['wealth'][-1] / rates_run(q, 'units', ser, c)['wealth'][-1] - 1.0)

# 3 ── does the value cap ever bind? (a finding, printed; the test only needs it to bind SOMEWHERE so test 2 is not vacuous)
for (n, sname), gp in gaps.items():
    print(f'INFO  terminal wealth, units_and_value vs units [{n}, {sname}]: {gp:+.4%}')
check('value_cap_binds_somewhere', any(abs(x) > 1e-12 for x in gaps.values()),
      'if this fails the cap never bites in any scenario here, and the engine check above does not exercise it')

# 4 ── basis
pl = wc.with_val_basis(p)
check('legacy_basis_when_keys_omitted', p['val_gen'].get('g_real') is not None or (pl['g'] == p['g'] and pl['index_rate'] == p['budget_growth']
                                                                                    and pl['val_basis'] == 'legacy_nominal'))
p2 = dict(p, val_gen=dict(p['val_gen'], g_real=0.05, index_rate=0.012))
pr = wc.with_val_basis(p2)
check('real_basis_overrides_g_and_index', pr['g'] == 0.05 and pr['index_rate'] == 0.012 and pr['val_basis'] == 'real')
check('valgen_ir_follows_p', vc._ir(pr) == 0.012 and vc._ir(p) == p['budget_growth'])

# 5 ── honest inertness (verify_down, auction)
ser0 = [g0] * T
h = {}
for rule in ('units_and_value/allow/off', 'units_and_value/reset/off', 'units_and_value/allow/on', 'units_and_value/reset/on'):
    h[rule] = vc.run_family3(p, 1.0, 1.0, ser0, G, 'delta', **vc._p5_opts(p, rule, p['val_gen']['lambda_base']))['family_true_T']
spread = (max(h.values()) - min(h.values())) / min(h.values())
check('honest_inert_to_verify_down_and_auction', spread < 1e-12, f'spread={spread:.1e}')

print('\n%d failed' % len(FAILS) if FAILS else '\nall passed')
sys.exit(1 if FAILS else 0)