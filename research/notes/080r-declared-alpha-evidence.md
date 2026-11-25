# 080r: evidence on declared value against true value (alpha)

Accessed 2026-11-20. Brief `docs/briefs/080r-declared-alpha-evidence.md`; data gap M-3 in `docs/model-v3/added/supporting.md`. Nothing here edits the register, the model or the manifest.

**Question, restated.** Among payers, how is declared value over true value (alpha) distributed: centre, spread, shape, any bunching or understatement pattern? The old papers' "behavioural centre near 1.1" (VAL section 7.1 and 7.3) is described there as a model-implied prediction that is "not an empirical estimate"; it rests on a refund asymmetry and an assumed error band of plus or minus 10 to 20% for illiquid assets. It has no source.

## Answer in brief
- **No source measures the distribution of declared over true value among wealth-tax payers, in the UK or elsewhere.** There is no UK wealth tax, and the UK inheritance tax data I found give a tax gap, not a value gap.
- The nearest direct evidence is foreign and partial: Sweden (cars, registry values: 75 to 80% of taxpayers near the threshold declared less than true value) and Colombia (the marginal buncher would have reported about 20% more wealth at the first notch, 9% at the second).
- The evidence points one way: **understatement where third-party reporting is weak, with a sizeable truthful minority.** It gives no support to a centre above 1 from the refund mechanism. Any regime with symmetric loss refunds is absent from the evidence, so that mechanism cannot be tested.
- Honest valuation noise has numbers: professional valuations differ from later sale prices by about 7% (UK, 2025) to 13% (US) in absolute terms. Owner self-reports of homes run above price indices (euro area about 9%), which is a different route to a centre above 1.
- M7c and M7d do not depend on the answer. Only M7e does, and on the OD1 grid it will read 1.00 for any centre between about 0.875 and 1.125 (section 4).

## 1. Sources

How read: **held** means checked in a PDF in `literature/` (`Fiscal Studies - 2021 - Advani - Behavioural responses to a wealth tax.pdf`, S13, printed page given). **Fetched** means read through the web fetch tool, which returns a summary; page numbers are the tool's, not checked by me. The shell cannot reach the sites, so primary PDFs could not be opened. Licences were not seen for any source: cite only, reproduce nothing.

### 1.1 Declared against true value, direct

