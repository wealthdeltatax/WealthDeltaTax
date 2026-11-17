# Spoke checker specification

> **Ids (author, 2026-11-17).** Spoke shortcodes (`docs/restructure/shortcodes.md`) are the page ids, URLs, front-matter `spoke:` values and figure and table ids. Where this file still writes `S1` to `S12`, read it through `docs/restructure/ids-map.md`; the S numbers are planning labels only.

> **Questions.** All proposed answers in this file's question section were accepted by the author on 2026-11-17 (nothing else reads `site-index.json`), except where `ids-map.md` overrides the S ids. Guru follow-through done the same day: `outputs.yml` carries `unit`, `decimals`, `horizons`, `by` maps and `series` (hooks Q1 to Q4); the template's table label is `F-<spoke>-<n>` and its example is an output the spoke owns (hooks Q13, checker Q14 and Q17).

Brief 020w, part of 013g stage D. Status: draft for the guru; the author decides the numbered questions in section 9. This file designs the checker. It builds nothing. The guru merges it into `docs/restructure/site.md` with its siblings (`ids.md`, `hooks.md`, `figures.md`, `nav.md`).

Sources: `docs/restructure/template.md` (sections 1 to 8), `docs/agents/reference/writing/style-guide.md` and `prose-rules.md`, `docs/model-v3/outputs.yml` (version `stage-A3-integrated-2026-11-17`), `docs/model-v3/inputs.md`, `pipeline/check_wdt_format.py`. Where the template is silent or inconsistent, this file proposes an answer in section 9 and marks the check "(Q n)". It does not guess.

## 1. Shape of the tool

Proposed name `pipeline/check_spokes.py` (Q16). It replaces `check_wdt_format.py` for spokes; the old checker keeps running on the old paper shape until the ids and migration brief (017s) retires it.

**Two modes.**
- **Source mode (S).** Needs the spoke file, the manifest, the input register and the reference database. Runs in the writing lane on every save and in CI. Catches shape, budget, syntax, lint and manifest consistency.
- **Build mode (B).** Adds the resolver's results and the generated Data block. Runs in the site build after the resolver (`hooks.md`). Catches unresolved hooks and generator faults.

**Output.** One line per finding, `path:line: SEV CODE message`, then counts per part (words per Short answer, Evidence and Objection block) and counts per severity. Exit 1 if any E, else 0.

**Severities.**
- **E** fails the build. The spoke page does not deploy; `main` deploys on push, so CI stops.
- **W** warns. Printed, exit 0. The writing lane clears each one or lists it in the change report with a reason.
- **I** information. Printed only with `-v`.

**Writing-lane actions** (the last column of every table).
- **FIX**: edit the spoke text.
- **MANIFEST**: the manifest is the guru's. Report the mismatch; do not edit `outputs.yml`, and do not drop a hook to silence R1.
- **AUTHOR**: stop and ask, with a proposed resolution (`AGENTS.md`, Finishing).
- **TOOL**: the checker or the build is wrong. Do not change the text to dodge it. Append an entry to `docs/brief-suggestions.md` (lane c or s) and say so in the change report.

A check is never relaxed to make a spoke pass. A fix to the text is made only when the finding is true.

**Status downgrade (Q4).** For a spoke with `status: draft`, the count and coverage errors (WC1, WC2, OB2, OB3, FM10, R1 reverse, F4 first half) report as W; all syntax and identifier errors stay E. `author-review` and `accepted` are strict. A release build (`--release`, set when the data gate opens) makes every unresolved hook an E whatever the status (template section 4, rule 5).

## 2. Inputs

| Input | Used by |
|---|---|
| The spoke file (`.md`) | all |
| `docs/model-v3/outputs.yml` | FM, HK, R1, FG, F1 to F6, DB: ids, `element:`, `summary:`, `by:`, `schedules`, `horizons`, `once_not_per_schedule`, `kind`, `version`, `country_pack`, the `checks:` list |
| `docs/model-v3/inputs.md` (register rows) | FM11, HK9 (Q10) |
| `registry/references.bib` and the literature-figure table (Q11) | HK10, OB6, WR16 |
| Spoke list: ids, file paths, `depends` graph | FM5, FM12, XR6, XR7 (a machine-readable list, from 017s) |
| Sibling spoke files | XR7 when the target spoke is present |
| Resolver output and the generated Data block | HK13, DB1 to DB9 (build mode) |

## 3. Parse model

Assumed until Q2 and Q3 are decided.

1. Front matter: the first `---` block, parsed as YAML. Removed before everything else.
2. Fenced code blocks and figure blocks (`::: {#fig-...}` to `:::`) are parsed separately and excluded from prose checks, except where a check names them.
3. The body is split on H2. Reserved H2 titles: `Short answer` (first) and `Strongest objection` (last). Every H2 between is an Evidence section.
4. Counted prose (template section 3): the text of Short answer, Evidence and the Objection block. Excluded: front matter, headings, figure blocks (so captions), the Data block, the bold labels of the objection block.
5. Hook grammar, from template section 4:

