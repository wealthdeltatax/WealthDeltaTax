"""
diagrams.py — Mermaid diagram preprocessing and flowcharts.qmd generation.

Reads .mmd source files from site/diagrams/, injects click directives from
anchor_map into the WDT diagrams, and generates flowcharts.qmd in _build/.

To add a clickable node:  add an entry to DIAGRAM_CLICK_MAP.
To add a new diagram:     add a .mmd to site/diagrams/ and a call to
                          _load_mmd() + mermaid_block() in
                          generate_flowcharts_qmd().
To restyle:               edit classDef lines in site/diagrams/*.mmd, or add
                          CSS to site/style/styles.css under the
                          /* ── Mermaid diagrams ── */ section.
"""

from __future__ import annotations

import re
from pathlib import Path

from config import AUTHOR, DIAGRAMS_DIR, SITE_URL


# ── Click-directive map ───────────────────────────────────────────────────────
# Maps Mermaid node ID → (shortcode, section_key_or_None, tooltip)
# section_key must match a key in anchors.yml (e.g. "3.5" for WP§3.5).
# Use None to link to the paper root page.
# Nodes shared between full and skeleton diagrams are marked "# sk".

DIAGRAM_CLICK_MAP: dict[str, tuple[str, str | None, str]] = {
    # ── Assessment window ──────────────────────────────────────────────────
    "WIN":           ("WP", "4",    "Assessment window — WP §4"),
    "WIN_Q":         ("WP", "4",    "Window length election — WP §4"),
    "WIN_A":         ("WP", "4",    "One-year window — WP §4"),
    "WIN_B":         ("WP", "4",    "Multi-year: deferral premium — WP §4"),
    "ROUTE_ASSIGN":  ("WP", "4.1",  "Route assignment — WP §4.1"),
    "ROUTE":         ("WP", "4.1",  "Route assignment — WP §4.1"),        # sk

    # ── Privacy election ───────────────────────────────────────────────────
    "PRIV":          ("WP", "4.2",  "Privacy election — WP §4.2"),
    "PRIV_Q":        ("WP", "4.2",  "Disclosed or private? — WP §4.2"),
    "PRIV_DISC":     ("WP", "4.2",  "Disclosed: rate discount — WP §4.2"),
    "PRIV_PRIV":     ("WP", "4.2",  "Private: rate premium — WP §4.2"),

    # ── Valuation routes ───────────────────────────────────────────────────
    "VAL_ROUTE":     ("VAL", None,  "Valuation routes — VAL"),
    "VAL":           ("VAL", None,  "Asset valuation — VAL"),             # sk
    "A_Q":           ("VAL", "3",   "Route A — VAL §3"),
    "A_AUTO":        ("VAL", "3.1", "Auto-priced assets — VAL §3.1"),
    "A_PROF":        ("VAL", "3.2", "Professional valuation — VAL §3.2"),
    "A_DISP":        ("VAL", "3.3", "Valuation dispute — VAL §3.3"),
    "A_REVIEW":      ("VAL", "3.3", "Independent review — VAL §3.3"),
    "A_RQ":          ("VAL", "3.3", "Review outcome — VAL §3.3"),
    "A_ORIG":        ("VAL", "3.3", "Original valuation stands — VAL §3.3"),
    "A_TP":          ("VAL", "3.3", "Taxpayer position accepted — VAL §3.3"),
    "A_REDIR":       ("VAL", "3.4", "Reclassified to Route C — VAL §3.4"),
    "RA":            ("VAL", "3",   "Route A — VAL §3"),                  # sk

    "B_PROF":        ("VAL", "4",   "Route B valuation — VAL §4"),
    "B_DISP":        ("VAL", "4.1", "Route B dispute — VAL §4.1"),
    "B_REVIEW":      ("VAL", "4.1", "Independent review — VAL §4.1"),
    "B_RQ":          ("VAL", "4.1", "Review outcome — VAL §4.1"),
    "B_ORIG":        ("VAL", "4.1", "Original valuation stands — VAL §4.1"),
    "B_TP":          ("VAL", "4.1", "Taxpayer position accepted — VAL §4.1"),
    "B_REDIR":       ("VAL", "4.2", "Reclassified to Route D — VAL §4.2"),
    "RB":            ("VAL", "4",   "Route B — VAL §4"),                  # sk

    "C_SELF":        ("VAL", "5",   "Route C self-declaration — VAL §5"),
    "RC":            ("VAL", "5",   "Route C — VAL §5"),                  # sk

    "D_SELF":        ("VAL", "6",   "Route D self-declaration — VAL §6"),
    "D_VOL":         ("VAL", "6.1", "Voluntary settlement options — VAL §6.1"),
    "D_DEFER":       ("VAL", "6.1", "Deferred to realisation — VAL §6.1"),
    "D_SOFT":        ("VAL", "6.2", "Soft reset — VAL §6.2"),
    "D_HARD":        ("VAL", "6.3", "Hard reset (public auction) — VAL §6.3"),
    "RD":            ("VAL", "6",   "Route D — VAL §6"),                  # sk

    # ── Net worth & threshold ──────────────────────────────────────────────
    "TOTAL":         ("WP", "5",    "Net worth calculation — WP §5"),
    "NW":            ("WP", "5",    "Net worth — WP §5"),                 # sk
    "THRESH":        ("WP", "5.1",  "Exemption threshold — WP §5.1"),

    # ── Rate & delta ───────────────────────────────────────────────────────
    "RATE":          ("RATES", "2", "Marginal rate schedule — RATES §2"),
    "DELTA":         ("WP", "3.2",  "Wealth delta — WP §3.2"),
    "SIGN":          ("WP", "3.2",  "Delta sign — WP §3.2"),

    # ── Tax & refund ───────────────────────────────────────────────────────
    "TAX":           ("WP", "3.3",  "WDT charge — WP §3.3"),
    "REFUND":        ("WP", "3.5",  "Symmetric refund — WP §3.5"),
    "ENVELOPE":      ("WP", "3.6",  "Lifetime contribution envelope — WP §3.6"),
    "REFUND_OK":     ("WP", "3.5",  "Refund confirmed — WP §3.5"),
    "REFUND_CAP":    ("WP", "3.6",  "Refund capped at envelope — WP §3.6"),

    # ── Settlement ─────────────────────────────────────────────────────────
    "SETTLE":        ("WP", "6",    "Settlement — WP §6"),
    "SA":            ("WP", "6.1",  "Route A: cash settlement — WP §6.1"),
    "SB":            ("WP", "6.2",  "Route B: lien — WP §6.2"),
    "SC":            ("WP", "6.3",  "Route C: in-kind transfer — WP §6.3"),
    "SD":            ("WP", "6.4",  "Route D: deferred — WP §6.4"),

    # ── Corporate levy credits ─────────────────────────────────────────────
    "CREDIT_Q":      ("CORP", None, "Corporate levy credits — CORP"),
    "CREDIT":        ("CORP", None, "Claim corporate levy credits — CORP"),
    "CREDIT_USE":    ("CORP", None, "Credit disposition — CORP"),
    "CREDIT_APPLY":  ("CORP", None, "Apply credit now — CORP"),
    "CREDIT_CARRY":  ("CORP", None, "Carry forward credit — CORP"),
    "CREDIT_RETURN": ("CORP", None, "Return credit to company — CORP"),

    # ── Administration ─────────────────────────────────────────────────────
    "DEADLINES":     ("GOV", None,  "Administrator credential & deadlines — GOV"),
    "ADMIN":         ("GOV", None,  "Administrator credential — GOV"),    # sk
    "REGISTER":      ("GOV", None,  "Public Valuation Register — GOV"),

    # ── SWF ────────────────────────────────────────────────────────────────
    "SWF":           ("WP", "7",    "Sovereign Wealth Fund — WP §7"),

    # ── Route D auction ────────────────────────────────────────────────────
    "AUCTION_Q":     ("VAL", "6.4", "Route D audit trigger — VAL §6.4"),
    "AUCTION":       ("VAL", "6.4", "Enforced auction — VAL §6.4"),

    # ── Annual loop ────────────────────────────────────────────────────────
    "ANNUAL":        ("WP", "8",    "Annual report — WP §8"),
    "LOOP":          ("WP", "4",    "Window end / new window — WP §4"),

    # ── Closure events ─────────────────────────────────────────────────────
    "CLOSURE_Q":     ("CLOSE", None, "Closure events — CLOSE"),
    "CLOSE":         ("CLOSE", None, "Closure events — CLOSE"),           # sk
    "DEATH":         ("CLOSE", "2", "Death — CLOSE §2"),
    "CL1":           ("CLOSE", "2", "Death — CLOSE §2"),                  # sk
    "EXIT":          ("CLOSE", "3", "Exit — CLOSE §3"),
    "CL2":           ("CLOSE", "3", "Exit — CLOSE §3"),                   # sk
    "FALLTHROUGH":   ("CLOSE", "4", "Fall-through — CLOSE §4"),
    "CL3":           ("CLOSE", "4", "Fall-through — CLOSE §4"),           # sk
    "BANKRUPT":      ("CLOSE", "5", "Bankruptcy — CLOSE §5"),
    "CL4":           ("CLOSE", "5", "Bankruptcy — CLOSE §5"),             # sk
}


