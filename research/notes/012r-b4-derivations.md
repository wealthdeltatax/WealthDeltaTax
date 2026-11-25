# 012r stage B4: derivations

Method behind the M2 check and the computed rows I-D7c in `model-specs/inputs.md`. Run with `python3 -I`, reading the tables printed in the repo papers (nothing from outside the repo). Accessed 2026-11-17.

## 1. Tables read
- Burden by tier and bracket, N = 30: `papers/legacy/8_Rates_and_Revenue.md`, matrix under "Annual wealth burden" (same as appendix B.3.3). 4 growth tiers (Poor, Ok, Good, Great) by 10 brackets (50th to 99.99th+ percentile).
- Starting wealth V_0 per bracket and terminal wealth V_N per tier and bracket: appendix B.3.1.
- Taxpayers per cell: appendix B.3.6 (34.6m in total; tier weights 10, 30, 40, 20%).

## 2. Replication of the paper's aggregates
Per cell, burden B = average annual net tax over terminal settlement wealth, so average annual tax T = B x TW. TW_settled is not printed, so V_N stands in for it.
- Population-weighted mean of B, weights taxpayers: 0.243% (paper 0.24%).
- Wealth-weighted: sum of B x V_N x n over sum of V_N x n: 0.361% (paper 0.35%; the 0.011 point gap is the TW_settled proxy). This is the paper's formula, appendix B.3.3.

## 3. M2 as defined in `metrics.md`
M2 = sum_i T_i (T_i / W_i) / sum_i T_i, with T_i = B x V_N per taxpayer, weights the cell populations.
| W_i | M2 |
|---|---|
| terminal wealth V_N | 0.392% |
| geometric mean of V_0 and V_N (crude path average) | 1.239% |
| starting wealth V_0 | 4.081% |

The path average is a proxy: it assumes wealth grows smoothly and ignores tier-specific returns by year. A proper figure needs the model's yearly wealth per cohort. The check did not run the model.

## 4. Caveats
- The tables are the 2000 Balanced reference scenario only; a different return series changes every figure.
- T is derived as B x V_N, not read: the appendix's per-year net tax tables (B.3.2, B.3.5) are on a different window and do not reproduce B x V_N cell by cell (for example the 99th percentile Great tier: B.3.5 gives about 0.39% of terminal wealth against 0.46% in the burden table). I did not resolve why; it needs the code.
- No paper text was edited.

## 5. I-D7c
Levy yield over corporation tax retired: 2.77/3.37 = 0.822, 2.82/3.37 = 0.837, 2.88/3.37 = 0.855.
