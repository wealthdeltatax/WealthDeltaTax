# Wealth-to-GDP and revenue decomposition (brief 090c)

**Of the fall in relief between the blocks ending in years 20 (its peak) and 100 (central run, constant 4.74% return, tm50 to tm90), consumption accounts for all of it and more: with consumption at 0 relief rises by 36.6 to 36.9 GDP-points instead of falling by 1.22 to 1.53; fixing the threshold in real terms removes 8 to 11% of the fall, the levy 0 to 0% (M1b is constant), and the tax's own drag on compounding is 35 to 36% of the log fall in wealth to GDP (year 100 index 0.62 with the tax off, 0.47 to 0.47 with it on).**

**The hypothesis is supported (rule: supported when removing consumption accounts for at least half of the fall in every schedule, wealth to GDP at year 100 is below 0.9 and the tax adds to the fall; weakened when the ratio at year 100 stays at 0.9 or above; mixed otherwise).**

**With the tax on, wealth to GDP at year 100 is 1.00 at a consumption rate of 2.67, 2.65, 2.65% (tm50, tm70, tm90); at the central 3.5% it is 0.47 to 0.47.**

Reproduce: `python -I docs/model-v3/wealth-ratio-diagnostic/wealth_ratio.py` from the repository root (seed 20261118; two runs print identical text). Central inputs; schedules tau_m 0.5, 0.7, 0.9 at k 0.5, ratio 0.5. Constant path at the arithmetic mean 4.74% unless a table says random paths; constant GDP growth 1.570%. The report recommends nothing about the feasibility rule, I-D14c or CK1.

**Early check (stop condition).** Consumption 3.5% and the tax off: wealth to GDP at year 100 is 0.62; the hypothesis's own illustration is about two thirds. It holds, so the kernel's compounding is what the hypothesis assumes.

**083c reproduction.** First year relief falls below M1d at consumption 3.5 on 083c's own constant-path schedules (k 1.0, ratio 0.5): tm50 year 13 (5 taxes retired), tm70 year 13 (5 taxes retired), tm90 year 11 (6 taxes retired); 083c: year 13 at tau_m 0.5 and 0.7, year 11 at 0.9. This brief's schedules use k 0.5 as the brief asks, and there the first year is tm50 year 13, tm70 year 13, tm90 year 13: 083c's year 11 at tau_m 0.9 comes from k 1.0 (six taxes retired, M1d 8.11), not from a difference in the kernel.


## Item 1 (A): consumption sweep, constant path at 4.74% (I-D14c: low 0.5, central 3.5, high 5)

Schedules: tau_m 0.5, 0.7, 0.9 at k 0.5, ratio 0.5. Rows are (schedule, consumption %). Years are single years; blocks are the five years ending in the year shown, in GDP-points (percent of GDP). Indexes are 1.00 in year 1.

### Aggregate wealth, real level (pounds, index to year 1) and as a share of GDP (index to year 1), items 1 and 3 (C)

