# 168: GitHub Actions for the long runs

- **Status:** ready; Agent 2 (or any free code agent)
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 057c and 164c (both merged 2026-11-26)
- **Read:** `.github/workflows/deploy.yml` (the only workflow today), `tests/model/model_v3/accept.sh`, `model/model_v3/run.py` (the `--size`, `--point`, `--workers`, `--o1e-draws` options; `--final` is refused), `model-specs/acceptance.md`, `project/agents/agent-code.md`, the 057c brief's handover (`project/briefs/done/057c-v3-12-run-script-and-acceptance.md`)

## Goal
The long checks run on GitHub, not on the author's machine: one workflow the author can start by hand, plus a fast job on every push. An agent also starts the first run and reports the result.

## Decisions (author, 2026-11-26)
All long work runs on GitHub Actions. `--final` stays the author's act: no job passes it unless the author ticks an input when starting the run, and for now `run.py` still refuses it (do not change that). The agent starts the first runs itself.

## Design (guru proposal, labelled for challenge)
New file `.github/workflows/model-checks.yml`. Do not touch `deploy.yml`. A GitHub-hosted job stops at 6 hours, so work is split into jobs that run side by side. Every job runs `git clean -fdx`-equivalent (fresh checkout), installs the pinned requirements, uses `python -I` as the repo does (`sys.path.insert(0, 'model')`), and uploads its output files as a run artifact.

1. **fast** (on every push to main, on pull requests, and by hand; about 15 min): the quick suites, one pytest per suite (`tests/model/data`, `gate`, `tools`, `tests/project`, `tests/website/*`), `tests/model/model_v3` with `-m "not converge"` and smoke ignored, `project/tools/check_agent_docs.py`, `model/tools/check_gate.py --all`, and the tripwire (needs `fetch-depth: 0`).
2. **smoke** (by hand; about 30 min): `tests/model/model_v3/test_smoke.py`.
3. **converge** (by hand; about 3.5 h): `tests/model/model_v3/test_converge.py -m converge`.
4. **accept** (by hand; about 2.5 h): two `--size quick` runs, `validate_outputs.py`, `accept.sh --check` (step 5), `accept.sh --compare` (step 6: byte-identical) and step 7. Do not call the whole of `accept.sh` if that makes one job exceed 5 hours; call its `--check` and `--compare` modes and the new job steps instead, so `accept.sh` stays the single definition of the steps. Upload both output files.
5. **final run, split** (by hand, only if the box "run final size" is ticked): one job per grid point (matrix over the five `POINTS`), each with `--size final --point <p>` and a 5.5 hour cap, uploading its partial output; then a merge job that assembles the range, validates, and uploads `outputs.json`. The run script must write per-point partial files that the merge job can combine with the same range rule as `run.py` (`scenario_range`, one place). **Stage F0 is a check, not a build:** report (with the code reference) whether `--point` already writes mergeable partials and whether one final-size point fits in 5.5 hours on a 2 to 4 vCPU runner (use the measured 94 min without O1e from the 057c notes, and `--workers`). If either is no, stop, report, and leave job 5 out. Do not guess.
6. **Inputs on the manual start:** `run_smoke`, `run_converge`, `run_accept`, `run_final_size` (booleans, default false except `run_accept`); no input exists for `--final`.

Every job writes the commands, tool versions and wall time to its log. Pin action versions as `deploy.yml` does. Use `concurrency` so a second start of the same job does not cancel a running long one.

## Stages
- A: fast job and the workflow skeleton with the manual inputs. Checkpoint: pushed to a branch; check: `fast` passes on the branch (start it, see below).
- B: smoke, converge, accept jobs. Checkpoint: pushed; check: each started once by hand and its result read.
- C: the final-size matrix (only after the F0 check says yes). Checkpoint: pushed; check: one point run at `--size quick` through the same matrix job to prove the merge, never a final run.

