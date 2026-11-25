# 146r: Per-path GDP growth, evidence and design for a labelled "growth risk only" axis

Accessed 2026-11-23. Brief `project/briefs/open/146r-gdp-growth-and-top-tail-evidence.md`. Evidence and design only; no code, register, pack or manifest change. Scenario values are labelled, never a forecast; no central value.

Status: done (block 1 of brief 146r).

## 1. Summary

- Today every path has one real GDP-per-head growth, 0.0157 a year (the mean of the pack's JST `gdp_pc` growth over the 117 usable years: 1.5704%, checked to 1e-12). The kernel, revenue and burden code already take growth as a `(T, P)` array; the runner fills it with the constant (`np.full(g.shape, ctx.gdp_g)`). A per-path axis therefore needs a generator and a rule for household income, not new machinery in the kernel.
- The pack's own series support a labelled process: AR(1) deviation around the fixed mean, SD 2.68 points (full sample, the same 117 years as the market process) or 1.93 (postwar, 70 years), lag-1 0.28 (SE about 0.09), same-year correlation with the market real return 0.37 (95% interval 0.20 to 0.51). All `derived` from one country's history; none is a register row.
- Correlation is the open ruling: **A independent** (0; isolates growth from market risk; outside the sample's interval) or **B historic** (0.37). Both are listed; none is chosen.
- Scales with the path: the GDP index (M1, P6, M15a/b, the W_min index) and, if the author rules it, household income, and with it saving and pension accrual in pounds. Stays fixed: class returns of property and physical, the saving and accrual ratios, the market process itself.
- Arithmetic only (not a model run): under the full-sample AR(1) the 10th to 90th percentile of the GDP index relative to the fixed path is 0.80 to 1.25 at year 25, 0.63 to 1.58 at year 100.


## 2. What is fixed today and what scales with a path

**Fixed today.** `runner.py` sets `gdp_g = mean(gdp_growth(pack, real_series years))` = 0.0157039 and passes `np.full(g.shape, ctx.gdp_g)` into `evaluate` and `core_run`. The household arm's income growth is the same number (`inputs_used.json`, `g`). 128c made the market return per path (net financial and pension add `g - mu`, loading 1; property 0.016455 and physical I-D1j fixed) and left GDP constant on purpose (`household-arm-paths.md`).

**What a path-varying growth would change** (read from `revenue.py`, `burden.py`, `runner/arm.py`; nothing run):

| Quantity | Reads GDP growth how | With a per-path axis |
|---|---|---|
| GDP index `gdp_index` (`cumprod(1 + gdp_g)`) | denominator of M1, P6 (fund over GDP), M15a/b (% of GDP) | varies by path: these cells acquire growth risk |
| W_min (threshold) | `index='gdp_pc'`: moves with GDP per head | varies by path: the payer set moves |
| Household income per line (`income * (1 + gr)^t`) | `gr` is the constant `g` today | scales only if the arm is given the path (a rule for the author, section 5) |
| Saving and pension accrual in pounds | ratios of income | scale with income; the ratios stay fixed (scenario values) |
| Property (0.016455) and physical (I-D1j) gains | fixed scenario rates | stay fixed |
| Net financial and pension gains | the market path (128c) | unchanged; correlated with growth only under option B |
| GDP-only cells (M1b, M1d, O6, O7, OD1, OH1b2, OR1, OS1) | depend on the constant growth | acquire spread; today they are flat at every point |


## 3. Held evidence for a growth process (page or table, flag)

Rows in `research/tables/146r-gdp-process-and-top-tail/gdp_process.csv` (G-D-*). Source: the pack's `returns.csv`, columns `gdp_pc` (JST R6 `rgdpmad`, real GDP per head; `NOTICE.md`), `capital_tr` and `cpi`, years usable in `returns.real_series`. Flag `table` for the series, `derived` for every statistic below (computed by `gdp_process.py` from the pack; no published page).

| Window | Years | Mean | SD | Lag-1 | Correlation with the market real return (95% interval) |
|---|---|---|---|---|---|
| All usable years | 117 (1896 to 2019, 1940-46 absent) | 1.57 | 2.69 | 0.28 | 0.37 (0.20 to 0.51) |
| 1950 to 2019 | 70 | 1.94 | 1.93 | 0.33 | 0.40 |
| 1871 to 1938 | 43 | 1.05 | 3.58 | 0.22 | 0.34 |

Units: % a year. Lag-1 inside the contiguous runs only is 0.27 (the all-years figure pairs across the 1939/1947 seam, as the market process does). The market real return leads: its correlation with growth one year later is 0.38 and with growth one year earlier is -0.01, so a same-year correlation is a simplification. For two AR(1) series the same-year correlation equals the innovation correlation times 0.9996, so the observed value serves as the innovation correlation.

The market process in 128c uses the same 117 years (mean 4.74, SD 8.22, lag-1 0.30), so the two processes share a sample and a seam.


## 4. Proposed deviation process and parameters

A labelled axis "growth risk only", off by default, same machinery as the market paths: the per-path growth is `gdp_g[t, p] = 0.0157039 + d[t, p]`, with `d` a zero-mean AR(1): `d_t = phi d_{t-1} + u_t`, `u` normal, marginal SD `sd`. Zero deviation reproduces the fixed arm byte for byte (the 128c rule).

| Parameter | Value | Class | Challenge |
|---|---|---|---|
| mean | 1.5704% (the pack constant) | `derived` | not a deviation; fixes today's behaviour at zero |
| `sd`, option "full sample" | 2.68 points | `derived` | includes the wars and the 1930s; 117 years, one country |
| `sd`, option "postwar" | 1.93 points | `derived` | 70 years; the author rules between the two |
| `phi` | 0.28 | `derived` | SE about 0.09; postwar 0.33; seam pair included |
| correlation with the market return | option A 0, option B 0.37 | A `scenario`, B `derived` | section 5 |

Arithmetic illustration (`gdp_illustration.csv`; the formula for the spread of a sum of AR(1) deviations, not a model run): the 10th and 90th percentile of the GDP index relative to the fixed path.

| Year | full sample | postwar |
|---|---|---|
| 10 | 0.87 to 1.15 | 0.90 to 1.11 |
| 25 | 0.80 to 1.25 | 0.85 to 1.18 |
| 50 | 0.73 to 1.38 | 0.79 to 1.26 |
| 100 | 0.63 to 1.58 | 0.72 to 1.39 |

Challenge: the illustration treats growth deviations as stationary with a fixed mean, so the level spreads like a random walk; the JST history is one realisation and does not test that. The spread at year 100 is a property of the assumed process, not an estimate of UK output risk.


## 5. Correlation options, unset, open rulings

**Options for the correlation with the market return** (no choice made):
- **A, independent (0).** Isolates growth risk from market risk, so the added spread in the GDP-denominated cells is due to growth only. Contradicts the sample (0 lies outside the 95% interval 0.20 to 0.51).
- **B, historic (0.37).** Reproduces the sample association: good market years tend to come with good growth, so fund-to-GDP ratios are partly self-hedged. Own sample uncertainty is wide; one country.
- Not offered: a lead or lag structure (market leads growth by a year, 0.38) because it is a timing refinement the evidence is too thin to size; listed as a possible third option.

**Unset** (rows G-U01 to G-U05): a register row for the process; growth after 2019 (the pack ends 2019); growth by line or band; any link between growth and the property or physical returns; the distribution shape.

**Open rulings for the author.**
1. Correlation: A or B (the label of the axis changes: "growth risk only" with A, "growth and market risk, correlated" with B).
2. Marginal SD: full sample 2.68 or postwar 1.93 points.
3. Whether household income follows the path (so saving and accrual in pounds scale) or stays on the constant `g` (only the GDP-denominated cells and W_min move). The second isolates the denominator; the first is the consistent reading.
4. Whether to add register rows for the process, or keep the parameters as labelled scenario constants in the arm dict, as 128c did for `mu`.


## 6. Reproduction

`python -I research/scripts/gdp_process.py` from the repo root. It reads the pack read-only, checks that the mean growth equals the model constant and that 117 usable years exist, writes `gdp_process.csv` (17 rows) and `gdp_illustration.csv` (8 rows) and prints one `ok:` line; it exits 1 on a failed check. Check: `python -I project/tools/check_agent_docs.py`.