| # | Source | Quantity | Number | Sample, year | Country | How read |
|---|---|---|---|---|---|---|
| 1 | Seim (2017), AEJ: Economic Policy 9(4) | Share of taxpayers near the exemption threshold reporting assets (mostly cars) below registry value | 75 to 80% (held, S13 printed p. 522); 75 to 85% in the fetched text (pp. 396-397, 414). Not reconciled; the held figure is used. Truthful: 15 to 25% of car owners (fn 20, p. 414, fetched). Cut tax liability by about 70% near the kink (fetched, p. 414). Under-reporting explains about a third of bunching: excess mass 0.61 falls to 0.41 (p. 413, fetched; S13 agrees on "one-third"). Elasticity due to under-reporting 0.03 to 0.09 (S13). Tax lost to car under-reporting 5.5% of wealth-tax revenue in 2000, 4.5% in 2006 (p. 414, fetched) | Administrative data 2000-2006, about 31 to 34 million person-years; cars only, bunchers near the threshold | Sweden | held (S13), fetched (Seim) |
| 2 | Londoño-Vélez and Ávila-Mahecha (2024), NBER WP 32134 (earlier AER: Insights 2021) | Wealth the marginal buncher would have reported without the tax; asset-level understatement among bunchers | Marginal buncher reports 20% more at the 2010 notch (alpha about 0.83) and 9% more at the second notch (about 0.92) (p. 12). Inventories reported 22% lower among record-keepers, about 20% of the sample (p. 24). Debt ratio 35% above a 9.4% baseline (p. 22). "Other assets" about 55% lower, marginally significant (p. 24). Revenue loss up to one fifth of the expected gain (pp. 2, 13). Third-party reported assets (bank, listed shares) are not understated (p. 7) | Wealth tax returns 2002-2017, income tax data 1993-2016 | Colombia | fetched; S13 held for the 22% and 35% (printed p. 522) |
| 3 | Brülhart, Gruber, Krapf and Schmidheiny (2022), AEJ: Economic Policy 14(4) | Evasion share of the response; bunching | No estimate of understated values. Authors say no rigorous estimates of evasion exist for Switzerland (p. 7, fetched). Bern bunching small: 6,404 excess filers, about 0.3% of filers above the notch (p. 19). Non-financial wealth responds about half as much as financial (Table 7, p. 19), marginal. S13 (held, printed p. 521) reports that about half the elasticity sits in reported financial assets; of the whole response only 1.3 points is voluntary offshore disclosure, and the authors attribute the rest of that half to evasion | Cantons 2003-2012; Bern 2001-2011 | Switzerland | fetched (abstract and body); S13 held |
| 4 | Statistics Norway, Rapport 2022/31 and article "Valuation of unlisted equity in Norway" | Estimated market value over tax value of unlisted firms | About 1.9 times over 2004-2019 (declared about 53% of market), about 2.15 in 2019, range about 1 to 3 across years. With the 2022 rebate of 25%, owners are taxed on about 35% of estimated value (p. 8, 28). No spread across firms | Price-to-book of about 2,200 listed and 600 NOTC firm-years 2004-2019 applied to unlisted firms (a strong assumption, as the authors say) | Norway | fetched |
| 5 | Thoresen, Ring, Nygård and Epland (2021 version), "A wealth tax at work" | Taxable household wealth against market wealth | Taxable about NOK 1,800bn against about 6,800bn market in 2018, under 30% (Sec. 3.1, p. 10). Statutory discounts: homes 75% from 2010, shares 0 to 45% over 2016-2021 (Table 1). Authors note reported wealth is also understated, especially unlisted firms (fn 23, p. 10) | Register data 2018 | Norway | fetched |

Rows 4 and 5 measure a **rule** (statutory valuation), not misdeclaration. They show how large declared over true gets when a rule sets the value (0.3 to 0.5), and are not a behavioural alpha.

### 1.2 UK evidence found (none measures alpha)

| # | Source | Quantity | Number | Sample, year | How read |
|---|---|---|---|---|---|
| 6 | HMRC, Measuring tax gaps (other taxes) and methodological annex | Inheritance tax gap | 3.0% of theoretical liabilities, about £0.3bn, in 2024-25; the 2022-23 estimate corrected to 3.7%. Bottom-up risk-based audit model with a non-detection multiplier of 1.7. All non-compliance; the pages do not break out valuation errors | Audit data from 2013-14 | fetched |
| 7 | Professional Adviser (17 Sep 2012), citing an FOI request by UHY Hacker Young | HMRC challenges to IHT property valuations | More than 10,000 valuations assessed in 2011, almost £90m extra tax, over £27,000 per case on average. Secondary source; no base values, so no alpha | 2011 | fetched |
| 8 | Property Investor Today (Apr 2026), citing TWM Solicitors | Referrals of IHT property valuations to the Valuation Office Agency | 11,845 rising to 14,631 (up 23.5%) in the 12 months to 30 Sep 2025; residential property 46.8% of net estate value in 2022-23 (£29.5bn), as reported. Basis of the referral count not stated | 2024-25 | fetched |
| 9 | National Audit Office (May 2025), Collecting the right tax from wealthy individuals | IHT context | About £4bn IHT from wealthy individuals in 2023-24, roughly half of IHT. Nothing on valuation error in the first part read (about 100,000 of 123,000 characters) | 2023-24 | fetched, partly |
| 10 | ONS, Household total wealth in Great Britain: quality and methods guide | Self-reported property values in the Wealth and Assets Survey | Typically higher than UK HPI and lender HPIs; the guide gives no size. Top-tail under-coverage and differential non-response among the very wealthy | WAS | fetched |
| 11 | Advani and Tarrant (2021), S13, and Daly, Hughson and Loutzenhiser (2021) | UK valuation range | Professional valuations, such as those for IHT, can return a range of legitimate values, and the lowest cannot be prevented from being reported (S13 printed pp. 527-528, held). Disputed UK valuation ranges "can be very wide" (Pentelow 2020, as cited by the 2021 paper). No number | | held (S13), fetched (Daly et al.) |

