import sys, json; sys.path.insert(0,'.')
from dataclasses import replace
from pathlib import Path
import yaml
from model_v3 import run
from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm
from model_v3.runner import out_sweeps as osw, runner as R, sweeps as S
man=yaml.safe_load(run.MANIFEST.read_text()); lv=json.loads(run.LEVERS.read_text())
tier1=next(o for o in man['outputs'] if o['id']=='OT1')['by']['input']
once=[e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
ctx=R.context(pk.load_pack(next(d for d in sorted(run.PACKS.iterdir()) if (d/'manifest.json').is_file())),pk.load_register(run.INPUTS),lv,tier1,list(asm.entries(man)),once)
inp=json.loads(run.HH_INPUTS.read_text()); cp=replace(ctx,arm=dict(arm='household',inputs=inp,saving='median',regime='mid',fund_return='market'))
st=rt.streams(run.SEED); ev=R.make_ev(cp,st['tornado_crn'].standard_normal((R.T,20)))
fmap,_=S.feasibility(ev,S.grid(lv)); named=S.choose(fmap,man['feasibility'])
draws=R.draw_theta(st['level2_draws'],ctx,ctx.tier1,3)

for k,spec in named.items():
    print(k,[(m, float(S._mean(ev(spec,{R.RET['mean']:m})['M1']['short']))) for m in (0.0,2.0,5.0,10.0,15.0)])
