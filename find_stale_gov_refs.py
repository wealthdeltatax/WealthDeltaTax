"""
find_stale_gov_refs.py — Find stale GOV section references
GOV only goes to section 8. References to §9+ or non-existent subsections are stale.
"""

import re
from pathlib import Path
from collections import defaultdict

SOURCE_DIR = "source_md"

# Valid GOV sections (based on series.yml)
VALID_GOV_SECTIONS = {
    "1", "1.1", "2", "2.1", "3", "3.1", "3.2", "4", "5", "5.1", "5.2", "5.3",
    "6", "6.1", "6.2", "6.3", "6.4", "7", "8"
}

# Pattern for GOV references with optional subsections
GOV_REF_PATTERN = re.compile(
    r'\(GOV(?:\.(?:A|B))?\s+§([\d.A-Za-z]+)\)|GOV(?:\.(?:A|B))?\s+§([\d.A-Za-z]+)'
)

def find_stale_gov_refs(filepath):
    """Find stale GOV references in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stale = []
    for line_num, line in enumerate(lines, 1):
        for match in GOV_REF_PATTERN.finditer(line):
            section = match.group(1) or match.group(2)
            # Extract just the main section (before the dot if it exists)
            main_section = section.split('.')[0] if '.' in section else section
            
            # Check if stale (only for GOV, not GOV.A or GOV.B)
            if 'GOV.A' not in match.group(0) and 'GOV.B' not in match.group(0):
                # Check if this section exists
                if section not in VALID_GOV_SECTIONS:
                    stale.append({
                        'line': line_num,
                        'section': section,
                        'context': line.rstrip(),
                        'match': match.group(0)
                    })
    
    return stale

def main():
    """Find all stale GOV references."""
    source_path = Path(SOURCE_DIR)
    all_stale = defaultdict(list)
    
    for md_file in sorted(source_path.glob("*.md")):
        refs = find_stale_gov_refs(md_file)
        if refs:
            all_stale[md_file.name] = refs
    
    if not all_stale:
        print("✓ No stale GOV references found.")
        return
    
    print(f"Found stale GOV references in {len(all_stale)} files:\n")
    
    # Group by section number to see patterns
    by_section = defaultdict(list)
    total = 0
    
    for filename, refs in sorted(all_stale.items()):
        for ref in refs:
            by_section[ref['section']].append((filename, ref))
            total += 1
    
    print("Stale sections (grouped):")
    for section in sorted(by_section.keys(), key=lambda x: (int(x.split('.')[0]) if x[0].isdigit() else 99, x)):
        refs = by_section[section]
        print(f"\n  GOV§{section}: {len(refs)} occurrence(s)")
        # Show first few examples
        for filename, ref in refs[:2]:
            print(f"    {filename}:{ref['line']}")
            print(f"      {ref['match']}")
        if len(refs) > 2:
            print(f"    ... and {len(refs) - 2} more")
    
    print(f"\n\nTotal stale GOV references: {total}")
    print("\nReminder: GOV only has sections 1-8.")
    print("  - GOV§9+ don't exist (GOV only goes to §8)")
    print("  - GOV§2.2, GOV§3.3, GOV§6.2.2, GOV§6.2.3, GOV§6.2, GOV§8.3-8.8 don't exist")
    print("  - Check GOV.A and GOV.B for the correct location")

if __name__ == "__main__":
    main()
