"""profile_after_154c.py -- brief 179c: where the time goes after 151c, 154c and 186c, and is it call overhead.  Measurement only; the model is not touched.
  python -I model/studies/run-cost/profile_after_154c.py scale  --out F    core_run and a full evaluation at 20 .. 1000 paths; t = a + b P fit (a: time that does not scale with the data)
  python -I model/studies/run-cost/profile_after_154c.py prof   --out F    cProfile of one full evaluation at 20 and 200 paths; numpy calls per simulated year; array sizes of the wrapped numpy functions
  python -I model/studies/run-cost/profile_after_154c.py floor  --out F    the same sizes in a tight loop: time per numpy call by size
  python -I model/studies/run-cost/profile_after_154c.py split  --out F [--workers W]   a `quick` run by part (level 1, map, tornado, O1e): wall seconds, one run
Household arm, median_mid, the spec of timing.py. Set NPY_DISABLE_CPU_FEATURES=X86_V4 (this file imports model_v3.numerics first, which does it)."""
from __future__ import annotations

import argparse, cProfile, importlib.util, json, pstats, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from model_v3 import numerics  # noqa: E402,F401  before numpy
import numpy as np  # noqa: E402

sp = importlib.util.spec_from_file_location('timing', HERE / 'timing.py'); T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
from model_v3.runner import runner as R  # noqa: E402
from model_v3.core import kernel as K  # noqa: E402

SPEC, SEED = T.SPEC, T.SEED


def household():
    return T.build()[0]['household']


def paths_for(n):
    return np.random.default_rng(SEED).standard_normal((R.T, n))