| schedule | c % | real y10 | real y30 | real y100 | W/GDP y10 | W/GDP y30 | W/GDP y50 | W/GDP y100 |
|---|---|---|---|---|---|---|---|---|
| tm50 | 0 | 1.45 | 3.19 | 44.39 | 1.26 | 2.03 | 3.23 | 9.49 |
| tm50 | 0.5 | 1.39 | 2.80 | 29.72 | 1.21 | 1.78 | 2.61 | 6.36 |
| tm50 | 1.5 | 1.28 | 2.15 | 12.94 | 1.11 | 1.37 | 1.68 | 2.77 |
| tm50 | 2.5 | 1.18 | 1.65 | 5.42 | 1.02 | 1.05 | 1.07 | 1.16 |
| tm50 | 3.5 | 1.08 | 1.25 | 2.22 | 0.94 | 0.80 | 0.68 | 0.47 |
| tm50 | 5 | 0.94 | 0.82 | 0.53 | 0.82 | 0.52 | 0.33 | 0.11 |
| tm70 | 0 | 1.44 | 3.15 | 42.74 | 1.25 | 2.01 | 3.17 | 9.14 |
| tm70 | 0.5 | 1.39 | 2.77 | 28.83 | 1.20 | 1.76 | 2.56 | 6.17 |
| tm70 | 1.5 | 1.28 | 2.13 | 12.69 | 1.11 | 1.35 | 1.66 | 2.71 |
| tm70 | 2.5 | 1.17 | 1.63 | 5.35 | 1.02 | 1.04 | 1.06 | 1.14 |
| tm70 | 3.5 | 1.08 | 1.24 | 2.19 | 0.94 | 0.79 | 0.67 | 0.47 |
| tm70 | 5 | 0.94 | 0.81 | 0.53 | 0.82 | 0.52 | 0.33 | 0.11 |
| tm90 | 0 | 1.44 | 3.12 | 41.84 | 1.25 | 1.99 | 3.14 | 8.95 |
| tm90 | 0.5 | 1.38 | 2.75 | 28.35 | 1.20 | 1.75 | 2.54 | 6.06 |
| tm90 | 1.5 | 1.27 | 2.11 | 12.56 | 1.10 | 1.34 | 1.64 | 2.68 |
| tm90 | 2.5 | 1.17 | 1.62 | 5.31 | 1.02 | 1.03 | 1.05 | 1.14 |
| tm90 | 3.5 | 1.07 | 1.23 | 2.18 | 0.93 | 0.78 | 0.67 | 0.47 |
| tm90 | 5 | 0.94 | 0.81 | 0.53 | 0.82 | 0.51 | 0.33 | 0.11 |

### Wealth above W_min as a share of GDP (index), payers (percent of adults), annual positive taxable increments (percent of GDP, blocks)

| schedule | c % | taxable/GDP y10 | taxable/GDP y50 | taxable/GDP y100 | payers y10 | payers y50 | payers y100 | incr b10 | incr b50 | incr b100 |
|---|---|---|---|---|---|---|---|---|---|---|
| tm50 | 0 | 1.33 | 3.58 | 10.58 | 60.00 | 80.00 | 90.00 | 29.57 | 81.01 | 241.11 |
| tm50 | 0.5 | 1.28 | 2.82 | 7.08 | 60.00 | 70.00 | 90.00 | 25.18 | 57.62 | 144.77 |
| tm50 | 1.5 | 1.11 | 1.83 | 3.05 | 50.00 | 70.00 | 80.00 | 17.31 | 28.20 | 47.69 |
| tm50 | 2.5 | 1.02 | 1.12 | 1.19 | 50.00 | 60.00 | 60.00 | 10.85 | 11.96 | 12.71 |
| tm50 | 3.5 | 0.92 | 0.61 | 0.34 | 48.33 | 40.00 | 28.33 | 5.08 | 3.36 | 1.91 |
| tm50 | 5 | 0.76 | 0.18 | 0.02 | 40.00 | 15.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| tm70 | 0 | 1.32 | 3.51 | 10.19 | 60.00 | 80.00 | 90.00 | 29.44 | 79.50 | 232.26 |
| tm70 | 0.5 | 1.27 | 2.77 | 6.87 | 60.00 | 70.00 | 90.00 | 25.07 | 56.62 | 140.48 |
| tm70 | 1.5 | 1.10 | 1.80 | 2.99 | 50.00 | 70.00 | 80.00 | 17.24 | 27.78 | 46.75 |
| tm70 | 2.5 | 1.02 | 1.11 | 1.18 | 50.00 | 60.00 | 60.00 | 10.82 | 11.79 | 12.52 |
| tm70 | 3.5 | 0.92 | 0.60 | 0.34 | 48.33 | 40.00 | 28.33 | 5.07 | 3.31 | 1.88 |
| tm70 | 5 | 0.76 | 0.18 | 0.02 | 40.00 | 15.00 | 1.00 | 0.00 | 0.00 | 0.00 |
| tm90 | 0 | 1.32 | 3.47 | 9.97 | 60.00 | 80.00 | 90.00 | 29.34 | 78.63 | 227.42 |
| tm90 | 0.5 | 1.26 | 2.74 | 6.76 | 60.00 | 70.00 | 90.00 | 24.98 | 56.03 | 138.16 |
| tm90 | 1.5 | 1.10 | 1.78 | 2.96 | 50.00 | 70.00 | 80.00 | 17.19 | 27.52 | 46.26 |
| tm90 | 2.5 | 1.01 | 1.10 | 1.17 | 50.00 | 60.00 | 60.00 | 10.79 | 11.69 | 12.43 |
| tm90 | 3.5 | 0.92 | 0.60 | 0.34 | 48.33 | 40.00 | 28.33 | 5.06 | 3.28 | 1.86 |
| tm90 | 5 | 0.76 | 0.18 | 0.02 | 40.00 | 15.00 | 1.00 | 0.00 | 0.00 | 0.00 |

