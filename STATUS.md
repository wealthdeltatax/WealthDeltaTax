# Status board

Maintained by the guru. Last updated 2026-11-15 (evening).

## Where the project is
Papers are being rewritten by the author. The simulation model is to be rebuilt from scratch (third refactor) using lessons from the first two. The agent scaffold was added on branch `docs/scaffold-audit`.

## Agents
| Agent | Now | Next |
|---|---|---|
| guru | Brief 002 (triage) done on branch `brief/002-repo-triage`; briefs 003 to 009 written or revised | Merge 002; wait for the author's decisions below |
| code | Idle | Briefs 003 and 006 (ready, can run in parallel); brief 001 (model v3) when the lessons note exists; 009 after 001 |
| writing | Idle | Author-led paper rewrite |
| research | Idle | `references.bib` and `internal.json` updates after rewrites |
| web | Idle | Brief 004 (architecture doc), then the citation button fix from `docs/todo.md`; 003 touches `deploy.yml` |

## Waiting on the author
- Test the five new `.skill` files in `Tools/`; then brief 005 removes the old archives and the uploaded `wdt-*` skills.
- Approve the revised cleanup briefs (order in `docs/briefs/002-repo-triage.md`): 003, 004, 006 ready; 008 docs and naming and 009 legacy-model retirement are new drafts; 005 waits on your skill test; 007 is parked.
- Decisions listed at the end of brief 002: `.obsidian` scope (003), `Tools/web_search.json` and keeping both skill locations (005), v2 plans and folder renames (008), data dumps and when `model/` goes (009).
- Brief 001 needs your account of what `model_new_2` got wrong (the "lessons" note).

## Recently done
- 2026-11-15: scaffold audit, agent guides, skill stubs, superseded `SS` folders removed; scaffold merged to `main`; v2 model added as `model_new_2/`; open audit items written up as briefs 002 to 007; role stubs packaged as flat `.skill` files.

## Open findings
See `OVERVIEW.md` section 6. Priority list carried over from `docs/todo.md`: citation button, CLOSE updates, PDF title page, WFR refactor, WP Appendix B forward links, internal bibliography to Zenodo v2.
