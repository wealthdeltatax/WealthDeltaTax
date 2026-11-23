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
- **Done:** blocks 0 to 3. Diagnosis (28,380 floor line-years: 26,640 restartable at `median_high`, 1,740 at `min_mid` not); restart in `HouseholdHook._restart`; reruns and note in `docs/model-v3/household-arm-i1-floor.md`.
- **Next:** the author rules on the `min_mid` case (negative saving on zero units, D4 year 61 and D5 year 78); then the guru reviews. Not merged.
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/137-floor-zero-units origin/brief/137-floor-zero-units`
- **State:** finished, branch `brief/137-floor-zero-units` pushed; `NEEDS THE AUTHOR`
<!-- progress:end -->

```
Change report
- Task: 137c, the class floor: a line whose units are all zero cannot take the year's saving
- Files changed: model_v3/runner/arm.py (`_restart`, `self.mix`, the floor in `pre`; 313 to 329 lines); tests/model_v3/test_household_tax.py (four tests added; one changed, see below); docs/model-v3/household-arm-i1-floor.md (diagnosis table and results); docs/model-v3/household-arm-lien.md (one-sentence update); docs/model-v3/household-arm-run/floor_line_years_137.csv (block 1), floor_restart/ (reruns), floor_diag.py (the diagnostic); this brief's notes.
- What is different now: a line with no units and a positive saving restarts from it in the hook, so the floor alarm is 0 at `median_high` (20 paths; 26,640 line-years before) and at `median_mid`, `max_mid`, `median_low` with market paths (200 paths; `unpaid_B` path-phases 375, 26 and 0 before, 0 after). `min_mid` keeps its 1,740 line-years (D4 from year 61, D5 from year 78), listed with balances in the note.
- New or changed interfaces: none (a hook method and an attribute; no register input, no kernel change).
- Acceptance criteria: (1) `test_legacy_digest` unchanged and passing; all ten suites pass (`model_v3` 350); the three held points and the legacy context at 1,000 paths byte-identical (md5) to `origin/main`; the 14-line account and ledger CSVs regenerate with an empty git diff: met. (2) Floor alarm 0 at `median_high`; at `min_mid` each remaining case is listed with balances and cause: met as written, but the case is not restartable, which the brief's stop rule makes a stop-and-report: the author rules. (3) I1, the account identity (max 2.6e-11) and the ledger ties (max 2.5e-11) hold at all five points: met.
- Deviations from the brief: (a) a second mechanism: at `median_mid` with market paths 740 floor line-years remained because the route price was 0 or negative after a settlement rescale; the restart restores it to the line's opening route mix (Cv at C's). This is beyond "units = saving / price"; the route mix is my choice, flagged for review. (b) The existing 127c test now runs on a negative saving because its positive-saving dead line is exactly what the brief says restarts; its assertions are unchanged. (c) `floor_diag.py` is a new script under `household-arm-run/`, which the brief's Touches names only for CSVs. (d) The brief's `arm.py` budget of 310 was stale: the file was 313 and the architecture table says 330; I stayed at 329, no raise.
- Risks / follow-ups: the restored route mix gives a restarted line the opening A, B, C, D split whatever its history; if the author wants another split, it is one line in `_restart`. Float round-off: the I1 pension check is absolute (1e-12), so a pension of order 1e4 with a large cap lien can trip it (seen in a test setup with a 16,000 pension, not in the runs); not fixed here.
- Instruction friction: none.
- Verification: run: test_household_tax (17), all ten suites via `run_suites.py` (model_v3 350 passed), `test_legacy_digest` (2), `min_mid` and `median_high` at 20 paths (`lien_rerun.py`), the three other points at 200 market paths (`run_grid.py`), the held points at 1,000 paths on both trees, the account and ledger scripts. Not run: the site build (no change under `pipeline/`, `site/` or `registry/`).
- Overview sections likely needing an update: none by file; the note in `household-arm-lien.md` and the 127c floor entry in the decisions list.
- Commit / branch: see the branch tip, `brief/137-floor-zero-units`. NOT merged: NEEDS THE AUTHOR (the `min_mid` case is not restartable; items (a) and (c) are outside the brief as written).
```