### Receipts and relief (percent of GDP, five-year blocks): M1a, relief, relief minus M1d

| schedule | c % | M1a b5 | M1a b10 | M1a b20 | M1a b30 | M1a b50 | M1a b75 | M1a b100 |
|---|---|---|---|---|---|---|---|---|
| tm50 | 0 | 3.94 | 4.67 | 6.31 | 8.65 | 14.94 | 29.41 | 26.56 |
| tm50 | 0.5 | 3.62 | 4.16 | 5.33 | 6.91 | 10.62 | 18.46 | 14.34 |
| tm50 | 1.5 | 3.00 | 3.21 | 3.75 | 4.29 | 5.33 | 6.92 | 3.71 |
| tm50 | 2.5 | 2.42 | 2.44 | 2.49 | 2.55 | 2.55 | 2.43 | 0.77 |
| tm50 | 3.5 | 1.86 | 1.77 | 1.57 | 1.44 | 1.13 | 0.71 | 0.10 |
| tm50 | 5 | 1.23 | 1.06 | 0.74 | 0.54 | 0.30 | 0.08 | -0.00 |
| tm70 | 0 | 4.38 | 5.07 | 6.64 | 8.95 | 15.14 | 29.79 | 26.77 |
| tm70 | 0.5 | 4.03 | 4.52 | 5.63 | 7.16 | 10.74 | 18.61 | 14.43 |
| tm70 | 1.5 | 3.35 | 3.51 | 3.99 | 4.47 | 5.36 | 6.91 | 3.71 |
| tm70 | 2.5 | 2.70 | 2.69 | 2.69 | 2.69 | 2.56 | 2.39 | 0.76 |
| tm70 | 3.5 | 2.08 | 1.97 | 1.73 | 1.56 | 1.14 | 0.69 | 0.09 |
| tm70 | 5 | 1.39 | 1.19 | 0.84 | 0.62 | 0.31 | 0.07 | -0.00 |
| tm90 | 0 | 4.73 | 5.35 | 6.82 | 9.07 | 15.18 | 29.98 | 26.90 |
| tm90 | 0.5 | 4.36 | 4.79 | 5.80 | 7.26 | 10.74 | 18.68 | 14.50 |
| tm90 | 1.5 | 3.63 | 3.74 | 4.13 | 4.56 | 5.32 | 6.88 | 3.71 |
| tm90 | 2.5 | 2.94 | 2.89 | 2.82 | 2.78 | 2.52 | 2.36 | 0.76 |
| tm90 | 3.5 | 2.27 | 2.14 | 1.85 | 1.64 | 1.11 | 0.66 | 0.09 |
| tm90 | 5 | 1.53 | 1.32 | 0.94 | 0.70 | 0.31 | 0.07 | -0.00 |

