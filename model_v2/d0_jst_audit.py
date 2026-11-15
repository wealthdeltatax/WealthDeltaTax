"""
d0_jst_audit.py -- D0 internal JST audit (WDT Data Audit Spec, section 3, D0)
=============================================================================
Reads the JST file the cores read (jst_r6.json) and reports, per country:
  * raw variable coverage (first / last year, gaps, longest run)
  * usable years for three column sets: BASE (MODEL_COLS), LEVY (+ eq_capgain, gdpg), HOUSE (+ real house-price growth)
  * contiguous spans of usable years, and the column that binds each country
  * window counts (full loop, contiguous-only, seam-crossing, repeat) for several T
  * a check of the T = 100 counts against the Table 26 figures from the 13 Oct run
  * sensitivity of usable years to how pct_change treats missing values ("pad" legacy vs "none")
  * usable_years.csv: one row per usable year (country, set, year, run_id, run_len, flagged), so overlap with external
    series (D1 onward) can be counted exactly and per run

Why the pct_change item: rates_core.panel() calls Series.pct_change() with no fill argument. Older pandas forward-fills NaN
before differencing (so a missing CPI year becomes 0% inflation and the next year spans the gap); newer pandas does not.
The same code can therefore give different usable years, and different real returns, under different pandas versions.
This script runs both ways so you can see whether it matters for your file.

It is standalone (json, numpy, pandas). It mirrors rates_core.panel / flag_years / MODEL_COLS and wdt_jst.loop_windows as of
14 Oct 2026; pass --use-core DIR to import the real rates_core.panel instead (then the 'pad' / 'none' comparison is skipped).

Usage
  python d0_jst_audit.py --jst jst_r6.json [--toml WDT_Params.toml] [--out audit_d0] [--T 30 40 50 60 100]
                         [--infl none|pad] [--use-core MODEL_DIR] [--no-check26]
  python d0_jst_audit.py --selftest
"""

import argparse
import json
import sys
import tomllib
from pathlib import Path

import numpy as np
import pandas as pd

RETURN_COLS = ['capital_tr', 'eq_tr', 'housing_tr', 'risky_tr', 'safe_tr', 'bond_tr', 'eq_capgain']
FISCAL_COLS = ['gdp', 'expenditure', 'revenue', 'cpi', 'pop', 'hpnom']
MODEL_COLS = ['capital_tr_real', 'safe_tr_real', 'risky_tr_real', 'exp_gdp', 'infl', 'gpc', 'gpc_real']
LEVY_EXTRA = ['eq_capgain', 'gdpg']
HOUSE_EXTRA = ['hpg_real']
FLAG_DEFAULTS = {'real_return_lo': -0.40, 'real_return_hi': 0.60, 'infl_hi': 0.50}

# Table 26 (13 Oct run), gain ladder, T = 100: full-loop windows and contiguous windows per country.
TABLE26 = {
    'AUS': (115, 0), 'BEL': (112, 0), 'CHE': (79, 0), 'DEU': (114, 0), 'DNK': (139, 0), 'ESP': (112, 0), 'FIN': (98, 0),
    'FRA': (143, 0), 'GBR': (117, 0), 'ITA': (86, 0), 'JPN': (74, 0), 'NLD': (85, 0), 'NOR': (132, 0), 'PRT': (55, 0),
    'SWE': (137, 38), 'USA': (130, 31),
}


# ---------------------------------------------------------------- panel (mirrors rates_core.panel)

def _series(J, iso, var):
    c = J['countries'][iso]
    return pd.Series([np.nan if v is None else v for v in c['series'].get(var, [None] * len(c['years']))],
                     index=pd.Index(c['years'], name='year'), dtype=float)


def _pct(s, mode):
    """Year-on-year growth of a series. 'none': NaN if either year is missing. 'pad': forward-fill first (legacy pandas default)."""
    if mode == 'pad':
        s = s.ffill()
    elif mode != 'none':
        raise ValueError(mode)
    return s / s.shift(1) - 1.0


def build_panel(J, iso, mode='none'):
    d = pd.DataFrame({v: _series(J, iso, v) for v in RETURN_COLS + FISCAL_COLS})
    d['infl'] = _pct(d['cpi'], mode)
    for r in RETURN_COLS:
        d[f'{r}_real'] = (1.0 + d[r]) / (1.0 + d['infl']) - 1.0
    d['exp_gdp'] = d['expenditure'] / d['gdp']
    d['gdp_pc'] = d['gdp'] / d['pop']
    d['gdpg'] = _pct(d['gdp'], mode)
    d['gpc'] = _pct(d['gdp_pc'], mode)
    d['gpc_real'] = (1.0 + d['gpc']) / (1.0 + d['infl']) - 1.0
    d['hpg'] = _pct(d['hpnom'], mode)
    d['hpg_real'] = (1.0 + d['hpg']) / (1.0 + d['infl']) - 1.0
    return d