## Starting the runs (the agent does this)
After each stage, start the workflow on the branch with `gh workflow run model-checks.yml --ref <branch> -f run_smoke=true ...` (a workflow must exist on the default branch to appear in the Actions tab, but `gh workflow run --ref` works for a branch once the file is pushed; if GitHub refuses, merge the skeleton to main in a tiny first commit by author's word and report). Watch with `gh run list` and `gh run watch`, read failures with `gh run view --log-failed`, fix and rerun. If the session's token cannot start workflows (a 403 or "Resource not accessible"), stop and report the exact error and the click path for the author: Actions tab, "Model checks", "Run workflow", branch, tick boxes. Do not tick `run_final_size` in any agent-started run.

## Touches
`.github/workflows/model-checks.yml` (new), possibly `tests/model/model_v3/accept.sh` (only to expose steps as modes), a short `project/agents` note on how to start and read a run, `STATUS.md`. Not `deploy.yml`, not model code (stage C may add a small `--point` partial-writer only if F0 shows it is missing and the author agrees).

## Acceptance criteria
- `fast` is green on main.
- `smoke`, `converge` and `accept` each have one green manual run, linked in the change report, with run ids and wall times.
- The artifacts of the accept run contain two byte-identical `outputs.json` files.
- Stage F0 is answered in the report either way.
- No run was started with `--final`.

## Checks to run
`check_agent_docs.py`; the fast suites locally before pushing the workflow; YAML lint (`python -c "import yaml; yaml.safe_load(open(...))"`). The long runs are the Actions runs themselves.

## Out of scope
The SWF redesign, any model change, a full C3 run (a later manual run), changing `deploy.yml`, changing the refusal of `--final`.

## Open questions
Ask the author before any change outside Touches, and if GitHub minutes or runner size look like a limit (private repos have monthly minutes; report the cost of one `accept` plus `converge` run).

## Implementation notes
<!-- progress:start -->
- **Done:** stage A and stage B written and pushed on `brief/168-github-actions-long-runs` (draft PR 3, only so `pull_request` runs `fast`): `.github/workflows/model-checks.yml` with `fast`, `smoke`, `converge`, `accept` and the four inputs (no `--final` input); `accept.sh --r6` mode. Stage F0 answered: no (below).
- **Next (the author):** (1) say whether the skeleton may go to `main` (GitHub cannot dispatch a workflow that is not on the default branch: `POST .../workflows/model-checks.yml/dispatches` returns 404 for the branch), then the agent starts smoke, converge and accept; (2) decide the CPU-dependent digest (below), else `fast` is red on about half of the runners.
- **Decisions:** pytest without `-I` (a test imports `tests.model...`; `accept.sh` step 1 fails under `-I` the same way, so the accept job calls only `--check`, `--compare`, `--r6`); `check_gate.py --all` report-only (exit 1 by design while every gate is closed); `tests/website/layout` left out of `fast` (needs Quarto and a Playwright browser); `poppler-utils` installed (the pack builder calls `pdftotext`); pins inline (`numpy==2.5.3 pyyaml==6.0.3 pytest==9.1.1 openpyxl==3.1.5 bibtexparser==1.4.3`, Python 3.13).
- **Gotchas:** the legacy digest, `test_groups` and the tripwire evaluation hashes depend on the CPU (see the report); GitHub-hosted runners are a mix of Intel and AMD.
- **Resume:** `git checkout brief/168-github-actions-long-runs`.
- **Not run:** `smoke`, `converge`, `accept` (cannot be started before the workflow is on `main`); no run with `--final`.
- **State:** stages A and B written; blocked on the author

Change report (interim)
- Task: brief 168c, GitHub Actions for the long runs
- Files changed: `.github/workflows/model-checks.yml` (new); `tests/model/model_v3/accept.sh` (`--r6` mode, one line); this brief.
- Acceptance criteria:
  - `fast` green on main: not met yet. The workflow is on the branch only. On the branch the fast job has run seven times: runs on an AMD EPYC 7763 fail `test_legacy_digest` and `test_groups::test_an_empty_group_changes_no_number` (and the tripwire pack and evaluation hashes); runs on Intel Xeon (8370C, 6973P, 6975P) and AMD EPYC 9V74 pass all of it (suites 97, 17, 5, 16 + 1 skipped, 8, 27, 67, 59, 28, 13; model suite 408 passed in 8.5 min; tripwire PASS in about 85 s). Cause measured, see below.
  - `smoke`, `converge`, `accept`: not started; GitHub does not list or dispatch a workflow that is not on the default branch (404 by file name and by path). Wall times and run ids to follow.
  - Two byte-identical `outputs.json` in the accept artifacts: not run.
  - Stage F0: answered, no. (a) `--point` does not write mergeable partials: `run.main` with one point writes a complete single-point `outputs.json` (`outs = docs[0]`, after `mark_no_payer`, the O1e marker rewrite and the PENDING entries, wrapped by `wr.document`); `scenario_range` takes the per-point assembled docs from `run_point`, the targets, the O1e ends and the level 1 info live in memory, and no merge entry point reads files; `run.py` is at its 120-line budget. A merge job needs new code in `run.py`. (b) Time fits: one final-size point without O1e is 5,655 s (94 min, serial, 2 cores; 057c notes), far under the 5.5 h cap, so one hosted job per point is feasible. Job 5 is left out, as the brief says.
  - No run was started with `--final`: met (no input, no flag in any step).
- Deviations from the brief: `check_gate.py --all` is report-only; `tests/website/layout` not in `fast`; pytest without `-I`; `poppler-utils` and pins added.
- Risks / follow-ups:
  1. **CPU-dependent numerics (needs the author).** numpy float64 `exp`, `log` and `pow` take an AVX512 path (`X86_V4`) on CPUs that have it and another path elsewhere; the results differ in the last bits (measured on the runners and reproduced here with `NPY_DISABLE_CPU_FEATURES="X86_V4 AVX512_ICL AVX512_SPR"`: `exp` hash `cc54...` instead of `c9c0...`, and the legacy digest test fails). Every fixture and hash in the repo (`legacy_digest.json`, the `test_groups` pin, the tripwire baseline, the stored run hashes) matches the AVX512 path. So a result computed on a runner without AVX512 differs from the committed ones, and a final run's digest would depend on which machine GitHub gives. Options: regenerate the pins on one agreed path and force it everywhere (`NPY_DISABLE_CPU_FEATURES` in the workflow, the author's machine and `run.py`); compare with a tolerance instead of a hash; or run on a larger runner with a fixed CPU (paid). A pin cannot force AVX512 on a machine that lacks it. I changed no model or fixture file.
  2. `accept.sh` step 1 (`python -I -m pytest tests/model/model_v3 ...`) fails at collection (`No module named 'tests'`, `test_pension_lien.py`), so the whole script cannot pass as written; the accept job avoids steps 1 and 2.
  3. GitHub minutes: the repository is public, so hosted runners are free; the cost of one `accept` plus `converge` run is zero minutes billed, about 6 hours of runner time.
  4. Step 5 on a real `quick` file is not known to pass yet (057c notes say it failed on O8 nulls); the first accept run will show it.
- Instruction friction: the brief assumes `gh workflow run --ref` works for a new workflow on a branch; it does not (404). Not yet in the friction log.
- Verification: fast commands local: all suites, 408 model tests, agent docs, tripwire PASS; YAML lint passes; on GitHub as above.
- Commit / branch: branch `brief/168-github-actions-long-runs`; draft PR 3 (do not merge).
<!-- progress:end -->

## Change report
(The agent fills this in, per `project/agents/change-report.md`.)
