"""
cell_baseline.py -- brief 110c: the untaxed baseline of the ten cells under convention A (and B, and the legacy rule), 100 years.
Brief 111c reruns it with the pension accrual as a share of income (I-D1k, D.8 over B.6g) and every cell's income scaled by one factor to the B.6g total of 2024 (the run is labelled
aggregate-constrained; the unscaled run is kept as a sensitivity).
A one-off measurement outside model_v3: it imports model_v3.core.cells and the runner's context, and edits neither. Nothing is tuned.

Run from the repository root:   python -I docs/model-v3/cell-baseline/cell_baseline.py
Writes cell_paths.csv, aggregates.csv and tables.md next to itself; prints only summary lines.
"""
from __future__ import annotations

import csv
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np
import openpyxl
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
HERE = Path(__file__).resolve().parent

from model_v3.core import cells as ce, pack as pk  # noqa: E402
from model_v3.runner import runner as R  # noqa: E402

YEARS, D = 100, ROOT / 'docs' / 'research' / 'data'
CLASSES = ce.CLASSES


def rows_of(name, folder):
    return list(csv.DictReader(open(D / folder / name, newline='', encoding='utf-8')))


def inputs():
    lv = json.loads((ROOT / 'model_v3' / 'levers.json').read_text())
    out = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    pack, reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
    ctx = R.context(pack, reg, lv, tier1, [o['id'] for o in out['outputs']])
    # saving ratio: the ONS non-pension part of the saving ratio, 1998 to 2025 (101r derived series), percent
    s = [float(r['value']) / 100 for r in rows_of('derived_ons_flows.csv', '101r') if r['item'] == 'ratio_nonpension_part_pct']
    sav = dict(min=min(s), median=st.median(s), max=max(s))
    # retired fraction: ETB FYE 2024 Tables 3a (non-retired) and 4a (retired), household-weighted mean gross income over the five quintiles
    wb = openpyxl.load_workbook(ROOT / 'Research' / 'etbreferencetablesfye202324final.xlsx', read_only=True, data_only=True)

    def mean_gross(t):
        rows = [list(r) for r in wb[t].iter_rows(values_only=True)]
        f = lambda lab: next(r for r in rows if str(r[1]).startswith(lab) or str(r[0]).startswith(lab))[2:7]
        n, g = f('Number of households'), f('Gross income')
        return sum(a * b for a, b in zip(n, g)) / sum(n)
    etb = mean_gross('Table 4a') / mean_gross('Table 3a')
    # regime yields: JST portfolio real cash yield, 1947 to 1979 and 1980 to 2019 (101r jst_split_stats)
    y = {r['period_or_check']: float(r['mean_or_value']) / 100 for r in rows_of('jst_split_stats.csv', '101r') if r['item'] == 'portfolio_y_real'}
    return ctx, pack, reg, sav, etb, dict(low=y['1947_1979'], high=y['1980_2019'], mid=(y['1947_1979'] + y['1980_2019']) / 2), y['all_1896_2019']


def run(cells, kind, sav, acc, growth, rets, convention='A', c=0.0):
    """-> {cell: rows} and the aggregate arrays by year 0..YEARS."""
    paths = {x['cell']: ce.run_cell(x, YEARS, sav, acc, growth, rets, convention, c) for x in cells}
    return paths


def aggregate(cells, paths, growth):
    n = np.array([x['households'] for x in cells])
    pos = np.array([[[x['pos'][k] for k in CLASSES]] + [[r[1][k] for k in CLASSES] for r in paths[x['cell']]] for x in cells])   # cell, year, class
    nw = pos.sum(2)
    W = (n[:, None] * nw).sum(0) * ce.UNIT                                 # pounds
    idx = (1.0 + growth) ** np.arange(YEARS + 1)
    flow = lambda k: np.array([[float(r[2][k]) for r in paths[x['cell']]] for x in cells])
    S, CG, Y, dNW = flow('S'), flow('CG'), flow('income'), flow('dNW')
    stock = np.diff(nw, axis=1)
    resid = float(np.abs(stock - dNW).max()), float(np.abs(dNW - (S + CG + flow('O'))).max())
    ratio = (n[:, None] * S).sum(0) / (n[:, None] * Y).sum(0)
    bands = {b: (n[[i for i, x in enumerate(cells) if x['band'] == b]][:, None] * nw[[i for i, x in enumerate(cells) if x['band'] == b]]).sum(0) * ce.UNIT / W for b in ce.BANDS}
    return dict(W=W, wgdp=(W / idx) / W[0], ratio=ratio, bands=bands, resid=max(resid), flows=((n[:, None] * S).sum(0), (n[:, None] * CG).sum(0)), n=n, pos=pos)


