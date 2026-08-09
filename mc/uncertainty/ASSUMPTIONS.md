# ASSUMPTIONS.md — Conservative Reading & Assumption Register

## Purpose
Every ambiguity resolved, every choice documented. Conservative reading: where
two interpretations of a published value are possible, take the one that
produces a LARGER uncertainty on the final 9Q_U(M_Z).

## Primary Inputs (PDG 2024)

| Parameter | Value | Uncertainty | Source | Note |
|-----------|-------|-------------|--------|------|
| m_u(2 GeV) | 2.16 MeV | ±0.07 MeV | PDG 2024, Quark Masses review (S. Navas et al., Phys. Rev. D 110, 030001), Table 72.1; FLAG 2021 lattice average | MSbar, n_f=3 scheme |
| m_c(m_c) | 1.2730 GeV | ±0.0046 GeV | PDG 2024, ibid., Table 72.1 | MSbar, n_f=4 scheme. The PDG quotes this as the running mass at its own scale. |
| m_t(pole) | 172.4 GeV | ±0.7 GeV | PDG 2024, ibid., cross-section measurement average | Pole mass. We use the cross-section average rather than the direct-reconstruction value (172.57 ± 0.29) to be conservative (larger uncertainty). |
| α_s(M_Z) | 0.1180 | ±0.0009 | PDG 2024, ibid., QCD review (S. Bethke et al.) | 5-flavour MSbar scheme |
| m_b(m_b) | 4.183 GeV | ±0.007 GeV | PDG 2024, ibid., for threshold location only | Used to set the flavour threshold μ = m_b. The threshold scale is not varied in the central reconstruction. |
| G_F | 1.1663788×10⁻⁵ GeV⁻² | — | PDG 2024, Electroweak review | Fermi constant; used to define v = (√2 G_F)⁻¹/² |

## QCD Running Assumptions

1. **Loop order:** 4-loop beta function + 4-loop mass anomalous dimension.
   Coefficients from van Ritbergen, Vermaseren, Larin, Phys. Lett. B 400
   (1997) 379 (beta) and Chetyrkin, Phys. Lett. B 404 (1997) 161 /
   Vermaseren, Larin, van Ritbergen, Phys. Lett. B 405 (1997) 327 (gamma_m).

2. **Threshold matching:** 3-loop decoupling for α_s and the MSbar mass,
   coefficients from Chetyrkin, Kniehl, Steinhauser, Nucl. Phys. B 510
   (1998) 61; Phys. Rev. Lett. 79 (1997) 2184; Schröder & Steinhauser,
   JHEP 01 (2006) 051; Chetyrkin, Kühn & Sturm, Nucl. Phys. B 744 (2006)
   121. Numerical values for SU(3) with n_h=1 at L=0 (μ=m_q) transcribed
   from the CRunDec source code (Herren & Steinhauser, Comput. Phys.
   Commun. 224 (2018) 333).

3. **Flavour scheme conventions:**
   - m_u(2 GeV) is in the n_f=3 scheme (u, d, s active; charm and bottom
     integrated out, even though 2 GeV > m_c).
   - m_c(m_c) is in the n_f=4 scheme.
   - α_s(M_Z) is in the n_f=5 scheme.
   - m_t(m_t) is computed in the n_f=5 scheme (top integrated out at its
     own scale, per CRunDec convention).

4. **Running direction for u-quark:** The input scale (2 GeV) is ABOVE
   m_c (1.273 GeV) but in the 3-flavour scheme. The mass is first run
   DOWN to m_c in n_f=3, matched UP through the charm threshold (3→4),
   run UP to m_b, matched UP through the bottom threshold (4→5), and
   run UP to M_Z. This is the standard CRunDec convention for light-quark
   MSbar masses defined in the 3-flavour scheme at 2 GeV.

5. **m_t pole → MSbar:** 4-loop conversion from Marquard, Smirnov,
   Smirnov & Steinhauser, Phys. Rev. Lett. 114 (2015) 142002 and
   Phys. Rev. D 94 (2016) 074025. Numerical coefficients for n_f=5
   transcribed from the RunDec source. Iterated to self-consistency
   (the conversion depends on α_s at m_t, which depends on m_t itself).

6. **Integration method:** scipy.integrate.solve_ivp (RK45, rtol=1e-12,
   atol=1e-14) for α_s running; 200-point trapezoidal quadrature for the
   mass running integral ∫ γ_m/β da. Both verified against 1-loop analytic
   solutions.

## Uncertainty Propagation Assumptions

1. **Method:** Draw-once Monte Carlo, N ≥ 1×10⁵. Each draw samples the
   four primary inputs (m_u, m_c, m_t, α_s) from independent Gaussians
   (PDG uncertainties), runs the full pipeline to M_Z, and computes 9Q.

2. **Correlation envelope (Part B):** The ±0.0074 band is bracketed by
   two extremes: (a) fully correlated input variations (all δ move
   together → widest 9Q band), (b) anti-correlated where the 9Q
   sensitivity signs allow (narrowest 9Q band). The actual uncertainty
   lies between these extremes.

3. **Induced correlation (operator addition):** The PDG primaries are
   propagated as independent Gaussians, and the INDUCED covariance of
   (y_u, y_c, y_t) at M_Z is computed from the MC sample. This induced
   correlation arises from the shared dependence on α_s through the QCD
   running and threshold matching. It is COMPUTED, not assumed.

4. **No PDG-internal correlations are modelled.** If the PDG inputs have
   published correlations (e.g., m_t and α_s from global electroweak
   fits), they are conservatively treated as independent. This inflates
   the final uncertainty band relative to a fit that uses the full
   correlation matrix, consistent with the "conservative reading"
   directive.

## Physical Constants

| Constant | Value | Source |
|----------|-------|--------|
| v (Higgs vev) | 246.21971 GeV | Derived from G_F = 1.1663788×10⁻⁵ GeV⁻² |
| M_Z | 91.1876 GeV | PDG 2024 |
| ζ₃ (Apéry) | 1.2020569031595942854 | — |
| ζ₄ | π⁴/90 ≈ 1.0823232337 | — |
| ζ₅ | 1.0369277551433699263 | — |

## Gate Criteria

- **GATE R1:** |9Q_recon − 7.9886| ≤ sqrt(σ²_recon + 0.0074²). STOP if
  it fails; do not tune.
- **GATE R2:** σ_recon ∈ [0.0037, 0.0148] (factor 2 either way from 0.0074).
- **Correlation gate:** The derived-correlation band must be COMPUTED from
  the MC sample, never assumed. Report whether it lands inside the bracketed
  envelope (0.004–0.014).
