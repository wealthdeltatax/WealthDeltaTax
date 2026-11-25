"""
floor_diag.py -- brief 137c: every floor line-year (HouseholdHook.pre sets the floor entry non-zero) and every lien the settlement could not pay, at the grid points, with the line's balances, units and route price. Millions of pounds per adult.
Run from the repository root:  python -I model/studies/household-arm-run/floor_diag.py [--paths N] [--market-paths] [--points a,b] [--out FILE.csv]
Writes FILE.csv (one row per phase, path, line and year of a floor line-year) and FILE_settle.csv (what stayed unpaid at a settlement); prints only summary lines. No headline number is read.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path.cwd()                                                              # the repository root
HERE = ROOT / 'docs' / 'model-v3' / 'household-arm-run'
sys.path[:0] = [str(ROOT / 'model'), str(ROOT / 'model' / 'studies' / 'household-arm-run')]

import run_grid as G                                                           # noqa: E402
from model_v3.runner import arm as ab                                          # noqa: E402

L = 14
rows, rest = [], []


class Log(ab.HouseholdHook):
    ph, name = 0, ''

    def _start(self, book):
        Log.ph += 1
        super()._start(book)

    def pre(self, book, t, g):
        out = super().pre(book, t, g)
        fl = np.asarray(self.fl, float)
        fam = np.asarray(book.family_true(), float)
        for i in np.flatnonzero(fl != 0):
            rows.append(dict(point=Log.name, phase=Log.ph, path=int(i // L), line=int(i % L), year=int(t), floor=float(fl[i]),
                             N1=float(-fl[i]), saving=float(self.acct['S'][i]), units_family=float(fam[i]), property=float(self.q['property'][i]),
                             net_financial=float(self.q['net_financial'][i]), physical=float(self.q['physical'][i]), pension=float(self.q['pension'][i]),
                             lien=float(self.PL[i]), lien_unit_part=float(self.PL[i] - self.PK[i]),
                             price=float(sum(x['V'][i] for r, x in book.R.items() if r != 'Cv')), f=float(sum(x['f'][i] for x in book.R.values())), s=float(sum(x['s'][i] for x in book.R.values())), sold=float(sum(x['sold'][i] for x in book.R.values()))))
        return out

    def settle(self, book):
        super().settle(book)
        for i in np.flatnonzero(np.asarray(self.unpaid) > 0):
            rest.append(dict(point=Log.name, phase=Log.ph, path=int(i // L), line=int(i % L), unpaid=float(self.unpaid[i]), lien=float(self.PL[i]), pension=float(self.q['pension'][i]),
                             nonpension=float(sum(self.q[k][i] for k in ab.CLASSES[:3]))))


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int, default=20)
    p.add_argument('--out', default='floor_lines.csv')
    p.add_argument('--market-paths', action='store_true')
    p.add_argument('--points', default=','.join(G.POINTS))
    a = p.parse_args(argv)
    ctx, inp = G.A.setup()
    manifest = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    orig = ab.HouseholdHook
    for name in a.points.split(','):
        Log.ph, Log.name = 0, name
        n0 = len(rows)
        ab.HouseholdHook = Log
        try:
            _, c = G.run_point(G.point_ctx(ctx, inp, name, a.market_paths), inp, name, manifest, a.paths, a.paths)
        finally:
            ab.HouseholdHook = orig
        print(name, 'floor line-years', len(rows) - n0, 'error', c.get('error'), flush=True)
    print('settle unpaid rows', len(rest))
    if rest:
        with open(a.out.replace('.csv', '_settle.csv'), 'w', newline='') as fh:
            w = csv.DictWriter(fh, list(rest[0]))
            w.writeheader()
            w.writerows(rest)
    cols = list(rows[0]) if rows else ['point']
    with open(a.out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main()
