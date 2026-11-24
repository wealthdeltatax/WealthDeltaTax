import sys; sys.path.insert(0,'.'); sys.path.insert(0,'tests/model_v3')
import test_converge as T
from model_v3.runner import runner as R
R.N1, R.N2P, T.C3_DRAWS, T.C3_PATHS = 50, 20, 3, 20
a = T.arm.__wrapped__() if hasattr(T.arm,'__wrapped__') else None
cp, spec = a
m = {s: T.stats(cp, spec, s, 50) for s in T.SEEDS[:2]}
print({o: [round(x,3) for x in m[T.SEEDS[0]][o]] for o in T.KEY})
import numpy as np
from model_v3.core import returns as rt
x = R.level2(cp, spec, rt.streams(T.run.SEED)['level2_draws'], n=3, n_paths=20).samples['O1'][T.KEY['O1']]; print(np.shape(x))
ev = R.make_ev(cp, rt.streams(1)['tornado_crn'].standard_normal((R.T, 20)))
rows = T.S.tornado(ev, spec, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp)); print([r['input'] for r in rows if r['headline']=='M1' and r['horizon']=='short'][:3])
