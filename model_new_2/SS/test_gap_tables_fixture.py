"""Plumbing test for 5_8_VAL_gap_tables.py on a SYNTHETIC fixture (val_core / val_data.json are not
available in this workspace). Checks shapes, keys, units, and that every printed value is in the JSON.
It does NOT check that the real val_data.json produces sensible numbers."""
import importlib.util, json, math, sys, tempfile, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import numpy as np
from wdt_core import load_params, tau

spec = importlib.util.spec_from_file_location('gap', str(pathlib.Path(__file__).resolve().parent / '5_8_VAL_gap_tables.py'))
gap = importlib.util.module_from_spec(spec); spec.loader.exec_module(gap)
p = load_params()
N = p['N_val']

def flat(x, acc):
    if isinstance(x, dict):
        for v in x.values(): flat(v, acc)
    elif isinstance(x, list):
        for v in x: flat(v, acc)
    elif isinstance(x, (int, float)): acc.add(round(float(x), 9))
    return acc

def fixture():
    ws = list(np.geomspace(p['W_min'], 10000, 120))
    af = [round(0.5 + 0.01 * i, 2) for i in range(151)]
    gsc = [0.059, 0.084, 0.1045, 0.139]
    cost = lambda g, a: 100 * (g * (a - 1) ** 2 - 0.2 * (a - 1))
    gp = [round(0.1 * i, 1) for i in range(0, 501)]
    under, over = [0.1, 0.25, 0.5], [1.2, 1.5, 2.0]
    sat = lambda a, g: 40 * (1 - a) * (1 - math.exp(-g / 12))
    ovr = lambda a, g: (a - 1) * (g - 15) * 0.8
    gs = [round(0.01 * i, 4) for i in range(0, 41)] + [0.1045]
    gs = sorted(set(gs)); ns = list(range(5, 61))
    return {
      'meta': {'scenario_start_year': 1990},
      'params': {}, 'grids': {'alpha_under': under, 'alpha_over': over},
      'charts': {
        'fig_5_rate_function': {'w_vals': ws, 'tau_vals': [tau(w, p) for w in ws]},
        'fig_7_1b_equilibrium_cost_curve': {
            'N': N, 'alpha_fine': af, 'g_scenarios': gsc,
            'net_pct_by_g': {str(g): [cost(g, a) for a in af] for g in gsc},
            'tw_cost_by_g': {str(g): [cost(g, a) * 0.8 for a in af] for g in gsc},
            'hist_net_pct': [cost(0.09, a) for a in af], 'hist_tw_cost': [cost(0.09, a) * .8 for a in af],
            'mean_g_hist': 0.09},
        'fig_7_1c_tw_advantage_gN_surface': {
            'g_surf': gs, 'n_surf': ns,
            'surfaces': {str(a): [[(a - 1) * g * n for n in ns] for g in gs] for a in (1.2, 1.5, 1.8, 2.0)},
            'surfaces_net': {str(a): [[(a - 1) * (g - .1) * n for n in ns] for g in gs] for a in (1.2, 1.5, 1.8, 2.0)}},
        'fig_7_2b_saturation_reversal': {
            'N': N, 'g_pct': gp,
            'c1_curves': {str(a): [sat(a, g) for g in gp] for a in under},
            'tw_cost_curves': {str(a): [sat(a, g) * 0.9 - 0.1 * g for g in gp] for a in under}},
        'fig_7_2c_overstatement_reversal': {
            'N': N, 'g_pct': gp,
            'c1_curves': {str(a): [ovr(a, g) for g in gp] for a in over},
            'tw_cost_curves': {str(a): [ovr(a, g) * 0.7 for g in gp] for a in over}},
      }}

def test_all():
    d = pathlib.Path(tempfile.mkdtemp())
    (d / 'fx.json').write_text(json.dumps(fixture()))
    gap.main(data_path=d / 'fx.json', out=d / 'tables')
    data = json.loads((d / 'fx.json').read_text())
    for pid, spec_ in gap.PAIRS.items():
        f = d / 'tables' / f"val_table_gap_{pid}_{spec_['slug']}.md"
        assert f.exists() and 'Table' in f.read_text(), pid
        res = gap.BUILDERS[pid](data, p)
        pool = flat(get_ := gap.get_key(data, spec_['json']), set())
        pool |= flat(data['grids'], set())
        # derived stats (inflection, onset, first reversal, peaks) are g or curve values already in the JSON
        miss = [v for v in res['values'] if round(float(v), 9) not in pool]
        assert not miss, (pid, miss[:5])
        print('PASS', pid, len(res['values']), 'values')
    print((d / 'tables' / 'val_table_gap_F7_2b_saturation_reversal.md').read_text())
    print((d / 'tables' / 'val_table_gap_F5_rate_function.md').read_text())

if __name__ == '__main__':
    test_all()
