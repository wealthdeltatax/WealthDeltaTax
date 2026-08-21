"""
WDT site preprocessing pipeline.
Reads .md source files, processes them for HTML rendering, writes .qmd to _build/.
Run this before every `quarto render _build`.

Steps:
  1–5.  Per-paper text transforms        (transforms.py)
  6.    corpus.qmd                        (pages/corpus.py)
  7.    references.qmd                    (pages/references.py)
  8.    Copy static assets                (this file)
  9.    Copy machine-readable data        (pages/site_index.py)
  10.   site-index.json                   (pages/site_index.py)
  11.   flowcharts.qmd                    (diagrams.py)
  --.   _quarto.yml sidebar + toc: false  (quarto_config.py)
"""

import shutil
from pathlib import Path

import yaml

import config as cfg
from diagrams import generate_flowcharts_qmd
from pages.corpus import generate_corpus_qmd
from pages.references import generate_references_qmd
from pages.site_index import copy_machine_readable_assets
from quarto_config import generate_quarto_yml
from transforms import process_file, strip_latex, convert_crossrefs

def main() -> None:
    site_cfg = cfg.load()

    build  = cfg.BUILD_DIR
    source = cfg.SOURCE_DIR

    # ── Clean and recreate _build/ ────────────────────────────────────────
    if build.exists():
        shutil.rmtree(build, ignore_errors=True)
    build.mkdir(exist_ok=True)

    # ── Copy site/ assets into _build/ ───────────────────────────────────
    # site/pages/ is flattened to _build/ root (strips the pages/ prefix).
    # All other site/ contents preserve their relative paths.
    FLATTEN_DIRS = {"pages"}

    for p in [f for f in cfg.SITE_DIR.rglob("*") if f.is_file()]:
        parts = p.relative_to(cfg.SITE_DIR).parts
        destination = build / Path(*parts[1:]) if parts[0] in FLATTEN_DIRS else build / Path(*parts)
        destination.parent.mkdir(parents=True, exist_ok=True)

        if parts[0] in FLATTEN_DIRS and p.suffix == ".md":
            # Run crossref transforms on hand-authored pages before copying.
            # strip_latex and convert_crossrefs are safe on any Markdown text.
            # inject_front_matter and build_jsonld are paper-specific — skip.
            destination = destination.with_suffix(".qmd")
            text = p.read_text(encoding="utf-8")
            text = strip_latex(text)
            text = convert_crossrefs(text, site_cfg.link_map, site_cfg.anchor_map)
            destination.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(p, destination)

    # ── _quarto.yml: nested sidebar + toc: false ─────────────────────────
    generate_quarto_yml(build, site_cfg.contents, site_cfg.anchor_map)

    # ── Auto-generated pages ──────────────────────────────────────────────
    generate_corpus_qmd(build / "corpus.qmd", site_cfg.link_map, site_cfg.paper_meta)

    if cfg.REFERENCES_JSON.exists():
        generate_references_qmd(
            build / "references.qmd", site_cfg.refs_data, site_cfg.link_map
        )
    else:
        print(f"  ! references.json not found — skipping references.qmd")

    if cfg.DIAGRAMS_DIR.exists():
        generate_flowcharts_qmd(build, site_cfg.link_map, site_cfg.anchor_map)
    else:
        print(f"  ! site/diagrams/ not found — skipping flowcharts.qmd")

    # ── Machine-readable static endpoints + site-index.json ──────────────
    copy_machine_readable_assets(
        build,
        site_cfg.refs_data,
        site_cfg.anchor_map,
        site_cfg.contents,
        site_cfg.link_map,
    )

    # ── Per-paper processing ──────────────────────────────────────────────
    registry_path = cfg.REGISTRY_YML
    print(f"  Looking for papers.yml at: {registry_path.resolve()}")
    if not registry_path.exists():
        print("ERROR: registry/papers.yml not found.")
        return

    with registry_path.open(encoding="utf-8") as fh:
        registry = yaml.safe_load(fh)

    found = missing = 0
    for entry in registry:
        shortcode   = entry["shortcode"]
        source_glob = entry["source_glob"]
        output_name = entry["output"]

        matches = sorted(source.glob(source_glob))
        if not matches:
            print(f"  – {shortcode}: no file found (skipped)")
            missing += 1
            continue
        if len(matches) > 1:
            print(f"  ! {shortcode}: multiple matches, using {matches[-1].name}")

        process_file(
            matches[-1],
            build / output_name,
            shortcode,
            site_cfg.link_map,
            site_cfg.anchor_map,
            site_cfg.paper_meta,
        )
        found += 1

    print(f"\nDone. {found} papers staged, {missing} not yet available.")
    print(f"Run: quarto render {cfg.BUILD_DIR}")


if __name__ == "__main__":
    main()
