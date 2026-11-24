# 166: Can the fund's reserves cover the gap years? (diagnostic)

- **Status:** ready; any free agent (lane plan shows Agent 3 until it is reassigned); must finish before 162c starts (162c moves `model_v3`)
- **Author/date:** K. Ogata with the guru, 2026-11-25
- **Depends on:** nothing (089c, 149c, 140c are merged)
- **Read:** `docs/model-v3/f1-household.md` (section "Is the failure structural?"); `model_v3/core/revenue.py` (module docstring, `fund`, `retire`, `revenue`); `docs/model-v3/f1-household/f1_household.py` (the harness: `setup`, `point_ctx`, `core`, the constant-path run); `docs/model-v3/death-phases/death_phases.py` (phase count switch); `docs/model-v3/inputs.md` rows I-D8a, I-D14d

## Goal
The strict closure test fails, and the author's reading is that money the fund already holds is not allowed to cover the gap years. Test that reading: how much of the fund sits idle in each year in which retired receipts exceed relief, and how much of the failure disappears if the fund may pay out over a longer window or top up a gap year from what it holds above its short reserve. This is a diagnostic. It decides nothing about the design.

## What the code does now (read, not tested)
`fund()` pays relief R = min(R*, S_pre minus the short reserve), where R* is the mean over the last `ml` (3) post-fill years of (net receipts minus upkeep). So the payout is a three-year average of recent flows, not a draw on the stock. At `median_mid`, tm70_k1_r050, constant path (`f1-household.md`), the fund holds S of 38 to 45% of GDP while relief falls to 3.82 against M1d 4.74 in years 13 and 14. The reserve targets are 3 times the trailing mean refund A each (about 19% of GDP in total at that point), so on this reading roughly 20% of GDP sits above both reserves in the gap years. **Labelled assumption (guru, to challenge):** that figure is read from the table, not computed; part A computes it.

## Design
Everything is a labelled scenario in a script; no model code changes. Household arm, 10 death phases (149c ruling), `safe` and `market` fund, the five scenario points, schedules tm50, tm70, tm90 (k_ln 1, w_min r050).

**A. Accounting, no rule changed.** On the constant path at 4.74%, for each row and each year after the fill: the shortfall max(0, M1d minus relief); the fund's S; S minus the short reserve (`srr`); S minus the total target. Report the first shortfall year, the largest shortfall, the idle stock in that year and the ratio of idle stock to the shortfall, and P3 to the end of the short window against the idle stock at the start of it. Also run once at 6 phases and show the first shortfall is year 13 and P3 equals `f1_safe_constant_path.csv` (the harness check).

**B. Longer payout window.** Copy `fund()` into the script with the payout window `w_pay` separate from the reserve multiple `ml` (the core uses one number for both). At `w_pay` 3 the copy must equal the core to 1e-9 on every output (the proof the copy is faithful). Then `w_pay` 5 (the death-phase cycle), 10 and 15; and `a_window` 10 (register row I-D14d's high) with `w_pay` 3. Reserve multiples stay 3 (I-D8a is a lever of the papers).

**C. Gap top-up.** In the copy: relief R = min(max(R*, shortfall to M1d), S_pre minus the short reserve). That is: if staged retirement would show a gap this year, the fund may draw it from what it holds above the short reserve target. Retired taxes still retire by the existing trigger.

**D. What each variant does, side by side.** For A's constant path and for 200 level-1 paths (seed 20261118, the 089c paths): F1 at the strict rule (tolerance 0, margin 0) and at tolerance 1% with margin 25% for comparison, M1a to M1d means over the short window, P1, P6 (fund as % of GDP at years 10, 25, 50, 100), P7a (reserve insolvency share), P7b (minimum cover). **The cost of every variant is shown beside its gain**: a rule that lifts F1 by emptying the fund shows in P6 and P7.

**Size stop.** Time one 200-path run first. If the full set (variants x 3 schedules x 5 points x 2 funds) would take over about 60 minutes, drop to `median_mid` and `median_low` and the `safe` fund and say so in the report. Run in the background (nohup, poll); never pipe.

## Deliverables (two)
1. `docs/model-v3/reserve-diagnostic/reserve_diagnostic.py` with its CSV outputs (A to D).
2. `docs/model-v3/reserve-diagnostic.md`: the plain-English answer first (does the idle stock cover the gaps; how much of F1's failure each variant removes; what each costs in P6 and P7), then the tables, then every assumption labelled for challenge, then what was not run.

## Touches
Two new paths under `docs/model-v3/`. Nothing in `model_v3/`, `runner/switches.py`, `flow_switches.py`, `arm.py`, the register, `outputs.yml` or the gate.

## Acceptance criteria
- The copy of `fund()` equals the core at `w_pay` 3 (stated in the report, with the largest difference).
- The 6-phase constant-path check reproduces the 140c first-shortfall year and P3.
- The report gives, for every variant, F1 (strict and relaxed), P6, P7a, P7b, with the 200-path standard error noted.
- No design is recommended; the report ends with the question for the author (below), not an answer.

## Out of scope
Changing the fund rule in the model; new switches or register rows; the GDP growth hypothesis (separate, below); death-phase counts other than 10 (and the one 6-phase check); the reorganisation.

## Open questions (for the author, after the report)
If a top-up from above the short reserve closes the gap years at an acceptable reserve cost, should the Sovereign Wealth Fund be allowed to cover retired-tax gaps? That changes the RATES paper's relief rule (section 6.1), so it is a design ruling, not the agent's call. Stop and report any result that contradicts the reading above.

## Note: the growth hypothesis (not part of this brief)
Author hypothesis, 2026-11-25: raising the same revenue as the taxes it displaces with the WDT generates greater productivity and growth. It is not in the model (the `gdp_paths` switch exists, default off, and no evidence for its size is held). It is investigated later as its own labelled scenario; nothing here assumes it.

Rules that apply: one block, one push; suites in the background, never piped; any `arm.py` or core change is stop-and-report (none is expected).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** not started
<!-- progress:end -->
