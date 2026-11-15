"""Test for patch W2-04."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
def find(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) if '.bak' not in p and 'patch_' not in p]
    assert len(h) == 1, (n, h); return h[0]
core = open(find('wdt_core.py'), encoding='utf-8').read()
code = re.sub(r'#.*', '', core)
for k in ("raw['swf']", "raw['budget']", "raw['returns']", "raw['tcm']", "raw['tiers']", "raw['brackets']", '_ssm_lrr_fill_year', '_ssm_marginals',
          "p['N_fill']", "p['hist_mean']", "budget_growth", 'returns_meta', 'wfr_', 'rates_g_sweep', '_canon'):
    check(k not in code, f'wdt_core: no {k}')
vg = open(find('valgen_core.py'), encoding='utf-8').read()
check('_RETIRED_KEYS' not in vg and 'budget_growth' not in re.sub(r'#.*', '', vg), 'valgen: no _RETIRED_KEYS / budget_growth')
sys.path.insert(0, os.path.dirname(find('wdt_core.py')))
try:
    import wdt_core as wc
    import time; t = time.time()
    p = wc.load_params()
    check(time.time() - t < 5, f'load_params fast ({time.time() - t:.2f}s, was a 71x10 SSM)')
    check(all(k not in p for k in ('N_fill', 'N', 'tcm', 'returns', 'tiers', 'brackets', 'g', 'g_real')), 'retired keys absent; no nominal g_real at load')
    check(p['sweep']['g_offsets'] and p['sweep']['g_vals'] == [], 'g_offsets parsed, g_vals filled later')
    q = wc.with_val_basis(wc.with_rate_scenario(p), None) if p['val_gen']['basis'] == 'manual' else None
    if q is None:
        try:
            q = wc.with_val_basis(wc.with_rate_scenario(p))
        except FileNotFoundError as e:
            print('SKIP with_val_basis (JST file not found)')
    if q is not None:
        check(abs(q['sweep']['g_vals'][4] - q['g_real']) < 1e-12, 'g_vals recentred on g_real (offset 0 -> g_real)')
        check(q['val_basis'] == 'real', 'basis is real')
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f'SKIP runtime checks ({type(e).__name__}: {str(e)[:100]})')
except Exception as e:
    check(False, f'{type(e).__name__}: {e}')
sys.exit(0 if ok else 1)
