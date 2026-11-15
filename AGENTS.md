# Notes for agents working on this repo

Read `START_HERE.md`, then the guide for your role in `docs/agents/`. This file holds only rules every role shares; role rules live in the role's own guide.

## Roles
- **guru**: design partner, owns docs, overview, status, briefs, scaffold health.
- **code**: model and pipeline code, tests, tools.
- **writing**: drafts, edits, formats and compresses the papers.
- **research**: references, bibliography, literature.
- **web**: Quarto site, build, deploy.
- **The author** (K. Ogata) decides open questions.

## Git
- `main` deploys the live site on every push. Never push to `main` except guru docs-only edits.
- One branch per task: `brief/NNN-slug` or `fix/<slug>`, from the latest `main`. Commit and push to the branch.
- Never force-push `main`. `git pull --rebase` before pushing.
- Commit message: `type(scope): imperative summary`; types `feat fix refactor docs chore perf`. Stage specific files; one logical change per commit.

## Generated files (never edit by hand)
`_build/`, `_site/`, `registry/anchors.yml`, `registry/crosslinks.json`, `model/OUTPUTS/`. Change the source and regenerate.

## Reading
- Router first, then your role guide, then only the files the task names. Do not open `docs/archive/` or `docs/model-lessons/`.
- `OVERVIEW.md` is a map and can be out of date; the files are the truth. Read by section.
- `source/` is canonical. Never rewrite a paper to make a check pass.

## Finishing
- End every task with the change report (`docs/agents/change-report.md`).
- A session can end at any time: checkpoint as `docs/agents/handover.md` says.
- If a result misses its target, say so with numbers. Do not change the check to make it pass.
- If the task conflicts with the repo or is ambiguous on something that matters, stop and ask with a proposed resolution.
- Only the guru edits `OVERVIEW.md` and `STATUS.md`; others report changes and flag drift.
