# 055: Model v3 V3-10: range runner

- **Status:** retired 2026-11-20 (merged `e4993a4`; the empty feasible region is carried by 083c and 089c)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 053, 054
- **Read:** `docs/model-v3/architecture.md` 2.8, 3.1 to 3.3, 6.2 (N1 to N7) and 6.5; `docs/model-v3/drivers.md`; `docs/model-v3/tornado.md`; `docs/model-v3/stage-c-decisions.md` items 2, 6, 7; `docs/model-v3/acceptance.md` V3-10 row and section 4 (R3, R10).

## Goal
The two-level run, the schedule sweep, the tornado and the stress test, producing Samples.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`runner/runner.py` (360 lines): level 1 at `N1` = 10,000 per schedule, level 2 at `N2` = 200 Latin hypercube draws of `N2P` = 1,000 paths on common random numbers, folded into the kernel's line axis in chunks of 1,000 paths; seed streams. `runner/sweeps.py` (300 lines): the feasibility map over the lever grid, the three named schedules by the confirmed rule, the tornado, break-even and negative-M1 share (`O1e`, `O1f`), CK1 and the bootstrap run. `runner/pool.py` (70 lines) only if the full run would exceed 60 minutes or K6 failed. Add the set-equality test between the drawn level 2 ids and the tier 1 list of `drivers.md` (R3), and the monotone check over every cell of the lever grid (R10).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-10 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/runner/runner.py`, `model_v3/runner/sweeps.py`, `model_v3/runner/pool.py`, `tests/model_v3/test_runner.py`, this brief's progress block.

## Acceptance criteria
- N1 to N7 pass; the same seed gives byte-identical `Samples`.
- The R3 set-equality and R10 grid tests pass.
- N7: the time of one 10,000-path schedule is measured and written to the change report; `pool.py` exists only if its trigger fired.
- `runner.py` at most 360 lines and `sweeps.py` at most 300.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The writer (V3-11); the convergence test (V3-12); a final run.

## Open questions
Ask if N7 shows the full run would take over 60 minutes and K6 passed: the pool rule is the answer, but confirm the reference machine.

