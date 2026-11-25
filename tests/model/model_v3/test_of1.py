"""OF1 under tolerance and retirement-margin rules, its summary markers and CK1's window (brief 089c)."""

import numpy as np

from model_v3.runner import out_sweeps as O, runner as R, sweeps as S

from test_runner import SPEC, ctx, lv, out, tier1   # noqa: F401  (fixtures)


def _pts(ctx, n=3):
    ev = R.make_ev(ctx, np.random.default_rng(11).standard_normal((100, 40)))
    return ev, S.feasibility(ev, [SPEC, dict(SPEC, tau_m=0.5), dict(SPEC, k_ln=2.0)][:n])


def test_the_strict_rule_is_the_existing_headline_and_a_looser_tolerance_never_closes_fewer_paths(ctx):
    ev, (pts, of1) = _pts(ctx)
    e = ev(SPEC)
    for hz in ('transition', 'short'):
        assert pts[0]['F1'][hz] == 100 * (e['P3h'][hz] <= S.CLOSED).mean()                          # tol 0, margin 0 is the old definition
        assert np.isclose(pts[0]['M2'][hz], np.nanmean(e['M2'][hz]['overall'])) and np.isclose(pts[0]['M4a'][hz], np.nanmean(e['M4a'][hz]['overall']))
    for p in pts:
        for m in O.MARGINS:
            f = [p['map'][t, m]['short'][0] for t in O.TOLS]
            assert f == sorted(f)
    assert len(of1) == len(pts) * len(O.TOLS) * len(O.MARGINS) * 2 * 3 and {k[3] for k in of1} == {'F1', 'M2', 'M4a'}
    assert {dict(k[2])['tolerance'] for k in of1} == {O.tolabel(t, 0)[0] for t in O.TOLS} and {dict(k[2])['margin'] for k in of1} == {'m0', 'm10', 'm25'}


def test_the_summary_marks_where_no_schedule_passes_and_labels_relaxations():
    rule = dict(closure_share_pct=75, m2_cap_pct_per_year=2.0, m4a_floor_pct=0)
    mk = lambda f: {(t, m): {'transition': (f(t, m), 1.0, 5.0), 'short': (f(t, m), 1.0, 5.0)} for t in O.TOLS for m in O.MARGINS}
    pts = [dict(spec=i, schedule_grid=f'g{i}', w_min='r050', F1={}, M2={}, M4a={}, map=mk(lambda t, m, i=i: 40 + 10 * i + 20 * (t == 1.0 and m == 0.25))) for i in range(3)]
    s = S.map_summary(pts, rule)
    assert s[0.0, 0.0]['feasible'] == S.NONE_PASSES and s[0.0, 0.0]['named'] is None and s[0.0, 0.0]['best_any'][0] == 60        # nothing is chosen where nothing passes
    assert s[1.0, 0.25]['feasible'] == 1 and s[1.0, 0.25]['named'] is not None and s[1.0, 0.25]['best_inside'][1] == 'g2'


def test_ck1_reports_the_window_from_year_one_and_keeps_amplitude_zero(ctx):
    res, top = S.stress(R.make_ev(ctx, np.zeros((100, 1))), SPEC, 4.74, (0, 4), 100)
    assert set(res[0]) == {'P1', 'P3', 'P3_long', 'P7b'} and res[0]['P3_long'] >= res[0]['P3'] >= 0
    cells = O.ck1(res)['CK1']
    assert {dict(k[2])['amplitude'] for k in cells} == {'A0', 'A4'} and len(cells) == 6 and (top is None or res[0]['P3'] <= S.CLOSED)
