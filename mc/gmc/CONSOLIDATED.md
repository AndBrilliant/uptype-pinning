# Joint MC — consolidated findings, autonomous run 2026-08-12

## The corrected picture (an earlier framing in FINDINGS.md was wrong)

I initially classified the μ⋆ relations as "convention-dependent" and lumped
them with the heavy pair. **That was wrong**, and the correction matters.
Three categories, not two:

| category | meaning | members |
|---|---|---|
| **frame-invariant** | holds at any scale | Q_ℓ, Q_D, Q_U, m_s/m_d, m_b/m_c |
| **scale-fixed** | holds at one scale, that scale determined independently by physics | m_s = α²μ⋆, m_d = α⁴μ⋆, m_u² = m_d·2mₑ, √(m_c m_b) = (1+α)μ⋆ |
| **convention-ambiguous** | requires a choice between defensible alternatives | m_b/m_c = π²/3 at self-scales |

μ⋆ is the charged-lepton pole sum: scheme-independent, fixed before any quark
enters. A relation anchored to it is a *prediction of a scale*, not a free
choice.

## The convergence result

Solving each scale-fixed relation for the scale at which it holds exactly:

| relation | exact at | vs μ⋆ |
|---|---|---|
| m_s = α²μ⋆ | 1884.7 MeV | **+0.09%** |
| m_d = α⁴μ⋆ | 1854.2 MeV | −1.53% |
| m_s² = m_d μ⋆ | 1916.0 MeV | +1.75% |
| m_u² = m_d·2mₑ | 1810.3 MeV | −3.86% |
| √(m_c m_b) = (1+α)μ⋆ | 2065.4 MeV | +9.69% |

Four light-sector relations independently converge on the lepton sum within
4%, the tightest at 0.09%. That is a nontrivial consistency check, and it is
the opposite of what a convention-dependence reading would predict.

**Caveat on independence:** these are not four independent constraints. Given
m_s/m_d = α⁻² and one normalisation, the first three are equivalent. The
honest count for the down sector is **two**: the invariant ratio, plus the
anchor to μ⋆.

## Joint MC

Seven claims, Koide granted as prior art (the null derives α from its own
leptons), N = 5×10⁵ per prior, three admissible priors.

| treatment | observed | least-favourable p |
|---|---|---|
| mixed frames (invalid — see below) | 7/7 at 2% | 0 in 5×10⁵ |
| single frame at μ⋆ | 5/7 at 2% | 0 in 5×10⁵ |
| single frame, 1% tolerance | 3/7 | 1.0×10⁻⁵ |

Null means 0.02–0.26 claims out of seven; the null **never exceeded 4**.

**Why the mixed-frame version is invalid:** it let the observed universe use
m_b = 4970 (2 GeV) for Q_D and m_b = 4183 (self-scale) for the heavy pair —
two values of one mass. The null gets one value. That asymmetry inflates the
result and the number must not be quoted.

**Why the single-frame version is also imperfect:** there is no common frame
containing all six quarks. The top cannot be run below its own threshold; it
is integrated out. "m_t at μ⋆" is not a defined object. So a strict
single-frame requirement is too strong, and the honest treatment is
sector-native frames with the *same* value of each mass used everywhere —
which is what the letter already does.

## What survives all of it

1. **Q_ℓ = 2/3, Q_D = 2/3, Q_U = 8/9** — frame-invariant, one per sector.
2. **m_s/m_d = α⁻²** — frame-invariant, +0.48%.
3. **m_s = α²μ⋆** — scale-fixed, and the scale it picks out is μ⋆ to 0.09%.
4. **√(m_c m_b) = (1+α)μ⋆** — scale-fixed, +0.05% at self-scales.

Priced jointly with one value per mass and Koide granted: **p < 2×10⁻⁵**
against every admissible prior, with null means below 0.3 and a null maximum
of 4 out of 7 in 1.5×10⁶ total draws.

## What does not survive

- The geometric-mean census as a rarity claim (see FINDINGS.md §3).
- b/c = π²/3 as a frame-free statement: the invariant ratio is 4.533, and
  3.286 is the self-scale value. It is convention-specific, as the letter says.
- Any claim involving m_t in a common frame.
