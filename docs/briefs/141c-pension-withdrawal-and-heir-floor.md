# 141: Pension withdrawal scenario and the heir-protection floor (both off by default)

- **Status:** ready (after 139c: touches `arm.py` and `pension_lien.py`)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 132c, 133c, 137c, 135c, 138c, 139c
- **Read (block 0: the first two only):** (1) `docs/research/129r-was-access-audit.md` (IFS/ELSA drawdown row) and `docs/research/data/129r/feasibility_map.csv`; (2) `docs/agents/code.md`. Later: the drawdown source named there (open the PDF in `docs/research/data/129r/` through `pipeline/to_markdown.py`, only the pages you cite); `docs/model-v3/household-arm-lien.md`; `model_v3/core/pension_lien.py`; `model_v3/runner/arm.py`; `docs/decisions.md` (the 2026-11-22 pension rulings).

## Goal
Two labelled scenario switches, both off by default so every existing output is unchanged. (1) **Pension withdrawal**: today the pension is never drawn in life (a ruling for the first integrated run; a mandatory labelled sensitivity before any long-run claim). Add a withdrawal rate by age band as a range (low / mid / high), the draw going to non-pension wealth (liquid), still inside the assessed base. (2) **Heir-protection floor**: the lien's settlement draw on the pension at death is uncapped (author ruling 2026-11-23: base case); add a labelled floor that leaves the heir a stated share of the pension.

## Decisions (author, 2026-11-22 and 2026-11-23)
- Withdrawal is a **scenario**, evidence class `proxy` at best (IFS/ELSA financial-wealth drawdown, wealthier faster), never a forecast; the range is read from the held 129r sources only. No UKDS licence, no new data collection. If the held sources do not give a rate by age band, say so and use the nearest labelled statement, flagged `unset` where there is none.
- The pension stays in the assessed base while held; withdrawal moves value from the pension class to non-pension classes (cash and net financial), so total wealth and the base are unchanged by the draw itself.
- Heir's share: the lien settlement stays uncapped in the base case. The floor is a sensitivity (a share of the pension the draw cannot take, 0 default; scenario values 0 / 25 / 50%, labelled; the unpaid remainder is written off and reported in the ledger as a write-off, not hidden).
- Default off for both: `test_legacy_digest`, the legacy arm and every household output are byte-identical with the switches off. No register row now (a later register brief); the constants are named and labelled in the code.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: evidence.** `docs/research/141c-withdrawal-range.md` and a small CSV: the drawdown figures found in the held 129r sources, each with page and flag (`text`, `read from chart`), the proposed low / mid / high rates by age band, and what stays `unset`. Convert PDFs on the fly with `to_markdown.py`; no new sources. Push.
- **Block 2: withdrawal switch.** In the hook: pension draw each year by the labelled rate for the line's stage, into non-pension classes; the kernel's `pen` and the I1 check stay consistent; tests (switch off: byte-identical; switch on: class total and I1 hold, total wealth unchanged by the draw). Push.
- **Block 3: heir floor and rerun.** The floor in `pension_lien.py` (tests: floor 0 is today's settlement; floor 50% leaves half the pension and reports the write-off). Rerun the five grid points at 20 paths with withdrawal low / mid / high and floor 0 / 50%: shortfall lines, lien balances, write-offs, ledger tie. One table in `household-arm-lien.md`. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 310; name any raise), `model_v3/core/pension_lien.py`, `docs/research/141c-withdrawal-range.md` and its data folder, `docs/model-v3/household-arm-lien.md`, tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- Every drawdown figure has a page and flag; the range and its `unset` parts are stated.
- Both switches off: all suites pass and all outputs byte-identical; `test_legacy_digest` unchanged.
- With the switches on, I1, the account identity and the ledger ties hold at all five points; write-offs from the floor are reported.

## Out of scope
The deferral rate, the saving gradient (142c), per-path regimes, the register rows, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/141-withdrawal-heir-floor origin/brief/141-withdrawal-heir-floor`
- **State:** ready; not started (after 139c)
<!-- progress:end -->
