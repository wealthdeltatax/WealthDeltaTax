# Model v3: supporting outputs (brief 016g)

> Integrated into `metrics.md` and `outputs.yml` on 2026-11-17 (ids renumbered there). Those two files are the definition; this file keeps the working, flags and research requests.

Proposals for the guru's merge into `metrics.md` and `outputs.yml` after 014g, 015g and 016g are all done. Nothing here edits those files. Source of the list: `website/notes/ledger.md` section 6.2 and the author's decisions of 2026-11-17 (section 8, item 5 and 6).

Rules followed. One definition per metric: no second denominator for an existing metric. Where an output is a view of an existing metric, it reuses that metric and says so. New metric ids used: B1 (a to d), P7 (a, b), M7c to M7e, M9, M4c, F1, T1. All are free in `metrics.md`. `element:` values are the ledger's; spoke ids follow the ledger and the guru renumbers after the S4 and S6 split (ledger section 8, item 1). Every `summary:` token is one already used in `outputs.yml`.

Numbers quoted from the register are inputs, not results. Nothing was run.

## OB1: payers, entries, exits and fall-through refunds, by threshold

**Metric rows** (new metric B1; payer and W_min as in the `metrics.md` conventions)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| B1a | Payers | Adults whose net wealth at the start of year t is at or above W_min | adults | millions, and % of adults | transition, short, long |
| B1b | Entries | Payers in year t who were not payers in year t-1 | payers at the start of year t-1 | % per year, and count | as B1a |
| B1c | Exits | Payers in year t-1 whose net wealth at the start of year t is below W_min | payers at the start of year t-1 | % per year, and count | as B1a |
| B1d | Fall-through refund volume | Refunds paid in year t to adults who were payers in year t-1 and are below W_min at the start of year t (the claim is capped by tax paid to date, as in M1a) | GDP_t | % of GDP | as B1a |

B1d is part of the refunds already inside M1a, so it is a split of M1a and never added to it. The refund event is read from the ledger's pointer (CLOSE §4.3, §7.2); I did not open CLOSE for this brief, so the code lane confirms the event against it before stage C. Summary form: `p10_mean_p90` (level 1), each line reported over a grid of W_min values at S_central. The grid is the lever D3, fixed in stage C or D; reference points the papers already use are £150,000 (I-D4b), £2m (SWEEPS balanced parameters) and £10m (WP §9.3).

**Inputs.** B1a: I-D4a, I-D4b, I-D4c (base and share at £150,000), I-D4d, I-D4e, I-D4f (tail). B1b to B1d: I-D1a to I-D1d (returns move people across the line, and loss years trigger refunds). MISSING: M-1 (payer share and wealth held at thresholds other than £150,000) and M-2 (movement of adults across the threshold from year to year).

**`outputs.yml` line to add**
```yaml
  - {id: OB1,  metric: B1,  title: "Payers, entries, exits and fall-through refund volume, by threshold", summary: p10_mean_p90, by: [w_min], lines: [B1a, B1b, B1c, B1d], element: [S3, S5, S12], kind: supporting}
```

**Claim it lets a spoke make.** How many people pay at each threshold, how many cross it each year, and how large the refund flow is when payers fall back through it (ledger claim 13), so the old "about 32,000 payers at £10m" is replaced by a measured count.

## OR1: reserve solvency

**Metric rows** (new metric P7; targets as P1, 3 times the trailing mean annual refund)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| P7a | Reserve insolvency share | Share of level-1 return paths in which the long reserve reaches zero in at least one year after the long-reserve fill | return paths | % of paths | short, long |
| P7b | Minimum cover | Over the years after the fill, the minimum of the long reserve divided by its P1 target; mean over paths, with the P10 over paths beside it | the P1 target | ratio | as P7a |

P7 differs from P3. P3 asks whether retired receipts ever exceed revenue under staged retirement; P7 asks whether the reserve itself runs out. A path can fail one and pass the other, so both are reported. Summary form: `point_and_range`, where the point is the level-1 value at central parameters and the range is the P10 to P90 over level-2 parameter draws.

**Inputs.** I-D1a, I-D1b, I-D1c, I-D1d (return level, volatility, loss-year frequency and runs), I-D8a (target multiple, a lever), I-D8b, I-D8c (fill times, a cross-check on P1). No MISSING input.

