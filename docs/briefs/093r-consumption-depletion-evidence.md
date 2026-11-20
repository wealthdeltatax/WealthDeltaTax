# 093: Evidence for the consumption setting I-D14c (tests A and C of the household-consumption hypothesis)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none (090c merged)
- **Read:** `docs/hypotheses/household-consumption-income-and-replenishment-of-private-wealth.md` (sections 3, 6 and 7; tests A and C only); `docs/model-v3/wealth-ratio-diagnostic/report.md` (the sensitivity: wealth to GDP at year 100 is 0.47 at 3.5%, 1.16 at 2.5%, 2.77 at 1.5%; break-even about 2.65%); register row **I-D14c** in `docs/model-v3/inputs.md` (low 0.5, central 3.5, high 5, marked (J)); `model_v3/core/kernel.py` `grow_and_consume`; v2's `WDT_Params.toml` and `valgen` D16 (`c_mode` fixed, the stationary mode) wherever the repository holds them; `docs/model-v3/source-map.md`; archived `docs/archive/briefs/080r-declared-alpha-evidence.md` and `069r-*.md` (how a research brief reports and how rows are proposed).

## Goal
Say what the 3.5% in I-D14c is and what the evidence supports, so the author can rule on the row. Two questions only: (A) what does the parameter represent and where did it come from; (C) what do UK data bound for **net depletion of existing household wealth by band** (the quantity the kernel's proportional drawdown stands for).

## Decisions (author, 2026-11-20)
- No model, register or manifest change comes from this brief, and no value is to be chosen because it makes WDT's fiscal closure look better or worse. The hypothesis says so (section 6, test C) and the author confirmed it.
- Tests B, D, E and F (alternative household-flow specifications, decomposition, re-run of WDT outcomes) wait for this report. They are a later code brief, only if the evidence gives defensible ranges.

## Design
1. **Test A, audit.** Trace I-D14c to its origin: v2's `c` (`valgen` D16, `c_mode` fixed), the v2 comments that call 0.5, 2 and 5 the sensitivity grid, and anything in `docs/` or the old papers that says what it was meant to be (consumption from wealth, net liquidation, a proxy for net dissaving, a depletion hazard). Say which it is, whether it was meant to apply uniformly to every household and asset class, and whether any empirical source exists. If none, say so: it stays a judgement assumption.
2. **Test C, evidence.** Find UK data that bound **net change in household net wealth from non-valuation causes** (saving, net of gifts and bequests given) by wealth band or decile, and consumption relative to net wealth by band: ONS Wealth and Assets Survey (waves, changes in wealth by decile, the split between saving and revaluation where published), ONS household finances and the sectoral financial and non-financial accounts (household sector saving, revaluations, the saving ratio), Resolution Foundation and IFS work on wealth accumulation and decumulation by age and band, and academic work on wealth decumulation at the top (the Bank of England's household wealth work, Advani and Summers, Atkinson). Keep **saving**, **revaluation (capital gains)** and **transfers** apart: the hypothesis (section 3) says a rise in asset values is not saving and expenditure is not a reduction in existing wealth.
3. For each source: the quantity measured, the number (by band where given), the sample, the year, the population coverage, the definitions (disposable income, saving, net wealth, what is excluded), and the licence if data is reproduced. Reconcile or flag definitions that do not match; do not combine survey and national-accounts figures without saying how they differ. Use the repository's research-note form; no long extracts.
4. **Table of what the evidence supports** (do not edit the register): for each band (D4-5, D6-7, D8-9, D10) and overall, a low, central and high **net depletion rate** if the data support one, whether each is data or judgement (J), and the gap, if any, between that and the kernel's 3.5% applied to every line. If the evidence cannot support a rate, say what weaker statement it can.
5. **Say plainly** whether the evidence suggests net depletion of existing wealth is, for the bands that pay WDT, above, below or about equal to 3.5%, and how confident that reading is. Do not translate it into a WDT result. The note may say which rows the guru would propose; it does not propose a value for any band that no data support.
6. Report anything found on **income-funded saving at the top** (the share of top-decile wealth accumulation that comes from saving out of income against returns), because the hypothesis's specification B needs it; mark as a pointer for the later code brief only.

## Touches
`docs/research/093r-consumption-depletion-evidence.md` (new), `docs/model-v3/inputs-added/` only if the research-note convention puts proposed rows there (follow 069r), this brief's progress block, `docs/agents/friction-log.md`. No register, code or manifest edits.

## Acceptance criteria
- The audit (item 1) names the origin of I-D14c, or says none was found; each source in item 2 has quantity, number, sample, year and definitions.
- The table in item 4 is present, with (J) marked and the gap to 3.5% stated; item 5's reading is stated with its confidence.
- Saving, revaluation and transfers are kept apart in every figure used, or the note says which a figure mixes.
- `git diff --stat` limited to Touches.

## Checks to run
None to run (a research note); the guru checks each cited number against its source before review.

## Out of scope
Any change to the kernel, `I-D14c`, the register, the schedule, the retirement rule or the fund; tests B, D, E, F; a fiscal result.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** wrote `docs/research/093r-consumption-depletion-evidence.md`. Audit: I-D14c is v2 plan decision D16 (1 Oct, user-set, steady-state device, c 2 to 5%, baseline 3.5%, set against nominal returns), applied uniformly, no empirical source. Evidence: no UK net depletion rate by band; aggregate saving positive (ratio 9.5% in 2024, about 1.6% of net worth, my arithmetic), kernel-equivalent aggregate c at most about 3.0%; ELSA net financial wealth ages 70+ down 1.8% a year (2.4% wealthier half, 0.7% poorer half, total change). Reading: below 3.5% in aggregate, about equal or above for retired financial wealth, unmeasured by band; low to moderate confidence.
- **Next:** guru checks each cited number against its source (all read via fetch summaries, page numbers not checked); author rules on the three open questions in section 7 of the note.
- **Decisions:** no band rates entered in the table (no data support one); aggregate row uses an income-yield assumption marked (J); rows proposed in the note only, no `inputs-added` file (080r form).
- **Gotchas:** the brief's hypothesis path differs from the file (`household-consumption-and-wealth-replenishment.md`); `docs/agents/research.md` names `reference/research/` but the files are in `docs/agents/reference/research/`; register cites `WDT_Params.toml` line 714 for `c`, actual line 711.
- **Resume:** n/a
- **Not run:** no checks named by the brief; numbers not yet checked against primary PDFs.
- **State:** done on branch `brief/093-consumption-depletion-evidence`; not merged, NEEDS THE AUTHOR
<!-- progress:end -->

### Change report
- Task: brief 093r, evidence for I-D14c (tests A and C)
- Files changed: `docs/research/093r-consumption-depletion-evidence.md` (new research note); this brief's progress block; `docs/agents/friction-log.md` (one entry, two wrong paths)
- What is different now: the repository has an audit of I-D14c's origin and a sourced statement of what UK data do and do not bound
- New or changed interfaces: none
- Acceptance criteria: audit names the origin (D16, 1 Oct), each source has quantity, number, sample, year and definitions: met. Item 4 table present with (J) marked and the gap to 3.5% stated, item 5 reading stated with confidence: met, with no band rates because no data support one. Saving, revaluation and transfers kept apart or the mix named for every figure: met. `git diff --stat` limited to Touches: met
- Deviations from the brief: none; hypothesis file opened under its actual name
- Risks / follow-ups: all numbers read through fetch summaries, so the guru's number check matters; ELSA figure is a total change and needs an assumed return to become a kernel c; aggregate row depends on an unsourced income yield
- Instruction friction: one entry added to `docs/agents/friction-log.md` (two wrong paths)
- Verification: no checks named; arithmetic in section 3.2 recomputed by hand; nothing else run
- Overview sections likely needing an update: none
- Commit / branch: see final message, `brief/093-consumption-depletion-evidence`
