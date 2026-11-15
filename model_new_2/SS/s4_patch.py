"""
s4_patch.py - work order S4 (RATES presentation): patches 8_2_RATES_tables.py and 8_3_RATES_charts.py in place.

Run from the RATES folder:   python s4_patch.py
Every replacement must match exactly once or the script stops before writing that file. Backups: *.bak.
Touches only 8_2_RATES_tables.py and 8_3_RATES_charts.py. No TOML edits, no core imports.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sub(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit(f'[{label}] anchor matched {n} times (expected 1); nothing written for this file.')
    return text.replace(old, new)


def rsub(text, pattern, new, label):
    out, n = re.subn(pattern, lambda m: new, text, flags=re.S)
    if n != 1:
        sys.exit(f'[{label}] regex matched {n} times (expected 1); nothing written for this file.')
    return out


CONTRACT = '''
JSON contract with S2 (rates_core.py) for the new outputs. Absent keys print "skipped" or show a dash; nothing here simulates.
  data['archetype_sweep'] = {'scenario': name, 'mode': index mode,
      'rows': [{'key', 'label', 'V0_m' (£m), 'shares': {'A','B','C','D'} (fractions),
                'censored_share': share of windows whose fund never fills,
                'medians': {'cov_ref', 'stock_rate', 'gain_rate', 'fill_year', 'income_paid_cum_gdp', 'shortfall_share'}}]}
      cov_ref / fill_year: medians over windows that fill. stock_rate / gain_rate: realised WDT over wealth / over accrued return.
      income_paid_cum_gdp: cumulative external income paid to WDT over the window, in years of GDP.
      shortfall_share: share of the liability met by selling holdings when income falls short (income mode).
  Route B scenarios, per launch-wealth band i (all-window medians, as the other *_band{i} columns):
      income_paid_cum_gdp_band{i}   cumulative income paid over the window, in years of GDP
      income_short_share_band{i}    share of liability met by selling holdings
  headline.overall['rel_cov_never_share']   share of windows that fill in which relief never reaches expenditure
'''

NEW_LIST = '''  20 consumption  spending covered and burden under each consumption assumption
  21 threshold_beneficiaries  who gains from the tax-free threshold, and by how much
  22 net_position  net position by launch-wealth band while relief is paid (22b, table only: the budget behind it)
  23 representativeness  slices of the history by regime
  24 bootstrap  how many independent windows there really are
  25 levy_sensitivity  how much of the headline rests on the CORP levy
  26 effective_windows  windows per country at T = 100: full loop, contiguous, seam-crossing, repeat years
  27 decade_relief  relief and expenditure every tenth year
  28 route_b_fund  fund and receivable by Route B treatment
  29 route_b_receipts  Route B receipts by launch-wealth band
  30 route_b_wealth  family wealth and cumulative income paid by band, reported separately
  31 archetype_sweep  revenue, burden and fund outcomes by route-mix archetype
'''

# ───────────────────────── 8_2_RATES_tables.py ─────────────────────────
p2 = HERE / '8_2_RATES_tables.py'
def read_lf(path):
    raw = path.read_bytes().decode('utf-8')
    return raw.replace('\r\n', '\n'), ('\r\n' in raw)


def write_nl(path, text, crlf):
    path.write_bytes((text.replace('\n', '\r\n') if crlf else text).encode('utf-8'))


t, crlf2 = read_lf(p2)
orig2 = t

t = sub(t, 'Tables 13-16 present the headline:', 'Tables 13-31 present the headline and what is built on it:', '8_2 heading')
t = sub(t, '  19 threshold_by_schedule  the tax-free thresholds under each WDT rate schedule, and what a person saves at example incomes\n',
        '  19 threshold_by_schedule  the tax-free thresholds under each WDT rate schedule, and what a person saves at example incomes\n'
        + NEW_LIST + CONTRACT, '8_2 docstring')

# c_ref was hardcoded in the Table 20 caption
t = sub(t, 'def t20_consumption(data, p):',
        '''def _c_ref_text(p, sc):
    """'c_ref = 1%' for the scenario's ladder (from [rates.schedules]); generic wording for a logistic, which has no c_ref."""
    sched = (p['rates']['schedules'] or {}).get(sc['cfg'].get('schedule'))
    return f"c_ref = {fmt_pct0(sched['c_ref'])}" if sched else 'its reference consumption'


