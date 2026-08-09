/-
Formal verification of the algebraic propositions in the Descartes–Soddy
heavy-quark cascade paper (A. M. Brilliant, draft 2026).

Proposition 1 (cone lemma): sampling Z(φ) = c0 + A·cos(φ + δ) at
the family phases φ_a = 2πa/3 (a = 0,1,2, written out explicitly below),
e1 = 3c0 and p2 = 3c0² + (3/2)A² for every δ; the Koide ratio p2/e1² = 2/3
iff A = √2·c0; and under that condition (e1 − √p2)/√p2 = α = √(3/2) − 1.
The two-coordinate application — leptons sitting on the cone in √m and
down-type quarks in 1/√m, so both share α — is an empirical statement made
in the paper. It is NOT an algebraic invariance of a fixed mass triple under
m ↦ 1/m (reading one fixed triple as √m vs 1/√m does not give the same ratio);
the cone lemma below quantifies only over sampled values z_a on the cone.

Proposition 2 (heavy sector from one coefficient): with G² = (3/2)μ²,
m_c = 3αμ and m_b = G²/m_c, one gets m_b = μ/(2α) = μ/(√6 − 2) and the
bridge m_c·m_b = (3/2)μ².

Executable spec: prover/prover.py Part A (sympy) in the same repository.
Verified against Lean 4 / Mathlib (toolchain v4.31.0).
-/
import Mathlib

noncomputable section

open Real

namespace HeavyQuarks

/-- The cascade constant α = √(3/2) − 1. -/
def alphaK : ℝ := Real.sqrt (3 / 2) - 1

/-- √6 = 2·√(3/2): the bridge between the Koide norm and the cascade constant. -/
lemma sqrt6_eq : Real.sqrt 6 = 2 * Real.sqrt (3 / 2) := by
  rw [show (6 : ℝ) = 2 ^ 2 * (3 / 2) by norm_num,
      Real.sqrt_mul (by positivity) (3 / 2),
      Real.sqrt_sq (by norm_num : (0 : ℝ) ≤ 2)]

lemma sqrt_three_halves_sq : Real.sqrt (3 / 2) ^ 2 = 3 / 2 :=
  Real.sq_sqrt (by norm_num)

/-- α > 0 (needed wherever we divide by it). -/
lemma alphaK_pos : 0 < alphaK := by
  have h : Real.sqrt 1 < Real.sqrt (3 / 2) :=
    Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  rw [Real.sqrt_one] at h
  simp only [alphaK]
  linarith

lemma alphaK_ne_zero : alphaK ≠ 0 := ne_of_gt alphaK_pos

/-- α² = 5/2 − √6. -/
theorem alphaK_sq : alphaK ^ 2 = 5 / 2 - Real.sqrt 6 := by
  rw [alphaK, sqrt6_eq]
  linear_combination sqrt_three_halves_sq

/-- (α + 1)² = 3/2 — the Koide norm squared. -/
theorem alphaK_add_one_sq : (alphaK + 1) ^ 2 = 3 / 2 := by
  rw [alphaK]
  linear_combination sqrt_three_halves_sq

/-- 2α = √6 − 2 (the closed form used for m_b). -/
theorem two_alphaK : 2 * alphaK = Real.sqrt 6 - 2 := by
  rw [alphaK, sqrt6_eq]; ring

/-- 3/α = 6 + 3√6 — the claimed m_c/m_s ratio. -/
theorem three_div_alphaK : 3 / alphaK = 6 + 3 * Real.sqrt 6 := by
  rw [div_eq_iff alphaK_ne_zero, alphaK, sqrt6_eq]
  linear_combination (-6 : ℝ) * sqrt_three_halves_sq

/-! ## Cone lemma

For values sampled on the cone z_a = c0 + A cos(2πa/3 + δ), the Koide ratio is
2/3 iff A = √2 c0, and then (e1 − √p2)/√p2 = α. The two-coordinate application
(leptons in √m, down-type in 1/√m) is an empirical statement made in the paper,
NOT an algebraic invariance of a fixed mass triple under m ↦ 1/m.

The three family phases φ_a = 2πa/3 for a = 0, 1, 2 are written out
explicitly as 0, 2π/3, 4π/3. -/

/-- Direct reading √m_a = Z(φ_a): the sum e1 = Σ √m_a. -/
def e1 (c0 A δ : ℝ) : ℝ :=
  (c0 + A * Real.cos δ)
    + (c0 + A * Real.cos (2 * π / 3 + δ))
    + (c0 + A * Real.cos (4 * π / 3 + δ))

/-- Direct reading: the sum p2 = Σ m_a. -/
def p2 (c0 A δ : ℝ) : ℝ :=
  (c0 + A * Real.cos δ) ^ 2
    + (c0 + A * Real.cos (2 * π / 3 + δ)) ^ 2
    + (c0 + A * Real.cos (4 * π / 3 + δ)) ^ 2

