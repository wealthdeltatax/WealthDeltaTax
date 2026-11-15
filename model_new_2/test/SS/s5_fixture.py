"""
s5_fixture.py -- a SYNTHETIC valgen_data.json for testing the S5 tables and figures (lives in Model/test/).

The numbers are random and mean nothing. Only the SHAPE is real: every key and nesting is the one valgen_core.main writes
(replay, p6, rho, p3_lambda_grid, v0_sweep, p5.hlc_pair, p5.search.best_by_cycle ...). Never quote a result from it.

    make_data(p)   -> dict (JSON round-tripped, so keys are strings exactly as after json.load)
"""
import json
import random

RULES = ['units/allow/off', 'units/allow/on', 'units/reset/off', 'units/reset/on',
         'units_and_value/allow/off', 'units_and_value/allow/on', 'units_and_value/reset/off', 'units_and_value/reset/on']
HEAD = ['units/allow/off', 'units_and_value/reset/on']
LAMS = [0.0, 0.01, 0.02, 0.05, 0.10]
ALPHAS = [0.0, 0.01, 0.1, 0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 3.0, 5.0, 10.0]
SWEEP_A = [0.1, 0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0]
BANDS = [0.25, 0.5, 1.0, 2.5, 5.0, 25.0, 100.0, 1000.0]
RHOS = [0.0, 0.025, 0.035, 0.05]
ARCH = {'housing_pension': ('Housing and pension', 0.4), 'startup_founder': ('Start-up founder', 8.0),
        'generational': ('Generational wealth', 50.0), 'ceo_fintech': ('CEO / fintech', 30.0),
        'resource_monopoly': ('Resource monopoly', 500.0)}


