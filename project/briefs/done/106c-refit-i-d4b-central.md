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
- **Done:** old central reproduced (54.9% of adults, wealth 92.7% at £150,000; 62.5% and 95.8% at £112,500; 47.642m adults over 26.991m households = 1.765 per household). Refit: all type counts (1, 2, 3) times 1.0934 (= 1.93 / 1.7651; counts 1.093, 2.187, 3.280; no type added) gives a mean of 1.93 and a central of **52.4%** (52.41). Low 49.3 and high 64.3 kept (52.4 lies inside). Row I-D4b, the 012r addendum and `registry/inputs.json` (central only) updated; `judgement-decisions.md` mirror updated; `tests/hooks/test_codes.py` line 105 now expects 52.4%.
- **Next:** author decides I-D4c (below); then merge.
- **Decisions:** the target is the I-D4h central 1.93 (not 52,043/26,991 = 1.9282, which gives 52.44, same to one decimal). Common scale factor rather than shifting only the multi-adult types.
- **Gotchas:** (1) `check_gate.py --all` exits 1 with output identical to main's. (2) Suites: `model_v3` 230 passed (no digest moved: the model reads no I-D4b value); `data` 5 failed (`test_validate_outputs` fixture tests, the same five fail on main); `hooks` 1 failed (`test_cli::test_both_fixture_spokes_resolve_cleanly_in_both_modes`, fails on main too); all others pass. (3) `docs/model-v3/judgement-decisions.md` quotes the central and is outside the brief's Touches; changed one cell, flagged. (4) The I-D4b row sentence on the held bracket now says the central lies below it, which still holds.
- **Resume:** branch `brief/106-refit-i-d4b` (from main 52a3321), pushed.
- **Not run:** nothing skipped; the five `data` and one `hooks` failures are not mine.
- **State:** done except the author's I-D4c decision; NEEDS THE AUTHOR
<!-- progress:end -->

### Places quoting I-D4b's central or numbers derived from it
| Place | Quotes | Action |
|---|---|---|
| `docs/model-v3/inputs.md` row I-D4b | 54.9, 1.77, 62.5 at £112,500 | updated: 52.4, text, 60.2 |
| `registry/inputs.json` (generated) | central 54.9 | regenerated: 52.4 |
| `tests/hooks/test_codes.py:105` | "54.9%" from the real register | 52.4% |
| `docs/model-v3/judgement-decisions.md:25` | central 54.9 | 52.4 (outside Touches) |
| `docs/research/012r-b1-derivations.md` section 1 | 54.9, 92.7, 1.61, 1.48 | left as history; dated addendum added |
| `docs/model-v3/inputs.md` row I-D4c, I-W6 rows, 016g line 331 | 92.7, 1.61, £241,721 | not changed (I-D4c below) |
| `docs/research/012r-b3-derivations.md` line 6, `102r` and `103r` audit files, `STATUS.md` | 54.9, 92.7, "1.77" as audit history | not changed |
| `tests/data/fixtures/outputs.fixture.json`, `source/` | no I-D4b central; no `{{i:I-D4b}}` hook in `source/` | none |
| model digests (084c, 092c, `test_groups` PIN) | none | unchanged |

### I-D4c (open question for the author)
By the same method (the household threshold that reproduces the adult share), I-D4c would be **91.5%** (was 92.7%) at £150,000 and 95.0% (was 95.8%) at £112,500; the equivalent household threshold is 1.78 times W_min (£267,412), not 1.61 (£241,721). That is inside its bounds 89.7 to 96.4. Not made: out of scope. If made, rows quoting 1.61 or £241,721 follow (I-D4c; I-H2a1 to I-H2a10 central thresholds; the I-W6 coverage notes; I-M6a, I-M6h, which divide by I-D4c's wealth range), and the model reads I-D4c, so digests may move.

Change report
- Task: brief 106c, refit I-D4b central with the I-D4h adult count
- Files changed: `docs/model-v3/inputs.md` (row I-D4b); `docs/model-v3/judgement-decisions.md` (one cell, outside Touches); `docs/research/012r-b1-derivations.md` (dated addendum); `registry/inputs.json` (generated); `tests/hooks/test_codes.py` (expected 52.4%); this brief
- What is different now: I-D4b central 52.4% (was 54.9), built on a mean of 1.93 adults per household, agreeing with I-D4h.
- New or changed interfaces: none
- Acceptance criteria: old central reproduced, met (54.9, 92.7); new central and scaling stated, met; I-D4b and I-D4h agree on 1.93, met; registry regenerated, met; v3 suites run in the background, met, no digest moved; diff limited to Touches, met except `judgement-decisions.md`
- Deviations from the brief: one extra cell in `judgement-decisions.md`
- Risks / follow-ups: I-D4c decision (above); `data` (5) and `hooks` (1) suite failures pre-exist on main
- Instruction friction: none
- Verification: `build_inputs.py` (293 rows); all suites; `check_gate.py --all` against main (identical)
- Overview sections likely needing an update: STATUS register-mismatch line (I-D4b against I-D4h)
- Commit / branch: `brief/106-refit-i-d4b`; NEEDS THE AUTHOR (I-D4c)
