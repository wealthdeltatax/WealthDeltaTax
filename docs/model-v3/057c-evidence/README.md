# 057c evidence (paused 2026-11-24)

Files produced while building brief 057c, kept so the work can resume without re-running it. **All of it is dated evidence, not acceptance.** Everything here was produced on a tree at or before commit `4c91a86`; `main` has since moved (089c, 147c, the 044c briefs) and the manifest hash no longer matches, so none of these files validates today. Regenerate before relying on any figure. Run command for all `quick` files: `python -I -c "import sys; sys.path.insert(0,'.'); from model_v3 import run; run.main(['--size','quick','--out',DIR])"` (seed 20261118, 1,000 level 1 paths, 50 tornado paths, 0 O1e draws, tolerance 1e-2, five grid points, serial, `--workers 1`, a 2-core machine).

| Folder | What | Wall time | State |
|---|---|---|---|
| `quick-q3/` | `quick` run after the sixth-round code (cap, `target_not_met`, `no_sign_change_0_15`, O1e root at 0 draws). All five points in the range; 2 of 5 met their target. Validated with 0 errors on the tree at `4c91a86`; fails V8 (manifest hash) on current main. 10 of 12 O8 cells are null. | 3,991 s | **The current reference, stale until regenerated** |
| `quick-q2-superseded/` | `quick` run with the cap only around level 1: three points still failed (the error was also raised in the tornado), O1e centre wrongly `no_sign_change_0_15` for all three schedules (a NaN range hid finite roots). | 3,534 s | Superseded by q3 |
| `quick-q1-superseded/` | `quick` run before the sixth round: two points in the range, three failed and left out, O1e centre null. | 2,665 s | Superseded; its 44 min is the figure quoted in the author's decision of 2026-11-24 |
| `smoke-round3/` | `--size smoke`-equivalent file from round 3 (50 paths, one point), before the market-fund O1e. | 7.7 min | Superseded (smoke is now 17 min) |
| `scripts/final1.py`, `final1.txt` | Times one final-size grid point without O1e (level 1 at 10,000 paths on 3 schedules, tornado at 1,000 paths): **5,655 s (94 min)**, serial; 150c projected 79 min. | | Measurement, still true of the code at `4c91a86` |
| `scripts/o1e.py`, `keys.py`, `tc.py`, `time_ev.py` | Throw-away probes: M1 against the generator mean under the safe and market funds; the sample keys of O1, O2, O3, O4a; a tiny-size run of the convergence helpers; the timing of one evaluation. | | Reusable as written; paths are relative to the repository root |

Not preserved because stale and reproducible: the round-2 smoke baselines (`real_ok.json`, `real_seed.json`).
