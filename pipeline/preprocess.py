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
  6. Auto-generate corpus.qmd from references.json
  7. Auto-generate references.qmd — flat bibliography with cited-in links
  8. Copy static assets and hand-authored pages into _build/
  9. Copy machine-readable data files (references.json, anchors.yml,
    contents.yml) into _build/ as static endpoints
  10. Generate site-index.json — merged single-fetch navigation index
    (papers + sections + anchor URLs + relationships)
  11. Generate flowcharts.qmd — WDT and UK comparison diagrams with
    click directives injected from anchor_map
"""

import re, shutil, json
from pathlib import Path
from datetime import datetime, timezone
import yaml
import os
from pathlib import Path

# ── CONFIGURATION ────────────────────────────────────────────────────────────
SCRIPT_DIR      = Path(__file__).resolve().parent   # wdt-site/pipeline/
ROOT_DIR        = SCRIPT_DIR.parent                  # wdt-site/

SITE_DIR        = ROOT_DIR / 'site'                  # hand-authored pages, style, _quarto.yml
SOURCE_DIR      = ROOT_DIR / 'source'                # paper .md source files
BUILD_DIR       = ROOT_DIR / '_build'                # fully generated; never edit directly

CONTENTS_YML    = ROOT_DIR / 'registry' / 'contents.yml'
ANCHORS_YML     = ROOT_DIR / 'registry' / 'anchors.yml'
REFERENCES_JSON = ROOT_DIR / 'registry' / 'references.json'
REGISTRY_YML    = ROOT_DIR / 'registry' / 'papers.yml'
DIAGRAMS_DIR    = SITE_DIR / 'diagrams'

SITE_URL        = "https://wealthdeltatax.org"
AUTHOR          = "K. Ogata"
# ─────────────────────────────────────────────────────────────────────────────

# Load registry/contents.yml    contents[SHORTCODE] = {page, title, sections}
#                                link_map[SHORTCODE] = "page.html"
# Load registry/anchors.yml     anchor_map[SHORTCODE§X.Y] = "page.html#anchor-id"
# Load registry/references.json  paper_meta[SHORTCODE] = {...}

if not CONTENTS_YML.exists():
    raise FileNotFoundError(f"contents.yml not found at {CONTENTS_YML}")
with open(CONTENTS_YML, encoding='utf-8') as f:
    contents = yaml.safe_load(f)

link_map = {}
for shortcode, paper in contents.items():
    link_map[shortcode] = paper['page']

with open(ANCHORS_YML, encoding='utf-8') as f:
    anchor_map = yaml.safe_load(f)

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
    status    = meta.get('status', 'active')

    # Collect all related internal paper URLs: outbound + inbound, deduped
    related_codes = list(dict.fromkeys(
        meta.get('outbound_internal', []) + meta.get('inbound_internal', [])
    ))
    related_urls = []
    for r in related_codes:
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
        "creativeWorkStatus": status,
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
# References page generation
# ---------------------------------------------------------------------------

def _ref_link(ref):
    """Return a markdown link string for a reference, or None if no URL/DOI."""
    doi = ref.get('doi')
    url = ref.get('url')
    if doi:
        return f'https://doi.org/{doi}'
    if url:
        return url
    return None


def _format_authors(authors):
    """Format author list as 'Last, F., Last, F. & Last, F.'"""
    if not authors:
        return '—'
    parts = []
    for a in authors:
        last  = a.get('last', '')
        first = a.get('first', '')
        if first:
            parts.append(f'{last}, {first[0]}.')
        else:
            parts.append(last)
    if len(parts) == 1:
        return parts[0]
    return ', '.join(parts[:-1]) + ' & ' + parts[-1]


def _ref_type_label(ref_type):
    return {
        'journal_article':    'Article',
        'book':               'Book',
        'book_chapter':       'Book chapter',
        'working_paper':      'Working paper',
        'report':             'Report',
        'institutional_report': 'Institutional report',
        'preprint':           'Preprint',
        'misc':               'Misc',
    }.get(ref_type, ref_type or '—')


def _cited_in_labels(ref_id, citations):
    """Return sorted list of paper shortcodes that cite this reference."""
    # citation IDs are "{ref_id}__{paper_id}" — extract paper_id from each match
    paper_ids = sorted({
        c['paper_id']
        for c in citations
        if c['ref_id'] == ref_id
    })
    return paper_ids


def generate_references_qmd(dest_path, refs_data):
    """Write references.qmd — flat alphabetical list of all external references."""
    external_refs = refs_data.get('external_references', [])
    citations     = refs_data.get('citations', [])

    # Sort alphabetically by first author last name, then year
    def sort_key(r):
        authors = r.get('authors', [])
        first_last = authors[0].get('last', 'ZZZ') if authors else 'ZZZ'
        return (first_last.lower(), r.get('year', 0))

    sorted_refs = sorted(external_refs, key=sort_key)

    lines = []
    lines.append('---')
    lines.append('title: "External References"')
    lines.append('description: "Complete bibliography of external sources cited across the Wealth Delta Tax research programme."')
    lines.append(f'author: "{AUTHOR}"')
    lines.append('---')
    lines.append('')
    lines.append(
        f'This page lists all {len(external_refs)} external sources cited across the '
        'Wealth Delta Tax research programme. Each entry shows which papers cite it. '
        'Links go to the DOI or publisher page where available.'
    )
    lines.append('')
    lines.append(
        'The full reference database including citation relationships is available as '
        '[machine-readable JSON](/references.json).'
    )
    lines.append('')
    lines.append('---')
    lines.append('')

    for ref in sorted_refs:
        ref_id   = ref['id']
        authors  = _format_authors(ref.get('authors', []))
        year     = ref.get('year', '—')
        title    = ref.get('title', '—')
        rtype    = _ref_type_label(ref.get('type'))
        link     = _ref_link(ref)
        verified = ref.get('verified', False)

        # Journal/publisher info
        details_parts = []
        if ref.get('journal'):
            details_parts.append(f'*{ref["journal"]}*')
            if ref.get('volume'):
                vol = ref['volume']
                iss = ref.get('issue')
                details_parts.append(f'*{vol}*({iss})' if iss else f'*{vol}*')
            if ref.get('pages'):
                details_parts.append(ref['pages'])
        elif ref.get('publisher'):
            details_parts.append(ref['publisher'])
        if ref.get('series') and ref.get('number'):
            details_parts.append(f'{ref["series"]} No. {ref["number"]}')
        elif ref.get('series'):
            details_parts.append(ref['series'])
        details = ', '.join(details_parts) if details_parts else ''

        # Which WDT papers cite this ref
        cited_in = _cited_in_labels(ref_id, citations)
        if cited_in:
            # Link each shortcode to its page
            cited_links = []
            for sc in cited_in:
                page = link_map.get(sc)
                if page:
                    cited_links.append(f'[{sc}]({page})')
                else:
                    cited_links.append(sc)
            cited_str = 'Cited in: ' + ' · '.join(cited_links)
        else:
            cited_str = ''

        # Build the entry
        # Title line: linked if we have a URL, plain otherwise
        verified_badge = ' ✓' if verified else ''
        type_badge = f'`{rtype}`'

        if link:
            title_md = f'[{title}]({link})'
        else:
            title_md = title

        lines.append(f'**{authors} ({year}).** {title_md}{verified_badge}  ')
        if details:
            lines.append(f'{details}  ')
        lines.append(f'{type_badge}')
        if cited_str:
            lines.append(f'<small>{cited_str}</small>')
        lines.append('')  # blank line between entries

    dest_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'  ✓ Generated references.qmd ({len(sorted_refs)} entries)')


# ---------------------------------------------------------------------------
# Diagram preprocessing  — Step 11 of preprocess.py
# ---------------------------------------------------------------------------
#
# Reads .mmd source files from site/diagrams/, injects Mermaid `click`
# directives from anchor_map, and generates flowcharts.qmd in _build/.
#
# How to extend:
#   • Add a clickable node: add an entry to DIAGRAM_CLICK_MAP
#   • Add a new diagram: add a .mmd to site/diagrams/, add an entry to
#     DIAGRAM_SPECS, reference it in generate_flowcharts_qmd()
#   • Restyle: edit classDef lines in site/diagrams/*.mmd, or add CSS
#     to styles.css under the  /* ── Mermaid diagrams ── */  section



# ---------------------------------------------------------------------------
# Click-directive map
# ---------------------------------------------------------------------------
# Maps Mermaid node ID → (shortcode, section_key_or_None, tooltip)
# section_key must match a key in anchors.yml (e.g. "3.5" for WP§3.5).
# Use None to link to the paper root page.
# Include the same node ID with different entry for skeleton variants (marked
# with "# sk" comments — node IDs differ between full and skeleton .mmd files).

DIAGRAM_CLICK_MAP = {
    # ── Assessment window ──────────────────────────────────────────────────
    'WIN':           ('WP', '4',    'Assessment window — WP §4'),
    'WIN_Q':         ('WP', '4',    'Window length election — WP §4'),
    'WIN_A':         ('WP', '4',    'One-year window — WP §4'),
    'WIN_B':         ('WP', '4',    'Multi-year: deferral premium — WP §4'),
    'ROUTE_ASSIGN':  ('WP', '4.1',  'Route assignment — WP §4.1'),
    'ROUTE':         ('WP', '4.1',  'Route assignment — WP §4.1'),        # sk

    # ── Privacy election ───────────────────────────────────────────────────
    'PRIV':          ('WP', '4.2',  'Privacy election — WP §4.2'),
    'PRIV_Q':        ('WP', '4.2',  'Disclosed or private? — WP §4.2'),
    'PRIV_DISC':     ('WP', '4.2',  'Disclosed: rate discount — WP §4.2'),
    'PRIV_PRIV':     ('WP', '4.2',  'Private: rate premium — WP §4.2'),

    # ── Valuation routes ───────────────────────────────────────────────────
    'VAL_ROUTE':     ('VAL', None,  'Valuation routes — VAL'),
    'VAL':           ('VAL', None,  'Asset valuation — VAL'),             # sk
    'A_Q':           ('VAL', '3',   'Route A — VAL §3'),
    'A_AUTO':        ('VAL', '3.1', 'Auto-priced assets — VAL §3.1'),
    'A_PROF':        ('VAL', '3.2', 'Professional valuation — VAL §3.2'),
    'A_DISP':        ('VAL', '3.3', 'Valuation dispute — VAL §3.3'),
    'A_REVIEW':      ('VAL', '3.3', 'Independent review — VAL §3.3'),
    'A_RQ':          ('VAL', '3.3', 'Review outcome — VAL §3.3'),
    'A_ORIG':        ('VAL', '3.3', 'Original valuation stands — VAL §3.3'),
    'A_TP':          ('VAL', '3.3', 'Taxpayer position accepted — VAL §3.3'),
    'A_REDIR':       ('VAL', '3.4', 'Reclassified to Route C — VAL §3.4'),
    'RA':            ('VAL', '3',   'Route A — VAL §3'),                  # sk

    'B_PROF':        ('VAL', '4',   'Route B valuation — VAL §4'),
    'B_DISP':        ('VAL', '4.1', 'Route B dispute — VAL §4.1'),
    'B_REVIEW':      ('VAL', '4.1', 'Independent review — VAL §4.1'),
    'B_RQ':          ('VAL', '4.1', 'Review outcome — VAL §4.1'),
    'B_ORIG':        ('VAL', '4.1', 'Original valuation stands — VAL §4.1'),
    'B_TP':          ('VAL', '4.1', 'Taxpayer position accepted — VAL §4.1'),
    'B_REDIR':       ('VAL', '4.2', 'Reclassified to Route D — VAL §4.2'),
    'RB':            ('VAL', '4',   'Route B — VAL §4'),                  # sk

    'C_SELF':        ('VAL', '5',   'Route C self-declaration — VAL §5'),
    'RC':            ('VAL', '5',   'Route C — VAL §5'),                  # sk

    'D_SELF':        ('VAL', '6',   'Route D self-declaration — VAL §6'),
    'D_VOL':         ('VAL', '6.1', 'Voluntary settlement options — VAL §6.1'),
    'D_DEFER':       ('VAL', '6.1', 'Deferred to realisation — VAL §6.1'),
    'D_SOFT':        ('VAL', '6.2', 'Soft reset — VAL §6.2'),
    'D_HARD':        ('VAL', '6.3', 'Hard reset (public auction) — VAL §6.3'),
    'RD':            ('VAL', '6',   'Route D — VAL §6'),                  # sk

    # ── Net worth & threshold ──────────────────────────────────────────────
    'TOTAL':         ('WP', '5',    'Net worth calculation — WP §5'),
    'NW':            ('WP', '5',    'Net worth — WP §5'),                 # sk
    'THRESH':        ('WP', '5.1',  'Exemption threshold — WP §5.1'),

    # ── Rate & delta ───────────────────────────────────────────────────────
    'RATE':          ('RATES', '2', 'Marginal rate schedule — RATES §2'),
    'DELTA':         ('WP', '3.2',  'Wealth delta — WP §3.2'),
    'SIGN':          ('WP', '3.2',  'Delta sign — WP §3.2'),

    # ── Tax & refund ───────────────────────────────────────────────────────
    'TAX':           ('WP', '3.3',  'WDT charge — WP §3.3'),
    'REFUND':        ('WP', '3.5',  'Symmetric refund — WP §3.5'),
    'ENVELOPE':      ('WP', '3.6',  'Lifetime contribution envelope — WP §3.6'),
    'REFUND_OK':     ('WP', '3.5',  'Refund confirmed — WP §3.5'),
    'REFUND_CAP':    ('WP', '3.6',  'Refund capped at envelope — WP §3.6'),

    # ── Settlement ─────────────────────────────────────────────────────────
    'SETTLE':        ('WP', '6',    'Settlement — WP §6'),
    'SA':            ('WP', '6.1',  'Route A: cash settlement — WP §6.1'),
    'SB':            ('WP', '6.2',  'Route B: lien — WP §6.2'),
    'SC':            ('WP', '6.3',  'Route C: in-kind transfer — WP §6.3'),
    'SD':            ('WP', '6.4',  'Route D: deferred — WP §6.4'),

    # ── Corporate levy credits ─────────────────────────────────────────────
    'CREDIT_Q':      ('CORP', None, 'Corporate levy credits — CORP'),
    'CREDIT':        ('CORP', None, 'Claim corporate levy credits — CORP'),
    'CREDIT_USE':    ('CORP', None, 'Credit disposition — CORP'),
    'CREDIT_APPLY':  ('CORP', None, 'Apply credit now — CORP'),
    'CREDIT_CARRY':  ('CORP', None, 'Carry forward credit — CORP'),
    'CREDIT_RETURN': ('CORP', None, 'Return credit to company — CORP'),

    # ── Administration ─────────────────────────────────────────────────────
    'DEADLINES':     ('GOV', None,  'Administrator credential & deadlines — GOV'),
    'ADMIN':         ('GOV', None,  'Administrator credential — GOV'),    # sk
    'REGISTER':      ('GOV', None,  'Public Valuation Register — GOV'),

    # ── SWF ────────────────────────────────────────────────────────────────
    'SWF':           ('WP', '7',    'Sovereign Wealth Fund — WP §7'),

    # ── Route D auction ────────────────────────────────────────────────────
    'AUCTION_Q':     ('VAL', '6.4', 'Route D audit trigger — VAL §6.4'),
    'AUCTION':       ('VAL', '6.4', 'Enforced auction — VAL §6.4'),

    # ── Annual loop ────────────────────────────────────────────────────────
    'ANNUAL':        ('WP', '8',    'Annual report — WP §8'),
    'LOOP':          ('WP', '4',    'Window end / new window — WP §4'),

    # ── Closure events ─────────────────────────────────────────────────────
    'CLOSURE_Q':     ('CLOSE', None,'Closure events — CLOSE'),
    'CLOSE':         ('CLOSE', None,'Closure events — CLOSE'),            # sk
    'DEATH':         ('CLOSE', '2', 'Death — CLOSE §2'),
    'CL1':           ('CLOSE', '2', 'Death — CLOSE §2'),                  # sk
    'EXIT':          ('CLOSE', '3', 'Exit — CLOSE §3'),
    'CL2':           ('CLOSE', '3', 'Exit — CLOSE §3'),                   # sk
    'FALLTHROUGH':   ('CLOSE', '4', 'Fall-through — CLOSE §4'),
    'CL3':           ('CLOSE', '4', 'Fall-through — CLOSE §4'),           # sk
    'BANKRUPT':      ('CLOSE', '5', 'Bankruptcy — CLOSE §5'),
    'CL4':           ('CLOSE', '5', 'Bankruptcy — CLOSE §5'),             # sk
}


# ---------------------------------------------------------------------------
# Core injection logic
# ---------------------------------------------------------------------------

def _build_click_directive(node_id, shortcode, section_key, tooltip,
                            link_map, anchor_map):
    """Return a single Mermaid click directive line, or '' if URL unresolvable."""
    if shortcode not in link_map:
        return ''
    page = link_map[shortcode]
    if section_key:
        anchor_key = f'{shortcode}\u00a7{section_key}'   # §
        url = anchor_map.get(anchor_key)
        if not url:
            print(f'  \u26a0 diagram click: {anchor_key} not in anchors.yml'
                  f' \u2014 linking to {page}')
            url = page
    else:
        url = page
    full_url = f'{SITE_URL}/{url}'
    safe_tip = tooltip.replace('"', "'")
    return f'click {node_id} href "{full_url}" "{safe_tip}"\n'


def _inject_click_directives(mmd_text, link_map, anchor_map):
    """
    Append click directives to a Mermaid diagram for every node ID that
    (a) appears in DIAGRAM_CLICK_MAP and (b) actually exists in this diagram.
    """
    # Crude but effective: check whether each mapped ID appears as a word in the source
    present = set(re.findall(r'\b([A-Z][A-Z0-9_]{1,30})\b', mmd_text))

    directives = []
    for node_id, (shortcode, section_key, tooltip) in DIAGRAM_CLICK_MAP.items():
        if node_id not in present:
            continue
        line = _build_click_directive(
            node_id, shortcode, section_key, tooltip, link_map, anchor_map
        )
        if line:
            directives.append(line)

    if not directives:
        return mmd_text

    block = '\n%% ── CLICK DIRECTIVES (injected by preprocess.py) ──────────\n'
    block += ''.join(directives)
    return mmd_text.rstrip('\n') + '\n' + block + '\n'


def _load_mmd(filename, inject_clicks, link_map, anchor_map):
    """Load one .mmd file, optionally inject click directives, return text."""
    src = DIAGRAMS_DIR / filename
    if not src.exists():
        print(f'  ! diagram not found: {src}')
        return f'%% diagram {filename} not found %%'
    text = src.read_text(encoding='utf-8')
    if inject_clicks:
        text = _inject_click_directives(text, link_map, anchor_map)
    return text


# ---------------------------------------------------------------------------
# flowcharts.qmd generation
# ---------------------------------------------------------------------------

def generate_flowcharts_qmd(build, link_map, anchor_map):
    """
    Generate _build/flowcharts.qmd, embedding all four diagrams inline
    as Mermaid fenced code blocks.  WDT diagrams get click directives;
    UK comparison diagrams are embedded as-is.
    """
    wdt_full     = _load_mmd('260812_WDT_Flowchart_LR.mmd',  True,  link_map, anchor_map)
    wdt_skeleton = _load_mmd('260812_WDT_Skeleton_LR.mmd',   True,  link_map, anchor_map)
    uk_full      = _load_mmd('260812_UK_Tax_Flowchart_LR.mmd', False, link_map, anchor_map)
    uk_skeleton  = _load_mmd('260812_UK_Skeleton_LR.mmd',    False, link_map, anchor_map)

    def mermaid_block(mmd_text, label, width=14):
        # Quarto mermaid fenced block with fig options
        lines = [f'```{{mermaid}}']
        lines.append(f'%%| label: {label}')
        lines.append(f'%%| fig-width: {width}')
        lines.append(mmd_text.strip())
        lines.append('```')
        return '\n'.join(lines)

    qmd = f'''\
---
title: "Taxpayer Journey Flowcharts"
description: "Interactive flowcharts mapping the WDT taxpayer journey and the current UK tax system. Click any node to jump to the relevant paper section."
author: "K. Ogata"
---

These diagrams map the taxpayer journey under the Wealth Delta Tax and, for comparison, under the current UK tax system. Two versions are provided for each: a **full detail** chart covering every decision branch and mechanism, and a **skeleton overview** suitable for orientation.

WDT nodes are clickable: hover over a node to see where it links, and click to navigate to the relevant section of the research papers.

::: {{.callout-tip}}
## Navigating these diagrams
The full detail charts are large — use your browser's **zoom** (Ctrl +/−) to read node text comfortably. All labelled nodes in the WDT diagrams link to the relevant paper section. The UK diagrams are shown for structural comparison only.
:::

---

## WDT Taxpayer Journey

The WDT journey begins when an assessment window opens and ends when a closure event fires the final delta calculation. Each asset is assigned a valuation route; the taxpayer's net worth delta determines whether tax or a symmetric refund is owed; settlement follows the asset's route.

::: {{.panel-tabset}}

### Full Detail

The full chart covers: window election and deferral premiums, route assignment (A–D), privacy elections, all valuation sub-routes and dispute resolution paths, net worth calculation and threshold check, rate computation and delta sign, the WDT charge and symmetric refund with lifetime envelope check, settlement by route, corporate levy credits, administrator credentialling, the Sovereign Wealth Fund allocation, Route D auction enforcement, the annual reporting loop, and all four closure events.

::: {{.wdt-diagram #wdt-full}}
{mermaid_block(wdt_full, 'wdt-full-chart', width=14)}
:::

### Skeleton Overview

::: {{.wdt-diagram #wdt-skeleton}}
{mermaid_block(wdt_skeleton, 'wdt-skeleton-chart', width=10)}
:::

:::

---

## UK Tax System (Comparison)

The current UK system is shown as a structural comparator. Unlike the WDT, the UK system assesses each tax year independently with no carry-forward of wealth position. Income, capital gains, inheritance, and corporate profits are taxed under separate regimes with distinct administrative calendars.

::: {{.panel-tabset}}

### Full Detail

::: {{.wdt-diagram #uk-full}}
{mermaid_block(uk_full, 'uk-full-chart', width=14)}
:::

### Skeleton Overview

::: {{.wdt-diagram #uk-skeleton}}
{mermaid_block(uk_skeleton, 'uk-skeleton-chart', width=10)}
:::

:::

---

## About these diagrams

These diagrams are generated at each site build by `pipeline/preprocess.py`. Clickable links in the WDT diagrams are injected automatically from `registry/anchors.yml` — the same cross-reference registry used throughout the paper series. Source `.mmd` files live in `site/diagrams/`.

To add or update a click link, edit `DIAGRAM_CLICK_MAP` in `preprocess.py`. To restyle the diagrams, edit the `classDef` blocks in the relevant `.mmd` file or add CSS to `site/style/styles.css` under the `/* ── Mermaid diagrams ── */` section.
'''

    dest = build / 'flowcharts.qmd'
    dest.write_text(qmd, encoding='utf-8')
    print(f'  \u2713 Generated flowcharts.qmd (4 diagrams, click directives injected)')

# ---------------------------------------------------------------------------
# Machine-readable asset copy + site-index generation
# ---------------------------------------------------------------------------

def generate_site_index(build, refs_data, anchor_map, contents):
    """
    Write site-index.json to _build/.

    Single-fetch navigation index for tools, search, and LLMs.
    Merges paper metadata, section hierarchy, and anchor URLs.
    Omits editorial internals (outbound_ext_citation_ids, flag_ids, notes).

    Schema:
    {
      "meta": { "generated": "ISO date", "site": URL, "papers": N, "anchors": N },
      "papers": [
        {
          "shortcode": "WP",
          "title": "...",
          "url": "https://wealthdeltatax.org/wp.html",
          "version": "2.1",
          "version_date": "2026-08-10",
          "status": "active",
          "outbound_internal": ["MF", "LR", ...],
          "inbound_internal":  ["MF", "CORP", ...],
          "sections": [
            { "key": "1", "title": "Introduction",
              "anchor": "wp.html#introduction",
              "url": "https://wealthdeltatax.org/wp.html#introduction" },
            ...
          ]
        },
        ...
      ],
      "anchors": { "WP§1": "wp.html#introduction", ... }
    }
    """
    internal_papers = {p['shortcode']: p for p in refs_data.get('internal_papers', [])}

    papers_out = []
    for shortcode, entry in contents.items():
        page  = entry.get('page', f'{shortcode.lower()}.html')
        url   = f'{SITE_URL}/{page}'
        meta  = internal_papers.get(shortcode, {})

        # Build sections list, pulling anchor URL from anchor_map
        sections = []
        for key, title in entry.get('sections', {}).items():
            anchor_key = f'{shortcode}§{key}'
            anchor     = anchor_map.get(anchor_key, page)
            sections.append({
                'key':    str(key),
                'title':  title,
                'anchor': anchor,
                'url':    f'{SITE_URL}/{anchor}',
            })

        paper_entry = {
            'shortcode':         shortcode,
            'title':             entry.get('title', meta.get('title', shortcode)),
            'url':               url,
            'version':           meta.get('version', ''),
            'version_date':      _format_date(meta.get('version_date')) or '',
            'status':            meta.get('status', 'active'),
            'outbound_internal': meta.get('outbound_internal', []),
            'inbound_internal':  meta.get('inbound_internal', []),
            'sections':          sections,
        }
        papers_out.append(paper_entry)

    index = {
        'meta': {
            'generated':     datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'site':          SITE_URL,
            'papers':        len(papers_out),
            'anchors':       len(anchor_map),
            'description':   (
                'Single-fetch navigation index for the Wealth Delta Tax research '
                'programme. Contains paper metadata, section hierarchy, and resolved '
                'anchor URLs. Generated by preprocess.py at each site build.'
            ),
        },
        'papers':  papers_out,
        'anchors': anchor_map,
    }

    dest = build / 'site-index.json'
    dest.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'  ✓ Generated site-index.json ({len(papers_out)} papers, {len(anchor_map)} anchors)')


def copy_machine_readable_assets(build, refs_data, anchor_map, contents):
    """
    Copy source-of-truth data files into _build/ so Quarto serves them
    as static endpoints:
      /references.json   — full reference database
      /anchors.yml           — section-to-URL anchor map
      /wdt-contents.yml      — paper/section hierarchy
      /site-index.json       — merged single-fetch navigation index
    """
    assets = [
        (REFERENCES_JSON,                              build / 'references.json'),
        (ROOT_DIR / 'registry' / 'anchors.yml',        build / 'anchors.yml'),
        (ROOT_DIR / 'registry' / 'contents.yml',       build / 'wdt-contents.yml'),
        (ROOT_DIR / 'registry' / 'references.bib', build / 'references.bib'),
    ]
    for src, dst in assets:
        if src.exists():
            shutil.copy2(src, dst)
            print(f'  ✓ {src.name} → {dst.name}')
        else:
            print(f'  ! {src.name} not found — skipping')

    generate_site_index(build, refs_data, anchor_map, contents)


# ---------------------------------------------------------------------------
# _quarto.yml generation
# ---------------------------------------------------------------------------

SIDEBAR_SECTION_ORDER = [
    ("Core Papers",            ["WP", "MF"]),
    ("Literature",             ["LR", "LR.A", "LR.B", "JUR"]),
    ("Valuation",              ["VAL", "VAL.A", "VAL.B"]),
    ("Corporate & Governance", ["CORP", "CORP.A", "GOV", "GOV.A", "GOV.B"]),
    ("Revenue & Behaviour",    ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A", "BEHAV"]),
    ("Implementation",         ["CLOSE", "PHASE1"]),
    ("Analysis",               ["POL", "ENV", "FM", "MOD"]),
]

SIDEBAR_LABELS = {
    "WP":       "White Paper (WP)",
    "MF":       "Moral Foundations (MF)",
    "LR":       "Systematic Literature Review (LR)",
    "LR.A":     "Research Gaps (LR.A)",
    "LR.B":     "Intellectual Background (LR.B)",
    "JUR":      "UK Jurisdiction (JUR)",
    "VAL":      "Valuing Wealth (VAL)",
    "VAL.A":    "Mathematical Companion (VAL.A)",
    "VAL.B":    "Worked Examples (VAL.B)",
    "CORP":     "Corporate Architecture (CORP)",
    "CORP.A":   "Corporate Appendix (CORP.A)",
    "GOV":      "Constitutional Governance (GOV)",
    "GOV.A":    "Governance Appendix (GOV.A)",
    "GOV.B":    "Operational Appendix (GOV.B)",
    "RATES":    "Rates and Revenue (RATES)",
    "RATES.A":  "Rates Appendix (RATES.A)",
    "SWEEPS":   "Parameter Sweeps (SWEEPS)",
    "SWEEPS.A": "Sweeps Appendix (SWEEPS.A)",
    "BEHAV":    "Behavioural Robustness (BEHAV)",
    "CLOSE":    "Position Closure (CLOSE)",
    "PHASE1":   "Phase One (PHASE1)",
    "POL":      "Political Architecture (POL)",
    "ENV":      "Environmental Effects (ENV)",
    "FM":       "First Mover (FM)",
    "MOD":      "Modular Adoption (MOD)",
}


def _section_depth(key: str) -> int:
    return str(key).count('.') + 1


def _build_paper_sidebar_contents(shortcode: str, contents: dict,
                                   anchor_map: dict) -> list:
    """Return sidebar content list for one paper, two levels deep."""
    paper    = contents.get(shortcode, {})
    page     = paper.get('page', f'{shortcode.lower()}.html')
    sections = paper.get('sections', {})

    result      = []
    current_l1  = None

    for key, title in sections.items():
        depth      = _section_depth(str(key))
        anchor_key = f'{shortcode}§{key}'
        url        = anchor_map.get(anchor_key, page)

        if depth == 1:
            if current_l1 is not None:
                result.append(current_l1)
            current_l1 = {'text': str(title), 'href': url, 'contents': []}
        elif depth == 2:
            if current_l1 is None:
                result.append({'text': str(title), 'href': url})
            else:
                current_l1['contents'].append({'text': str(title), 'href': url})
        # depth >= 3: omitted

    if current_l1 is not None:
        result.append(current_l1)

    # Remove empty contents lists
    for item in result:
        if isinstance(item, dict) and not item.get('contents'):
            item.pop('contents', None)

    return result


def generate_quarto_yml(build: Path, contents: dict, anchor_map: dict) -> None:
    """
    Overwrite _build/_quarto.yml with:
      - toc: false in format.html
      - generated nested sidebar contents (two levels deep)
    The file must already exist in _build/ from the static copy step.
    """
    dest = build / '_quarto.yml'
    if not dest.exists():
        print('  ! _quarto.yml not found in _build/ — skipping sidebar generation')
        return

    with dest.open(encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 1. Disable right-hand TOC globally
    config.setdefault('format', {}).setdefault('html', {})['toc'] = False

    # 2. Build nested sidebar
    sidebar_contents = []
    for section_name, shortcodes in SIDEBAR_SECTION_ORDER:
        present = [sc for sc in shortcodes if sc in contents]
        if not present:
            continue
        section_items = []
        for sc in present:
            page   = contents[sc].get('page', f'{sc.lower()}.html')
            label  = SIDEBAR_LABELS.get(sc, sc)
            nested = _build_paper_sidebar_contents(sc, contents, anchor_map)
            entry  = {'text': label, 'href': page}
            if nested:
                entry['contents'] = nested
            section_items.append(entry)
        sidebar_contents.append({'section': section_name, 'contents': section_items})

    # config.setdefault('website', {}).setdefault('sidebar', {})['contents'] = sidebar_contents

    sidebar = config.setdefault('website', {}).setdefault('sidebar', {})
    sidebar['collapse-level'] = 2
    sidebar['contents'] = sidebar_contents

    # 3. Write
    with dest.open('w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False)
    print('  ✓ _quarto.yml — nested sidebar generated, toc: false')


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(src_path, dest_path, shortcode):
    text = src_path.read_text(encoding='utf-8')
    text = LATEX_RE.sub('', text)
    text = convert_crossrefs(text)
    lines = convert_internal_bibliography(text.splitlines(keepends=True))
    text = ''.join(lines)
    text = inject_front_matter(text, shortcode)
    text = text.rstrip('\n') + '\n' + build_jsonld(shortcode)
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

    # Copy site/ assets into _build/.
    # pages/ is flattened to _build/ root (strips the pages/ prefix).
    # style/ and _quarto.yml preserve their paths (_build/style/, _build/_quarto.yml).
    FLATTEN_DIRS = {'pages'}

    static_files = [f for f in SITE_DIR.rglob("*") if f.is_file()]
    for p in static_files:
        relative_path = p.relative_to(SITE_DIR)
        parts = relative_path.parts
        if parts[0] in FLATTEN_DIRS:
            destination = build / Path(*parts[1:])
        else:
            destination = build / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, destination)

    # Generate _quarto.yml: nested sidebar (2 levels deep) + toc: false
    generate_quarto_yml(build, contents, anchor_map)

    generate_corpus_qmd(build / 'corpus.qmd')

    if Path(REFERENCES_JSON).exists():
        generate_references_qmd(build / 'references.qmd', refs_data)
    else:
        print(f'  ! references.json not found in registry/ — skipping references.qmd')

    # Step 11: Generate flowcharts.qmd with click-directive-injected diagrams
    if DIAGRAMS_DIR.exists():
        generate_flowcharts_qmd(build, link_map, anchor_map)
    else:
        print(f'  ! site/diagrams/ not found — skipping flowcharts.qmd')

    copy_machine_readable_assets(build, refs_data, anchor_map, contents)

    registry_path = REGISTRY_YML
    print(f'  Looking for papers.yml at: {registry_path.resolve()}')
    if not registry_path.exists():
        print('ERROR: registry/papers.yml not found.')
        return

    with registry_path.open(encoding='utf-8') as f:
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

        process_file(matches[-1], build / output_name, shortcode)
        found += 1

    print(f'\nDone. {found} papers staged, {missing} not yet available.')
    print(f'Run: quarto render {BUILD_DIR}')


if __name__ == '__main__':
    main()
