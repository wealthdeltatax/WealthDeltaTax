# Status board

Maintained by the guru. Last updated 2026-11-15 (night). Plan view: `docs/lane-plan.html`.

## Where the project is
Papers are being rewritten by the author. Housekeeping comes first (all merged; 004s awaits its retirement); the audit 001c is now running; then model v1 and v2 are audited (001c) before any model v3 design (011g). Brief files are named `NNNx-slug.md`; the letter is the skill to open (g guru, w writing, c code, r research, s site/web).

## Agents
| Agent | Now | Next |
|---|---|---|
| Agent 1 | Free | none planned |
| Agent 2 (web) | Free | none planned |
| Agent 3 (guru) | Reviewed and retired 003s, 006c, 010s | 011g after the audit; compiles `docs/brief-suggestions.md` into briefs |
| Agent 4 | Audit 001c, stage A | stages B to D, one per session |
| Agent 5 | Free | none planned |

## Waiting on the author
- Decide whether `registry/contents.yml`, `site/pages/glossary.md` and `registry/references.json` stay tracked (the build rewrites them; 003s).
- Revoke and rotate the Zenodo sandbox token hardcoded in `pipeline/zenodo_upload.py` (architecture doc Issue 7); check git history too.
- Decide the revenue calculator: it fetches `rates_model.py`, which is gone (Issue 16).
- Small choice with a default: letter `s` for the web role.
- Remove the old uploaded `wdt-*` skills from the claude.ai account (005g follow-up; cannot be done from the repo).

## Recently done
- 2026-11-15: briefs 003s (untracked reports and editor state, CI debug step removed) and 010s (`model_v1`, `model_v2`; URL `/model/` kept) reviewed and retired; `OVERVIEW.md` drift fixed. Both merged with the Action green on later tips. The author started the audit 001c with Agent 4, which counts as its approval.
- 2026-11-15: brief 006c (model folder cleanup) reviewed and retired: 226 tracked files deleted (709 to 483), `model_new_2` 192 to 154 MB, pack unchanged at 105.83 MiB, core imports resolve. New `docs/brief-suggestions.md`: agents log problems that need a brief there instead of fixing them out of scope.
- 2026-11-15: briefs 005g (`Tools/` holds the five role `.skill` files and `repo-scaffold.skill`) and 008g (docs and data renames, owners in `OVERVIEW.md`) reviewed against their criteria, decisions entries added, briefs retired to `docs/archive/briefs/`, with 002g.
- 2026-11-15: auto-merge rule added to `AGENTS.md` (agents merge their own finished briefs; site changes build locally first because the Action runs only on `main`); branch `brief/002-repo-triage` merged to `main`.
- 2026-11-15: scaffold audit and agent guides; repo triage (002g) with the final brief order; author's decisions applied (untrack `source/.obsidian/`, delete old `Tools/` skill files and `web_search.json`, rename and keep docs, keep data dumps, audit models before v3); lane-letter rule added to the guru guide and brief template; `docs/lane-plan.html` rebuilt for these briefs.

## Open findings
See `OVERVIEW.md` section 6. Priority list carried over from `docs/todo.md`: citation button, CLOSE updates, PDF title page, WFR refactor, WP Appendix B forward links, internal bibliography to Zenodo v2.
