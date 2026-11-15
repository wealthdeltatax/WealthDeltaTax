# 003: Crosslink output files, gitignore and CI debug step

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002 (merged). Order: 1st of the cleanup set; independent of 004, 006, 008, so they may run in parallel.
- **Read:** `check.txt`, `pipeline/check2.txt`, `.gitignore`, `.github/workflows/deploy.yml`, `source/.obsidian/`

## Goal
Stop tracking generated reports and editor state, and remove the debug step from the deploy workflow.

## Decisions (author, 2026-11-15)
- Audit items from group B and C, not yet approved item by item; confirm each diff before applying.
- Untrack the editor state (author, 2026-11-15: "untrack"); read as the whole of `source/.obsidian/`.

## Design
- `check.txt` (110 KB, repo root) and `pipeline/check2.txt` (90 KB) are old output of `wdt_crosslinks.py check`. Delete both (git history keeps them) or gitignore future output; the script stays.
- Triage found nothing reads `check.txt` or `check2.txt` (no script, workflow or guide names them), so deletion is safe. `docs/agents/reference/writing/style-guide.md` tells the writer to run the check fresh.
- `.gitignore`: add `source/.obsidian/` and untrack all five files in it (`git rm -r --cached source/.obsidian`); the author's local Obsidian config stays on disk. Also add `check*.txt` and `pipeline/check*.txt` so future output is not committed.
- `deploy.yml`: remove the final "Inspect build output" step, which only lists WFR figures. Confirm the WFR figures are produced first.
- `main` deploys on push, so do this on a branch and check that the Action stays green.

## Touches
`check.txt`, `pipeline/check2.txt`, `.gitignore`, `.github/workflows/deploy.yml`, `source/.obsidian/`.

## Acceptance criteria
- The deploy workflow still builds and deploys; no tracked generated report remains at the repo root.

## Checks to run
Push the branch and watch the GitHub Action; `git status` clean after a local `pipeline/build.bat` run.

## Out of scope
Changing any build step other than the debug step.

## Open questions
- None. If the author meant only `workspace.json`, restore the other four files.

## Open questions
- Delete the check files or move them somewhere? Default: delete.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
