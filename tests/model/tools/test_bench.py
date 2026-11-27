"""bench.py compare (brief 176c): one changed bit is `identical: no`, and files from different numerics settings or CPUs are refused unless forced."""
import importlib.util
import json
import struct
from pathlib import Path

import numpy as np

SCRIPT = Path(__file__).resolve().parents[3] / 'model/studies/run-cost/bench.py'
spec = importlib.util.spec_from_file_location('bench', SCRIPT)
bench = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench)

HEAD = {'cpu_model': 'cpu A', 'cores': 2, 'memory': '8 GB', 'numpy': '2.0.0', 'NPY_DISABLE_CPU_FEATURES': 'X86_V4', 'git_sha': 'a', 'git_dirty': False, 'workers': 1}


def flip(x):
    """x with its lowest mantissa bit toggled."""
    return struct.unpack('<d', struct.pack('<Q', struct.unpack('<Q', struct.pack('<d', x))[0] ^ 1))[0]


def doc(result, head=None, seconds=2.0):
    return {'header': dict(head or HEAD), 'cases': {'c1': {'seconds': seconds, 'all_seconds': [seconds], 'reps': 1, 'hash': bench.digest(result)}}}


def run(a, b, force=False):
    lines = []
    return bench.compare(a, b, force, say=lines.append), '\n'.join(lines)


def test_the_same_result_is_identical():
    res = {'M1': np.array([0.1, 0.2, 0.3]), 'x': 0.5}
    code, out = run(doc(res), doc(res, seconds=1.0))
    assert code == 0 and 'identical: yes' in out and 'ratio  0.500' in out


def test_one_changed_bit_in_a_float_is_flagged():
    code, out = run(doc({'x': 0.5}), doc({'x': flip(0.5)}))
    assert flip(0.5) != 0.5 and code == 1 and 'identical: no' in out


def test_one_changed_bit_in_an_array_is_flagged():
    a = np.array([0.1, 0.2, 0.3])
    b = a.copy(); b[1] = flip(b[1])
    code, out = run(doc({'M': a}), doc({'M': b}))
    assert code == 1 and 'identical: no' in out


def test_a_different_numerics_setting_or_cpu_is_refused_unless_forced():
    res = {'x': 0.5}
    for key, val in (('NPY_DISABLE_CPU_FEATURES', 'unset'), ('cpu_model', 'cpu B'), ('numpy', '2.1.0')):
        code, out = run(doc(res), doc(res, {**HEAD, key: val}))
        assert code == 2 and 'REFUSED' in out and key in out and 'identical' not in out
        code, out = run(doc(res), doc(res, {**HEAD, key: val}), force=True)
        assert code == 0 and 'FORCED' in out and 'identical: yes' in out


def test_a_different_core_count_only_warns():
    res = {'x': 0.5}
    code, out = run(doc(res), doc(res, {**HEAD, 'cores': 4}))
    assert code == 0 and 'WARNING: cores differs' in out


def test_the_command_line_compare_reads_files(tmp_path, capsys):
    res = {'x': 0.5}
    (tmp_path / 'a.json').write_text(json.dumps(doc(res)))
    (tmp_path / 'b.json').write_text(json.dumps(doc({'x': flip(0.5)})))
    assert bench.main(['compare', str(tmp_path / 'a.json'), str(tmp_path / 'b.json')]) == 1
    assert 'identical: no' in capsys.readouterr().out


def test_the_run_date_is_masked_in_an_outputs_file():
    a = b'{"run": {"run_date": "2026-11-26", "paths": 1000}}'
    b = b'{"run": {"run_date": "2026-12-01", "paths": 1000}}'
    assert a != b and bench.mask_date(a) == bench.mask_date(b) and b'2026' not in bench.mask_date(a)
    assert bench.mask_date(a) != bench.mask_date(b.replace(b'1000', b'1001'))
