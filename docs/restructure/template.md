# Restructure, stage C: spoke template and writing rules

Brief 013g. Status: approved by the author 2026-11-17 (shape and rules), with stage B decisions applied (cap 6,000, appendix spokes, S4 and S6 split, ENT as S8-A) and section 6a, figures and tables, added at the author's direction. Stage D is next. No spoke or hub prose exists beyond the one test paragraph in section 8. The data gate (013g) is still shut.

**Gate (author, 2026-11-16).** No spoke prose is written until the data is finalised. The draft mode in section 4, rule 5 exists to test the build and the template, not to write spokes ahead of results.

## 1. Shape of a spoke

Every spoke answers one reader question and has four parts, in this order. A reader who stops after any part has a complete, honest answer at that depth.

| Part | What it is | Written by |
|---|---|---|
| Front matter | id, question, outputs cited, budget, depends-on | author or writing lane |
| 1. Short answer | the claim, the headline numbers (by hook), and a pointer to the objection | writing lane |
| 2. Evidence | the argument, in H2 sections; each opens with its claim | writing lane |
| 3. Strongest objection | one block, section 5 | writing lane |
| 4. Data block | generated at build from the hooks, section 6 | build |

The reader question in the front matter is the spoke's title. If a paragraph does not help answer it, it belongs in another spoke or nowhere.

### Front matter

```yaml
---
spoke: S5
question: "What rate, what threshold, how much?"
status: draft            # draft | author-review | accepted
budget: {cap: 6000}      # words of counted prose, section 3
defaults: {schedule: S_central, horizon: short}   # used by hooks that omit them
outputs: [O1, O1a, O1b, O1c, O1d, O2, O3, O5, O6, O7, O8, OP1, OP4]   # equals the S5 set in outputs.yml
inputs: [W_min]          # input-register names the prose cites
depends: [S3, S4]        # spokes whose claims this one assumes
---
```

`outputs` must equal the set of IDs whose `element:` lists this spoke in `outputs.yml` (rule R1, section 4). Shortcodes for cross-references are provisional until stage D fixes site IDs.

## 2. Parts in detail

**Short answer.** 80 to 150 words, one paragraph. Lead with the answer to the question. Give the headline figures by hook, not typed. Name the strongest objection in one clause and the horizon the numbers refer to. No history, no definitions the reader already has from the hub.

**Evidence.** H2 sections, usually three to six. Each section's first sentence is its claim. A paragraph carries one structural idea (claim, mechanism, implication, limitation). Mechanism is prose. There are no tables in the prose: a comparison a reader needs is drawn as a figure, and its numbers sit in that figure's reference table (section 6a). Figures come from figure blocks, never pasted. A caveat is stated once, where it bites, and cross-referenced elsewhere.

**Strongest objection.** Exactly one block per spoke. Lesser objections get a sentence in Evidence or a pointer to S12. Section 5.

**Data block.** Generated. The author may add one optional `reading note` of at most 60 words for how to read the numbers (for example that the long horizon is a steady-state property, not a forecast: `metrics.md`, reading rule A2). Section 6.

## 3. Word budget

Counted prose: Short answer, Evidence and Objection block text. Hooks count as one word each. Not counted: front matter, headings, figure captions, the Data block and its tables.

| Part | Range |
|---|---|
| Short answer | 80 to 150 |
| Objection block | 150 to 400 |
| Evidence | the rest |
| Whole spoke | up to 6,000 (author, 2026-11-17); no floor |

The cap is a front-matter field, so a spoke that the author allows to run longer, or that is split, changes one line. The build warns above 100% of cap and fails above 125%.

**Caps (author, 2026-11-17).** Cap 6,000 for every spoke, main or appendix. A spoke that would exceed its cap moves its less important material into an appendix spoke (id suffix `-A`, reached from the main spoke; an appendix has its own front matter, cap and Data block). S4 and S6 are split; ENT is S8-A.

| Spoke | Kept words (old) | Unit | Cap |
|---|---:|---|---:|
| S1, S2, S3, S5, S7, S11 | 5,947 to 8,580 | as the map | 6,000 |
| S8 | 9,671 | main; **S8-A** entity attribution (ENT, 6,498) | 6,000 each |
| S9, S10, S12 | 10,668 to 13,238 | as the map; test at stage E | 6,000 |
| S4 | 17,484 | valuation routes; **S4-A** declaration incentives | 6,000 each |
| S6 | 20,680 | who pays; **S6-A** what they do; **S6-B** welfare comparison | 6,000 each |

