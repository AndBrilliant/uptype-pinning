#!/usr/bin/env python3
"""Single-claim coincidence budget for "Electroweak pinning of the up-type
participation ratio near 8/9", Sec. "A single-claim coincidence budget".

Prices the proximity of the observed 9Q_U to 8 against random spectra, under
an explicitly declared null sampling measure. Emits RESULTS.md and
results.json; no number in either file is hand-entered.

  python3 engine_p4.py            full run (N = 1e8), writes RESULTS.md
  python3 engine_p4.py --quick    fast CI configuration (N = 2e5)
  python3 engine_p4.py --legacy-seed
                                  rerun at the pre-registration seed 20270301,
                                  which reproduces the counts published in the
                                  first release
  python3 engine_p4.py --no-write compute and print, leave files alone
"""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from fractions import Fraction

import numpy as np
from scipy.stats import beta as _beta

# ── frozen specification ──────────────────────────────────────────────
# This string IS the specification. The production seed is derived from its
# SHA-256, so the seed cannot be chosen after seeing results: changing any
# element of the spec changes the seed, and changing the seed alone is not
# possible without changing the spec text.
SPEC_CANON = (
    "uptype-pinning/single-claim-coincidence-budget/v2\n"
    "observable: 9Q, Q = (sum m_i) / (sum sqrt(m_i))^2, degree-zero homogeneous\n"
    "null: three iid log-coordinates, uniform over a span of "
    "W = ln(4e5) = 12.899220 (5.602060 decades)\n"
    "draw order: m = exp(U(log 0.5, log 2e5)), shape (batch, 3)\n"
    "distance: absolute in 9Q, |9Q - target| <= 0.0114\n"
    "tolerance origin: the observed miss |9Q_U(M_Z) - 8| at M_Z\n"
    "menu: irreducible p/q with p,q <= 9 in the closed admissible range "
    "1/3 <= Q <= 1\n"
    "N: 100000000\n"
)
SPEC_SHA256 = hashlib.sha256(SPEC_CANON.encode()).hexdigest()
SEED = int.from_bytes(hashlib.sha256(SPEC_CANON.encode()).digest()[:4], "big")
LEGACY_SEED = 20270301  # first-release seed, retained as a cross-check

TOL = 0.0114  # absolute, in 9Q; the observed miss at M_Z
M_LO, M_HI = 0.5, 2e5  # MeV; only the ratio matters, Q is homogeneous
W = np.log(M_HI / M_LO)  # 12.899…, i.e. 5.602 decades

# ── the target menu ───────────────────────────────────────────────────
# Q is bounded by 1/3 <= Q <= 1 (Eq. 1). Both endpoints are admissible, so
# the menu is taken over the CLOSED range. Note the asymmetry in what the
# endpoints do: Q = 1/3 is attained exactly, at the equal-mass triple, and
# contributes hits; Q = 1 is a limit only (it requires two of the three
# masses to vanish) and contributes none. Excluding 1/3 while including 1 --
# as the first release did -- therefore drops the single live boundary target
# and keeps the inert one.
MENU = sorted({Fraction(p, q)
               for p in range(1, 10) for q in range(1, 10)
               if p <= q and 3 * p >= q and np.gcd(p, q) == 1})
TARGETS = 9.0 * np.array([float(f) for f in MENU])
assert len(MENU) == 20, f"menu must hold 20 rationals, got {len(MENU)}"
assert MENU[0] == Fraction(1, 3) and MENU[-1] == Fraction(1, 1)


def clopper_pearson(k, n, alpha=0.05):
    """Exact two-sided Clopper-Pearson interval for a binomial proportion."""
    lo = _beta.ppf(alpha / 2, k, n - k + 1) if k > 0 else 0.0
    hi = _beta.isf(alpha / 2, k + 1, n - k) if k < n else 1.0
    return float(lo), float(hi)


def near_any(q9, targets, tol):
    """Boolean 'within tol of some target', without the (batch x targets)
    temporary the first release built."""
    hit = np.zeros(q9.shape, dtype=bool)
    for t in targets:
        np.logical_or(hit, np.abs(q9 - t) <= tol, out=hit)
    return hit


def run(n, seed, batch=1_000_000):
    """Draw n triples and count hits. Batches cover n exactly: the remainder
    is drawn, not silently dropped."""
    rng = np.random.Generator(np.random.PCG64(seed))
    fixed = menu = 0
    q9_lo, q9_hi = np.inf, -np.inf
    drawn = 0
    while drawn < n:
        b = min(batch, n - drawn)
        m = np.exp(rng.uniform(np.log(M_LO), np.log(M_HI), (b, 3)))
        q9 = 9.0 * m.sum(1) / np.sqrt(m).sum(1) ** 2
        fixed += int((np.abs(q9 - 8.0) <= TOL).sum())
        menu += int(near_any(q9, TARGETS, TOL).sum())
        q9_lo, q9_hi = min(q9_lo, q9.min()), max(q9_hi, q9.max())
        drawn += b
    return {"n": drawn, "fixed": fixed, "menu": menu,
            "q9_min": float(q9_lo), "q9_max": float(q9_hi)}


