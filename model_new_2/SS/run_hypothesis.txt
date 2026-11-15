"""
run_hypothesis.py - "the rich consume almost nothing of their wealth", tested without
letting the whole tax base compound faster than GDP.

    python run_hypothesis.py                 # all countries, every 3rd start year
    python run_hypothesis.py --stride 5 --countries GBR USA FRA

Mechanism: payout_top sets consumption for the top cells; with payout_constrained=True
everyone else's consumption is solved so the WEALTH-WEIGHTED MEAN stays at c (the
stationary level). For each scenario it prints the implied consumption of the rest,
flags impossible (negative) values, and reports the base-drift diagnostic.
"""
import argparse
import numpy as np
import pandas as pd

import rates_data as rd
import rates_sweep as rs

ap = argparse.ArgumentParser()
ap.add_argument('--stride', type=int, default=3)
ap.add_argument('--countries', nargs='*', default=None)
a = ap.parse_args()

J = rd.load_jst()
C_STAT = 0.035       # stationary mean leakage (valgen D16)
SCEN = [
    ('uniform c=3.5% (stationary baseline)', dict(c=C_STAT)),
    ('uniform c=0.5% (everyone)',            dict(c=0.005)),
    ('top 6% at 3.0%, rest absorb',          dict(c=C_STAT, payout_top=0.030)),
    ('top 6% at 2.0%, rest absorb',          dict(c=C_STAT, payout_top=0.020)),
    ('top 6% at 1.0%, rest absorb',          dict(c=C_STAT, payout_top=0.010)),
    ('top 6% at 0.5%, rest absorb',          dict(c=C_STAT, payout_top=0.005)),
    ('top 2% at 0.5%, rest absorb',          dict(c=C_STAT, payout_top=0.005, payout_top_frac=0.02)),
]
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 30)

rows = []
for label, kw in SCEN:
    cfg = rs.make_cfg(index_modes=('gdp_pc',), start_stride=a.stride,
                      countries=a.countries, **kw)
    cal = rs.calibration(J, cfg)
    w0 = cal['wealth_to_gdp']
    c_rest = np.nan; wt = np.nan
    if cfg['payout_top'] is not None:
        share = cal['share']; wsh = share * cal['V0']; wsh = wsh / wsh.sum()
        top = np.cumsum(share[::-1])[::-1] <= cfg['payout_top_frac'] * (1 + 1e-6)
        wt = wsh[top].sum()
        c_rest = (cfg['c'] - cfg['payout_top'] * wt) / (1 - wt)
    print(f'{label}: top-cell wealth share {wt:.2f}, implied c for the rest {c_rest:.4f}'
          + ('   <-- NEGATIVE: scenario invalid' if c_rest < 0 else ''), flush=True)
    df = rs.sweep(J, cfg, verbose=False)
    d = df[~df['censored']].copy()
    d['drift'] = d['wealth_gdp_end'] / w0
    st = d[d['drift'].between(0.67, 1.5)]
    rows.append({
        'scenario': label,
        'c_rest': c_rest,
        'windows': len(d),
        'relief/GDP % (median)': 100 * d['relief_gdp'].median(),
        'cov_ref % (median)': 100 * d['cov_ref'].median(),
        'drift median (x launch)': d['drift'].median(),
        'drift p90': d['drift'].quantile(.9),
        '% windows drift>1.5': 100 * (d['drift'] > 1.5).mean(),
        'stable n': len(st),
        'stable relief/GDP %': 100 * st['relief_gdp'].median() if len(st) else np.nan,
        'fail %': 100 * d['fail'].astype(float).mean(),
    })

out = pd.DataFrame(rows)
print('\n', out.round(2).to_string(index=False))
out.to_csv('sweep_out/hypothesis.csv', index=False)
print('\nInterpretation: compare relief/GDP only between rows with similar drift.')