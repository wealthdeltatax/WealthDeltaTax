# 081: Drop M7e (modal declaration) from the metrics and the manifest

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none
- **Read:** `docs/research/080r-declared-alpha-evidence.md` (section 4: M7e reads 1.00 on the OD1 grid for any centre between 0.875 and 1.125); `docs/model-v3/outputs.yml` entry OD1; `docs/model-v3/metrics.md` rows M7c to M7e and the paragraph under them; `docs/model-v3/architecture.md` where it names M7e; `docs/archive/briefs/079g-m2-with-death-output.md` (the manifest amendment pattern: version string, validator, pins, cards).

## Goal
M7e is not produced. The manifest and the metrics list say so, so the runner, the writer, the hooks and the site never look for it.

## Decisions (author, 2026-11-20)
- Drop M7e. OD1 keeps `lines: [M7c, M7d]`; O7 (tolerant zone) is unchanged. No register rows for the declared-alpha distribution.
- The old papers' behavioural centre near alpha 1.1 is retracted as a claim (model-implied, unsourced): guru-edited `framework.md`, `ledger.md` and `ledger-sections.md` already say so (merged with this brief).

## Design
1. `outputs.yml`: remove M7e from OD1's `lines`, `unit` and `decimals`; bump the manifest version string as 079g did; update any count in the header.
2. `metrics.md`: strike the M7e row (keep the id with "dropped 2026-11-20: see 080r"; do not reuse it), remove the sentence on M7e in the paragraph after the supporting rows, and the mention in the "Amendments" paragraph if it names M7e.
3. `architecture.md`: remove M7e from the V3-9 "Does" line and anywhere else it is named; if a test budget or line count there depends on it, say so in the report, do not recompute.
4. Update pinned counts and fixtures as 079g did (`tests/data`, `tests/hooks`), regenerate the cards (`python pipeline/page_cards.py`), and report any test or page that names M7e.
5. Do not edit `model_v3/` code: Agent 3 removes `modal_alpha` and its test in 055c.

## Touches
`docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md`, `docs/model-v3/architecture.md`, `pipeline/validate_outputs.py` (only if it pins ids), `tests/data/` and `tests/hooks/` (pin updates only), `docs/restructure/pages/` (regenerated), this brief's progress block.

## Acceptance criteria
- `grep -rn M7e docs/model-v3/outputs.yml` returns nothing; `metrics.md` names M7e only as dropped.
- `python pipeline/validate_outputs.py` exit 0; `python pipeline/run_suites.py` passes.
- `git diff --stat` limited to Touches.

## Checks to run
`python pipeline/validate_outputs.py`; `python pipeline/run_suites.py`.

## Out of scope
Model code, the register, the old papers (082w).

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
