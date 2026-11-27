# Brief template

Save to `project/briefs/open/NNNx-short-slug.md`. Keep a brief as short as the change allows.

**Lane letter `x`** (after the three-digit number) says which role runs the brief, so the author knows which skill to open:

| Letter | Role / skill |
|---|---|
| `g` | guru (`wdt-guru`): docs, status, briefs, scaffold |
| `w` | writing (`wdt-write`): papers |
| `c` | code (`wdt-code`): model, pipeline code, tests |
| `r` | research (`wdt-research`): references, literature |
| `s` | site (`wdt-web`): Quarto site, build, deploy |

The four lines above are read by `project/tools/build_lane_plan.py`, which generates the lane plan and the agent table in `project/STATUS.md`; `check_agent_docs.py` fails on a bad one. A brief whose stages run apart may add `- **Row:** 183a | agent 4 | ready | needs none | length 1 | text` lines (one extra plan row each). After editing a header run `python -I project/tools/build_lane_plan.py`.

Example: `001c-model-audit.md`. The heading inside the file stays `# 001: Title` (no letter).

```markdown
# NNN: <Title>

- **Status:** underway | review | ready | author | hold  (first word; draft and parked read as hold; the rest is free text)
- **Agent:** 2 to 6, author, or none
- **Needs:** <ids of open briefs, ~ before a soft file-order need, e.g. 151c, ~176c; none>
- **Length:** <sessions; default 1>
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

## Session budget (research and data briefs)
A session has finite tokens; the brief's length is not the risk, the work is. Cap a brief at one source group or about 15 register rows, and one reviewable note. Block 0 pushes the note skeleton (every section marked pending) before any source is opened; each later block fills one section, updates the progress block and pushes in the same commit. After three blocks, write the note from what exists, push and stop, listing the rest under Next. Name any earlier outputs and branches the agent must reuse rather than re-derive.

## Stages
One session finishes one stage; a stage is the unit of checkpoint. `- <id>: <what>. Checkpoint: <what is pushed>; check: <cheapest check>`. Stages are for sequential steps only; split parallel work into separate briefs (see Splitting). A small brief may omit this.

## Inputs and early check (build stages)
List each register row, pack field or file the stage reads and where it exists; a missing one needs its own brief first. If the stage feeds a target number, name the cheapest check against it and say to stop and report the numbers if it misses.

## Acceptance criteria
Measurable: a test, a bound, a manual check. For experiments, an adoption bar written before measuring.

## Checks to run
The checks that prove this brief and no more; say why any usual check is skipped. A brief that names held workbooks or a repo script says so here: the run needs a local checkout and a shell (research sessions sometimes have neither; `research.md`). An import check run with `python -I` must add the folder to the path (`sys.path.insert(0, '.')`); see `code.md`.

## Out of scope

## Open questions
The implementer asks rather than guesses on these.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:** (exact branch name and `git fetch origin <branch>:refs/remotes/origin/<branch>` line, last block pushed, first action; a clone tracks main only)
- **Not run:**
- **State:**
<!-- progress:end -->
```
## Splitting (do this first)
Before writing a brief, ask which parts can run at the same time, and split them into separate briefs. Several small briefs on different agents beat one large brief run in sequence.
- **Parallel parts** touch disjoint files and do not need each other's output. Each becomes its own brief: own number, one lane letter, one session, a checkpoint that merges alone, and a `Touches` list that overlaps no sibling.
- **Shared inputs** (data format, names, interfaces, the gate) are fixed before the children start, in an earlier brief or in a short parent brief. Children never edit a shared file. The guru alone edits `project/STATUS.md`, `project/lane-plan.html` and `project/decisions.md`.
- **Sequential parts** stay as `Stages` in one brief, or as a `Depends on` chain when they need different lanes.
- **Size:** a child fits one session: about 5 files, or one paper group, or one module. If it does not, split again.
- **Parent brief:** only when children share a design or gate. It holds the goal, decisions and gate, links the children, and retires when they all have.
- **Lane plan:** list the siblings on different agent lanes at the same time, with the same `Depends on`.
- A brief that cannot be split should say why in one line under `Design`.

Number: the next unused three digits across `project/briefs/open/` and `project/briefs/done/` (ignore the letter when checking what is unused). If the repo keeps a generated brief index, regenerate it after changing Status or Depends on.
