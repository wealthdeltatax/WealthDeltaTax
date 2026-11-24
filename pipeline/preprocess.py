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
  12.   Calculator .qmd pages             (tools.py)
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
from tools import generate_tool_pages, _strip_html_shell


# Sentinel used in avoidance.md (and any future page) to mark where a
# calculator fragment should be injected at build time.
# Format: <!-- WDT_CALC_INJECT: {filename} -->
# Filename is resolved relative to site/tools/.
import re as _re
_CALC_INJECT_RE = _re.compile(r'<!--\s*WDT_CALC_INJECT:\s*(\S+?)\s*-->')


def main() -> None:
    # ── Step 0: generate references.json from .bib + internal.json ───────
    generate_references_json()

    source = cfg.SOURCE_DIR

    # ── Step 0.5: extract metadata from all source .md files ─────────────
    # Read pages.yml (brief 029s) for the source→output mapping of the papers.
    # Shortcode is read from each file's front matter, not from the registry.
    registry_path = cfg.PAGES_YML
    print(f"  Looking for pages.yml at: {registry_path.resolve()}")
    if not registry_path.exists():
        print("ERROR: registry/pages.yml not found.")
        return

    pages = cfg.load_pages(registry_path)
    errors = cfg.validate_pages(pages)
    if errors:
        print("ERROR: registry/pages.yml is invalid:")
        for e in errors:
            print(f"  ! {e}")
        raise SystemExit(1)
    for c in cfg.find_url_collisions(pages):
        print(f"  ! URL {c['url']} claimed by {', '.join(c['ids'])}: "
              f"built from {', '.join(c['live']) or 'none'}, held (not published): {', '.join(c['held']) or 'none'}")
        if len(c["live"]) > 1:
            print("ERROR: two live pages claim one URL.")
            raise SystemExit(1)
    registry = cfg.paper_registry(pages)

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
                # Inject calculator fragments at sentinel comments.
                # <!-- WDT_CALC_INJECT: filename --> is replaced with a
                # {=html} pass-through block containing the named fragment
                # from site/tools/, shell-stripped by tools._strip_html_shell.
                tools_src = cfg.ROOT_DIR / "site" / "tools"
                def _inject_calc(m: "_re.Match") -> str:
                    calc_name = m.group(1)
                    calc_path = tools_src / calc_name
                    if not calc_path.exists():
                        print(f"  ! WDT_CALC_INJECT: {calc_name} not found — sentinel left in place")
                        return m.group(0)
                    fragment = _strip_html_shell(calc_path.read_text(encoding="utf-8"))
                    print(f"  ✓ Injected {calc_name} into {p.name}")
                    return (
                        "```{=html}\n"
                        "<!-- quarto-disable-processing=true -->\n"
                        f"{fragment}\n"
                        "```"
                    )
                text = _CALC_INJECT_RE.sub(_inject_calc, text)
                destination.write_text(text, encoding="utf-8")
            else:
                shutil.copy2(p, destination)

        else:
            destination = build / Path(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, destination)

    # The legacy model assets and figures (model_v1/) are removed from the tree (tag legacy-models-2026-11); nothing is copied into _build/model/ or _build/figures/ any more.

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

    # ── Step 12: Calculator .qmd pages ────────────────────────────────────
    tools_src = cfg.ROOT_DIR / "site" / "tools"
    if tools_src.exists():
        generate_tool_pages(tools_src, build / "model")
    else:
        print("  ! site/tools/ not found — skipping calculator page generation")

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