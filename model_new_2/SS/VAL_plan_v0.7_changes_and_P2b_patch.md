# VAL generational model plan: v0.7 changes (2 Oct 2026 design replies) and P2b patch notes

Apply to `VAL_generational_model_plan.md` (v0.6 → v0.7). Replacement text is given per section.

## A. Plan text changes

**§1 evidence table.** Flat-rate row: change "N = 90" to "N = 30" (the 0.685117 stake is reproduced at N = 30; the row label was wrong).

**D8 (unchanged in substance, add the caps).** Append: "Caps are separate and in the unit paid. Route C pays in kind, so its refund cap is the **units this individual has paid to the state** (net of units returned); it cannot be refunded cash or more units than it paid. Routes that settle in cash (A/B) keep the real-value envelope (E2). Heirs start with a clean units cap (D10)."

**D17 (add).** "Consumption is a sale of units to the market: it lowers the family's declared W and enters the delta like any other fall. It is not part of the family objective (D11 maximises terminal net worth only); cumulative consumption is reported as a diagnostic."

**D16 (add).** "Indexing is applied at the rate function: τ(W / I_t) with I_t = (1 + budget_growth)^t. This indexes W_min and scales k together, so τ(W) keeps its shape. Indexing W_min alone would steepen the curve."

**New D21 — allocation of L across routes (P3).** "L is allocated by each route's share of **positive** deltas when L > 0, and by each route's share of **negative** deltas when L < 0. Routes with a delta of the opposite sign take no part of the allocation."

**§2 G3.** Replace the tolerance sentence with: "G3: wherever Gain(σ) > 0, the state's PV tax revenue is within **±tol_rev of honest PV tax revenue** (two-sided; default 2%, sensitivity 5%, 10%). The state's interest is receiving about the right revenue; the family's interest is maximising TW." The legacy TOML `tol_pp` (2% of honest TW(1)) is a different, legacy definition; leave it for `val_core` and do not read it from `valgen_core`.

**§4 rule switches table.** Replace the three Route C refund rows (R_C write-down refund; Route C refund rule; Route C refund cash/units · carry-forward) with a single row:

| Route C refund rule | **ratio-mirror units, capped by units paid** (baseline, D8) · legacy (refund = τΔ/W_new, credited/real envelope; bridge only) · units valued at the price paid · cash at true value · pro-rata units · carry-forward credit only |

**§7 check numbering.** Check 7 (oscillation) belongs to P2b, not P4. Checks 8 (λ → 0) belongs to P4. Check 10 (consumption identity) belongs to P2b. Check 11 (gift conservation) is deferred with D20 (gifts not modelled in the baseline).

**§8 build order.** Insert after P2:
> **P2b — Consumption, W_min/k indexing, ratio-mirror refund, units-paid cap.** Checks 7 and 10, round-trip and cap checks, flat-rate α-free identity under every switch. Legacy settings (c = 0, no index, legacy refund) reproduce P1/P2 exactly.

P3 checks stay 3–6, P4 check 8.

**§9.3.** Replace with: "Route C refund — **decided (D8)**: ratio-mirror in units, capped by the units the individual has paid. Remaining judgement: whether the haircut on large self-declared write-downs is also needed. Decided after P5 against G1–G3."

**§9.10 (revenue base).** Add: "Net-accumulation base metric is specified in §6 but not yet built."

## B. Observations from the P2b run (scratch harness, plan parameters)

- **Oscillation (check 7):** one-off delta of 100 nets 13.957 of tax (first flows 16.19, −2.59, +0.41, −0.07), equal to legacy `settle_tw_flows` to 1e-9. The plan quotes this as 14.0.
- **Round trip, flat 15%, price +50% then back:** ratio-mirror returns exactly the units paid (f = 1.00000). The legacy refund rule returns f = 1.025, i.e. more units than were paid. This is the case the units-paid cap exists for.
- **P2b grid (T = 100, G = 30, W_min and k indexed at 4.51%, honest family):** at c = 3.5% the honest family ends with about 0.8% of the asset; consumption and indexing keep τ near τ₀ in real terms.
- **Constant-α runs barely distinguish the refund rules** (gain differs by under 0.1pp). Refunds only arise from heir years and consumption. The rules separate when declared values actually fall (P4 verification events).
- **α = 0.1 at c = 5% gains +92% with state revenue −50%.** This is the exemption cliff: declared W falls below the indexed W_min and tax stops. A conflict case for G3; it needs the route-mix floor (A/B at α = 1) from P3 before any conclusion.
- **Grid output label:** `V_T_honest` is the asset's value, not the family's net worth. Family net worth is f_T × V_T.

