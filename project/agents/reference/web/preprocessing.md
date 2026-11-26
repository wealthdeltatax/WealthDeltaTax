# Preprocessing Diagnostics

Quick-reference troubleshooting for rendering problems. For how the pipeline works,
see `website/wdt-site-architecture.md` → `preprocess.py` section.

---

## `\newpage` (or `\medskip`, `\tableofcontents` etc.) appearing as literal text

The preprocessing script either wasn't run, or the LaTeX strip regex didn't match.
Check that `LATEX_RE` in `preprocess.py` includes the relevant command. Re-run
`preprocess.py` and render again.

## Cross-reference like `(VAL §3.7)` not becoming a link

Check `wdt-contents.yml` — is `VAL` in the map? Check that the shortcode in the
source matches the key exactly (case-sensitive). Check `anchors.yml` — is the
specific section key `VAL§3.7` present? If missing from anchors, re-run
`build_anchors.py` and commit the updated `anchors.yml`.

## `[WP]` internal bibliography lines rendering as raw text

`INTBIB_LINE_RE` requires the format `[SHORTCODE] Author, ...` — no space before
the bracket. Check the source file for any deviation from this format.

## Math not rendering

Quarto uses MathJax by default for HTML output. If math breaks, check that `$`
delimiters survived preprocessing intact (the script doesn't touch math).

## YAML front matter error

Quarto ignores unknown YAML keys (`documentclass`, `geometry`, etc.) but will error
on malformed YAML. Look for tabs instead of spaces, or unquoted colons in values.

## Custom styles not applying (Georgia serif, `.internal-bibliography` box)

Likely the `css:` path mismatch documented in the architecture doc (Issue 3). Check
whether `_quarto.yml` specifies `css: styles.css` or `css: style/styles.css` and
verify which path the file actually landed at in `_build/` after preprocessing.
