# Brief template

Save to `docs/briefs/NNNx-short-slug.md`. Keep a brief as short as the change allows.

**Lane letter `x`** (after the three-digit number) says which role runs the brief, so the author knows which skill to open:

| Letter | Role / skill |
|---|---|
| `g` | guru (`wdt-guru`): docs, status, briefs, scaffold |
| `w` | writing (`wdt-write`): papers |
| `c` | code (`wdt-code`): model, pipeline code, tests |
| `r` | research (`wdt-research`): references, literature |
| `s` | site (`wdt-web`): Quarto site, build, deploy |

Example: `001c-model-audit.md`. The heading inside the file stays `# 001: Title` (no letter).

```markdown
# NNN: <Title>

- **Status:** draft | ready | built | superseded | parked
- **Author/date:** <author> with the guru, <YYYY-MM-DD>
- **Depends on:** <brief numbers, or none>
- **Read:** <exact files and overview sections the agent needs; nothing else need be opened>

## Goal
What the user gets, and why. One or two sentences.

## Decisions (author, <date>)
The author's stated rules, in their words where it matters.

## Design
Behaviour written so someone who was not in the conversation can build it.

## Touches
Files and areas affected.

## Stages
One session finishes one stage; a stage is the unit of checkpoint. `- <id>: <what>. Checkpoint: <what is pushed>; check: <cheapest check>`. Split a brief with more than three deliverables or about 15 files. A small brief may omit this.

## Acceptance criteria
Measurable: a test, a bound, a manual check. For experiments, an adoption bar written before measuring.

## Checks to run
The checks that prove this brief and no more; say why any usual check is skipped.

## Out of scope

## Open questions
The implementer asks rather than guesses on these.

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
```
Number: the next unused three digits across `docs/briefs/` and `docs/archive/briefs/` (ignore the letter when checking what is unused). If the repo keeps a generated brief index, regenerate it after changing Status or Depends on.