```
{{o:ID[.STAT][@SCHEDULE][/HORIZON][#BAND]}}   {{i:NAME}}   {{ref:fig-ID}}   {{lit:KEY}}
```

Effective values: an omitted SCHEDULE or HORIZON takes the front-matter `defaults`; an omitted STAT takes `mean` for `p10_mean_p90` outputs and `point` for `point_and_range` outputs; an omitted BAND takes `overall` where the output lists it.

## 4. Checks

Columns: **M** is the mode (S source, B build). Examples are minimal; hooks use real ids from `outputs.yml`.

### 4.1 Front matter (FM)

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| FM1 | File opens with a `---` block that closes and parses as YAML | E | S | block closed by `---` | no closing `---` | FIX |
| FM2 | Keys `spoke`, `question`, `status`, `budget`, `defaults`, `outputs`, `depends` present; `inputs` present, may be `[]` | E | S | all eight present | `defaults` missing | FIX |
| FM3 | No unknown key. The old paper keys `title`, `shortcode`, `zenodo_doi`, `jel`, `keywords` are unknown (Q1) | E | S | only template keys | `zenodo_doi: "10.5072/zenodo.TBD"` | FIX, or AUTHOR if the key is wanted |
| FM4 | Key order is `spoke`, `question`, `status`, `budget`, `defaults`, `outputs`, `inputs`, `depends`. W because the build reads keys by name | W | S | template order | `status` before `question` | FIX |
| FM5 | `spoke` matches `S1` to `S12` with optional `-A` to `-Z`, is in the spoke list, and equals the file name | E | S | `spoke: S4-A` in `S4-A.md` | `spoke: S13` | FIX or AUTHOR |
| FM6 | `question` is non-empty; W if it does not end in `?`; W if two spokes share one question (corpus run) | E, W | S | `"What rate, what threshold, how much?"` | `question: ""` | FIX |
| FM7 | `status` is `draft`, `author-review` or `accepted` | E | S | `status: draft` | `status: ready` | FIX |
| FM8 | `budget.cap` is a positive integer; W if it is not 6,000 (the series default, author 2026-11-17) | E, W | S | `budget: {cap: 6000}` | `budget: {cap: 8000}` warns | AUTHOR for the warn |
| FM9 | `defaults.schedule` is in `schedules`; `defaults.horizon` is in `horizons` | E | S | `{schedule: S_central, horizon: short}` | `{schedule: central, horizon: short}` | FIX |
| FM10 | `outputs` equals the set of ids whose `element:` lists this spoke (both directions). Checks entries in `checks:` too | E | S | S6-A with `outputs: [OM1]` | S6-A with `outputs: [OM1, O2]` | FIX if the list is wrong, MANIFEST if the manifest is |
| FM11 | Every `inputs` name is in the input register | E | S | a name present in the register | `inputs: [W_floor]` | FIX or AUTHOR (Q10) |
| FM12 | Every `depends` id is in the spoke list, is not this spoke, and the graph has no cycle (corpus run) | E | S | `depends: [S3, S4]` in S5 | `depends: [S5]` in S5 | FIX |

### 4.2 Part order and shape (PT)

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| PT1 | Exactly one `## Short answer`, first; one or more Evidence H2s; exactly one `## Strongest objection`, last; no H1 (the question is the title) (Q2) | E | S | Short answer, `## 1.`, `## 2.`, `## 3.`, objection | objection placed before the last Evidence section | FIX |
| PT2 | The source has no Data block: no heading `Data block`, no hand-written reference table | E | S | none | `## Data block` | FIX |
| PT3 | Short answer is one paragraph: no second paragraph, list, figure block or subheading | E | S | one paragraph | two paragraphs | FIX |
| PT4 | Evidence has three to six H2s ("usually", template section 2) | I | S | four sections | eight sections | FIX or split (AUTHOR) |
| PT5 | Each Evidence H2 starts with a paragraph, not a figure block, list or quote | W | S | claim sentence first | figure block directly under the heading | FIX |
| PT6 | Evidence headings are numbered `1.` upward in order, no lower-case letters (Q3) | E | S | `## 2. The refund cap` after `## 1.` | `## 3.` after `## 1.`; `## 2.b` | FIX |
| PT7 | No heading below H2 (Q2) | W | S | none | `### The cap` | FIX |
| PT8 | No pasted image: figures come from figure blocks only | E | S | a figure block | `![Figure 3: ...](../figures/x.png)` | FIX |

### 4.3 Word budget (WC)

The count follows Q5. A hook counts as one word. The summary line reports each part's count whether or not a check fires.

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| WC1 | Short answer is 80 to 150 words | E | S | 112 words | 61 words | FIX |
| WC2 | Objection block is 150 to 400 words (template section 3). The sub-maxima in section 5 of the template add to about 440, so the block total is the binding cap | E | S | 310 words | 430 words | FIX |
| WC3 | Whole spoke at most `budget.cap`: W above 100%, E above 125% (7,500 words at a cap of 6,000). No floor | W, E | S | 5,400 words | 6,300 words warns; 7,600 fails | FIX or split (AUTHOR) |
| WC4 | `reading_note` is at most 60 words (Q6) | E | S | 41 words | 75 words | FIX |

