"""Test for patch W2-06 (static)."""
import glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
def txt(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) if '.bak' not in p]
    assert len(h) == 1, (n, h); return open(h[0], encoding='utf-8').read()
check('[val_gen.hlc]' in txt('5_6_VALGEN_tables.py') and 'valgen_core.py.' in txt('5_6_VALGEN_tables.py'), '5_6 HLP caption/note')
check('[val_gen.hlc]' in txt('5_7_VALGEN_charts.py'), '5_7 HLP footnote')
t = txt('8_2_RATES_tables.py')
check("data['archetype_sweep'] = {" not in t and 'income_short_share_band{i}' in t and 'income_paid_cum_gdp' not in t, '8_2 docstring contract')
sys.exit(0 if ok else 1)
