# 134: Evidence and a register row for the lien deferral rate

- **Status:** research complete; awaiting author ruling
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
- **Done:** `docs/research/134r-lien-deferral-rate.md` written with 11 UK official sources, the HMRC IHT and CGT comparators, HMT's 2% real risk-free benchmark and 3% STPR, nominal student-loan and mortgage comparators, and a proposed I-D15a row (0 / 2 / 3% real, all (J)).
- **Next:** author rules on pricing principle (2% risk-free financing benchmark or 3% STPR), whether 0% remains the policy floor, and whether the same rate applies to Route B and the household pension lien.
- **Corrections to conversational answer:** 4% is not retained as the proposed high; no primary source supported it. The earlier lifetime-mortgage figure is omitted because it was not verified. CGT statutory instalment/deferment provisions are distinguished from ordinary UK residential-property CGT, normally payable within 60 days.
- **Not run:** no code or model run, as required by scope.
- **State:** note pushed; brief awaits author ruling
<!-- progress:end -->

```
Change report
- Task: 134r, evidence and a register row for the lien deferral rate
- Files changed: `docs/research/134r-lien-deferral-rate.md` (new); `docs/briefs/134r-lien-deferral-rate.md` (progress block)
- What is different now: sourced UK comparators and a provisional row proposal are recorded; the note distinguishes a contractual lien charge, the state's real risk-free financing benchmark and social time preference
- New or changed interfaces: none
- Acceptance criteria: candidate quantities, rates, dates/bases and source links recorded; proposed row complete with (J) flags; no code or model changes
- Deviations from the brief: no friction-log entry; the research workflow itself did not fail. The brief's request to append friction applies only when an instruction, workflow or tool failed.
- Risks / follow-ups: I-D15a is a placeholder pending register namespace check and author approval; 0 / 2 / 3% is judgemental; the 2% benchmark is not a directly observed price for a pension-secured WDT lien
- Verification: primary GOV.UK/HMT/BoE/DMO pages read on 2026-11-22; no model suites run because this is a documentation-only research task
- Commit / branch: `brief/134`
```
