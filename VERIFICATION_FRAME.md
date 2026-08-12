# Verification note — frame invariance and the light-sector map

Modules: `LeanMath/FrameInvariance.lean` (7 decls), `LeanMath/LightMap.lean` (16 decls)
Toolchain: leanprover/lean4 v4.31.0 with Mathlib
Build: `lake build LeanMath` — 8565 jobs, completed successfully
Axiom sweep: `{propext, Classical.choice, Quot.sound}` throughout
Repo total: 133 declarations across seven modules

## FrameInvariance — which claims are scale-free

Under flavour-blind evolution every member of a same-charge sector is
multiplied by one common factor Z. Certified:

  ratio_invariant        v_i/v_j is unchanged under v -> Z v
  sum_scale              the sum scales by Z
  sqrtsum_scale          the square-root sum scales by sqrt(Z)
  Q_invariant            the participation ratio is unchanged
  anchor_not_invariant   a relation m = c*S with S inert holds after
                         rescaling IFF Z = 1
  anchor_unique_scale    two distinct scales cannot both satisfy it

The last two are the point. They separate the corpus into two classes:

  FRAME-FREE      m_s/m_d = alpha^-2, and every same-sector cone
  SCALE-FIXED     m_s = alpha^2 mu*, and every relation anchoring a quark
                  to an external scale

A scale-fixed relation is not thereby suspect — mu* is the charged-lepton
pole sum, scheme-independent and fixed before any quark enters — but it IS a
statement about one evaluation point, and anchor_unique_scale proves it can
be a statement about at most one.

## LightMap — the iterated ladder

Certifies the algebraic content of the companion's construction: that the
orbit of M : x -> alpha^2 x is a geometric ladder, that consecutive rungs
make each interior rung the geometric mean of its neighbours, that the ladder
is strictly decreasing and injective, and that alpha is the unique positive
root of (1+alpha)^-2 = 2/3.

## Not certified

No mass value. Nothing about renormalization-group running. Whether the
physical masses sit on the orbit is the empirical claim of the companion
papers and is not a theorem.
