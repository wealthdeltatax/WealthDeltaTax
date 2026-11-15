"""diff_json.py OLD.json NEW.json [--tol 1e-12] [--top 15]
Numeric diff of two JSON outputs: keys added/removed, and the numbers that moved (max abs / rel diff, first paths).
Use it to prove a patch is numbers-neutral:  cp valgen_data.json before.json ; (patch, rerun) ; diff_json.py before.json valgen_data.json
Exit 0 if nothing moved beyond tol (added keys are reported but do not fail), 1 otherwise."""
import json, math, sys
def walk(a, b, path, out, tol):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in a.keys() - b.keys(): out['removed'].append(f'{path}/{k}')
        for k in b.keys() - a.keys(): out['added'].append(f'{path}/{k}')
        for k in a.keys() & b.keys(): walk(a[k], b[k], f'{path}/{k}', out, tol)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): out['moved'].append((path, f'len {len(a)} -> {len(b)}', math.inf)); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f'{path}[{i}]', out, tol)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        d = abs(a - b)
        if d > tol * max(1.0, abs(a)): out['moved'].append((path, f'{a!r} -> {b!r}', d))
    elif a != b:
        out['moved'].append((path, f'{str(a)[:40]!r} -> {str(b)[:40]!r}', math.inf))
if __name__ == '__main__':
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    tol = float(sys.argv[sys.argv.index('--tol') + 1]) if '--tol' in sys.argv else 1e-12
    top = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 15
    args = [a for a in args if a not in (str(tol), str(top))]
    out = {'added': [], 'removed': [], 'moved': []}
    walk(json.load(open(args[0])), json.load(open(args[1])), '', out, tol)
    print(f"added {len(out['added'])}, removed {len(out['removed'])}, moved {len(out['moved'])} (tol {tol:g})")
    for k in ('added', 'removed'):
        for x in out[k][:top]: print(f'  {k}: {x}')
    for path, what, d in sorted(out['moved'], key=lambda t: -t[2])[:top]: print(f'  moved: {path}: {what}')
    sys.exit(1 if out['moved'] else 0)
