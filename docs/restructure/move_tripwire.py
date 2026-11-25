#!/usr/bin/env python3
"""Move tripwire (044c, tier 3): the model's numbers and gates must not move when files move.

    python docs/restructure/move_tripwire.py --baseline     # write move-tripwire-baseline.json (at the merged 009c state)
    python docs/restructure/move_tripwire.py                # compare with the baseline; exit 1 on any difference
    python docs/restructure/move_tripwire.py --only inputs,evaluation

It finds each file at its old or its new place, so the same script runs before and after the move
(CANDIDATES); a stage that moves a file adds nothing here unless it invents a third place.
Checks, on one process, about two minutes:
  inputs       sha256 of the bytes of the input register (the gate hashes it) and of the legacy digest fixture
  legacy       tests/.../test_legacy_digest.py::test_the_legacy_digest_equals_the_fixture passes
  pack         build_gbr.py re-run in place gives the committed pack and levers.json byte for byte (files are restored if not)
  evaluation   a household evaluation at 20 paths for saving median and min, fund safe and market, schedule tau_0 .04, tau_m .5, k_ln .5, ratio 1:
               sha256 of M1a, M2, revenue P6 and the list of output ids (the manifest), per case
It does not replace the suites; it is the quick alarm that a move changed a path-dependent number.
"""
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path

ROOT = Path(subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() or '.')
CANDIDATES = {
    'inputs': ['data/input-register/inputs.json', 'data/input-register/inputs.json'],
    'fixture': ['tests/model/model_v3/fixtures/legacy_digest.json', 'tests/model/model_v3/fixtures/legacy_digest.json'],
    'digest_test': ['tests/model/model_v3/test_legacy_digest.py', 'tests/model/model_v3/test_legacy_digest.py'],
    'outputs': ['docs/model-v3/outputs.yml', 'model-specs/outputs.yml'],
    'levers': ['model/model_v3/levers.json', 'model/model_v3/levers.json'],
    'pack': ['data/country-packs/GBR', 'data/country-packs/GBR'],
    'builder': ['model/model_v3/pack/build_gbr.py', 'model/model_v3/pack/build_gbr.py'],
    'cell_inputs': ['docs/model-v3/cell-baseline/inputs_used.json', 'results/cell-baseline/inputs_used.json'],
}
BASELINE = Path(__file__).with_name('move-tripwire-baseline.json')
SPEC = dict(tau_0=0.04, tau_m=0.5, k_ln=0.5, ratio=1.0)
CASES = [('median', 'safe'), ('median', 'market'), ('min', 'safe'), ('min', 'market')]
N_PATHS, SEED = 20, 20261118


def find(key):
    for c in CANDIDATES[key]:
        if (ROOT / c).exists():
            return ROOT / c
    raise SystemExit(f'move_tripwire: {key} is at none of {CANDIDATES[key]}')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def tree_hash(d):
    h = hashlib.sha256()
    for f in sorted(p for p in d.rglob('*') if p.is_file() and '__pycache__' not in p.parts):
        h.update(f.relative_to(d).as_posix().encode() + b'\0' + f.read_bytes() + b'\0')
    return h.hexdigest()


def c_inputs():
    return {'inputs.json': sha(find('inputs').read_bytes()), 'legacy_digest.json': sha(find('fixture').read_bytes())}


def c_legacy():
    t = find('digest_test')
    r = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-x', '-p', 'no:cacheprovider', f'{t}::test_the_legacy_digest_equals_the_fixture'], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-1500:])
    return {'digest_equals_fixture': r.returncode == 0}


def c_pack():
    pack, lev, builder = find('pack'), find('levers'), find('builder')
    files = [p for p in pack.rglob('*') if p.is_file()]
    keep = {p: p.read_bytes() for p in [*files, lev]}
    before = (tree_hash(pack), sha(lev.read_bytes()))
    r = subprocess.run([sys.executable, '-B', '-I', str(builder)], cwd=ROOT, capture_output=True, text=True)
    after = (tree_hash(pack), sha(lev.read_bytes()))
    if after != before or r.returncode:
        for p in [*pack.rglob('*'), lev]:        # restore what the rebuild changed or added
            if p.is_file() and p not in keep:
                p.unlink()
        for p, b in keep.items():
            if not p.exists() or p.read_bytes() != b:
                p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
        print(r.stdout[-800:], r.stderr[-800:])
    return {'rebuild_is_byte_identical': after == before and r.returncode == 0, 'pack_tree_sha256': before[0], 'levers_sha256': before[1]}


def c_evaluation():
    from dataclasses import replace
    import numpy as np, yaml
    for sp in (ROOT, ROOT / 'model'):
        if (sp / 'model_v3' / '__init__.py').exists():
            sys.path.insert(0, str(sp)); break
    from model_v3.core import pack as pk, returns as rt
    from model_v3.out import assemble as asm
    from model_v3.runner import runner as R
    man = yaml.safe_load(find('outputs').read_text())
    lv = json.loads(find('levers').read_text())
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    once = [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
    ctx = R.context(pk.load_pack(find('pack')), pk.load_register(find('inputs')), lv, tier1, list(asm.entries(man)), once)
    inp = json.loads(find('cell_inputs').read_text())
    eps = rt.streams(SEED)['tornado_crn'].standard_normal((R.T, N_PATHS))
    h = lambda x: sha(np.ascontiguousarray(np.asarray(x, float)).tobytes())
    def walk(d, out):
        for k in sorted(d, key=str):
            walk(d[k], out) if isinstance(d[k], dict) else out.append(h(d[k]))
        return out
    res = {'output_ids': sha(json.dumps(sorted(asm.entries(man))).encode())}
    for saving, fund in CASES:
        cp = replace(ctx, arm=dict(arm='household', inputs=inp, saving=saving, regime='mid', fund_return=fund))
        e = R.make_ev(cp, eps)(SPEC, {})
        res[f'{saving}_mid_{fund}'] = {'M1a': sha(''.join(walk(e['M1a'], [])).encode()), 'M2': sha(''.join(walk(e['M2'], [])).encode()), 'P6': sha(''.join(walk(e['revenue']['P6'], [])).encode())}
    return res


CHECKS = {'inputs': c_inputs, 'legacy': c_legacy, 'pack': c_pack, 'evaluation': c_evaluation}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', action='store_true')
    ap.add_argument('--only')
    a = ap.parse_args()
    names = a.only.split(',') if a.only else list(CHECKS)
    got, t0 = {}, time.perf_counter()
    for n in names:
        t = time.perf_counter()
        got[n] = CHECKS[n]()
        print(f'{n:11} {time.perf_counter() - t:6.1f} s')
    print(f'total       {time.perf_counter() - t0:6.1f} s')
    if a.baseline:
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        BASELINE.write_text(json.dumps({'commit': head, 'note': 'taken at the merged 009c state (817dccc) before any move; recapture only on the author\'s word', 'spec': SPEC, 'paths': N_PATHS, 'seed': SEED, 'checks': got}, indent=1) + '\n')
        print('baseline written', BASELINE.relative_to(ROOT))
        return 0
    want = json.loads(BASELINE.read_text())['checks']
    bad = [n for n in names if got[n] != want.get(n)]
    for n in bad:
        print(f'DIFFERS {n}:\n  baseline {json.dumps(want.get(n))[:400]}\n  now      {json.dumps(got[n])[:400]}')
    print('PASS: the tripwire holds' if not bad else f'FAIL: {bad}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
