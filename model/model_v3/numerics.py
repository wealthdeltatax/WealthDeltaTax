"""numerics.py -- the one numerics path (brief 169c).  Imported first, before any numpy import.
numpy picks an AVX512 code path for exp, log and pow where the CPU has it, and that path differs from the AVX2 path in the last bit. The committed digests and pins must hold on every machine, so the AVX512 path is switched off here: `NPY_DISABLE_CPU_FEATURES=X86_V4` (the smallest list that moves the digest: disabling AVX512_SKX, AVX512_ICL, AVX512_SPR or AVX512F alone does not).
numpy reads the variable once, when it is first imported, so setting it later does nothing; that is a hard error here, not a silent wrong number. `setdefault`: a value already set (the workflow, a conftest) is kept."""
import os, sys

VAR, FEATURES = 'NPY_DISABLE_CPU_FEATURES', 'X86_V4'
late = VAR not in os.environ and 'numpy' in sys.modules
os.environ.setdefault(VAR, FEATURES)
if late:
    raise RuntimeError(f'numpy was imported before model_v3.numerics: import it first, or set {VAR}={FEATURES} in the environment')
