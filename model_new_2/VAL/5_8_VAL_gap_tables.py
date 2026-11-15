"""
5_8_VAL_gap_tables.py — gap tables for the old VAL figures (presentation layer)
===============================================================================
The plan (VAL_tables_figures_plan.md, section 1) requires every figure to have a paired
table. Five old figures have none: Fig 5, 7.1b, 7.1c, 7.2b, 7.2c. This script adds one small
table for each. It reads the same keys of OUTPUTS/VAL/valgen_data.json that the old chart
script 5_4_VAL_charts.py reads, and it does not touch the old tables (5_3_VAL_tables.py) or
the old charts.

Layer rules: never simulates, never imports val_core or another presentation script. Uses
wdt_core (load_params only), wdt_fmt, wdt_md. Every grid, tolerance and label comes from
WDT_Params.toml ([val]) or from the JSON.

Units. valgen_data.json stores the cost curves and surfaces in percentage points of honest
TW(1) (not fractions) and tau(W) as a fraction. Cells are printed with the unit named in the
header; nothing is multiplied here except tau, via fmt_pct.

Contract: build_<ID>(data, p) -> {'md', 'values'}, as in 5_6_VALGEN_tables.py.
Output: OUTPUTS/VAL/tables/val_table_gap_<ID>_<slug>.md

    python 5_8_VAL_gap_tables.py [IDs]
"""

from __future__ import annotations

import json
import sys

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # model root: wdt_core, wdt_fmt, wdt_md, wdt_style

from wdt_core import load_params
from wdt_fmt import out_dir, ensure_dir, fmt_pct
from wdt_md import MdDoc, md_table

_DATA = out_dir('VAL') / 'valgen_data.json'
_OUT = out_dir('VAL') / 'tables'

# Old figure -> the JSON chart key it draws (same key 5_4_VAL_charts.py reads), slug, title.
PAIRS = {
    'F5':   {'json': ['charts', 'fig_5_rate_function'], 'slug': 'rate_function',
             'title': 'Marginal rate function'},
    'F7_1b': {'json': ['charts', 'fig_7_1b_equilibrium_cost_curve'], 'slug': 'equilibrium_cost_curve',
              'title': 'Declaration equilibrium cost curves'},
    'F7_1c': {'json': ['charts', 'fig_7_1c_tw_advantage_gN_surface'], 'slug': 'gN_surface',
              'title': '(g, N) surfaces'},
    'F7_2b': {'json': ['charts', 'fig_7_2b_saturation_reversal'], 'slug': 'saturation_reversal',
              'title': 'Understater penalty structure'},
    'F7_2c': {'json': ['charts', 'fig_7_2c_overstatement_reversal'], 'slug': 'overstatement_reversal',
              'title': 'Overstater reversal boundary'},
}


def load_data(path=_DATA) -> dict:
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def get_key(data: dict, path: list):
    cur = data
    for part in path:
        cur = cur[part]
    return cur


def _check_stamp(cd: dict, p: dict, name: str) -> None:
    n = cd.get('N')
    if isinstance(n, int) and n != p['N_val']:
        raise ValueError(f'{name}: data N stamp {n} != N_val {p["N_val"]}. Re-run val_core.py.')


def _nearest(grid, x) -> int:
    return min(range(len(grid)), key=lambda i: abs(grid[i] - x))


def _g_label(g_pct: float) -> str:
    return f'{g_pct:.2f}%'


def _pp(v: float, dp: int = 2) -> str:
    return f'{v:+.{dp}f}'


# ── Fig 5 ────────────────────────────────────────────────────────────────────

def build_F5(data: dict, p: dict) -> dict:
    cd = get_key(data, PAIRS['F5']['json'])
    ws, ts = cd['w_vals'], cd['tau_vals']
    rows, values = [], []
    for w in p['rate_table_W']:
        i = _nearest(ws, w)
        rows.append([f'**£{ws[i]:.4g}m**', fmt_pct(ts[i], 2)])
        values += [ws[i], ts[i]]
    cap = (f"Table 5.G: Marginal rate τ(W) at selected declared net worth, read from the plotted curve "
           f"(nearest plotted grid point to the requested W). k = {p['k']}, τ_0 = {fmt_pct(p['tau_0'], 0)}, "
           f"τ_m = {fmt_pct(p['tau_m'], 0)}, W_min = £{p['W_min']:g}m. "
           f"Entry rate at W_min = {fmt_pct(ts[0], 2)}.")
    return {'md': md_table(['Declared net worth W', 'Marginal rate τ(W)'], rows, col_fmt=['center', 'center'])
            + '\n\n' + cap, 'values': values}


# ── Fig 7.1b ─────────────────────────────────────────────────────────────────

