# Site design: hook resolution, data interface and the Data block

> **Ids (author, 2026-11-17).** Spoke shortcodes (`docs/restructure/shortcodes.md`) are the page ids, URLs, front-matter `spoke:` values and figure and table ids. Where this file still writes `S1` to `S12`, read it through `docs/restructure/ids-map.md`; the S numbers are planning labels only.

> **Questions.** All proposed answers in this file's question section were accepted by the author on 2026-11-17 (nothing else reads `site-index.json`), except where `ids-map.md` overrides the S ids. Guru follow-through done the same day: `outputs.yml` carries `unit`, `decimals`, `horizons`, `by` maps and `series` (hooks Q1 to Q4); the template's table label is `F-<spoke>-<n>` and its example is an output the spoke owns (hooks Q13, checker Q14 and Q17).

Brief 018s, part of 013g stage D. Status: design draft for the guru; the guru merges it with the sibling files into `docs/restructure/site.md`. Design only: nothing here is built, no value is chosen, and every number in the worked example (section 10) is a placeholder, not a model result.

Read: `docs/restructure/template.md` (sections 4, 6, 6a), `docs/model-v3/outputs.yml`, `metrics.md`, `inputs.md`, and the file names in `pipeline/`. Where this design needs something the manifest, template or register does not hold, it is a numbered question in section 11 with a proposed answer. The text says "proposed" wherever a rule depends on a question.

## 1. What this file fixes

| Area | Fixed here | Left to a question |
|---|---|---|
| Output data file | schema, validation rules, three summary forms | file name and commit policy (Q10), fields the manifest lacks (Q1 to Q6) |
| Hooks `o`, `i`, `ref`, `lit` | resolution order, formatting, error cases | input naming and display (Q7, Q8), literature figures (Q9) |
| Builds | draft and release behaviour | severity of two checks in draft (Q11), who marks data final (Q12) |
| Data block | row-by-row generator, HTML and CSV tables, run metadata | link targets (Q14), reading note location (Q15), number style (Q16) |

## 2. Pieces and build order

| Piece | Status | Writer | Reader |
|---|---|---|---|
| `docs/model-v3/outputs.yml` (manifest) | exists | author, guru | resolver, validator, spoke checker |
| `docs/model-v3/inputs.md` | exists | research lane | `pipeline/build_inputs.py` |
| `registry/inputs.json` | new, generated, never edited | `build_inputs.py` | resolver, and the v3 run (so the run and the page read one file) |
| Output data file | new, written by the v3 run script (built later) | model | resolver, Data block generator |
| `registry/lit-figures.yml` | new, hand-maintained (Q9) | research lane | resolver |
| `registry/references.bib`, `internal.json` | exist | research lane | resolver (`lit`), bibliography |
| `pipeline/hooks.py` | new | web | parser and resolver, also imported by the spoke checker |
| `pipeline/data_block.py` | new | web | Data block, reference tables, CSV |
| `_build/data/csv/<table-id>.csv`, `_build/hooks-report.json` | new, generated | `data_block.py`, `hooks.py` | site, author |

The existing rule holds: nothing in `source/` is touched, and all output goes to `_build/`, regenerated each run.

Order inside the site build, after the preprocess steps that read the registry and before Quarto renders:

1. `build_inputs.py`: parse the register tables to `registry/inputs.json`.
2. Load the manifest, `inputs.json`, `lit-figures.yml`, `references.json`, and the output data file if one exists.
3. Validate the output data file against the manifest (section 3.3). In draft mode a missing file is allowed and every `o` hook is unresolved; in release mode it is an error.
4. For each spoke file: read front matter, expand hooks (section 4), expand figure blocks (section 5), append the Data block (section 7), write `_build/<spoke>.qmd`.
5. After all spokes: run the reverse R1 check, write `_build/hooks-report.json` (counts of hooks by outcome, unresolved list, warnings), apply the mode's failure rule (section 6).

## 3. The output data file

Format: JSON, UTF-8, one file per run. Proposed name and location in Q10. Values are stored in the unit the manifest declares (Q1) and are never rescaled by the resolver: a value of `0.22` for a `pct` output means 0.22 percent.

### 3.1 Top level

| Field | Type | Rule |
|---|---|---|
| `schema` | string | `wdt-outputs/1`; the validator rejects any other value |
| `run` | object | section 9 |
| `outputs` | object | keys are output ids from the manifest; every key must exist there; a manifest id with no key is allowed only in a file whose `run.status` is `provisional` |
| `level2` | object, optional | tornado and parameter-ignorance results, reported apart from `outputs` (form C below, Q5) |

