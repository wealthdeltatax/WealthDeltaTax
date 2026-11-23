"""speedup.py -- speed-up of the sweeps by worker count (brief 150c block 3).  python docs/model-v3/run-cost/speedup.py [--out FILE]
Household arm, median_mid, 20 paths, spec of timing.py. Workload A: the tornado, one schedule (1 + 2 x 5 read inputs = 11 evaluations). Workload B: O1e roots, one schedule,
point and 6 draws (7 roots). Wall seconds per worker count; the results of each count are compared with the serial ones to the last digit."""
from __future__ import annotations

import argparse, importlib.util, json, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('timing', HERE / 'timing.py'); T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
from model_v3.runner import runner as R, sweeps as S   # noqa: E402


def raw(x):
    if isinstance(x, dict): return b'{' + b','.join(raw(k) + b':' + raw(v) for k, v in x.items()) + b'}'
    if isinstance(x, (list, tuple)): return b'[' + b','.join(raw(v) for v in x) + b']'
    if isinstance(x, np.ndarray): return x.dtype.str.encode() + repr(x.shape).encode() + x.tobytes()
    return float(x).hex().encode() if isinstance(x, (float, np.floating)) else repr(x).encode()


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--out'); p.add_argument('--workers', type=int, nargs='*', default=[1, 2, 4]); p.add_argument('--paths', type=int, default=20)
    a = p.parse_args(argv)
    ctx = T.build()[0]['household']
    ev = R.make_ev(ctx, np.random.default_rng(T.SEED).standard_normal((R.T, a.paths)))
    rows, spec = {i: ctx.reg[i] for i in ctx.tier1}, {'S': T.SPEC}
    draws = R.draw_theta(np.random.default_rng(T.SEED + 1), ctx, ctx.tier1, 6)
    work = {'tornado': lambda w: S.tornado(ev, spec, rows, R.reads(ctx), workers=w),
            'o1e_roots': lambda w: S.breakeven_return(ev, spec, R.RET['mean'], draws=draws, tol=1.0, workers=w)}
    res = {'paths': a.paths, 'cpu_count': __import__('os').cpu_count(), 'seconds': {}, 'identical_to_serial': {}}
    for name, f in work.items():
        base = None
        for w in a.workers:
            t = time.perf_counter(); r = f(w); dt = time.perf_counter() - t
            base = raw(r) if base is None else base
            res['seconds'].setdefault(name, {})[w] = dt; res['identical_to_serial'].setdefault(name, {})[w] = raw(r) == base
            print(name, w, f'{dt:.1f}s', raw(r) == base, flush=True)
    if a.out: Path(a.out).write_text(json.dumps(res, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
