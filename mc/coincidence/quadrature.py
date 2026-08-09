#!/usr/bin/env python3
"""Deterministic cross-check of the coincidence budget.

The Monte Carlo of `engine_p4.py` is not actually necessary for this null:
the frequencies are a two-dimensional integral that can be evaluated by
quadrature, with no random numbers at all. Agreement between the two is a
much stronger statement than "the seed reproduces".

Reduction. Let x_i = ln m_i, iid uniform on a span of width W. Q is
degree-zero homogeneous, so a common translation of the x_i cancels and only
the two ordered gaps survive:

    a = x_(2) - x_(1),   b = x_(3) - x_(2),   a, b >= 0,  a + b <= W

with density (3! orderings, the translation integrated out)

    f(a, b) = 6 (W - a - b) / W^3

on that triangle. Q is then evaluated on the representative triple
(1, e^a, e^{a+b}).

Accuracy. The integrand is an indicator function, so midpoint quadrature
converges as O(h) rather than O(h^2): the error is set by the length of the
hit-region boundary, which is why the 20-target menu is less accurate at
fixed grid than the single target. The discretisation error is therefore
ESTIMATED, by halving the grid, and carried into the comparison rather than
assumed negligible.

  python3 quadrature.py            evaluate, estimate error, compare
  python3 quadrature.py --grid N   grid resolution per axis (default 6000)
"""
import argparse
import json
import os
import sys

import numpy as np

from engine_p4 import TARGETS, TOL, W, near_any


def integrate(grid):
    """Midpoint rule over the gap triangle, accumulated row by row so memory
    stays O(grid) rather than O(grid^2)."""
    h = W / grid
    c = (np.arange(grid) + 0.5) * h
    norm = fixed = menu = 0.0
    for a0 in c:
        keep = (a0 + c) <= W
        if not keep.any():
            continue
        b = c[keep]
        a = np.full(b.shape, a0)
        w = 6.0 * (W - a - b) / W ** 3 * h * h
        m = np.stack([np.ones_like(a), np.exp(a), np.exp(a + b)], axis=1)
        q9 = 9.0 * m.sum(1) / np.sqrt(m).sum(1) ** 2
        norm += w.sum()
        fixed += w[np.abs(q9 - 8.0) <= TOL].sum()
        menu += w[near_any(q9, TARGETS, TOL)].sum()
    return {"grid": grid, "normalisation": float(norm),
            "fixed": float(fixed), "menu": float(menu)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", type=int, default=6000)
    a = ap.parse_args()

    fine = integrate(a.grid)
    coarse = integrate(a.grid // 2)
    # For O(h) convergence, |I(g) - I(g/2)| estimates the remaining error at g.
    err = {k: abs(fine[k] - coarse[k]) for k in ("fixed", "menu")}

    print(f"grid            : {fine['grid']} (error estimated against "
          f"{coarse['grid']})")
    print(f"normalisation   : {fine['normalisation']:.8f}   (exact value 1)")
    print(f"fixed 8/9       : {fine['fixed']:.6e}  +/- {err['fixed']:.1e} (discretisation)")
    print(f"menu p/q<=9     : {fine['menu']:.6e}  +/- {err['menu']:.1e} (discretisation)")

    if abs(fine["normalisation"] - 1.0) > 1e-5:
        print("FAIL: density does not integrate to 1", file=sys.stderr)
        return 1

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "results.json")
    if not os.path.exists(path):
        print("\nresults.json absent; run engine_p4.py to enable comparison.")
        return 0

    mc = json.load(open(path))
    print(f"\ncompared against Monte Carlo (N = {mc['n']:,}, seed {mc['seed']}):")
    status = 0
    for label, qkey, mkey in (("fixed 8/9", "fixed", "fixed"),
                              ("menu p/q<=9", "menu", "menu_result")):
        lo, hi = mc[mkey]["cp95_lo"], mc[mkey]["cp95_hi"]
        f = mc[mkey]["f"]
        q = fine[qkey]
        # Budget: Monte-Carlo sampling error (CP95 half-width) plus the
        # quadrature's own discretisation error. Neither alone is the whole
        # uncertainty on this comparison.
        budget = max(hi - f, f - lo) + err[qkey]
        ok = abs(q - f) <= budget
        status |= 0 if ok else 1
        print(f"  {label:12s} quadrature {q:.6e}  MC {f:.6e}  "
              f"|diff| {abs(q - f):.2e}  budget {budget:.2e}  "
              f"{'agree' if ok else 'DISAGREE'}")
    if status:
        print("\nFAIL: quadrature and Monte Carlo disagree beyond their "
              "combined uncertainty", file=sys.stderr)
    else:
        print("\nQuadrature agrees with the Monte Carlo within combined "
              "sampling and discretisation error, for every target reading.")
    return status


if __name__ == "__main__":
    sys.exit(main())
