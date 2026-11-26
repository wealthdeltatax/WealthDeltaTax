# 146: Evidence and mapping for two scenario axes: per-path GDP growth, and the top tail

- **Status:** ready (research only; can start now; feeds 147c and 148c)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 128c (merged), 129r (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-paths.md` (what varies per path; GDP growth is fixed) and `docs/research/129r-was-access-audit.md` (the P5 top-tail row: Advani, Summers and Tarrant 2025, top-1% share 14.4% to 16.5% across sources); (2) `docs/agents/research.md`. Later: `model_v3/core/revenue.py` (`gdp_growth`; read only) and the return generator rows in `docs/model-v3/inputs.md` (I-D1a to I-D1g); the held JST series in the pack (read only); `docs/model-v3/household-arm-validation.md` (BF-13); the tail lines (D10a, D10b, RL3 to RL1) and I-D1l in `docs/model-v3/inputs.md` and `household-arm-account.md`; the AST PDF in `docs/research/data/129r/` through `pipeline/to_markdown.py`, only the pages you cite.

## Goal
(1) **Per-path GDP growth.** Every household-arm path has the same real GDP growth (0.0157 a year), so fund-to-GDP ratios, burden shares and M15a/b carry no growth risk. Say what a labelled per-path growth axis would need. (2) **Top tail.** The pack has no top-1% row; the tail lines carry D10's mix with a capped pension and the top-decile share starts at 0.41 against 0.50. Say how the opening stock of the top lines would be scaled to the published top-1% range. Evidence and design only.

## Decisions (author, 2026-11-23)
- GDP: a scenario axis labelled "growth risk only", off by default; same machinery as the market-return paths (128c). Parameters (growth spread, persistence, correlation with the market return) come from the held JST data or the register, with page or table and flag; where the pack has no such row, mark it `unset` and list the labelled options (independent; the historic correlation) for the author to rule on; do not choose silently. Say which model quantities scale with the path (income, saving, the GDP index in M1, P6 and M15) and which stay fixed.
- Top tail: a **stock** sensitivity, two settings `ast_low` (top-1% share 14.4%) and `ast_high` (16.5%); tail behaviour (saving, returns, pension accrual) stays `unset` and unchanged. Propose which lines are scaled, how the added wealth is offset in the rest of the distribution so total wealth is unchanged (or the alternative), and show the pack's current top-1% share from its own lines. Added wealth is non-pension (labelled); the I-D1l ceiling holds. If two readings are plausible, list both; the author rules. Nothing is tuned to hit 0.50.

## Blocks (one push each; `docs/agents/research.md`)
- **Block 0:** progress block pushed.
- **Block 1: GDP growth.** `docs/research/146r-gdp-growth-process.md` with a small CSV: the proposed deviation process and its parameters (page or table, flag, class), which quantities scale, the correlation options and what is `unset`. Push.
- **Block 2: top tail.** `docs/research/146r-top-tail-mapping.md` with a small CSV: the pack's current top-1% and top-decile shares, the AST range (page, flag), the proposed scaling for `ast_low` and `ast_high`, the offset rule and the alternatives. Push.
- **Block 3:** change report with the open rulings listed for the author; push; stop.
**Stop rule.** No model, register or manifest change. After three blocks or a quarter of the budget left, push and list the rest.

## Touches
New: `docs/research/146r-*.md`, `docs/research/data/146r/`. Read-only use of `model_v3/` and the pack. Not the register, the manifest or the pack.

## Acceptance criteria
- Every figure has a page and flag; each parameter or scaling has an evidence class and challenge note; `unset` parts and open rulings listed.
- The top-1% share of the pack's own lines is computed and stated, with the command.
- Nothing outside `docs/research/` changes; `python -I pipeline/check_agent_docs.py` exits 0.

## Out of scope
Any code, any register row, withdrawal and saving (145r), tail behaviour, any headline number.

## Implementation notes
Change report
- Task: brief 146r, evidence and mapping for two scenario axes (per-path GDP growth; the top tail)
- Files changed: `docs/research/146r-gdp-growth-process.md`, `docs/research/146r-top-tail-mapping.md` (notes); `docs/research/data/146r/` (`gdp_process.py`, `gdp_process.csv`, `gdp_illustration.csv`, `top_tail_mapping.py`, `tail_current.csv`, `tail_ast_evidence.csv`, `tail_scenarios.csv`); this brief's progress block.
- What is different now: (1) GDP growth: the kernel already takes a per-path growth array; the pack's JST series support a labelled AR(1) deviation around the fixed 1.5704% (SD 2.68 full sample or 1.93 postwar, lag-1 0.28, correlation with the market return 0.37, 95% interval 0.20 to 0.51), with correlation options A (independent) and B (historic) both listed. (2) Top tail: the pack's own top 1% is 21.9% and its top 10% 43.5% (computed from its lines), above the AST range 14.4% to 16.5%, so `ast_low` and `ast_high` lower the top stock (£1,069bn and £770bn) rather than add to it; recommended D10b only, Rich List fixed, offset to D10a; alternatives listed. The I-D1l ceiling holds in every row.
- New or changed interfaces: none.
- Acceptance criteria: figures have page and flag, parameters an evidence class and challenge, unset parts and open rulings listed (met; AST figures asserted on their pages, GDP statistics computed from the pack, mean checked to the model constant); top-1% share of the pack's own lines computed and stated with the command (met); nothing outside `docs/research/` and this brief changes, check exits 0 (met).
- Deviations from the brief: the brief assumed the AST range was above the pack and the offset would be for added wealth; it is below, so the settings reduce the top stock and the offset receives wealth. Stated in the note. The brief's "top-decile share 0.41" is the survey-only share; the pack's lines give 43.5%.
- Risks / follow-ups: AST's 14.4 and 16.5 are income-capitalisation figures for 2016-18 on individuals; the preferred Pareto-adjusted series (Appendix F.3) is not held (data request). GDP process from one country's 117 usable years, ends 2019.
- Open rulings for the author: GDP: correlation A or B; marginal SD (full sample or postwar); household income following the path or staying on the constant; register rows or arm-dict constants. Top tail: accept a downward sensitivity or choose another reference; lines scaled; offset; whether to also run with I-D4e at 0%.
- Instruction friction: none new.
- Verification: `gdp_process.py` ok (17 rows), `top_tail_mapping.py` ok (12 scenario rows), `check_agent_docs.py` rc 0. No model run.
- Overview sections likely needing an update: none until the author rules.
- Commit / branch: brief/146-gdp-growth-and-top-tail-evidence; not merged, per the brief (stop after the push, rulings pending).
<!-- progress:start -->
- **Done:** block 0 (note skeletons); block 1 GDP growth (`146r-gdp-growth-process.md`, `gdp_process.py`); block 2 top tail (`146r-top-tail-mapping.md`, `top_tail_mapping.py`)
- **Next:** author rules on the open rulings in the change report
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/146-gdp-growth-and-top-tail-evidence origin/brief/146-gdp-growth-and-top-tail-evidence`
- **State:** done
<!-- progress:end -->
