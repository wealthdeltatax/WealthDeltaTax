#!/usr/bin/env python3
"""root_methods.py -- brief 153c: bisection against Illinois steps for the O1e roots, same run, same draws, on the real model.

    python -I model/studies/run-cost/root_methods.py --size quick|smoke|probe20 [--o1e-draws N] [--workers 1] --out DIR

Runs run.py with `--parts map,o1e` once per `--root-method` (bisect, illinois), counting the evaluations of every root (`sweeps.breakeven` is wrapped; serial only), and writes
DIR/root-methods-<size>.json: per method the outputs' O1e cells, the evaluations per root, wall seconds. `report` (below) makes the per-cell difference table."""
from __future__ import annotations
import os
os.environ.setdefault('NPY_DISABLE_CPU_FEATURES', 'X86_V4')
import argparse, json, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'model'))
from model_v3 import run
from model_v3.runner import sweeps as S


run.SIZES['probe20'] = (50, 20, 6, 1e-2, 1)   # 20 tornado/root paths, 6 draws, the quick tolerance 1e-2, one point: the brief's "20-path draws" at a tolerance where the rule bites


def go(size, draws, method):
    orig, log = S.breakeven, []
    def counted(f, lo, hi, tol=1e-3, maxit=60, method='bisect'):
        n = [0]
        def g(x): n[0] += 1; return f(x)
        r = orig(g, lo, hi, tol, maxit, method); log.append(dict(root=r, evals=n[0])); return r
    S.breakeven = counted
    try:
        with tempfile.TemporaryDirectory() as d:
            t = time.perf_counter()
            run.main(['--size', size, '--parts', 'map,o1e', '--workers', '1', '--root-method', method, '--out', d] + (['--o1e-draws', str(draws)] if draws is not None else []))
            secs = time.perf_counter() - t
            doc = json.loads((Path(d) / 'outputs.json').read_text())
    finally:
        S.breakeven = orig
    return dict(method=method, seconds=secs, roots=log, o1e=doc['outputs']['O1e'], run=doc['run'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--size', default='quick'); p.add_argument('--o1e-draws', type=int); p.add_argument('--out', required=True)
    p.add_argument('--tag'); a = p.parse_args()
    res = {m: go(a.size, a.o1e_draws, m) for m in ('bisect', 'illinois')}
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    f = out / f'root-methods-{a.tag or a.size}.json'; f.write_text(json.dumps(res, indent=1)); print('wrote', f)
    for m, r in res.items():
        ev = [x['evals'] for x in r['roots']]; print(m, f'{r["seconds"]:.0f} s', 'roots', len(ev), 'evaluations', sum(ev), 'per root', round(sum(ev) / max(1, len(ev)), 2))
