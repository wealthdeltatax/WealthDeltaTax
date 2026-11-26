#!/usr/bin/env python3
"""Brief 175r: level, trend, volatility and asset-price correlation of the retired-tax series.

    python -I research/tables/174r-evidence/retired_tax_stats.py     (run retired_tax_series.py first; both are deterministic)

Reads retired-tax-gdp-annual-full.csv (this folder) and the UK series of `data/jst/jst_r6.json` (Jorda-Schularick-Taylor, release 6; read only; calendar years):
`hpnom` (nominal house price index), `eq_capgain` (equity price change, fraction; the index is its cumulative product), `gdp` (nominal GDP).
Writes retired-tax-stats.csv, one row per tax and basis, outturn years only (the sheet's own flag). Prints one summary line.

Definitions (fixed here so the numbers regenerate):
  first3, last3   mean share of GDP (percent) of the first and the last three outturn years.
  slope_per_decade  OLS slope of the share on the year, percentage points per ten years.
  volatility_sd_change  standard deviation (n-1) of the annual change in the share, percentage points.
  The house price and equity ratios are index / nominal GDP (levels in arbitrary units; only changes and correlations are used). A financial year 20XX-YY is
  matched to calendar year 20XX (April 20XX to March 20YY: nine months fall in 20XX).
  corr_chg_*  Pearson correlation of the annual change in the tax share (percentage points) with the annual log change of the ratio; corr_lvl_* the correlation
  of the two levels (shown for completeness: two trending levels correlate spuriously). n_* is the number of years in the overlap.
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
JST = 'data/jst/jst_r6.json'


def jst_ratios():
    c = json.loads((ROOT / JST).read_text(encoding='utf-8'))['countries']['GBR']
    yrs, s = c['years'], c['series']
    gdp, hp, eq = s['gdp'], s['hpnom'], s['eq_capgain']
    hpr, eqr, idx = {}, {}, 1.0
    for i, y in enumerate(yrs):
        if eq[i] is not None:
            idx *= 1.0 + float(eq[i])
        if gdp[i] and hp[i]:
            hpr[y] = float(hp[i]) / float(gdp[i])
        if gdp[i] and eq[i] is not None:
            eqr[y] = idx / float(gdp[i])
    return hpr, eqr


def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1]) if len(a) > 3 else float('nan')


def stats(rows, hpr, eqr):
    out = []
    keys = []
    for r in rows:
        k = (r['tax'], r['basis'])
        if k not in keys:
            keys.append(k)
    for tax, basis in keys:
        s = [(r['financial_year'], float(r['receipts_percent_GDP']), r['flag']) for r in rows if (r['tax'], r['basis']) == (tax, basis)]
        o = [(int(y[:4]), v) for y, v, f in s if f == 'outturn']
        fc = [(y, v) for y, v, f in s if f == 'forecast']
        yr, v = np.array([a for a, _ in o], float), np.array([b for _, b in o], float)
        d = np.diff(v)
        hi, lo = int(np.argmax(v)), int(np.argmin(v))
        row = dict(tax=tax, basis=basis, first_year=f'{o[0][0]}-{str(o[0][0] + 1)[2:]}', last_outturn_year=f'{o[-1][0]}-{str(o[-1][0] + 1)[2:]}', n_years=len(o),
                   first3=f'{v[:3].mean():.3f}', last3=f'{v[-3:].mean():.3f}', mean=f'{v.mean():.3f}', min=f'{v[lo]:.3f}', min_year=int(yr[lo]), max=f'{v[hi]:.3f}', max_year=int(yr[hi]),
                   slope_per_decade=f'{10 * np.polyfit(yr, v, 1)[0]:+.3f}', volatility_sd_change=f'{d.std(ddof=1):.3f}',
                   forecast_end=(f'{fc[-1][0]}:{fc[-1][1]:.3f}' if fc else ''))
        for name, ratio in (('hp', hpr), ('eq', eqr)):
            ys = [int(y) for y, p in zip(yr, v) if int(y) in ratio and int(y) - 1 in ratio and int(y) - 1 in dict(o)]
            if len(ys) > 3:
                dv = [dict(o)[y] - dict(o)[y - 1] for y in ys]
                dr = [float(np.log(ratio[y] / ratio[y - 1])) for y in ys]
                row[f'corr_chg_{name}'], row[f'n_chg_{name}'] = f'{corr(dv, dr):+.2f}', len(ys)
            else:
                row[f'corr_chg_{name}'], row[f'n_chg_{name}'] = '', len(ys)
            ls = [int(y) for y in yr if int(y) in ratio]
            if len(ls) > 3:
                row[f'corr_lvl_{name}'] = f'{corr([dict(o)[y] for y in ls], [ratio[y] for y in ls]):+.2f}'
            else:
                row[f'corr_lvl_{name}'] = ''
        row['jst_last_year'] = max(hpr)
        out.append(row)
    return out


SIX = ('corporation_tax', 'capital_gains_tax', 'inheritance_tax', 'stamp_duties_total', 'business_rates', 'council_tax')


def six(rows):
    """The sum of the six retired taxes (corporation tax in total, stamp duties in total), cash basis, each year where all six are held, as a synthetic series."""
    by = {}
    for r in rows:
        if r['basis'] == 'cash' and r['tax'] in SIX:
            by.setdefault(r['financial_year'], {})[r['tax']] = (float(r['receipts_percent_GDP']), r['flag'])
    return [dict(tax='six_taxes_sum', financial_year=y, basis='cash', receipts_percent_GDP=f'{sum(v for v, _ in d.values()):.4f}',
                 flag='outturn' if all(f == 'outturn' for _, f in d.values()) else 'forecast') for y, d in sorted(by.items()) if len(d) == len(SIX)]


def main():
    rows = list(csv.DictReader((HERE / 'retired-tax-gdp-annual-full.csv').open(encoding='utf-8')))
    rows += six(rows)
    hpr, eqr = jst_ratios()
    res = stats(rows, hpr, eqr)
    cols = list(res[0])
    with (HERE / 'retired-tax-stats.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, cols, lineterminator='\n')
        w.writeheader()
        w.writerows(res)
    print(f'{len(res)} series; JST UK ratios to {max(hpr)} (house) and {max(eqr)} (equity)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
