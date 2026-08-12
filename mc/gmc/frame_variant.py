#!/usr/bin/env python3
"""Frame robustness for the census: repeat at a genuine common scale."""
import numpy as np, itertools, math, json
import rundec
from gmc_engine import triples, derive, spec_seed, draw_universe, census_flat
cr=rundec.CRunDec(); asMZ,MZ=0.1180,91.1876; mbmb,mcmc=4.183,1.2730
as_mb=cr.AlphasExact(asMZ,MZ,mbmb,5,4); as_mb4=cr.DecAsDownMS(as_mb,mbmb,mbmb,4,4)
as_2=cr.AlphasExact(as_mb4,mbmb,2.0,4,4); as_mc=cr.AlphasExact(as_mb4,mbmb,mcmc,4,4)
mus=1883.03
def quarks_at(mu):
    A=cr.AlphasExact(as_mb4,mbmb,mu,4,4)
    f=lambda m0,a0: cr.mMS2mMS(m0,a0,A,4,4)*1000
    return {'m_u':f(2.16e-3,as_2),'m_d':f(4.70e-3,as_2),'m_s':f(93.5e-3,as_2),
            'm_c':f(mcmc,as_mc),'m_b':f(mbmb,as_mb4),
            'm_t':cr.mMS2mMS(162.5,cr.AlphasExact(as_mb,mbmb,162.5,5,4),A,5,4)*1000}
lep={'m_e':0.51099895,'m_mu':105.6583755,'m_tau':1776.86}
print("FRAME ROBUSTNESS — census at a genuine common scale\n")
print(f"{'scale':>10s} {'n@2%':>6s}  relations")
res={}
for mu,lbl in [(1.273,'m_c'),(2.0,'2 GeV'),(3.0,'3 GeV'),(4.183,'m_b')]:
    o=dict(lep); o.update(quarks_at(mu)); o=derive(o)
    h=census_flat(o,0.02)
    res[lbl]={'n':len(h),'hits':[f"{j}^2={i}*{k}" for i,j,k,_ in h]}
    print(f"{lbl:>10s} {len(h):6d}  {', '.join(res[lbl]['hits']) if h else '(none)'}")
# the paper's mixed frame for comparison
mixed={'m_e':0.51099895,'m_mu':105.6583755,'m_tau':1776.86,
       'm_u':2.198,'m_d':4.782,'m_s':95.141,'m_c':1272.9,'m_b':4183.0,'m_t':162500.}
h=census_flat(derive(mixed),0.02)
res['mixed(paper)']={'n':len(h),'hits':[f"{j}^2={i}*{k}" for i,j,k,_ in h]}
print(f"{'mixed':>10s} {len(h):6d}  {', '.join(res['mixed(paper)']['hits'])}")
json.dump(res,open('results/frame_variant.json','w'),indent=1)
print("\n=> if the count collapses at a common scale, the census is frame-dependent")
print("   and that must be the headline caveat, not a footnote.")
