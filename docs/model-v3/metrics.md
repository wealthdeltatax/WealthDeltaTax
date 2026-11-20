# Model v3: metric register (brief 011g, stage A)

One definition per metric. Code and papers cite the ID. Status: **stage A passed, author confirmed all four items on 2026-11-16; the added metrics of briefs 014g to 016g were integrated on 2026-11-17** (sections after the path metrics). One open check remains: the Green Book schedule text for M3 (012r). Decisions behind this file: `docs/model-audit/synthesis.md` section 3.

Horizons (author, 2026-11-16: report short and long term effects). Every headline is reported for three windows, so the time profile is visible:
- **Transition:** launch to the long-reserve fill (v2 median 7 years on UK windows), while taxes are retired in steps.
- **Short term:** the 10 years after the long-reserve fill (v2's own horizon, so v2 and v3 can be compared). Confirmed.
- **Long term:** the mean of years 51 to 100 and the year-100 value. Confirmed.
The author reads the v2 time profile (for one schedule, 9.9% of GDP at the fill year against 5.4% over 100 years) as a sign that WDT may not be sustainable as a revenue source. v3 therefore reports the sustainability test P4 as a result, whichever way it comes out.

Reading rule (A2, author, 2026-11-16). The long window is a steady-state property, not a forecast: the whitepaper's headline claims rest on the transition and short windows and the path to year 50. P4 is read together with P6 (the fund's assets), so a falling M1 beside a rising fund is not read as failure.

Conventions. Time t = years since launch. Payer = adult whose net wealth is at or above W_min (half the median house price, per adult). Non-payer = every other adult. All money is real, in the stated base year; shares of GDP use GDP in year t.

Range design (A2, author, 2026-11-16; amends `synthesis.md` section 3, rows "Range method" and "Rate function"). Policy levers are swept, not sampled: the rate schedule, the threshold and the retirement order. Each headline is reported for each of three named schedules, S_low, S_central and S_high, plus a feasibility map over the schedule family that shows which schedules close (P3 equals zero in at least a stated share of paths), keep M2 under a stated cap and keep M4a above a stated floor. Choice rule for the named schedules (confirmed 2026-11-16): S_central is the feasible-map point with the highest closure share under the burden cap, S_low and S_high are the edges of the feasible region. Exogenous inputs are sampled at two levels and reported apart: **level 1, return risk**: for fixed parameters, the sampled P10, mean and P90 over return paths (R5); **level 2, parameter ignorance**: a tornado (one input at a time, low and high) and the P10 to P90 of the level-1 mean over parameter draws. "No hand-picked scenarios" now applies to exogenous inputs only. A "range" in this register means the level-1 spread unless it says tornado.

