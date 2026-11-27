"""map_only.py -- the saving of running only the OF1 group for the feasibility map (brief 186c).  python model/studies/run-cost/map_only.py [--out FILE] [--paths 50] [--workers 1 0] [--reps 1]
Household arm, median_mid. One map point (the timing.py spec) and the whole `quick` map (the lever grid, 50 tornado paths as run.py's quick size), each with the full evaluator and with
`make_ev(..., only=('sweeps',))`: wall seconds, the results compared to the last byte. Set NPY_DISABLE_CPU_FEATURES=X86_V4 for every timing that is compared."""
from __future__ import annotations

import argparse, importlib.util, json, os, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('timing', HERE / 'timing.py'); T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
sp = importlib.util.spec_from_file_location('heads_only', HERE / 'heads_only.py'); H = importlib.util.module_from_spec(sp); sp.loader.exec_module(H)
from model_v3.runner import runner as R, sweeps as S   # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--out'); p.add_argument('--paths', type=int, default=50); p.add_argument('--workers', type=int, nargs='*', default=[1, 0]); p.add_argument('--reps', type=int, default=1)
    a = p.parse_args(argv)
    ctx = T.build()[0]['household']
    lv = json.loads(T.LEVERS.read_text(encoding='utf-8')); grid = S.grid(lv)
    eps = np.random.default_rng(T.SEED).standard_normal((R.T, a.paths))
    full, part = R.make_ev(ctx, eps), R.make_ev(ctx, eps, only=('sweeps',))
    res = dict(paths=a.paths, grid_points=len(grid), numerics=os.environ.get('NPY_DISABLE_CPU_FEATURES', ''), cpu_count=os.cpu_count(), reps=a.reps, seconds={}, identical={})
    work = {'one_point': lambda ev, w: S.feasibility(ev, [grid[0]], 1)}
    for w in a.workers: work[f'whole_map_workers_{w}'] = (lambda w: lambda ev, _: S.feasibility(ev, grid, w))(w)
    for name, f in work.items():
        (tf, rf), (to, ro) = T.best(lambda: f(full, 1), a.reps), T.best(lambda: f(part, 1), a.reps)
        res['seconds'][name] = dict(full=round(tf, 1), only_sweeps=round(to, 1), saving=round(tf / to, 2)); res['identical'][name] = H.raw(rf[1]) == H.raw(ro[1]) and H.raw(rf[0]) == H.raw(ro[0])
        print(name, res['seconds'][name], res['identical'][name], flush=True)
    if a.out: Path(a.out).write_text(json.dumps(res, indent=1), encoding='utf-8')
    return 0 if all(res['identical'].values()) else 1


if __name__ == '__main__':
    sys.exit(main())
