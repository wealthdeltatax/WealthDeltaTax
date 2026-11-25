# VAL Generational Model — Plan (v0.6, 1 October 2026)

Status: design settled except the items in §9 (updated after the user's further replies of 1 Oct). No code written.

**Changes in v0.6** (design discussion, 1 Oct): D6 reworded (heir influx is not a special transaction); D16 extended (consumption earns a refund); new D17–D20 (delta definition, lending, unverified Route C, gifts); new metrics for the verified share of Route C wealth and an illiquidity-discount switch; new checks 10–11; D9 note (λ exogenous, eventual failure or realisation); §9 items 5, 10, 11; §10 additions. This plan replaces the single-life, sale-at-N frame of the current `val_core` (v1.2).

---

## 1. Why rebuild

The current VAL model follows one taxpayer for N = 30 years, then sells. Three things in that frame mislead:

1. **The sale is a verification event.** At sale the declaration drops out and the true value appears. It caps understatement and triggers a cash refund for overstatement. Neither happens at death under the settlement rules below.
2. **Everything is one asset class (Route C), one strategy (constant α), one life.** Real families hold A/B/C/D, die, and pass a stock to an heir.
3. **The metric was inconsistent.** PV was divided by a terminal amount (fixed in v1.2: tolerance is now % of honest PV revenue).

Evidence already in hand (all N = 30, g = 10.45%, τ₀ = 15%, τ_m = 70%, V₀ = £20m):

| Finding | Number |
|---|---|
| Wedge identity at α = 2 (ρ = 0): credited holding tax 90.2, true value surrendered 45.1, sell-year cash refund 44.2 | State revenue 8.0 vs honest 45.3 (−82%) |
| TW gain vs honest is flat in N | +10% (N=5), +12% (N=10–20), +11.4% (N=30), +7.2% (N=50) |
| Taxing the year-1 step-up (honest entry basis, then declare α) | +11.4% falls to +4.7% |
| No verification ever (no sale, no write-down), constant α, family stake vs honest, N = 90 | α=0.1: +109%; α=0.5: +25%; α=2: −20%; α=5: −40% (see caveat: wealth reaches £150bn, where τ ≈ τ_m) |
| Same, flat 15% rate, no threshold | Family stake is **identical for every α** (0.685117 at α = 0.1 … 5.0) |
| Same, N = 30, actual rate function | α=0.5: +1.4%; α=0.1: +2.5%; declared-W floor at 75% of V (A/B honest): +0.7% |
| Envelope in real value paid (E2) vs credited (E1), cash refund at sale, N = 30 | α=1.2: +2.4% both; α=2: +11.4% both; α=5: +40.5% → +6.7%. E2 only binds at large α. |
| Route C refund unit, α = 2, N = 30 (TW gain): cash at true value / units, same proportion of units paid / units valued at the price paid | +11.4% / +20.4% / +5.0% |
| Same, α = 1.2 / 1.5 / 5 | cash +2.4 / +5.9 / +40.5; pro-rata units +5.5 / +13.5 / +22.9; price-paid units +2.1 / +3.9 / +0.8 |
| **Ratio-mirror refund** (units; refund fraction of holdings = τ × (1 − p_new/p_old), mirror of payment fraction τ × (1 − p_prev/p_new)), N = 30. Family TW gain: α = 1.2 / 1.5 / 2 / 5 / 10 | +2.2 / +4.2 / +5.5 / +1.6 / −9.1 (legacy cash: +2.4 / +5.9 / +11.4 / +40.5 / +77.3) |
| Same, state terminal value vs honest (ρ ≈ g) | −4.3 / −8.1 / −10.7 / −3.0 / +17.5 (legacy cash: −4.6 / −11.3 / −22.1 / −78.2 / −149.1) |
| Same, honest family refund on a genuine sale-year fall of −20% / −50% | 7.85 / 11.07 (legacy cash 9.96 / 22.48) |
| Decomposition, α = 2 vs honest, N = 30 (£m): holding payments (true value) / sell-year tax(+) or refund(−) / post-sale settlement / TW before settlement / TW settled | honest 41.6 / +4.4 / −0.7 / 286.2 / 286.9; α=2: 45.1 / −44.2 / +7.1 / 326.9 / 319.7 |
| Post-sale settlement claws back 16.1% of the refund | TW gain +14.2% before settlement, +11.4% after |
| One-off delta of 100 on an empty envelope (the settlement oscillation) | net tax 14.0 (first flows 16.2, −2.6, +0.4, −0.07 …); converges in about 3 years |
| τ(W) at £2m / £20m / £100m / £1bn / £10bn | 15.0% / 15.2% / 16.2% / 29.8% / 70.0% |

Reading:
- **Payment in kind makes level misdeclaration neutral.** The tax base moves with α, so L = τ·αΔV, while the equity fraction handed over is q = L/(αV) = τΔV/V, independent of α. Understating does not hand over more equity per pound of V; the tax base shrinks by the same factor. What survives is the **rate progressivity** τ(αW) and the **exemption cliff** W_min. Both are bounded by the route mix: A/B are declared at α = 1, so total declared W cannot fall below the A+B share of V.
- **Overstatement pays only through a refund on a later write-down.** Payments are in kind at the declared price; the refund returns credited pounds in cash. Counting the envelope in real value paid (E2) bounds the refund but does not remove the gain at moderate α, because the refund can still recover almost everything paid (α = 2: refund 44.2 vs real value paid 45.1), leaving net tax near zero against the honest family's positive tax. The lever is **which losses are refundable**, not the envelope unit.
- **τ(W) is close to τ₀ for ordinary wealth** (≈15–16% up to £100m). The 70% region is reached only at £bn+, so the long-horizon results in §1 reflect wealth compounding unchecked. Dynastic runs need consumption and heir splitting (D16).

## 2. Goal (formal)

For every declaration strategy σ, compare the family with an honest family:

- **G1 — bounded gain.** Gain(σ) = family terminal net worth under σ minus honest. Honest is the maximum, or the maximum lies in a narrow band around α = 1 (the mild-overstatement equilibrium). Both over- and understatement must be unattractive.
- **G2 — bounded consequences.** An honest error, or a market that reveals a different value, never ruins a family. Penalties scale with the error.
- **G3 — bounded state loss.** Wherever Gain(σ) > 0, the state's PV loss is within the tolerance (default 2% of honest PV revenue; sensitivity 5%, 10%).

Deliverable of the model: the payoff curve Gain(α_C, α_D) by route mix, rule set and verification hazard, and the set of rules under which G1–G3 hold.

## 3. Settled design decisions

| # | Decision | Source |
|---|---|---|
| D1 | Route A and B: α = 1 always (professional valuation). Settled in cash at true value. | user |
| D2 | Route C: self-declared fungibles. Periodic tax paid in kind at the declared price. No auction, no verified basis, except at a **verification event** (D9). | user |
| D3 | Route D: no periodic payments. Settlement at realisation. A **voluntary hard reset every 10 years** (auction, verified basis). Inheritance auction at death unless the death-auction waiver applies. | user; CLOSE §4.1.1 |
| D4 | Death, Route C: settled at the **last declared value before death**. No estate-managed final declaration. Delta from last assessment to death = 0 for Route C. Consequence: the heir's basis is the same declared value, so an unverified Route C stake can pass down unverified until a verification event (see D19). | user (1 Oct) |
| D5 | Death, Routes A/B: professional valuation at date of death. Delta from last assessment to death taxed on the deceased at τ(W_death). | CLOSE §4.1 |
| D6 | Heir receives the estate **after tax**. The influx is not a special transaction: it is simply a rise in the heir's net worth between two assessments, taxed like any other delta (in kind for Route C) at the heir's rate. Heir's basis for each asset = the previous owner's last declared value (Route C), the valuation at death (A/B), or the auction price (D). The effective rate is τ(W_heir), which is ≈ τ₀ for ordinary wealth. CLOSE §4.1 needs updating to match. | user (1 Oct) |
| D7 | Delta is on **total declared net worth** of the individual (MF §2), netting across routes within an assessment. Rate τ(W) on total declared W. | existing model; MF §2 |
| D8 | **Refund: symmetric, at the realisation event, in the same manner as the tax was paid** (in kind for Route C, proportional to the tax or refund owed), bounded by the lifetime contribution envelope counted in the real value paid (E2). Symmetry is a cooperativeness and non-extractiveness commitment, not a parameter. No oracle: the rule cannot depend on judging a loss as genuine or manufactured. Baseline refund rule for Route C: **ratio-mirror** — the refund is a fraction of holdings equal to τ × the fractional fall in declared value, the exact mirror of the payment fraction τ × (1 − p_prev/p_new), returned in units from the state's stake and capped by the units paid. It is currency-free. Cash at true value, units at the price paid, and pro-rata units run as switches (§4). | user (1 Oct) |
| D9 | **Verification event** on Route C: Poisson hazard λ per year (IPO, funding round, sale, marking of the state's stake). The family does not control it. Settled (1 Oct): a holder may avoid verification during their own lifetime and keep what they have; nobody controls it after death, and the stake eventually fails (nothing owed beyond the declared basis, which is zero in the limit of full understatement) or is realised, within or beyond the owner's life. λ stays exogenous. At the event the declared value is replaced by the true value. Upward correction = positive delta, taxed. Downward correction = symmetric refund, bounded by the envelope. | proposed here |
| D10 | Envelope is a property of the individual. Heirs start with a clean envelope. | CLOSE §4.1 |
| D11 | Family is one coordinated decision-maker maximising **total family terminal net worth** at horizon T, in true (economic) value. | user |
| D12 | Horizon T = 100 years. Generation gap G = 30 years (deterministic baseline). Random mortality is a sensitivity. | user; baseline proposed |
| D13 | Route shares of WDT-taxable wealth (BEHAV): A 40–55%, B 20–30%, C 5–10%, D 10–20%. Baseline **A 50 / B 25 / C 8 / D 17**; sweep the ranges. | BEHAV (user) |
| D14 | Ground truth is the economic value V. The tax system sees only declared values, except at verification events, resets and professional valuations. Outcomes are always measured in true value. | design |
| D15 | State outcome measured two ways: PV of true value received at ρ (headline 5%, sweep to 25%), and the SWF's terminal stake at T (ρ ≈ fund return). Shortfall always as % of honest PV. | v1.2 |
| D16 | **Steady-state wealth.** Wealth per family cannot compound unchecked for 100 years. Baseline: nominal returns, W_min indexed at `budget_growth` (4.51%), family consumption c = 2–5% of net worth per year (baseline 3.5%), one heir per generation (2 parents, 2 children). Parameters in TOML. Consumption is a fall in net worth and enters the delta (D17). | user (1 Oct), index proposed here |
| D17 | **Delta is the pure change in each individual's net worth, however it arises.** Transactions are not examined. Consumption is a loss of net worth and earns a refund, bounded by the lifetime envelope. A gift gives the giver a refund and taxes the receiver, each at their own τ(W); gifts and transfers are not taxed as such. Consequence: the base is net accumulation (income less consumption, less tax), not gross return. | user (1 Oct) |
| D18 | **Lending is not a verification event** and is not modelled. A loan nets to zero delta (cash in, liability out). Lenders value collateral themselves; the WDT does not use lender valuations to update the basis (VAL §3.3). Any pressure on families to declare Route C honestly from existing lending practice is real but lies outside the WDT and the model. | user (1 Oct) |
| D19 | **Unverified Route C is treated as having no usable value until realised.** Cash income or dividends it generates is recorded as Route A and taxed as normal. Long-term steady-state goal: assets get verified over time. λ is read as a sensitivity on how long the WDT must run before steady state. | user (1 Oct) |
| D20 | **Gifts and wealth-splitting through τ(W) are accepted** as redistribution under the guise of tax saving, net positive for the country. No gift or transfer strategy axis in the baseline. | user (1 Oct) |

## 4. Mechanics

**State per family member:** holdings by route (units, declared value, true value), cumulative envelope (credited and received), last assessment date, bases.

**Annual assessment (every member alive):**
1. Update true values by route: V_r(t) = V_r(t−1)(1+g_r). Baseline g_r = g for all routes; route-specific g is a sensitivity.
2. Declared values: A/B = V; C = α_C · V (strategy); D = last declared or reset value, revised by the strategy between resets.
3. Total declared W = Σ declared. Total delta Δ = W − W_prev (net of units paid). Δ is the pure change in net worth (D17): consumption and gifts out enter as negative deltas; gifts and inheritance received as positive.
4. Tax L = τ(W)·Δ if Δ > 0 (or refund max(−cum, τ(W)·Δ) if Δ < 0, bounded by the envelope).
5. Allocation of L across routes by each route's delta share:
   - A/B: paid by transferring units at true value.
   - C: paid in kind at the declared price: fraction q_C = L_C / W_C, true value surrendered = L_C / α.
   - D: accrues, no payment until a settlement event (reset, death, sale).
6. Envelope credited with L (credited units).

**Ratio-mirror property.** A price that rises by x pays τ·x/(1+x) of the post-gain holding; a price that falls back by the same ratio refunds τ·x/(1+x). A round trip up and back nets (almost) zero tax, in units, whatever the declared price level. The extractable amount per unit of fictional write-down is bounded by τ × holdings.

**Settlement oscillation.** The rule "delta = change in after-tax net worth, symmetric refund on a negative delta up to the envelope" means a tax payment lowers next year's net worth, so next year's delta is negative and part of the tax comes back (at rate τ), and so on. A one-off delta Δ nets about τΔ/(1+τ) of tax and the flows damp by about −τ a year. This is intrinsic to the rule and stays. What goes is the legacy *device*: iterating the oscillation to convergence at a single instant after the sale, as if the taxpayer lived on in cash. In the generational engine the heir's years run explicitly (the damping is visible within about three assessments). The legacy `settle_tw_flows` is kept only for the P1 bridge test.

**Events:**
- **Route D reset (every 10 years):** auction reveals true value V_D. Settle the accrued delta at τ(W_total at reset date). New declared = auction price. Refund on a downward correction follows rule switch R_D (below).
- **Route C verification (hazard λ):** as D9.
- **Death (every G years):** estate settles per D4/D5 and the D3 auction/waiver. Tax first, then heir. Bonds (closure bond facility, CLOSE §5) are timing instruments only and are not modelled.
- **Heir's first assessment:** influx declared at inherited bases; delta = influx; tax at τ(W_heir total) paid in kind (C), cash (A/B), accrued (D).

**Rule switches (all in `WDT_Params.toml`, compared pairwise):**

| Switch | Values |
|---|---|
| R_C write-down refund | symmetric cash (D8) · carry-forward credit only (no cash) |
| R_D reset refund | symmetric (VAL §11) · none on downward correction against the family's own declaration |
| Envelope unit | real value paid (E2, baseline) · credited (E1, legacy) |
| Route C refund rule | ratio-mirror units (baseline) · units valued at the price paid · cash at true value · same proportion of the units originally paid |
| Mechanical haircut on large self-declared write-downs | none (baseline) · refund scaled by h(\|Δ\|/W_prev), h decreasing; oracle-free, but penalises honest large losses |
| Route C refund | cash/units · carry-forward credit only (oracle-free, but gives up symmetry for final losses) |
| Heir influx | taxed as a delta (D6) · fresh entrant at received value (CLOSE §4.1) |
| Death-auction waiver | period 0 / 5 / 10 years |
| Illiquidity discount on unrealised Route C at T | none (baseline) · haircut sensitivity (D19; conservative for G3, since it shrinks any understatement gain) |

## 5. Strategy space

Each is a pattern of declaration for each route, held across the family's horizon:

- **Honest:** α_C = α_D = 1.
- **Constant over/understate:** α_C ∈ [0.1, 10], α_D ∈ [0.1, 10], log grid, incl. α = 10 on a slice (route-mix dilution test).
- **First-generation only:** deviate during generation 1, honest afterwards.
- **Dynastic:** same deviation every generation.
- **Timed:** overstate in the final k years before death; understate early then correct before a verification or reset; understate in the years before a reset.
- **Reset gaming (D):** declare high before reset, low after.
- **Mixed:** C and D together.

The family chooses the strategy that maximises terminal net worth. Output is the best response and the full payoff surface, not only the maximiser.

## 6. Metrics

| Metric | Definition |
|---|---|
| Family gain | (TW_family(σ) − TW_family(honest)) / TW_family(honest), true value at T |
| State shortfall | (PV_true(σ) − PV_true(honest)) / PV_true(honest), honest PV at the same ρ; NaN where honest PV < 0.1% of TW |
| SWF stake | State's true-value stake at T, vs honest |
| Worst honest error | Gain when the realised verification differs from the declaration by a stated error (G2) |
| Alignment | Share of (α_C, α_D) cells with Gain > 0 and shortfall > tolerance (conflict), vs Gain > 0 and shortfall ≤ tolerance |
| Per generation | Each of the above by generation, plus the first-generation transition cost, reported separately from the steady state |
| Verified share of Route C wealth | Share of true Route C wealth that has been verified (D9 event or realisation) by year, per λ; and the first year it crosses a threshold (default 90%). Reads λ as time to steady state (D19). |
| Net-accumulation base | Taxable base (sum of positive deltas) per year as a share of gross return, to compare revenue with the legacy v1.2 runs (no consumption) |

Time-value note (D8): cash now is worth more than cash later, so a state paid early and repaying later gains from time value alone. The existing results show that effect is swamped when the refund returns more real value than the state received; the model measures both.

## 7. Validation (conservation first)

1. **Conservation:** at every step, true wealth lost by the family = true wealth gained by the state (declared values differ, true values must balance). Fail the run if not.
2. **Bridge to legacy:** single life, all Route C, constant α, sale at N, E1 envelope, no deaths → must reproduce `_run_core` / `run_pair` for `tw_gap`, `net_pct` and `pv_rel`. Pure-move discipline: identical to 1e-9.
3. **Honest identity:** α = 1 on all routes gives zero gain and zero shortfall under every switch.
4. **A/B inertness:** A- and B-only families have zero gain for every strategy (α fixed at 1).
5. **Dilution check:** with C only deviating, the family gain scales with the C share (linear at small share); records the deviation from linearity from the bracket effect.
6. **Envelope cap:** refunds never exceed the envelope in the chosen unit; E2 never refunds more than the state received.
7. **Oscillation check:** a one-off delta on an empty envelope run through explicit annual assessments reproduces the legacy `settle_tw_flows` net tax (14.0 at Δ = 100, τ(100) = 16.2%) to 1e-6 after enough years.
8. **λ → 0 limit** reproduces the no-verification result in §1 (understatement wins).
9. **Determinism and seeds** for Monte Carlo variants.
10. **Consumption identity:** a family whose consumption exactly offsets growth and tax (net worth flat) has zero delta every year and pays zero lifetime tax. With consumption below that, lifetime net tax is non-negative (envelope).
11. **Gift conservation:** a gift moves true value from giver to receiver with no loss; with equal τ and an unbinding giver envelope, giver refund and receiver tax net to zero.

## 8. Architecture and build order

Layout follows the repository hierarchy (TOML → `wdt_core` → one core → JSON → presentation).

| Layer | File | Notes |
|---|---|---|
| Params | `WDT_Params.toml` `[val_gen]` | route shares, T, G, reset interval, λ grid, switches, α grids, tolerance levels. Nothing hardcoded. |
| Base | `wdt_core.py` | keep `tau`, `load_params`; promote anything a second core needs. |
| Core | `valgen_core.py` (working name; becomes `val_core.py` at cutover) | ledger engine, route settlement, death/heir loop, strategy search, validation harness, writes `OUTPUTS/VAL/val_data.json` |
| Presentation | `{n}_2_VAL_tables.py`, `{n}_3_VAL_charts.py` (target naming) | read JSON only. Existing `5_3`, `5_4`, `5_5` stay until cutover. |

Build order, with a pass/fail check at each step:

1. **P1 — Engine for one life, one route** reproduces legacy (check 2). Add the double-entry ledger (check 1).
2. **P2 — Death and heir loop**, Route C only, rule switches for heir influx and envelope unit. Reproduces the no-verification table in §1 at λ = 0.
3. **P3 — Four routes** with A/B α = 1, D reset every 10 years, death auction/waiver. Checks 3–6.
4. **P4 — Verification hazard λ** on C; sweep. Check 7.
5. **P5 — Strategy search** and the payoff surfaces; alignment maps; G1–G3 verdict by rule set.
6. **P6 — Presentation scripts** and the paper rewrite against regenerated numbers (VAL, VAL.A, and CLOSE edits if D4/D6 stand).

Per step I report which layers changed, which numbers moved, and which tables/figures to re-run.

## 9. Open items

1. **Heir influx vs CLOSE §4.1 — decided (D6).** The heir pays tax on the influx as a delta at τ(W_heir), ≈ τ₀ for ordinary wealth. The estate taxes the accrued gain; the stock received is the heir's delta; not the same delta. CLOSE §4.1 needs updating (heir enters as a fresh entrant today). Heir's own pre-existing wealth H: baseline 0; sensitivity.
2. **CLOSE §3 vs §4.1 on Route C at death — decided (D4).** Last declared value. CLOSE §3 needs editing.
3. **Refund rule for Route C — unit decided, bound not yet.** The envelope counts real value paid; refunds are returned in kind at the price paid. Neither bounds the gain on its own: a flat-rate, no-growth example shows the refund units approach the units paid as α grows, so the cap and growth, not the unit, hold it down in the model at α = 5. The verified-loss rule is dropped (it needs an oracle). The remaining oracle-free levers, all run as switches in P5 and judged against G1–G3: the haircut on large write-downs, the carry-forward credit, and the interaction with λ. Decision after P5.
4. **Route D reset refund (R_D):** VAL §11.2/§11.4 keep symmetric refunds on voluntary reset; §11.3's no-refund correction applies only to egregious outliers via a corrective auction. Both run as a switch.
5. **λ for Route C:** no empirical anchor yet. Sweep 0–10% per year. Read as time to steady state (D19): report the verified share of Route C wealth by year and the year it crosses 90% (§6). Decided (1 Oct): λ stays exogenous (D9). A holder who never realises may keep what they have within their lifetime; the stake eventually fails or is realised, so avoidable and unavoidable verification need not be split.
6. **τ_h and CORP:** dropped from scope for P1–P5 (user).
7. **Units of g — decided from context:** nominal. `hist_mean` is the mean of the UK equity capital total-return series 1947–2019 (10.45%), `budget_growth` is explicitly nominal (4.51%), and ρ is nominal. The tier comments calling the tier returns "real" are labelled loosely (10.45 − 4.55 = 5.90 is plain subtraction). Real return ≈ 5.7% ((1.1045/1.0451) − 1). Consequence: over 100 years W_min (£2m, nominal, fixed) is not a real threshold. **Baseline: index W_min and the horizon's money to `budget_growth`** (legacy unindexed as a switch; the 30-year legacy results are unaffected within tolerance). Check on the series source still welcome but not blocking.
8. **Grandfathered entry for generation 1:** free declaration at entry (current model), with the taxed step-up as a sensitivity.
9. **Consumption and heirs (D16) — decided:** consumption rate c swept over 2%, 3%, 4%, 5% of net worth per year (baseline 3.5%); one heir per generation (two parents, two children, so each family line carries one heir). Wealth stays in the mid-range where τ ≈ τ₀ unless a run leaves it.
10. **Revenue base under consumption (D17) — to check.** The legacy single-life model has no consumption. At g = 10.45% and c = 3.5% the taxable base is roughly 7% a year, so generational revenue should be lower than v1.2 for the same α. Check whether RATES calibrates revenue on gross return or net accumulation (RATES not available in this review).
11. **Gift rate gradient — accepted (D20).** Giving down the wealth gradient can earn a refund at the giver's rate against tax at the receiver's lower rate; the A.3.2 current-W rule softens it and the giver's envelope caps it. Not modelled in the baseline. Revisit only if dynastic runs reach the steep part of τ(W).

## 10. Paper claims to revisit after P5

- "Advantage doesn't survive NPV / timing artefact" (legacy C.12 only).
- "Bracket effects deter overstatement" (refunded under E1).
- §4.3 "no auction backstop is needed or available" on Route C.
- §7.3 risk-aversion rationale for α ≈ 1.1.
- §11.2, §11.3, §11.4 refund and corrective-auction wording.
- CLOSE §3 vs §4.1 (Route C at death), §4.1 (heir basis, influx taxed as a delta at τ(W_heir)).
- Any description of the base as gross return: under D17 it is net accumulation, with consumption refunded within the envelope.
- Route C steady state: "assets eventually get verified" holds for Route D (auction at death) but for Route C only through the verification hazard (D4, D19).
