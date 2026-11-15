# D5: HMRC Corporate Taxes against OECD 1200 (UK), 17 Oct 2026

Source: HMRC, Annual UK Corporation Tax Statistics 2025, Table 1A (receipts, £m, fiscal years). Table 2A (liabilities by accounting year) is the same set on a liability basis and is not used for the target. CSV: `hmrc_corporate_taxes_table1A.csv`.

## HMRC receipts, £m

| Fiscal year | Onshore + offshore CT | Bank levy | Bank surcharge | RPDT | EPL | EGL | All Corporate Taxes | All / CT |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019-20 | 61,565 | 2,472 | 1,988 | | | | 66,025 | 1.072 |
| 2020-21 | 50,486 | 2,343 | 1,409 | | | | 54,238 | 1.074 |
| 2021-22 | 63,745 | 1,469 | 2,335 | | | | 67,548 | 1.060 |
| 2022-23 | 77,894 | 1,332 | 2,580 | 157 | 2,632 | | 84,595 | 1.086 |
| 2023-24 | 85,637 | 1,428 | 1,446 | 103 | 3,587 | 1,473 | 93,675 | 1.094 |
| 2024-25 | 91,159 | 1,320 | 974 | 102 | 2,857 | 749 | 97,161 | 1.066 |

The components sum to All Corporate Taxes within £1m rounding. Over 2020-21 to 2024-25 corporation tax proper is 93.0% of All Corporate Taxes on average (All / CT = 1.075).

## Reconciliation against OECD 1200 (UK file `2a`, 17 Oct)

The OECD file holds percent of GDP only (unit PT_B1GQ, no sterling levels). To compare in sterling, OECD % x UK nominal GDP (calendar year; IMF series via FRED NGDPXDCGBA: 2019 2,252,961; 2020 2,124,720; 2021 2,322,652; 2022 2,580,949; 2023 2,752,164; 2024 2,890,254, £m) gives an implied OECD 1200 amount, set against HMRC receipts for the fiscal year starting in the same year. CSV: `d5_oecd_hmrc_check.csv`.

| Year | OECD 1200 % GDP | OECD implied £m | HMRC All Corporate Taxes (FY t/t+1) | All / OECD | HMRC corporation tax proper | CT / OECD |
|:---|---:|---:|---:|---:|---:|---:|
| 2019 | 2.32 | 52,370 | 66,025 | 1.26 | 61,565 | 1.18 |
| 2020 | 2.38 | 50,660 | 54,238 | 1.07 | 50,486 | 1.00 |
| 2021 | 2.94 | 68,381 | 67,548 | 0.99 | 63,745 | 0.93 |
| 2022 | 3.20 | 82,710 | 84,595 | 1.02 | 77,894 | 0.94 |
| 2023 | 3.38 | 92,916 | 93,675 | 1.01 | 85,637 | 0.92 |
| 2024 | 3.47 | 100,392 | 97,161 | 0.97 | 91,159 | 0.91 |

- **2020-24 totals:** OECD implied £395,059m against HMRC All Corporate Taxes £397,217m (ratio 1.006). Corporation tax proper is £368,921m (0.93 of the OECD amount). So over the five years the 3.08% target equals HMRC All Corporate Taxes to within 0.6%, and corporation tax proper is about 7% short of it.
- **Year by year:** 2021-24 are within 3% of All Corporate Taxes; 2020 is 7% high on the HMRC side. 2019 is not reconciled (HMRC 26% above the OECD amount); not investigated, and outside the 2020-24 window.
- **Basis caveats:** the alignment (OECD calendar year t against HMRC fiscal year t to t+1, calendar GDP) is my reading, tested only by how closely it fits; HMRC receipts are cash, the OECD series may include accrual adjustments (the file also carries cash and accrual totals, not used here). Which HMRC items OECD books under 1200 (for example whether the bank levy sits elsewhere) is not shown by the file.

## Consequence for the levy target

- The 3.08% target is, on the five-year totals, all corporate taxes in HMRC's sense, so the levy would replace the bank surcharge, EPL, EGL and RPDT as well as corporation tax. If the intent is corporation tax proper, the equivalent is 3.08% x 0.930 = 2.86% of GDP.
- Decision made 17 Oct: 3.08% (all corporate taxes). Patch `patch_NNN_ct_retire_308.py` applied. The 2.86% corporation-tax-proper variant and the 3.47% latest-year sensitivity are not in the TOML.
