# OPERATION TAXONOMY — the running list
# What distinct structural things does this corpus claim, and how do we price
# each one separately, in our universe and in null ones?
#
# Two questions per row, kept apart:
#   (A) how rare is the OPERATION -- that a spectrum admits this kind of
#       relation at all, with the analyst free to choose within a declared menu
#   (B) how rare are the NUMBERS -- that our specific choice lands
#
# Bob's requirement: (A) must let the null make the same choices we could have
# made, not only the ones we did. That is Null C of the APPB pre-registration
# (the frozen function catalogue), generalised.

---

## O1. MEAN WITH A PHYSICAL SCALE AT ONE END
    m_j^2 = m_i * S      where S is an externally fixed scale

  instances:  m_s^2 = m_d * mu*          (+0.52%)
              m_u^2 = m_d * 2m_e         (-1.15%)
  scale menu: the 7 non-empty sums of charged-lepton pole masses, plus 2m_e
              (the pair threshold).  8 candidates, rule declared in advance.
  pair menu:  which two quarks. C(6,2) = 15 ordered-by-mass pairs.
  operation rarity (A): does ANY (pair, scale) combination hold?  8*15 = 120 tries.
  number rarity (B):    does OUR (pair, scale) hold?  1 try.

## O2. MEAN WHERE THE PHYSICAL SCALE *IS* THE MEAN
    S^2 = m_i * m_k      the scale sits at the centre, not the end

  instance:   G^2 = m_c * m_b,  G = (1+alpha) mu*      (-0.11%)
  this is structurally DIFFERENT from O1 and must be priced separately:
  O1 asks whether a quark is the mean of a quark and a scale;
  O2 asks whether a scale is the mean of two quarks.
  scale menu: 8 as above, times the alpha-dressings {1, alpha, (1+alpha)}
              -> 24 candidate centres
  pair menu:  15
  operation rarity (A): 24*15 = 360 tries.

## O3. CHAIN — CONSECUTIVE MEANS SHARING MEMBERS
    S, m_s, m_d, m_u, 2m_e  with each interior term the mean of its neighbours

  this is the P3 cascade read as a chain.  The chain property is stronger than
  the sum of its links: three separate means among six masses is common
  (see the SM baseline, ~4 expected by chance); three means that CHAIN is not.
  operation rarity (A): does any ordering of the 6 quarks + 2 scales admit a
              chain of length >= 4?
  number rarity (B):    does OUR chain, in OUR order, hold?

## O4. CONE / PARTICIPATION RATIO
    Q = (sum m)/(sum sqrt m)^2 = rational

  instances:  Q_l = 2/3 (direct, leptons)      GRANTED as prior art
              Q_D = 2/3 (inverse, downs)       (+0.11%)
              Q_U = 8/9 (direct, ups)          (-0.14%)
  menu:       3 sectors x 2 coordinates x {rationals p/q, q<=9, in [1/3,1]}
              = 6 x 20 = 120 tries
  NOTE this is a different operation from O1-O3 entirely: frame-invariant,
  and it constrains a triple's SHAPE rather than relating masses to a scale.

## O5. LADDER STEP — INTEGER POWER OF ONE CONSTANT
    m = c * alpha^n * S

  instances:  m_s = alpha^2 mu*, m_d = alpha^4 mu*
  menu:       already enumerated in the heavy-quarks paper: coefficients
              {1/3,1/2,1,2,3,4,9} x exponents -6..8 = 105 pairs per quark.
  finding on record: 4 of 6 quarks admit a UNIQUE assignment within 1 sigma.

---

## WHAT MUST BE MEASURED, FOR EACH ROW

    1. our universe, our choice           -> the residual (have it)
    2. our universe, ALL choices in menu  -> how many alternatives also work?
                                             (this is the heavy-quarks Table VI
                                             result, generalised)
    3. null universes, our choice         -> the naive p (have it)
    4. null universes, ALL choices in menu -> the LOOK-ELSEWHERE-CORRECTED p
                                             (this is what Bob asked for)

Row 4 is the number that should be quoted. Rows 1-3 are diagnostics.

## THE JOINT QUESTION

Having priced each operation separately, the claim is not any one of them but
that ONE algebra {alpha, mu*} supplies all five constraints simultaneously.
The joint null must therefore:
  - draw a spectrum
  - derive ITS OWN mu* and ITS OWN alpha from its own leptons
  - be allowed the full menu at every step
  - and be scored on whether ANY menu choice satisfies all five at once

That is the honest number and it is not yet computed.

---
# MEASURED, 2026-08-12

## O1 — mean with a scale at one end
  menu: 8 scales x 15 pairs x 3 middles = 160 candidates (declared before scoring)
  OUR UNIVERSE: 3 of 160 hold at 2%
      s^2 = d * (e+mu+tau)     +0.524%   <- used
      s^2 = d * (mu+tau)       +0.551%   <- degenerate with the above (electron
                                            is 0.03% of the sum; quark data
                                            cannot separate them; Q_l = 2/3
                                            selects e+mu+tau, not the fit)
      u^2 = d * 2m_e           -1.146%   <- used
  NULL, same menu: mean 0.50-0.65 hits;  P(>=3) = 0.081 - 0.104

## O2 — the scale IS the mean
  menu: 24 centres (8 scales x {1, alpha, 1+alpha}) x 15 pairs = 360
  OUR UNIVERSE: 2 of 360 hold at 2%
      ((e+mu+tau)(1+a))^2 = c*b   -0.110%   <- used
      ((mu+tau)(1+a))^2   = c*b   -0.164%   <- same degeneracy again
  NULL, same menu: mean 0.39-0.64 hits;  P(>=2) = 0.091 - 0.171

## O1 and O2 JOINTLY, look-elsewhere corrected
  P(both) = 0.010 - 0.021        i.e. 1 in 50 to 1 in 100

## THE LESSON
  The look-elsewhere correction costs ~2 orders of magnitude on the
  scale-anchored operations. Reporting the uncorrected number would be
  wrong. What survives correction is still 1-in-50 to 1-in-100 for the two
  scale operations ALONE, before the cone conditions (O4) are counted, and
  those are frame-invariant and priced separately.

  Second lesson, and it is the more interesting one: in our universe only
  3 of 160 and 2 of 360 menu entries land, and in BOTH cases the only
  alternative to our choice is the same relation with the electron removed
  from the lepton sum. The menu is large and almost empty. That is not what
  a tuned construction looks like -- a tuned one would find many near-misses
  in the neighbourhood of its choice.

## STILL TO DO
  - O3 chain: price the chain property with menu, not just the links
  - O4 cones: menu = 3 sectors x 2 coordinates x 20 rationals = 120
  - O5 ladder: reuse the heavy-quarks 105-pair enumeration
  - the FULL joint with menus at every step (the honest headline)
