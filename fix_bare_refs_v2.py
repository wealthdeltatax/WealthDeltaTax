"""
fix_bare_refs_v2.py — Fix bare internal references (with better exclusions)
Skips tables, footnotes, and other problematic sections
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Map filename patterns to paper shortcodes
FILE_TO_PAPER = {
    "1.0": "WP", "2.0": "MF", "3.0": "LR", "3.1": "LR.B",
    "4.0": "JUR", "5.0": "VAL", "5.1": "VAL.A", "5.2": "VAL.B",
    "6.0": "CORP", "6.1": "CORP.A", "7.0": "GOV", "7.1": "GOV.A", "7.2": "GOV.B",
    "8.0": "RATES", "8.1": "RATES.A", "9.0": "SWEEPS", "9.1": "SWEEPS.A",
    "10.0": "BEHAV", "11.0": "CLOSE", "12.0": "POL", "13.0": "PHASE1",
    "14.0": "ENV", "15.0": "FM", "16.0": "MOD",
}

def get_paper_code(filename):
    """Extract paper code from filename."""
    prefix = filename.split("_")[0]
    return FILE_TO_PAPER.get(prefix, None)

def fix_bare_refs_carefully(filepath):
    """
    Fix bare internal references while avoiding:
    1. Table cells (lines starting with |)
    2. Already bracketed references
    3. Footnotes and reference sections
    """
    filename = filepath.name
    paper_code = get_paper_code(filename)
    
    if not paper_code:
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_fixes = 0
    
    for i, line in enumerate(lines):
        # Skip table rows
        if line.strip().startswith('|'):
            continue
        
        # Skip bibliography/reference sections
        if line.strip().startswith('['):
            continue
        
        # Process line: find bare §X.Y not preceded by paper code or (
        # Pattern: not preceded by alphanumeric or (, then §, then digits/dots/letters
        new_line = re.sub(
            r'(?<![A-Z0-9(])(?<!\))§([\d.A-Za-z]+)',
            lambda m: f'({paper_code} §{m.group(1)})',
            line
        )
        
        if new_line != line:
            fixes_in_line = len(re.findall(r'(?<![A-Z0-9(])(?<!\))§([\d.A-Za-z]+)', line))
            total_fixes += fixes_in_line
            lines[i] = new_line
    
    # Write back if changes made
    if total_fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return total_fixes

def main():
    """Fix bare internal references in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_bare_refs_carefully(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Carefully fixed {total_fixes} bare internal references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        paper_code = get_paper_code(filename)
        print(f"  {filename} ({paper_code}): {count} references")
    
    if not files_fixed:
        print("No bare internal references found to fix.")

if __name__ == "__main__":
    main()
