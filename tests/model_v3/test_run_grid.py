"""Brief 124c: the first-run script on a two-path smoke: one household grid point and the legacy context, the checks hold and every row carries its label."""
import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'docs' / 'model-v3' / 'household-arm-run' / 'run_grid.py'


def test_the_script_runs_a_smoke_grid_with_labels_and_holding_checks(tmp_path):
    spec = importlib.util.spec_from_file_location('run_grid', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main(['--paths', '2', '--out', str(tmp_path), '--points', 'median_mid'])
    res = list(csv.DictReader((tmp_path / 'grid_results.csv').open()))
    chk = list(csv.DictReader((tmp_path / 'checks.csv').open()))
    assert {r['grid'] for r in res} == {'median_mid', 'legacy'} and all('central' not in r['label'].replace('not central', '') for r in res)
    assert all(r['label'].startswith('household') for r in res if r['grid'] == 'median_mid') and all(r['label'].startswith('legacy') for r in res if r['grid'] == 'legacy')
    ids = {r['id'] for r in res if r['grid'] == 'median_mid'}
    assert not ids & {'OW3', 'OM1'} and {'O1', 'O2', 'O2d', 'OP1', 'O3', 'OW1'} <= ids and 'O3' in {r['id'] for r in res if r['grid'] == 'legacy'}
    c = chk[0]
    assert len(chk) == 1 and float(c['account_residual_max']) < 1e-9 and float(c['unpaid_max']) == 0 and float(c['unpaid_B_max']) == 0 and int(c['shortfall_lines']) == 0
    assert float(c['ledger_tie_max']) < 1e-9 and float(c['ledger_dL_max']) < 1e-9
