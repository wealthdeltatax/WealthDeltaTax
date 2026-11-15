"""
5_7_VALGEN_charts.py — VALGEN figures (presentation layer)
==========================================================
One figure per table in 5_6_VALGEN_tables.py. Both read the same JSON keys (PAIRS).
Plan: VAL_tables_figures_plan.md (section 4). Reads OUTPUTS/VAL/valgen_data.json.

Layer rules: never simulates, never imports a core or the tables script. Uses wdt_core
(load_params only), wdt_fmt, wdt_style. JSON stores raw fractions; formatting happens here.
apply_style() first in every figure function; colours and sizes from wdt_style only.

Contract for every builder  build_<ID>(data, p) -> dict
    'path'    saved PNG (300 dpi via save_fig)
    'series'  dict name -> list of the raw numbers drawn (pairing test checks the paired
              table's values appear here)
Output: OUTPUTS/VAL/charts/val_fig_<ID>_<slug>.png
"""

from __future__ import annotations

import json
import sys

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # model root: wdt_core, wdt_fmt, wdt_md, wdt_style

from wdt_core import load_params
from wdt_fmt import out_dir, ensure_dir
from wdt_style import (apply_style, save_fig, FIG_PAIR, FIG_PAIR_XW, FIG_SINGLE_W, C_CONV, C_WDT,  # noqa: F401
                       C_WDT_BASE, C_CEILING, C_ANNOTATION, C_GRID, C_DARK, C_UNDER, C_PASS, C_FAIL,
                       RULE_COLOURS, CMAP_GAIN)

_DATA = out_dir('VAL') / 'valgen_data.json'
_OUT = out_dir('VAL') / 'charts'

# id -> JSON keys (dotted paths into valgen_data.json), slug, title. The tables script declares
# the same ids and keys; test_valgen_pairs.py asserts they agree.
PAIRS = {
    'UCC': {'json': ['p2b_round_trip_units', 'p2b_oscillation', 'p2_benchmark_plan_s1'], 'slug': 'units_conserved', 'title': 'Units are conserved',
          'label': 'Figure UCC'},
    'WLG': {'json': ['bridge', 'examples'], 'slug': 'worked_ledger', 'title': 'Worked example ledger',
          'label': 'Figure WLG'},
    'CDS': {'json': ['p3_surface'], 'slug': 'alpha_surface', 'title': 'alpha_C x alpha_D surface',
          'label': 'Figure CDS'},
    'RIS': {'json': ['p3_reset_sensitivity'], 'slug': 'reset_sensitivity', 'title': 'Route D reset sensitivity',
          'label': 'Figure RIS'},
    'DSH': {'json': ['p3_dilution', 'p4_C_share_sensitivity', 'p4_C_heavy_stress_gain'], 'slug': 'dilution_share', 'title': 'Dilution and Route C share',
          'label': 'Figure DSH'},
    'VSY': {'json': ['p4_lambda_sweep'], 'slug': 'verified_share', 'title': 'Corrective auction: verified share by year',
          'label': 'Figure VSY'},
    'ABL': {'json': ['p5.search', 'p5.rules'], 'slug': 'ablation_by_lambda', 'title': 'Best response vs lambda by rule set',
          'label': 'Figure ABL'},
    'VMP': {'json': ['p5.verdict_by_rule', 'p5.thresholds'], 'slug': 'verdict_map', 'title': 'Verdict map BRG/HSC/SPT/SST',
          'label': 'Figure VMP'},
    'FBR': {'json': ['p5.search'], 'slug': 'family_best', 'title': 'Best response by strategy family',
          'label': 'Figure FBR'},
    'PSS': {'json': ['p5.search'], 'slug': 'spt_sst_scatter', 'title': 'SPT/SST scatter over the strategy library',
          'label': 'Figure PSS'},
    'GLM': {'json': ['p5.growth_surface'], 'slug': 'growth_lambda', 'title': 'Growth x lambda surface',
          'label': 'Figure GLM'},
    'HLC': {'json': ['p5.headline', 'p5.conventional_baseline', 'p5.no_tax_ceiling'], 'slug': 'headline_contrast', 'title': 'Headline contrast: conventional vs WDT',
          'label': 'Figure HLC'},
    'HCS': {'json': ['p5.g2_honest_shock_cost'], 'slug': 'shock_cost', 'title': 'Honest-family cost in a market shock',
          'label': 'Figure HCS'},
    'DOMG': {'json': ['p5.dmg', 'p5.thresholds'], 'slug': 'dominance_grid', 'title': 'Dominance grid: strategies that gain in every scenario',
          'label': 'Figure DOMG'},
    'HERR': {'json': ['p5.hec', 'p5.thresholds'], 'slug': 'honest_error', 'title': 'Honest valuation error: gain and cost',
          'label': 'Figure HERR'},
    'UOS': {'json': ['p5.uos', 'p5.thresholds'], 'slug': 'under_over_share', 'title': 'Understatement against overstatement by Route C share',
          'label': 'Figure UOS'},
    'LGR': {'json': ['life'], 'slug': 'life_gain_grid', 'title': 'Single-life gain by declaration ratio and growth',
          'label': 'Figure LGR'},
    'LNS': {'json': ['life'], 'slug': 'life_n_sweep', 'title': 'Single-life gain by declaration ratio and holding period',
          'label': 'Figure LNS'},
}


