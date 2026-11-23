# 146r: Top tail, scaling the opening stock of the top lines to the published top-1% range

Accessed 2026-11-23. Brief `docs/briefs/146r-gdp-growth-and-top-tail-evidence.md`. Evidence and design only; a stock sensitivity (`ast_low`, `ast_high`); tail behaviour stays unset and unchanged. Nothing is tuned to reach 0.50.

Status: done (block 2 of brief 146r).

## 1. Summary

- **The pack's own top 1% is already above the published range.** From its lines (D10b and the three Rich List tiers) the pack holds £3,121bn of £14,246bn: **21.9%**; the top 10% (D10a plus the top 1%) holds **43.5%**. The AST range is 14.4% to 16.5% (Advani, Summers and Tarrant 2025, pp. 1, 12). So `ast_low` and `ast_high` **lower** the top lines' stock (by £1,069bn and £770bn, 7.5% and 5.4% of the total); they do not add wealth to them, which the brief assumed.
- The two AST figures are **income-capitalisation** series for 2016-18 on individuals aged 20 and over (survey aggregates 14.4%, National Accounts aggregates 16.5%), not the WAS distribution; the authors' preferred Pareto-adjusted series (Appendix F.3) is **not held**. Evidence class `proxy`.
- **Recommended** (author rules): scale **D10b only**, keeping the Rich List tiers at their observed £784bn (I-D4f); offset **to D10a**, so total wealth and the top-decile share (43.5%) are unchanged and only the top-1% stock moves. Alternatives are listed (all four top-1% lines pro rata; pro rata over D1 to D10a, which lowers the top-decile share to 38.1% and 39.6%; no offset, which shrinks the total by 8.8% and 6.5%).
- Pension: the I-D1l ceiling (£0.386m an adult) holds. The reduced lines keep their capped pension and lose non-pension wealth (at least £1.7m an adult stays); the receiving line D10a gets non-pension wealth only (its pension stays £0.239m).
- The brief's "top-decile share starts at 0.41" is the survey-only share (40.7%, before the 5% missing wealth is added at the top); the pack's lines give 43.5%. Neither the scalings nor this note aim at 0.50.


## 2. The pack's own top-1% and top-decile shares

Computed by `top_tail_mapping.py` (command in section 6) from `build_base(pack, register, 0.44)`; the lines are D1 to D9, D10a, D10b, RL3, RL2, RL1 (`base.py`). Rows in `tail_current.csv`.

| Item | Value |
|---|---|
| Pack total after the missing-wealth addition (I-D4e, 5%) | £14,246.4bn |
| Top 1% (D10b + RL3 + RL2 + RL1) | £3,120.6bn = **21.905%** |
| Top 10% (D10a + top 1%) | **43.531%** |
| Survey total before the addition | £13,568.0bn |
| Top 1% of the survey total (I-D4d central, WAS as published) | 18.0% |
| Top 10% of the survey total (survey deciles, no addition) | 40.7% |
| Rich List inside the top 1% (I-D4f, 350 entries) | £784bn |
| Adults in the top 1% and top 10% | 1.00% and 10.00% |

How 21.9% arises: the tail construction (073c) adds the missing-wealth share at the top, so the top 1% is (18.0% + 5.0%) over 105.0% of the survey total. It sits inside the register range for I-D4d (14.4, 18.0, 23.0) near its high end. With I-D4e at its low value (0%) the pack's top 1% would be 18.0% by construction, still above 16.5%.


## 3. The AST range (page, flag)

`docs/research/data/129r/1-s2.0-S0014292125001266-main.pdf`, *Measuring top wealth shares in the UK*, European Economic Review 178 (2025) 105076; journal page = PDF page. Each figure is asserted on its page by the script. Rows in `tail_ast_evidence.csv`.

| Figure | Value | Page | Flag | Limit |
|---|---|---|---|---|
| Top 1% share, 2016-18, income capitalisation, survey aggregates | 14.4% | 1, 12; Fig. 3 (p. 13) | text, figure | individuals aged 20+; capitalised income; no Pareto adjustment |
| Same, National Accounts aggregates | 16.5% | 1, 12; Fig. 3 | text, figure | NA total £9.9tn against survey £14.2tn (p. 2) |
| NA minus survey top-1% share, 2006 to 2016-18 | 2.1 to 3.3 points | 12 | text | 2016-18 gap 2.1 |
| Wealth definition | market value net of debts incl. pensions; excludes durables, vehicles, unfunded DB (main results) | 2 | text | the pack's lines are adults of households, wealth shared equally inside a household |
| Preferred series (Pareto-adjusted) | not held | 5; Appendix F.3 | `unset` | data request; the appendix is not in the held PDF |
| Including unfunded DB lowers the top 1% share | size not held | 8; Appendix F.2 | `unset` | direction only |


## 4. Proposed scaling and offset rule, with alternatives

Two settings, `ast_low` (top-1% share 14.4%) and `ast_high` (16.5%), stock only; tail behaviour (saving, returns, pension accrual) stays `unset` and unchanged (brief). The target is a share of the pack total (£14,246bn), held fixed except in option 3. Full results are in `tail_scenarios.csv` (12 rows).

