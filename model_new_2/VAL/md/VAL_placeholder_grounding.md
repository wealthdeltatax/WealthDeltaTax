# VAL Phase 4: grounding the placeholders

Date: 5 October 2026. Scope: the placeholders in `[val_gen]` that the build log marks as pending Phase 4. Evidence is ballpark only. Nothing below is a calibration, and no placeholder should be reported as if it were one.

Route C is defined here as fungible but not professionally valued. It is a fluid category: a fungible asset can move between Route A and Route C at each assessment cycle. The Route C share is therefore a choice variable for the holder, not a fixed input.

## Summary

| Placeholder | Current value | Best anchor found | Confidence | Recommended change |
|:---|:---|:---|:---|:---|
| `route_shares.C`, `c_share_vals` | 8%; 2, 5, 8, 15, 25% | Business assets about 7% of household wealth; financial plus business about 20 to 25% | Low | Keep 8% as an economy-wide reference. Add a 40% stress point. |
| `lambda_base`, `lambda_vals` | 5%; 0, 1, 2, 5, 10% | Unicorn exit pace about 2% a year (US venture data) | Very low | Keep the grid. Relabel 5% as a 20-year mean wait. Report the minimum passing λ per rule set. |
| `hec_sigmas` | 0, 5, 10, 20% | Commercial property appraisal standard error 11% (range 6 to 13%) | Moderate | Keep. Cite the 11% figure for the 10% case. |
| `hec_phi` | 0.5 | Valuers anchor on past values (direction only) | Very low | Keep as a placeholder with the direction noted. |
| HEC bias | none (mean-zero error) | Illiquidity discounts 25 to 50%; private equity fair values below transaction price | Low | Add a bias parameter or fix the valuation basis in the rules. |
| `brg_tol` | 1% | UK tax gap 4.0 to 18.1% of liabilities by tax | Policy choice | Report the smallest tolerance at which each rule set passes. |
| `hsc_tol` | 1% | None needed | Not applicable | The test cannot fail as built. Pair HEC with the market-fall scenario. |
| `state_tol` | 2% | Irish one-year receipts forecast error (mean -1.1%; 2009 about -30%) | Low | Present 2, 5 and 10% side by side from `state_tol_sens`. |

## Route C share

The Wealth and Assets Survey (2016 to 2018, Great Britain) puts business wealth at £1.0tn of £14.4tn total household wealth, about 7% by simple division. That is the closest match to the 8% baseline, but it is the wrong concept for Route C. Survey business assets are assets used in a business the respondent runs, including unincorporated firms. Shares in private companies are counted in financial wealth. Roughly half of respondents who report owning a business give it a market value of zero, and the survey undercounts the business population by about 25%.

Financial plus business wealth is about 20% of the total, and about 25% once Sunday Times Rich List wealth and a Pareto correction are added. That bundle includes listed shares and cash, so it is an upper bound for assets that could sit in Route C. The reading of these shares comes from the extracted text of Figure 16 and should be checked against the figure. The share is higher for the taxpayers a wealth tax reaches: the paper reports that business and financial assets dominate for families above £5 million per adult, and a family just inside the top 1% has about £1.9 million per adult, which is close to `W_min` of £2m.

Two consequences follow. The top of the sweep is the relevant exposure, because a holder can move assets into Route C, and 25% is about the economy-wide ceiling, below what top taxpayers could hold. A 40% stress point is a judgment, not a sourced figure. Second, the strategy library holds route shares fixed, so the choice of how much to hold in Route C is not searched. Time-varying declaration strategies on a fixed share capture part of switching, since a move between A and C appears as a delta, but not the share decision itself.

Under CORR at λ of 5%, the best gain exceeds the 1% BRG placeholder from a Route C share of 15%. That lies inside the plausible range for top taxpayers, so the finding stands in the draft.

## Verification hazard λ

No source gives an annual verification rate for self-valued assets. HMRC compliance checks are selected by a risk model, so there is no uniform rate, and its published valuation-enquiry figures give tax under consideration, not counts. The only usable number is the pace of unicorn exits in US venture data: at the pace of the latest 12 months, the backlog would take just over 49 years to clear, about 2% a year. That is a loose lower anchor and not a UK family-business rate. The model's own note is correct that the WDT changes the listing decision, so historical exit rates do not transfer.

What λ implies in the model follows from the verified share, 1 − (1 − λ)^t. These figures are derived, not sourced.

| λ | Mean wait | Year share reaches 90% | Share at T = 100 |
|:---:|:---:|:---:|:---:|
| 1% | 100 years | about 229 | 63% |
| 2% | 50 years | about 114 | 87% |
| 5% | 20 years | about 45 | 99% |
| 10% | 10 years | about 22 | about 100% |

A 5% hazard means an average Route C asset is checked once in 20 years, shorter than the generation gap of 30. The candidate rule fails BRG at λ of 0, 1 and 2% and passes at 5 and 10%, so the verdict depends on a parameter that no source can pin down. The draft should state the minimum λ at which each rule set passes, not defend one value.

## Honest valuation error (HEC)

