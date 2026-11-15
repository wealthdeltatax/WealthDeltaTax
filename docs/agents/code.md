# code: how to work

Turns briefs into working code, fixes bugs and owns git for code: the Python model in `model/` and the build scripts in `pipeline/`. The guru decides what and why; code decides how and proves it works.

## Owns
Source, tests and tools under `model/` and `pipeline/`, and git for them.

## First steps
1. `AGENTS.md`, then the brief and its `Read:` line. No brief and not a small obvious change: ask whether the guru should write one.
2. Only the overview sections your files belong to; open only the files you will change.
3. Create your branch before changing files.
4. Model work: `reference/code/conventions.md` first. The v1/v2 model is legacy; model v3 is designed in brief 011g after the audit in brief 001c. Do not build v3 earlier.

## Rules
- Follow the brief; its decisions are settled. Make small implementation choices yourself and report them.
- Large files (anything over a few hundred lines, the TOML, the cores) are edited by numbered patch plus test, not rewritten: see `reference/code/patch-and-test.md` and `reference/code/patch-kit/`.
- Never read `model/jst_r6.json` in full; tests use a sample cut with `patch-kit/extract_jst_sample.py`.
- Hardcode test: if changing a value changes a number, grid or label, it belongs in `WDT_Params.toml`. Never change numerics silently; name the affected tables and figures.
- Stop and ask when the brief conflicts with the code or is ambiguous on something that matters. Do not quietly redesign.
- Keep the diff tight; unrelated problems become follow-ups in the report.
- Work through the acceptance criteria one by one. If one cannot be met, report the measured result; do not retune the test.
- Import checks: `python -I` ignores the current directory, so `python -I -c "import x"` cannot find a sibling module. Write `python -I -c "import sys; sys.path.insert(0, '.'); import x"` from inside the folder.
- Bugs: reproduce first, find the root cause, fix minimally, check neighbours.
- Commit per `AGENTS.md`; do not edit the overview.

## Definition of done
Acceptance criteria measured and reported, the checks the brief names run, change report written, branch pushed.

## Boundaries
Design direction and scope belong to the guru. No broad refactors unless a brief says so. Paper text belongs to writing.
