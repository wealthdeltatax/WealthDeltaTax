"""
solve_rates.py - find the rate floor (tau_0) that hits a target effective rate for payers,
then report what that design raises.

    python solve_rates.py                         # 1% stock-rate and 25% gain-rate targets
    python solve_rates.py --stock 0.015 --gain 0.30
    python solve_rates.py --k 0.005               # steeper schedule: more of the burden on the very top
    python solve_rates.py --stride 5 --countries GBR USA FRA     # faster

Definitions (rates_engine.effective_rates, window sums, wealth- or gain-weighted):
  stock rate = sum_t net WDT / sum_t wealth          comparator: annual stock wealth tax
  gain  rate = sum_t net WDT / sum_t (r_t * W_t-1)   comparator: income / capital-gains tax
  'net' includes tax on inheritance receipts. 'payers' = cells whose window net tax > 0.
Because stock rate = gain rate x return, the two targets cannot both be met unless the
return is stock/gain. The script solves each separately and shows the other.

The target is hit on the MEDIAN across windows (uncensored, one index mode).
PLACEHOLDER: income tax + NI is taken as 15% of GDP (--inc-ni). Check against OBR.
"""
import argparse
import numpy as np
import pandas as pd

import rates_data as rd
import rates_sweep as rs

ap = argparse.ArgumentParser()
ap.add_argument('--stock', type=float, default=0.01)
ap.add_argument('--gain', type=float, default=0.25)
ap.add_argument('--k', type=float, default=None, help='k_per_gbp_m (default: DEFAULT_CFG)')
ap.add_argument('--tau-m', type=float, default=0.70)
ap.add_argument('--stride', type=int, default=3)
ap.add_argument('--countries', nargs='*', default=None)
ap.add_argument('--mode', default='gdp_pc')
ap.add_argument('--inc-ni', type=float, default=0.15,
                help='income tax + NI as a share of GDP (PLACEHOLDER)')
ap.add_argument('--c-mode', default='fixed', choices=['fixed', 'stationary'])
a = ap.parse_args()

J = rd.load_jst()
_cache = {}


def run(tau0):
    key = round(tau0, 6)
    if key in _cache:
        return _cache[key]
    kw = dict(index_modes=(a.mode,), start_stride=a.stride, countries=a.countries,
            tau_0=tau0, tau_m=a.tau_m, c_mode=a.c_mode)
    if a.k:
        kw['k_per_gbp_m'] = a.k
    cfg = rs.make_cfg(**kw)
    df = rs.sweep(J, cfg, verbose=False)
    df = df[~df['censored']].copy()
    df['drift'] = df['wealth_gdp_end'] / rs.calibration(J, cfg)['wealth_to_gdp']
    _cache[key] = df
    return df


def med(d, col):
    return float(np.nanmedian(d[col].astype(float)))


def solve(col, target, lo=0.02, hi=None, it=14):
    hi = hi or (a.tau_m - 0.01)
    f_lo, f_hi = med(run(lo), col), med(run(hi), col)
    if target < f_lo:
        return lo, f'target below the minimum reachable ({f_lo:.2%})'
    if target > f_hi:
        return hi, f'target above the maximum reachable ({f_hi:.2%}) at tau_m={a.tau_m}'
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if med(run(mid), col) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), 'ok'


r_real = med(run(0.15), 'r_mean')
print(f'median real return in windows: {r_real:.2%}.  Stock {a.stock:.1%} / gain {a.gain:.0%} '
      f'implies a return of {a.stock/a.gain:.1%}; the two targets agree only near that.')

designs = [('current default (tau_0 15%)', 0.15, '')]
for label, col, tgt in ((f'stock-rate target {a.stock:.1%}', 'er_stock_payers', a.stock),
                        (f'gain-rate target {a.gain:.0%}', 'er_gain_payers', a.gain)):
    t0, status = solve(col, tgt)
    designs.append((label, t0, status))

rows = []
for label, t0, status in designs:
    d = run(t0)
    st = d[d['drift'].between(0.67, 1.5)]
    rows.append({
        'design': label, 'solve status': status,
        'tau_0 %': 100 * t0,
        'stock rate, payers %': 100 * med(d, 'er_stock_payers'),
        'gain rate, payers %': 100 * med(d, 'er_gain_payers'),
        'stock rate, top 10% %': 100 * med(d, 'er_stock_top10'),
        'stock rate, top 1% %': 100 * med(d, 'er_stock_top1'),
        'stock rate, top 0.1% %': 100 * med(d, 'er_stock_top0.1'),
        'gain rate, top 1% %': 100 * med(d, 'er_gain_top1'),
        'payers (% of adults)': 100 * med(d, 'er_payer_adult_share'),
        'payers (% of wealth)': 100 * med(d, 'er_payer_wealth_share'),
        'net receipts % GDP': 100 * med(d, 'net_gdp_mean'),
        'relief % GDP': 100 * med(d, 'relief_gdp'),
        'relief % GDP (stable base)': 100 * med(st, 'relief_gdp') if len(st) else np.nan,
        'relief / (inc tax+NI) %': 100 * med(d, 'relief_gdp') / a.inc_ni,
        'cov_ref %': 100 * med(d, 'cov_ref'),
        'drift median': med(d, 'drift'),
        'fail %': 100 * d['fail'].astype(float).mean(),
        'windows': len(d),
    })

out = pd.DataFrame(rows).set_index('design').T
pd.set_option('display.width', 200)
print(f'\n(index mode {a.mode}, stride {a.stride}, k {a.k or "default"}, tau_m {a.tau_m}, '
      f'income tax+NI placeholder {a.inc_ni:.0%} of GDP)\n')
print(out.round(2).to_string())
out.to_csv('sweep_out/solve_rates.csv')
print('\nWritten: sweep_out/solve_rates.csv')