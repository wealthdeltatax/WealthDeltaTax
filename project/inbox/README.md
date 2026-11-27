# Inbox: notes between the guru and the OpenAI agent

The OpenAI agent can read the repository and push new markdown files to the branch `inbox/openai`, nothing else. This folder is how the guru and that agent talk. Rules for the agent: `project/agents/agent-openai.md`.

| Folder | Written by | Lives on | What |
|---|---|---|---|
| `from-openai/` | the OpenAI agent | branch `inbox/openai`; the guru copies a note onto main when it is worth keeping | notes: web research, repo answers, hypotheses, bug suggestions |
| `to-openai/` | the guru | `main` | replies, messages, questions, the context for the next session |
| `index.md` | the guru | `main` | one row per note: id, type, status, outcome |

## The guru's routine (each time the agent has pushed)
1. `git fetch`, list new files: `git diff --name-status main...origin/inbox/openai -- project/inbox/from-openai/`.
2. Read each note. Check the repo quotes against the named commit and spot-check two sources. A note is unverified until then.
3. Decide the outcome and write it in `index.md`: `promoted` (copy to `research/notes/` or fold into a brief; the copy keeps the note id and source list), `recorded` (a line in `decisions.md`), `answered` (a file in `to-openai/` with `in-reply-to`), or `archived`. Copy the note onto main with `git checkout origin/inbox/openai -- <path>` so main holds every note that has an outcome.
4. Write the next message or brief in `to-openai/` or `project/briefs/open/` (`Agent: openai`).
5. Never merge the branch itself; copy files. Delete nothing the agent wrote.

## Messages to the agent
`to-openai/YYYYMMDD-NN-slug.md`: header `to: openai`, `in-reply-to:` (a note id or none), `status: open` or `closed`, then the message. A brief for the agent is a normal brief with `Agent: openai`; its deliverable is a note in `from-openai/`.
