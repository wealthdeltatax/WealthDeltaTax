"""V3-4 schedule tests S1 to S5 (architecture.md 6.2). Self-contained: no conftest needed."""
import ast
import math
import pathlib
import sys

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from model_v3.core import schedule as S  # noqa: E402

P = dict(k=0.002, tau_0=0.04, tau_m=0.9, W_min=0.5)
PL = dict(k=1.0, tau_0=0.04, tau_m=0.9, W_min=0.5)


def test_S1_tau_at_wmin_is_tau0_and_rises_to_taum():
    for form, p, top in (('logistic', P, 0.5 + 60 / 0.002), ('logistic_ln', PL, 0.5 * math.exp(60))):
        assert S.tau(p['W_min'], form=form, **p) == pytest.approx(p['tau_0'], abs=1e-15)
        assert S.tau(top, form=form, **p) == pytest.approx(p['tau_m'], abs=1e-12)
        assert S.tau(p['W_min'] * 0.999, form=form, **p) == 0.0
        assert S.tau(np.array([0.0, -3.0]), form=form, **p).tolist() == [0.0, 0.0]


def test_S2_marginal_rate_monotone_on_grid():
    for form, p in (('logistic', P), ('logistic_ln', PL)):
        f = S.rate_function(form=form, **p)
        W = np.geomspace(0.5, 1e7, 4000)
        assert np.all(np.diff(f(W)) >= 0.0)


@pytest.mark.parametrize('form,bad', [
    ('logistic', dict(P, k=-0.002)),                 # rate falls with wealth
    ('logistic', dict(P, tau_m=0.02)),               # ceiling below the floor
    ('logistic_ln', dict(PL, k=-1.0)),
    ('logistic_ln', dict(PL, tau_m=0.03)),
])
def test_S3_non_progressive_draw_raises(form, bad):
    with pytest.raises(ValueError, match='progressive'):
        S.rate_function(form=form, **bad)


def test_S3_other_invalid_draws_raise():
    with pytest.raises(ValueError):
        S.rate_function(form='logistic_ln', **dict(PL, W_min=0.0))
    with pytest.raises(ValueError):
        S.rate_function(**dict(P, tau_0=0.0))
    with pytest.raises(ValueError):
        S.rate_function(**dict(P, tau_m=1.2))
    with pytest.raises(ValueError):
        S.rate_function(form='ladder', **P)


def test_S4_logistic_ln_matches_the_closed_form_at_five_points():
    # tau_m / (1 + ((tau_m - tau_0)/tau_0) * (W / W_min)^(-k)), written out by hand
    for W in (0.5, 1.0, 5.0, 50.0, 2000.0):
        want = 0.9 / (1.0 + ((0.9 - 0.04) / 0.04) * (W / 0.5) ** (-1.0))
        assert float(S.tau(W, form='logistic_ln', **PL)) == pytest.approx(want, rel=1e-14)
    # hand values: W = W_min gives tau_0; W = 2 W_min at k = 1 gives 0.9 / (1 + 21.5 / 2)
    assert float(S.tau(1.0, form='logistic_ln', **PL)) == pytest.approx(0.9 / 11.75, rel=1e-14)


def test_S5_no_ladder_branch_exists():
    assert S.FORMS == ('logistic', 'logistic_ln')
    with pytest.raises(ValueError):
        S.tau(1.0, form='ladder', **P)
    src = pathlib.Path(S.__file__).read_text().lower()
    code = [n for n in ast.walk(ast.parse(src)) if isinstance(n, (ast.FunctionDef, ast.Name))]
    assert not any('ladder' in (getattr(n, 'name', '') or getattr(n, 'id', '')) for n in code)


def test_schedule_imports_numpy_only():
    tree = ast.parse(pathlib.Path(S.__file__).read_text())
    mods = {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    mods |= {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert mods <= {'numpy', '__future__'}
