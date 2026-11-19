# 065: Make the stress-test output CK1 hookable

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** none (058c and 060c are merged)
- **Read:** `docs/briefs/` archive `060c-hook-resolver.md` (its Gotchas 1); `docs/model-v3/outputs.yml` entries CK1 and OW3 (a multi-metric entry with `lines` and `line_horizons`); `pipeline/validate_outputs.py` (V7); `pipeline/hooks.py` (H13); `docs/restructure/site/hooks.md` 3.2 and 4.2.

## Goal
Every manifest output can be reached by a hook. CK1 holds three metrics (P1, P3, P7b) with units and decimals given per metric but no `lines`, so its cells carry no metric and the resolver returns H13. Give CK1 the `lines` form that OW3 uses.

## Decisions (author and guru, 2026-11-19)
- CK1 becomes `lines: [P1, P3, P7b]` with its existing per-metric `unit` and `decimals`, the same form as OW3; `horizons` stays `[short]`; its `by: {amplitude: ...}` stays.
- Version string of the manifest changes to `stage-A9-ck1-lines-2026-11-19`.
- A hook for a CK1 cell reads `{{o:CK1:P1.mean@A5}}`-style per the 060c line selector; the resolver needs no change if CK1 then resolves; if it does, change only what H13 needs and say so.

## Design
1. Edit the CK1 line of `outputs.yml` and the version string; check `metrics.md` needs no change.
2. Regenerate: `python pipeline/build_metrics.py`, the fixture (`python tests/data/make_fixture.py`, whose hash embeds the manifest), and the page cards (`python pipeline/page_cards.py`).
3. Add a test in `tests/hooks/` that resolves one CK1 cell for each of P1, P3 and P7b on the fixture and formats them with the per-metric units and decimals.
4. Check that V7 now expects 3 lines times 5 amplitudes cells for CK1 (45 with the three schedules if CK1 is per schedule, otherwise as the entry states) and that the fixture and model-v3 tests still pass.

## Touches
`docs/model-v3/outputs.yml` (the CK1 line and the version only), `registry/metrics.json` (regenerated), `tests/data/fixtures/outputs.fixture.json` (regenerated), `docs/restructure/pages/` (regenerated cards), `tests/hooks/test_hooks.py` (one test added) and `tests/hooks/fixtures/` if a fixture needs a CK1 cell, this brief's progress block. If `pipeline/hooks.py` must change, stop and report it to the guru before editing.

## Acceptance criteria
- `python pipeline/validate_outputs.py tests/data/fixtures/outputs.fixture.json --fixture` exits 0.
- The three CK1 hooks resolve to the fixture's values with the right units.
- `pytest tests/data`, `tests/gate`, `tests/hooks`, `tests/cards`, `tests/model_v3` pass (separate commands).
- `git diff --stat` limited to the Touches list; the CK1 line differs only in the added `lines`.

## Checks to run
The commands above.

## Out of scope
The model, other outputs, `hooks.md`.

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
