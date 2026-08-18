"""
build_anchors.py — WDT anchor map generator
Reads wdt-contents.yml, derives the Quarto-generated HTML anchor ID for every
section, writes anchors.yml mapping PAPER§SECTION → page.html#anchor-id.

Run this whenever wdt-contents.yml is updated, before running preprocess.py.

Quarto anchor rules (confirmed against rendered HTML):
  - Numeric top-level (#): no anchor generated (page title level)
  - Numeric ## and ###:    strip the leading number prefix, slugify title only
      e.g. "1.1 The Cooperative Basis of the Design" → "the-cooperative-basis-of-the-design"
  - Letter-prefixed (any level, incl. lone letters like "A", "J"):
      keep the full heading text including prefix, slugify everything together
      e.g. "A.1 The Taxpayer Chamber (TP)"  → "a.1-the-taxpayer-chamber-tp"
      e.g. "A"  "The Chambers in Full"      → "a.-the-chambers-in-full"  (top-level appendix)
      e.g. "J"  "The Deferred Delta"        → "j-the-deferred-delta"
"""

import re
import yaml
from pathlib import Path

ROOT_DIR     = Path(__file__).resolve().parent.parent
CONTENTS_YML = ROOT_DIR / 'registry' / 'contents.yml'
ANCHORS_YML  = ROOT_DIR / 'registry' / 'anchors.yml'


def slugify(text: str) -> str:
    """Convert heading text to a Quarto anchor ID."""
    text = text.lower()
    # remove characters that Quarto strips: parentheses, colons, apostrophes,
    # quotes, commas, periods (except inside the letter-prefix, handled before call)
    text = re.sub(r"[():'\"?,]", "", text)
    # em-dash and en-dash → space
    text = text.replace("—", " ").replace("–", " ")
    # replace any remaining non-alphanumeric (except hyphens and dots) with space
    text = re.sub(r"[^a-z0-9\-\.]", " ", text)
    # collapse whitespace to hyphens
    text = re.sub(r"\s+", "-", text.strip())
    # collapse multiple hyphens
    text = re.sub(r"-+", "-", text)
    return text


def make_anchor(section_key: str, section_title: str) -> str:
    """
    Derive the Quarto anchor ID from the section key and title.

    Four key types from wdt-contents.yml:
      pure_int          e.g. "1", "10"          → numeric top-level, NO anchor
      numeric_dot       e.g. "1.1", "3.4.1"     → strip prefix, slugify title only
      letter_only       e.g. "A", "J", "B"      → keep prefix + title together
      letter_dot_numeric e.g. "A.1", "B.2.3"    → keep prefix + title together
    """
    # Pure integer top-level: Anchor 
    if re.match(r"^\d+$", section_key):
        return slugify(section_title) 

    # Numeric sub-section: strip the number prefix, slugify title only
    if re.match(r"^\d+\.", section_key):
        return slugify(section_title)

    # Letter-only top-level appendix section (e.g. "A", "J")
    # Quarto keeps the letter and the dot that appears in rendered heading "A. Title"
    # Observed: "A. The Chambers in Full" → "a.-the-chambers-in-full"
    #           "J" "The Deferred Delta"  → "j-the-deferred-delta"  (no dot in heading text)
    # The dot appears in the appendix heading because Quarto adds it for {.appendix} sections.
    # For non-appendix letter sections (J, K, L in VAL.B), no dot is added.
    # We detect appendix-style by checking if the paper uses A/B/C/D/E letter sequence
    # starting from "A" — VAL.B uses J/K/L/M/N/O so those are not appendix-style.
    # Simpler rule: if key is a single letter A-H, Quarto adds a dot; I-Z it does not.
    # BUT: we have confirmed data only for GOV.B §A (dot added) not for VAL.B §J (unknown).
    # Safe approach: build the full heading as it appears in the source and slugify.
    if re.match(r"^[A-Z]$", section_key):
        # The source heading is "# A. The Chambers in Full {.appendix}" or "# J The Deferred Delta"
        # Quarto's anchor for appendix sections includes the dot: "a.-the-chambers-in-full"
        # For non-appendix single letters we don't have confirmed data yet.
        # Use the confirmed appendix pattern for A-H; flag others as needing verification.
        letter = section_key
        if letter in "ABCDEFGH":
            # appendix style: "A." + title → slugify together
            full = f"{letter}. {section_title}"
        else:
            # VAL.B style (J,K,L,M,N,O): "J The Deferred Delta" → "j-the-deferred-delta"
            # No dot. Unverified — marked with TODO in output.
            full = f"{letter} {section_title}"
        return slugify(full)

    # Letter-dot-numeric: "A.1", "B.2.3", "F.2.1" etc.
    # Quarto keeps the full prefix: "a.1-the-taxpayer-chamber-tp"
    if re.match(r"^[A-Z]\.", section_key):
        full = f"{section_key} {section_title}"
        return slugify(full)

    # Fallback (should not occur given current data)
    return slugify(section_title)


def build_anchors(contents_path: str, output_path: str) -> None:
    with open(contents_path, encoding="utf-8") as f:
        contents = yaml.safe_load(f)

    anchor_map = {}
    skipped   = []
    unverified = []

    for paper_id, paper_data in contents.items():
        if not isinstance(paper_data, dict):
            continue
        page = paper_data.get("page", "")
        sections = paper_data.get("sections", {})

        for key, title in sections.items():
            lookup_key = f"{paper_id}§{key}"
            anchor = make_anchor(str(key), str(title))

            if anchor is None:
                # Pure top-level numeric: link to page root only
                skipped.append(lookup_key)
                anchor_map[lookup_key] = page
            else:
                anchor_map[lookup_key] = f"{page}#{anchor}"

                # Flag unverified single-letter non-appendix sections
                if re.match(r"^[I-Z]$", str(key)):
                    unverified.append(lookup_key)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(anchor_map, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=True)

    total = len(anchor_map)
    deep  = sum(1 for v in anchor_map.values() if "#" in v)
    print(f"anchors.yml written: {total} entries, {deep} with deep links, "
          f"{len(skipped)} top-level (page root only)")
    if unverified:
        print(f"\nNOTE: {len(unverified)} single-letter non-appendix section anchors "
              f"are unverified (VAL.B §J–§O style). Confirm in browser:")
        for k in unverified:
            print(f"  {k}  →  {anchor_map[k]}")


if __name__ == "__main__":
    build_anchors(CONTENTS_YML, ANCHORS_YML)
