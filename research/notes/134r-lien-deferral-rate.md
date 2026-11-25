# 134r: Evidence and a register row for the lien deferral rate

**Status.** Research note complete, 2026-11-22. Brief `docs/briefs/134r-lien-deferral-rate.md`. No register, code, run or manifest changes. The proposed row is for the author's decision only.

## Answer in brief

There is no directly comparable UK market rate for a tax liability voluntarily deferred and secured against a pension entitlement. The evidence therefore supports a benchmark and a sensitivity range, not an empirically estimated contractual rate.

The strongest starting point is HM Treasury's **2.00% real risk-free discount rate** in the October 2026 Green Book supplementary guidance. HM Treasury triangulates this with inflation-adjusted 10-, 20- and 40-year gilt yields of around 2% in June 2026. This is a closer comparator than HMRC's late-payment rate. The latter is a nominal enforcement rate with an explicit prompt-payment incentive.

The Green Book's **3.00% real social time-preference rate** is a useful upper comparator, but it is not a loan rate: it adds a 1 percentage-point systematic risk premium to the 2% risk-free rate. A 0% case remains useful as an explicit policy sensitivity, not as an evidence-based market rate.

**Provisional proposal:** 0% / 2% / 3% real per year (low / central / high), all marked **(J)** because transferring these benchmarks to the WDT lien is a policy judgement. The previous conversational suggestion of 4% as the high value is not retained: no sufficiently close evidence supports that as the register's high. It could be retained as a separate outer stress test if the author wants one.

## 1. What rate is being priced?

The model's `r_def` accrues on an unpaid WDT balance carried as a lien. In 132c the balance is a receivable of the public ledger, settled later from non-pension classes and then (once) from the pension. The same `r_def` is also used by the Route B lien.

Three concepts must stay separate:

1. **A contractual/administrative charge to the taxpayer:** the amount added to the deferred liability.
2. **The state's financing or opportunity cost:** the return forgone while the public sector carries a receivable rather than cash.
3. **Social time preference:** the rate used to compare social costs and benefits at different dates.

They can inform one another but are not interchangeable. HMRC late-payment interest is not a neutral financing benchmark; the Green Book STPR is not a contractual debt rate.

The note treats `r_def` as a **real annual rate**, consistent with the model's real-value accounting. If the implementation instead accrues on nominal balances, the model would need a consistent nominal-rate and inflation convention. Do not add inflation to a real rate.

## 2. UK comparators

Figures below are from official pages or documents read on 2026-11-22. Unless stated otherwise, the sources are UK sources. Nominal rates are labelled as such; no nominal comparator is silently treated as real.

