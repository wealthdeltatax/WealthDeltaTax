"""Brief 113c (W1): the legacy arm's reference digest. Any change to the kernel, revenue, burden or support code that moves it is a legacy change.
Recapture only on the author's word: `python tests/model/model_v3/test_legacy_digest.py --capture` from the repo root, on a clean checkout of origin/main."""
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[3]
sys.path.insert(0, str(ROOT / 'model'))
from model_v3.core import pack as pk, returns as rt                      # noqa: E402
from model_v3.runner import groups as G, runner as R                     # noqa: E402

FIX = ROOT / 'tests' / 'model' / 'model_v3' / 'fixtures' / 'legacy_digest.json'
SEEDS, N, CHUNK = (7, 11), 20, 10
POINTS = {'low_corner': (0.5, 0.5, 0.25), 'centre': (0.7, 1, 0.5), 'high_corner': (0.9, 2, 1.0), 'tm50_k2_r100': (0.5, 2, 1.0), 'tm90_k05_r025': (0.9, 0.5, 0.25)}
SPECS = {n: dict(tau_0=0.04, tau_m=t, k_ln=k, ratio=r) for n, (t, k, r) in POINTS.items()}       # the named schedules wait for 089c: five fixed grid points stand in
GROUPS = {'runner': ('O1', 'O1a', 'O1b', 'O1c', 'O2', 'O3', 'O4a', 'O1f'), **{m.NAME: m.IDS for m in G.GROUPS}}
CALL = "python tests/model/model_v3/test_legacy_digest.py --print (compute(): R.level1(ctx, SPECS, rt.streams(seed)['level1_paths'], n=20, chunk=10) for seed in (7, 11))"


def compute(seeds=SEEDS):
    """{seed: {'samples': digest, 'groups': {group: digest of its ids}}} on the legacy arm (the only arm there is), the context built as test_runner's, with once."""
    lv, out = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text()), yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1,
                    [o['id'] for o in out['outputs']], [o['id'] for o in out['outputs'] if o.get('once_not_per_schedule')])
    res = {}
    for seed in seeds:
        s = R.level1(ctx, SPECS, rt.streams(seed)['level1_paths'], n=N, chunk=CHUNK)[0]
        res[str(seed)] = {'samples': R.digest(s), 'groups': {g: R.digest({i: s[i] for i in ids if i in s}) for g, ids in GROUPS.items()}}
    return res


def test_the_legacy_digest_equals_the_fixture():
    t0 = time.perf_counter()
    got = compute()
    print(f'legacy digest: {time.perf_counter() - t0:.1f} s')
    assert got == json.loads(FIX.read_text())['digest'], 'the legacy digest moved: a change to kernel, revenue, burden or support altered the legacy arm; that is a legacy change and needs the author (113c)'


def test_the_digest_is_byte_equal_in_the_same_process_and_in_a_fresh_one():
    a = compute((7,))
    assert a == compute((7,))                                                   # one seed: the cost is three runs
    r = subprocess.run([sys.executable, str(Path(__file__)), '--print', '7'], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout) == a, r.stderr[-500:]


if __name__ == '__main__':
    if sys.argv[1:2] == ['--print']:
        print(json.dumps(compute((int(sys.argv[2]),)) if len(sys.argv) > 2 else compute()))
    else:
        assert sys.argv[1:] == ['--capture']
        FIX.parent.mkdir(exist_ok=True)
        FIX.write_text(json.dumps({'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, cwd=ROOT).strip(), 'call': CALL, 'seeds': SEEDS, 'paths': N,
                                   'chunk': CHUNK, 'schedules': POINTS, 'digest': compute()}, indent=1) + '\n')
