---
id: OA-20261127-02
type: web-research
question: How are reserves sized against the outflows or claims they are intended to cover, and what happens when the target is breached?
in-reply-to: 185r
supersedes: none
repo-commit: ea449fdc
sources: https://www.fdic.gov/board/memorandum-notice-designated-reserve-ratio-2025-october-17-2024 (read 2026-11-27); https://www.ssa.gov/oact/TR/2026/II_B_cyoper.html (read 2026-11-27); https://www.osfi-bsif.gc.ca/sites/default/files/documents/cpp32-rev-ed-en.pdf (read 2026-11-27); https://www.bankofbotswana.bw/content/reserve-management-guidelines (read 2026-11-27); https://www.gao.gov/assets/hrd-88-55.pdf (read 2026-11-27)
verified: unverified
confidence: medium
status: new
---

## Answer

The clearest outflow-multiple comparators are funded pension schemes and unemployment insurance solvency metrics: Canada's base CPP is projected at roughly 9.7 to 10.4 times the following year's expenditure over 2025-30, while the US UI high-cost multiple standard is 1.5 times a historically high benefit-cost ratio. Social Security's OASDI reserve was 151% of estimated next-year cost at end-2025 (about 1.51 years of cost). Botswana uses six months of import cover for its liquid foreign-exchange reserve. FDIC uses a reserve ratio against insured deposits, not months of claims, and restores the ratio through assessments when below the statutory minimum. These are not interchangeable: insurance claims are contingent and shock-sensitive; pensions and tax refunds are scheduled/earned outflows; import cover is a liquidity stress metric.

## Evidence

All sources were read 2026-11-27. Ratios expressed as assets divided by one year's expenditure are described as years of annual outflow only as a derived interpretation; they are not actuarial duration or a promise that the assets alone fund the scheme for that many years.

| Arrangement | Reserve sizing rule | Figure and status | Breach / interpretation | Source / location |
|---|---|---|---|---|
| Canada Pension Plan (base CPP) | Actuarial valuation projects assets relative to following year's expenditures. It is a partially funded pension plan, not a segregated one-year liquidity buffer. | 9.7 times following-year expenditure in 2025, 10.4 in 2030, 14.1 in 2050 and 20.7 in 2100 (reported, read 2026-11-27, 32nd Actuarial Report §5.1, PDF pp.29-30; Table 11). Interpreted as 9.7-10.4 years of one-year expenditure in 2025-30 (derived). | Statutory contribution rate is 9.9%; actuarial report calculates a minimum contribution rate to sustain the base plan. Not an immediate claims-payable cash reserve. | https://www.osfi-bsif.gc.ca/sites/default/files/documents/cpp32-rev-ed-en.pdf |
| US Social Security OASDI | Trust fund reserves measured against estimated next-year programme cost, not a fixed statutory target multiple. | End-2025 reserves were 151% of estimated 2026 cost (reported, read 2026-11-27, 2026 Trustees Report §II.B, “Trust fund reserves”; about 1.51 years of that annual cost, derived). | Reserves are drawn when income including interest is below costs. Trustees project depletion under current law; after depletion, ongoing income would cover less than scheduled benefits. | https://www.ssa.gov/oact/TR/2026/II_B_cyoper.html |
| US unemployment insurance trust funds | High Cost Multiple (HCM) compares reserve ratio with the system's historically highest 12-month benefit-cost ratio. It is a stress benchmark rather than a forecast of ordinary claims. | Generally accepted HCM adequacy standard is 1.5 and above (reported, read 2026-11-27, GAO/HRD-88-55, Appendix IV, p.90). | Metric anchors reserves to a high-cost year. More relevant as a stress buffer comparator than a multiple of average annual benefits. Source is old (1988); current state-by-state compliance not checked. | https://www.gao.gov/assets/hrd-88-55.pdf |
| Botswana foreign-exchange liquidity portfolio | Liquid tranche maintained at benchmark measured in months of imports; foreign-exchange reserves above this portfolio transfer to long-term Pula Fund. | Six months of import cover (reported, read 2026-11-27, Bank of Botswana “Reserve Management Guidelines”, lines 23-26). | Benchmark reviewed from time to time. Covers short-term trade and capital-account requirements, not a legally certain household claim. | https://www.bankofbotswana.bw/content/reserve-management-guidelines |
| US FDIC Deposit Insurance Fund | Designated reserve ratio is fund balance / estimated insured deposits, not expected annual payouts. 2% is a long-range minimum goal; 1.35% is statutory minimum. | DRR 2.0%, statutory floor 1.35% (reported, read 2026-11-27, FDIC 2025 DRR memo, pp.1-2). | Ratio fell to 1.30% in June 2020; FDIC adopted a restoration plan to reach at least 1.35% within eight years, with assessments increased in 2022. It was above the statutory minimum by June 2025. | https://www.fdic.gov/board/memorandum-notice-designated-reserve-ratio-2025-october-17-2024 |
| Chile PRF / ESSF | PRF earmarked for future minimum-pension commitments; ESSF is broader fiscal stabilisation fund. No explicit months-of-claims or years-of-outflow multiple found. | PRF annual contribution linked to effective surplus, capped at 0.5% of previous-year GDP (reported, read 2026-11-27, Ministry FAQ, “What are the contributions rules?”). Not an outflow multiple. | ESSF can finance a fiscal deficit; PRF withdrawals now require a minister-defined rule intended to provide stable, predictable withdrawals and preserve real capital. | https://www.hacienda.cl/english/work-areas/international-finance/sovereign-wealth-funds/frequently-asked-questions |
| Alaska, Alberta and New Zealand funds | Not short-term claims buffers. Alaska's POMV constrains annual withdrawals; Alberta is a long-term savings endowment; NZSF uses a 40-year funding formula. No comparable claims-cover multiple found in reviewed sources. | Alaska draw cap 5% of average market value (reported, read 2026-11-27, APFC “Percent of Market Value”); NZSF horizon 40 years (reported, read 2026-11-27, Act 2001 s.43). | Not directly comparable to a short reserve whose breach is a hard failure. | https://apfc.org/the-fund/ ; https://www.alberta.ca/heritage-savings-trust-fund ; https://www.legislation.govt.nz/act/public/2001/84/en/latest/ |