# ── Click-directive injection ─────────────────────────────────────────────────

def _build_click_directive(
    node_id: str,
    shortcode: str,
    section_key: str | None,
    tooltip: str,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> str:
    """Return a single Mermaid click directive line, or '' if URL unresolvable."""
    if shortcode not in link_map:
        return ""
    page = link_map[shortcode]
    if section_key:
        anchor_key = f"{shortcode}\u00a7{section_key}"  # §
        url = anchor_map.get(anchor_key)
        if not url:
            print(
                f"  ⚠ diagram click: {anchor_key} not in anchors.yml"
                f" — linking to {page}"
            )
            url = page
    else:
        url = page
    full_url = f"{SITE_URL}/{url}"
    safe_tip = tooltip.replace('"', "'")
    return f'click {node_id} href "{full_url}" "{safe_tip}"\n'


def _inject_click_directives(
    mmd_text: str,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> str:
    """
    Append click directives to a Mermaid diagram for every node ID that
    (a) appears in DIAGRAM_CLICK_MAP and (b) actually exists in this diagram.
    """
    present = set(re.findall(r"\b([A-Z][A-Z0-9_]{1,30})\b", mmd_text))

    directives: list[str] = []
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

    block = "\n%% ── CLICK DIRECTIVES (injected by preprocess.py) ──────────\n"
    block += "".join(directives)
    return mmd_text.rstrip("\n") + "\n" + block + "\n"


def _load_mmd(
    filename: str,
    inject_clicks: bool,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> str:
    """Load one .mmd file, optionally inject click directives, return text."""
    src = DIAGRAMS_DIR / filename
    if not src.exists():
        print(f"  ! diagram not found: {src}")
        return f"%% diagram {filename} not found %%"
    text = src.read_text(encoding="utf-8")
    if inject_clicks:
        text = _inject_click_directives(text, link_map, anchor_map)
    return text


# ── flowcharts.qmd generation ─────────────────────────────────────────────────

def generate_flowcharts_qmd(
    build: Path,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> None:
    """
    Generate _build/flowcharts.qmd, embedding all four diagrams inline
    as Mermaid fenced code blocks. WDT diagrams get click directives;
    UK comparison diagrams are embedded as-is.
    """
    wdt_full     = _load_mmd("260812_WDT_Flowchart_LR.mmd",    True,  link_map, anchor_map)
    wdt_skeleton = _load_mmd("260812_WDT_Skeleton_LR.mmd",     False,  link_map, anchor_map)
    uk_full      = _load_mmd("260812_UK_Tax_Flowchart_LR.mmd", False, link_map, anchor_map)
    uk_skeleton  = _load_mmd("260812_UK_Skeleton_LR.mmd",      False, link_map, anchor_map)

    def mermaid_block(mmd_text: str) -> str:
        # Note: %%| chunk-option lines are intentionally omitted here.
        # They interact with the %%{init}%%  directive and cause parse
        # failures in some Quarto versions.  Width is controlled via CSS
        # on the .wdt-diagram-full / .wdt-diagram-skeleton wrapper divs.
        lines = [
            "```{mermaid}",
            mmd_text.strip(),
            "```",
        ]
        return "\n".join(lines)

    qmd = f"""\
---
title: "Taxpayer Journey Flowcharts"
description: "Interactive flowcharts mapping the WDT taxpayer journey and the current UK tax system. Click any node to jump to the relevant paper section."
author: "{AUTHOR}"
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

::: {{.wdt-diagram-tabset}}
::: {{.panel-tabset}}

### Full Detail

The full chart covers: window election and deferral premiums, route assignment (A–D), privacy elections, all valuation sub-routes and dispute resolution paths, net worth calculation and threshold check, rate computation and delta sign, the WDT charge and symmetric refund with lifetime envelope check, settlement by route, corporate levy credits, administrator credentialling, the Sovereign Wealth Fund allocation, Route D auction enforcement, the annual reporting loop, and all four closure events.

{mermaid_block(wdt_full)}

### Skeleton Overview

{mermaid_block(wdt_skeleton)}

:::
:::

---

## UK Tax System (Comparison)

The current UK system is shown as a structural comparator. Unlike the WDT, the UK system assesses each tax year independently with no carry-forward of wealth position. Income, capital gains, inheritance, and corporate profits are taxed under separate regimes with distinct administrative calendars.

::: {{.wdt-diagram-tabset}}
::: {{.panel-tabset}}

### Full Detail

{mermaid_block(uk_full)}

### Skeleton Overview

{mermaid_block(uk_skeleton)}

:::
:::

---

## About these diagrams

These diagrams are generated at each site build by `pipeline/preprocess.py`. Clickable links in the WDT diagrams are injected automatically from `registry/anchors.yml` — the same cross-reference registry used throughout the paper series. Source `.mmd` files live in `site/diagrams/`.

To add or update a click link, edit `DIAGRAM_CLICK_MAP` in `pipeline/diagrams.py`. To restyle the diagrams, edit the `classDef` blocks in the relevant `.mmd` file or add CSS to `site/style/styles.css` under the `/* ── Mermaid diagrams ── */` section.
"""

    dest = build / "flowcharts.qmd"
    dest.write_text(qmd, encoding="utf-8")
    print("  ✓ Generated flowcharts.qmd (4 diagrams, click directives injected)")
