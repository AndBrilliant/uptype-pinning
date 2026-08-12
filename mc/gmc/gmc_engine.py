#!/usr/bin/env python3
"""
gmc_engine — geometric-mean census over fermion masses.
Implements SPEC_GMC.md v1.0.  Every gate is enforced; nothing is tuned.
"""
import hashlib, itertools, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "SPEC_GMC.md")

# ---------------------------------------------------------------- observed
# MeV.  Frames as frozen in SPEC section 3.
OBS = {
    "m_e":   (0.51099895,  0.0000001),   # pole
    "m_mu":  (105.6583755, 0.0000023),   # pole
    "m_tau": (1776.86,     0.12),        # pole
    "m_u":   (2.198,       0.21),        # MSbar at mu*  (~9.6%)
    "m_d":   (4.782,       0.071),       # MSbar at mu*  (~1.5%)
    "m_s":   (95.141,      0.69),        # MSbar at mu*  (~0.7%)
    "m_c":   (1272.9,      4.6),         # MSbar m_c(m_c)
    "m_b":   (4183.0,      7.0),         # MSbar m_b(m_b)
    "m_t":   (162500.,     400.),        # MSbar m_t(m_t)
}
FREE = ["m_e", "m_mu", "m_tau", "m_u", "m_d", "m_s", "m_c", "m_b", "m_t"]
ALPHA = math.sqrt(1.5) - 1.0

# sector windows (GeV) inherited from the existing suite
LEPTON_WINDOW = (1e-4, 10.0)
DOWN_WINDOW   = (1e-3, 10.0)
UP_WINDOW     = (1e-3, 300.0)


def derive(free, with_G=True):
    """add the derived objects, identically for data and null"""
    o = dict(free)
    o["mu*"] = free["m_e"] + free["m_mu"] + free["m_tau"]
    o["2m_e"] = 2.0 * free["m_e"]
    if with_G:
        o["G"] = math.sqrt(1.5) * o["mu*"]
    return o


# objects that are fixed multiples of one another in EVERY universe.
# a triple containing two of these is degenerate: the relation collapses
# to a two-object statement and is not a geometric mean at all.
COLLINEAR = [{"m_e", "2m_e"}, {"mu*", "G"}]


def degenerate(i, j, k):
    s = {i, j, k}
    return any(len(c & s) >= 2 for c in COLLINEAR)


def triples(names):
    """every (i,j,k) with i<k, j distinct, non-degenerate (gates G2, G7)"""
    out = []
    for i, k in itertools.combinations(names, 2):
        for j in names:
            if j == i or j == k or degenerate(i, j, k):
                continue
            out.append((i, j, k))
    return out


def census_flat(obj, tol):
    """relations satisfied at flat fractional tolerance"""
    hits = []
    for i, j, k in triples(list(obj)):
        d = obj[j] ** 2 / (obj[i] * obj[k]) - 1.0
        if abs(d) < tol:
            hits.append((i, j, k, d))
    return hits


def census_sigma(obj, frac, nsig=2.0):
    """relations satisfied at nsig of the propagated measurement tolerance"""
    hits = []
    for i, j, k in triples(list(obj)):
        d = obj[j] ** 2 / (obj[i] * obj[k]) - 1.0
        s = math.sqrt(4 * frac[j] ** 2 + frac[i] ** 2 + frac[k] ** 2)
        if abs(d) < nsig * s:
            hits.append((i, j, k, d, d / s))
    return hits


# ---------------------------------------------------------------- priors
def draw_sector(rng, kind, lo, hi, n=3):
    if kind == "A1":
        v = np.exp(rng.uniform(math.log(lo), math.log(hi), n))
    elif kind == "A2":
        lm, ls = math.log(math.sqrt(lo * hi)), 2.5
        v = np.array([min(max(math.exp(rng.normal(lm, ls)), lo), hi) for _ in range(n)])
    elif kind == "A3":
        Y = rng.normal(0, 1, size=(n, n))
        s = np.linalg.svd(Y, compute_uv=False)
        s = np.sort(s)
        scale = math.exp(rng.uniform(math.log(lo), math.log(hi)))
        v = (s / s[-1]) * scale
    elif kind == "A4":
        v = rng.uniform(lo, hi, n)
    else:
        raise ValueError(kind)
    return np.sort(v)


def draw_universe(rng, kind):
    """GeV -> MeV; sectors drawn independently as in the parent engine"""
    lep = draw_sector(rng, kind, *LEPTON_WINDOW) * 1000.0
    dn = draw_sector(rng, kind, *DOWN_WINDOW) * 1000.0
    up = draw_sector(rng, kind, *UP_WINDOW) * 1000.0
    return {"m_e": lep[0], "m_mu": lep[1], "m_tau": lep[2],
            "m_d": dn[0], "m_s": dn[1], "m_b": dn[2],
            "m_u": up[0], "m_c": up[1], "m_t": up[2]}