| Comparator | Quantity and figure | Period / basis | What it measures, and relevance |
|---|---|---|---|
| HMRC late-payment interest | 7.75% late-payment; 2.75% repayment | Main taxes, from 9 Jan 2026; nominal. From 24 Nov 2026 the published rates become 8.00% and 3.00% respectively | Statutory rates set at Bank Rate +4 percentage points for late payment and Bank Rate -1 point for repayment (0.5% floor). The late rate deliberately encourages prompt payment and compensates for late payment; repayment interest compensates taxpayers for overpayments. It is a useful tax-administration comparator, but too punitive and too asymmetric to transfer directly to a voluntarily deferred, secured WDT liability. HMRC's 6 Nov 2026 notice says Bank Rate rose to 4.00% on 5 Nov; the 8%/3% change takes effect 24 Nov. |
| IHT annual instalments | Up to 10 equal annual instalments for qualifying assets; no interest on the first instalment unless late; later instalments normally bear interest on the outstanding tax balance | Statutory instalment arrangement; HMRC guidance current on 22 Nov 2026 | The closest UK institutional analogy: tax is deferred because an asset may take time to sell. It establishes that the state normally charges interest on later instalments, but does not supply a universal contractual rate in the instalment guidance. New assets qualifying for Agricultural Relief or Business Relief from 6 Apr 2026 have interest-free instalments on the outstanding balance. This exception shows that zero interest can be a deliberate policy choice, not a neutral financing rate. |
| CGT statutory deferrals and instalments | TCGA 1992 s280 can apply where sale consideration is payable by instalments over more than 18 months; s281 allows 10 yearly instalments for certain gifts/deemed disposals; s279 covers qualifying delayed remittances | Statutory cases, not a general payment deferral for ordinary UK residential-property CGT | HMRC's manual identifies these distinct routes but does not establish one general rate applicable to all of them on the page read. Ordinary UK residential-property CGT is generally reportable and payable within 60 days. The brief's proposed search for a general CGT-on-UK-property deferral rate did not produce a comparable benchmark. |
| HM Treasury risk-free discount rate | 2.00% real | October 2026 Green Book supplementary guidance; 10-, 20- and 40-year real gilt yields around 2% in June 2026 | Best available central benchmark. HMT derives a 1.875% Ramsey estimate (0.5% pure time preference + 1.875% wealth effect - 0.5% rare-disaster term) and rounds/triangulates to 2.00%, using expert, international and social-opportunity-cost evidence including real gilt yields. It is a risk-free social discount benchmark, not specifically the Treasury's marginal borrowing cost or a price for a pension-secured lien. |
| HM Treasury social time-preference rate (STPR) | 3.00% real for years 1–30; 2.50% for years 31–75; 2.25% for years 76–125 | October 2026 Green Book; real forward discount schedule | The 3% headline rate is the 2% risk-free rate plus a 1% systematic risk premium. It measures social time preference for appraisal, not a taxpayer loan rate. The declining later schedule is expressed as forward rates. It is a useful outer comparator, but should not be copied mechanically into a contractual lien. |
| Student loans | 2026/27 RPI is 4.1%; Plan 5 normally charges RPI (4.1%); Plan 2 varies from RPI to RPI+3%, with a 6% cap; postgraduate loans normally RPI+3%, also capped at 6% | 1 Sep 2026–31 Aug 2027; nominal rates linked to RPI | Government charges interest on long-lived statutory liabilities, but student loans are unsecured and income-contingent, with cancellation and distributional features. They are not a close pricing comparator. The 4.1% RPI figure is nominal inflation, not a 4.1% real rate. |
| Owner-occupier mortgages | 2-year fixed at 75% LTV: 5.39%; 5-year fixed at 75% LTV: 5.19% | Bank of England quoted rates, 31 Oct 2026; nominal | Illustrates household borrowing costs and the private cost of accessing liquidity. It includes lender funding costs, credit risk, capital, operating costs and margin; it is not the state's cost of carrying a pension-secured receivable. It is an upper-side context, not a direct input. |

### 2.1 Sources