| schedule | c % | relief b5 | relief b10 | relief b20 | relief b30 | relief b50 | relief b75 | relief b100 |
|---|---|---|---|---|---|---|---|---|
| tm50 | 0 | -0.00 | 4.93 | 8.58 | 10.72 | 16.51 | 29.93 | 45.19 |
| tm50 | 0.5 | -0.00 | 4.59 | 7.73 | 9.15 | 12.67 | 19.98 | 26.64 |
| tm50 | 1.5 | -0.00 | 3.97 | 6.33 | 6.84 | 7.84 | 9.36 | 9.76 |
| tm50 | 2.5 | -0.00 | 3.46 | 5.20 | 5.26 | 5.27 | 5.15 | 4.57 |
| tm50 | 3.5 | -0.00 | 3.02 | 4.36 | 4.22 | 3.92 | 3.50 | 3.14 |
| tm50 | 5 | -0.00 | 2.58 | 3.61 | 3.37 | 3.11 | 2.87 | 2.79 |
| tm70 | 0 | -0.00 | 5.16 | 8.91 | 11.01 | 16.70 | 30.28 | 45.69 |
| tm70 | 0.5 | -0.00 | 4.79 | 8.03 | 9.40 | 12.77 | 20.12 | 26.86 |
| tm70 | 1.5 | -0.00 | 4.13 | 6.58 | 7.03 | 7.87 | 9.35 | 9.75 |
| tm70 | 2.5 | -0.00 | 3.58 | 5.40 | 5.41 | 5.28 | 5.11 | 4.54 |
| tm70 | 3.5 | -0.00 | 3.10 | 4.52 | 4.35 | 3.92 | 3.47 | 3.13 |
| tm70 | 5 | -0.00 | 2.62 | 3.72 | 3.46 | 3.12 | 2.86 | 2.79 |
| tm90 | 0 | 0.00 | 5.32 | 9.09 | 11.13 | 16.73 | 30.44 | 45.97 |
| tm90 | 0.5 | -0.00 | 4.94 | 8.20 | 9.50 | 12.77 | 20.18 | 26.99 |
| tm90 | 1.5 | -0.00 | 4.25 | 6.73 | 7.13 | 7.84 | 9.32 | 9.76 |
| tm90 | 2.5 | 0.00 | 3.68 | 5.54 | 5.50 | 5.25 | 5.07 | 4.53 |
| tm90 | 3.5 | 0.00 | 3.17 | 4.65 | 4.44 | 3.90 | 3.45 | 3.12 |
| tm90 | 5 | -0.00 | 2.66 | 3.82 | 3.54 | 3.11 | 2.85 | 2.79 |

| schedule | c % | relief-M1d b5 | relief-M1d b10 | relief-M1d b20 | relief-M1d b30 | relief-M1d b50 | relief-M1d b75 | relief-M1d b100 |
|---|---|---|---|---|---|---|---|---|
| tm50 | 0 | -0.00 | 0.47 | 0.47 | 2.61 | 8.40 | 21.82 | 37.08 |
| tm50 | 0.5 | -0.00 | 0.12 | -0.38 | 1.04 | 4.56 | 11.87 | 18.53 |
| tm50 | 1.5 | -0.00 | 1.22 | 1.59 | -1.27 | -0.27 | 1.25 | 1.65 |
| tm50 | 2.5 | -0.00 | 0.72 | 0.46 | 0.52 | 0.53 | 0.41 | -0.17 |
| tm50 | 3.5 | -0.00 | 0.27 | -0.38 | -0.52 | -0.82 | -1.24 | -1.60 |
| tm50 | 5 | -0.00 | 0.96 | 0.62 | 0.38 | 0.12 | -0.12 | -0.20 |
| tm70 | 0 | -0.00 | 0.70 | 0.80 | 2.90 | 8.59 | 22.17 | 37.58 |
| tm70 | 0.5 | -0.00 | 0.33 | -0.08 | 1.29 | 4.66 | 12.01 | 18.75 |
| tm70 | 1.5 | -0.00 | 1.39 | 1.16 | -1.08 | -0.24 | 1.24 | 1.64 |
| tm70 | 2.5 | -0.00 | 0.84 | 0.66 | 0.67 | 0.54 | 0.37 | -0.20 |
| tm70 | 3.5 | -0.00 | 0.36 | -0.22 | -0.39 | -0.82 | -1.27 | -1.61 |
| tm70 | 5 | -0.00 | 0.65 | -1.02 | -1.28 | -1.62 | -1.88 | -1.95 |
| tm90 | 0 | 0.00 | 0.86 | 0.98 | 3.02 | 8.62 | 22.33 | 37.86 |
| tm90 | 0.5 | -0.00 | 0.47 | 0.09 | 1.39 | 4.66 | 12.07 | 18.88 |
| tm90 | 1.5 | -0.00 | 1.51 | -1.38 | -0.98 | -0.27 | 1.21 | 1.65 |
| tm90 | 2.5 | 0.00 | 0.94 | 0.80 | 0.76 | 0.51 | 0.33 | -0.21 |
| tm90 | 3.5 | 0.00 | 0.43 | -0.09 | -0.30 | -0.84 | -1.29 | -1.62 |
| tm90 | 5 | -0.00 | 0.70 | -0.92 | -1.20 | -1.63 | -1.89 | -1.95 |

