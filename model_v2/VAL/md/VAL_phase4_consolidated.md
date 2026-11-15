# VAL Phase 4: consolidated grounding note

Date: 5 October 2026. This note merges `brief_phase4_grounding.md` (parallel searches, then direct reading) with the placeholder review in this session. It supersedes `VAL_placeholder_grounding.md`, which contained two statements corrected in section 3.

Standard of evidence: a source counts as opened only if the page or PDF was read this session. Abstract-only sources are marked. Everything else is a lead. All figures are framing ranges (D9), not calibrations. Route C is fungible but not professionally valued, and an asset can move between Route A and Route C at each assessment cycle, so the Route C share is a choice variable for the holder.

## 1. Consolidated recommendations

| Key | Current | Low / central / high | Basis | Confidence | Action |
|:---|:---|:---|:---|:---|:---|
| `route_shares.C`, `c_share_vals` | C = 8%; 2, 5, 8, 15, 25% | 8% / 25% / 40% | WAS business assets about 7% of household wealth (opened). Top decile "other" wealth 26% and financial or business assets 30% (brief, opened). | Low | Add 0.40. Treat 8% as the economy-wide floor and 25% as the exposure case. |
| `lambda_base` (Route C) | 5%; 0, 1, 2, 5, 10% | 2% / 5% / 12% | US unicorn exits against the 741 still private: 15 in the past 12 months, 38 a year on the 5-year average, 86 in 2021 (opened, ratios derived). Brief upper end 20% (Tunguz, conditional on exit). | Low | Keep the grid and the 5% headline. Report the minimum passing λ per rule set. |
| λ for Route D | same as C | 2% / 5% / 10% | Judgment (brief). | None | Keep. |
| `rho` | 5% | 2.5% to 3.5% | Green Book STPR 3.5% to year 30, 3.0% to year 75, 2.5% after; 2026 review recommends 3.0% (brief, opened). | High for the figure | Decided at 3.5%, not yet applied. See section 4. |
| `hec_sigmas` | 0, 5, 10, 20% | 10% central | Russell-NCREIF appraisal standard error 11.07%, robust range 6 to 13% (abstract opened). Institutional property, so a Route D anchor. | Moderate for D, none for C | Keep. Cite for Route D only. |
| `hec_phi` | 0.5 | Route D high, Route C low | Serial correlation of valuations: real estate significant over three quarters (R-squared 75%), private equity one quarter only (13%) (opened). | Low | Make φ route-specific. Values stay placeholders. |
| HEC bias (new) | none | Route C down, Route D up; sizes unquantified | Private equity fair values below transaction price in 75% of cases, mean -25% (abstract opened). Marketability discounts 25 to 50%, 35% common median (opened). Appraisal upward bias, FHFA wp1803 (brief). | Low | Add a per-route bias parameter, or fix the valuation basis in the rules. |
| `brg_tol` | 1% | Policy choice | HMRC gaps 4.0% to 18.1% of liabilities by tax (opened). | Policy | Report the smallest tolerance at which each rule set passes. |
| `hsc_tol` | 1% | Not applicable | Every rule shows 0.000% honest cost (build log). | n/a | Make the test non-vacuous (section 6). |
| `state_tol` | 2%; 2, 5, 10% | Inside forecast noise | Irish one-year receipts forecasts (opened). | Low | Present 2, 5 and 10% side by side. |
| `hec_paths`, `hec_seed` | 200; fixed | Technical | n/a | n/a | Keep. |

## 2. Evidence by placeholder

**Route C share.** The Wealth and Assets Survey puts business wealth at £1.0tn of £14.4tn (about 7%), but business assets exclude shares in private companies, which sit in financial wealth. Financial plus business wealth is about 20%, and 25% after Rich List and Pareto adjustments. The ONS composition in the brief puts the top decile at property 38%, pension 36% and other 26%, and CAGE puts financial or business assets at 30% of the richest decile. Pensions and property are not Route C, so "other" (about 26%) is a ceiling for the top decile as a whole. The Route C share for the top 1% or for families above £5m per adult could exceed it, which is the case for a 40% stress point. That is a judgment, not a sourced figure. A family just inside the top 1% has about £1.9m per adult, close to `W_min` of £2m.

