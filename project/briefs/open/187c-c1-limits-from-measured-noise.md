# 187: Set the C1 limits from measured seed noise

- **Status:** ready
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
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
