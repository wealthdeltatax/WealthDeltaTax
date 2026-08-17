"""
fix_gov_appendix_refs.py — Fix GOV references that should point to GOV.A/GOV.B
References like (GOV §A.1) should be (GOV.A §A.1)
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Map letter-prefixed GOV sections to appendix references
APPENDIX_MAPPINGS = {
    # Letter-only sections (A, B, C, D, E, F, G, H)
    r'\(GOV §([A-H])\)': r'(GOV.A §\1)',
    r'\(GOV §([A-H])\.\)': r'(GOV.A §\1)',
    
    # Letter.number sections (A.1, B.2, C.3, etc)
    r'\(GOV §([A-H])\\.(\d+)\)': r'(GOV.A §\1.\2)',
    r'\(GOV §([A-H])\\.(\d+)\.\)': r'(GOV.A §\1.\2)',
    
    # Letter.number.number sections
    r'\(GOV §([A-H])\\.(\d+)\\.(\d+)\)': r'(GOV.A §\1.\2.\3)',
}

def fix_gov_appendix_refs(filepath):
    """Fix GOV references that should point to appendices."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    total_fixes = 0
    
    for pattern_str, replacement in APPENDIX_MAPPINGS.items():
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
    """Fix GOV appendix references in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_gov_appendix_refs(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} GOV appendix references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if total_fixes == 0:
        print("No GOV appendix reference errors found.")

if __name__ == "__main__":
    main()