### 4.4 Objection block (OB)

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| OB1 | The five labels `**Objection.**`, `**Held by.**`, `**Response.**`, `**Status.**`, `**What would change the answer.**` appear once each, in that order, each with text | E | S | all five | `**Reply.**` in place of `**Response.**` | FIX |
| OB2 | Objection text is 60 to 150 words | E | S | 95 words | 40 words | FIX |
| OB3 | Response is 1 to 200 words | E | S | 150 words | 260 words | FIX |
| OB4 | Status text starts with exactly one of `open question`, `named compromise`, `empirical`, lower case, then a full stop | E | S | `**Status.** Named compromise. The design accepts...` | `**Status.** Partly empirical.` | FIX |
| OB5 | After the label sentence, exactly one sentence. W because splitting on full stops is heuristic | W | S | one sentence | three sentences | FIX |
| OB6 | Held by holds a resolving citation (`(@Key)` or `{{lit:KEY}}`) or the fixed phrase "no one has put this in print; it is the sceptic's obvious point" | E | S | `(@Harberger1965)` | `Held by. Several economists.` | FIX |
| OB7 | What would change the answer is non-empty. A pointer such as `(S12 §2)` is validated by XR6 and XR7 | E | S | `If the rate exceeds the cap, see (S12 §2).` | empty field | FIX |

### 4.5 Hooks and R1 (HK)

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| HK1 | Every `{{...}}` parses under the grammar: kind `o`, `i`, `ref` or `lit`; braces balanced; fields in order STAT, SCHEDULE, HORIZON, BAND | E | S | `{{o:O1.range@S_central/short}}` | `{{o:O1/short@S_central}}` | FIX |
| HK2 | ID, STAT, SCHEDULE, HORIZON and BAND key exist in the manifest (template section 4, rule 1) | E | S | `{{o:OP1.p90@S_low/transition}}` | `{{o:O99.mean}}` | FIX or MANIFEST |
| HK3 | STAT is valid for the output's `summary:`: `p10_mean_p90` takes p10, mean, p90, range; `point_and_range` takes point, lo, hi, range; `point` takes point (Q7) | E | S | `{{o:OS1.range}}` | `{{o:OS1.p10}}` | FIX |
| HK4 | BAND is omitted only where the output lists `overall`; otherwise the hook names a band (template section 4 table) | E | S | `{{o:O2.mean}}` (O2 lists `overall`) | `{{o:OB1.mean}}` (OB1 is `by: [w_min]`) | FIX |
| HK5 | `@SCHEDULE` and `/HORIZON` appear only on outputs indexed by them. `once_not_per_schedule: true` and `kind: data_fact` take no schedule (Q7) | E | S | `{{o:OH1b.mean#overall}}` | `{{o:OH1b.mean@S_low#overall}}` | FIX |
| HK6 | R1 forward: the output's `element:` lists this spoke | E | S | `{{o:OB1...}}` in S3 | `{{o:O2.mean}}` in S3 (O2 lists H0, H3, S5, S6, S12) | FIX or MANIFEST |
| HK7 | R1 reverse: every output whose `element:` lists this spoke is cited by a hook or a figure block (F5) | E | S | S6-A cites `{{o:OM1.mean/short}}` | S6-A cites nothing (its set is OM1) | FIX or MANIFEST |
| HK8 | A hook to a check id (`{{o:CK1}}`) resolves in `checks:` and counts for R1 (Q8) | E | S | `{{o:CK1.range}}` in S12 | `{{o:CK1}}` in S5 | FIX |
| HK9 | `{{i:NAME}}` resolves in the input register (Q10) | E | S | `{{i:I-D4b}}` | `{{i:I-D9z}}` | FIX or AUTHOR |
| HK10 | `{{lit:KEY}}` resolves in the literature-figure table, and its source key is in `references.bib` (Q11) | E | S | a known key | an unknown key | FIX or AUTHOR |
| HK11 | `{{ref:fig-ID}}` resolves to a figure block in this spoke | E | S | `{{ref:fig-S5-1}}` with that block present | `{{ref:fig-S5-2}}` with no such block | FIX |
| HK12 | Hooks sit only in Short answer, Evidence and the Objection block: not in headings, front matter, captions or alt text (captions: F1) | E | S | hook in a body sentence | hook in `## The rate is {{o:O1.mean}}` | FIX |
| HK13 | Unresolved hook: renders `[[...]]` and marks the page draft in a draft build; E in a release build | I, E | B | all resolved | `[[O2.mean@S_central/short]]` in a release build | AUTHOR (data gate) or TOOL |
| HK14 | Horizon discipline (template section 4, rule 6; reading rule A2): in Short answer a hook at the long horizon has, in the same sentence, a hook to the same output at the short horizon | E | S | `{{o:O1.range/short}} in the short run and {{o:O1.range/long}} in the long run` | `{{o:O1.range/long}}` alone | FIX |
| HK15 | A sentence with a long-horizon hook does not call it a forecast: words `forecast`, `predict`, `project`, `expected to` | W | S | `a steady-state value of {{o:O1.range/long}}` | `we forecast {{o:O1.range/long}}` | FIX |
| HK16 | No unit typed beside a hook: unit symbols or words (`%`, `£`, `bn`, `per cent`) next to a hook that already renders its unit | W | S | `{{o:O1.mean}} of GDP` | `{{o:O1.mean}}%` | FIX |
| HK17 | No `[[` in the source (draft output pasted back) | E | S | none | `[[O2.mean]]` typed in | FIX |

