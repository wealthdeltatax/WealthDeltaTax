# 089: Feasibility map and stress test outputs into Samples (OF1, CK1)

- **Status:** ready (139c and 150c merged; design set 2026-11-23, below; block 1 done on the branch)
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c, 088c, 083c, 140c (the household-arm diagnostic, 2026-11-23) and the author's ruling on the feasibility rule after it
- **Read:** `docs/model-v3/f1-diagnostic/report.md` (from 083c); `model_v3/runner/sweeps.py` (`feasibility`, `choose`, `stress`, `CLOSED`); `model_v3/runner/out_sweeps.py`; `docs/model-v3/outputs.yml` entries OF1 and the CK1 check; `docs/model-v3/metrics.md` rows F1 and CK1.

## Goal
OF1 (F1, M2 and M4a over the 27 schedule-grid points, transition and short) and the CK1 stress check are shaped for the file, under whatever rule the author sets.

## Author rulings, 2026-11-23 (after 140c and 149c)
- **OF1 is a map, not a gate.** Publish F1, M2 and M4a for every schedule-grid point, tolerance and retirement margin; no schedule is called feasible unless it passes the stated 75% threshold. The three named schedules are the best-F1 points under a stated rule, and the file says "none passes the 75% threshold" where that is true. Nothing is relaxed silently. CK1 is reported as it is, with the amplitude-0 caveat (P3 positive at amplitude 0 is a finding to carry, not hide).
- **Phase count:** the household arm uses 10 death phases for the first official run (139c wiring); the legacy arm keeps 6 so its digest does not move. OF1 and CK1 are run at 10. 149c showed the five-year cycle at 6 phases is partly an artifact: best F1 at the 055c rule 9.0% (6), 12.5% (15), 25.5% (30); 10 phases was not run for F1, so the first block here runs F1 at 10 phases for the 27 points at `median_mid` (about 2 minutes) and reports it before anything is written.
- The `market` fund case (140c, after 138c) is a second labelled setting of OF1.

## Decisions (author, 2026-11-20)
055c found no feasible schedule: short-window F1 is 4.0 to 11.2% against 75% with `CLOSED` 1e-9, and CK1's P3 is 100.9 at amplitude 0 over 100 years. 083c measures tolerance, a retirement margin and the CK1 window. The author rules afterwards; this brief is written with those rulings, then set to ready.

## Design
Block 1 result (agent, 10 phases, `median_mid`, 200 paths): best F1 at tolerance 0, margin 0 is 21.5% (`safe`) and 31.5% (`market`), both at `tm50_k05_r100`; a cell reaches 75% only at tolerance 1% with margin 25% (1 cell `safe`, 3 cells `market`); constant-path first shortfall at year 61 to 63, outside the short window. This is what the map must show, unsoftened.
- **OF1 shape:** one record per (grid point, fund setting, schedule-grid point, tolerance, margin) with F1 and M2 and M4a for transition and short, as block 1's `f1_*_grid.csv`; the rule axes are the block 1 sets (tolerance 0, 0.05, 0.25, 1.0 percent of the base; margin 0, 10, 25 percent), each a labelled scenario constant in `sweeps.py` (not a register row, to be challenged). The published headline row is the strictest rule (tolerance 0, margin 0, the 055c rule `CLOSED` 1e-9); the looser rules are rows of the same map and labelled as relaxations, never as the feasibility result.
- **Marker:** per (grid point, fund) the summary holds the best F1 and where, and `none_passes_75` (a stated marker, accepted for OF1 by the validator) where no cell reaches 75% under the rule; where a cell does pass under a relaxed rule the file says which rule.
- **Named schedules:** reported with their own F1 under each rule next to the best-F1 point, so a reader sees the named schedule is not the best one; no schedule is renamed or re-chosen here.
- **Grid points and cost:** OF1 and CK1 at all five grid points and both fund settings (about 2 minutes per point and setting at 200 paths); the other points are not skipped as O1e's are.
- **CK1:** the stress check at 10 phases, both fund settings, window transition plus short, mu = I-D1a central 4.74 (the arithmetic mean), amplitude 0 included and its positive P3 carried as a finding.
- Markers `none_passes_75` and (if used) `not_run_this_point` are added to the validator's accepted list for OF1 and CK1 only; any other non-finite cell stays an error. Coordinate with 057c (its file for the validator).

## Touches
`model_v3/runner/sweeps.py` and `out_sweeps.py` (at their budgets: new code only if it fits, otherwise stop and report), `pipeline/validate_outputs.py` (the two markers), `docs/model-v3/outputs.yml` entries for OF1 and CK1, `docs/model-v3/feasibility-map.md` (the report), tests. Not `arm.py` (330), the kernel, the register or the pack.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 1:** done (F1 at 10 phases, `median_mid`).
- **Block 2: OF1.** Shaped for the file as above, at the five points and both fund settings, with the markers; tests; `feasibility-map.md` has the tables. Push.
- **Block 3: CK1.** Shaped and run as above; the change report; push; stop.
**Stop rule.** A kernel or model change is stop-and-report. After two blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Acceptance criteria
OF1 and CK1 are shaped and validate at smoke size; the summary and `none_passes_75` markers are present where true; nothing relaxed unlabelled; the legacy digest is unchanged; all suites pass; `feasibility-map.md` reports the strict-rule result first.

## Open questions
None (the ruling is above); the agent flags any rule or constant it has to choose.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** parked; not started
<!-- progress:end -->