def t20_consumption(data, p):''', '8_2 t20 helper')
t = sub(t, "    ref = _scen(data, fg['consumption'][0])\n    d = MdDoc()",
        "    ref = _scen(data, fg['consumption'][0])\n    c_ref_txt = _c_ref_text(p, ref)\n    d = MdDoc()", '8_2 t20 ref')
t = sub(t, 'calibrated for c_ref = {fmt_pct0(0.01)}, so', 'calibrated for {c_ref_txt}, so', '8_2 t20 caption')

# T27: share of windows that never reach expenditure
t = sub(t, "    rows.append(['**Windows that fill (of all)**',",
        """    never = lambda h: fmt_pct(h['overall'].get('rel_cov_never_share'), 0) if h else DASH
    rows.append(['**Share of filling windows where relief never reaches expenditure**', never(full), never(cont), '', '', ''])
    rows.append(['**Windows that fill (of all)**',""", '8_2 t27 row')
t = sub(t, 'windows where it never does are not in that median.")',
        'windows where it never does are not in that median, so the next row gives their share.")', '8_2 t27 caption')

# T30: cumulative income paid, reported beside (never folded into) family wealth
t = sub(t, """        return heads, gets
    cap = ("Table 30:""",
        """        if 'income' in have:
            heads += ['Cumulative income paid to WDT, income', 'Shortfall sold from holdings, income']
            gets += [lambda meds, i: fmt_pct(_med(meds['income'], f'income_paid_cum_gdp_band{i}', True), 2),
                     lambda meds, i: fmt_pct(_med(meds['income'], f'income_short_share_band{i}', True), 0)]
        return heads, gets
    cap = ("Table 30:""", '8_2 t30 cols')
t = sub(t, 'that gap is not a welfare gain until the income paid is set against it.")',
        'that gap is not a welfare gain until the income paid is set against it. Cumulative income paid is the sum over the window of the '
        'external income handed to WDT, in years of GDP; the shortfall column is the share of liability met by selling holdings when income '
        'falls short. Neither is netted against family wealth. A dash means the core has not yet written the column.")', '8_2 t30 caption')

# T31: archetype sweep
t = sub(t, "# (number, slug, function): the numbers and slugs must match FIGURES in 8_3_RATES_charts.py",
        '''# ─────────────────────────────────────────────────────────────
# T31  archetype sweep
# ─────────────────────────────────────────────────────────────

def _arch_block(data):
    blk = data.get('archetype_sweep')
    if not blk or not blk.get('rows'):
        print("  skipped: no 'archetype_sweep' block in rates_data.json (written by rates_core; contract in this file's docstring)")
        return None
    return blk


def t31_archetype_sweep(data, p):
    blk = _arch_block(data)
    if blk is None:
        return None
    rows = []
    for r in blk['rows']:
        m = r.get('medians') or {}
        s = r['shares']
        rows.append([f"**{r['label']}**", f"£{r['V0_m']:g}m", ' / '.join(fmt_pct0(s[k]) for k in 'ABCD'),
                     _x(m, 'stock_rate'), _x(m, 'gain_rate', fmt_pct1), _x(m, 'cov_ref', fmt_pct1),
                     fmt_pct(r.get('censored_share'), 0), fmt_f0(m.get('fill_year')),
                     _x(m, 'income_paid_cum_gdp', fmt_pct), _x(m, 'shortfall_share', fmt_pct0)])
    d = MdDoc()
    d.table(['Archetype', 'Entry wealth', 'Route mix A / B / C / D', 'Stock rate', 'Gain rate', 'Spending covered', 'Never fills',
             'Fill year', 'Cumulative income paid', 'Shortfall sold from holdings'], rows,
            col_fmt=[LEFT, RIGHT, RIGHT] + [RIGHT] * 7)
    d.caption(f"Table 31: Revenue, burden and fund outcomes by route-mix archetype, scenario '{blk.get('scenario', '')}', index = {blk.get('mode', '')}. "
              f"Route mix is the share of entry wealth on Route A (listed, annual cash), B (property, deferred or paid from income), C (self-declared, "
              f"settled in kind) and D (appraised, cash). Stock and gain rates are realised WDT over wealth and over accrued return. Spending covered "
              f"and fill year are medians over windows in which the fund fills; 'never fills' is the share of all windows. Cumulative income paid and the "
              f"shortfall met by selling holdings are income-mode quantities and are reported apart from wealth. Mixes, entry wealth and external income are "
              f"placeholders in [archetypes.*] and [income.by_archetype], to be replaced by a joint WAS cut.")
    return d