### 1.3 Honest valuation noise and bias (no tax incentive to misreport)

| # | Source | Quantity | Number | Sample, year | Country | How read |
|---|---|---|---|---|---|---|
| 12 | MSCI, Valuation and Sale Price Comparison 2025 | Sale price against earlier valuation, commercial property | Mean absolute difference 7.4% (7.0% value-weighted). Average premium of sale over valuation +0.5% (+0.8% weighted). Global: 8.6% and 7.6%, 2,018 sales in 26 countries | 486 UK sales in 2025; series 2000-2025 | UK | fetched |
| 13 | Cannon and Cole, "How accurate are commercial real estate appraisals?" (MPRA 52621) | Sale price against appraisal two quarters earlier | Bias +4.9% (+3.9% adjusted for market change); mean absolute difference about 13% (12.5% adjusted); median absolute about 8 to 8.6% | 7,214 sales, 1984 to mid-2010 | US | fetched |
| 14 | ECB Working Paper 2328 (Household Finance and Consumption Survey, wave 2) | Owners' self-reported home value against a hedonic price index | Euro-area mean overstatement about 8.7%; 3.2% Germany to 22.0% Italy; interquartile range about 61% as read (check before use) | About 75,000 observations, interviews 2013-2015 | Euro area, not UK | fetched |

### 1.4 Searched, not usable
- Uruguay (IZA DP 12286, Bergolo and others, 2019): income-tax bunching at a kink; no wealth, no declared against true value.
- Netherlands (IZA DP 17722, Kastoryano, 2025): Box 3 declarations after announcements, about €30m of previously undeclared tax; Box 3 taxes a deemed return, so alpha has no counterpart.
- Spain (Durán-Cabré and others, IEB WP 2019/04 and 2025/15): Catalonia, 2011-2015 returns. No valuation test; the authors say asset values follow assessment rules (unlisted firms at book value). About 15.2% of 2011 filers filed a supplementary return around the Nov 2012 amnesty (fn 47, p. 11), which the authors read as earlier under-declaration. The 2025 paper finds audits raise compliance only briefly. No understatement magnitude.
- UK private-company valuation gaps: nothing found.

## 2. What the evidence supports

1. **Shape: a truthful point mass plus an understating tail.** Seim's cars are the only individual-level comparison against registry values: a truthful 15 to 25% and 75 to 80% below true value, near a threshold. Colombia gives the depth for the marginal buncher (alpha 0.83 and 0.92) and for one asset class (inventories, 0.78).
2. **Depth: 0.78 to 1.0 on discretionary assets.** The three published Colombian points bracket I-D5d (0 / 11 / 22% understatement, alpha 1.00 / 0.89 / 0.78).
3. **Third-party reporting decides it.** Both Seim and Colombia find under-reporting concentrated where there is no third-party report. VAL section 7.5 already sets Routes A and B to alpha 1 by rule; the kernel sets A, B and Cv at the true price and applies alpha only to Routes C and D (`core/kernel.py` `declare`). The evidence therefore bears on Route C and D declarations only.
4. **Noise: 7 to 13% mean absolute error for professionally valued property, none found for private companies.** The VAL band of 10 to 20% is above the UK figure and at or just above the US one.
5. **Sign of honest bias is mixed.** Appraisals sit below later sale prices (alpha about 0.95 to 1.00); owners' self-reports sit above price indices (alpha about 1.09 in the euro area, direction only for the UK). Neither tests the refund-asymmetry mechanism, which the foreign systems do not have.
6. **No evidence for taxpayers raising declarations to protect refunds.** A centre of 1.1 can be produced by owner over-estimation of their homes alone, a belief effect, with no refund motive. That cannot be separated from the model's mechanism with this evidence.
7. **UK scale check.** The IHT gap is 3.0 to 3.7% of liability. It bounds all IHT non-compliance in a self-assessed, valuation-heavy tax, not valuation error alone, and cannot be turned into an alpha without estate sizes.

