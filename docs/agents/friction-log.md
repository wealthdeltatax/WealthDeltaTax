# Friction log

Any agent appends here when the **instructions, workflow or tooling** failed it: a rule that was missing, stale or contradictory, a command that does not work as written, an ambiguity that forced a guess. Log only what cost time or caused a wrong action. Not here: a flaw in the brief (change report), work for a new brief (`docs/brief-suggestions.md`), preferences.

Append at the bottom, at most four lines per entry, when it happens (commit it with your next checkpoint). Never edit or delete another entry; only the guru sets `Status`. The file merges with git's union driver (`.gitattributes`), so concurrent appends do not conflict.

Entry format:
```
### <date> · <brief or task> · <role>
- Instruction: <file and section, or "none: missing">
- Happened: <what went wrong, with the first error line>
- Cost: <time lost, rework, wrong action, blocked>
- Suggest: <optional one line>
```
The guru adds `- Status: open | fixed <commit> | dropped (reason)` when triaging. One entry is noted; two on the same instruction mean the guide is edited. Fixed and dropped entries move to `docs/archive/friction-log-archive.md`; keep this file under about 100 lines.

## Entries

### 2026-11-20 · 084c · code
- Instruction: brief 084c Touches and architecture.md 5.1 (R4 layers): a new runner module needs a row in the LAYER table of `tests/model_v3/conftest.py`
- Happened: the brief adds `model_v3/runner/groups.py` and four `out_*.py` files that `runner.py` imports; R4 fails any edge with a module not in LAYER, and conftest.py was not in Touches
- Cost: stopped to ask; the author said to add the rows (out_* 3.5, groups 3.7), so conftest.py changed outside Touches
- Suggest: briefs that add a module name the LAYER row, and 5.1 lists the new modules
- Status: open (one entry; the guru wrote 5.1 for the group files on 2026-11-20 and adds the LAYER row to any brief that adds a module)
### 2026-11-20 · brief 083c · code
- Instruction: brief 083c "Read:" and Design (how to build the runner context); `runner.context` needs the tier 1 list and `payer_taxes`.
- Happened: neither is named in the brief; `payer_taxes` has no home in `levers.json` (055c gotcha 6), so I copied the fixture from `tests/model_v3/test_runner.py`.
- Cost: a few minutes reading the tests to find the call.
- Suggest: a brief for a one-off script should name the test fixture that builds the context (084c has since moved `payer_taxes` into `levers.json`).
- Status: open (one entry)
### 2026-11-20 · brief 086c · code
- Instruction: brief 086c Design: fill `out_burden.per_path(raw, again)` and read the inputs "from the register and pack as 055c does (`ctx`, `theta`)".
- Happened: `per_path` gets `Raw` and `again` only; `Raw` has no `pack`, `reg`, `ctx` or `theta`. O5, O6, O8, OH1b, OH1b2, OH1c, DH1c need them (m5, m6, m8, m3_today, m11, m12, dh1c). 084c's tests also pin every group's `IDS == ()` and the empty-group digest, so any filled group fails `test_groups.py`.
- Cost: built five of twelve ids, stopped on seven (the brief's own stop rule).
- Suggest: the guru widens the group interface (`per_path(raw, again, ctx, theta)` or `Raw` carrying `ctx` and `theta`, an edit to `runner.py`) and loosens the two 084c tests to "IDS in the manifest".
- Status: open (one entry)
