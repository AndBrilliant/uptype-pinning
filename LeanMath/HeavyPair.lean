/-
Formal verification of the involution structure of the heavy-quark pair.

Companion to "The map does not stop at the light quarks: the charm-bottom
pair from the charged-lepton scale" (A. M. Brilliant, 2026).

The letter's structural claim is that {m_c, m_b} is an ORBIT of the map
R : x ↦ G²/x, with G = (1+α)μ⋆, rather than the first two rungs of a
ladder.  The distinction matters because an involution has orbits of length
at most two: the top quark's exclusion is then a consequence of the map's
order rather than an observation about where numbers land.

This file proves:
  R_involutive          R ∘ R = id on ℝ≠0
  R_fixed_iff           G is the unique positive fixed point
  R_orbit_card_le_two   every orbit has at most two elements
  pair_of_split         the pair determined by centre and ratio
  pair_product          its product is G², independent of the ratio
  pair_ratio            its ratio is r
  mb_pi_form, mc_pi_form   the closed forms at r = π²/3
  pi_cancels_in_product    π appears in the ratio and not in the product

Toolchain: leanprover/lean4 v4.31.0 with Mathlib.
-/
import Mathlib
import LeanMath.HeavyQuarks

noncomputable section
open Real
namespace HeavyPair

open HeavyQuarks (alphaK alphaK_pos alphaK_add_one_sq)

/-! ## The reflection -/

/-- Reflection of the multiplicative line about the centre `G`. -/
def R (G x : ℝ) : ℝ := G ^ 2 / x

/-- `R` is an involution wherever it is defined. -/
theorem R_involutive {G x : ℝ} (hG : G ≠ 0) (hx : x ≠ 0) :
    R G (R G x) = x := by
  unfold R
  field_simp

/-- The centre is a fixed point. -/
theorem R_fixed (G : ℝ) (hG : G ≠ 0) : R G G = G := by
  unfold R; field_simp

/-- On the positive reals the centre is the *only* fixed point. -/
theorem R_fixed_iff {G x : ℝ} (hG : 0 < G) (hx : 0 < x) :
    R G x = x ↔ x = G := by
  constructor
  · intro h
    unfold R at h
    have hx' : x ≠ 0 := ne_of_gt hx
    have hsq : G ^ 2 = x ^ 2 := by field_simp at h; linarith
    have hz : (x - G) * (x + G) = 0 := by nlinarith [hsq]
    rcases mul_eq_zero.mp hz with h3 | h3
    · linarith
    · linarith
  · rintro rfl
    unfold R
    field_simp

/-- An orbit of `R` through a positive point. -/
def orbit (G x : ℝ) : Set ℝ := {x, R G x}

/-- Every orbit has at most two elements: an involution admits no third
    slot.  This is the structural form of the top-quark exclusion. -/
theorem R_orbit_card_le_two (G x : ℝ) : (orbit G x).Finite ∧
    (orbit G x).ncard ≤ 2 := by
  constructor
  · exact (Set.finite_singleton _).insert _
  · exact le_trans (Set.ncard_insert_le _ _) (by simp)

/-- The orbit is closed under `R`. -/
theorem orbit_closed {G x : ℝ} (hG : G ≠ 0) (hx : x ≠ 0) :
    R G x ∈ orbit G x ∧ R G (R G x) ∈ orbit G x := by
  refine ⟨by simp [orbit], ?_⟩
  rw [R_involutive hG hx]
  simp [orbit]

/-! ## The pair, given a centre and a split -/

/-- The lighter member, given centre `G` and ratio `r > 1`. -/
def mLo (G r : ℝ) : ℝ := G / Real.sqrt r

/-- The heavier member. -/
def mHi (G r : ℝ) : ℝ := G * Real.sqrt r

/-- The two members are exchanged by `R`. -/
theorem pair_of_split {G r : ℝ} (hG : G ≠ 0) (hr : 0 < r) :
    R G (mLo G r) = mHi G r := by
  unfold R mLo mHi
  have hs : Real.sqrt r ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hr)
  field_simp

/-- The product is `G²` whatever the split: the centre is fixed by the
    product alone. -/
theorem pair_product {G r : ℝ} (hr : 0 < r) :
    mLo G r * mHi G r = G ^ 2 := by
  unfold mLo mHi
  have hs : Real.sqrt r ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hr)
  field_simp

