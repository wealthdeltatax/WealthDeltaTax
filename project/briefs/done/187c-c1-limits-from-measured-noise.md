# 187: Set the C1 limits from measured seed noise

- **Status:** done, merged 2026-11-28 (not yet run on Actions: `run_noise` untested)
- **Agent:** 6
- **Needs:** none
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-27
- **Depends on:** none (statistics only; works on either numerics path; the pins are not touched)
- **Read:** `tests/model/model_v3/test_converge.py` (the fixtures and C1); `model-specs/acceptance.md` rows 79 to 100; the converge log of Actions run 45956946871 (job `converge`, failed C1 on O3); `model/model_v3/runner/runner.py` `level1`

## Goal
Replace the guessed C1 limit (0.15 for every output and statistic) with limits derived from measured noise, so C1 fails only when the model is unrepeatable and not when an output is merely noisy. Known failure (Actions 45956946871, commit d834b8a4, `legacy` arm, `N1` = 10,000): O3 spread 0.191 (mean), 0.262 (P10), 0.192 (P90) against 0.15. The values for O1, O2 and O4a are not known: the test stops at the first failing output.

## Decisions (author, 2026-11-27)
Set limits from data, as for 171c. The limits come from a written rule fixed before the numbers are seen (below); the author signs the rule's constants.

## Method (pre-registered, written before measuring)
1. Run `level1` on the `legacy` arm, S_central, short horizon, for **10 seeds** at `N1` = 10,000 (the five C1 seeds and five more). Keep the per-path arrays of O1, O2 (overall), O3 and O4a (overall) for each seed; do not summarise inside the run.
2. From each seed's paths take the first 1,250, 2,500, 5,000 and all 10,000 paths and compute the mean, P10 and P90. (Paths are independent within a seed, so the first n paths are exactly a run of n paths.) Also pool two disjoint seeds for N = 20,000 (five pairs).
3. For every output, statistic and N: the standard deviation across seeds, `sd(N)`. Test the Monte Carlo law: `sd(N) * sqrt(N)` constant within about 20%. Report the ratio table. If it fails for an output (heavy tail, knife edge), say so and say what the numbers do instead.
4. **Limit rule (proposal):** for each output and statistic, `limit = q * sd(N1)`, where `q` is the 99th percentile of the range (max minus min) of 5 draws, in units of sd. For a normal that is about 4.6 (guru's recollection: verify by a 10^6-draw simulation and report the figure used). With q = 4.6 a healthy model fails C1 about once in a hundred runs; the actual spread in the 10 seeds must be under the limit for every row, or the rule is wrong and the report says so. The author may choose a different false-failure rate.
5. Also report, for each output, the limit as a share of the output's own cross-path standard deviation and of its mean (so a reader can see whether the limit is loose in the output's own terms), and the N needed to bring O3's limit down to 0.15 under the measured scaling (information, not a proposal).

## Design (one push)
- `model/tools/c1_noise.py`: the measurement above; writes `results/converge/c1-noise.csv` (output, statistic, N, sd, range, ratio) and `results/converge/c1-noise.md` (tables, the rule, the limits, caveats). Runs on Actions: add a `workflow_dispatch` input `run_noise` and a job that uploads the two files; use `--workers`. Estimate 10 seeds at 10,000 paths about 2.5 hours serial (C1 and C2 together took 1 h 47 for 7 such runs); say what it took.
- `tests/model/model_v3/c1_limits.json`: the limits per output and statistic with the rule, the date and the commit it was measured at. `test_converge.py` reads it; C1 reports all outputs and statistics that fail (collect, do not stop at the first). `model-specs/acceptance.md` C1 row and the Assertions text updated.

## Touches
`model/tools/` (new script, tool-size budget as in `agent-guru.md`), `tests/model/model_v3/test_converge.py`, `tests/model/model_v3/c1_limits.json`, `model-specs/acceptance.md`, `.github/workflows/model-checks.yml` (new dispatch input and job only), `results/converge/`.

## Acceptance criteria
- Report with the machine header and the Actions run URL; every table row from real output; the pre-registered rule applied as written (any departure listed).
- The 10 measured spreads sit under the derived limits, or the report says which do not and why.
- Fast job green; the regular converge job unchanged except for reading the limits file and listing all failures. No change to the model.
- Do not rerun the full converge job on the branch; the guru dispatches it after merge.

## Out of scope
Changing N1; the model; the legacy arm's own ruling (kept to learn from); the household arm (a later brief if wanted); C2 and C3 limits.

## Open questions
For the author: the false-failure rate (default about 1 in 100) and whether the limits should also have an absolute ceiling (for example 0.5) so a drift in a heavy-tailed output cannot be hidden by a wide measured limit.