**First compression measurement.** The test paragraph (section 8) compresses a 238-word passage of the whitepaper to 125 words, a ratio of 1.9. It is one non-model paragraph and the old text is fairly padded, so it is a floor for what laconic drafting gives on prose, not a forecast for the whole. At a 6,000 cap the highest ratio of kept words to cap is S10 at 2.2, then S12 at 2.0 and S9 at 1.8 (ledger words, before removing model numbers); the split units of S4 and S6 are at or below 1.8 by the ledger's rough unit sizes. S10, S12 and S9 stay open for stage E. Model-dependent words shrink further because hooks replace typed numbers and their narration.

## 4. Data hooks

A hook is a named reference to a value in the data layer. The build replaces it with the formatted value. Authors never type a model number.

### Grammar

```
{{o:ID[.STAT][@SCHEDULE][/HORIZON][#BAND]}}     output value
{{i:NAME}}                                      input-register value
{{fig:ID[@SCHEDULE][/HORIZON]}}                 figure from an output
{{lit:KEY}}                                     literature figure, keyed to the reference database
```

| Field | Values | Default |
|---|---|---|
| `ID` | an `id` in `outputs.yml` (O1, O1a to O1d, O2, O2b, O2c, O3, O4a, O4b, O5 to O8, OP1, OP3 to OP6, OS1) | none; required |
| `STAT` | `p10`, `mean`, `p90`, `range` (renders "p10 to p90"), `point`, `lo`, `hi` | `mean` for `p10_mean_p90` outputs; `point` for `point_and_range` outputs |
| `SCHEDULE` | `S_low`, `S_central`, `S_high` (from `outputs.yml` `schedules`) | front-matter `defaults.schedule` |
| `HORIZON` | `transition`, `short`, `long` (from `horizons`) | front-matter `defaults.horizon` |
| `BAND` | a key from the output's `by:` list, `key:value`, for example `wealth_band:top` or `overall` | `overall` where the output has one; otherwise the hook is an error |

Examples: `{{o:O1.range@S_central/short}}`, `{{o:O2.mean#overall}}`, `{{o:OP1.p90@S_low/transition}}`, `{{i:W_min}}`, `{{fig:OP6@S_central}}`.

Units, rounding and the "p10 to p90" wording come from the metric register, never from the author. A hook inside a sentence reads as the value alone, so the sentence has to work with "x%" or "x to y%" in the slot.

### Rules the build enforces (stage D builds them; stage C fixes them)

1. **Unknown ID is an error.** The ID, `STAT`, `SCHEDULE`, `HORIZON` and `BAND` must all exist in the manifest.
2. **R1, forward.** A hook to an output whose `element:` does not list this spoke is an error. Fix the manifest or drop the hook.
3. **R1, reverse.** An output whose `element:` lists this spoke and that no hook cites is an error. The output either belongs elsewhere or the spoke is incomplete.
4. **No typed model numbers.** Any figure in prose that is a model result or input value is a lint error. The lint flags percentages, currency amounts, decimals and numbers of three or more digits outside hooks, headings, years and section references. Small structural counts are written as words ("six taxes are retired"). A figure from the literature is entered through `{{lit:KEY}}` so it carries its source.
5. **Draft versus release.** Until the data gate opens, a hook to a value with no run renders as `[[O2.mean@S_central/short]]` and the page is marked draft. A release build fails on any unresolved hook.
6. **Horizon discipline.** A claim about the long horizon is worded as a steady-state property, not a forecast, and the long value never appears in a Short answer without the short one beside it (author, 2026-11-16, `metrics.md` reading rule A2).

## 5. The objection block

One per spoke. It states the objection at full strength, as a holder of it would, before any reply.