lemma cos_two_pi_div_three : Real.cos (2 * π / 3) = -(1 / 2) := by
  rw [show (2 * π / 3 : ℝ) = π - π / 3 by ring, Real.cos_pi_sub,
      Real.cos_pi_div_three]

lemma sin_two_pi_div_three : Real.sin (2 * π / 3) = Real.sqrt 3 / 2 := by
  rw [show (2 * π / 3 : ℝ) = π - π / 3 by ring, Real.sin_pi_sub,
      Real.sin_pi_div_three]

lemma cos_four_pi_div_three : Real.cos (4 * π / 3) = -(1 / 2) := by
  rw [show (4 * π / 3 : ℝ) = π + π / 3 by ring, Real.cos_add, Real.cos_pi,
      Real.sin_pi, Real.cos_pi_div_three]
  ring

lemma sin_four_pi_div_three : Real.sin (4 * π / 3) = -(Real.sqrt 3 / 2) := by
  rw [show (4 * π / 3 : ℝ) = π + π / 3 by ring, Real.sin_add, Real.sin_pi,
      Real.cos_pi, Real.sin_pi_div_three]
  ring

/-- Orthogonality of the family phases: e1 = 3c0 for every δ. -/
theorem e1_eq (c0 A δ : ℝ) : e1 c0 A δ = 3 * c0 := by
  unfold e1
  rw [Real.cos_add, Real.cos_add, cos_two_pi_div_three, sin_two_pi_div_three,
      cos_four_pi_div_three, sin_four_pi_div_three]
  ring

/-- p2 = 3c0² + (3/2)A² for every δ. -/
theorem p2_eq (c0 A δ : ℝ) : p2 c0 A δ = 3 * c0 ^ 2 + 3 / 2 * A ^ 2 := by
  unfold p2
  rw [Real.cos_add, Real.cos_add, cos_two_pi_div_three, sin_two_pi_div_three,
      cos_four_pi_div_three, sin_four_pi_div_three]
  have h3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have hp : Real.sin δ ^ 2 + Real.cos δ ^ 2 = 1 := Real.sin_sq_add_cos_sq δ
  linear_combination (A ^ 2 * Real.sin δ ^ 2 / 2) * h3
    + (3 * A ^ 2 / 2) * hp

/-- The Koide ratio p2/e1² equals 2/3 iff A = √2·c0 (positive branch).
This is the load-bearing step: the condition fixes r/c0 = 1/√2 with r = A/2. -/
theorem ratio_iff (c0 A δ : ℝ) (hc : 0 < c0) (hA : 0 < A) :
    p2 c0 A δ / e1 c0 A δ ^ 2 = 2 / 3 ↔ A = Real.sqrt 2 * c0 := by
  rw [e1_eq, p2_eq]
  have h9 : ((3 * c0) ^ 2 : ℝ) ≠ 0 := by positivity
  rw [div_eq_iff h9]
  constructor
  · intro h
    have hA2 : A ^ 2 = 2 * c0 ^ 2 := by nlinarith [h]
    have h1 : Real.sqrt (A ^ 2) = Real.sqrt (2 * c0 ^ 2) := by rw [hA2]
    rwa [Real.sqrt_sq hA.le, Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 2),
         Real.sqrt_sq hc.le] at h1
  · intro h
    subst h
    linear_combination (3 / 2 * c0 ^ 2) * Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)

/-- Under the Koide condition A = √2·c0, the companion constant is α = √(3/2) − 1:
(e1 − √p2)/√p2 = α.  This is a statement about values z_a sampled on the cone; any
data set landing on the cone (leptons in √m, down-type in 1/√m — an empirical fact,
not an algebraic m ↦ 1/m invariance) shares this α. Proposition 1 (cone lemma). -/
theorem alpha_from_cone (c0 δ : ℝ) (hc : 0 < c0) :
    (e1 c0 (Real.sqrt 2 * c0) δ - Real.sqrt (p2 c0 (Real.sqrt 2 * c0) δ)) /
      Real.sqrt (p2 c0 (Real.sqrt 2 * c0) δ) = alphaK := by
  have hp2 : p2 c0 (Real.sqrt 2 * c0) δ = 6 * c0 ^ 2 := by
    rw [p2_eq]
    linear_combination (3 / 2 * c0 ^ 2) * Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  have h6 : Real.sqrt (6 * c0 ^ 2) = Real.sqrt 6 * c0 := by
    rw [Real.sqrt_mul (by norm_num : (0 : ℝ) ≤ 6), Real.sqrt_sq hc.le]
  have hs6 : (0 : ℝ) < Real.sqrt 6 := Real.sqrt_pos.mpr (by norm_num)
  have hne : Real.sqrt 6 * c0 ≠ 0 := by positivity
  rw [e1_eq, hp2, h6, div_eq_iff hne, alphaK, sqrt6_eq]
  linear_combination (-2 * c0) * sqrt_three_halves_sq

/-! ### Positivity of the physical domain (Proposition 1 caveat)

