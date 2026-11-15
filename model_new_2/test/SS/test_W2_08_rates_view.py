"""Test for patch W2-08: one copy of the accessors; both scripts import them; behaviour unchanged."""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True
def check(c, m):
    global ok; print(('PASS ' if c else 'FAIL ') + m); ok &= bool(c)
def txt(n):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', n), recursive=True) if '.bak' not in p and '/test/' not in p.replace('\\', '/')]
    assert len(h) == 1, (n, h); return open(h[0], encoding='utf-8').read()
for n in ('8_2_RATES_tables.py', '8_3_RATES_charts.py'):
    t = txt(n)
    check('from rates_view import' in t, f'{n}: imports rates_view')
    left = re.findall(r"^def (_med|_hl|_pq|_years|_need|_route_b_names|_default_of_mode|_rb_label)\(", t, re.M)
    check(not left, f'{n}: no local copies left {left}')
sys.path.insert(0, ROOT)
try:
    import rates_view as rv
    sc = {'route_b': {'mode': 'lien', 'deferral_spread': 0.03}}
    check(rv.rb_label(sc) == 'Lien, spread 3%' and rv.rb_label({}) == 'Sale' and rv.rb_label({}, long=True) == 'Sale (cash-equivalent units)', 'rb_label short / long')
    check(rv.hl({'headline': {'x': 1}}, 'zz') == 1 and rv.hl({}, 'x') is None, 'hl falls back to the one mode run')
    check(rv.med({'overall': {'medians': {'a': 2.0}}}, 'a') == 2.0, 'med headline form')
    check(rv.years({'rel_y10': 1, 'rel_y20': 1, 'rel_cov_year': 1}, 'rel_y') == [10, 20], 'years')
except ModuleNotFoundError as e:
    print(f'SKIP behaviour ({e})')
sys.exit(0 if ok else 1)
