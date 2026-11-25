import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import check_gate as cg

REPO = Path(__file__).resolve().parents[3]


def run(cfg, argv):
    return cg.main(argv, cfg=cfg)


def test_complete_fixture_all_open(cfg, all_pages):
    res = cg.evaluate(cfg, all_pages)
    for p, r in res.items():
        assert cg.open_of(r), (p, {g: r[g] for g in cg.ALL5 if not r[g][0]})
    assert run(cfg, ['--page', 'MECH']) == 0


def test_needs_table(cfg):
    res = cg.evaluate(cfg, ['HUB', 'VAL', 'FAIR'])
    assert res['HUB']['needs'] == cg.ALL5
    assert res['VAL']['needs'] == ('G3', 'G5')
    assert res['FAIR']['needs'] == ('G5',)


def test_26_units():
    assert len(cg.PAGES) == 26


def test_page_without_outputs_escalates_when_it_cites_one(cfg):
    (cfg.root / 'papers/legacy/fair.md').write_text('---\nid: FAIR\noutputs: [O1]\n---\n', encoding='utf-8')
    assert cg.needs_of(cfg, 'FAIR', None) == cg.ALL5


def test_g3_counts_and_reports_pending(cfg):
    p = cfg.root / 'docs/model-v3/judgement-decisions.md'
    p.write_text(p.read_text().replace('accepted | 2026-11-20', 'pending | '), encoding='utf-8')
    ok, why = cg.check_g3(cfg)
    assert not ok and '2 flagged (J) rows, 1 pending, 1 decided' in why


def test_g3_set_mismatch_and_bad_line(cfg):
    p = cfg.root / 'docs/model-v3/judgement-decisions.md'
    p.write_text(p.read_text().replace('replaced by I-B | 2026-11-21', 'replaced by I-ZZ | 2026-11-21'), encoding='utf-8')
    ok, why = cg.check_g3(cfg)
    assert not ok and 'malformed' in why
    q = cfg.root / 'docs/model-v3/inputs.md'
    q.write_text(q.read_text() + '| I-D | four | 1 | 2 | 3 | (J) new |\n', encoding='utf-8')
    ok, why = cg.check_g3(cfg)
    assert not ok and 'no line in the decisions file' in why


def test_g1_missing_and_no_single_command(cfg):
    (cfg.root / 'docs/model-v3/acceptance.md').write_text('# acceptance\nno command\n', encoding='utf-8')
    ok, why = cg.check_g1(cfg)
    assert not ok and '0 acceptance commands' in why
    (cfg.root / 'docs/model-v3/architecture.md').unlink()
    assert not cg.check_g1(cfg)[0]


def test_g1_failing_command(cfg):
    (cfg.root / 'docs/model-v3/acceptance.md').write_text(
        f'Acceptance command: `{sys.executable} -c "raise SystemExit(3)"`\n', encoding='utf-8')
    ok, why = cg.check_g1(cfg)
    assert not ok and 'exited 3' in why


def test_g2_each_condition(cfg):
    out = cfg.root / cfg.outputs_json
    base = json.loads(out.read_text())
    for key, val, frag in [('status', 'provisional', 'not final'), ('fixture', True, 'not false'),
                           ('manifest_version', 'old', 'manifest_version'), ('manifest_sha256', 'ab', 'manifest_sha256'),
                           ('inputs_sha256', 'ab', 'inputs_sha256')]:
        d = json.loads(json.dumps(base))
        d['run'][key] = val
        out.write_text(json.dumps(d))
        ok, why = cg.check_g2(cfg)
        assert not ok and frag in why, (key, why)
    out.write_text(json.dumps(base))
    assert cg.check_g2(cfg)[0]
    (cfg.root / 'model/tools/validate_outputs.py').write_text('import sys; sys.exit(1)\n')
    ok, why = cg.check_g2(cfg)
    assert not ok and 'validator exited 1' in why


