"""
check_coverage.py - decompose cov_ref into its parts, using the baseline
windows already saved by run_sweep.py (sweep_out/baseline_windows.csv).

    python check_coverage.py [mode]        # mode: gdp_pc (default) | cpi | wealth

cov_ref   = relief_gdp / exp_ref          (exp_ref = UK 2019 expenditure/GDP, fixed)
coverage  = relief_gdp / own exp/GDP      (own-country, post-fill years)
So relief_gdp (relief as a share of GDP) is the number to judge first;
every coverage figure is that number divided by some spending ratio.
"""
import sys
import numpy as np
import pandas as pd

import rates_data as rd
import rates_sweep as rs

mode = sys.argv[1] if len(sys.argv) > 1 else 'gdp_pc'
df = pd.read_csv('sweep_out/baseline_windows.csv')
d = df[(df['mode'] == mode) & (~df['censored'])].copy()
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 30)

# 1. the reference spending ratio actually used, and the launch wealth/GDP
J = rd.load_jst()
cal = rs.calibration(J, rs.make_cfg())
exp_ref = cal['exp_ref']
w0 = cal['wealth_to_gdp']
print(f'exp_ref (UK 2019 expenditure/GDP) used as denominator : {exp_ref:.3f}')
print(f'wealth/GDP at launch (calibration)                    : {w0:.2f}')

# 2. own post-fill spending ratio recovered from the saved columns
d['own_exp_gdp'] = d['relief_gdp'] / d['coverage']
d['exp_ratio_own_vs_ref'] = d['own_exp_gdp'] / exp_ref

print(f'\n=== {mode}: relief as a share of GDP, and the spending ratios it is divided by ===')
g = d.groupby('era').agg(
    windows=('iso', 'size'),
    relief_gdp_pct=('relief_gdp', lambda x: 100 * x.median()),
    own_exp_gdp_pct=('own_exp_gdp', lambda x: 100 * x.median()),
    cov_own_pct=('coverage', lambda x: 100 * x.median()),
    cov_ref_pct=('cov_ref', lambda x: 100 * x.median()),
    net_gdp_mean_pct=('net_gdp_mean', lambda x: 100 * x.median()),
    fill_year=('fill_year', 'median'),
    wealth_gdp_end=('wealth_gdp_end', 'median'),
)
print(g.round(2).to_string())
print(f'\nAll eras: median relief/GDP {100*d["relief_gdp"].median():.2f}%, '
      f'median own spending/GDP {100*d["own_exp_gdp"].median():.1f}%, '
      f'reference {100*exp_ref:.1f}%')

# 3. coverage at fixed spending ratios (what the same relief covers at each)
print('\n=== Same relief against fixed spending levels (median window) ===')
rel = d['relief_gdp'].median()
for e in (0.10, 0.20, 0.30, 0.40, 0.50):
    print(f'  spending = {100*e:.0f}% of GDP  ->  coverage {100*rel/e:.1f}%')

# 4. is the tax base staying near its launch size relative to GDP?
d['w_drift'] = d['wealth_gdp_end'] / w0
print('\n=== Wealth/GDP at end of window relative to launch (1.0 = unchanged) ===')
print(d['w_drift'].describe(percentiles=[.1, .5, .9]).round(2).to_string())
print(f'windows with wealth/GDP more than 1.5x launch: {100*(d["w_drift"]>1.5).mean():.1f}%')
print(f'windows with wealth/GDP below 0.67x launch    : {100*(d["w_drift"]<0.67).mean():.1f}%')

# 5. correlation of relief with the things that should drive it
print('\n=== Correlation with relief_gdp ===')
for c in ('r_mean', 'wealth_gdp_mean', 'wealth_gdp_end', 'fill_year', 'net_gdp_mean',
          'paying_at_fill', 'er_stock_payers'):
    if c in d:
        print(f'  {c:18s} {d["relief_gdp"].corr(d[c]):+.2f}')

# 6. the extremes
cols = ['iso', 'start', 'era', 'relief_gdp', 'own_exp_gdp', 'coverage', 'cov_ref',
        'r_mean', 'wealth_gdp_end', 'fill_year']
print('\n=== 12 highest relief/GDP windows ===')
print(d.sort_values('relief_gdp', ascending=False)[cols].head(12).round(3).to_string(index=False))
print('\n=== 12 windows with the smallest own spending/GDP (inflates own-country coverage) ===')
print(d.sort_values('own_exp_gdp')[cols].head(12).round(3).to_string(index=False))
