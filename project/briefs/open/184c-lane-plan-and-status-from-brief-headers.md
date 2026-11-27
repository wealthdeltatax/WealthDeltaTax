# 184: Build the lane plan and the STATUS agent table from the brief headers

- **Status:** ready
- **Agent:** 3
- **Needs:** none
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-27
- **Depends on:** none (touches `project/tools/`, the open briefs' header lines, `project/lane-plan.html` and `project/STATUS.md`, none of which the speed-up chain edits)
- **Read:** `project/agents/brief-template.md`, `project/lane-plan.html` (the `LANES` and `B` arrays and the `pack()` function; start sessions are already computed there), `project/STATUS.md` (the agent table), `project/tools/check_agent_docs.py`, `tests/project/tools/` (how the tools are tested)

## Goal
Nobody edits the lane plan or the STATUS agent table by hand. They are generated from the header lines of the open briefs, so they cannot drift from the briefs. A brief is the one place that says who is doing it, what state it is in, and what it waits for.

## Decisions (author, 2026-11-27)
The immediate brief of every agent is always in session 1 and the dependent briefs line up after it (the page already computes this from status and needs; fd35d3b2). The remaining hand-maintenance goes away.

## Design (guru proposal, labelled for challenge)
1. **Header lines.** Each brief in `project/briefs/open/` carries, besides the existing lines, three machine-readable ones:
   - `- **Agent:** 3` (an agent number 2 to 6, or `author` for work that needs the author, or `none` when unassigned).
   - `- **Needs:** 151c, 154c, ~176c` (ids of open briefs; a leading `~` means a soft file-order dependency, as `soft` in the page today; `none` when empty).
   - `- **Length:** 1` (sessions; default 1).
   The `Status:` line must start with one of these words, the rest is free text: `underway`, `review` (branch pushed, waiting for merge), `ready`, `author` (needs the author's decision), `hold` (waits for its needs; `draft` and `parked` are read as `hold`). An unknown first word is an error, not a guess.
2. **Brief with stages that run apart** (the case of 183a and 183c). A brief may add more rows with lines of the form `- **Row:** 183a | agent 4 | ready | needs none | length 1 | Split run, stage A (new files only)`. These become extra plan rows with that id; the brief's own row is the one built from the lines in item 1. Keep this to what the plan needs today.
3. **The script** `project/tools/build_lane_plan.py` reads the open briefs and writes (a) the `B` array of `project/lane-plan.html` between `// plan:start` and `// plan:end` markers, (b) the lane notes (`LANES[].note`: the agent's current brief, then `then` the rest of its lane in the order the page uses), (c) the agent table of `project/STATUS.md` between `<!-- agents:start -->` and `<!-- agents:end -->`. The title is the brief's H1 without the number, the tooltip text is the first sentence of its `## Goal`, the files text is the `Touches` line cut to 60 characters. Rows for briefs in `done/` do not exist, so retiring a brief (moving it to `done/`) removes it from the plan with no other edit. Agent 1 (guru prime) and the `author` lane keep their fixed rows (text from a small `project/lane-plan-lanes.json`, which the author or guru edits rarely).
4. **Modes:** `build_lane_plan.py` rewrites the generated parts; `--check` exits 1 and prints a diff if they differ from what the headers say; both exit 2 on a malformed header, naming the file and line.
5. **Checks wired in:** `check_agent_docs.py` calls the same parser and fails on a malformed or missing header line, an unknown id in `Needs`, a cycle, or an agent number outside 2 to 6 and `author` and `none`; `.github/workflows/model-checks.yml` `fast` job runs `build_lane_plan.py --check` so a stale plan is a red check on main. Do not change any other job.
6. **Migration:** write the three header lines into every open brief (14 today) from the current plan, with no change to meaning; `Status:` first words normalised. Run the script and show that the generated `B` rows, lane notes and agent table equal the hand-kept ones today except for text the script now derives (list each difference). Update `project/agents/brief-template.md`, `project/agents/agent-guru.md` (the "keep the lane plan" step becomes "edit the brief header, run the script") and `project/START_HERE.md` if it describes the manual way.

## Blocks (one push each; `project/agents/agent-code.md`)
- **Block 0:** progress block pushed.
- **Block 1:** the parser and the script, with `tests/project/tools/test_build_lane_plan.py`: header parsing (all status words, `~` soft needs, `Row:` lines, malformed lines), cycle and unknown-id errors, idempotence (run twice, identical bytes), `--check` exit codes, retired brief disappears. Checkpoint: the tests pass; `python -I project/tools/build_lane_plan.py --check` runs on a copy of today's tree and reports the migration differences.
- **Block 2:** migrate the open briefs' headers, generate, wire `check_agent_docs.py` and the `fast` check, update the template and guru rules. Checkpoint: `node /tmp/lp.js` style load of the page (headless, only the external-font error allowed), the bar positions equal today's (session 1 for the first brief of each agent), `check_agent_docs.py` exit 0, the project tools suite passes.
- **Block 3:** change report; push; stop.

## Touches
`project/tools/build_lane_plan.py` (new), `project/tools/check_agent_docs.py`, `tests/project/tools/test_build_lane_plan.py` (new), `project/lane-plan-lanes.json` (new), `project/lane-plan.html` (markers only, plus the generated array), `project/STATUS.md` (markers around the agent table), the header lines of the open briefs, `project/agents/brief-template.md`, `project/agents/agent-guru.md`, `project/START_HERE.md`, `.github/workflows/model-checks.yml` (one added step in `fast`). No model code, no brief text beyond the header lines.

## Acceptance criteria
- Editing only a brief's `Agent`, `Status`, `Needs` or `Length` line and running the script changes the page and the table, and nothing else.
- `--check` is green on main and red after a header edit without a rebuild.
- Moving a brief to `done/` removes its row; adding a brief adds one.
- The first brief of each agent is at session 1 whenever its needs are met; the page's other behaviour is unchanged.
- The migration difference list is in the change report.

## Out of scope
Changing how the page draws or packs (`pack()` stays), the finished-brief archive, the account skills (the guru updates those after this merges), any brief's content.

## Open questions
If a status word in a current brief cannot be mapped (say, a free-text status like "done in part"), list it and stop for the author's call. Do not guess.

## Implementation notes
<!-- progress:start -->
- **Done:** nothing yet.
- **Next:** block 0.
<!-- progress:end -->

## Change report
(The agent fills this in, per `project/agents/change-report.md`.)
