# 053: Model v3 V3-8: burden and savings

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 052
- **Read:** `docs/model-v3/architecture.md` 2.6 and 6.2 (D1 to D6); `docs/model-v3/metrics.md` (M2, M2b, M2c, M3, M4a to M4c, M5, M6, M8, M11, M12); `docs/model-v3/added/` (welfare and problem outputs); `docs/model-v3/acceptance.md` V3-8 row.

## Goal
Burden, non-payer savings and the comparators as per-path arrays.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/burden.py` (430 lines) for the ids `O2, O3, O2b, O2c, O4a, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c` of `architecture.md` 2.10. Comparators read only the pack and register. Imports `pack`, `base`, `schedule`, `kernel`, `revenue`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-8 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/burden.py`, `tests/model_v3/test_burden.py`, this brief's progress block.

## Acceptance criteria
- D1 to D6 pass; hand cases exact to 1e-12.
- DH1c equals the pack decile table.
- `burden.py` at most 430 lines.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Supporting metrics (V3-9); the runner.

## Open questions
Ask if a metric formula in `metrics.md` is ambiguous.

## Implementation notes
<!-- progress:start -->
- **Done:** `core/burden.py` (316 of 430 lines) and `tests/model_v3/test_burden.py` (206 of 250): `line_flows`, M2, M2b, M2c, M3, OH1b (today line), OH1c, M4a to M4c, DH1c, M5, M6, M8 (burden), M11. D1 to D6 pass; `pytest tests/model_v3 -q`: 176 passed.
- **Next:** merged by the auto-merge rule after the author's rulings of 2026-11-20 (`docs/decisions.md`, `metrics.md` closed list); 079g adds O2d to the manifest; V3-10 reads these functions.
- **Decisions:** (1) `line_flows` keeps every line and death phase (revenue's run is aggregate only); it reconciles with `revenue.run_lines` to 1e-9. (2) M2 is in life by default (author ruling 2026-11-20), `m2d` is M2 with death flows; M2b and M2c still read all net WDT (the ruling does not cover them; `inlife` flag exists). (3) M3 and M12: gains are the positive real changes in net wealth. (4) M4: incidence by income decile of all households (no joint income and wealth table); corporation tax by gross income; the two payer-side taxes give non-payers nothing. (5) M8 burden only.
- **Gotchas:** (1) Death flows are 87% of M2d (short: 22.2% with death, 2.8% in life). (2) M5 and M8 are on launch line means, so only RL tiers pass the large thresholds. (3) Not built: M3-all-tax line, M8 non-payer saving, M2b/M2c below-W_min income.
- **Resume:** `git checkout brief/053-burden`; after the ruling edit the defaults in `burden.py` (`inlife`, gain definition) and the hand cases.
- **Not run:** the runner and `out/` (V3-9); anything with the pack for another country.
- **State:** done; merged to main; ready to retire.
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 053c, model v3 stage V3-8: burden, non-payer savings and comparators
- Files changed: model_v3/core/burden.py (316 lines, budget 430); tests/model_v3/test_burden.py (206 lines, budget 250); this brief
- What is different now: per-line, per-year flows over the kernel (`line_flows`) and the metrics M2, M2b, M2c, M3, OH1b, OH1c, M4a, M4b, M4c, DH1c, M5, M6, M8, M11 as array functions with hand cases
- New or changed interfaces: burden.py public functions (arguments: flows dict, windows lo/hi, register, pack, tax names `order`/`parts`/`payer_taxes` passed in so no tax or country is named, R11)
- Acceptance criteria:
  - D1 M2 revenue-weighted hand case: met (18.0 against payer-weighted 12.5, to 1e-12); M2b, M2c hand cases met
  - D2 M3 gain-weighted hand case: met (103.0 = PV year-1 tax over PV year-2 gain, 1e-12); OH1b and OH1c hand cases met
  - D3 M4a by income decile hand case: met (1e-12)
  - D4 DH1c equals the pack decile table: met (bill and income equal the pack's total_tax and gross_income, exactly)
  - D5 M8 equals the revenue at the same people: met (revenue_bn equals the input to 1e-12; lines below W_min pay nothing)
  - D6 comparators read only pack and register values: met (m5 and m6 run on a register-only stub; a missing row raises)
  - burden.py at most 430 lines: met (316). git diff limited to Touches: met (two new files and this brief)
- Deviations from the brief: none in scope; two metrics partly built (see Risks)
- Risks / follow-ups (items 1 to 3 ruled by the author on 2026-11-20 and built as ruled; items 4 and 5 are limits of the first run, listed in `metrics.md`; M2b and M2c still read all net WDT, not covered by the ruling):
  1. M2 and death flows. M2 as written is net WDT of the year over start-of-year wealth; that includes what a death triggers. On 117 windows (14 lines, register mix, v2-like settings, post-fill 10 years, median): M2d 22.2% a year (D10 27.4%), M2 in life 2.8% (D10 3.6%); long run 10.9% against 0.75%. RULED (author, 2026-11-20): O2 is in life, O2d with death (brief 079g); `m2` is in life by default, `m2d` is the with-death reading, and `m5` takes both and returns `_diff` (in life) and `_diff_death`. The comparators burden 1.0 to 2.0% a year: about -1 point against in life, -20 against M2d.
  2. M3 gains. The signed sum of real changes in net wealth is zero or negative over many lives, so no rate exists; I use the positive part (as M12). Median M3 25.0% (10th to 90th 20.6 to 32.8) with death flows, 7.7% in life. Today's liabilities (OH1b): 7.4% overall, D10 10.4%.
  3. M4a incidence. The pack has a tax's share only for the top decile and the bottom five; the rest split evenly, corporation tax by gross income, the two payer-side taxes zero. Result: retired taxes save the non-payers 25.1% of their tax bill overall (D1 36.2%, D10 17.6%), 8.4% of income (D1 17.2%); M4c 331, 397, 559, 620 pounds a month at p25 to p90. The non-payers' share of a decile is taken as the decile's (no joint income and wealth table).
  4. Lines. Each line is one representative adult, so M2b has D10 at 89.9% of income and M5 and M8 test thresholds on line means (D10b mean 4.7 million: nothing passes 10 million). Same cause as the I1 gap.
  5. Not built: M3-all-tax line of OH1b (investment income rows exist for D10 only), the non-payer saving form of M8 (the reform's own incidence by income decile is not held), M2b and M2c for lines below W_min (no source). M8 burden: a property reform raising the WDT's 89.4bn (post-fill 10-year, 3.92% of GDP) costs its payers 0.70% of wealth a year, a gains reform 0.69%.
- Verification: pytest tests/model_v3 -q: all pass after the rebase on main (count in the merge note). line_flows net, weighted and scaled, equals revenue's aggregate tax + refund + death + heirs to 1e-9 on 6 paths; R11 scan clean
- Overview sections likely needing an update: model v3 build status (V3-8 built)
- Commit / branch: brief/053-burden, merged by fast-forward; brief 053 merged, ready to retire
```
