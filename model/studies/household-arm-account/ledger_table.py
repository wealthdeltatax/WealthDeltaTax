"""
ledger_table.py -- brief 120c (W6, block 3): the identity table of the public ledger of the taxed household arm.
The production path (revenue.run_lines with the HouseholdHook, six death phases, deaths every 30 years, the horizon settled in year 100, then revenue.revenue for the ledger),
at the centre grid point of the stored digest and the B.6g income scaling of the 118c/119c account script (account_table.setup, line_state and the same three saving values, none called
central); one path, real growth zero in the kernel (the household's class returns carry the growth), GDP per head growing at the index rate. Years 1, 10, 30 and 100.
Units: billions of pounds, real, of the pack's CPI basis; receipts, return, payout and closing balance by ledger class (property, net financial, physical, safe); the pension is not a class.
Receipts include the corporate levy as cash (net financial and the safe asset by `safe_share`, I-D14f); the safe asset earns the net financial class return (a stand-in: no safe return is wired).
Two residuals: `res_pay` (household payments weighted over the lines, minus the ledger's WDT receipts, which are its receipts less the levy) and `res_dL` (the largest class |dL - (receipts + return - payout)|).
No revenue, fund-fill or burden number is read or written. Run from the repository root:   python -I model/studies/household-arm-account/ledger_table.py
Writes ledger_table.csv next to itself; prints only summary lines.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'results' / 'household-arm-account'   # outputs and stored tables stay here until 163c
sys.path[:0] = [str(ROOT / 'model'), str(HERE)]

import account_table as A                                                      # noqa: E402  (the 118c/119c account: setup, SPEC, the same grid point)
from model_v3.core import kernel as K, revenue as rv, schedule as sc          # noqa: E402
from model_v3.runner import arm, runner as R                                   # noqa: E402

KS, T, G, N_PHASE = ('property', 'net_financial', 'physical', 'safe'), 100, 30, 6
COLS = ('saving_value', 'saving', 'year') + tuple(f'{w}_{k}' for k in KS for w in ('receipts', 'return', 'payout', 'closing')) + ('res_pay', 'res_dL', 'unpaid_B_max', 'shortfall_lines')


class Tally(arm.HouseholdHook):
    """Adds up what the households pay (billions of pounds, weighted over the lines), by year: the household side of the tie."""

    def __init__(self, base, *a, **k):
        super().__init__(*a, **k)
        self.w, self.A, self.paid, self.t = base.weights / N_PHASE, base.adults_k.sum(), {}, 0

    def pre(self, book, t, g):
        self.t = t
        return super().pre(book, t, g)

    def _pay(self, q, T_):
        self.paid[self.t] = self.paid.get(self.t, 0.0) + (self.w[None, :] * np.asarray(T_, float).reshape(-1, 14)).sum(axis=1) * self.A
        return super()._pay(q, T_)


def main():
    ctx, inp = A.setup()
    th, spec = ctx.centre, A.SPEC
    base = R.shaped(ctx, th, spec['ratio'])
    rate = sc.rate_function(spec['k_ln'], spec['tau_0'], spec['tau_m'], base.w_min, 'logistic_ln')
    y, g_i, c = inp['yreg']['mid'], inp['g'], th['I-D14c'] / 100
    gain = dict(property=0.016455, net_financial=inp['regimes']['mid'] - y, physical=0.0, pension=inp['regimes']['mid'] - y)
    books, orig, rows = [], K.Book, []
    K.Book = lambda *a, **k: books.append(orig(*a, **k)) or books[-1]               # the production books, to read unpaid_B and the shortfalls
    try:
        for name, sav in inp['sav'].items():
            books.clear()
            st = arm.line_state(base, ctx.pack.tables['decile_composition'], ctx.reg, sav, scale=inp['income_scale'], cap=ctx.reg['I-D1l'].central)
            h, g0 = Tally(base, st, gain, g_i), np.zeros((T, 1))
            run = rv.run_lines(base, rate, g0, np.full((T, 1), g_i), c, G=G, n_phase=N_PHASE, hook=h, **R.env_of(ctx, th).lam)
            o = rv.revenue(run, ctx.gdp0, th['I-D7a'], ctx.rec, g0, ctx.exp, c, int(th['I-D14d']), th['I-D8a'], th['I-D8a'], int(th['I-D14e']), np.full((T, 1), gain['net_financial']), th['I-D14f'] / 100)
            f, levy = o['fund'], th['I-D7a'] / 100 * run['gdp_index'] * ctx.gdp0
            wdt = sum(run['ledger']['rc'].values())
            res_pay = np.concatenate([h.paid[t] for t in range(1, T + 1)]) - wdt[:, 0]
            dL = {k: np.diff(np.concatenate([[0.0], f['L'][k][:, 0]])) - (f['rc'][k][:, 0] + f['ret'][k][:, 0] - f['pay'][k][:, 0]) for k in KS}
            res_dL = np.max([np.abs(v) for v in dL.values()], axis=0)
            ub, sf = max(float(np.max(b.unpaid_B)) for b in books), sum(K.shortfall_lines(b) for b in books)
            for t in A.SHOW:
                rows.append({'saving_value': name, 'saving': sav, 'year': t, 'res_pay': res_pay[t - 1], 'res_dL': res_dL[t - 1], 'unpaid_B_max': ub, 'shortfall_lines': sf,
                             **{f'{w}_{k}': f[src][k][t - 1, 0] for k in KS for w, src in (('receipts', 'rc'), ('return', 'ret'), ('payout', 'pay'), ('closing', 'L'))}})
            print(f'{name}: max |res_pay| {np.abs(res_pay).max():.2e}; max |res_dL| {res_dL.max():.2e}; max unpaid_B {ub:.2e}; shortfall lines {sf}; levy in receipts, year 1: {levy[0, 0]:.3f}')
    finally:
        K.Book = orig
    with open(DATA / 'ledger_table.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        w.writerows(rows)
    print(f'rows {len(rows)}; pension in a ledger class: {"pension" in f["L"]}')


if __name__ == '__main__':
    main()
