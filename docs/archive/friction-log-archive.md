# Friction log archive

Closed entries (fixed or dropped) moved from `docs/agents/friction-log.md` by the guru. Oldest first.

### 2026-11-20 · 084c · code
- Instruction: brief 084c Touches and architecture.md 5.1 (R4 layers): a new runner module needs a row in the LAYER table of `tests/model/model_v3/conftest.py`
- Happened: the brief adds `model/model_v3/runner/groups.py` and four `out_*.py` files that `runner.py` imports; R4 fails any edge with a module not in LAYER, and conftest.py was not in Touches
- Cost: stopped to ask; the author said to add the rows (out_* 3.5, groups 3.7), so conftest.py changed outside Touches
- Suggest: briefs that add a module name the LAYER row, and 5.1 lists the new modules
- Status: fixed (code.md: module and test_groups rule)

### 2026-11-20 · brief 083c · code
- Instruction: brief 083c "Read:" and Design (how to build the runner context); `runner.context` needs the tier 1 list and `payer_taxes`.
- Happened: neither is named in the brief; `payer_taxes` has no home in `levers.json` (055c gotcha 6), so I copied the fixture from `tests/model/model_v3/test_runner.py`.
- Cost: a few minutes reading the tests to find the call.
- Suggest: a brief for a one-off script should name the test fixture that builds the context (084c has since moved `payer_taxes` into `levers.json`).
- Status: fixed (guru.md: name the context fixture)

### 2026-11-20 · 085c · code
- Instruction: brief 085c Touches; `tests/model/model_v3/test_groups.py` (084c, 092c) asserts every group is empty: `all(m.cells({}) == m.per_path(None, None, None) == {} ...)`
- Happened: filling `out_revenue.py` made that assertion fail (`KeyError: 'M1e'`); test_groups.py is not in Touches
- Cost: edited it outside Touches (the clause now covers groups with no IDS), so the merge rule "diff inside Touches" is not met
- Suggest: briefs 086c to 088c name test_groups.py in Touches, or the test stops asserting emptiness of the filled groups
- Status: fixed (code.md rule)

### 2026-11-20 · brief 088c · code
- Instruction: brief 088c guru ruling 2: plain functions `o1e(ev, specs, draws)` and `ot1(ev, specs, rows, read)` in `out_sweeps`.
- Happened: they must call `sweeps.breakeven_return` and `sweeps.tornado`, but R4 (`test_rules` cross-layer import) fails `runner/out_sweeps` importing `runner/sweeps`; the first version failed the suite.
- Cost: one rewrite: the functions now format the sweeps' results and the run script calls the sweeps.
- Suggest: rulings that name a function signature check it against the layer table of architecture.md 5.1.
- Status: fixed (code.md layer check)

