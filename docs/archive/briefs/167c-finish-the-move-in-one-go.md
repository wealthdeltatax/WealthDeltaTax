# 167: Finish the file move in one go, using the apply tool and the rehearsal patch (replaces 162c to 164c if it passes)

- **Status:** dropped by the author 2026-11-25 before it started (stages run one at a time)
- **Author/date:** K. Ogata with the guru, 2026-11-25
- **Depends on:** 160c, 161c and 165c merged (done); no other branch may touch paths while this runs
- **Read (6):** `docs/briefs/044c-file-layout-move.md` (rules R1 to R5, tree, hazards, verification tiers); `docs/restructure/rehearsal-report.md`; `docs/restructure/file-layout-map.md`; and the three stage briefs `162c`, `163c`, `164c` (their "Design", "Rulings" and "Added from the rehearsal" sections apply here unchanged). `docs/restructure/rehearsal-fixes.patch` is applied, not read.

## Goal
The stages 162c (model code and inputs), 163c (specs and results) and 164c (project, skills, final sweep) are done as one move, because the rehearsal showed the whole map applies mechanically. The author skips the three stage briefs if, and only if, the trial below passes. If it fails, stop and report; the three stage briefs then run as written.

Rules, tree and hazards: 044c (R1 to R5, hazards 1 to 10). Any content change beyond paths, the R3 renames and the listed rulings is stop-and-report. Suites run in the background, one pytest per suite, never piped; use `git clean -fdx` (or a fresh clone) before every final check.

## Design: three blocks, one push per block
**Block 1: the trial on a scratch copy (go or no-go).** Make a full-history scratch clone of current `main` (outside this repository's folder, deleted at the end). Run `python pipeline/path_refs.py --apply <clone>` for the remaining stages; then take the hunks of `rehearsal-fixes.patch` labelled `# ===== stage 162c`, `163c`, `164c` and apply them (the 160c and 161c hunks are already done: skip them). The patch was built on the tree before 160c and 161c merged, so some hunks may reject: fix each by hand and count them. Then the verification tiers: static checks, `path_rewrite_proof.py` (with the shared `Rewriter`, ruling in 162c), `move_tripwire.py`, suites. **Go** only if all hold: tripwire PASS; proof shows no unexplained change; data, gate, tools, model_v3 (about 10 minutes), website and project suites pass in a clean tree; `check_agent_docs.py` exits 0; no suite fails for a reason other than a path; at most 40 hunks rejected; every content line changed beyond paths is on the declared list (pinned lines, the proof change, converter re-root, prose sweep). **No-go** otherwise: stop, push only the report. Push the report `docs/restructure/trial-report.md` (go or no-go with the counts, the rejected hunks and what each needed).

**Block 2: the real move, model side (R4 and R5).** Only if Go. On the branch of this brief, repeat the same steps on the real tree: apply, the stage 162c and 163c hunks (as adjusted in the trial), the pinned-list allow-list, the proof change, the verification tiers, one push.

**Block 3: project, skills, final sweep (R6) and acceptance.** The 164c work: project documents and `Tools/` to `project/`; the prose sweep (37 findings, by hand); converter re-root and home; the five `.skill` archives regenerated and every changed skill line listed in the report; the duplicate-name script and the root check; the 044c acceptance criteria. No `quick` comparison (057c is not merged, so there is no reference to compare); the tripwire's four evaluation cases stand in, and the report says so. One push.

## Touches
Everything except the content of `model/` (paths only), the archived briefs and decision history. Nothing in the model's numbers.

## Acceptance criteria
- Block 1: the trial report with a clear Go or No-go and the counts.
- Block 2 and 3: the 044c acceptance criteria met (tree by type, unique descriptive names, duplicates removed, readers rewritten), tripwire equal to the baseline, proof clean, digest and gate hash unchanged, all suites and `check_agent_docs.py` pass (a red site accepted per R5 and listed), skills rebuilt with the changed lines listed, local-only files to move by hand listed.

## Out of scope
Any model change; the speed-ups; 057c; the Actions workflow; editing archived briefs or decision history.

## Open questions
None. If the trial is a No-go or any rule cannot settle a call, stop and report; do not improvise.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** not started
<!-- progress:end -->
