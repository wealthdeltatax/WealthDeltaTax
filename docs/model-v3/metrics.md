# Model v3: metric register (brief 011g, stage A)

One definition per metric. Code and papers cite the ID. Status: **stage A passed, author confirmed all four items on 2026-11-16**. Two open items remain, both checks and neither blocks stage B: the M2 formula against the RATES paper's 0.35% (writing or research lane), and the Green Book schedule text for M3 (012r). Decisions behind this file: `docs/model-audit/synthesis.md` section 3.

Horizons (author, 2026-11-16: report short and long term effects). Every headline is reported for three windows, so the time profile is visible:
- **Transition:** launch to the long-reserve fill (v2 median 7 years on UK windows), while taxes are retired in steps.
- **Short term:** the 10 years after the long-reserve fill (v2's own horizon, so v2 and v3 can be compared). Confirmed.
- **Long term:** the mean of years 51 to 100 and the year-100 value. Confirmed.
The author reads the v2 time profile (for one schedule, 9.9% of GDP at the fill year against 5.4% over 100 years) as a sign that WDT may not be sustainable as a revenue source. v3 therefore reports the sustainability test P4 as a result, whichever way it comes out.

Conventions. Time t = years since launch. Payer = adult whose net wealth is at or above W_min (half the median house price, per adult). Non-payer = every other adult. A "range" is the sampled P10, mean and P90 of the metric over the input draws (R5). All money is real, in the stated base year; shares of GDP use GDP in year t.

## Headline metrics
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M1 | Government revenue, net fiscal effect | M1 = M1a + M1b + M1c - M1d, where M1a = individual WDT paid minus refunds paid; M1b = corporate levy; M1c = fund income minus fund retention (v2 identity, `rates_core.py` line 109); M1d = the sum, over the taxes retired by year t, of their receipts M1e. The lines M1a to M1d are reported beside M1; none is merged into another | GDP_t | % of GDP and real £bn | transition, short and long (above) |
| M1e | Retired-tax receipts | Receipts the state forgoes for each retired tax k. Six taxes are retired (author's decision): corporation tax, council tax, business rates, capital gains tax, inheritance tax, stamp duties. Stamp duties carry two receipt lines (property; shares), so M1e has seven lines and P5 has six retirement years. Retired in steps as relief arrives. **Order (confirmed): ascending by receipts**, smallest first, a policy input that a Phase One governing council may change. **Trigger (stated default, follows from P3):** a tax is retired in the first year after the long-reserve fill in which relief R_t, net of the receipts of taxes already retired, covers that tax's receipts. Each headline is reported for the three windows above | GDP_t | % of GDP | as M1 |
| M2 | Taxpayer burden, share of wealth | Revenue-weighted mean of each payer's burden (author, 2026-11-16): M2 = sum_i T_i (T_i / W_i) / sum_i T_i, where T_i is payer i's net WDT in year t and W_i the payer's net wealth at the start of the year. Reported overall and by wealth band. To check against the RATES paper's 0.35% figure before it is used | tax paid | % per year | transition, short and long |
| M3 | Taxpayer burden, gain-weighted lifetime rate | Present value of net WDT paid over a payer's life divided by the present value of the gains the payer realises or accrues over that life. v2 candidates: `er_stock_payers`, `er_gain_payers` in `rates_core.py`. Discount rate: the HM Treasury Green Book schedule, 3.0% for years 1 to 30, 2.5% for years 31 to 75, 2.25% for years 76 to 125 (the October 2026 revision; read from HM Treasury's response to the 2026 discount-rate review, to be confirmed against the Green Book text by research); a sensitivity runs at the previous 3.5% and 3.0% schedule. v2 used 3.5% and v1 5%. Life length G = 30 years (confirmed; the v2 generation length) | PV of gains | % | one life, G years |
| M4a | Non-payer savings, share of current tax bill | For the non-payers: (tax they pay today minus tax they pay after the change) divided by the tax they pay today. Includes the retired taxes they pay (council tax, business rates passed on, stamp duty, corporation tax incidence) and any relief beyond the retired taxes. Reported by income decile of the non-payers (author, 2026-11-16), plus an overall figure. The incidence of each retired tax by decile is an input to source (012r) | current tax bill | % | transition, short and long |
| M4b | Non-payer savings, share of income | The same saving divided by the non-payer's income, by income decile | income | % | transition, short and long |

## Revenue lines (parts of M1)
| ID | Name | Definition | Unit |
|---|---|---|---|
| M1a | Individual WDT, net | WDT paid by payers in year t minus refunds paid in loss years (refund capped by the tax paid to date, as the papers state) | % of GDP |
| M1b | Corporate levy | The CORP delta levy collected in year t (positive years only; no levy and no refund in loss years). Own line, never merged into M1a | % of GDP |
| M1c | Fund income net of retention | Fund investment income minus fund growth retained in the reserves (v2: 5.29 and 5.88 for one schedule, so about -0.6) | % of GDP |

## Comparison metrics (for the whitepaper's argument)
| ID | Name | Definition | Notes |
|---|---|---|---|
| M5 | Burden against suggested wealth taxes | M2 recomputed with each suggested wealth tax on the same people, and the difference | Two sets (author, 2026-11-16): the Zucman global minimum tax on billionaires, a 2% floor on wealth above about £1bn (v2 already has this as a check, `zucman_floor`), and the UK wealth tax proposals of about 2%; research (012r) finds and cites the UK proposals and their rates |
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
| P4 | Sustainability | Two numbers per draw: the long-term M1 divided by the short-term M1, and the first year after the fill in which M1 is below zero (never, if it stays non-negative). A ratio well below 1, or a year below zero, means WDT does not hold up as a revenue source at that schedule |
| P5 | Retirement schedule | The year in which each of the six taxes is retired under the stated order and trigger (M1e) |

## Closed on 2026-11-16 (author)
Reporting windows: short and long term both (see Horizons). Retirement order: a policy input, probably a Phase One governing-council decision. M2: revenue-weighted. Discount rate: as defensible as possible (Green Book schedule). Non-payers: by income decile. Comparisons: Zucman global minimum and UK proposals of about 2%.

## Confirmed on 2026-11-16 (author, "confirm all")
1. Window cut points: transition to the long-reserve fill; short term the 10 years after it; long term the mean of years 51 to 100 and year 100.
2. Default retirement order: ascending by receipts.
3. M2 as revenue-weighted, with the check against the RATES paper's 0.35% kept as an open check (writing or research lane).
4. Life length G = 30 years for M3.
The retirement trigger was not among the four; it is stated above as the rule P3 implies. Change it here if the author prefers another.