def flag_years(d, thr):
    r = d['capital_tr_real']
    return ((r < thr['real_return_lo']) | (r > thr['real_return_hi'])) | (d['infl'] > thr['infl_hi'])


def usable_years(d, cols):
    ok = d[list(cols)].notna().all(axis=1)
    return [int(y) for y in d.index[ok.to_numpy()]]


# ---------------------------------------------------------------- spans and windows

def runs(years):
    """Maximal runs of consecutive calendar years: list of (first, last, length)."""
    out, start, prev = [], None, None
    for y in years:
        if start is None:
            start = prev = y
        elif y == prev + 1:
            prev = y
        else:
            out.append((start, prev, prev - start + 1))
            start = prev = y
    if start is not None:
        out.append((start, prev, prev - start + 1))
    return out


def window_counts(years, T):
    """
    Same definitions as wdt_jst.loop_windows(years, T, wrap=True):
      total       = n (every start position)
      wraps       = starts whose window crosses the seam = min(n, T - 1)
      repeat      = T > n (all windows repeat years)
      contiguous  = windows that fit inside the series and contain no calendar gap
    """
    n = len(years)
    if n == 0 or T < 1:
        return {'total': 0, 'contiguous': 0, 'wraps': 0, 'repeat': 0}
    gap = np.array([years[k + 1] - years[k] != 1 for k in range(n - 1)], dtype=int)
    G = np.concatenate([[0], np.cumsum(gap)])
    fit = max(0, n - T + 1)
    cont = int(sum(1 for i in range(fit) if G[i + T - 1] - G[i] == 0))
    return {'total': n, 'contiguous': cont, 'wraps': min(n, T - 1), 'repeat': n if T > n else 0}


# ---------------------------------------------------------------- audit

def audit(J, mode, thr, Ts, panel_fn=None, years_out=None):
    """
    Returns (variables, usable, windows) DataFrames. If years_out is a list, one dict per usable year is appended to it:
    country, set, year, run_id (1-based, in calendar order), run_len (length of that run), flagged.
    """
    panel_fn = panel_fn or (lambda iso: build_panel(J, iso, mode))
    sets = {'BASE': MODEL_COLS, 'LEVY': MODEL_COLS + LEVY_EXTRA, 'HOUSE': MODEL_COLS + LEVY_EXTRA + HOUSE_EXTRA}
    var_rows, use_rows, win_rows = [], [], []
    for iso in sorted(J['countries']):
        d = panel_fn(iso)
        fl = flag_years(d, thr)
        for v in RETURN_COLS + FISCAL_COLS:
            ys = [int(y) for y in d.index[d[v].notna().to_numpy()]]
            rr = runs(ys)
            var_rows.append({'country': iso, 'var': v, 'first': ys[0] if ys else None, 'last': ys[-1] if ys else None,
                             'n': len(ys), 'runs': len(rr), 'longest_run': max((r[2] for r in rr), default=0)})
        for name, cols in sets.items():
            ys = usable_years(d, cols)
            rr = runs(ys)
            if years_out is not None:
                for rid, (a, b, ln) in enumerate(rr, start=1):
                    for y in range(a, b + 1):
                        years_out.append({'country': iso, 'set': name, 'year': y, 'run_id': rid, 'run_len': ln,
                                          'flagged': bool(fl.get(y, False))})
            span = d.loc[ys[0]:ys[-1]] if ys else d.iloc[0:0]
            # columns that are null inside the potential span, most damaging first
            lo, hi = int(d.index.min()), int(d.index.max())
            nulls = {c: int(d[c].isna().sum()) for c in cols}
            binding = sorted(nulls.items(), key=lambda kv: -kv[1])[:3]
            use_rows.append({'country': iso, 'set': name, 'n_usable': len(ys), 'first': ys[0] if ys else None,
                             'last': ys[-1] if ys else None, 'runs': len(rr), 'longest_run': max((r[2] for r in rr), default=0),
                             'n_flagged': int(sum(bool(fl.get(y, False)) for y in ys)),
                             'binding': '; '.join(f'{c}:{n}' for c, n in binding if n), 'panel_years': hi - lo + 1,
                             'span_breaks': int(span[cols].isna().any(axis=1).sum()) if len(span) else 0})
            for T in Ts:
                wc = window_counts(ys, T)
                win_rows.append({'country': iso, 'set': name, 'T': T, **wc})
    return pd.DataFrame(var_rows), pd.DataFrame(use_rows), pd.DataFrame(win_rows)


