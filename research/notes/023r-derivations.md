# 023r derivations

Method behind the computed rows in `model-specs/inputs-added/tax.md`. Accessed 2026-11-17. Run with `python3 -I`.

## Held data
- Round 8, Table 2.2 (April 2020 to March 2022): decile aggregates of total, net property, net financial, physical and private pension wealth; column K (Round 8) and column J (Round 7). Groups D4-5, D6-7, D8-9, D10.
- IFS sheet 'Composition (cash)' and '% GDP (cash)', columns 2024-25, 2025-26, 2026-27 (AV to AX). 2025-26 reads income tax £292.4bn, NICs £180.2bn, VAT £171.6bn, corporation tax £93.0bn (3.37% of GDP, the I-D7b cell), CGT £21.2bn, IHT £7.4bn.

## Formulas
- Gain-bearing wealth = net property + net financial (physical left out). All deciles £7,376bn; D10 £3,181bn.
- Realisation rate = realised gains / gain-bearing wealth: 127/7,376 = 1.7% (2024-25); 69.8/7,376 = 0.9% (2023-24, 69.8 = 127/1.82).
- D10 realisation uses 52% or 55% of gains going to taxable income over £125,140 over D10 gain-bearing wealth. This mixes an income split with a wealth decile (judgement).
- Accrued gains D10 = D10 gain-bearing wealth x 20%, 35% or 50% (judgement, no UK series).
- Investment income: (£71.8bn + £18.3bn) over aggregate net financial wealth; D10 share low = D10 financial wealth over the total; central 70% and high 90% judgement; tax = income share x rate (35.75, 40, 45%).
- Median worker: tax 20% on pay between £12,570 and £50,270; NICs 8% on the same band; pay low £40,580 (hourly x 37.5 x 52), central £40,911, high £42,182 (weekly x 52).
- ISA/total wealth = £952bn (end 2024-25) / £13,568bn.

## Limits
GB wealth against UK income and receipts; periods differ across 2020-22, 2023-24 and 2024-25.
