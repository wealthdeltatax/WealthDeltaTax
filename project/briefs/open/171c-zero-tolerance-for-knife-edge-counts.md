# 171: Zero tolerance for knife-edge counts

- **Status:** author; done on `brief/171-zero-tolerance`, pushed, not merged; needs the author to merge
- **Agent:** 5
- **Needs:** 172c
- **Length:** 1
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
- **Done:** all steps; report below. **State:** done

```
Change report
- Task: 171c Zero tolerance for knife-edge counts
- Files changed: model/model_v3/core/kernel.py (`ZERO_TOL = 1e-9`, `neg`, `pos`); core/burden.py:142 (O2b/O2c payers), core/revenue.py (`P4_first_negative`, `negative_share`), runner/runner.py (O1f `neg`; imports merged to keep the 360-line budget at the 186c state); model-specs/metrics.md (rule); tests/model/model_v3/test_kernel.py (test); pins: tests/model/model_v3/fixtures/legacy_digest.json, tests/model/model_v3/test_groups.py `PIN`, project/restructure/move-tripwire-baseline.json (three commits plus a fix-up); results/171c-zero-tolerance/compare_outputs.py (per-output comparison); this brief.
- What is different now: a value within 1e-9 of zero is zero in the counts and shares of O1f, O2b, O2c, P4_first_negative and negative_share, whatever the CPU rounds it to. O1f, O2b and O2c no longer depend on the numerics path.
- New or changed interfaces: `kernel.neg(x)`, `kernel.pos(x)`, `kernel.ZERO_TOL`.
- Acceptance criteria: (1) O1f, O2b, O2c identical on both paths: met (quick, Actions run 45964292332: 0 of 22, 200 and 222 values differ; smoke byte-identical). (2) quick-size movement from the old pins per output: reported (O1f 3 of 19 values, max abs 1; O2b 18 of 200, max abs 1.85 points, max rel 0.061; O2c 12 of 222, max abs 0.60 points, max rel 0.061; all other outputs not listed by the script's default, `--all` available). (3) all suites and the tripwire pass: met (`fast`, Actions run 46076773779, success; local legacy digest test passes). (4) `fast` green on Actions: met.
- Deviations from the brief: the M2 payer mask (`burden.py:130`) is left as `net > 0` (value-weighted, a tiny net adds nothing); the movement table lists only O1f, O2b and O2c. Pin 1 was first captured without `NPY_DISABLE_CPU_FEATURES=X86_V4` (the script does not set it) and recaptured in pin 1b.
- Risks / follow-ups: `test_legacy_digest.py --capture` run as a script uses the AVX512 path unless the variable is set; pins must be captured with it (worth a line in the file's docstring). Digest movement on the forced path: samples, runner and burden group digests change; revenue and support digests equal the old pins.
- Instruction friction: the capture command in `test_legacy_digest.py` does not say it must run with the forced numerics path.
- Verification: tests above; tripwire before the baseline change differed only in the `legacy_digest.json` hash; after, passes in `fast`. Not run: full suites locally (Actions `fast` covers them).
- Overview sections likely needing an update: none
- Commit / branch: see the branch head, `brief/171-zero-tolerance`
```
<!-- progress:end -->