def scale(a):
    ctx, rows = household(), []
    for n in a.paths:
        eps = paths_for(n); ev = R.make_ev(ctx, eps); evh = R.make_ev(ctx, eps, heads=True)
        g = R.paths(eps, ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']])
        gdp_g = np.full(g.shape, ctx.gdp_g)
        ev(SPEC)                                                                                    # warm-up
        t_core, _ = T.best(lambda: R.core_run(ctx, ctx.centre, SPEC, g, gdp_g), reps=a.reps)
        t_heads, _ = T.best(lambda: evh(SPEC), reps=a.reps)
        t_full = T.best(lambda: ev(SPEC), reps=a.reps)[0] if n <= a.full_max else None     # the full evaluator at 1,000 paths holds every group's arrays and is OOM-killed on 8 GB
        rows.append(dict(paths=n, core_run_s=t_core, heads_eval_s=t_heads, full_eval_s=t_full)); print(rows[-1], flush=True)
    out = dict(rows=rows, fits=fit(rows))
    Path(a.out).write_text(json.dumps(out, indent=1)); print(json.dumps(out['fits'], indent=1))


def fit(rows):
    fits = {}
    for key in ('core_run_s', 'heads_eval_s', 'full_eval_s'):
        pts = [r for r in rows if r.get(key) is not None]
        x, y = np.array([r['paths'] for r in pts], float), np.array([r[key] for r in pts])
        b, c = np.polyfit(x, y, 1)
        fits[key] = dict(per_path_s=b, fixed_s=c, fixed_share_at={int(n): float(c / (c + b * n)) for n in x}, max_residual_pct=float(np.max(np.abs(c + b * x - y) / y) * 100))
    return fits


def refit(a):
    rows = [r for f in a.rows for r in json.loads(Path(f).read_text())['rows']]
    rows.sort(key=lambda r: r['paths']); Path(a.out).write_text(json.dumps(dict(rows=rows, fits=fit(rows)), indent=1))


class Sizes:
    """Counts and sizes of the first array argument of the wrapped numpy functions."""
    NAMES = ('where', 'asarray', 'zeros', 'maximum', 'minimum', 'array', 'any', 'abs', 'repeat', 'tile', 'ones', 'full', 'diff', 'isfinite', 'isnan', 'cumprod', 'sum', 'clip', 'zeros_like', 'concatenate', 'broadcast_to')

    def __init__(self):
        self.rec, self.orig = {}, {}

    def on(self):
        for nm in self.NAMES:
            f = getattr(np, nm); self.orig[nm] = f
            def w(*a, _f=f, _nm=nm, **k):
                x = a[0] if a else None
                s = x.size if isinstance(x, np.ndarray) else (len(x) if isinstance(x, (list, tuple)) else (1 if isinstance(x, (int, float, np.floating)) else -1))
                self.rec.setdefault(_nm, []).append(s)
                return _f(*a, **k)
            setattr(np, nm, w)

    def off(self):
        for nm, f in self.orig.items(): setattr(np, nm, f)


def prof(a):
    ctx, out = household(), {}
    for n in a.paths:
        ev = R.make_ev(ctx, paths_for(n)); ev(SPEC)
        steps = [0]; orig = K.step_year
        def counted(*x, **k):
            steps[0] += 1; return orig(*x, **k)
        K.step_year = counted
        pr = cProfile.Profile(); t = time.perf_counter(); pr.enable(); ev(SPEC); pr.disable(); wall = time.perf_counter() - t
        K.step_year = orig
        st = pstats.Stats(pr).stats
        total_own = sum(v[2] for v in st.values())
        top = sorted(st.items(), key=lambda kv: -kv[1][2])[:20]
        builtin = {k: v for k, v in st.items() if k[0] == '~'}
        np_calls = sum(v[1] for k, v in builtin.items() if any(s in k[2] for s in ('numpy', 'ufunc', 'ndarray', 'multiarray')))
        np_own = sum(v[2] for k, v in builtin.items() if any(s in k[2] for s in ('numpy', 'ufunc', 'ndarray', 'multiarray')))
        all_builtin_own = sum(v[2] for v in builtin.values())
        sz = Sizes(); sz.on()
        try: ev(SPEC)
        finally: sz.off()
        flat = np.array([s for v in sz.rec.values() for s in v if s >= 0])
        out[str(n)] = dict(
            wall_unprofiled_note='profiled wall includes cProfile overhead', profiled_wall_s=wall, step_year_calls=steps[0],
            top20=[dict(function=f'{Path(k[0]).name}:{k[1]}({k[2]})', calls=v[1], own_s=round(v[2], 3), cum_s=round(v[3], 3)) for k, v in top],
            numpy_builtin_calls=int(np_calls), numpy_calls_per_step_year=float(np_calls / max(1, steps[0])), numpy_builtin_own_s=np_own, all_builtin_own_s=all_builtin_own,
            python_and_operator_own_s=total_own - all_builtin_own, total_own_s=total_own,
            wrapped_calls=int(flat.size), wrapped_median_size=float(np.median(flat)), wrapped_p90_size=float(np.percentile(flat, 90)), wrapped_share_under_1000=float((flat < 1000).mean()),
            wrapped_by_function={k: dict(calls=len(v), median_size=float(np.median([s for s in v if s >= 0] or [0]))) for k, v in sorted(sz.rec.items(), key=lambda kv: -len(kv[1]))[:10]})
        print(n, out[str(n)]['profiled_wall_s'], out[str(n)]['numpy_calls_per_step_year'], out[str(n)]['wrapped_median_size'], flush=True)
    Path(a.out).write_text(json.dumps(out, indent=1))


def floor(a):
    out = {}
    for n in a.sizes:
        x, y = np.random.default_rng(1).standard_normal(n), np.random.default_rng(2).standard_normal(n)
        reps = max(2000, 2_000_000 // max(n, 1))
        ops = {'add': lambda: x + y, 'mul': lambda: x * y, 'maximum': lambda: np.maximum(x, 0.0), 'where': lambda: np.where(x > 0, x, y), 'sum': lambda: x.sum(), 'zeros': lambda: np.zeros(n), 'asarray': lambda: np.asarray(x)}
        out[str(n)] = {}
        for k, f in ops.items():
            f(); t = time.perf_counter()
            for _ in range(reps): f()
            out[str(n)][k] = (time.perf_counter() - t) / reps
        print(n, {k: f'{v * 1e6:.2f} us' for k, v in out[str(n)].items()}, flush=True)
    Path(a.out).write_text(json.dumps(out, indent=1))


def split(a):
    """A `quick` run by part, by wrapping the run script's own calls; one run, wall seconds."""
    from model_v3 import run
    from model_v3.runner import sweeps as S
    acc, calls = {}, {}

    def wrap(mod, name, key):
        orig = getattr(mod, name)
        def f(*x, **k):
            t = time.perf_counter(); r = orig(*x, **k); acc[key] = acc.get(key, 0.0) + time.perf_counter() - t; calls[key] = calls.get(key, 0) + 1; return r
        setattr(mod, name, f)
    wrap(R, 'level1', 'level1'); wrap(S, 'tornado', 'tornado'); wrap(S, 'breakeven_return', 'o1e_roots')
    for nm in dir(S):
        if 'feas' in nm.lower() or 'map' in nm.lower():
            if callable(getattr(S, nm)): wrap(S, nm, 'map:' + nm)
    for nm in dir(R):
        if 'feas' in nm.lower() and callable(getattr(R, nm)): wrap(R, nm, 'map:' + nm)
    t = time.perf_counter()
    run.main(['--size', 'quick', '--out', a.run_dir, '--workers', str(a.workers)])
    out = dict(workers=a.workers, total_s=time.perf_counter() - t, parts_s=acc, calls=calls)
    Path(a.out).write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))


def main(argv=None):
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('scale'); s.add_argument('--out', required=True); s.add_argument('--paths', type=int, nargs='*', default=[20, 50, 100, 200, 500, 1000]); s.add_argument('--reps', type=int, default=2); s.add_argument('--full-max', type=int, default=500); s.set_defaults(f=scale)
    s = sub.add_parser('refit'); s.add_argument('--out', required=True); s.add_argument('--rows', nargs='+', required=True); s.set_defaults(f=refit)
    s = sub.add_parser('prof'); s.add_argument('--out', required=True); s.add_argument('--paths', type=int, nargs='*', default=[20, 200]); s.set_defaults(f=prof)
    s = sub.add_parser('floor'); s.add_argument('--out', required=True); s.add_argument('--sizes', type=int, nargs='*', default=[20, 100, 280, 1000, 10000, 100000]); s.set_defaults(f=floor)
    s = sub.add_parser('split'); s.add_argument('--out', required=True); s.add_argument('--workers', type=int, default=1); s.add_argument('--run-dir', required=True); s.set_defaults(f=split)
    a = p.parse_args(argv); a.f(a)


if __name__ == '__main__':
    main()
