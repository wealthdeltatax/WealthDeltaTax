# 169c stage A (d): what the numerics switch changes

Machine: Intel Xeon (Sapphire Rapids class, AVX512), numpy 2.5.3. Old path = AVX512 (`NPY_DISABLE_CPU_FEATURES=""`, what the pins were captured on); new path = `NPY_DISABLE_CPU_FEATURES=X86_V4` (`model_v3/numerics.py`).

**Feature list.** Only `X86_V4` moves the digest. Disabling `AVX512F`, `AVX512_SKX`, `AVX512_ICL` or `AVX512_SPR` alone leaves it equal to the old path (digest of seed 7: old 24fd9669..., `X86_V4` 3787c02b...). The 168c list (`X86_V4 AVX512_ICL AVX512_SPR`) equals `X86_V4`. Not yet confirmed on an AMD runner (EPYC 7763): that needs an Actions run.

**Smoke size** (`--size smoke`, 50 paths, both paths): the two `outputs.json` are byte-identical (sha256 1d2f8164fbee...). Quick size was not run locally (2 cores; no output after 10 minutes).

**Raw level-1 samples** (the legacy digest call: seeds 7 and 11, 20 paths, 5 schedules, full precision; `numerics_diff.py`). Most ids differ only in the last bits or in values that are mathematically zero. Not last-bit only:

- **O1f** (share of paths with negative net revenue): 3 of 600 values flip 1 to 0 or 0 to 1 (`centre`, `low_corner`, `tm50_k2_r100`, transition). The sign of a net revenue that is zero in theory (O1 values of order 1e-15) is decided by the rounding. At 1,000 paths one flip moves O1f by 0.1 point.
- **O2b, O2c** (cash-flow burden, `short` horizon, seed 7, `centre`): 10 values move by up to 0.22 relative (e.g. 16.67 to 21.43, 5.56 to 7.14), a path-count change in a share; some numbers move by 4.8 points of a share.
- **O1, OM1, OW3**: relative differences up to 1.4 are on values of order 1e-15 to 1e-21 (zero in theory); absolute differences are below 1.3e-14.
- Everything else: relative difference at most 4e-12; largest absolute difference 4.9e-12 (OW1).

Full table: run `python -I results/169c-numerics/numerics_diff.py compare OLD.pkl NEW.pkl` after the two dumps.

**Reading.** The brief's premise (last bit only, headline difference at most 1e-9 relative) does not hold at path level: at quick size (1,000 paths) the O1f and O2b/O2c flips will move aggregates by far more than 1e-9. Stop rule applies: no pin was regenerated.
