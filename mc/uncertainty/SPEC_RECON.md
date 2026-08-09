# INDEPENDENT RECONSTRUCTION OF THE LOW-SCALE OBSERVABLE — SPEC v1.0
# Self-contained. Ambiguity: conservative reading, ASSUMPTIONS.md, continue — never ask.
# Purpose: kill the single-source dependence. Reconstruct 9Q_U(M_Z) from PRIMARY
# PDG inputs through our own pipeline and compare to the AHS tabulation.
# This is a CROSS-CHECK, not a replacement: AHS remains the quoted source.

## PART A — INDEPENDENT RECONSTRUCTION
Primary inputs (PDG 2024, cite table/page in ASSUMPTIONS.md; do NOT take these
from AHS): m_u(2 GeV), m_c(m_c), m_t (pole), alpha_s(M_Z), m_b(m_b) as needed
for flavor thresholds. Use published conversion/running machinery only:
- 4-loop QCD running + 3-loop threshold matching to bring m_u, m_c to M_Z
  (RunDec/CRunDec conventions; cite Herren-Steinhauser CPC 224 (2018) 333).
- m_t pole -> MSbar via published relation (state loop order + citation).
- Convert to Yukawas y_i = sqrt(2) m_i(M_Z)/v with v from G_F (state value).
Compute 9Q_U(M_Z) and propagate the PDG input uncertainties (draw-once,
N >= 1e5, correlation envelope spanning fully-correlated to anticorrelated).

GATE R1: the reconstructed central 9Q_U(M_Z) must agree with the AHS tabulated
7.9886 within the combined uncertainty of the two determinations. Print both
values, both bands, and the pull. STOP and print if it fails — do not tune.
GATE R2: reconstructed band must be the same order as the quoted +-0.0074
(factor 2 either way). Report both.

## PART B — mc/uncertainty MODULE (repo uptype-pinning)
Package the AHS-input propagation that produced 7.9886 +- 0.0074 as a runnable
module: extract_inputs.py, propagate_mz.py, correlation_stress.py,
reproduce_table.py, SOURCE_NOTES.md. One command must reproduce the quoted
central value, the +-0.0074 band, the component sensitivities (y_c, y_u, y_t),
and the correlation envelope. Include the Part A reconstruction as
independent_reconstruction.py with its gate records.

## OUTPUT
Archive under uptype-pinning (new dir mc/uncertainty/), commit + push, tag
v2.1. Print: reconstructed value +- band, AHS value +- band, pull, gate
records, module reproduction check, artifact paths, DONE.
NO manuscript edits.
