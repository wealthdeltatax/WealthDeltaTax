# 089: Feasibility map and stress test outputs into Samples (OF1, CK1)

- **Status:** parked (waits for the author's ruling on the feasibility rule, after 083c; 2026-11-21: the feasibility numbers were measured under the legacy 3.5% rule, so the rule is re-examined after the cell model and the comparison run, not before)
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 084c, 088c, 083c and the author's ruling
- **Read:** `docs/model-v3/f1-diagnostic/report.md` (from 083c); `model_v3/runner/sweeps.py` (`feasibility`, `choose`, `stress`, `CLOSED`); `model_v3/runner/out_sweeps.py`; `docs/model-v3/outputs.yml` entries OF1 and the CK1 check; `docs/model-v3/metrics.md` rows F1 and CK1.

## Goal
OF1 (F1, M2 and M4a over the 27 schedule-grid points, transition and short) and the CK1 stress check are shaped for the file, under whatever rule the author sets.

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
