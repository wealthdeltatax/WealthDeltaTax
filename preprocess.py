"""
WDT site preprocessing pipeline.
Reads .md source files, processes them for HTML rendering, writes .qmd to _build/.
Run this before every `quarto render _build`.

Steps:
  1. Strip LaTeX artifacts
  2. Convert cross-references to hyperlinks
  3. Convert internal bibliography lines to styled divs
  4. Inject per-paper front matter metadata (description, keywords, date, version)
  5. Inject JSON-LD structured data (ScholarlyArticle) into each paper
  6. Auto-generate corpus.qmd from wdt_references.json
  7. Copy static assets and hand-authored pages into _build/
"""

import re, shutil, json
from pathlib import Path
from datetime import datetime
import yaml
import os
os.chdir(Path(__file__).parent)

# ── CONFIGURATION ────────────────────────────────────────────────────────────
SOURCE_DIR      = "source_md"
BUILD_DIR       = "_build"
SERIES_YML      = "series.yml"
ANCHORS_YML     = "anchors.yml"
REFERENCES_JSON = "wdt_references.json"
SITE_URL        = "https://wealthdeltatax.org"
AUTHOR          = "K. Ogata"
# ─────────────────────────────────────────────────────────────────────────────

# ---------------------------------------------------------------------------
# Load series.yml  link_map[SHORTCODE] = "page.html"
# Load anchors.yml  anchor_map[SHORTCODE§X.Y] = "page.html#anchor-id"
# Load wdt_references.json  paper_meta[SHORTCODE] = {...}
# ---------------------------------------------------------------------------

with open(SERIES_YML, encoding='utf-8') as f:
    series = yaml.safe_load(f)

link_map = {}
for shortcode, paper in series.items():
    link_map[shortcode] = paper['page']

with open(ANCHORS_YML, encoding='utf-8') as f:
    anchor_map = yaml.safe_load(f)

print(f"anchor_map sample: {list(anchor_map.items())[:5]}")
print(f"anchor_map size: {len(anchor_map)}")

paper_meta = {}
if Path(REFERENCES_JSON).exists():
    with open(REFERENCES_JSON, encoding='utf-8') as f:
        refs_data = json.load(f)
    for p in refs_data.get('internal_papers', []):
        paper_meta[p['shortcode']] = p
    print(f"Loaded metadata for {len(paper_meta)} papers from {REFERENCES_JSON}")
else:
    print(f"  ! {REFERENCES_JSON} not found — skipping metadata injection")

# ---------------------------------------------------------------------------
# Cross-reference conversion
# ---------------------------------------------------------------------------

CROSSREF_RE = re.compile(
    r'\(([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)(?:\s+§([\d.A-Za-z]+))?\)'
    r'|'
    r'\b([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\s+§([\d.A-Za-z]+)'
)


def convert_crossrefs(text):
    def replace(m):
        shortcode = m.group(1) or m.group(3)
        section   = (m.group(2) or m.group(4) or '').rstrip('.')
        full      = m.group(0)

        if shortcode not in link_map:
            return full

        if section:
            key = f'{shortcode}§{section}'
            url = anchor_map.get(key)
            if url:
                return f'[{full}]({url})'
            print(f'  ⚠ section not in anchors.yml: {key}')
            return f'[{full}]({link_map[shortcode]})'

        return f'[{full}]({link_map[shortcode]})'

    return CROSSREF_RE.sub(replace, text)


# ---------------------------------------------------------------------------
# LaTeX artifact stripping
# ---------------------------------------------------------------------------

LATEX_STRIP = [
    r'\\newpage', r'\\medskip', r'\\bigskip', r'\\smallskip',
    r'\\tableofcontents', r'\\appendix', r'\\maketitle',
    r'\\begin\{center\}', r'\\end\{center\}',
    r'\\noindent', r'\\clearpage',
    r'\\vspace\*?\{[^}]+\}', r'\\hspace\*?\{[^}]+\}',
    r'\\setcounter\{[^}]+\}\{[^}]+\}',
]
LATEX_RE = re.compile('|'.join(LATEX_STRIP))


# ---------------------------------------------------------------------------
# Internal bibliography conversion
# ---------------------------------------------------------------------------

INTBIB_LINE_RE = re.compile(r'^\[([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\]\s+(.+)$')


def convert_internal_bibliography(lines):
    result, in_block = [], False
    for line in lines:
        m = INTBIB_LINE_RE.match(line.rstrip())
        if m:
            if not in_block:
                result.append('\n::: {.internal-bibliography}\n')
                in_block = True
            code, rest = m.group(1), m.group(2)
            result.append(f'**[{code}]** {rest}\n')
        else:
            if in_block:
                result.append(':::\n')
                in_block = False
            result.append(line)
    if in_block:
        result.append(':::\n')
    return result


# ---------------------------------------------------------------------------
# Front matter metadata injection
# ---------------------------------------------------------------------------

