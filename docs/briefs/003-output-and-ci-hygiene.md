# 003: Crosslink output files, gitignore and CI debug step

- **Status:** draft
- **Author/date:** K. Ogata with the guru, 2026-11-15
- **Depends on:** 002
- **Read:** `check.txt`, `pipeline/check2.txt`, `.gitignore`, `.github/workflows/deploy.yml`, `source/.obsidian/`

## Goal
Stop tracking generated reports and editor state, and remove the debug step from the deploy workflow.

## Decisions (author, 2026-11-15)
- Audit items from group B and C, not yet approved item by item; confirm each diff before applying.

## Design
- `check.txt` (110 KB, repo root) and `pipeline/check2.txt` (90 KB) are old output of `wdt_crosslinks.py check`. Delete both (git history keeps them) or gitignore future output; the script stays.
- `.gitignore`: add `source/.obsidian/workspace.json` and untrack it; decide whether the rest of `source/.obsidian/` stays.
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
