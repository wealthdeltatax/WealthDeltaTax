"""
WDT site preprocessing pipeline.
Reads .md source files, processes them for HTML rendering, writes .qmd to _build/.
Run this before every `quarto render _build`.

Steps:
  0.    Generate references.json from references.bib + internal.json  (bib_to_json.py)
  0.5.  Extract paper metadata from source .md front matter + revision history
  1–5.  Per-paper text transforms        (transforms.py)
  6.    corpus.qmd                        (pages/corpus.py)
  7.    references.qmd                    (pages/references.py)
  8.    Copy static assets                (this file)
  9.    Copy machine-readable data        (pages/site_index.py)
  10.   site-index.json                   (pages/site_index.py)
  11.   flowcharts.qmd                    (diagrams.py)
"""

import shutil
from pathlib import Path

import yaml

import config as cfg
from bib_to_json import run as generate_references_json
from diagrams import generate_flowcharts_qmd
from pages.corpus import generate_corpus_qmd
from pages.references import generate_references_qmd
from pages.site_index import copy_machine_readable_assets
from transforms import process_file, strip_latex, convert_crossrefs
from link_map import generate_link_map_html

# ── Tool metadata ─────────────────────────────────────────────────────────────
# Maps source filename stem → (title, description)
_TOOL_META: dict[str, tuple[str, str]] = {
    "tools_index": (
        "WDT — Interactive Tools",
        "Computational tools for exploring the Wealth Delta Tax mechanism. "
        "Both tools run the WDT Python model unmodified in your browser via Pyodide — "
        "no data leaves your machine. The first load takes around 10 seconds to initialise "
        "the runtime; subsequent calculations are fast.",
    ),
    "revenue": (
        "WDT — National Revenue Calculator",
        "Aggregate WDT revenue modelled across the full UK taxable wealth distribution "
        "(Taxpayer Cohort Model). Four return tiers (Fagereng et al. 2020). "
        "UK equity return series 1947–2019.",
    ),
    "taxpayer": (
        "WDT — Individual Taxpayer Calculator",
        "Route C simulation: equity-transfer mechanism over N holding periods plus "
        "terminal sell year. Results always shown alongside the honest-declaration "
        "(α = 1) baseline.",
    ),
}

_TOOL_RUNTIME_SUFFIXES = {".py", ".toml"}


def _wrap_tool_html(html: str, title: str, description: str) -> str:
    """Wrap a body-fragment HTML file in Quarto front matter + raw HTML pass-through."""
    return (
        f'---\n'
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        f'toc: false\n'
        f'---\n\n'
        f'```{{=html}}\n'
        f'<!-- quarto-disable-processing=true -->\n'
        f'{html.strip()}\n'
        f'```\n'
    )


