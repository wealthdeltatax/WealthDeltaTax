"""Output layer tests W1 to W7 (brief 056c): assemble.py and writer.py against synthetic Samples and the real validator."""
import copy, importlib.util, json, re, sys
from pathlib import Path

import numpy as np
import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(REPO))
from model_v3 import interface
from model_v3.out import assemble, writer

MANIFEST, INPUTS, LEVERS = (REPO / p for p in ('docs/model-v3/outputs.yml', 'registry/inputs.json', 'model_v3/levers.json'))
FIXTURE = REPO / 'tests/data/fixtures/outputs.fixture.json'
INFO = dict(status='provisional', run_date='2026-11-18', model_version='test', paths=50, base_year=2025)
spec = importlib.util.spec_from_file_location('validate_outputs', REPO / 'pipeline/validate_outputs.py')
V = importlib.util.module_from_spec(spec); sys.modules['validate_outputs'] = V; spec.loader.exec_module(V)

manifest = yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
input_ids = [r['id'] for r in json.loads(INPUTS.read_text(encoding='utf-8'))['inputs']]
IDS = assemble.entries(manifest)

def cell_key(c):
    return (c.get('schedule'), c['horizon'], tuple(sorted(c['by'].items())), c.get('line'))

def vals(summary, c, rng):
    if summary == 'p10_mean_p90':
        return rng.normal(c['mean'], 1.0, 400)
    return np.array([c[f] for f in {'point_and_range': ('point', 'lo', 'hi'), 'point': ('point',)}[summary]])

def synthetic(skip=()):
    """Samples with one array per cell of the fixture, minus the M15b cells the manifest gives only the transition horizon."""
    rng, samples = np.random.default_rng(7), {}
    for oid, out in fixture['outputs'].items():
        if oid in skip:
            continue
        lh = IDS[oid].get('line_horizons') or {}
        samples[oid] = {}
        for c in out['cells']:
            if c.get('line') in lh and c['horizon'] not in lh[c.get('line')]:
                continue
            samples[oid][cell_key(c)] = vals(out['summary'], c, rng)
            for pt in c.get('series', []):
                rest = tuple(p for p in cell_key(c)[2] if p[0] != 'year')
                samples[oid][(c.get('schedule'), c['horizon'], rest + (('t', pt['t']),), c.get('line'))] = rng.normal(pt['mean'], 1.0, 400)
    return samples

def level2():
    rows = (interface.TornadoRow(input_ids[1], -2.0, 1.0), interface.TornadoRow(input_ids[0], 0.5, 0.25))
    return {'O1': interface.Level2(rows, 0.1, 0.9)}

def good(status='provisional', samples=None, l2=None):
    outputs, lv = assemble.assemble(manifest, samples or synthetic(), l2 or level2(), status)
    return writer.document(outputs, lv, writer.run_block(manifest, MANIFEST, INPUTS, LEVERS, {**INFO, 'status': status}))

def findings(doc, mode='default'):
    return {(f.rule, f.level) for f in V.validate(doc, manifest, MANIFEST, INPUTS, mode)}

def test_w1_fixture_round_trip(tmp_path):
    doc = good()
    for oid, out in fixture['outputs'].items():
        lh = IDS[oid].get('line_horizons') or {}
        want = {cell_key(c) for c in out['cells'] if not (c.get('line') in lh and c['horizon'] not in lh[c.get('line')])}
        assert doc['outputs'][oid]['summary'] == out['summary']
        assert {cell_key(c) for c in doc['outputs'][oid]['cells']} == want
    assert not [f for f in findings(doc) if f[1] == 'error']
    writer.write_outputs(tmp_path, doc, MANIFEST, INPUTS)   # the validator runs inside and would raise

@pytest.mark.parametrize('rule,level,change', [
    ('V1', 'error', lambda d: d.update(schema='x')),
    ('V2', 'error', lambda d: d['outputs'].update(ZZ9={'summary': 'point', 'cells': []})),
    ('V3', 'error', lambda d: d['outputs']['O1a']['cells'][0].update(horizon='bogus')),
    ('V4', 'error', lambda d: d['outputs']['O1a']['cells'].append(copy.deepcopy(d['outputs']['O1a']['cells'][0]))),
    ('V5', 'error', lambda d: d['outputs']['O1a']['cells'][0].update(p10='x')),
    ('V6', 'error', lambda d: d['outputs']['O1a']['cells'][0].update(p10=9.0, p90=1.0)),
    ('V7', 'error', lambda d: (d['run'].update(status='final'), d['outputs']['O1a']['cells'].pop())),
    ('V8', 'error', lambda d: d['run'].update(manifest_version='old')),
    ('V9', 'error', lambda d: d['run'].update(status='final', inputs_sha256='0' * 64)),
    ('V10', 'error', lambda d: d['outputs']['OP6']['cells'][0]['series'].reverse()),
    ('V11', 'error', lambda d: (d['run'].update(status='final'), d['outputs'].update(OP6={**d['outputs']['OP6'], 'cells': [c for c in d['outputs']['OP6']['cells'] if c['by']['year'] != '25']}))),
    ('V12', 'warning', lambda d: d.update(extra=1)),
])
def test_w2_each_validator_rule_has_a_failing_input(rule, level, change):
    assert not [f for f in findings(good()) if f[1] == 'error']
    doc = good(); change(doc)
    assert (rule, level) in findings(doc)

