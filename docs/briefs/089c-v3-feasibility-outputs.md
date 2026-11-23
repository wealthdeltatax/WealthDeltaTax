# 089: Feasibility map and stress test outputs into Samples (OF1, CK1)

- **Status:** ready, after 139c wiring (the household phase count) and 150c block 2 (both touch the run path); rulings 2026-11-23 below
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
To be completed by the guru after the ruling: which of (a tolerance on `CLOSED`, a retirement margin lever in `levers.json`, a different closure share, a CK1 window of transition plus short) applies, with the constants. CK1's mu is I-D1a central 4.74 (the arithmetic mean), not 4.42.

## Touches
To be set with the design (expected: `model_v3/runner/sweeps.py`, `out_sweeps.py`, `levers.json`, `docs/model-v3/outputs.yml` and `metrics.md` if a constant or definition changes, their tests).

## Acceptance criteria
To be set with the design.

## Open questions
The author's ruling.

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
