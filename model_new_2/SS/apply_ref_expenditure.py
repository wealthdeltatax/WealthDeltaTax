"""
apply_ref_expenditure.py: put every revenue-like quantity in RATES tables/figures on ONE denominator,
fixed reference expenditure (the denominator of "spending covered" = cov_ref).

Presentation-layer change only. cov_ref = relief_gdp / exp_ref and exp_ref is a constant per scenario,
so x / exp_ref is exact for medians and quantiles: no core change, no re-run of rates_core.py.
Re-run 8_2_RATES_tables.py and 8_3_RATES_charts.py afterwards.

Usage (from the folder that holds 8_2_RATES_tables.py; wdt_core.py is looked up there and one level up):
    python apply_ref_expenditure.py             # dry run: checks every anchor, writes nothing
    python apply_ref_expenditure.py --write     # applies, keeps <file>.bak next to each file
    python apply_ref_expenditure.py --dir PATH  # folder to search

Every edit must match exactly once, or the script stops and writes NOTHING.

Deliberately NOT changed (pairs that must move together and need a decision): T17-T22b / F17-F19, F21, F22
(tax-replacement budget, defined in GDP shares and GBP bn), T23 / F23 (compares today's expenditure and revenue),
T2 (its job is to compare denominators), the base-multiple column of T8, and the CORP calibration sentence
(_levy_note: the levy is calibrated to corporation tax, 3.2% of GDP).
"""

import argparse
import re
import sys
from pathlib import Path

SP = lambda n: ' ' * n   # continuation-line indentation, spelled out to avoid miscounting

# ───────────────────────────── wdt_core.py ─────────────────────────────
CORE = [
(r'''    if all_windows and ov.get('medians_all'):
        return ov['medians_all']
    return ov['medians']
''',
r'''    if all_windows and ov.get('medians_all'):
        return ov['medians_all']
    return ov['medians']


def of_ref(gdp_share, exp_ref):
    """
    A quantity quoted as a share of GDP -> the same quantity as a share of the fixed reference expenditure
    (the denominator of 'spending covered', cov_ref). None-safe.
    Exact for medians and quantiles because exp_ref is one constant per scenario: of_ref(relief_gdp, exp_ref) == cov_ref.
    Use it for every revenue-like quantity shown in RATES tables and figures (relief, net receipts, components, levy).
    """
    return None if gdp_share is None else gdp_share / exp_ref
'''),
]