**Verification hazard λ.** The Crunchbase analysis counts 15 unicorn exits in the past 12 months against 741 still private (2.0%), a 5-year average of 38 a year (5.1%) and a record 86 in 2021 (11.6%). These ratios are my arithmetic on mixed years and are indicative. The population is US venture-backed unicorns, not family businesses, and Crunchbase notes a growing secondary market that gives liquidity without an exit. HMRC compliance checks use a risk model, so no uniform annual rate exists. What λ implies in the model follows from the verified share, 1 - (1 - λ)^t. The mean wait is 1/λ: 100 years at 1%, 50 at 2%, 20 at 5%, 10 at 10%.

**Honest valuation error.** The NCREIF estimate (11.07%, range 6 to 13%) is the only quantified error size, and it covers professional appraisal of institutional property. No source quantifies error for self-valued company equity. Private equity valuations underestimated transaction prices in 75% of the thesis sample, with a mean deviation of -25% (multiples: -14%). That is one 2010 thesis, read at abstract level. The marketability-discount range comes from restricted-stock studies from 1969 to 1989, which found mean or median discounts of 34 to 35%, with one later study at 20%. The article states that the discount affects pricing, not necessarily intrinsic value.

**Tolerances.** HMRC's provisional 2024-25 tax gap is 6.4% of £924.4bn of theoretical liabilities (£59.2bn). By tax: Income Tax, NICs and CGT 4.0%, VAT 6.6%, excise 5.5%, Corporation Tax 18.1%. Small businesses are 62% of the gap and wealthy individuals 6% (4% in 2020-21). HMRC lists improving the wealthy-taxpayer estimate as a future priority, so no wealthy-specific rate exists. Behaviourally, failure to take reasonable care is 35% of the gap, error 16% and evasion 12%. For the state tolerance, Irish one-year-ahead forecasts of total tax receipts had a mean error of -1.1% over 1997 to 2012 (+2.7% before the crisis, -24.7% in 2008-09), with a peak of +8.5% in 2006. Capital taxes did far worse (+21.8% before the crisis, -128.8% in 2008-09), and in 2005 capital and "other" taxes were 13% of revenue but over two-thirds of the error. A wealth tax base is asset-price sensitive, so it behaves more like capital taxes than like the total.

## 3. Conflicts and corrections

1. **The brief conflates φ and bias.** It lists `hec_phi` as "(bias)" and cites FHFA for its sign. In the TOML `hec_phi` is the persistence of the error, and HEC centres the error so that E[exp(e)] = 1, so bias is not a parameter at all. FHFA supports a bias sign, not a persistence value.
2. **The direction of honest bias differs by asset.** FHFA (brief) finds upward bias in appraisals, while the private equity thesis and marketability discounts point down. The incentive resolves this. A lender-driven appraisal anchors to a contract price. A self-declared wealth tax rewards a low value. Model the bias per route: down for Route C, up for Route D.
3. **Route C central share.** The brief chose 25% as central and I proposed 8% as the reference. With a fluid Route C, the exposure case is the larger one, so 25% is the case to defend and 8% is the floor.
4. **λ upper end.** The brief's 20% (Tunguz, median exit about 5 years from first funding) is conditional on companies that exit, so it overstates the hazard for the whole population. It is also above the grid. Adding it changes no verdict, because CORR already passes from 5%.
5. **Corrections to my earlier note.**
   - The CAIA piece does not show anchoring in private equity. It finds anchoring a serious concern only for real estate, with private equity limited to a one-quarter lag and an R-squared of 13%. I had overstated it as support for φ above zero in general. The page also contradicts itself on volatility (10.1% against 6.2% in the text, 11.06% against 16.81% in the appendix), so I used none of its volatility figures.
   - I called 2% a lower anchor for λ. It is the trough year. The 5-year average is about 5%, which supports the 5% headline for this population.
   - The HMRC estimates are provisional and are routinely revised up: 2023-24 from 5.3% to 6.0%, and 2022-23 from 4.8% to 5.7% and then 6.6%. HMRC rates 35% of the gap as high-uncertainty and advises reading the trend, not the level. The 4.0% for Income Tax, NICs and CGT is probably low, and the whole gap is not evasion.

## 4. Applying ρ = 3.5%

The brief records the decision but `WDT_Params.toml` still has `rho = 0.05`. As I read the code, ρ enters only the PV measures: `pv_true`, `pv_rel` (SPT), the life `pv` and `by_rho` blocks, and the PV panels of CDS and PSS. BRG gain is a ratio of terminal wealth and SST is a stake ratio, so neither uses ρ, and none of the 24 ids in the numbers register is built on a PV quantity. A rerun at 3.5% should therefore leave the register unchanged, which makes the register a regression test for this claim. A constant 3.5% over T = 100 discounts more heavily than the Green Book schedule, which falls to 3.0% after year 30 and 2.5% after year 75. Say so in the draft, and keep the 0 to 12% sweep.

