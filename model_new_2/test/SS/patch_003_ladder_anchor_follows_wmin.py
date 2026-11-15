"""
patch_NNN_ladder_anchor_follows_wmin.py -- the first anchor of a rate ladder sits at the scenario's W_min (rates_core.calibration).

Files edited : rates_core.py
Changes numbers?  YES, only together with the TOML patch (wmin_house_ratio 0.5): for every ladder scenario (gain_ladder and all gl_* /
    *_cohort* / stock_ladder variants) the ladder now starts at W_min = 0.5 x house median = GBP 0.1125m with the first anchor's target
    rate (3% gain, 0.15% stock), instead of being flat from W_min to GBP 0.225m. Alone (W_min still GBP 0.225m) it changes nothing.
    Scenarios with W_min = 0 (wmin_all) or W_min set by wmin_pct keep the TOML anchors. JSON field schedule_diag.anchors_target now holds the
    EFFECTIVE anchors (first one at W_min); anchors_tau likewise. Re-run: rates_core -> 8_2/8_3 tables and charts; valgen_core if VAL reads a ladder.
Rule: wmin in (0, second anchor): replace the first anchor's W by wmin. Otherwise the TOML anchors are used as written.

Run from Model/test:   python patch_NNN_ladder_anchor_follows_wmin.py [--apply]     Test: python test_patch_NNN_ladder_anchor_follows_wmin.py [--live]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wdt_patchlib import Replace, InsertBefore, patch_cli           # noqa: E402

NAME = Path(__file__).stem

HELPER = '''def _anchors_at_wmin(anchors, wmin):
    """A ladder's first anchor sits at W_min (decided 17 Oct 2026), so the schedule starts where the tax does and has no flat stretch.
    Only when 0 < W_min < the second anchor; W_min = 0 (every adult in scope), W_min above the second anchor, or W_min set later by
    wmin_pct keep the anchors as written in [rates.schedules.*]. The first anchor keeps its target rate."""
    if wmin and 0 < wmin < anchors[1][0]:
        return [[float(wmin), anchors[0][1]]] + [list(a) for a in anchors[1:]]
    return anchors


'''

SPEC = {'rates_core.py': [
    InsertBefore(
        anchor='def calibration(J, cfg, p):',
        new=HELPER,
        label='helper _anchors_at_wmin',
        done='def _anchors_at_wmin(anchors, wmin):'),
    Replace(
        old="""        sp = rp['schedules'][sched]
        ladder, capped = wc.ladder_to_tau(sp['anchors'], sp['basis'], sp['r_ref'], sp['c_ref'],
                                          cfg['tau_m'])
        sdiag = {'name': sched, 'basis': sp['basis'], 'r_ref': sp['r_ref'], 'c_ref': sp['c_ref'],
                 'anchors_target': sp['anchors'], 'anchors_tau': ladder, 'capped_at_tau_m': capped}""",
        new="""        sp = rp['schedules'][sched]
        anchors = _anchors_at_wmin(sp['anchors'], wmin_gbp_m)
        ladder, capped = wc.ladder_to_tau(anchors, sp['basis'], sp['r_ref'], sp['c_ref'],
                                          cfg['tau_m'])
        sdiag = {'name': sched, 'basis': sp['basis'], 'r_ref': sp['r_ref'], 'c_ref': sp['c_ref'],
                 'anchors_target': anchors, 'anchors_tau': ladder, 'capped_at_tau_m': capped}""",
        label='calibration: ladder from anchors at W_min',
        done="anchors = _anchors_at_wmin(sp['anchors'], wmin_gbp_m)"),
]}

if __name__ == '__main__':
    sys.exit(patch_cli(SPEC, NAME, __doc__))