| Setting | Lines scaled | Offset | Wealth moved | Top 1% | Top 10% | Total vs pack | D10a an adult (£m) | D10b an adult (£m) |
|---|---|---|---|---|---|---|---|---|
| pack today | none | none | 0 | 21.9 | 43.5 | 1.000 | 0.657 | 4.489 |
| **ast_low, recommended** | D10b only (list fixed at £784bn) | to D10a | £1,069bn | 14.4 | 43.5 | 1.000 | 0.885 | 2.435 |
| ast_high, recommended | D10b only | to D10a | £770bn | 16.5 | 43.5 | 1.000 | 0.821 | 3.009 |
| ast_low, alt 1 | all four top-1% lines pro rata (the list tiers shrink) | to D10a | £1,069bn | 14.4 | 43.5 | 1.000 | 0.885 | 2.951 |
| ast_low, alt 2 | D10b only | pro rata over D1 to D10a | £1,069bn | 14.4 | 38.1 | 1.000 | 0.720 | 2.435 |
| ast_low, alt 3 | D10b only | none, total falls | £1,249bn | 14.4 | 38.1 | 0.912 | 0.657 | 2.089 |
| ast_high, alt 2 | D10b only | pro rata over D1 to D10a | £770bn | 16.5 | 39.6 | 1.000 | 0.703 | 3.009 |
| ast_high, alt 3 | D10b only | none, total falls | £922bn | 16.5 | 39.6 | 0.935 | 0.657 | 2.717 |

Why D10b only: the Rich List total is an observed figure (I-D4f), and D10b is the only top line without one, so it is the line the AST range can move. Why D10a: it changes two lines, keeps total wealth (so the wealth-to-GDP ratio and every denominator) and the top-decile share, and isolates the top-1% stock. Cost: it raises the 90th to 99th percentile line's wealth by 35% (ast_low) and 25% (ast_high), for which no source speaks.

**Pension and the I-D1l ceiling.** Reduced lines keep their pension balance (capped at £0.386m an adult, I-D1l); wealth is removed from the non-pension classes pro rata to D10's mix, and the smallest remaining non-pension wealth in any reduced line is £1.7m an adult. D10a receives non-pension wealth only: its pension stays £0.239m. The ceiling therefore holds in every row. `line_state` builds class balances from wealth times D10's class shares, so a code brief needs a rule to apply the adjustment after the composition step, not before.

**Evidence classes.** The two settings are `proxy` (a different method, vintage and unit; the preferred series is not held); the scalings and offsets are `scenario`.


## 5. Unset, challenge note, open rulings

**Unset:** the AST preferred (Pareto-adjusted) top-1% share (Appendix F.3, not held); the effect of unfunded DB on the top share (size); any source for the wealth of the 90th to 99th percentile that would support the offset to D10a; tail behaviour (saving, returns, pension accrual by tail line); a top-1% figure on the Round 8 basis.

**Challenge.**
1. **Direction.** The held range is below the pack, so the sensitivity lowers the top; there is no held published figure above 21.9% to scale up to except the register's I-D4d high (23.0%, WAS plus Rich List and Pareto adjustment), which is on a different total and is not used.
2. **Method.** AST's 14.4 and 16.5 come from capitalised income tax data, not the WAS the pack is built on, for 2016-18 and for individuals. Household-level shares and individual-level shares differ, and the pack's tail already adds the missing wealth at the top (I-D4e) and the Rich List; applying AST on top of that would mix two corrections.
3. **Rich List.** Keeping the list at £784bn assumes the observed total is right and the shortfall is in D10b; scaling all four lines (alt 1) shrinks an observed figure.
4. **Offset.** No source says where the displaced wealth goes; D10a is a convenience, pro rata (alt 2) lowers the top-decile share and moves it from 43.5% to 38.1% or 39.6%, further from the observed half. That is reported, not a reason to choose; nothing here is tuned to 0.50 and nothing to WDT revenue or closure.
5. **Total.** Option 3 changes total wealth and so every ratio on GDP (M1, M2, omega); it is listed because the AST figure is a share of its own aggregate, not recommended.

**Open rulings for the author.**
1. Accept a downward stock sensitivity for the top 1% (the pack is above the AST range), or ask for a different reference (for example the Appendix F.3 series, or the register's I-D4d low).
2. Lines scaled: D10b only with the list fixed (recommended), or all four top-1% lines.
3. Offset: to D10a only (recommended), pro rata over D1 to D10a, or none.
4. Whether `ast_low` and `ast_high` are also run with I-D4e at 0%, which lowers the pack's top 1% to 18.0% by itself.


## 6. Reproduction

`python -I docs/research/data/146r/top_tail_mapping.py` from the repo root (needs `pdftotext`; reads the pack, the register and `runner/arm.line_state` read only). It asserts the AST figures on their pages, computes the pack's top-1% and top-decile shares (21.905%, 43.531%), builds the 12 scenario rows and checks that the total is held, the Rich List tiers and D10b stay positive, and the non-pension wealth of every reduced top line stays non-negative. It writes `tail_current.csv` (9 rows), `tail_ast_evidence.csv` (7) and `tail_scenarios.csv` (12) and prints one `ok:` line; it exits 1 on any failed check. Check: `python -I pipeline/check_agent_docs.py`.

