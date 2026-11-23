# Why the household arm differs from the legacy arm (brief 136c)

Status: diagnosis. No model file, register row, parameter or rule was changed. Every number is a **scenario value at a labelled grid point on a labelled market path, not a forecast and not a central case**; no figure here is a headline. The legacy arm (`I-D14c`, 3.5%) is a comparator only; the note says what each arm assumes and does not say which is right. Files: `household-vs-legacy/flows.py` and `flows.csv` (per line), `decomp.py` and `decomp.csv` (outputs as base x rate), tests `tests/model_v3/test_household_vs_legacy.py`.

## Setup, and the answer to the open question

- **Common ground** ("common"): both arms through `core_run` on one constant market path, the register's mean market return 4.74% a year real (sd 8.22 and phi 0.3 unused: one path), GDP growth 0.0157, schedule S (tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5); the household arm at `median_mid`, `max_mid` and `median_low`. The household arm does not read the path except for the fund's safe stand-in, so its numbers on this path are the 124c numbers: the decomposition reproduces every 124c household value to 3e-15 (relative).
- **The legacy arm on its own paths** ("stoch"): 1,000 paths, chunks of 100, seed 1 (the 124c paths); the decomposition reproduces the 124c legacy values to 2e-16. Terms are means over paths, so a product of two means differs from the mean of the product; `ratio_interaction` in `decomp.csv` reports that error (it is 1 on the common ground).
- **The open question: P6 is the same quantity in both arms.** `P6 = 100 x S / GDP` at years 10, 25, 50 and 100 (S the fund's assets, GDP the common GDP index); units, years and GDP are the same. The gap is real, not a unit.
- Interpretation I took for "the household arm's mean `mu`": the register mean market return (4.74%), which is also the mean of the 124c paths; the household arm's class returns (regime returns `low` 3.44, `mid` 5.20, `high` 6.96% and yields from the inputs file; net financial = return minus yield) stay its own.

## Where the two arms' wealth sits (`flows.csv`)

Year 1 starts equal (same base wealth). The legacy arm grows every class at the market return and consumes 3.5%: wealth grows 1.07% a year before tax, in every line (`c_eq` 3.50%). The household arm's implied consumption-equivalent `c_eq = 1 - (W_end/W_start)/(1+g)` differs by line:

| Line (year 30, after tax) | Legacy | Household `median_mid` | `max_mid` | `median_low` |
|---|---:|---:|---:|---:|
| D1 | 3.50% | 0.16% | 0.04% | 1.06% |
| D5 | 3.50% | 2.35% | 1.39% | 2.97% |
| D9 | 3.57% | 2.92% | 2.19% | 3.53% |
| D10a | 3.59% | 3.06% | 2.42% | 3.71% |
| RL1 | 3.96% | 3.81% | 3.81% | 3.98% |

(`flows.csv` has all 14 lines and years 1, 10, 30, 100.) Lines D1 to D9 deplete less than 3.5% because saving (1.7% of wealth for D5 at `median_mid`, 5.3% at `max_mid`) and the holding gain (1.1%) together exceed the market-return-less-3.5% the legacy arm leaves; the top lines save nothing (RL: S = 0) and earn a holding gain of 1.3 to 1.5%, so they deplete about as the legacy arm does. The household account closes in every line and year (residual 1e-16).
Weighted mean wealth per adult (millions of pounds) at year 100: legacy 0.47; household 0.73 (`median_low`), 1.25 (`median_mid`), 2.44 (`max_mid`). D1 to D9 hold 72% of it under the legacy arm and 79 to 85% under the household arm: the gap in the wealth base is made in the lines with saving, not at the top.

## M1a: gross receipts (% of GDP)

M1a = 100 x Base x Rate (window sums, exact). Base is the aggregate taxed wealth over GDP, Rate the WDT cash over it. For the household arm the model's own base (`w0`, the family value) leaves out the pension; the tax is assessed on the total, so the table uses the total wealth (`base_total`).

| Horizon | Legacy const | Legacy stoch | Household `median_mid` / `max_mid` / `median_low` |
|---|---:|---:|---:|
| short | 3.11 | 3.66 | 3.19 / 4.48 / 2.43 |
| long | 0.68 | 1.18 | 1.73 / 6.66 / 0.88 |

Ranked reasons (log shares of the gap household / legacy stoch, `median_mid`):
1. **Short: the market path.** Household / legacy const 1.03 (base 1.12 x rate 0.92); legacy const / stoch 0.85. The short gap (0.87) is made by the volatility of the legacy arm (118% of it); the arms themselves agree on the common ground.
2. **Long: lower depletion makes the base bigger.** Household / legacy const 2.54 = base 2.17 x rate 1.17 (the base explains 83% of the log gap). `max_mid`: 9.78 = 4.04 x 2.42; `median_low`: 1.29 = 1.37 x 0.95. The base is the saving lines' accumulated wealth (section above).
3. **Volatility of the legacy arm raises its long receipts** by 1.73 (the mean of the per-path base is 1.01 times and of the rate 1.11 times the constant-path values; the rest, 1.54, is the interaction of the two across paths: the paths with the larger base pay more). On the common ground the household long value is 2.5 times the legacy's; against the legacy arm's own paths 1.5.
4. Death settlement timing and the schedule are the same in both arms (same kernel): not a reason.
Unexplained: the interaction term (up to the stated factor) and the split of the long base between saving and holding gain by line (not separated here).

## M2 (in life) and M2d (with the settlement at death)

M2 = R_pay x K: R_pay = tax over the payers' start-of-year family value `w0` (net > 0, w0 > 0), K = M2 / R_pay the tax-weighting. Long, overall, % a year:

| | Legacy const | Legacy stoch | Household `median_mid` / `max_mid` / `median_low` |
|---|---:|---:|---:|
| M2 | 0.10 | 1.27 | 0.34 / 0.38 / 0.15 |
| R_pay (on `w0`) | 0.069 | 0.540 | 0.338 / 0.359 / 0.135 |
| K | 1.44 | 2.39 | 1.02 / 1.05 / 1.13 |
| payers' share of wealth-years | 0.66 | 0.30 | 0.93 / 1.00 / 0.83 |
| R_pay on **total** wealth | (same, `w0` is total) | (same) | 0.136 / 0.239 / 0.086 |
| M2 like for like (R_pay total x K, approx.) | 0.10 | 1.27 | 0.14 / 0.25 / 0.10 |

Short, overall: legacy const 0.29, stoch 2.44; household 0.40 / 0.47 / 0.22 (like for like 0.26 / 0.33 / 0.15). D10 long: legacy 0.13 and 1.50; household 0.38 / 0.46 / 0.20 (like for like 0.18 / 0.29 / 0.14).

Ranked reasons for the M2 gap, household `median_mid` / legacy stoch, long, overall (log gap -1.30):
1. **The legacy arm's M2 is made of its market volatility: -2.55 (196%).** On a constant path the legacy M2 is 0.10, on its own paths 1.27 (R_pay x7.8, K x1.66). M2 averages only the years a line pays (net > 0): 30% of the legacy wealth-years pay, the rest are refund or zero years (loss years of an AR(1) return with sd 8.22), and the payers' years are the up-years with the large assessed gains. The household arm has no market volatility (fixed class rates): 93 to 100% of its wealth-years pay a small steady tax.
2. **The household denominator is not total wealth: +0.91 (-70%).** `w0` is the kernel's family value; under the household arm it is total wealth in year 1 and the non-pension wealth from year 2 (the pension, 37% of D5's total, stays in the tax base but not in `w0`). Dividing by total wealth cuts the household M2 to 0.14 (`median_mid`), 0.25 (`max_mid`), 0.10 (`median_low`): factors 2.5, 1.5 and 1.6. See Defects 1.
3. **What is left of the arm difference on the common ground: +0.34 (-26%).** Like for like the household M2 is 1.4 times the legacy const (0.14 against 0.10); its tax is on a larger base (section M1a) at a similar rate.
So the 124c "an order below" is made of (1) and the legacy arm's own volatility; the household arm is not low for a reason of its own. On the common ground and like for like the two are within a factor 1.4 to 2.5 (0.10 legacy; 0.10 to 0.25 household).

