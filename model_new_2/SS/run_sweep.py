"""
run_sweep.py - one-at-a-time sensitivity run over the rates_sweep options.

Usage (from the folder holding the rates_*.py files and jst_r6.json):
    python run_sweep.py                    # all countries, every 3rd start year
    python run_sweep.py --stride 1         # every start year (slow)
    python run_sweep.py --countries GBR USA FRA
    python run_sweep.py --quick            # GBR only, stride 5, fewer scenarios

Each scenario = the baseline (DEFAULT_CFG) with ONE setting changed.
Outputs (in ./sweep_out/):
    summary_by_scenario.csv   one row per scenario x index mode
    baseline_by_country.csv   per-country table for the baseline
    baseline_by_era.csv       baseline split by era
    baseline_windows.csv      every baseline window (raw rows)
    all_windows.csv           every window of every scenario
Headline metric: cov_ref  = relief over the 10 years after LRR fill / fixed
modern UK expenditure (2019). Comparable across countries and eras.
'coverage' (own-country expenditure) is reported too, but is distorted by
small historical governments.
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd

import rates_data as rd
import rates_sweep as rs

OUT = Path('sweep_out')

# (label, overrides). Every entry changes only what it names.
SCENARIOS = [
    ('BASELINE', {}),
    # reserves and fund mechanics
    ('ms=1', {'ms': 1.0}), ('ms=2', {'ms': 2.0}), ('ms=5', {'ms': 5.0}),
    ('ml=1', {'ml': 1.0}), ('ml=2', {'ml': 2.0}), ('ml=5', {'ml': 5.0}),
    ('a_window=3', {'a_window': 3}), ('a_window=10', {'a_window': 10}),
    ('safe_share=0.5', {'safe_share': 0.5}),
    ('safe_share=1.0', {'safe_share': 1.0}),
    # horizon and window length
    ('horizon=5', {'horizon': 5}),
    ('T=40, horizon=10', {'T': 40}),
    ('T=40, horizon=15', {'T': 40, 'horizon': 15}),
    # rate function
    ('tau_0=0.10', {'tau_0': 0.10}), ('tau_0=0.20', {'tau_0': 0.20}),
    ('tau_m=0.50', {'tau_m': 0.50}), ('tau_m=0.90', {'tau_m': 0.90}),
    ('k=0.0005', {'k_per_gbp_m': 0.0005}), ('k=0.002', {'k_per_gbp_m': 0.002}),
    ('wmin=1m', {'wmin_gbp_m': 1.0}), ('wmin=5m', {'wmin_gbp_m': 5.0}),
    ('wmin=top 5%', {'wmin_pct': 0.05}), ('wmin=top 2%', {'wmin_pct': 0.02}),
    # behaviour
    ('c=0.02', {'c': 0.02}), ('c=0.05', {'c': 0.05}),
    ('heir=fresh (ablation)', {'heir_rule': 'fresh'}),
    ('top payout 1%', {'payout_top': 0.01}),
    ('top payout 7%', {'payout_top': 0.07}),
    ('stationary c', {'c_mode': 'stationary'}),
    # distribution
    ('dist=advani upper', {'dist': 'advani', 'dist_mode': 'upper'}),
    ('dist=adjusted/add', {'dist': 'adjusted', 'dist_mode': 'add'}),
    ('dist=adjusted/reallocate', {'dist': 'adjusted', 'dist_mode': 'reallocate'}),
    ('dist=survey', {'dist': 'survey', 'dist_mode': 'add'}),
    # sample policy
    ('exclude flagged years', {'exclude_flagged': True}),
]
QUICK_LABELS = {'BASELINE', 'ms=1', 'ms=5', 'ml=1', 'ml=5', 'horizon=5',
                'tau_0=0.10', 'tau_0=0.20', 'c=0.02', 'c=0.05',
                'dist=advani upper', 'dist=survey', 'exclude flagged years', 
                'stationary c'}


def q(x, p):
    x = pd.Series(x).dropna()
    return float(np.quantile(x, p)) if len(x) else np.nan


def summarise(df, label, mode):
    g = df[df['mode'] == mode]
    ok = g[~g['censored']]
    cm = ok.groupby('iso')['cov_ref'].median()
    return {
        'scenario': label, 'mode': mode,
        'windows': len(g), 'countries': g['iso'].nunique(),
        'censored %': 100 * g['censored'].mean() if len(g) else np.nan,
        'cov_ref p10 %': 100 * q(ok['cov_ref'], .10),
        'cov_ref median %': 100 * q(ok['cov_ref'], .50),
        'cov_ref p90 %': 100 * q(ok['cov_ref'], .90),
        'country-median cov_ref %': 100 * float(cm.median()) if len(cm) else np.nan,
        'own-exp coverage median %': 100 * q(ok['coverage'], .50),
        'fail %': 100 * float(ok['fail'].astype(float).mean()) if len(ok) else np.nan,
        'median fill year': q(ok['fill_year'], .50),
        'UK (GBR) median cov_ref %': 100 * q(ok[ok['iso'] == 'GBR']['cov_ref'], .5),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stride', type=int, default=3)
    ap.add_argument('--countries', nargs='*', default=None)
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()
    if a.quick:
        a.countries = a.countries or ['GBR']
        a.stride = max(a.stride, 5)

    OUT.mkdir(exist_ok=True)
    J = rd.load_jst()
    scen = [s for s in SCENARIOS if (not a.quick or s[0] in QUICK_LABELS)]
    rows, frames = [], []
    t0 = time.time()
    for i, (label, kw) in enumerate(scen, 1):
        print(f'[{i}/{len(scen)}] {label} ...', flush=True)
        cfg = rs.make_cfg(start_stride=a.stride, countries=a.countries, **kw)
        try:
            df = rs.sweep(J, cfg, verbose=False)
        except Exception as e:                      # keep going; report the failure
            print(f'    FAILED: {type(e).__name__}: {e}')
            continue
        df.insert(0, 'scenario', label)
        frames.append(df)
        for mode in cfg['index_modes']:
            rows.append(summarise(df, label, mode))
        if label == 'BASELINE':
            df.to_csv(OUT / 'baseline_windows.csv', index=False)
            for m in cfg['index_modes']:
                rs.by_country(df, m).to_csv(OUT / f'baseline_by_country_{m}.csv')
            ok = df[~df['censored']]
            era = (ok.groupby(['mode', 'era'])
                     .agg(windows=('cov_ref', 'size'),
                          cov_ref_median=('cov_ref', 'median'),
                          cov_ref_p10=('cov_ref', lambda x: x.quantile(.1)),
                          cov_ref_p90=('cov_ref', lambda x: x.quantile(.9)),
                          fail=('fail', lambda x: x.astype(float).mean())))
            era.to_csv(OUT / 'baseline_by_era.csv')
            print('\nBASELINE by era (cov_ref, fraction of expenditure):')
            print(era.round(4).to_string(), '\n')

    summ = pd.DataFrame(rows)
    summ.to_csv(OUT / 'summary_by_scenario.csv', index=False)
    if frames:
        pd.concat(frames).to_csv(OUT / 'all_windows.csv', index=False)

    pd.set_option('display.width', 200)
    pd.set_option('display.max_columns', 30)
    for metric in ('country-median cov_ref %', 'fail %', 'censored %'):
        print(f'\n=== {metric}, by scenario and index mode ===')
        pv = summ.pivot(index='scenario', columns='mode', values=metric)
        pv = pv.reindex([s[0] for s in scen if s[0] in pv.index])
        print(pv.round(2).to_string())

    base = summ[(summ['scenario'] == 'BASELINE') & (summ['mode'] == 'gdp_pc')]
    if len(base):
        b = float(base['country-median cov_ref %'].iloc[0])
        d = summ[summ['mode'] == 'gdp_pc'].copy()
        d['change vs baseline (pp)'] = d['country-median cov_ref %'] - b
        print('\n=== Largest movers vs baseline (gdp_pc) ===')
        print(d.reindex(d['change vs baseline (pp)'].abs()
                        .sort_values(ascending=False).index)
                [['scenario', 'country-median cov_ref %',
                  'change vs baseline (pp)', 'fail %', 'censored %']]
                .head(12).round(2).to_string(index=False))

    print(f'\nDone in {time.time() - t0:.0f}s. Files in {OUT.resolve()}')


if __name__ == '__main__':
    main()