def build_F7_1b(data: dict, p: dict) -> dict:
    cd = get_key(data, PAIRS['F7_1b']['json'])
    _check_stamp(cd, p, 'Fig 7.1b')
    af = cd['alpha_fine']
    gs = cd['g_scenarios']
    net_by_g = cd.get('net_pct_by_g', cd.get('cost_by_g'))
    tw_by_g = cd['tw_cost_by_g']
    hist_net = cd.get('hist_net_pct', cd.get('hist_cost'))
    hist_tw = cd['hist_tw_cost']
    yr = data['meta']['scenario_start_year']
    idx = [_nearest(af, a) for a in p['cost_curve_alphas']]
    values = []

    def block(by_g, hist):
        heads = ['α'] + [f'g = {g * 100:.1f}%' for g in gs] + [f'{yr} historical series']
        rows = []
        for i in idx:
            row = [f'**{af[i]:.2f}**']
            for g in gs:
                v = by_g[str(g)][i]
                row.append(_pp(v))
                values.append(v)
            row.append(_pp(hist[i]))
            values.append(hist[i])
            rows.append(row)
        return md_table(heads, rows, col_fmt=['center'] * len(heads))

    net = block(net_by_g, hist_net)
    tw = block(tw_by_g, hist_tw)
    cap = (f"Table 7.1b.G: Cost of declaring α of true value, in percentage points of honest terminal wealth "
           f"TW(1) (+ = worse for the declarer), at the plotted grid point nearest each requested α. "
           f"Top: net tax paid relative to honest. Bottom: terminal wealth lost relative to honest. "
           f"Constant-growth scenarios and the {yr} historical series (mean g = {cd['mean_g_hist'] * 100:.1f}%). "
           f"N = {p['N_val']}, V_0 = £{p['V0_m']:g}m, k = {p['k']}, τ_0 = {fmt_pct(p['tau_0'], 0)}.")
    return {'md': net + '\n\n' + tw + '\n\n' + cap, 'values': values}


# ── Fig 7.1c ─────────────────────────────────────────────────────────────────

def build_F7_1c(data: dict, p: dict) -> dict:
    cd = get_key(data, PAIRS['F7_1c']['json'])
    gs, ns = cd['g_surf'], cd['n_surf']
    ni = _nearest(ns, p['N_val'])
    if ns[ni] != p['N_val']:
        raise ValueError(f"N_val = {p['N_val']} is not on the plotted N grid {ns[0]}..{ns[-1]}")
    gi = [_nearest(gs, g) for g in p['surface_table_g']]
    alphas = sorted(cd['surfaces'], key=float)
    values = []

    def block(key):
        heads = ['α'] + [f'g = {gs[i] * 100:.2f}%' for i in gi]
        rows = []
        for a in alphas:
            m = cd[key][a]                      # [g x N]
            row = [f'**{float(a):g}**']
            for i in gi:
                v = m[i][ni]
                row.append(_pp(v))
                values.append(v)
            rows.append(row)
        return md_table(heads, rows, col_fmt=['center'] * len(heads))

    tw = block('surfaces')
    net = block('surfaces_net')
    cap = (f"Table 7.1c.G: Overstatement at the canonical holding period N = {p['N_val']}, in percentage "
           f"points of honest TW(1), at the plotted growth rate nearest each requested g. "
           f"Top: terminal-wealth advantage TW(α) − TW(1) (+ = declarer retains more). "
           f"Bottom: net tax difference (Net(α) − Net(1)) / TW(1) (+ = pays more). "
           f"V_0 = £{p['V0_m']:g}m, k = {p['k']}. Historical mean g = {p['g'] * 100:.2f}%.")
    return {'md': tw + '\n\n' + net + '\n\n' + cap, 'values': values}


# ── Fig 7.2b / 7.2c ──────────────────────────────────────────────────────────

def _under_stats(g_pct: list, curve: list, slope_tol: float, cutoff_pct: float) -> dict:
    """Inflection, plateau onset and peak of a net-cost curve (same derivation as 5_4 Fig 7.2b,
    with the search window and slope tolerance taken from TOML instead of literals)."""
    deriv = [curve[i + 1] - curve[i] for i in range(len(curve) - 1)]
    peak_idx = max(range(len(deriv)), key=lambda i: deriv[i])
    end = max(i for i, g in enumerate(g_pct) if g <= cutoff_pct)
    onset = next((g_pct[i] for i in range(peak_idx, min(len(deriv), end)) if deriv[i] < slope_tol), None)
    return {'inflection': g_pct[peak_idx], 'onset': onset, 'peak': max(curve)}