## Headline metrics
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M1 | Government revenue, net fiscal effect | M1 = M1a + M1b + M1c - M1d, where M1a = individual WDT paid minus refunds paid; M1b = corporate levy; M1c = fund income minus fund retention (v2 identity, `rates_core.py` line 109); M1d = the sum, over the taxes retired by year t, of their receipts M1e. The lines M1a to M1d are reported beside M1; none is merged into another | GDP_t | % of GDP and real £bn | transition, short and long (above) |
| M1e | Retired-tax receipts | Receipts the state forgoes for each retired tax k. Six taxes are retired (author's decision): corporation tax, council tax, business rates, capital gains tax, inheritance tax, stamp duties. **Source rule (author, 2026-11-17): for each tax the primary source is the central figure (HMRC for capital gains tax, 24.2bn pounds), with the IFS sheet as cross-check and the gap stated beside the number** (023r found IFS 19.5bn against HMRC 24.2bn). Stamp duties carry two receipt lines (property 0.50% of GDP; shares 0.16%): the IFS row 'Stamp duties' (0.66) is their sum, so the seven lines total 8.11% of GDP at 2025-26 (not 8.27, a double count found by the tier 1 tornado). M1e has seven lines and P5 has six retirement years. Retired in steps as relief arrives. **Order (confirmed): ascending by receipts**, smallest first, a policy input that a Phase One governing council may change. **Trigger (confirmed 2026-11-16, follows from P3):** a tax is retired in the first year after the long-reserve fill in which relief R_t, net of the receipts of taxes already retired, covers that tax's receipts. Each headline is reported for the three windows above | GDP_t | % of GDP | as M1 |
| M1f | Break-even mean return | The arithmetic mean real return at which M1 is zero, at the named schedule, with every other input at its central value (author, 2026-11-18; stage C1 item 2). At central inputs the identity gives 3.55% (epsilon held at 29.97%; tornado.md) against 4.74% central; the model reports its own value | none | % per year | single |
| M1g | Share of paths with negative net revenue | Share of simulated paths whose M1 is below zero in the reported year, for each horizon (author, 2026-11-18; stage C1 item 2). M1 is never floored or clipped; a receipt to the state is positive and fund income M1c can be negative | paths | % of paths | transition, short, long |
| M2 | Taxpayer burden in life, share of wealth | Revenue-weighted mean of each payer's burden (author, 2026-11-16): M2 = sum_i T_i (T_i / W_i) / sum_i T_i, where T_i is payer i's net WDT in year t and W_i the payer's net wealth at the start of the year. In life: net WDT of the year without death flows (death assessments and heirs' assessments), comparable with the annual comparator taxes of M5; M2d is the reading with them (author, 2026-11-20). Reported overall and by wealth band. Denominator closed 2026-11-17: same year (see the end of this file); not comparable with the RATES 0.35% | tax paid | % per year | transition, short and long |
| M2d | Taxpayer burden including settlement at death, share of wealth | M2 with the death flows included: the whole net WDT of the year (in life, death and heirs' assessments) in place of the in-life amount in T_i; same weights and denominator. Always labelled as including death (author, 2026-11-20) | tax paid | % per year | transition, short and long |
| M2b | Taxpayer cash-flow burden, share of income | Payer's net WDT in year t divided by the payer's income. Reported by wealth band, with the share of payers whose WDT exceeds a cut-off share of income (reported at 5%, 10% and 20%). Income by wealth band is an input (012r) | payer income | % per year; share of payers | transition, short and long |
| M2c | Taxpayer cash-flow burden, share of liquid assets | Payer's net WDT in year t divided by the payer's liquid assets (cash, deposits, listed holdings; housing and pension excluded). Reported by wealth band, with the share of payers whose WDT exceeds 25%, 50% and 100% of liquid assets. Liquid assets by band is an input (012r) | payer liquid assets | % per year; share of payers | transition, short and long |
| M3 | Taxpayer burden, gain-weighted lifetime rate | Present value of net WDT paid over a payer's life divided by the present value of the gains the payer realises or accrues over that life. v2 candidates: `er_stock_payers`, `er_gain_payers` in `rates_core.py`. Discount rate: the HM Treasury Green Book schedule, 3.0% for years 1 to 30, 2.5% for years 31 to 75, 2.25% for years 76 to 125 (the October 2026 revision; read from HM Treasury's response to the 2026 discount-rate review, to be confirmed against the Green Book text by research); a sensitivity runs at the previous 3.5% and 3.0% schedule. v2 used 3.5% and v1 5%. Life length G = 30 years (confirmed; the v2 generation length). **Gains (author default, 2026-11-17): the real change in net wealth, the same quantity as the WDT delta**, so a gain includes income and capital gain. Views of M3 on today's system are in the problem metrics below | PV of gains | % | one life, G years |
| M4a | Non-payer savings, share of current tax bill | For the non-payers: (tax they pay today minus tax they pay after the change) divided by the tax they pay today. Includes the retired taxes they pay (council tax, business rates passed on, stamp duty, corporation tax incidence) and any relief beyond the retired taxes. Reported by income decile (author, 2026-11-16), plus an overall figure. **Decile definition (author default, 2026-11-17): deciles of all adults by income, then the non-payers inside each decile**, which matches the ONS tables; M4b, M4c and the data fact DH1c use the same definition. The incidence of each retired tax by decile is an input to source (012r) | current tax bill | % | transition, short and long |
| M4b | Non-payer savings, share of income | The same saving divided by the non-payer's income, by income decile | income | % | transition, short and long |

