# 142: Saving gradient: saving that rises with wealth, as a labelled scenario axis

- **Status:** ready (after 141c: both touch `arm.py` and the grid)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 124c, 125c, 128c (merged), 141c
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-validation.md` (BF-13 and the concentration gap: 0.41 to 0.20-0.34 against 0.50); (2) `docs/agents/code.md`. Later: `docs/research/129r-was-access-audit.md` and `docs/research/data/129r/feasibility_map.csv` (saving by wealth band, RF/ONS, `proxy`, scenario only); `docs/model-v3/household-arm-account.md`; `model_v3/runner/arm.py` (saving ratio, `sav`); the saving inputs in `docs/model-v3/inputs.md` (I-D1j).

## Goal
The household arm applies one saving ratio to every line, so wealth concentration collapses over time (top-decile share 0.41 to 0.20-0.34; BF-13 observed 0.50). Add a labelled **saving-gradient** scenario axis: the saving ratio varies by line (lower in the bottom deciles, higher at the top) as a range across labelled gradients, not a fitted result and not a central case, and report what it does to concentration and to the outputs. Off by default.

## Decisions (author, 2026-11-23)
- A scenario, not a measurement: the held evidence (RF "Before the Fall", ONS tables) is a `proxy` for saving by wealth band; there is no household-level saving by starting wealth without a licence. Label each gradient with its evidence class and a challenge note.
- Three labelled gradients: `flat` (today, the default), `mild` and `steep`; the shapes (saving ratio by decile) are chosen in block 1 from the held evidence and stated with their source or marked `unset`/author's judgement. No gradient is tuned to hit 0.50: report what each gives, never fit to the target.
- Default `flat`: every existing output byte-identical. No register row now; named constants, labelled.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: evidence and shapes.** `docs/research/142c-saving-gradient.md` with a small CSV: what the held sources say about saving by wealth band (page, flag), the proposed `mild` and `steep` saving ratios by decile and tail line, and what is `unset`. Convert PDFs on the fly with `to_markdown.py`; no new sources. Push.
- **Block 2: switch.** `sav` by line from the chosen gradient (decile ratios scaled to the same aggregate saving as `flat`, state the scaling and test it); tests: `flat` byte-identical; aggregate saving equal across gradients within tolerance; I1 and the account identity hold. Push.
- **Block 3: rerun and note.** Five grid points, 20 paths, three gradients: the top-decile share by year (1, 10, 30, 100), BF-13 and its gap, M1a and M2 as ranges, shortfall lines. `household-arm-validation.md` updated: the gradient range against the observed 0.50, **no fitting, no headline number**. Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 310; name any raise), `docs/research/142c-saving-gradient.md` and data, `docs/model-v3/household-arm-validation.md` and its CSVs, `docs/model-v3/household-arm-run/` (`run_grid.py`), tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- Every saving figure cited has a page and flag; `unset` parts stated.
- `flat` byte-identical; all suites pass; `test_legacy_digest` unchanged.
- The note shows concentration by year under each gradient against 0.50 and says it is a scenario, with no fitted value.

## Out of scope
Per-line heterogeneity beyond the gradient, withdrawal (141c), the register rows, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/142-saving-gradient origin/brief/142-saving-gradient`
- **State:** ready; not started (after 141c)
<!-- progress:end -->
