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
### 2026-11-20 · 085c · code
- Instruction: brief 085c Touches; `tests/model_v3/test_groups.py` (084c, 092c) asserts every group is empty: `all(m.cells({}) == m.per_path(None, None, None) == {} ...)`
- Happened: filling `out_revenue.py` made that assertion fail (`KeyError: 'M1e'`); test_groups.py is not in Touches
- Cost: edited it outside Touches (the clause now covers groups with no IDS), so the merge rule "diff inside Touches" is not met
- Suggest: briefs 086c to 088c name test_groups.py in Touches, or the test stops asserting emptiness of the filled groups
### 2026-11-20 · brief 088c · code
- Instruction: brief 088c guru ruling 2: plain functions `o1e(ev, specs, draws)` and `ot1(ev, specs, rows, read)` in `out_sweeps`.
- Happened: they must call `sweeps.breakeven_return` and `sweeps.tornado`, but R4 (`test_rules` cross-layer import) fails `runner/out_sweeps` importing `runner/sweeps`; the first version failed the suite.
- Cost: one rewrite: the functions now format the sweeps' results and the run script calls the sweeps.
- Suggest: rulings that name a function signature check it against the layer table of architecture.md 5.1.
### 2026-11-20 · brief 086c · code
- Instruction: brief 086c Design: fill `out_burden.per_path(raw, again)` and read the inputs "from the register and pack as 055c does (`ctx`, `theta`)".
- Happened: `per_path` gets `Raw` and `again` only; `Raw` has no `pack`, `reg`, `ctx` or `theta`. O5, O6, O8, OH1b, OH1b2, OH1c, DH1c need them (m5, m6, m8, m3_today, m11, m12, dh1c). 084c's tests also pin every group's `IDS == ()` and the empty-group digest, so any filled group fails `test_groups.py`.
- Cost: built five of twelve ids, stopped on seven (the brief's own stop rule).
- Suggest: the guru widens the group interface (`per_path(raw, again, ctx, theta)` or `Raw` carrying `ctx` and `theta`, an edit to `runner.py`) and loosens the two 084c tests to "IDS in the manifest".
- Status: resolved (092c added `env`; 086c rulings 2 fixed the rest)
- Status: resolved by guru rulings 2 (tweak hook); the brief's ruling 1 named only `wealth`, but line_flows reads `V0` (one more entry-worth: name the field the kernel reads)
### 2026-11-20 · brief 087c · code
- Instruction: brief 087c ruling 5 (S1 via `core_run` with a replaced ctx) and the 092c group interface
- Happened: `core_run` is in runner.py (L4), out_support is L3.5 (R4), and `again` overrides only the spec; the group also gets no ctx or rng except through `env`; `test_groups.py` asserted empty per_path for every group
- Cost: stopped on OS1; one test edit outside Touches
- Suggest: give the group interface a core-run hook (or move `core_run` below L3.5); briefs that fill a group name the test_groups assertion
- Status: resolved by guru rulings 2 (tweak hook); the brief's ruling 1 named only `wealth`, but line_flows reads `V0` (one more entry-worth: name the field the kernel reads)

### 2026-11-20 · brief 093r · research
- Instruction: brief 093r Read line (hypothesis path) and `docs/agents/research.md` First steps 2 (`reference/research/...`)
- Happened: the hypothesis path in the brief (a longer, wrong file name) does not exist (the file is `household-consumption-and-wealth-replenishment.md`); `reference/research/` does not exist (it is `docs/agents/reference/research/`)
- Cost: a few extra lookups; no wrong action
- Suggest: correct both paths
- Status: brief path was the guru's error (fixed in the archived brief); research.md paths fixed

### 2026-11-20 · brief 095r · research
- Instruction: fetch cited sources with WebFetch
- Happened: WebFetch returned URL_NOT_ON_ALLOWLIST for URLs not first returned by a search; the HAL copy of IFS WP 13/30 returned an access-denied page; the ONS decile composition page links only an xlsx
- Cost: Bozio and others' numbers and the decile composition were not read; extra searches
- Suggest: say in research.md that the author should attach PDFs that are not fetchable; note xlsx-only ONS pages as a data-request item
- Status: open

### 2026-11-21 · 097r · research
- Instruction: brief 097r Design; retrieve and inspect the cited open numeric files.
- Happened: ONS CSV/XLSX, BoE XLSX/Stata, and HMRC ODS downloads returned `Unsupported content-type`; HTML time-series/commentary pages remained readable.
- Cost: source workbooks and the NMG variable inventory could not be inspected; exact upload links were recorded instead.
- Suggest: author uploads the named files, or provide a repository runtime that can parse ODS/XLSX/Stata downloads.
- Status: fixed fc3906e (research.md runtime-check rule)

### 2026-11-21 · 098r · research
- Instruction: brief 098r Design; inspect held WAS and ONS XLSX/ZIP files.
- Happened: the connector returned XLSX as base64, ONS file fetches returned `Unsupported content-type`, and the runtime had no XLSX/ZIP parser or checkout, so the first pass reported the held tables as unreadable and concluded the joint stage-by-band distribution was not published. It is (Tables 2.11, 2.13).
- Cost: a wrong finding had to be corrected at close-out; the brief's acceptance test 1 could not be run.
- Suggest: research briefs that name held workbooks should say the run needs a local checkout with openpyxl, or the agent should stop and ask instead of concluding from marginals.
- Status: fixed fc3906e (research.md rule and brief-template Checks line)


### 2026-11-21 · 100r · research
- **Instruction:** 100r Checks to run; `python -I pipeline/check_agent_docs.py`.
- **Happened:** The GitHub-connected session has no local checkout or shell; the repository API can read/write files but cannot execute the repository's Python checker.
- **Cost:** The required automated documentation check could not be run; relevant paths were inspected through the repository API instead.
- **Suggest:** Provide a local checkout/shell in the research runtime, or run the checker in CI for research branches.
- Status: fixed fc3906e (research.md rule; guru runs the checker before merge)
### 2026-11-21 · brief 099r · research
- Instruction: brief 099r "Read in full the PDFs ... with page checks" (18 PDFs, one session).
- Happened: the context ran out mid-brief; the half-built moment tuples were lost to the summary and had to be re-extracted from the PDFs.
- Cost: about a third of the extraction repeated.
- Suggest: split a multi-PDF brief by file group, or have the agent write each file's rows to the repo as it goes.

### 2026-11-21 · brief 102r · research
- Instruction: continue a brief from a pushed branch ("resume from the branch")
- Happened: the prior agent left the brief's progress block at "ready; not started" and the branch name was not in the brief; a plain `git checkout` failed because the remote ref had to be fetched by name; one audit verdict (I-D4b "supports, bounds inside") was not borne out by its own numbers
- Cost: a few lookups; one verdict corrected
- Suggest: require a progress-block update with each wip commit (the brief already says so) and have the audit script state the comparison it makes in the verdict
- Status: open
