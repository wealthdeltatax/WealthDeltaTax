# 033: Code: spoke gate checker (order.md B17)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 029s and 030c for real inputs (soft: build against the formats in the Read files and fixtures; wire to the real files when they land)
- **Read:** `docs/restructure/order.md` sections 4 and 6.5; `docs/restructure/site.md` sections 3 and 6; `docs/restructure/site/hooks.md` section 9 (run metadata); `docs/model-v3/outputs.yml`; `docs/model-v3/inputs.md` (the `(J)` flag); `docs/model-v3/judgement-decisions.md`; `docs/agents/code.md`.

## Goal
Make "the data gate is open" a command, not an opinion: one script that tests the five gate checks for a page or for all 26 units.

## Decisions (author, 2026-11-17)
`docs/restructure/site.md` is approved with its eight answers (drafts under `/draft/`, hub Data block, ADOPT, PILOT and HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding before the gate, standalones move after the gate). The data gate holds: no spoke or hub prose. This brief builds on fixtures and delivers without the model data. It is one of the first parallel set (029s, 030c, 031s, 032r, 033c, 034c); the Touches lists do not overlap. The gate is G1 to G5 of `order.md` 4.1; the page needs table is `order.md` 4.2 (default: every page waits for G1 to G5, author, 2026-11-17).

## Design
`python pipeline/check_gate.py --page <ID>` prints G1 to G5 for the page with pass or fail and a reason and exits 0 only if the page's needs are met; `--all` prints the table of `order.md` 4.2 for the 26 units. Implement the commands of `order.md` 4.1 as written: G1 files and the acceptance command named in `acceptance.md`; G2 the `outputs.json` run fields and hashes and the validator; G3 the `(J)` set equals the ids in `judgement-decisions.md` and each has a dated decision; G4 per-page outputs and inputs complete, with R1 both ways against front matter; G5 the build briefs merged and the tests pass. Needs per page come from a small table in the script's data file, not hard-coded in prose. Tests on fixtures: gate closed with the repository as it is today (G1, G2, G3 fail), and open for a synthetic complete fixture.

## Touches
`pipeline/check_gate.py` (new), `tests/gate/` (new), this brief's progress block. Nothing else.

## Acceptance criteria
- With today's repository, `--all` exits non-zero and names the failing checks with reasons.
- A synthetic fixture with every input present exits 0.
- G3 counts 87 flagged rows today and reports them as pending.
- `git diff --stat` shows only the Touches list.

## Checks to run
`pytest tests/gate`; run `--all` on the repository and read the reasons.

## Out of scope
Building the data files, the model, the resolver, writing prose.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
