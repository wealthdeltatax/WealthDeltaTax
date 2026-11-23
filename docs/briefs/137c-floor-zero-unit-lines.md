# 137: The class floor (127c alarm): a line whose units are all zero cannot take the year's saving

- **Status:** ready (after 133c merged)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 127c, 132c, 133c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-lien.md` ("Still failing" paragraph and `cap_lien/lien_alarms.csv`); (2) `docs/agents/code.md`. Later: `model_v3/runner/arm.py` (`pre`: the `dead` floor, `self.fl`); `model_v3/core/kernel.py` (units, `family_true`); `docs/model-v3/household-arm-i1-floor.md`.

## Goal
After 133c the floor alarm is the only shortfall left (`min_mid` D4 year 61, D5 year 78; `median_high` D10a year 70 to D1 year 97; about 0.001 to 0.002m per adult). Cause: tax on pension gains takes all of a line's non-pension wealth, its units are 0, units grow multiplicatively, so the year's saving cannot enter and the floor records it. Let such a line restart from its saving, so the account is clean, without changing economics anywhere else.

## Decisions (author, 2026-11-23)
- Merge 133c; fix the floor in a brief (this one). Diagnose first, then the smallest change.
- Preferred design: a line with zero units and positive saving re-creates units from the saving at the year's price (units = saving / price), in the hook; the kernel changes only if the hook cannot do it, and then stop and report.
- Lines whose wealth is negative keep their units (unchanged). No new register input; the restart is a labelled bookkeeping rule, stated in the note.
- Passing grid points and the fixed-rate and legacy arms stay byte-identical; `test_legacy_digest` unchanged.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: diagnose.** A table in `household-arm-i1-floor.md`: every floor line-year at the five grid points (20 paths): line, year, saving, units, balances, whether the saving is positive. Say how many are restartable and how many are another case (e.g. negative saving on zero units). Push.
- **Block 2: fix.** The restart in the hook, with a test (a dead line with saving restarts; closing class total equals the family value, I1 holds; a dead line with no saving stays at zero). Held points byte-identical. Push.
- **Block 3: rerun and note.** Rerun `min_mid` and `median_high` at 20 paths and the other three at 200: shortfall lines and `unpaid_B` per point, any remaining alarm with balances. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change, or a case that is not restartable, is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 310; name any raise), tests, `docs/model-v3/household-arm-i1-floor.md`, `docs/model-v3/household-arm-lien.md`, rerun CSVs under `docs/model-v3/household-arm-run/`. Not the register, the pack, the manifest, the digest fixture or the kernel (unless stopped and reported).

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; held points and legacy account byte-identical.
- At `min_mid` and `median_high` the floor alarm is 0 or each remaining case is listed with its balances and cause.
- I1, the account identity and the ledger ties hold at all five points.

## Out of scope
The deferral rate, per-path loose ends (135c), pension withdrawal, any change to household economics, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 (progress block pushed); block 1 (diagnosis: 28,380 floor line-years, 26,640 restartable at `median_high`, 1,740 not at `min_mid`: negative saving on zero units; table in `household-arm-i1-floor.md`)
- **Next:** block 2 (restart in the hook, test; `min_mid` stays a listed alarm for the author)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/137-floor-zero-units origin/brief/137-floor-zero-units`
- **State:** in progress; branch `brief/137-floor-zero-units`
<!-- progress:end -->
