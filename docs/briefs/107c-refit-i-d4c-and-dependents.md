# 107: Refit I-D4c and the rows that quote its threshold

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 106c (merged)
- **Read:** the 106c addendum in `docs/research/012r-b1-derivations.md` (method, scaling factor 1.0934, I-D4c result 91.5%, threshold 1.78 times W_min = £267,412); rows I-D4b, I-D4c, I-H2a1 to I-H2a10, I-M6a, I-M6h and the I-W6 coverage notes in `docs/model-v3/inputs.md`; `docs/model-v3/judgement-decisions.md`; `docs/research/data/102r/existing_row_audit.csv`; `model_v3/core/base.py` (what reads I-D4c).

## Goal
Make I-D4c consistent with I-D4b's refit, and update every row that quotes its equivalent household threshold (1.61 times W_min, £241,721), reporting every model digest that moves.

## Decisions (author, 2026-11-21)
Refit I-D4c, as its own brief; stop for review if digests move.

## Design
1. Reproduce the old I-D4c (92.7% at £150,000; 95.8% at £112,500) from the 012r script, then take the 106c refit (91.5% and 95.0%). Keep its bounds 89.7 and 96.4 unless the new central falls outside them (it does not).
2. List every row and file that quotes 1.61, £241,721 or 92.7 (grep inputs.md, judgement-decisions.md, `docs/model-v3/added/`, tests, fixtures, pack code). For each, say whether the value follows from I-D4c by arithmetic (update it with the same method, show the working in a table) or is an independent figure (leave it).
3. **Before regenerating or editing any test**, run the v3 suites with the new I-D4c and I-H2a thresholds in a scratch copy and record which digests, test pins and outputs move and by how much. If any model digest moves, stop after writing the table and the change report with the numbers; do not update pins. If none moves, proceed.
4. Update the rows, regenerate `registry/inputs.json`, update the tests that quote the old values.

## Touches
`docs/model-v3/inputs.md` (I-D4c and the dependent rows), `docs/model-v3/judgement-decisions.md`, `docs/research/012r-b1-derivations.md` (dated addendum), `registry/inputs.json` (generated), tests and fixtures that quote the old values. No model code. Name any further file you must touch before editing it.

## Acceptance criteria
- Old I-D4c reproduced; new value and the dependent-row table stated with working.
- A table of every digest, pin or output that moves, with old and new values, written before any pin is changed.
- Registry regenerated; suites run in the background (never piped); the pre-existing failures (five in `data`, one in `hooks`, same on main) reported as such.
- Diff limited to Touches.

## Checks to run
`python -I pipeline/build_inputs.py`; v3, data and hooks suites in the background; `python -I pipeline/check_gate.py --all` (fails on main; report only a difference).

## Out of scope
W_min, I-D4b, the pack GDP, the cell model.

## Open questions
Which pins move and whether the author accepts the new digests (author, if any move).

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