### 4.6 Typed figures (TF)

Template section 4, rule 4, strict (author, 2026-11-17). Applies to Short answer, Evidence and the Objection block. Not scanned: hooks, headings, front matter, figure blocks, code. Not flagged: a year (four digits from 1800 to 2199, not next to a currency sign or unit), `§` references, spoke and output ids (`S5`, `OP6`), figure and table ids (`F-S5-1`), cross-reference brackets, ordinals (`10th`).

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| TF1 | No percentage, currency amount, decimal, or integer of three or more digits (including comma-grouped) in prose | E | S | `The levy raises {{o:O1.range@S_central/short}} of GDP.` | `The levy raises 1.4% of GDP.` | FIX: a hook for a model value, `{{lit:KEY}}` for a literature or current-law value |
| TF2 | No number written in words beside a unit: `per cent`, `percent`, `pounds`, `million`, `billion`, `trillion` after a number word or digit | W | S | `about half of adults` | `twenty per cent of wealth` | FIX |
| TF3 | A one- or two-digit integer standing alone is written as a word if it is a structural count (template section 4, rule 4) | W | S | `Six taxes are retired.` | `6 taxes are retired.` | FIX |

### 4.7 Figure blocks (FG) and caption lint (F1 to F6)

The F-numbers are the template's (section 6a).

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| FG1 | Block is a fenced div `::: {#fig-...}` closed by `:::`, with YAML fields | E | S | closed block | no closing `:::` | FIX |
| FG2 | Id is `fig-<this spoke>-<n>`, `n` an integer from 1, unique | E | S | `fig-S6-A-1` in S6-A | `fig-S5-1` in S7; two blocks `fig-S5-1` | FIX |
| FG3 | Numbers run 1, 2, 3 in order of appearance. A gap is W: a deleted figure leaves a hole, and renumbering breaks outside references | W | S | 1, 2, 3 | 1, 3 | FIX |
| FG4 | Fields `output`, `kind`, `schedule`, `horizon`, `caption`, `alt` present; `by` present where the output has a `by:` list | E | S | all present | `alt` missing | FIX |
| FG5 | `kind` is `line`, `band`, `bar`, `dot`, `map` or `stack` | E | S | `kind: band` | `kind: pie` | FIX |
| FG6 | Every `output` id exists; `schedule` is one valid value or a list of valid values; `horizon` is one valid value; `by` is a key of the output's `by:` list | E | S | `schedule: [S_low, S_central, S_high]` | `horizon: long-run` | FIX |
| FG7 | A figure block sits inside an Evidence section, not in Short answer or the Objection block | E | S | under `## 2.` | inside `## Strongest objection` | FIX |
| FG8 | Alt text holds no hook (E), no result word from the F2 list (W), no figure of three or more digits other than years (W) | E, W | S | `Line chart of fund assets against year, with a shaded range.` | `Line chart showing fund assets rising.` | FIX |
| FG9 | Caption names the schedule and the horizon, in words: `low schedule`, `central schedule`, `high schedule`; `transition`, `short`, `long` horizon (W; lexical) | W | S | `central schedule, long horizon` | caption names neither | FIX |
| FG10 | If `schedule` lists all three, the caption says so (`three schedules` or the three names) | W | S | `Draws all three schedules.` | three listed, caption silent | FIX |
| F1 | Caption has no `{{o:}}`, `{{i:}}` or `{{lit:}}` hook and no figure of three or more digits other than years and ids. A number directly followed by `year` or `years` is exempt (Q12) | E | S | `Public wealth path (fund assets, share of GDP), central schedule, long horizon.` | caption holds `{{o:OP6.mean/long}}` | FIX |
| F2 | Caption has none of the result words (section 6) | E | S | `Shaded band runs from the 10th to the 90th percentile.` | `Fund assets rise over the horizon.` | FIX |
| F3 | Caption ends with `Data: Table F-<spoke>-<n>`, the same spoke and `n` as the block's own id (Q14) | E | S | `... Data: Table F-S7-1.` in `fig-S7-1` | `... Data: Table F5.1.` | FIX |
| F4 | Every figure block is cited by `{{ref:}}` at least once (E, W while draft). The citing sentence holds an `{{o:}}` hook (W). That the sentence states the result is manual | E, W | S | `Fund assets reach {{o:OP6.mean/long}} of GDP ({{ref:fig-S7-1}}).` | block never cited; or `see {{ref:fig-S7-1}}` with no hook | FIX |
| F5 | Every output in a block is in the spoke's `outputs` set; it counts as cited for HK7 | E | S | `fig-S7-1` with `output: [OP6]` (OP6 lists S7 and S12) | `fig-S5-1` with `output: [OP6]`, which is the template's own example | FIX or MANIFEST |
| F6 | Source holds no table (TB1). The generated Data block lists every figure and every reference table (DB3) | E | S, B | no pipe table | a pipe table under `## 2.` | FIX, or TOOL for DB3 |
| TB1 | No table in the prose: no pipe-table separator row and no `<table>` anywhere in the source, the objection block included. A list that is not data (the six retired taxes) is prose | E | S | a sentence naming the taxes | `\| Tax \| Year \|` rows | FIX |

