"""
gdp_spread.py -- brief 148c, block 3: the spread of P6 and M1 and the binding of M15a/b under `gdp_paths`, read from the grid files that `run_grid.py --paths 200` wrote (no model run).
For each file (settings: `off`, `indep`, `hist`; alone and with market paths) and each grid point: P6 (the fund in % of GDP, schedule S, years 10, 25, 50, 100) and M1 (net fiscal effect, % of GDP,
schedule S, short and long horizon) as P10, mean, P90 over the paths, and for M15a/b the largest value in any cell and the number of cells that are nonzero (does the envelope ever bind). The rows
are the ones `run_grid.py` wrote (a = mean, b = P10, c = P90). No number is tuned and none is called central. Run from the repository root:
python -I model/studies/household-arm-run/gdp_spread.py [DIR]          (DIR: the folder of the grid files, default results/household-arm-run/gdp_paths)
Writes gdp_spread.csv in DIR; prints one line a file and point.
"""
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'results' / 'household-arm-run'   # outputs and stored tables stay here until 163c
FILES = {'alone, off': 'grid_results.csv', 'alone, indep': 'grid_results_gdp_indep.csv', 'alone, hist': 'grid_results_gdp_hist.csv',
         'market paths, off': 'grid_results_paths.csv', 'market paths, indep': 'grid_results_paths_gdp_indep.csv', 'market paths, hist': 'grid_results_paths_gdp_hist.csv'}
COLS = ('config', 'point', 'metric', 'cell', 'p10', 'mean', 'p90')


def num(x):
    return float(x) if x not in ('', None) else np.nan


def main(d):
    out, d = [], Path(d)
    for cfg, f in FILES.items():
        if not (d / f).exists():
            print(f'{cfg}: {f} missing')
            continue
        rows = list(csv.DictReader(open(d / f)))
        for pt in sorted({r['grid'] for r in rows}):
            rs = [r for r in rows if r['grid'] == pt and r['schedule'] == 'S']
            for r in rs:
                if r['id'] == 'OP6':
                    out.append(dict(config=cfg, point=pt, metric='P6', cell=r['by'], p10=num(r['b']), mean=num(r['a']), p90=num(r['c'])))
                elif r['id'] == 'O1' and r['line'] == 'M1' and r['horizon'] in ('short', 'long'):
                    out.append(dict(config=cfg, point=pt, metric='M1', cell=r['horizon'], p10=num(r['b']), mean=num(r['a']), p90=num(r['c'])))
            w = [(num(r['a']), num(r['b']), num(r['c'])) for r in rs if r['id'] == 'OW3']
            v = np.array([x for t in w for x in t], float)
            out.append(dict(config=cfg, point=pt, metric='M15', cell=f"{len(w)} cells, {int((np.nan_to_num(v) != 0).sum())} nonzero values, {int(np.isnan(v).sum())} nan", p10=np.nanmin(v) if np.isfinite(v).any() else np.nan,
                            mean=np.nanmean(v) if np.isfinite(v).any() else np.nan, p90=np.nanmax(v) if np.isfinite(v).any() else np.nan))
            p6 = {r['cell']: r for r in out if r['config'] == cfg and r['point'] == pt and r['metric'] == 'P6'}
            m1 = {r['cell']: r for r in out if r['config'] == cfg and r['point'] == pt and r['metric'] == 'M1'}
            print(f"{cfg:22}{pt:12}", ' '.join(f"P6 {k.split('=')[1]}: {v['p10']:.1f}/{v['mean']:.1f}/{v['p90']:.1f}" for k, v in sorted(p6.items(), key=lambda kv: int(kv[0].split('=')[1]))),
                  '|', ' '.join(f"M1 {k}: {v['p10']:.2f}/{v['mean']:.2f}/{v['p90']:.2f}" for k, v in m1.items()), '|', out[-1]['cell'])
    with open(d / 'gdp_spread.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        w.writerows(out)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else DATA / 'gdp_paths')
