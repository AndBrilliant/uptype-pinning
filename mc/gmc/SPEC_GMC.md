# SPEC_GMC — Geometric-Mean Census, frozen specification v1.0
# Frozen 2026-08-12 before any production run.
# Author: A. M. Brilliant.  Engine drafted by Claude under instruction.

## 0. Why this null is different

Every previously-priced relation in this corpus has the form
`m_j = kappa * f(m_i, ...)` with `kappa` a constant chosen after the
target was known. Such relations cannot be priced: the constant absorbs
any residual, so the hit rate under a null is a statement about the
constant's freedom, not about the masses.

A geometric mean carries no constant:

        m_j^2 = m_i * m_k

Its only freedom is *which three objects are named*. That freedom is
finite and enumerable. This is the entire reason the present null is
meaningful where earlier ones required a "fixed grammar" caveat.

## 1. Object set (frozen)

FREE objects — 9 charged-fermion masses:
    m_e, m_mu, m_tau, m_u, m_d, m_s, m_c, m_b, m_t

DERIVED objects — computed identically in data and in every null draw:
    mu*   = m_e + m_mu + m_tau          (charged-lepton sum)
    2m_e  = 2 * m_e                     (pair-production threshold)
    G     = sqrt(3/2) * mu*             (= (1+alpha) mu*, alpha from Koide)

Total 12 objects. Derived objects carry NO extra freedom: the null
constructs them from its own draw by the same three formulae.

RATIONALE for including G: it is the only derived scale that uses an
external constant (alpha, fixed by the charged-lepton relation, itself
prior art). Runs are reported BOTH with and without G. If the result
depends on G, that is disclosed, not hidden.

## 2. Relation family (frozen)

For every ordered triple (i, j, k) with i < k and j not in {i,k}:

        R(i,j,k):   m_j^2 = m_i * m_k

Count of triples: C(12,2) * 10 = 66 * 10 = 660  (with G)
                  C(11,2) * 9  = 55 * 9  = 495  (without G)

No other functional form is admitted. No constants. No exponents.

## 3. Frames (frozen, and the known weakness)

    leptons        : pole masses
    m_u, m_d, m_s  : MSbar at mu*
    m_c, m_b       : MSbar at own scale, m_q(m_q)
    m_t            : MSbar at own scale, m_t(m_t)

This is mixed-frame and it is the single largest methodological
weakness of the census. It is adopted because each sector's masses are
quoted in the frame in which that sector is defined (Sec. 3 of the
heavy-pair letter). A common-scale variant MUST be run as a robustness
cell and reported whatever it says.

## 4. Tolerance (frozen)

PRIMARY: measurement-driven. For relation R(i,j,k) define

        D = m_j^2 / (m_i m_k) - 1
        sigma_D = sqrt( 4 f_j^2 + f_i^2 + f_k^2 )

with f_x the fractional 1-sigma uncertainty of object x. A relation
counts as a hit iff |D| < 2 * sigma_D.

Null draws are assigned the SAME fractional uncertainties, matched by
rank order within each sector, so the null sees the same tolerance
structure.

SECONDARY (reported alongside, never instead): flat fractional
tolerance scanned over 0.5%, 1%, 1.5%, 2%, 3%, 4%, 5%. The full curve
is reported. A result that exists only at one tolerance is not a
result.

## 5. Null priors (frozen — all four run, all four reported)

Inherited from engine/priors.py of mass-relations-mc-suite:
    A1  log-uniform per sector over the frozen windows
    A2  log-normal per sector
    A3  random-matrix (SVD singular values of a Gaussian matrix)
    A4  uniform-in-mass per sector

Sector windows are those of engine/constants.py, unchanged.

The HEADLINE number is the LEAST favourable of the four (the prior
giving the highest null hit rate). This is the reporting doctrine of
the corpus and it is not negotiable in either direction.

## 6. Statistic

    N_obs  = number of relations satisfied in the observed universe
    N_null = same count in a null draw
    p      = P(N_null >= N_obs)

Clopper-Pearson 95% interval on p. No conversion to sigma anywhere.

## 7. Gates (stop on failure; never widen, never auto-pass)

G1  ENUMERATION: the triple count must equal 660 (with G) / 495
    (without). If not, the enumerator is wrong. STOP.

G2  SELF-CONSISTENCY: R(i,j,k) and R(k,j,i) are the same relation and
    must be counted once. Verify no double-counting. STOP if the count
    changes when the loop order is reversed.

G3  DEGENERACY: no null draw may contain two objects within 1e-9 of
    each other (would create trivial hits). Reject and redraw.

G4  KNOWN-ANSWER: the observed universe must return, at 2% flat
    tolerance, at least the four relations already identified by hand:
    G^2 = m_c m_b, m_s^2 = m_d mu*, m_u^2 = m_d 2m_e, m_s^2 = m_u m_b.
    If any is missing the frame handling is wrong. STOP.

G5  NULL SANITY: the null hit rate must be > 0 at 5% tolerance. A null
    that never hits indicates a bug, not rarity. STOP.

G6  SEED: PCG64, seed = SHA-256 of this file's text, first 8 bytes.
    Recorded in the manifest. No reseeding after inspection.

## 8. What this cannot price

- The choice of the geometric-mean family itself. That is the
  structural hypothesis, not a statistical one.
- The choice of object set, in particular the inclusion of mu*, 2m_e
  and G. Runs with and without are reported.
- The frame assignment of Sec. 3.
- Hypothesis birth. Unlisted freedom caps inference and is not
  quantified here.

## 9. Deliverable

results/gmc/
    manifest.json      spec hash, seed, versions, timestamps
    census_obs.json    every satisfied relation in the observed set
    null_<prior>.json  hit distributions, p, CP95
    tolerance_curve.json
    GATES.json         every gate with PASS/FAIL and its numbers
