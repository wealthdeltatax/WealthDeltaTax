#!/usr/bin/env python3
"""
bridge_d9.py -- D9 bridge: a single RATES line (rates_core.run_lines, honest, alpha = 1) against the family engine
(valgen_core.run_family3, honest) on the same path, over the Route B payment modes.

  python bridge_d9.py MODEL_DIR            (run after apply_phase2_*.py; reads WDT_Params.toml through wdt_core)

Part 1 (exact): one-route families. Route A and Route C (in kind at alpha = 1 = cash-equivalent units) and Route B under
  sale, lien and income, on a rising path and on a volatile path. Rising path, any mode: must agree to 1e-9.
  Volatile path: refunds are capped differently (valgen: pooled real value for A/B, the state's stake in the route; RATES:
  the units this line has paid, optionally also the true value paid), so a difference is reported, not asserted,
  except for Route C where the two caps are the same rule (asserted).
Part 2 (approximation): each archetype of [archetypes.*] with its Route D share moved into Route A (an honest Route D settles
  by accrual, not in kind each year, so it is not the same mechanism), RATES with the archetype's constant Route B share and
  income ratio against the engine, where Route B's share of each year's tax moves with the deltas. Reported only.
Compared: family wealth at T, state units at T (valgen: net of cash), receipts to date (valgen excluding the terminal lien
settlement, which RATES does not collect inside the window), deferred balance outstanding.
Exit status 1 if an asserted case fails.
"""
import sys
from pathlib import Path


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    root = Path(argv[1]).resolve()
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(Path(__file__).parent))
    from apply_basis_change import locate
    for fname in ('valgen_core.py', 'rates_core.py'):
        sys.path.insert(0, str(locate(root, fname).parent))
    import wdt_core as wc
    import valgen_core as vgc
    import rates_core as rc
    return bridge(wc.load_params(), vgc, rc)


def bridge(p, vgc, rc):
    import numpy as np
    import inspect

    if 'rb' not in inspect.signature(rc.run_lines).parameters or 'route_b' not in inspect.signature(vgc.run_family3).parameters:
        print('ABORT run apply_phase2_valgen.py and apply_phase2_rates.py first'); return 1
    vg, rb_p, inc_p = p['val_gen'], p['route_b'], p['income']
    T, G, g = vg['T'], vg['G'], p['g']
    ir = vgc._ir(p) if vg['index_wmin'] else 0.0
    cons = vg['consumption']
    heir = vg['heir_influx']
    hr = 'delta' if heir == 'delta' else 'fresh'
    idx = (1.0 + ir) ** np.arange(1, T + 1)
    rp = {'tau_0': p['tau_0'], 'tau_m': p['tau_m'], 'k': p['k'], 'wmin': p['W_min']}
    r_def, cap = rb_p['r_def'], inc_p['cap']
    paths = {'rising': np.full(T, g),
             'volatile': np.array([g + (0.25 if (t // 7) % 2 == 0 else -0.45) for t in range(T)])}
    failed = False

    def compare(V0, shares_v, path, mode, ratio, bshare, c_cap, rb_ratio=None):
        pv_ = dict(p, V0_m=V0)
        run = vgc.run_family3(pv_, 1.0, 1.0, list(path), G, heir, consumption=cons, index_rate=ir, shares=shares_v,
                              route_b=mode, r_def=r_def, income_ratio=ratio, income_cap=cap, c_cap=c_cap)
        rbk = None if mode == 'sale' or bshare == 0.0 else {'mode': mode, 'r_def': r_def, 'cap': cap,
                                                            'bshare': np.array([bshare]), 'income': np.array([ratio])}
        out = rc.run_lines(path, idx, np.array([V0]), np.array([1.0]), np.array([0]), 1, np.array([G]), G, cons, rp,
                           heir_rule=hr, c_cap=c_cap, rb=rbk)
        led = run['ledger']
        den = max(run['family_true_T'], run['state_true_T'], 1e-12)
        settle = min(out['lien_out'][-1], out['wealth'][-1])      # the engine settles the balance at the horizon; RATES reports it
        d_fam = abs(out['wealth'][-1] - settle - run['family_true_T']) / den
        d_st = abs(out['stake'][-1] + settle - (run['state_true_T'] - led.bal['state_cash'])) / den
        rec_v = sum(v for (_, k, v, _) in run['receipts'] if k not in ('terminal_B', 'terminal_D'))
        rec_r = (out['tax'] + out['refund'] + out['heir'] + out['lien']).sum()
        d_rc = abs(rec_v - rec_r) / den
        return d_fam, d_st, d_rc, out['lien_out'][-1]

    print('Part 1: one-route families (relative to terminal family wealth)')
    print(f"  {'route/mode':<16}{'path':<10}{'c_cap':<17}{'family':>10}{'state':>10}{'receipts':>10}  asserted")
    V0 = 50.0
    cases = [('A sale', {'A': 1.0}, 'sale', 0.0, 0.0), ('C sale', {'C': 1.0}, 'sale', 0.0, 0.0),
             ('B sale', {'B': 1.0}, 'sale', 0.0, 0.0), ('B lien', {'B': 1.0}, 'lien', 0.0, 1.0),
             ('B income 2%', {'B': 1.0}, 'income', 0.02, 1.0), ('B income 20%', {'B': 1.0}, 'income', 0.20, 1.0)]
    for name, sh, mode, ratio, bsh in cases:
        for pname, path in paths.items():
            for c_cap in ('units', 'units_and_value'):
                d = compare(V0, sh, path, mode, ratio, bsh, c_cap)
                must = pname == 'rising' or name.startswith('C')
                bad = must and max(d[:3]) > 1e-9
                failed |= bad
                print(f"  {name:<16}{pname:<10}{c_cap:<17}{d[0]:>10.1e}{d[1]:>10.1e}{d[2]:>10.1e}  "
                      f"{'FAIL' if bad else ('ok' if must else 'info')}")

    print('\nPart 2: archetypes (route D moved into A), RATES constant Route B share vs the engine; rising path')
    print(f"  {'archetype':<20}{'mode':<8}{'family':>10}{'state':>10}{'receipts':>10}{'lien out (RATES)':>18}")
    for name, a in p.get('archetypes', {}).items():
        sh = dict(a['shares'])
        sh['A'] = sh.get('A', 0.0) + sh.pop('D', 0.0)
        sh = {k: v for k, v in sh.items() if v > 0.0}
        ratio = inc_p['by_archetype'].get(name, inc_p['default_ratio'])
        for mode in ('sale', 'lien', 'income'):
            d = compare(a['V0_m'], sh, paths['rising'], mode, ratio if mode == 'income' else 0.0, sh.get('B', 0.0), 'units')
            print(f"  {name:<20}{mode:<8}{d[0]:>10.1e}{d[1]:>10.1e}{d[2]:>10.1e}{d[3]:>18.4f}")
    print('\nBRIDGE ' + ('FAILED' if failed else 'OK (asserted cases)'))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
