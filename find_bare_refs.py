"""
find_bare_refs.py — Find bare internal section references
Finds: §5.2 without a paper prefix immediately before it
These need manual fixing since the correct paper prefix must be added by hand.
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Find bare § references: those NOT preceded by a paper shortcode
# This regex looks for § followed by numbers/dots/letters, but NOT preceded by uppercase letters
# which would indicate a paper prefix
BARE_PATTERN = re.compile(
    r'(?<![A-Z])§([\d.A-Za-z]+)'
)

def find_bare_refs(filepath):
    """Find bare internal references in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    results = []
    for line_num, line in enumerate(lines, 1):
        # Skip lines that are likely table of contents or metadata
        if line.strip().startswith('|'):
            continue
        
        for match in BARE_PATTERN.finditer(line):
            section = match.group(1)
            # Get context: show the line with position
            context = line.rstrip()
            start = max(0, match.start() - 30)
            end = min(len(context), match.end() + 30)
            context_snippet = context[start:end]
            results.append({
                'line': line_num,
                'section': section,
                'context': context_snippet,
                'full_line': context
            })
    
    return results

def main():
    """Find all bare internal references."""
    source_path = Path(SOURCE_DIR)
    all_bare_refs = {}
    
    for md_file in sorted(source_path.glob("*.md")):
        refs = find_bare_refs(md_file)
        if refs:
            all_bare_refs[md_file.name] = refs
    
    if not all_bare_refs:
        print("✓ No bare internal references found.")
        return
    
    print(f"Found bare internal references in {len(all_bare_refs)} files:\n")
    
    total = 0
    for filename, refs in all_bare_refs.items():
        print(f"\n{filename}:")
        # Group by section number
        by_section = {}
        for ref in refs:
            section = ref['section']
            if section not in by_section:
                by_section[section] = []
            by_section[section].append(ref)
        
        for section in sorted(by_section.keys()):
            ref_list = by_section[section]
            print(f"  §{section}: {len(ref_list)} occurrence(s)")
            for ref in ref_list[:2]:  # Show first 2 occurrences
                print(f"    Line {ref['line']}: ...{ref['context']}...")
            if len(ref_list) > 2:
                print(f"    ... and {len(ref_list) - 2} more")
            total += len(ref_list)
    
    print(f"\n\nTotal bare references: {total}")
    print("\nThese need manual fixing. For each bare §X.Y reference:")
    print("1. Determine which paper it should reference")
    print("2. Convert §X.Y to (PAPER §X.Y)")

if __name__ == "__main__":
    main()