YAML_FENCE_RE = re.compile(r'^---\s*\n(.*?)^---\s*\n', re.DOTALL | re.MULTILINE)


def _format_date(raw_date):
    """Convert YYMMDD (e.g. 260815)  YYYY-MM-DD (e.g. 2026-08-15)."""
    if not raw_date or len(str(raw_date)) != 6:
        return None
    s = str(raw_date)
    try:
        return f"20{s[0:2]}-{s[2:4]}-{s[4:6]}"
    except Exception:
        return None


def inject_front_matter(text, shortcode):
    """Enrich or create YAML front matter with metadata from paper_meta."""
    meta = paper_meta.get(shortcode)
    if not meta:
        return text

    fm_match = YAML_FENCE_RE.match(text)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1)) or {}
        except Exception:
            fm = {}
        body = text[fm_match.end():]
    else:
        fm = {}
        body = text

    if 'description' not in fm:
        fm['description'] = meta.get('title', '')

    if 'author' not in fm:
        fm['author'] = AUTHOR

    if 'date' not in fm:
        iso = _format_date(meta.get('version_date'))
        if iso:
            fm['date'] = iso

    if 'version' not in fm:
        fm['version'] = meta.get('version', '')

    if 'keywords' not in fm:
        related = meta.get('outbound_internal', [])[:4]
        kws = ['Wealth Delta Tax', 'WDT', shortcode] + related
        fm['keywords'] = ', '.join(kws)

    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True,
                       sort_keys=False)
    return f'---\n{new_fm}---\n{body}'


# ---------------------------------------------------------------------------
# JSON-LD structured data injection
# ---------------------------------------------------------------------------

def build_jsonld(shortcode):
    """Return a Quarto raw HTML block containing JSON-LD for this paper."""
    meta = paper_meta.get(shortcode)
    if not meta:
        return ''

    page_html = link_map.get(shortcode, f'{shortcode.lower()}.html')
    url       = f'{SITE_URL}/{page_html}'
    title     = meta.get('title', shortcode)
    version   = meta.get('version', '')
    iso_date  = _format_date(meta.get('version_date')) or ''

    related = meta.get('outbound_internal', [])
    related_urls = []
    for r in related:
        rpage = link_map.get(r)
        if rpage:
            related_urls.append(f'{SITE_URL}/{rpage}')

    ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": title,
        "author": {
            "@type": "Person",
            "name": AUTHOR
        },
        "url": url,
        "isPartOf": {
            "@type": "Book",
            "name": "The Wealth Delta Tax Research Programme",
            "url": SITE_URL
        },
        "version": version,
        "keywords": ["Wealth Delta Tax", "WDT", "wealth taxation", shortcode],
    }
    if iso_date:
        ld["dateModified"] = iso_date
    if related_urls:
        ld["relatedLink"] = related_urls

    ld_json = json.dumps(ld, indent=2, ensure_ascii=False)

    return (
        '\n```{=html}\n'
        f'<script type="application/ld+json">\n{ld_json}\n</script>\n'
        '```\n'
    )


# ---------------------------------------------------------------------------
# Corpus page generation
# ---------------------------------------------------------------------------

