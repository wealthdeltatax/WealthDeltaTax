# 171: Zero tolerance for knife-edge counts

- **Status:** ready; was draft, released after 170c (author asked for pin first, then tolerance)
- **Agent:** 5
- **Needs:** 172c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 170c
- **Read:** `results/169c-numerics/difference-report.md`, `model-specs/metrics.md` (O1f, O2b, O2c definitions), `model/model_v3/` where O1f and the O2 shares are computed

## Goal
O1f (share of paths with negative net revenue) and the O2b and O2c threshold shares no longer depend on the CPU's rounding. A value that is zero in theory counts as zero.

## Decisions (author, 2026-11-26)
Pin one path first (170c), then add the tolerance. Tolerance size is a guru proposal for challenge: treat |value| below 1e-9 (in the quantity's own units, relative to the scale of the series) as zero.

## Design
1. Find every comparison against zero or a threshold that feeds a count or share (O1f, O2b, O2c and any like them: sign tests, `<`, `<=`, `>` on net revenue, shortfall, burden). List them with file and line before changing any.
2. Show for each the size of the near-zero values that exist (a histogram of |value| below 1e-6 on the quick run) so the tolerance is chosen from data, not assumed.
3. Add one shared helper (one place, named, documented in `metrics.md`) and use it in each. No other arithmetic changes.
4. Run on both numerics paths (with and without `NPY_DISABLE_CPU_FEATURES=X86_V4`): O1f, O2b and O2c must be byte-identical across paths at smoke and quick size. Report how far each number moved from the pinned value, and regenerate the pins once, in separate commits, after the author reads the report.

## Touches
The compare sites found in step 1, the new helper, `model-specs/metrics.md`, pins, tests. Brief is draft: the file list is completed by step 1.

## Acceptance criteria
O1f, O2b, O2c identical on both paths; the quick-size movement from the old pins reported per output; all suites and the tripwire pass; `fast` green on Actions.

## Out of scope
Any change to a scenario value, schedule, or the meaning of an output.

## Open questions
Whether the tolerance should be absolute or relative per output (step 2 informs it; ask the author).

## Implementation notes
<!-- progress:start -->
- **Done:** nothing yet.
- **Next:** wait for 170c.
<!-- progress:end -->
