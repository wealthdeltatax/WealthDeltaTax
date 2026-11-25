"""V3-12 smoke and acceptance wiring (architecture.md 6.4, acceptance.md 2, 057c): --size smoke (N1 50, 3 draws, N2P 20) on the first grid point (minutes). Pins shapes and identities, never a household-arm value."""
import copy, json, shutil, subprocess, sys
from pathlib import Path
import pytest
REPO = Path(__file__).resolve().parents[3]
RUN = "import sys; sys.path.insert(0, 'model'); from model_v3 import run; run.main(sys.argv[1:])"
NEEDED = ('model-specs/outputs.yml', 'results/cell-baseline/inputs_used.json', 'data/input-register/inputs.json', 'model/tools/validate_outputs.py')

def smoke(root, out): return subprocess.run([sys.executable, '-I', '-c', RUN, '--size', 'smoke', '--out', str(out)], cwd=root, capture_output=True, text=True)

def validate(path, *flags): return subprocess.run([sys.executable, '-I', str(REPO / 'model/tools/validate_outputs.py'), str(path), *flags], capture_output=True, text=True)

def accept(*args): return subprocess.run(['bash', str(REPO / 'tests/model/model_v3/accept.sh'), *args], cwd=REPO, capture_output=True, text=True).returncode

def tree(tmp):
    """A copy of the tree the run needs, for a seeded breakage."""
    shutil.copytree(REPO / 'model/model_v3', tmp / 'model/model_v3', ignore=shutil.ignore_patterns('__pycache__')); shutil.copytree(REPO / 'data/country-packs', tmp / 'data/country-packs')
    for f in NEEDED:
        (tmp / f).parent.mkdir(parents=True, exist_ok=True); shutil.copy(REPO / f, tmp / f)
    return tmp

@pytest.fixture(scope='module')
def good(tmp_path_factory):
    out = tmp_path_factory.mktemp('smoke')
    return smoke(REPO, out), out / 'outputs.json'

def test_smoke_passes(good):
    done, path = good
    assert done.returncode == 0, done.stderr[-600:]
    run = json.loads(path.read_text())['run']
    assert (run['status'], run['paths'], run['seed']) == ('provisional', 50, 20261118) and run['arm']['arm'] == 'household' and run['arm']['central'] is False
    assert validate(path).returncode == 0

def test_renamed_module_copy_fails(tmp_path):
    t = tree(tmp_path)
    (t / 'model/model_v3/core/kernel.py').rename(t / 'model/model_v3/core/kernel_renamed.py')
    done = smoke(t, tmp_path / 'out')
    assert done.returncode != 0 and 'kernel' in done.stderr

def test_broken_import_fails(tmp_path):
    t = tree(tmp_path)
    with open(t / 'model/model_v3/core/schedule.py', 'a') as fh:
        fh.write('\nimport model_v3_no_such_module\n')
    assert smoke(t, tmp_path / 'out').returncode != 0

def cell(lo, mid, hi, form='p10_mean_p90'):
    return dict(zip(('p10', 'mean', 'p90') if form == 'p10_mean_p90' else ('lo', 'point', 'hi'), (lo, mid, hi)), horizon='short', by={'wealth_band': 'D4_5'}, schedule='S_low')

def test_range_rule_has_no_centre_and_marks_no_payer():
    from model_v3 import run
    mk = lambda o2: {'O2': {'summary': 'p10_mean_p90', 'cells': [o2]}, 'O1e': {'summary': 'point_and_range', 'cells': [cell(0, 1, 4, 'point_and_range')]}}
    docs = [mk(cell(1, 2, 3)), {'O2': mk(cell(0, 5, 9))['O2']}]   # O1e is computed at the first point only
    out = run.scenario_range(docs)
    assert out['O2']['cells'][0]['p10'] == 0 and out['O2']['cells'][0]['p90'] == 9 and out['O2']['cells'][0]['mean'] == run.NO_CENTRAL   # envelope of the points
    assert out['O1e']['cells'][0]['point'] == 1                                  # points agree: kept, not marked
    for oid in ('O2', 'OW3'): out[oid] = copy.deepcopy(out['O2']); out[oid]['cells'][0].update(p10=None, mean=None, p90=None)
    out['O1e']['cells'][0].update(point=None); run.mark_no_payer(out)
    assert all({out[o]['cells'][0][k] for k in ('p10', 'mean', 'p90')} == {run.NO_PAYER} for o in ('O2', 'OW3')) and out['O1e']['cells'][0]['point'] is None   # ruled ids marked; O1e never
    assert docs[0]['O2']['cells'][0]['mean'] == 2                                # the inputs are not edited

def test_validator_accepts_markers_only_where_ruled(good, tmp_path):
    d = json.loads(good[1].read_text())
    o2 = next(c for c in d['outputs']['O2']['cells'] if c['by'] == {'wealth_band': 'D4_5'})
    o2.update(p10='no_payer_at_launch', mean='no_payer_at_launch', p90='no_payer_at_launch'); d['outputs']['O1e']['cells'][0].update(point='no_sign_change_0_15', lo='not_run_this_run', hi='not_run_this_run'); d['run']['pack_country'] = 'GBR'   # O1e not run at the other points; the pack code maps to the label
    f = tmp_path / 'a.json'; f.write_text(json.dumps(d))
    assert validate(f).returncode == 0
    for mut in (lambda x: x['outputs']['O1']['cells'][0].update(p10='no_payer_at_launch'), lambda x: x['outputs']['OF1'].update(pending=''), lambda x: x['outputs']['O1']['cells'][0].update(mean='not_run_this_point')):   # a marker outside its cells, an unlabelled pending
        bad = copy.deepcopy(d); mut(bad); f.write_text(json.dumps(bad)); assert validate(f).returncode != 0
    d['run']['arm']['targets'] = [dict(point='median_mid', status='met', shortfalls={}), dict(point='max_mid', status='target_not_met', shortfalls={'income_tax_gains': dict(reached=0.1, target=0.17)})]; f.write_text(json.dumps(d)); assert validate(f).returncode == 0; d['run']['arm']['targets'][1]['shortfalls'] = {}; f.write_text(json.dumps(d)); assert validate(f).returncode != 0   # target_not_met needs the figures
    assert d['outputs']['OF1']['pending'] and d['outputs']['CK1']['pending'] and not d['outputs']['OF1']['cells']

def test_seeded_breakages_fail_acceptance_steps_5_and_6(good, tmp_path):
    d = json.loads(good[1].read_text().replace('null', '1.0')); d['run'].update(paths=1000, level2_paths=50)   # the smoke file with its nulls filled and made large enough: the baseline for step 5
    f = tmp_path / 'ok.json'; f.write_text(json.dumps(d)); assert accept('--check', str(f)) == 0
    seeds = [lambda x: x['run'].update(seed=1), lambda x: x['outputs'].pop('O1'), lambda x: x['outputs']['O1']['cells'][0].update(mean=None)]   # a changed seed, a missing id, a null cell
    for i, brk in enumerate(seeds):
        e = copy.deepcopy(d); brk(e); g = tmp_path / f'b{i}.json'; g.write_text(json.dumps(e))
        assert accept('--check', str(g)) != 0
    g = tmp_path / 'rerun.json'; g.write_text(json.dumps(d) + ' ')               # a non-identical rerun
    assert accept('--compare', str(f), str(f)) == 0 and accept('--compare', str(f), str(g)) != 0
