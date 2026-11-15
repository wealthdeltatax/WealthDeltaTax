"""
print_val_real_inputs.py: the two REAL inputs VAL needs to match RATES, from the JST history RATES reads.
    g_real      real return of the VAL asset      -> [val_gen] g_real
    index_rate  real GDP/head growth (W_min index) -> [val_gen] index_rate
Prints the UK over several samples, arithmetic and geometric. Which one to adopt is a judgment: RATES itself replays every
country's history, so it has no single number. VAL's constant-g runs compound g, so the GEOMETRIC mean is the like-for-like
growth of a held asset; the arithmetic mean overstates compound growth by about half the variance.
Run from the model folder:  python print_val_real_inputs.py [--dir PATH]
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--dir', default='.')
a = ap.parse_args()
base = Path(a.dir).resolve()


def _add_paths(base, modules):
    """Put the folder of every named module on sys.path, wherever it sits (the model folder, one level up, or any subfolder)."""
    roots = [base, base.parent]
    for m in modules:
        hits = []
        for r in roots:
            hits += [h for h in r.rglob(m + '.py') if not any(x.startswith('.') or x in ('OUTPUTS', '__pycache__') for x in h.parts)]
            if hits:
                break
        if not hits:
            raise SystemExit(f'{m}.py not found under {base} or {base.parent}; pass --dir with the folder that holds wdt_core.py')
        sys.path.insert(0, str(sorted(hits, key=lambda h: len(h.parts))[0].parent))


_add_paths(base, ('wdt_core', 'rates_core'))

import numpy as np

import rates_core as rc
import wdt_core as wc

p = wc.load_rates_params()
rp = p['rates']
J = rc.load_jst(rp)
d = rc.panel(J, rp['uk_iso'])
d['gpc_real'] = d['gpc_real']


def stats(x):
    x = x.dropna()
    return (len(x), float(x.mean()), float(np.prod(1.0 + x) ** (1.0 / len(x)) - 1.0))


print(f"UK ({rp['uk_iso']}), JST: n years, arithmetic mean, geometric mean")
for label, lo, hi in (('all years', -1, 9999), ('1947-2019 (the VAL series)', 1947, 2019), ('1980 onwards', 1980, 9999),
                      ('2000 onwards', 2000, 9999)):
    sub = d[(d.index >= lo) & (d.index <= hi)]
    print(f'\n{label}')
    for col, name in (('capital_tr_real', 'real capital return (what RATES replays)'), ('eq_tr_real', 'real equity return'),
                      ('gpc_real', 'real GDP/head growth (the index)'), ('capital_tr', 'NOMINAL capital return'),
                      ('infl', 'CPI inflation')):
        n, am, gm = stats(sub[col])
        print(f'  {name:42s} n={n:3d}  arith {am:7.2%}  geom {gm:7.2%}')
print('\n[val_gen] today (legacy): g = [tcm] hist_mean = 10.45% NOMINAL, index = [budget] budget_growth = 4.51% NOMINAL, rho = 3.5% REAL.')