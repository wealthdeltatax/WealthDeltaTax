"""
patch_003_ct_retire_308.py -- corporation-tax retire share 3.2% -> 3.08% of GDP (the D5 target: OECD 1200 UK, trailing 5-year 2020-24).

Files edited : WDT_Params.toml
Changes numbers?  YES.
    [rates.replacement].retire: ["Corporation tax", 0.0320] -> 0.0308. This is (a) the corporate-tax relief in the tax-replacement tables (T17 to T22 / F17 to F22: the
    leftover relief that funds the thresholds X and X_e falls by 0.12 pp of GDP, so those thresholds fall), and (b) the target of the levy calibration
    ([rates.levy_calibration].target = "Corporation tax"), so the solved tau0 and the levy columns move (levy-related tables incl. T25 / F25 and the headline tables).
    Re-run: rates_core -> 8_2/8_3 tables and charts (and valgen_core if it reads the levy through the rate scenario).
Decision: 16 Oct (D5 year basis 3.08%, latest year 3.47% as sensitivity), 17 Oct (scope: all corporate profit taxes; HMRC Table 1A reconciliation,
    claude/d5_hmrc_oecd_reconciliation_2026-10-17.md). The entry keeps its name "Corporation tax" because the calibration looks it up by name.
The 3.47% sensitivity and the corporation-tax-proper variant (2.86%) are NOT added here.

Run from Model/test:  python patch_003_ct_retire_308.py [--apply]     Test: python test_patch_003_ct_retire_308.py [--live]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wdt_patchlib import Replace, patch_cli           # noqa: E402

NAME = Path(__file__).stem

SPEC = {'WDT_Params.toml': [
    Replace(
        old='["Corporation tax", 0.0320]]',
        new='["Corporation tax", 0.0308]]',
        label='retire: Corporation tax 0.0320 -> 0.0308',
        done='["Corporation tax", 0.0308]]'),
    Replace(
        old='its share of GDP is the target ("Corporation tax" = 3.2%)',
        new='its share of GDP is the target ("Corporation tax" = 3.08%: OECD 1200 UK, trailing 5-year 2020-24, all corporate profit taxes; 3.47% latest year is the sensitivity)',
        label='levy_calibration comment',
        done='("Corporation tax" = 3.08%: OECD 1200 UK'),
]}

if __name__ == '__main__':
    sys.exit(patch_cli(SPEC, NAME, __doc__))