# ───────────────────────────── 8_2_RATES_tables.py ─────────────────────────────
TABLES = [
# docstring
(r'''Spending covered = relief paid after fund fill / fixed reference expenditure. Relief and coverage are medians over''',
 r'''Spending covered = relief paid after fund fill / fixed reference expenditure. Every revenue-like quantity in tables
1-10, 14, 20 and 25 (relief, net receipts, components, levy) is shown on that same denominator via wc.of_ref; tables
17-23 keep GDP shares by design (tax-replacement budget, regime comparison). Relief and coverage are medians over'''),
# helpers
(r'''def _x(m, key, f=fmt_pct):
    """Format medians[key], or a dash when it is missing / null."""
    v = m.get(key)
    return '—' if v is None else f(v)''',
 r'''def _x(m, key, f=fmt_pct):
    """Format medians[key], or a dash when it is missing / null."""
    v = m.get(key)
    return '—' if v is None else f(v)


def _e(sc):
    """Fixed reference expenditure / GDP of a scenario: the one denominator of 'spending covered'."""
    return sc['calibration']['exp_ref']


def _xr(m, key, e, f=fmt_pct):
    """Format medians[key] (a share of GDP) as a share of reference expenditure e, or a dash when missing."""
    v = m.get(key)
    return '—' if v is None else f(wc.of_ref(v, e))


def _band_r(d, e, f=fmt_pct):
    """'p10 / p50 / p90' of a dist_stats block in GDP shares, shown as shares of reference expenditure e."""
    return f"{f(d['p10'] / e)} / {f(d['p50'] / e)} / {f(d['p90'] / e)}"'''),

# ── T1
(r'''def t1_relief_by_country(data, p):
    sc, mode, h, _ = _ctx(data, p)
''',
 r'''def t1_relief_by_country(data, p):
    sc, mode, h, _ = _ctx(data, p)
    e = _e(sc)
'''),
(r'''b['windows'], b['uncensored'], _band(b['relief_gdp']),''',
 r'''b['windows'], b['uncensored'], _band_r(b['relief_gdp'], e),'''),
(r'''ov['windows'], ov['uncensored'], _band(ov['relief_gdp']),''',
 r'''ov['windows'], ov['uncensored'], _band_r(ov['relief_gdp'], e),'''),
(r'''d.table(['Country', 'Windows', 'Uncensored', 'Relief / GDP (p10 / median / p90)', 'Fail share'],''',
 r'''d.table(['Country', 'Windows', 'Uncensored', 'Spending covered (relief / reference expenditure; p10 / median / p90)', 'Fail share'],'''),
(r'''Table 1: Relief paid over the horizon after fund fill, as a share of GDP, by country.''',
 r'''Table 1: Spending covered by country (relief paid over the horizon after fund fill, over fixed reference expenditure of {fmt_pct1(e)} of GDP).'''),

# ── T3
(r'''rows.append([f"**{sc['label']}**", fmt_pct(a['tax_gdp_mean']), fmt_pct(a['heir_gdp_mean']),
                     fmt_pct(a['levy_gdp_mean']), fmt_pct(a['refund_gdp_mean']), fmt_pct(a['net_gdp_mean']),
                     fmt_pct(m['relief_gdp']), fmt_f2(a['drift'])])''',
 r'''e = _e(sc)
        rows.append([f"**{sc['label']}**", _xr(a, 'tax_gdp_mean', e), _xr(a, 'heir_gdp_mean', e),
                     _xr(a, 'levy_gdp_mean', e), _xr(a, 'refund_gdp_mean', e), _xr(a, 'net_gdp_mean', e),
                     _xr(m, 'relief_gdp', e), fmt_f2(a['drift'])])'''),
(r'''as a share of GDP by component, index = {mode}.''',
 r'''as a share of reference expenditure ({fmt_pct1(e)} of GDP) by component, index = {mode}.'''),

# ── T4
("fmt_pct(m['relief_gdp']),\n",
 "_xr(m, 'relief_gdp', _e(sc), fmt_pct1),\n"),
(r'''d.table(['Scenario', 'tau_0', 'k per £m', 'Relief / GDP',''',
 r'''d.table(['Scenario', 'tau_0', 'k per £m', 'Spending covered',''' ),
(r'''Table 4: Revenue against burden for tau_0 and k combinations, index = {mode}.''',
 r'''Table 4: Spending covered (relief / reference expenditure) against burden for tau_0 and k combinations, index = {mode}.'''),

# ── T5
(r'''lo, hi = p['rates']['run']['drift_band']
    rows = []
    for iso, b in sorted(h['by_country'].items()):''',
 r'''lo, hi = p['rates']['run']['drift_band']
    e = _e(sc)
    rows = []
    for iso, b in sorted(h['by_country'].items()):'''),
(r'''fmt_pct(st['relief_gdp_median'])])''',
 r'''fmt_pct1(wc.of_ref(st['relief_gdp_median'], e))])'''),
(r'''fmt_pct(ov['stable']['relief_gdp_median'])])''',
 r'''fmt_pct1(wc.of_ref(ov['stable']['relief_gdp_median'], e))])'''),
(r'''Relief / GDP, stable only''',
 r'''Spending covered, stable only'''),
(r'''{fmt_f2(hi)}]. {_desc(sc, mode)}.''',
 r'''{fmt_f2(hi)}]. Spending covered is relief over fixed reference expenditure ({fmt_pct1(e)} of GDP). {_desc(sc, mode)}.'''),

# ── T6
(r'''def t6_by_era(data, p):
    sc, mode, h, _ = _ctx(data, p)
''',
 r'''def t6_by_era(data, p):
    sc, mode, h, _ = _ctx(data, p)
    e = _e(sc)
'''),
(r'''fmt_f(b['fill_year']['p50'], '.0f'), _band(b['relief_gdp'])])''',
 r'''fmt_f(b['fill_year']['p50'], '.0f'), _band_r(b['relief_gdp'], e)])'''),
(r'''Relief / GDP (p10 / median / p90)'], rows, col_fmt=[LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT])''',
 r'''Spending covered (relief / reference expenditure; p10 / median / p90)'], rows, col_fmt=[LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT])'''),
(r'''Table 6: Fund outcomes by era of the window start year.''',
 r'''Table 6: Fund outcomes by era of the window start year. Spending covered is relief over fixed reference expenditure ({fmt_pct1(e)} of GDP).'''),

# ── T8 (net receipts column only; the base multiple is a ratio of GDP shares and is left alone)
(r'''def t8_closure(data, p):
    sc, mode, h, _ = _ctx(data, p)
''',
 r'''def t8_closure(data, p):
    sc, mode, h, _ = _ctx(data, p)
    e = _e(sc)
'''),
(r'''fmt_pct1(b['net_gdp_mean']['p50'])''', r'''fmt_pct1(wc.of_ref(b['net_gdp_mean']['p50'], e))'''),
(r'''fmt_pct1(ov['net_gdp_mean']['p50'])''', r'''fmt_pct1(wc.of_ref(ov['net_gdp_mean']['p50'], e))'''),
(r'''Net receipts / GDP (median)''', r'''Net receipts / reference expenditure (median)'''),
(r'''to replace it. {_desc(sc, mode)}.''',
 r'''to replace it (a ratio of GDP shares, so independent of the expenditure denominator). Net receipts are shown over fixed reference expenditure ({fmt_pct1(e)} of GDP). {_desc(sc, mode)}.'''),

# ── T9: drop the Relief / GDP column (redundant beside Spending covered); net receipts on reference expenditure
# one anchor spanning both lines: T20 has the same first line, but on one line with net_gdp_mean after it
("_x(m, 'cov_ref', fmt_pct1), _x(m, 'relief_gdp'),\n" + SP(21) + "_x(a, 'net_gdp_mean'),",
 "_x(m, 'cov_ref', fmt_pct1),\n" + SP(21) + "_xr(a, 'net_gdp_mean', _e(sc), fmt_pct1),"),
(r'''Spending covered (relief / reference expenditure)', 'Relief / GDP', 'Net WDT / GDP',''',
 r'''Spending covered (relief / reference expenditure)', 'Net receipts incl. levy / reference expenditure','''),
(r'''[RIGHT] * 9)
    d.caption(f'Table 9:''', r'''[RIGHT] * 8)
    d.caption(f'Table 9:'''),
(r'''GDP). Spending covered and relief are medians over windows in which the fund fills; the other ''',
 r'''GDP). Spending covered is a median over windows in which the fund fills; net receipts (including the CORP levy) are shown over the same expenditure; the other '''),

# ── T10
("_x(m, 'cov_ref', fmt_pct1), _x(a, 'net_gdp_mean'),\n" + SP(21) + "_x(m, 'relief_gdp'), _x(a, f'er_stock_{grp}'), _x(a, f'er_gain_{grp}', fmt_pct1)])",
 "_x(m, 'cov_ref', fmt_pct1), _xr(a, 'net_gdp_mean', _e(sc), fmt_pct1),\n" + SP(21) + "_x(a, f'er_stock_{grp}'), _x(a, f'er_gain_{grp}', fmt_pct1)])"),
(r'''Spending covered', 'Net WDT / GDP', 'Relief / GDP',''',
 r'''Spending covered', 'Net receipts incl. levy / reference expenditure','''),
("f'Gain rate ({grp})'],\n" + SP(12) + "rows, col_fmt=[LEFT] + [RIGHT] * 7)",
 "f'Gain rate ({grp})'],\n" + SP(12) + "rows, col_fmt=[LEFT] + [RIGHT] * 6)"),
(r'''and relief are medians over windows in which the fund fills; the other columns are medians over all ''',
 r'''is a median over windows in which the fund fills; net receipts are shown over the same reference expenditure; the other columns are medians over all '''),

# ── T14
(r"""'Individual WDT / GDP',""", r"""'Individual WDT / reference expenditure',"""),
(r'''_x(a, 'wdt_gdp_mean'),''', r'''_xr(a, 'wdt_gdp_mean', _e(sc), fmt_pct1),'''),
(r'''Individual WDT / GDP, burden and drift ''', r'''Individual WDT / reference expenditure, burden and drift '''),

# ── T20
(r'''_x(m, 'cov_ref', fmt_pct1), _x(m, 'relief_gdp'), _x(a, 'net_gdp_mean'),''',
 r'''_x(m, 'cov_ref', fmt_pct1), _xr(a, 'net_gdp_mean', _e(sc), fmt_pct1),'''),
("'Relief / GDP', 'Net WDT / GDP', f'Stock rate ({gl})', f'Stock rate ({tl})', f'Gain rate ({gl})',\n"
 + SP(13) + "f'Gain rate ({tl})', 'Drift (median)', 'Censored'],\n" + SP(12) + "rows, col_fmt=[LEFT] + [RIGHT] * 12)",
 "'Net receipts incl. levy / reference expenditure', f'Stock rate ({gl})', f'Stock rate ({tl})', f'Gain rate ({gl})',\n"
 + SP(13) + "f'Gain rate ({tl})', 'Drift (median)', 'Censored'],\n" + SP(12) + "rows, col_fmt=[LEFT] + [RIGHT] * 11)"),
(r'''raises mean saving and is the upper bound. Spending covered and relief are medians over windows in which the fund ''',
 r'''raises mean saving and is the upper bound. Spending covered is a median over windows in which the fund '''),
(r'''fills; the other columns, over all windows. Read revenue''',
 r'''fills; net receipts (including the CORP levy, over the same reference expenditure) and the other columns, over all windows. Read revenue'''),

# ── T25
(r'''_x(lev['nominal']['medians_all'], 'levy_gdp_mean', fmt_pct), _x(lev['real']['medians_all'], 'levy_gdp_mean', fmt_pct),''',
 r'''_xr(lev['nominal']['medians_all'], 'levy_gdp_mean', _e(sc), fmt_pct1), _xr(lev['real']['medians_all'], 'levy_gdp_mean', _e(sc), fmt_pct1),'''),
(r'''Median levy / GDP, nominal base', 'Median levy / GDP, real base''',
 r'''Median levy / reference expenditure, nominal base', 'Median levy / reference expenditure, real base'''),
(r'''Medians over all windows for levy / GDP, over ''', r'''Medians over all windows for levy / reference expenditure, over '''),
]