### What is weak or conflicting

- CPP's asset/expenditure ratio is a whole-plan actuarial funding metric. It includes assets and future contributions; it is not a recommended cash buffer.
- OASDI's ratio is a snapshot against one year of estimated cost. The programme has continuing payroll-tax income; the reserve does not need to fund all future benefits unaided.
- GAO's HCM benchmark is old and not evidence of today's typical UI reserve. It is a clearly defined stress-multiple methodology.
- FDIC's denominator is insured deposits, not expected claims or annual payouts. It is risk-based and intended to support a positive balance through banking crises.
- WDT refunds appear more certain than bank-failure insurance claims once assessed losses are established. But aggregate refund timing and amount may be correlated with asset-price downturns, when fund investment values may also fall.

## Relevance to our design

For the **short reserve**, the evidence supports testing a range of denominators rather than importing one fund multiple: (a) a multiple of expected annual refunds, (b) a high-cost / stress-year refund multiple analogous to UI's HCM, and (c) a months-of-outflow target analogous to a liquidity portfolio. The relevant comparison is not CPP's 9.7-10.4 years, which is a pension-plan funding ratio, but the difference between a predictable accrued liability and a contingent stress claim. For the **long reserve**, CPP and NZSF illustrate long-horizon actuarial funding rather than a fixed cash buffer. The **cap** can be assessed separately: FDIC's 2% reserve ratio is a target against exposure, not a cap on fund assets.

## What I could not check

- Current UI trust-fund HCM values across US states; the GAO benchmark source is from 1988.
- A directly comparable national refund reserve or tax-loss refund fund with legally guaranteed prompt payment.
- Current detailed OASDI actuarial ratio tables beyond the 2026 report extract cited.
- Chile's current PRF withdrawal formula as implemented after the 2024 amendment.

## Suggested next step

Calculate the WDT short reserve against both expected annual refund flow and a historically adverse refund year, then label the ratio as a claims-coverage metric. Do not compare it directly with CPP's assets/expenditure ratio without stating the structural difference.

## Proposed references (not added to bibliography)

- FDIC, “Designated Reserve Ratio for 2025” (17 October 2024), https://www.fdic.gov/board/memorandum-notice-designated-reserve-ratio-2025-october-17-2024
- 2026 OASDI Trustees Report §II.B, https://www.ssa.gov/oact/TR/2026/II_B_cyoper.html
- OSFI, 32nd Actuarial Report on the Canada Pension Plan §5.1, https://www.osfi-bsif.gc.ca/sites/default/files/documents/cpp32-rev-ed-en.pdf
- GAO, Unemployment Insurance Trust Fund Reserves Inadequate, GAO/HRD-88-55, Appendix IV, https://www.gao.gov/assets/hrd-88-55.pdf
- Bank of Botswana, Reserve Management Guidelines, https://www.bankofbotswana.bw/content/reserve-management-guidelines