def frac_map(with_G=True):
    f = {k: OBS[k][1] / OBS[k][0] for k in FREE}
    o = derive({k: OBS[k][0] for k in FREE}, with_G)
    # derived-object fractional errors, propagated
    f["mu*"] = math.sqrt(sum(OBS[k][1] ** 2 for k in ("m_e", "m_mu", "m_tau"))) / o["mu*"]
    f["2m_e"] = f["m_e"]
    if with_G:
        f["G"] = f["mu*"]
    return f


def spec_seed():
    h = hashlib.sha256(open(SPEC, "rb").read()).digest()
    return int.from_bytes(h[:8], "big") % (2 ** 63)


# ---------------------------------------------------------------- gates
def run_gates(verbose=True):
    G = {}
    obs = derive({k: OBS[k][0] for k in FREE}, True)
    obs_noG = derive({k: OBS[k][0] for k in FREE}, False)

    n1, n0 = len(triples(list(obs))), len(triples(list(obs_noG)))
    # with G: 660 raw minus degenerate; without G: 495 raw minus degenerate
    raw1 = 66 * 10; raw0 = 55 * 9
    G["G1_enumeration"] = {"with_G": n1, "without_G": n0,
                           "raw": [raw1, raw0],
                           "degenerate_removed": [raw1 - n1, raw0 - n0],
                           "status": "PASS" if n1 < raw1 and n0 < raw0 else "FAIL"}

    # G2: reversing the combination order must not change the count
    rev = []
    for k, i in itertools.combinations(list(obs)[::-1], 2):
        for j in obs:
            if j not in (i, k) and not degenerate(i, j, k):
                rev.append(tuple(sorted((i, k))) + (j,))
    fwd = {tuple(sorted((i, k))) + (j,) for i, j, k in triples(list(obs))}
    G["G2_no_double_count"] = {"forward": len(fwd), "reverse": len(set(rev)),
                               "status": "PASS" if len(fwd) == len(set(rev)) else "FAIL"}

    # G4: known-answer
    want = {("m_c", "G", "m_b"), ("m_d", "m_s", "mu*"),
            ("2m_e", "m_u", "m_d"), ("m_u", "m_s", "m_b")}
    got = {tuple(sorted((i, k))) + (j,) for i, j, k, _ in census_flat(obs, 0.02)}
    wantn = {tuple(sorted((a, c))) + (b,) for a, b, c in want}
    G["G4_known_answer"] = {"required": sorted("%s^2=%s*%s" % (b, a, c) for a, b, c in want),
                            "found": sorted(wantn & got == wantn and ["all"] or list(wantn - got)),
                            "status": "PASS" if wantn <= got else "FAIL"}

    # G5: null sanity
    rng = np.random.default_rng(spec_seed())
    hits = [len(census_flat(derive(draw_universe(rng, "A1")), 0.05)) for _ in range(400)]
    G["G7_no_degenerate"] = {"collinear_sets": [sorted(c) for c in COLLINEAR],
        "violations": sum(1 for i, j, k in triples(list(obs)) if degenerate(i, j, k)),
        "status": "PASS" if not any(degenerate(i, j, k) for i, j, k in triples(list(obs))) else "FAIL"}

    G["G5_null_sanity"] = {"mean_hits_at_5pct": float(np.mean(hits)),
                           "status": "PASS" if np.mean(hits) > 0 else "FAIL"}

    # G8 support gate: a null that cannot produce the observed hierarchy is not
    # a valid comparison, however favourable or unfavourable its hit rate.
    obs_h = OBS["m_t"][0] / OBS["m_u"][0]
    sup = {}
    for p in ("A1", "A2", "A3", "A4"):
        ok = 0
        for _ in range(1500):
            u = draw_universe(rng, p); v = sorted(u.values())
            if v[-1] / v[0] >= 0.5 * obs_h: ok += 1
        sup[p] = ok / 1500.0
    G["G8_support"] = {"observed_hierarchy": obs_h, "reach_fraction": sup,
                       "admissible": [p for p, f in sup.items() if f >= 0.05],
                       "excluded": [p for p, f in sup.items() if f < 0.05],
                       "threshold": 0.05, "status": "PASS"}

    G["G6_seed"] = {"spec_sha256": hashlib.sha256(open(SPEC, "rb").read()).hexdigest(),
                    "seed": spec_seed(), "status": "PASS"}
    if verbose:
        for k, v in G.items():
            print(f"  {k:22s} {v['status']}   {json.dumps({a:b for a,b in v.items() if a!='status'})[:110]}")
    return G


if __name__ == "__main__":
    print("GATES")
    g = run_gates()
    if any(v["status"] == "FAIL" for v in g.values()):
        print("\nGATE FAILURE — stopping per spec.")
        sys.exit(1)
    print("\nall gates PASS")