### 4.8 Cross-references (XR)

The syntax checks carry over from the old checker with a new shortcode pattern (section 7).

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| XR1 | Form is `(SC)`, `(SC §N)`, `(SC §N) to (SC §M)`, `(SC §N) and (SC §M)`; fully bracketed; the shortcode is a spoke id (`S5`, `S4-A`), a hub id (`H3`), or a standalone paper (ADD, INST, SCOPE); a retired source (`MF`, `WP`) is allowed but W | E, W | S | `(S5 §2)` | `(S5 §2.b)` | FIX |
| XR2 | No bare `§` | E | S | `(S5 §2)` | `see §2` | FIX |
| XR3 | No range with `§§`, a dash or "through" | E | S | `(S5 §1) to (S5 §3)` | `(S5 §1-3)` | FIX |
| XR4 | No "Section N" | E | S | `(S5 §2)` | `Section 2` | FIX |
| XR5 | No lower-case letter in a section number; no extra words inside the brackets | E | S | `(S4-A §3)` | `(S4-A §3, above)` | FIX |
| XR6 | The shortcode names a spoke, hub or standalone paper that exists in the spoke list | E | S | `(S12 §1)` | `(S13 §1)` | FIX or AUTHOR |
| XR7 | The section exists: checked in this spoke (Evidence H2 numbers) and in any sibling file present. Targets in absent files are reported as I "unverified", not passed (as in `wdt_crosslinks.py`). Full resolution across spokes is the crosslink tool's job (Q15) | E, I | S | `(S5 §2)` in S5, which has `## 2.` | `(S5 §7)` in S5, which has four | FIX |
| XR8 | No plain-text `Figure N` or `Table N` in prose; cite a figure with `{{ref:}}`, a figure in another spoke as `(S6 Figure 2)` (Q15) | W | S | `{{ref:fig-S5-1}}` | `Figure 1 shows` | FIX |
| XR9 | No `see above`, `see below`, or "the ... paper" without a shortcode | W | S | `(S3 §1)` | `see above` | FIX |

### 4.9 Writing rules that can be automated (WR)

Word lists are in section 6. Template section 7 gives the rule numbers.

| ID | Check | Sev | M | Pass | Fail | Action |
|---|---|---|---|---|---|---|
| WR1 | No em dash anywhere in the source, headings, captions and front matter included (rule 9). The old checker exempted headings and table rows | E | S | `The cap binds (see (S3 §2)).` | `The cap binds — always.` | FIX |
| WR2 | No en dash and no spaced hyphen used as a dash | W | S | `the cap binds, so refunds stop` | `the cap binds - refunds stop` | FIX |
| WR3 | No "genuine" or "genuinely" (rule 9) | E | S | `a real trade-off` | `a genuine trade-off` | FIX |
| WR4 | No hedge preamble from `prose-rules.md` (list 2) | E | S | `Refunds are capped.` | `It is worth noting that refunds are capped.` | FIX |
| WR5 | No decorative intensifier or rhetorical adverb (list 3). "central schedule" is exempt | W | S | `the central schedule` | `a fundamental feature` | FIX |
| WR6 | "not X but Y" heuristic (rule 9) | W | S | `The refund is a share of tax paid.` | `The refund is not a subsidy but a share of tax paid.` | FIX or keep if the contrast does analytic work |
| WR7 | No preamble or closing-summary phrase (list 4; rule 1) | W | S | starts with the claim | `In this section we will argue...` | FIX |
| WR8 | No temporal artifact (rule 3). "has since been" is E; the rest of list 5 is W | E, W | S | `The cap is the tax paid.` | `The cap has since been tightened.` | FIX |
| WR9 | No list in Evidence or the Objection block (W). In Short answer PT3 already fails it | W | S | prose | a `-` bullet under `## 2.` | FIX unless the reader follows a sequence |
| WR10 | No bold except the five objection labels; no italic spans | W | S | labels only | `**the cap**` in Evidence | FIX |
| WR11 | No typed author-year citation; use `(@Key)`. A typed DOI is W (Q11) | W | S | `(@Harberger1965)` | `(Harberger, 1965)` | FIX |
| WR12 | `@Key` citations resolve in `references.bib` | E | S | a known key | `(@Harberger1066)` | FIX or AUTHOR |
| SA1 | Short answer cites at least one hook where the spoke has outputs, mentions the objection, and names a horizon by word or hook field (template section 2) | W | S | a hook with `/short`, the word "objection" | no hook; no horizon | FIX |

