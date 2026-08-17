"""
fix_bare_refs.py — Fix bare internal references by adding paper prefix
Each bare §X.Y gets the paper code from its filename prefix
"""

import re
from pathlib import Path

SOURCE_DIR = "source_md"

# Map filename patterns to paper shortcodes
FILE_TO_PAPER = {
    "1.0": "WP",          # Whitepaper
    "2.0": "MF",          # Moral and Philosophical
    "3.0": "LR",          # Research Gaps (summary of LR)
    "3.1": "LR.B",        # Intellectual Background (LR.B)
    "4.0": "JUR",         # UK Jurisdiction
    "5.0": "VAL",         # Valuing Wealth
    "5.1": "VAL.A",       # Valuing Wealth Appendix A
    "5.2": "VAL.B",       # Valuing Wealth Appendix B
    "6.0": "CORP",        # Corporate Architecture
    "6.1": "CORP.A",      # Corporate Architecture Appendix
    "7.0": "GOV",         # Constitutional Governance
    "7.1": "GOV.A",       # GOV Intellectual Appendix
    "7.2": "GOV.B",       # GOV Operational Appendix
    "8.0": "RATES",       # Rates and Revenue
    "8.1": "RATES.A",     # Rates and Revenue Appendix
    "9.0": "SWEEPS",      # Parameter Sweeps
    "9.1": "SWEEPS.A",    # Parameter Sweeps Appendix
    "10.0": "BEHAV",      # Behavioural Robustness
    "11.0": "CLOSE",      # Position Closure
    "12.0": "POL",        # Political Architecture
    "13.0": "PHASE1",     # Phase One
    "14.0": "ENV",        # Environmental Effects
    "15.0": "FM",         # First Mover
    "16.0": "MOD",        # Modular Adoption
}

# Pattern for bare § references: NOT preceded by a paper code
# Negative lookbehind ensures we don't match (VAL §5.2) style which is already fixed
BARE_PATTERN = re.compile(
    r'(?<![A-Z])(?<!\()§([\d.A-Za-z]+)(?!\))'
)

def get_paper_code(filename):
    """Extract paper code from filename."""
    # Get the prefix (e.g., "1.0", "7.2")
    prefix = filename.split("_")[0]
    return FILE_TO_PAPER.get(prefix, None)

def fix_bare_refs_in_file(filepath):
    """Fix all bare internal references in a file."""
    filename = filepath.name
    paper_code = get_paper_code(filename)
    
    if not paper_code:
        print(f"  ⚠ {filename}: Unknown paper code prefix")
        return 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    def replace_func(match):
        section = match.group(1)
        # Check if this looks like it's already bracketed
        # (should not happen given our negative lookbehind, but be safe)
        return f'({paper_code} §{section})'
    
    content = BARE_PATTERN.sub(replace_func, content)
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Count replacements
        matches = list(BARE_PATTERN.finditer(original_content))
        return len(matches)
    
    return 0

def main():
    """Fix bare internal references in all source files."""
    source_path = Path(SOURCE_DIR)
    total_fixes = 0
    files_fixed = []
    
    for md_file in sorted(source_path.glob("*.md")):
        fixes = fix_bare_refs_in_file(md_file)
        if fixes > 0:
            files_fixed.append((md_file.name, fixes))
            total_fixes += fixes
    
    print(f"✓ Fixed {total_fixes} bare internal references across {len(files_fixed)} files:")
    for filename, count in files_fixed:
        paper_code = get_paper_code(filename)
        print(f"  {filename} ({paper_code}): {count} references")
    
    if not files_fixed:
        print("No bare internal references found to fix.")

if __name__ == "__main__":
    main()