**`outputs.yml` line to add**
```yaml
  - {id: OR1,  metric: P7,  title: "Reserve solvency: share of paths where the long reserve reaches zero, and minimum cover", summary: point_and_range, lines: [P7a, P7b], element: [S5, S10], kind: path}
```

**Claim it lets a spoke make.** A measured share of paths in which the long reserve runs out, with the worst-case cover, in place of the v1 claim that it "never reaches zero", which is not carried because v2 closes only 42 to 55% of windows (ledger claim 3; `drivers.md` D1).

## OD1: declaration curve across alpha

**Metric rows** (extends M7; M7 itself is unchanged, its zone is still `|C.1| < 2` points)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M7c | Declaration curve | C.1(alpha) = (Net(alpha) - Net(1)) / TW(1), the M7 formula evaluated at every alpha on a grid, not only at the zone edges | TW(1) | percentage points | the M7 horizon |
| M7d | Lost refund protection | (Refunds(1) - Refunds(alpha)) / TW(1): the part of C.1(alpha) that is refunds forgone because declared wealth is understated; a split of M7c, never added to it | TW(1) | percentage points | as M7c |
| M7e | Modal declaration | The alpha held by the largest share of payers, taken from the distribution of declared alpha across payers | payers | alpha (ratio) | as M7c |

The understater plateau is read off M7c: the alpha range below the zone in which C.1 stops changing by more than a stated tolerance. It is a reading of the curve, not a metric. The tolerance is a choice for stage C. M7e is the "behavioural centre near 1.1" of the old papers; the old definition sits in VAL §7, which I did not open, so the code lane confirms it there. Summary form: `point_and_range`.

**Inputs.** I-D5b (avoidance and under-reporting), I-D5d (understatement of discretionary valuations), I-D5a (total base response, a bound). The tax schedule is the lever D2, not an input. MISSING: M-3 (distribution of declared alpha among payers). Without it M7e is an assumption, flagged as such.

**`outputs.yml` line to add**
```yaml
  - {id: OD1,  metric: M7,  title: "Declaration curve across alpha (C.1 over TW(1), refund protection lost, modal declaration)", summary: point_and_range, by: [alpha_grid], lines: [M7c, M7d, M7e], element: [H5, S4], kind: supporting}
```

**Claim it lets a spoke make.** The whole curve of the cost of misdeclaring: where understating stops paying and why (lost refund protection), and where overstating limits itself (ledger claim 7), not only the width of the tolerant zone O7 gives.

## OM1: net fiscal effect after migration

**Metric row** (new metric M9; a view of M1, same denominator)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M9 | Net fiscal effect after migration | M9 = M1 - X, where X is the income tax, NICs and VAT that the state loses from people who leave UK tax residence in response to the tax, in year t. X = (share leaving) x (their taxable income and spending) x (the rates on them) | GDP_t | % of GDP and real £bn | transition, short, long |

M9 sits beside M1. M1 is not redefined, and the line X is reported on its own, not merged. The ledger's term is the "cross-base externality": the income tax and VAT lost per unit of wealth tax lost to emigration (BEHAV §9.2, BEHAV.A §D; WP §7.3). Summary form: `p10_mean_p90`.

