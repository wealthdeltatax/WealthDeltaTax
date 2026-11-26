"""heads_only.py -- the saving of the headline-only evaluator (brief 151c block 2).  python model/studies/run-cost/heads_only.py [--out FILE] [--paths 20]
Household arm, median_mid, the spec of timing.py. The tornado (one schedule, 1 + 2 x read inputs evaluations) and one O1e root (tol 1.0, as the run uses for quick),
each with the full evaluator and with `make_ev(..., heads=True)`: wall seconds, best of REPS, the results compared to the last byte, and the ten largest own-time
functions (cProfile) of one tornado before and after. Set NPY_DISABLE_CPU_FEATURES=X86_V4 for every timing that is compared (151c re-release note)."""
from __future__ import annotations

import argparse, cProfile, importlib.util, json, os, pstats, sys, time
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


def top(f, n=10):
    pr = cProfile.Profile(); pr.enable(); f(); pr.disable()
    st = pstats.Stats(pr).stats
    rows = sorted(st.items(), key=lambda kv: -kv[1][2])[:n]
    return [dict(function=f'{Path(k[0]).name}:{k[1]}({k[2]})', calls=v[1], own_s=round(v[2], 2), cum_s=round(v[3], 2)) for k, v in rows]


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--out'); p.add_argument('--paths', type=int, default=20); a = p.parse_args(argv)
    ctx = T.build()[0]['household']
    eps = np.random.default_rng(T.SEED).standard_normal((R.T, a.paths))
    full, heads = R.make_ev(ctx, eps), R.make_ev(ctx, eps, heads=True)
    rows, spec = {i: ctx.reg[i] for i in ctx.tier1}, {'S': T.SPEC}
    work = {'tornado': lambda ev: S.tornado(ev, spec, rows, R.reads(ctx)),
            'one_o1e_root': lambda ev: S.breakeven(lambda m: S._mean(ev(T.SPEC, {R.RET['mean']: m})['M1']['short']), 0.0, 15.0, 1.0)}
    res = dict(paths=a.paths, numerics=os.environ.get('NPY_DISABLE_CPU_FEATURES', ''), cpu_count=os.cpu_count(), reps=T.REPS, seconds={}, identical={})
    for name, f in work.items():
        (tf, rf), (th, rh) = T.best(lambda: f(full)), T.best(lambda: f(heads))
        res['seconds'][name] = dict(full=round(tf, 2), heads=round(th, 2), saving=round(tf / th, 2)); res['identical'][name] = raw(rf) == raw(rh)
        print(name, res['seconds'][name], res['identical'][name], flush=True)
    res['profile_top10'] = dict(full=top(lambda: work['tornado'](full)), heads=top(lambda: work['tornado'](heads)))
    if a.out: Path(a.out).write_text(json.dumps(res, indent=1), encoding='utf-8')
    return 0 if all(res['identical'].values()) else 1


if __name__ == '__main__':
    sys.exit(main())