```markdown
## Strongest objection

**Objection.** [The strongest version, 60 to 150 words, in the objector's terms.
No strawman. Use a hook if the objection rests on a number.]

**Held by.** [A named source from the literature, or "no one has put this in print;
it is the sceptic's obvious point".]

**Response.** [Up to 200 words. What the design does about it, with hooks for
numbers. Say where the response is a trade-off.]

**Status.** [Exactly one: open question | named compromise | empirical.]
[One sentence on what that means here.]

**What would change the answer.** [A condition, or a pointer: (S12 ...).]
```

Labels follow the style guide: *open question* is work nobody has done, assigned to a future paper and to SCOPE if outside the project; *named compromise* is a trade-off already accepted and stated; *empirical* is what only implementation can settle. The response never claims more than the label allows. "What would change the answer" points at the falsification item in S12 where one exists.

## 6. The Data block

Generated from the hooks the spoke uses. It lets a reader or economist check every number without leaving the page, and it is the only place the run and inputs are named.

| Row | Content |
|---|---|
| Outputs cited | one line per output ID: title, `STAT`, schedule, horizon, value with unit |
| Figures | one row per figure: id, outputs plotted, schedule, horizon, link to its reference table and CSV |
| Reference tables | one table per figure (section 6a), holding every value plotted |
| Run | manifest `version`, `country_pack`, run date |
| Inputs | each `{{i:}}` name, value, unit, register entry link |
| Literature figures | each `{{lit:}}` key with its source |
| Reading note | the author's optional note, at most 60 words |
| Replicate | link to the data-layer page for each output |

The block has no prose the author must keep in step with the text. A hook added to the body appears in the block at the next build.

## 6a. Figures and tables (author, 2026-11-17)

Three rules, then the mechanism.

1. **Every figure has a reference table in the Data block.** The table holds every value the figure plots, with unit, `STAT`, schedule and horizon. The build draws the figure and the table from the same data, so they cannot disagree. Each table also downloads as CSV.
2. **A caption describes the figure and states no result.** It says what is plotted: the quantity, axes and units, the series, the schedule, the horizon, and what bands or markers mean. It never says what the figure shows, and it carries no model number. The prose states the result, by hook, and cites the figure.
3. **No table in the prose.** Tables live only in the Data block, and each is referenced from its figure's caption (`Data: Table F5.1`). A comparison a reader needs is drawn as a figure, so its numbers become that figure's reference table. A list that is not data (the six retired taxes, say) is prose.

**Figure block** (replaces the `{{fig:}}` hook; the hook now only cites a figure in prose):

