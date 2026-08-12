#!/usr/bin/env python3
"""
JOINT MC — every corpus claim priced together.

Doctrine (inherited): Koide is GRANTED as prior art. The null derives its own
alpha from its own charged leptons, exactly as the observed universe does.
This removes the ~1e-5 lepton credit from the count and is conservative.
"""
import numpy as np, json, math
from gmc_engine import draw_sector, spec_seed, LEPTON_WINDOW, DOWN_WINDOW, UP_WINDOW

def Q(v):
    v = np.asarray(v, float)
    return v.sum() / (np.sqrt(v).sum() ** 2)

def universe_stats(lep, dn, up, grant_koide=True):
    lep, dn, up = sorted(lep), sorted(dn), sorted(up)
    e, mu_, tau = lep
    d, s, b = dn
    u, c, t = up
    mus = sum(lep)
    Ql = Q(lep)
    # alpha from the universe's own lepton cone (Koide granted), else fixed
    al = (Ql ** -0.5) - 1.0 if grant_koide else math.sqrt(1.5) - 1.0
    G = (1.0 + al) * mus
    return {
        "Q_D":    (Q([1/x for x in dn]),            2.0/3.0),   # down inverse cone
        "Q_U":    (Q(up),                            8.0/9.0),   # up cone
        "r_sd":   (s / d,                            1.0/al**2), # invariant down ratio
        "anchor": (s / mus,                          al**2),     # down sector -> mu*
        "Gpair":  (math.sqrt(c*b) / mus,             1.0 + al),  # heavy pair centre -> mu*
        "split":  (b / c,                            math.pi**2/3.0),  # heavy split
        "uterm":  (u**2 / (d * 2*e),                 1.0),       # light terminal rule
    }

KEYS = ["Q_D", "Q_U", "r_sd", "anchor", "Gpair", "split", "uterm"]

def nhit(st, tol):
    return sum(1 for k in KEYS if abs(st[k][0]/st[k][1] - 1) < tol)

OBS_LEP  = [0.51099895, 105.6583755, 1776.86]
OBS_DOWN = [4.70, 93.4, 4970.]                 # MSbar 2 GeV common scale
OBS_UP   = [7.04e-6, 3.56e-3, 0.967]           # Yukawas at M_Z (cone is scale-free)
OBS_HEAVY = [1272.9, 4183.0]                   # self-scale, for Gpair and split

# SINGLE-FRAME observed set: every quark at mu*, no per-claim frame choice.
# This is the frame the null implicitly uses (one value per mass), so the
# comparison is now like-for-like.  Values from 4-loop running to mu*.
OBS_AT_MUSTAR = {"u": 2.198, "d": 4.782, "s": 95.141,
                 "c": 1112.1, "b": 4903.3, "t": 163175.}

def observed():
    m = OBS_AT_MUSTAR
    return universe_stats(OBS_LEP, [m["d"], m["s"], m["b"]],
                          [m["u"], m["c"], m["t"]])

if __name__ == "__main__":
    o = observed()
    print("JOINT MC — every corpus claim, Koide granted as prior art\n")
    print(f"{'claim':10s} {'observed':>14s} {'target':>14s} {'dev':>9s}")
    for k in KEYS:
        v, t = o[k]
        print(f"{k:10s} {v:14.6f} {t:14.6f} {(v/t-1)*100:+8.3f}%")
    print()
    rng = np.random.default_rng(spec_seed() + 90210)
    N = 500000
    print(f"{'tol':>7s} {'obs':>5s}" + "".join(f"{p:>26s}" for p in ["A1","A2","A3"]))
    out = {}
    for tol in (0.005, 0.01, 0.02, 0.05):
        ob = nhit(o, tol)
        row = f"{tol*100:6.1f}% {ob:5d}"
        out[str(tol)] = {"obs": ob}
        for prior in ("A1", "A2", "A3"):
            c = np.empty(N, dtype=np.int8)
            for i in range(N):
                st = universe_stats(draw_sector(rng, prior, *LEPTON_WINDOW),
                                    draw_sector(rng, prior, *DOWN_WINDOW),
                                    draw_sector(rng, prior, *UP_WINDOW))
                c[i] = nhit(st, tol)
            p = float((c >= ob).mean())
            out[str(tol)][prior] = {"p": p, "null_mean": float(c.mean()),
                                    "null_max": int(c.max())}
            row += f"  p={p:.6f} mu={c.mean():.3f} max={c.max()}"
        out[str(tol)]["worst_p"] = max(out[str(tol)][p]["p"] for p in ("A1","A2","A3"))
        print(row)
    json.dump(out, open("results/joint_mc.json", "w"), indent=1)
    print()
    for tol in ("0.005","0.01","0.02","0.05"):
        d = out[tol]
        print(f"   tol {float(tol)*100:4.1f}%: {d['obs']}/7 claims, least-favourable p = {d['worst_p']:.6f}"
              + ("   (0 hits in N -> 95% CL upper %.1e)" % (3.0/N) if d['worst_p']==0 else ""))
