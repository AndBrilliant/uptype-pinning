#!/usr/bin/env python3
"""
O5 — the ladder-step menu null.

Claim form: m = c * alpha^n * mu*, with the menu declared in advance in the
heavy-quarks paper: coefficients {1/3,1/2,1,2,3,4,9} x exponents -6..8,
i.e. 105 pairs (c,n) per quark.

Question (Bob's): how many menu entries land in OUR universe, and how many
land in a null one given the same freedom?
"""
import numpy as np, math, json, itertools
from gmc_engine import draw_sector, spec_seed, LEPTON_WINDOW, DOWN_WINDOW, UP_WINDOW

COEFFS = [1/3, 1/2, 1, 2, 3, 4, 9]
EXPS = list(range(-6, 9))
TOL = 0.02

def menu_hits(mus, alpha, masses):
    """total (c,n) entries landing within TOL, summed over the quarks given"""
    n = 0
    per = {}
    for name, m in masses.items():
        k = 0
        for c in COEFFS:
            for e in EXPS:
                if abs(c * alpha**e * mus / m - 1) < TOL:
                    k += 1
        per[name] = k; n += k
    return n, per

if __name__ == "__main__":
    a = math.sqrt(1.5) - 1
    mus = 1883.03
    OBS = {'m_u': 2.198, 'm_d': 4.782, 'm_s': 95.141, 'm_c': 1272.9, 'm_b': 4183.0}
    n_obs, per = menu_hits(mus, a, OBS)
    print("O5 — LADDER MENU")
    print(f"menu: {len(COEFFS)} coefficients x {len(EXPS)} exponents = "
          f"{len(COEFFS)*len(EXPS)} entries per quark, {len(COEFFS)*len(EXPS)*len(OBS)} total\n")
    print(f"OUR UNIVERSE: {n_obs} entries land at {TOL*100:.0f}%")
    for k, v in per.items():
        print(f"   {k}: {v}")
    print()
    rng = np.random.default_rng(spec_seed() + 105105)
    N = 60000
    print(f"{'prior':6s} {'null mean':>10s} {'null sd':>9s} {'P(>=obs)':>10s}")
    out = {"obs": n_obs, "per_quark": per, "menu_size": len(COEFFS)*len(EXPS), "tol": TOL}
    for prior in ("A1", "A2", "A3"):
        c = []
        for _ in range(N):
            lp = draw_sector(rng, prior, *LEPTON_WINDOW) * 1000
            dn = draw_sector(rng, prior, *DOWN_WINDOW) * 1000
            up = draw_sector(rng, prior, *UP_WINDOW) * 1000
            m_ = sum(lp)
            al = ((m_ / (math.sqrt(lp[0])+math.sqrt(lp[1])+math.sqrt(lp[2]))**2) ** -0.5) - 1
            if al <= 0: continue
            nm = {'m_u': up[0], 'm_d': dn[0], 'm_s': dn[1], 'm_c': up[1], 'm_b': dn[2]}
            c.append(menu_hits(m_, al, nm)[0])
        c = np.array(c)
        p = float((c >= n_obs).mean())
        out[prior] = {"mean": float(c.mean()), "sd": float(c.std()), "p": p}
        print(f"{prior:6s} {c.mean():10.3f} {c.std():9.3f} {p:10.5f}")
    out["worst_p"] = max(out[p]["p"] for p in ("A1","A2","A3"))
    json.dump(out, open("results/o5_ladder.json","w"), indent=1)
    print(f"\n   worst-prior p = {out['worst_p']:.5f}")
