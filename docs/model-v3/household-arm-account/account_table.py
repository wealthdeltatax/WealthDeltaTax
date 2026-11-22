"""
account_table.py -- brief 118c (W5b), rerun by 119c with the tail pension ceiling (I-D1l; the one change, plus a pension_share column): the per-line account of the taxed household arm at the centre grid point of the stored digest.
One path, 100 years, the 14 lines, three saving values (the min, median and max of the ONS non-pension saving ratio, none called central); deaths at 30, 60 and 90 (one phase),
the horizon settled. Schedule: tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5 (logistic in ln W, the digest's 'centre'); register central inputs; mid return regime; pension accrual as observed;
incomes scaled to the B.6g factor (inputs_used.json); wealth scale and behavioural loss as the runner shapes the base. Units: millions of pounds per adult, real pounds of the pack's CPI basis.
No revenue, fund or burden number is computed or written. Run from the repository root:   python -I docs/model-v3/household-arm-account/account_table.py
Writes account_table.csv next to itself; prints only summary lines.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

from model_v3.core import kernel as K, pack as pk, schedule as sc  # noqa: E402
from model_v3.runner import arm, runner as R  # noqa: E402

YEARS, G, SHOW = 100, 30, (1, 10, 30, 100)
SPEC = dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5)
COLS = ('line', 'saving_value', 'saving', 'year', 'status', 'dNW', 'S', 'CG', 'T_WDT', 'unpaid_B', 'pay_over_net_financial', 'pay_over_nonpension', 'identity_residual', 'pension_share')


def setup():
    lv, out = json.loads((ROOT / 'model_v3' / 'levers.json').read_text()), yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])
    return ctx, json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())


def one(ctx, inp, name, sav):
    """The 14 lines of one saving value, each run alone (the kernel treats lines independently) until its first payment shortfall: the hook cannot carry a line with no non-pension wealth,
    so a line that exhausts it stops in the year its tax first exceeds what it holds (that year's row is kept, later years are blank with the status)."""
    theta, base = ctx.centre, R.shaped(ctx, ctx.centre, SPEC['ratio'])
    rate = sc.rate_function(SPEC['k_ln'], SPEC['tau_0'], SPEC['tau_m'], base.w_min, 'logistic_ln')
    y, g_i, lc, ld = inp['yreg']['mid'], inp['g'], ctx.centre['I-D14a'] / 100, ctx.centre['I-D14b'] / 100
    gain = dict(property=0.016455, net_financial=inp['regimes']['mid'] - y, physical=0.0, pension=inp['regimes']['mid'] - y)
    full = arm.line_state(base, ctx.pack.tables['decile_composition'], ctx.reg, sav, scale=inp['income_scale'], cap=ctx.reg['I-D1l'].central)
    rows, stopped, neg = [], {}, 0
    for i, lab in enumerate(base.labels):
        sl = lambda v: np.asarray(v)[i:i + 1]
        st = dict(pos={k: sl(v) for k, v in full['pos'].items()}, income=sl(full['income']), sav=sl(full['sav']), acc=sl(full['acc']))
        hook, V0 = arm.HouseholdHook(st, gain, g_i), {r: sl(v) for r, v in base.V0.items()}
        book = K.Book(1, V0, alpha0={'C': 1.0, 'D': 1.0}, has_cv=lc > 0 and 'C' in V0 and bool(np.any(V0['C'] > 0)))
        for t in range(1, YEARS + 1):
            idx = (1.0 + g_i) ** t
            K.step_year(book, rate, idx, np.zeros(1), 0.0, 1.0, 1.0, lc, ld, False, hook, t)
            if t % G == 0 and t < YEARS:
                K.step_death(book, rate, idx)
                hook.reconcile(book)
            if t == YEARS:
                K.settle_terminal(book)
                hook.reconcile(book)
            a, short = hook.account(), K.shortfall_lines(book) > 0
            neg += sum(hook.q[k][0] for k in arm.CLASSES) < 0
            if t in SHOW or short:
                rows.append(dict(line=lab, saving_value=name, saving=sav, year=t, status='shortfall' if short else 'ok', dNW=a['dNW'][0], S=a['S'][0], CG=a['CG'][0], T_WDT=a['T_WDT'][0], unpaid_B=book.unpaid_B[0],
                                 pay_over_net_financial=a['pay_over_fin'][0], pay_over_nonpension=a['pay_over_nonpension'][0], identity_residual=a['residual'][0], pension_share=hook.q['pension'][0] / sum(hook.q[k][0] for k in arm.CLASSES)))
            if short:
                stopped[lab] = t
                rows += [dict(line=lab, saving_value=name, saving=sav, year=u, status=f'stopped after the shortfall of year {t}') for u in SHOW if u > t]
                break
    return rows, stopped, neg


def main():
    ctx, inp = setup()
    rows, summary = [], {}
    for name, sav in inp['sav'].items():
        r, stopped, neg = one(ctx, inp, name, sav)
        rows += r
        summary[name] = (stopped, neg)
    with open(HERE / 'account_table.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rows)
    ok = [r for r in rows if 'dNW' in r]
    print(f'rows {len(rows)} ({len(ok)} with numbers); max |identity residual| {max(abs(r["identity_residual"]) for r in ok):.2e}')
    for name, (stopped, neg) in summary.items():
        print(f'{name}: lines stopped by a shortfall (line: year) {stopped}; line-years with negative total wealth {neg}')
    fin = [r['pay_over_nonpension'] for r in ok if np.isfinite(r['pay_over_nonpension'])]
    print(f'max payment over non-pension wealth {max(fin):.4f}; rows with an infinite ratio {len(ok) - len(fin)}; rows above 1: {sum(x > 1 for x in fin)}')


if __name__ == '__main__':
    main()