# ───────────────────────────── 8_3_RATES_charts.py ─────────────────────────────
CHARTS = [
# F1
(r'''med = np.array([_nan(b['relief_gdp']['p50']) for _, b in items])''',
 r'''e = sc['calibration']['exp_ref']
    med = np.array([_nan(b['relief_gdp']['p50']) / e for _, b in items])'''),
(r'''lo = np.array([_nan(b['relief_gdp']['p10']) for _, b in items])''',
 r'''lo = np.array([_nan(b['relief_gdp']['p10']) / e for _, b in items])'''),
(r'''hi = np.array([_nan(b['relief_gdp']['p90']) for _, b in items])''',
 r'''hi = np.array([_nan(b['relief_gdp']['p90']) / e for _, b in items])'''),
(r'''ax.set_xlabel('Relief paid, share of GDP (median, bars p10-p90)')''',
 r'''ax.set_xlabel(f'Spending covered: relief / reference expenditure ({e:.0%} of GDP); median, bars p10-p90')'''),
(r'''_title(sc, mode, 'Relief paid after fund fill, by country')''',
 r'''_title(sc, mode, 'Spending covered after fund fill, by country')'''),

# F3
(r'''tax = np.array([m['tax_gdp_mean'] for m in med])''',
 r'''exp = np.array([_scen(data, n)['calibration']['exp_ref'] for n in names])    # GDP share -> share of reference expenditure
    tax = np.array([m['tax_gdp_mean'] for m in med]) / exp'''),
(r'''heir = np.array([m['heir_gdp_mean'] for m in med])''', r'''heir = np.array([m['heir_gdp_mean'] for m in med]) / exp'''),
(r'''ref = np.array([m['refund_gdp_mean'] for m in med])''', r'''ref = np.array([m['refund_gdp_mean'] for m in med]) / exp'''),
(r'''net = np.array([m['net_gdp_mean'] for m in med])''', r'''net = np.array([m['net_gdp_mean'] for m in med]) / exp'''),
(r'''lev = np.array([m['levy_gdp_mean'] for m in med])''', r'''lev = np.array([m['levy_gdp_mean'] for m in med]) / exp'''),
(r'''ax.set_ylabel('Share of GDP, median over windows')
    ax.set_title(f'Where the receipts''',
 r'''ax.set_ylabel('Share of reference expenditure, median over windows')
    ax.set_title(f'Where the receipts'''),

# F4
(r'''a1.bar(x, [v['relief_gdp'] for v in m], color=C_LRR)
    a1.set_title('Relief paid (share of GDP)')
    _pct(a1, 'y')''',
 r'''a1.bar(x, [_nan(v.get('cov_ref')) for v in m], color=C_LRR)
    a1.set_title('Spending covered (relief / reference expenditure)')
    _pct(a1, 'y', 0)'''),

# F5
(r'''ax.scatter(df['drift'], df['relief_gdp'], s=12, alpha=0.5, color=C_SSM)''',
 r'''ax.scatter(df['drift'], df['cov_ref'], s=12, alpha=0.5, color=C_SSM)'''),
(r'''ax.set_ylabel('Relief paid, share of GDP')''',
 r'''ax.set_ylabel('Spending covered (relief / reference expenditure)')'''),
(r'''_title(sc, mode, 'Relief against tax-base drift (one dot per window)')''',
 r'''_title(sc, mode, 'Spending covered against tax-base drift (one dot per window)')'''),

# F10
(r'''ax.bar(x - w / 2, [_nan(v.get('net_gdp_mean')) for v in ma], w, color=C_SSM, label='Net receipts')''',
 r'''ax.bar(x - w / 2, [_nan(v.get('net_gdp_mean')) / s['calibration']['exp_ref'] for v, s in zip(ma, scs)], w, color=C_SSM, label='Net receipts (incl. levy)')'''),
(r'''ax.bar(x + w / 2, [_nan(v.get('relief_gdp')) for v in m], w, color=C_LRR, label='Relief paid')''',
 r'''ax.bar(x + w / 2, [_nan(v.get('cov_ref')) for v in m], w, color=C_LRR, label='Relief paid')'''),
(r'''ax.set_ylabel('Share of GDP, median over windows')
    ax.set_title(f'Net receipts and relief''',
 r'''ax.set_ylabel('Share of reference expenditure, median over windows')
    ax.set_title(f'Net receipts and relief'''),
]

