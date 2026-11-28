"""171c: per-output movement between two quick `outputs.json` files (O1f, O2b, O2c by default; --all for every output).
  python -I results/171c-zero-tolerance/compare_outputs.py A.json B.json [--all]"""
import json, sys

def flat(x, p=''):
    if isinstance(x, dict):
        for k in sorted(x, key=str): yield from flat(x[k], f'{p}/{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from flat(v, f'{p}[{i}]')
    elif isinstance(x, (int, float)) and not isinstance(x, bool): yield p, float(x)
    else: yield p, x

a, b = (json.load(open(f))['outputs'] for f in sys.argv[1:3])
ids = sorted(a) if '--all' in sys.argv else [i for i in ('O1f', 'O2b', 'O2c') if i in a]
for i in ids:
    x, y = dict(flat(a[i].get('cells', []))), dict(flat(b[i].get('cells', [])))
    num = [k for k in x if isinstance(x[k], float) and k in y and isinstance(y[k], float)]
    diff = [k for k in num if x[k] != y[k] and not (x[k] != x[k] and y[k] != y[k])]
    mx = max((abs(x[k] - y[k]) for k in diff), default=0.0)
    rel = max((abs(x[k] - y[k]) / max(abs(x[k]), abs(y[k]), 1e-300) for k in diff), default=0.0)
    print(f'{i}: values {len(num)}, differing {len(diff)}, max abs {mx:.6g}, max rel {rel:.6g}, keys only in one {len(set(x) ^ set(y))}')
    for k in diff[:5]: print(f'    {k}: {x[k]} -> {y[k]}')