def load_data(path=_DATA) -> dict:
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def get_key(data: dict, dotted: str):
    """Resolve 'p5.search' style paths."""
    cur = data
    for part in dotted.split('.'):
        cur = cur[part]
    return cur


def _check_stamp(data: dict, p: dict) -> None:
    """The JSON must come from the same parameters as the TOML in use."""
    m, vg = data['meta'], p['val_gen']
    got = (m['N_val'], m['params']['T'], m['params']['G'])
    want = (p['N_val'], vg['T'], vg['G'])
    if got != want:
        raise ValueError(f'valgen_data.json stamp (N_val, T, G) = {got} != TOML {want}; re-run valgen_core.py')


def _stub(pid):
    def build(data, p):
        raise NotImplementedError(f'Figure {pid} not built')
    build.__name__ = f'build_{pid}'
    return build


BUILDERS = {pid: _stub(pid) for pid in PAIRS}


# ── HLC headline contrast ────────────────────────────────────────────────────

def build_HLC(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    apply_style()
    hl = get_key(data, 'p5.headline')
    conv = get_key(data, 'p5.conventional_baseline')
    th = get_key(data, 'p5.thresholds')
    ceil_all = get_key(data, 'p5.no_tax_ceiling')['gain_ceiling_by_rule_lambda']
    rules = hl['rules']
    base, cand = rules[0], rules[-1]
    lam_base = p['val_gen']['lambda_base']
    alphas = [a for a in sorted(hl['alphas']) if a <= 1.0]
    ceiling = ceil_all[f'{cand}|{lam_base}']

    def wdt(rule, lam):
        return [(hl['by_rule'][rule][str(lam)][str(a)]['gain']) for a in alphas]

    ser = {'alpha': alphas,
           'conventional': [conv['diag_alpha'][str(a)] for a in alphas],
           'wdt_base_lam0': wdt(base, 0.0), 'wdt_base_lam_base': wdt(base, lam_base),
           'wdt_cand_lam0': wdt(cand, 0.0), 'wdt_cand_lam_base': wdt(cand, lam_base),
           'ceiling': [ceiling]}

    def arr(v):
        return np.array([np.nan if x is None else x for x in v], dtype=float)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=FIG_PAIR)
    for ax in (a1, a2):
        ax.set_xlim(1.0, 0.0)                      # understatement increases to the right
        ax.set_xlabel('Declaration ratio α (declared / true value)')
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    a1.plot(alphas, ser['conventional'], color=C_CONV, marker='o', label='Conventional self-declared tax')
    a1.plot(alphas, arr(ser['wdt_base_lam0']), color=C_WDT_BASE, marker='o',
            label=f'WDT {base}, λ = {0.0:.0%}')
    a1.plot(alphas, arr(ser['wdt_cand_lam0']), color=C_WDT, marker='o',
            label=f'WDT {cand}, λ = {0.0:.0%}')
    a1.axhline(ceiling, color=C_CEILING, ls='--', lw=1.2)
    a1.text(0.99, ceiling, 'No-tax ceiling: leak check, not a result', color=C_CEILING,
            va='bottom', ha='left', fontsize=9)
    a1.set_ylabel("Gain over honest family (share of its terminal wealth)")
    a1.set_title('Full scale, no verification (worst case)')
    a1.legend(loc='center left', fontsize=9)
    for rule, lam, col, mk, ls in ((cand, 0.0, C_WDT, 'o', '-'), (cand, lam_base, C_WDT, 's', '--'),
                                   (base, lam_base, C_WDT_BASE, 's', '--')):
        a2.plot(alphas, arr(wdt(rule, lam)), color=col, ls=ls, marker=mk, ms=4,
                label=f'{rule}, λ = {lam:.0%}')
    a2.axhline(th['brg_tol'], color=C_ANNOTATION, ls=':', lw=1.2)
    a2.text(0.99, th['brg_tol'], 'BRG threshold', color=C_ANNOTATION, va='bottom', ha='left', fontsize=9)
    a2.set_title('Zoom: the candidate rule set and the base rule set with verification')
    a2.legend(loc='upper left', fontsize=8)
    fig.text(0.5, 0.005, 'Strategy search is a lower bound. α = 0 is undefined for the WDT (zero declared price). '
             'Conventional tax: no audits modelled.', ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_HLC_{PAIRS['HLC']['slug']}.png")
    return {'path': path, 'series': ser}


BUILDERS['HLC'] = build_HLC


def _chain(p: dict, data: dict) -> list:
    """Ablation chain: start from the first value of each rule list, then adopt each component's
    last value in turn (cap, verify-down, auction). Rule keys are checked against p5.rules."""
    vg = p['val_gen']
    c, v, d = vg['c_cap_rules'], vg['verify_down_rules'], vg['d_auction_rules']
    steps = [(c[0], v[0], d[0]), (c[-1], v[0], d[0]), (c[-1], v[-1], d[0]), (c[-1], v[-1], d[-1])]
    keys = []
    for s in steps:
        k = '/'.join(s)
        if k not in keys:
            keys.append(k)
    missing = [k for k in keys if k not in get_key(data, 'p5.rules')]
    if missing:
        raise KeyError(f'rule sets {missing} not in p5.rules')
    return keys


def _arr(v):
    import numpy as np
    return np.array([np.nan if x is None else x for x in v], dtype=float)


def _pct_cbar(cb, dec=1):
    from matplotlib.ticker import PercentFormatter
    cb.ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=dec))


