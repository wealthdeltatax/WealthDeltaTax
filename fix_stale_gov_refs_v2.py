"""
fix_stale_gov_refs_v2.py — Fix stale GOV references using v2.1 restructure mappings
Based on revision history notes showing exact corrections needed
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Mappings from GOV.B §0.7 revision notes
STALE_MAPPINGS = {
    # Primary mappings
    r'\(GOV §7\)': '(GOV §5.3)',
    r'\(GOV §8\)': '(GOV §6.3)',
    r'\(GOV §8\.3\)': '(GOV §6.3)',
    r'\(GOV §8\.4\)': '(GOV §6.3)',
    r'\(GOV §8\.5\)': '(GOV §6.3)',
    r'\(GOV §8\.6\)': '(GOV §6.3)',
    r'\(GOV §8\.7\)': '(GOV §6.3)',
    r'\(GOV §8\.8\)': '(GOV §6.3)',
    r'\(GOV §9\)': '(GOV.B §G)',
    r'\(GOV §9\.1\)': '(GOV.B §G.1)',
    r'\(GOV §9\.3\)': '(GOV §5.3)',
    r'\(GOV §10\)': '(GOV.B §G)',
    r'\(GOV §10\.3\)': '(GOV.B §G.2)',
    r'\(GOV §7\.2\)': '(GOV §5.2)',
    r'\(GOV §7\.3\)': '(GOV §5.3)',
    r'\(GOV §7\.4\)': '(GOV §5.3)',
    r'\(GOV §7\.5\)': '(GOV §5.3)',
    r'\(GOV §11\.1\)': '(GOV §8)',  # No GOV §11
    
    # Trailing dots (incomplete references)
    r'\(GOV §7\.\)': '(GOV §5.3)',
    r'\(GOV §8\.\)': '(GOV §6.3)',
    r'\(GOV §9\.\)': '(GOV.B §G)',
    r'\(GOV §10\.\)': '(GOV.B §G)',
    
    # Bare references that got corrupted
    r'G\(OV §5\)': '(GOV §5)',
    r'G\(OV §6\)': '(GOV §6)',
    r'G\(OV §5\)\.': '(GOV §5).',
    r'G\(OV §6\)\.': '(GOV §6).',
}

def fix_stale_gov_refs(filepath):
    """Fix stale GOV references in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    total_fixes = 0
    
    for pattern_str, replacement in STALE_MAPPINGS.items():
        pattern = re.compile(pattern_str, re.IGNORECASE)
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
    """Fix stale GOV references in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_stale_gov_refs(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} stale GOV references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if total_fixes == 0:
        print("No stale GOV references found to fix.")

if __name__ == "__main__":
    main()
