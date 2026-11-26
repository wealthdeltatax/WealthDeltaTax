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
- **Done:** claimed 2026-11-26; stage A written: `.github/workflows/model-checks.yml` with the `fast` job and the four manual inputs; the fast commands pass locally (all suites, 408 model tests, agent docs, tripwire).
- **Next:** push the branch and start `fast` by hand (`gh api` dispatch); then stage B.
- **Decisions:** pytest runs without `-I` (a test imports `tests.model...`, which fails under `-I`: `accept.sh` step 1 breaks the same way); `check_gate.py --all` is a report-only step (exit 1 by design while every gate is closed); pins are inline in the workflow (no requirements file exists).
- **Gotchas:** the tripwire moved to `project/restructure/`; GraphQL is blocked in this session, REST works.
- **Resume:** `git checkout brief/168-github-actions-long-runs`.
- **Not run:** everything on GitHub.
<!-- progress:end -->

## Change report
(The agent fills this in, per `project/agents/change-report.md`.)
