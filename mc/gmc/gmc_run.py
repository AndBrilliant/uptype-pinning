#!/usr/bin/env python3
"""Production run for the geometric-mean census. Implements SPEC_GMC.md v1.0."""
import argparse, json, math, os, time
import numpy as np
from gmc_engine import (OBS, FREE, derive, census_flat, census_sigma, draw_universe,
                        frac_map, spec_seed, run_gates, triples)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
os.makedirs(OUT, exist_ok=True)
PRIORS = ["A1", "A2", "A3", "A4"]
TOLS = [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]


def cp95(k, n):
    from scipy.stats import beta
    lo = 0.0 if k == 0 else beta.ppf(0.025, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(0.975, k + 1, n - k)
    return float(lo), float(hi)


def observed(with_G):
    o = derive({k: OBS[k][0] for k in FREE}, with_G)
    f = frac_map(with_G)
    if not with_G:
        f.pop("G", None)
    res = {"n_triples": len(triples(list(o))), "flat": {}, "sigma": None}
    for t in TOLS:
        h = census_flat(o, t)
        res["flat"][str(t)] = {"n": len(h),
                               "hits": [f"{j}^2={i}*{k}" for i, j, k, _ in h],
                               "dev_pct": [round(d * 100, 4) for _, _, _, d in h]}
    hs = census_sigma(o, f)
    res["sigma"] = {"n": len(hs),
                    "hits": [f"{j}^2={i}*{k}" for i, j, k, _, _ in hs],
                    "pull": [round(p, 3) for _, _, _, _, p in hs]}
    return res


def null_run(prior, N, with_G, tol_mode="flat"):
    rng = np.random.default_rng(spec_seed() + PRIORS.index(prior) + (0 if with_G else 100))
    f = frac_map(with_G)
    if not with_G:
        f.pop("G", None)
    counts = {str(t): [] for t in TOLS} if tol_mode == "flat" else {"sigma": []}
    for _ in range(N):
        u = draw_universe(rng, prior)
        vals = sorted(u.values())
        if any(abs(vals[i + 1] / vals[i] - 1) < 1e-9 for i in range(len(vals) - 1)):
            continue                                   # gate G3
        o = derive(u, with_G)
        if tol_mode == "flat":
            for t in TOLS:
                counts[str(t)].append(len(census_flat(o, t)))
        else:
            counts["sigma"].append(len(census_sigma(o, f)))
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=20000)
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    N = 2000 if a.quick else a.N

    print("=" * 74)
    print("GEOMETRIC-MEAN CENSUS — SPEC_GMC v1.0")
    print("=" * 74)
    gates = run_gates()
    if any(v["status"] == "FAIL" for v in gates.values()):
        print("GATE FAILURE — stop."); return
    json.dump(gates, open(f"{OUT}/GATES.json", "w"), indent=1)

    manifest = {"spec_sha256": gates["G6_seed"]["spec_sha256"], "seed": spec_seed(),
                "N": N, "priors": PRIORS, "tols": TOLS,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    json.dump(manifest, open(f"{OUT}/manifest.json", "w"), indent=1)

    for with_G in (True, False):
        tag = "withG" if with_G else "noG"
        obs = observed(with_G)
        json.dump(obs, open(f"{OUT}/census_obs_{tag}.json", "w"), indent=1)
        print(f"\n### OBSERVED ({tag}, {obs['n_triples']} triples)")
        print(f"  measurement-tolerance (2 sigma): {obs['sigma']['n']} relations")
        for h, p in zip(obs["sigma"]["hits"], obs["sigma"]["pull"]):
            print(f"     {h:24s} pull {p:+.2f}")
        print(f"  flat 2%: {obs['flat']['0.02']['n']} relations")

        allp = {}
        for prior in PRIORS:
            t0 = time.time()
            c = null_run(prior, N, with_G, "flat")
            cs = null_run(prior, max(N // 4, 500), with_G, "sigma")
            row = {}
            for t in TOLS:
                arr = np.array(c[str(t)]); ob = obs["flat"][str(t)]["n"]
                k = int((arr >= ob).sum()); n = len(arr)
                row[str(t)] = {"obs": ob, "null_mean": float(arr.mean()),
                               "null_sd": float(arr.std()), "p": k / n,
                               "cp95": cp95(k, n)}
            arr = np.array(cs["sigma"]); ob = obs["sigma"]["n"]
            k = int((arr >= ob).sum()); n = len(arr)
            row["sigma"] = {"obs": ob, "null_mean": float(arr.mean()),
                            "null_sd": float(arr.std()), "p": k / n, "cp95": cp95(k, n)}
            allp[prior] = row
            print(f"  {prior}: p(2% flat)={row['0.02']['p']:.5f}  "
                  f"p(sigma)={row['sigma']['p']:.5f}  null2%={row['0.02']['null_mean']:.2f}"
                  f"  [{time.time()-t0:.0f}s]")
        json.dump(allp, open(f"{OUT}/null_{tag}.json", "w"), indent=1)

        adm = gates["G8_support"]["admissible"]
        exc = gates["G8_support"]["excluded"]
        worst_flat = max(allp[p]["0.02"]["p"] for p in adm)
        worst_sig = max(allp[p]["sigma"]["p"] for p in adm)
        wp = [p for p in adm if allp[p]["0.02"]["p"] == worst_flat][0]
        print(f"  admissible priors (support gate): {adm}   excluded: {exc}")
        print(f"  HEADLINE ({tag}) least-favourable ADMISSIBLE prior {wp}: "
              f"p(2% flat)={worst_flat:.5f}, p(sigma)={worst_sig:.5f}")
        allp["_headline"] = {"admissible": adm, "excluded": exc,
                             "worst_prior": wp, "p_flat_2pct": worst_flat,
                             "p_measurement_tolerance": worst_sig}


if __name__ == "__main__":
    main()