def _pct_axis(ax, axis='y', dec=0):
    from matplotlib.ticker import PercentFormatter
    (ax.yaxis if axis == 'y' else ax.xaxis).set_major_formatter(PercentFormatter(1.0, decimals=dec))


# ── ABL ablation by lambda ────────────────────────────────────────────────────

def build_ABL(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    srch = get_key(data, 'p5.search')
    lams = get_key(data, 'p5.lambda_vals')
    th = get_key(data, 'p5.thresholds')
    chain = _chain(p, data)
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ser = {'lambda': lams}
    for r, col in zip(chain, RULE_COLOURS):
        y = [srch[f'{r}|{l}']['best']['gain'] for l in lams]
        ser[r] = y
        ax.plot(lams, y, marker='o', color=col, label=r)
    ax.axhline(th['brg_tol'], color=C_ANNOTATION, ls=':', lw=1.2)
    ax.text(lams[0], th['brg_tol'], 'BRG threshold ', color=C_ANNOTATION, va='bottom', ha='right', fontsize=9)
    ax.set_xticks(lams)
    _pct_axis(ax, 'x')
    _pct_axis(ax, 'y')
    ax.set_xlabel('Verification hazard λ (yearly odds an asset is verified)')
    ax.set_ylabel('Best-response gain over honest family')
    ax.legend(title='Rule set (cap / verify-down / auction)', fontsize=9)
    fig.text(0.5, 0.005, 'Best of the strategy library: a lower bound.', ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_ABL_{PAIRS['ABL']['slug']}.png")
    return {'path': path, 'series': ser}


# ── FBR best response by strategy family ──────────────────────────────────────

def build_FBR(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    srch = get_key(data, 'p5.search')
    lams = get_key(data, 'p5.lambda_vals')
    rule = _chain(p, data)[-1]
    lam_b = p['val_gen']['lambda_base']
    show = [lams[0], lam_b, lams[-1]]
    fams = list(srch[f'{rule}|{lam_b}']['best_by_family'])
    ys = {l: [srch[f'{rule}|{l}']['best_by_family'][f]['gain'] for f in fams] for l in show}
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    x = np.arange(len(fams))
    ax.bar(x, ys[lam_b], color=C_WDT, label=f'λ = {lam_b:.0%}')
    ax.scatter(x, ys[show[0]], marker='v', color=C_CONV, zorder=3, label=f'λ = {show[0]:.0%}')
    ax.scatter(x, ys[show[-1]], marker='^', color=C_ANNOTATION, zorder=3, label=f'λ = {show[-1]:.0%}')
    ax.set_xticks(x)
    ax.set_xticklabels([f.replace('_', '\n') for f in fams], fontsize=9)
    _pct_axis(ax)
    ax.set_ylabel('Best-response gain over honest family')
    ax.legend(fontsize=9)
    path = save_fig(fig, _OUT / f"val_fig_FBR_{PAIRS['FBR']['slug']}.png")
    return {'path': path, 'series': {f'lam_{l}': ys[l] for l in show}}


# ── GLM growth x lambda surface ──────────────────────────────────────────────

def build_GLM(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style(grid=False)
    gs = get_key(data, 'p5.growth_surface')
    rule = list(gs['by_rule'])[0]
    lams = get_key(data, 'p5.lambda_vals')
    gv = gs['growth_vals']
    Z = np.array([[gs['by_rule'][rule][str(g)]['by_lambda'][str(l)]['gain'] for l in lams] for g in gv])
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    im = ax.imshow(Z, cmap=CMAP_GAIN, aspect='auto', origin='lower', vmin=0.0)
    for i, g in enumerate(gv):
        for j, l in enumerate(lams):
            c = gs['by_rule'][rule][str(g)]['by_lambda'][str(l)]
            flag = ('' if c['BRG'] else ' BRG✗') + ('' if c['SPT'] else ' SPT✗') + ('' if c['SST'] else ' SST✗')
            ax.text(j, i, f"{c['gain']:.1%}{flag}", ha='center', va='center', fontsize=9,
                    color='white' if c['gain'] > 0.6 * Z.max() else C_DARK)
    ax.set_xticks(range(len(lams)))
    ax.set_xticklabels([f'{l:.0%}' for l in lams])
    ax.set_yticks(range(len(gv)))
    ax.set_yticklabels([f'{g:.2%}' for g in gv])
    ax.set_xlabel('Verification hazard λ')
    ax.set_ylabel('Asset growth g')
    _pct_cbar(fig.colorbar(im, ax=ax, label='Best-response gain'))
    path = save_fig(fig, _OUT / f"val_fig_GLM_{PAIRS['GLM']['slug']}.png")
    return {'path': path, 'series': {'gain': Z.flatten().tolist()}}


# ── HCS shock cost ───────────────────────────────────────────────────────────

def build_HCS(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    cost = get_key(data, 'p5.g2_honest_shock_cost')
    th = get_key(data, 'p5.thresholds')
    rules = list(cost)
    shocks = list(cost[rules[0]])
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    y = np.arange(len(rules))
    h = 0.3
    ser = {}
    for k, s in enumerate(shocks):
        vals = [cost[r][s] for r in rules]
        ser[f'shock_{s}'] = vals
        off = (k - (len(shocks) - 1) / 2) * h
        ax.scatter(vals, y + off, s=60, color=[C_UNDER[1], C_WDT][k % 2], zorder=3,
                   label=f'Fall of {abs(float(s)):.0%}')
        for v, yy in zip(vals, y + off):
            ax.annotate(f'{v:+.3%}', (v, yy), xytext=(9, 0), textcoords='offset points', ha='left',
                        va='center', fontsize=7, color=C_DARK)
    ax.axvline(-th['hsc_tol'], color=C_ANNOTATION, ls=':')
    ax.axvline(th['hsc_tol'], color=C_ANNOTATION, ls=':')
    ax.set_yticks(y)
    ax.set_yticklabels(rules, fontsize=9)
    ax.invert_yaxis()
    _pct_axis(ax, 'x', 1)
    ax.set_xlim(-2 * th['hsc_tol'], 2 * th['hsc_tol'])
    ax.set_xlabel('Change in honest family terminal wealth vs base rule set')
    ax.legend(fontsize=9)
    fig.text(0.5, 0.005, 'Dotted lines: HSC tolerance (placeholder).', ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_HCS_{PAIRS['HCS']['slug']}.png")
    return {'path': path, 'series': ser}


# ── VMP verdict map ───────────────────────────────────────────────────────────

def build_VMP(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    apply_style(grid=False)
    srch = get_key(data, 'p5.search')
    lams = get_key(data, 'p5.lambda_vals')
    th = get_key(data, 'p5.thresholds')
    vb = get_key(data, 'p5.verdict_by_rule')
    rules = get_key(data, 'p5.rules')
    g1v = np.array([[srch[f'{r}|{l}']['best']['gain'] for l in lams] for r in rules])
    g1ok = np.array([[srch[f'{r}|{l}']['BRG_pass'] for l in lams] for r in rules])
    g2v = np.array([[max(vb[r]['HSC_cost'].values(), key=abs)] for r in rules])
    g2ok = np.array([[vb[r]['HSC']] for r in rules])
    ws = [[srch[f'{r}|{l}']['worst_state'] for l in lams] for r in rules]
    g3v = np.array([[np.nan if w is None else w['value'] for w in row] for row in ws])
    g3ok = np.array([[True if w is None else abs(w['value']) <= th['state_tol'] for w in row] for row in ws])
    fig, axs = plt.subplots(1, 3, figsize=FIG_PAIR_XW, gridspec_kw={'width_ratios': [len(lams), 1, len(lams)]})
    cmap = ListedColormap([C_FAIL, C_PASS])
    panels = ((axs[0], g1v, g1ok, 'BRG: best-response gain', lams), (axs[1], g2v, g2ok, 'HSC: honest cost', ['']),
              (axs[2], g3v, g3ok, 'SST: worst stake change', lams))
    for k, (ax, V, OK, ttl, cols) in enumerate(panels):
        ax.imshow(OK.astype(int), cmap=cmap, vmin=0, vmax=1, aspect='auto')
        for i in range(V.shape[0]):
            for j in range(V.shape[1]):
                if not np.isnan(V[i, j]):
                    ax.text(j, i, f'{V[i, j]:+.1%}' if k != 1 else f'{V[i, j]:+.2%}', ha='center', va='center',
                            fontsize=8, color=C_DARK)
        ax.set_xticks(range(len(cols)))
        ax.set_xticklabels([f'{c:.0%}' if c != '' else '' for c in cols])
        ax.set_title(ttl)
        ax.set_xlabel('λ' if k != 1 else '')
        if k == 0:
            ax.set_yticks(range(len(rules)))
            ax.set_yticklabels(rules, fontsize=8)
        else:
            ax.set_yticks([])
    fig.text(0.5, 0.005, f"Thresholds are placeholders: BRG {th['brg_tol']:.1%}, HSC {th['hsc_tol']:.1%}, "
             f"SST ±{th['state_tol']:.1%} on the state's stake. Failures are shown as failures, not rounded.",
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_VMP_{PAIRS['VMP']['slug']}.png")
    return {'path': path, 'series': {'g1_gain': g1v.flatten().tolist(), 'g2_cost': g2v.flatten().tolist(),
                                     'sst_state': g3v[~np.isnan(g3v)].tolist()}}


# ── PSS SPT/SST scatter ───────────────────────────────────────────────────────────

def build_PSS(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    th = get_key(data, 'p5.thresholds')
    rule = _chain(p, data)[-1]
    lam_b = p['val_gen']['lambda_base']
    allr = get_key(data, 'p5.search')[f'{rule}|{lam_b}']['all']
    rr = [r for r in allr if r['pv_rel'] is not None and r['state_rel'] is not None]
    x = [r['gain'] for r in rr]
    ser = {'gain': x, 'pv_rel': [r['pv_rel'] for r in rr], 'state_rel': [r['state_rel'] for r in rr]}
    fig, axs = plt.subplots(1, 2, figsize=FIG_PAIR)
    for ax, key, ttl in ((axs[0], 'pv_rel', 'PV of revenue to the state'), (axs[1], 'state_rel', "State's terminal stake")):
        y = ser[key]
        ax.axhspan(-th['state_tol'], th['state_tol'], color=C_GRID, alpha=0.7, label='SPT/SST tolerance')
        ax.axvline(0.0, color=C_ANNOTATION, lw=0.8)
        out = [i for i, (gx, gy) in enumerate(zip(x, y)) if gx > 0 and abs(gy) > th['state_tol']]
        ok = [i for i in range(len(x)) if i not in set(out)]
        ax.scatter([x[i] for i in ok], [y[i] for i in ok], s=14, color=C_WDT, label='within tolerance or no gain')
        ax.scatter([x[i] for i in out], [y[i] for i in out], s=22, color=C_CONV, label='gains and outside tolerance')
        for i in sorted(out, key=lambda i: -abs(y[i]))[:3]:
            ax.annotate(rr[i]['label'], (x[i], y[i]), fontsize=7, xytext=(-6, 8), textcoords='offset points', ha='right')
        _pct_axis(ax, 'x', 1)
        _pct_axis(ax, 'y', 1)
        ax.set_xlabel('Family gain over honest')
        ax.set_ylabel('Change vs honest family')
        ax.set_title(ttl)
        ax.legend(fontsize=8)
    path = save_fig(fig, _OUT / f"val_fig_PSS_{PAIRS['PSS']['slug']}.png")
    return {'path': path, 'series': ser}


BUILDERS.update({'ABL': build_ABL, 'VMP': build_VMP, 'FBR': build_FBR, 'PSS': build_PSS,
                 'GLM': build_GLM, 'HCS': build_HCS})



# ── mechanism set: UCC to VSY ──────────────────────────────────────────────────

def _lab_reset(n) -> str:
    return 'never' if int(n) == 0 else f'every {int(n)}y'


def _grid(cells: dict):
    ac = sorted({float(k.split('|')[0]) for k in cells})
    ad = sorted({float(k.split('|')[1]) for k in cells})
    return ac, ad


def build_UCC(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    rt = get_key(data, 'p2b_round_trip_units')
    osc = get_key(data, 'p2b_oscillation')
    bm = get_key(data, 'p2_benchmark_plan_s1')
    fig, axs = plt.subplots(1, 3, figsize=FIG_PAIR_XW)
    names = list(rt)
    axs[0].scatter(names, [rt[k] for k in names], s=120, color=[C_WDT, C_CONV][:len(names)], zorder=3)
    axs[0].axhline(1.0, color=C_ANNOTATION, ls=':')
    axs[0].set_xlim(-0.6, len(names) - 0.4)
    axs[0].set_ylim(0.99, max(rt.values()) * 1.01)
    axs[0].set_ylabel('Units held after price rise then fall (1 = no more than paid)')
    axs[0].set_title('Round trip')
    fl = osc['first_flows']
    axs[1].bar(range(len(fl)), fl, color=C_WDT)
    axs[1].axhline(0.0, color=C_ANNOTATION, lw=0.8)
    axs[1].set_xticks(range(len(fl)))
    axs[1].set_xlabel('Year after the one-off delta')
    axs[1].set_ylabel('Annual flow (£m)')
    axs[1].set_title('Oscillation settles')
    import numpy as np
    x = np.arange(len(bm))
    axs[2].bar(x - 0.2, [r['gain'] for r in bm], 0.4, color=C_WDT, label='Engine')
    if data.get('p2_plan_fixture_applies', True):
        axs[2].bar(x + 0.2, [r['plan'] for r in bm], 0.4, color=C_ANNOTATION, label='Plan')
    axs[2].set_xticks(x)
    axs[2].set_xticklabels([f"N={r['N']}\nα={r['alpha']:g}" for r in bm], fontsize=8)
    _pct_axis(axs[2])
    axs[2].set_ylabel('Gain over honest')
    axs[2].set_title('Benchmark against plan' if data.get('p2_plan_fixture_applies', True)
                     else 'Single-life gain (plan values do not apply)')
    axs[2].legend(fontsize=8)
    path = save_fig(fig, _OUT / f"val_fig_UCC_{PAIRS['UCC']['slug']}.png")
    return {'path': path, 'series': {'round_trip': list(rt.values()), 'flows': fl + [osc['net_engine'], osc['net_legacy']],
                                     'bench': [r['gain'] for r in bm] + [r['plan'] for r in bm]}}


def build_WLG(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    ex = get_key(data, 'examples')
    ks = sorted(ex, key=float)
    hk = [k for k in ks if abs(float(k) - 1.0) < 1e-12]
    if not hk:
        raise KeyError('examples must include the honest case alpha = 1')
    h = ex[hk[0]]
    others = [ex[k] for k in ks if k != hk[0]]
    ah = h['decomposition']['alpha']
    t = [r['t'] for r in h['rows']]
    ser = {'V': [r['V'] for r in h['rows']], 'W_h': [r['W'] for r in h['rows']], 'L_h': [r['L'] for r in h['rows']],
           'f_h': [r['f'] for r in h['rows']]}
    fig, axs = plt.subplots(1, 3, figsize=FIG_PAIR_XW)
    axs[0].plot(t, ser['V'], color=C_DARK, label='True value')
    axs[0].plot(t, ser['W_h'], color=C_WDT, ls='--', label=f'Declared, α = {ah:g}')
    axs[1].plot(t, ser['L_h'], color=C_WDT, ls='--', label=f'Liability, α = {ah:g}')
    axs[2].plot(t, ser['f_h'], color=C_WDT, ls='--', label=f'Family units, α = {ah:g}')
    for o in others:
        al = o['decomposition']['alpha']
        col = C_CONV if al > 1 else C_WDT_BASE
        r = o['rows']
        for key, name in (('W', 'W'), ('L', 'L'), ('true_paid', 'paid'), ('f', 'f'), ('s', 's')):
            ser[f'{name}_{al:g}'] = [x[key] for x in r]
        axs[0].plot(t, ser[f'W_{al:g}'], color=col, label=f'Declared, α = {al:g}')
        axs[1].plot(t, ser[f'L_{al:g}'], color=col, label=f'Liability, α = {al:g}')
        axs[1].plot(t, ser[f'paid_{al:g}'], color=col, ls=':', label=f'True value paid, α = {al:g}')
        axs[2].plot(t, ser[f'f_{al:g}'], color=col, label=f'Family units, α = {al:g}')
        axs[2].plot(t, ser[f's_{al:g}'], color=C_ANNOTATION, ls='-.' if al > 1 else ':', label=f'State units, α = {al:g}')
    axs[0].set_ylabel('£m')
    axs[0].set_title('Value')
    axs[1].set_ylabel('£m')
    axs[1].set_title('Liability')
    axs[2].set_title('Units')
    for ax in axs:
        ax.set_xlabel('Year')
        ax.legend(fontsize=7)
    path = save_fig(fig, _OUT / f"val_fig_WLG_{PAIRS['WLG']['slug']}.png")
    return {'path': path, 'series': ser}


def build_CDS(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    apply_style(grid=False)
    s = get_key(data, 'p3_surface')
    ac, ad = _grid(s['cells'])
    conf = {tuple(map(float, k.split('|'))) for k in s['conflict_cells']}
    G = np.array([[s['cells'][f'{a}|{b}']['gain'] for b in ad] for a in ac])
    P = np.array([[np.nan if s['cells'][f'{a}|{b}']['pv_rel'] is None else s['cells'][f'{a}|{b}']['pv_rel']
                   for b in ad] for a in ac])
    fig, axs = plt.subplots(1, 2, figsize=FIG_PAIR_XW)
    for ax, M, ttl in ((axs[0], G, 'Family gain over honest'), (axs[1], P, 'Change in PV of revenue to the state')):
        lim = np.nanmax(np.abs(M))
        im = ax.imshow(M, cmap='RdBu_r', vmin=-lim, vmax=lim, aspect='auto', origin='lower')
        for i in range(len(ac)):
            for j in range(len(ad)):
                if not np.isnan(M[i, j]):
                    ax.text(j, i, f'{M[i, j]:.1%}'.replace('-0.0%', '0.0%'), ha='center', va='center', fontsize=7, color=C_DARK)
                if (ac[i], ad[j]) in conf:
                    ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec=C_DARK, lw=2))
        ax.set_xticks(range(len(ad)))
        ax.set_xticklabels([f'{b:g}' for b in ad])
        ax.set_yticks(range(len(ac)))
        ax.set_yticklabels([f'{a:g}' for a in ac])
        ax.set_xlabel('α_D (Route D declaration ratio)')
        ax.set_ylabel('α_C (Route C declaration ratio)')
        ax.set_title(ttl)
        _pct_cbar(fig.colorbar(im, ax=ax))
    path = save_fig(fig, _OUT / f"val_fig_CDS_{PAIRS['CDS']['slug']}.png")
    return {'path': path, 'series': {'gain': G.flatten().tolist(), 'pv_rel': P[~np.isnan(P)].tolist()}}


def build_RIS(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    rs = get_key(data, 'p3_reset_sensitivity')
    ivs = list(rs)
    ad = sorted(float(a) for a in rs[ivs[0]])
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ser = {}
    for iv, col in zip(ivs, RULE_COLOURS):
        y = [rs[iv][str(b)]['gain'] for b in ad]
        ser[f'reset_{iv}'] = y
        ax.plot(ad, y, marker='o', color=col, label=_lab_reset(iv))
    ax.axhline(0.0, color=C_ANNOTATION, lw=0.8)
    _pct_axis(ax)
    ax.set_xlabel('α_D (Route D declaration ratio)')
    ax.set_ylabel('Family gain over honest')
    ax.legend(title='Reset interval')
    path = save_fig(fig, _OUT / f"val_fig_RIS_{PAIRS['RIS']['slug']}.png")
    return {'path': path, 'series': ser}


def build_DSH(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    dil = get_key(data, 'p3_dilution')
    cs = get_key(data, 'p4_C_share_sensitivity')['cells']
    hv = get_key(data, 'p4_C_heavy_stress_gain')
    alphas = sorted(float(a) for a in next(iter(cs.values())))
    fig, axs = plt.subplots(1, 3, figsize=FIG_PAIR_XW)
    xs = [float(k) for k in dil]
    axs[0].plot(xs, list(dil.values()), marker='o', color=C_WDT)
    _pct_axis(axs[0], 'x')
    _pct_axis(axs[0], 'y', 2)
    axs[0].set_xlabel('Route C share of wealth')
    axs[0].set_ylabel('Gain over honest')
    axs[0].set_title('Dilution')
    ser = {'dilution': list(dil.values()), 'heavy': list(hv.values())}
    shares = list(dict.fromkeys(k.split('|')[0] for k in cs))
    lam_keys = list(dict.fromkeys(k.split('|')[1] for k in cs))
    for key, row in cs.items():
        sh, lm = key.split('|')
        y = [row[str(a)]['gain'] for a in alphas]
        ser[key] = y
        axs[1].plot(alphas, y, marker='o', ms=3, color=[C_WDT, C_CONV, C_ANNOTATION][shares.index(sh) % 3],
                    ls='-' if lam_keys.index(lm) == 0 else '--', label=key.replace('lambda', 'λ'))
    _pct_axis(axs[1])
    axs[1].set_xscale('log')
    axs[1].set_xlabel('α_C (log scale)')
    axs[1].set_title('Route C share sensitivity')
    axs[1].legend(fontsize=6, ncol=2)
    axs[2].plot([float(k) for k in hv], list(hv.values()), marker='o', color=C_CONV)
    axs[2].axhline(0.0, color=C_ANNOTATION, lw=0.8)
    _pct_axis(axs[2], 'x')
    _pct_axis(axs[2], 'y', 1)
    axs[2].set_xlabel('λ')
    axs[2].set_title('Route-C-heavy stress')
    path = save_fig(fig, _OUT / f"val_fig_DSH_{PAIRS['DSH']['slug']}.png")
    return {'path': path, 'series': ser}


def build_VSY(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    sw = get_key(data, 'p4_lambda_sweep')
    lams = [l for l in sw['by_lambda'] if float(l) > 0.0]
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ser = {}
    for l, col in zip(lams, RULE_COLOURS + [C_CONV]):
        y = sw['by_lambda'][l]['verified_share_by_year']
        ser[f'lam_{l}'] = y
        ax.plot(range(1, len(y) + 1), y, color=col, label=f'λ = {float(l):.0%}')
    ax.axhline(sw['verified_threshold'], color=C_ANNOTATION, ls=':')
    ax.text(1, sw['verified_threshold'], ' threshold', color=C_ANNOTATION, va='bottom', fontsize=9)
    _pct_axis(ax)
    ax.set_xlabel('Year')
    ax.set_ylabel('Share of Route C units verified')
    ax.legend()
    path = save_fig(fig, _OUT / f"val_fig_VSY_{PAIRS['VSY']['slug']}.png")
    return {'path': path, 'series': ser}


BUILDERS.update({'UCC': build_UCC, 'WLG': build_WLG, 'CDS': build_CDS, 'RIS': build_RIS, 'DSH': build_DSH, 'VSY': build_VSY})



# ── DOMG dominance grid ──────────────────────────────────────────────────────

def build_DOMG(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    dm = get_key(data, 'p5.dmg')['by_rule']
    th = get_key(data, 'p5.thresholds')
    rules = list(dm)
    labels = []
    for rule in rules:
        for r in dm[rule]['dominant']:
            if r['label'] not in labels:
                labels.append(r['label'])
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    y = np.arange(len(labels))
    ser = {}
    for i, rule in enumerate(rules):
        col = C_CONV if i == 0 else C_WDT
        by = {r['label']: r for r in dm[rule]['dominant']}
        yy = [k + (i - (len(rules) - 1) / 2) * 0.25 for k, lb in enumerate(labels) if lb in by]
        mins = [by[lb]['min_gain'] for lb in labels if lb in by]
        means = [by[lb]['mean_gain'] for lb in labels if lb in by]
        ser[f'{rule}_min'] = mins
        ser[f'{rule}_mean'] = means
        ax.scatter(mins, yy, color=col, marker='o', s=40, zorder=3, label=f'{rule}: smallest gain')
        ax.scatter(means, yy, color=col, marker='D', s=40, zorder=3, label=f'{rule}: mean gain')
    ax.axvline(th['brg_tol'], color=C_ANNOTATION, ls=':')
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    _pct_axis(ax, 'x', 1)
    ax.set_xlabel('Gain over honest family across scenarios')
    ax.legend(fontsize=8, loc='lower right')
    fig.text(0.5, 0.005, 'Dotted line: BRG tolerance (placeholder).', ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_DOMG_{PAIRS['DOMG']['slug']}.png")
    return {'path': path, 'series': ser}


# ── HERR honest valuation error ──────────────────────────────────────────────

def build_HERR(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    hc = get_key(data, 'p5.hec')
    cells = hc['cells']
    sig = [s_ for s_ in hc['sigmas'] if s_ > 0.0]
    combos = []
    for c in cells.values():
        k = (c['rule'], c['lambda'])
        if k not in combos:
            combos.append(k)
    rules = []
    for r, _l in combos:
        if r not in rules:
            rules.append(r)
    lams = sorted({l for _r, l in combos})
    fig, axs = plt.subplots(1, len(lams), figsize=FIG_PAIR, sharey=True)
    ser = {}
    for ax, lam in zip(axs, lams):
        for i, rule in enumerate(rules):
            col = C_CONV if i == 0 else C_WDT
            cs = [cells[f'{rule}|{lam}|{s_}'] for s_ in sig]
            mean = [c['gain_mean'] for c in cs]
            lo = [c['gain_p05'] for c in cs]
            hi = [c['gain_p95'] for c in cs]
            ser[f'{rule}_{lam}_mean'] = mean
            ser[f'{rule}_{lam}_p05'] = lo
            ser[f'{rule}_{lam}_p95'] = hi
            ax.plot(sig, mean, color=col, marker='o', label=rule)
            ax.fill_between(sig, lo, hi, color=col, alpha=0.15)
        ax.axhline(0.0, color=C_ANNOTATION, lw=0.8)
        ax.set_title(f'λ = {lam:.0%}', fontsize=9)
        ax.set_xlabel('Sd of honest valuation error')
        ax.set_xticks(sig)
        ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0, decimals=0))
        _pct_axis(ax, 'y', 1)
    axs[0].set_ylabel('Gain over error-free honest family')
    axs[0].legend(fontsize=8)
    fig.text(0.5, 0.005, 'Lines: mean over paths; bands: 5th to 95th percentile. Error parameters are placeholders.',
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_HERR_{PAIRS['HERR']['slug']}.png")
    return {'path': path, 'series': ser}


# ── UOS understatement against overstatement ────────────────────────────────

def build_UOS(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    uo = get_key(data, 'p5.uos')
    th = get_key(data, 'p5.thresholds')
    shares, cells = uo['c_share_vals'], uo['cells']
    blocks = []
    for c in cells.values():
        k = (c['rule'], c['lambda'])
        if k not in blocks:
            blocks.append(k)
    rules = []
    for r, _l in blocks:
        if r not in rules:
            rules.append(r)
    lams = sorted({l for _r, l in blocks})
    fig, axs = plt.subplots(1, len(lams), figsize=FIG_PAIR, sharey=False)
    ser = {'c_share': shares}
    for ax, lam in zip(axs, lams):
        for i, rule in enumerate(rules):
            col = C_CONV if i == 0 else C_WDT
            for d, ls in (('under', '-'), ('over', '--')):
                v = [cells[f'{rule}|{lam}|{cs}']['best'][d]['gain'] for cs in shares]
                ser[f'{rule}_{lam}_{d}'] = v
                ax.plot(shares, v, color=col, ls=ls, marker='o', ms=4, label=f'{rule}: {d}')
        ax.axhline(th['brg_tol'], color=C_ANNOTATION, ls=':')
        ax.set_title(f'λ = {lam:.0%}', fontsize=9)
        ax.set_xlabel('Route C share of asset base')
        ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0, decimals=0))
        _pct_axis(ax, 'y', 1)
    axs[0].set_ylabel('Best gain over honest family')
    axs[-1].legend(fontsize=7, loc='upper left')
    fig.text(0.5, 0.005, 'Solid: understating strategies; dashed: overstating. Dotted: BRG tolerance (placeholder).',
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_UOS_{PAIRS['UOS']['slug']}.png")
    return {'path': path, 'series': ser}


# ── LGR single-life gain grid ────────────────────────────────────────────────

def build_LGR(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style(grid=False)
    lf = get_key(data, 'life')
    alphas, gs = lf['alphas'], lf['g_vals']
    M = np.array([[lf['grid'][f'{a}|{g}']['gain'] for g in gs] for a in alphas])
    lim = float(np.nanmax(np.abs(M)))
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    im = ax.imshow(M, cmap='RdBu_r', vmin=-lim, vmax=lim, aspect='auto')
    ax.set_xticks(range(len(gs)))
    ax.set_xticklabels([f'{g:.1%}' for g in gs], fontsize=8, rotation=45)
    ax.set_yticks(range(len(alphas)))
    ax.set_yticklabels([str(a) for a in alphas], fontsize=8)
    ax.set_xlabel('Asset growth g')
    ax.set_ylabel('Declaration ratio α')
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f'{M[i, j]:+.1%}', ha='center', va='center', fontsize=6, color=C_DARK)
    cb = fig.colorbar(im, ax=ax)
    cb.ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    cb.set_label('Change in terminal wealth vs honest')
    path = save_fig(fig, _OUT / f"val_fig_LGR_{PAIRS['LGR']['slug']}.png")
    return {'path': path, 'series': {'gain': M.flatten().tolist()}}


BUILDERS.update({'DOMG': build_DOMG, 'HERR': build_HERR, 'UOS': build_UOS, 'LGR': build_LGR})



# ── LNS single-life holding-period sweep ─────────────────────────────────────

def build_LNS(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    lf = get_key(data, 'life')
    alphas, ns = lf['alphas'], lf['n_vals']
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ser = {'n': ns}
    for a in alphas:
        v = [lf['by_n'][f'{a}|{n}']['gain'] for n in ns]
        ser[f'alpha_{a}'] = v
        if a == 1.0:
            continue
        col = C_CONV if a > 1.0 else C_WDT
        ax.plot(ns, v, color=col, alpha=0.35 + 0.65 * min(abs(a - 1.0), 1.0), marker='o', ms=3, label=f'α = {a}')
    ax.axhline(0.0, color=C_ANNOTATION, lw=0.8)
    ax.set_xlabel('Holding period (years)')
    ax.set_ylabel('Change in terminal wealth vs honest')
    _pct_axis(ax, 'y', 0)
    ax.legend(fontsize=7, ncol=2)
    fig.text(0.5, 0.005, 'Red: overstating (α above 1). Blue: understating.', ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_LNS_{PAIRS['LNS']['slug']}.png")
    return {'path': path, 'series': ser}


BUILDERS.update({'LNS': build_LNS})


def main(only=None) -> None:
    p = load_params()
    data = load_data()
    _check_stamp(data, p)
    ensure_dir(_OUT)
    for pid in PAIRS:
        if only and pid not in only:
            continue
        BUILDERS[pid](data, p)


if __name__ == '__main__':
    main(only=sys.argv[1:] or None)