`ratio_iff` and `alpha_from_cone` are algebraic identities that hold for *every* δ;
positivity is not needed for them to be true. The physical *reading* √m_a = Z(φ_a),
however, requires each sample Z(φ_a) ≥ 0 (a mass has a real root). Under the Koide
condition A = √2·c₀ the sample c₀(1 + √2·cos(φ_a+δ)) can dip below zero at some
phases, so the physically meaningful configurations form a proper subset of δ-space.
The following shows that subset — the admissible domain the observed spectra occupy —
is nonempty and realizable, not merely assumed: at δ = 0 all three samples are
strictly positive. -/

/-- The a-th sample under the Koide condition A = √2·c₀:  √m_a = Z(φ_a). -/
def sample (c0 δ : ℝ) : Fin 3 → ℝ
  | 0 => c0 + Real.sqrt 2 * c0 * Real.cos δ
  | 1 => c0 + Real.sqrt 2 * c0 * Real.cos (2 * π / 3 + δ)
  | 2 => c0 + Real.sqrt 2 * c0 * Real.cos (4 * π / 3 + δ)

lemma sqrt2_lt_two : Real.sqrt 2 < 2 := by
  have h := Real.sq_sqrt (show (0 : ℝ) ≤ 2 by norm_num)
  nlinarith [Real.sqrt_nonneg 2, h, sq_nonneg (Real.sqrt 2 - 2)]

/-- At δ = 0 all three samples are strictly positive. -/
theorem sample_pos_at_zero (c0 : ℝ) (hc : 0 < c0) (a : Fin 3) :
    0 < sample c0 0 a := by
  have hlt := sqrt2_lt_two
  fin_cases a <;> simp only [sample, add_zero, Real.cos_zero,
    cos_two_pi_div_three, cos_four_pi_div_three]
  · nlinarith [hc, Real.sqrt_nonneg 2]
  · nlinarith [mul_pos hc (by linarith : (0 : ℝ) < 2 - Real.sqrt 2)]
  · nlinarith [mul_pos hc (by linarith : (0 : ℝ) < 2 - Real.sqrt 2)]

/-- The admissible domain: phases δ at which the physical reading √m_a = Z(φ_a) is
real, i.e. every sample is nonnegative. Prop 1's algebra holds regardless of δ; this
predicate isolates the physically meaningful subset. -/
def Admissible (c0 δ : ℝ) : Prop := ∀ a : Fin 3, 0 < sample c0 δ a

/-- The admissible domain is nonempty for any positive scale c₀: δ = 0 lies in it.
This is the formal content of the Proposition 1 caveat — the domain that the observed
spectra occupy is realizable, closing the one asterisk carried through to the paper. -/
theorem admissible_nonempty (c0 : ℝ) (hc : 0 < c0) : Admissible c0 0 :=
  sample_pos_at_zero c0 hc

/-! ## Proposition 2: the heavy sector from one coefficient

With G² = (3/2)μ★² and the involution m ↦ G²/m pairing charm and bottom,
the single input m_c = 3αμ★ forces everything else. -/

/-- G = (α+1)μ★, i.e. G² = (3/2)μ★². -/
theorem norm_scale_sq (μ : ℝ) : ((alphaK + 1) * μ) ^ 2 = 3 / 2 * μ ^ 2 := by
  linear_combination (μ ^ 2) * alphaK_add_one_sq

/-- m_b = G²/m_c = μ★/(2α). -/
theorem mb_from_involution (μ : ℝ) (hμ : μ ≠ 0) :
    (3 / 2 * μ ^ 2) / (3 * alphaK * μ) = μ / (2 * alphaK) := by
  field_simp

/-- The closed form m_b = μ★/(√6 − 2). -/
theorem mb_closed_form (μ : ℝ) :
    μ / (2 * alphaK) = μ / (Real.sqrt 6 - 2) := by
  rw [two_alphaK]

/-- The bridge: m_c · m_b = (3/2)μ★². The coefficients {3, 1/2} are one
constraint, not two. -/
theorem bridge (μ : ℝ) :
    (3 * alphaK * μ) * (μ / (2 * alphaK)) = 3 / 2 * μ ^ 2 := by
  have hα := alphaK_ne_zero
  field_simp

/-- The geometric mean of the pair is the Koide-norm scale:
√(m_c·m_b) = (α+1)μ★ for μ★ ≥ 0. -/
theorem geometric_mean (μ : ℝ) (hμ : 0 ≤ μ) :
    Real.sqrt ((3 * alphaK * μ) * (μ / (2 * alphaK))) = (alphaK + 1) * μ := by
  rw [bridge]
  have h : (3 / 2 * μ ^ 2 : ℝ) = ((alphaK + 1) * μ) ^ 2 := (norm_scale_sq μ).symm
  have hnn : (0 : ℝ) ≤ (alphaK + 1) * μ :=
    mul_nonneg (by linarith [alphaK_pos]) hμ
  rw [h, Real.sqrt_sq hnn]

end HeavyQuarks
