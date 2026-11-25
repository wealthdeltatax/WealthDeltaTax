"""
scenario_before_after.py -- brief 139c, block 3: the five grid points at 20 paths, one row a point: the run_grid checks (account residual, unpaid, unpaid_B, shortfall lines, ledger ties, I1), the pension lien (instances, largest balance,
settled from the classes and from the pension; millions of pounds per adult, real) and the mean of O1a (M1a) (% of GDP, schedule S) by horizon. Run from the repository root, once a configuration:
python -I model/studies/household-arm-run/scenario_before_after.py --tag NAME [--lien low|central|high] [--paths N] [--out FILE.csv]
`--lien` sets the arm's `lien_rate` switch (139c); on a tree before 139c the key is ignored, so that run is the before (six death phases, no accrual). No headline number is read.
"""
import argparse
import csv
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

ROOT = Path.cwd()                                                              # the repository root
sys.path[:0] = [str(ROOT), str(ROOT / 'docs' / 'model-v3' / 'household-arm-run')]

import run_grid as G                                                           # noqa: E402
from model_v3.runner import arm as ab                                          # noqa: E402


class Log(ab.HouseholdHook):
    n, bal, c, p = 0, 0.0, 0.0, 0.0

    def lien(self):
        out = super().lien()
        bal = np.zeros(len(self.PL)) + np.asarray(out['bal'])
        Log.bal = max(Log.bal, float(bal.max()))
        Log.c += float(np.sum(self.set_c)) if np.ndim(self.set_c) else 0.0
        Log.p += float(np.sum(self.set_p)) if np.ndim(self.set_p) else 0.0
        return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True)
    ap.add_argument('--lien', default=None)
    ap.add_argument('--paths', type=int, default=20)
    ap.add_argument('--out', default=None)
    a = ap.parse_args(argv)
    ctx, inp = G.A.setup()
    manifest = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    out, orig = [], ab.HouseholdHook
    for name in G.POINTS:
        c = G.point_ctx(ctx, inp, name)
        c = c if a.lien is None else replace(c, arm={**c.arm, 'lien_rate': a.lien})
        Log.bal = Log.c = Log.p = 0.0
        ab.HouseholdHook = Log
        try:
            rows, k = G.run_point(c, inp, name, manifest, a.paths, a.paths)
        finally:
            ab.HouseholdHook = orig
        m = {r['horizon']: r['a'] for r in rows if r['id'] == 'O1a' and r['schedule'] == 'S'}
        row = dict(tag=a.tag, **k, lien_bal_max=Log.bal, settled_classes=Log.c, settled_pension=Log.p, **{f'O1a_{h}': m.get(h) for h in ('transition', 'short', 'long')})
        out.append(row)
        print(a.tag, name, {x: row.get(x) for x in ('shortfall_lines', 'unpaid_max', 'unpaid_B_max', 'ledger_tie_max', 'i1', 'error')}, flush=True)
    cols = sorted({x for r in out for x in r})
    if a.out:
        with open(a.out, 'w', newline='') as fh:
            w = csv.DictWriter(fh, cols)
            w.writeheader()
            w.writerows(out)


if __name__ == '__main__':
    main()
