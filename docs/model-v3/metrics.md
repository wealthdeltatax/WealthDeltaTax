# Model v3: metric register (brief 011g, stage A draft)

One definition per metric. Code and papers cite the ID. Status: **draft for the author's review**; items marked OPEN are not yet decided. Decisions behind this file: `docs/model-audit/synthesis.md` section 3.

Conventions. Time t = years since launch. Payer = adult whose net wealth is at or above W_min (half the median house price, per adult). Non-payer = every other adult. A "range" is the sampled P10, mean and P90 of the metric over the input draws (R5). All money is real, in the stated base year; shares of GDP use GDP in year t.

## Headline metrics
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M1 | Government revenue, net fiscal effect | M1 = M1a + M1b + M1c - M1d, where M1a = individual WDT paid minus refunds paid; M1b = corporate levy; M1c = fund income minus fund retention (v2 identity, `rates_core.py` line 109); M1d = receipts of the taxes already retired in year t (M1e). The lines M1a to M1d are reported beside M1; none is merged into another | GDP_t | % of GDP and real £bn | OPEN: the reporting year or years (v2 shows 9.9% of GDP at the fill year and 5.4% over 100 years for one schedule) |
| M1e | Retired-tax receipts | Receipts the state forgoes for each retired tax k: corporation tax, council tax, business rates, capital gains tax, inheritance tax, stamp duties (property), stamp taxes on shares. Retired in steps as relief arrives (author, 2026-11-16); the order and the trigger are OPEN | GDP_t | % of GDP | as M1 |
| M2 | Taxpayer burden, share of wealth | Net WDT paid by payers in year t divided by the net wealth of payers at the start of year t (ratio of sums, not a mean of ratios). Reported overall and by wealth band. OPEN: the RATES paper used a revenue-weighted version | payer wealth | % per year | steady state and the reporting year |
| M3 | Taxpayer burden, gain-weighted lifetime rate | Present value of net WDT paid over a payer's life divided by the present value of the gains the payer realises or accrues over that life. v2 candidates: `er_stock_payers`, `er_gain_payers` in `rates_core.py`. OPEN: discount rate, life length G | PV of gains | % | one life, G years |
| M4a | Non-payer savings, share of current tax bill | For the non-payers: (tax they pay today minus tax they pay after the change) divided by the tax they pay today. Includes the retired taxes they pay (council tax, business rates passed on, stamp duty, corporation tax incidence) and any relief beyond the retired taxes. OPEN: incidence assumptions and who is counted (median adult, deciles, all non-payers) | current tax bill | % | as M1 |
| M4b | Non-payer savings, share of income | The same saving divided by the non-payer's income | income | % | as M1 |

## Revenue lines (parts of M1)
| ID | Name | Definition | Unit |
|---|---|---|---|
| M1a | Individual WDT, net | WDT paid by payers in year t minus refunds paid in loss years (refund capped by the tax paid to date, as the papers state) | % of GDP |
| M1b | Corporate levy | The CORP delta levy collected in year t (positive years only; no levy and no refund in loss years). Own line, never merged into M1a | % of GDP |
| M1c | Fund income net of retention | Fund investment income minus fund growth retained in the reserves (v2: 5.29 and 5.88 for one schedule, so about -0.6) | % of GDP |

## Comparison metrics (for the whitepaper's argument)
| ID | Name | Definition | Notes |
|---|---|---|---|
| M5 | Burden against suggested wealth taxes | M2 recomputed with each suggested wealth tax on the same people, and the difference | The set of suggested taxes is OPEN (research brief 012r). v2 has a stock ladder and a 2% floor above £1bn as checks |
| M6 | Burden against today's income tax, CGT and IHT | The payers' CGT and IHT liabilities today (both are retired) divided by the same payers' wealth, set beside M2; income tax stays | Needs HMRC data (012r) |

## Supporting metric
| ID | Name | Definition | Denominator | Unit |
|---|---|---|---|---|
| M7 | C.1, the tolerant-zone measure | (Net(alpha) - Net(1)) / TW(1), where Net is net tax over the horizon at declaration ratio alpha and TW(1) is the tax wealth change at honest declaration (alpha = 1). The tolerant zone is the alpha range where |C.1| < 2 percentage points | TW(1) (author, 2026-11-16; v1 error B1) | percentage points |

## Path metrics (needed to produce M1 and M4)
| ID | Name | Definition |
|---|---|---|
| P1 | Reserve fill years | Years until the short and the long reserve reach their targets (3 times the trailing mean annual refund each; v2 medians 3 and 7 on UK windows) |
| P2 | Relief available | R_t = M1a + M1b + M1c; retires taxes in the stated order |
| P3 | Cumulative shortfall | Sum over years of any year in which retired receipts exceed revenue; must be zero under staged retirement, reported to prove it |

## OPEN items to close before stage A passes
1. The reporting year or years for M1 to M4.
2. The order and the trigger for retiring the six taxes (relief covers the next tax's receipts?).
3. M2 weighting (ratio of sums, or revenue-weighted) and the M3 discount rate.
4. Who "non-payers" are for M4 (all, the median adult, income deciles) and the incidence rules.
5. The set of suggested wealth taxes for M5.