M2d (long, overall): legacy const 14.8, stoch 13.8; household 10.2 / 8.7 / 12.2. Here R_pay x K is dominated by K (9.7 to 25 against 1 to 1.4 in life): the settlement at death is one large flow in the lines that die in a phase, so the weighted rate is the rate of those flows. Household / legacy stoch 0.74 / 0.63 / 0.88; volatility moves the legacy M2d little (const / stoch 1.07). K is 12.4 (`median_mid`) against 39.5 on the legacy common ground and 11.2 on its own paths, R_pay 0.82 against 0.38 and 1.25. Not resolved: how much of the M2d gap is the size of the settlement and how much the denominator (Defect 1 applies to M2d too: R_pay on total wealth is 0.33 / 0.60 / 0.31 for the household arm); the per-line death flows are in `flows.csv` (`death_share`), the split is not made.

## M1 net, long, and M1c

M1 = M1a + M1b + M1c - M1d (long, % of GDP): legacy const -1.23, stoch -3.26; household -0.30 / +0.49 / -1.43.
Gap household `median_mid` against legacy stoch (+2.96): M1a +0.55 (19%), M1b 0, M1c -0.15 (-5%), **M1d +2.55 (86%)**: M1d is 4.74 in the household arm and on the legacy common ground, 7.29 on the legacy arm's own paths (household `max_mid`: 8.11). M1d is the retired taxes' relief, drawn from the fund's relief R; the legacy stoch fund (611% of GDP) funds more of it. So the M1 net gap is mostly the size of the legacy fund, i.e. the P6 gap below.

M1c = return on the fund minus its growth, % of GDP, long:

| | Legacy const | Legacy stoch | Household `median_mid` / `max_mid` / `median_low` |
|---|---:|---:|---:|
| M1c | +0.01 | +0.04 | -0.11 / -0.88 / -0.39 |
| return on the fund | 18.76 | 30.36 | 0.37 / 0.57 / -0.11 |
| growth of the fund | 18.75 | 30.32 | 0.48 / 1.45 / 0.28 |
| fund level | 396 | 611 | 33 / 55 / 22 |
| return rate | 4.74% | 4.67% | 1.11 / 1.04 / -0.50% |

