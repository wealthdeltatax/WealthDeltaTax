"""
kernel_test.py -- tests for wdt_kernel.py
=========================================
  1  hand cases (independent of valgen): ratio-mirror round trip, lien recursion, income cases
  2  vector == scalar: n lines in one Book equal n separate one-line Books, over a switch grid
  3  invariants over the same grid: units conserved, caps hold, asset value conserved
  4  parity with valgen_core.run_family3 (runs only when valgen_core and wdt_core import; else SKIP)

    python kernel_test.py
"""

import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
for _d in (_HERE, _HERE / 'VAL', _HERE.parent / 'VAL'):          # valgen_core is in VAL/
    if _d.is_dir():
        sys.path.insert(0, str(_d))
import wdt_kernel as wk

TOL = 1e-9
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name} {detail}")


def flat(tau0):
    return lambda x: np.where(np.asarray(x) > 0.0, tau0, 0.0)


def logistic(x):
    """A smooth rising schedule with a threshold, for the vector tests."""
    x = np.asarray(x, dtype=float)
    return np.where(x > 2.0, 0.15 + 0.55 / (1.0 + 40.0 * np.exp(-0.02 * (x - 2.0))), 0.0)


# ── 1. hand cases ────────────────────────────────────────────

def hand_cases():
    tau0, g = 0.15, 0.06
    # ratio-mirror round trip: price +50% then back; the family ends with 1 - tau^2/9 of its units
    b = wk.run_lines(flat(tau0), [0.5, -1.0 / 3.0], {'C': 100.0}, n=1)
    f = float(b.R['C']['f'][0])
    check('hand_ratio_mirror_round_trip', abs(f - (1.0 - tau0 ** 2 / 9.0)) < TOL, f'f={f:.9f} vs {1 - tau0 ** 2 / 9:.9f}')
    # a price fall with nothing paid refunds nothing
    b = wk.run_lines(flat(tau0), [-0.5], {'C': 100.0}, n=1)
    check('hand_no_refund_without_payment', b.R['C']['f'][0] == 1.0 and b.R['C']['s'][0] == 0.0)
    # first leg: payment fraction tau x / (1 + x)
    b = wk.run_lines(flat(tau0), [0.5], {'C': 100.0}, n=1)
    check('hand_payment_fraction', abs((1.0 - b.R['C']['f'][0]) - tau0 * 0.5 / 1.5) < TOL)

    # lien recursion, Route B only, flat rate, honest, no deaths (valgen _p6_lien_hand, restated)
    T, V0 = 30, 20.0
    for rd in (0.0, 0.025, 0.06):
        V, LBp = V0, 0.0
        for _ in range(T):
            V_prev, V = V, V * (1 + g)
            LBa = LBp * (1 + rd)
            LBp = LBa + tau0 * ((V - LBa) - (V_prev - LBp))
        bk = wk.run_lines(flat(tau0), [g] * T, {'B': V0}, b_mode='lien', r_def=rd, n=1)
        err = max(abs(bk.family_true()[0] - (V - LBp)), abs(bk.state_true()[0] - LBp)) / V
        check(f'hand_lien_recursion_r_def_{rd}', err < TOL, f'rel err={err:.2e}')

    # income, ample: every tax is paid from income, no units move, state holds the cash
    bk = wk.run_lines(flat(tau0), [g] * T, {'B': V0}, b_mode='income', inc_allow=1e6, n=1)
    V, tax = V0, 0.0
    for _ in range(T):
        V_prev, V = V, V * (1 + g)
        tax += tau0 * (V - V_prev)
    check('hand_income_ample', abs(bk.state_cash[0] - tax) < TOL * V and abs(bk.family_true()[0] - V) < TOL * V
          and bk.unpaid_B[0] == 0.0, f'state cash {bk.state_cash[0]:.6f} vs {tax:.6f}')
    # income, short: shortfall is sold; credited receipts equal the assessed tax
    bk, log = wk.run_lines(flat(tau0), [g] * T, {'B': V0}, b_mode='income', inc_allow=0.04, n=1, collect=True)
    cred = sum(fl.credited.get('B', np.zeros(1))[0] + fl.income[0] for (_, k, fl) in log if k == 'tax')
    ass = sum(fl.L[0] for (_, k, fl) in log if k == 'tax')
    check('hand_income_short_sold_and_conserved',
          0.0 < bk.inc_total[0] < tax and bk.R['B']['f'][0] < 1.0 and abs(cred - ass) < TOL * V,
          f'income {bk.inc_total[0]:.4f}, units {bk.R["B"]["f"][0]:.4f}, credited {cred:.4f} vs assessed {ass:.4f}')
    # sale mode == income with zero income
    a = wk.run_lines(flat(tau0), [g] * T, {'A': 5.0, 'B': 15.0}, b_mode='sale', n=1)
    c = wk.run_lines(flat(tau0), [g] * T, {'A': 5.0, 'B': 15.0}, b_mode='income', inc_allow=0.0, n=1)
    check('hand_zero_income_equals_sale', abs(a.family_true()[0] - c.family_true()[0]) < 1e-12)
    # a higher deferral rate leaves the lien family poorer
    lo = wk.run_lines(flat(tau0), [g] * T, {'B': V0}, b_mode='lien', r_def=0.01, n=1).family_true()[0]
    hi = wk.run_lines(flat(tau0), [g] * T, {'B': V0}, b_mode='lien', r_def=0.08, n=1).family_true()[0]
    check('hand_lien_wealth_falls_with_deferral_rate', hi < lo, f'{lo:.3f} -> {hi:.3f}')
    # flat rate: the family's stake does not depend on how Route C is declared (alpha-free)
    fs = [wk.run_lines(flat(tau0), [g] * 30, {'C': 20.0}, alpha_C=a, n=1).R['C']['f'][0] for a in (0.25, 0.5, 1.0, 2.0)]
    check('hand_flat_rate_alpha_free', max(fs) - min(fs) < 1e-12, f'spread={max(fs) - min(fs):.2e}')