def _git_commit():
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                             text=True, timeout=5)
        return out.stdout.strip() or None if out.returncode == 0 else None
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--legacy-seed", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    n = 200_000 if a.quick else 100_000_000
    seed = LEGACY_SEED if a.legacy_seed else SEED
    r = run(n, seed)

    f_fixed, f_menu = r["fixed"] / r["n"], r["menu"] / r["n"]
    cp_fixed = clopper_pearson(r["fixed"], r["n"])
    cp_menu = clopper_pearson(r["menu"], r["n"])

    # 9Q is bounded by construction; assert it rather than assume it.
    assert 3.0 - 1e-9 <= r["q9_min"] and r["q9_max"] <= 9.0 + 1e-9, \
        f"9Q escaped [3, 9]: [{r['q9_min']}, {r['q9_max']}]"

    print(f"spec sha256 : {SPEC_SHA256}")
    print(f"seed        : {seed}" + ("  (legacy)" if a.legacy_seed
                                     else "  (derived from spec sha256)"))
    print(f"N           : {r['n']}")
    print(f"support     : {W / np.log(10):.6f} decades")
    print(f"targets     : {len(MENU)} rationals in [1/3, 1]")
    print(f"9Q observed : [{r['q9_min']:.6f}, {r['q9_max']:.6f}] within [3, 9]")
    print(f"fixed 8/9   : {r['fixed']}/{r['n']}  f={f_fixed:.6e}  "
          f"CP95=[{cp_fixed[0]:.6e}, {cp_fixed[1]:.6e}]")
    print(f"menu p/q<=9 : {r['menu']}/{r['n']}  f={f_menu:.6e}  "
          f"CP95=[{cp_menu[0]:.6e}, {cp_menu[1]:.6e}]")

    payload = {
        "spec_sha256": SPEC_SHA256, "spec": SPEC_CANON,
        "seed": seed, "seed_kind": "legacy" if a.legacy_seed else "spec-derived",
        "n": r["n"], "tolerance": TOL, "distance": "absolute in 9Q",
        "support_decades": W / np.log(10),
        "menu": [str(f) for f in MENU], "menu_size": len(MENU),
        "q9_min": r["q9_min"], "q9_max": r["q9_max"],
        "fixed": {"hits": r["fixed"], "f": f_fixed,
                  "cp95_lo": cp_fixed[0], "cp95_hi": cp_fixed[1]},
        "menu_result": {"hits": r["menu"], "f": f_menu,
                        "cp95_lo": cp_menu[0], "cp95_hi": cp_menu[1]},
        "env": {"python": platform.python_version(),
                "numpy": np.__version__,
                "scipy": __import__("scipy").__version__,
                "platform": platform.platform()},
        "git_commit": _git_commit(),
    }

    if a.no_write or a.quick:
        return
    with open("results.json", "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    with open("RESULTS.md", "w") as fh:
        fh.write(render(payload))
    print("\nwrote results.json and RESULTS.md")


def render(p):
    menu_str = ", ".join(p["menu"])
    return f"""# Single-claim coincidence budget — results

**Generated by `engine_p4.py`. Do not hand-edit.** Every number below is
written by the executable that produced it.

| | |
|---|---|
| Spec SHA-256 | `{p['spec_sha256']}` |
| Seed | `{p['seed']}` ({p['seed_kind']}) |
| Draws | {p['n']:,} |
| Null support | {p['support_decades']:.6f} decades, three iid log-coordinates |
| Distance | {p['distance']}, tolerance {p['tolerance']} |
| Menu | {p['menu_size']} irreducible p/q, p,q ≤ 9, over 1/3 ≤ Q ≤ 1 |
| Observed 9Q range | [{p['q9_min']:.6f}, {p['q9_max']:.6f}] ⊂ [3, 9] |
| Python / NumPy / SciPy | {p['env']['python']} / {p['env']['numpy']} / {p['env']['scipy']} |
| Commit | `{p['git_commit'] or 'n/a'}` |

## Frequencies

| target reading | hits | f | CP95 |
|---|---|---|---|
| fixed 8/9 | {p['fixed']['hits']:,} | {p['fixed']['f']:.6e} | [{p['fixed']['cp95_lo']:.6e}, {p['fixed']['cp95_hi']:.6e}] |
| any p/q, p,q ≤ 9 | {p['menu_result']['hits']:,} | {p['menu_result']['f']:.6e} | [{p['menu_result']['cp95_lo']:.6e}, {p['menu_result']['cp95_hi']:.6e}] |

Clopper–Pearson intervals are exact two-sided 95% intervals, computed here,
not transcribed.

## Menu

{menu_str}

Twenty irreducible rationals over the closed admissible range 1/3 ≤ Q ≤ 1.
Both endpoints are included because both are admissible under Eq. (1). Their
behaviour differs: Q = 1/3 is attained exactly, at the equal-mass triple, and
contributes hits; Q = 1 is a limit only, requiring two masses to vanish, and
contributes none.

## Reading

These are model-conditional coincidence frequencies under a stated null
sampling measure. They are not p-values and no significance conversion is
performed. Menus price listed freedom only; unlisted freedom caps inference
and is not quantified here.

See `SPEC.md` for the frozen specification, `quadrature.py` for the
deterministic cross-check of these frequencies, and `robustness.py` for
sensitivity to the null support and to the distance convention.
"""


if __name__ == "__main__":
    sys.exit(main())