### 4.10 Data block, build mode (DB)

Generated by the build; a fault here is the generator's. Action TOOL for all.

| ID | Check | Sev | M | Pass | Fail |
|---|---|---|---|---|---|
| DB1 | Rows present as in template section 6: Outputs cited, Figures, Reference tables, Run, Inputs, Literature figures, Reading note, Replicate (a row is omitted only if it has nothing to list) | E | B | all present | Run row missing |
| DB2 | Outputs cited equals the set of output ids in hooks and figure blocks | E | B | sets equal | a hooked id missing |
| DB3 | Figures rows equal the figure blocks; each has a reference table and a CSV link | E | B | three blocks, three rows | a block without a table |
| DB4 | Run row `version` and `country_pack` equal the manifest's | E | B | `stage-A3-integrated-2026-11-17`, `UK` | an older version |
| DB5 | Inputs rows equal the `{{i:}}` set; Literature rows equal the `{{lit:}}` set | E | B | sets equal | a `{{lit:}}` key unlisted |
| DB6 | Each reference table has columns for value, unit, STAT, schedule and horizon (6a, rule 1) | E | B | all five | no horizon column |
| DB7 | A Replicate link per output cited | E | B | one per id | none for OP6 |
| DB8 | Reading note rendered if `reading_note` is set | E | B | rendered | dropped |

## 5. Manual-only rules

The checker cannot decide these, so the writing lane checks them by reading. Each is also a line in the change report ("prose pass done").

| Rule (source) | Why it stays manual |
|---|---|
| Each Evidence section opens with its claim (section 2) | needs a semantic read; PT5 only checks that a paragraph comes first |
| One paragraph, one structural idea (rule 2) | semantic |
| Short answer leads with the answer to the question | semantic; SA1 checks only the lexical parts |
| A caveat is stated once, where it bites (rule 4) | duplicates differ in wording; a sentence-similarity lint would flag legitimate pointers |
| Name trade-offs; do not oversell (rules 5, 8) | semantic |
| Hedge with a condition (rule 6) | a lint on "may" and "might" fires on almost every paragraph |
| A spoke stands alone (rule 10) | needs knowledge of what the hub and other spokes say |
| Never invent a figure, quote, citation or DOI (rule 11) | the checker can test that keys resolve (HK10, WR12), not that a claim is true |
| Caption matches the image; caption states no result (6a, rule 2) | F1 and F2 are lexical; the renderer's output has to be looked at |
| The sentence that cites a figure states the result (F4) | the checker finds a hook in the sentence, not whether it is the result |
| Alt text describes the form of the chart, never the finding (6a) | FG8 is lexical |
| The objection is the strongest version, no strawman; the response claims no more than the status label allows (section 5) | semantic |
| Status label is the right one of three (style guide, tone rules) | needs the author's knowledge of what work exists |
| An open question is assigned to a future paper, and to SCOPE if outside the project (style guide) | "outside the project" is a judgement and a future paper has no machine-readable target |
| A "Held by" source actually holds the objection | OB6 checks that the key resolves |
| Long-horizon claims are worded as steady-state properties (rule 6) | HK15 catches the obvious words only |
| The sentence reads with "x%" or "x to y%" in the hook slot (template section 4) | needs the rendered text; HK16 catches only a doubled unit |
| Money is in base-year pounds (6a) | stated by the metric register; the renderer applies it |
| AI-tell patterns: thesis-tension-resolution paragraphs, punchline endings, symmetric paragraph pairs, retrospective inevitability, dramatic moral seriousness, over-clean prose (`prose-rules.md`, set B) | structural and tonal; the old checker never tried them |

## 6. Word lists (live in the checker; they can grow)

```
RESULT_WORDS (F2, FG8), the template's list as the floor:
  rises, falls, grows, shrinks, exceeds, outweighs, shows that,
  demonstrates, confirms, higher, lower, larger, smaller, peaks, converges
  Match: case-insensitive, whole word; "shows that" as a phrase. Inflections: Q13.

BANNED (WR3): genuine, genuinely

HEDGE_PREAMBLE (WR4, error): it is worth noting that, it bears emphasising that,
  it bears emphasizing that, it should be said that, one might observe that
  (W, not listed in prose-rules but the same family): it is important to note

INTENSIFIERS (WR5, warn): fundamental, fundamentally, crucial, crucially, profound,
  profoundly, central, core, deeply, inherently, inevitably, necessarily
  Exempt: "central schedule", the id S_central

PREAMBLE_CLOSING (WR7, warn): in this section, this section will, we will argue,
  we argue that, in conclusion, to summarise, to summarize, thus we have shown,
  as we have seen

TEMPORAL (WR8): error: has since been
  warn: previously, formerly, no longer, originally, used to, earlier version,
  the old, was revised, was changed, now supersedes

FORECAST (HK15, warn): forecast, predict, project(s|ed|ion), expected to
```

Lists 2 to 5 of the writing rules in WR4 to WR8 come from `prose-rules.md` and template section 7; the lists above are the checker's initial contents, not new rules.

