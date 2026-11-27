#!/usr/bin/env python3
"""bench.py -- one measurement and one proof for every speed-up (brief 176c).

    python -I model/studies/run-cost/bench.py run --out FILE [--cases a,b] [--reps N] [--workers N]
    python -I model/studies/run-cost/bench.py compare BEFORE AFTER [--force]
    python -I model/studies/run-cost/bench.py list

`run` times named cases with fixed specs and seeds, best of `--reps` (default 2; `quick_full` default 1, it takes about an hour), and hashes each result (floats by hex,
arrays by dtype, shape and buffer; the same rule as tests/model/model_v3/test_pool.py). The file starts with a header: CPU model, cores, memory, numpy version,
NPY_DISABLE_CPU_FEATURES, git SHA (and whether the tree was dirty), worker count. `compare` prints per case the time ratio AFTER/BEFORE and `identical: yes/no` and exits 1
if any common case is not identical; it refuses to compare files whose CPU model, numpy version or NPY_DISABLE_CPU_FEATURES differ unless `--force`, and says so.
Default (small) cases: eval_hh_20 and eval_leg_20 (one evaluation, household and legacy arm, 20 paths); root_1_20 (one O1e root): about 40 s per pass on two cores.
On request (--cases): tornado_1sched_20 (one schedule: 11 evaluations, about 2.5 min); level1_1sched_1000 (about 2 min); quick_headlines (needs run.py's --parts switch, brief 178c: unavailable before it); quick_full (run.py --size quick; the hash is of outputs.json with
the run date masked). A change that touches the tornado or level 1 runs those two as well.
Set NPY_DISABLE_CPU_FEATURES=X86_V4 in the shell if you want to be sure: this script sets it with setdefault before numpy is imported, as model_v3.numerics does.
"""
from __future__ import annotations

import os
os.environ.setdefault('NPY_DISABLE_CPU_FEATURES', 'X86_V4')               # before numpy, as model_v3.numerics does

import argparse, dataclasses, hashlib, json, platform, re, subprocess, sys, tempfile, time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SPEC, SEED = dict(tau_0=0.04, tau_m=0.5, k_ln=0.5, ratio=1.0), 20261118      # the timing.py spec and seed
SMALL = ['eval_hh_20', 'eval_leg_20', 'root_1_20']                           # the default set: about 40 s per pass, two minutes with the warm-up and two reps
MEDIUM = ['tornado_1sched_20', 'level1_1sched_1000']                      # on request (--cases): about 143 s and 129 s per pass
ALL = SMALL + MEDIUM + ['quick_headlines', 'quick_full']
NUMERICS = ('cpu_model', 'numpy', 'NPY_DISABLE_CPU_FEATURES')                # a difference here can move the numbers: compare refuses


def raw(x):
    """The bytes of a nested result: floats by hex, arrays by dtype, shape and buffer. (Not pickle: its bytes differ with how objects are shared.)"""
    if isinstance(x, dict):
        return b'{' + b','.join(raw(k) + b':' + raw(v) for k, v in x.items()) + b'}'
    if isinstance(x, (list, tuple)):
        return b'[' + b','.join(raw(v) for v in x) + b']'
    if isinstance(x, np.ndarray):
        return x.dtype.str.encode() + repr(x.shape).encode() + np.ascontiguousarray(x).tobytes()
    if isinstance(x, (float, np.floating)):
        return float(x).hex().encode()
    if dataclasses.is_dataclass(x) and not isinstance(x, type):
        return type(x).__name__.encode() + raw({f.name: getattr(x, f.name) for f in dataclasses.fields(x)})
    if hasattr(x, '_asdict'):
        return raw(x._asdict())
    if hasattr(x, '__dict__') and not callable(x):
        return type(x).__name__.encode() + raw(vars(x))
    return repr(x).encode()


def mask_date(b):
    """The bytes of an outputs.json with the run date masked (the only field that differs between two runs of the same code on different days)."""
    return re.sub(rb'("run_date":\s*")\d{4}-\d{2}-\d{2}', rb'\1DATE', b)