## C. `WDT_Params.toml`: replace the `[val_gen]` block (P2b + P3 keys)

```toml
[val_gen]
T             = 100
G             = 30
heir_influx   = "delta"
envelope_unit = "real"
refund_rule   = "ratio_mirror"   # "ratio_mirror" (D8 baseline) | "legacy" (bridge only)
consumption   = 0.035            # baseline share of net worth consumed per year (D16)
consumption_vals = [0.02, 0.03, 0.04, 0.05]
index_wmin    = true             # index W_min and k at [budget] budget_growth (D16)
tol_rev       = 0.02             # G3: +-2% of honest PV tax revenue
tol_rev_sens  = [0.02, 0.05, 0.10]
reset_interval = 10              # Route D voluntary hard reset (D3); 0 = never
reset_sens     = [0, 5, 10, 20]  # reset-interval sensitivity
death_waiver   = 0               # death auction skipped if a reset was within this many years (0/5/10)
d_reset_refund = "symmetric"     # "symmetric" | "none" (R_D switch)

[val_gen.route_shares]           # D13 baseline, shares of V0; sweep the BEHAV ranges
A = 0.50
B = 0.25
C = 0.08
D = 0.17
```

## D. `wdt_core.load_params`: replace the `p['val_gen']` block

```python
vg = raw['val_gen']
rs = {k: float(v) for k, v in vg['route_shares'].items()}
if abs(sum(rs.values()) - 1.0) > 1e-9:
    raise ValueError(f"[val_gen.route_shares] must sum to 1, got {sum(rs.values())}")
p['val_gen'] = {
    'T':                int(vg['T']),
    'G':                int(vg['G']),
    'heir_influx':      str(vg['heir_influx']),
    'envelope_unit':    str(vg['envelope_unit']),
    'refund_rule':      str(vg['refund_rule']),
    'consumption':      float(vg['consumption']),
    'consumption_vals': [float(x) for x in vg['consumption_vals']],
    'index_wmin':       bool(vg['index_wmin']),
    'tol_rev':          float(vg['tol_rev']),
    'tol_rev_sens':     [float(x) for x in vg['tol_rev_sens']],
    'reset_interval':   int(vg['reset_interval']),
    'reset_sens':       [int(x) for x in vg['reset_sens']],
    'death_waiver':     int(vg['death_waiver']),
    'd_reset_refund':   str(vg['d_reset_refund']),
    'route_shares':     rs,
}
```

Also update the `[val_gen]` comment header and the `valgen_core` docstring from "plan v0.5" to "plan v0.7".

## E. P3 (four routes): what was built, with the plan sections it implements

`run_family3` / `family3_pair`, same ledger, per-route holdings.

- **Routes (D1-D3):** A and B at alpha = 1, settled in units at true value. C at alpha_C, in kind at the declared price. D at alpha_D between resets, accrues a liability, settled in units at the true (auction) price at a reset, at death, or at T.
- **Assessment (D7, plan §4 step 5):** one delta on total declared W, rate tau(W / I_t). L is allocated across routes by positive-delta shares when L > 0 and negative-delta shares when L < 0 (the 1 Oct decision, D21).
- **Refunds, separate caps (D8):** Route C is capped by units this individual has paid (cleared at death, D10). A, B and D refunds are capped by the pooled real value paid (E2) and by the state's stake in the route. Route D refund cancels accrued liability first (switch `d_reset_refund`).
- **Death (D3, D4, D10):** Route D auction at death unless `death_waiver` applies, then the heir is assessed on the received stake (`heir_influx`).
- **Terminal:** any outstanding Route D liability is settled at the true price at T before measuring family net worth.

### P3 checks (all pass)

| Check | Result |
|:---|:---|
| C-only family equals P2 (ratio-mirror, consumption on/off, every alpha) | 7e-16 |
| Honest A/B/C mix equals the single-asset run | 2e-16 |
| 3 honest identity under reset, waiver and R_D switches | 0 |
| 4 A/B-only families have zero gain for every (alpha_C, alpha_D) | 0 |
| 5 dilution: gain at C share 8% / gain at 4% | 2.0008 |
| 6 caps and conservation, 192 runs | min E_cash, A_D, u_out all 0; conservation 1e-15 |
| Resets reduce Route D understatement gain | +0.81% (10y reset) vs +2.27% (never) at alpha_D = 0.5 |

