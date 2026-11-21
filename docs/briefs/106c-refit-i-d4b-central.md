# 106: Refit the I-D4b central with the I-D4h adults per household

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 105c (merged)
- **Read:** `docs/research/012r-b1-derivations.md` (the I-D4b method: type-weighted lognormal fit per household type from Table 2.9 quartiles, adult counts assumed per type); row I-D4b and I-D4h in `docs/model-v3/inputs.md`; `docs/research/102r-parameter-map-stocks-and-cells.md` section 4; `docs/research/data/102r/existing_row_audit.csv` (I-D4b rows); `docs/model-v3/` any file that quotes 54.9 (grep).

## Goal
Replace the I-D4b central (54.9%, built on 1.77 adults per household) with a central built on the I-D4h value 1.93 (16 and over, Table 2.11), so the two rows agree.

## Decisions (author, 2026-11-21)
Refit the central with I-D4h. Adult means 16 and over, as held.

## Design
1. Reproduce the old central 54.9 from the 012r method first and report the reproduction; stop and report if it does not reproduce.
2. Recompute with adults per household scaled so the household-type weighted mean is 1.93 (state exactly how the per-type counts are scaled; scale the 1, 2, 3 counts proportionally, not by adding a type).
3. Keep low 49.3 and high 64.3 unless the refit puts the central outside them; if it does, stop and report.
4. Update the row text (method, the 16-and-over limit, the new central, what the old one was), the judgement flag stays. Regenerate `registry/inputs.json`.
5. Find every place that quotes 54.9 or a number derived from I-D4b's central (tests, hooks fixtures, paper text, pack, digests). List them and the changed values in a table; update what the register change requires; stop and report if a model digest moves.

## Touches
`docs/model-v3/inputs.md`, `registry/inputs.json` (generated), `docs/research/012r-b1-derivations.md` (a dated addendum, not a rewrite), tests and fixtures that quote 54.9, any paper text via the build. No model code.

## Acceptance criteria
- Old central reproduced; new central stated with the scaling method; I-D4b and I-D4h agree on adults per household.
- Registry regenerated; v3 suites run in the background (never piped); changed digests, if any, listed for the author.
- Diff limited to Touches.

## Checks to run
`python -I pipeline/build_inputs.py`; the v3 suites; `python -I pipeline/check_gate.py` (known to fail on this checkout; report only if it differs from main).

## Out of scope
I-D4c (its bounds share I-D4b's logic: list its change, do not make it unless it follows by the same method and the author is told), W_min, the pack GDP.

## Open questions
Does I-D4c need the same refit (agent lists the effect).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and fetch line, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
