"""183c stage C: a split run merges to the unsplit run's file, byte for byte (design 5). Slow (about an hour on two cores): `-m split`, not in `fast` and not in accept.sh step 1.
Smoke size, two grid points, batches of 2 draws: plan, 2 point units, the point roots and 6 batches of draws, then the merge. The second pass runs the O1e units in the reverse
order and one point unit again: every partial must come out byte-identical, and so must the merge. The refusals use the same partials."""
import json, shutil, subprocess, sys
from pathlib import Path
import pytest
from model_v3.out import split as sp
pytestmark = pytest.mark.split
REPO = Path(__file__).resolve().parents[3]
RUN = "import sys; sys.path.insert(0, 'model'); from model_v3 import run; run.main(sys.argv[1:])"
ARGS = ['--size', 'smoke', '--point', 'median_mid', '--point', 'max_mid', '--run-date', '2026-11-28', '--batch', '2']

def run(*a, ok=True):
    r = subprocess.run([sys.executable, '-I', '-c', RUN, *ARGS, *a], cwd=REPO, capture_output=True, text=True)
    assert (r.returncode == 0) == ok, r.stderr[-800:]
    return r

def units(d, order=1):
    return sp.expected(sp.loads((d / 'plan.json').read_bytes())['header'])[1:][::order]

@pytest.fixture(scope='module')
def work(tmp_path_factory):
    d = tmp_path_factory.mktemp('split'); run('--out', str(d / 'unsplit'))
    run('--unit', 'plan', '--out', str(d / 'a'))
    for u in units(d / 'a'): run('--unit', u, '--plan-file', str(d / 'a/plan.json'), '--out', str(d / 'a'))
    run('--merge', str(d / 'a'), '--out', str(d / 'merged_a'))
    shutil.copytree(d / 'a', d / 'b', ignore=shutil.ignore_patterns('o1e*', 'point_max_mid*'))
    for u in [x for x in units(d / 'a', -1) if x.startswith('o1e')] + ['point:max_mid']: run('--unit', u, '--plan-file', str(d / 'a/plan.json'), '--out', str(d / 'b'))
    run('--merge', str(d / 'b'), '--out', str(d / 'merged_b'))
    return d

def test_the_merge_equals_the_unsplit_run_byte_for_byte(work):
    assert (work / 'unsplit/outputs.json').read_bytes() == (work / 'merged_a/outputs.json').read_bytes()

def test_o1e_units_in_the_other_order_and_one_point_rerun_give_identical_partials_and_merge(work):
    assert sorted(p.name for p in (work / 'a').glob('*.json') if '.meta' not in p.name) == sorted(p.name for p in (work / 'b').glob('*.json') if '.meta' not in p.name)
    assert all((work / 'a' / p.name).read_bytes() == p.read_bytes() for p in (work / 'b').glob('*.json') if '.meta' not in p.name)
    assert (work / 'merged_a/outputs.json').read_bytes() == (work / 'merged_b/outputs.json').read_bytes()

def refuse(work, tmp_path, edit, text, *extra):
    d = tmp_path / 'p'; shutil.copytree(work / 'a', d); edit(d)
    r = run('--merge', str(d), '--out', str(tmp_path / 'out'), *extra, ok=False)
    assert text in r.stderr and not (tmp_path / 'out/outputs.json').exists()

def change(name, field, value):
    def edit(d):
        p = sp.loads((d / name).read_bytes()); p['header'][field] = value; (d / name).write_bytes(sp.dumps(p))
    return edit

def test_a_partial_with_another_seed_numerics_or_sha_is_refused_with_its_field(work, tmp_path):
    refuse(work, tmp_path, change('point_median_mid.json', 'seed', 7), 'header field seed')
    refuse(work, tmp_path / 'n', change('point_median_mid.json', 'numerics', {'variable': '', 'probe': 'x'}), 'header field numerics')
    refuse(work, tmp_path / 'g', change('o1e-point.json', 'git_sha', '0' * 40), 'header field git_sha')

def test_a_missing_unit_and_an_invocation_that_differs_from_the_partials_are_refused(work, tmp_path):
    refuse(work, tmp_path, lambda d: (d / 'o1e_S_central_2_3.json').unlink(), 'missing')
    refuse(work, tmp_path / 'i', lambda d: None, 'header field seed', '--seed', '2')