### First year relief is below M1d, fill year, taxes retired by year 100

| schedule | c % | first year below | fill year | taxes retired |
|---|---|---|---|---|
| tm50 | 0 | 13 | 6 | 6 |
| tm50 | 0.5 | 13 | 6 | 6 |
| tm50 | 1.5 | 13 | 6 | 6 |
| tm50 | 2.5 | 13 | 6 | 5 |
| tm50 | 3.5 | 13 | 6 | 5 |
| tm50 | 5 | 13 | 6 | 4 |
| tm70 | 0 | 13 | 6 | 6 |
| tm70 | 0.5 | 13 | 6 | 6 |
| tm70 | 1.5 | 13 | 6 | 6 |
| tm70 | 2.5 | 13 | 6 | 5 |
| tm70 | 3.5 | 13 | 6 | 5 |
| tm70 | 5 | 12 | 6 | 5 |
| tm90 | 0 | 13 | 6 | 6 |
| tm90 | 0.5 | 13 | 6 | 6 |
| tm90 | 1.5 | 13 | 6 | 6 |
| tm90 | 2.5 | 13 | 6 | 5 |
| tm90 | 3.5 | 13 | 6 | 5 |
| tm90 | 5 | 13 | 6 | 5 |

## Item 2 (B) and item 3 (C): the tax's own drag on compounding

Aggregate wealth, constant path; real level and share of GDP, both indexed to year 1.

| scenario | real y10 | real y30 | real y50 | real y100 | W/GDP y10 | W/GDP y30 | W/GDP y50 | W/GDP y100 |
|---|---|---|---|---|---|---|---|---|
| returns only (tax 1e-9, c 0) | 1.52 | 3.83 | 9.67 | 97.98 | 1.32 | 2.44 | 4.51 | 20.95 |
| returns and consumption (tax 1e-9, c 3.5) | 1.10 | 1.36 | 1.69 | 2.88 | 0.96 | 0.87 | 0.79 | 0.62 |
| returns, consumption and the tax (tm50, c 3.5) | 1.08 | 1.25 | 1.46 | 2.22 | 0.94 | 0.80 | 0.68 | 0.47 |
| returns, consumption and the tax (tm70, c 3.5) | 1.08 | 1.24 | 1.45 | 2.19 | 0.94 | 0.79 | 0.67 | 0.47 |
| returns, consumption and the tax (tm90, c 3.5) | 1.07 | 1.23 | 1.43 | 2.18 | 0.93 | 0.78 | 0.67 | 0.47 |

## Item 4 (D): threshold indexation

