# 079: Add the output for M2 including death flows (O2d) to the manifest

- **Status:** done, merged 2026-11-20
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
- **Done:** O2d added after O2 (same `by`, summary, unit, decimals, element, kind headline); O2 retitled "in life"; manifest version `stage-A10-o2d-2026-11-20`; metrics.md M2 reworded in life and a new M2d row (46 metrics); cards, metrics.json and fixture regenerated; all ten suites pass (`run_suites.py`), validator PASS in fixture mode.
- **Next:** 053c's writer and runner read O2d later (V3-10, V3-11). The author decides whether M5 gets a with-death line (below).
- **Decisions:** M5 NOT changed. Manifest form allows `lines` (OF1, O1), but O5 has none: adding `lines: [M5, M5d]` puts a `line` field on every O5 cell, needs an M5d metric row, and changes what the hooks resolve for O5. Decision for the author: add it in a separate brief, or leave M5 in life only.
- **Gotchas:** fixture fake numbers are positional, so inserting O2d shifted later numbers; five hooks pins re-pinned (CK1 P1 2.8, P3 4.30, P7b 5.80; O3 1.30). Logged in brief-suggestions. O2d listed in the fixture spokes `pay.md` and `fisc.md` (R1r needs a hook cite per element). Beyond Touches, needed: `architecture.md` 2.6 ids and the 2.10 module table (test W7 reads it), and the metric-count pin 45 to 46.
- **Resume:** merged.
- **Not run:** site build (nothing wired).
- **State:** done
<!-- progress:end -->
