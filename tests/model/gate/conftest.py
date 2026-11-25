"""Fixture repositories for the gate checker: a synthetic complete one and ways to break it."""
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'model' / 'tools'))
import check_gate as cg  # noqa: E402

MANIFEST = """version: "fx-1"
country_pack: UK
horizons: [short, long]
schedules: [S_low, S_central]
outputs:
  - {id: O1, metric: M1, title: t, summary: p10_mean_p90, unit: pct, decimals: 1, element: [H0, FISC], kind: headline}
  - {id: O2, metric: M2, title: t, summary: p10_mean_p90, by: {wealth_band: [overall, D10]}, unit: pct, decimals: 1, element: [FISC], kind: headline}
  - {id: OB1, metric: B1, title: t, summary: point_and_range, horizons: [single], element: [MECH], kind: line}
"""


def w(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return p


def cells_for(manifest_horizons=('short', 'long')):
    c = []
    for s in ('S_low', 'S_central'):
        for h in manifest_horizons:
            c.append({'schedule': s, 'horizon': h, 'by': {}, 'p10': 1.0, 'mean': 2.0, 'p90': 3.0})
    return c


def make_repo(root: Path) -> Path:
    """Every gate input present and correct for a page set of HUB, MECH, FISC, VAL, FAIR."""
    w(root, 'docs/model-v3/outputs.yml', MANIFEST)
    w(root, 'docs/model-v3/inputs.md',
      '| ID | Input | Low | Central | High | How |\n|---|---|---|---|---|---|\n'
      '| I-A | one | 1 | 2 | 3 | **(J)** judged |\n| I-B | two | 1 | 2 | 3 | derived |\n| I-C | three | 1 | 2 | 3 | (J) judged |\n')
    w(root, 'docs/model-v3/judgement-decisions.md',
      '| ID | Input | Low | Central | High | Decision | Date |\n|---|---|---|---|---|---|---|\n'
      '| I-A | one | 1 | 2 | 3 | accepted | 2026-11-20 |\n| I-C | three | 1 | 2 | 3 | replaced by I-B | 2026-11-21 |\n')
    w(root, 'docs/model-v3/architecture.md', '# arch\n')
    w(root, 'docs/model-v3/acceptance.md', f'# acceptance\n\nAcceptance command: `{sys.executable} -c "import sys; sys.exit(0)"`\n')
    w(root, 'docs/archive/briefs/011g-model-v3-design.md', '# 011g\n')
    w(root, 'data/input-register/inputs.json', json.dumps({'inputs': [{'id': 'I-A'}, {'id': 'I-B'}, {'id': 'I-C'}]}))
    man = root / 'docs/model-v3/outputs.yml'
    inp = root / 'data/input-register/inputs.json'
    outputs = {'O1': {'summary': 'p10_mean_p90', 'cells': cells_for()},
               'O2': {'summary': 'p10_mean_p90', 'cells': [dict(c, by={'wealth_band': b}) for c in cells_for() for b in ('overall', 'D10')]},
               'OB1': {'summary': 'point_and_range', 'cells': [{'schedule': 'S_low', 'horizon': 'single', 'by': {}, 'point': 1, 'lo': 0, 'hi': 2},
                                                               {'schedule': 'S_central', 'horizon': 'single', 'by': {}, 'point': 1, 'lo': 0, 'hi': 2}]}}
    w(root, 'model_v3/OUTPUTS/outputs.json', json.dumps({
        'schema': 'wdt-outputs/1',
        'run': {'status': 'final', 'fixture': False, 'manifest_version': 'fx-1', 'manifest_sha256': cg.sha256(man),
                'inputs_sha256': cg.sha256(inp)},
        'outputs': outputs}))
    w(root, 'model/tools/validate_outputs.py', 'import sys; sys.exit(0)\n')
    for files in cg.BRIEF_FILES.values():
        for f in files:
            if f.endswith('/') or '.' not in Path(f).name:
                (root / f).mkdir(parents=True, exist_ok=True)
            elif f != 'model/tools/validate_outputs.py':
                w(root, f, '')
    for d in cg.G5_TEST_DIRS:
        w(root, f'{d}/test_{Path(d).name}.py', 'def test_ok():\n    pass\n')
    w(root, 'tools/fixture_build.py',
      'import json, pathlib\np = pathlib.Path("_build"); p.mkdir(exist_ok=True)\n'
      '(p / "hooks-report.json").write_text(json.dumps({"unresolved": 0}))\n')
    pages = {'HUB': ('[O1]', ''), 'MECH': ('[OB1]', ''), 'FISC': ('[O1, O2]', ''), 'VAL': ('[]', '[I-A]'), 'FAIR': ('[]', '')}
    rows = []
    for pid, (outs, ins) in pages.items():
        fm = f'---\nid: {pid}\noutputs: {outs}\n' + (f'inputs: {ins}\n' if ins else '') + '---\nbody\n'
        w(root, f'papers/legacy/{pid.lower()}.md', fm)
    return root


@pytest.fixture
def cfg(tmp_path):
    root = make_repo(tmp_path / 'repo')
    return replace(cg.Config(), root=root, fixture_build=(sys.executable, 'tools/fixture_build.py'), timeout=120)


@pytest.fixture
def all_pages():
    return ['HUB', 'MECH', 'FISC', 'VAL', 'FAIR']