### First P3 results (baseline: shares 50/25/8/17, c = 3.5%, W_min indexed, T = 100, G = 30, reset 10y, lambda = 0)

- No conflict cells: 0 of 80 (alpha_C, alpha_D) cells have gain > 0 with |pv_rel| above 2%. State revenue stays within about +-1.3% of honest everywhere.
- Largest family gain +1.30% at alpha_C = 0.1, alpha_D = 0.5. So honest is not strictly the maximum (G1), but the maximum is small and driven by Route D.
- Route C barely matters at lambda = 0: its share is 8% and payment in kind makes level misdeclaration nearly neutral, as in §1. That is a lambda = 0 result; P4 changes it.
- Route D reset interval, gain at alpha_D = 0.5 (alpha_C = 1): never +2.3%, 5y +0.1%, 10y +0.8%, 20y +0.7%. 5y is the tightest. 10y and 20y are not monotonic because deaths fall at 30, 60, 90, so a 10y reset coincides with every death (and a waiver would then switch that auction off) while a 20y reset does not.
- Overstating Route D loses (-2% to -8.6% depending on the reset interval). State PV is higher than honest.

### Simplifications to confirm (P3)

1. **Route D tax rate:** liability accrues at each year's annual tau(W) on the annual delta, not at tau(W_total) on the reset date as plan §4 "Events" says. The two coincide only if the rate does not move between resets. Say if you want reset-date pricing.
2. **Death-year assessment:** the death falls on an assessment date, so the A/B delta from last assessment to death (D5) is zero. If deaths should fall between assessments, that needs a fractional-year step.
3. **Heir pre-existing wealth H** is 0 (plan §9.1 baseline).
4. **Route-specific g** is not built (all routes grow at g).
5. **Plan §4 haircut and carry-forward switches** are not built; they are P5 switches.

## F. P4 (verification hazard on Route C): additions

### TOML: add to `[val_gen]`

```toml
lambda_vals        = [0.0, 0.01, 0.02, 0.05, 0.10]   # D9, plan §9.5: sweep 0-10% per year
lambda_base        = 0.05                            # PLACEHOLDER: no empirical anchor (plan §9.5)
verified_threshold = 0.90                            # §6: year the verified share of Route C crosses this
c_share_sens       = [0.05, 0.08, 0.10]              # D13 BEHAV range for C; A absorbs the difference
alpha_ext          = [3.0, 5.0, 10.0]                # plan §5: alpha_C beyond the headline grid (slice only)
```

### `load_params`: add to the `p['val_gen']` dict

```python
    'lambda_vals':        [float(x) for x in vg['lambda_vals']],
    'lambda_base':        float(vg['lambda_base']),
    'verified_threshold': float(vg['verified_threshold']),
    'c_share_sens':       [float(x) for x in vg['c_share_sens']],
    'alpha_ext':          [float(x) for x in vg['alpha_ext']],
```

### Mechanics (plan D9, D19)

- **Expected-value hazard, no Monte Carlo.** Each year a fraction lambda of the unverified Route C units moves to a verified tranche `Cv`, declared at true value. The verified share is exactly 1 - (1 - lambda)^t (checked to 5e-16).
- **The state's stake is marked too.** The same fraction of the state's Route C units moves to `Cv`. The units-paid cap, the prior declared value and the units paid all move with the units, so the correction appears as a delta in that year's assessment and is netted across routes (D7).
- **Correction rule.** Upward correction (alpha_C < 1) is a positive delta, taxed in kind. Downward correction (alpha_C > 1) is a negative delta: ratio-mirror refund in units, capped by the units paid. Each of C and Cv has its own units-paid cap.
- **After verification the tranche is declared honestly** (alpha = 1). Re-understating a verified asset is not modelled. Confirm.
- **Failed assets** (value to zero, D9) are not modelled.

### P4 checks (all pass)

| Check | Result |
|:---|:---|
| 8 lambda -> 0 (lambda = 1e-9) reproduces the no-verification run | 1.3e-9 relative |
| 3 honest identity under lambda (0.01 ... 1.0) | 0 |
| Verification inert when alpha_C = 1 | 5e-16 |
| Verified share = 1 - (1 - lambda)^t | 5.6e-16 |
| No-C families ignore lambda | 0 |
| Caps and conservation with the verified tranche, 300 runs | min u_out 0, conservation 1.1e-15 |
| Verification erodes understatement gain (C-heavy mix) | +0.72% at 0%, then -1.6%, -2.5%, -3.0%, -3.1% |

