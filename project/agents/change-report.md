# Change report (hand-off to the guru)

End every task with this report; the guru uses it to update `project/OVERVIEW.md`.
```
Change report
- Task: <brief number/title or request>
- Files changed: <list, one-line purpose each>
- What is different now: <for the user or developer>
- New or changed interfaces: <commands, settings, exports, or "none">
- Acceptance criteria: <each with its measured result; mark any not met or partly met, and why>
- Deviations from the brief: <or "none">
- Risks / follow-ups: <or "none">
- Instruction friction: <entries added to `project/agents/friction-log.md`, or "none"; write "none" only after asking whether any instruction, workflow or tool failed you>
- Verification: <checks run and results; anything not run>
- Overview sections likely needing an update: <or "none">
- Commit / branch: <hash, branch>
```
If the work came from a brief, paste the report into the brief's "Implementation notes" and commit it with the work. Keep the final message to the author short: what changed, which criteria are met or not, what needs their decision.

When a brief's branch has merged, say "brief NNN merged, ready to retire" in the report; the guru writes the decisions entry and archives the brief.