### 2026-11-20 · brief 086c · code
- Instruction: brief 086c Design: fill `out_burden.per_path(raw, again)` and read the inputs "from the register and pack as 055c does (`ctx`, `theta`)".
- Happened: `per_path` gets `Raw` and `again` only; `Raw` has no `pack`, `reg`, `ctx` or `theta`. O5, O6, O8, OH1b, OH1b2, OH1c, DH1c need them (m5, m6, m8, m3_today, m11, m12, dh1c). 084c's tests also pin every group's `IDS == ()` and the empty-group digest, so any filled group fails `test_groups.py`.
- Cost: built five of twelve ids, stopped on seven (the brief's own stop rule).
- Suggest: the guru widens the group interface (`per_path(raw, again, ctx, theta)` or `Raw` carrying `ctx` and `theta`, an edit to `runner.py`) and loosens the two 084c tests to "IDS in the manifest".
- Status: resolved (092c, 086c rulings)

### 2026-11-20 · brief 087c · code
- Instruction: brief 087c ruling 5 (S1 via `core_run` with a replaced ctx) and the 092c group interface
- Happened: `core_run` is in runner.py (L4), out_support is L3.5 (R4), and `again` overrides only the spec; the group also gets no ctx or rng except through `env`; `test_groups.py` asserted empty per_path for every group
- Cost: stopped on OS1; one test edit outside Touches
- Suggest: give the group interface a core-run hook (or move `core_run` below L3.5); briefs that fill a group name the test_groups assertion
- Status: resolved (092c, tweak hook)

### 2026-11-20 · brief 093r · research
- Instruction: brief 093r Read line (hypothesis path) and `docs/agents/research.md` First steps 2 (`reference/research/...`)
- Happened: the hypothesis path in the brief (a longer, wrong file name) does not exist (the file is `household-consumption-and-wealth-replenishment.md`); `reference/research/` does not exist (it is `docs/agents/reference/research/`)
- Cost: a few extra lookups; no wrong action
- Suggest: correct both paths
- Status: fixed (paths corrected)

### 2026-11-20 · brief 095r · research
- Instruction: fetch cited sources with WebFetch
- Happened: WebFetch returned URL_NOT_ON_ALLOWLIST for URLs not first returned by a search; the HAL copy of IFS WP 13/30 returned an access-denied page; the ONS decile composition page links only an xlsx
- Cost: Bozio and others' numbers and the decile composition were not read; extra searches
- Suggest: say in research.md that the author should attach PDFs that are not fetchable; note xlsx-only ONS pages as a data-request item
- Status: fixed (research.md fetching rule)

### 2026-11-21 · 097r · research
- Instruction: brief 097r Design; retrieve and inspect the cited open numeric files.
- Happened: ONS CSV/XLSX, BoE XLSX/Stata, and HMRC ODS downloads returned `Unsupported content-type`; HTML time-series/commentary pages remained readable.
- Cost: source workbooks and the NMG variable inventory could not be inspected; exact upload links were recorded instead.
- Suggest: author uploads the named files, or provide a repository runtime that can parse ODS/XLSX/Stata downloads.
- Status: fixed fc3906e

### 2026-11-21 · 098r · research
- Instruction: brief 098r Design; inspect held WAS and ONS XLSX/ZIP files.
- Happened: the connector returned XLSX as base64, ONS file fetches returned `Unsupported content-type`, and the runtime had no XLSX/ZIP parser or checkout, so the first pass reported the held tables as unreadable and concluded the joint stage-by-band distribution was not published. It is (Tables 2.11, 2.13).
- Cost: a wrong finding had to be corrected at close-out; the brief's acceptance test 1 could not be run.
- Suggest: research briefs that name held workbooks should say the run needs a local checkout with openpyxl, or the agent should stop and ask instead of concluding from marginals.
- Status: fixed fc3906e

### 2026-11-21 · 100r · research
- **Instruction:** 100r Checks to run; `python -I pipeline/check_agent_docs.py`.
- **Happened:** The GitHub-connected session has no local checkout or shell; the repository API can read/write files but cannot execute the repository's Python checker.
- **Cost:** The required automated documentation check could not be run; relevant paths were inspected through the repository API instead.
- **Suggest:** Provide a local checkout/shell in the research runtime, or run the checker in CI for research branches.
- Status: fixed fc3906e

### 2026-11-21 · brief 099r · research
- Instruction: brief 099r "Read in full the PDFs ... with page checks" (18 PDFs, one session).
- Happened: the context ran out mid-brief; the half-built moment tuples were lost to the summary and had to be re-extracted from the PDFs.
- Cost: about a third of the extraction repeated.
- Suggest: split a multi-PDF brief by file group, or have the agent write each file's rows to the repo as it goes.
- Status: fixed (research.md long data briefs, 2026-11-21)

### 2026-11-21 · brief 101r · research
- Instruction: "continue on brief/101-parameter-map-flows ... four steps remain"; the brief's progress block was empty and `git checkout -b ... origin/brief/101-...` failed (clone tracks main only).
- Happened: I fetched the branch by name and inferred the four steps from the brief's design items against the committed tables.
- Cost: a few minutes and a guess at what "four steps" meant.
- Suggest: the checkpoint commit (or hand-over message) should fill the progress block's Done and Next lines.
- Status: fixed (template Resume line with branch fetch, 2026-11-21)

### 2026-11-21 · brief 102r · research
- Instruction: continue a brief from a pushed branch ("resume from the branch")
- Happened: the prior agent left the brief's progress block at "ready; not started" and the branch name was not in the brief; a plain `git checkout` failed because the remote ref had to be fetched by name; one audit verdict (I-D4b "supports, bounds inside") was not borne out by its own numbers
- Cost: a few lookups; one verdict corrected
- Suggest: require a progress-block update with each wip commit (the brief already says so) and have the audit script state the comparison it makes in the verdict
- Status: fixed (template Resume line; research.md audit rule)

### 2026-11-21 · brief 103r · research
- Instruction: "a row for every variable of the 094r dictionary" and "every row classified" (five classes: observed, derived, proxy, scenario, unset).
- Happened: `T_WDT`, `dNW` and `r_f` are model outputs, not parameters, so no existing class fits; I added an "endogenous" class for three dictionary rows.
- Cost: a vocabulary choice the guru did not make; the class count in the note has a sixth entry.
- Suggest: add "endogenous (model output, no parameter)" to the classification in `docs/hypotheses/empirical-household-flow-parameter-map.md`, or say that dictionary terms that are not parameters need no row.
- Status: fixed (endogenous class added to the hypothesis, 180ccae)
