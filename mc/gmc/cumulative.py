#!/usr/bin/env python3
"""
CUMULATIVE RARITY — does each added relation cost rarity or buy it?

If the search were fishing, adding constraints would eventually find one the
null satisfies easily and the curve would flatten. A monotone fall with a
steady marginal factor is the signature of independent constraints.
"""
import numpy as np, math, json, itertools
from gmc_engine import draw_sector, spec_seed, LEPTON_WINDOW, DOWN_WINDOW, UP_WINDOW

def Q(v):
    v = np.asarray(v, float); return v.sum()/(np.sqrt(v).sum()**2)

def devs(lep, dn, up):
    lep = sorted(lep); dn = sorted(dn); up = sorted(up)
    e = lep[0]; mus = sum(lep); al = (Q(lep)**-0.5) - 1.0
    d, s, b = dn; u, c, t = up
    return {"s_anchor": s/mus/(al**2) - 1,
            "d_anchor": d/mus/(al**4) - 1,
            "u_term":   u**2/(d*2*e) - 1,
            "Q_D":      Q([1/d,1/s,1/b])/(2/3) - 1,
            "Gpair":    math.sqrt(c*b)/mus/(1+al) - 1}

ORDER = ["s_anchor", "d_anchor", "u_term", "Q_D", "Gpair"]
OBS_LEP=[0.51099895,105.6583755,1776.86]
OBS_DN =[4.782,95.137,5041.092]
OBS_UP =[2.198,1112.141,1e9]
TOL = 0.03

if __name__ == "__main__":
    o = devs(OBS_LEP, OBS_DN, OBS_UP)
    print("CUMULATIVE RARITY  (tolerance %.0f%%, Koide granted)\n" % (TOL*100))
    print("observed deviations:")
    for k in ORDER: print(f"   {k:10s} {o[k]*100:+7.3f}%")
    N = 600000
    rng = np.random.default_rng(spec_seed()+112358)
    # one pass, store the boolean satisfaction matrix
    print(f"\ndrawing {N:,} null universes per prior ...")
    res = {}
    for prior in ("A1","A2","A3"):
        M = np.zeros((N, len(ORDER)), dtype=bool)
        for i in range(N):
            dv = devs(draw_sector(rng,prior,*LEPTON_WINDOW),
                      draw_sector(rng,prior,*DOWN_WINDOW),
                      draw_sector(rng,prior,*UP_WINDOW))
            for j,k in enumerate(ORDER):
                M[i,j] = abs(dv[k]) < TOL
        res[prior] = M
    print()
    print("=== individual: each relation alone ===")
    print(f"{'relation':12s}" + "".join(f"{p:>12s}" for p in ("A1","A2","A3")))
    for j,k in enumerate(ORDER):
        print(f"{k:12s}" + "".join(f"{res[p][:,j].mean():12.5f}" for p in ("A1","A2","A3")))
    print()
    print("=== cumulative in the chain order ===")
    print(f"{'after adding':14s} {'n':>2s}" + "".join(f"{p:>13s}" for p in ("A1","A2","A3")) + "   marginal(worst)")
    out={}; prev=None
    for n in range(1, len(ORDER)+1):
        cols = list(range(n))
        ps = []
        for p in ("A1","A2","A3"):
            hit = res[p][:, cols].all(axis=1)
            ps.append(hit.mean())
        worst = max(ps)
        marg = f"x{prev/worst:8.1f}" if prev and worst>0 else ("x>%.0f"%(prev*N) if prev else "")
        print(f"{ORDER[n-1]:14s} {n:2d}" + "".join(f"{x:13.6f}" for x in ps) + f"   {marg}")
        out[str(n)] = {"relations": ORDER[:n], "p": ps, "worst": worst}
        prev = worst if worst>0 else 1.0/N
    json.dump(out, open("results/cumulative.json","w"), indent=1)
    print()
    print("=== order-independence: every ordering of the 5, worst-prior p at each depth ===")
    for n in range(1, 6):
        best=1.0; wor=0.0
        for combo in itertools.combinations(range(5), n):
            w = max(res[p][:, list(combo)].all(axis=1).mean() for p in ("A1","A2","A3"))
            best=min(best,w); wor=max(wor,w)
        print(f"   depth {n}: worst-prior p ranges [{best:.6f}, {wor:.6f}] over all {len(list(itertools.combinations(range(5),n)))} subsets")
