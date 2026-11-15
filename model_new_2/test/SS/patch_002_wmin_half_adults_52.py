"""
patch_002_wmin_half_adults_52.py -- W_min = half the median house price (wmin_house_ratio 1.0 -> 0.5) and adults_m 54.0 -> 52.0.

Files edited : WDT_Params.toml
Changes numbers?  YES.
    wmin_house_ratio 1.0 -> 0.5 moves W_min from about GBP 225,000 to GBP 112,500 per adult at launch. Every RATES scenario that
    applies the house-price W_min (the default and every scenario that sets 1.0 explicitly: 47 of them) moves, and VAL moves with it
    (VAL reads W_min from the rate scenario through wdt_core.with_rate_scenario). Scenarios that set wmin_house_ratio = 0.0
    (logistic comparisons, wmin_all) are untouched.
    adults_m only turns the WDT scope adult share into millions (T-tables that print millions of adults).
    Re-run: rates_core -> 8_2/8_3 tables and charts; valgen_core -> VAL tables and charts; anything reading rates_output.json.
Plan / decision   : decisions of 15 Oct 2026 (W_min per person = half the median house price) and 16 Oct 2026 (adults_m = 52.0, 18+ convention).

New scenario gain_ladder_wmin_full (decided 17 Oct 2026): the gain ladder with wmin_house_ratio 1.0 (W_min = the full median house price), added to the
[rates.run] scenarios list, so the effect of halving W_min can be read off beside gain_ladder. Its ladder starts at its own W_min (second patch).

Also (no numbers): the two scenario labels that say "median house price" (wmin_house, wmin_house_hp) now say "half the median house price".
house_median_gbp_m: only the COMMENT changes (0.225 is the ONS HPSSA England median, existing dwellings, year ending Dec 2017, not a mean; status note 16 Oct s.5).

Ladder anchors are NOT edited here: patch_NNN_ladder_anchor_follows_wmin.py makes the first anchor of a ladder follow W_min in rates_core,
so the TOML anchors stay as the W_min = 0 / fallback values. Apply that patch with this one, or the ladders stay flat below GBP 0.225m.

Run from Model/test:
    python patch_002_wmin_half_adults_52.py            dry run
    python patch_002_wmin_half_adults_52.py --apply
Test:
    python test_patch_002_wmin_half_adults_52.py
    python test_patch_002_wmin_half_adults_52.py --live
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wdt_patchlib as wl                                            # noqa: E402
from wdt_patchlib import Replace, InsertBefore, patch_cli                          # noqa: E402

NAME = Path(__file__).stem

# Scenarios that carry an explicit wmin_house_ratio = 1.0 in the TOML as audited on 16 Oct 2026.
# Their blocks are located in the real file at import time and rewritten, so no block is retyped here.
SCENARIOS = [
    'wmin_house', 'wmin_house_hp', 'gain_ladder', 'stock_ladder', 'logistic_ln_ref', 'logistic_ln_gain', 'logistic_ln_stock',
    'logistic_gain', 'logistic_stock', 'stock_ladder_cohort', 'gain_ladder_cohort', 'gain_ladder_cohort_upper',
    'gl_c_001', 'gl_c_002', 'gl_c_005', 'gl_stationary', 'gl_top6_1', 'gl_top6_1_free', 'gain_ladder_cohort_upper_c1',
    'gl_levy_cal_nominal', 'gl_levy_cal_real', 'gl_levy_stat_f002', 'gl_levy_stat_f005', 'gl_levy_stat_f010',
    'gl_levy_stat_f015', 'gl_levy_stat_f020', 'gain_ladder_rule_base',
    'gl_rb_sale', 'gl_rb_lien', 'gl_rb_lien_sp0', 'gl_rb_lien_sp3', 'gl_rb_lien_sp6', 'gl_rb_lien_sp12',
    'gl_rb_income', 'gl_rb_income_cap75', 'gl_rb_income_cap50',
    'gl_arch_wealth', 'gl_arch_housing_pension', 'gl_arch_startup_founder', 'gl_arch_generational', 'gl_arch_ceo_fintech',
    'gl_arch_resource_monopoly', 'gl_arch_blend', 'gl_arch_wealth_lien', 'gl_arch_wealth_income',
    'gl_arch_wealth_lam005', 'gl_arch_wealth_lam005_dv',
]
SENS = 'gain_ladder_wmin_full'   # new sensitivity scenario: W_min = the FULL median house price (ratio 1.0); stays at 1.0 on purpose
LABEL_FIX = {'W_min = median house price': 'W_min = half the median house price'}   # inside the blocks above only

NEW_RATIO = '0.5'


def _toml_text() -> str:
    return wl._read(wl.find_file('WDT_Params.toml')).replace('\r\n', '\n')


def _scenario_ops(text: str) -> list:
    """One Replace per scenario: from its [rates.scenarios.NAME] header through its wmin_house_ratio line (1.0, or 0.5 if already patched)."""
    ops = []
    # guard: a scenario carrying 1.0 that this list does not know would be left behind silently
    known = set(SCENARIOS)
    for m in re.finditer(r'\[rates\.scenarios\.([A-Za-z0-9_]+)\]\n(?:(?!\[)[^\n]*\n)*?wmin_house_ratio = 1\.0\b', text):
        if m.group(1) not in known and m.group(1) != SENS:
            raise wl.PatchError(f'scenario {m.group(1)} has wmin_house_ratio = 1.0 but is not in SCENARIOS; add it, or set it to 0.0 on purpose')
    for name in SCENARIOS:
        pat = re.compile(r'\[rates\.scenarios\.' + re.escape(name) + r'\]\n(?:(?!\[)[^\n]*\n)*?wmin_house_ratio = (?:1\.0|' + re.escape(NEW_RATIO) + r')[^\n]*\n')
        hits = list(pat.finditer(text))
        if len(hits) != 1:
            raise wl.PatchError(f'scenario {name}: expected one block with wmin_house_ratio, found {len(hits)}')
        old = hits[0].group(0)
        new = re.sub(r'wmin_house_ratio = (?:1\.0|' + re.escape(NEW_RATIO) + ')', 'wmin_house_ratio = ' + NEW_RATIO, old)
        for a, b in LABEL_FIX.items():
            new = new.replace(a, b)
        ops.append(Replace(old=old, new=new, label=f'scenario {name}: wmin_house_ratio -> {NEW_RATIO}', done=new))
    return ops


def build_spec() -> dict:
    text = _toml_text()
    ops = [
        Replace(
            old='wmin_house_ratio = 1.0             # W_min = ratio x median house price at launch (0.0 = off:',
            new='wmin_house_ratio = 0.5             # W_min = ratio x median house price at launch (0.5 = half the median, decided 15 Oct 2026; 0.0 = off:',
            label='[rates.defaults] wmin_house_ratio -> 0.5',
            done='wmin_house_ratio = 0.5             # W_min = ratio x median house price at launch (0.5 = half the median, decided 15 Oct 2026; 0.0 = off:'),
        Replace(
            old='adults_m         = 54.0     # PLACEHOLDER: UK adults, millions (ONS; VERIFY). Only used',
            new='adults_m         = 52.0     # UK adults 18+, millions = population / pop_per_adult 1.27 (decided 16 Oct 2026; VERIFY against ONS). Only used',
            label='adults_m 54.0 -> 52.0',
            done='adults_m         = 52.0     # UK adults 18+, millions = population'),
        Replace(
            old='house_median_gbp_m = 0.225    # PLACEHOLDER: UK median house price in calibration_year (2017), £m. VERIFY against ONS HPSSA.',
            new='house_median_gbp_m = 0.225    # ONS HPSSA England median price paid, existing dwellings, year ending Dec 2017 (England £225,000; E&W £220,000), £m. A median, not a mean. UK-wide median not available.',
            label='house_median_gbp_m comment',
            done='house_median_gbp_m = 0.225    # ONS HPSSA England median price paid'),
        InsertBefore(
            anchor='[rates.scenarios.stock_ladder]',
            new=('[rates.scenarios.' + SENS + ']\n'
                 'label = "Gain ladder, W_min = full median house price (sensitivity to the 0.5 design)"\n'
                 'wmin_house_ratio = 1.0\n'
                 'schedule = "gain_ladder"\n'
                 'dist_kw = { body_split = 5, body_split_from = 0.5 }\n\n'),
            label='new scenario ' + SENS,
            done='[rates.scenarios.' + SENS + ']'),
        Replace(
            old='  "gain_ladder", "stock_ladder", "logistic_ln_ref",',
            new='  "gain_ladder", "gain_ladder_wmin_full", "stock_ladder", "logistic_ln_ref",',
            label='run list: add ' + SENS,
            done='"gain_ladder_wmin_full", "stock_ladder", "logistic_ln_ref",'),
    ]
    ops += _scenario_ops(text)
    return {'WDT_Params.toml': ops}


SPEC = build_spec()

if __name__ == '__main__':
    sys.exit(patch_cli(SPEC, NAME, __doc__))