def check_table26(win):
    """Compare LEVY-set T = 100 counts with the 13 Oct run (Table 26). Returns (DataFrame, n_mismatch)."""
    w = win[(win['set'] == 'LEVY') & (win['T'] == 100)].set_index('country')
    rows, bad = [], 0
    for iso, (tot, cont) in TABLE26.items():
        got_t = int(w.loc[iso, 'total']) if iso in w.index else None
        got_c = int(w.loc[iso, 'contiguous']) if iso in w.index else None
        ok = (got_t == tot) and (got_c == cont)
        bad += (not ok)
        rows.append({'country': iso, 'expected_total': tot, 'got_total': got_t, 'expected_contig': cont,
                     'got_contig': got_c, 'match': 'ok' if ok else 'DIFF'})
    return pd.DataFrame(rows), bad


def md_table(df):
    cols = list(df.columns)
    lines = ['| ' + ' | '.join(cols) + ' |', '|' + '|'.join(':---' for _ in cols) + '|']
    for r in df.itertuples(index=False):
        lines.append('| ' + ' | '.join('' if v is None or (isinstance(v, float) and np.isnan(v)) else str(v) for v in r) + ' |')
    return '\n'.join(lines)


def load_thr(toml_path):
    if not toml_path:
        return dict(FLAG_DEFAULTS)
    with open(toml_path, 'rb') as fh:
        t = tomllib.load(fh)
    return {k: float(v) for k, v in t['rates']['flags'].items()}


def run(jst, toml, out, Ts, mode, use_core, check26):
    with open(jst, 'r', encoding='utf-8') as fh:
        J = json.load(fh)
    thr = load_thr(toml)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    panel_fn = None
    if use_core:
        sys.path.insert(0, str(Path(use_core).resolve()))
        import RATES.rates_core as rc
        panel_fn = lambda iso: rc.panel(J, iso)
        print(f'using rates_core.panel from {use_core}')
    year_rows = []
    var, use, win = audit(J, mode, thr, Ts, panel_fn, years_out=year_rows)
    var.to_csv(out / 'variables.csv', index=False)
    use.to_csv(out / 'usable.csv', index=False)
    win.to_csv(out / 'windows.csv', index=False)
    pd.DataFrame(year_rows, columns=['country', 'set', 'year', 'run_id', 'run_len', 'flagged']).to_csv(
        out / 'usable_years.csv', index=False)

    avail = sorted({v for c in J['countries'].values() for v in c['series']})
    (out / 'variables_available.txt').write_text('\n'.join(avail) + '\n', encoding='utf-8')

    md = [f'# D0 JST audit', '', f'File: {jst}. Countries: {len(J["countries"])}. pct_change mode: {mode}. '
          f'Flag thresholds: {thr}.', '', '## Usable years by set', '', md_table(use.drop(columns=['panel_years'])), '',
          '## Window counts (sum over countries)', '']
    tot = win.groupby(['set', 'T'])[['total', 'contiguous', 'wraps', 'repeat']].sum().reset_index()
    ncont = win[win['contiguous'] > 0].groupby(['set', 'T'])['country'].nunique().rename('countries_with_contiguous').reset_index()
    md += [md_table(tot.merge(ncont, on=['set', 'T'], how='left').fillna(0).astype({'countries_with_contiguous': int})), '']

    bad = 0
    if check26 and mode and not use_core:
        md += ['## Table 26 check (LEVY set, T = 100) under both pct_change modes', '']
        for m in ('none', 'pad'):
            _, _, w2 = audit(J, m, thr, [100])
            chk, b = check_table26(w2)
            md += [f'### mode = {m}: {len(chk) - b} of {len(chk)} countries match', '', md_table(chk), '']
            if m == mode:
                bad = b
        _, u_none, _ = audit(J, 'none', thr, [100])
        _, u_pad, _ = audit(J, 'pad', thr, [100])
        cmp_ = u_none[['country', 'set', 'n_usable']].merge(u_pad[['country', 'set', 'n_usable']],
                                                           on=['country', 'set'], suffixes=('_none', '_pad'))
        cmp_['diff'] = cmp_['n_usable_pad'] - cmp_['n_usable_none']
        md += ['## Usable years: pad minus none', '', md_table(cmp_[cmp_['diff'] != 0]) if (cmp_['diff'] != 0).any()
               else 'No difference: the pct_change fill behaviour does not affect usable years in this file.', '']
    elif check26 and use_core:
        chk, bad = check_table26(win)
        md += ['## Table 26 check (LEVY set, T = 100, rates_core.panel)', '', md_table(chk), '']
    (out / 'audit_d0.md').write_text('\n'.join(md), encoding='utf-8')
    print('\n'.join(md[:3]))
    print(f'Written to {out}/: audit_d0.md, variables.csv, usable.csv, usable_years.csv, windows.csv, variables_available.txt')
    return var, use, win, bad


