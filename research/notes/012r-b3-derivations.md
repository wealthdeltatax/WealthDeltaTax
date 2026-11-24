# 012r stage B3: derivations

Method behind the computed rows in `docs/model-v3/inputs.md` (I-M6a to I-M6d, I-M6h, I-M6i, I-M6k, I-M8c, I-M8d). Inputs are the held ONS Round 8 table (`Rates Data/totalwealthtables.xlsx`, Table 2.2 decile aggregates) and the published figures named in each section. Run with `python3 -I`. Accessed 2026-11-16.

## 1. Denominators (wealth, £bn, Round 8, GB)
- Total wealth £13,568bn (Table 2.1). Adults at or above W_min = £150,000 hold 89.7%, 92.7% or 96.4% of it (I-D4c): £12,170bn, £12,578bn, £13,080bn.
- Decile aggregates, Table 2.2, April 2020 to March 2022: D4 to 5 £1,044bn, D6 to 7 £2,278bn, D8 to 9 £4,434bn, D10 £5,523bn.

## 2. IHT numerator (HMRC, tax year 2023 to 2024, S21)
- Total liabilities £7.03bn (up £0.33bn on 2022 to 2023, so about £6.70bn then).
- Estates by size, effective rate and average bill as published: £1m to £1.5m 7,770 estates at £151,000; £1.5m to £2m 2,930 at £324,000; £2m to £7.5m 3,156 at an effective 25% (average bill not published); £7.5m to £10m about 144 at £1.99m; over £10m 220 at £4.72m (the split of the combined 364 is the fetch tool's derivation from the stated 220, not read on the page).
- Known tax from the four bands with an average bill: £3.45bn (1.173 + 0.949 + 0.287 + 1.038).
- The £2m to £7.5m band: 3,156 estates times 25% times an assumed average estate. Judgement: £2.5m gives £1.97bn, £3.5m gives £2.76bn, £5.0m gives £3.94bn.
- Tax from estates of £1m or more: low £5.42bn, central £6.21bn, high £7.03bn (the £5.0m case gives £7.39bn, above the published total, so it is capped at £7.03bn).
- Residual to estates under £1m: £1.61bn, £0.82bn, nil. Assumed to sit with households in wealth D8 to 9 (judgement); D4 to 7 are assumed to pay none (judgement; estates that small are inside the nil-rate bands, which this session did not re-check).

Ratios: IHT over adults above W_min: 6.70/13,080 = 0.051%, 7.03/12,578 = 0.056%, 7.03/12,170 = 0.058%. IHT over D10 wealth: 5.42/5,523 = 0.098%, 6.21/5,523 = 0.112%, 7.03/5,523 = 0.127%. IHT over D8 to 9: 0.036%, 0.019%, 0.

Effective rate £1m to £2m, weighted by tax: (1.173 + 0.949) / (1.173/0.12 + 0.949/0.19) = 14.4%. Effective rate over £7.5m, weighted by tax: (0.287 + 1.038) / (0.287/0.23 + 1.038/0.18) = 18.9%.

## 3. CGT numerator
- Liabilities: £12.1bn in 2023 to 2024 (S35, secondary), £24.2bn in 2024 to 2025 (S34, secondary; HMRC release of 27 August 2026 not reached). Receipts basis differs: the held IFS sheet shows £19.5bn for 2024 to 2025 (an OBR Feb 2023 forecast vintage), a conflict reported in the gaps section.
- Over adults above W_min: 12.1/13,080 = 0.093%; mean 18.15/12,578 = 0.144%; 24.2/12,170 = 0.199%.
- D10 share of liabilities: low 45% (the one published figure: payers with gains of £5m or more account for 45% of the total, S36; unclear whether gains or liabilities), central 72.5% (midpoint, judgement), high 100%. Over D10: 0.45 x 12.1/5,523 = 0.099%; 0.725 x 18.15/5,523 = 0.238%; 24.2/5,523 = 0.438%.

## 4. Income tax
- Receipts 2025 to 2026: £293.2bn (held IFS/OBR sheet, forecast vintage); 2024 to 2025 £282.2bn; 2026 to 2027 £306.1bn. Over total wealth £13,568bn: 2.08%, 2.16%, 2.26%. This is all households, not payers above the threshold. No HMRC series by wealth band was found.

## 5. Property tax and land value tax
- Neidle (S40): England, residential. Combined baseline £56.717bn (council tax £45.217bn plus residential SDLT £11.5bn, an external estimate). Housing value about £8tn, land £4.433tn (55.4%). Revenue-neutral rate on land value 1.28%.
- Equivalent rate on whole property value: 56.717/8,000 = 0.709% (my calculation; 1.28% x 0.55 = 0.704%). Used as the central of I-M8d.

## 6. Zucman and the UK proposals
- No calculation beyond reading the published scenarios. Tippet and Zucman 2026 (S25): net revenue 2026 £10.41bn on £642.5bn of eligible wealth (1.62% of that wealth after the 10% avoidance haircut and the 0.2% credit).
