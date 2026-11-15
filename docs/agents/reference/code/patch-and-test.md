# Patches, tests and the JST sample

How edits to large files are made, tested and recorded. Decided by the user: (1) edits to
large files go through a Python patch with a matching test; (2) the JST file is too big to
read, so tests use a small extract made by a script; (3) every patch, test and fixture lives
in `model/test/` and runs from there.

Contents: 1 When this applies · 2 Layout · 3 One-time setup · 4 The workflow · 5 Writing
anchors · 6 Writing the test · 7 The JST sample · 8 The log · 9 What you can and can't run

---

## 1. When this applies

A **large file** is one you can't comfortably hold in context or would have to rewrite to
change: `wdt_core.py`, `valgen_core.py`, `rates_core.py`, `WDT_Params.toml`, and any other
file over a few hundred lines. Edit those with a patch. Reasons: the patch is a reviewable
record of exactly what changed, it fails loudly instead of rewriting something you didn't
read, and its test says what the change was supposed to do.

Not patches: a **new** file (use Write; add a test if it has logic) and a change of a few
lines in a small file (Edit is fine). Use judgment at the edge, and lean towards a patch
when the file is one the pipeline depends on. The patch/test rule does not replace the
other conventions: a patch that changes numbers still gets the "never change numerics
silently" treatment (SKILL.md rule 5).

## 2. Layout

```
model/                      the folder that holds WDT_Params.toml (older text calls it model)
    wdt_core.py, wdt_jst.py, wdt_kernel.py, …    wherever they actually are; never assume
    test/
        wdt_patchlib.py              helper library (copied from `patch-kit/`)
        extract_jst_sample.py        JST extractor (copied from `patch-kit/`)
        patch_NNN_slug.py            one patch each, numbered in order of writing
        test_patch_NNN_slug.py       its test
        PATCHES.md                   one line per patch (section 8)
        fixtures/jst_sample.json     the small JST (generated; safe to delete and regenerate)
        _backups/patch_NNN_slug/     originals saved by --apply (generated)
```

Nothing here hardcodes a path. `wdt_patchlib.model_root()` walks up from `test/` to the
folder with `WDT_Params.toml`; `find_file('wdt_core.py')` returns the single match under it
(and errors, listing candidates, if there are none or two). The cores may sit in subfolders
(`RATES/`, `VAL/`): `add_import_paths()` puts every folder with a `*_core.py` or `wdt_*.py`
on `sys.path`. Run `python wdt_patchlib.py` first in a new checkout to see the layout it found.

Existing tests (`kernel_test.py`, `test_valgen_pairs.py`, `rates_test.py`, `test_wdt_*.py`)
stay where they are unless the user asks to move them; several use `Path(__file__).parent` to
find the modules, so a move needs that line changed. New tests all go in `model/test/`. They are
not presentation scripts, so they may import any layer (cores included); keep real logic in the
core, not in the test.

## 3. One-time setup

Copy `patch-kit/wdt_patchlib.py` and `patch-kit/extract_jst_sample.py` into
`model/test/` (if the user hasn't already). Check with `python wdt_patchlib.py` (layout, import
dirs, next number). Generate the fixture once with `python extract_jst_sample.py` (section 7).

## 4. The workflow

1. **Locate, don't load.** Grep for the region (`Grep -n` with a few lines of context), then Read
   only that range. Don't read a 1,500-line file to change ten lines.
2. **Number it.** `python wdt_patchlib.py next` → `007`. Files: `patch_007_slug.py`,
   `test_patch_007_slug.py` (slug: lowercase words that say what it does).
3. **Write the patch** from `patch-kit/patch_template.py`: a docstring (files, whether numbers
   change, the plan item), then `SPEC = {file name: [ops]}`.
4. **Write the test** from `patch-kit/test_patch_template.py`: the generic checks come with the
   template; you write section 8 (what this patch is for).
5. **Run the test** (`python test_patch_007_slug.py`). It works on a copy of the code, so it is
   safe before anything is applied. Fix until green.
6. **Dry-run the patch on the real tree** (`python patch_007_slug.py`), then **apply** it
   (`--apply`). The user applies it, or you do if you have the real files (section 9).
7. **Check the real tree** (`python test_patch_007_slug.py --live`), then run the affected core
   and its dependents in pipeline order (SKILL.md rule 7).
8. **Log it** in `PATCHES.md`.

A patch is never deleted or edited after it has been applied. A mistake is fixed by the next
patch. The numbered sequence is the audit trail, and later patches may rely on earlier ones.

## 5. Writing anchors

- Copy the anchor **verbatim** from the file, including indentation. Write `\n` in the string
  whatever the file uses: the library converts to the file's own line endings (the repo is used
  on Windows; `.bat` and possibly CRLF sources), and keeps UTF-8 (£, τ, ρ).
- It must match **exactly once**. Zero matches or several abort the whole patch with the line
  numbers, and nothing is written. Fix by adding a neighbouring line, not by loosening the text.
- Prefer a signature line plus its neighbour (`"    return out\n\n\ndef rate_params(p):"`) to a
  bare phrase like `return out` that appears thirty times.
- Pick the smallest op: `InsertAfter` / `InsertBefore` to add, `Replace` to change, `Delete` to
  remove. Several small ops beat one big `Replace` of a whole function: the dry run then shows
  which landed, and a failure points at one anchor.