# ---------------------------------------------------------------- self-test (synthetic data, brute-force comparison)

def _loop_windows_ref(years, T, wrap=True):
    """Verbatim logic of wdt_jst.loop_windows, used only to check window_counts."""
    n, T = len(years), int(T)
    if n == 0 or T < 1:
        return []
    starts = range(n) if wrap else range(0, n - T + 1)
    out = []
    for i in starts:
        yrs = [years[(i + k) % n] for k in range(T)]
        seam = (i + T) > n
        gap = any(yrs[k + 1] - yrs[k] != 1 for k in range(T - 1))
        out.append({'wraps': seam, 'repeat': T > n, 'contiguous': (not seam) and (not gap)})
    return out


def selftest():
    rng = np.random.default_rng(0)
    # window_counts against the reference on random year sets with gaps
    for _ in range(300):
        n = int(rng.integers(0, 40))
        years = sorted(set(int(y) for y in rng.integers(1900, 1960, n)))
        for T in (1, 3, 7, 25, 60):
            ref = _loop_windows_ref(years, T)
            got = window_counts(years, T)
            exp = {'total': len(ref), 'contiguous': sum(w['contiguous'] for w in ref),
                   'wraps': sum(w['wraps'] for w in ref), 'repeat': sum(w['repeat'] for w in ref)}
            assert got == exp, (years, T, got, exp)
    # runs
    assert runs([1, 2, 3, 7, 8, 10]) == [(1, 3, 3), (7, 8, 2), (10, 10, 1)] and runs([]) == []
    # pad vs none: one missing CPI year
    yrs = list(range(2000, 2012))
    cpi = [100.0 * 1.02 ** k for k in range(12)]
    cpi[5] = None
    base = {v: [0.05] * 12 for v in RETURN_COLS}
    fis = {'gdp': [1000.0 * 1.03 ** k for k in range(12)], 'expenditure': [400.0] * 12, 'revenue': [380.0] * 12,
           'cpi': cpi, 'pop': [10.0] * 12, 'hpnom': [100.0] * 12}
    J = {'countries': {'XXX': {'years': yrs, 'series': {**base, **fis}}}}
    d_none, d_pad = build_panel(J, 'XXX', 'none'), build_panel(J, 'XXX', 'pad')
    assert np.isnan(d_none.loc[2005, 'infl']) and np.isnan(d_none.loc[2006, 'infl'])
    assert d_pad.loc[2005, 'infl'] == 0.0 and abs(d_pad.loc[2006, 'infl'] - (cpi[6] / cpi[4] - 1.0)) < 1e-12
    u_none, u_pad = usable_years(d_none, MODEL_COLS), usable_years(d_pad, MODEL_COLS)
    assert 2005 not in u_none and 2006 not in u_none and 2005 in u_pad and 2000 not in u_none
    assert len(u_pad) - len(u_none) == 2
    # end-to-end on the synthetic file, including the usable-years export
    ye = []
    var, use, win = audit(J, 'none', FLAG_DEFAULTS, [5], years_out=ye)
    r = use[(use['country'] == 'XXX') & (use['set'] == 'BASE')].iloc[0]
    assert r['n_usable'] == len(u_none) and r['runs'] == len(runs(u_none))
    yb = pd.DataFrame(ye)
    yb = yb[yb['set'] == 'BASE']
    assert list(yb['year']) == u_none                                    # same years as usable_years
    rr = runs(u_none)
    assert yb['run_id'].nunique() == len(rr) == int(r['runs'])           # run ids match runs
    for rid, (a, b, ln) in enumerate(rr, start=1):
        sub = yb[yb['run_id'] == rid]
        assert sub['year'].min() == a and sub['year'].max() == b and (sub['run_len'] == ln).all()
    assert len(pd.DataFrame(ye)) == sum(int(x) for x in use['n_usable'])  # rows across all sets = sum of n_usable
    # years_out is optional: default behaviour unchanged
    v2, u2, w2 = audit(J, 'none', FLAG_DEFAULTS, [5])
    assert u2.equals(use) and w2.equals(win)
    print('d0_jst_audit self-test ok')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--jst', default='jst_r6.json')
    ap.add_argument('--toml', default=None, help='WDT_Params.toml, for the [rates.flags] thresholds')
    ap.add_argument('--out', default='audit_d0')
    ap.add_argument('--T', nargs='*', type=int, default=[30, 40, 50, 60, 100])
    ap.add_argument('--infl', choices=['none', 'pad'], default='none', help='pct_change fill mode for the main outputs')
    ap.add_argument('--use-core', default=None, help='Model directory: import rates_core.panel instead of the mirror')
    ap.add_argument('--no-check26', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        run(a.jst, a.toml, a.out, a.T, a.infl, a.use_core, not a.no_check26)