## Revenue lines (parts of M1)
| ID | Name | Definition | Unit |
|---|---|---|---|
| M1a | Individual WDT, net | WDT paid by payers in year t minus refunds paid in loss years (refund capped by the tax paid to date, as the papers state) | % of GDP |
| M1b | Corporate levy | The CORP delta levy collected in year t (positive years only; no levy and no refund in loss years). Own line, never merged into M1a | % of GDP |
| M1c | Fund income net of retention | Fund investment income minus fund growth retained in the reserves (v2: 5.29 and 5.88 for one schedule, so about -0.6) | % of GDP |

## Comparison metrics (for the whitepaper's argument)
| ID | Name | Definition | Notes |
|---|---|---|---|
| M5 | Burden against suggested wealth taxes | M2 recomputed with each suggested wealth tax on the same people, and the difference | Two sets (author, 2026-11-16): the Zucman global minimum tax on billionaires, a 2% floor on wealth above about £1bn (v2 already has this as a check, `zucman_floor`), and the UK wealth tax proposals of about 2%; research (012r) finds and cites the UK proposals and their rates |
| M6 | Burden against today's income tax, CGT and IHT | The payers' CGT and IHT liabilities today (both are retired) divided by the same payers' wealth, set beside M2; income tax stays | Needs HMRC data (012r) |
| M8 | Reform-in-place benchmark | The burden (M2 form) and the non-payer saving (M4a form) when the same net revenue as M1 is raised by a reform inside the existing system, on the same people. Candidates (research, 012r, fixes the specifications and cites the strongest published version of each): CGT aligned with income tax and charged at death with no uplift; a proportional property tax after revaluation replacing council tax and stamp duty; a land value tax. Reported as the difference in percentage points against WDT. The claim to test is that WDT beats the best reform of comparable ambition, not only today's system | Denominators as M2 and M4a; percentage points; short term. Specifications from research (012r) |

## Sensitivity metric
| ID | Name | Definition |
|---|---|---|
| S1 | Capitalisation of retired property taxes | Change in the median house price when stamp duty and council tax are retired, a ranged input (012r). Reported as the change in M1, M2 and the payer count with the response on against off. The threshold is fixed at launch and indexed by the stated rule, so the response acts through wealth values and the payer count, not through a moving threshold |

## Supporting metric
| ID | Name | Definition | Denominator | Unit |
|---|---|---|---|---|
| M7 | C.1, the tolerant-zone measure | (Net(alpha) - Net(1)) / TW(1), where Net is net tax over the horizon at declaration ratio alpha and TW(1) is the tax wealth change at honest declaration (alpha = 1). The tolerant zone is the alpha range where |C.1| < 2 percentage points | TW(1) (author, 2026-11-16; v1 error B1) | percentage points |

## Path metrics (needed to produce M1 and M4)
| ID | Name | Definition |
|---|---|---|
| P1 | Reserve fill years | Years until the short and the long reserve reach their targets (3 times the trailing mean annual refund each; v2 medians 3 and 7 on UK windows) |
| P2 | Relief available | R_t = M1a + M1b + M1c; retires taxes in the stated order |
| P3 | Cumulative shortfall | Sum over years of any year in which retired receipts exceed revenue; must be zero under staged retirement, reported to prove it |
| P4 | Sustainability | Two numbers per draw: the long-term M1 divided by the short-term M1, and the first year after the fill in which M1 is below zero (never, if it stays non-negative). A ratio well below 1, or a year below zero, means WDT does not hold up as a revenue source at that schedule, unless P6 shows public wealth rising enough to carry the difference (see the reading rule above) |
| P6 | Public wealth path | The fund's assets (long and short reserves and the remainder) as a share of GDP at years 10, 25, 50 and 100. Read with P4 so that revenue falling while public wealth rises is not mistaken for failure |
| P5 | Retirement schedule | The year in which each of the six taxes is retired under the stated order and trigger (M1e) |