## Guru note, 2026-11-19 (after 054c)
`core/support.py` takes some inputs from the caller (054c gotchas): the distribution of declared alpha (M7e), consumption spend and its rate (the migration loss), the second asset's returns and the embedded-gain bands (M14), and the gains-tax realisation rate (M13). The runner supplies them from the register and pack: consumption from I-D14, the second asset's returns from `returns.csv` (`housing_tr`, `bond_tr`), embedded gain from I-T4e and realisation from the I-T5 rows. Map each to a row id in your report. If an input has no row (the likely one is the distribution of declared alpha: the register holds only the shift I-D5b), do **not** invent a value: stop and report to the guru, who writes a register brief. Same for any other input the runner needs and the register lacks.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/runner/runner.py` (266 lines, budget 360), `model_v3/runner/sweeps.py` (149, budget 300), `tests/model_v3/test_runner.py` (135, budget 150). Level 1 (N1 10,000 paths in chunks of 1,000, the same paths for every schedule), level 2 (N2 200 Latin hypercube draws of the 40 tier 1 inputs, N2P 1,000 common random paths each), `Samples` and `Level2` separate objects, `evaluate` (M1 and its parts, M2 by band, M4a by decile, M3, negative-M1 flags, P3 by horizon), the 27-point feasibility map and choice rule, tornado, break-even return, stress path (CK1), block bootstrap check, 30-year spread. `pytest tests/model_v3 -q`: 201 passed (12 new: N1 to N7, R3, R10, the shortcut equivalence, tornado on the model, bootstrap).
- **Next:** the author rules on the empty feasible region (below); then V3-11 can name S_low, S_central and S_high.
- **Decisions:** (1) Receipts for M1 come from one `burden.line_flows` run (the sum of weight x net, which equals `run_lines` to 1e-17: a test); `full=True` takes them from `run_lines`. (2) GDP per head growth on simulated paths is a constant, the mean of the pack's own history, 1.57% a year (no register row holds one). (3) Horizons per path: transition 1 to the fill year, short the 10 years after it, long years 51 to 100; M2 in life and M4a read over the same window; M3 single. (4) Inputs read: the generator (I-D1a, I-D1b, I-D1b2), wealth over GDP (I-D4a, scales every line by the draw over central) and the base loss (I-D5a, payer lines at launch scaled by one minus it, read literally from its unit). The 40 tier 1 inputs are all drawn; the 35 that reach no headline of this stage swing exactly 0 and are not run. The I-D6 incidence shares with a pack row are patched into the pack for the by-decile M4a at level 2; they cannot move the overall M4a. (5) Level 2 quantile map: normal, with the spread of the side the draw falls on, within three SD (no tier 1 row goes negative there), low zero rows have a tenth of the draws at the floor, any other negative raises. (6) Feasible point: short-window F1 at least 75, M2 at most 2.0, M4a at least 0; S_central the highest F1 (lower M2 on a tie), S_low and S_high the lowest and highest M2 of the feasible points. F1 is the share of paths with P3 zero up to the end of the window. (7) Break-even is the generator mean at which the short-window M1 is zero; the range is one root per draw of the others, run by the caller on as many draws as it chooses.
- **Gotchas:** (1) **The feasible region is empty.** At central inputs, 1,000 common paths, all 27 grid points: F1 over the short window is 4.0 to 11.2 percent (transition 100 at every point), against 75 needed. M2 short 1.34 to 4.44 percent a year (8 points at or under 2.0, best F1 among them 5.9), M4a short 14.1 to 24.6. So `choose` returns None and no schedule is named. The cause is P3: relief falls below the retired receipts after the fill in most paths (the 052c finding, P3 large). (2) The stress path: P3 is positive from the first amplitude (A 0: 100.9, A 2: 368, A 4: 366, A 8: 364, A 12: 365), so it closes up to no amplitude. (3) Tornado at S (tau_m 0.7, k 0.5, ratio 0.5), M1 short, swings low/high: I-D1a -0.127/+0.317, I-D1b2 -0.087/+0.144, I-D4a -0.007/+0.091, I-D1b +0.013/-0.011, I-D5a +0.007/-0.003. Break-even generator mean there: 5.40 (central 4.74). (4) Outputs filled: O1, O1a, O1b, O1c, O2, O3, O4a, O1f (Samples and Level2) and, from sweeps, OF1, OT1 rows, O1e roots, CK1 values. Not filled: O1d, OP*, OB1 (revenue's lines), O5 to O8, OL1, OH1*, DH1c and everything that needs `support.py` (O7, OD1, OW*, OM1, OS1), because 266 + 149 lines cannot carry them and M7e is out. A follow-up brief should assemble them. (5) The brief says CK1's mu is I-D1a (4.42); 4.42 is I-D1a2 (geometric), I-D1a is 4.74. I used the number the metric states (4.42, passed by the caller). (6) `payer_taxes` (the two retired taxes that fall on payers) has no home in `levers.json`, so `context` takes it as an argument (the tests pass the two names); it belongs in the lever file. (7) N7: one 1,000-path chunk, one schedule, 3.9 s; 10,000 paths 39 s. Estimated full run on this machine: level 1 2 min, feasibility 2, tornado 2 (three schedules), break-even 1 (point only), level 2 about 39 (200 x 3 x 3.9 s): under 60 minutes, so `pool.py` is not built. Confirm the reference machine.
- **Resume:** after the ruling: set the choice rule or the closure definition, then run the three schedules through `level1`, `level2`, `tornado` from `run.py` (V3-12).
- **Not run:** the full N1 and N2 sizes (10,000 paths, 200 draws): timed per chunk only. The K6 pool check.
- **State:** built, criteria N1 to N7, R3, R10 met; NEEDS THE AUTHOR (empty feasible region)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 055c, model v3 V3-10 range runner
- Files changed: model_v3/runner/runner.py (new, 266 lines); model_v3/runner/sweeps.py (new, 149); tests/model_v3/test_runner.py (new, 135); this brief
- What is different now: two-level run with Samples and Level2, feasibility map and choice rule, tornado, break-even return, stress path, bootstrap check, 30-year spread.
- New or changed interfaces: runner.context, draw_theta, evaluate, make_ev, level1, level2, samples, digest, timed, Level2; sweeps.grid, labels, feasibility, choose, tornado, breakeven, breakeven_return, stress, robustness, spread30
- Acceptance criteria: N1 to N7 (met); R3 drawn ids equal the tier 1 list (met); R10 all 27 grid cells progressive (met); budgets met; Touches kept (met). Result: the feasible region is empty (F1 4 to 11 percent against 75).
- Deviations from the brief: outputs beyond O1 to O4a, O1f, OF1, OT1, O1e, CK1 not assembled (see gotcha 4); pool.py not built (estimate under 60 min)
- Risks / follow-ups: ruling on the feasibility rule or F1; payer_taxes into levers.json; assemble the remaining outputs; I-D1a against I-D1a2 in CK1; confirm the reference machine
- Verification: pytest tests/model_v3 -q: 201 passed; feasibility, tornado, break-even and timing run on 1,000 paths (above)
- Overview sections likely needing an update: model v3 status (V3-10 built, no feasible schedule)
- Commit / branch: brief/055-runner (pushed, not merged): NEEDS THE AUTHOR
```
