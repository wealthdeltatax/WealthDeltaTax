# 171: Zero tolerance for knife-edge counts

- **Status:** author; helper applied and quick comparison done on Actions (run 45964292332); waiting for the author to read the movement report before the pins are regenerated (tolerance decided: absolute 1e-9)
- **Agent:** 5
- **Needs:** 172c
- **Length:** 1
- **Asks:** zero tolerance absolute 1e-9 (recommended) or relative
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 170c
- **Read:** `results/169c-numerics/difference-report.md`, `model-specs/metrics.md` (O1f, O2b, O2c definitions), `model/model_v3/` where O1f and the O2 shares are computed

## Goal
O1f (share of paths with negative net revenue) and the O2b and O2c threshold shares no longer depend on the CPU's rounding. A value that is zero in theory counts as zero.

## Decisions (author, 2026-11-26)
Pin one path first (170c), then add the tolerance. Tolerance size is a guru proposal for challenge: treat |value| below 1e-9 (in the quantity's own units, relative to the scale of the series) as zero.

## Design
1. Find every comparison against zero or a threshold that feeds a count or share (O1f, O2b, O2c and any like them: sign tests, `<`, `<=`, `>` on net revenue, shortfall, burden). List them with file and line before changing any.
2. Show for each the size of the near-zero values that exist (a histogram of |value| below 1e-6 on the quick run) so the tolerance is chosen from data, not assumed.
3. Add one shared helper (one place, named, documented in `metrics.md`) and use it in each. No other arithmetic changes.
4. Run on both numerics paths (with and without `NPY_DISABLE_CPU_FEATURES=X86_V4`): O1f, O2b and O2c must be byte-identical across paths at smoke and quick size. Report how far each number moved from the pinned value, and regenerate the pins once, in separate commits, after the author reads the report.

## Touches
The compare sites found in step 1, the new helper, `model-specs/metrics.md`, pins, tests. Brief is draft: the file list is completed by step 1.

## Acceptance criteria
O1f, O2b, O2c identical on both paths; the quick-size movement from the old pins reported per output; all suites and the tripwire pass; `fast` green on Actions.

## Out of scope
Any change to a scenario value, schedule, or the meaning of an output.

## Open questions
Whether the tolerance should be absolute or relative per output (step 2 informs it; ask the author).

## Implementation notes
<!-- progress:start -->
- **Claimed:** branch `brief/171-zero-tolerance` (from main 49c2bfd).
- **Step 1, compare sites** (feed a count or share):
  - `model/model_v3/runner/runner.py:230` `M1 < 0` -> `neg` -> O1f.
  - `model/model_v3/core/burden.py:130` `(net > 0)` payer mask in `m2` (weights; value-weighted, negligible).
  - `burden.py:142` `(net > 0)` in `_cash` -> payer-count denominator for O2b/O2c; `burden.py:148` `r > x/100` threshold shares (not knife-edge for tiny nets: ratio far below the cut).
  - `model/model_v3/core/revenue.py:274` `below = after & (m1 < 0)` (P4_first_negative); `revenue.py:284` `negative_share` (`short < 0`, `long_ < 0`).
  - Not sites: `kernel.py:238` (integer diagnostic on `unpaid_B`), `revenue.py:121`/`:282` already snap at 1e-12.
- **Step 2, histogram** (legacy-digest samples, seeds 7 and 11, 20 paths, 5 schedules; both numerics paths; script `hist171.py`): |burden net| over 42M values: 21.6M exact 0, 7.6k between 1e-21 and 1e-12 (noise), **none between 1e-12 and 1e-9**, 5.9k between 1e-9 and 1e-6 (real). |M1| over 600 per-path values: 200 below 1e-12 (zero in theory), none from 1e-12 to 1e-6. So 1e-9 separates cleanly in both quantities.
- **Decision (author):** absolute 1e-9, in the quantity's own units. Helper `ZERO_TOL`, `neg()`, `pos()` in `core/kernel.py`; spec note in `model-specs/metrics.md`; test in `test_kernel.py`.
- **Step 4, runs.** Smoke (local, 50 paths): `outputs.json` byte-identical on both numerics paths. Quick (Actions run 45964292332, hosted runner, `.github/workflows/171c-quick.yml`, temporary; `results/171c-zero-tolerance/compare_outputs.py`): new code on the forced path (`new_off`) against the AVX512 path (`new_avx`): **O1f 0 of 22, O2b 0 of 200, O2c 0 of 222 values differ**. Whole-file sha256 differ (`run_date`).
- **Movement from the old pins** (old code at 49c2bfd, forced path, against new code, forced path; quick size, differing values of the compared cells): O1f 3 of 19, max abs 1 (a path-count flip at zero-in-theory net revenue); O2b 18 of 200, max abs 1.85 points, max rel 0.061; O2c 12 of 222, max abs 0.60 points, max rel 0.061. All other outputs: not listed by the script's id filter; run `compare_outputs.py --all` locally if wanted.
- **Not done:** whether the runner had AVX512 is in the `lscpu` step of the quick jobs (not read); the full suites, the tripwire and `fast` on this branch after the merge of main; pin regeneration (separate commits, after the author reads this); remove the temporary workflow before merge.
<!-- progress:end -->
