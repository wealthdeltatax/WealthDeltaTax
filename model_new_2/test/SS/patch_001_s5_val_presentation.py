"""
patch_NNN_s5_val_presentation.py -- S5: VAL tables and figures for the S1 outputs, and RIS rebuilt as the voluntary-reset sensitivity.

Files edited : 5_6_VALGEN_tables.py, 5_7_VALGEN_charts.py, WDT_Params.toml ([names.val] only)
Changes numbers?  no. It only presents keys valgen_core already writes. Re-run: python 5_6_VALGEN_tables.py ; python 5_7_VALGEN_charts.py
Plan / decision   : Work Order S5; Refactor Plan Phase 2.8 (S1 contract: data['replay'], data['p6'], data['rho'])

Adds (each a table and a figure, same JSON keys, same id):
    RPL   JST replay, full loop and contiguous         BES   breakeven deferral spread (per archetype)
    ARC   archetypes: Route B sale / lien / income     RSP   rho and the SPT sensitivity (SST primary)
    LCD   lambda_C x lambda_D grid                     BAND  V0 swept across the RATES revenue bands
    HLP   headline contrast pair (average and top payer, from the RATES JSON)
Replaces RIS (reset-interval sensitivity, which read a retired clock) with the voluntary-reset sensitivity:
    (a) best response by reset cycle x lambda, from p5.search[...].best_by_cycle; (b) the old alpha_D by cycle table.
A part valgen_core skipped (no replay, no archetypes, no RATES JSON) gives a one-line note / no figure, not an error.

Run from Model/test:
    python patch_NNN_s5_val_presentation.py            dry run
    python patch_NNN_s5_val_presentation.py --apply
Test:
    python test_patch_NNN_s5_val_presentation.py       (sandbox)   then   --live   after --apply
Rename NNN to the next number (python wdt_patchlib.py next); the test finds this file by its slug.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wdt_patchlib import Delete, InsertAfter, InsertBefore, Replace, patch_cli   # noqa: E402,F401

NAME = Path(__file__).stem

_PAIRS_T = r'''    'RPL': {'json': ['replay', 'p5.thresholds'], 'slug': 'jst_replay', 'title': 'JST replay: full loop and contiguous windows',
          'label': 'Table RPL'},
    'ARC': {'json': ['p6', 'p5.thresholds'], 'slug': 'archetypes', 'title': 'Archetypes: Route B sale, lien and income',
          'label': 'Table ARC'},
    'BES': {'json': ['p6', 'rho'], 'slug': 'breakeven_spread', 'title': 'Breakeven deferral spread',
          'label': 'Table BES'},
    'RSP': {'json': ['rho', 'p5.search', 'p5.thresholds'], 'slug': 'rho_spt', 'title': 'Discount rate and the SPT sensitivity',
          'label': 'Table RSP'},
    'LCD': {'json': ['p3_lambda_grid', 'p5.thresholds'], 'slug': 'lambda_c_d', 'title': 'lambda_C x lambda_D grid',
          'label': 'Table LCD'},
    'BAND': {'json': ['v0_sweep', 'p5.thresholds'], 'slug': 'v0_bands', 'title': 'Launch wealth across the RATES revenue bands',
          'label': 'Table BAND'},
    'HLP': {'json': ['p5.hlc_pair', 'p5.headline'], 'slug': 'headline_pair', 'title': 'Headline contrast: average and top payer',
          'label': 'Table HLP'},
'''

_PAIRS_C = r'''    'RPL': {'json': ['replay', 'p5.thresholds'], 'slug': 'jst_replay', 'title': 'JST replay: full loop and contiguous windows',
          'label': 'Figure RPL'},
    'ARC': {'json': ['p6', 'p5.thresholds'], 'slug': 'archetypes', 'title': 'Archetypes: Route B sale, lien and income',
          'label': 'Figure ARC'},
    'BES': {'json': ['p6', 'rho'], 'slug': 'breakeven_spread', 'title': 'Breakeven deferral spread',
          'label': 'Figure BES'},
    'RSP': {'json': ['rho', 'p5.search', 'p5.thresholds'], 'slug': 'rho_spt', 'title': 'Discount rate and the SPT sensitivity',
          'label': 'Figure RSP'},
    'LCD': {'json': ['p3_lambda_grid', 'p5.thresholds'], 'slug': 'lambda_c_d', 'title': 'lambda_C x lambda_D grid',
          'label': 'Figure LCD'},
    'BAND': {'json': ['v0_sweep', 'p5.thresholds'], 'slug': 'v0_bands', 'title': 'Launch wealth across the RATES revenue bands',
          'label': 'Figure BAND'},
    'HLP': {'json': ['p5.hlc_pair', 'p5.headline'], 'slug': 'headline_pair', 'title': 'Headline contrast: average and top payer',
          'label': 'Figure HLP'},
'''

_OLD_RIS_T = r'''def build_RIS(data: dict, p: dict) -> dict:
    rs = get_key(data, 'p3_reset_sensitivity')
    ivs = list(rs)
    ad = sorted(float(a) for a in rs[ivs[0]])
    rows, values = [], []
    for iv in ivs:
        row = [f'**{_lab_reset(iv)}**']
        for b in ad:
            g = rs[iv][str(b)]['gain']
            row.append(fmt_pct(g, 1))
            values.append(g)
        rows.append(row)
    cap = (f"Table RIS: Family gain from understating Route D (α_D) by the family's own voluntary reset cycle, α_C = 1; the honest family never resets. A reset re-values "
           f"Route D at the auction price. T = {p['val_gen']['T']}, G = {p['val_gen']['G']}.")
    return {'md': md_table(['Reset cycle \\ α_D'] + [f'{b:g}' for b in ad], rows) + '\n\n' + cap, 'values': values}
'''

_NEW_RIS_T = r'''def build_RIS(data: dict, p: dict) -> dict:
    srch = get_key(data, 'p5.search')
    lams = get_key(data, 'p5.lambda_vals')
    rule = _chain(p, data)[-1]
    rs = get_key(data, 'p3_reset_sensitivity')
    cycles = list(srch[f'{rule}|{lams[0]}']['best_by_cycle'])
    heads1 = ['Voluntary reset cycle \\ λ'] + [f'{l:.0%}' for l in lams]
    rows1, values = [], []
    for c in cycles:
        row = [f'**{_lab_reset(c)}**']
        for l in lams:
            g = srch[f'{rule}|{l}']['best_by_cycle'][c]['gain']
            row.append(fmt_pct(g, 1))
            values.append(g)
        rows1.append(row)
    ivs = list(rs)
    ad = sorted(float(a) for a in rs[ivs[0]])
    rows2 = []
    for iv in ivs:
        row = [f'**{_lab_reset(iv)}**']
        for b in ad:
            g = rs[iv][str(b)]['gain']
            row.append(fmt_pct(g, 1))
            values.append(g)
        rows2.append(row)
    cap = (f"Table RIS: Voluntary Route D reset. (a) Best-response gain over the honest family by the family's own reset cycle and the "
           f"verification hazard λ, under {rule}; 'never' is the best of the strategies that do not reset. (b) Family gain from understating "
           f"Route D (α_D) by reset cycle, α_C = 1, λ = 0, against an honest family that never resets. A reset is an action the family "
           f"chooses, not a rule: it re-values Route D at the auction price and settles the accrued liability. "
           f"T = {p['val_gen']['T']}, G = {p['val_gen']['G']}.")
    return {'md': ('(a) Best response by reset cycle and λ\n\n' + md_table(heads1, rows1) +
                   '\n\n(b) Route D understatement by reset cycle\n\n' +
                   md_table(['Voluntary reset cycle \\ α_D'] + [f'{b:g}' for b in ad], rows2) + '\n\n' + cap),
            'values': values}
'''

_BLOCK_T = r'''# ── S5 (Work Order): replay, archetypes, breakeven, rho, lambda grid, V0 bands, HLC pair ──────────────────────────────────
# Every table below reads keys valgen_core already writes: replay, p6, rho, p3_lambda_grid, v0_sweep, p5.hlc_pair, p5.search.
# A section the core skipped (no replay, no archetypes, no RATES JSON) builds a one-line note instead of failing the run.

def _skipped(d) -> bool:
    return (not d) or (isinstance(d, dict) and bool(d.get('skipped')))


def _not_built(pid: str, why: str) -> dict:
    return {'md': f'Table {pid}: not built. {why}', 'values': []}


def _split_key(key: str):
    """'rule|lambda' -> (rule, float lambda). Rule keys contain '/' but never '|'."""
    rule, lam = key.rsplit('|', 1)
    return rule, float(lam)


_MODE_LABEL = {'sale': 'Sale', 'lien': 'Lien', 'income': 'Income'}


# ── RPL JST replay ───────────────────────────────────────────────────────────

def build_RPL(data: dict, p: dict) -> dict:
    rp = data.get('replay')
    if _skipped(rp):
        return _not_built('RPL', 'The JST replay was skipped (replay_stride = 0 or no replay_countries in [val_gen]).')
    th = get_key(data, 'p5.thresholds')
    heads = ['Country', 'Rule set', 'λ', 'Windows', 'Number', 'BRG pass', 'SST pass', 'Median gain', 'Max gain']
    rows, values, counts = [], [], []
    for iso, c in rp['countries'].items():
        ncont = sum(1 for r in c['rows'] if r['contiguous'])
        counts.append(f"{iso}: {c['usable_years']} usable years, {c['windows']} windows, {ncont} contiguous, "
                      f"{c['repeat_windows']} with repeated years")
        for key, sm in c['summary'].items():
            rule, lam = _split_key(key)
            for nm, lab in (('full_loop', 'Full loop'), ('contiguous', 'Contiguous')):
                s = sm[nm]
                if s is None:
                    rows.append([iso, f'**{rule}**', f'{lam:.0%}', lab, '0', 'n/a', 'n/a', 'n/a', 'n/a'])
                    continue
                rows.append([iso, f'**{rule}**', f'{lam:.0%}', lab, str(s['windows']), fmt_pct(s['BRG_pass_share'], 0),
                             fmt_pct(s['SST_pass_share'], 0), fmt_pct(s['gain_median'], 1), fmt_pct(s['gain_max'], 1)])
                values += [s['BRG_pass_share'], s['SST_pass_share'], s['gain_median'], s['gain_max']]
    m = data['meta']
    cap = (f"Table RPL: The headline rule sets on the real JST capital-return path of each loop window ({rp['T']} years, every "
           f"{rp['stride']}th start year). The history wraps, so a window that crosses the seam repeats years: it is in the full "
           f"loop but not in the contiguous set. Share of windows passing BRG (best-response gain at most {fmt_pct(th['brg_tol'], 1)}) "
           f"and SST (state stake within ±{fmt_pct(th['state_tol'], 1)}), and the median and largest best-response gain over the "
           f"strategy library. {'; '.join(counts)}. Windows overlap, so they are not independent draws. "
           f"T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['left', 'left', 'center', 'left'] + ['center'] * 5) + '\n\n' + cap,
            'values': values}


# ── ARC archetypes ───────────────────────────────────────────────────────────

def _arc_data(data: dict):
    arch = (data.get('p6') or {}).get('archetypes')
    if not arch:
        return None, None, None
    first = next(iter(arch.values()))
    modes = list(first['modes'])
    lams = sorted({float(k) for k in first['modes'][modes[0]]['best']})
    return arch, modes, lams


def build_ARC(data: dict, p: dict) -> dict:
    arch, modes, lams = _arc_data(data)
    if arch is None:
        return _not_built('ARC', 'valgen_core found no [archetypes] / [route_b] blocks in the parameter file.')
    heads = ['Archetype', 'V0', 'Route B mode', 'Honest terminal wealth (£m)', 'State PV (£m)', 'Income paid (£m)'] + \
        [f'Best response, λ = {l:.0%}' for l in lams]
    rows, values = [], []
    for name, a in arch.items():
        for mode in modes:
            c = a['modes'][mode]
            row = [f"**{a['label']}**", f"£{a['V0_m']:g}m", _MODE_LABEL.get(mode, mode), f"{c['TW']:,.1f}", f"{c['PV']:,.1f}",
                   f"{c['income_paid']:,.1f}"]
            values += [c['TW'], c['PV'], c['income_paid']]
            for l in lams:
                b = c['best'][str(l)]
                row.append(f"{fmt_pct(b['gain'], 1)} {'pass' if b['BRG'] else 'FAIL'} ({b['label']})")
                values.append(b['gain'])
            rows.append(row)
    th = get_key(data, 'p5.thresholds')
    shares = '; '.join(f"{a['label']}: " + ' '.join(f"{k} {v:.0%}" for k, v in a['shares'].items()) for a in arch.values())
    m = data['meta']
    cap = (f"Table ARC: The five archetypes through the family engine under the candidate rule set, with Route B settled by sale, "
           f"by a deferred lien and from external income. Honest terminal wealth and the present value of the state's receipts are "
           f"true £m; income paid is the cumulative external income the state received. Best response is the best of the "
           f"{data['p5']['n_strategies']}-strategy library (a lower bound), with the BRG verdict at {fmt_pct(th['brg_tol'], 1)}. "
           f"Route shares: {shares}. Shares, income ratios and the deferral spread are placeholders. "
           f"T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['left', 'center', 'left'] + ['center'] * (len(heads) - 3)) + '\n\n' + cap,
            'values': values}


# ── BES breakeven deferral spread ────────────────────────────────────────────

def build_BES(data: dict, p: dict) -> dict:
    arch, _modes, _lams = _arc_data(data)
    if arch is None:
        return _not_built('BES', 'valgen_core found no [archetypes] / [route_b] blocks in the parameter file.')
    rb = p.get('route_b') or {}
    toml_sp = rb.get('deferral_spread')
    heads = ['Archetype', 'V0', 'Breakeven spread'] + (['Placeholder spread', 'Placeholder against breakeven'] if toml_sp is not None else [])
    rows, values = [], []
    for name, a in arch.items():
        be = a['breakeven_spread']
        row = [f"**{a['label']}**", f"£{a['V0_m']:g}m", 'not bracketed in [-4%, +30%]' if be is None else f'{be:+.2%}']
        if be is not None:
            values.append(be)
        if toml_sp is not None:
            row.append(f'{toml_sp:+.2%}')
            values.append(toml_sp)
            row.append('n/a' if be is None else ('above' if toml_sp > be else 'below'))
        rows.append(row)
    m = data['meta']
    sov = rb.get('sovereign_real_rate')
    cap = (f"Table BES: Breakeven deferral spread by archetype: the spread over the sovereign real rate"
           + (f" ({fmt_pct(sov, 2)})" if sov is not None else '')
           + f" at which the present value of the state's receipts under the Route B lien equals its value under sale, "
           f"at ρ = {fmt_pct(data['rho']['base'], 1)}. At a spread above the breakeven the lien is worth more to the state than a sale. "
           f"Solved by bisection; 'not bracketed' means no spread in the range makes the two equal. "
           f"T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['left', 'center'] + ['center'] * (len(heads) - 2)) + '\n\n' + cap, 'values': values}


# ── RSP rho and the SPT sensitivity ──────────────────────────────────────────

def _rsp_grid(data: dict, p: dict):
    vg = p['val_gen']
    lams = [0.0, vg['lambda_base']]
    rules = list(vg['headline_rules'])
    srch = get_key(data, 'p5.search')
    spt = get_key(data, 'rho.spt_by_rho')
    rho_keys = sorted(next(iter(spt.values())), key=float)
    cells = []
    for rule in rules:
        for lam in lams:
            k = f'{rule}|{lam}'
            cells.append({'rule': rule, 'lam': lam, 'sst': srch[k]['n_conflict_sst'], 'sst_ok': srch[k]['SST_pass'],
                          'spt': [(float(r), spt[k][r]['n_conflict'], spt[k][r]['pass']) for r in rho_keys]})
    return cells, [float(r) for r in rho_keys]


def build_RSP(data: dict, p: dict) -> dict:
    cells, rhos = _rsp_grid(data, p)
    heads = ['Rule set', 'λ', 'SST (primary)'] + [f'SPT, ρ = {r:.1%}' for r in rhos]
    rows, values = [], []
    for c in cells:
        row = [f"**{c['rule']}**", f"{c['lam']:.0%}", f"{c['sst']} {'pass' if c['sst_ok'] else 'FAIL'}"]
        values.append(c['sst'])
        for _r, n, ok in c['spt']:
            row.append(f"{n} {'pass' if ok else 'FAIL'}")
            values.append(n)
        rows.append(row)
    th = get_key(data, 'p5.thresholds')
    m = data['meta']
    cap = (f"Table RSP: Number of gaining strategies that leave the state outside ±{fmt_pct(th['state_tol'], 1)}, by test. SST, the "
           f"state's terminal stake, does not depend on the discount rate and is the primary state test. SPT, the present value of "
           f"the state's receipts, is shown at each ρ in the sweep (base ρ = {fmt_pct(data['rho']['base'], 1)}). A cell passes when the "
           f"count is zero. {data['p5']['n_strategies']}-strategy library. T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['left', 'center'] + ['center'] * (len(heads) - 2)) + '\n\n' + cap, 'values': values}


# ── LCD lambda_C x lambda_D ──────────────────────────────────────────────────

def build_LCD(data: dict, p: dict) -> dict:
    g = get_key(data, 'p3_lambda_grid')
    lc, ld = g['lambda_C'], g['lambda_D']
    cells = g['cells']
    heads = ['λ_C \\ λ_D'] + [f'{b:.0%}' for b in ld]
    r1, r2, values = [], [], []
    for a in lc:
        row1, row2 = [f'**{a:.0%}**'], [f'**{a:.0%}**']
        for b in ld:
            c = cells[f'{a}|{b}']
            row1.append(fmt_pct(c['gain'], 1) + ('' if c['BRG'] else '*'))
            row2.append(c['label'])
            values.append(c['gain'])
        r1.append(row1)
        r2.append(row2)
    th = get_key(data, 'p5.thresholds')
    m = data['meta']
    cap = (f"Table LCD: Best-response gain over the honest family (top) and the strategy that achieves it (bottom), with the Route C "
           f"verification hazard λ_C and the Route D corrective-auction hazard λ_D varied independently, under {g['rule']}. "
           f"Cells marked * exceed the BRG threshold of {fmt_pct(th['brg_tol'], 1)}. Best of the strategy library: a lower bound. "
           f"T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': 'Best-response gain\n\n' + md_table(heads, r1) + '\n\nStrategy\n\n' + md_table(heads, r2) + '\n\n' + cap,
            'values': values}


# ── BAND V0 sweep across the RATES revenue bands ─────────────────────────────

def build_BAND(data: dict, p: dict) -> dict:
    v = get_key(data, 'v0_sweep')
    bands, rules, lams, cells = v['bands'], v['rules'], v['lambda_vals'], v['cells']
    combos = [(r, l) for r in rules for l in lams]
    heads = ['V0 (£m)'] + [f'{r}, λ = {l:.0%}: best gain' for r, l in combos] + [f'{r}: honest tax drag' for r in rules]
    rows, values = [], []
    for b in bands:
        row = [f'**{b:g}**']
        for r, l in combos:
            c = cells[f'{b}|{r}|{l}']
            row.append(f"{fmt_pct(c['gain'], 1)} {'pass' if c['BRG'] else 'FAIL'}")
            values.append(c['gain'])
        for r in rules:
            d = cells[f'{b}|{r}|{lams[0]}']['drag']
            row.append(fmt_pct(d, 1))
            values.append(d)
        rows.append(row)
    th = get_key(data, 'p5.thresholds')
    m = data['meta']
    cap = (f"Table BAND: Launch wealth V0 swept across the RATES revenue bands. Best-response gain over the honest family by rule set "
           f"and λ, with the BRG verdict at {fmt_pct(th['brg_tol'], 1)}, and the honest family's tax drag: one minus its terminal wealth "
           f"over the terminal wealth of a run with no tax. Route shares stay at the baseline mix; the archetype mixture by band is a "
           f"RATES output. {v['note'].split(';')[0]}. T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['left'] + ['center'] * (len(heads) - 1)) + '\n\n' + cap, 'values': values}


# ── HLP headline contrast: the pair (average payer, top payer) ───────────────

def build_HLP(data: dict, p: dict) -> dict:
    hp = data['p5'].get('hlc_pair')
    if _skipped(hp):
        why = hp.get('reason') if isinstance(hp, dict) else None
        return _not_built('HLP', (why or 'the RATES JSON was not available when valgen_core ran') + '. Run rates_core.py, then valgen_core.py.')
    hl = get_key(data, 'p5.headline')
    cand = hl['rules'][-1]
    lam_b = p['val_gen']['lambda_base']
    lams = [0.0, lam_b]
    avg, top = hp['burdens']['average'], hp['burdens']['top']
    alphas = [a for a in sorted(hl['alphas'], reverse=True) if a <= 1.0]
    heads = ['Declaration ratio α', f"Conventional, average payer ({fmt_pct(avg['rate'], 3)} a year)",
             f"Conventional, top payer ({fmt_pct(top['rate'], 3)} a year)"] + [f'WDT {cand}, λ = {l:.0%}' for l in lams]
    rows, values = [], []
    for a in alphas:
        row = [f'**{a:g}**', fmt_pct(avg['diag_alpha'][str(a)], 1), fmt_pct(top['diag_alpha'][str(a)], 1)]
        values += [avg['diag_alpha'][str(a)], top['diag_alpha'][str(a)]]
        for l in lams:
            gv = hl['by_rule'][cand][str(l)][str(a)]['gain']
            row.append(fmt_pct(gv, 1) if gv is not None else 'n/a')
            if gv is not None:
                values.append(gv)
        rows.append(row)
    m = data['meta']
    src = hp['source']
    cap = (f"Table HLP: Gain over the honest family by declaration ratio α, for a conventional self-declared flat tax set at the annual "
           f"burden the WDT puts on the average payer ({fmt_pct(avg['rate'], 3)}) and on the top payer ({fmt_pct(top['rate'], 3)}), against the "
           f"WDT best response under {cand}. Burdens are the wealth-weighted stock rates of RATES scenario {src['scenario']}, read from "
           f"the RATES JSON. Conventional: no audits modelled. WDT: best response over every strategy that deviates at exactly that α, a "
           f"lower bound. α = 0 is undefined for the WDT (zero declared price). T = {m['params']['T']}, G = {m['params']['G']}.")
    return {'md': md_table(heads, rows, col_fmt=['center'] * len(heads)) + '\n\n' + cap, 'values': values}


BUILDERS.update({'RPL': build_RPL, 'ARC': build_ARC, 'BES': build_BES, 'RSP': build_RSP, 'LCD': build_LCD,
                 'BAND': build_BAND, 'HLP': build_HLP})
'''

_OLD_RIS_C = r'''def build_RIS(data: dict, p: dict) -> dict:
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
'''

_NEW_RIS_C = r'''def build_RIS(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    srch = get_key(data, 'p5.search')
    lams = get_key(data, 'p5.lambda_vals')
    rule = _chain(p, data)[-1]
    rs = get_key(data, 'p3_reset_sensitivity')
    cycles = list(srch[f'{rule}|{lams[0]}']['best_by_cycle'])
    fig, axs = plt.subplots(1, 2, figsize=FIG_PAIR)
    ser = {'lambda': lams}
    for c, col in zip(cycles, RULE_COLOURS + [C_CONV]):
        y = [srch[f'{rule}|{l}']['best_by_cycle'][c]['gain'] for l in lams]
        ser[f'best_cycle_{c}'] = y
        axs[0].plot(lams, y, marker='o', color=col, label=_lab_reset(c))
    axs[0].set_xticks(lams)
    _pct_axis(axs[0], 'x')
    _pct_axis(axs[0], 'y', 1)
    axs[0].set_xlabel('Verification hazard λ')
    axs[0].set_ylabel('Best-response gain over honest family')
    axs[0].set_title(f'Best response by reset cycle ({rule})')
    axs[0].legend(title='Voluntary reset', fontsize=8)
    ivs = list(rs)
    ad = sorted(float(a) for a in rs[ivs[0]])
    for iv, col in zip(ivs, RULE_COLOURS + [C_CONV]):
        y = [rs[iv][str(b)]['gain'] for b in ad]
        ser[f'reset_{iv}'] = y
        axs[1].plot(ad, y, marker='o', color=col, label=_lab_reset(iv))
    axs[1].axhline(0.0, color=C_ANNOTATION, lw=0.8)
    _pct_axis(axs[1], 'y', 1)
    axs[1].set_xlabel('α_D (Route D declaration ratio)')
    axs[1].set_ylabel('Family gain over honest')
    axs[1].set_title('Route D understatement by reset cycle (α_C = 1, λ = 0)')
    axs[1].legend(title='Voluntary reset', fontsize=8)
    path = save_fig(fig, _OUT / f"val_fig_RIS_{PAIRS['RIS']['slug']}.png")
    return {'path': path, 'series': ser}
'''

_BLOCK_C = r'''# ── S5 (Work Order): replay, archetypes, breakeven, rho, lambda grid, V0 bands, HLC pair, voluntary reset ───────────────────
# One figure per table in 5_6_VALGEN_tables.py, same JSON keys. A section the core skipped returns {'path': None, 'series': {}}.

def _skipped(d) -> bool:
    return (not d) or (isinstance(d, dict) and bool(d.get('skipped')))


def _no_fig(pid: str, why: str) -> dict:
    print(f'  Figure {pid} not built: {why}')
    return {'path': None, 'series': {}}


def _split_key(key: str):
    """'rule|lambda' -> (rule, float lambda). Rule keys contain '/' but never '|'."""
    rule, lam = key.rsplit('|', 1)
    return rule, float(lam)


def _nums(v):
    """The numbers of a list, None dropped (what a table prints is what the series must hold)."""
    return [x for x in v if x is not None]


_MODE_LABEL = {'sale': 'Sale', 'lien': 'Lien', 'income': 'Income'}
_MODE_COL = {'sale': C_ANNOTATION, 'lien': C_WDT, 'income': C_UNDER[2]}


# ── RPL JST replay ───────────────────────────────────────────────────────────

def build_RPL(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    rp = data.get('replay')
    if _skipped(rp):
        return _no_fig('RPL', 'the JST replay was skipped')
    isos = list(rp['countries'])
    fig, axs = plt.subplots(len(isos), 2, figsize=(FIG_PAIR[0], FIG_PAIR[1] * len(isos)), squeeze=False)
    ser = {}
    th = get_key(data, 'p5.thresholds')
    for ri, iso in enumerate(isos):
        c = rp['countries'][iso]
        ax, bx = axs[ri]
        keys = list(c['summary'])
        for ki, key in enumerate(keys):
            rule, lam = _split_key(key)
            col = C_WDT if ki >= len(keys) // 2 else C_WDT_BASE
            mk = 'o' if lam == 0.0 else 's'
            st = [r['start'] for r in c['rows']]
            gn = [r['cells'][key]['gain'] for r in c['rows']]
            cont = [r['contiguous'] for r in c['rows']]
            ser[f'{iso}|{key}|start'] = st
            ser[f'{iso}|{key}|gain'] = gn
            ax.scatter([s for s, k in zip(st, cont) if k], [g for g, k in zip(gn, cont) if k], marker=mk, s=26, color=col,
                       label=f'{rule}, λ = {lam:.0%}')
            ax.scatter([s for s, k in zip(st, cont) if not k], [g for g, k in zip(gn, cont) if not k], marker=mk, s=26,
                       facecolors='none', edgecolors=col)
            sm = c['summary'][key]
            for nm, ls in (('full_loop', ':'), ('contiguous', '--')):
                if sm[nm] is not None:
                    ax.axhline(sm[nm]['gain_median'], color=col, ls=ls, lw=0.9, alpha=0.8)
                    ser[f'{iso}|{key}|{nm}|median'] = [sm[nm]['gain_median']]
                    ser[f'{iso}|{key}|{nm}|max'] = [sm[nm]['gain_max']]
        ax.axhline(th['brg_tol'], color=C_ANNOTATION, ls='-.', lw=1.0)
        _pct_axis(ax, 'y', 1)
        ax.set_xlabel('Start year of the loop window')
        ax.set_ylabel('Best-response gain over honest family')
        ax.set_title(f'{iso}: gain by window (hollow: window repeats years; dotted: full-loop median; dashed: contiguous median)', fontsize=8)
        ax.legend(fontsize=7)
        w = 0.2
        x = np.arange(len(keys))
        for j, (test, nm, colr, lab) in enumerate((('BRG', 'full_loop', C_WDT, 'BRG, full loop'),
                                                    ('BRG', 'contiguous', C_WDT_BASE, 'BRG, contiguous'),
                                                    ('SST', 'full_loop', C_DARK, 'SST, full loop'),
                                                    ('SST', 'contiguous', C_ANNOTATION, 'SST, contiguous'))):
            vals = []
            for key in keys:
                s = c['summary'][key][nm]
                vals.append(0.0 if s is None else s[f'{test}_pass_share'])
                if s is not None:
                    ser.setdefault(f'{iso}|{test}|{nm}|share', []).append(s[f'{test}_pass_share'])
            bx.bar(x + (j - 1.5) * w, vals, w, color=colr, label=lab)
        bx.set_xticks(x)
        bx.set_xticklabels([f"{_split_key(k)[0].split('/')[0]}\nλ = {_split_key(k)[1]:.0%}" for k in keys], fontsize=8)
        _pct_axis(bx, 'y', 0)
        bx.set_ylim(0, 1.05)
        bx.set_ylabel('Share of windows passing')
        bx.set_title(f'{iso}: BRG and SST pass shares', fontsize=9)
        bx.legend(fontsize=7, ncol=2)
    fig.text(0.5, 0.005, 'Real JST capital-return path, wrapped; windows overlap and are not independent draws. Strategy search is a lower bound.',
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_RPL_{PAIRS['RPL']['slug']}.png")
    return {'path': path, 'series': ser}


# ── ARC archetypes ───────────────────────────────────────────────────────────

def _arc_data(data: dict):
    arch = (data.get('p6') or {}).get('archetypes')
    if not arch:
        return None, None, None
    first = next(iter(arch.values()))
    modes = list(first['modes'])
    lams = sorted({float(k) for k in first['modes'][modes[0]]['best']})
    return arch, modes, lams


def build_ARC(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    arch, modes, lams = _arc_data(data)
    if arch is None:
        return _no_fig('ARC', 'no archetypes in the JSON')
    names = list(arch)
    x = np.arange(len(names))
    w = 0.8 / len(modes)
    fig, axs = plt.subplots(1, 3, figsize=FIG_PAIR_XW)
    ser = {}
    for mi, mode in enumerate(modes):
        off = (mi - (len(modes) - 1) / 2) * w
        col = _MODE_COL.get(mode, C_DARK)
        for l in lams:
            ser[f'gain_{mode}_lam{l}'] = [arch[n]['modes'][mode]['best'][str(l)]['gain'] for n in names]
        ser[f'TW_{mode}'] = [arch[n]['modes'][mode]['TW'] for n in names]
        ser[f'PV_{mode}'] = [arch[n]['modes'][mode]['PV'] for n in names]
        ser[f'income_{mode}'] = [arch[n]['modes'][mode]['income_paid'] for n in names]
        lb = max(lams)
        axs[0].bar(x + off, ser[f'gain_{mode}_lam{lb}'], w, color=col, label=f'{_MODE_LABEL.get(mode, mode)}, λ = {lb:.0%}')
        for l in lams:
            if l != lb:
                axs[0].scatter(x + off, ser[f'gain_{mode}_lam{l}'], marker='v', s=26, color=C_DARK, zorder=3)
        axs[1].bar(x + off, ser[f'TW_{mode}'], w, color=col, label=_MODE_LABEL.get(mode, mode))
        axs[2].bar(x + off, ser[f'PV_{mode}'], w, color=col, label=_MODE_LABEL.get(mode, mode))
        pos = [(xx, v) for xx, v in zip(x + off, ser[f'income_{mode}']) if v > 0.0]
        if pos:
            axs[2].scatter([a for a, _ in pos], [b for _, b in pos], marker='D', s=30, color=C_DARK, zorder=3)
    th = get_key(data, 'p5.thresholds')
    axs[0].axhline(th['brg_tol'], color=C_ANNOTATION, ls=':')
    _pct_axis(axs[0], 'y', 1)
    axs[0].set_ylabel('Best-response gain over honest family')
    axs[0].set_title('Best response (triangles: λ = 0)')
    axs[1].set_yscale('log')
    axs[1].set_ylabel('Honest terminal wealth (£m, log scale)')
    axs[1].set_title('Honest terminal wealth')
    axs[2].set_yscale('log')
    axs[2].set_ylabel("PV of the state's receipts (£m, log scale)")
    axs[2].set_title('State PV (diamonds: income paid)')
    for ax in axs:
        ax.set_xticks(x)
        ax.set_xticklabels([arch[n]['label'] for n in names], fontsize=7, rotation=20, ha='right')
        ax.legend(fontsize=7)
    path = save_fig(fig, _OUT / f"val_fig_ARC_{PAIRS['ARC']['slug']}.png")
    return {'path': path, 'series': ser}


# ── BES breakeven deferral spread ────────────────────────────────────────────

def build_BES(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    apply_style()
    arch, _modes, _lams = _arc_data(data)
    if arch is None:
        return _no_fig('BES', 'no archetypes in the JSON')
    rb = p.get('route_b') or {}
    toml_sp = rb.get('deferral_spread')
    names = list(arch)
    be = [arch[n]['breakeven_spread'] for n in names]
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    x = np.arange(len(names))
    ax.bar([i for i, b in zip(x, be) if b is not None], _nums(be), color=C_WDT)
    for i, b in zip(x, be):
        if b is None:
            ax.text(i, 0, 'not bracketed', rotation=90, ha='center', va='bottom', fontsize=8, color=C_ANNOTATION)
    ser = {'breakeven': _nums(be)}
    if toml_sp is not None:
        ax.axhline(toml_sp, color=C_CONV, ls='--', lw=1.2)
        ax.text(-0.45, toml_sp, 'placeholder spread', color=C_CONV, va='bottom', ha='left', fontsize=9)
        ser['toml_spread'] = [toml_sp] * sum(1 for b in be if b is not None) or [toml_sp]
    ax.axhline(0.0, color=C_ANNOTATION, lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([arch[n]['label'] for n in names], fontsize=8)
    _pct_axis(ax, 'y', 1)
    ax.set_ylabel('Breakeven deferral spread over the sovereign real rate')
    fig.text(0.5, 0.005, "Spread at which the PV of the state's receipts under the lien equals its PV under sale; above it the lien is worth more to the state.",
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_BES_{PAIRS['BES']['slug']}.png")
    return {'path': path, 'series': ser}


# ── RSP rho and the SPT sensitivity ──────────────────────────────────────────

def _rsp_grid(data: dict, p: dict):
    vg = p['val_gen']
    lams = [0.0, vg['lambda_base']]
    rules = list(vg['headline_rules'])
    srch = get_key(data, 'p5.search')
    spt = get_key(data, 'rho.spt_by_rho')
    rho_keys = sorted(next(iter(spt.values())), key=float)
    cells = []
    for rule in rules:
        for lam in lams:
            k = f'{rule}|{lam}'
            cells.append({'rule': rule, 'lam': lam, 'sst': srch[k]['n_conflict_sst'], 'sst_ok': srch[k]['SST_pass'],
                          'spt': [(float(r), spt[k][r]['n_conflict'], spt[k][r]['pass']) for r in rho_keys]})
    return cells, [float(r) for r in rho_keys]


def build_RSP(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    apply_style(grid=False)
    cells, rhos = _rsp_grid(data, p)
    V = np.array([[c['sst']] + [n for _r, n, _ok in c['spt']] for c in cells])
    OK = np.array([[c['sst_ok']] + [ok for _r, _n, ok in c['spt']] for c in cells])
    th = get_key(data, 'p5.thresholds')
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    ax.imshow(OK.astype(int), cmap=ListedColormap([C_FAIL, C_PASS]), vmin=0, vmax=1, aspect='auto')
    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            ax.text(j, i, str(int(V[i, j])), ha='center', va='center', fontsize=10, color=C_DARK)
    ax.set_xticks(range(V.shape[1]))
    ax.set_xticklabels(['SST\n(primary)'] + [f'SPT\nρ = {r:.1%}' for r in rhos], fontsize=9)
    ax.set_yticks(range(V.shape[0]))
    ax.set_yticklabels([f"{c['rule']}, λ = {c['lam']:.0%}" for c in cells], fontsize=8)
    ax.set_title(f"Gaining strategies outside ±{th['state_tol']:.1%} on the state (0 = pass)")
    ser = {'sst_conflicts': [int(v) for v in V[:, 0]]}
    for j, r in enumerate(rhos, start=1):
        ser[f'spt_conflicts_rho_{r}'] = [int(v) for v in V[:, j]]
    path = save_fig(fig, _OUT / f"val_fig_RSP_{PAIRS['RSP']['slug']}.png")
    return {'path': path, 'series': ser}


# ── LCD lambda_C x lambda_D ──────────────────────────────────────────────────

def build_LCD(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    apply_style(grid=False)
    g = get_key(data, 'p3_lambda_grid')
    lc, ld = g['lambda_C'], g['lambda_D']
    cells = g['cells']
    Z = np.array([[cells[f'{a}|{b}']['gain'] for b in ld] for a in lc])
    fig, ax = plt.subplots(figsize=FIG_SINGLE_W)
    im = ax.imshow(Z, cmap=CMAP_GAIN, aspect='auto', origin='lower', vmin=0.0)
    for i, a in enumerate(lc):
        for j, b in enumerate(ld):
            c = cells[f'{a}|{b}']
            ax.text(j, i, f"{c['gain']:.1%}", ha='center', va='center', fontsize=9, color='white' if c['gain'] > 0.6 * Z.max() else C_DARK)
            if not c['BRG']:
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec=C_DARK, lw=2))
    ax.set_xticks(range(len(ld)))
    ax.set_xticklabels([f'{b:.0%}' for b in ld])
    ax.set_yticks(range(len(lc)))
    ax.set_yticklabels([f'{a:.0%}' for a in lc])
    ax.set_xlabel('λ_D (Route D corrective-auction hazard)')
    ax.set_ylabel('λ_C (Route C verification hazard)')
    _pct_cbar(fig.colorbar(ax.images[0], ax=ax, label='Best-response gain'))
    fig.text(0.5, 0.005, f"Rule set {g['rule']}. Outlined cells fail BRG. Best of the strategy library: a lower bound.",
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_LCD_{PAIRS['LCD']['slug']}.png")
    return {'path': path, 'series': {'gain': Z.flatten().tolist()}}


# ── BAND V0 sweep across the RATES revenue bands ─────────────────────────────

def build_BAND(data: dict, p: dict) -> dict:
    import matplotlib.pyplot as plt
    apply_style()
    v = get_key(data, 'v0_sweep')
    bands, rules, lams, cells = v['bands'], v['rules'], v['lambda_vals'], v['cells']
    th = get_key(data, 'p5.thresholds')
    fig, axs = plt.subplots(1, 2, figsize=FIG_PAIR)
    ser = {'v0': bands}
    for ri, rule in enumerate(rules):
        col = C_WDT_BASE if ri == 0 else C_WDT
        for l in lams:
            y = [cells[f'{b}|{rule}|{l}']['gain'] for b in bands]
            ser[f'gain_{rule}_{l}'] = y
            axs[0].plot(bands, y, marker='o' if l == lams[0] else 's', ms=4, color=col, ls='-' if l == lams[0] else '--',
                        label=f'{rule}, λ = {l:.0%}')
        d = [cells[f'{b}|{rule}|{lams[0]}']['drag'] for b in bands]
        ser[f'drag_{rule}'] = d
        axs[1].plot(bands, d, marker='o', ms=4, color=col, label=rule)
    axs[0].axhline(th['brg_tol'], color=C_ANNOTATION, ls=':')
    for ax in axs:
        ax.set_xscale('log')
        ax.set_xlabel('Launch wealth V0 (£m, log scale)')
        _pct_axis(ax, 'y', 1)
        ax.legend(fontsize=8)
    axs[0].set_ylabel('Best-response gain over honest family')
    axs[0].set_title('Best response by launch wealth')
    axs[1].set_ylabel('Honest family tax drag (share of no-tax wealth)')
    axs[1].set_title('Honest tax drag by launch wealth')
    fig.text(0.5, 0.005, 'V0 = RATES revenue bands; route shares at the baseline mix. Dotted: BRG threshold (placeholder).',
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_BAND_{PAIRS['BAND']['slug']}.png")
    return {'path': path, 'series': ser}


# ── HLP headline contrast: the pair (average payer, top payer) ───────────────

def build_HLP(data: dict, p: dict) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter
    apply_style()
    hp = data['p5'].get('hlc_pair')
    if _skipped(hp):
        return _no_fig('HLP', (hp.get('reason') if isinstance(hp, dict) else None) or 'no RATES burdens in the JSON')
    hl = get_key(data, 'p5.headline')
    cand = hl['rules'][-1]
    lam_b = p['val_gen']['lambda_base']
    lams = [0.0, lam_b]
    alphas = [a for a in sorted(hl['alphas'], reverse=True) if a <= 1.0]
    fig, axs = plt.subplots(1, 2, figsize=FIG_PAIR, sharey=True)
    ser = {'alpha': alphas}
    wdt = {l: [hl['by_rule'][cand][str(l)][str(a)]['gain'] for a in alphas] for l in lams}
    for l in lams:
        ser[f'wdt_{cand}_lam{l}'] = _nums(wdt[l])
    for ax, lab, ttl in ((axs[0], 'average', 'Average payer'), (axs[1], 'top', 'Top payer')):
        b = hp['burdens'][lab]
        y = [b['diag_alpha'][str(a)] for a in alphas]
        ser[f'conventional_{lab}'] = y
        ax.plot(alphas, y, color=C_CONV, marker='o', label=f"Conventional tax at {b['rate']:.3%} a year")
        for l, mk, ls in zip(lams, ('o', 's'), ('-', '--')):
            ax.plot(alphas, np.array([np.nan if x is None else x for x in wdt[l]], dtype=float), color=C_WDT, marker=mk, ls=ls, ms=4,
                    label=f'WDT {cand}, λ = {l:.0%}')
        ax.set_xlim(1.0, 0.0)
        ax.set_xlabel('Declaration ratio α (declared / true value)')
        ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        ax.set_title(ttl)
        ax.legend(fontsize=8)
    axs[0].set_ylabel('Gain over honest family (share of its terminal wealth)')
    fig.text(0.5, 0.005, 'Burden = wealth-weighted stock rate from the RATES JSON. Conventional tax: no audits modelled. WDT best response is a lower bound; α = 0 undefined for the WDT.',
             ha='center', fontsize=8, color=C_ANNOTATION)
    path = save_fig(fig, _OUT / f"val_fig_HLP_{PAIRS['HLP']['slug']}.png")
    return {'path': path, 'series': ser}


BUILDERS.update({'RPL': build_RPL, 'ARC': build_ARC, 'BES': build_BES, 'RSP': build_RSP, 'LCD': build_LCD,
                 'BAND': build_BAND, 'HLP': build_HLP})
'''

_NAMES = r'''[names.val.RPL]
kind = "output"
name = "JST replay"
legacy = ""
note = ""
[names.val.ARC]
kind = "output"
name = "Archetypes"
legacy = ""
note = ""
[names.val.BES]
kind = "output"
name = "Breakeven deferral spread"
legacy = ""
note = ""
[names.val.RSP]
kind = "output"
name = "Rho and SPT sensitivity"
legacy = ""
note = ""
[names.val.LCD]
kind = "output"
name = "Lambda C by lambda D grid"
legacy = ""
note = ""
[names.val.BAND]
kind = "output"
name = "V0 band sweep"
legacy = ""
note = ""
[names.val.HLP]
kind = "output"
name = "Headline contrast pair"
legacy = ""
note = ""
'''

SPEC = {
    '5_6_VALGEN_tables.py': [
        Replace("'RIS': {'json': ['p3_reset_sensitivity'], 'slug': 'reset_sensitivity', 'title': 'Route D reset sensitivity',",
                "'RIS': {'json': ['p5.search', 'p3_reset_sensitivity'], 'slug': 'reset_sensitivity', 'title': 'Voluntary Route D reset',",
                label='PAIRS: RIS reads p5.search too', done="'title': 'Voluntary Route D reset',"),
        InsertAfter("'label': 'Table LNS'},\n", _PAIRS_T, label='PAIRS: seven new tables', done="'label': 'Table RPL'"),
        Replace(_OLD_RIS_T, _NEW_RIS_T, label='build_RIS: voluntary reset', done='(a) Best response by reset cycle and'),
        InsertBefore('def main(only=None) -> None:\n', _BLOCK_T + '\n\n', label='tables block', done='def build_RPL(data: dict, p: dict) -> dict:'),
    ],
    '5_7_VALGEN_charts.py': [
        Replace("'RIS': {'json': ['p3_reset_sensitivity'], 'slug': 'reset_sensitivity', 'title': 'Route D reset sensitivity',",
                "'RIS': {'json': ['p5.search', 'p3_reset_sensitivity'], 'slug': 'reset_sensitivity', 'title': 'Voluntary Route D reset',",
                label='PAIRS: RIS reads p5.search too', done="'title': 'Voluntary Route D reset',"),
        InsertAfter("'label': 'Figure LNS'},\n", _PAIRS_C, label='PAIRS: seven new figures', done="'label': 'Figure RPL'"),
        Replace(_OLD_RIS_C, _NEW_RIS_C, label='build_RIS: voluntary reset', done="axs[0].set_title(f'Best response by reset cycle ({rule})')"),
        InsertBefore('def main(only=None) -> None:\n', _BLOCK_C + '\n\n', label='charts block', done='def build_RPL(data: dict, p: dict) -> dict:'),
    ],
    'WDT_Params.toml': [
        Replace('name = "Reset interval sensitivity"', 'name = "Voluntary reset sensitivity"', label='names.val.RIS',
                done='name = "Voluntary reset sensitivity"'),
        InsertAfter('name = "LIFE holding-period sweep"\nlegacy = "C.8"\nnote = ""\n', _NAMES, label='names.val: seven new outputs',
                    done='[names.val.RPL]'),
    ],
}

if __name__ == '__main__':
    sys.exit(patch_cli(SPEC, NAME, __doc__))