The legacy fund earns the market mean on a fund of 4 to 6 times GDP, so its return almost equals its growth (M1c about 0). The household fund earns the safe stand-in (the net financial class return, -0.5 to 1.1%) on a fund of 22 to 55% of GDP and grows by more than it earns, so M1c is negative (-0.11 to -0.88). The sign differs because of the fund's return rate and size, not because of a different formula. Short horizon: legacy -0.44 (const) / -0.31, household -0.04 / -0.10 / -0.39.

## P6: the public wealth path (fund assets, % of GDP)

S = cumulative inflow (WDT cash + levy) + return - payout, each as % of that year's GDP (`decomp.csv`, P6 rows):

| Year 100 | S | Inflow | Return | Payout |
|---|---:|---:|---:|---:|
| Legacy const | 729 | 205 | 719 | 195 |
| Legacy stoch | 1,167 | 232 | 1,156 | 221 |
| Household `median_mid` | 35 | 248 | 19 | 233 |
| `max_mid` | 78 | 459 | 28 | 409 |
| `median_low` | 22 | 205 | -5 | 178 |

Ranked reasons (household `median_mid` against legacy stoch, gap -1,132 points of GDP at year 100):
1. **The fund's return: -1,137 (100.4%).** The legacy fund earns the market mean 4.74% (stoch: 4.67%) on a fund that compounds to 6 to 12 times GDP; the household fund earns the safe stand-in, 1.11% (`median_mid`), 1.04%, -0.50% (`median_low`). Compounding 4.74% for 100 years against about 1% explains the order of magnitude. Year 10 differs little (legacy const 50, stoch 64, household 38 to 52) and the gap opens with time (year 50: 159 and 230 against 28 to 59).
2. Inflow +16 (-1.4%), payout -12 (+1.1%): alike in the two arms (inflow 205 to 459 against 205 to 232; payout 178 to 409 against 195 to 221).
3. Volatility: legacy stoch 1,167 against const 729 (x1.6) because the model draws the arithmetic mean return with spread, so the mean of the compounded fund exceeds the compounding of the mean (Jensen); this is a property of the legacy comparator.
The household P6 is flat or falling after year 25 (`median_mid` 44, 39, 35; `median_low` 35, 28, 22): the fund pays out about what it receives and earns about nothing.

## What each arm assumes (the difference, in one list)

- **Wealth growth.** Legacy: every class earns the market return, 3.5% consumed, the same in every line and path. Household: saving S (income x ratio, B.6g scaled) and class-specific holding gains (scenario rates), the pension accrues and is never drawn in life.
- **Market path.** Legacy: the tax and the fund see the AR(1) market return (volatility matters for M1a, M2, M1c, P6). Household: fixed scenario class rates; the path reaches only GDP growth.
- **Tax base.** Same kernel: wealth delta on the total (pension included in the household arm).
- **Fund.** Legacy: the market return. Household: the safe stand-in (the net financial class return), labelled.
- **Denominator of M2.** Legacy: total wealth. Household: non-pension family value from year 2 (Defect 1).

## Defects list

1. **The M2 and M2d denominator is not like for like.** `line_flows` stores `w0 = book.family_true()` before each year's step. Under the household arm the kernel's family value is the non-pension wealth after the hook's first year (the pension lives in `book.pen`), so `w0` is total in year 1 and non-pension from year 2. Minimal case: line D5, `median_mid`, phase 0: `w0` = 0.1252 in year 1, 0.0808 in year 2, 0.0821 in year 3; total wealth (pension included) at the start of year 2 = 0.1286. Effect: the household M2 (in life and with settlement) divides by 40 to 67% of the wealth the tax is assessed on (M2 long overall 0.34 against 0.14 like for like at `median_mid`; 0.38 against 0.25; 0.15 against 0.10), while the legacy M2 divides by total wealth. Any other reader of `fl['w0']` has the same break (not checked). Not fixed (brief); the author decides whether M2 should divide by total wealth.
2. **No other inconsistency was found:** units of P6 and M1 are the same in both arms; the household decomposition reproduces the 124c values; the account closes; the legacy P6 of 1,170% of GDP is the arithmetic-mean market return compounding on an uncapped fund (a property of the comparator, recorded in 124c "Odd", item 4), not a computation error.

## Unexplained

The M1a long and M2d gaps are only partly resolved (the base split by line, the death-flow share); the interaction between volatility and the arm difference is reported (`ratio_interaction`) but not separated; saving (income and the B.6g scaling) enters through S and was not varied here, so its share of the base gap is not isolated from the holding gain. The stoch legacy terms are means of per-path terms.

## Next

- The author rules on Defect 1 (M2 denominator).
- If wanted: a run of the household arm with per-path market returns (128c) against the legacy arm on the same paths, which would answer the volatility reasons above directly; the same for the saving split of the base.
