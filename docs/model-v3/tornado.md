# Model v3: tier 1 tornado on the revenue identity (brief 027r)

Status: research result for stage C design; no value is chosen and nothing in the register is edited. Date 2026-11-17. Script and data: `docs/model-v3/tornado/` (`tornado.py` reads `inputs.md`; `check.py` is the second method). Run both with `python3 -I`.

**Note, 2026-11-19 (guru):** the corporation tax rows I-D6c and I-D6j changed (central 24.5 to 25.2 and 30.7 to 29.5, workers' share 51%, brief 059r) after this tornado ran. No rerun: the v3 model produces its own tornado (brief 055c), which supersedes this one; the D6 figures below are the old ones.

**Superseded in part, 2026-11-18 (brief 041r):** the I-D1a row (geometric mean, 2.18 to 7.47) and every statement that rests on it (section 1 items 1 and 2, the I-D1a rows of the M1 and M2 tables, section 9 last bullet, break-even g in section 8) are replaced by section 10 below. The ranking of the other inputs stands. The old tables are kept unchanged.

## 1. What it says
1. **Return history dominates.** On M1 the mean real return (I-D1a, 2.18 to 7.47% a year) swings the result by 8.8 points of GDP; the next input, the wealth-to-GDP ratio (I-D4a), by 1.9. Behavioural response (I-D5a) 0.8, the payer wealth share (I-D4c) 0.5. Everything else is under 0.5.
2. **The sign of M1 is not safe.** At central inputs M1 is **+1.45% of GDP** (full retirement of the six taxes, steady state, section 3). It reaches zero at g = 3.55% a year, against a register central of 4.42% and a low of 2.18%. At the low g, M1 is -2.27.
3. **M1d is 8.11, not 8.27.** The 8.27% used in `synthesis.md` section 10 adds stamp duties (0.66) and stamp taxes on shares (0.16) as separate lines. In the IFS sheet 0.66 is the whole of stamp duties and already contains the shares line (property 0.50 plus shares 0.16). The sum of the seven lines is 8.11. This tornado uses 8.11; `metrics.md` M1e, `synthesis.md` and the 8.27 quoted in `drivers.md` need the guru's attention (not edited here).
4. **The identity needs a rate that the register does not hold.** The wealth-weighted effective rate ε is a lever (D2), not a register row. Backed out against v2's 7.34%, it is **30.0%** on register central inputs and 24.5% on inputs like v2's (section 4). v2's own realised ε is not recorded anywhere in the repo.
5. **Tier 2 stays at one range.** Every tier 2 input moves M1 by less than 0.5 points of GDP (largest 0.15), or does not act on steady-state M1 at all (section 6).
6. **Reachability.** M1 fully; M2 and M4a through proxies (stated); M3 not reachable by any register input except ε.

## 2. Method
- Identity (`drivers.md` section 1): M1 = M1a + M1b + M1c - M1d, with M1a = ε · g · ω, steady state after the six taxes are retired. One input at a time over its register low and high, all others at central.
- ω = I-D4a · (I-D4c + I-D4e) + capitalisation term, all times (1 - I-D5a). The capitalisation term is I-D10b · 2.2 · I-D4c, where 2.2 = £6.6tn dwellings and land over about £3.0tn GDP (the figures in the I-D10b row text).
- M1b = I-D7a (2.82). M1d = I-D7b (3.37) + I-T3n council tax (1.75) + I-T3m business rates (1.29) + I-T3h CGT (0.77) + I-T3i IHT (0.27) + I-T3k stamp duties on property (0.50) + I-T3l stamp taxes on shares (0.16) = 8.11. The CGT line follows the IFS sheet; the M1e source rule gives HMRC 24.2bn as primary (about 0.81 on the GDP implied by I-D7d), a change of +0.04 in M1d, below any swing here.
- M1c = -0.6 (assumption A2; v2 only, no register row, one value, so no swing).
- "Result at low" and "result at high" are M1 when the input takes its register low or high value. Swing = absolute difference. Rank by swing. Units: % of GDP for M1; % of payer wealth for M2; % of tax bill for M4a.

### Assumptions (labelled; none is a register value)
| ID | Assumption | Why |
|---|---|---|
| A1 | ε = 29.97%, the value that reproduces 7.34% at register central inputs | ε is a lever (D2); needed to put M1a on the identity. Holding ε here makes M1a = 7.34 at the centre by construction |
| A2 | M1c = -0.6 | `synthesis.md` section 10 point 6 (v2) |
| A3 | Refunds are netted inside g (M1a = ε g ω) | Exact only if the refund cap never binds; section 7 |
| A4 | I-D5a applies to the base as a fraction removed; I-D5b is a part of I-D5a, so its row varies the total by the change in its own value | I-D5a measured at a 1% annual stock tax; transfer to WDT unproven |
| A5 | I-D5c (leavers) applied to the whole payer base (upper bound); I-D5d (understated values) weighted by 4.4%, business assets of about 10% of D10 wealth times D10's 44% share of payer wealth | The row units are shares of a subgroup; the register has no group sizes |
| A6 | Non-payers for M4a are the bottom five income deciles; their share of all tax is 25.1% from the I-H1 quintile averages (5 equal quintiles, half of the third); all taxes = HMRC receipts (I-T3o 31.61) + council tax + business rates, % of GDP | Register has no non-payer decile split (028r will) |
| A7 | M2 is the wealth-weighted mean burden ε · g · (1 - avoided share) | M2 proper is revenue-weighted and needs the distribution |

## 3. Central values
| Term | Value | Row ids |
|---|---|---|
| ω before response | 5.51 (5.94 · 0.927); with tail add-on 5.80 (+5.94 · 0.05) | I-D4a, I-D4c, I-D4e |
| Capitalisation term | 0.49 (0.242 · 2.2 · 0.927) | I-D10b |
| ω after response of 12% | (5.80 + 0.49) · 0.88 = 5.54 | I-D5a |
| g | 4.42% | I-D1a |
| ε · g · ω | 7.34 by construction; g · ω = 24.49% of GDP | A1 |
| M1a / M1b / M1c / M1d | 7.34 / 2.82 / -0.60 / 8.11 | as above |
| **M1** | **1.45** | |
| M2 proxy | 1.24% of payer wealth a year | A7 |
| M4a | 29.7% of the non-payers' tax bill (savings 2.59% of GDP over 8.70%) | A6 |

## 4. Back-out of ε · g · ω against v2's 7.34%
Source: `synthesis.md` section 10, `logistic_ln_ref`, post-fill years, WDT line (the levy is a separate 2.77).

| | Register central | Inputs like v2's |
|---|---|---|
| Wealth to GDP | 5.94 (I-D4a, Round 8) | 6.81 (Round 7, old pension basis, I-D4a note) |
| Payer wealth share | 92.7% + 5% tail = 97.7% | 93% (v2 record, I-D4c note) |
| Capitalisation and behaviour | +0.49, then x0.88 | none |
| ω | 5.54 | 6.33 |
| g | 4.42% (geometric) | 4.74% (arithmetic, I-D1a note) |
| g · ω, % of GDP | 24.49 | 30.02 |
| **Implied ε** (7.34 / g · ω) | **30.0%** | **24.5%** |
| ε · g · ω at ε = 20% | 4.90 | 6.00 |

Reading. My 2026-11-16 illustration (3% of GDP at 20%) does not follow from the register: at 20% the product is 4.9 to 6.0. The implied ε of 24% to 30% is a wealth-weighted rate on gains inside v2's 4% to 90% logistic (`logistic_ln_ref`); the repo does not record v2's wealth-weighted ε, so the check is one-sided. Likely sources of any residual gap, from the register without fitting: ω (the old against the revised pension valuation moves I-D4a from 5.94 to 6.81, +15%); g (arithmetic against geometric, +7%; the 1950-2019 sub-sample mean is 5.56%, +26%); no behavioural response in v2 (+14% on the base); the refund cap (A3). Each is a choice for stage C, not a fit.

## 5. Tornado tables
### M1 (revenue, % of GDP; central 1.45)
| Rank | Input | Row id | Tier | Input low / central / high | Result at low | Central | Result at high | Swing | Note |
|---|---|---|---|---|---|---|---|---|---|
| ~~1~~ | ~~Mean real total return on wealth, geometric~~ **superseded (section 10)** | I-D1a | 1 | 2.18 / 4.42 / 7.47 | -2.27 | 1.45 | 6.51 | 8.78 |  |
| 2 | Household wealth to GDP, total wealth incl. private pensions | I-D4a | 1 | 5.8 / 5.94 / 7.5 | 1.29 | 1.45 | 3.23 | 1.94 |  |
| 3 | Share of affected people leaving UK tax residence after a targeted tax | I-D5c | 1 | 0.0 / 6.0 / 11.0 | 1.95 | 1.45 | 1.03 | 0.92 |  |
| 4 | Loss of taxable base to all behavioural responses at a 1% annual wealt | I-D5a | 1 | 7.0 / 12.0 / 17.0 | 1.87 | 1.45 | 1.03 | 0.83 |  |
| 5 | Share of total wealth held by those adults | I-D4c | 1 | 89.7 / 92.7 / 96.4 | 1.22 | 1.45 | 1.73 | 0.51 |  |
| 6 | Part of the response that is avoidance or under-reporting | I-D5b | 1 | 3.5 / 6.0 / 8.5 | 1.66 | 1.45 | 1.24 | 0.42 |  |
| 7 | Wealth missing from WAS at the top, as % of WAS total | I-D4e | 1 | 0.0 / 5.0 / 5.6 | 1.10 | 1.45 | 1.49 | 0.39 |  |
| 8 | Receipts, Corporation tax, central 2025-26 | I-T3f | M1d line | 3.24 / 3.37 / 3.55 | 1.58 | 1.45 | 1.27 | 0.31 |  |
| 9 | Fall in house price per £1 of annual council tax | I-D10a | 1 | 24.4 / 30.4 / 33.6 | 1.34 | 1.45 | 1.51 | 0.17 |  |
| 10 | Rise in dwelling and land value if council tax is retired, full capita | I-D10b | 1 | 19.4 / 24.2 / 26.7 | 1.34 | 1.45 | 1.51 | 0.17 |  |
| 11 | Corporation tax receipts, 2025-26 | I-D7d | 2 | 96.6 / 100.4 / 101.1 | 1.58 | 1.45 | 1.43 | 0.15 |  |
| 12 | Receipts, of which property transactions, central 2025-26 | I-T3k | M1d line | 0.43 / 0.5 / 0.57 | 1.52 | 1.45 | 1.38 | 0.14 |  |
| 13 | Corporate levy yield, v2 | I-D7a | 2 | 2.77 / 2.82 / 2.88 | 1.40 | 1.45 | 1.51 | 0.11 |  |
| 14 | Levy yield as a share of corporation tax retired | I-D7c | 2 | 0.82 / 0.84 / 0.85 | 1.39 | 1.45 | 1.49 | 0.10 |  |
| 15 | Receipts, Capital gains tax, central 2025-26 | I-T3h | M1d line | 0.73 / 0.77 / 0.82 | 1.49 | 1.45 | 1.40 | 0.09 |  |
| 16 | Understatement of assessed value for assets with discretionary valuati | I-D5d | 1 | 0.0 / 11.0 / 22.0 | 1.49 | 1.45 | 1.41 | 0.08 |  |
| 17 | Receipts, Business rates, central 2025-26 | I-T3m | M1d line | 1.33 / 1.29 / 1.26 | 1.41 | 1.45 | 1.48 | 0.07 |  |
| 18 | Receipts, Council tax, central 2025-26 | I-T3n | M1d line | 1.72 / 1.75 / 1.78 | 1.48 | 1.45 | 1.42 | 0.06 |  |
| - | Share of a cut in stamp duty that ends up in the pre-tax house price | I-D10c | 1 | 0.0 / 40.0 / 100.0 | n/r | 1.45 | n/r | 0 | Share of a stamp duty cut that reaches house prices. Needs the transaction turnover, which the register does not hold. Not reachable. Direction: a higher share raises omega. |
| - | Discount rate, years 1 to 30 | I-D11a | 2 | 3.0 / 3.0 / 3.5 | n/r | 1.45 | n/r | 0 | Discount rate: M3 only. |
| - | Discount rate, years 31 to 75 | I-D11b | 2 | 2.5 / 2.5 / 3.0 | n/r | 1.45 | n/r | 0 | M3 only; unused at G = 30. |
| - | Discount rate, years 76 to 125 | I-D11c | 2 | 2.25 / 2.25 / 2.5 | n/r | 1.45 | n/r | 0 | M3 only; unused at G = 30. |
| - | Discount rate beyond year 125 | I-D11d | 2 | None / None / None | n/r | 1.45 | n/r | 0 | M3 only; no value. |
| - | Standard deviation of annual real total return | I-D1b | 1 | 6.5 / 8.2 / 9.8 | n/r | 1.45 | n/r | 0 | Spread of annual returns. In the identity refunds are netted in g, so sigma acts only through the refund cap and the fill years (not reachable). Direction: a higher sigma raises the arithmetic mean over the geometric g (+0.34 points of return at the central 8.2%, my arithmetic) and the loss-year share. |
| - | Loss-year frequency, share of years with negative real return | I-D1c | 1 | 15.0 / 22.9 / 28.2 | n/r | 1.45 | n/r | 0 | Loss-year share. Acts through refunds, the cap on them and the reserve fill (P1, P4). Not reachable on the identity. Direction: more loss years, larger refunds, longer fill. |
| - | Longest run of consecutive loss years | I-D1d | 1 | 1.0 / 3.0 / 6.0 | n/r | 1.45 | n/r | 0 | Longest loss run. Acts on the reserve fill and on P3 only. Not reachable. Direction: a longer run lengthens the transition. |
| - | Gap between the end of the return history and the last full year | I-D1e | 1 | 5.0 / 6.0 / 6.0 | n/r | 1.45 | n/r | 0 | Gap between the end of the return history and the last full year. A data-vintage input; no term in the identity. |
| - | Share of adults at or above W_min = £150,000 | I-D4b | 1 | 49.3 / 54.9 / 64.3 | n/r | 1.45 | n/r | 0 | Share of adults at or above W_min. Sets the number of payers and M2b; omega depends on the wealth share I-D4c, not on the head count. |
| - | Top 1% wealth share, 2016-18 | I-D4d | 1 | 14.4 / 18.0 / 23.0 | n/r | 1.45 | n/r | 0 | Top 1% share: a check on the tail (I-D4e), no separate term. |
| - | Sunday Times Rich List 2026, combined wealth of 350 entries | I-D4f | 1 | 784.0 / 784.0 / 784.0 | n/r | 1.45 | n/r | 0 | Rich List total (one value): cross-check on I-D4e, no range. |
| - | Household net worth over GDP, national balance sheet basis | I-D4g | 1 | 3.6 / 3.6 / 3.6 | n/r | 1.45 | n/r | 0 | National balance sheet ratio (one value): cross-check on I-D4a, no range. |
| - | Share of council tax receipts borne by the top income decile | I-D6a | 1 | 13.5 / 13.5 / 14.0 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of business rates receipts borne by the top income decile | I-D6b | 1 | 23.2 / 23.7 / 23.7 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of corporation tax receipts borne by the top income decile | I-D6c | 1 | 22.7 / 24.5 / 25.7 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of capital gains tax receipts borne by the top income decile | I-D6d | 1 | 52.0 / 55.0 / 55.0 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of inheritance tax receipts borne by the top income decile | I-D6e | 1 | 25.0 / 28.5 / 30.4 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of stamp duties on property receipts borne by the top income dec | I-D6f | 1 | 21.8 / 21.8 / 28.2 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of stamp taxes on shares receipts borne by the top income decile | I-D6g | 1 | 21.8 / 25.0 / 28.5 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of council tax receipts borne by the bottom five income deciles | I-D6h | 1 | 44.8 / 45.8 / 47.1 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of business rates receipts borne by the bottom five income decil | I-D6i | 1 | 29.8 / 30.6 / 32.4 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of corporation tax receipts borne by the bottom five income deci | I-D6j | 1 | 28.5 / 30.7 / 33.9 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of capital gains tax receipts borne by the bottom five income de | I-D6k | 1 | 2.5 / 3.3 / 4.9 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of inheritance tax receipts borne by the bottom five income deci | I-D6l | 1 | 33.3 / 34.5 / 40.4 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of stamp duties on property receipts borne by the bottom five in | I-D6m | 1 | 24.5 / 36.0 / 36.0 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of stamp taxes on shares receipts borne by the bottom five incom | I-D6n | 1 | 33.3 / 33.3 / 36.0 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of business rates receipts borne by the top income decile, ONS a | I-D6o | 1 | 15.7 / 15.7 / 18.6 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of business rates receipts borne by the bottom five income decil | I-D6p | 1 | 37.7 / 42.7 / 42.7 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Share of stamp duty on house purchase borne by the top original-income | I-D6q | 1 | 55.9 / 55.9 / 55.9 | n/r | 1.45 | n/r | 0 | Incidence by income decile: allocates the retired taxes among households (M4a), not the receipts (M1d). |
| - | Corporation tax receipts retired by WDT, 2025-26 | I-D7b | 2 | 3.37 / 3.37 / 3.37 | n/r | 1.45 | n/r | 0 | Single value; its range is in I-T3f (below). |
| - | Reserve target as a multiple of the trailing mean annual refund, each  | I-D8a | 2 | 3.0 / 3.0 / 3.0 | n/r | 1.45 | n/r | 0 | Reserve multiple. Acts on fill years and the transition only; steady-state M1 is unchanged. |
| - | Long reserve fill time | I-D8b | 2 | 6.0 / 7.0 / 10.0 | n/r | 1.45 | n/r | 0 | Long reserve fill time (P1): transition only. |
| - | Short reserve fill time | I-D8c | 2 | 3.0 / 3.0 / 3.0 | n/r | 1.45 | n/r | 0 | Short reserve fill time (P1): transition only. |
| - | Mean gross household income, wealth D4 to 5 | I-D9a | 1 | 40200.0 / 50300.0 / 60400.0 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Mean gross household income, wealth D6 to 7 | I-D9b | 1 | 50400.0 / 63000.0 / 75600.0 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Mean gross household income, wealth D8 to 9 | I-D9c | 1 | 57200.0 / 71500.0 / 85800.0 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Mean gross household income, wealth D10 | I-D9d | 1 | 57100.0 / 71400.0 / 85700.0 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Net financial wealth as share of total wealth, wealth D4 to 5 | I-D9e | 1 | 5.6 / 6.6 / 6.6 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Same, wealth D6 to 7 | I-D9f | 1 | 8.4 / 9.3 / 9.3 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Same, wealth D8 to 9 | I-D9g | 1 | 10.4 / 12.8 / 12.8 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| - | Same, wealth D10 | I-D9h | 1 | 17.1 / 19.3 / 21.5 | n/r | 1.45 | n/r | 0 | Income and liquid assets by wealth band: enter M2b, M2c and M4b, not M1. |
| 19 | Receipts, Inheritance tax, central 2025-26 | I-T3i | M1d line | 0.27 / 0.27 / 0.27 | 1.45 | 1.45 | 1.45 | 0.00 |  |
| 20 | Receipts, of which stamp taxes on shares, central 2025-26 | I-T3l | M1d line | 0.16 / 0.16 / 0.16 | 1.45 | 1.45 | 1.45 | 0.00 |  |

Lever for scale (not an input): the six v2 schedules give WDT of 3.12 to 9.35 (`synthesis.md` section 10), so M1 of -2.77 to +3.46, a swing of 6.23. It sits second after g. Held at A1 in every row above.

### M2 (mean burden proxy, % of payer wealth a year; central 1.24)
M2 proper is revenue-weighted (`metrics.md`) and larger than the mean burden; only the mean is reachable. ω, the retired taxes and the discount rates do not enter it.
| Rank | Input | Row id | Tier | Input low / central / high | Result at low | Central | Result at high | Swing | Note |
|---|---|---|---|---|---|---|---|---|---|
| ~~1~~ | ~~Mean real total return on wealth, geometric~~ **superseded (section 10)** | I-D1a | 1 | 2.18 / 4.42 / 7.47 | 0.61 | 1.24 | 2.09 | 1.48 |  |
| 2 | Part of the response that is avoidance or under-reporting | I-D5b | 1 | 3.5 / 6.0 / 8.5 | 1.27 | 1.24 | 1.21 | 0.07 |  |
| 3 | Understatement of assessed value for assets with discretionary valuati | I-D5d | 1 | 0.0 / 11.0 / 22.0 | 1.25 | 1.24 | 1.23 | 0.01 |  |

### M4a (non-payer savings, % of the non-payers' tax bill; central 29.7)
Only D6 incidence rows and the receipts lines enter. D6 top-decile rows (a to g, o, q) do not. The I-D6p row replaces I-D6i (the central uses I-D6i).
| Rank | Input | Row id | Tier | Input low / central / high | Result at low | Central | Result at high | Swing | Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Share of corporation tax receipts borne by the bottom five income deci | I-D6j | 1 | 28.5 / 30.7 / 33.9 | 28.86 | 29.72 | 30.96 | 2.09 |  |
| 2 | Receipts, Corporation tax, central 2025-26 | I-T3f | M1d line | 3.24 / 3.37 / 3.55 | 29.26 | 29.72 | 30.35 | 1.09 |  |
| 3 | Share of business rates receipts borne by the bottom five income decil | I-D6p | 1 | 37.7 / 42.7 / 42.7 | 30.77 | 29.72 | 31.51 | 0.74 |  |
| 4 | Share of stamp duties on property receipts borne by the bottom five in | I-D6m | 1 | 24.5 / 36.0 / 36.0 | 29.05 | 29.72 | 29.72 | 0.66 |  |
| 5 | Receipts, of which property transactions, central 2025-26 | I-T3k | M1d line | 0.43 / 0.5 / 0.57 | 29.43 | 29.72 | 30.01 | 0.58 |  |
| 6 | Share of council tax receipts borne by the bottom five income deciles | I-D6h | 1 | 44.8 / 45.8 / 47.1 | 29.51 | 29.72 | 29.98 | 0.46 |  |
| 7 | Share of business rates receipts borne by the bottom five income decil | I-D6i | 1 | 29.8 / 30.6 / 32.4 | 29.60 | 29.72 | 29.98 | 0.39 |  |
| 8 | Receipts, Council tax, central 2025-26 | I-T3n | M1d line | 1.72 / 1.75 / 1.78 | 29.56 | 29.72 | 29.87 | 0.32 |  |
| 9 | Receipts, Business rates, central 2025-26 | I-T3m | M1d line | 1.33 / 1.29 / 1.26 | 29.86 | 29.72 | 29.61 | 0.25 |  |
| 10 | Share of inheritance tax receipts borne by the bottom five income deci | I-D6l | 1 | 33.3 / 34.5 / 40.4 | 29.68 | 29.72 | 29.90 | 0.22 |  |
| 11 | Share of capital gains tax receipts borne by the bottom five income de | I-D6k | 1 | 2.5 / 3.3 / 4.9 | 29.64 | 29.72 | 29.86 | 0.21 |  |
| 12 | Share of stamp taxes on shares receipts borne by the bottom five incom | I-D6n | 1 | 33.3 / 33.3 / 36.0 | 29.72 | 29.72 | 29.76 | 0.05 |  |
| 13 | Receipts, Capital gains tax, central 2025-26 | I-T3h | M1d line | 0.73 / 0.77 / 0.82 | 29.70 | 29.72 | 29.73 | 0.03 |  |
| 14 | Receipts, Inheritance tax, central 2025-26 | I-T3i | M1d line | 0.27 / 0.27 / 0.27 | 29.72 | 29.72 | 29.72 | 0.00 |  |
| 15 | Receipts, of which stamp taxes on shares, central 2025-26 | I-T3l | M1d line | 0.16 / 0.16 / 0.16 | 29.72 | 29.72 | 29.72 | 0.00 |  |

### M3 (gain-weighted lifetime rate): not reachable
In the identity net WDT is ε times gains in every year, so the present-value ratio is ε whatever the discount rate. Direction only: I-D1a to I-D1d act through the refund cap (a loss year refunds less than the tax it reverses when the cap binds, which raises M3 against ε); I-D11a to I-D11d act only on the timing of tax against gain (unequal weights across a payer's life), the sign depends on whether gains arrive late; D4, D5, D6, D7, D9 and D10 do not enter. Ranking: ε (lever) first; no register input moves M3 at first order.

## 6. Tier 2 cut-off (0.5 points of GDP on M1)
| Input | Row ids | Swing on M1 | Below 0.5? | Result |
|---|---|---|---|---|
| D7 corporate levy yield | I-D7a, I-D7c | 0.11, 0.10 | yes | single range |
| D7 retired corporation tax, cross-check | I-D7b (no range), I-D7d | 0, 0.15 | yes | single range |
| D8 reserve rule | I-D8a to I-D8c | not reachable (transition, fill years) | yes | single range |
| D11 discount schedule | I-D11a to I-D11d | not reachable on M1 (M3 only) | yes | single range |
| Retired receipts lines (M1d, added to the list) | I-T3f, I-T3k, I-T3h, I-T3m, I-T3n, I-T3i, I-T3l | 0.31, 0.14, 0.09, 0.07, 0.06, 0, 0 | yes | single range |

Caveat. The register ranges for the levy are v2's yield band only. Whether corporation tax is retired at all moves M1d by 3.37 (the bar falls to 4.90 on `synthesis.md`): that is a policy lever, not an input, and is not a tier 2 input.

## 7. What the identity cannot do
- **Refunds.** A3 nets them in g. In loss years the cap (tax paid to date) binds for early years and for high-loss runs; then M1a exceeds ε g ω. The size needs a path run; I-D1b to I-D1d only act here.
- **Interactions** (a one-at-a-time tornado cannot show them), pairs to examine in stage C: g and the loss-year share and run length (refund cap and the fill); g and ε (a tax on gains changes the behavioural response I-D5a is measured against); ω and I-D5a/I-D5c (leavers are the tail, I-D4e, and hold the most wealth); I-D4a and I-D4e (the tail add-on may already sit in the Resolution Foundation valuation); I-D10b and I-D5 (capitalisation raises values and the incentive to understate); I-D1a and D11 (M3 timing).
- **Retirement order and staging.** The identity is steady state at full retirement. During the transition M1d rises in steps (ascending by receipts); P3 (shortfall) and P5 need the path.
- **Overlap.** I-D5a, I-D5b, I-D5c and I-D5d are not additive; I-D10a and I-D10b come from one range.
- **Aggregation.** One-at-a-time swings do not add. All-low and all-high corners were not run.

## 8. Checks
- Second method (`check.py`, hand arithmetic with the register numbers typed in): central M1 = 1.45; g low -2.27 and g high 6.52 (the script prints 6.51, rounding); I-D4a low 1.29; break-even g 3.547%.
- Seven retired lines sum to 8.11 from the IFS sheet cells 20 to 25 (`Revenue composition spreadsheet.xlsx`, '% GDP (cash)', 2025-26): 3.37 + 1.75 + 1.29 + 0.77 + 0.50 + 0.16 + 0.27.
- Traceability: every number is a register row id (listed in the tables) or an assumption A1 to A7.

## 9. For the author and guru
- Replace 8.27 with 8.11 in `metrics.md` (M1e), `drivers.md` section 1 and `synthesis.md` section 10, or tell me the stamp-duty reading is different.
- Decide whether stage C wants ε fixed at a schedule value (levers D2 and D3) before the next tornado; the ranking above holds at any ε because every M1a swing scales with it.
- The register range for I-D1a (10th to 90th percentile of rolling 30-year means) is wide enough to flip M1; this is the main uncertainty stage C should spend on.

## 10. Rerun 2026-11-18 (brief 041r): level 2 band on the arithmetic mean
Script `tornado/tornado_v2.py` (the original `tornado.py` is kept); second method `tornado/check_v2.py`; outputs `tornado_v2_*`. Both run with `python3 -I`. The register is the 274-row `inputs.md`; I-D1a is now the arithmetic mean, level 2: **3.41 / 4.74 / 6.07** % a year. Nothing else in the identity changed (M1b 2.82, M1c -0.6 (A2), M1d 8.11, omega 5.54).

### 10.1 The wealth-weighted rate ε at the arithmetic mean (assumption A1, a lever, not a register row)
| Treatment | ε | M1a at I-D1a central | M1 central |
|---|---|---|---|
| Held: ε = 29.97% from the first run (7.34 reproduced at g = 4.42, I-D1a2 central) | 29.97% | 7.87 (0.2997 x 4.74% x 5.54) | 1.98 |
| Recalibrated: 7.34 reproduced at g = 4.74 | 27.95% (7.34 / (4.74% x 5.54 x 100)) | 7.34 | 1.45 |

The brief's "about 31% recalibrated" does not reproduce from the register: recalibrating ε at the arithmetic mean lowers it (4.74 > 4.42), to 27.95%. A 31% figure would need g below 4.42% or a smaller omega. Flagged to the guru; both treatments are carried below. The ranking does not depend on the choice.

### 10.2 I-D1a swing and the other return rows
Swing = ε x omega x (6.07 - 3.41) = ε x 5.54 x 2.66.
| Treatment | Result at 3.41 | Central | Result at 6.07 | Swing |
|---|---|---|---|---|
| Held ε 29.97% | -0.23 | 1.98 | 4.19 | **4.42** |
| Recalibrated ε 27.95% | -0.61 | 1.45 | 3.51 | **4.12** |
| First run (geometric, 2.18 to 7.47, ε 29.97%), superseded | -2.27 | 1.45 | 6.51 | 8.78 |

Other return rows (I-D1b to I-D1g, I-D1a2, I-D1a0, I-D1f):
| Row | Reaches the identity? |
|---|---|
| I-D1b SD, band 7.47 to 8.96 | **No.** M1a = ε g ω has no SD term; refunds are netted in g (A3). It acts through the refund cap and the reserve fill; needs a path run (036r generator). |
| I-D1b2 lag-1, band 0.19 to 0.42 | **No**, same reason: it changes the spread of 30-year means and loss runs, not the steady-state mean. |
| I-D1a2 geometric mean (3.07 / 4.42 / 5.73) | Derived from I-D1a; belongs to M3 (wealth path compounding). Not varied separately. |
| I-D1c loss-year frequency, I-D1d longest run | Generator outputs, not inputs (register); reported, not varied. |
| I-D1a0 spread of 30-year means | Level 1 display, not a parameter range; **leaves the tornado**. |
| I-D1f, I-D1g | Named scenario; effective observations behind the I-D1a band. No range, no swing. |
| I-D1e data gap | Unchanged: no term in the identity. |

### 10.3 Ranking restated (M1, swing in points of GDP)
| Rank | Input | Row | First run | Rerun, ε held | Rerun, ε recalibrated |
|---|---|---|---|---|---|
| 1 | Mean real return, arithmetic, level 2 | I-D1a | 8.78 | 4.42 | 4.12 |
| 2 | Wealth to GDP | I-D4a | 1.94 | 2.08 | 1.94 |
| 3 | Leavers | I-D5c | 0.92 | 0.98 | 0.92 |
| 4 | Behavioural loss of base | I-D5a | 0.83 | 0.89 | 0.83 |
| 5 | Payer wealth share | I-D4c | 0.51 | 0.54 | 0.51 |
| 6 | Avoidance share | I-D5b | 0.42 | 0.45 | 0.42 |
| 7 | Missing top wealth | I-D4e | 0.39 | 0.42 | 0.39 |
| 8 | Corporation tax receipts (M1d line) | I-T3f | 0.31 | 0.31 | 0.31 |
| 9 | Council tax capitalisation | I-D10a, I-D10b | 0.17 | 0.19 | 0.17 |
| - | everything else | | below 0.15 | below 0.15 | below 0.15 |
M2 proxy, I-D1a swing (% of payer wealth a year): 1.48 first run; 0.75 held; 0.70 recalibrated (central 1.33 held, 1.24 recalibrated). M4a is unchanged (no return row enters it). Full tables: `tornado/tornado_v2_tables_held.md`, `tornado_v2_tables_recal.md`; CSVs alongside.

### 10.4 Changes from the first run
| Item | First run | Rerun | Why |
|---|---|---|---|
| I-D1a definition | geometric 4.42 | arithmetic 4.74 | the identity and the AR(1) generator use the arithmetic mean (stage C item 1) |
| I-D1a range | 2.18 to 7.47 (level 1 spread of 30-year means) | 3.41 to 6.07 (level 2: uncertainty of the true mean) | the first range counted level 1 return risk as parameter ignorance |
| I-D1a swing on M1 | 8.78 | 4.42 held, 4.12 recalibrated | band 2.66 points wide against 5.29 |
| ε | 29.97% | 29.97% held or 27.95% recalibrated | A1 |
| M1 central | 1.45 | 1.98 held, 1.45 recalibrated | held ε on a higher g raises M1a |
| I-D1b, I-D1b2 | I-D1b "not reachable" | both not reachable, stated with reasons | no SD or lag-1 term in the identity |
| I-D1a0 | not in the first run | leaves the tornado | not a parameter range |
| Rank 1 | I-D1a (8.78 vs 1.94 next) | I-D1a (4.12 to 4.42 vs 1.94 to 2.08 next) | unchanged order; the lead falls from 4.5 times to 2.1 times the next input (both treatments) |
| Other swings | | about 7% larger with held ε (they scale with ε g); equal with ε recalibrated | first run's M1 identity values |
| Tier 2 cut-off 0.5 | all tier 2 below | unchanged (largest 0.15) | section 6 stands |

### 10.5 Break-even return and its level 2 probability
M1 = 0 needs M1a = M1d - M1b - M1c = 8.11 - 2.82 + 0.6 = **5.89** % of GDP (I-T3f, I-T3n, I-T3m, I-T3h, I-T3i, I-T3k, I-T3l, I-D7b, I-D7a; M1c is A2). Then g* = 5.89 / (ε x omega) with omega = 5.54 (I-D4a, I-D4c, I-D4e, I-D10b, I-D5a).
| Treatment | ε x omega | Break-even arithmetic mean g* | z = (g* - 4.74) / 1.038 | P(true mean below g*) |
|---|---|---|---|---|
| Held ε 29.97% | 1.660 | **3.55%** | -1.15 | **12.5%** |
| Recalibrated ε 27.95% | 1.549 | **3.80%** | -0.91 | **18.3%** |
The standard error 1.038 is the level 2 band itself, (6.07 - 3.41) / 2 / 1.2816 (I-D1a; register note: 1.2816 x 1.04). The probability uses level 2 alone, a normal true mean around the sample 4.74; it does not include level 1 return risk (the year to year spread I-D1b, I-D1b2), which is a separate layer for the generator, and it takes ε, ω and M1d at central. Reading: with ε held, M1 turns negative at a true mean 1.19 points below the sample mean, about one chance in eight; with ε recalibrated, about one in five.

### 10.6 Checks
- `check_v2.py` (hand arithmetic, register numbers typed in): ε 0.2997 and 0.2795; central M1 1.45 and 1.98; I-D1a swing 4.12 and 4.42; I-D4a swing 1.94; g* 3.547 and 3.804; P 0.125 and 0.183. All match the script.
- Traceability: every number is a register row id or assumption A1 to A7. The new items: the 1.2816 normal quantile (the register's own method) and the normal approximation for the true mean (assumption A8, from I-D1a's note).
