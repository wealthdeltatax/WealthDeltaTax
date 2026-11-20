# 079: Add the output for M2 including death flows (O2d) to the manifest

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none (053c's code change is separate and does not touch these files)
- **Read:** `docs/model-v3/outputs.yml` entries O2 and O2b; `docs/model-v3/metrics.md` rows M2 and M5 and the section "Closed on 2026-11-20 (author)" (merged with this brief); the 053c change report (`git show origin/brief/053-burden:docs/briefs/053c-v3-8-burden-and-savings.md`, Risks 1); `docs/archive/briefs/065g-ck1-lines.md` and `045g-*.md` (how a manifest amendment was done: version string, validator, pins, cards); `pipeline/validate_outputs.py`; `docs/restructure/site/hooks.md` 3.2.

## Goal
M2, the taxpayer burden as a share of wealth, is reported twice (author, 2026-11-20): O2 as the headline **in life** (comparable with the annual comparator taxes of M5), and a new output O2d as the same metric **including the settlement at death**, labelled as such. The manifest holds O2d so the run, the hooks and the site can reach it.

## Decisions (author, 2026-11-20)
- O2 = M2 in life only. O2d = M2 including death flows (the whole net WDT of the year over start-of-year wealth). Same `by`, `summary`, unit and decimals as O2; element, kind as O2 unless the validator needs otherwise.
- M5's difference is computed on the in-life reading; M5 also reports the with-death difference as a second line if its output form allows (check the M5 entry; if not, report it to the guru, do not invent a form).

## Design
1. `outputs.yml`: add O2d next to O2, title stating "including settlement at death", bump the manifest version string as 065g did, update any count in the header. O2's own title gets "in life".
2. `metrics.md`: add an `M2d` row (M2 including death flows) after M2, one sentence; amend the M2 row's wording to name the in-life reading (the guru's "Closed on 2026-11-20" paragraph holds the ruling; do not edit that paragraph).
3. Update pinned counts and fixtures the way 065g did (tests/data, tests/hooks, `pipeline/validate_outputs.py` if it pins ids), regenerate the cards if they embed the manifest (`python pipeline/page_cards.py`), and report any test or page that names O2 and might need O2d.
4. Do not edit `model_v3/` code: 053c (Agent 5) builds the function with a flag; the writer and runner read the manifest later (V3-10, V3-11).

## Touches
`docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md`, `pipeline/validate_outputs.py` (only if it pins ids), `tests/data/` and `tests/hooks/` (pin updates only), `docs/restructure/pages/` (regenerated), this brief's progress block.

## Acceptance criteria
- O2d exists in the manifest; the validator exits 0.
- `pytest tests/data`, `tests/gate`, `tests/cards`, `tests/hooks`, `tests/model_v3` pass (separate commands or `python pipeline/run_suites.py`).
- `git diff --stat` limited to Touches.

## Checks to run
`python pipeline/validate_outputs.py`; `python pipeline/run_suites.py`.

## Out of scope
The model code; M2b, M2c, M3 and M5 outputs beyond the check in Decisions.

## Open questions
None. Ask rather than guess if the manifest's form for M5 cannot carry a second line.

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