def make_data(p: dict | None = None) -> dict:
    R = random.Random(7)
    T = (p or {}).get('val_gen', {}).get('T', 100)
    G = (p or {}).get('val_gen', {}).get('G', 30)
    lam_b = (p or {}).get('val_gen', {}).get('lambda_base', 0.05)
    lams = sorted(set(LAMS + [lam_b]))
    cyc = ['0', '5', '10', '20']

    def best(lam, scale=1.0):
        return {'gain': scale * R.uniform(0.0, 0.04) * (1 - lam * 4), 'label': f'constant C={R.choice([0.1, 0.5])} D=1.0'}

    search = {}
    for rule in RULES:
        for lam in lams:
            g = R.uniform(0.0, 0.05)
            search[f'{rule}|{lam}'] = {
                'best': {'gain': g, 'label': 'constant C=0.5 D=1.0'}, 'BRG_pass': g <= 0.01,
                'n_conflict_sst': R.randint(0, 4), 'SST_pass': R.random() > 0.4, 'worst_state': None,
                'best_by_cycle': {c: best(lam) for c in cyc},
                'best_by_family': {f: {'gain': R.uniform(0, 0.03), 'label': f} for f in ('constant', 'first_gen_only')}}
    spt = {k: {str(r): {'n_conflict': R.randint(0, 3), 'pass': R.random() > 0.5} for r in RHOS} for k in search}

    def replay_cells(starts):
        return {f'{rule}|{lam}': {'gain': R.uniform(-0.01, 0.06), 'label': 'x', 'BRG': R.random() > 0.3, 'SST': R.random() > 0.3,
                                  'SPT': True, 'n_conflict': 0} for rule in HEAD for lam in (0.0, lam_b)}

    rows = []
    for i, s in enumerate(range(1870, 2010, 20)):
        rows.append({'start': s, 'wraps': i > 4, 'repeat': i > 4, 'contiguous': i <= 4, 'g_geo': 0.04, 'cells': replay_cells(s)})
    summ = {}
    for k in rows[0]['cells']:
        def st(keep):
            cs = [r['cells'][k] for r in rows if keep(r)]
            if not cs:
                return None
            gs = sorted(c['gain'] for c in cs)
            return {'windows': len(cs), 'BRG_pass_share': sum(c['BRG'] for c in cs) / len(cs),
                    'SST_pass_share': sum(c['SST'] for c in cs) / len(cs), 'gain_max': gs[-1], 'gain_median': gs[len(gs) // 2], 'gain_min': gs[0]}
        summ[k] = {'full_loop': st(lambda r: True), 'contiguous': st(lambda r: r['contiguous'])}
    replay = {'T': T, 'stride': 20, 'rules': HEAD, 'lambda_vals': [0.0, lam_b], 'note': 'synthetic',
              'countries': {'GBR': {'usable_years': 68, 'windows': len(rows), 'repeat_windows': 3, 'rows': rows, 'summary': summ}}}

    arch = {}
    for name, (lab, v0) in ARCH.items():
        modes = {}
        for mode in ('sale', 'lien', 'income'):
            modes[mode] = {'TW': v0 * R.uniform(5, 40), 'PV': v0 * R.uniform(1, 9), 'state_true_T': v0, 'unpaid_B': 0.0,
                           'income_paid': 0.0 if mode != 'income' else v0 * R.uniform(0.1, 2),
                           'best': {str(l): {'gain': R.uniform(0, 0.03), 'label': 'route_shift BD a=0.5', 'BRG': R.random() > 0.3,
                                             'SPT': True, 'SST': True} for l in (0.0, lam_b)}}
        arch[name] = {'label': lab, 'V0_m': v0, 'shares': {'A': 0.4, 'B': 0.2, 'C': 0.2, 'D': 0.2}, 'income_ratio': 0.02,
                      'modes': modes, 'breakeven_spread': None if name == 'resource_monopoly' else R.uniform(-0.01, 0.08)}

    cells = {f'{a}|{b}': {'gain': R.uniform(0, 0.05), 'label': 'constant C=0.5 D=0.5', 'BRG': R.random() > 0.5, 'SST': True, 'SPT': True,
                          'n_conflict': 0} for a in (0.0, 0.02, 0.05, 0.1) for b in (0.0, 0.02, 0.05, 0.1)}
    lgrid = {'lambda_C': [0.0, 0.02, 0.05, 0.1], 'lambda_D': [0.0, 0.02, 0.05, 0.1], 'rule': HEAD[-1], 'cells': cells, 'note': 'synthetic'}
    v0cells = {}
    for b in BANDS:
        for rule in HEAD:
            for lam in (0.0, lam_b):
                v0cells[f'{b}|{rule}|{lam}'] = {'gain': R.uniform(0, 0.05), 'label': 'x', 'BRG': R.random() > 0.5, 'SST': True, 'SPT': True,
                                                'n_conflict': 0, 'honest_TW': b * 10, 'drag': R.uniform(0.05, 0.4)}
    v0 = {'bands': BANDS, 'rules': HEAD, 'lambda_vals': [0.0, lam_b], 'cells': v0cells,
          'note': 'V0 = RATES revenue band (£m); route shares at the baseline mix; drag = 1 - honest terminal wealth / no-tax terminal wealth'}

    by_rule = {rule: {str(lam): {str(a): ({'gain': None, 'label': 'undefined'} if a <= 0 else
                                          {'gain': R.uniform(0, 0.4) * min(1.0, a) if a < 1 else (0.0 if a == 1.0 else R.uniform(-0.01, 0.01)),
                                           'label': 'x'}) for a in ALPHAS} for lam in (0.0, lam_b)} for rule in HEAD}
    conv = lambda rate: {'rate': rate, 'target_tw': None, 'honest_TW': 1.0, 'cells': {}, 'best': {'key': '0.0|0.0', 'gain': 1.0},
                         'full_understatement_gain': 1.0, 'diag_alpha': {str(a): R.uniform(0, 3) * (1 - min(a, 1)) for a in ALPHAS}}
    hlc_pair = {'skipped': False, 'source': {'scenario': 'gain_ladder', 'by_band': [0.01], 'wealth_share': [1.0]},
                'burdens': {'average': conv(0.0035), 'top': conv(0.0112)}}

    sens = {c: {str(a): {'gain': R.uniform(-0.05, 0.2)} for a in SWEEP_A} for c in cyc}
    data = {
        'meta': {'N_val': 30, 'params': {'T': T, 'G': G}},
        'replay': replay, 'p6': {'archetypes': arch, 'checks': {}, 'info': {}},
        'rho': {'base': 0.035, 'sweep': RHOS, 'note': 'synthetic', 'spt_by_rho': spt, 'verdict_spt_by_rho': {}},
        'p3_lambda_grid': lgrid, 'v0_sweep': v0, 'p3_reset_sensitivity': sens,
        'p5': {'thresholds': {'brg_tol': 0.01, 'hsc_tol': 0.01, 'state_tol': 0.02}, 'rules': RULES, 'lambda_vals': lams,
               'n_strategies': 600, 'search': search, 'hlc_pair': hlc_pair,
               'headline': {'alphas': ALPHAS, 'rules': HEAD, 'lambda_vals': [0.0, lam_b], 'by_rule': by_rule}},
    }
    return json.loads(json.dumps(data))