The runner (`core_run`) has no switch for a fixed real threshold; `burden.line_flows` and `revenue.run_lines` take `index` (anything but `gdp_pc` leaves the threshold fixed in real terms). The script repeats core_run's steps with that argument (no core edit) and asserts the copy equals core_run for the GDP-indexed case. Consumption 3.5, constant path.

| schedule | threshold | payers y10 | payers y50 | payers y100 | taxable/GDP y10 | taxable/GDP y50 | taxable/GDP y100 | M1a b10 | M1a b50 | M1a b100 | relief b100 | first year below M1d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tm50 | GDP per head | 48.33 | 40.00 | 28.33 | 0.92 | 0.61 | 0.34 | 1.77 | 1.13 | 0.10 | 3.14 | 13 |
| tm50 | fixed real | 50.00 | 60.00 | 70.00 | 0.94 | 0.69 | 0.46 | 1.86 | 1.51 | 0.19 | 3.47 | 13 |
| tm70 | GDP per head | 48.33 | 40.00 | 28.33 | 0.92 | 0.60 | 0.34 | 1.97 | 1.14 | 0.09 | 3.13 | 13 |
| tm70 | fixed real | 50.00 | 60.00 | 70.00 | 0.93 | 0.68 | 0.45 | 2.06 | 1.54 | 0.19 | 3.47 | 13 |
| tm90 | GDP per head | 48.33 | 40.00 | 28.33 | 0.92 | 0.60 | 0.34 | 2.14 | 1.11 | 0.09 | 3.12 | 13 |
| tm90 | fixed real | 50.00 | 60.00 | 70.00 | 0.93 | 0.68 | 0.45 | 2.23 | 1.52 | 0.19 | 3.46 | 13 |

## Item 5 (E): relief components, percent of GDP, five-year blocks (consumption 3.5, constant path)

| schedule | component | b5 | b10 | b20 | b30 | b50 | b75 | b100 |
|---|---|---|---|---|---|---|---|---|
| tm50 | M1a individual WDT | 1.86 | 1.77 | 1.57 | 1.44 | 1.13 | 0.71 | 0.10 |
| tm50 | M1b corporate levy | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 |
| tm50 | M1c fund income | -4.68 | -1.58 | -0.03 | -0.03 | -0.03 | -0.04 | 0.22 |
| tm50 | reserve (stock) | 11.65 | 31.23 | 43.61 | 59.91 | 112.06 | 243.17 | 525.67 |
| tm50 | relief | -0.00 | 3.02 | 4.36 | 4.22 | 3.92 | 3.50 | 3.14 |
| tm50 | retired receipts M1d | 0.00 | 2.74 | 4.74 | 4.74 | 4.74 | 4.74 | 4.74 |
| tm70 | M1a individual WDT | 2.08 | 1.97 | 1.73 | 1.56 | 1.14 | 0.69 | 0.09 |
| tm70 | M1b corporate levy | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 |
| tm70 | M1c fund income | -4.90 | -1.69 | -0.03 | -0.03 | -0.03 | -0.04 | 0.21 |
| tm70 | reserve (stock) | 11.99 | 32.62 | 45.55 | 62.54 | 116.77 | 253.28 | 547.46 |
| tm70 | relief | -0.00 | 3.10 | 4.52 | 4.35 | 3.92 | 3.47 | 3.13 |
| tm70 | retired receipts M1d | 0.00 | 2.74 | 4.74 | 4.74 | 4.74 | 4.74 | 4.74 |
| tm90 | M1a individual WDT | 2.27 | 2.14 | 1.85 | 1.64 | 1.11 | 0.66 | 0.09 |
| tm90 | M1b corporate levy | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 | 2.82 |
| tm90 | M1c fund income | -5.09 | -1.78 | -0.02 | -0.02 | -0.03 | -0.04 | 0.21 |
| tm90 | reserve (stock) | 12.28 | 33.80 | 47.20 | 64.76 | 120.70 | 261.72 | 565.68 |
| tm90 | relief | 0.00 | 3.17 | 4.65 | 4.44 | 3.90 | 3.45 | 3.12 |
| tm90 | retired receipts M1d | 0.00 | 2.74 | 4.74 | 4.74 | 4.74 | 4.74 | 4.74 |