**Consistency check on the register (my arithmetic).** Routes C and D hold 8 + 17 = 25% of initial value (I-D13c, I-D13d; 22 to 27% across the C range). I-D5d at 0 / 11 / 22% on that share gives a mean shortfall of 0 / 2.75 / 5.5% of value. I-D5b is 3.5 / 6.0 / 8.5% of the base, about 3 points higher at each end. So roughly half of I-D5b is not understatement of declared C and D value; it is avoidance, non-declaration or the extensive margin, as its own definition allows. I-D5b should not be used to set the alpha distribution. I-D5d is read here as a mean over all C and D assets; if a truthful share P1 is added, the depth among understaters is I-D5d divided by (1 minus P1), 13.75% at P1 = 20%.

## 3. Proposed rows for M7e (table only; the register is not edited)

**Form.** A parametric mixture over route-level alpha, binned onto the OD1 grid by the caller, fits better than support-and-weights. Weights on eight grid bins would be seven free numbers with no source. The mixture needs five quantities; the evidence fixes the depth, bounds the truthful share and the noise, and says nothing on overstatement. Ids are placeholders.

| Placeholder | Quantity | Unit | Low | Central | High | Data or J | Evidence and link |
|---|---|---|---|---|---|---|---|
| P1 | Share of Route C and D value declared at true value (point mass at alpha 1) | % of C and D value | 15 | 20 | 25 | Low and high are data for one asset class (Seim, cars, near a threshold; fn 20 fetched); transfer to C and D assets and the midpoint are **(J)** | Routes A and B are at 1 by rule, so the truthful share of all initial value is I-D13a + I-D13b + P1 x (I-D13c + I-D13d), about 80% at central |
| P2 | Mean understatement among Route C and D assets | % of true value | 0 | 11 | 22 | Existing row I-D5d (already **(J)**); the three Colombian points 0.78, 0.83, 0.92 are consistent with it | No new row. If P1 is added, I-D5d's wording should say whether it is a mean over all C and D assets or over understaters |
| P3 | Noise in honest valuation, mean absolute error of declared against true | % of true value | 7 | 10 | 13 | Low and high are data for professionally valued property (UK 7.4%, US 12.5 to 13%); the central midpoint and the transfer to private assets are **(J)**. For a normal error, standard deviation is about 1.25 times the mean absolute error: 9, 12.5, 16% | Compare the VAL band of 10 to 20% |
| P4 | Bias of honest declaration (centre of the non-strategic part) | alpha | 0.95 | 1.00 | 1.09 | Bounds are data (appraisal below sale about 0.95 to 1.00; owners above index about 1.09, euro area); the central 1.00 is **(J)** | Sign is mixed, so central stays at 1 |
| P5 | Share of Route C and D value declared above true to keep refund protection, and by how much | % and alpha | no value | no value | no value | **(J)** only. No source, because no regime with symmetric refunds exists | The VAL section 7.3 centre of 1.1 is a model-implied assumption. Options for the author: drop the component, so the centre is set by P4, or keep it as a stage C lever labelled unsourced |

**What the evidence cannot support.** A distribution with its own sourced centre and spread. **The weaker statement it can support:** on Route C and D assets, declared value is more likely below than above true value where no third party reports it; a truthful minority of roughly one in five exists in the one test found; understatement of 8 to 22% is observed at the margin; honest noise alone is 7 to 13% in absolute terms. Whether the WDT's refund symmetry and auction deterrent shrink or reverse that pattern cannot be inferred from foreign systems without those features.

## 4. Effect on OD1

- **M7c and M7d: no change.** Both are evaluated at every alpha on the grid; the curve does not depend on who chooses what.
- **M7e: only this line depends on the answer.** On the OD1 grid (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0) any centre between about 0.875 and 1.125 falls in the 1.0 bin, so the old 1.1 would read 1.00 (nearest-bin mode, `modal_alpha` in `core/support.py`), and for any unimodal mixture of P1 to P4 with a centre in that range (spread 9 to 16%) the mode stays at 1.00. M7e would then show the grid, not the evidence. A finer grid near 1, or a mean or median declared alpha beside the mode, would carry information; that choice belongs to the guru and the author.
- **O7 (tolerant zone).** Observed understatement reaches alpha 0.78, just under the old zone's lower edge of 0.8 (VAL section 7.1, an old-paper run, not v3). Once v3 computes the zone, the evidence supports one reading: observed understatement depth is at or near the zone's edge.
- The brief's decision (provisional run without M7e) is unaffected: this note changes nothing on the critical path.