SECTION_ORDER = [
    ("Core Papers",              ["WP", "MF"]),
    ("Literature",               ["LR", "LR.A", "LR.B", "JUR"]),
    ("Valuation",                ["VAL", "VAL.A", "VAL.B"]),
    ("Corporate & Governance",   ["CORP", "CORP.A", "GOV", "GOV.A", "GOV.B"]),
    ("Revenue & Behaviour",      ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A", "BEHAV"]),
    ("Implementation",           ["CLOSE", "PHASE1"]),
    ("Analysis",                 ["POL", "ENV", "FM", "MOD"]),
    ("Reference",                ["SCOPE"]),
]


def _yymmdd_to_display(raw):
    """260815  15 Aug 2026"""
    iso = _format_date(raw)
    if not iso:
        return '—'
    try:
        dt = datetime.strptime(iso, '%Y-%m-%d')
        return dt.strftime('%-d %b %Y')
    except Exception:
        try:
            dt = datetime.strptime(iso, '%Y-%m-%d')
            return dt.strftime('%d %b %Y').lstrip('0')
        except Exception:
            return iso


def generate_corpus_qmd(dest_path):
    """Write corpus.qmd to dest_path."""
    lines = []

    lines.append('---')
    lines.append('title: "Papers"')
    lines.append('description: "Complete index of the Wealth Delta Tax research programme — all papers with version history and relationships."')
    lines.append(f'author: "{AUTHOR}"')
    lines.append('---')
    lines.append('')
    lines.append(
        'This page is the authoritative index of the Wealth Delta Tax research programme. '
        'The HTML versions of these papers, as published at this site, are the current '
        'authoritative versions. Version numbers and dates are updated on each revision.'
    )
    lines.append('')
    lines.append(f'The programme currently comprises **{len(paper_meta)} working papers**.')
    lines.append('')

    # Collection-level JSON-LD
    collection_ld = {
        "@context": "https://schema.org",
        "@type": "Collection",
        "name": "The Wealth Delta Tax Research Programme",
        "url": SITE_URL,
        "author": {"@type": "Person", "name": AUTHOR},
        "hasPart": []
    }
    for sc, meta in paper_meta.items():
        page = link_map.get(sc, f'{sc.lower()}.html')
        collection_ld["hasPart"].append({
            "@type": "ScholarlyArticle",
            "name": meta.get('title', sc),
            "url": f'{SITE_URL}/{page}',
            "version": meta.get('version', '')
        })

    ld_json = json.dumps(collection_ld, indent=2, ensure_ascii=False)
    lines.append('```{=html}')
    lines.append(f'<script type="application/ld+json">\n{ld_json}\n</script>')
    lines.append('```')
    lines.append('')

    for section_name, shortcodes in SECTION_ORDER:
        present = [s for s in shortcodes if s in link_map]
        if not present:
            continue

        lines.append(f'## {section_name}')
        lines.append('')
        lines.append('| Paper | Title | Version | Updated | Status |')
        lines.append('|-------|-------|---------|---------|--------|')

        for sc in present:
            page   = link_map[sc]
            meta   = paper_meta.get(sc, {})
            title  = meta.get('title', sc).replace('The Wealth Delta Tax: ', '')
            ver    = meta.get('version', '—')
            date   = _yymmdd_to_display(meta.get('version_date'))
            status = meta.get('status', '—')
            status_label = {
                'active':     '✓ Active',
                'superseded': '↩ Superseded',
                'draft':      '⚙ Draft',
            }.get(status, status)

            lines.append(f'| [{sc}]({page}) | {title} | v{ver} | {date} | {status_label} |')

        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## Reading dependencies')
    lines.append('')
    lines.append(
        'Most papers assume familiarity with the [White Paper (WP)](wp.html). '
        'The valuation appendices (VAL.A, VAL.B) assume familiarity with [VAL](val.html). '
        'The governance appendices (GOV.A, GOV.B) assume familiarity with [GOV](gov.html). '
        'The rates appendix (RATES.A) assumes familiarity with [RATES](rates.html).'
    )
    lines.append('')
    lines.append(
        'For first-time readers, the recommended sequence is: '
        '[WP](wp.html) → [MF](mf.html) → [VAL](val.html) → '
        '[GOV](gov.html) → [RATES](rates.html). '
        'See also the [Start Here](start-here.html) guide.'
    )
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## About this index')
    lines.append('')
    lines.append(
        'This page is generated automatically from the project reference database '
        'at each site build. The HTML papers at this site are the authoritative '
        'current versions; PDF versions archived at Zenodo may lag by one or more revisions.'
    )

    dest_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  ✓ Generated corpus.qmd ({len(paper_meta)} papers)')

# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(src_path, dest_path):
    text = src_path.read_text(encoding='utf-8')
    text = LATEX_RE.sub('', text)
    text = convert_crossrefs(text)
    lines = convert_internal_bibliography(text.splitlines(keepends=True))
    text = ''.join(lines)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(text, encoding='utf-8')
    print(f'  ✓ {src_path.name} → {dest_path.name}')

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    build  = Path(BUILD_DIR)
    source = Path(SOURCE_DIR)

    if build.exists():
        shutil.rmtree(build, ignore_errors=True)
    build.mkdir(exist_ok=True)

    static_files = [
        '_quarto.yml', 'styles.css', 'wdt_references.bib',
        'index.qmd', 'apa.csl', 'series.yml',
        'robots.txt',
        'start-here.qmd',
        'glossary.qmd', 'faq.qmd',
    ]
    for fname in static_files:
        p = Path(fname)
        if p.exists():
            shutil.copy(p, build / fname)
        else:
            if fname not in ('wdt_references.bib', 'series.yml'):
                print(f'  ! Missing: {fname}')

    generate_corpus_qmd(build / 'corpus.qmd')

    registry_path = Path('paper_registry.yml')
    if not registry_path.exists():
        print('ERROR: paper_registry.yml not found.')
        return

    with open(registry_path, encoding='utf-8') as f:
        registry = yaml.safe_load(f)

    found, missing = 0, 0
    for entry in registry:
        shortcode   = entry['shortcode']
        source_glob = entry['source_glob']
        output_name = entry['output']

        matches = sorted(source.glob(source_glob))
        if not matches:
            print(f'  – {shortcode}: no file found (skipped)')
            missing += 1
            continue
        if len(matches) > 1:
            print(f'  ! {shortcode}: multiple matches, using {matches[-1].name}')

        process_file(matches[-1], build / output_name)
        found += 1

    print(f'\nDone. {found} papers staged, {missing} not yet available.')
    print(f'Run: quarto render {BUILD_DIR}')


if __name__ == '__main__':
    main()
