"""
test_rate_schedules.py: checks for STEP 1 (schedule-aware tau, with_rate_scenario, valgen wiring).
Run from the model folder (or pass --dir): python test_rate_schedules.py
Tests are the only place that may import both a RATES core and a VAL core.

 1  legacy logistic: tau(W, p) is bit-identical to the original formula; rate_params(p) is exactly the four keys
 2  scalar tau == vector rate_vec for logistic, logistic_ln and ladder (grid across and beyond the anchors)
 3  with_rate_scenario('gain_ladder') builds the same ladder rates_core.calibration builds (ladder_to_tau on the TOML anchors)
 4  with_rate_scenario('') leaves the legacy logistic; unknown scenario raises
 5  the honest-family engines agree: rates_core.run_lines (one line, in-kind, units cap, delta heir) against
    valgen_core.run_family3 (shares {C: 1}, c_cap = 'units', alpha = 1), under logistic AND the gain ladder
 6  valgen helpers: _flat and the no-tax ceiling force the logistic; plan-S1 fixtures are skipped under a ladder
"""
import argparse
import math
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


p0 = wc.load_params()
GRID = [0.05, 0.2, 0.225, 0.3, 0.5, 0.9, 1.0, 1.5, 2.0, 2.5, 4.0, 7.0, 20.0, 25.0, 60.0, 100.0, 5e3]

# 1 ── legacy logistic is unchanged
worst = 0.0
for W in GRID:
    ref = 0.0 if W < p0['W_min'] else p0['tau_m'] / (1.0 + ((p0['tau_m'] - p0['tau_0']) / p0['tau_0']) * math.exp(-p0['k'] * (W - p0['W_min'])))
    worst = max(worst, abs(wc.tau(W, p0) - ref))
check('legacy_logistic_bit_identical', worst == 0.0, f'max|diff|={worst:.1e}')
check('rate_params_is_four_keys_without_schedule', sorted(wc.rate_params(p0)) == sorted(['k', 'tau_0', 'tau_m', 'W_min']))


# 2 ── scalar == vector
def vec(rp_val):
    """Translate a tau() dict (W_min) to the rate_vec dict (wmin)."""
    out = {'tau_0': rp_val['tau_0'], 'tau_m': rp_val['tau_m'], 'k': rp_val['k'], 'wmin': rp_val['W_min'],
           'schedule': rp_val.get('schedule', 'logistic')}
    if 'ladder' in rp_val:
        out['ladder'] = rp_val['ladder']
    return out


rates = p0['rates']['scenarios']
names = [n for n in ('gain_ladder', 'stock_ladder', 'logistic_ln_ref', 'logistic_ln_gain', 'logistic_gain', 'wmin_house')
         if n in rates]
for n in [''] + names:
    q = wc.with_rate_scenario(p0, n)
    v = wc.rate_vec(np.array(GRID), vec(q))
    s = np.array([wc.tau(W, q) for W in GRID])
    check(f'scalar_equals_vector[{n or "legacy"}]', np.max(np.abs(s - v)) < 1e-12, f'max|diff|={np.max(np.abs(s - v)):.1e} ({q["schedule"]})')

# 3 ── same ladder as RATES builds
q = wc.with_rate_scenario(p0, 'gain_ladder')
sp = p0['rates']['schedules']['gain_ladder']
lad, _ = wc.ladder_to_tau(sp['anchors'], sp['basis'], sp['r_ref'], sp['c_ref'], p0['rates']['defaults']['tau_m'])
check('gain_ladder_matches_rates_calibration', q['schedule'] == 'ladder' and [tuple(x) for x in q['ladder']] == [tuple(x) for x in lad])
want_wmin = p0['rates']['scenarios']['gain_ladder']['overrides']['wmin_house_ratio'] * p0['rates']['dist']['house_median_gbp_m']
check('wmin_is_house_ratio_times_median_house', abs(q['W_min'] - want_wmin) < 1e-15, f"W_min={q['W_min']}")

# 4 ── switches
q0 = wc.with_rate_scenario(p0, '')
check('empty_scenario_is_legacy_logistic', q0['schedule'] == 'logistic' and q0['W_min'] == p0['W_min'] and q0['tau_0'] == p0['tau_0'])
try:
    wc.with_rate_scenario(p0, 'no_such_scenario')
    check('unknown_scenario_raises', False)
except ValueError:
    check('unknown_scenario_raises', True)

# 5 ── RATES engine against valgen engine, honest family, one line
T, G = 100, 30
g, c, ir, V0 = p0['g'], 0.035, p0['budget_growth'], p0['V0_m']
idx = (1.0 + ir) ** np.arange(1, T + 1)
worst = {}
for n in ('', 'gain_ladder'):
    q = wc.with_rate_scenario(p0, n)
    v = vc.run_family3(q, 1.0, 1.0, [g] * T, G, 'delta', consumption=c, index_rate=ir, shares={'C': 1.0})
    raw = rc.run_lines(np.full(T, g), idx, np.array([V0]), np.array([1.0]), np.array([0]), 1,
                       np.array([G]), G, c, vec(q), heir_rule='delta')
    worst[n] = abs(raw['wealth'][-1] - v['family_true_T']) / v['family_true_T']
    check(f'rates_run_lines_equals_valgen_C_only[{n or "legacy"}]', worst[n] < 1e-9,
          f"rel diff={worst[n]:.1e}; family true T {v['family_true_T']:.4f}")

# 6 ── valgen helpers
ql = wc.with_rate_scenario(p0, 'gain_ladder')
check('flat_forces_logistic', vc._flat(ql)['schedule'] == 'logistic')
check('plan_s1_fixture_skipped_under_ladder', not vc._plan_fixture_applies(ql))

print('\n%d failed' % len(FAILS) if FAILS else '\nall passed')
sys.exit(1 if FAILS else 0)