### 3.2 One output entry

```json
"O2": {
  "summary": "p10_mean_p90",
  "cells": [ { "schedule": "S_central", "horizon": "short",
               "by": {"wealth_band": "D10"},
               "p10": 0.11, "mean": 0.22, "p90": 0.33 } ]
}
```

| Field | Type | Rule |
|---|---|---|
| `summary` | string | equals the manifest `summary` for this id |
| `cells` | array | one object per combination of the dimensions below; no two cells share a key |
| `series` | array, optional | on a cell: annual points for a line figure, `{"t": 10, "p10": .., "mean": .., "p90": ..}` (Q4) |

A cell's key is `(schedule, horizon, by)`. `schedule` is one of the manifest `schedules`. `horizon` is one of the manifest `horizons`, or `single` for an output the manifest declares has no horizon dimension (Q2). `by` is an object whose keys are exactly the output's `by` keys, each with a value from that key's vocabulary (Q3); `{}` for an output with none. Under the proposal in Q3, `overall` is an ordinary vocabulary value of a key (for example `"by": {"wealth_band": "overall"}`), not a special case.

### 3.3 Three summary forms

The brief asks for the three forms in `outputs.yml`. The entries use two (19 `p10_mean_p90`, 2 `point_and_range`: O7 and OS1); the manifest header names a third, level 2 uncertainty (`tornado_and_parameter_p10_p90`), reported apart. Q5 asks whether the third is hookable.

| Form | Cell fields | Meaning (from `metrics.md`) | Validation |
|---|---|---|---|
| A. `p10_mean_p90` | `p10`, `mean`, `p90` | level 1 return-risk spread over sampled paths, parameters fixed (range design) | numbers, `p10 <= p90` is an error; `mean` outside `[p10, p90]` is a warning |
| B. `point_and_range` | `point`, `lo`, `hi` | a point value and a range; what the range is differs by output (Q6) | numbers, `lo <= hi` is an error; `point` outside `[lo, hi]` is a warning |
| C. level 2, in `level2.<id>` | `tornado`: array of `{input, low_effect, high_effect}`; `p10`, `p90`: the P10 to P90 of the level-1 mean over parameter draws | parameter ignorance, tornado at the 0.5 point cut-off (metric register, stage A2) | `input` must be a register id; `p10 <= p90`; each output with a tornado lists inputs in descending absolute effect |

### 3.4 Validator rules

The validator runs at build and as a command (`python pipeline/hooks.py validate <file>`). Exit status is non-zero on any error.

| Rule | Check | Level |
|---|---|---|
| V1 | `schema` equals `wdt-outputs/1` | error |
| V2 | every key of `outputs` is a manifest id; `summary` matches the manifest | error |
| V3 | every cell has exactly the dimension keys the manifest declares for its output, with vocabulary values | error |
| V4 | no two cells share a key | error |
| V5 | numeric fields are finite JSON numbers; `null` allowed only where `run.status` is `provisional` | error |
| V6 | ordering rules of section 3.3 | error or warning as stated |
| V7 | coverage: for each output present, the cells equal the full product of schedules, horizons and `by` vocabularies the manifest declares | error when `run.status` is `final`, warning when `provisional` |
| V8 | `run.manifest_version` equals the manifest `version`; `run.manifest_sha256` equals the hash of the manifest file | error |
| V9 | `run.inputs_sha256` equals the hash of `registry/inputs.json` | error when `final`, warning when `provisional` |
| V10 | `series` points have strictly increasing integer `t` from 1, and the cell's reported years appear among them | error |
| V11 | every `t` named in a `by.year` vocabulary has a cell | error when `final` |
| V12 | unknown top-level or cell fields | warning (so the model can add diagnostics) |

## 4. Hooks: grammar and resolution

### 4.1 Parsing

The grammar is the template's, with one change proposed in Q3 (the band field takes several `key:value` pairs):

```
{{o:ID[.STAT][@SCHEDULE][/HORIZON][#KEY:VALUE[,KEY:VALUE...]]}}
{{i:ID[.STAT]}}
{{ref:fig-SPOKE-N}}
{{lit:KEY}}
```

