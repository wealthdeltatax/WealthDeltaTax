"""
fix_stale_gov_refs.py — Manually fix stale GOV section references
Maps old GOV sections to new locations based on context
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Mapping of stale GOV sections to correct references
# Based on current series.yml structure analysis
STALE_GOV_MAPPINGS = {
    # GOV §5.1 "Anti-Collusion Guarantee" exists in current structure
    "GOV §2.2": "GOV §5.1",  # anti-collusion related
    "GOV §3.3": "GOV §5.1",  # anti-collusion related
    
    # GOV §7 is "Limitations and Further Work", GOV §8 is "Conclusion"  
    # Old §7.2-7.5 and §8.3-8.8 and §9+ don't exist
    # Most operational details moved to GOV.B
    
    # Route D Auction is now GOV.B §G
    "GOV §9": "GOV.B §G",
    "GOV §10": "GOV.B §G",
    "GOV §9.1": "GOV.B §G.1",
    "GOV §10.3": "GOV.B §G.4",
    
    # SWF operational details are in GOV.B §E
    "GOV §8.3": "GOV.B §E.3",
    "GOV §8.4": "GOV.B §E.3",
    "GOV §8.5": "GOV.B §E.3",
    "GOV §8.6": "GOV.B §E.3",
    "GOV §8.7": "GOV.B §E.3",
    "GOV §8.8": "GOV.B §E.3",
    
    # Limitations and other GOV §7.x sections
    "GOV §7.2": "GOV §7",  # These are about limitations which is now GOV §7
    "GOV §7.3": "GOV §7",
    "GOV §7.4": "GOV §7",
    "GOV §7.5": "GOV §7",
    
    # Trailing dots (stale references with periods at end)
    "GOV §4.": "GOV §4",
    "GOV §5.2.": "GOV §5.2",
    "GOV §5.3.": "GOV §5.3",
    "GOV §6.": "GOV §6",
    "GOV §6.1.": "GOV §6.1",
    "GOV §6.3.": "GOV §6.3",
    "GOV §6.4.": "GOV §6.4",
    "GOV §8.": "GOV §8",
    "GOV §9.": "GOV §8",  # GOV §9 doesn't exist, reference "Limitations"
    "GOV §10.": "GOV.B §G",  # GOV §10 doesn't exist
    
    # Stray references
    "GOV §11.1": "GOV §8",  # GOV §11 doesn't exist
    
    # Already malformed ones from previous script corruption
    # These have trailing parentheses or weird prefixes
}

def fix_stale_gov_in_file(filepath):
    """Fix stale GOV references in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    total_fixes = 0
    
    # Sort by length descending to avoid partial replacements
    for old_ref, new_ref in sorted(STALE_GOV_MAPPINGS.items(), key=lambda x: len(x[0]), reverse=True):
        # Match both (GOV §X.Y) and bare GOV §X.Y formats
        pattern = re.compile(
            r'\(GOV\s+' + re.escape(old_ref.replace("GOV ", "§")) + r'\)' +
            r'|' +
            r'\bGOV\s+' + re.escape(old_ref.replace("GOV ", "§")),
            re.IGNORECASE
        )
        
        def replace_func(m):
            # If it was bracketed, keep bracketed
            if m.group(0).startswith('('):
                return f'({new_ref})'
            else:
                return f'({new_ref})'  # Convert bare refs to bracketed
        
        matches = list(pattern.finditer(content))
        if matches:
            content = pattern.sub(replace_func, content)
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
        fixes = fix_stale_gov_in_file(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} stale GOV references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        print(f"  {filename}: {count} references")
    
    if not files_fixed:
        print("No stale GOV references found to fix.")
    
    print("\n⚠ Note: These mappings are educated guesses based on structure analysis.")
    print("Please verify the replacements against the actual content context.")

if __name__ == "__main__":
    main()