## Added metrics (integrated 2026-11-17 from briefs 014g, 015g, 016g)
Source files with the full reasoning, flags and research requests: `docs/model-v3/added/h1.md`, `welfare.md`, `supporting.md`. This file is the definition; those files are the working. Provisional ids of 014g and 015g were renumbered: MH1a, MH1b, MH1c are M10 (dropped), M11, M12; MW1, MW2, MW3a, MW3b are M13, M14, M15a, M15b. Author answers of 2026-11-17 are applied below.

### Problem metrics (hub section H1)
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M10 | (dropped 2026-11-17) Top-q share of adult net wealth | Dropped by the author: the concentration path needed returns that rise with wealth rank, and 022r found no UK evidence for that. The id is not reused. DH1a still gives today's shares and history as a data fact | | | |
| M11 | Worker's average tax rate | (Income tax plus employee NICs) divided by gross earnings, at median full-time earnings, current rates and thresholds | gross earnings | % | one year of the data pack |
| M12 | Escape share | Present value of the gains never charged to CGT over a payer's life (unrealised at death and uplifted, held in exempt wrappers, inside the annual exempt amount, or relieved) divided by the present value of gains accrued, by wealth band. Reported in two lines by cause: deferral then uplift at death, and exempt by law | PV of accrued gains | % | one life, G = 30 |

Views of M3 on today's system (OH1b): **M3-today** is M3 with the tax system set to today (CGT and IHT paid over the life, income tax in both numerator and denominator system as today); **M3-all-tax** adds income tax on investment income to the numerator. The headline claim rests on M3-all-tax with M3-today beside it, so the gap against a worker's rate (M11) is not overstated. IHT falls on estates, not gains; including it in a rate on gains is a convention, stated beside the number. Both are reported once, not per WDT schedule, because today's system does not depend on it.