# ── 2 / 3. vector == scalar, invariants ──────────────────────

def make_inputs(n, rng):
    sh = rng.dirichlet(np.ones(4), size=n)                       # route shares
    V0 = {r: sh[:, i] * rng.uniform(3.0, 400.0, n) for i, r in enumerate('ABCD')}
    aC = rng.choice([0.3, 0.7, 1.0, 1.6, 3.0], n)
    aD = rng.choice([0.3, 0.7, 1.0, 1.6, 3.0], n)
    inc = rng.uniform(0.0, 0.06, n) * sum(V0.values())
    return V0, aC, aD, inc


def run_grid(n=10, T=34, G=9):
    rng = np.random.default_rng(7)
    worst = {'diff': 0.0, 'units': 0.0, 'min_E_cash': 0.0, 'min_A_D': 0.0, 'min_EC': 0.0, 'min_state_units': 0.0,
             'min_uo': 0.0, 'uo_excess': 0.0}
    runs = 0
    gs = [0.07, -0.02, 0.10, 0.04, -0.15, 0.12] * 6
    for b_mode in wk.B_MODES:
        for c_cap in wk.C_CAPS:
            for vd in ('allow', 'reset'):
                for lamC, lamD, dv in ((0.0, 0.0, False), (0.12, 0.12, False), (0.05, 0.0, True)):
                    for heir in wk.HEIR_RULES:
                        V0, aC, aD, inc = make_inputs(n, rng)
                        gser = [np.full(n, v) + 0.01 * np.arange(n) / n for v in gs[:T]]   # per-line growth
                        kw = dict(G=G, heir_influx=heir, consumption=0.03, index_rate=0.02, lam_C=lamC,
                                  lam_D=lamD, death_verify=dv, reset_years=(11, 25), b_mode=b_mode, c_cap=c_cap,
                                  verify_down=vd, r_def=0.03, inc_allow=inc)
                        alC = lambda t, gen, td, a=aC: a if gen == 0 else np.ones_like(a)    # a strategy hook
                        alD = lambda t, gen, td, a=aD: a if td >= 3 else np.ones_like(a)
                        book, log = wk.run_lines(logistic, gser, V0, alpha_C=alC, alpha_D=alD, n=n, collect=True, **kw)
                        runs += 1
                        ck = book.check()
                        for k in ('units', 'uo_excess'):
                            worst[k] = max(worst[k], ck[k])
                        for k in ('min_E_cash', 'min_A_D', 'min_EC', 'min_state_units', 'min_uo'):
                            worst[k] = min(worst[k], ck[k])
                        for i in range(n):
                            sl = slice(i, i + 1)
                            V0i = {r: v[sl] for r, v in V0.items()}
                            gi = [x[sl] for x in gser]
                            kwi = dict(kw, inc_allow=inc[sl])
                            alCi = lambda t, gen, td, a=aC[sl]: a if gen == 0 else np.ones_like(a)
                            alDi = lambda t, gen, td, a=aD[sl]: a if td >= 3 else np.ones_like(a)
                            b1 = wk.run_lines(logistic, gi, V0i, alpha_C=alCi, alpha_D=alDi, n=1, **kwi)
                            d = max(abs(b1.family_true()[0] - book.family_true()[i]),
                                    abs(b1.state_true()[0] - book.state_true()[i]),
                                    abs(b1.lost_refund[0] - book.lost_refund[i]),
                                    abs(b1.unpaid_B[0] - book.unpaid_B[i]), abs(b1.unpaid_D[0] - book.unpaid_D[i]))
                            worst['diff'] = max(worst['diff'], d)
    check('vector_equals_scalar', worst['diff'] < 1e-9, f"{runs} grids x {n} lines; max|diff|={worst['diff']:.2e}")
    check('units_conserved', worst['units'] < TOL, f"max err={worst['units']:.2e}")
    check('caps_hold', worst['min_E_cash'] > -1e-9 and worst['min_A_D'] > -1e-12 and worst['min_EC'] > -1e-9
          and worst['min_state_units'] > -1e-12 and worst['min_uo'] > -1e-12 and worst['uo_excess'] < 1e-12,
          f"min E_cash {worst['min_E_cash']:.1e}, A_D {worst['min_A_D']:.1e}, EC {worst['min_EC']:.1e}, "
          f"state units {worst['min_state_units']:.1e}, uo {worst['min_uo']:.1e}")


