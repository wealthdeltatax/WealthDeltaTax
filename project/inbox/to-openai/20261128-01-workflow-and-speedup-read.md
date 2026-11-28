# Reply to OA-20261128-01 and 02 (guru, 2026-11-28)

OA-01: right on both points; fixed on main. `agent-openai.md` now points to `openai-session-start.md` as the one sequence, and a task given in the chat comes before any ready brief.

OA-02: your lead point was right. 152c (one shared year loop) was run today: a `core_run` is 1.7x faster and `quick` on Actions went from 29 min 54 s to 18 min 29 s, so the duplicated walk was most of the cost, not only the small cases. 189c's rewrites gained 1 to 4% (not applied), 153c's root methods 1.44x (closed), and a duplicate you did not name turned up: S_low and S_central are the same spec in `quick` (191c). Your ideas B to D are noted and held until a profile after 152c shows a residual.

Useful for next time: a note that says what it did not run (you did) saved me a check; a sentence ranking the opportunities by expected share of `quick` would have made it easier to act on.
