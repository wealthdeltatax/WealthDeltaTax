"""Test for patch W2-05."""
import glob, os, sys
try: import tomllib
except ModuleNotFoundError: import tomli as tomllib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
f = [p for p in glob.glob(os.path.join(ROOT, '**', 'WDT_Params.toml'), recursive=True) if '.bak' not in p]
assert len(f) == 1, f
t = tomllib.load(open(f[0], 'rb'))
for k in ('swf', 'budget', 'returns', 'tcm', 'tiers', 'brackets', 'rate'):
    check(k not in t, f'[{k}] gone')
sw = t['sweep']
check(not [k for k in sw if k.endswith('_canon') or k.startswith(('rates_', 'wfr_')) or k == 'g_vals'], '[sweep]: canon / rates_* / wfr_* / g_vals gone')
check(len(sw['g_offsets']) == 10 and 0.0 in sw['g_offsets'], '[sweep].g_offsets present, includes 0.0 (g_real)')
check(abs(t['synthetic_scenario']['mu'] - 0.02) < 1e-12, '[synthetic_scenario] mu = 2%')
check(all(k in t['val_gen'] for k in ('basis', 'rate_scenario')), '[val_gen] basis and rate_scenario present')
check('hlc' in t['val_gen'], '[val_gen.hlc] present (W2-02)')
sys.path.insert(0, os.path.dirname(f[0]))
try:
    import wdt_core as wc
    p = wc.load_params(); check(p['sweep']['g_offsets'] == sw['g_offsets'], 'wdt_core parses g_offsets')
    wc.load_rates_params(); check(True, 'load_rates_params loads')
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f'SKIP runtime ({e})')
except Exception as e:
    check(False, f'{type(e).__name__}: {e}')
sys.exit(0 if ok else 1)