def test_g2_manifest_change_after_run_closes_gate(cfg):
    m = cfg.root / cfg.manifest
    m.write_text(m.read_text() + '# edit after the run\n', encoding='utf-8')
    ok, why = cg.check_g2(cfg)
    assert not ok and 'manifest_sha256' in why


def test_g4_null_and_missing_cells(cfg):
    out = cfg.root / cfg.outputs_json
    d = json.loads(out.read_text())
    d['outputs']['O1']['cells'][0]['mean'] = None
    out.write_text(json.dumps(d))
    ok, why = cg.check_g4(cfg, 'FISC')
    assert not ok and 'mean=None' in why
    d['outputs']['O1']['cells'][0]['mean'] = 2.0
    del d['outputs']['O2']['cells'][-1]
    out.write_text(json.dumps(d))
    ok, why = cg.check_g4(cfg, 'FISC')
    assert not ok and 'missing 1 of 8 cells' in why


def test_g4_r1_both_ways(cfg):
    (cfg.root / 'papers/legacy/fisc.md').write_text('---\nid: FISC\noutputs: [O1, OB1]\n---\n', encoding='utf-8')
    ok, why = cg.check_g4(cfg, 'FISC')
    assert not ok and 'O2 but front matter' in why and 'OB1 but the manifest' in why


def test_g4_input_not_in_register(cfg):
    (cfg.root / 'papers/legacy/val.md').write_text('---\nid: VAL\ninputs: ["{{i:I-NOPE}}"]\n---\n', encoding='utf-8')
    ok, why = cg.check_g4(cfg, 'VAL')
    assert not ok and 'I-NOPE' in why


def test_g5_pieces(cfg):
    assert cg.check_g5(cfg)[0]
    (cfg.root / 'website/build/hooks.py').unlink()
    ok, why = cg.check_g5(cfg)
    assert not ok and 'B3 not merged' in why
    (cfg.root / 'website/build/hooks.py').write_text('')
    (cfg.root / 'tests/website/hooks/test_hooks.py').write_text('def test_bad():\n    assert False\n')
    ok, why = cg.check_g5(cfg)
    assert not ok and 'pytest' in why
    (cfg.root / 'tests/website/hooks/test_hooks.py').write_text('def test_ok():\n    pass\n')
    assert cg.check_g5(replace(cfg, fixture_build=None))[0] is False


def test_g5_unresolved_hooks(cfg):
    (cfg.root / 'tools/fixture_build.py').write_text(
        'import json, pathlib\np = pathlib.Path("_build"); p.mkdir(exist_ok=True)\n'
        '(p / "hooks-report.json").write_text(json.dumps({"unresolved": ["H21"]}))\n')
    ok, why = cg.check_g5(cfg)
    assert not ok and 'unresolved' in why


def test_cli_exit_codes_and_all_table(cfg, capsys):
    assert run(cfg, ['--page', 'bogus']) == 2
    out = cfg.root / cfg.outputs_json
    out.unlink()
    assert run(cfg, ['--page', 'MECH']) == 1
    capsys.readouterr()
    # --all on the fixture: the 21 pages the fixture has no source for stay open or closed by their own needs, never crash
    assert run(cfg, ['--all']) == 1
    text = capsys.readouterr().out
    assert 'G2 FAIL' in text and 'pages open' in text


def test_real_repository_is_closed_today():
    """The repository as it stands: G1, G2, G3 fail and --all exits non-zero. Retire this test when the gate opens."""
    if (REPO / 'model_v3/OUTPUTS/outputs.json').exists():
        return
    p = subprocess.run([sys.executable, '-B', str(REPO / 'model/tools/check_gate.py'), '--all'],
                       capture_output=True, text=True, cwd=REPO)
    assert p.returncode == 1
    for g in ('G1 FAIL', 'G2 FAIL', 'G3 FAIL'):
        assert g in p.stdout
    assert 'flagged (J) rows' in p.stdout
