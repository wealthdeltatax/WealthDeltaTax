# 185: Precedents for the SWF design (pilot for the OpenAI agent)

- **Status:** ready
- **Agent:** openai
- **Needs:** none
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-27
- **Depends on:** none (the agent's first brief; also a test of the inbox and the note format)
- **Read:** `project/agents/agent-openai.md` (rules and note header), `project/inbox/README.md`, then in `project/decisions.md` the entries of 2026-11-25 on the SWF terms (short reserve = refund reserve, long reserve = stabiliser, the fund capped at short plus long, excess accelerates tax replacement, replacement time as headline)

## Goal
Find how real funds and reserves are sized, capped, drawn down and protected, so the author can judge the SWF redesign against precedent. Ranges and mechanisms, not a recommendation. Public sources only.

## Questions (one note per two questions; deliverable is notes in `project/inbox/from-openai/`)
1. **Size caps and release of the excess.** Does any sovereign, stabilisation or reserve fund hold a stated maximum size and release what is above it (to spending, tax cuts or a successor fund)? Candidates: Alberta Heritage Fund, Chile's Economic and Social Stabilization Fund and Pension Reserve Fund, Norway's fiscal rule (expected real return, the handling rule), Alaska Permanent Fund (POMV and the Constitutional Budget Reserve), New Zealand Super Fund, Botswana Pula Fund. For each: the rule, the size or ratio, when it was set, whether it has been changed or breached.
2. **Reserves sized as a multiple of the outflow they back.** Months or years of expected outflow held as a buffer (a "short reserve" for refunds): deposit insurance funds (US DIF designated reserve ratio, other countries), pension protection funds, Social Security trust fund ratio, Canada Pension Plan reserve, unemployment insurance funds. For each: how the target is set, the multiple, what happens when it is breached, and whether claims are certain (a refund) or contingent.
3. **Rule-based drawdown and smoothing.** How stabilisation funds smooth income: rule-based (structural balance rules, 3-year or 5-year averages, a percentage of market value) versus discretionary; evidence on which kept the fund alive through shocks (IMF and OECD reviews, Davis et al., Bauer, Ossowski, Segura-Ubiergo). Our design draws the long reserve to cover retired taxes and uses a smoothed trigger; give the closest precedents.
4. **Political-economy protection.** What made funds hard to raid or reverse (constitutional entrenchment, dividends to citizens, independent management, legal ring-fencing) and what failed (examples of funds drained, merged or closed). The author's aim is a fund that becomes essential to the economy so reversal or capture is unlikely: list the mechanisms with their track record.

## Output
Two or three notes, header as in the guide (`type: web-research`, `in-reply-to: 185r`), each answering its questions: a table per question (fund, rule, figure with flag `reported`/`derived`/`estimated`, source with date read), what is weak or conflicting, and a "relevance to our design" paragraph (one per question) that says what it suggests as a **range or an option to test**, not a choice. No bibliography changes: list proposed references at the end.

## Acceptance criteria
- Every figure has a URL, the date read and the page or table, and a flag.
- Funds named in the candidates are covered or the note says why one is missing.
- Each "relevance" paragraph names the SWF term it bears on (short reserve, long reserve, cap, excess release, trigger).
- No claim of having run or tested anything; `verified` is `unverified` for web claims.

## Out of scope
Recommending the design, UK-specific fiscal data (held in the repo), anything in the model.

## Open questions
If a fund's rule cannot be found from a primary source, say so; do not fill from memory.

## Implementation notes
<!-- progress:start -->
- **Done:** nothing yet.
- **Next:** read the guide, then questions 1 and 2.
<!-- progress:end -->

## Change report
(The agent writes a short last note, `type: discussion`, saying what it did and did not cover.)