def grid_value_conservation():
    """family + state true value + consumed + (income paid from outside) = value created + endowment, per line."""
    rng = np.random.default_rng(11)
    n, T, G = 8, 30, 10
    worst = 0.0
    for b_mode in wk.B_MODES:
        V0, aC, aD, inc = make_inputs(n, rng)
        book = wk.Book(n, V0, alpha0={'C': aC, 'D': aD}, has_cv=True, b_mode=b_mode, r_def=0.03, inc_allow=inc)
        created = np.zeros(n)
        consumed = np.zeros(n)
        start = sum(np.asarray(v) for v in V0.values())
        total_income = np.zeros(n)
        for t in range(1, T + 1):
            ops = wk.step_year(book, logistic, 1.02 ** t, 0.06, 0.03, aC, aD, 0.1, 0.1, False)
            fl = ops[0][1]
            created += sum(fl.growth_family.values()) + sum(fl.growth_state.values())
            consumed += sum(fl.consumed.values())
            if t % G == 0 and t < T:
                wk.step_death(book, logistic, 1.02 ** t, 'delta', True)
        wk.settle_terminal(book)
        total_income = book.inc_total          # paid out of external income, so it is not inside the asset base
        # state_cash holds the income; assets: family + state units
        lhs = book.family_true() + sum(x['s'] * x['V'] for x in book.R.values()) + consumed
        rhs = start + created
        worst = max(worst, float(np.abs(lhs - rhs).max() / rhs.max()))
    check('asset_value_conserved', worst < 1e-9, f'max rel err={worst:.2e}')


# ── 4. parity with valgen_core ───────────────────────────────

def parity_valgen():
    try:
        import valgen_core as vc
        import wdt_core as wc
        p0 = vc.with_rate_scenario(vc.load_params())
        try:
            p = vc.with_val_basis(p0)
        except FileNotFoundError:                            # no JST file: the hand values of [val_gen]
            p = vc.with_val_basis(dict(p0, val_gen=dict(p0['val_gen'], basis='manual', g_real=0.0442, index_rate=0.01872)))
            print('  NOTE  JST file not found: manual basis g_real=0.0442, index_rate=0.01872')
        rp = vc.rate_params(p)
        rpv = dict(rp, wmin=rp['W_min'])                   # rate_vec reads 'wmin'; rate_params gives 'W_min'
        rate = lambda x: wc.rate_vec(np.asarray(x, dtype=float), rpv)
    except Exception as e:                                   # noqa: BLE001
        print(f'  SKIP  parity_valgen_core ({type(e).__name__}: {str(e)[:80]})')
        return
    vg = p['val_gen']
    T, G, g = vg['T'], vg['G'], p['g_real']
    ir = vc._ir(p) if vg['index_wmin'] else 0.0
    ser = [g] * T
    worst, n_runs = 0.0, 0
    for shares in (dict(vg['route_shares']), {'A': 0.2, 'B': 0.5, 'C': 0.2, 'D': 0.1}):
        for mode in wk.B_MODES:
            for aC, aD in ((1.0, 1.0), (0.5, 0.5), (2.0, 0.5), (0.1, 2.0)):
                for lam, dv in ((0.0, False), (0.1, False), (0.1, True)):
                    for rule in ('units', 'units_and_value/reset/on'):
                        o = vc._p5_opts(p, rule, lam)
                        o.update(shares=shares, route_b=mode, r_def=0.03,
                                 income_ratio=0.02, income_cap=1.0, death_verify=dv)
                        ref = vc.run_family3(p, aC, aD, ser, G, vg['heir_influx'], **o)
                        parts = o['c_cap'], o['verify_down'], o['verify_hazard_D']
                        bk = wk.run_lines(rate, ser, {r: s * p['V0_m'] for r, s in shares.items()}, G=G,
                                          heir_influx=vg['heir_influx'], consumption=o['consumption'], index_rate=o['index_rate'],
                                          alpha_C=aC, alpha_D=aD, lam_C=lam, lam_D=o['verify_hazard_D'], death_verify=dv,
                                          n=1, b_mode=mode, c_cap=o['c_cap'], verify_down=o['verify_down'], r_def=0.03,
                                          inc_allow=1.0 * 0.02 * p['V0_m'])
                        d = max(abs(bk.family_true()[0] - ref['family_true_T']), abs(bk.state_true()[0] - ref['state_true_T']))
                        worst = max(worst, d / ref['family_true_T'])
                        n_runs += 1
    check('parity_valgen_run_family3', worst < 1e-9, f'{n_runs} runs; max rel diff={worst:.2e}')


def main():
    print('wdt_kernel tests')
    print('1. hand cases')
    hand_cases()
    print('2/3. vector vs scalar, invariants')
    run_grid()
    grid_value_conservation()
    print('4. parity with valgen_core')
    parity_valgen()
    bad = [r for r in results if not r[1]]
    print(f'\n{len(results) - len(bad)} passed, {len(bad)} failed')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
