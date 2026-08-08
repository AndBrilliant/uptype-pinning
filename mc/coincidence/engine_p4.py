#!/usr/bin/env python3
"""Single-claim coincidence budget for 'Electroweak pinning of the
up-type participation ratio near 8/9', Sec. 'A single-claim
coincidence budget'. Standalone; ~30 s full run, ~1 s with --quick."""
import sys
import numpy as np
from fractions import Fraction
QUICK = "--quick" in sys.argv
N = 100_000 if QUICK else 10_000_000
B = min(N, 1_000_000)
TOL = 0.0114
rng = np.random.default_rng(20270301)
T9 = 9 * np.array(sorted({float(Fraction(p, q))
     for p in range(1, 10) for q in range(1, 10)
     if p <= q and 3 * p > q and np.gcd(p, q) == 1}))
hf = hm = 0
for _ in range(N // B):
    m = np.exp(rng.uniform(np.log(0.5), np.log(2e5), (B, 3)))
    q9 = 9 * m.sum(1) / np.sqrt(m).sum(1) ** 2
    hf += int((np.abs(q9 - 8) <= TOL).sum())
    hm += int((np.min(np.abs(q9[:, None] - T9[None, :]), 1) <= TOL).sum())
print(f"targets    : {len(T9)} rationals")
print(f"fixed 8/9  : {hf}/{N}  f={hf/N:.3e}")
print(f"menu p/q<=9: {hm}/{N}  f={hm/N:.3e}")
if not QUICK:
    same = (hf, hm) == (33741, 696610)
    print("note:", "matches" if same else "differs from",
          "the paper-run counts (33741, 696610); informational only.")
