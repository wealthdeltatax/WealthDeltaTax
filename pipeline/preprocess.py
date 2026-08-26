"""
WDT site preprocessing pipeline.
Reads .md source files, processes them for HTML rendering, writes .qmd to _build/.
Run this before every `quarto render _build`.

Steps:
  0.    Generate references.json from references.bib + internal.json  (bib_to_json.py)
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


# ── Tool metadata ─────────────────────────────────────────────────────────────
# Maps source filename stem → (title, description)
# Source files live at site/tools/<stem>.html as body-fragment HTML (no skeleton).
# Runtime files (.py, .toml) in site/tools/ are copied verbatim.
_TOOL_META: dict[str, tuple[str, str]] = {
    "index": (
        "WDT — Interactive Tools",
        "Computational tools for exploring the Wealth Delta Tax mechanism. "
        "Both calculators run the Python model directly in your browser via Pyodide — "
        "no data is sent to any server.",
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

# File extensions in site/tools/ that are runtime assets (copied verbatim, not wrapped)
_TOOL_RUNTIME_SUFFIXES = {".py", ".toml"}


def _wrap_tool_html(html: str, title: str, description: str) -> str:
    """Wrap a body-fragment HTML file in Quarto front matter + raw HTML pass-through.

    The sentinel comment on the first line of the block tells Quarto's Lua filter
    to skip all processing of this block entirely — including the table-parse pass
    that fires on <table> strings inside JS template literals and logs a warning.
    """
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
    # Must run before cfg.load() so the loaded refs_data is fresh.
    generate_references_json()

    site_cfg = cfg.load()

    build  = cfg.BUILD_DIR
    source = cfg.SOURCE_DIR

    # ── Clean and recreate _build/ ────────────────────────────────────────
    if build.exists():
        shutil.rmtree(build, ignore_errors=True)
    build.mkdir(exist_ok=True)

    # ── Copy site/ assets into _build/ ───────────────────────────────────
    # Handling per directory:
    #
    #   site/pages/   → flattened to _build/ root
    #                   .md files get crossref transforms + renamed to .qmd
    #                   all other files copied verbatim
    #
    #   site/tools/   → path preserved as _build/tools/
    #                   .html files wrapped in Quarto front matter → .qmd
    #                   .py / .toml runtime files copied verbatim
    #                   (no crossref transforms — these are interactive tool fragments)
    #
    #   everything else → path preserved, copied verbatim

    FLATTEN_DIRS = {"pages"}
    TOOL_DIR     = "tools"

    for p in [f for f in cfg.SITE_DIR.rglob("*") if f.is_file()]:
        parts = p.relative_to(cfg.SITE_DIR).parts

        if parts[0] in FLATTEN_DIRS:
            # Flatten pages/ to _build/ root
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
            # Preserve tools/ path
            destination = build / Path(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if p.suffix == ".html":
                # Wrap body-fragment HTML in Quarto front matter
                stem = p.stem
                title, description = _TOOL_META.get(stem, (stem, ""))
                html = p.read_text(encoding="utf-8")
                qmd  = _wrap_tool_html(html, title, description)
                destination = destination.with_suffix(".qmd")
                destination.write_text(qmd, encoding="utf-8")
                print(f"  ✓ site/tools/{p.name} → _build/tools/{destination.name}")
            elif p.suffix in _TOOL_RUNTIME_SUFFIXES:
                # Runtime files: copy verbatim so browser fetch() calls resolve
                shutil.copy2(p, destination)
                print(f"  ✓ site/tools/{p.name} → _build/tools/{p.name} (runtime)")
            else:
                shutil.copy2(p, destination)

        else:
            destination = build / Path(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, destination)

    # ── Copy image outputs into _build/figures/ ───────────────────────────────
    OUTPUTS_DIR = cfg.SITE_DIR / "tools" / "OUTPUTS"
    if OUTPUTS_DIR.exists():
        figures_dest = build / "figures"
        figures_dest.mkdir(exist_ok=True)
        for img in OUTPUTS_DIR.rglob("*"):
            if img.is_file():
                shutil.copy2(img, figures_dest / img.name)
        print(f"  ✓ Copied image outputs → _build/figures/ ({sum(1 for _ in OUTPUTS_DIR.rglob('*') if _.is_file())} files)")
    else:
        print(f"  ! site/tools/OUTPUTS/ not found — skipping figure copy")

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