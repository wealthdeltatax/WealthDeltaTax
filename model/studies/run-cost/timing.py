"""timing.py -- run cost of model_v3 (brief 150c block 1).  python model/studies/run-cost/timing.py [--out FILE]
Times, on both arms at the median_mid grid point and the spec tau_m 0.5, k_ln 0.5, ratio 1.0: one evaluation at 20 and 200 paths with the cost split by output group,
the level 1 run, one O1e root, and the statics. Wall time per call (time.perf_counter), best of REPS. Writes JSON; run-cost.md quotes it."""
from __future__ import annotations

import argparse, json, sys, time
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'model'))
from model_v3.core import pack as pk, returns as rt                      # noqa: E402
from model_v3.out import assemble as asm                                  # noqa: E402
from model_v3.runner import runner as R, sweeps as S                      # noqa: E402
from model_v3.runner.groups import GROUPS                                 # noqa: E402

MANIFEST, INPUTS, LEVERS = ROOT / 'docs/model-v3/outputs.yml', ROOT / 'data/input-register/inputs.json', ROOT / 'model/model_v3/levers.json'
HH_INPUTS, PACKS = ROOT / 'docs/model-v3/cell-baseline/inputs_used.json', ROOT / 'model_v3/pack'
SPEC, SEED, REPS = dict(tau_0=0.04, tau_m=0.5, k_ln=0.5, ratio=1.0), 20261118, 2


def build():
    man, lv = yaml.safe_load(MANIFEST.read_text(encoding='utf-8')), json.loads(LEVERS.read_text(encoding='utf-8'))
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    once = [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
    ctx = R.context(pk.load_pack(next(d for d in sorted(PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(INPUTS), lv, tier1, list(asm.entries(man)), once)
    inp = json.loads(HH_INPUTS.read_text(encoding='utf-8'))
    return {'household': replace(ctx, arm=dict(arm='household', inputs=inp, saving='median', regime='mid')), 'legacy': ctx}, man


def best(f, reps=REPS):
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); r = f(); ts.append(time.perf_counter() - t)
    return min(ts), r


def split(ctx, n):
    """Seconds of one evaluation at n paths by part: core_run (all runs, `again` included), headlines, each group's per_path (own time, core runs inside `again` excluded)."""
    eps = np.random.default_rng(SEED).standard_normal((R.T, n))
    acc = {}

    def wrap(mod, name, key):
        orig = getattr(mod, name)
        def f(*a, **k):
            t = time.perf_counter(); r = orig(*a, **k); acc[key] = acc.get(key, 0.0) + time.perf_counter() - t; acc[key + '_calls'] = acc.get(key + '_calls', 0) + 1; return r
        setattr(mod, name, f)
        return lambda: setattr(mod, name, orig)
    undo = [wrap(R, 'core_run', 'core_run'), wrap(R, 'headlines', 'headlines')]
    for m in GROUPS:
        undo.append(wrap(m, 'per_path', m.NAME))
    try:
        ev = R.make_ev(ctx, eps)
        t = time.perf_counter(); ev(SPEC); tot = time.perf_counter() - t
    finally:
        for u in undo: u()
    out = {'total': tot, 'core_run': acc.get('core_run', 0.0), 'core_run_calls': acc.get('core_run_calls', 0), 'headlines': acc.get('headlines', 0.0)}
    out.update({m.NAME + '_incl_again': acc.get(m.NAME, 0.0) for m in GROUPS})
    out['groups_own'] = {m.NAME: acc.get(m.NAME, 0.0) for m in GROUPS}
    return out


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--out', default=None); p.add_argument('--paths', type=int, nargs='*', default=[20, 200]); p.add_argument('--quick', action='store_true', help='the cost split only')
    a = p.parse_args(argv)
    ctxs, man = build()
    res = {'cpu_count': __import__('os').cpu_count(), 'spec': SPEC, 'arms': {}}
    for arm, ctx in ctxs.items():
        r = res['arms'][arm] = {}
        for n in a.paths:
            eps = np.random.default_rng(SEED).standard_normal((R.T, n))
            ev = R.make_ev(ctx, eps)
            ev(SPEC)   # warm-up
            if a.quick:
                r[f'split_{n}'] = split(ctx, n); continue
            t_ev, _ = best(lambda: ev(SPEC))
            r[f'eval_{n}'] = t_ev
            r[f'split_{n}'] = split(ctx, n)
            calls = []
            def f(m):
                calls.append(m); return float(np.nanmean(ev(SPEC, {R.RET['mean']: m})['M1']['short']))
            t = time.perf_counter()
            try:
                S.breakeven(f, 0.0, 15.0, 1e-2); r[f'o1e_root_{n}_error'] = None
            except ValueError as exc:   # the legacy arm's welfare solver cannot reach its target at an end of the bracket: recorded, not repaired
                r[f'o1e_root_{n}_error'] = str(exc)[:120]
            t_root = time.perf_counter() - t
            r[f'o1e_root_{n}'], r[f'o1e_root_{n}_evals'] = t_root, len(calls)
            print(arm, n, f'eval {t_ev:.2f}s root {t_root:.1f}s in {len(calls)} evals', flush=True)
        if a.quick: continue
        st = rt.streams(SEED)
        r['level1_n1000'] = best(lambda: R.level1(ctx, {'S_central': SPEC}, st['level1_paths'], n=1000), reps=1)[0]
        r['statics'] = best(lambda: R.statics(ctx, ctx.centre), reps=1)[0]
    if a.out: Path(a.out).write_text(json.dumps(res, indent=1), encoding='utf-8')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
