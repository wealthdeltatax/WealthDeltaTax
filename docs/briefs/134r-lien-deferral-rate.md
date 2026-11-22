# 134: Evidence and a register row for the lien deferral rate

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 132c (merged)
- **Read:** `docs/model-v3/household-arm-lien.md` ("The rule as built"); `docs/model-v3/inputs.md` ("Rows and judgement rows", D11 discount schedule); `docs/agents/reference/research/reference-workflow.md`; archived `docs/archive/briefs/080r-declared-alpha-evidence.md` (note form).

## Goal
The pension-secured lien (132c) and the Route B lien accrue at `r_def`, which is 0.0 in every run because no register row sets it. At zero real interest a balance carried 29 years is a deferral subsidy and moves revenue. Find what defensible real rates exist for tax deferred and secured on an asset, and propose a register row with a low, central and high.

## Decisions (author, 2026-11-22)
- No rate is chosen for its effect on WDT revenue or closure. The row records evidence; the author rules.
- 0.0 stays a labelled legacy value, not the default.

## Design
1. Candidates, UK first (say what is foreign): HMRC interest on late and deferred payments (including inheritance tax paid by instalments and the CGT-on-UK-property deferral), interest on student and other statutory deferrals, the gilt yield (real), the Green Book discount rate (D11) as a time-preference benchmark, mortgage and equity-release rates as the cost a household would face.
2. For each: quantity, number, years, nominal or real, who sets it, what it is a rate on, and whether it is a charge to the taxpayer or a return to the state. Keep the two apart.
3. Propose one register row (`inputs.md` format, columns as the other rows) with low, central and high, the **(J)** flag where a judgement is needed, and one line on what the model does with it. A real-zero case stays as the lower bound if the evidence supports it.
4. List what the author must rule: charged rate against state discount rate; whether the lien interest is revenue (it is, in the ledger receivable).

## Touches
`docs/research/134r-lien-deferral-rate.md` (new), this brief's progress block, `docs/agents/friction-log.md`. Proposed row in the note only (080r form); no register, code or manifest edits.

## Acceptance criteria
- Each candidate has quantity, number, years, real or nominal, and source link; numbers marked "read from a fetched page" unless checked against the primary.
- The proposed row is complete or says why no supportable range exists.
- `git diff --stat` limited to Touches.

## Out of scope
Changing any code or run; the heir's share; revenue effects.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready; not started
<!-- progress:end -->
