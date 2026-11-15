# Brief suggestions

Any agent appends here when it finds a problem that needs its own brief and is outside its current brief. Do not fix it. The guru reads this file, writes briefs for the worth-doing entries, and marks each `briefed NNN` or `dropped (reason)`. Only the guru changes an entry's status.

Entry format, newest at the bottom:
```
### <short title>
- Found by: <role / brief>, <date>
- Where: <files or area>
- Problem: <what is wrong, with a number or an error message>
- Suggested lane: g | w | c | r | s
- Status: open
```

### `wdt_analytics` does not import
- Found by: guru review of 006c, 2026-11-15
- Where: `model_v1/wdt_analytics.py` (was `model/`)
- Problem: `import rates_core` fails with ModuleNotFoundError; the module is now `rates_core1.py`. Present before 006c (baseline 16b06df has only `rates_core1.py`). Legacy; may be moot after the audit 001c.
- Suggested lane: c
- Status: open

### Revenue calculator fetches a file that no longer exists
- Found by: brief 010s, 2026-11-15
- Where: `site/tools/revenue_calc.html`, `site/_quarto.yml` (resources)
- Problem: both name `model/rates_model.py` (now `rates_core1.py`, and not published), so the calculator probably fails. Needs the author's decision (fix, replace or remove); architecture doc Issue 16.
- Suggested lane: s
- Status: open

### Hardcoded Zenodo sandbox token
- Found by: brief 004s, 2026-11-15
- Where: `pipeline/zenodo_upload.py`; git history
- Problem: a sandbox token is in the source (Issue 7). The author revokes it; then read it from an environment variable.
- Suggested lane: s
- Status: open

### Site build leaves tracked files modified
- Found by: brief 003s, 2026-11-15
- Where: `registry/contents.yml`, `site/pages/glossary.md`, `registry/references.json`
- Problem: the build rewrites them (561 + 244 changed lines in the first two) so it is not `git status` clean. Needs the author's decision on whether they stay tracked.
- Suggested lane: s
- Status: open
