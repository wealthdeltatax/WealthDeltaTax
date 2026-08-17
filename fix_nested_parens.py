"""
fix_nested_parens.py — Fix all corrupted nested parentheses from script issues
Patterns like (GOV.B (GOV.A §C)1) need to become (GOV.B §C) or similar
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Fix nested parentheses patterns
NESTED_FIXES = [
    # (GOV.B (GOV §...) → (GOV.B §...)
    (r'\(GOV\.B \(GOV §([A-Z]\.\d+)\)\)', r'(GOV.B §\1)'),
    (r'\(GOV\.B \(GOV §([A-Z])\)\)', r'(GOV.B §\1)'),
    (r'\(GOV\.B \(GOV §([A-Z]\.\d+\.\d+)\)\)', r'(GOV.B §\1)'),
    
    # (GOV.B (GOV.A §...) → (GOV.B §...) - strip inner reference
    (r'\(GOV\.B \(GOV\.A §([A-Z]\.\d+)\)[\d\)]*\)', r'(GOV.B §\1)'),
    (r'\(GOV\.B \(GOV\.A §([A-Z])\)[\d\)]*\)', r'(GOV.B §\1)'),
    (r'\(GOV\.B \(GOV\.A §([A-Z]\.\d+\.\d+)\)[\d\)]*\)', r'(GOV.B §\1)'),
    
    # (GOV.A (GOV.A §...) → (GOV.A §...)
    (r'\(GOV\.A \(GOV\.A §([A-Z]\.\d+)\)\)', r'(GOV.A §\1)'),
    (r'\(GOV\.A \(GOV\.A §([A-Z])\)\)', r'(GOV.A §\1)'),
    
    # Standalone (GOV.A §...) patterns that got corrupted
    (r'\(GOV\.B \(GOV\.A §([A-Z])[\)\.].*?\)([0-9])\)', r'(GOV.B §\1.\2)'),
    
    # Just remove inner parens and keep outer structure
    (r'\(GOV\.([A-Z]\.?) \(GOV([\.A-Z]*) §', r'(GOV.\1 §'),
]

def fix_nested_parens(filepath):
    """Fix nested parentheses in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    total_fixes = 0
    
    for pattern_str, replacement in NESTED_FIXES:
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
    """Fix nested parentheses in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_nested_parens(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} nested parentheses across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if total_fixes == 0:
        print("No nested parentheses found to fix.")

if __name__ == "__main__":
    main()
