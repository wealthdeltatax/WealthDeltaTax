# 152: One year loop shared by burden and ledger (household arm)

- **Status:** ready; released by the author 2026-11-27 (the 180c profile already names it; 179c may refine)
- **Agent:** 5
- **Needs:** ~179c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 179c (the profile says whether it is worth it), 171c
- **Read:** `results/speedup/profile-after-154c.md` (when it exists); `model/model_v3/runner/arm.py` (329 of 330 lines: new code goes in `switches.py` or a new file); `model/model_v3/core/burden.py`; `model-specs/architecture.md` 5.1

## Goal
Under the household arm the burden run and the revenue and ledger run each walk the same years over the same lines. Share one year loop if the profile shows the duplication costs a real share of `core_run`. Small to medium gain by the guru's guess; probably not byte-identical, because shared sums change the order of float additions.

## Design
Decided only after 179c. Until then: the profile row it must show (share of `core_run` spent in the duplicated work), the proof (byte-identical if the order of operations is kept; else a tolerance rule signed off, as 153c), the layer check, the `arm.py` budget.

## Touches
Named after 179c; at least `runner/arm.py` or `switches.py`, `core/burden.py`, `tests/model/model_v3/`, `results/speedup/ledger.md`.

## Acceptance criteria
Written when the brief is released: the profile share, the proof, the bench times before and after.

## Out of scope
The compiled kernel (180c): if the kernel brief goes ahead, this one may be dropped because the loop is rewritten there.

## Open questions
Whether to do it at all if 180c is adopted; decided after 179c and 180c stage A.

## Implementation notes
<!-- progress:start -->
- **State:** parked
<!-- progress:end -->
