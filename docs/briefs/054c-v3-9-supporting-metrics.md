# 054: Model v3 V3-9: supporting metrics

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 052
- **Read:** `docs/model-v3/architecture.md` 2.7 and 6.2 (U1 to U6); `docs/model-v3/metrics.md` (M7, M7c to M7e, M9, M13, M14, M15a, M15b, S1); `docs/model-v3/added/`; `docs/model-v3/acceptance.md` V3-9 row.

## Goal
Declaration, welfare, lock-in, envelope, migration and capitalisation metrics.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/support.py` (520 lines) for `O7, OD1, OW1, OW2, OW3, OM1, OS1`. S1 is a switch, off in every headline cell, with one extra variant run. It does not import `burden`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-9 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/support.py`, `tests/model_v3/test_support.py`, this brief's progress block.

## Acceptance criteria
- U1 to U6 pass; hand cases exact.
- S1 off equals S1 absent.
- `support.py` at most 520 lines; no import of `burden`.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Burden metrics (V3-8); the runner.

## Open questions
Ask if a welfare formula needs a risk-aversion value the register does not hold.

## Implementation notes
<!-- progress:start -->
- **Done:** `core/support.py` (234 lines of 520) and `tests/model_v3/test_support.py` (159 of 300): M7, M7c to M7e, M9, M13, M14, M15a, M15b, S1; U1 to U6 pass; whole `tests/model_v3` suite 172 passed.
- **Next:** none for this brief; V3-10 (runner) calls these with register values as fractions and one call per block of paths for the certainty-equivalent metrics.
- **Decisions:** certainty equivalent read as U^-1(E[U(W)]) (metrics.md M13 prints E[U^-1(W)]); M14 payer picks the better terminal wealth per path (hindsight); comparators tax start-of-year payers only; M7 has no settlement loop (post-surrender basis leaves nothing to settle); M15b is the mean annual percent of GDP over the first N years.
- **Gotchas:** inputs the caller must supply because the register or pack lack them: distribution of declared alpha (M7e, supporting.md M-3), consumption spend and its rate for the migration loss (M-4), the second asset's returns and the embedded-gain bands (M14), the gains-tax realisation rate (M13).
- **Resume:** n/a
- **Not run:** nothing.
- **State:** done; merged by the auto-merge rule
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 054c, model v3 V3-9: supporting metrics
- Files changed: model_v3/core/support.py (new); tests/model_v3/test_support.py (new); this brief's progress block
- What is different now: v3 can compute the declaration curve and tolerant zone, the migration-adjusted revenue, the four-system welfare table at equal revenue, CGT lock-in, envelope binding and the S1 switch, all from arguments (no register or pack read)
- New or changed interfaces: support.declaration_runs / declaration_curve / tolerant_zone / modal_alpha; migration_effect; crra_ce / cew_bp / system_run / solve_rate / wdt_run / welfare / wmean; lockin; envelope / liquidity_timing; capitalise / payer_count / s1_effect. Rates and shares are fractions; percent and basis points come back as such
- Acceptance criteria:
  - U1 to U6 pass, hand cases exact: met (U1 hand case on the kernel: net 3.1 against 5, TW(1) 145, C.1 -1.3103; U2 CE 80 and 100, -5000 bp; U4 X 0.4 and M9 = M1 - X exactly; lock-in hand costs -195.12 and -266.67 bp; U3 envelope forgone equals the kernel's lost_refund, line 0 7.25 - 2.5 = 4.75)
  - S1 off equals S1 absent: met (array equal, payer count equal, effect zero)
  - support.py at most 520 lines, no import of burden: met (234 lines; imports numpy and kernel only)
  - git diff --stat limited to Touches: met
- Deviations from the brief: none
- Risks / follow-ups:
  (1) metrics.md M13 and welfare.md write CEW with E[U^-1(W)]; I implemented the standard certainty equivalent U^-1(E[U(W)]). Author or guru to confirm and fix the wording.
  (2) Risk aversion is held (I-H5a 1.0 / 1.5 / 1.99), so no stop was needed. The other welfare inputs are not in the register: the gains-tax rate and realisation share, the second asset's return path and the embedded-gain bands (M14), and the consumption base of the migration loss (M-4). The functions take them as arguments; V3-10 needs them or a stated stand-in.
  (3) M7e takes a distribution of declared alpha as an argument; the register holds none (supporting.md M-3), so the modal declaration cannot yet be produced from the model.
  (4) Certainty equivalents are one number per set of paths; the manifest's p10_mean_p90 over paths means V3-10 must call them per block of paths (a level 2 draw) and summarise across blocks.
  (5) The wealth tax comparator and the gains-tax comparator are one-asset payer rules written here (start-of-year stock tax; tax on positive annual gains with losses unrelieved); the author may want other rules.
  (6) A line under W_min at the start can cross it later under the WDT while its comparators stay untaxed; weights and revenue count start-of-year payers only.
- Verification: pytest tests/model_v3 -q on main as of today plus this branch: 172 passed (includes the V3-1 import-graph, side-effect, orphan, country and budget rules)
- Overview sections likely needing an update: model v3 build status
- Commit / branch: brief/054-supporting-metrics
```

