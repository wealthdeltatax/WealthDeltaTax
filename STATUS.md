# Status board

Maintained by the guru. Last updated 2026-11-15 (night). Plan view: `docs/lane-plan.html`.

## Where the project is
Papers are being rewritten by the author. Housekeeping comes first (remaining: 003s, 004s, 010s; 005g, 006c and 008g are merged); then model v1 and v2 are audited (001c) before any model v3 design (011g). Brief files are named `NNNx-slug.md`; the letter is the skill to open (g guru, w writing, c code, r research, s site/web).

## Agents
| Agent | Now | Next |
|---|---|---|
| Agent 1 | Free | none planned |
| Agent 2 (web) | Free | 003s, then 010s |
| Agent 3 (guru) | Reviewed and retired 006c | 011g, after the audit 001c; compiles `docs/brief-suggestions.md` into briefs |
| Agent 4 (web) | Free | 004s |
| Agent 5 | Free | the audit 001c (code) after 003s, 004s and 010s merge |

## Waiting on the author
- Approve the audit brief 001c (scope, one stage per session, writes only under `docs/model-audit/`).
- Two small choices with defaults in the briefs: letter `s` for the web role; keep the published URL `/model/` when the folder becomes `model_v1` (010s).
- Remove the old uploaded `wdt-*` skills from the claude.ai account (005g follow-up; cannot be done from the repo).

## Recently done
- 2026-11-15: brief 006c (model folder cleanup) reviewed and retired: 226 tracked files deleted (709 to 483), `model_new_2` 192 to 154 MB, pack unchanged at 105.83 MiB, core imports resolve. New `docs/brief-suggestions.md`: agents log problems that need a brief there instead of fixing them out of scope.
- 2026-11-15: briefs 005g (`Tools/` holds the five role `.skill` files and `repo-scaffold.skill`) and 008g (docs and data renames, owners in `OVERVIEW.md`) reviewed against their criteria, decisions entries added, briefs retired to `docs/archive/briefs/`, with 002g.
- 2026-11-15: auto-merge rule added to `AGENTS.md` (agents merge their own finished briefs; site changes build locally first because the Action runs only on `main`); branch `brief/002-repo-triage` merged to `main`.
- 2026-11-15: scaffold audit and agent guides; repo triage (002g) with the final brief order; author's decisions applied (untrack `source/.obsidian/`, delete old `Tools/` skill files and `web_search.json`, rename and keep docs, keep data dumps, audit models before v3); lane-letter rule added to the guru guide and brief template; `docs/lane-plan.html` rebuilt for these briefs.

## Open findings
See `OVERVIEW.md` section 6. Priority list carried over from `docs/todo.md`: citation button, CLOSE updates, PDF title page, WFR refactor, WP Appendix B forward links, internal bibliography to Zenodo v2.