## 7. What carries over from `check_wdt_format.py`

| Old check | Fate | New check and note |
|---|---|---|
| Front matter: required fields `title`, `shortcode`, `status`, `keywords`, `zenodo_doi`, `jel` | retired | replaced by FM2 and FM3 (Q1) |
| Front matter field order | changed | FM4, new field set, W instead of fail |
| `zenodo_doi` format | retired | no DOI on a spoke unless Q1 is answered the other way; then it carries over unchanged |
| `jel` line format | retired | same as above |
| Lower-case letter in a section number | carried over | XR5 and PT6; now also applies to Evidence heading numbers |
| `{.appendix}` attribute | retired | appendix spokes are the `-A` suffix (template section 3); a heading attribute is not allowed anywhere (PT7 covers headings, FM3 covers keys) |
| Bare `§` | carried over | XR2; shortcode pattern widened: the old `[A-Z][A-Za-z]*(?:\.[A-Z])?` does not match `S5` or `S4-A` |
| Malformed `(SC §...)` | carried over | XR1 and XR5; the bracket grammar changes only for figure references (XR8) |
| Range with `§§`, dash or "through" | carried over | XR3 |
| "Section N" | carried over | XR4 |
| Figure line `![Figure N: ...](...)`: label from section, letters, path name, `{width=100%}`, `Source: (SC §x)` | retired | a pasted figure is now PT8 (E); figure blocks are FG1 to FG10; `Source:` becomes `Data: Table F-<spoke>-<n>` (F3) |
| Em dash in prose | changed | WR1: now E in headings, captions and tables too |
| Fenced code skipping | carried over | section 3, point 2 |
| Exit 1 if any issue | changed | exit 1 only on E; W and I do not fail (section 1) |

The old checker's neighbours: `wdt_crosslinks.py` resolves references against `registry/anchors.yml` and `contents.yml`, which are built from old papers. Whether spokes enter those files is for 017s; section 9, Q15 keeps the split of work between that tool and this one.

## 8. Findings in the template (for the guru; `template.md` is not edited here)

1. The 6a example caption says "over 100 years". F1 as written flags it (three digits that are not a year). Q12 proposes the exemption.
2. The 6a example block is `fig-S5-1` with `output: [OP6]`. OP6's `element:` is S7 and S12, so the example fails F5 and HK6. The S5 outputs are O1 to O3, O5 to O7, OP1, OP4, O8, OB1, OR1, OF1, OT1 and the lines O1a to O1d. Q17.
3. 6a rule 3 says `Data: Table F5.1`; F3 and the ids paragraph say `F-<spoke>-<n>`. Q14.
4. `(S5 §2)` is used for cross-references (section 7, rule 7), but the template does not number spoke sections, and section 1 numbers the four parts 1 to 4. Q3.
5. `{{i:W_min}}` names a symbol. The input register's row ids are `I-D4b` and the like, and W_min is a policy lever (`drivers.md`, D3). Q10.
6. The front-matter `outputs` list in section 1 equals the S5 set in the manifest (checked: 17 ids each way).

## 9. Questions

Each has a proposed answer. The checker spec above assumes the proposal.

1. **Front matter fields.** The template front matter has no `title`, `shortcode`, `zenodo_doi`, `jel` or `keywords`. Do spokes carry them? *Proposed:* no. The question is the title. Zenodo and JEL metadata for the whitepaper set live in a registry file (017s). FM3 then rejects the old keys.
2. **Part headings and levels.** The template names the four parts but fixes only one heading text, `## Strongest objection`. *Proposed:* `## Short answer` first; Evidence sections as numbered H2s; `## Strongest objection` last; no H1; no H3 or below (Evidence stays flat, one idea per section). The Data block is never in the source.
3. **Numbering and addressing.** Section 7 of the template cites `(S5 §2)`. *Proposed:* Evidence H2s are numbered `## 1.` upward and `§N` means the Nth Evidence section. Short answer and the objection block are unnumbered; a cross-spoke pointer to either is just `(S5)`. The Short answer's pointer to its own objection is plain words ("the strongest objection, below").
4. **What fails the build, and the draft downgrade.** *Proposed:* as section 1. Errors that report counts or coverage (WC1, WC2, OB2, OB3, FM10, HK7, F4 first half) become W while `status: draft`. Syntax and identifier errors stay E. `author-review` and `accepted` are strict. `--release` makes unresolved hooks E for every status.
5. **Word counting.** *Proposed:* split on whitespace; strip Markdown markers and link URLs, keep link text; a hook is one word; a cross-reference counts its tokens as written (`(S5 §2)` is two); a hyphenated word is one; a number is one; the five bold labels are excluded, and everything after them counts. 018s should use the same function for the Data block's reading note.
6. **Reading note.** The template allows an optional note of at most 60 words but not where it lives. *Proposed:* front-matter key `reading_note:`, so it never enters counted prose.
7. **Which STAT, SCHEDULE and HORIZON an output takes.** The manifest has no field for it. *Proposed:* the checker uses this table, and the guru may later add an explicit `indexed:` field that overrides it.

   | Summary | STAT allowed | Default |
   |---|---|---|
   | `p10_mean_p90` | p10, mean, p90, range | mean |
   | `point_and_range` | point, lo, hi, range | point |
   | `point` | point | point |

   No `@SCHEDULE` where `once_not_per_schedule: true` (OH1b, OH1c) or `kind: data_fact` (DH1a to DH1c); no `/HORIZON` on `data_fact`.
