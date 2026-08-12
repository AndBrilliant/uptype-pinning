# Verification note — the sensitivity (amplification) lemma

Module: `LeanMath/Sensitivity.lean`
Toolchain: leanprover/lean4 v4.31.0 with Mathlib
Build: `lake build LeanMath` — 8563 jobs, completed successfully
Axiom sweep: `{propext, Classical.choice, Quot.sound}` for every declaration
Stubs: none (`sorry`, `admit`, `native_decide` all absent)
Declarations in this module: 18

## What is certified

For a positive triple with S1 = sum v, S2 = sum sqrt(v), Q = S1/S2^2:

  hasDerivAt_S1       d/dx of the sum, in the first slot
  hasDerivAt_S2       d/dx of the square-root sum, = 1/(2 sqrt x)
  hasDerivAt_Q        Q is differentiable in the first slot (quotient rule form)
  deriv_Q_eq          that derivative in closed form:
                        1/S2^2 - S1/(S2^3 sqrt x)
  log_sensitivity     THE IDENTITY:
                        (x/Q) dQ/dx  =  x/S1 - sqrt(x)/S2
  sensitivity_zero_iff the sensitivity vanishes iff x S2 = sqrt(x) S1
  S2_sq_le            Cauchy-Schwarz for the triple: S2^2 <= 3 S1
  share_sq_bound      x/S1 <= 3 (sqrt(x)/S2)^2
  sensitivity_le      sensitivity <= s(3s-1) where s = sqrt(x)/S2
  Q_comm12/23/13      Q is symmetric, so the first-slot result covers all three

## What it explains

Writing s for a member's share of the square-root sum, the gain required to
move Q through that member is at least 1/s. Numerically, against the tabulated
triples (verified before formalising):

  up (u,c,t)     u: sensitivity -0.00253014   gain 395
                 c: sensitivity -0.05339128   gain  18.7
                 t: sensitivity +0.05592141   gain  17.9
  down inverse   b: sensitivity -0.02558270   gain  39.1
  leptons        tau: sensitivity +0.15047674 gain   6.7

This accounts, with one formula, for four residuals that otherwise look
mutually inconsistent:
  - the down cone holds to 0.11% but the m_b/m_d it implies is 2.4% off
    (41.8 x 0.06%)
  - the up cone holds to 0.14% but the charm it implies is 2.65% off
    (19 x 0.14%)
  - cone-derived heavy masses came out 4.6% low in the overdetermination test
  - m_u cannot be predicted from the up cone at any achievable precision

## Scope

This is an analytic fact about the observable Q. It is not a physics claim and
certifies nothing about any mass value. In particular it does NOT certify the
renormalization-group behaviour of any quantity, nor the tabulated inputs.