/-- The ratio is `r`: the split is fixed by the ratio alone. -/
theorem pair_ratio {G r : ℝ} (hG : G ≠ 0) (hr : 0 < r) :
    mHi G r / mLo G r = r := by
  unfold mLo mHi
  have hs : Real.sqrt r ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hr)
  have hsq : Real.sqrt r * Real.sqrt r = r := Real.mul_self_sqrt (le_of_lt hr)
  field_simp
  linarith [hsq]

/-! ## The closed forms at the observed split

With centre `G = (1+α)μ` and split `r = π²/3` the pair takes the closed
forms of the letter.  The point of stating both is that `π` appears in the
*ratio* and cancels in the *product*: the position of the pair is fixed by
`α` alone, and `π` enters only in the separation. -/

/-- Positive reals with equal squares are equal. -/
lemma eq_of_sq_eq {a b : ℝ} (ha : 0 < a) (hb : 0 < b) (h : a ^ 2 = b ^ 2) :
    a = b := by
  have hz : (a - b) * (a + b) = 0 := by nlinarith [h]
  rcases mul_eq_zero.mp hz with h1 | h1
  · linarith
  · linarith

lemma sqrt_three_sq : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
lemma sqrt_two_sq : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)

/-- `√(π²/3) = π/√3`. -/
lemma sqrt_pi_sq_div_three : Real.sqrt (π ^ 2 / 3) = π / Real.sqrt 3 := by
  rw [Real.sqrt_div (by positivity) 3, Real.sqrt_sq (le_of_lt Real.pi_pos)]

/-- `(1+α)/√3 = 1/√2`. -/
lemma norm_div_sqrt_three : (alphaK + 1) / Real.sqrt 3 = 1 / Real.sqrt 2 := by
  have hpos : 0 < alphaK + 1 := by linarith [alphaK_pos]
  have h3 : (0:ℝ) < Real.sqrt 3 := by positivity
  have h2 : (0:ℝ) < Real.sqrt 2 := by positivity
  refine eq_of_sq_eq (by positivity) (by positivity) ?_
  rw [div_pow, div_pow, alphaK_add_one_sq, sqrt_three_sq, sqrt_two_sq]
  norm_num

/-- `(1+α)·√3 = 3/√2`. -/
lemma norm_mul_sqrt_three : (alphaK + 1) * Real.sqrt 3 = 3 / Real.sqrt 2 := by
  have hpos : 0 < alphaK + 1 := by linarith [alphaK_pos]
  have h3 : (0:ℝ) < Real.sqrt 3 := by positivity
  have h2 : (0:ℝ) < Real.sqrt 2 := by positivity
  refine eq_of_sq_eq (by positivity) (by positivity) ?_
  rw [mul_pow, alphaK_add_one_sq, sqrt_three_sq, div_pow, sqrt_two_sq]
  norm_num

/-- The heavy member: `m_b = πμ/√2`. -/
theorem mHi_pi_form (μ : ℝ) :
    mHi ((alphaK + 1) * μ) (π ^ 2 / 3) = π * μ / Real.sqrt 2 := by
  unfold mHi
  rw [sqrt_pi_sq_div_three,
      show (alphaK + 1) * μ * (π / Real.sqrt 3)
        = ((alphaK + 1) / Real.sqrt 3) * (π * μ) by ring,
      norm_div_sqrt_three]
  ring

/-- The light member: `m_c = 3μ/(π√2)`. -/
theorem mLo_pi_form (μ : ℝ) :
    mLo ((alphaK + 1) * μ) (π ^ 2 / 3) = 3 * μ / (π * Real.sqrt 2) := by
  unfold mLo
  have hpi : π ≠ 0 := ne_of_gt Real.pi_pos
  have h3 : Real.sqrt 3 ≠ 0 := by positivity
  have h2 : Real.sqrt 2 ≠ 0 := by positivity
  rw [sqrt_pi_sq_div_three, div_div_eq_mul_div,
      show (alphaK + 1) * μ * Real.sqrt 3
        = ((alphaK + 1) * Real.sqrt 3) * μ by ring,
      norm_mul_sqrt_three]
  field_simp

/-- **π cancels in the product.**  The centre is `α`-only; `π` lives
    entirely in the split. -/
theorem pi_cancels_in_product (μ : ℝ) :
    mLo ((alphaK + 1) * μ) (π ^ 2 / 3) * mHi ((alphaK + 1) * μ) (π ^ 2 / 3)
      = 3 / 2 * μ ^ 2 := by
  rw [pair_product (by positivity : (0:ℝ) < π ^ 2 / 3), mul_pow,
      alphaK_add_one_sq]

end HeavyPair
