# Verification note — frame invariance

Module: `LeanMath/FrameInvariance.lean`   (6 declarations)
Build: `lake build LeanMath` — 8564 jobs, completed successfully
Axiom sweep: `{propext, Classical.choice, Quot.sound}` on every declaration
Stubs: none

## The distinction being certified

Under pure QCD running inside a fixed-nf window, every member of a same-charge
triple carries the same anomalous dimension, so the masses are multiplied by a
common Z(mu). Which statements survive that is not a matter of taste:

  ratio_invariant             m_j/m_i unchanged
  Q_invariant                 the participation ratio unchanged (degree zero)
  Qinv_invariant              likewise in inverse coordinates, so the
                              down-sector cone is frame-free
  power_ratio_invariant       power-blind: (sum v^p)/(sum v^(p/2))^2 sheds the
                              common factor for EVERY real p. p=1 gives
                              Q_invariant, p=-1 the inverse cone.
  external_scale_not_invariant  a relation m_j^2 = m_i * S against an external
                              non-running scale S is NOT invariant: it holds
                              at one scale only, and Z=1 is forced.

## Consequence for the corpus

  FRAME-FREE      m_s/m_d = alpha^-2,  Q_l = 2/3,  Q_D = 2/3,  Q_U = 8/9
  SCALE-FIXED     m_s = alpha^2 mu*,  m_d = alpha^4 mu*,  m_u^2 = m_d 2m_e,
                  sqrt(m_c m_b) = (1+alpha) mu*

The second group is not weaker for being scale-fixed — mu* is the charged
lepton pole sum, scheme-independent and fixed before any quark enters — but
the two groups make different kinds of claim and the letter labels them as
such. `external_scale_not_invariant` is the formal statement of why.
