import re
from pathlib import Path

SOURCE = Path("source_md")
FILE_TO_PAPER = {
    "1.0": "WP", "2.0": "MF", "3.0": "LR", "3.1": "LR.B",
    "4.0": "JUR", "5.0": "VAL", "5.1": "VAL.A", "5.2": "VAL.B",
    "6.0": "CORP", "6.1": "CORP.A", "7.0": "GOV", "7.1": "GOV.A", "7.2": "GOV.B",
    "8.0": "RATES", "8.1": "RATES.A", "9.0": "SWEEPS", "9.1": "SWEEPS.A",
    "10.0": "BEHAV", "11.0": "CLOSE", "12.0": "POL", "13.0": "PHASE1",
    "14.0": "ENV", "15.0": "FM", "16.0": "MOD",
}

nested_pattern = re.compile(r'\(GOV \((?P<paper>[A-Z][A-Z0-9.]*?) §(?P<section>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)\)\.? (?P<suffix>[0-9A-Za-z]+)?\)', re.VERBOSE)

# A slightly more forgiving version for the malformed pattern without the inner space before the closing )
nested_pattern_2 = re.compile(r'\(GOV \((?P<paper>[A-Z][A-Z0-9.]*?) §(?P<section>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)\)\.? (?P<suffix>[0-9A-Za-z]+)?\)', re.VERBOSE)

# This is the actual malformed form in the files: (GOV (PAPER §n.)3)
# There is no extra space before the final suffix; the pattern above handles the fixed forms.
actual_nested_pattern = re.compile(r'\(GOV \((?P<paper>[A-Z][A-Z0-9.]*?) §(?P<section>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)\.\)(?P<suffix>[0-9A-Za-z]+)\)')

# Some corrupted forms are already close to the target but still wrap the target in an extra GOV call,
# such as (GOV (GOV.B §5.)3) and (GOV (WP §6.)1)

def fix_nested(text: str) -> str:
    def repl(match):
        inner = match.group('paper')
        section = match.group('section').rstrip('.')
        suffix = match.group('suffix') or ''
        if suffix:
            return f'({inner} §{section}.{suffix})'
        return f'({inner} §{section})'

    text = actual_nested_pattern.sub(repl, text)
    # Also clean the variant with a dot before the outer close: (GOV (PAPER §6.)1)
    text = re.sub(r'\(GOV \((?P<paper>[A-Z][A-Z0-9.]*?) §(?P<section>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)\.\)(?P<suffix>[0-9A-Za-z]+)\)',
                  lambda m: f'({m.group("paper")} §{m.group("section")}.{m.group("suffix")})', text)
    text = re.sub(r'\(GOV \((?P<paper>[A-Z][A-Z0-9.]*?) §(?P<section>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)\)\)',
                  lambda m: f'({m.group("paper")} §{m.group("section")})', text)
    return text


def fix_bare_internal_refs(text: str, paper: str) -> str:
    # Leave tables and bibliography blocks alone.
    lines = text.splitlines(True)
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') or stripped.startswith('['):
            new_lines.append(line)
            continue

        def repl(match):
            section = match.group(1)
            return f'({paper} §{section})'

        new_line = re.sub(r'(?<![A-Z0-9\)\]])§([0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)', repl, line)
        new_lines.append(new_line)
    return ''.join(new_lines)


changed_files = []
for md in sorted(SOURCE.glob('*.md')):
    paper = FILE_TO_PAPER.get(md.name.split('_')[0])
    text = md.read_text(encoding='utf-8')
    new_text = fix_nested(text)
    if paper:
        new_text = fix_bare_internal_refs(new_text, paper)
    if new_text != text:
        md.write_text(new_text, encoding='utf-8')
        changed_files.append(md.name)

print(f'Updated {len(changed_files)} files:')
for name in changed_files:
    print(f'  {name}')