An analysis of Russell-NCREIF data estimates the standard error of institutional commercial property appraisals at 11.07%, with a robust range of 6 to 13%. This fits the sweep: 10% as the central case and 20% as a stress. It is property, not company equity, and it is professional appraisal, so it is an indirect anchor for Route C.

The error in practice is not mean-zero. A 2010 master's thesis found private equity fair values below transaction prices in 75% of cases, with an average deviation of -25%. That source is weak (one thesis, small sample). Illiquidity discounts of 25 to 50% are standard in private company valuation, with 35% cited as a common median. An honest family that applies a 25 to 35% marketability discount to an unlisted holding declares α of about 0.65 to 0.75 every year. That is persistent understatement, not noise, and it sits where understating gains. `_hec_paths` centres the error so that E[exp(e)] = 1, which removes this bias. The reported result that honest error pays mildly (mean gain up to +0.62% under BASE at λ of 0) was computed on mean-zero error, so a downward-biased valuer would do better than HEC shows. Either add a bias parameter, or have the valuation rules fix the basis (for example, no marketability discount) so that a discount counts as understatement.

Persistence (`hec_phi`) has directional support only. A practitioner source says valuers anchor on past values, which implies φ above zero. No estimate of the annual persistence of appraisal error was found.

## Tolerances

These are policy choices. The evidence gives reference points and a way to report.

**BRG.** HMRC's 2024-25 tax gap is 6.4% of liabilities: 4.0% for Income Tax, NICs and CGT, 6.6% for VAT, 5.5% for excise and 18.1% for Corporation Tax. Wealthy individuals account for about 5% of the gap (6% in 2024-25). No gap as a share of the wealthy group's own liabilities was found. A real-world gap x converts to a BRG tolerance of x·c, where c is the no-tax ceiling (`p5.no_tax_ceiling`): a family that recovers a fraction x of its tax gains x·c of its terminal wealth. At x of 4%, 6.4% and 18.1% that is 0.04c, 0.064c and 0.181c. The tax gap is an average over all taxpayers, most of them honest, while BRG tests the single best of 428 strategies, so a tolerance set from the gap is conservative. A cleaner standard is the WDT best response as a share of the conventional-tax best response, which HLC already computes.

**HSC.** Every rule shows exactly 0.000% honest cost, because honest declarations never touch the caps or resets. The test cannot fail as built. It would bite if honest valuation error from HEC were applied in the market-fall scenario.

**SPT and SST.** No UK forecast-error figure was found. Irish one-year-ahead forecasts of total tax receipts had a mean error of -1.1% over 1997 to 2012, with 2009 overestimated by almost 30%. A 2% tolerance therefore lies inside ordinary forecast noise. The candidate rule fails SST at every λ (near misses of -2.1% at 5% and -2.3% at 10%) and would pass at a 5% tolerance, so the verdict is sensitive to this one placeholder.

## Recommended changes

1. Add 0.40 to `c_share_vals`, and relabel `route_shares.C` as an economy-wide reference.
2. Keep `lambda_vals`; describe `lambda_base` as a 20-year mean wait; add a derived output giving the minimum passing λ per rule set.
3. Keep `hec_sigmas`; add a bias parameter to HEC, or specify the valuation basis in the rules.
4. Add a derived output giving the smallest BRG and state tolerance at which each rule set passes.
5. Add a route-switching strategy family, or flag the gap in the draft.
6. Apply HEC error in the market-fall scenario so that HSC can fail.

## Not found

- Private-company equity as a share of top-1% or £5m-plus wealth. Leads: Advani, Summers and Tarrant (2025), Table 3; HMRC business property relief data; Wealth Tax Commission background papers.
- Private equity holding periods, which would give an upper anchor for λ.
- How Swiss cantonal wealth taxes revalue unlisted shares.
- A UK forecast error for total receipts.
- The annual persistence of appraisal error.

## Sources

- Advani, Bangham and Leslie (2020), *The UK's wealth distribution and characteristics of high-wealth households*, Resolution Foundation: https://www.resolutionfoundation.org/app/uploads/2020/12/The-UKs-wealth-distribution.pdf
- Crunchbase News, unicorn exit pace: https://news.crunchbase.com/startups/unicorn-startup-exits-ipo-acquisitions-pace-backlog-data/
- Random disaggregate appraisal error in commercial property (Russell-NCREIF): https://core.ac.uk/works/3022173
- Fair value measuring in the private equity industry (master's thesis, 2010): https://openaccess.nhh.no/nhh-xmlui/handle/11250/169243
- Valuation and liquidity discounts, Financier Worldwide: https://www.financierworldwide.com/valuation-and-liquidity-discounts
- CAIA, private asset valuation and anchoring: https://caia.org/node/6664
- HMRC, Tax gap 2024-25 estimated at 6.4%: https://www.gov.uk/government/news/tax-gap-2024-25-estimated-at-64
- HMRC, Measuring tax gaps summary: https://www.gov.uk/government/statistics/measuring-tax-gaps/1-tax-gaps-summary
- Irish Department of Finance, one-year-ahead tax forecasts: https://www.fiscalcouncil.ie/wp-content/uploads/2020/01/FAR-APRIL-2013-BOX-B-DEPARTMENT-OF-FINANCE-ONE-YEAR-AHEAD-TAX-FORECASTS.pdf
