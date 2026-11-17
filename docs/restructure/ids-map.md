# Id map: planning ids to shortcodes

Author decision, 2026-11-17: the shortcodes of `shortcodes.md` are the page ids. The S numbers (S1 to S12, with `-A` and `-B`) were planning labels; they appear in `map.md`, `ledger.md`, `template.md` and the three stage D designs (`site/ids.md`, `hooks.md`, `checker.md`) and are read through this table. The manifest `docs/model-v3/outputs.yml` already uses shortcodes.

| Planning id | Shortcode | Page |
|---|---|---|
| S1 | FAIR | Is the tax fair? |
| S2 | LIT | Prior work and literature |
| S3 | MECH | How the tax works |
| S4 | VAL | Valuation |
| S4-A | DECL | Declaration incentives |
| S5 | FISC | Rates and revenue |
| S6 | PAY | Who pays |
| S6-A | BEHAV | Behavioural responses |
| S6-B | WELF | Welfare comparison |
| S7 | FUND | The fund and replaced taxes |
| S8 | CORP | Companies |
| S8-A | ATTR | Entity attribution |
| S9 | GOV | Law and governance |
| S10 | POL | Politics and adoption |
| S11 | FIRST and WIDER | Direct effects; wider transmission effects |
| S12 | UNCER, LIMIT and FALS | Empirical uncertainties; structural limitations; falsification |
| H0 to H7 | H0 to H7 | hub sections, unchanged |
| (standalone) | ADD, INST, SCOPE | outside the wheel |

## Rules
- **Page id, URL and file:** the shortcode lower-cased for URLs (`/fisc.html`), upper-case in front matter (`spoke: FISC`) and for the file (`source/spokes/FISC.md`).
- **Figure and table ids:** `fig-<CODE>-<n>` and `F-<CODE>-<n>` (`fig-FUND-1`, `F-FUND-1`).
- **Cross-references:** `(FISC §2)`. The old `(S5 §2)` form is retired with the S numbers.
- **The `-A` suffix retires.** Appendix status is no longer in the id. A page that overflows its 6,000-word cap gets its own shortcode, reached from its parent.
- **Splits:** S11 and S12 are split by `shortcodes.md`. Until the ledger rows are re-assigned (stage B follow-up), the ledger's S11 rows go to FIRST or WIDER and its S12 rows to UNCER, LIMIT or FALS by subject, and the spoke word budgets of `template.md` section 3 are recomputed then.
- **Assignment of outputs:** the manifest gives S11 outputs to FIRST (O4a, O4b) or WIDER (OS1), and S12 outputs to UNCER, except the stress test CK1, which goes to FALS. No output is assigned to LIMIT, since structural limits are not numeric; the author may reassign.