def tab(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    return '\n'.join(out + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])


def tables(res, runs, pack, reg, sav, etb, g, x):
    """tables.md: the units reconciliation, the runs, the account terms, the sensitivities and the checks."""
    P = lambda v, d=1: f'{v:.{d}f}'
    wd = lambda var: next(r['value'] for r in pack.tables['wealth_distribution'] if r['variable'] == var and r['band'] == 'all')
    base = runs['A_mid_median']['cells']
    n = np.array([x['households'] for x in base])
    pers = sum(r['persons'] for r in pack.tables['cell_weights'])
    inc = sum(x['households'] * x['income'] for x in base) * ce.UNIT
    W0 = float(res['A_mid_median']['W'][0])
    d8 = {r['year']: float(r['value']) for r in rows_of('derived_ons_flows.csv', '101r') if r['item'] == 'D8_pension_adj'}
    acc1 = reg['I-D1k'].central / 100 * inc
    inc_raw = sum(c['households'] * c['income'] for c in x['raw']) * ce.UNIT
    u = ['### Units and reconciliation (wealth and households as the pack has them; income scaled to B.6g 2024)\n',
         'Money is carried in thousands of pounds per household inside the module (so the identity check is not at the mercy of rounding) and reported in pounds. Weights are households.\n',
         tab(['quantity', 'cells', 'reference', 'gap'], [
             ['households (millions)', P(n.sum() / 1e6, 3), f'{wd("households") / 1e3:.3f} (pack, all)', f'{P(100 * (n.sum() / (wd("households") * 1e3) - 1), 2)}%'],
             ['persons 16+ (millions, cell_weights)', P(pers / 1e6, 3), f'{P(n.sum() / 1e6 * reg["I-D4h"].central, 3)} (households times I-D4h {reg["I-D4h"].central}); {P(n.sum() / 1e6 * reg["I-D4h"].low, 3)} at {reg["I-D4h"].low}',
              f'{P(100 * (pers / (n.sum() * reg["I-D4h"].central) - 1), 1)}% against central, {P(100 * (pers / (n.sum() * reg["I-D4h"].low) - 1), 1)}% against low'],
             ['wealth (pounds, billions)', P(W0 / 1e9, 1), f'{wd("wealth_total"):.0f} (pack, all)', f'{P(100 * (W0 / 1e9 / wd("wealth_total") - 1), 2)}%'],
             ['wealth over GDP at the start', P(W0 / 1e9 / wd('gdp'), 2), f'{wd("gdp"):.0f} billion GDP (pack, 2020 to 2022 mean)', 'by construction the pack total'],
             ['pension accrual in year 1 (pounds, billions), I-D1k observed 2024 share times cell income', P(acc1 / 1e9, 1), f'{d8["2024"] / 1e3:.1f} (ONS D.8 2024); share of B.6g {reg["I-D1k"].central / 100:.4f} times {x["b6g"] / 1e9:.1f}', f'{P(100 * (acc1 / 1e6 / d8["2024"] - 1), 2)}%'],
             ['non-pension saving in year 1 at the median ratio (pounds, billions)', P(sav['median'] * inc / 1e9, 0), f'{next(float(r["value"]) for r in rows_of("derived_ons_flows.csv", "101r") if r["item"] == "nonpension_saving_GBPm" and r["year"] == "2024") / 1e3:.0f} (ONS non-pension saving 2024)', 'a ratio of income, not matched in level'],
             ['income, scaled (pounds, billions): every cell times one factor', P(inc / 1e9, 1), f'{x["b6g"] / 1e9:.1f} (ONS B.6g, calendar 2024, no price adjustment)', f'{P(100 * (inc / x["b6g"] - 1), 4)}% (by construction)'],
             ['income before scaling (pounds, billions, per household table, FYE 2024, gross)', P(inc_raw / 1e9, 1), f'factor {x["k"]:.4f} to reach B.6g 2024', f'{P(100 * (inc_raw / x["b6g"] - 1), 1)}% before scaling']]),
         '\nWealth matches the pack by construction. The main runs are aggregate-constrained: income is scaled by the one factor above (band proportions and the retired split kept; B.6g is disposable income and the per-household table is gross, so the factor is a concept-and-level adjustment, not a correction). The run `S_unscaled` keeps the unscaled income as a sensitivity.\n']
    yrs = (0, 10, 50, 100)
    names = [k for k in runs if k.startswith('A_')]
    r1 = [[k, P(runs[k]['sav'] * 100, 2), *[P(res[k]['wgdp'][t], 2) for t in yrs], *[P(100 * res[k]['ratio'][max(t, 1) - 1], 1) for t in yrs], f'{res[k]["resid"]:.1e}'] for k in names + ['legacy']]
    t1 = ['### Runs: wealth over GDP (index, start = 1.00) and the realised saving ratio (saving including the pension accrual, over cell income, percent; year 0 shows year 1)\n',
          tab(['run', 'saving %', *[f'W/GDP y{t}' for t in yrs], *[f'ratio y{t}' for t in yrs], 'identity residual'], r1)]
    k = 'A_mid_median'
    acct = lambda kk, t: (float(res[kk]['flows'][0][t - 1] / res[kk]['W'][t - 1]) * ce.UNIT, float(res[kk]['flows'][1][t - 1] / res[kk]['W'][t - 1]) * ce.UNIT)
    t2 = ['### Account terms: saving plus gain over opening wealth, against GDP growth {:.2f}%\n'.format(100 * g),
          tab(['run', 'year', 'S/W %', 'CG/W %', 'dNW/W %', 'GDP growth %'], [[kk, t, *[P(100 * x, 2) for x in acct(kk, t)], P(100 * sum(acct(kk, t)), 2), P(100 * g, 2)] for kk in ('A_low_median', 'A_mid_median', 'A_high_median', 'legacy') for t in (1, 10, 50, 100)])]
    bn = list(ce.BANDS)
    t3 = ['### Share of wealth by band\n', tab(['run', 'year', *bn], [[kk, t, *[P(100 * res[kk]['bands'][b][t], 1) for b in bn]] for kk in ('A_mid_median', 'legacy') for t in yrs])]
    sens = [('accrual low (3.01% of income)', 'S_accrual_low'), ('accrual observed 2024 (4.83%, the main run)', 'A_mid_median'), ('accrual high (9.74%)', 'S_accrual_high'), ('income not scaled', 'S_unscaled'),
            (f'retired fraction {P(etb, 3)} (the main run)', 'A_mid_median'), ('retired fraction 0.6', 'S_retired_0.6'), ('retired fraction 0.8', 'S_retired_0.8')]
    t4 = ['### Sensitivities (return mid-point label, saving median)\n', tab(['variant', 'W/GDP y10', 'y50', 'y100'], [[n, *[P(res[kk]['wgdp'][t], 2) for t in (10, 50, 100)]] for n, kk in sens])]
    a, b = res['A_mid_median'], res['B_mid_median']
    t5 = ['### Convention B check (return mid, saving median)\n',
          f'Year 1 aggregate dNW: A {a["flows"][0][0] + a["flows"][1][0]:.6e} (per-household money units, summed), B {b["flows"][0][0] + b["flows"][1][0]:.6e}; relative difference {abs((a["flows"][0][0] + a["flows"][1][0]) / (b["flows"][0][0] + b["flows"][1][0]) - 1):.2e}. '
          f'Identity residual A {a["resid"]:.1e}, B {b["resid"]:.1e}. The paths then differ (W/GDP y100 {P(a["wgdp"][100], 2)} in A, {P(b["wgdp"][100], 2)} in B) because B credits the yield to the class that earns it and A leaves it in net financial wealth: the two conventions are equal in the first year, not in composition afterwards.\n']
    neg = []
    for kk in names + ['legacy']:
        pos = res[kk]['pos']
        first = [int(np.argmax(pos[i].sum(1) < 0)) if (pos[i].sum(1) < 0).any() else None for i in range(len(base))]
        nf = [int(np.argmax(pos[i][:, 1] < 0)) if (pos[i][:, 1] < 0).any() else None for i in range(len(base))]
        neg.append([kk, ', '.join(f'{base[i]["cell"]} y{f}' for i, f in enumerate(first) if f) or 'none', ', '.join(f'{base[i]["cell"]} y{f}' for i, f in enumerate(nf) if f) or 'none'])
    t6 = ['### Negative positions (first year)\n', tab(['run', 'net worth below zero', 'net financial wealth below zero'], neg)]
    (HERE / 'tables.md').write_text('\n\n'.join(['\n'.join(x) if isinstance(x, list) else x for x in (u, t1, t2, t3, t4, t5, t6)]) + '\n')


