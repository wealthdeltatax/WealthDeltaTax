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
  7. Auto-generate references.qmd — flat bibliography with cited-in links
  8. Copy static assets and hand-authored pages into _build/
  9. Copy machine-readable data files (wdt_references.json, anchors.yml,
     wdt-contents.yml) into _build/ as static endpoints
 10. Generate site-index.json — merged single-fetch navigation index
     (papers + sections + anchor URLs + relationships)
"""

import re, shutil, json
from pathlib import Path
from datetime import datetime, timezone
import yaml
import os
from pathlib import Path

# ── CONFIGURATION ────────────────────────────────────────────────────────────
SCRIPT_DIR      = Path(__file__).resolve().parent

STATIC_DIR      = SCRIPT_DIR / 'static'
SOURCE_DIR      = SCRIPT_DIR / 'source_md'
BUILD_DIR       = SCRIPT_DIR / '_build'

CONTENTS_YML    = SCRIPT_DIR / 'wdt-contents.yml'
ANCHORS_YML     = SCRIPT_DIR / 'anchors.yml'
REFERENCES_JSON = SCRIPT_DIR / 'wdt_references.json'
REGISTRY_YML    = SCRIPT_DIR / 'paper_registry.yml'

SITE_URL        = "https://wealthdeltatax.org"
AUTHOR          = "K. Ogata"
# ─────────────────────────────────────────────────────────────────────────────

# Load wdt-contents.yml  contents[SHORTCODE] = {page, title, sections}
#                         link_map[SHORTCODE] = "page.html"
# Load anchors.yml        anchor_map[SHORTCODE§X.Y] = "page.html#anchor-id"
# Load wdt_references.json paper_meta[SHORTCODE] = {...}

if not CONTENTS_YML.exists():
    raise FileNotFoundError(f"wdt-contents.yml not found at {CONTENTS_YML}")
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
        '[machine-readable JSON](/wdt_references.json).'
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
      /wdt_references.json   — full reference database
      /anchors.yml           — section-to-URL anchor map
      /wdt-contents.yml      — paper/section hierarchy
      /site-index.json       — merged single-fetch navigation index
    """
    assets = [
        (REFERENCES_JSON,                 build / 'wdt_references.json'),
        (SCRIPT_DIR / 'anchors.yml',      build / 'anchors.yml'),
        (SCRIPT_DIR / 'wdt-contents.yml', build / 'wdt-contents.yml'),
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
    sidebar['collapse-level'] = 1
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

    # Subdirectories of static/ whose contents are copied flat to _build/ root.
    FLATTEN_DIRS = {'pages', 'seo', 'style'}

    static_files = [f for f in STATIC_DIR.rglob("*") if f.is_file()]
    for p in static_files:
        relative_path = p.relative_to(STATIC_DIR)
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
        print(f'  ! wdt_references.json not found — skipping references.qmd')

    copy_machine_readable_assets(build, refs_data, anchor_map, contents)

    registry_path = REGISTRY_YML
    if not registry_path.exists():
        print('ERROR: paper_registry.yml not found.')
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
