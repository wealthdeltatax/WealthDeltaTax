# 024r derivations

Method behind the computed rows in `model-specs/inputs-added/hh.md`. Accessed 2026-11-17. Run with `python3 -I`.

## Quintile gross income (I-H3a to I-H3e)
Gross income = average total tax / (total tax % of gross income), from Civitas Table 4.1 and Figure 3.3 (ONS FYE 2023 quintiles): bottom £8,829/0.379 = £23,295; 2nd £38,663; 3rd £53,192; 4th £73,698; top £141,350. Range is the rounding half-step (0.05 points) of the percentage.

## Real returns (I-H6)
Held JST Release 6, UK rows (`eq_tr`, `housing_tr`, `bond_tr`, `cpi`). Real return = (1 + nominal total return) / (cpi_t / cpi_{{t-1}}) - 1. Windows 1871-2020, 1950-2020 (central), 1980-2020, 2000-2020; mean, sample standard deviation and Pearson correlation of annual real returns. Housing starts 1896. Equity and housing correlation is -0.14 (1950-2020) and ranges -0.14 to 0.05; equity and bonds 0.37 (range -0.53 to 0.47); housing and bonds -0.17 (range -0.17 to 0.15).

## Per pound of wealth (I-H4)
Additional-rate income tax £103.0bn (HMRC 2023-24) over Round 8 wealth: D9 + D10 £8,152bn (1.26%), D10 £5,523bn (1.87%), D10 less private pension £2,010bn = £3,513bn (2.93%). VAT: top-quintile VAT 3.6% of gross £141,350 = £5,089 over mean top-fifth net wealth £2,135,600 = 0.24%.

## Spending ratios (I-H7)
12,300/14,700 = 0.837; 58,700/2,135,600 = 0.0275; 12,300/10,500 = 1.17; 58,700/86,000 = 0.68.

## Risk aversion (I-H5)
Published values from Groom and Maddison (WP121); I-H5b and I-H5e bounds are plus or minus two standard errors (0.047 and 0.706).
