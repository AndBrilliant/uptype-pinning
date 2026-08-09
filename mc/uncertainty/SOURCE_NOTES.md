# SOURCE_NOTES.md — Citation Register

## Primary Data: PDG 2024

S. Navas et al. (Particle Data Group),
"Review of Particle Physics,"
Phys. Rev. D 110, 030001 (2024).

- Quark masses: Sec. 72, "Quark Masses" (A. Hoang, C. Lepenik, V. Mateu,
  S. Peris, M. Steinhauser)
- Quantum Chromodynamics: Sec. 9, "Quantum Chromodynamics" (S. Bethke,
  G. Dissertori, G. P. Salam)
- Electroweak model: Sec. 10, "Electroweak Model and Constraints on
  New Physics" (J. Erler, A. Freitas, M. Gonzalez-Garcia, et al.)

Selected PDG 2024 summary table values:
- m_u(2 GeV) = 2.16 ± 0.07 MeV (MSbar, FLAG 2021 lattice average,
  PDG Table 72.1, "Quark masses" summary)
- m_c(m_c) = 1.2730 ± 0.0046 GeV (MSbar, PDG Table 72.1)
- m_t(pole) = 172.4 ± 0.7 GeV (cross-section measurements,
  PDG Table 72.1 "Top quark pole mass")
- α_s(M_Z) = 0.1180 ± 0.0009 (PDG QCD review, world average)
- m_b(m_b) = 4.183 ± 0.007 GeV (MSbar, PDG Table 72.1; used for
  flavour threshold location only)
- G_F = 1.1663788 × 10⁻⁵ GeV⁻² (PDG Electroweak review)
- M_Z = 91.1876 ± 0.0021 GeV (PDG)

## QCD Running Machinery

### Beta Function (4-loop)
T. van Ritbergen, J. A. M. Vermaseren, S. A. Larin,
"The four-loop beta function in quantum chromodynamics,"
Phys. Lett. B 400 (1997) 379–384.
[hep-ph/9701390]

### Mass Anomalous Dimension (4-loop)
K. G. Chetyrkin,
"Quark mass anomalous dimension to O(α_s⁴),"
Phys. Lett. B 404 (1997) 161–165.
[hep-ph/9703278]

J. A. M. Vermaseren, S. A. Larin, T. van Ritbergen,
"The four-loop quark mass anomalous dimension and the invariant quark mass,"
Phys. Lett. B 405 (1997) 327–333.
[hep-ph/9703284]

### Threshold Matching (α_s, 3-loop)
K. G. Chetyrkin, B. A. Kniehl, M. Steinhauser,
"Strong coupling constant with flavour thresholds at four loops in the MSbar scheme,"
Phys. Rev. Lett. 79 (1997) 2184–2187.
[hep-ph/9706430]

K. G. Chetyrkin, B. A. Kniehl, M. Steinhauser,
"Decoupling relations to O(α_s³) and their connection to low-energy theorems,"
Nucl. Phys. B 510 (1998) 61–87.
[hep-ph/9708255]

### Threshold Matching (α_s, 4-loop)
Y. Schröder, M. Steinhauser,
"Four-loop decoupling relations for the strong coupling,"
JHEP 01 (2006) 051.
[hep-ph/0512058]

### Threshold Matching (mass, 4-loop)
K. G. Chetyrkin, J. H. Kühn, C. Sturm,
"Four-loop mass decoupling relation for the MSbar scheme,"
Nucl. Phys. B 744 (2006) 121–135.
[hep-ph/0512060]

### CRunDec Package (reference implementation)
F. Herren, M. Steinhauser,
"Version 3 of RunDec and CRunDec,"
Comput. Phys. Commun. 224 (2018) 333–345.
[arXiv:1709.07405]

The matching coefficients used in this module were transcribed from the
CRunDec Fortran source code (available at
https://www.ttp.kit.edu/Progdata/ttp18/ttp18-024/) and evaluated
numerically for SU(3) with n_h = 1 at μ = m_q (L = 0).

### Top Quark Pole → MSbar (4-loop)
P. Marquard, A. V. Smirnov, V. A. Smirnov, M. Steinhauser,
"Quark mass relations to four-loop order in perturbative QCD,"
Phys. Rev. Lett. 114 (2015) 142002.
[arXiv:1502.01030]

P. Marquard, A. V. Smirnov, V. A. Smirnov, M. Steinhauser,
"Four-loop quark mass relation in the MSbar scheme,"
Phys. Rev. D 94 (2016) 074025.
[arXiv:1607.06821]

### Input Correlations
PDG 2024 does not publish a full correlation matrix for the quark masses.
The m_t pole mass from cross-section measurements and α_s(M_Z) from the
world average are treated as independent. This is a conservative choice:
any genuine correlation between m_t and α_s from global electroweak fits
would reduce the uncertainty on 9Q_U(M_Z).

## AHS Tabulation (target values)

The reference values against which this reconstruction is checked:
- 9Q_U(M_Z) = 7.9886
- Band: ±0.0074
- y_u(M_Z) = 7.04 × 10⁻⁶
- y_c(M_Z) = 0.00356
- y_t(M_Z) = 0.967

These come from the AHS (Brilliant, 2026) tabulation that this module
cross-checks. They are the TARGET, not an input to the reconstruction.

## Running of quark masses — independent reference

S. Antusch, S. Hinze, S. Saad,
"Updated running quark and lepton parameters at various scales,"
arXiv:2510.01312 (2025).

Provides an independent cross-check of the mass running values at M_Z
from the same PDG 2024 inputs. Used to verify that our running engine
produces physically reasonable values.
