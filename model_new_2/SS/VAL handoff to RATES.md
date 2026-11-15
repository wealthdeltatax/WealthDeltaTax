# Handoff: VAL generational model (for the RATES remodel)

## What this is
`valgen_core.py` (VAL generational model, plan v0.7, steps P1–P5) is built, cleaned and passing all 63 of its checks. It simulates a family line over a 100-year horizon, with a death every 30 years and an heir. The family pays the Wealth Delta Tax (WDT) through four valuation routes and chooses how honestly to declare. The model tests whether any declaration strategy pays without limit. P6 (presentation scripts and the paper rewrite) is not started.

**The core theory:** no declaration strategy has an unbounded payoff, and the state doesn't need to know the true value of illiquid assets. Under a conventional self-declared wealth tax, understatement is always a clear, unbounded benefit.

## Headline results
- **Conventional wealth tax (reference):** a flat 1.207% a year on declared value, set so honest families bear the same burden as under the WDT. Declaring nothing gains +59.2%, declaring half gains +21%, and the gain rises steadily as the declaration falls.
- **WDT final rule (`units_and_value/reset/on`):** the best response over 428 strategies is +4.4% with no verification (λ=0), and about +0.8% from λ=5% upward. G1 passes at 5% and 10%, and the G2 cost is 0.000%.
- **G3 is a near-miss:** 1 of 98 gaining strategies at λ=5%, and 2 of 180 at 10%, leave the state's terminal stake 2.1–2.3% below the honest case against the 2% tolerance. Revenue (PV) is inside tolerance in all of them.
- **Growth × λ:** slow growers leave about 1% or less of room even with no verification. The exposed corner is high growth (g ≥ 7%) with λ below 5%.
- **No-tax ceiling:** no strategy can beat a run with no tax at all (+236.6%). This is a loose check, asserted in every cell and passing.

## The final rule (what to model)
1. **Delta base and netting:** tax is on the delta of declared net worth, netted across routes (D7), with the rate τ(W_total) from the total.
2. **Refund:** ratio-mirror (D8). A fall refunds τ × (1 − W_new/W_prev) of holdings, the mirror of the payment fraction.
3. **Route C:** self-declared, paid in kind at the declared price. The refund cap is units paid plus the real value paid. The units-only cap lets refunds reach about 4× the value paid, so both are needed.
4. **Routes A and B:** professionally valued, paid in cash-equivalent units, with a pooled real-value refund cap.
5. **Route D:** self-declared and non-fungible. Liability accrues and is settled in units at the true price at a 10-year reset, at death, or at T. The write-down refund is symmetric.
6. **Corrective auction on C and D (VAL §11.3):** under-declaration means accepting the new basis and paying the delta, or selling. Over-declaration means a basis correction with no refund, or selling. In the model this is an expected-value yearly hazard λ, with a basis-reset rule (`reset`) for self-corrected overstatement.
7. **λ is a framing device.** It is the yearly odds that a self-declared asset reaches a market or auction. The WDT changes the listing decision itself, so historical listing data doesn't apply.

## What we learned (the non-obvious parts)
- **In-kind payment bounds dishonesty.** Units paid equal tax owed divided by the declared price, so inflating the price cancels. Only the higher marginal rate on the larger declared wealth costs anything.
- **The leak was never the entry basis or the in-kind price.** It was a declared-value write-down (from verification or self-correction) netted against other routes' growth, with no refund test and no cap. Removing the credit for self-corrected overstatement removes the gain.
- **Haircuts, carry-forward, taxed entry, pro-rata allocation and a paid-cap did not give a simple fix.** The auction plus the no-credit rule did.
- **The residual** is a family cutting its own Route C declaration shortly before death. An honest fall looks identical, so closing it would need a verified-basis refund rule. You declined that as not simple.

## Parameters for RATES (all in `WDT_Params.toml` under `[val_gen]`)
- **Rate schedule:** τ(W) = τ_m / (1 + ((τ_m − τ_0)/τ_0) · e^{−k(W − W_min)}), with τ_0=0.15, τ_m=0.70, k=0.001, W_min=£2m.
- **Indexation:** W_min and k are indexed at the budget growth of 4.51% a year.
- **Setup:** V0=£20m, g=10.45%, ρ=5%, consumption 3.5% a year (not in the family objective), T=100, G=30, route shares A 50 / B 25 / C 8 / D 17.
- **Placeholders:** λ_base=5%, and the verdict thresholds G1=1%, G2=1%, G3 ±2%.

## Limitations the next agent should know
- **One parameter point:** there is little sensitivity across τ_0, τ_m, k, W_min, V0, shares or consumption. This matters most for RATES.
- **Constant growth for every asset:** no route-specific g, no heir pre-existing wealth, no gifts, no failed assets, and no re-understating after verification.
- **The strategy search is a lower bound:** 428 strategies show that none tested is unbounded, not that none exists.
- **λ is exogenous:** it is independent of growth, and an expected-value flow, not a discrete event, with no variance and no Monte Carlo.
- **Heirs inherit the declared basis** (D4/D6) unless a Route D death auction happens. The paper may say otherwise, and I haven't checked.
- **The conventional baseline has no audits.** A conventional tax with audits would sit between the two columns, and I haven't modelled that.
- **The G thresholds are placeholders,** and the relative G3 measure is unreliable where revenue is near zero (for example g=3%).

## Open items
- **Paper edits:** VAL §4.3 and §11 (the paper says Route C needs no auction and treats the auction as a Route D device), the §7 and §10 tolerance and mild-overstatement claims, and the heir-basis check.
- **Paper headline:** deferred for now.
- **P6:** the presentation scripts (`{n}_2_VAL_tables.py`, `{n}_3_VAL_charts.py`) and the paper rewrite.

## Files (in `/tmp/p2b/out/`)
- `valgen_core.py`: the model.
- `WDT_Params.toml`: the full parameter file.
- `load_params_val_gen_patch.py`: the `load_params` patch for the `[val_gen]` block.
- `VAL_plan_v0.7_changes_and_P2b_patch.md`: change log, sections A–M. K is superseded where L and M differ. L has the final symmetric-refund numbers and M the conventional baseline.

I haven't read the RATES paper or its code in this stretch of the work, so none of the above says how RATES should change. The next agent should start from the one-parameter-point limitation and the rate-schedule inputs.