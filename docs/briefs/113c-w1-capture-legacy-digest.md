# 113 (W1): Capture the legacy reference digest before any wiring

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 112r (merged)
- **Read:** (1) `docs/model-v3/kernel-wiring-design.md` section 3.7 (the legacy switch and the digest) and the W1 row of 4.0; (2) `model_v3/runner/runner.py` (`digest`, `Samples`, `core_run`) and the existing determinism tests in `tests/model_v3/`; `docs/agents/code.md`.

## Goal
Store a reference digest of what the legacy arm computes today, with a test that fails if any later change to the kernel, revenue, burden or support code moves it. No digest exists in the tests or docs now, so every wiring brief that follows (W2 to W7) has nothing to prove it is bit-equal to. This brief is the gate for all of them.

## Decisions (author, 2026-11-22)
112r adopted: legacy is the default arm and must stay bit-equal to a digest captured first (Q9).

## Design
1. `tests/model_v3/fixtures/legacy_digest.json`: `runner.digest` of `Samples`, and the SHA-256 of each output group the runner writes, for fixed seeds, a small schedule grid (the three named schedules plus two grid corners) and `P = 20` paths. Record the git commit it was captured on and the exact call that reproduces it.
2. `tests/model_v3/test_legacy_digest.py`: recomputes the digest in the test and compares to the fixture; a second test runs twice in the same process and in a fresh process and asserts byte-equal. The failure message says what to do (a change that moves it is a legacy change and needs the author).
3. Capture on a clean checkout of `origin/main` before any other edit, and prove it reproduces on a second clean checkout.

## Touches
`tests/model_v3/fixtures/legacy_digest.json` (new), `tests/model_v3/test_legacy_digest.py` (new). No code, register, pack or doc beyond the progress block.

## Acceptance criteria
- The digest reproduces in a second run, a fresh process and a clean checkout; the test passes and takes under the suite's per-test time limit (report the time).
- Existing suites unchanged; no digest, pin or output moves (pre-existing data and hooks failures reported as on main).
- Diff limited to Touches.

## Checks to run
v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`.

## Out of scope
Any change to the kernel or runner, the hook, the arm switch, the household arm (W2 onward), any register or paper edit.

## Open questions
If the runner is not bit-reproducible across processes (threads, hash order, floating-point reductions), report exactly where and stop; do not weaken the comparison.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and fetch line, last block pushed, first action)
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