def digest(x):
    return hashlib.sha256(raw(x)).hexdigest()


def header(workers):
    def first(path, key):
        try:
            return next(l.split(':', 1)[1].strip() for l in Path(path).read_text().splitlines() if l.startswith(key))
        except (OSError, StopIteration):
            return 'unknown'
    git = lambda *a: subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True, text=True).stdout.strip()
    return {'cpu_model': first('/proc/cpuinfo', 'model name') if platform.system() == 'Linux' else platform.processor(),
            'cores': os.cpu_count(), 'memory': first('/proc/meminfo', 'MemTotal'), 'numpy': np.__version__, 'python': platform.python_version(),
            'NPY_DISABLE_CPU_FEATURES': os.environ.get('NPY_DISABLE_CPU_FEATURES', 'unset'),
            'git_sha': git('rev-parse', 'HEAD'), 'git_dirty': bool(git('status', '--porcelain', '--untracked-files=no')), 'workers': workers}


# ---- the cases: each returns (callable to time, setup done once outside the timing); the callable returns the result to hash -------------------------------------------------

def _model():
    sys.path.insert(0, str(ROOT / 'model'))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import importlib.util
    sp = importlib.util.spec_from_file_location('timing', Path(__file__).resolve().parent / 'timing.py')
    T = importlib.util.module_from_spec(sp); sp.loader.exec_module(T)
    from model_v3.runner import runner as R, sweeps as S
    from model_v3.core import returns as rt
    return T, R, S, rt


def build_case(name, workers):
    """(f, warm): f() returns the result; warm says whether one untimed call comes first."""
    if name == 'quick_full':
        def f():
            from importlib import import_module
            sys.path.insert(0, str(ROOT / 'model'))
            run = import_module('model_v3.run')
            with tempfile.TemporaryDirectory() as d:
                run.main(['--size', 'quick', '--workers', str(workers), '--out', d])
                b = (Path(d) / 'outputs.json').read_bytes()
            return mask_date(b).hex()   # the bytes, run date masked; digest() then hashes the hex text
        return f, False
    if name == 'quick_headlines':
        if '--parts' not in (ROOT / 'model/model_v3/run.py').read_text(encoding='utf-8'):
            raise LookupError('quick_headlines needs the --parts switch of run.py (brief 178c)')
        def f():
            sys.path.insert(0, str(ROOT / 'model'))
            from importlib import import_module
            run = import_module('model_v3.run')
            with tempfile.TemporaryDirectory() as d:
                run.main(['--size', 'quick', '--parts', 'headlines', '--workers', str(workers), '--out', d])
                b = (Path(d) / 'outputs.json').read_bytes()
            return mask_date(b).hex()
        return f, False
    T, R, S, rt = _model()
    ctxs = T.build()[0]
    eps = np.random.default_rng(SEED).standard_normal((R.T, 20))
    if name in ('eval_hh_20', 'eval_leg_20'):
        ev = R.make_ev(ctxs['household' if name == 'eval_hh_20' else 'legacy'], eps)
        return (lambda: ev(SPEC)), True
    ctx = ctxs['household']
    ev = R.make_ev(ctx, eps)
    if name == 'tornado_1sched_20':
        rows = {i: ctx.reg[i] for i in ctx.tier1}
        return (lambda: S.tornado(ev, {'S': SPEC}, rows, R.reads(ctx), workers=workers)), True
    if name == 'root_1_20':
        return (lambda: S.breakeven_return(ev, {'S': SPEC}, R.RET['mean'], workers=workers)), True
    if name == 'level1_1sched_1000':
        st = rt.streams(SEED)
        return (lambda: R.level1(ctx, {'S_central': SPEC}, st['level1_paths'], n=1000)), False
    raise LookupError(f'unknown case {name!r}; cases: {", ".join(ALL)}')


