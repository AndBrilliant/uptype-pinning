#!/usr/bin/env python3
"""Reproducibility gate.

Re-runs the production configuration and asserts that the committed
`results.json` matches, field by field, on every number that the calculation
determines. Environment fields (interpreter and library versions, platform,
commit) are deliberately excluded from the comparison: they are recorded for
provenance, and they legitimately differ between machines.

Exits non-zero on any mismatch. This is what CI runs.
"""
import json
import os
import sys

from engine_p4 import (MENU, SEED, SPEC_CANON, SPEC_SHA256, TOL,
                       clopper_pearson, run)

N = 100_000_000


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "results.json")
    if not os.path.exists(path):
        print("results.json is missing; run engine_p4.py", file=sys.stderr)
        return 1
    committed = json.load(open(path))

    fail = []

    def check(name, got, want):
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:22s} {got!r}"
              + ("" if ok else f"   expected {want!r}"))
        if not ok:
            fail.append(name)

    print("specification")
    check("spec sha256", SPEC_SHA256, committed["spec_sha256"])
    check("spec text", SPEC_CANON, committed["spec"])
    check("seed", SEED, committed["seed"])
    check("tolerance", TOL, committed["tolerance"])
    check("menu size", len(MENU), committed["menu_size"])
    check("menu", [str(f) for f in MENU], committed["menu"])

    if fail:
        print("\nspecification drift; not re-running", file=sys.stderr)
        return 1

    print(f"\nre-running production (N = {N:,}, seed {SEED})")
    r = run(N, SEED)
    check("draws", r["n"], committed["n"])
    check("fixed hits", r["fixed"], committed["fixed"]["hits"])
    check("menu hits", r["menu"], committed["menu_result"]["hits"])

    lo, hi = clopper_pearson(r["fixed"], r["n"])
    check("fixed CP95 lo", round(lo, 12), round(committed["fixed"]["cp95_lo"], 12))
    check("fixed CP95 hi", round(hi, 12), round(committed["fixed"]["cp95_hi"], 12))
    lo, hi = clopper_pearson(r["menu"], r["n"])
    check("menu CP95 lo", round(lo, 12), round(committed["menu_result"]["cp95_lo"], 12))
    check("menu CP95 hi", round(hi, 12), round(committed["menu_result"]["cp95_hi"], 12))

    # bound asserted on the sample, not assumed
    ok = 3.0 - 1e-9 <= r["q9_min"] and r["q9_max"] <= 9.0 + 1e-9
    print(f"  {'ok  ' if ok else 'FAIL'}  {'9Q within [3, 9]':22s} "
          f"[{r['q9_min']:.6f}, {r['q9_max']:.6f}]")
    if not ok:
        fail.append("9Q range")

    if fail:
        print(f"\nFAIL: {len(fail)} mismatch(es): {', '.join(fail)}",
              file=sys.stderr)
        return 1
    print("\nCommitted results reproduce exactly.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
