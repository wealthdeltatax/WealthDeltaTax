"""
5_10_VAL_examples.py — worked-example tables for VAL.B (plan phases 3 and 8)
===========================================================================
One markdown table block per example, generated from valgen_data.json ('life' block); inputs are in
[val_gen.life_examples] and [val_gen.route_d_examples]. Table-only outputs, so they sit outside the
figure/table pair mechanism. Ids: DEF (legacy J), DIL (K), RDD (L), VOL (M), FEX (N); see the register.
Presentation layer: no simulation, no core import.

Output: OUTPUTS/VAL/tables/val_example_<ID>.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # model root
from wdt_core import load_params
from wdt_fmt import out_dir, ensure_dir, fmt_pct
from wdt_md import MdDoc, md_table

_DATA = out_dir('VAL') / 'valgen_data.json'
_OUT = out_dir('VAL') / 'tables'


def _m(v: float, d: int = 3) -> str:
    return f'£{v:,.{d}f}m'


def _life_example(data: dict, key: str, eid: str, title: str) -> str:
    ex = data['life']['examples'][key]
    runs = ex['runs']
    alphas = [str(a) for a in ex['alphas']]
    honest = runs['1.0']
    heads = ['α', 'Tax paid in the holding period (true value)', 'Tax at sale', 'Post-sale settlement', 'Net tax',
             'Terminal wealth', 'Terminal wealth vs honest', 'Net tax vs honest']
    rows = []
    for a in alphas:
        r = runs[a]
        tw_rel = r['TW_settled'] / honest['TW_settled'] - 1.0
        net_rel = r['Net_settled'] / honest['Net_settled'] - 1.0
        rows.append([f'**{a}**', _m(r['hold_true']), _m(r['sell_L']), _m(r['settle_net']), _m(r['Net_settled']),
                     _m(r['TW_settled']), '-' if a == '1.0' else fmt_pct(tw_rel, 2),
                     '-' if a == '1.0' else fmt_pct(net_rel, 2)])
    cap = (f"Table {eid}: {title}. Single life, Route C, asset value {_m(ex['V0_m'], 1)} at entry, growth "
           f"{fmt_pct(ex['g'], 1)} a year, held {ex['N']} years then sold. Terminal wealth includes post-sale settlement. "
           f"Declaration ratio α = 1.0 is honest.")
    out = md_table(heads, rows, col_fmt=['center'] * len(heads)) + '\n\n' + cap
    for a in alphas:
        rr = runs[a]['rows']
        h2 = ['Year', 'True value', 'Declared', 'Delta', 'Marginal rate', 'Tax', 'Retained fraction']
        r2 = [[str(x['t']), _m(x['V']), _m(x['W']), _m(x['delta']), fmt_pct(x['rate'], 2), _m(x['L']), f"{x['f']:.4f}"]
              for x in rr]
        out += '\n\n' + md_table(h2, r2, col_fmt=['center'] * len(h2)) + \
            f"\n\nTable {eid}.{a}: Year by year, α = {a}, entry {_m(ex['V0_m'], 1)}."
    return out


def _example_L(data: dict) -> str:
    L = data['life']['route_d_examples']['L']
    inp = L['inputs']
    heads = ['Year', 'True value', 'Annual liability (annual settlement)', 'Cumulative, annual settlement',
             'Accrued liability (Route D)']
    rows = [[str(r['t']), _m(r['V']), _m(r['annual_L']), _m(r['cum_L']), _m(r['D_accrued'])] for r in L['rows']]
    cmp_heads = ['Metric', 'Annual settlement (Route A)', 'Route D']
    cmp_rows = [['Cash-equivalent demand during the holding period', _m(L['A']['cash_demand_total']), _m(0.0)],
                ['Settled at the end, true value', '-', _m(L['D']['settlement_true'])],
                ["State's terminal stake, true value", _m(L['A']['state_true_T']), _m(L['D']['state_true_T'])],
                ['Family terminal wealth, true value', _m(L['A']['family_true_T']), _m(L['D']['family_true_T'])]]
    cap1 = (f"Table RDD: Annual liability on a non-fungible asset of {_m(inp['V0_m'], 1)} growing {fmt_pct(inp['g'], 1)} a "
            f"year, over {inp['N']} years: paid each year under annual settlement, accrued under Route D with no payment until "
            f"the end of the horizon.")
    cap2 = "Table RDD.1: Comparison at the end of the horizon, same asset and growth."
    return (md_table(heads, rows, col_fmt=['center'] * len(heads)) + '\n\n' + cap1 + '\n\n' +
            md_table(cmp_heads, cmp_rows, col_fmt=['left', 'center', 'center']) + '\n\n' + cap2)


def _example_M(data: dict) -> str:
    M = data['life']['route_d_examples']['M']
    inp = M['inputs']
    names = {'soft': 'Soft reset', 'hard': 'Hard reset', 'none': 'No reset'}
    heads = ['Option', 'Settled at the reset', 'Settled at the end', "State's terminal stake", 'Family terminal wealth']
    rows = []
    for k, o in M['options'].items():
        at_reset = sum(tv for (t, kind, tv, cr) in o['settlements'] if kind == 'reset_D')
        at_end = sum(tv for (t, kind, tv, cr) in o['settlements'] if kind != 'reset_D')
        rows.append([f'**{names[k]}**', _m(at_reset), _m(at_end), _m(o['state_true_T']), _m(o['family_true_T'])])
    cap = (f"Table VOL: Voluntary settlement of a Route D asset of {_m(inp['V0_m'], 1)} growing {fmt_pct(inp['g'], 1)} a year. "
           f"Soft reset: {fmt_pct(inp['soft_factor'], 1)} of true value declared in year {inp['N_reset']} only. Hard reset: "
           f"settled at true value in year {inp['N_reset']}. Horizon {inp['N_death']} years. A hard-reset auction would cost "
           f"{_m(M['auction_cost'])} (an input, not in the settled figures).")
    return md_table(heads, rows, col_fmt=['left'] + ['center'] * 4) + '\n\n' + cap


def main() -> None:
    p = load_params()
    data = json.load(open(_DATA, encoding='utf-8'))
    ensure_dir(_OUT)
    docs = {'DEF': _life_example(data, 'J', 'DEF', 'Deferred delta: understatement compared with honest declaration'),
            'DIL': _life_example(data, 'K', 'DIL', 'Dilution under understatement at high growth'),
            'FEX': _life_example(data, 'N', 'FEX', 'Forecast exposure: three founders, same asset'),
            'RDD': _example_L(data), 'VOL': _example_M(data)}
    for eid, md in docs.items():
        d = MdDoc()
        d.add_block(md)
        d.write(_OUT / f'val_example_{eid}.md')


if __name__ == '__main__':
    main()