def run_cases(names, reps, workers):
    out = {}
    for n in names:
        r = reps if reps else (1 if n == 'quick_full' or n == 'quick_headlines' else 2)
        try:
            f, warm = build_case(n, workers)
            if warm:
                f()
            ts, res = [], None
            for _ in range(r):
                t = time.perf_counter(); res = f(); ts.append(time.perf_counter() - t)
            out[n] = {'seconds': min(ts), 'all_seconds': ts, 'reps': r, 'hash': digest(res)}
            print(f'{n:22} {min(ts):9.2f} s  best of {r}  {out[n]["hash"][:12]}', flush=True)
        except LookupError as e:
            out[n] = {'unavailable': str(e)}; print(f'{n:22} unavailable: {e}', flush=True)
    return out


# ---- compare -------------------------------------------------------------------------------------------------------------------------------------------------------------------

def compare(a, b, force=False, say=print):
    """Return 0 if every common case is identical, 1 if one is not, 2 if the files cannot be compared. `say` receives each output line."""
    diff = [k for k in NUMERICS if a['header'].get(k) != b['header'].get(k)]
    if diff and not force:
        say('REFUSED: the files differ in ' + ', '.join(f'{k} ({a["header"].get(k)!r} against {b["header"].get(k)!r})' for k in diff) + '; the numbers may differ for that reason alone. Use --force to compare anyway.')
        return 2
    if diff:
        say('FORCED: comparing across ' + ', '.join(diff) + '; an `identical: no` below may be the platform, not the change.')
    for k in ('cores', 'workers', 'memory'):
        if a['header'].get(k) != b['header'].get(k):
            say(f'WARNING: {k} differs ({a["header"].get(k)!r} against {b["header"].get(k)!r}): the time ratios are not like for like.')
    bad = 0
    for n in a['cases']:
        x, y = a['cases'][n], b['cases'].get(n)
        if y is None or 'seconds' not in x or 'seconds' not in y:
            say(f'{n:22} not in both files'); continue
        same = x['hash'] == y['hash']
        bad += not same
        say(f'{n:22} before {x["seconds"]:9.2f} s  after {y["seconds"]:9.2f} s  ratio {y["seconds"] / x["seconds"]:6.3f}  identical: {"yes" if same else "no"}')
    for n in b['cases']:
        if n not in a['cases']:
            say(f'{n:22} only in the second file')
    return 1 if bad else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = p.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run'); r.add_argument('--out', required=True); r.add_argument('--cases', default=','.join(SMALL)); r.add_argument('--reps', type=int); r.add_argument('--workers', type=int, default=1)
    c = sub.add_parser('compare'); c.add_argument('before'); c.add_argument('after'); c.add_argument('--force', action='store_true')
    sub.add_parser('list')
    a = p.parse_args(argv)
    if a.cmd == 'list':
        print('small (default):', ', '.join(SMALL)); print('medium, on request:', ', '.join(MEDIUM)); print('long, on request: quick_headlines, quick_full'); return 0
    if a.cmd == 'compare':
        load = lambda f: json.loads(Path(f).read_text(encoding='utf-8'))
        return compare(load(a.before), load(a.after), a.force)
    names = [n.strip() for n in a.cases.split(',') if n.strip()]
    unknown = [n for n in names if n not in ALL]
    if unknown:
        sys.exit(f'unknown case {unknown}; cases: {", ".join(ALL)}')
    h = header(a.workers)
    if h['NPY_DISABLE_CPU_FEATURES'] != 'X86_V4':
        print(f'WARNING: NPY_DISABLE_CPU_FEATURES is {h["NPY_DISABLE_CPU_FEATURES"]!r}, not the pinned X86_V4: results are not comparable with the pins.')
    t0 = time.perf_counter()
    res = {'header': h, 'cases': run_cases(names, a.reps, a.workers)}
    res['total_seconds'] = time.perf_counter() - t0
    Path(a.out).write_text(json.dumps(res, indent=1) + '\n', encoding='utf-8')
    print(f'total {res["total_seconds"]:.1f} s -> {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