**Inputs.** I-D5c (share leaving residence, 0 to 11%), I-D5a (total base response), I-D9d (mean income of the top wealth decile, a proxy for leavers' income), I-M6l (effective income tax rate of people with £3m or more of income, income only, 37 to 47%), I-D4b, I-D4c (who is in the base). MISSING: M-4 (income, NICs and VAT paid by the likely leavers, per pound of wealth tax base, and their consumption share).

**`outputs.yml` line to add**
```yaml
  - {id: OM1,  metric: M9,  title: "Net fiscal effect after migration (M1 less income tax, NICs and VAT lost from leavers)", summary: p10_mean_p90, lines: [M1, X], element: [S6], kind: headline_support}
```

**Claim it lets a spoke make.** What the revenue is once the people who leave, and the taxes they stop paying, are counted, so the migration objection is answered with a number on the same basis as O1 (ledger claim 12).

## OL1: the worker's saving in pounds per month

**Metric row** (new metric M4c; a derived view of M4b, no new denominator)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M4c | Non-payer saving, pounds per month | M4c(y) = M4b(d) x y / 12, where d is the income decile of a reference worker with income y, and M4b(d) is the decile's saving as a share of income. The worker is assumed to have the decile average M4b. Real pounds in the stated base year | none (a level) | £ per month | transition, short, long |

M4c does not compute a purchasing-power effect on prices. The old payslip figures (purchasing power up 36% and 29%) were v1 results and are not carried. Price pass-through of the retired business taxes is already inside the incidence inputs I-D6b and I-D6c, and so inside M4a and M4b. Summary form: `p10_mean_p90`.

**Inputs.** Those of M4a and M4b: I-D6a to I-D6n (incidence of the six retired taxes, partial: they give the top income decile and the bottom five only, and M4a by decile needs all ten, a gap that already affects O4a), I-D1a to I-D1d (through M1). MISSING: M-5 (mean household income by income decile, and the reference earners: median earnings and the care worker of LDW §2, so the pound figures rest on published earnings and not on the paper's example).

**`outputs.yml` line to add**
```yaml
  - {id: OL1,  metric: M4c, title: "Non-payer saving in pounds per month for a reference worker (view of O4b)", summary: p10_mean_p90, by: [reference_worker], element: [S6, S7], kind: headline_support}
```

**Claim it lets a spoke make.** What the tax saves a care worker and a median earner each month, in pounds (ledger claim 9), derived from O4b and so never in conflict with it.

## OF1: feasibility map over the schedule family

**Metric row** (new metric F1; the other quantities on the map are existing metrics)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| F1 | Closure share | For one schedule and threshold, the share of level-1 return paths in which P3 equals zero | return paths | % of paths | transition and short |

The map reports, at each point of a grid over the schedule family (entry rate, ceiling rate, steepness: the three parameters of D2) and the threshold (D3): F1, the level-1 mean of M2, and the level-1 mean of M4a. A point is feasible when F1 is at or above a stated share, M2 is under a stated cap, and M4a is above a stated floor, exactly as `metrics.md` (range design) says. The named schedules S_low, S_central and S_high are read off the map by the choice rule already confirmed there. The share, cap and floor are the author's to fix in stage C; this file does not choose them. Summary form: `p10_mean_p90` for each plotted quantity (level 1 at each grid point).

**Inputs.** No lever is a research input (D2, D3). The map needs the whole level-1 set: I-D1a to I-D1d, I-D4a to I-D4c, I-D5a to I-D5d, I-D6a to I-D6n, I-D8a. No MISSING input.

**`outputs.yml` line to add**
```yaml
  - {id: OF1,  metric: F1,  title: "Feasibility map over the schedule family (closure share, M2 and M4a at each point)", summary: p10_mean_p90, by: [schedule_grid, w_min], lines: [F1, M2, M4a], element: [S5], kind: supporting}
```

**Claim it lets a spoke make.** Which schedules close, keep the burden under the cap and keep the saving above the floor, and why the named schedules sit where they do (the parameter hierarchy of ledger claim 8, found by the model instead of asserted).

## OT1: tornado

**Metric row** (new metric T1)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| T1 | Tornado swing | For headline h and input j: T1(h, j, low) = h(j at Low) - h(central), and T1(h, j, high) = h(j at High) - h(central), every other input at central. Inputs are ranked by the larger of the two absolute swings | the headline's own | points of GDP for M1; percentage points for M2 and M4a | transition, short, long |

Low, Central and High are the columns of `inputs.md`. The tornado is run at each named schedule. It is the level-2 reading of `metrics.md`, set beside, not replacing, the P10 to P90 of the level-1 mean over parameter draws. The 0.5-point cut-off for tier 2 inputs (`drivers.md` section 4, item 4) is applied to the M1 swing. Headlines: M1, M2 and M4a; adding M3 is one more column if the author counts it among the "three headlines". The pen-and-paper tornado of `drivers.md` section 4 is the cross-check on the M1 column. Summary form: `point_and_range`, where the point is the swing at Low and at High.

**Inputs.** Every row of `inputs.md` with Low different from High. Levers D2 and D3 are not varied here; they are swept in OF1. No MISSING input.

**`outputs.yml` line to add**
```yaml
  - {id: OT1,  metric: T1,  title: "Tornado: one input at a time, low and high, on M1, M2 and M4a", summary: point_and_range, by: [input, headline, schedule], element: [S5], kind: supporting}
```

**Claim it lets a spoke make.** Which inputs the headlines depend on, and which do not matter (ledger claim 8), with the swings on each headline.

## CK1: synthetic cyclical stress test (SWEEPS 7.5)

**Decision: a check, not an output.** It estimates nothing the world decides. The path is a fixed function, g(t) = mu + A sin(2 pi t / T), with no draws and so no range. Its job is to show that the mechanism holds up against a deterministic cycle that historical sampling may under-represent, which is a test of the model, not a finding about the UK. It therefore lives in the check suite and is cited in S12 as evidence, not reported as a headline.

**Metric row** (no new metric; the check reads existing ones)

| ID | Name | Formula | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| CK1 | Cyclical stress test | On the synthetic path, report P1 (fill years), P3 (cumulative shortfall) and P7b (minimum cover) for each amplitude A on a stated grid. Pass: P3 equals zero up to the amplitude at which the check is stated to hold, and the amplitude is reported | as P1, P3, P7b | as P1, P3, P7b | short |

Two points for the code lane, both from reading SWEEPS 7.5 against the register. First, the canonical mu of 7% is not the register's real return (I-D1a central 4.42%, low 2.18%, high 7.47%); the fixture should take mu from I-D1a, and the choice is the author's. Second, a sinusoid of amplitude A has a standard deviation of A divided by the square root of 2. The canonical A of 8% gives about 5.7%, below I-D1b's central 8.2% (low 6.5%, high 9.8%); matching 8.2% needs A of about 11.6%. So the amplitude grid should run to about 12%, or the check is milder than the history it complements. This answers the ledger's question: keep the check, and do not rely on level-1 sampling to cover cycles without it, because the sampled windows keep historical sequences, not a fixed period.

**Inputs.** I-D1a, I-D1b (the mean and the volatility the grid is matched to), I-D8a (target multiple). The cycle period T (10 years in SWEEPS 7.5) is a fixture, not a research input. No MISSING input.

**`outputs.yml` line to add** (if the manifest holds outputs only, move this to a `checks:` list; the guru decides at the merge)
```yaml
  - {id: CK1,  metric: [P1, P3, P7b], title: "Synthetic cyclical stress test (fixed sinusoidal return path, by amplitude)", summary: point_and_range, by: [amplitude], element: [S12], kind: check}
```

**Claim it lets a spoke make.** The staged-retirement mechanism and the reserves hold under a regular ten-year cycle up to a stated amplitude, and the amplitude is matched to the historical volatility (ledger section 8, item 6; SWEEPS §7.5).

## MISSING inputs: research requests (012r follow-up)

| Ref | Needed for | Request |
|---|---|---|
| M-1 | OB1 | The share of adults, and the share of wealth they hold, above each threshold on a grid from about £150,000 to £10m, from the held WAS Round 8 percentile tables plus the tail sources (I-D4d to I-D4f). Extends I-D4b and I-D4c, which give one threshold |
| M-2 | OB1 | How often adults cross a given wealth threshold in a year, by band: a published wealth-mobility estimate, or the saving and portfolio assumption the model would otherwise need |
| M-3 | OD1 | The distribution of declared value against true value among payers, or the closest evidence on bunching and understatement (I-D5d is a mean, not a distribution) |
| M-4 | OM1 | Income tax, NICs and VAT paid per pound of wealth by the people most likely to leave, with their consumption share. I-M6l is a rate only, for taxpayers with £3m or more of income (income only) |
| M-5 | OL1 | Mean household income by income decile, and published earnings for the median worker and a care worker (the ONS decile workbook was not reachable in B2) |

## Author's choices that this file leaves open

- The share, cap and floor that define a feasible schedule (OF1). Stage C.
- The amplitude grid and mu of the stress test (CK1), and the tolerance for the understater plateau (OD1). Stage C.
- Whether the three headlines in the tornado are M1, M2 and M4a, or include M3 (OT1).