1. HMRC, [Interest rates for late and early payments](https://www.gov.uk/government/publications/rates-and-allowances-hmrc-interest-rates-for-late-and-early-payments/rates-and-allowances-hmrc-interest-rates), updated 6 Nov 2026. The table gives the tax-specific historical rates and the effective date of the 24 Nov change.
2. HMRC, [Interest rates update](https://www.gov.uk/government/news/hmrc-interest-rates-update--2), 6 Nov 2026. Explains the Bank Rate move to 4.00%, the +4/-1 formula and the prompt-payment rationale.
3. HMRC, [Pay your Inheritance Tax bill in yearly instalments](https://www.gov.uk/paying-inheritance-tax/yearly-instalments), accessed 22 Nov 2026. Covers the 10-year arrangement, interest treatment and 2026 Agricultural/Business Relief exception.
4. HMRC, [CG18601: paying and recovering tax in exceptional cases](https://www.gov.uk/hmrc-internal-manuals/capital-gains-manual/cg18601), updated 19 Nov 2026. Identifies TCGA 1992 ss279–281 and the statutory cases.
5. HMRC, [Reporting and paying Capital Gains Tax](https://www.gov.uk/capital-gains-tax/reporting-and-paying-capital-gains-tax), accessed 22 Nov 2026. Ordinary UK residential-property CGT payment deadline.
6. HM Treasury, [Green Book 2026](https://www.gov.uk/government/publications/the-green-book--2/the-green-book-2026), October 2026. The real STPR schedule.
7. HM Treasury, [Green Book supplementary guidance: Discounting](https://assets.publishing.service.gov.uk/media/6ae0b34016428df537606216/Green_Book_supplementary_guidance_-_discounting.pdf), October 2026, especially §§2.1–2.15. OGL v3. Gives the 2% risk-free rate, 1% systematic risk premium, 3% STPR and the June 2026 real-gilt comparison.
8. UK Debt Management Office, [Quarterly Review, April–June 2026](https://www.dmo.gov.uk/media/21jhek14/apr-jun-2026b.pdf), accessed 22 Nov 2026. Official gilt-market context; the HMT supplementary guidance is the clearer source for the 2% real-yield statement.
9. Student Loans Company / Department for Education, [Student loans: terms and conditions 2026 to 2027](https://www.gov.uk/government/publications/student-loans-a-guide-to-terms-and-conditions/student-loans-a-guide-to-terms-and-conditions-2026-to-2027), accessed 22 Nov 2026.
10. Department for Education, [Student loan interest-rate announcement](https://www.gov.uk/government/news/student-loans-interest-rates-and-repayment-threshold-announcement--7), 10 Aug 2026. Sets the 4.1% RPI basis and Plan 2/3 cap.
11. Bank of England, [Quoted household interest rates database](https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp?CSVF=TT&DAT=RNG&FD=1&FM=Jan&FNY=Y&FY=2026&Filter=N&FromSeries=1&SeriesCodes=IUMBV34%2CIUMBV42%2CIUMB482&TD=6&TM=Nov&TY=2026&ToSeries=50&Travel=NIxAZxSUx&UsingCodes=Y&VPD=Y&html.x=66&html.y=26&title=Quoted+rates), series IUMBV34 and IUMBV42, October 2026 observations.

## 3. Proposed register row (not entered)

The register's current D14 note says the Route B deferral rate was omitted because lien mode was unused under the sale route. Since 132c now uses `r_def` for the pension-secured lien, that rationale no longer covers the household arm. This row should be given a distinct identifier after checking the register's D12/D15 allocation; **I-D15a is a placeholder**, not a confirmed ID.

| ID | Input | Unit | Low | Central | High | How the range was set | Source | Licence and access | Coverage | In repo | Confidence |
|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| I-D15a (provisional) | Real annual interest rate on deferred WDT lien balances (`r_def`; Route B and pension-secured household lien) | % real per year | 0.00 | 2.00 | 3.00 | **(J) throughout.** Low is the explicit interest-free policy/legacy case, not an observed market rate. Central is HMT's 2.00% real risk-free discount benchmark, corroborated by real gilt yields around 2% in June 2026; transferring it to the WDT receivable is a judgement. High is the 3.00% Green Book STPR, including its 1 percentage-point systematic risk premium; this is an outer social-discount comparator, not a directly observed lien price. | HM Treasury Green Book supplementary guidance §§2.1–2.15; HMRC IHT instalment guidance; HMRC late-payment rates as contextual comparator | HMT supplementary guidance: OGL v3. HMRC pages: Crown copyright / GOV.UK terms; cite only unless licence checked. | UK public-sector discounting, statutory tax deferral and household borrowing comparators; no direct observed WDT-like lien market | no | Medium: central benchmark is well sourced; transfer to a WDT contractual rate and both ends of the range are judgement |

**Model treatment:** apply `r_def` as a real annual accrual to the outstanding lien balance; accrued interest increases the public-ledger receivable but is not cash received until settlement. Keep new deferred principal, interest accrued, cash settled and any write-off separately identifiable. Do not count accrual as current-year cash receipts.

## 4. Scale of the choice

For a balance carried for 29 years with no interim payments, annual compounding gives:

| Real annual rate | Balance per £1 initially deferred after 29 years |
|---:|---:|
| 0% | £1.00 |
| 1% | £1.33 |
| 2% | £1.78 |
| 3% | £2.36 |
| 4% | £3.12 |

This illustrates why zero is a substantive subsidy choice. It does not estimate the aggregate WDT revenue effect; no model rerun was in scope.

## 5. What the author must rule

1. **Pricing principle:** should the lien charge the state's risk-free financing/opportunity-cost benchmark (proposed central 2%), or should it use a broader social time-preference benchmark (3%)? The latter includes a systematic risk premium that may not belong in a secured tax receivable.
2. **Policy floor:** retain 0% as an explicit interest-free policy sensitivity, or exclude it from the register range.
3. **Accounting:** confirm that accrued interest increases the public receivable but is not treated as cash revenue until settlement. This is consistent with the 132c ledger separation.
4. **Scope:** confirm that one `r_def` applies to both Route B and the pension-secured household lien. If the policy differs, separate parameters are required.

## 6. Limitations and exclusions

- No UK source found that prices a voluntary, long-term tax deferral secured specifically against pension wealth.
- HMRC late-payment interest is a statutory compliance charge, not a risk-free lending rate.
- The IHT instalment arrangement is the closest institutional comparator, but the guidance page does not state one universal interest rate for all instalments; it points to HMRC's applicable interest rules.
- The CGT manual confirms special statutory instalment/deferment routes, not a general CGT-on-UK-property payment deferral. Ordinary residential-property CGT is normally payable within 60 days.
- Student-loan rates and mortgage rates are nominal and structurally different. They are context only.
- No lifetime-mortgage/equity-release rate is proposed: the previous conversational figure was not verified against a primary source and is omitted.
- The proposed values are scenario judgements, not a fitted probability distribution or a revenue-optimised choice.
