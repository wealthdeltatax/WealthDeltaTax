"""
fix_bracketless_refs.py — Fix bracketless external references
Converts: GOV §5.2 → (GOV §5.2)
Handles: Negative lookbehind/lookahead to avoid double-bracketing

Usage: python fix_bracketless_refs.py
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Safe regex: won't match if already in parentheses
PATTERN = re.compile(
    r'(?<!\()([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\s+§([\d.A-Za-z]+)(?!\))'
)

def fix_file(filepath):
    """Fix bracketless references in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    def replace_func(match):
        shortcode = match.group(1)
        section = match.group(2)
        return f'({shortcode} §{section})'
    
    content = PATTERN.sub(replace_func, content)
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Count replacements
        matches = list(PATTERN.finditer(original_content))
        return len(matches)
    
    return 0

def main():
    """Fix all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_file(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} bracketless references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if not files_fixed:
        print("No bracketless references found.")

if __name__ == "__main__":
    main()