# (number, slug, function): the numbers and slugs must match FIGURES in 8_3_RATES_charts.py''', '8_2 t31')
t = sub(t, "    (30, 'route_b_wealth', t30_route_b_wealth)\n]",
        "    (30, 'route_b_wealth', t30_route_b_wealth),\n    (31, 'archetype_sweep', t31_archetype_sweep),\n]", '8_2 registry')

# ───────────────────────── 8_3_RATES_charts.py ─────────────────────────
p3 = HERE / '8_3_RATES_charts.py'
c, crlf3 = read_lf(p3)
orig3 = c

c = sub(c, 'Figures 13-16 present the headline:', 'Figures 13-31 present the headline and what is built on it:', '8_3 heading')
c = sub(c, '  19 threshold_by_schedule  the tax-free threshold under each WDT rate schedule, and the tax a person saves by income\n',
        '  19 threshold_by_schedule  the tax-free threshold under each WDT rate schedule, and the tax a person saves by income\n'
        + NEW_LIST + '  (the JSON contract for 30 and 31 is in the docstring of 8_2_RATES_tables.py)\n', '8_3 docstring')

c = sub(c, 'FIG_PAIR, FIG_PAIR_T, FIG_SINGLE, FIG_WIDE, FIG_TRIPLE, apply_style, save_fig)',
        'FIG_PAIR, FIG_PAIR_T, FIG_QUAD, FIG_SINGLE, FIG_TALL, FIG_WIDE, FIG_TRIPLE, apply_style, save_fig)', '8_3 imports')
c = sub(c, 'subplots(1, 2, figsize=(14, 8), sharey=True)', 'subplots(1, 2, figsize=FIG_QUAD, sharey=True)', '8_3 f13 figsize')
c = sub(c, 'fig, ax = _plt().subplots(figsize=(10, 8))', 'fig, ax = _plt().subplots(figsize=FIG_TALL)', '8_3 f18 figsize')
c = sub(c, 'fig, (a1, a2) = _plt().subplots(1, 2, figsize=(14, 6.5))', 'fig, (a1, a2) = _plt().subplots(1, 2, figsize=FIG_PAIR_T)', '8_3 f19 figsize')

