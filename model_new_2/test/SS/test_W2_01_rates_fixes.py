"""Test for patch W2-01.  Static checks always; JSON checks if rates_data.json exists (run rates_core --quick first)."""
import json, os, re, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def find(name):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', name), recursive=True) if '.bak' not in p]
    assert len(h) == 1, (name, h); return h[0]
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)

src = open(find('rates_core.py'), encoding='utf-8').read()
check("'rel_cov_never_share'" in src, 'rel_cov_never_share written')
check('income_short_share_band' in src, 'income_short_share_band written')
check("fg.get('route_b'" in src and "startswith('gl_arch_')" in src, 'figure_scenarios covers route_b + archetypes')
check(src.count('_route_plan(cfg, cal, p)') == 3, '_route_plan: def + cache helper + run_scenario diag only (not per window)')
check('def _plan_ver' in src, '_plan_ver cache helper present')
import importlib.util
sys.path.insert(0, os.path.dirname(find('rates_core.py')))
try:
    import rates_core as rc
    check(hasattr(rc, 'figure_scenarios'), 'rates_core imports')
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f'SKIP import rates_core ({e})')
except Exception as e:
    check(False, f'rates_core imports ({type(e).__name__}: {e})')

jp = glob.glob(os.path.join(ROOT, '**', 'rates_data.json'), recursive=True)
if jp:
    d = json.load(open(jp[0]))
    for n, sc in d['scenarios'].items():
        for mode, h in sc['headline'].items():
            o = h['overall']
            check('rel_cov_never_share' in o, f'{n}/{mode}: rel_cov_never_share key')
            v = o['rel_cov_never_share']
            check(v is None or 0 <= v <= 1, f'{n}/{mode}: share in [0,1]')
            break
        if n.startswith('gl_rb_income'):
            m = next(iter(sc['headline'].values()))['overall']['medians']
            ks = [k for k in m if k.startswith('income_short_share_band')]
            check(len(ks) > 0, f'{n}: income_short_share_band columns ({len(ks)})')
            check(all(m[k] is None or 0 <= m[k] <= 1 for k in ks), f'{n}: shares in [0,1]')
else:
    print('SKIP JSON checks (no rates_data.json)')
sys.exit(0 if ok else 1)
