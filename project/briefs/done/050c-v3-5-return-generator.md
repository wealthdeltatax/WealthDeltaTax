# 050: Model v3 V3-5: return generator

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 048
- **Read:** `docs/model-v3/architecture.md` 2.2, 3.1 and 6.2 (R1 to R7); `docs/model-v3/returns-method.md`; `docs/model-v3/returns-gap.md`; `docs/model-v3/stage-c-decisions.md` item 4; `docs/model-v3/acceptance.md` V3-5 row.

## Goal
The level 1 return generator and the level 2 parameter draw, reproducible from a seed.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/returns.py` (260 lines): AR(1) with normal innovations on the arithmetic mean, marginal SD and lag-1 from the pack series (the sample ends in 2019, author 2026-11-18; effective sample as the pack gives it), stationary start; the stationary block bootstrap (mean block 3, wrapping within each contiguous segment) as a check; the level 2 draw of mean, SD and lag-1 from their register ranges; sample statistics; `loop_windows`. No draw is clipped. Streams from `numpy.random.SeedSequence(20261118).spawn(5)`, in the order of 3.1.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-5 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/returns.py`, `tests/model_v3/test_returns.py`, this brief's progress block.

## Acceptance criteria
- R1 to R7 pass; sample statistics pinned to 0.001 as in the acceptance V3-5 row (the pin is re-derived if the 2019 end changes n, and the change is written in the change report).
- 100,000-path mean, SD and lag-1 within 0.05, 0.05 and 0.02 of the inputs; the level 2 band reproduces its register range within 0.02.
- `returns.py` at most 260 lines; it imports numpy and `core/pack.py` types only.
- The pinned sample statistics are re-derived on the 2019 sample and reported; a difference from the register's 4.742 and 8.219 stops the build for the author (author, 2026-11-18).
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The window rule's use in revenue (V3-7); replay of historical paths as the generator.

## Open questions
The architecture pins n 117, written before the author ended the sample in 2019. Read n from the pack, report it, and re-derive the pinned statistics from the pack series before pinning.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/core/returns.py` (121 lines, budget 260; numpy only, no pack import needed since the pack arrives as an argument and `Row` is duck-typed) and `tests/model_v3/test_returns.py` (93 lines, budget 220). `real_series`, `sample_stats`, `ar1_paths`, `block_bootstrap`, `level2_draw` (Latin hypercube), `loop_windows`, `streams` (SeedSequence(20261118).spawn(5)). R1 to R7 pass. `pytest tests/model_v3 -q`: 116 passed.
- **Next:** V3-7 (revenue, fund, identity) once 051c is done.
- **Decisions:** parameters in percent, paths as fractions (kernel's arithmetic growth). Level 2 draws mean, SD and lag-1 independently, normal about the register central with the standard error that makes low and high the 10th and 90th percentiles. The normal quantile is Acklam's approximation (1e-9), because the brief allows numpy only. Sample lag-1 is the v2 definition over the series in order (pairs 1939 with 1947); the bootstrap wraps within contiguous segments.
- **Gotchas:** (1) The pinned statistics re-derived on the pack series (sample ends 2019): n 117, arithmetic 4.7423, geometric 4.4200, SD 8.2188, lag-1 0.3030, effective sample 63. They equal the register's 4.742, 4.420, 8.219, 0.303 and n is unchanged, so no stop for the author. (2) 100,000-path generator: mean, SD and lag-1 within 0.05, 0.05 and 0.02; level 2 10th and 90th percentiles within 0.02 of the register low and high. (3) The branch was stacked on 048 until 048 merged.
- **Resume:** none needed.
- **Not run:** nothing in the brief.
- **State:** done; merged to main by the auto-merge rule (048c merged first)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 050c, model v3 stage V3-5: return generator
- Files changed: model_v3/core/returns.py (new, 121 lines); tests/model_v3/test_returns.py (new, 93); this brief
- What is different now: v3 can draw level 1 return paths and level 2 parameters from a seed, and compute the sample statistics from the pack.
- New or changed interfaces: SEED, STREAMS, streams, real_series, sample_stats, ar1_paths, block_bootstrap, level2_draw, loop_windows in model_v3.core.returns
- Acceptance criteria: R1 to R7 pass (met); 100,000-path statistics and level 2 band within tolerance (met); returns.py 121 of 260 lines, numpy only (met); pinned statistics re-derived on the 2019 sample and equal to the register (met, n unchanged at 117); git diff --stat limited to Touches (met)
- Deviations from the brief: none
- Risks / follow-ups: (1) none now: 048 is on main; (2) level 2 independence of the three parameters is my choice (the sample correlation of the estimates is not modelled); (3) architecture says n 117 and effective 63: both confirmed
- Verification: pytest tests/model_v3 -q: 116 passed
- Overview sections likely needing an update: model v3 build status (V3-5)
- Commit / branch: brief/050-return-generator, merged to main
```
