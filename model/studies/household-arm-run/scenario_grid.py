"""
scenario_grid.py -- brief 147c block 3: one grid point, every `top_tail` setting crossed with every `saving_shape`, 20 paths. A row a cell:
 - untaxed concentration by year (0, 1, 10, 30, 100): the top-decile share (D10a, D10b and the named-list tiers) and the top-1% share (D10b and the tiers) of the arm's own household wealth, pension included, run with no tax through the arm's own step (the `none` comparator);
 - the saving floor (147c block 4): lines floored and the dissaving it removes, in points of the mean saving ratio;
 - from the run (run_grid checks): shortfall lines, `unpaid`, ledger tie, I1, the largest lien balance, and O1a (M1a) and O2 (M2, overall and the D10 band) by horizon (schedule S); a cell that stops reports its error and no run values (the concentration is still read).
Run from the repository root, one point a call:  python -I model/studies/household-arm-run/scenario_grid.py --point median_mid --out FILE.csv [--paths 20]
Each cell is a labelled scenario; nothing is fitted and no headline number is read.
"""
import argparse
import csv
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

ROOT = Path.cwd()
sys.path[:0] = [str(ROOT / 'model'), str(ROOT / 'model' / 'studies' / 'household-arm-run')]

import run_grid as G                                                           # noqa: E402
from model_v3.runner import arm as ab, runner as R, switches as sw            # noqa: E402

YEARS = (0, 1, 10, 30, 100)


class Log(ab.HouseholdHook):
    bal = 0.0

    def lien(self):
        out = super().lien()
        Log.bal = max(Log.bal, float(np.max(np.asarray(out['bal']))))
        return out


def concentration(ctx, c):
    """Untaxed top-decile and top-1% shares of household wealth at YEARS, from the arm's state through its own yearly step."""
    b = R.shaped(c, c.centre, G.A.SPEC['ratio'])
    h = ab.build(c.arm, c, c.centre, b).make()
    L, n, s = list(b.labels), b.adults_k, h.st
    top10, top1 = [L.index(x) for x in ('D10a', 'D10b', 'RL3', 'RL2', 'RL1')], [L.index(x) for x in ('D10b', 'RL3', 'RL2', 'RL1')]
    q, out = {**{k: np.asarray(v, float) for k, v in s['pos'].items()}, 'debt': np.zeros(len(s['income']))}, {}
    for t in range(max(YEARS) + 1):
        if t in YEARS:
            W = sum(q[k] for k in ab.CLASSES) * n
            out[t] = (float(W[top10].sum() / W.sum()), float(W[top1].sum() / W.sum()))
        inc = s['income'] * (1.0 + h.gr) ** t
        q1, _ = h._year(q, inc, s['sav'], s['acc'], ab.returns(q, h.gn))
        q, _, _ = ab.hh.apply_payment(q1, 0.0 * q1['property'], {k: np.maximum(q1[k], 0.0) for k in ab.CLASSES[:3]})
    return out, getattr(h, 'floor_report', None)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--paths', type=int, default=20)
    a = ap.parse_args(argv)
    ctx, inp = G.A.setup()
    manifest = yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())
    out, orig = [], ab.HouseholdHook
    for tail in sw.TAIL:
        for shape in sw.SHAPES:
            c = G.point_ctx(ctx, inp, a.point)
            c = replace(c, arm={**c.arm, 'top_tail': tail, 'saving_shape': shape})
            row = dict(point=a.point, top_tail=tail, saving_shape=shape)
            try:
                conc, rep = concentration(ctx, c)
                for t, (d, p) in conc.items():
                    row[f'top10_y{t}'], row[f'top1_y{t}'] = d, p
                row['lines_floored'], row['saving_added_pts'] = (rep['lines_floored'], rep['saving_added_pts']) if rep else (0, 0.0)
            except Exception as e:                                             # a setting that cannot be built
                row['error'] = f'concentration: {e}'
            Log.bal = 0.0
            ab.HouseholdHook = Log
            try:
                rows, k = G.run_point(c, inp, a.point, manifest, a.paths, a.paths)
            finally:
                ab.HouseholdHook = orig
            row.update(k)
            row['lien_bal_max'] = Log.bal
            if not k.get('error'):
                for r in rows:
                    if r['schedule'] == 'S' and (r['id'], r['by'] or '') in (('O1a', ''), ('O2', 'wealth_band=overall'), ('O2', 'wealth_band=D10')):
                        row[f"{r['id']}{'_' + r['by'].split('=')[1] if r['by'] else ''}_{r['horizon']}"] = float(r['a'])
            out.append(row)
            print(a.point, tail, shape, '|', (row.get('error') or 'ok')[:50], row.get('i1', '')[:4], row.get('shortfall_lines'), flush=True)
    cols = sorted({x for r in out for x in r})
    with open(a.out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(out)


if __name__ == '__main__':
    main()