````
::: {#fig-S5-1}
output: [OP6]            # ids in outputs.yml; every one must be in this spoke's set
kind: line               # line | band | bar | dot | map | stack
schedule: S_central      # one value, or [S_low, S_central, S_high] to draw all three
horizon: long
by: overall              # a `by:` key of the output, where it has one
caption: "Public wealth path (fund assets, share of GDP) over 100 years, central schedule. Line is the mean; shaded band runs from the 10th to the 90th percentile of return risk. Data: Table F-S5-1."
alt: "Line chart of fund assets as a share of GDP against year, with a shaded range."
:::
````

IDs: figure `fig-<spoke>-<n>`, its table `F-<spoke>-<n>`. The prose cites with `{{ref:fig-S5-1}}`, which renders "Figure 1" and links. Appendix spokes use their own id (`fig-S6-A-1`).

**Drawing rules.** A `p10_mean_p90` output is drawn as the mean with a band from p10 to p90, and the table lists all three. A figure that compares schedules draws all three and says so in the caption. Money is in base-year pounds, as the metric register states. One palette and one style across the series (stage D fixes them with the `dataviz` guidance). Alt text describes the form of the chart, never the finding.

**Caption lint** (stage D builds it; until then the writing lane checks by hand):
- F1. A caption contains no `{{o:}}`, `{{i:}}` or `{{lit:}}` hook and no figure of three or more digits other than years and IDs.
- F2. A caption contains none of the result words: rises, falls, grows, shrinks, exceeds, outweighs, shows that, demonstrates, confirms, higher, lower, larger, smaller, peaks, converges. The list lives in the checker and can grow.
- F3. A caption ends with `Data: Table F-<spoke>-<n>` and that table exists in the Data block.
- F4. Every figure block is cited by `{{ref:}}` at least once in the prose, and the sentence that cites it states the result with a hook.
- F5. Every output named in a figure block is in the spoke's `outputs` set (rule R1) and counts as cited for the reverse check.
- F6. The Data block lists every figure and every reference table; a table in the prose is an error.

## 7. Writing rules

The writing lane applies `docs/agents/reference/writing/style-guide.md` and `prose-rules.md` in one pass while drafting. For spokes this adds:

1. **Draft compressed.** Lead with the point. No preamble, no closing restatement, no reflexive hedging.
2. **Prose first.** Bullets only where the reader follows a sequence. No tables in the prose; figures follow section 6a.
3. **State positions in the present tense.** No account of earlier versions, no "has since been", no revision narrative inside a spoke.
4. **One caveat, once.** Name it where it bites and cross-reference it.
5. **Name trade-offs.** Where the design departs from its principle, say so.
6. **Hedge with a condition.** Say under what condition a claim fails, not that it might.
7. **Cross-references** carry the shortcode and are fully bracketed: `(S5)`, `(S5 §2)`, `(MF §6)` for a retired source if a spoke must cite one. Never a bare section sign. Spoke shortcodes are provisional until stage D.
8. **Do not oversell.** A spoke undercuts its strongest claim with a direct statement of what is unproven.
9. **No em dashes, no "genuine", no decorative intensifiers, no "not X but Y" for plain claims.** Uneven paragraph length is allowed.
10. **A spoke stands alone.** It defines in a clause any term it needs; it does not assume the reader came through the hub, and it does not re-explain what the hub or another spoke explains. Link instead.
11. **Never invent** a figure, quote, citation or DOI. Mark anything unverified.
12. **Check.** Spokes use a new checker; `check_wdt_format.py` is for the old paper shape. The spoke checker is a stage D task. Until it exists, the writing lane checks shape, budget and hook syntax by hand against this file.

The hub (H0 to H7) follows rules 1 to 12 and its own outline in `map.md`; it does not use the four-part shape.

## 8. Test paragraph

Test only. It is not spoke text and is not to be reused as written. Spoke S3, Evidence section on the symmetric refund. Source: whitepaper §3.5, first three paragraphs (238 words). Draft: 125 words. No model numbers, so no hooks.

> Most tax systems take a share of a rise in wealth and leave the whole of a fall with the holder. That penalises founders whose wealth moves with one illiquid asset, and it gives them reason to restructure, delay realisation or leave. The WDT treats gains and losses alike: a loss year is refunded at the marginal rate an equivalent gain would have paid, so the state shares the downside. Refunds sit inside a lifetime envelope. Total refunds to a person cannot exceed the total tax they have paid, because without the cap the WDT would insure failed speculation instead of sharing a contribution history. If cumulative refunds ever exceed cumulative tax, later gains repay the excess before ordinary liability resumes. Early repayment is allowed.

What the test shows: the old text's worked 25% example is dropped because the rate is a schedule parameter and belongs to a hook if a spoke needs it. Content kept: asymmetry problem, symmetry rule, cap and its reason, repayment, early repayment. Content left for later paragraphs: the envelope as cooperative stake, the distributional consequence, the inheritance reset.

## 9. Checks run

| Check | Result |
|---|---|
| Shape defined: four parts, order, front matter | section 1 and 2 |
| Word budget defined and counted | section 3 |
| Data-hook syntax defined | section 4 |
| Objection block defined | section 5 |
| Data block defined | section 6 |
| One paragraph written as a test only | section 8 |
| Hook grammar checked against `outputs.yml` | examples in section 4 parsed; IDs, schedules and horizons exist |

## 10. For the author

All approved by the author on 2026-11-17: the shape, the single-objection rule, the 60-word reading note, the long value never alone in a Short answer, and strict lint on typed figures including `{{lit:}}`. The cap (6,000, appendix spokes) is closed. Added the same day: section 6a, figures and tables.

Open for the author on 6a: (a) a caption's result-word list (F2) is a lint, so it will miss some phrasings; the writing lane reviews captions by hand too. (b) A table that is not data and not a figure's source (for example a list of statutory dates in S9) is read as prose or an appendix spoke; say if you want a table type for it. (c) Stage D then fixes site IDs, URLs, hook mechanics, the figure renderer and the spoke checker.
