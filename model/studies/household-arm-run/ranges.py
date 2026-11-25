"""Brief 124c block 3: ranges across the held household grid points (min to max, no central), with the legacy arm beside them as context.
    python -I model/studies/household-arm-run/ranges.py     writes ranges.csv, prints summary lines.
Column a of grid_results.csv is the point or mean (p10_mean_p90 rows: a mean, b p10, c p90)."""
from __future__ import annotations

import csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELD = ('median_mid', 'max_mid', 'median_low')   # min_mid and median_high fail I1 and have no rows (checks.csv)


def num(x):
    return float('nan') if x in ('', 'nan') or x.startswith('withheld') else float(x)      # a withheld cell (135c) is not a number


SUF = '_paths' if '--market-paths' in sys.argv else ''   # 128c: reads grid_results_paths.csv and writes ranges_paths.csv


def main():
    rows = list(csv.DictReader(open(HERE / f'grid_results{SUF}.csv', encoding='utf-8')))
    key = lambda r: (r['id'], r['horizon'], r['by'], r['line'])
    cells = {}
    for r in rows:
        cells.setdefault(key(r), {})[r['grid']] = r
    out, flat, nanrows = [], 0, 0
    for k, g in cells.items():
        hh = {p: g[p] for p in HELD if p in g}
        vals = {p: num(r['a']) for p, r in hh.items()}
        ok = {p: v for p, v in vals.items() if v == v}
        if not ok:
            nanrows += 1
        lo = min(ok, key=ok.get) if ok else ''; hi = max(ok, key=ok.get) if ok else ''
        spread = any(num(r['c']) - num(r['b']) > 1e-12 for r in hh.values() if r['summary'] == 'p10_mean_p90' and r['b'] and r['c'] not in ('', 'nan'))
        flat += (not spread) and any(r['summary'] == 'p10_mean_p90' for r in hh.values())
        L = g.get('legacy')
        mark = next((r['a'] for r in hh.values() if r['a'].startswith('withheld')), '')       # 135c: a withheld id keeps its marker, no min or max
        out.append(dict(id=k[0], horizon=k[1], by=k[2], line=k[3], unit=next(iter(hh.values()))['unit'] if hh else '', n_points=len(ok),
                        min=ok[lo] if ok else mark, max=ok[hi] if ok else mark, min_at=lo, max_at=hi, path_spread=spread,
                        legacy_a=L['a'] if L else '', legacy_p10=L['b'] if L else '', legacy_p90=L['c'] if L else ''))
    with open(HERE / f'ranges{SUF}.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(out[0])); w.writeheader(); w.writerows(out)
    print(f'{len(out)} cells; {nanrows} all-nan; {flat} p10_mean_p90 cells with no path spread in any held household point')


if __name__ == '__main__':
    main()
