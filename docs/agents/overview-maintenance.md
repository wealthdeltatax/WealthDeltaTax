# Maintaining OVERVIEW.md and STATUS.md

Only the guru edits these. Other roles report changes in the change report and flag drift.

## When to update the overview
When something it describes changes: files or modules added, moved or renamed, behaviour or defaults, commands, status of briefs, findings. Pure refactors that change nothing visible need nothing.

## How
1. Collect what changed from the change report, the brief's notes or the diff. If thin, read the files; do not write from assumption.
2. Edit the affected section in place. It is a map of what exists now, not a history; history lives in `docs/decisions.md`.
3. Keep it under about 15 KB. Prefer names over prose.
4. Move resolved items out of the findings section; add new findings with numbers and where they came from.
5. Commit with a `docs:` message straight to `main`.

## STATUS.md
Agents and what each is doing now and next, waiting on the author, recently done, open findings. Update when the author says an agent started or finished something, and after each merge. Keep under 5 KB.

## Drift check
If the author mentions changes made outside the loop, or the files contradict the overview, compare the directory map with the file listing and spot-check two or three claims. Fix and say so in the commit message.
