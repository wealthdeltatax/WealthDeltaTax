"""Rule checkers for the v3 rules tests (R4, R8, R9, R11). Each takes a tree root, so a test can seed a violation in a temp tree."""
import ast, json, re, subprocess, sys, types
import pytest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(REPO))
MODEL, TESTS = REPO / 'model_v3', REPO / 'tests' / 'model_v3'
LAYER = {'core/pack': 0, 'core/returns': 1, 'core/base': 1, 'core/schedule': 1, 'core/kernel': 1, 'core/household': 1, 'core/pension_lien': 1, 'core/cells': 2, 'core/revenue': 2,
         'core/burden': 3, 'core/support': 3, 'runner/out_revenue': 3.5, 'runner/out_burden': 3.5, 'runner/out_support': 3.5, 'runner/out_sweeps': 3.5, 'runner/arm': 3.6, 'runner/groups': 3.7, 'runner/runner': 4, 'runner/sweeps': 4, 'runner/pool': 4,
         'out/assemble': 5, 'out/writer': 5}   # architecture.md 5.1

files = lambda root: sorted(Path(root).rglob('*.py'))
key = lambda root, p: p.relative_to(root).with_suffix('').as_posix()

def tree(tmp, files_):
    for name, src in files_.items():
        (tmp / 'model_v3' / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp / 'model_v3' / name).write_text(src, encoding='utf-8')
    return tmp / 'model_v3'

def imports(root):
    root, out = Path(root), []
    rel = lambda s: s[len(root.name) + 1:].replace('.', '/')
    for p in files(root):
        t, src = ast.parse(p.read_text(encoding='utf-8')), key(root, p)
        up = src.split('/')[:-1]
        lazy = {id(n) for f in ast.walk(t) if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) for n in ast.walk(f)}
        for n in ast.walk(t):
            if isinstance(n, ast.Import):
                pairs = [(a.name, [a.name]) for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                m = '.'.join([root.name, *up[:len(up) - n.level + 1], n.module or ''] if n.level else [n.module or '']).strip('.')
                pairs = [(m, [f'{m}.{a.name}' for a in n.names])]
            else:
                continue
            for m, cands in pairs:
                own = m.split('.')[0] == root.name
                dst = next((rel(c) for c in cands if (root / (rel(c) + '.py')).exists()), rel(m)) if own else None
                out.append((src, dst, id(n) in lazy, n.lineno))
    return out

def graph_errors(root):
    return [f'{s}:{ln} imports {d}' for s, d, _, ln in imports(root) if d and s != 'run' and not (
        (d == 'interface' and LAYER.get(s, -1) >= 4) or (s in LAYER and d in LAYER and LAYER[s] > LAYER[d]
         and s not in ('core/kernel', 'core/schedule') and not s.startswith('out/')))]

lazy_errors = lambda root: [f'{s}:{ln} import inside a function' for s, _, lazy, ln in imports(root) if lazy]

PROBE = """import importlib, json, os, sys; from pathlib import Path
root, pkg = sys.argv[1:3]; sys.path.insert(0, os.path.dirname(root))
snap = lambda: (dict(os.environ), os.getcwd(), sorted(map(str, Path(root).rglob('*'))), os.listdir('.'))
a, err = snap(), []
for m in sys.argv[3:]:
    try: importlib.import_module(m)
    except Exception as e: err.append(m + ': ' + repr(e))
print(json.dumps(err + [k for k, x, y in zip(('environ', 'cwd', 'tree', 'cwd listing'), a, snap()) if x != y]))"""

def side_effect_errors(root):
    root = Path(root).resolve()
    mods = ['.'.join([root.name, *key(root, p).split('/')]).removesuffix('.__init__') for p in files(root)]
    r = subprocess.run([sys.executable, '-B', '-I', '-c', PROBE, str(root), root.name, *mods], capture_output=True, text=True, cwd=root.parent)
    return json.loads(r.stdout) if r.returncode == 0 else [r.stderr[-300:]]

def orphan_errors(root, tests):
    defs, refs = [], set()
    for p in files(root) + files(tests):
        t = ast.parse(p.read_text(encoding='utf-8'))
        defs += [f'{p.name}:{n.name}' for n in t.body if isinstance(n, ast.FunctionDef) and p.is_relative_to(root)]
        refs |= {n.id for n in ast.walk(t) if isinstance(n, ast.Name)} | {n.attr for n in ast.walk(t) if isinstance(n, ast.Attribute)} | {
            a.name for n in ast.walk(t) if isinstance(n, ast.ImportFrom) for a in n.names}
    return [d for d in defs if d.split(':')[1] not in refs]

def country_errors(root):
    doc = (REPO / 'docs/model-v3/country-pack.md').read_text(encoding='utf-8')
    pats = [re.search(rf"^{c}='(.*)'$", doc, re.M).group(1) for c in 'NTA']
    rx = [re.compile('^[^#]*(?:' + p.removeprefix('(?i)') + ')', re.I if p.startswith('(?i)') else 0) for p in pats]
    return [f'{key(root, p)}:{i}' for p in files(root) if p.name != 'build_gbr.py'
            for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1) if any(r.search(line) for r in rx)]

def budgets():
    doc = (REPO / 'docs/model-v3/architecture.md').read_text(encoding='utf-8')
    rows = re.findall(r'^(\S.*?)\s+(\d+)\s+(\d+)$', doc.split('```budgets')[1].split('```')[0], re.M)
    tot = re.search(r'\*\*Total\*\* \| \*\*([\d,]+)\*\* \| \*\*([\d,]+)\*\*', doc).groups()
    return [(f, int(c), int(t)) for f, c, t in rows], tuple(int(x.replace(',', '')) for x in tot)

nlines = lambda p: len(Path(p).read_text(encoding='utf-8').splitlines()) if Path(p).exists() else 0

def budget_errors(root, tests):
    root, tests, pairs = Path(root), Path(tests), []
    for f, code, tst in budgets()[0]:
        stem = Path(f).stem
        if f.startswith('rules'):
            pairs.append((f, sum(nlines(tests / n) for n in ('test_rules.py', 'test_budget.py', 'conftest.py')), tst))
        elif f.startswith('tests/'):
            pairs.append((f, nlines(root.parent / f), tst))
        else:
            pairs += [(f, nlines(root / f), code), (f'test_{stem}.py', nlines(tests / f'test_{stem}.py'), tst)]
    size = lambda d: sum(nlines(p) for p in (root / d).rglob('*.py'))
    o, c = size('out'), size('core') + size('runner')
    return [f'{n}: {a} lines, budget {b}' for n, a, b in pairs if a > b] + (['out/ not smaller than core plus runner'] if (o or c) and o >= c else [])

CHECKS = {'graph': lambda m, t: graph_errors(m), 'lazy': lambda m, t: lazy_errors(m), 'side': lambda m, t: side_effect_errors(m),
          'orphan': orphan_errors, 'country': lambda m, t: country_errors(m), 'budget': budget_errors}

@pytest.fixture
def R():
    return types.SimpleNamespace(**globals())
