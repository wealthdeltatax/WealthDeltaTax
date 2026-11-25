"""Brief 138c block 1: M2 and M2d divide by total wealth (pension included) in the household arm; the legacy arm's `w0` is unchanged."""
import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'model' / 'studies' / 'household-arm-run' / 'run_grid.py'


def _mod():
    spec = importlib.util.spec_from_file_location('run_grid_m2', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_the_household_w0_is_total_wealth_from_year_2():
    """D5, `median_mid`, phase 0: 0.1252 in year 1 and total wealth 0.1286 in year 2 (the non-pension 0.0808 was 136c's defect); legacy `w0` is the family value as before (test_legacy_digest)."""
    mod = _mod()
    from model_v3.runner import runner as R
    ctx, inp = mod.A.setup()
    g = np.full((R.T, 1), 0.0157)
    c = mod.point_ctx(ctx, inp, 'median_mid')
    raw = R.core_run(c, c.centre, mod.A.SPEC, g, np.full(g.shape, c.gdp_g))
    w, d5 = raw.fl['w0'], raw.base.labels.index('D5')
    assert abs(w[0, d5, 0] - 0.1252) < 5e-4 and abs(w[1, d5, 0] - 0.1286) < 5e-4
