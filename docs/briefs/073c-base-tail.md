# 073: Give the base a tail: top lines from the Rich List and a Pareto split

- **Status:** done (072g merged 2026-11-19)
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** 051c (merged), 072g (tail rows)
- **Read:** `model_v3/core/base.py` and `tests/model_v3/test_base.py`; the 052c report on branch `brief/052-revenue` (Gotchas 1; `git show origin/brief/052-revenue:docs/briefs/052c-v3-7-revenue-fund-identity.md`); `model_v2/RATES/rates_core.py` `_build_advani` (lines 408 to 599) as specification only (not ported or imported); `docs/model-v3/tornado.md` section 4 (the effective rate 24.5% for v2-like inputs); `docs/model-v3/architecture.md` 2.3 and the tests row for `base`; register rows I-D4d, I-D4e, I-D4f, I-W5c, I-W7a, I-W7b and the rows 072g added.

## Goal
`build_base` carries the top of the wealth distribution as lines fine enough for the schedule to reach billionaires: the top 1% is replaced by the part of the top 1% below the Rich List and three Rich List tiers, split by a Pareto tail. Without it v3 reproduces 3.5% of GDP where v2 gives 7.34% (effective rate 10.2% against 24.5%).

## Decisions (author, 2026-11-19)
- Adopt v2's construction: survey total plus the 5% missing wealth (I-D4e), the top 1% share (I-D4d), the Rich List total (I-D4f) as a named tier of 350 members split at the tier cuts (072g) with Pareto alpha (072g), and the remainder of the top 1% below the list as its own line.
- **The tail builder takes its constants as arguments**, defaulting to the register: so the identity test I1 can pass v2's own constants (2017/18 Rich List, `s1_survey` 0.18, `s10_survey` 0.51, 5% extra, 1,000 entries, £700bn, entry £100m, alpha 1.5, cuts 1%, 10%, 100%) and the model passes the register's. No v2 constant is copied into `base.py` as a default.
- The deciles below D10 and the D10a line (90th to 99th percentile) stay as 051c built them; D10b (top 1%) is replaced by the tail lines. The count of lines changes (about 14); nothing downstream may hard-code 11: report any place that does.
- The Rich List overlaps the survey (I-D4f: "not additive"): follow v2's treatment of the overlap and say how it is written.

## Design
1. `core/base.py`: add `tail(...)` (or extend `build_base`) as above; budget: base.py stays at or under 380 lines (it is 122 now).
2. Tests (B6 tail): the tier members sum to 350 and the tiers to the Rich List total as v2 adds it; the top 1% share of the base equals the register's I-D4d central; total wealth equals the survey total times 1.05; the construction is passed v2's constants in one test and the result reproduces v2's own tier sums computed by hand from the toml values (hand arithmetic written into the test, v2 not run); B1 to B5 keep passing with the new line count.
3. Report the new line labels, counts, and the effective-rate proxy the agent can compute without the kernel (wealth-weighted share above the schedule's bend) so the guru can see the change before 052c reruns.
4. Do not edit `core/revenue.py` or the 052c branch: 052c continues on its own branch afterwards.

## Touches
`model_v3/core/base.py`, `tests/model_v3/test_base.py`, this brief's progress block. If other `core/` files hard-code 11 lines, stop and report to the guru.

## Acceptance criteria
- `pytest tests/model_v3 -q` passes (all existing tests with the new line count); B6 added.
- No default constant from v2 in `base.py` (grep for 0.18, 0.51, 700, 1000 in the file).
- `git diff --stat` limited to Touches.

## Checks to run
`pytest tests/model_v3 -q`, `pytest tests/data -q`, `pytest tests/gate -q` (separate commands).

## Out of scope
The kernel, revenue, the pack, the register (072g), I1 to I3 (052c).

## Open questions
Ask rather than guess: if `_build_advani` uses an input the register still lacks after 072g, name it.

## Implementation notes
<!-- progress:start -->
- **Done:** `core/base.py` (149 lines, budget 380) gains `tail(total_bn, d10_bn, s1, extra, n, list_bn, alpha, cuts)`, every constant an argument; `build_base` passes the register's (I-D4d, I-D4e, I-D4f, I-D4i, I-D4j, I-D4k, I-D4l). The top 1% line is replaced by D10b and three tiers. No v2 constant in `base.py` (grep for 0.18, 0.51, 700, 1000: none; also a test). The wealth_tail table and `_tail_ratio` are no longer used by the base (removed).
- **Lines (14):** D1 to D9, D10a, D10b (top 1% below the list), RL3, RL2, RL1 (RL1 richest). At the register's central values: D10a 3,081.0bn; D10b 2,336.6bn (520,576 adults); RL3 420.1bn (315 members), RL2 187.3bn (31), RL1 176.6bn (4); total 14,246.4bn = 13,568 x 1.05; wealth/GDP 6.44.
- **Overlap:** as v2: the list is inside the top 1%. top 1% after the addition = s1 x survey total + extra x survey total = 3,120.6bn; D10b = that less the list (784bn). Nothing is added for the list itself.
- **Effective-rate proxy (no kernel):** wealth-weighted marginal rate of the `logistic_ln` schedule (tau_0 0.04, ratio 0.5, W_min 0.15m), all lines, before the 11-line base and after: tau_m 0.9, k_ln 1: 16.3% to 21.1%; tau_m 0.9, k_ln 2: 35.3% to 37.9%; tau_m 0.7, k_ln 1: 15.1% to 18.6%. Wealth above W_min: 90.2% to 90.7%. Top 1% share of the base: 15.2% to 21.9%. This is a marginal-rate proxy, not the effective rate on gains (tornado.md section 4's 24.5%); 052c measures that.
- **Next:** 052c continues on its own branch.
- **Decisions:** (1) I-D4d is a share of the SURVEY total, as v2's `s1_survey` is; the test says the base's top 1% less the added wealth, over the survey total, equals I-D4d central. The top 1% share of the new total is 21.9%. (2) D10a is now D10 less the survey top 1% (v2's (s10 - s1) x total), not D10 x (1 - WID ratio) as 051c had it; both lines had to change for the partition, I-D4d and the 1.05 total to hold together. Old D10a 3,462.9bn, new 3,081.0bn; old D10b 2,060.3bn against the new top 1% 3,120.6bn. (3) `wealth_to_gdp` is the total with the missing wealth over GDP (6.44, v2's calibrate); it was 5.94. (4) Tier cuts are `round(fraction x n)` (Python rounding): 1% of 350 gives 4, 10% gives 35, so the tiers hold 4, 31 and 315 members. (5) The named-list name is not in code (R11 flags it); the code and docstring say "named list".
- **Gotchas:** B1 had to change: the wealth sum is the pack total x 1.05, the split-by-WID-ratio assertion is gone, wealth_to_gdp includes the addition; B3's shape is `len(LABELS)`. Nothing outside `base.py` and its test hard-codes 11 lines (grep of `model_v3/`). All tail lines take the D10 band's income and liquid assets, as D10b did (one register income for the whole top decile: richer lines carry the same income per adult).
- **Resume:** nothing.
- **Not run:** nothing named was skipped.
- **State:** done; merged to main. Tests: tests/model_v3 142 passed, tests/data 84, tests/gate 17.
<!-- progress:end -->
