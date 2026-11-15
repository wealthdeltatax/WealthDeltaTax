"""Test for patch W2-03: no parameter-dict ['g'] left in the cores/tests; p['g_real'] exists and 'g' does not."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
def find(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) if '.bak' not in p and 'patch_' not in p]
    assert len(h) == 1, (n, h); return h[0]
for n in ('wdt_core.py', 'valgen_core.py', 'rates_core.py', 'bridge_test.py', 'kernel_test.py', 'test_valgen_pairs.py'):
    s = open(find(n), encoding='utf-8').read()
    left = re.findall(r"(?<![\w])(?:p|pg|P|p_in|q)\['g'\]", s)
    check(not left, f"{n}: no parameter-dict ['g'] left ({len(left)})")
check("'g_real': 0.1045" in open(find('valgen_core.py'), encoding='utf-8').read(), 'PLAN_S1_BASELINE keyed g_real')
sys.path.insert(0, os.path.dirname(find('wdt_core.py')))
try:
    import wdt_core as wc
    p = wc.load_params()
    check('g' not in p, "load_params(): no 'g' key")
    try:
        q = wc.with_val_basis(wc.with_rate_scenario(p))
        check('g_real' in q and 'g' not in q, f"with_val_basis(): g_real={q['g_real']:.5f}")
    except FileNotFoundError:
        print('SKIP with_val_basis (JST file not found)')
except (ModuleNotFoundError, FileNotFoundError) as e:
    print(f'SKIP runtime checks ({type(e).__name__}: {str(e)[:100]})')
except Exception as e:
    check(False, f'wdt_core load: {type(e).__name__}: {e}')
sys.exit(0 if ok else 1)