### P4 results (baseline shares 50/25/8/17, c = 3.5%, W_min indexed, 100 years, 10-year reset)

**1. Verification flips the Route C incentive.** Without verification, understating C gains a little (+0.2% at alpha_C = 0.1) and overstating loses. At any lambda >= 1%, understating C loses (-0.8% at alpha_C = 0.1, lambda = 5%) because the understated step-up is taxed when verified. Overstating C gains (+0.9% at alpha_C = 2, +3.3% at alpha_C = 5, lambda = 5%) because the downward correction earns a ratio-mirror refund. This is the plan §1 refund-on-write-down channel; the cap on units paid does not close it.

**2. State PV at rho = 5% hides it; the terminal stake does not.** At lambda = 5%, alpha_D = 1:

| alpha_C | 1.5 | 2 | 5 | 10 |
|:---|:-:|:-:|:-:|:-:|
| Family gain, C = 5% | +0.3% | +0.6% | +2.1% | +4.5% |
| State terminal stake, C = 5% | -0.6% | -1.1% | -4.1% | -8.1% |
| Family gain, C = 8% | +0.4% | +0.9% | +3.3% | +6.7% |
| State terminal stake, C = 8% | -0.9% | -1.8% | -6.2% | -11.8% |
| Family gain, C = 10% | +0.6% | +1.1% | +4.1% | +8.0% |
| State terminal stake, C = 10% | -1.1% | -2.2% | -7.5% | -13.9% |

PV at rho = 5% shows the state within +-0.2% on the headline grid, because rho < g values early receipts highly. Using the terminal stake (D15, rho ~ g), conflict cells (gain > 0 and |state shortfall| > 2%) on the headline alpha grid are 0, 3, 5, 8, 12 and 15 of 80 for lambda = 0, 1, 2, 5, 10 (printed as 3 / 5 / 8 / 12 / 15 for lambda > 0). With C at 10% of wealth, alpha_C = 2 is already outside tolerance (-2.2%).

**3. Time to steady state (D19).** The year the verified share of Route C reaches 90%: lambda = 5% -> year 45; 10% -> year 22. At 1% and 2% it never reaches 90% within 100 years (63% and 87%).

**4. Route D** results are unchanged from P3 (verification does not touch D).

### Implication for the P5 decision on the refund rule (§9.3)

The overstatement gain is a property of the refund rule on a downward correction, not of the unit. At realistic route mixes it is small (about +1% at alpha_C = 2) but it grows with alpha_C and with the C share. P5 should run the two remaining oracle-free levers against exactly this slice: the mechanical haircut on large write-downs, and carry-forward credit only.

### To confirm

1. Terminal state stake (D15) as the G3 measure alongside PV at rho = 5%: the conflict count uses both and reports them separately.
2. lambda_base = 5% is a placeholder; the sweep is the result.
3. Verified tranche declared honestly afterwards; failed assets not modelled.

---

# G. P5 additions (strategy search, payoff surfaces, G1–G3 verdicts by rule set)

## G.1 New `[val_gen]` TOML keys (all placeholders unless stated)
```toml
strategy_k      = [3, 5, 10]        # late / pre-reset / correct-before-death horizons
haircut_zero    = 0.5               # fall in declared W at which the Route C refund is fully withheld
g1_tol          = 0.01              # G1: best response may beat honest by at most 1% of honest TW
g2_tol          = 0.01              # G2: honest family's cost of an error / shock <= 1%
shock_sizes     = [-0.2, -0.5]
shock_year      = 20
c_refund_rules  = ["ratio_mirror", "carry_forward", "haircut", "haircut_total"]
c_cap_rules     = ["units", "units_and_value"]
d_refund_rules  = ["symmetric", "none"]
entry_rules     = ["free", "taxed"]
```
`load_params` must pass these through, as for the P3/P4 keys (same pattern as section D). `PV_REL_MIN_FRAC` (1e-3) is still hardcoded and should move to TOML. Rule-set key = `c_refund/c_cap/d_reset_refund/entry_basis`.

