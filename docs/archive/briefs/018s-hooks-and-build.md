# 018: Hook resolution, data interface and the Data block

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 013g stage C (merged); part of 013g stage D. Runs in parallel with 2 (with 017s, 019s, 020w, 021s).
- **Read:** `docs/restructure/template.md` (sections 4, 6 and 6a), `docs/model-v3/outputs.yml`, `docs/model-v3/metrics.md` (summary forms and reading rules), `docs/model-v3/inputs.md` (row format), and `pipeline/` file names. Nothing else need be opened.

## Goal
Design how a hook becomes a value at build time: the file the model writes, the resolver, draft and release builds, and the generated Data block with its CSV reference tables.

## Decisions (author, 2026-11-17)
The spoke template (`docs/restructure/template.md`) is approved, including section 6a (figures and tables). Hub and spokes: `docs/restructure/map.md` section 7. The data gate holds: no spoke prose until the data is final. This brief designs; it builds nothing.

## Design
One file only: `docs/restructure/site/hooks.md`. Cover: the output data file (a schema with one entry per output id holding p10, mean, p90 or a point, per schedule, horizon and `by` key, with unit and rounding set by the metric register); where it lives and who writes it (the v3 run script, built later); how `{{i:}}` reads the input register (a generated data file from `inputs.md`) and `{{lit:}}` reads the reference database; how `{{ref:}}` numbers figures; the draft build (unresolved hooks render as `[[...]]`) and the release build (fails on any unresolved hook); the Data block generator, row by row from template section 6; reference tables as HTML and CSV; run metadata (manifest version, country pack, run date). Give one worked example from hook to rendered value to Data block row. For every point where the document needs a decision it does not own, write a numbered question with a proposed answer; do not guess. The guru merges the sibling files into `docs/restructure/site.md` (shared file; `brief-template.md`, Splitting).

## Touches
New `docs/restructure/site/hooks.md` and this brief's progress block. Nothing in `source/`, `pipeline/`, `site/`, `registry/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- The data file schema is complete enough to write a validator, and is stated for the three summary forms in `outputs.yml`.
- Every hook form of template section 4 has a resolution rule and an error case.
- The worked example round-trips: hook, data entry, rendered text, Data block row.
- Where the schema needs a field the manifest lacks, it is listed as a question.
- `git diff --stat` shows only the Touches list.

## Out of scope
Building the pipeline, writing spoke or hub prose, editing `template.md`, choosing values.

## Open questions
The implementer asks rather than guesses.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/restructure/site/hooks.md` written (data file schema and validator rules, hook resolution and error codes for `o`, `i`, `ref`, `lit`, draft and release builds, Data block generator, HTML and CSV tables, run metadata, worked example, 18 numbered questions with proposed answers).
- **Next:** the guru reviews the 18 questions with the author (Q1 to Q6 and Q17 to Q18 are manifest gaps) and merges the file into `docs/restructure/site.md`.
- **State:** done, NEEDS THE AUTHOR (open questions remain; not merged)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 018s, hook resolution, data interface and the Data block
- Files changed: docs/restructure/site/hooks.md (new, the design); docs/briefs/018s-hooks-and-build.md (this progress block)
- What is different now: the hook-to-value path is specified end to end, from the manifest and run file to the rendered value, the Data block row and the CSV. Nothing is built.
- New or changed interfaces: none built. Proposed: output data file schema wdt-outputs/1, registry/inputs.json (generated from inputs.md), registry/lit-figures.yml, WDT_MODE=draft|release, pipeline/hooks.py, data_block.py, build_inputs.py.
- Acceptance criteria:
  - Data file schema complete enough for a validator, stated for the three forms: met (section 3, rules V1 to V12). Note: outputs.yml entries use two forms (19 p10_mean_p90, 2 point_and_range); the third is the level 2 block named in the manifest header. Q5 asks whether it is hookable.
  - Every hook form of template section 4 has a resolution rule and an error case: met (sections 4.2 to 4.5, codes in 4.7).
  - Worked example round-trips: met (section 10); the parser regex and the example were run in a scratch script and all template examples parse. Example values are placeholders, not results.
  - Fields the manifest lacks are listed as questions: met (Q1 to Q6, Q17, Q18).
  - git diff --stat shows only the Touches list: met, see Verification.
- Deviations from the brief: the template's single `#BAND` field is extended to `#key:value,key:value` (Q3), and its example `wealth_band:top` has no vocabulary in the register. Both are proposals in questions; template.md is not edited.
- Risks / follow-ups: template 6a writes `Table F5.1` against `F-<spoke>-<n>` elsewhere (Q13). The template's `inputs: [W_min]` has no register row (Q7). The figure example plots OP6 over 100 years but P6 is defined at four years (Q4).
- Verification: hook regex and worked-example script run (scratchpad, not committed): all pass. No em dashes in the file. Site build not run: the diff touches no site file.
- Overview sections likely needing an update: none until the guru merges site.md; section 2 directory map gains docs/restructure/site/.
- Commit / branch: see git log, branch brief/018-hooks-and-build. NEEDS THE AUTHOR: open questions remain, so the auto-merge rule does not apply.
```