## Implementation notes
<!-- progress:start -->
- **Done:** `model/tools/c1_noise.py` (measure, analyse, limits file); 10 seeds at 10,000 paths measured here (about 30 min, not 2.5 h); `results/converge/c1-noise.md`, `.csv` and the per-path arrays; `tests/model/model_v3/c1_limits.json`; `test_converge.py` C1 reads it and lists every failure; `acceptance.md` C1 row and Q2; `run_noise` input and `noise` job in `model-checks.yml`; tool test.
- **Next:** the author answers the three questions in the change report; then dispatch `run_noise` on Actions for the run URL (set `run_accept` false in the same dispatch: it defaults true), and merge.
- **Resume:** branch `brief/187c-c1-limits-from-measured-noise`. The limits file is final unless the author changes the rate, the ceiling or the O4a handling: `python -I model/tools/c1_noise.py analyse --write-limits tests/model/model_v3/c1_limits.json [--ceiling X]` regenerates it from the saved paths in seconds.
- **State:** needs the author
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 187c, C1 limits from measured seed noise
- Files changed: model/tools/c1_noise.py (new); tests/model/tools/test_c1_noise.py (new, 4 tests); tests/model/model_v3/c1_limits.json (new); tests/model/model_v3/test_converge.py (C1 only); model-specs/acceptance.md (C1 row, Q2); .github/workflows/model-checks.yml (run_noise input, noise job only); results/converge/ (report, csv, 10 per-path files, 2.3 MB); this brief.
- What is different now: C1 limits are q x sd(N1) per output and statistic, q = 4.613 (10^6-draw simulation; the brief recalled 4.6), instead of 0.15 everywhere. Limits (mean, P10, P90): O1 0.164, 0.275, 0.321; O2 0.033, 0.070, 0.117; O3 0.307, 0.456, 0.340; O4a 0.101, 0, 0. The failing run's O3 spreads (0.191, 0.262, 0.192, the five C1 seeds here give the same) sit under the O3 limits. C1 collects all failures.
- New or changed interfaces: c1_noise.py run|analyse; workflow_dispatch input run_noise (default false); no model change, no pin change.
- Acceptance criteria: report with every table row from real output, rule applied as written: met, plus one addition (slope of log sd on log N, departure listed below). Spreads under the limits: met (the five C1 seeds: none above; the range of all ten seeds: none above). Machine header and Actions run URL: PARTLY: machine header yes; no Actions run URL, the measurement ran here because the session's GitHub token cannot dispatch workflows. Fast job green: not seen (no Actions); locally the tool and budget tests, agent docs, lane plan and tripwire pass and test_converge.py collects. Converge job unchanged except reading the limits and listing failures: met. Not rerun on the branch: met.
- Deviations from the brief: run here, not on Actions; added the slope table (the ratio to one reference is dominated by the reference's own noise: O2 and O3 means read 1.5 to 1.9 below N1); the tool imports `model_v3.numerics` so it needs NPY_DISABLE_CPU_FEATURES=X86_V4 set before numpy when imported by a test (the fast job sets it).
- Findings: the Monte Carlo law holds on slopes for O1 mean (-0.50), O1 P10, O2 P10, O3 P10 and P90 (-0.43 to -0.59), O4a mean (-0.42); steeper for O3 mean (-0.71) and O2 mean (-0.65), shallower for O2 P90 (-0.40), and O1 P90 is -0.90 (heavy tail or a knife edge); with 10 seeds each slope is uncertain, so none of these is shown to break the law. O4a P10 and P90 are constant: the overall O4a takes three distinct values per path, and P10 = P90 = 25.07 in every seed at every N, so sd = 0 and the rule's limit is 0. O3's limit is 0.31 to 0.46, about 2 to 3 times the guessed 0.15: bringing it to 0.15 needs about 42,000 to 92,000 paths (information).
- Risks / questions for the author: (1) limit 0 for O4a P10 and P90 is right while the statistic is constant but fails on any change at all (one ulp across numerics paths); keep, drop those two from C1, or give them a floor? (2) false-failure rate: 1 in 100 as the default; (3) absolute ceiling: none applied; the widest limit is 0.46 (O3 P10), so a ceiling of 0.5 would change nothing today. The sd comes from 10 seeds (about 22% uncertain), so limits could be 20% off either way. The household arm is not covered (out of scope).
- Instruction friction: none new.
- Verification: pytest tests/model/tools (16 passed); test_budget, test_groups; check_agent_docs; build_lane_plan --check; move_tripwire PASS; test_converge.py --collect-only (4); measurement and analysis rerun from the saved paths gave the same table.
- Overview sections likely needing an update: none.
- Commit / branch: brief/187c-c1-limits-from-measured-noise (pushed, not merged: NEEDS THE AUTHOR)
```
