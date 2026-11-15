| Id | Value | Source | Meaning |
|:---|:---:|:---|:---|
| **DMG_NDOM_BASE** | 6 | p5.dmg | strategies gaining in every scenario, units/allow/off |
| **DMG_NMAT_BASE** | 0 | p5.dmg | of those, gaining by more than the BRG tolerance, units/allow/off |
| **DMG_MAXIMIN_BASE** | 0.039% | p5.dmg | highest worst-scenario gain, units/allow/off |
| **DMG_NSCEN_BASE** | 35 | p5.dmg | scenarios per rule set |
| **BRG_WORST_BASE** | 24.9% | p5.verdict_by_rule | worst best-response gain over lambda, units/allow/off (at lambda 0.0) |
| **HEC_MEANMAX_BASE** | 0.62% | p5.hec | largest mean gain from honest error, units/allow/off (sigma 0.2, lambda 0.0) |
| **HEC_STATEMIN_BASE** | -2.34% | p5.hec | largest mean fall in the state stake from honest error, units/allow/off |
| **UOS_CROSS_BASE** | 2% | p5.uos | smallest Route C share where overstating beats understating at lambda_base, units/allow/off |
| **UOS_BRGC_BASE** | 2% | p5.uos | smallest Route C share where the best gain exceeds the BRG tolerance at lambda_base, units/allow/off |
| **UOS_OVERMAX_BASE** | 17.6% | p5.uos | largest overstating gain over the share sweep at lambda_base, units/allow/off |
| **UOS_UNDERMAX_BASE** | 3.0% | p5.uos | largest understating gain over the share sweep at lambda_base, units/allow/off |
| **DMG_NDOM_CAND** | 6 | p5.dmg | strategies gaining in every scenario, units_and_value/reset/on |
| **DMG_NMAT_CAND** | 0 | p5.dmg | of those, gaining by more than the BRG tolerance, units_and_value/reset/on |
| **DMG_MAXIMIN_CAND** | 0.035% | p5.dmg | highest worst-scenario gain, units_and_value/reset/on |
| **DMG_NSCEN_CAND** | 35 | p5.dmg | scenarios per rule set |
| **BRG_WORST_CAND** | 4.4% | p5.verdict_by_rule | worst best-response gain over lambda, units_and_value/reset/on (at lambda 0.0) |
| **HEC_MEANMAX_CAND** | 0.07% | p5.hec | largest mean gain from honest error, units_and_value/reset/on (sigma 0.2, lambda 0.0) |
| **HEC_STATEMIN_CAND** | -1.99% | p5.hec | largest mean fall in the state stake from honest error, units_and_value/reset/on |
| **UOS_CROSS_CAND** | 2% | p5.uos | smallest Route C share where overstating beats understating at lambda_base, units_and_value/reset/on |
| **UOS_BRGC_CAND** | 15% | p5.uos | smallest Route C share where the best gain exceeds the BRG tolerance at lambda_base, units_and_value/reset/on |
| **UOS_OVERMAX_CAND** | 3.1% | p5.uos | largest overstating gain over the share sweep at lambda_base, units_and_value/reset/on |
| **UOS_UNDERMAX_CAND** | 1.6% | p5.uos | largest understating gain over the share sweep at lambda_base, units_and_value/reset/on |
| **LIFE_OVERMAX** | 12.4% | life.grid | largest single-life gain from overstating (alpha|g 2.0|0.059) |
| **LIFE_UNDERMAX** | 3.6% | life.grid | largest single-life gain from understating (alpha|g 0.1|0.2545) |