- `done=` is the text that exists only **after** the edit. It makes a re-run a no-op. Give it
  explicitly for inserts (the anchor is still there afterwards) and whenever `new` is generic.
  Under 12 characters the library refuses it as too generic. If the sandbox test says an op was
  "skipped" on its first run, the marker is already in the file or the anchor is mistyped.
- All edits to all files are staged and validated (`.py` compiles, `.toml` parses) before any is
  written, so a failed patch never leaves a half-edited tree.
- One patch = one purpose. A behaviour change and a pure move are two patches (refactoring
  mode, SKILL.md), so a pure move can be checked for identical numbers.

## 6. Writing the test

The template's checks 1 to 7 are the same for every patch (dry run writes nothing; apply changes
the files; second run is a no-op; valid Python/TOML; line endings kept; files it doesn't name
are untouched; the existing tests do no worse than before). Section 8 is the point of the test.

- **Assert behaviour, not text.** "The string is in the file" proves the patch ran, not that it
  works. Import the patched module in a subprocess (`wl.run_py(sandbox, [...])`, so the test
  doesn't pollute its own process) and call the function with a hand-worked case, as
  `kernel_test.py` does (ratio-mirror round trip, lien recursion).
- **A patch that should not change numbers** gets a test that does the same run before and after
  on the sample data and asserts equality (tolerance 1e-9, the project's bridge tolerance).
- **A patch that changes numbers** states in its docstring which outputs move, and the test pins
  the new value against an independent hand calculation, never against its own output.
- **New TOML keys:** assert the key parses through `wdt_core.load_params` (or
  `load_rates_params`) and that a misspelt or out-of-range value raises.
- **Regression list:** `REGRESSION` in the template names existing tests to run before and after
  on the sandbox. A test that already fails before the patch (needs the real JST or `OUTPUTS/`)
  is compared, not blamed: the check is "no worse than before".
- Don't weaken a check to make a test pass. If the sample data trips a core's own `validate`,
  say so and look into it; the sample is smaller than the real data and some counts will differ.

## 7. The JST sample

The full `jst_r6.json` is multi-megabyte. Never read or paste it. `extract_jst_sample.py` writes
a small file with the same structure to `test/fixtures/jst_sample.json`, and the sandbox puts it
where `[rates].jst_path` is looked up, so `wdt_jst.load_jst`, `rates_core` and `valgen_core` read
it unchanged.

```
python extract_jst_sample.py                                  GBR + USA, 1950-2017, only the series the code reads
python extract_jst_sample.py --countries GBR PRT --years 1900 2017
python extract_jst_sample.py --gap 1975                       blank one year: tests `contiguous` and the seam
python extract_jst_sample.py --keep hpnom                     force another series in
```

- **Series kept:** those whose name appears as a quoted string in the project code, plus the four
  `wdt_jst` reads (`capital_tr`, `cpi`, `gdp`, `pop`). The script prints the list. If a test
  later fails with a missing series, the code built the name dynamically: re-run with `--keep`.
- **It is for mechanics, not numbers.** A 68-year sample is shorter than T = 100, so every window
  repeats years (flagged `repeat`), which is exactly what the loop/seam tests want and exactly why
  you must not quote results from it. A test that needs non-repeating windows shortens `T` in the
  *sandbox* TOML (a `Replace` on the sandbox copy), never in the real one.
- **What a sample should exercise:** a country with a long clean series (GBR), a second country,
  a calendar gap (`--gap`), and, for repeat flags, one country whose usable years are fewer than T.
  Pick the countries for the test you are writing, not once for all.
- It records its own provenance in a `_sample` block. A fixture is generated: regenerate rather
  than hand-edit it, and don't commit anything derived from it as a result.
- If the extractor stops with "unexpected JST structure", it prints what it found. The structure
  it assumes is the one `wdt_jst._jst_series` reads (`countries[ISO] = {years, series{name:[…]}}`).

## 8. The log

`model/test/PATCHES.md`, one line per patch, appended when it is applied:

```
| 007 | 2026-10-12 | patch_007_lambda_split.py | valgen_core.py, WDT_Params.toml | independent λ_C, λ_D | numbers move: VAL JSON, tables 5_6, figs 5_7 | applied |
```

Columns: number, date, patch file, files touched, one-phrase purpose, whether numbers move (and
what to re-run), status. If a plan item or decision drove it (D6, D12), name it in the purpose.
This is also where "Drift noticed" items that a patch closes get recorded, so the user can strike
them from `drift-register.md`.

## 9. What you can and can't run

You may not have the real files in your session (they live on the user's machine). Say what you
actually did:

- **Files available:** write the patch and test, run the test on the sandbox, report the output.
  Don't `--apply` to the user's real tree unless they asked; give them the commands.
- **Files not available:** write the patch and test, say plainly that neither has been run, and
  give the exact commands (`python test_patch_007_slug.py`, then the dry run, then `--apply`, then
  `--live`). Anchors written from a pasted excerpt are unverified until the dry run says otherwise,
  so tell the user to expect an "anchor not found" and what to send back if they see one.
- Never report a patch as applied or a test as passing on the strength of reading the code.
