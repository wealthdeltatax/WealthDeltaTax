"""Rule tests R4, R8, R11 and R9 (acceptance V3-1): each passes on the real tree and fails on a seeded violation."""
import pytest

SEEDS = {   # rule -> (checker, files of a temporary tree that break it)
    'cross-layer import': ('graph', {'core/revenue.py': 'from model_v3.core import burden\n', 'core/burden.py': ''}),
    'out imports core': ('graph', {'out/writer.py': 'from model_v3.core import pack\n', 'core/pack.py': ''}),
    'lazy import': ('lazy', {'core/pack.py': 'def f():\n    import json\n'}),
    'env set on import': ('side', {'core/pack.py': "import os\nos.environ['X'] = '1'\n"}),
    'file written on import': ('side', {'core/pack.py': "open('x.txt', 'w').close()\n"}),
    'orphan function': ('orphan', {'core/pack.py': 'def unused():\n    pass\n'}),
    'country name in code': ('country', {'core/base.py': 'x = "UK"\n'}),
    'tax name in code': ('country', {'core/base.py': 'rate = "council tax"\n'}),
    'file over budget': ('budget', {'core/pack.py': 'x = 1\n' * 400}),
}

@pytest.mark.parametrize('rule', SEEDS)
def test_clean_tree_passes(R, rule):
    assert R.CHECKS[SEEDS[rule][0]](R.MODEL, R.TESTS) == []

@pytest.mark.parametrize('rule', SEEDS)
def test_seeded_violation_fails(R, rule, tmp_path):
    assert R.CHECKS[SEEDS[rule][0]](R.tree(tmp_path, SEEDS[rule][1]), tmp_path / 'tests')

def test_allowed_edges_are_not_flagged(R, tmp_path):
    ok = {'core/pack.py': '', 'core/base.py': 'from model_v3.core import pack\n', 'runner/runner.py': 'from model_v3 import interface\nfrom model_v3.core.base import x\n',
          'out/writer.py': 'from ..interface import Samples\nimport json\n'}
    assert R.graph_errors(R.tree(tmp_path, ok)) == []

def test_interface_contract():
    from model_v3 import interface
    assert {'Samples', 'Level2', 'TornadoRow'} <= set(dir(interface))