PLAN = [('wdt_core.py', CORE), ('8_2_RATES_tables.py', TABLES), ('8_3_RATES_charts.py', CHARTS)]


def _pattern(old):
    """Regex for an anchor: literal text, but indentation after a line break may differ."""
    parts = old.split('\n')
    out = re.escape(parts[0])
    for part in parts[1:]:
        # an empty part is the end of the anchor: the newline is matched but the NEXT line's indent is not consumed
        out += '\n' + ('[ \t]*' + re.escape(part.lstrip(' \t')) if part.strip() else '')
    return re.compile(out)


def find(name, base):
    for cand in (base / name, base.parent / name):
        if cand.exists():
            return cand
    hits = sorted(base.rglob(name))
    return hits[0] if hits else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.', help='folder to search (default: current)')
    ap.add_argument('--write', action='store_true', help='apply the edits (default: dry run)')
    a = ap.parse_args()
    base = Path(a.dir).resolve()

    results, errors = {}, []
    for name, edits in PLAN:
        path = find(name, base)
        if path is None:
            errors.append(f'{name}: not found under {base} or its parent')
            continue
        text = path.read_text(encoding='utf-8')
        for i, (old, new) in enumerate(edits, 1):
            pat = _pattern(old)
            n = len(pat.findall(text))
            if n != 1:
                errors.append(f'{name} edit {i}: anchor matched {n} times (need exactly 1): {old[:90]!r}')
                continue
            text = pat.sub(lambda _m: new, text, count=1)
        try:
            compile(text, name, 'exec')
        except SyntaxError as exc:
            errors.append(f'{name}: patched text does not compile: {exc}')
        results[name] = (path, text, len(edits))

    if errors:
        print('NOTHING WRITTEN. Problems:')
        for e in errors:
            print('  -', e)
        sys.exit(1)

    for name, (path, text, n) in results.items():
        print(f'{"WRITE" if a.write else "ok   "} {path}  ({n} edits)')
        if a.write:
            path.with_suffix(path.suffix + '.bak').write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
            path.write_text(text, encoding='utf-8')
    if a.write:
        print('\nNow re-run: python 8_2_RATES_tables.py  and  python 8_3_RATES_charts.py   (no need to re-run rates_core.py)')
    else:
        print('\nDry run only. Re-run with --write to apply.')


if __name__ == '__main__':
    main()
