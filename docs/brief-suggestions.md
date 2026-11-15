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