Parts follow in the fixed order `.` `@` `/` `#`. Hooks are found in the Short answer, Evidence and Objection text; never inside code spans or fenced blocks, and never in a figure caption (rule F1 forbids it, so a hook in a caption is a lint error, not a rendering case). A text with `{{` that does not match any form is error H01.

The regular expression the parser uses for `o`:

```
\{\{o:(?P<id>O[A-Z]?[0-9]+[a-z]?)(?:\.(?P<stat>[a-z0-9]+))?(?:@(?P<sched>S_[a-z]+))?(?:/(?P<hor>[a-z]+))?(?:#(?P<by>overall|[A-Za-z0-9_]+:[A-Za-z0-9_]+(?:,[A-Za-z0-9_]+:[A-Za-z0-9_]+)*))?\}\}
```

A bare `#overall` (the template's form) means every `by` key of the output is `overall`.

### 4.2 Resolution of `{{o:}}`

In order; the first failing step stops the hook with its code.

1. Match the grammar (H01).
2. `ID` exists in the manifest (H02).
3. Apply defaults. `STAT`: `mean` for form A, `point` for form B. `SCHEDULE` and `HORIZON`: from the spoke front matter `defaults`. A missing value with no default is H09.
4. `STAT` is legal for the output's summary form: A allows `p10`, `mean`, `p90`, `range`; B allows `point`, `lo`, `hi`, `range`. The template lists `lo` and `hi` generally; they are legal only for form B (H03).
5. `SCHEDULE` is in the manifest `schedules` (H04). `HORIZON` is in the manifest `horizons` and, if the output declares its horizons (Q2), in that set; an output declared `single` rejects any horizon, and its cells use `single` (H05, H06).
6. `by`: a bare `#overall` sets every key of the output's `by` to `overall` (H08 if some key has no `overall`). Otherwise every key given must be a key of the output's `by`, with a vocabulary value (H07). Every key of the output's `by` that is not given takes `overall` if its vocabulary has it, otherwise the hook is H08. This makes the template's "overall where the output has one, otherwise error" a per-key rule.
7. R1 forward: the spoke's id is in the output's `element` list (H10). This fires in both modes: a hook to an output that does not belong to this spoke is an authoring error, not a data gap.
8. Look up the cell by key in the output data file. No file, or no cell: unresolved (H11). Cell present with a `null` field: unresolved (H12).
9. Format the value (4.6) and substitute.

### 4.3 Resolution of `{{i:}}`

`ID` is a register id as in `inputs.md` (for example `I-D4b`). Q7 explains why the template's `W_min` cannot be used as it stands.

1. `ID` exists in `registry/inputs.json` (H20).
2. `STAT`: `central` (default), `low`, `high`, `range` (renders "low to high"). Anything else is H21.
3. A display specification exists for the row, unit and decimals (Q8) (H22).
4. The chosen value parses as a number (H23). Rows whose Low, Central or High is text, such as a judgement flag, are not hookable until the research lane gives them numbers.
5. Format as in 4.6 and substitute. An `i` hook never needs the run, so it is never unresolved in draft mode: it resolves or fails.

### 4.4 Resolution of `{{ref:}}`

1. The id matches `fig-<spoke>-<n>` where `<spoke>` is an id such as `S5` or `S6-A`, and `<n>` is a positive integer: `^fig-(S[0-9]+(?:-[A-Z])?)-([0-9]+)$`.
2. A figure block with that id exists in this spoke file (H30). A figure cannot be cited from another spoke; cross-spoke reference is the ordinary `(S5 §2)` form.
3. Figure numbers in a file run 1 to k in block order with no gap or duplicate (H31).
4. Substitute the text `Figure n` as a link to `#fig-<spoke>-<n>`.
5. F4: every figure block has at least one `ref` hook, and the sentence that cites it contains an `o` hook (H32, checked by the spoke checker).

### 4.5 Resolution of `{{lit:}}`

1. `KEY` is `<bibkey>:<slug>` where `<bibkey>` is a key in `registry/references.bib` and `<slug>` names one figure in `registry/lit-figures.yml` (proposed form, Q9). A key not in the file is H40; a `bibkey` not in the bibliography is H42.
2. The entry holds `value`, `unit`, `decimals`, `locator` (page or table) and `verified` (date or `false`).
3. `verified: false` renders in draft mode as `[[lit:KEY]]` and fails in release mode (H41). Verified entries substitute the formatted value and add the bibliography key to the page's citation list, so the figure carries its source with no further author action.

### 4.6 Formatting

Units, rounding and wording come from the manifest and register, never the author (template section 4). Proposed rules:

| Unit tag (manifest, Q1) | Renders | Example for 0.22 |
|---|---|---|
| `pct` | number then `%` | `0.22%` |
| `pct_per_year` | number then `% per year` | `0.22% per year` |
| `pct_gdp` | number then `% of GDP` | `0.22% of GDP` |
| `gbp_bn` | `£` number `bn` | `£0.22bn` |
| `years` | number then `years` | `0.22 years` |
| `pp` | number then `percentage points` | `0.22 percentage points` |
| `ratio` | number alone | `0.22` |
| `bp` | number then `basis points` | `22 basis points` |
| `count` | number with thousands separators | `220,000` |
| `gbp_month` | `£` number `a month` | `£22 a month` |

- **Range** (`range`): "p10 to p90" or "lo to hi", with the unit once at the end: `0.11 to 0.33% per year`. For `gbp_bn` the `£` leads and `bn` trails the pair: `£0.11 to 0.33bn`.
- **Rounding:** decimal half-up on the stored value to the manifest `decimals`, computed on the decimal representation of the stored number so that `0.125` at two decimals gives `0.13`. Bands of one range are rounded separately.
- **Equal after rounding:** a `range` whose two ends round to the same string renders the single value and logs warning W2 (Q16).
- **Negative values:** rendered with a hyphen-minus and no space (`-0.6%`); Q16 asks whether to use a true minus sign.
- **Money:** stated in the real base year the metric register names; the base year is stated once per page, in the Data block Run row (Q16).
- **Unresolved placeholder:** `[[ID.STAT@SCHEDULE/HORIZON]]`, fully expanded with defaults applied, with `#KEY:VALUE` appended only for keys not `overall`. Hooks `{{o:O2.mean#wealth_band:overall}}` and `{{o:O2}}` in a spoke with default schedule `S_central` and horizon `short` both produce `[[O2.mean@S_central/short]]`, which matches the template's example.

### 4.7 Error codes

Draft mode (section 6) renders unresolved hooks and fails on every other code; release mode fails on all.

| Code | Case | Draft | Release |
|---|---|---|---|
| H01 | text does not match any hook form | fail | fail |
| H02 | unknown output id | fail | fail |
| H03 | `STAT` illegal for the summary form | fail | fail |
| H04 | unknown schedule | fail | fail |
| H05 | unknown horizon | fail | fail |
| H06 | horizon given for an output declared `single`, or horizon outside the output's declared set | fail | fail |
| H07 | `by` key or value not in the manifest | fail | fail |
| H08 | required `by` key missing and no `overall` | fail | fail |
| H09 | schedule or horizon omitted with no front-matter default | fail | fail |
| H10 | R1 forward: output's `element` does not list this spoke | fail | fail |
| H11 | no data file, or no cell for the key | placeholder | fail |
| H12 | cell field is `null` | placeholder | fail |
| H13 | data file inconsistent with manifest (V8) | fail | fail |
| H20 | unknown input id | fail | fail |
| H21 | `STAT` illegal for an input | fail | fail |
| H22 | no display spec for the input | fail | fail |
| H23 | selected input value is not a number | fail | fail |
| H30 | `ref` to a figure not in this file | fail | fail |
| H31 | figure numbers not 1 to k | fail | fail |
| H32 | figure block never cited, or citing sentence has no `o` hook (F4) | fail | fail |
| H40 | `lit` key not in `lit-figures.yml` | fail | fail |
| H41 | `lit` entry `verified: false` | placeholder | fail |
| H42 | `lit` bib key not in `references.bib` | fail | fail |
| R1r | reverse R1: an output lists this spoke in `element` and no hook cites it | warning (Q11) | fail |
| A2 | `/long` hook in the Short answer with no `/short` hook of the same output in that paragraph (template rule 6) | fail | fail |

Hook counting: the word budget counts each hook as one word before resolution, and an unresolved placeholder counts the same, so draft and release builds report the same budget.

## 5. Figures and reference tables: the data side

The figure renderer is not designed here. This file fixes where its numbers and the table come from, so the figure and the table cannot disagree (template 6a, rule 1).

For each figure block the builder computes one table:

1. Take each output id in the block's `output` list; each must be in the spoke's `outputs` set (F5, rule R1 forward, code H10).
2. Select cells with the block's `schedule` (a value, or all three), `horizon`, and `by`. A `by` the block omits expands to every vocabulary value of that key, so a figure of retired taxes (`per`) draws one line per tax.
3. For a cell with `series`, one table row per series point; otherwise one row per cell.
4. The same selected rows feed the renderer and the HTML and CSV tables.
5. A block that selects zero cells in release mode is an error (H11); in draft mode it renders an empty frame with the text `[[F-S5-1: no data]]`.

## 6. Draft and release builds

Selected by `WDT_MODE=draft|release`, default `draft`. The deploy workflow runs `draft` until the data gate opens (spoke prose is not written before then, template gate note) and `release` after.

| Behaviour | Draft | Release |
|---|---|---|
| unresolved hook (H11, H12, H41) | placeholder `[[...]]`, page marked draft | build fails |
| syntax, unknown id, R1 forward, other H codes | build fails | build fails |
| reverse R1 | warning | build fails |
| data file `run.status` | any | must be `final` (Q12) |
| V7 and V9 coverage and hash checks | warning | error |
| word budget (template section 3) | warn above 100% of cap, fail above 125% | same |

A draft page carries a banner "Draft: numbers are not final" and the count of placeholders. `_build/hooks-report.json` lists every unresolved hook with file and line, so the author can see what the missing run owes.

## 7. The Data block generator

One `data_block.py` function takes the spoke's resolved hook list and figure blocks and returns the block as Markdown with raw HTML tables for the build. Rows follow template section 6; a row with no content is omitted, never rendered empty.

| Row | Built from | Content and order |
|---|---|---|
| Outputs cited | each distinct `o` hook, de-duplicated on `(ID, STAT, schedule, horizon, by)` | columns: output id, title (manifest), `STAT`, schedule, horizon, `by`, value with unit. Order: first appearance in the text. The value string is the identical string shown in the prose, so a reader matches by eye |
| Figures | each figure block | id, outputs plotted, schedule, horizon, `by`, link to its table, link to its CSV |
| Reference tables | section 8 | one table per figure, in figure order |
| Run | data file `run` | manifest version, country pack, run date, status, base year (section 9) |
| Inputs | each distinct `i` hook | register id, name, value shown, unit, link to the register entry (Q14) |
| Literature figures | each distinct `lit` hook | key, formatted value, formatted bibliography entry from `references.json`, locator |
| Reading note | front matter `reading_note` (Q15) | text, at most 60 words; longer is an error |
| Replicate | each output id cited, plus each figure's outputs | link to that output's data-layer page (Q14) |

A hook added to the body appears in the block at the next build, with no step by the author. The block holds no prose except the reading note and the draft banner.

## 8. Reference tables as HTML and CSV

**HTML.** One table per figure, id `F-<spoke>-<n>` (matches `Data: Table F-S5-1` in the caption), with a `<caption>` that repeats the figure id and states no result, `<th scope="col">` headers, and a link `Download CSV` beside it. The caption's `Data: Table F-S5-1` string is linked to the table by the builder. Column set depends on the form:

| Form | Columns |
|---|---|
| A | series or category, schedule, horizon, `by` columns, `p10`, `mean`, `p90`, unit |
| B | category, schedule, horizon, `by` columns, `point`, `lo`, `hi`, unit |

HTML values use the display rounding of 4.6. Multiple outputs in one figure add an `output` column and the output title.

**CSV.** One file per table at `data/csv/F-<spoke>-<n>.csv`, UTF-8, comma-separated, a single header row and no comment lines, so spreadsheet tools open it cleanly. Provenance (run date, manifest version, country pack) goes in a sibling `F-<spoke>-<n>.meta.json`. Columns are the HTML columns with full-precision values (not display-rounded) and a final `unit` column. A per-output slice `data/csv/<ID>.csv` with every cell of that output (all schedules, horizons and bands) is generated from the same data; the Replicate row links to it.

## 9. Run metadata

Written by the model run into `run`; the builder never invents it.

| Field | Rule | Shown in Run row |
|---|---|---|
| `manifest_version` | equals manifest `version` (V8) | yes |
| `manifest_sha256` | hash of `outputs.yml` at run time | no |
| `country_pack` | equals manifest `country_pack` | yes |
| `run_date` | ISO date | yes |
| `status` | `provisional` or `final` | yes |
| `model_version` | free text, set by the model; git commit of the model code | no |
| `inputs_sha256` | hash of `registry/inputs.json` used | no |
| `paths` | number of return paths sampled | no |
| `base_year` | the year money is real in | yes (Q16) |

## 10. Worked example

All values are placeholders and are not a model result. The example is a hook in S5, whose `outputs` include O2 (the manifest lists S5 in O2's `element`).

**Hook in the Evidence text of S5**, with front matter defaults `schedule: S_central`, `horizon: short`:

```
The burden on the richest tenth of households is {{o:O2.range#wealth_band:D10}}.
```

Resolution: `ID` O2, `STAT` range, schedule `S_central` and horizon `short` from defaults, `by` `{wealth_band: D10}`; O2's manifest `by` is `[overall, wealth_band]`, so under Q3 the vocabulary of `wealth_band` includes `D10` and no other key is left to default. R1 forward: S5 is in `element`. The cell is found.

**Data file entry**, the cell the hook reads:

```json
"O2": {
  "summary": "p10_mean_p90",
  "cells": [
    { "schedule": "S_central", "horizon": "short",
      "by": {"wealth_band": "D10"},
      "p10": 0.11, "mean": 0.22, "p90": 0.33 }
  ]
}
```

Manifest additions assumed (Q1): `O2` has `unit: pct_per_year`, `decimals: 2`.

**Rendered text:**

```
The burden on the richest tenth of households is 0.11 to 0.33% per year.
```

**Data block, Outputs cited row** (one line, first in the table because it is the first hook):

| Output | Title | Stat | Schedule | Horizon | By | Value |
|---|---|---|---|---|---|---|
| O2 | Taxpayer burden, share of wealth | range | S_central | short | wealth_band: D10 | 0.11 to 0.33% per year |

**Same hook before a run exists** (draft mode, no data file): rendered `[[O2.range@S_central/short#wealth_band:D10]]`, the page banner shows one placeholder, and the Outputs cited row shows the value cell as `unresolved`.

**Same value in a CSV** if a figure plots it (`F-S5-1.csv`, full precision):

```
output,schedule,horizon,wealth_band,p10,mean,p90,unit
O2,S_central,short,D10,0.11,0.22,0.33,pct_per_year
```

The string in the prose, the Data block row and the table cells all come from the one cell, so they cannot disagree.

## 11. Questions

Each has a proposed answer. Until answered, the proposed rule is the working rule of this file.

1. **Manifest has no `unit` or `decimals` per output.** `metrics.md` gives units in prose (`% per year`, `% of GDP and real £bn`, `percentage points`), so the resolver cannot format from the manifest. *Proposed:* add to each `outputs.yml` entry `unit:` (one tag from section 4.6) and `decimals:` (integer), set by the guru from the metric register. M1 and its lines report two units (`% of GDP` and real £bn). *Proposed:* the hook renders `pct_gdp`; £bn appears only in the data-layer CSV. If prose needs £bn, the guru adds a unit field to the grammar, which this file does not do.
2. **Which outputs carry the horizon dimension.** The manifest `horizons` applies to all, but `metrics.md` gives M3 "one life, G years", M8 "short term", and path outputs P1, P3 to P6 have no horizon. *Proposed:* add `horizons:` per output, a list or `[single]`: O3 `[single]`, O8 `[short]`, OP1 to OP6 `[single]`, O7 and OS1 as the guru decides.
3. **Dimensions beyond `by`.** O1d lists `per` (seven taxes); OP5 has six taxes; OP1 has two reserves; OP4 has two numbers; OP6 has four years; OS1 has three quantities; O2b and O2c have a cut-off share; O4a and O4b have `income_decile`; the template's example `wealth_band:top` has no vocabulary (the register's bands are household wealth deciles grouped D4 to 5, D6 to 7, D8 to 9, D10). The grammar's `#BAND` takes a single key. *Proposed:* fold `per` and the component lists into `by` as a map `key: [values]` (for example `wealth_band: [overall, D4_5, D6_7, D8_9, D10]`, `per: [corporation_tax, ...]`, `year: [10, 25, 50, 100]`), and allow `#key:value,key:value`. This replaces the template's `wealth_band:top`; the guru edits `template.md`, this brief does not.
4. **Annual series.** The template's figure example plots OP6 "over 100 years", but P6 is defined at years 10, 25, 50, 100 only. *Proposed:* a cell may carry `series` (annual points); outputs that need a line over time declare `series: true` in the manifest, and OP6 is declared `year: [10, 25, 50, 100]` for hooks and `series: true` for figures.
5. **Level 2 hooks.** Template section 4 has no `STAT` for tornado results, and the brief's three forms include level 2. *Proposed:* level 2 is not hookable in this version; a tornado is shown only as a figure of kind `bar` whose table is built from `level2`. The guru adds `l2lo` and `l2hi` as stats if S12 needs them in prose.
6. **`point_and_range` meaning.** For O7 (tolerant zone) and OS1 (capitalisation, three quantities) the register does not say whether `lo` and `hi` are the level-1 spread or a policy range such as the alpha band. *Proposed:* the metric register states it per output in one sentence, the validator accepts any `lo <= hi`, and OS1's three quantities become a `by` key `quantity: [m1, m2, payer_count]`.
7. **Input naming.** The template's `inputs: [W_min]` and `{{i:W_min}}` name a quantity, but the register's ids are `I-D4a` and so on and no row holds the value of W_min (I-D4b is the share of adults at or above it, with £150,000 in the label). *Proposed:* hooks use register ids; the research lane adds a row for W_min; the template example changes to `{{i:I-D?}}` once that row exists.
8. **Input display.** Register rows have free-text units (for example "ratio, nominal GDP of wave midpoint year") and Low, Central, High columns, not a display unit or decimals. *Proposed:* a sidecar `registry/inputs-display.yml` mapping id to unit tag and decimals, written by the research lane, so the 89 register rows are not edited; `build_inputs.py` merges it. `STAT` for inputs is `low`, `central`, `high` or `range`.
9. **Literature figures.** `{{lit:KEY}}` is "keyed to the reference database" but the database holds citations, not figures. *Proposed:* `registry/lit-figures.yml` with entries `key: <bibkey>:<slug>`, `value`, `unit`, `decimals`, `locator`, `verified`. The research lane owns it. Register sources S1 to S43 that are cited rather than used as inputs are candidates.
10. **Data file name and policy.** *Proposed:* `model_v3/OUTPUTS/outputs.json`, tracked and generated like `model_v1/OUTPUTS/` (never edited by hand), copied to `_build/data/` at build. A provisional file is committed so draft builds are repeatable; a final file is committed by the author's decision (Q12).
11. **Severity of reverse R1 in draft.** The template makes it an error. During draft the spokes are incomplete by design. *Proposed:* warning in draft, error in release.
12. **Who marks data final.** *Proposed:* `run.status` is set `final` by the run script only when invoked with a flag the author passes; release builds require it. This is the mechanical form of the data gate.
13. **Template label mismatch.** Section 6a rule 3 writes `Data: Table F5.1`; the same section's ids and rule F3 are `Table F-<spoke>-<n>`. *Proposed:* `F-<spoke>-<n>` everywhere; the guru corrects the template.
14. **Link targets.** The Replicate row and the Inputs row link to data-layer pages, whose addresses `nav.md` (brief 021s) fixes. *Proposed:* this design emits links through a function `data_url(kind, id)`, with placeholders `data/outputs/<ID>.html` and `data/inputs.html#<ID>` until `nav.md` settles them.
15. **Reading note location.** Template section 2 allows an optional 60-word note but not where it lives. *Proposed:* front matter key `reading_note:`.
16. **Number style.** Open: minus sign (hyphen or true minus), thousands separator for `gbp_bn` over 999, behaviour when a range rounds to one value (proposed: single value plus warning W2), and where the money base year is stated (proposed: the Run row). The manifest names no base year.
17. **Proposed outputs not in the manifest.** `docs/model-v3/added/` holds proposed outputs (OH1a to OH1c, OW1 to OW3, OM1, OL1). Hooks to them are H02 until the guru merges them into `outputs.yml`.
18. **Manifest `version`.** `stage-A2-passed` is a stage label, not a version. The Run row prints it as written. *Proposed:* keep it as an opaque string; V8 compares text.

## 12. Checks run

| Check | Result |
|---|---|
| Data file schema complete enough for a validator, three forms stated | sections 3.1 to 3.4 (rules V1 to V12) |
| Every hook form has a resolution rule and an error case | `o`, `i`, `ref`, `lit`: sections 4.2 to 4.5, codes in 4.7 |
| Worked example round-trips | section 10: hook, data entry, rendered text, Data block row, CSV row |
| Manifest gaps listed as questions | Q1 to Q6, Q17, Q18 |
| Regex parses every example in template section 4 and the worked example | run in the session, result in the change report |
