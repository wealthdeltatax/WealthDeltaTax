"""
fund_axis.py -- brief 138c, block 3: M2, M2d, M1c, M1 net and P6 of the household arm at its three held grid points under both settings of the fund_return axis (`safe`: the fund earns the net financial class return,
the low case; `market`: it earns the path's market return, like the legacy arm), on the constant common-ground path of 136c (the register mean market return, GDP growth as `decomp.py`), beside the legacy arm.
M2 and M2d divide by total wealth (138c block 1). Every value is a scenario value at a labelled point and fund setting; there is no central value and none is a headline. Writes fund_axis.csv.
Run from the repository root:  python -I model/studies/household-vs-legacy/fund_axis.py [--out DIR]
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[2]), str(HERE), str(HERE.parents[2] / 'model' / 'studies' / 'household-arm-account'), str(HERE.parents[2] / 'model' / 'studies' / 'household-arm-run')]

import account_table as A                                                      # noqa: E402
import decomp as D                                                             # noqa: E402
import flows as F                                                              # noqa: E402
import run_grid as G                                                           # noqa: E402
from model_v3.runner import runner as R                                        # noqa: E402

KEYS = (('M2', 'long', 'overall', 'value'), ('M2', 'short', 'overall', 'value'), ('M2d', 'long', 'overall', 'value'), ('M1', 'long', 'all', 'value'), ('M1c', 'long', 'all', 'value'),
        ('M1c', 'long', 'all', 'return_rate_pct'), ('P6', 'year 10', 'all', 'value'), ('P6', 'year 50', 'all', 'value'), ('P6', 'year 100', 'all', 'value'))


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--out', default=str(HERE))
    a = p.parse_args(argv)
    ctx, inp = A.setup()
    g, gg = np.full((R.T, 1), ctx.centre[R.RET['mean']] / 100.0), np.full((R.T, 1), ctx.gdp_g)
    rows = []
    rec, raw = F.run_arm(ctx, ctx.centre, g, gg, False)
    t = D.terms(raw)
    rows += [dict(case='legacy (common ground)', fund_return='legacy', output=k[0], horizon=k[1], band=k[2], term=k[3], value=float(t[k][0])) for k in KEYS]
    for name in D.POINTS:
        for fund in ('safe', 'market'):
            rec, raw = F.run_arm(G.point_ctx(ctx, inp, name, False, fund), ctx.centre, g, gg, True)
            t = D.terms(raw)
            rows += [dict(case=f'household {name}', fund_return=fund, output=k[0], horizon=k[1], band=k[2], term=k[3], value=float(t[k][0])) for k in KEYS]
    with open(Path(a.out) / 'fund_axis.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, ('case', 'fund_return', 'output', 'horizon', 'band', 'term', 'value'))
        w.writeheader()
        w.writerows(rows)
    print(f'fund_axis.csv: {len(rows)} rows')


if __name__ == '__main__':
    main()
