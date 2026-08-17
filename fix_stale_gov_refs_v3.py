"""
fix_stale_gov_refs_v3.py — Fix remaining stale GOV references
Handles trailing dots and GOV.A references
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# All remaining stale references to fix
FINAL_MAPPINGS = {
    # Stale main GOV sections with trailing dots (just remove the dot, they're now valid)
    r'\(GOV §(\d+)\.\)': r'(GOV §\1)',
    r'\(GOV §(\d+\.\d+)\.\)': r'(GOV §\1)',
    
    # Specific stale mappings that still need updating
    r'\(GOV §2\.2\)': '(GOV §5.1)',  # anti-collusion guarantee → GOV §5.1
    r'\(GOV §3\.3\)': '(GOV §5.1)',  # Also anti-collusion related
    
    # GOV.A references with trailing dots (just remove the dot)
    r'\(GOV\.A §([A-Z])\.\)': r'(GOV.A §\1)',
    r'\(GOV\.A §(\d+)\.\)': r'(GOV.A §\1)',
    r'\(GOV\.A §([A-Z]\.\d+)\.\)': r'(GOV.A §\1)',
    
    # GOV.B references with trailing dots
    r'\(GOV\.B §([A-Z])\.\)': r'(GOV.B §\1)',
    r'\(GOV\.B §([A-Z]\.\d+)\.\)': r'(GOV.B §\1)',
}

def fix_remaining_stale_gov_refs(filepath):
    """Fix remaining stale GOV references."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    total_fixes = 0
    
    for pattern_str, replacement in FINAL_MAPPINGS.items():
        pattern = re.compile(pattern_str)
        matches = list(pattern.finditer(content))
        if matches:
            content = pattern.sub(replacement, content)
            total_fixes += len(matches)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return total_fixes
    
    return 0

def main():
    """Fix remaining stale GOV references in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_remaining_stale_gov_refs(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} remaining stale GOV references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if total_fixes == 0:
        print("No remaining stale GOV references found.")

if __name__ == "__main__":
    main()
