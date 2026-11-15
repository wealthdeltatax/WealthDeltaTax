#!/usr/bin/env python3
"""Consistency checker for WDT paper markdown files.

Usage: python check_wdt_format.py paper.md [more.md ...]

Checks front matter, cross-reference format, heading numbering, and figure
captions against the conventions in SKILL.md. Reports line numbers; exits 1
if any issue is found. Mechanical checks only: it does not judge prose.
"""
import re
import sys

SC = r"[A-Z][A-Za-z]*(?:\.[A-Z])?"            # shortcode, e.g. VAL, VAL.A, GOV.B
NUM = r"(?:\d+|[A-Z])(?:\.\d+)*"                 # 5.2 (main paper) or A.2 (appendix); no lower-case letters
REF_OK = re.compile(rf"\(({SC})(?: §{NUM}| Figure {NUM}[a-z]?| Table {NUM})?\)")
FIG = re.compile(r"^!\[Figure ([^:]*): (.*)\]\((.*?)\)(\{.*\})?\s*$")
JEL = re.compile(r"^\s{2}- ([A-Z]\d{2})\s{3}# \S")


def split_front(lines):
    if not lines or lines[0].strip() != "---":
        return [], 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], i + 1
    return [], 0


def main(path):
    issues = []
    add = lambda n, msg: issues.append((n, msg))
    lines = open(path, encoding="utf-8").read().split("\n")
    fm, body_start = split_front(lines)

    # ---- front matter ----
    keys = [re.match(r"^([a-z_]+):", l).group(1) for l in fm if re.match(r"^[a-z_]+:", l)]
    want = ["title", "shortcode", "status", "keywords", "zenodo_doi", "jel"]
    for k in want:
        if k not in keys:
            add(1, f"front matter: missing field '{k}'")
    order = [k for k in keys if k in want]
    if order != [k for k in want if k in order]:
        add(1, f"front matter: field order should be {', '.join(want)}")
    for i, l in enumerate(fm, start=2):
        if l.startswith("zenodo_doi:") and not re.match(r'^zenodo_doi: "10\.5072/zenodo\.(\d+|TBD)"$', l):
            add(i, "front matter: zenodo_doi must be \"10.5072/zenodo.NNNNNN\" (or TBD placeholder)")
    in_jel = False
    for i, l in enumerate(fm, start=2):
        if l.startswith("jel:"):
            in_jel = True
        elif in_jel and re.match(r"^\S", l):
            in_jel = False
        elif in_jel and l.strip() and not JEL.match(l):
            add(i, "front matter: jel line must be '  - X00   # Description'")
    sc = next((re.search(r'"(.*)"', l).group(1) for l in fm if l.startswith("shortcode:")), "")

    # ---- body ----
    sec = None            # current section number (lowest heading with a number)
    figs = {}             # section -> list of (line, label)
    in_code = False
    for n, l in enumerate(lines[body_start:], start=body_start + 1):
        if l.startswith("```"):
            in_code = not in_code
        if in_code:
            continue

        h = re.match(r"^(#{1,4}) (.*)$", l)
        if h:
            title = h.group(2)
            m = re.match(rf"^({NUM})\.?\s", title + " ")
            if m:
                sec = m.group(1)
            if re.match(r"^[A-Z]\.\d", title) is None and re.match(r"^[a-z]\.", title):
                add(n, "lower-case letter in section number")
            if "{.appendix}" in title:
                add(n, "{.appendix} attribute not used; appendix sections are lettered in the heading text")

        # cross-references
        for m in re.finditer("§", l):
            pre = l[: m.start()]
            if not re.search(rf"\({SC} $", pre):
                add(n, f"bare § reference: '…{l[max(0, m.start()-12):m.start()+12]}…' (use (SHORTCODE §x.y))")
        for m in re.finditer(rf"\({SC} §[^)]*\)", l):
            if not REF_OK.fullmatch(m.group(0)):
                add(n, f"malformed cross-reference {m.group(0)} (no lower-case letters, no extra words inside brackets)")
        if re.search(r"§§|§\s*[\d.]+\s*[–-]\s*[\d.]+|\bthrough\s+\(", l):
            add(n, "range written with §§, dash or 'through'; use (X §a) to (X §b)")
        if re.search(r"\b[Ss]ection \d", l):
            add(n, "'Section N' used; use (SHORTCODE §N)")

        # figures
        f = FIG.match(l)
        if f:
            label, cap, path_, attr = f.groups()
            if not re.fullmatch(rf"(?:\d+|[A-Z]\.\d+)(?:\.\d+)*[a-z]?", label):
                add(n, f"figure label '{label}' must be section number plus optional letter")
            else:
                base = re.match(r"(?:\d+|[A-Z]\.\d+)(?:\.\d+)*", label).group(0)
                if sec and base != sec:
                    add(n, f"figure {label} sits in section {sec}; label should start with {sec}")
                figs.setdefault(base, []).append((n, label))
                stem = "_".join(label.lower().split("."))
                if not re.fullmatch(rf"\.\./figures/{re.escape(sc.lower().replace('.', '_'))}_fig_{stem}_[A-Za-z0-9_]+\.png", path_):
                    add(n, f"figure path '{path_}' should be ../figures/{sc.lower()}_fig_{stem}_<slug>.png")
            if attr != "{width=100%}":
                add(n, "figure needs {width=100%}")
            if not re.search(rf"Source: \({SC} §{NUM}\)(?:, \({SC} §{NUM}\))*\.$", cap):
                add(n, "figure caption must end with 'Source: (SHORTCODE §x.y).'")
        elif l.startswith("![") and "Figure" in l[:12]:
            add(n, "figure line not in the form ![Figure N: caption](path){width=100%}")

        # prose hygiene
        if "—" in l and not h and not l.startswith("|"):
            add(n, "em dash in prose")

    for base, items in figs.items():
        letters = [re.sub(r"^(?:\d+|[A-Z]\.\d+)(?:\.\d+)*", "", lab) for _, lab in items]
        if len(items) == 1 and letters[0]:
            add(items[0][0], f"figure {items[0][1]} is alone in its section; drop the letter")
        if len(items) > 1:
            exp = [chr(97 + i) for i in range(len(items))]
            if letters != exp:
                add(items[0][0], f"figures in section {base} should be lettered {', '.join(base + e for e in exp)}; found {', '.join(l for _, l in items)}")

    for n, msg in sorted(issues):
        print(f"{path}:{n}: {msg}")
    print(f"{path}: {len(issues)} issue(s)")
    return len(issues)


if __name__ == "__main__":
    total = sum(main(p) for p in sys.argv[1:])
    sys.exit(1 if total else 0)
