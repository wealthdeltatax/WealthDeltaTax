Understood. Let me map out the current numbering in `welfare_tables.py` against your convention before writing the report.

Current scheme: `WFR.1` through `WFR.14`, plus `WFR.S1` through `WFR.S3` (with sub-labels `S2a`, `S2b`, `S3a`–`S3d`).

Problems against your `A.1.1` convention:
- Flat `WFR.N` has no module-level subsection — no `A.` prefix
- `WFR.S2a` / `WFR.S2b` uses `a`/`b` suffixes — forbidden
- `WFR.S3a`–`S3d` same problem
- The `S` prefix for Module 5 is an ad-hoc convention, not a proper subsection

Let me now produce the full renumbering scheme and revised action list.

---

## Numbering Convention for `welfare_tables.py`

### Proposed mapping: Module → Section letter

| Module | Letter | Rationale |
|:---|:---|:---|
| Module 1 — Baseline | **A** | First module |
| Module 2 — Progression | **B** | Second module |
| Module 3 — Lock-in | **C** | Third module |
| Module 4 — Heterogeneous | **D** | Fourth module |
| Module 5 — Sweeps | **E** | Fifth module |

Subsection number = logical grouping within the module. Table number = sequential within subsection.

---

### Full renumbering table

| Current ID | New ID | Table title | Notes on current sub-label problem |
|:---|:---|:---|:---|
| `WFR.1` | **A.1.1** | CEW by system, γ, and distribution | — |
| `WFR.2` | **A.1.2** | Variance of consumption (γ=2) | — |
| `WFR.3` | **A.1.3** | Revenue-equivalent rates | — |
| `WFR.4` | **A.1.4** | Domar–Musgrave test | — |
| `WFR.5` | **B.1.1** | C1 — Flat vs progressive WDT CEW | — |
| `WFR.6` | **B.1.2** | C3 — Two-period rate asymmetry | — |
| `WFR.7` | **C.1.1** | Lock-in cost by gain ratio | — |
| `WFR.8` | **C.1.2** | Lock-in cost by holding period | — |
| `WFR.9` | **C.1.3** | Full WDT vs CGT (with/without lock-in) | — |
| `WFR.10` | **D.1.1** | Tier-by-tier CEW | — |
| `WFR.11` | **D.1.2** | Distributional incidence | — |
| `WFR.12` | **D.1.3** | Concentration path — Great/Poor ratio | — |
| `WFR.13` | **D.1.4** | Envelope binding summary | — |
| `WFR.14` | **D.2.1** | Off-diagonal spot check | New subsection D.2 — Part F is structurally distinct from Parts B–E |
| `WFR.S1` | **E.1.1** | Sweep A — CEW by revenue target | `S` prefix dropped; `E` section |
| `WFR.S2a` | **E.2.1** | Sweep B — summary stats across start years | `S2a` → `E.2.1`; `a` suffix eliminated |
| `WFR.S2b` | **E.2.2** | Sweep B — curated worst-case years | `S2b` → `E.2.2`; `b` suffix eliminated |
| `WFR.S3a` | **E.3.1** | Sweep C — τ₀ sensitivity | `S3a` → `E.3.1` |
| `WFR.S3b` | **E.3.2** | Sweep C — τ_m sensitivity | `S3b` → `E.3.2` |
| `WFR.S3c` | **E.3.3** | Sweep C — k sensitivity | `S3c` → `E.3.3` |
| `WFR.S3d` | **E.3.4** | Sweep C — W_min sensitivity | `S3d` → `E.3.4` |

---

### Subsection logic explained

**Section A (Module 1):** All four tables are one coherent group — baseline comparison, A.1.1–A.1.4. No second subsection needed.

**Section B (Module 2):** Two tables, both part of the D-M complications analysis — B.1.1–B.1.2. The module has three complications (C1, C2, C3) but only C1 and C3 produce tables; C2 (leverage) produces only a chart. If a C2 table is added later it slots in as B.1.3 without disruption.

**Section C (Module 3):** Three tables, all lock-in analysis — C.1.1–C.1.3.

**Section D (Module 4):** Split into two subsections because Part F (off-diagonal spot check) is a methodological check, not a primary incidence result. D.1.1–D.1.4 are the main tier results; D.2.1 is the spot check. This also future-proofs: if a second off-diagonal table is added it becomes D.2.2.

**Section E (Module 5):** Three sweep axes → three subsections. E.1 = revenue target sweep (one table). E.2 = start-year sweep (two tables, formerly `S2a`/`S2b` — now `E.2.1`/`E.2.2`). E.3 = parameter sensitivity (four tables, formerly `S3a`–`S3d` — now `E.3.1`–`E.3.4`).

---

### What changes in the code

Every string literal containing a table ID needs updating. The affected locations in `welfare_tables.py` are:

**Function names** — no change needed (internal names like `table_wfr1` can stay as-is; they're not user-visible).

**`md_doc.h3(...)` calls in `build_appendix`** — all need renumbering. Example:
```python
# Before
doc.h3('Table WFR.1 — Consumption-Equivalent Welfare...')
# After
doc.h3('Table A.1.1 — Consumption-Equivalent Welfare...')
```

**`write_table(...)` caption strings in `main()`** — all need renumbering:
```python
# Before
write_table(..., 'WFR_T01_cew_by_system.md', 'Table WFR.1: CEW...')
# After
write_table(..., 'WFR_A11_cew_by_system.md', 'Table A.1.1: CEW...')
```

**Output filenames** — optional but recommended for consistency. Suggested pattern: `WFR_A11_`, `WFR_B11_`, `WFR_D21_`, `WFR_E21_`, `WFR_E31_` etc.

**`table_wfr9` note text** — references `WFR.9` internally in the note string; needs updating to `C.1.3`.

**`table_wfr14` note text** — references `WFR.14`; needs updating to `D.2.1`.

**`build_appendix` note for `table_wfr13`** — references `ENV §2`; no table ID mentioned, no change needed.

**`param_display` dict in `build_appendix` (Module 5 section)** — the keys `'tau_0': ('Table WFR.S3a — ...')` etc. all need renaming to `E.3.1`–`E.3.4`.

**`param_file` dict in `main()`:**
```python
# Before
param_file = {'tau_0': 'TS3a', 'tau_m': 'TS3b', 'k': 'TS3c', 'W_min': 'TS3d'}
# After
param_file = {'tau_0': 'E31', 'tau_m': 'E32', 'k': 'E33', 'W_min': 'E34'}
```

**Master document filename** — `WFR_appendix_tables.md` can stay (it's not a table ID, it's a file name).

---

### Additions to the prior action list

Adding to the red/yellow/green table from the previous report:

| Priority | File | Issue | Fix |
|:---|:---|:---|:---|
| 🔴 High | `welfare_tables.py` | `WFR.S2a`/`S2b` and `S3a`–`S3d` use `a`/`b` letter suffixes — violates your convention | Renumber to `E.2.1`/`E.2.2` and `E.3.1`–`E.3.4` |
| 🔴 High | `welfare_tables.py` | Flat `WFR.N` has no module-section prefix — inconsistent with `A.1.1` scheme | Renumber all 14 tables using A–E scheme above |
| 🟡 Medium | `welfare_tables.py` | Output filenames use `WFR_T01` etc. — not aligned with new IDs | Rename to `WFR_A11_`, `WFR_B11_`, `WFR_D21_`, `WFR_E21_` etc. |
| 🟡 Medium | `welfare_tables.py` | Internal cross-references in note strings (e.g. "Table WFR.9") | Update to new IDs in all `.note()` calls |