## 5. Open questions for the author
1. **Foreign evidence.** The only evidence for P1 to P3 is from Sweden, Colombia and non-UK property markets (UK for P3 and the IHT scale check only). Use it for rows P1 to P4 flagged **(J)** with the Coverage cell stating the foreign origin (the register's practice for I-W9)? Proposed resolution: yes, as flagged rows, and keep P5 as an unsourced lever.
2. **I-D5d wording** if P1 is adopted (see section 2). Proposed resolution: the guru decides at the next register edit.

## Sources
- Seim (2017): https://eml.berkeley.edu/~saez/course/seimAEJ17wealth.pdf
- Londoño-Vélez and Ávila-Mahecha (2024): https://www.nber.org/system/files/working_papers/w32134/w32134.pdf
- Brülhart and others (2022): https://edoc.unibas.ch/90165/1/pol.20200258.pdf and https://www.nber.org/papers/w22376.pdf
- Statistics Norway, valuation of unlisted equity: https://www.ssb.no/en/virksomheter-foretak-og-regnskap/skatt-for-naeringsvirksomhet/artikler/valuation-of-unlisted-equity-in-norway
- Statistics Norway Rapport 2022/31: https://www.ssb.no/virksomheter-foretak-og-regnskap/skatt-for-naeringsvirksomhet/artikler/verdsetting-av-unoterte-selskaper/_/attachment/inline/2dfe00a0-9082-41c4-b35e-d3401974b074:c5f351dd34888e134a97ea5d1c4a057b23e24aea/RAPP2022-31.pdf
- Thoresen and others: https://mariusring.github.io/web/TRNE_awealthtaxatwork.pdf
- HMRC tax gaps, other taxes: https://www.gov.uk/government/statistics/measuring-tax-gaps/6-tax-gaps-other-taxes and annex https://www.gov.uk/government/statistics/measuring-tax-gaps-methodological-annex/6-tax-gaps-other-taxes
- Professional Adviser (2012): https://www.professionaladviser.com/news/2205830/hmrc-netted-gbp90m-iht-challenges
- Property Investor Today (2026): https://www.propertyinvestortoday.co.uk/breaking-news/2026/04/property-values-increasingly-questioned-in-iht-crackdown-by-hrmc/
- NAO (2025): https://www.nao.org.uk/wp-content/uploads/2025/05/collecting-the-right-tax-from-wealthy-individuals.pdf
- ONS quality and methods guide: https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/methodologies/householdtotalwealthingreatbritainqualityandmethodsguide
- Daly, Hughson and Loutzenhiser: https://law.ox.ac.uk/sites/default/files/migrated/dalyhughsonloutzenhiser_final_submission.pdf
- MSCI (2025): https://www.msci.com/downloads/documents/indexes/real-assets/real-estate-methodology-documents/index-and-methodology-review/Valuation-and-Sale-Price_Comparison-2025.pdf
- Cannon and Cole: https://mpra.ub.uni-muenchen.de/52621/1/MPRA_paper_52621.pdf
- ECB WP 2328: https://ecb.europa.eu/pub/pdf/scpwps/ecb.wp2328~119c7e6f25.sk.pdf
- Bergolo and others (Uruguay): https://docs.iza.org/dp12286.pdf
- Kastoryano (Netherlands): https://docs.iza.org/dp17722.pdf
- Durán-Cabré and others: https://ieb.ub.edu/wp-content/uploads/2019/05/2019-IEB-WorkingPaper-04.pdf and https://ieb.ub.edu/publication/2015-15-wealth-tax-enforcement-the-role-of-tax-and-institutional-design/
- Held: `literature/Fiscal Studies - 2021 - Advani - Behavioural responses to a wealth tax.pdf`