## 5. Tolerance comparators

A real-world gap x converts to a BRG tolerance of x·c, where c is the no-tax ceiling in `p5.no_tax_ceiling`: a family that recovers a fraction x of its tax gains x·c of its terminal wealth. At gaps of 4.0%, 6.4% and 18.1%, the tolerances are 0.04c, 0.064c and 0.181c. Evasion alone is 12% of a 6.4% gap, or about 0.8% of liabilities (my arithmetic), which is the better comparator for deliberate misdeclaration. Because the gap is an average over taxpayers and BRG tests the best of 428 strategies, a tolerance set from the gap is conservative. Small-business Corporation Tax, the most self-reported regime, sits at the top of the range, so it is the closest analogue to Route C. The conventional-tax best response already in HLC is a cleaner standard that needs no external number.

## 6. Model gaps these sources surface

- **Route switching.** `_strategies()` holds route shares fixed, so the choice of how much to hold in Route C is not searched.
- **Bias and persistence by route.** HEC applies one error process to both routes with no bias.
- **HSC cannot fail.** Honest declarations never touch the caps or resets. Apply HEC error in the market-fall scenario so that it can.
- **Anchoring and shocks (hypothesis).** Stale declared values after a market fall would delay honest refunds, which could give HSC a non-zero cost. Not tested.
- **Verification independent of size.** The hazard does not depend on how large the misdeclaration is.

## 7. Source register

| Source | Used for | Status |
|:---|:---|:---|
| Advani, Bangham and Leslie (2020), Resolution Foundation, UK wealth distribution | Route C share, `W_min` | Opened |
| HMRC press release, Tax Gap 2024-25 | BRG comparator | Opened |
| HMRC, Measuring tax gaps summary (2026 edition) | BRG comparator, wealthy share | Opened |
| Crunchbase News, "The 49-Year Unicorn Backlog" (May 2024) | λ | Opened |
| Russell-NCREIF appraisal error (core.ac.uk/works/3022173) | σ | Abstract opened |
| Fair value measuring in private equity (NHH master's thesis, 2010) | Bias | Abstract opened |
| Financier Worldwide, "Valuation and liquidity discounts" (2017) | Bias | Opened |
| CAIA, Nesbitt, private asset valuation | φ | Opened |
| Irish Department of Finance forecasts (Fiscal Assessment Report, Apr 2013, Box B) | State tolerance | Opened |
| Tunguz exit timelines (PitchBook data) | λ upper end | Brief, opened there |
| FHFA wp1803 | Bias sign | Brief, opened there |
| Tax Observatory, UK UHNW | Route C share | Brief, opened there |
| Resolution Foundation, "The missing billions" | Route C share | Brief, opened there |
| HMT Green Book discounting guidance (Feb 2026) and Discount Rate Review 2026 | ρ | Brief, opened there |
| ONS, Household total wealth in GB, Apr 2020 to Mar 2022 | Route C share | Brief, opened there |
| Advani, Bangham, Leslie, CAGE wp576 (2021) | Route C share | Brief, opened there; no business-share figure extracted |
| DMO gilt auction releases | ρ | Unverified lead |
| Reading, "The accuracy of valuations" | σ | Unverified lead (access denied) |

## 8. Still open

1. The Reading valuation-accuracy paper, for a σ that covers company equity (needs the PDF).
2. A business-asset or private-company share for families above £5m per adult (CAGE wp576 body text, a CenTax table, or HMRC business property relief data).
3. Private equity holding periods, which would give an upper anchor for λ.
4. How Swiss cantonal wealth taxes revalue unlisted shares.
5. A UK, not Irish, forecast error for tax receipts.
6. Annual persistence of appraisal error.

## 9. Decisions for you

1. **Valuation basis.** Should the WDT rules require Route C to be valued without a marketability discount? If yes, an honest discounted declaration counts as understatement, and the bias parameter can be dropped in favour of the existing α rows. If no, HEC needs the bias parameter.
2. **ρ.** Apply 3.5% and rerun the full pipeline.
3. **Model gaps.** Whether to build route switching and route-specific HEC parameters now or flag them as limitations in the draft.
