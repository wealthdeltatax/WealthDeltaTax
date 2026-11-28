# Inbox index

One row per note from the OpenAI agent. Written by the guru. Outcomes: `promoted`, `recorded`, `answered`, `archived`; `new` until read.

| id | type | question | outcome | where it went |
|---|---|---|---|---|
| OA-20261127-01 | web-research | Fund-size caps and release of excess | promoted | `research/notes/OA-20261127-01-fund-caps-and-excess-release.md`; spot-checked FDIC DRR (2%, minimum 1.35%, dividend threshold 1.5%, no upper limit) and Alberta (C$32.0bn at 31 March 2026, plan C$250bn by 2050, income retained unless Treasury Board authorises) against the pages |
| OA-20261127-02 | web-research | Reserves sized against outflows | promoted | `research/notes/OA-20261127-02-reserve-sizing-and-outflow-cover.md`; FDIC 2020 ratio 1.30% and the restoration plan confirmed |
| OA-20261127-03 | web-research | Drawdown rules; protection and failure | promoted | `research/notes/OA-20261127-03-drawdown-smoothing-and-protection.md`; sources not spot-checked beyond those shared with 01 |
| OA-20261127-04 | discussion | Change report for 185r | archived | stays in `project/inbox/from-openai/` |
| OA-20261128-01 | discussion | Is the OpenAI workflow coherent? | promoted | stays in `project/inbox/from-openai/`; checked against `agent-openai.md` and `openai-session-start.md` (two read orders, confirmed); fixed: `agent-openai.md` points to the session-start card, and the card says a chat task comes before a ready brief |
| OA-20261128-02 | performance-review | Further speed-up opportunities | recorded | `research/notes/OA-20261128-02-speedup-opportunities.md`; its lead point (share the household year loop, 152c) was measured the same day by Agent 5: 1.7x on `core_run`; ideas B (allocation overhead), C (chunk and worker balance) and D (shared derived masks) are held until 189c's stop note and 152c merge show a residual; no float32 or compiled rewrite, as already ruled |
