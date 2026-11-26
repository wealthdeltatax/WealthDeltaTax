"""169c stage A (d): the raw level-1 samples of the legacy digest test (seeds 7, 11; 20 paths; 5 schedules), full precision, on one numerics path.
  NPY_DISABLE_CPU_FEATURES="" python -I results/169c-numerics/numerics_diff.py dump OLD.pkl     # the AVX512 path (the old pins)
  python -I results/169c-numerics/numerics_diff.py dump NEW.pkl                                   # X86_V4 off (model_v3.numerics default)
  python -I results/169c-numerics/numerics_diff.py compare OLD.pkl NEW.pkl                        # largest abs and rel difference per output id"""
import pickle, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'model')); sys.path.insert(0, str(ROOT / 'tests/model/model_v3'))
from model_v3 import numerics  # noqa: F401  before numpy
import numpy as np


def flat(x, p=''):
    if isinstance(x, dict):
        for k in sorted(x, key=str): yield from flat(x[k], f'{p}/{k}')
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x): yield from flat(v, f'{p}/{i}')
    else:
        a = np.asarray(x)
        if a.dtype.kind in 'fiu': yield p, a.astype(float)


if sys.argv[1] == 'dump':
    import json, yaml
    from model_v3.core import pack as pk, returns as rt
    from model_v3.runner import runner as R
    import test_legacy_digest as T
    lv, out = json.loads((ROOT / 'model/model_v3/levers.json').read_text()), yaml.safe_load((ROOT / 'model-specs/outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data/country-packs/GBR'), pk.load_register(ROOT / 'data/input-register/inputs.json'), lv, tier1, [o['id'] for o in out['outputs']], [o['id'] for o in out['outputs'] if o.get('once_not_per_schedule')])
    res = {seed: dict(flat(R.level1(ctx, T.SPECS, rt.streams(seed)['level1_paths'], n=T.N, chunk=T.CHUNK)[0])) for seed in T.SEEDS}
    pickle.dump(res, open(sys.argv[2], 'wb'))
else:
    a, b = (pickle.load(open(f, 'rb')) for f in sys.argv[2:4])
    rows, worst = {}, (0.0, 0.0)
    for seed in a:
        for k, x in a[seed].items():
            y = b[seed][k]; oid = k.split('/')[1]
            same = (x == y) | (np.isnan(x) & np.isnan(y)); d = np.where(same, 0.0, np.abs(x - y)); r = d / np.maximum(np.maximum(np.abs(x), np.abs(y)), 1e-300)
            s = rows.setdefault(oid, [0, 0, 0.0, 0.0]); s[0] += x.size; s[1] += int((~same).sum()); s[2] = max(s[2], float(np.nanmax(d, initial=0))); s[3] = max(s[3], float(np.nanmax(np.where(d > 0, r, 0), initial=0)))
    print('| id | numbers | differing | max abs | max rel |\n|---|---|---|---|---|')
    for k in sorted(rows): print(f'| {k} | {rows[k][0]} | {rows[k][1]} | {rows[k][2]:.3g} | {rows[k][3]:.3g} |')
    print('worst abs', max(v[2] for v in rows.values()), 'worst rel', max(v[3] for v in rows.values()))
