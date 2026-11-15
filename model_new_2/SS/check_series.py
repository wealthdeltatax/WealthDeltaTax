"""
check_series.py - verify what the TOML returns series actually is, against raw JST data.

    python check_series.py        (run from the folder with WDT_Params.toml, rates_data.py, jst_r6.json)

Answers: which JST column does the TOML series equal (nominal or real, which concept)?
Is hist_mean the arithmetic mean? What are the arithmetic and geometric means,
nominal and real, for the same years?
"""
import tomllib
import numpy as np
import pandas as pd
import rates_data as rd

with open('../WDT_Params.toml', 'rb') as fh:
    raw = tomllib.load(fh)
vals = np.array(raw['returns']['values'], float)
base = int(raw['returns']['series_base_year'])
hist = float(raw['tcm']['hist_mean'])
yrs = np.arange(base, base + len(vals))
n = len(vals)

def gmean(x):
    x = np.asarray(x, float)
    return float(np.prod(1 + x) ** (1 / len(x)) - 1)

print(f'TOML series: {n} values, {yrs[0]}-{yrs[-1]}')
print(f'  arithmetic mean : {vals.mean():.4%}')
print(f'  geometric mean  : {gmean(vals):.4%}')
print(f'  std dev         : {vals.std(ddof=1):.4%}')
print(f'  hist_mean in TOML: {hist:.4%}   '
      f'(diff vs arithmetic mean {abs(hist - vals.mean()):.2e})')

J = rd.load_jst()
u = rd.panel(J, 'GBR').reindex(yrs)
cands = [c for c in u.columns
         if c.endswith('_tr') or c.endswith('_tr_real')
         or c in ('eq_capgain', 'eq_capgain_real')]

print('\nWhich JST column matches the TOML series? (match = within 4dp rounding)')
rows = []
for c in cands:
    a = u[c].to_numpy(float)
    ok = ~np.isnan(a)
    if ok.sum() == 0:
        continue
    d = np.abs(a[ok] - vals[ok])
    rows.append((c, int(ok.sum()), int((d < 6e-5).sum()), float(d.max()), float(d.mean())))
tab = pd.DataFrame(rows, columns=['column', 'years', 'matches', 'max |diff|', 'mean |diff|'])
print(tab.sort_values('matches', ascending=False).round(5).to_string(index=False))

best = tab.sort_values('matches', ascending=False).iloc[0]['column']
print(f'\nBest column: {best}. Year-shift test (does shifting the alignment improve the match?)')
full = rd.panel(J, 'GBR')[best]
for s in (-3, -2, -1, 0, 1, 2, 3):
    a = full.reindex(yrs + s).to_numpy(float)
    ok = ~np.isnan(a)
    print(f'  shift {s:+d}: {(np.abs(a[ok]-vals[ok]) < 6e-5).sum()}/{ok.sum()} match')

bad = [(int(y), v, float(a)) for y, v, a in zip(yrs, vals, u[best].to_numpy(float))
       if np.isnan(a) or abs(a - v) >= 6e-5]
if bad:
    print('\nYears that do not match:', bad[:15])

print('\nSame years, from raw JST (UK):')
print(f'  nominal capital_tr  arithmetic {u["capital_tr"].mean():.4%}   geometric {gmean(u["capital_tr"].dropna()):.4%}')
print(f'  inflation (CPI)     arithmetic {u["infl"].mean():.4%}')
print(f'  real capital_tr     arithmetic {u["capital_tr_real"].mean():.4%}   geometric {gmean(u["capital_tr_real"].dropna()):.4%}')
print(f'  real GDP per head   arithmetic {u["gpc_real"].mean():.4%}   geometric {gmean(u["gpc_real"].dropna()):.4%}')
g_gap = gmean(u['capital_tr_real'].dropna()) - gmean(u['gpc_real'].dropna())
print(f'  real return less real GDP/head growth (geometric): {g_gap:.2%} a year')

m = tab.set_index('column').loc[best]
print('\nVERDICT:')
if best == 'capital_tr' and m['matches'] >= n - 1:
    print('  TOML series = JST capital_tr, NOMINAL (matches the rates_data.py docstring).')
elif best == 'capital_tr_real' and m['matches'] >= n - 1:
    print('  TOML series = JST capital_tr_real, i.e. REAL. The docstring is wrong.')
else:
    print(f'  TOML series does not cleanly equal one JST column (best: {best}, {int(m["matches"])}/{n}).')