def main() -> None:
    # ── Step 0: generate references.json from .bib + internal.json ───────
    generate_references_json()

    source = cfg.SOURCE_DIR

    # ── Step 0.5: extract metadata from all source .md files ─────────────
    # Read papers.yml for the source→output mapping.
    # Shortcode is now read from each file's front matter, not from papers.yml.
    registry_path = cfg.REGISTRY_YML
    print(f"  Looking for papers.yml at: {registry_path.resolve()}")
    if not registry_path.exists():
        print("ERROR: registry/papers.yml not found.")
        return

    with registry_path.open(encoding="utf-8") as fh:
        registry = yaml.safe_load(fh)

    # Build paper_meta by extracting from each source file.
    # Also build a lookup: shortcode → output filename (still needed by the pipeline).
    paper_meta:      dict[str, dict] = {}
    shortcode_to_output: dict[str, str] = {}
    shortcode_to_src:    dict[str, Path] = {}

    for entry in registry:
        source_name = entry["source"]
        output_name = entry["output"]
        src_path    = source / source_name

        if not src_path.exists():
            print(f"  – {source_name}: file not found (skipped)")
            continue

        meta = cfg.extract_paper_meta(src_path)
        if not meta:
            print(f"  ! {source_name}: metadata extraction failed (skipped)")
            continue

        shortcode = meta["shortcode"]
        paper_meta[shortcode]           = meta
        shortcode_to_output[shortcode]  = output_name
        shortcode_to_src[shortcode]     = src_path
        print(
            f"  ✓ {source_name}: [{shortcode}] v{meta['version']} "
            f"({meta['word_count']:,} words)"
        )

    print(f"  Extracted metadata for {len(paper_meta)} papers.\n")

    # ── Load site config (now receives paper_meta from extraction above) ──
    site_cfg = cfg.load(paper_meta=paper_meta)

    build = cfg.BUILD_DIR

    # ── Clean and recreate _build/ ────────────────────────────────────────
    if build.exists():
        shutil.rmtree(build, ignore_errors=True)
    build.mkdir(exist_ok=True)

    # ── Copy site/ assets into _build/ ───────────────────────────────────
    FLATTEN_DIRS = {"pages"}
    TOOL_DIR     = "model"

    for p in [f for f in cfg.SITE_DIR.rglob("*") if f.is_file()]:
        parts = p.relative_to(cfg.SITE_DIR).parts

        if parts[0] in FLATTEN_DIRS:
            destination = build / Path(*parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix == ".md":
                destination = destination.with_suffix(".qmd")
                text = p.read_text(encoding="utf-8")
                text = strip_latex(text)
                text = convert_crossrefs(text, site_cfg.link_map, site_cfg.anchor_map)
                destination.write_text(text, encoding="utf-8")
            else:
                shutil.copy2(p, destination)

        elif parts[0] == TOOL_DIR:
            destination = build / Path(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix == ".html":
                stem = p.stem
                title, description = _TOOL_META.get(stem, (stem, ""))
                html = p.read_text(encoding="utf-8")
                qmd  = _wrap_tool_html(html, title, description)
                destination = destination.with_suffix(".qmd")
                destination.write_text(qmd, encoding="utf-8")
                print(f"  ✓ site/model/{p.name} → _build/model/{destination.name}")
            elif p.suffix in _TOOL_RUNTIME_SUFFIXES:
                shutil.copy2(p, destination)
                print(f"  ✓ site/model/{p.name} → _build/model/{p.name} (runtime)")
            else:
                shutil.copy2(p, destination)

        else:
            destination = build / Path(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, destination)

    # ── Copy image outputs into _build/figures/ ───────────────────────────
    OUTPUTS_DIR = cfg.SITE_DIR / "model" / "OUTPUTS"
    if OUTPUTS_DIR.exists():
        figures_dest = build / "figures"
        figures_dest.mkdir(exist_ok=True)
        for img in OUTPUTS_DIR.rglob("*"):
            if img.is_file():
                shutil.copy2(img, figures_dest / img.name)
        print(
            f"  ✓ Copied image outputs → _build/figures/ "
            f"({sum(1 for _ in OUTPUTS_DIR.rglob('*') if _.is_file())} files)"
        )
    else:
        print("  ! site/model/OUTPUTS/ not found — skipping figure copy")

    # ── Auto-generated pages ──────────────────────────────────────────────
    generate_corpus_qmd(build / "corpus.qmd", site_cfg.link_map, site_cfg.paper_meta)

    if cfg.REFERENCES_JSON.exists():
        generate_references_qmd(
            build / "references.qmd", site_cfg.refs_data, site_cfg.link_map
        )
    else:
        print("  ! references.json not found — skipping references.qmd")

    if cfg.DIAGRAMS_DIR.exists():
        generate_flowcharts_qmd(build)
    else:
        print("  ! site/diagrams/ not found — skipping flowcharts.qmd")

    generate_link_map_html(build / "link-map.html", site_cfg.refs_data, site_cfg.link_map)

    # ── Machine-readable static endpoints + site-index.json ──────────────
    copy_machine_readable_assets(
        build,
        site_cfg.refs_data,
        site_cfg.anchor_map,
        site_cfg.contents,
        site_cfg.link_map,
    )

    # ── Per-paper processing ──────────────────────────────────────────────
    found = missing = 0
    for shortcode, src_path in shortcode_to_src.items():
        output_name = shortcode_to_output[shortcode]
        process_file(
            src_path,
            build / output_name,
            shortcode,
            site_cfg.link_map,
            site_cfg.anchor_map,
            site_cfg.paper_meta,
        )
        found += 1

    skipped = len(registry) - found - missing
    print(f"\nDone. {found} papers staged, {len(registry) - found} not available.")
    print(f"Run: quarto render {cfg.BUILD_DIR}")


if __name__ == "__main__":
    main()