def test_w3_percentiles_are_numpy_percentile_on_a_known_array():
    m = {'schedules': ['S'], 'horizons': ['h'], 'outputs': [{'id': 'O1', 'summary': 'p10_mean_p90'}, {'id': 'O7', 'summary': 'point_and_range'}]}
    arr = np.arange(1, 102, dtype=float) ** 1.5
    cell = assemble.assemble(m, {'O1': {('S', 'h', (), None): arr}, 'O7': {('S', 'h', (), None): [2.0, 1.0, 3.0]}})[0]
    p10, p90 = np.percentile(arr, [10, 90])
    assert {k: cell['O1']['cells'][0][k] for k in ('p10', 'mean', 'p90')} == pytest.approx({'p10': p10, 'mean': arr.mean(), 'p90': p90}, rel=1e-11)
    assert (cell['O7']['cells'][0]['point'], cell['O7']['cells'][0]['lo'], cell['O7']['cells'][0]['hi']) == (2.0, 1.0, 3.0)
    with pytest.raises(assemble.AssembleError):
        assemble.assemble(m, {'O7': {('S', 'h', (), None): [1.0, 2.0]}})

def test_w4_non_finite_is_an_error_when_final_and_null_when_provisional(tmp_path):
    bad = synthetic()
    k = next(iter(bad['O1a'])); bad['O1a'][k] = np.append(bad['O1a'][k], np.nan)
    with pytest.raises(assemble.AssembleError, match='non-finite'):
        assemble.assemble(manifest, bad, None, 'final')
    doc = good(samples=bad)
    assert doc['outputs']['O1a']['cells'][0]['p10'] is None
    assert b'null' in writer.write_outputs(tmp_path, doc, MANIFEST, INPUTS).read_bytes()
    with pytest.raises(writer.WriterError):
        writer.dumps({'x': float('nan')})

def test_w5_same_input_gives_the_same_bytes(tmp_path):
    a = writer.write_outputs(tmp_path / 'a', good(), MANIFEST, INPUTS).read_bytes()
    s = synthetic(); rev = {o: dict(reversed(list(c.items()))) for o, c in reversed(list(s.items()))}
    assert writer.write_outputs(tmp_path / 'b', good(samples=rev), MANIFEST, INPUTS).read_bytes() == a

def test_w6_an_id_not_in_the_manifest_raises():
    with pytest.raises(assemble.AssembleError, match='ZZ9'):
        assemble.assemble(manifest, {'ZZ9': {}})
    with pytest.raises(assemble.AssembleError, match='ZZ9'):
        assemble.assemble(manifest, {}, {'ZZ9': level2()['O1']})

def test_w7_module_to_id_table_covers_the_manifest_exactly():
    table = (REPO / 'docs/model-v3/architecture.md').read_text(encoding='utf-8').split('### 2.10')[1].split('39 outputs')[0]
    ids = [i for row in re.findall(r'^\| `[^`]+` \| (.+) \|$', table, re.M) for i in row.split(', ')]
    assert len(ids) == len(set(ids)) and set(ids) == set(IDS)

def test_series_lines_and_gaps(tmp_path):
    doc = good()
    assert all(len(c['series']) == 100 and c['series'][0]['t'] == 1 for c in doc['outputs']['OP6']['cells'])
    ow3 = {(c['line'], c['horizon']) for c in doc['outputs']['OW3']['cells']}
    assert ('M15b', 'transition') in ow3 and ('M15b', 'short') not in ow3 and ('M15a', 'long') in ow3
    short = synthetic(skip=('O2',))
    assert 'O2' not in good(samples=short)['outputs']
    with pytest.raises(assemble.AssembleError, match='O2'):
        assemble.assemble(manifest, short, None, 'final')
    one = synthetic(); one['O1a'].popitem()
    with pytest.raises(assemble.AssembleError, match='no samples'):
        assemble.assemble(manifest, one, None, 'final')
    one['O1a'][('S_central', 'short', (('x', 'y'),), None)] = [1.0]
    with pytest.raises(assemble.AssembleError, match='outside the manifest'):
        assemble.assemble(manifest, one)

def test_run_block_needs_run_information_and_rejects_unknown_fields():
    with pytest.raises(writer.WriterError, match='run_date'):
        writer.run_block(manifest, MANIFEST, INPUTS, LEVERS, {k: v for k, v in INFO.items() if k != 'run_date'})
    with pytest.raises(writer.WriterError, match='nonsense'):
        writer.run_block(manifest, MANIFEST, INPUTS, LEVERS, {**INFO, 'nonsense': 1})
    run = writer.run_block(manifest, MANIFEST, INPUTS, LEVERS, INFO)
    assert run['fixture'] is False and run['manifest_version'] == manifest['version'] and len(run['levers_sha256']) == 64

def test_validator_failure_raises(tmp_path):
    doc = good(); doc['schema'] = 'bad'
    with pytest.raises(writer.WriterError, match='rejected'):
        writer.write_outputs(tmp_path, doc, MANIFEST, INPUTS)
