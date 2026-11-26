# 169: One numerics path, first Actions runs, split final run

- **Status:** ready; Agent 2 (or any free code agent)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 168c (workflow on main), 057c, 164c
- **Read:** `project/briefs/done/168c-github-actions-long-runs.md` (interim report: the CPU finding, F0 answer, accept.sh gotchas), `.github/workflows/model-checks.yml`, `tests/model/model_v3/accept.sh`, `model/model_v3/run.py` (120-line budget), `model/tools/validate_outputs.py`, `project/restructure/move_tripwire.py`, `project/agents/agent-code.md`

## Goal
Every committed number and hash holds on every machine (GitHub's, the author's, an agent's), so `fast` is green on every runner; then the long checks (smoke, converge, accept) run on GitHub and are read; then the final-size grid can be split across jobs.

## Decisions (author, 2026-11-26)
1. The workflow is on `main` now (merged by the guru with the 168c files).
2. **Force one numerics path everywhere:** switch off numpy's AVX512 path with `NPY_DISABLE_CPU_FEATURES` and regenerate the pins once on that path. Same numbers on every machine; the pins change once, openly.
3. `--final` stays the author's act (`run.py` refuses it; leave that).

## Design (guru; labelled for challenge)
**Stage A, the numerics path.** (a) Find the smallest feature list that reproduces on both kinds of runner (the 168c agent used `X86_V4 AVX512_ICL AVX512_SPR`; confirm by running the digest tests on this machine with and without it, and read the CPU line each Actions run logs). (b) Set it where numpy is first imported: top of `model/model_v3/run.py` (before any numpy import; `os.environ.setdefault`; mind the 120-line budget, so put it in a tiny module imported first, e.g. `model/model_v3/numerics.py`, and say why in a comment), the root `conftest.py` of each test tree that imports numpy, `model-checks.yml` (env at workflow level), and the tripwire's child processes. (c) Regenerate the pins: `legacy_digest.json`, the `test_groups` pin, the tripwire baseline (inputs, legacy, pack, evaluation hashes), the stored run hashes, and any `quick` reference file. One commit per pin family, each with the old and new value in the message. (d) **Prove the change is last-bit only:** run `--size quick` (or the smallest meaningful size) on both paths and report the largest absolute and relative difference per output id (O, OR, OT, checks). If any headline value differs by more than 1e-9 relative, stop and report to the author before regenerating anything. (e) Document it in `project/agents/agent-code.md` and `model-specs/acceptance.md` (one paragraph: the variable, why, and that the author's own machine must set it).
- **Checkpoint:** pushed to a branch; check: `fast` green on at least two runs that landed on different CPU models (read the logged CPU line), and the tripwire PASS locally.

**Stage B, `accept.sh` runs whole.** Step 1 fails at collection under `python -I` (`No module named 'tests'`, `test_pension_lien.py`); fix at the cause (the test's import or the invocation) so `accept.sh` passes end to end, rather than routing around it in the workflow. Check step 5 against a real `quick` file (057c notes say it failed on O8 nulls: the marker is now `reform_not_defined`; report the actual state). The `accept` job then calls the whole script.
- **Checkpoint:** pushed; check: `accept.sh --check` on `results/057c-evidence/quick-q4/outputs.json` and the fast tests of the script.

**Stage C, first runs (the agent starts them).** Merge stages A and B to `main` only by the author's word; until then start jobs on `main` as they are (`gh workflow run model-checks.yml --ref main -f run_smoke=true -f run_converge=true -f run_accept=true`; if the dispatch API refuses, report the exact error and the click path). Poll with `gh run list`/`gh run view`, read failures with `--log-failed`, fix on the branch and rerun. Record run ids, wall times, runner CPU model. Report the first real results: converge at real sizes (never run before), accept steps 1 to 7, the two quick outputs byte-identical. Do not tick `run_final_size`.

**Stage D, split final run (design only; ask the author before building).** F0 found `--point` writes a complete single-point `outputs.json`, not a mergeable partial; targets, O1e ends and level 1 info are only in memory, and `run.py` has no merge entry point. Write a half-page design: `run.py --point P --partial-out F` writing the per-point docs plus targets, O1e ends and info; a new module (not `run.py`) that reads the five partials and applies `scenario_range`, the O1e marker rewrite, `mark_no_payer`, PENDING entries and the document wrapper exactly once; a test that the merge of the five partials at `--size smoke` equals the single `run.main` output byte for byte. Also measure, from the first runs, one final-size point's wall time with O1e (O1e runs at the first point only, `median_mid`). Stop after the design and report; the author decides.

## Touches
`model/model_v3/run.py` (one import line), new `model/model_v3/numerics.py`, test `conftest.py` files, `.github/workflows/model-checks.yml`, `tests/model/model_v3/accept.sh` and the one test that fails under `-I`, the pin files named above, `project/restructure/move_tripwire.py` only for the env on child processes, `project/agents/agent-code.md`, `model-specs/acceptance.md`, `STATUS.md`. No model arithmetic, no scenario values, no `deploy.yml`.

## Acceptance criteria
- `fast` is green on runners with and without AVX512 (two logged CPU models), and locally.
- The difference report in stage A (d) is on file under `results/` (a short note; large files stay out).
- `accept.sh` passes whole locally in its step 1 and on Actions; the two accept artifacts are byte-identical.
- `smoke`, `converge`, `accept` each have one green run with id and wall time in the change report.
- No run used `--final`.

## Checks to run
The fast suites one pytest per suite, `check_agent_docs.py`, the tripwire after `git clean -fdx` and a commit, YAML lint. The long checks are the Actions runs. Pin regeneration is committed before the tripwire (it reads git history).

## Out of scope
Any model change, the SWF redesign, the full C3, changing the refusal of `--final`, building stage D.

## Open questions
Stop and report if the stage A difference is above 1e-9 relative on any headline output, if the feature list cannot be made to reproduce on a runner, or if a pin family needs a change beyond its hash.

## Implementation notes
<!-- progress:start -->
- **Done:** superseded by 170c: the author ruled, pins regenerated, accept job whole, first run read. See the 170c change report.
- **Next:** author (170c NEEDS THE AUTHOR list).
<!-- progress:end -->

## Change report
(The agent fills this in, per `project/agents/change-report.md`.)
