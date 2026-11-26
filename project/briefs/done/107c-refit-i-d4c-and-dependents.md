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
- **Done:** I-D4c refitted: old 92.7% (95.8% at £112,500) reproduced from the 012r script; new **91.5%** (95.0%), household threshold 1.78 times W_min (£267,412; was 1.61, £241,721); bounds 89.7 and 96.4 kept. Dependents updated by arithmetic: I-H2a1 to I-H2a10 centrals, I-M6a, I-M6h, the I-W6 coverage notes and the 016g line. Scratch-copy run done before any edit: no digest, pin or output moved. Registry regenerated; judgement-decisions cells mirrored; 012r addendum written.
- **Next:** none.
- **Decisions:** I-H2a method as printed in each row (linear between the 25th, 50th, 75th percentile points; two-piece lognormal outside them, deciles 9 and 10); I-M6 central = liability / (£13,568bn x I-D4c), bounds untouched (they use the I-D4c bounds and the other year's liability).
- **Gotchas:** (1) I-H2a5 old central computes 50.5, the row printed 50.4 (an existing 0.1 rounding slip); new 52.7 is computed. (2) `tornado.md` lines 54 and 72 quote 92.7 (a dated design note, outside Touches, left). (3) Model code reads I-M6a and I-M6h and the I-H2a rows through the register, yet nothing pinned moved: model_v3 tests assert against the register values or fixtures not built from them.
- **Resume:** branch `brief/107-refit-i-d4c`.
- **Not run:** nothing skipped.
- **State:** done
<!-- progress:end -->

### What follows from I-D4c (working)
| Row | Old | New | Working |
|---|---|---|---|
| I-D4c central | 92.7 | 91.5 | 012r script with counts x 1.0934 (106c); wealth above the household threshold matching the adult share 52.41% |
| I-D4c at £112,500 | 95.8 | 95.0 | same |
| I-H2a1 .. a10 central | 61.2, 64.8, 62.4, 58.7, 50.4, 47.9, 36.1, 27.5, 19.9, 9.9 | 63.8, 67.7, 65.1, 61.3, 52.7, 50.9, 38.7, 29.8, 22.6, 11.7 | share below £267,412 (was £241,721) in each Table 2.6 decile |
| I-M6a central | 0.056 | 0.057 | £7.03bn / £12,415bn (= 13,568 x 91.5%) = 0.0566 |
| I-M6h central | 0.144 | 0.146 | £18.15bn / £12,415bn = 0.1462 |
| I-W6 coverage, 016g line | about 1.61 | about 1.78 | text |
Independent figures left: I-W6 values (household shares), I-M6c (£1.61bn), I-T3o (31.61), I-H5b (1.61 elasticity), I-D4a (2,211.48).

### Digests, pins and outputs (scratch copy and real run)
| Item | Old | New |
|---|---|---|
| model_v3 suite (includes the 055c PIN, 084c and 092c digests) | 230 passed | 230 passed, none moves |
| `data` suite | 5 failed (pre-existing, `test_validate_outputs`) | the same 5 |
| `hooks` suite | 1 failed (pre-existing, `test_cli`) | the same 1 |
| `check_gate.py --all` | exit 1 | exit 1, output identical to main |

Change report
- Task: brief 107c, refit I-D4c and the rows that quote its threshold
- Files changed: `docs/model-v3/inputs.md` (I-D4c, I-H2a1 to a10, I-M6a, I-M6h, I-W6 coverage, 016g line); `docs/model-v3/judgement-decisions.md` (six cells); `docs/research/012r-b1-derivations.md` (addendum); `registry/inputs.json` (generated); this brief
- What is different now: I-D4c central 91.5%, and the rows that quote its threshold follow it.
- New or changed interfaces: none
- Acceptance criteria: old I-D4c reproduced, met; dependent-row table with working, met; digest table written before any pin change (none changed), met; registry regenerated, suites run in the background, pre-existing failures reported as such, met; diff within Touches, met
- Deviations from the brief: none
- Risks / follow-ups: `tornado.md` lines 54 and 72 still quote 92.7; I-H2a5's old printed 50.4 was 50.5
- Instruction friction: none
- Verification: `build_inputs.py` (293 rows); all 10 suites (8 pass, `data` and `hooks` as on main); `check_gate.py --all` identical to main; scratch run before edits
- Overview sections likely needing an update: none
- Commit / branch: `brief/107-refit-i-d4c`; merged, ready to retire
