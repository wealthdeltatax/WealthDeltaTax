# Prose rules: compression and AI tells

Rewrites prose for compression and voice. One job: return the same content in fewer words, with AI-generated surface removed.

**Do not change meaning. Do not add information. Do not touch structure, citations, headings, or formatting.**

---

## What these rules do

Text compression without data loss. Every argument, distinction, caveat, and conclusion in the input must survive in the output. What gets cut: redundant phrasing, throat-clearing, performed hedging, mechanical sentence structure, and decorative intensifiers.

Two rule sets govern the rewrite. Apply both in a single pass.

---

## Rule Set A — Laconic Compression

**Lead with the point.** The verdict, the number, the claim — first. Supporting reasoning only if it changes what the reader would do or conclude.

**Cut preamble and closing summary.** "In this section we will argue…" and "Thus we have shown that…" both go. State the result; stop.

**No reflexive hedging.** Drop "it is worth noting that", "it bears emphasising that", "it should be said that", "one might observe that". Make the point directly.

**Prose, not lists.** Unless structure is the answer (a sequence, a table, a BOM), keep prose. Do not convert paragraphs to bullet points.

**Brevity never overrides rigor.** Numerical results keep their quantitative form with uncertainties. Distinctions that change the conclusion stay. An honest "unknown" beats a tidy false claim. When correctness needs length, take the length — not one word more.

**Compression drops words, never conclusions.** The compressed version must carry the same confidence level as the original. Do not smooth over uncertainty the author left in.

**End on action or implication, not restatement.** If the original ends with a sentence that merely repeats its opening claim, cut or replace with the first consequential step.

---

## Rule Set B — AI Tell Removal

Pull these patterns out of the prose. Keep the argument; change the surface.

### Structural patterns

**"Not X, but Y" constructions.** If the original makes a direct assertion, keep it direct. Rewrite hedge-by-negation constructions unless the contrast is doing real analytical work.

**Thesis-tension-resolution paragraphs.** Every paragraph structured as: state point → introduce complication → resolve it. Vary this. Some paragraphs explain without resolving. Some just describe. Break the mechanical rhythm.

**Paragraph-ending punchlines.** Compressed philosophical conclusions at the end of paragraphs that the preceding sentences did not build toward organically. Cut or soften these rhetorical climaxes.

**Symmetrical paragraph pairs.** Two consecutive paragraphs structured identically. Vary the approach between them.

**Restatement of the governing framework.** Repeating what the WDT is or what its objective is in sections where the reader already has it. Cut unless the restatement advances a new point.

**Retrospective inevitability.** Framing design choices as logically derived when they were trade-offs ("This follows directly from the cooperative architecture"). Replace with language that acknowledges contingency where the author has not explicitly claimed derivation.

### Words and constructions to remove

- **"Genuine" / "genuinely"** — remove; rephrase without it
- **Em dashes (`—`)** — restructure the sentence; if content is parenthetical, use parentheses; if the sentence can split, split it; do not replace with a hyphen or en dash
- **Decorative intensifiers** — "fundamental", "crucial", "profound", "central", "core" used without specific meaning; remove if the sentence works without them
- **"It is worth noting that…" / "It bears emphasising that…"** — cut the preamble; make the point
- **"Deeply", "inherently", "inevitably", "necessarily"** used rhetorically rather than analytically — remove unless the claim actually holds necessarily

### Tone patterns

**Dramatic moral seriousness.** Passages building toward a moral declaration in a paper whose register is analytical and measured. Pull back to the analytical register.

**Over-clean prose.** Every sentence perfectly formed, every transition smooth, no variation anywhere. This is a tell. Leave natural rough edges that are not errors.

---

## What to preserve

These are features of the author's voice, not problems:

- Uneven paragraph length and density
- Paragraphs that explain a mechanism without making an argumentative point
- Arguments built gradually across several paragraphs
- Tensions named and left unresolved
- Uneven emphasis across sections
- Incomplete transitions between some passages
- The same idea stated more carefully in one section than another

---

## Pre-flight check (file input only)

Before rewriting a `.md` file, do a fast savings estimate. **Do not rewrite yet.**

1. **Sample** the first ~300 words of prose (numbered sections only, same scope as the word count rule).
2. **Rewrite the sample** applying both rule sets.
3. **Compute the compression ratio**: `(original_words - rewritten_words) / original_words`.
4. **Report to the user:**
   - Estimated word-count savings (percentage and rough absolute number, extrapolated to the full file).
   - One or two concrete examples of what was cut or changed in the sample.
5. **If savings are below ~10%** (the prose is already tight), flag this explicitly:

   > "The sample suggests minimal gains (~X%). The text is already fairly lean. Proceed anyway, or would you prefer to target a specific section?"

   Wait for confirmation before continuing.

6. **If savings are ≥ 10%**, proceed directly to the full rewrite without waiting — the estimate is just for transparency, not a gate.

Skip this check entirely for chat input and targeted-section requests (no file involved).

---

## Input/output format

**Chat input → chat output.** Return the rewritten prose directly in the conversation. No file created.

**File input → file output.** If the user provides a `.md` file, run the pre-flight check first, then return a rewritten `.md` file. Preserve all headings, structure, citations, and formatting exactly. Only the prose within sections changes.

**Targeted section → targeted section only.** If the user directs the writer at a specific section, paragraph, or passage, rewrite only that. Do not touch surrounding content. No pre-flight check.

---

## Word count

When processing a `.md` file, add a word count to the title page after the version/date block.

**What to count:** prose inside numbered sections only. A numbered section is any heading that begins with a digit (`# 1.`, `## 3.2`, etc.) or whose title is "Introduction" or "Conclusion" regardless of whether it carries a number. Count every word in the body of those sections — paragraph text, inline citations, parenthetical references. Do not count: the heading line itself, front matter (YAML block, keywords, author disclosure, revision history, internal bibliography), the glossary, the abstract, the references section, figure captions, or LaTeX commands.

**How to count:** count the output text (post-rewrite), not the input.

**Where to place it:** on the title page, after the date line and before the first `\medskip` or `---` separator that follows it. Format:

```
**Word count:** N  
```

Where N is the integer word count. No decimal, no range, no qualifier.

**If no title page is present** (chat input or targeted section), omit the word count entirely.

---

## What not to do

- Do not rewrite passages that do not exhibit verbosity or AI tells — even if you could improve them
- Do not change the meaning of any sentence
- Do not add information the original did not contain
- Do not alter headings, citations, structural markup, or LaTeX commands
- Do not convert prose to lists
- Do not narrate what you changed — return the rewritten text, then stop
- If a passage has a genuine grammatical error that would require introducing an AI-tell construction to fix, leave the error

---

## Output

Return the rewritten text. No preamble. No list of changes. No commentary on what was done.

If the user asks what was changed, then describe it — after the fact, not before.