## G.2 Mechanics
* Strategies: constant (full alpha_C x alpha_D grid plus alpha_ext), first_gen_only, late_deviation, correct_before_death, pre_reset_deviation, reset_gaming; targets C / D / CD.
* Route C refund variants: ratio_mirror (baseline), carry_forward, haircut (event level), haircut_total (aggregate).
* Route C cap: units paid only, or units plus a real-value envelope.
* `entry_basis`: free (declared basis = alpha*V0) or taxed (basis = V0 at entry).

## G.3 Findings (lambda 0-10%, thresholds above)
* Baseline ratio_mirror/units/symmetric: best response +24.9% (lambda=0), about +7% at lambda>=1%. G1 and G3 fail.
* carry_forward only delays the refund; haircut_total is diluted by route mix. Neither helps.
* Units-only cap lets Route C refunds reach about 4x the value paid (net Route C receipts -£329m). The value cap closes that hole (best response +24.9% to +4.4% at lambda=0) but not the main gain (about +7%).
* Event-level haircut gives +1.50% best response. With the Route D reset refund set to `none` it passes G1 (+0.79%) and G3 (0 conflicts), but fails G2 (honest cost -0.84% at a -20% shock, -2.04% at -50%).
* Taxed entry does not fix it, and it **raises** G3 conflicts (e.g. 30 to 88 on the baseline). The earlier diagnosis (free entry + netting) was incomplete: the residual gain also comes from paying in kind at an inflated declared price and from heirs inheriting the declared basis (D4/D6). The check was relaxed to "taxed < free" with that note.
* Full run: about 4 min; output 8.9 MB JSON.

## G.4 Decisions needed
1. Route C cap: units only, or units + value? (Value is the accounting-correct reading of "can only get refunded what you paid"; it matters most at lambda=0.)
2. Baseline rule set. Only `haircut/*/none/free` passes G1+G3, and it fails G2. Options: accept it and relax g2_tol, keep the symmetric Route D refund and accept G1/G3 failure (+1.5%), or design a rule between the two (e.g. partial Route D reset refund).
3. Drop `taxed` entry from the rule family (no benefit)?
4. Confirm g1_tol / g2_tol / haircut_zero values.

---

# H. P5 follow-up: why Route C overstatement gained, and three new switches

## H.1 Diagnosis (corrects G.3)
The +5–7% gain from overstating Route C is not caused by the entry basis, by in-kind payment, or (mainly) by a refund. When a tranche is verified (λ>0) its declared value falls from α·V to V. That write-down is netted against growth on the other routes (D7). It lowers current tax with no refund, no cap and no payment. Switching off the Route C write-down credit removes the gain (−0.2%).

## H.2 New `run_family3` switches (defaults reproduce P5 exactly; checks pass)
* `alloc='holdings'` (vs `'delta'`): allocate L pro-rata to declared holdings. No effect on the gain. Kept for reference; not recommended.
* `net_cap='paid'`: a write-down on an in-kind route counts only up to the tax paid on it (units paid × declared price / rate). Cuts the best response from 7.0% to 5.0%. Not sufficient alone, because it still returns the tax paid on the verified tranche.
* `verify_down='reset'`: correcting your own overstatement at verification is a basis reset. There is no write-down credit and no netting shield. Up-corrections (understatement) are still taxed. Genuine falls still refund through the route-level rule.
* Rule-set key is now `c_refund/c_cap/d_reset_refund/entry/alloc/net_cap/verify_down`; trailing parts optional.

## H.3 Results (ratio_mirror, free entry; best response, G3 conflicts)
| rule (cap / D reset refund / extras) | λ=0 | λ=1% | λ=5% | λ=10% | G2 shock −20% / −50% |
|---|---|---|---|---|---|
| units / sym / none (P5 baseline) | +24.9% | +16.7% | +7.1% | +7.3% | 0 / 0 |
| units+value / none / reset | +4.4% (7) | +3.2% (3) | +0.45% (0) | +0.37% (0) | −0.69% / −1.51% |
| units+value / sym / reset | +4.4% (19) | +3.2% (9) | +1.6% (6) | +1.5% (6) | 0 / 0 |
| units+value / none / paid+reset | +2.9% (4) | +2.5% (0) | +0.35% (0) | +0.17% (0) | −0.69% / −1.51% |

