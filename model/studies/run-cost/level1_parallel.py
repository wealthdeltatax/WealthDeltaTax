"""level1_parallel.py -- level 1 through the parallel map (brief 154c). python model/studies/run-cost/level1_parallel.py [--out FILE]
`level1_3sched_1000`: level 1, three schedules, 1,000 paths (one chunk: `runner.CHUNK` = 1,000), household arm, median_mid, the three units of a quick point (chunk, schedule); workers 1, 2 and 0 (one per core): wall seconds (one run each),
the Samples and info compared to the last byte against workers 1. Set NPY_DISABLE_CPU_FEATURES=X86_V4 for every timing that is compared (151c re-release note)."""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('timing', HERE / 'timing.py'); T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
sp = importlib.util.spec_from_file_location('heads_only', HERE / 'heads_only.py'); H = importlib.util.module_from_spec(sp); sp.loader.exec_module(H)
from model_v3.core import returns as rt   # noqa: E402
from model_v3.runner import runner as R   # noqa: E402


def one(w, paths):
    """One worker count in its own process: a parent that has run level 1 serially keeps its 3 GB, and the forked workers then run out of memory together."""
    ctx = T.build()[0]['household']
    named = {'S_low': dict(T.SPEC, tau_m=0.5), 'S_central': dict(T.SPEC, tau_m=0.7), 'S_high': dict(T.SPEC, tau_m=0.9)}
    t, out = T.best(lambda: R.level1(ctx, named, rt.streams(T.SEED)['level1_paths'], n=paths, workers=w), reps=1)
    print(json.dumps(dict(seconds=round(t, 2), digest=hashlib.sha256(H.raw(out)).hexdigest())))


def main(argv=None):
    p = argparse.ArgumentParser(); p.add_argument('--out'); p.add_argument('--paths', type=int, default=1000); p.add_argument('--one', type=int); a = p.parse_args(argv)
    if a.one is not None:
        return one(a.one, a.paths)
    res = dict(paths=a.paths, chunk=R.CHUNK, numerics=os.environ.get('NPY_DISABLE_CPU_FEATURES', ''), cpu_count=os.cpu_count(), reps=1, level1_3sched_1000={}, identical_to_workers_1={})
    base = None
    for w in (1, 2, 0):
        r = json.loads(subprocess.run([sys.executable, __file__, '--one', str(w), '--paths', str(a.paths)], capture_output=True, text=True, check=True).stdout.splitlines()[-1])
        base = r['digest'] if base is None else base
        res['level1_3sched_1000'][f'workers_{w}'] = r['seconds']; res['identical_to_workers_1'][f'workers_{w}'] = r['digest'] == base
        print(f'workers {w}: {r["seconds"]} s, identical {r["digest"] == base}', flush=True)
    s = res['level1_3sched_1000']; res['saving_workers_0'] = round(s['workers_1'] / s['workers_0'], 2)
    if a.out: Path(a.out).write_text(json.dumps(res, indent=1), encoding='utf-8')
    return 0 if all(res['identical_to_workers_1'].values()) else 1


if __name__ == '__main__':
    sys.exit(main())
