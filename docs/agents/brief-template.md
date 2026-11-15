# Brief template

Save to `docs/briefs/NNN-short-slug.md`. Keep a brief as short as the change allows.

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
Number: the next unused three digits across `docs/briefs/` and `docs/archive/briefs/`. If the repo keeps a generated brief index, regenerate it after changing Status or Depends on.
