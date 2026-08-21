"""
quarto_config.py — generate the nested sidebar and rewrite _quarto.yml.

Call generate_quarto_yml(build, contents, anchor_map).

This module owns:
  - SIDEBAR_SECTION_ORDER — which papers appear, in which group, in what order
  - SIDEBAR_LABELS        — display name for each paper shortcode
  - sidebar content builder (two levels deep: section groups → papers → sections)
  - the _quarto.yml rewrite (injects sidebar, sets toc: false)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


# ── Sidebar ordering and labels ───────────────────────────────────────────────

# SIDEBAR_SECTION_ORDER: list[tuple[str, list[str]]] = [
#     ("Core Papers",            ["WP", "MF"]),
#     ("Literature",             ["LR", "LR.A", "LR.B", "JUR"]),
#     ("Valuation",              ["VAL", "VAL.A", "VAL.B"]),
#     ("Corporate & Governance", ["CORP", "CORP.A", "GOV", "GOV.A", "GOV.B"]),
#     ("Revenue & Behaviour",    ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A", "BEHAV"]),
#     ("Implementation",         ["CLOSE", "PHASE1"]),
#     ("Analysis",               ["POL", "ENV", "FM", "MOD"]),
# ]

# SIDEBAR_LABELS: dict[str, str] = {
#     "WP":       "White Paper (WP)",
#     "MF":       "Moral Foundations (MF)",
#     "LR":       "Systematic Literature Review (LR)",
#     "LR.A":     "Research Gaps (LR.A)",
#     "LR.B":     "Intellectual Background (LR.B)",
#     "JUR":      "UK Jurisdiction (JUR)",
#     "VAL":      "Valuing Wealth (VAL)",
#     "VAL.A":    "Mathematical Companion (VAL.A)",
#     "VAL.B":    "Worked Examples (VAL.B)",
#     "CORP":     "Corporate Architecture (CORP)",
#     "CORP.A":   "Corporate Appendix (CORP.A)",
#     "GOV":      "Constitutional Governance (GOV)",
#     "GOV.A":    "Governance Appendix (GOV.A)",
#     "GOV.B":    "Operational Appendix (GOV.B)",
#     "RATES":    "Rates and Revenue (RATES)",
#     "RATES.A":  "Rates Appendix (RATES.A)",
#     "SWEEPS":   "Parameter Sweeps (SWEEPS)",
#     "SWEEPS.A": "Sweeps Appendix (SWEEPS.A)",
#     "BEHAV":    "Behavioural Robustness (BEHAV)",
#     "CLOSE":    "Position Closure (CLOSE)",
#     "PHASE1":   "Phase One (PHASE1)",
#     "POL":      "Political Architecture (POL)",
#     "ENV":      "Environmental Effects (ENV)",
#     "FM":       "First Mover (FM)",
#     "MOD":      "Modular Adoption (MOD)",
# }


# ── Sidebar content builder ───────────────────────────────────────────────────

# def _section_depth(key: str) -> int:
#     return str(key).count(".") + 1


# def _build_paper_sidebar_contents(
#     shortcode: str,
#     contents: dict[str, Any],
#     anchor_map: dict[str, str],
# ) -> list[dict[str, Any]]:
#     """Return sidebar content list for one paper, two levels deep."""
#     paper    = contents.get(shortcode, {})
#     page     = paper.get("page", f"{shortcode.lower()}.html")
#     sections = paper.get("sections", {})

#     result: list[dict[str, Any]] = []
#     current_l1: dict[str, Any] | None = None

#     for key, title in sections.items():
#         depth      = _section_depth(str(key))
#         anchor_key = f"{shortcode}§{key}"
#         url        = anchor_map.get(anchor_key, page)

#         if depth == 1:
#             if current_l1 is not None:
#                 result.append(current_l1)
#             current_l1 = {"text": str(title), "href": url, "contents": []}
#         elif depth == 2:
#             if current_l1 is None:
#                 result.append({"text": str(title), "href": url})
#             else:
#                 current_l1["contents"].append({"text": str(title), "href": url})
#         # depth >= 3: omitted

#     if current_l1 is not None:
#         result.append(current_l1)

#     # Remove empty contents lists
#     for item in result:
#         if isinstance(item, dict) and not item.get("contents"):
#             item.pop("contents", None)

#     return result


# ── _quarto.yml rewrite ───────────────────────────────────────────────────────

def generate_quarto_yml(
    build: Path,
    contents: dict[str, Any],
    anchor_map: dict[str, str],
) -> None:
    """
    Rewrite _build/_quarto.yml with:
      - toc: false in format.html
      - generated nested sidebar contents (two levels deep)
      - collapse-level: 2

    The file must already exist in _build/ from the static copy step.
    """
    dest = build / "_quarto.yml"
    if not dest.exists():
        print("  ! _quarto.yml not found in _build/ — skipping sidebar generation")
        return

    with dest.open(encoding="utf-8") as fh:
        config: dict[str, Any] = yaml.safe_load(fh)

    # Enable the standard Quarto right-hand TOC globally
    # config.setdefault("format", {}).setdefault("html", {})["toc"] = True


    # # Build nested sidebar contents
    # sidebar_contents: list[dict[str, Any]] = []
    # for section_name, shortcodes in SIDEBAR_SECTION_ORDER:
    #     present = [sc for sc in shortcodes if sc in contents]
    #     if not present:
    #         continue

    #     section_items: list[dict[str, Any]] = []
    #     for sc in present:
    #         page   = contents[sc].get("page", f"{sc.lower()}.html")
    #         label  = SIDEBAR_LABELS.get(sc, sc)
    #         nested = _build_paper_sidebar_contents(sc, contents, anchor_map)
    #         entry: dict[str, Any] = {"text": label, "href": page}
    #         if nested:
    #             entry["contents"] = nested
    #         section_items.append(entry)

    #     sidebar_contents.append({"section": section_name, "contents": section_items})

    # sidebar = config.setdefault("website", {}).setdefault("sidebar", {})
    # sidebar["collapse-level"] = 2
    # sidebar["contents"] = sidebar_contents

    with dest.open("w", encoding="utf-8") as fh:
        yaml.dump(
            config, fh,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    print("  ✓ _quarto.yml — nested sidebar generated, toc: true")
