# OpenAI agent: do this every time you start

You read the repository (`main`) and push new markdown files to the branch `inbox/openai`. Nothing else. Full rules: `project/agents/agent-openai.md`.

1. **Get the latest.** Read `main` as it is now. Note the short commit sha: it goes in every note's `repo-commit`.
2. **Check your branch.** `inbox/openai` exists; if not, create it from `main`. If `main` has moved a lot, say so in your notes (you read `main`, you write to your branch).
3. **Read what changed for you.**
   - `project/inbox/index.md`: what happened to each of your earlier notes. Do not repeat a question that is answered.
   - `project/inbox/to-openai/`: new messages and replies, newest first. Answer open ones first.
4. **Find your task.**
   - A brief for you: `project/briefs/open/` files whose header says `Agent: openai`, status `ready` or `underway`. Take the first by number unless told otherwise; an explicit task given in the current chat comes before any ready brief. Follow its Read, Questions, Output and Acceptance sections.
   - Otherwise do what the author asked in this chat.
5. **Know the current state.** `project/STATUS.md` (what is happening now). Skim `project/OVERVIEW.md` only if the task needs it.
6. **Write notes.**
   - New files only, in `project/inbox/from-openai/`, named `OA-YYYYMMDD-NN-short-slug.md` (NN counts that day's notes from `01`). Never edit or overwrite an existing file; correct with a new note using `supersedes:`.
   - Use the header in the guide. Put the answer first, then evidence, then what you could not check, then the suggested next step.
7. **Before you push, check:**
   - Every figure has a source (URL, date read, page or table) and a flag (`reported`, `derived`, `estimated`).
   - Repo claims quote the text with path and commit; numbers are copied, not paraphrased.
   - Nothing says "tested", "ran" or "fixed". `verified` is `unverified` or `read-only`.
   - Ranges and options, not one central forecast and not a recommendation.
   - No brief numbers in file names; nothing pushed to `main`.
8. **Push and report.** Push to `inbox/openai`. Tell the author the branch and the file names, in one short message. The guru reads, checks, and replies in `project/inbox/to-openai/`.

**When unsure:** say what you could not check, in the note. Do not fill gaps from memory. Ask the author in chat if a question is unclear.
