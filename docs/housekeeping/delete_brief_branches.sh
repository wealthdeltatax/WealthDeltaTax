#!/usr/bin/env bash
# Deletes remote brief/* branches whose briefs are merged or retired (as of 2026-11-23 11:30).
# In-flight branches are left out: 057, 135, 140, 146. Re-generate with: git ls-remote --heads origin "brief/*"
# Run from a clone with push rights; PowerShell: see docs/housekeeping/README.md
set -u
git push origin --delete brief/130-readable-research
git push origin --delete brief/137-floor-zero-units
git push origin --delete brief/145-withdrawal-and-saving-evidence
