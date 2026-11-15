I'll load the WDT guru skill, then go through the refactored RATES and VAL results against what the papers currently claim.

The two refactors point the same way. The old papers claimed more than the new models support, and in both cases the old result was driven by a static or favourable assumption that the refactor removed.

## RATES

**The headline has changed from replacement to partial funding.** The new median is 23% of reference expenditure (p10 to p90: 9.6% to 42.5%), falling to 14.9% without the corporate levy. The UK's own history gives 16.6%. The "today-like" slice gives 14.2% of today's expenditure, or 9.4% without the levy. The base would need to be about 4× larger (median 3.97) to replace current revenue, and only Finland is close. Compare the old figures: a 125.5% TCM median and a combined pre-behavioural estimate at "near-parity" with TME.

Two things probably explain the gap, and both are worth checking in the old code:
- **Base growth.** The old model compounded all wealth at 10.45% nominal against expenditure growing at 4.51%. If GDP tracks expenditure, that implies wealth/GDP rising roughly 5× over 30 years. The new model has c = 3.5% consumption, and its median drift is 0.80, with a 0.41 to 1.39 range at p10 to p90.
- **Time basis.** The £874b "lifetime average" was compared with the £1,157b base-year TME. Expenditure reaches about £2,560b by year 19, so a like-for-like comparison is probably nearer 40% than parity.

The old worst case (6 to 15%) is about where the new central estimate sits for the UK today, so the old floor survives and the old median doesn't. The new c = 3.5% is close to the stationary value (3.63%), which makes it a defensible central case. Even so, c = 1% gives 37% and c = 5% gives 17.5%.

**The package is smaller than LDW assumes.** Relief of 8.5% of GDP retires CGT, IHT and corporation tax (4.0% of GDP) and then funds a median allowance of about £23.5k. That is far from full income-tax displacement, and mean saving is about £2.7k, not £618 a month. LDW's £43k purchasing-power figure sits at or beyond the top of the lever stack (£41k).

**The taxed population is much larger than the papers assume.** Tying W_min to the median house price (£225k) puts 19.4m adults in scope, which is 36% of adults holding 85% of wealth. About 74% of receipts come from the £0.25m to £5m bands, and only about 14% from above £25m. This conflicts with several premises:
- WP §3.4's "small high-threshold population".
- JUR's 32,000 individuals.
- TP as a small chamber (19.4m members would be TP).
- The concentrated-versus-diffuse Olson logic in POL.
- Liquidity, which becomes a mass-homeowner and pension problem on Routes A/B/D rather than a UHNW one.

On the other side, 88% of adults come out ahead, and only 6.5m are in net-loss bands.

**Heir receipts are a third of the revenue.** They contribute 15.85% against 18.12% from holding-year tax. Untaxing them drops net receipts from 32.7% to 21.4%. Billionaire cells pay a mean 2.77% a year, falling to 0.85% without heir receipts. This effectively implements SCOPE #33, but the lumpy, death-timed revenue is now load-bearing for fund fill, so CLOSE and the Route D inheritance auction carry more weight than the papers give them.

**The burden claim is weaker.** Payers bear 1.01% of wealth a year, and the top 0.1% bear 2.62%, against the old 0.35% revenue-weighted figure and 0.79% maximum. "Below a 1 to 2% stock levy" holds on average but not at the top.

**The corporate levy is more circular than it looks.** It supplies 8.2pp of the 23.1%, and its tau0 of 47.2% is solved so that it raises exactly corporation tax. The statutory versions (tau0 3.8%, f_inc 2 to 20%) add only 1.2 to 4.5pp. Treat the headline as "with a levy that replaces CT", not as something the individual tax delivers.

**Smaller points:**
- Table 13's note says fill is "much rarer without the levy", yet every censored share reads 0.0%. One of the two is stale.
- Fail share is now 0.3% (PRT 9.1%, FRA 1.2%, ESP 1.9%), so "never fails" can't stand as written.
- Median fill year is 6 to 7. That needs mapping onto the old SRR (3) and LRR (13) structure, since I can't tell whether "fund fill" is one reserve or two.
- Period-block bootstrap intervals are wide (17.3% to 29.8% on the central case), with only 14 to 28 effective windows.

## VAL

**The refactor breaks the "dissolved" claim.** The old analysis tested constant declaration ratios. The new 428-strategy library includes time-varying ones such as late deviation and correct-before-death. Against those, no rule set passes the 1.0% best-response test at canonical growth for any verification hazard λ up to 10%. The full rule set (value cap, verify-down reset, auction) gives 15.0%, 9.8%, 6.5%, 2.6% and 3.5% at λ = 0, 1, 2, 5 and 10%. BRG passes only when g ≤ 7% and λ ≥ 5%, and higher growth makes it worse, the opposite of the old "more costly at high growth" story. The reason is that dilution cost needs time to accrue, and a late deviation never gives it that time.

The defensible reframing is "bounded, not dissolved". At α = 0.1 the conventional self-declared comparator gains 600.7%, against 15.0% (λ = 0) and 1.7% (λ = 5%) under the full rule set. That comparator models no audits, though, so it is a generous foil.

**Which levers matter:**
- The value cap takes the λ = 0 gain from 81.8% to 15.0%.
- The verify-down reset (no refund on a verified correction) is what makes λ bite. Without it, overstatement plus verification yields 16 to 17% at any λ. This extends VAL §11.3's corrective no-refund rule to Route C.
- Auction "on" is never better than "off" on BRG, and is worse at λ = 1% and 10%. Something in that arm is exploitable, and it needs explaining before VAL §11 can lean on it.
- Route D reset cadence matters a great deal. With no resets, understating D gains up to 6.9%. The baseline assumes a reset every 10 years, which isn't in the settled design (voluntary, corrective or inheritance only).

**Conflicts with settled VAL text:**
- Route C is described as needing no audit and having no auction backstop, yet λ is an audit-like verification hazard. Reaching 90% verified takes 45 years at 5%, and λ = 2% never gets there within the 100-year horizon.
- The old mild-overstatement result (nominal timing artefact, NPV-reversed) conflicts with LGR and LNS, where α = 1.5 gains about 17% and α = 2 about 33% single-life. Either the ratio-mirror engine really changed the economics, or the table needs more explanation.
- Rule-set "reset" and Route D "reset interval" are two different things sharing a name.

**What survives:** static results, honest valuation error not paying (the full rule set at λ = 5% shows about zero cost at sd ≤ 10%), and state PV exposure staying within ±3% in the static grids. The honest-family shock cost is 0.000% everywhere, but that's tautological because honest declaration means verification plays no part. A meaningful HSC test would use honest error plus a shock.

**A candidate fix to test:** a mandatory Route C verification at closure events (death, sale, exit) in place of a random hazard. That would target exactly the late-deviation family, and it fits CLOSE's unified-closure logic.

## Things I'd check

1. What exactly do "fund fill", "fail" and "auction on" encode in the new models?
2. Why does Table 13 say censoring is high while the censored shares read 0.0%?
3. Do the UCC benchmark rows (α = 0.1 at +13.7%) and LGR (−21.8%) use different parameters or sign conventions? I also couldn't reconcile the WLG terminal-wealth row from its component rows, so a "retained units × V" row would help.
4. Table 23's placeholder revenue (40.4%) doesn't match JUR's 36.1%.

Where do you want to go first? I'd start with the implied wealth/GDP drift in the old model, since that decides how much of the RATES downgrade is correction versus new information.