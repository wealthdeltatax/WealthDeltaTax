"""Test for patch W2-02 (static + load_params)."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def find(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) if '.bak' not in p and '/test/' not in p.replace('\\', '/')]
    assert len(h) == 1, (n, h); return h[0]
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
vg = open(find('valgen_core.py'), encoding='utf-8').read()
check('rates_data.json' not in re.sub(r'#.*|""".*?"""', '', vg, flags=re.S), 'valgen_core no longer reads rates_data.json (code)')
check("p['val_gen'].get('hlc')" in vg, '_rates_burdens reads [val_gen.hlc]')
check('[val_gen.hlc]' in open(find('WDT_Params.toml'), encoding='utf-8').read(), 'TOML block present')
sys.path.insert(0, os.path.dirname(find('wdt_core.py')))
try:
    import wdt_core as wc
    p = wc.load_params()
    h = p['val_gen']['hlc']
    check(h is not None and set(h) >= {'average_stock_rate', 'top_stock_rate', 'placeholder'}, 'load_params parses hlc')
    import valgen_core as vg_
    b = vg_._rates_burdens(p)
    check(b['ok'] is (not h['placeholder']), f"_rates_burdens ok={b['ok']} consistent with placeholder={h['placeholder']}")
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f'SKIP runtime checks ({type(e).__name__}: {str(e)[:100]})')
except Exception as e:
    check(False, f'load_params / valgen import: {type(e).__name__}: {e}')
sys.exit(0 if ok else 1)
