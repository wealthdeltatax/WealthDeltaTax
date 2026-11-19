# Handover: never lose work when a session ends

A session can end at any moment. Work only on an agent's disk is lost and the next agent re-reads everything. So: push after every stage, keep one short progress block, start the next session from it.

## Rules
- Checkpoint after every stage: commit as `wip(NNN): stage N done` and push the branch. No checks needed to push.
- Progress block in the brief's Implementation notes (or the task notes), at most 15 lines: **Done**, **Next**, **Decisions** (what the next agent must not redo), **Gotchas**, **Resume** (exact commands), **Not run**, **State** (pushed commit).
- One small edit per stage; never paste logs, only the first error line and the command.

- A stop-hook warning of unpushed commits is stale when `git ls-remote origin <branch>` equals `git rev-parse HEAD`; check before pushing again.

## Prompts (the author pastes one)
**Wrap up:**
```
Stop work now. Commit everything as wip, push the branch, fill in the progress block, then stop. Do not run checks.
```
**Resume:**
```
Read the brief and its progress block, `git log origin/main..HEAD`, and `git diff --stat origin/main`. Continue from Next. Do not re-explore. Run the Resume commands first.
```