def build_F7_2b(data: dict, p: dict) -> dict:
    cd = get_key(data, PAIRS['F7_2b']['json'])
    _check_stamp(cd, p, 'Fig 7.2b')
    g = cd['g_pct']
    alphas = data['grids']['alpha_under']
    net = {float(k): v for k, v in cd['c1_curves'].items()}
    tw = {float(k): v for k, v in cd['tw_cost_curves'].items()}
    hi = _nearest(g, p['g'] * 100)
    rows, values = [], []
    stats = {}
    for a in alphas:
        s = _under_stats(g, net[a], p['reversal_plateau_slope'], p['reversal_g_cutoff_pct'])
        stats[a] = s
        row = [f'**{a:g}**', f"{s['inflection']:.1f}%",
               f"{s['onset']:.1f}%" if s['onset'] is not None else 'none in range',
               _pp(s['peak']), _pp(net[a][hi]), _pp(tw[a][hi])]
        rows.append(row)
        values += [s['inflection'], s['peak'], net[a][hi], tw[a][hi]]
        if s['onset'] is not None:
            values.append(s['onset'])
    mean_inf = sum(s['inflection'] for s in stats.values()) / len(stats)
    cap = (f"Table 7.2b.G: Structure of the understater net-tax penalty by growth rate. Inflection = growth "
           f"rate of the steepest rise of the net curve; plateau onset = first growth rate after it at which the "
           f"curve rises by less than {p['reversal_plateau_slope']:g} pp per grid step, searched up to "
           f"g = {p['reversal_g_cutoff_pct']:g}%; peak = maximum of the net curve. The last two columns are the "
           f"net penalty and the terminal-wealth cost at the historical mean g = {g[hi]:.2f}%. All in "
           f"percentage points of honest TW(1), + = worse for the declarer. Mean inflection "
           f"{mean_inf:.1f}%. N = {p['N_val']}, V_0 = £{p['V0_m']:g}m, k = {p['k']}.")
    heads = ['α', 'Inflection g', 'Plateau onset g', 'Peak net penalty (pp)',
             'Net penalty at hist. g (pp)', 'TW cost at hist. g (pp)']
    return {'md': md_table(heads, rows, col_fmt=['center'] * len(heads)) + '\n\n' + cap, 'values': values}


def build_F7_2c(data: dict, p: dict) -> dict:
    cd = get_key(data, PAIRS['F7_2c']['json'])
    _check_stamp(cd, p, 'Fig 7.2c')
    g = cd['g_pct']
    alphas = data['grids']['alpha_over']
    net = {float(k): v for k, v in cd['c1_curves'].items()}
    tw = {float(k): v for k, v in cd['tw_cost_curves'].items()}
    hi = _nearest(g, p['g'] * 100)
    rows, values = [], []
    for a in alphas:
        c = net[a]
        first = next((x for x, v in zip(g, c) if v > 0), None)
        pk = max(range(len(c)), key=lambda i: c[i])
        rows.append([f'**{a:g}**', f'{first:.1f}%' if first is not None else 'never',
                     _pp(c[pk]), f'{g[pk]:.1f}%', _pp(c[hi]), _pp(tw[a][hi])])
        values += [c[pk], c[hi], tw[a][hi]] + ([first] if first is not None else [])
    cap = (f"Table 7.2c.G: Overstater net-tax reversal by growth rate. First reversal = lowest plotted growth "
           f"rate at which the net tax difference turns positive (the overstater pays more than honest); "
           f"'never' = the curve stays at or below zero over the plotted range. Peak = maximum of the net "
           f"curve and the g at which it occurs. Last two columns at the historical mean g = {g[hi]:.2f}%. "
           f"Percentage points of honest TW(1). N = {p['N_val']}, V_0 = £{p['V0_m']:g}m, k = {p['k']}, "
           f"τ_0 = {fmt_pct(p['tau_0'], 0)}.")
    heads = ['α', 'First reversal g', 'Peak net difference (pp)', 'g at peak',
             'Net difference at hist. g (pp)', 'TW cost at hist. g (pp)']
    return {'md': md_table(heads, rows, col_fmt=['center'] * len(heads)) + '\n\n' + cap, 'values': values}


BUILDERS = {'F5': build_F5, 'F7_1b': build_F7_1b, 'F7_1c': build_F7_1c, 'F7_2b': build_F7_2b, 'F7_2c': build_F7_2c}


def main(only=None, data_path=_DATA, out=_OUT) -> None:
    p = load_params()
    data = load_data(data_path)
    ensure_dir(out)
    combined = MdDoc()
    for pid, spec in PAIRS.items():
        if only and pid not in only:
            continue
        res = BUILDERS[pid](data, p)
        doc = MdDoc()
        doc.add_block(res['md'])
        doc.write(out / f"val_table_gap_{pid}_{spec['slug']}.md")
        if len(combined):
            combined.blank().rule().blank()
        combined.h2(f"{spec['title']} ({pid})").blank().add_block(res['md'])
        print(f'  wrote {pid}')
    if len(combined):
        combined.write(out / 'val_table_gap_all.md', verbose=False)
        print('  wrote combined val_table_gap_all.md')


if __name__ == '__main__':
    main(only=sys.argv[1:] or None)
