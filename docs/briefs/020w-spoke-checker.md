# 020: Spoke checker specification

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 017s, 018s, 019s, 021s).
- **Read:** `docs/restructure/template.md` (all sections), `docs/agents/reference/writing/` (style guide and prose rules), `docs/agents/writing.md`, `docs/model-v3/outputs.yml`, and `pipeline/check_wdt_format.py` (read to see what carries over). Nothing else need be opened.

## Goal
Specify the checker for spokes that replaces `check_wdt_format.py` for the new shape: every check, severity, input and an example pass and fail.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/checker.md`. Cover: front matter validation; part order; the word count and cap rules (template section 3); the objection block fields and status labels (section 5); typed-figure lint (section 4, rule 4); hook syntax and the R1 forward and reverse checks; caption lint F1 to F6 including the result-word list (section 6a); cross-reference form; the writing rules that can be automated (dashes, banned words, stray bullets and tables in prose) and the ones that stay manual. For each check say whether it fails the build or warns, and what the writing lane does when it fires. List what carries over from the old checker. For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/checker.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- Each template rule that can be checked has a check with a severity.
- Each check has one passing and one failing example.
- Manual-only rules are listed, with the reason.
- The old checker's checks are each marked carried over, changed or retired.
- `git diff --stat` shows only the Touches list.

## Out of scope
Building the pipeline, writing spoke or hub prose, editing `template.md`, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **State:** ready
<!-- progress:end -->
