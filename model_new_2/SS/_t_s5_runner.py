
import importlib.util, json, math, sys, tempfile, tomllib
from pathlib import Path
sys.path.insert(0, r"C:\Users\kyleo\OneDrive\My Documents\Hobbies\Wealth Delta Tax\Model\test")
from s5_fixture import make_data
import wdt_core
root = Path(r"C:\Users\kyleo\OneDrive\My Documents\Hobbies\Wealth Delta Tax\Model")
def load(n, f):
    s = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
tb = load('s5t', next(root.rglob('5_6_VALGEN_tables.py')))
ch = load('s5c', next(root.rglob('5_7_VALGEN_charts.py')))
ch._OUT = Path(tempfile.mkdtemp())
p = wdt_core.load_params()
d = make_data(p)
res = {'ids_equal': set(tb.PAIRS) == set(ch.PAIRS),
       'keys_equal': all(tb.PAIRS[k]['json'] == ch.PAIRS[k]['json'] for k in tb.PAIRS if k in ch.PAIRS),
       'builders': {}}
names = tomllib.loads(next(root.rglob('WDT_Params.toml')).read_text(encoding='utf-8'))['names']['val']
res['names_ok'] = all(i in names and names[i]['kind'] == 'output' for i in ['RPL', 'ARC', 'BES', 'RSP', 'LCD', 'BAND', 'HLP'] + ['RIS'])
res['ris_name'] = names['RIS']['name']
def flat(ser):
    out = []
    for v in ser.values():
        out += [x for x in v if isinstance(x, (int, float)) and not isinstance(x, bool)]
    return out
for pid in ['RPL', 'ARC', 'BES', 'RSP', 'LCD', 'BAND', 'HLP'] + ['RIS']:
    t = tb.BUILDERS[pid](d, p); c = ch.BUILDERS[pid](d, p)
    fl = flat(c['series'])
    miss = [v for v in t['values'] if not any(math.isclose(v, x, rel_tol=1e-9, abs_tol=1e-12) for x in fl)]
    res['builders'][pid] = {'table_rows': t['md'].count('\n|'), 'values': len(t['values']), 'missing': len(miss),
                            'png': bool(c['path']) and Path(c['path']).exists()}
# skipped parts
d2 = make_data(p)
d2['replay'] = {'skipped': True}; d2['p6'] = {'archetypes': {}}; d2['p5']['hlc_pair'] = {'skipped': True, 'reason': 'no RATES JSON'}
skip = {}
for pid in ('RPL', 'ARC', 'BES', 'HLP'):
    t = tb.BUILDERS[pid](d2, p); c = ch.BUILDERS[pid](d2, p)
    skip[pid] = (t['md'].startswith(f'Table {pid}: not built') and t['values'] == [] and c['path'] is None)
res['skip_ok'] = skip
print('S5RESULT' + json.dumps(res))
