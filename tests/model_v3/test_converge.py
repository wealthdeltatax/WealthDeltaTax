"""V3-12 convergence (acceptance.md 5, 057c): C1 to C4 at S_central, the household arm's first grid point, level 1 through the runner (no file writer). Sizes are run.py's (never lowered here);
C3 runs REDUCED: C3_DRAWS against twice that, at C3_PATHS paths a draw (the full 400 against 200 at 1,000 paths is a later manual run, not acceptance; sixth-round ruling, 2026-11-24)."""
import json
from dataclasses import replace
import numpy as np, pytest, yaml
from model_v3 import run
from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm
from model_v3.runner import runner as R, sweeps as S
pytestmark = pytest.mark.converge
C3_DRAWS, C3_PATHS = 40, 250
SEEDS = (run.SEED, 20261119, 20261120, 20261121, 20261122)
KEY = {'O1': ('S_central', 'short', (), 'M1'), 'O2': ('S_central', 'short', (('wealth_band', 'overall'),), None), 'O3': ('S_central', 'single', (), None), 'O4a': ('S_central', 'short', (('income_decile', 'overall'),), None)}

@pytest.fixture(scope='module')
def arm():
    man, lv = yaml.safe_load(run.MANIFEST.read_text()), json.loads(run.LEVERS.read_text())
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(run.INPUTS), lv, tier1, list(asm.entries(man)),
                    [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')])
    cp = replace(ctx, arm=dict(arm='household', inputs=json.loads(run.HH_INPUTS.read_text()), saving='median', regime='mid'))
    fmap, _ = S.feasibility(R.make_ev(cp, rt.streams(run.SEED)['tornado_crn'].standard_normal((R.T, 20))), S.grid(lv))
    return cp, {'S_central': S.choose(fmap, man['feasibility'])['S_central']}

def stats(cp, spec, seed, n):
    smp, _ = R.level1(cp, spec, rt.streams(seed)['level1_paths'], n=n)
    return {o: np.array([np.nanmean(v), *np.nanpercentile(v, (10, 90))]) for o, v in ((o, smp[o][k]) for o, k in KEY.items())}   # mean, P10, P90

@pytest.fixture(scope='module')
def master(arm):
    return {s: stats(*arm, s, R.N1) for s in SEEDS}

def test_c1_five_seeds_agree(master):
    for o in KEY:
        a = np.array([master[s][o] for s in SEEDS]); sp = a.max(0) - a.min(0)
        assert sp[0] <= 0.10 and sp[1] <= 0.15 and sp[2] <= 0.15, (o, sp)

def test_c2_doubling_moves_the_means_little(arm, master):
    big = stats(*arm, run.SEED, 2 * R.N1)
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
