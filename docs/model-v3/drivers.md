# Model v3: driver table (brief 011g, stage A2, passed 2026-11-16)

Purpose: say what moves the three headlines before the input register (012r) is written, so research effort goes to the inputs that matter. Pen and paper only: no code was run for this file. Numbers come from `docs/model-audit/synthesis.md` (v2 scratch runs, which rank and size but are not results) and are marked where they are not.

## 1. The revenue identity
For the individual tax, year t, as a share of GDP:

M1a ≈ ε · g · ω - refunds

- **ω** = taxable base over GDP = (net wealth of payers) / GDP. It is total household wealth over GDP times the share held at or above W_min. v2 at W_min of about £113k: about half of adults, 93% of wealth.
- **g** = mean real accrued gain rate on that base in year t. In loss years it is negative and refunds are paid, capped by tax paid to date (the papers' rule), so the identity is not linear in g.
- **ε** = wealth-weighted effective rate on gains, set by the schedule (family: logistic in ln W, v2's `logistic_ln_ref` runs 4% to 90%).
- **refunds** = refunds paid in loss years.

The other lines: M1b = corporate levy (v2 post-fill about 2.8% of GDP, against corporation tax 3.37); M1c = fund income minus retention (v2 about -0.6); M1d = retired receipts (8.11% of GDP at 2025-26, seven lines; the 8.27 of earlier drafts counted the stamp-duty row and its shares sub-row twice, corrected 2026-11-17 by the tier 1 tornado, `tornado.md`). Closure: M1a + M1b + M1c covers M1d, staged by the trigger in `metrics.md` (M1e).

**Correction.** In the 2026-11-16 chat review I gave an illustrative 3% of GDP at a 20% effective rate. That figure was my guess, not sourced from the repo, and it does not fit v2: post-fill WDT is 7.34% of GDP for `logistic_ln_ref` (`synthesis.md` section 10). Either v2's wealth-to-GDP ratio, its gain rate or its effective rate is higher than my guess. Backing out which one is the first job of 012r's tier 1 (section 4).

## 2. Driver table
Kind: **lever** = the author chooses it (swept, not sampled); **exo** = the world decides it (sampled, two levels, see `metrics.md`).

| # | Driver | Enters as | Moves | Kind | What the repo has |
|---|---|---|---|---|---|
| D1 | Return path and loss years | g, refunds, fill years | M1, M1a, M1c, P1, P3, P4 | exo, level 1 (risk) | JST R6 (`jst_r6.json`); v2 on 117 UK windows: relief P10 to P90 about 3% to 15% of GDP, so the return history alone moves closure from 42% to 55% of windows |
| D2 | Rate schedule (3 parameters) | ε | M1a, M2, M3, M4 | lever | v2 table, `synthesis.md` section 8: 3.75% to 7.16% net revenue across eight schedules |
| D3 | Threshold W_min | ω, number of payers, M2b | all | lever | half the median house price (decided); v2 about £113k; sensitivity at the full median in the v2 parameter file |
| D4 | Wealth-to-GDP ratio and the tail | ω | M1a, M2 | exo, level 2 | WAS 2016-18 plus Rich List in v2; latest wave not held; no single ratio recorded in the repo |
| D5 | Behavioural response (avoidance, migration, valuation understatement) | shrinks ω, shifts declared alpha | M1a, M7 | exo, level 2 | Norway leakage in the Project Map only; no range yet |
| D6 | Retired receipts and who pays them | M1d, M4 | M1, M4a, M4b | exo, level 2 | totals from IFS (8.11%); incidence by income decile not held (`synthesis.md` section 9, 3a) |
| D7 | Corporate levy base | M1b | M1 | exo, level 2 | v2 2.77% to 2.88% of GDP; its own line |
| D8 | Reserve rule (3 times trailing mean refund) | fill years, when retirement can start | P1, P3, P5 | lever (set by the papers) | v2 medians 3 and 7 years |
| D9 | Income by wealth, liquid assets | M2b, M2c, M4b | burden and savings by band | exo, level 2 | v2 placeholders only (`income_by_wealth`) |
| D10 | Capitalisation of retired property taxes (S1) | wealth values, payer count | ω, M2, M4 | exo, level 2 | nothing |
| D11 | Discount schedule | M3 only | M3 | fixed schedule plus sensitivity | Green Book, to be confirmed by research |

## 3. Hypothesis to test, not a result
Expected order of influence on M1: D1 (return history), then D2 and D3 (levers, so shown as separate lines per named schedule, not as uncertainty), then D4 and D5 together (the size of the base after behaviour), then D6, D7 and D10. D8 and D11 are second order. The synthesis already points at D1: the spread in closure "is driven by the return history".

## 4. How this changes 012r (stage B)
1. **Tier 1, sourced fully** (low, central, high, unit, citation, licence): D4, D5, D6, D9, D10, and the loss-year and return inputs D1. These decide whether the headlines are credible.
2. **Tier 2, one documented range** with a source or a stated reason, no further sourcing: D7, D8, D11, the corporate levy base.
3. **Levers D2 and D3 are not research inputs.** They are the named schedules and the threshold rule, set in stage C and D.
4. **Tornado before stage C.** When 012r delivers tier 1, run the identity one input at a time over low and high on a sheet of paper or in the research lane's notes; the result is `docs/model-v3/tornado.md`. Any tier 2 input that moves M1 by less than 0.5 points of GDP stays at its single range (the 0.5 is confirmed, 2026-11-16). The tornado also fixes the first number to back out: ε · g · ω against v2's 7.34%.
5. **Add to the input list**, from the A2 decisions: liquid assets and income by wealth band (M2b, M2c), the specifications of the reform-in-place benchmarks (M8), the house-price response to retiring stamp duty and council tax (S1), and the public balance sheet path (P6).

## 5. The sustainability test, read correctly
v2 shows revenue falling from 9.87% of GDP at the fill year to 5.39% over 100 years for `gain_ladder`. Before reading that as WDT failing as a revenue source, split it. Part may be the fund absorbing returns that the tax takes out of private wealth growth, which is public wealth rising and not revenue failing. P4 therefore reports with P6, the fund's assets as a share of GDP at years 10, 25, 50 and 100. A falling M1 with a rising P6 is a different finding from a falling M1 with a flat P6.

## Note, 2026-11-17: which mean return the revenue identity uses (author)
The annual tax falls on expected annual gain, so the revenue identity M1a = ε · g · ω takes the arithmetic mean return for g (register I-D1a is geometric, 4.42%; the arithmetic mean is about 4.76% at a standard deviation of 8.2%, v2 used 4.74%). Wealth paths still compound at the geometric rate. Stage C writes this into the architecture and the register carries both figures.
