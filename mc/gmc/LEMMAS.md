# What b/c can and cannot be made theorem-shaped

## The honest constraint

P3's light-sector theorem works because a CASCADE is a ladder: each rung is
determined by the previous one, so the structure has content beyond its
endpoints. The heavy pair is a PAIR. Two positive numbers have exactly two
invariants -- a product and a ratio -- and any two numbers have both. There
is no shape to constrain.

So b/c cannot carry a theorem of the same strength, and the paper should not
pretend otherwise. What it CAN carry is three lemmas, one of which is new and
useful across the whole corpus.

## Lemma A (homogeneity) -- already proved, Lean-checked

Q is degree-zero homogeneous. Under a common rescaling of a same-sector
triple, Q is unchanged. Consequence: same-sector cones are frame-free, and
cross-sector relations are not. This is what separates the frame-invariant
claims from the scale-fixed ones.

## Lemma B (involution) -- provable, short

Define R: x -> G^2/x with G = (1+alpha) mu*. Then
   (i)   R o R = identity
   (ii)  G is the unique fixed point
   (iii) every orbit has length at most 2
Consequence, and this is the point: {m_c, m_b} being an orbit means no third
member can be admitted. The top's exclusion is structural, not a numerical
accident -- an order-two map has no third slot. That converts Sec. V of the
letter from an observation into a consequence.

## Lemma C (amplification) -- NEW, and the useful one

For a triple v = (v1,v2,v3) with Q(v) = q, solving for one member v_k, the
gain is
      A_k = |d ln v_k / d ln q|
and A_k grows without bound as sqrt(v_k)/S -> 0, where S = sum sqrt(v_i).
That is: the cone constrains SHAPE, shape information is carried almost
entirely by the heaviest members, and the lightest member is nearly free.

Measured gains:
   leptons, solve m_tau        A = 9.0
   up triple, solve m_c        A = 19.0
   down triple, solve m_b      A = 41.8
   up triple, solve m_u        A = 642

Consequences, all previously unexplained and now accounted for by one formula:
   - the letter's m_b/m_d prediction is 2.4% off while the cone residual is
     0.1%: that is exactly the factor 41.8 x 0.06%.
   - the up-sector charm prediction is 2.65% off: 19 x 0.14%.
   - m_u cannot be predicted from Q_U at any achievable precision: gain 642.
   - the cone-derived heavy masses came out 4.6% low in the overdetermination
     test: 41.8 x 0.11%.

And the corollary that matters for planning: NO improvement in cone precision
rescues the light members. It is a property of the observable.

## What a genuine b/c theorem would require

One of:
   (a) a derivation of pi^2/3 for the split, which would make the ratio
       structural rather than fitted; or
   (b) a third object that belongs with c and b, making it a triple with a
       shape -- but the top is excluded on four independent grounds, so this
       route appears closed; or
   (c) a derivation of G = (1+alpha) mu* from the waveform rather than by
       identification, which would make the centre structural.

None is available. The letter should state Lemmas A-C, claim the two
relations as observations, and say plainly that the pair carries no shape.
