"""c1_noise.py (brief 187c): the limit rule and the Monte Carlo law check, on synthetic paths with a known standard deviation."""
import importlib.util
from pathlib import Path

import numpy as np

SCRIPT = Path(__file__).resolve().parents[3] / 'model/tools/c1_noise.py'
spec = importlib.util.spec_from_file_location('c1_noise', SCRIPT)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)


MANY = tuple(range(200))                                              # many seeds: sd is then known to about 5%, so the law check can be tight


def fake(n=4000, seeds=c1.SEEDS):
    return {s: {o: np.random.default_rng(s + i).normal(1.0, 2.0, n) for i, o in enumerate(c1.OUTS)} for s in seeds}


def test_q_is_the_99th_percentile_of_a_range_of_five_normals():
    q = c1.q_factor()
    assert 4.5 < q < 4.7 and c1.q_factor(0.05) < q


def test_the_law_and_the_limit_on_normal_paths():
    rows, limits, extra = c1.analyse(fake(800, MANY), MANY, 800)
    assert all(0.75 < r['ratio'] < 1.25 for r in rows if r['statistic'] == 'mean')
    sd_true = 2.0 / np.sqrt(800)                                     # the sd of a mean
    assert abs(limits['O1']['mean'] / (extra['q'] * sd_true) - 1) < 0.2 and all(v > 0 for o in limits.values() for v in o.values())


def test_the_ceiling_caps_the_limit():
    _, limits, _ = c1.analyse(fake(), c1.SEEDS, 4000, ceiling=0.01)
    assert all(v <= 0.01 for o in limits.values() for v in o.values())


def test_a_constant_output_has_a_zero_limit_not_a_crash():
    p = fake()
    for s in p:
        p[s]['O4a'] = np.ones(4000)
    rows, limits, _ = c1.analyse(p, c1.SEEDS, 4000)
    assert limits['O4a']['p10'] == 0.0 and np.isnan([r['ratio'] for r in rows if r['output'] == 'O4a'][0])