### Attribution of the fall in relief, block ending year 20 to block ending year 100

Relief does not fall between the blocks ending in years 10 and 100 in the central run (it is still rising to its post-fill peak in the block ending year 20), so the fall is measured from the block ending year 20, the peak, to the block ending year 100. F0 is that fall in relief (GDP-points) in the central run. "By component" splits F0 into the fall of M1a, M1b and M1c. "Counterfactual" rows are F0 minus the fall with the factor removed, over F0: consumption set to 0, the threshold fixed in real terms, the levy set to 0 (I-D7a). Removing consumption does not shorten the fall, it reverses it (last column: relief rises by that many GDP-points from the block ending year 20 to year 100), so its share is far above 100% and is read as: consumption accounts for all of the fall and more. The tax's own drag on compounding is measured in item 2 (B), not here.

| schedule | F0 | M1a % | M1b % | M1c % | consumption % | threshold % | levy % | relief change with c = 0 |
|---|---|---|---|---|---|---|---|---|
| tm50 | 1.22 | 121 | 0 | -21 | 3106 | 11 | 0 | +36.61 |
| tm70 | 1.39 | 117 | 0 | -17 | 2738 | 9 | 0 | +36.78 |
| tm90 | 1.53 | 115 | 0 | -15 | 2514 | 8 | 0 | +36.88 |

## Item 6 (F): conventions

### (i) constant path at the arithmetic mean 4.74 (I-D1a) against the geometric mean 4.42 (I-D1a2), consumption 3.5

| schedule | return | W/GDP y30 | W/GDP y100 | M1a b100 | relief b100 | first year below M1d |
|---|---|---|---|---|---|---|
| tm50 | 4.74 | 0.80 | 0.47 | 0.10 | 3.14 | 13 |
| tm50 | 4.42 | 0.74 | 0.36 | 0.04 | 2.99 | 13 |
| tm70 | 4.74 | 0.79 | 0.47 | 0.09 | 3.13 | 13 |
| tm70 | 4.42 | 0.73 | 0.36 | 0.04 | 2.98 | 13 |
| tm90 | 4.74 | 0.78 | 0.47 | 0.09 | 3.12 | 13 |
| tm90 | 4.42 | 0.72 | 0.36 | 0.04 | 2.97 | 13 |

### (ii) 1000 random paths of the AR(1) generator at central inputs (seed 20261118), consumption 3.5

| schedule | W/GDP y30 median | P10 | y50 median | P10 | y100 median | P10 | paths with relief below M1d at some year % | median first year below |
|---|---|---|---|---|---|---|---|---|
| tm50 | 0.72 | 0.36 | 0.58 | 0.24 | 0.34 | 0.09 | 100.0 | 11 |
| tm70 | 0.72 | 0.36 | 0.57 | 0.23 | 0.34 | 0.09 | 100.0 | 11 |
| tm90 | 0.71 | 0.35 | 0.57 | 0.23 | 0.34 | 0.09 | 100.0 | 11 |

### (iii) constant GDP growth: arithmetic mean 1.570% (what runner.context uses) against geometric mean 1.534% of the same 117 years (the brief quoted 1.49%, which this series does not give; the full 1870-2019 history gives 1.43%), constant return 4.74, consumption 3.5

| schedule | GDP growth | W/GDP y100 | first year below M1d |
|---|---|---|---|
| tm50 | arithmetic | 0.47 | 13 |
| tm50 | geometric | 0.49 | 13 |
| tm70 | arithmetic | 0.47 | 13 |
| tm70 | geometric | 0.49 | 13 |
| tm90 | arithmetic | 0.47 | 13 |
| tm90 | geometric | 0.48 | 13 |

