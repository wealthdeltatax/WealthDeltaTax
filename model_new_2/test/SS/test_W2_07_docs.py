"""Test for patch W2-07 (static): the docs no longer describe retired machinery as live."""
import glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
def txt(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) + glob.glob(os.path.join(os.path.dirname(ROOT), n)) if '.bak' not in p]
    assert h, n; return open(h[0], encoding='utf-8').read()
c, r = txt('WDT_Code_Reference.md'), txt('WDT_Refactor_Plan.md')
for k in ('`[swf]` |', '`[budget]` |', '`[returns]` |', 'found at load time by `_ssm_lrr_fill_year`', 'p[\'N\']` is a legacy alias'):
    check(k not in c, f'Code Reference: no live description of {k}')
check('wdt_kernel (D12)' in c and '[val_gen.hlc]' in c and 'wdt_jst' in c, 'Code Reference: kernel, wdt_jst, hlc sections')
check('No code written yet' not in r and 'Status (14 October 2026)' in r, 'Refactor Plan status line')
sys.exit(0 if ok else 1)
