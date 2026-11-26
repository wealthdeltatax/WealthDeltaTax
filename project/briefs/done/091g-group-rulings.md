# 091g: guru rulings after the four stopped output-group briefs

- **Status:** done, merged 2026-11-20
- **Author/date:** K. Ogata with the guru, 2026-11-20

Record of the work, written after the fact (no brief was issued first). 085c to 088c each stopped at its rule. Done by the guru:
- Register rows **I-T3q** (VAT standard rate 20%, statute, source ST11 gov.uk VAT rates, not a judgement row) and **I-D14h** (reference entry wealth of a declaring holder, £20m, v2 `V0_m`, `(J)`): register 293 rows, 108 `(J)`.
- Manifest **A12** (`stage-A12-group-outputs-2026-11-20`): O1d and OP5 carry six taxes named as the core (`cgt`, `iht`, `stamp_duties`); OP4 is the ratio only; OR1 single-horizon; DH1a (`series`: wid_top1, wid_top10) and DH1b (`line`: the 16 pack lines) once-not-per-schedule single cells, DH1a without wealth to GDP and DH1b without groups; OT1 cells by input and headline per named schedule (point 0, lo and hi the swings), single horizon.
- `tests/data/make_fixture.py` numbers are now a hash of the cell key (they used to be a counter, so any new output shifted every later pin; hooks pins re-set once).
- Budgets: `groups.py` 20 to 40, `sweeps.py` 300 to 280 (`architecture.md` 6.1).
- Brief **092c** (group interface) written; rulings added to 085c to 088c.
- Cause: the 084c interface was specified without an input audit of what the groups read; the audit rule is now in `guru.md`.