def main():
    ctx, pack, reg, sav, etb, yreg, y_all = inputs()
    g = ctx.gdp_g
    gprop = dict(property=0.016455)                                      # F-20: the JST housing holding gain, all years (the yield 3.758 is inside saving)
    cls = lambda gfin, gpen: dict(g=dict(property=gprop['property'], net_financial=gfin, physical=reg['I-D1j'].central / 100, pension=gpen), y=dict(property=0.03758, net_financial=0.0, pension=0.0))
    regimes = {k: reg['I-D1h'].__getattribute__(a) / 100 for k, a in (('low', 'low'), ('mid', 'central'), ('high', 'high'))}
    rets = {k: dict(g=dict(property=0.016455, net_financial=regimes[k] - yreg[k], physical=reg['I-D1j'].central / 100, pension=regimes[k] - yreg[k]),
                    y=dict(property=0.03758, net_financial=yreg[k], physical=0.0, pension=yreg[k])) for k in regimes}
    acc = {k: getattr(reg['I-D1k'], a) / 100 for k, a in (('low', 'low'), ('obs', 'central'), ('high', 'high'))}
    b6g = 1e6 * next(float(r['value']) for r in rows_of('derived_ons_flows.csv', '101r') if r['item'] == 'B6g_gdhi' and r['year'] == '2024')          # pounds, calendar 2024, no price adjustment
    raw = ce.cell_table(pack, reg, etb)
    base, kfac = ce.scaled(raw, b6g)
    runs = {}
    for rg in regimes:
        for sv in sav:
            runs[f'A_{rg}_{sv}'] = dict(cells=base, sav=sav[sv], acc=acc['obs'], rets=rets[rg], conv='A', note=f'return {rg}, saving {sv}, accrual observed, retired {etb:.3f}, aggregate-constrained')
    for a in ('low', 'high'):
        runs[f'S_accrual_{a}'] = dict(cells=base, sav=sav['median'], acc=acc[a], rets=rets['mid'], conv='A', note=f'return mid, saving median, accrual {a}')
    runs['S_unscaled'] = dict(cells=raw, sav=sav['median'], acc=acc['obs'], rets=rets['mid'], conv='A', note='return mid, saving median, accrual observed, income not scaled')
    for f in (0.6, 0.8):
        runs[f'S_retired_{f}'] = dict(cells=ce.scaled(ce.cell_table(pack, reg, f), b6g)[0], sav=sav['median'], acc=acc['obs'], rets=rets['mid'], conv='A', note=f'return mid, saving median, accrual observed, retired {f}')
    runs['B_mid_median'] = dict(cells=base, sav=sav['median'], acc=acc['obs'], rets=rets['mid'], conv='B', note='convention B check of A_mid_median')
    runs['legacy'] = dict(cells=base, sav=0.0, acc=0.0, rets=dict(r=reg['I-D1a'].central / 100), conv='legacy', c=reg['I-D14c'].central / 100, note='legacy rule: W(1+r)(1-c), r I-D1a, c I-D14c')
    res, cw, aw = {}, csv.writer(open(HERE / 'cell_paths.csv', 'w', newline='')), csv.writer(open(HERE / 'aggregates.csv', 'w', newline=''))
    cw.writerow(['run', 'cell', 'year', 'households', *CLASSES, 'dNW', 'S', 'CG', 'CG_wedge', 'O'])
    aw.writerow(['run', 'year', 'wealth', 'wealth_over_gdp_index', 'saving_ratio', *[f'share_{b}' for b in ce.BANDS]])
    for name, r in runs.items():
        paths = run(r['cells'], name, r['sav'], r['acc'], g, r['rets'], r['conv'], r.get('c', 0.0))
        a = aggregate(r['cells'], paths, g)
        res[name] = a
        for x in r['cells']:
            cw.writerow([name, x['cell'], 0, round(x['households']), *[round(x['pos'][k], 2) for k in CLASSES], '', '', '', '', ''])
            for t, pos, ac in paths[x['cell']]:
                cw.writerow([name, x['cell'], t, round(x['households']), *[round(float(pos[k]), 2) for k in CLASSES], *[round(float(ac[k]), 4) for k in ('dNW', 'S', 'CG', 'CG_wedge', 'O')]])
        for t in range(YEARS + 1):
            aw.writerow([name, t, round(a['W'][t]), round(a['wgdp'][t], 5), round(a['ratio'][min(max(t, 1), YEARS) - 1], 5), *[round(a['bands'][b][t], 5) for b in ce.BANDS]])
        print(f'{name}: W/GDP index y10 {a["wgdp"][10]:.3f} y50 {a["wgdp"][50]:.3f} y100 {a["wgdp"][100]:.3f}; residual {a["resid"]:.2e}')
    json.dump(dict(sav=sav, etb=etb, yreg=yreg, y_all=y_all, regimes=regimes, acc=acc, g=g, b6g_2024=b6g, income_scale=kfac), open(HERE / 'inputs_used.json', 'w'), indent=1)
    tables(res, runs, pack, reg, sav, etb, g, dict(b6g=b6g, k=kfac, raw=raw))
    return res


if __name__ == '__main__':
    main()