NEW_F30_F31 = '''def f30_route_b_wealth(data, p):
    """Left: family wealth at window end by band and Route B treatment. Right: cumulative income paid (income mode), kept separate."""
    apply_style()
    names = _route_b_names(data, p)
    pick = {m: _default_of_mode(data, names, m) for m in ('sale', 'lien', 'income')}
    if not pick['sale'] or sum(bool(v) for v in pick.values()) < 2:
        print('  skipped figure 30: needs a sale scenario and one of lien / income in [rates.figures].route_b')
        return None
    mode = p['rates']['figures']['mode']
    labels = band_labels(data['scenarios'][pick['sale']]['calibration']['bands']['edges_gbp_m'])
    have = [m for m in ('sale', 'lien', 'income') if pick[m]]
    hs = {m: _hl(data['scenarios'][pick[m]], mode) for m in have}
    x = np.arange(len(labels))
    w = 0.8 / len(have)
    paid = np.array([_nan(_med(hs['income'], f'income_paid_cum_gdp_band{i}', True)) for i in range(len(labels))]) if 'income' in hs else None
    show_paid = paid is not None and not np.all(np.isnan(paid))
    fig, axs = _plt().subplots(1, 2 if show_paid else 1, figsize=FIG_PAIR if show_paid else FIG_WIDE, squeeze=False)
    ax = axs[0][0]
    for k, m in enumerate(have):
        ax.bar(x + (k - (len(have) - 1) / 2) * w, [_nan(_med(hs[m], f'wealth_gdp_end_band{i}', True)) for i in range(len(labels))], w,
               color=_MODE_COL[m], label=f'Family wealth, {m}')
    ax.set_xticks(x, [_wrap(l, 12) for l in labels], fontsize=7)
    ax.set_xlabel('Launch wealth band')
    ax.set_ylabel('Share of GDP at window end (median, all windows)')
    ax.set_title('Family wealth at window end')
    ax.legend(fontsize=8)
    _pct(ax, 'y', 1)
    if show_paid:
        a2 = axs[0][1]
        a2.bar(x, paid, color=_MODE_COL['income'])
        a2.set_xticks(x, [_wrap(l, 12) for l in labels], fontsize=7)
        a2.set_xlabel('Launch wealth band')
        a2.set_ylabel('Cumulative income paid to WDT, years of GDP (median, all windows)')
        a2.set_title('Income paid, income mode (not netted against wealth)')
        _pct(a2, 'y', 1)
    fig.suptitle(f'Route B: family wealth and income paid by launch-wealth band, index {mode}', fontsize=10)
    return save_fig(fig, _path(30, 'route_b_wealth'))


def f31_archetype_sweep(data, p):
    """Route mix (left), realised burden (middle), spending covered with the never-fills share (right), by archetype."""
    apply_style()
    blk = data.get('archetype_sweep')
    if not blk or not blk.get('rows'):
        print("  skipped figure 31: no 'archetype_sweep' block in rates_data.json")
        return None
    rows = blk['rows']
    x = np.arange(len(rows))
    labels = [_wrap(r['label'], 14) for r in rows]
    fig, (a1, a2, a3) = _plt().subplots(1, 3, figsize=FIG_TRIPLE)
    bottom = np.zeros(len(rows))
    for key, col in zip('ABCD', (C_SSM, C_LRR, C_TCM, C_SURPLUS)):
        v = np.array([_nan(r['shares'].get(key)) for r in rows])
        a1.bar(x, v, bottom=bottom, color=col, label=f'Route {key}')
        bottom += v
    a1.set_title('Route mix at entry')
    a1.legend(fontsize=7, loc='lower right')
    _pct(a1, 'y', 0)
    w = 0.38
    a2.bar(x - w / 2, [_nan((r.get('medians') or {}).get('stock_rate')) for r in rows], w, color=C_SSM, label='Stock rate (left axis)')
    a2.set_ylabel('Realised stock rate per year')
    _pct(a2, 'y', 1)
    a2b = a2.twinx()
    a2b.bar(x + w / 2, [_nan((r.get('medians') or {}).get('gain_rate')) for r in rows], w, color=C_TCM, label='Gain rate (right axis)')
    a2b.set_ylabel('Realised gain rate per year')
    _pct(a2b, 'y', 0)
    a2b.grid(False)
    a2.set_title('Burden (wealth-weighted)')
    a3.bar(x - w / 2, [_nan((r.get('medians') or {}).get('cov_ref')) for r in rows], w, color=C_LRR, label='Spending covered (median, filling windows)')
    a3.bar(x + w / 2, [_nan(r.get('censored_share')) for r in rows], w, color=C_BASELINE, label='Never fills (share of windows)')
    a3.set_title('Fund outcome')
    a3.legend(fontsize=7)
    _pct(a3, 'y', 0)
    for ax in (a1, a2, a3):
        ax.set_xticks(x, labels, fontsize=7)
    fig.suptitle(f"Route-mix archetypes, scenario '{blk.get('scenario', '')}', index {blk.get('mode', '')}")
    return save_fig(fig, _path(31, 'archetype_sweep'))


'''
c = rsub(c, r"def f30_route_b_wealth\(data, p\):.*?\n\n\n(?=# \(number, slug, function\))", NEW_F30_F31, '8_3 f30/f31')
c = sub(c, "    (30, 'route_b_wealth', f30_route_b_wealth),\n]",
        "    (30, 'route_b_wealth', f30_route_b_wealth),\n    (31, 'archetype_sweep', f31_archetype_sweep),\n]", '8_3 registry')

# write both only if every anchor matched
write_nl(p2.with_suffix('.py.bak'), orig2, crlf2)
write_nl(p3.with_suffix('.py.bak'), orig3, crlf3)
write_nl(p2, t, crlf2)
write_nl(p3, c, crlf3)
print('S4 patch applied to 8_2_RATES_tables.py and 8_3_RATES_charts.py (backups: *.py.bak)')
