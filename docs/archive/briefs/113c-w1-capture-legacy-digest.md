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
- **Done:** `tests/model_v3/fixtures/legacy_digest.json` captured on origin/main a0b70e8 (seeds 7 and 11, 5 schedules, P = 20, chunk 10; `runner.digest` of Samples and of each group's ids: runner, revenue, burden, support, sweeps). `tests/model_v3/test_legacy_digest.py` (58 lines).
- **Next:** W2 onward prove bit-equality against this fixture.
- **Decisions:** the three named schedules do not exist yet (089c), so five fixed lever-grid points stand in (low corner, centre, high corner, two more corners); the context is built with `once` so the sweeps group's static cells (DH1a, DH1b) are in the digest; the reproduction call is the file itself (`--print`, `--capture`).
- **Gotchas:** one `compute()` takes about 25 s a seed; the two tests take 127 s together (no per-test limit is configured); the fresh-process test uses one seed to keep that down.
- **Resume:** none.
- **Not run:** nothing.
- **State:** done; merged

Change report
- Task: brief 113c (W1), capture the legacy reference digest
- Files changed: `tests/model_v3/fixtures/legacy_digest.json` (new, the reference); `tests/model_v3/test_legacy_digest.py` (new, the two tests and the capture command); this brief's progress block
- What is different now: a stored digest of the legacy arm exists; any later change that moves a Samples digest or a group digest fails `test_the_legacy_digest_equals_the_fixture` with a message saying it needs the author.
- New or changed interfaces: none in code; `python tests/model_v3/test_legacy_digest.py --capture` recaptures (author's word only), `--print [seed]` prints the digest.
- Acceptance criteria: reproduces in a second run, a fresh process and a clean checkout of origin/main: met (same-process and fresh-process equal in the test; a clean worktree at a0b70e8 gave a digest equal to the fixture). Test passes: met, 49 s for the fixture test and 127 s for both tests. Existing suites unchanged: model_v3 254 passed; data (5), cards (1) and hooks (1) fail identically on bare main (fixture currency), not touched. Diff limited to Touches: met.
- Deviations from the brief: five stand-in grid points instead of "the three named schedules plus two corners" (the named schedules are not computed until 089c).
- Risks / follow-ups: a recapture is needed if the lever grid points, the manifest `once` ids or the pack change; the test costs about 2 minutes of the v3 suite.
- Instruction friction: none
- Verification: `python pipeline/run_suites.py` (7 of 10 suites passed, the three failures as on main); `python -I pipeline/check_agent_docs.py` exit 0.
- Overview sections likely needing an update: none
- Commit / branch: `brief/113-legacy-digest`; brief 113 merged, ready to retire
<!-- progress:end -->
