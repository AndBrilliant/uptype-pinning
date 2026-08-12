#!/usr/bin/env python3
"""
THE mu* MC.  One frame, one value per mass, one paper.
Five independent constraints determine five quark masses from the lepton
sector alone.  Koide granted as prior art: the null derives alpha from its
own charged leptons exactly as the observed universe does.
"""
import numpy as np, json, math
from gmc_engine import draw_sector, spec_seed, LEPTON_WINDOW, DOWN_WINDOW, UP_WINDOW

def Q(v):
    v = np.asarray(v, float); return v.sum()/(np.sqrt(v).sum()**2)

def stats(lep, dn, up):
    lep = sorted(lep); dn = sorted(dn); up = sorted(up)
    e = lep[0]; mus = sum(lep); al = (Q(lep) ** -0.5) - 1.0
    d, s, b = dn; u, c, t = up
    return {
        "s_anchor": (s / mus,                     al**2),        # m_s = a^2 mu*
        "d_anchor": (d / mus,                     al**4),        # m_d = a^4 mu*
        "u_term":   (u**2 / (d * 2*e),            1.0),          # m_u^2 = m_d 2m_e
        "Q_D":      (Q([1/d, 1/s, 1/b]),          2.0/3.0),      # down inverse cone
        "Gpair":    (math.sqrt(c*b) / mus,        1.0 + al),     # b/c centre at mu*
    }
KEYS = ["s_anchor", "d_anchor", "u_term", "Q_D", "Gpair"]
def nhit(st, tol): return sum(1 for k in KEYS if abs(st[k][0]/st[k][1]-1) < tol)

# every mass at mu*, 4-loop.  one value each.
OBS_LEP = [0.51099895, 105.6583755, 1776.86]
OBS_DN  = [4.782, 95.137, 5041.092]
OBS_UP  = [2.198, 1112.141, 1e9]      # top absent at mu*; placeholder unused by any claim

if __name__ == "__main__":
    o = stats(OBS_LEP, OBS_DN, OBS_UP)
    print("THE mu* MC — five constraints, five quark masses, one frame\n")
    for k in KEYS:
        v, t = o[k]; print(f"   {k:10s} {v:14.6f} vs {t:14.6f}   {(v/t-1)*100:+7.3f}%")
    print()
    rng = np.random.default_rng(spec_seed() + 24680); N = 2000000
    print(f"{'tol':>7s} {'obs':>5s}" + "".join(f"{p:>28s}" for p in ["A1","A2","A3"]))
    out = {}
    for tol in (0.005, 0.01, 0.02, 0.03, 0.05):
        ob = nhit(o, tol); row = f"{tol*100:6.1f}% {ob:5d}"; out[str(tol)] = {"obs": ob, "N": N}
        for prior in ("A1", "A2", "A3"):
            c = np.empty(N, dtype=np.int8)
            for i in range(N):
                c[i] = nhit(stats(draw_sector(rng, prior, *LEPTON_WINDOW),
                                  draw_sector(rng, prior, *DOWN_WINDOW),
                                  draw_sector(rng, prior, *UP_WINDOW)), tol)
            p = float((c >= ob).mean())
            out[str(tol)][prior] = {"p": p, "null_mean": float(c.mean()), "null_max": int(c.max())}
            row += f"  p={p:.6f} mu={c.mean():.3f} max={c.max()}"
        out[str(tol)]["worst_p"] = max(out[str(tol)][p]["p"] for p in ("A1","A2","A3"))
        print(row)
    json.dump(out, open("results/mustar_mc.json", "w"), indent=1)
    print("\nsummary")
    for tol in ("0.005","0.01","0.02","0.03","0.05"):
        d = out[tol]; wp = d["worst_p"]
        tail = "  [0 hits in %d: 95 pct CL upper %.1e]" % (N, 3.0/N) if wp == 0 else ""
        print(f"   tol {float(tol)*100:4.1f}%: {d['obs']}/5, worst-prior p = {wp:.6f}{tail}")
