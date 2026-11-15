#!/usr/bin/env python3
"""
check_params_and_plan_s1.py -- run from the VAL folder (next to valgen_core.py), after
apply_basis_change.py has been applied.

  1. Parse-check WDT_Params.toml through wdt_core (load_params and load_rates_params).
  2. Re-derive the plan's PLAN_S1 no-verification fixtures on the POST basis, at the plan
     baseline (PLAN_S1_BASELINE in valgen_core), and print them next to the plan values.
     Nothing is written. If you accept the numbers, paste the printed dicts back to me and
     I will update PLAN_S1_GAIN / PLAN_S1_FLAT_STAKE and un-gate the fixtures.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import valgen_core as vc
import wdt_core as wc


def check_params():
    print('== 1. WDT_Params.toml ==')
    p = wc.load_params()
    rp = wc.load_rates_params()
    vg = p['val_gen']
    print(f"  load_params: OK   (N_val={p['N_val']}, N_fill={p['N_fill']}, g={p['g']:.4%}, "
          f"val_basis={p.get('val_basis')}, index_rate={p.get('index_rate')})")
    print(f"  load_rates_params: OK   (scenarios={len(rp['rates']['scenarios'])}, "
          f"levy_case={rp['rates']['replacement']['levy_case']})")
    print(f"  val_gen: g_real={vg.get('g_real')}, index_rate={vg.get('index_rate')}, "
          f"rate_scenario={vg.get('rate_scenario')!r}, route_shares={vg['route_shares']}")
    return p


def derive_plan_s1(p):
    print('\n== 2. PLAN_S1 fixtures on the post basis (plan baseline) ==')
    print(f"  basis convention: {wc.BASIS_CONVENTION}")
    base = vc.PLAN_S1_BASELINE
    q = dict(p, tau_0=base['tau_0'], tau_m=base['tau_m'], k=base['k'], W_min=base['W_min'],
             V0_m=base['V0_m'], g=base['g'], schedule='logistic')
    gains = {}
    print('  gain = f_T(alpha)/f_T(1) - 1, single life, no verification, delta/real  (N, alpha): derived | plan | diff')
    for (n, a), target in vc.PLAN_S1_GAIN.items():
        h = vc.run_family(q, 1.0, [q['g']] * n, None, 'delta', 'real')
        r = vc.run_family(q, a, [q['g']] * n, None, 'delta', 'real')
        gain = r['f_T'] / h['f_T'] - 1.0
        gains[(n, a)] = gain
        print(f"    ({n:>2}, {a:>3}): {gain:+.6f} | {target:+.6f} | {gain - target:+.6f}")

    fp = vc._flat(q)
    stakes = {a: vc.run_family(fp, a, [q['g']] * vc.PLAN_S1_FLAT_N, None, 'delta', 'real')['f_T']
              for a in (0.5, 1.0, 2.0, 5.0)}
    spread = max(stakes.values()) - min(stakes.values())
    print(f"  flat rate stake (N={vc.PLAN_S1_FLAT_N}): " +
          ', '.join(f'alpha {a}: {s:.6f}' for a, s in stakes.items()) +
          f" | spread {spread:.2e} | plan {vc.PLAN_S1_FLAT_STAKE}")

    print('\n  Paste-ready (rounded to 3 dp for gains, 6 dp for the stake):')
    print('  PLAN_S1_GAIN = {' + ', '.join(f'({n}, {a}): {round(g_, 3)}' for (n, a), g_ in gains.items()) + '}')
    print(f"  PLAN_S1_FLAT_STAKE = {round(stakes[1.0], 6)}")
    return gains, stakes


if __name__ == '__main__':
    params = check_params()
    derive_plan_s1(params)