8. **Selecting a line or a retired tax; citing a check.** Outputs carry `lines:` (O1, OB1, OR1, OW3, OD1, OF1, OM1) and one has `per:` (O1d, seven taxes). The grammar has no slot for them. *Proposed:* use the BAND slot with the reserved keys `line` and `per`: `{{o:OB1.mean#line:B1a}}`, `{{o:O1d.mean#per:corporation_tax}}`. No grammar change. `{{o:CK1}}` is accepted, resolved from `checks:`, and counts for R1.
9. **Band values.** The manifest lists `by:` keys but not their values (`wealth_band:top`). *Proposed:* the data layer emits a table of allowed values (`hooks.md`). Until it does, a band value is checked for form only and HK2 reports an unknown value as I.
10. **Input hooks.** Register rows are `I-D4b`; the template example is `{{i:W_min}}`. *Proposed:* hooks use register ids (`{{i:I-D4b}}`); where a spoke needs a symbol such as W_min, the register gets an alias row. The hook renders the central value; `.lo` and `.hi` select the others. Front-matter `inputs` equals the set of `{{i:}}` hooks (FM11, DB5). Do lever values, which the register may not hold, get hooks? Proposed yes, from the driver table, by the same rule; the author names the file.
11. **Literature and current-law figures.** Strict lint forbids a typed figure, so a statutory rate or a published statistic needs a source. *Proposed:* `{{lit:KEY}}` resolves in a literature-figure table (`KEY` to value, unit, bib key, page), and the bib key must exist in `registry/references.bib`. Spokes keep `(@Key)` citations for sources, and WR11 and WR12 check them. The table's format is `hooks.md`'s.
12. **F1 and the horizon length.** F1 flags "100 years". *Proposed:* a figure of three or more digits directly followed by `year` or `years` is exempt, because the horizons are vocabulary of the manifest, not results.
13. **F2 inflections.** The template list is exact forms. *Proposed:* keep it as the floor, and match the family of each word (rise, rises, rising, rose, risen; fall, falls, falling, fell; grow, grows, growing, grew; shrink and its forms; exceed and its forms; outweigh and its forms), the comparatives and `peak`, `converge` and their forms.
14. **Table id form.** *Proposed:* `F-<spoke>-<n>` everywhere (F3, the ids paragraph, the example); rule 3's `F5.1` is corrected by the guru.
15. **Cross-reference resolution.** *Proposed:* this checker validates syntax (XR1 to XR5), that the shortcode exists (XR6), and that same-spoke and present-sibling sections exist (XR7). It leaves full resolution, drift against a baseline and renumbering to `wdt_crosslinks.py`, extended by stage D to read spokes. A figure in another spoke is cited `(S6 Figure 2)` and resolves to `fig-S6-2`. A retired source (`(MF §6)`) is W.
16. **Names, locations, hub files.** *Proposed:* tool `pipeline/check_spokes.py`; spoke files in `source/spokes/` as `S5.md`, `S4-A.md`; the check runs in CI before the Quarto step. A `--hub` flag runs the hub files (H0 to H7) with part, word and objection checks off and hooks, typed-figure lint, cross-references and writing rules on. Both are `ids.md`'s to confirm.
17. **Template example.** *Proposed:* the guru changes the 6a example to an S7 figure (output OP6) or an S5 output such as OP1, and the caption drops the unit "100 years" or keeps it under Q12.
18. **Suppression.** *Proposed:* a W may be waived on one line with `<!-- spoke-check: ignore WR5 reason -->`; the reason is required, errors cannot be waived, and every waiver goes in the change report. Without a waiver mechanism WR5, WR6 and WR9 will push authors to rewrite sound prose.

## 10. Checks run

| Check | Result |
|---|---|
| Every template rule that can be checked has a check with a severity | sections 4.1 to 4.10: front matter (FM1 to FM12), shape (PT1 to PT8), budget (section 3: WC1 to WC4), objection block (section 5: OB1 to OB7), hooks and R1 (section 4: HK1 to HK17), typed figures (TF1 to TF3), figures and captions (6a: FG1 to FG10, F1 to F6, TB1), cross-references (section 7, rule 7: XR1 to XR9), writing rules (section 7: WR1 to WR12, SA1), Data block (section 6: DB1 to DB8) |
| Each check has one passing and one failing example | yes; the DB checks give a pass and a fail in the same row |
| Manual-only rules listed with the reason | section 5, 19 rules |
| Old checker's checks marked | section 7, 14 rows |
| Template front matter checked against the manifest | S5 `outputs` equals the manifest set; the 6a example block does not (section 8, point 2) |
| `git diff --stat` | `docs/restructure/site/checker.md` and the brief's progress block only |
