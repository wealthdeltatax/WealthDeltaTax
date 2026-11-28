"""V3-12 convergence (acceptance.md 5, 057c): C1 to C4 at S_central, level 1 through the runner (no file writer). C1 and C2 run on the legacy arm: the household arm ignores the level 1 path draws (one path repeated), so
seeds and doubling cannot move it and the two tests would pass without testing anything (author, 2026-11-25); C3 (level 2) and C4 (tornado) run on the household arm's first grid point. Sizes are run.py's (never lowered here);
The legacy arm has no feasible named schedule by design (its 3.5% consumption assumption, I-D14c, is abandoned as a central assumption; author, 2026-11-26): `named()` then takes the grid point with the highest F1 (ties: lowest M2 short), because C1 and C2 test sampling noise, which does not depend on which schedule is used.
C3 runs REDUCED: C3_DRAWS against twice that, at C3_PATHS paths a draw (the full 400 against 200 at 1,000 paths is a later manual run, not acceptance; sixth-round ruling, 2026-11-24)."""
import json
from dataclasses import replace
from pathlib import Path
import numpy as np, pytest, yaml
from model_v3 import run
from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm
from model_v3.runner import runner as R, sweeps as S
pytestmark = pytest.mark.converge
C3_DRAWS, C3_PATHS = 40, 250
SEEDS = (run.SEED, 20261119, 20261120, 20261121, 20261122)
LIMITS = json.loads((Path(__file__).parent / 'c1_limits.json').read_text())['limits']   # measured seed noise, brief 187c (model/tools/c1_noise.py)
KEY = {'O1': ('S_central', 'short', (), 'M1'), 'O2': ('S_central', 'short', (('wealth_band', 'overall'),), None), 'O3': ('S_central', 'single', (), None), 'O4a': ('S_central', 'short', (('income_decile', 'overall'),), None)}

@pytest.fixture(scope='module')
def base():
    man, lv = yaml.safe_load(run.MANIFEST.read_text()), json.loads(run.LEVERS.read_text())
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(run.INPUTS), lv, tier1, list(asm.entries(man)),
                    [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')])
    return ctx, lv, man

def named(cp, lv, man):
    fmap, _ = S.feasibility(R.make_ev(cp, rt.streams(run.SEED)['tornado_crn'].standard_normal((R.T, 20))), S.grid(lv))
    named = S.choose(fmap, man['feasibility'])
    if named is None:   # the legacy arm: no feasible schedule by design (see the module docstring); the highest-F1 point stands in
        return cp, {'S_central': max(fmap, key=lambda p: (p['F1']['short'], -p['M2']['short']))['spec']}
    return cp, {'S_central': named['S_central']}

@pytest.fixture(scope='module')
def arm(base):
    ctx, lv, man = base
    return named(replace(ctx, arm=dict(arm='household', inputs=json.loads(run.HH_INPUTS.read_text()), saving='median', regime='mid')), lv, man)

@pytest.fixture(scope='module')
def legacy(base):
    return named(*base)

def stats(cp, spec, seed, n):
    smp, _ = R.level1(cp, spec, rt.streams(seed)['level1_paths'], n=n)
    return {o: np.array([np.nanmean(v), *np.nanpercentile(v, (10, 90))]) for o, v in ((o, smp[o][k]) for o, k in KEY.items())}   # mean, P10, P90

@pytest.fixture(scope='module')
def master(legacy):
    return {s: stats(*legacy, s, R.N1) for s in SEEDS}

def test_c1_five_seeds_agree_on_the_legacy_arm(master):
    bad = {}
    for o in KEY:
        a = np.array([master[s][o] for s in SEEDS]); sp = a.max(0) - a.min(0)
        bad.update({f'{o} {st}': (round(float(x), 4), LIMITS[o][st]) for st, x in zip(('mean', 'p10', 'p90'), sp) if not x <= LIMITS[o][st]})   # all failures, not the first; NaN fails
    assert not bad, bad

def test_c2_doubling_moves_the_means_little_on_the_legacy_arm(legacy, master):
    big = stats(*legacy, run.SEED, 2 * R.N1)
    assert all(abs(big[o][0] - master[run.SEED][o][0]) <= 0.05 for o in KEY), {o: big[o][0] - master[run.SEED][o][0] for o in KEY}

def test_c3_reduced_level2_percentiles_hold(arm):
    cp, spec = arm
    p = [np.percentile(R.level2(cp, spec, rt.streams(run.SEED)['level2_draws'], n=n, n_paths=C3_PATHS).samples['O1'][KEY['O1']], (10, 90)) for n in (C3_DRAWS, 2 * C3_DRAWS)]
    assert np.abs(p[0] - p[1]).max() <= 0.10, p

def test_c4_tornado_top_three_agree(arm):
    cp, spec = arm
    top = []
    for seed in SEEDS[:2]:
        ev = R.make_ev(cp, rt.streams(seed)['tornado_crn'].standard_normal((R.T, R.N2P)))
        rows = S.tornado(ev, spec, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp))
        top.append([r['input'] for r in rows if r['headline'] == 'M1' and r['horizon'] == 'short'][:3])
    assert top[0] == top[1], top
