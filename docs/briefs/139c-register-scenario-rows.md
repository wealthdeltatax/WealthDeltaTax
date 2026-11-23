# 139: Register rows for the household-arm scenario constants (lien rate, pension basis, housing gain, fund return)

- **Status:** ready (after 137c, 135c, 138c: the fund-return switch must exist first; the rows are the last register edit before the first official run; 2026-11-23: blocks 0 and 1 (the rows and the gate hash: `inputs.md`, `registry/inputs.json`, no `arm.py`) may start now while 135c is under way; block 2 (wiring) waits for 135c and 138c; the fund-return row's name and values follow 138c's switch, so enter it as a placeholder and say so)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 134r, 131r (merged), 138c
- **Read (block 0: the first two only):** (1) `docs/research/134r-lien-deferral-rate.md` section 7 and `docs/research/131r-pension-basis-sensitivity.md` section 7 (the proposed rows); (2) `docs/agents/code.md`. Later: `docs/model-v3/inputs.md` (the I-D1h to I-D1l rows as the pattern); `registry/inputs.json`; `model_v3/runner/arm.py` (`PROPERTY_GAIN`, the lien rate, the fund switch); `pipeline/check_gate.py` (the gate hash).

## Goal
Enter, as register rows, the four scenario constants that are still named constants or kernel defaults, so each is labelled, ranged and open to challenge: (1) the lien deferral rate (134r: 0 / 2 / 3% real, central 2%), (2) the pension valuation basis multiplier (131r: 1.00 / 1.96 / 2.02, `scenario`, ONS SCAPE stays the pack), (3) the housing holding gain (0.016455, F-20, now `PROPERTY_GAIN` in `arm.py`), (4) the fund return setting (138c: `safe` or `market`).

## Decisions (author, 2026-11-22 and 2026-11-23)
- Lien rate: central 2.0% real (risk-free financing benchmark), high 3.0% (STPR), low 0% (policy floor), one rate for both liens; all (J). The kernel default stays 0.0 until the row is entered and the arm reads the row; then the arm's default is the register central. This changes household-arm outputs: say so and show before and after at the five grid points.
- Pension basis: ONS SCAPE is central in the pack; the IFS multiplier is a labelled scenario on the opening stock only (1.00 / 1.96 / 2.02, by band 1.64 / 2.02 / 2.01 / 1.91 / 1.98), run as a sensitivity, never a headline. The arm reads it only when switched on; default 1.00.
- Row ids: the next free letters in the I-D1 group (`I-D1m` to `I-D1p`); `I-D15a` in 134r was a placeholder and is not used. Check the group before choosing.
- A register edit changes the gate hash: re-bless it as the checker prescribes, in this brief only, and say so in the change report.

## Added by author ruling, 2026-11-23 (149c): the household arm's death-phase count
In block 2 (wiring), the household arm runs with **10 death phases** (`n_phase=10`), set in `switches.py` as a labelled numerical-approximation constant (not a register row: it is an approximation, not an input), passed through the hook or the runner call for the household arm only. The legacy arm keeps 6, `test_legacy_digest` and every legacy output stay byte-identical. Say in `household-arm-run.md` that every household output after this change is at 10 phases and show a before and after at the five grid points (the lump in M1a, the ledger ties, `unpaid`, shortfall lines). If it cannot be done without a change in `core/`, stop and report.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: rows.** The four rows in `docs/model-v3/inputs.md` and `registry/inputs.json` (low, central, high, unit, evidence class, label, challenge note, as in the 134r and 131r proposals), the gate hash re-blessed. Check the legacy digest is unchanged. Push.
- **Block 2: wire.** The arm reads the lien rate and the housing gain from the register (the named constant removed or set from the row), the basis multiplier and fund setting as switches with default 1.00 and `safe`. Tests: defaults reproduce today's household outputs except the lien rate (which moves to 2%); `test_legacy_digest` unchanged. Push.
- **Block 3: before and after.** At the five grid points, 20 paths: shortfall lines, `unpaid`, lien balances and the ledger tie with the lien rate at 0 and at the register central; one table in `household-arm-lien.md`. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`docs/model-v3/inputs.md`, `registry/inputs.json` (and the gate hash file the checker names), `model_v3/runner/arm.py` is at 329 of its 330 lines (137c; the old 'budget 310' is stale): new scenario-switch code goes in the new `model_v3/runner/switches.py` (budget 200, a new file; `arm.py` gains call sites only, or shrinks); any growth of `arm.py` past 330 is stop-and-report, `docs/model-v3/household-arm-lien.md`, tests. Not the kernel, the pack, the manifest or the digest fixture.

## Acceptance criteria
- Four rows exist, each with low, central, high, class and label; the gate checker passes with the new hash.
- `test_legacy_digest` unchanged; all suites pass; the legacy arm byte-identical.
- The before and after table is in the lien note; the household default is the register central and says so.

## Out of scope
Pension withdrawal, the saving gradient, per-path regimes, any headline number, `I-D1l` or `I-D1k` changes.

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 (progress block pushed)
- **Next:** block 1 (the four rows in `inputs.md` and `registry/inputs.json`, gate hash re-blessed, legacy digest check); block 2 waits for 135c (and 138c)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/139-register-scenario-rows origin/brief/139-register-scenario-rows`
- **State:** in progress; branch `brief/139-register-scenario-rows`
<!-- progress:end -->