## H.4 Reading
* From λ=5% up, `units+value / none / reset` passes G1 and G3 and misses G2 only at the −50% shock (g2_tol 1%). With a symmetric Route D refund G2 holds but Route D pre-reset deviation leaves +1.5%.
* At λ≤1% no rule passes G1. The remaining gain is late understatement or overstatement when nothing is ever verified; the units+value cap bounds it at +3–4%.
* The value cap is needed. The units cap alone leaves +25% at λ=0.

## H.5 Decisions needed
1. Adopt `verify_down='reset'` (correction of one's own overstatement earns no credit)? It is asymmetric by design: understatement corrections are still taxed.
2. Route D reset refund: symmetric (G2 clean, +1.5% left) or none (G1/G3 clean at λ≥5%, G2 cost 0.7–1.5%)?
3. What λ should the verdicts be judged at? Nothing passes G1 at λ≤1%.
4. Full `main()` has not been re-run with the new switches; the P5 verdict table in the data JSON predates them.

---

# I. Corrective auction on Route C and Route D (VAL §11.3 generalised)

## I.1 What was modelled
The corrective auction (two non-flagging Valuation Bodies corroborate, then a compulsory auction; under-declaration pays tax on the upward delta, over-declaration resets the basis with no refund) now applies to Route C **and** Route D, as an expected-value hazard λ per year:
* Route C: unchanged. The verified tranche Cv is the auctioned share. `verify_down='reset'` is the over-declaration arm.
* Route D (new): `verify_hazard_D` (rule-key part 8 = `on` sets it to λ). A share vD = 1−(1−λ)^t is declared at the true price; the rest follows the strategy. The write-down from correcting an overstatement is excluded from the delta (`Wp` shifted, capped so it never creates tax). The under-declaration arm is the normal positive delta.
* `verify_down='reset'` also applies the no-refund rule to Route D hard-reset years and the death auction when the declared price exceeds the auction price. Honest families are unaffected, because they already declare the true price.
Rule key: `c_refund/c_cap/d_reset_refund/entry/alloc/net_cap/verify_down/dauc`.

## I.2 Results (ratio_mirror, units+value cap, free entry; best response, G3 conflicts)
| rule | λ=0 | λ=1% | λ=5% | λ=10% | G2 −20% / −50% |
|---|---|---|---|---|---|
| sym D, no change | +4.4% (19) | +6.4% (32) | +7.0% (57) | +7.3% (65) | 0 / 0 |
| sym D, reset, auction C only | +4.4% (16) | +3.2% (8) | +1.6% (5) | +1.5% (5) | 0 / 0 |
| **sym D, reset, auction C+D** | +4.4% (16) | +3.2% (8) | **+0.64% (1)** | **+0.67% (0)** | **0 / 0** |
| none D, reset, auction C only | +4.4% (7) | +3.2% (3) | +0.45% (0) | +0.37% (0) | −0.69% / −1.51% |
| none D, reset, auction C+D | +4.4% (7) | +3.2% (3) | +0.45% (0) | +0.67% (0) | −0.69% / −1.51% |

## I.3 Reading
* With the auction on both routes, the symmetric Route D refund can stay: G2 is clean (honest families lose nothing) and G1 and G3 pass from λ=5% (best response below 1%). This removes the G2 trade-off from section H.
* Below λ≈1% nothing passes. The residual (+3.2% at λ=1%, +4.4% at λ=0) is the family's own downward re-declaration of Route C before death (`correct_before_death`, `late_deviation`). A voluntary write-down is refunded, capped by tax paid, because an honest fall looks identical. Closing it needs refunds on self-declared C/D falls to require an auction-verified price. That would also hit honest falls unless the refund runs only from the last market-verified basis. Not built.

## I.4 To confirm
1. Is the voluntary hard reset (VAL §11.2, refund allowed) kept? In the model it is still refunded unless the declared price exceeded the auction price, in which case the no-refund rule applies.
2. Is a verified-basis refund rule (refund only below the last auction-set price) worth building?
3. What is the right λ range for Phase One? The verdict depends heavily on it.
4. Full `main()` not re-run; p5 checks pass.

---

# J. Complete TOML and load_params patch (supersedes sections C, D, F and G.1 as the source of truth)
* `WDT_Params.toml`: your full file with the `[val_gen]` block replaced by the complete set of 32 keys (every key `valgen_core.py` reads), plus `[val_gen.route_shares]`. Checked: parses, 73 returns, route shares sum to 1, and the keys and values match the set the validated run used.
* Two comment fixes in `[val]`: the `alpha_max` comment had drifted onto `unc_seed`; both now describe their own key. Values untouched.
* **Not changed, please check:** `[synthetic_scenario] mu = 0.07` but its comments say "UK CPI inflation (2%)" and a −2% to +6% range. With mu = 0.07 and amplitude = 0.08 the range is −1% to +15%.
* `load_params_val_gen_patch.py`: replaces the whole `p['val_gen']` block.
* Default search lists were narrowed so the full run takes about 3 minutes: `c_refund_rules = ["ratio_mirror"]`, `entry_rules = ["free"]`; the new `verify_down_rules` and `d_auction_rules` are on. Widen them in the TOML to compare haircut and the others.

---

# K. Sanity sweep, bug fix and the growth x lambda surface (supersedes the numbers in H.3, I.2 and the earlier verdict tables)

## K.1 Bug found and fixed
The `verify_down='reset'` rule compared the prior declared VALUE of the verified units with their true value now. Units that had left the family (consumption, tax paid in kind) look like a price fall, so an honest family lost its small refund after an heir-year tax payment (a 1.2e-5 effect, caught by the new check `auction_switches_inert_for_honest_family`). It now compares declared PRICE per unit with the true price (`ppu`), so only a real overstatement gets no credit. Honest families are identical under every switch (0 difference).

## K.2 Corrected results (best response; the TOML parameters as before)
| rule | λ=0 | λ=1% | λ=2% | λ=5% | λ=10% |
|---|---|---|---|---|---|
| value cap, D refund kept, reset, auction C+D | +4.4% | +3.4% | +3.2% | +0.8% (G1) | +0.8% (G1) |
| value cap, no D refund, reset, auction C only | +4.4% | +3.4% | +3.2% | +0.8% (G1, G3) | +0.7% (G1, G3) |
| value cap, no D refund, reset, auction C+D | +4.4% | +3.4% | +3.2% | +0.8% (G1, G3) | +0.8% (G1) |
G3 at λ=10% fails by a hair in two strategies (state stake −2.2% against a 2% tolerance, gain 0.7%). The thresholds are placeholders, so treat the G3 flags near 2% as borderline, not as failures of substance. G2 is unchanged (D refund kept: 0 / 0; none: −0.69% / −1.51%).

## K.3 Growth x lambda surface (new; `p5.growth_surface` in the JSON)
Best-response gain by g and λ for the two surface rules (TOML `growth_vals`, `surface_rules`). With the value cap, no D refund, reset, auction C+D:
| g | λ=0 | λ=1% | λ=2% | λ=5% | λ=10% |
|---|---|---|---|---|---|
| 3% | +0.9% | +0.6% | +0.5% | +0.2% | +0.0% |
| 5% | +0.9% | +0.7% | +0.8% | +0.3% | +0.5% |
| 7% | +3.0% | +3.6% | +1.3% | +0.4% | +0.8% |
| 10.45% | +4.4% | +3.4% | +3.2% | +0.8% | +0.8% |
| 15% | +3.6% | +2.5% | +1.3% | +0.7% | +0.5% |
Reading: slow growers leave at most about 1% of room even if never verified; the exposed corner is g of 7% or more with λ below 5%. At g = 3% the honest family's declared wealth falls (real wealth below the indexed threshold) and revenue is near zero, so the relative G3 measure there is unreliable; the G1 numbers are the ones to read. Growth and λ are independent inputs: the model does not link them.

## K.4 Sanity sweep (code and comments)
* Module header rewritten (it still described P1 to P2b, "Route C only"). It now lists P1 to P5, the caps, the rule-set key and what is not built.
* `run_family3` docstring now covers `verify_hazard_D`, `verify_down`, `net_cap`, `alloc`; invalid values of those raise `ValueError` (checked).
* `_p5_opts` docstring and the verdict table header describe the 8-part rule key. P3 header no longer says "only ratio_mirror".
* Two empty f-strings fixed (pyflakes now clean).
* New checks: honest family inert under every new switch; `reset` removes the overstatement gain (+6.67% to +0.19%); the Route D auction is inert when alpha_D = 1; invalid switch values raise; the caps check now also covers the auction rule sets (1,116 runs).
* `alloc='holdings'` and `net_cap='paid'` are exploratory and off; `alloc='holdings'` moves the honest family by about 1e-4, so it is not inert. Remove them if you want the code simpler.
* Still hardcoded: `PV_REL_MIN_FRAC = 1e-3`. New TOML keys: `growth_vals`, `surface_rules`.

## L. Cleanup (3 Oct): decisions applied, redundant code removed

Decisions: Route D reset refund stays symmetric; Route C cap is units plus value; delete redundant code; paper headline deferred.

Removed from `valgen_core.py` (all had been tested and rejected, or were exploratory): `c_refund` (carry_forward, haircut, haircut_total) and `haircut_zero`; `entry_basis` ('taxed'); `alloc` ('holdings'); `net_cap` ('paid'); `d_reset_refund` ('none'); `refund_rule` in `run_family3`; the `credit` ledger; six checks that only tested those switches. Rule-set key is now `c_cap/verify_down/dauc` (e.g. `units_and_value/reset/on`). Kept as ablations, because they show what each part of the final rule buys: `c_cap` (units | units_and_value), `verify_down` (allow | reset), `dauc` (off | on).

Moved to TOML: `pv_rel_min_frac` (was hardcoded). Removed from TOML: `refund_rule`, `d_reset_refund`, `haircut_zero`, `c_refund_rules`, `d_refund_rules`, `entry_rules`. `surface_rules` is now `["units_and_value/reset/on"]`. `load_params` patch updated to match.

Bug found by the sanity check: `main()` reused the name `surface` for the growth surface, so `p3_surface.cells` in the JSON held the growth surface instead of the P3 alpha grid. Fixed (`growth_surf`), plus an assert before writing.

Regression: all retained rule sets reproduce the pre-cleanup run exactly (best response, G1/G2/G3 flags, conflict counts, growth surface: max diff 0.0; P1-P4 sections identical; 55 retained checks pass, 6 removed). Run time 1m47s (was about 3 minutes).

Result for the chosen rule (`units_and_value/reset/on`, symmetric D refund), best response by lambda 0/1/2/5/10%: +4.4/+3.4/+3.2/+0.8/+0.8%. G1 passes at 5% and 10%. G2 cost is 0.000% at both shocks. G3 fails by a hair: at 5%, 1 strategy of 98 gaining (pre_reset_deviation D a=0.5 k=10, stake -2.14% vs 2%); at 10%, 2 of 180 (stake -2.19% and -2.27%). PV is inside tolerance in all of them.

Growth x lambda surface for this rule, best response at lambda 0/1/2/5/10%: g=3%: +0.8/+0.6/+0.5/+0.2/+0.0; 5%: +0.9/+0.7/+0.8/+0.3/+0.5; 7%: +3.0/+3.6/+2.1/+0.4/+0.8; 10.45%: +4.4/+3.4/+3.2/+0.8/+0.8; 15%: +4.9/+4.5/+2.7/+0.7/+0.5. This supersedes the surface in K, which was for the no-D-refund rule.

## M. Conventional baseline and the no-tax ceiling (3 Oct)

Added to `valgen_core.py` (P5): `_conventional_run`, `_conventional_rate`, `_p5_conventional`, `_p5_no_tax_tw`, `_p5_upper_bound`; TOML key `conv_extra_alphas = [0.0, 0.01]`; JSON `p5.conventional_baseline`, `p5.no_tax_ceiling`; two new checks (63 total).

Conventional reference: a flat self-declared wealth tax on declared value, paid in kind, A/B professionally valued, C/D declared at alpha, no delta, refund, verification, auction or reset. The flat rate (1.207% a year) is calibrated so the honest family ends with the same terminal wealth as under the WDT (equal PV of receipts is unattainable: with g above the discount rate, PV peaks at a modest rate and then falls).

Result (best response = terminal wealth vs honest): conventional +59.2% at full understatement; alpha 0.5: +21.0%; 0.2: +41.1%; 0.1: +49.6%; 0.01: +58.2%. Gain rises monotonically as the declaration falls, with no interior optimum; overstating loses up to 25%. WDT (units_and_value/reset/on): +4.4% at lambda 0, +0.8% at lambda 5%.

No-tax ceiling: no declaration strategy can beat a run with no tax, so gain <= TW(no tax)/TW(honest) - 1 = +236.6%. Asserted against every best response in every rule set and lambda (passes). It is loose (it counts the tax on A/B, which cannot be misdeclared) and is a leak detector, not the informative number; the conventional comparison is.

Regression: best responses for all retained rule sets are unchanged from the pre-cleanup run.