### Welfare metrics (spoke S6-B)
All are read off the same v3 run as the headlines: the same return paths, schedules and windows. They need payer-level paths (return, wealth, tax and refund ledger).
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| M13 | Certainty-equivalent welfare cost, by tax system | For payer i, CEW_i(s) = E[U^-1(W_N,i(s))] / E[U^-1(W_N,i(none))] - 1, with U the CRRA utility of terminal wealth under system s and the no-tax run on the same paths as benchmark. Systems: the v3 WDT, income tax and CGT on the realised-gain base, a stock wealth tax and **a consumption tax (kept as a comparator, author, 2026-11-17: the WDT's main intellectual competitor)**. Each comparator rate is solved so its expected revenue equals the WDT's, on the same payers and paths. Reported overall and by wealth band; the headline is the difference to the WDT. **Risk aversion is sampled at level 2** (author default), its range from 024r. Behavioural response applies equally to all systems | no-tax certainty equivalent | basis points; difference in basis points | one life, G = 30 |
| M14 | CGT lock-in cost | The CEW of a payer holding asset A with embedded gain ratio g who can switch to asset B, under CGT with realisation on switching, minus the CEW of the same payer with the switch tax-neutral. Also P(locked in), the share of paths where CGT blocks the switch. **Produced by a post-processing module over the v3 payer paths** (author default: option b), using v3's draws; not a separate model | tax-neutral switching certainty equivalent | basis points; share of paths | remaining holding period, one life |
| M15a | Envelope binding | Slack_i,t is cumulative net tax paid by payer i to year t minus cumulative refunds received. The envelope binds when a refund due exceeds slack. Reported: share of payers for whom it binds at least once; the first year it binds; refunds forgone because of the cap as a share of refunds due; by entry year and by return tier. **This output holds the envelope only; concentration is not an output (M10 dropped 2026-11-17)** | payers; refunds due | % of payers; year; % of refunds due | transition, short, long |
| M15b | Aggregate liquidity timing of the cap | Refunds the short reserve would owe in the first N years without the cap, minus refunds with it | GDP_t | % of GDP | transition |

### Supporting metrics
| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| B1a | Payers | Adults whose net wealth at the start of year t is at or above W_min | adults | millions; % of adults | transition, short, long |
| B1b | Entries | Payers in year t who were not payers in year t-1 | payers at the start of t-1 | % per year; count | as B1a |
| B1c | Exits | Payers in year t-1 whose net wealth at the start of t is below W_min | payers at the start of t-1 | % per year; count | as B1a |
| B1d | Fall-through refund volume | Refunds paid in year t to adults who were payers in t-1 and are below W_min at the start of t (capped by tax paid, as M1a). A split of M1a, never added to it | GDP_t | % of GDP | as B1a |
| P7a | Reserve insolvency share | Share of level-1 paths in which the long reserve reaches zero in at least one year after the fill | return paths | % of paths | short, long |
| P7b | Minimum cover | Over the years after the fill, the minimum of the long reserve divided by its P1 target; mean over paths with the P10 beside it | the P1 target | ratio | short, long |
| M7c | Declaration curve | C.1(alpha) = (Net(alpha) - Net(1)) / TW(1), the M7 formula at every alpha on a grid | TW(1) | percentage points | the M7 horizon |
| M7d | Lost refund protection | (Refunds(1) - Refunds(alpha)) / TW(1): the part of M7c that is refunds forgone because declared wealth is understated; a split of M7c | TW(1) | percentage points | as M7c |
| M7e | (dropped 2026-11-20: see 080r) | Not produced; the id is not reused | | | |
| M9 | Net fiscal effect after migration | M9 = M1 - X, where X is the income tax, NICs and VAT lost from people who leave UK tax residence in response to the tax. X is reported on its own line | GDP_t | % of GDP; real pounds | transition, short, long |
| M4c | Non-payer saving, pounds per month | M4c(y) = M4b(d) x y / 12 for a reference worker with income y in decile d. A derived view of M4b; no price pass-through beyond the incidence inputs already in M4a and M4b | none (a level) | pounds per month | transition, short, long |
| F1 | Closure share | For one schedule and threshold, the share of level-1 return paths in which P3 equals zero | return paths | % of paths | transition, short |
| T1 | Tornado swing | For headline h and input j: h(j at Low) - h(central) and h(j at High) - h(central), every other input at central, ranked by the larger absolute swing. **Headlines: M1, M2, M4a and M3** (author default). Run at each named schedule; the 0.5-point cut-off of tier 2 is applied to the M1 swing | the headline's own | points of GDP for M1; percentage points otherwise | transition, short, long |
P7 differs from P3: P3 asks whether retired receipts ever exceed revenue; P7 asks whether the reserve runs out. Both are reported. The understater plateau is read off M7c with a tolerance fixed in model stage C. F1 and the feasibility map use a share, burden cap and saving floor fixed in model stage C (OF1).

### Check (a test of the model, not an output)
| ID | Name | Definition |
|---|---|---|
| CK1 | Synthetic cyclical stress test | On a fixed path g(t) = mu + A sin(2 pi t / T), report P1, P3 and P7b for each amplitude A on a grid. Pass: P3 equals zero up to a stated amplitude. **mu comes from I-D1a (central 4.42%), not the old 7%; the grid runs to about 12%**, because a sinusoid of amplitude A has a standard deviation A over the square root of 2, so matching the historical 8.2% needs A near 11.6%. T is 10 years, a fixture. Cited in S12 as evidence; no range, so not in the manifest's outputs |

### Data facts (hub H1; not model outputs)
Held in the manifest with `kind: data_fact` so R1 and the hooks cover them.
| ID | Fact | Rule |
|---|---|---|
| DH1a | Top-1% and top-10% share of adult net wealth, and wealth to GDP, now and over time | The shares are today's values and history from the data (the concentration path M10 is dropped). **Wealth to GDP is stated on the survey basis (I-D4a, 5.8 to 7.5) with the national-accounts figure (I-D4g, 3.6) named as a cross-check; "top 10%" is stated on one named basis** (author default, 2026-11-17) |
| DH1b | UK tax mix by head and by group | Receipts as % of GDP and of receipts, grouped labour, consumption, capital and wealth, from the held IFS sheet; the retired heads read the same figures as M1e (primary source central, IFS cross-check). The labour group is an upper bound because the sheet does not split income tax into earnings and investment income; say so beside the number |
| DH1c | Tax bill of non-payers by income decile | The M4a denominator as a share of income and in pounds, with the retired taxes as their own part; deciles as defined under M4a |

## Closed on 2026-11-16 (author)
Reporting windows: short and long term both (see Horizons). Retirement order: a policy input, probably a Phase One governing-council decision. M2: revenue-weighted. Discount rate: as defensible as possible (Green Book schedule). Non-payers: by income decile. Comparisons: Zucman global minimum and UK proposals of about 2%.

## Confirmed on 2026-11-16 (author, "confirm all")
1. Window cut points: transition to the long-reserve fill; short term the 10 years after it; long term the mean of years 51 to 100 and year 100.
2. Default retirement order: ascending by receipts.
3. M2 as revenue-weighted, with the check against the RATES paper's 0.35% kept as an open check (writing or research lane).
4. Life length G = 30 years for M3.
The retirement trigger, the named-schedule choice rule and the 0.5-point tornado cut-off were confirmed on 2026-11-16 (stage A2).

## Closed on 2026-11-17 (author)
- **M2 denominator: same year.** W_i is the payer's net wealth at the start of the year the tax is charged, as the M2 formula already says. The RATES 0.35% divides by terminal wealth (30 years on) and is a different quantity; the two are not compared and RATES' claim that the burden stays below 1 to 2% of stock levies is re-derived on M2 when v3 runs (012r check: terminal 0.39%, crude path average about 1.2%, starting wealth 4.08%). The 012r M2 open check is closed.

## Closed on 2026-11-17 (author): added outputs
Defaults accepted: M3 gains as the real change in net wealth; M4a deciles of all adults with non-payers inside; OW2 as a post-processing module; risk aversion sampled at level 2; the envelope output separate from concentration; the stress test a check; tornado on M1, M2, M4a and M3. Not default: the consumption tax stays as a comparator in M13.

## Contract amendments V3-0 (2026-11-18, brief 045g)
Manifest `stage-V3-0-contract-2026-11-18` applies `architecture.md` 8.1: `by` vocabularies for OW2, OB1, OD1, OL1, OF1, OT1 and CK1 (A1, A2; the OT1 `input` list is the tier 1 register rows with a low and a high, derived inputs I-D1a2 and I-D1a0 excluded); `line_horizons` for OW3, with M15b transition only (A3); own-net lines M1 on O1 and M9 on OM1 (A4); `feasibility` constants: closure share 75% of paths, M2 cap 2.0% a year, M4a floor 0% (A5, author, 2026-11-18); run fields `pack_sha256`, `pack_country`, `levers_sha256` (A6). No metric definition changes.

## Closed on 2026-11-20 (author), after 053c
- **M2 is reported twice.** The headline M2 is the burden **in life** (net WDT of the year without death flows), comparable with the annual comparator taxes of M5; M2d is the same metric **including the settlement at death** (death assessments and heirs' assessments), labelled so. Death flows are 87% of M2 on the 117 windows (22.2% a year with them, 2.8% without), so the two readings must never be shown unlabelled. M5's difference is computed on the in-life reading, with the with-death difference as a second line where the output form allows. Manifest entry O2d: brief 079g.
- **M3 gains** are the positive real changes in net wealth (as M12): the signed sum is zero or negative over many lives and gives no rate.
- **M4a incidence is a stated limit of the pack:** a tax's share is held only for the top decile and the bottom five; the rest split evenly, corporation tax follows gross income, the two payer-side taxes give non-payers nothing, and there is no joint income and wealth table.
- **Limits of the first run (not built, data not held):** the all-tax line of OH1b; the non-payer saving form of M8; M2b and M2c for lines below W_min; and M5 and M8 test thresholds on line means, so only the Rich List tiers pass the large thresholds. Revisit after the first provisional run.
