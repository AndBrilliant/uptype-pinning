/-
Frame invariance of same-sector claims.

The corpus contains claims of two kinds, and the distinction decides which
are scale-free facts and which are statements about a chosen evaluation
point.  Under pure QCD running inside a fixed-n_f window every member of a
same-charge sector is multiplied by one common factor Z(mu).  Consequently:

  * a RATIO of two same-sector masses is unchanged            (ratio_invariant)
  * the participation ratio of a same-sector triple is unchanged  (Q_invariant)
  * a relation tying ONE mass to an external fixed scale is NOT  (anchor_not_invariant)

The third statement is the one that matters and it is proved, not asserted:
the anchor changes by exactly the factor Z, so a claim of the form
`m = c * S` with `S` inert can hold at at most one scale.

This is what separates `m_s/m_d = alpha^-2`, which is frame-free, from
`m_s = alpha^2 mu*`, which is a statement about mu* specifically.

Toolchain: leanprover/lean4 v4.31.0 with Mathlib.
-/
import Mathlib

noncomputable section
open Real
namespace FrameInvariance

/-! ## Common rescaling -/

/-- Flavour-blind evolution: one common positive factor on every member. -/
def scale (Z : ℝ) (v : Fin 3 → ℝ) : Fin 3 → ℝ := fun i => Z * v i

/-- Ratios of same-sector members are invariant. -/
theorem ratio_invariant {Z : ℝ} (hZ : Z ≠ 0) (v : Fin 3 → ℝ) (i j : Fin 3)
    (hj : v j ≠ 0) :
    scale Z v i / scale Z v j = v i / v j := by
  unfold scale
  rw [mul_div_mul_left _ _ hZ]

/-- The sum scales by `Z`. -/
theorem sum_scale (Z : ℝ) (v : Fin 3 → ℝ) :
    (scale Z v 0 + scale Z v 1 + scale Z v 2) = Z * (v 0 + v 1 + v 2) := by
  unfold scale; ring

/-- The square-root sum scales by `√Z`. -/
theorem sqrtsum_scale {Z : ℝ} (hZ : 0 ≤ Z) (v : Fin 3 → ℝ) (h : ∀ i, 0 ≤ v i) :
    (Real.sqrt (scale Z v 0) + Real.sqrt (scale Z v 1) + Real.sqrt (scale Z v 2))
      = Real.sqrt Z * (Real.sqrt (v 0) + Real.sqrt (v 1) + Real.sqrt (v 2)) := by
  unfold scale
  rw [Real.sqrt_mul hZ, Real.sqrt_mul hZ, Real.sqrt_mul hZ]
  ring

/-- The participation ratio of a same-sector triple is invariant. -/
theorem Q_invariant {Z : ℝ} (hZ : 0 < Z) (v : Fin 3 → ℝ) (h : ∀ i, 0 < v i) :
    (scale Z v 0 + scale Z v 1 + scale Z v 2) /
      (Real.sqrt (scale Z v 0) + Real.sqrt (scale Z v 1) + Real.sqrt (scale Z v 2)) ^ 2
    = (v 0 + v 1 + v 2) /
      (Real.sqrt (v 0) + Real.sqrt (v 1) + Real.sqrt (v 2)) ^ 2 := by
  have hnn : ∀ i, 0 ≤ v i := fun i => (h i).le
  have hs0 := Real.sqrt_pos.mpr (h 0)
  have hs1 := Real.sqrt_pos.mpr (h 1)
  have hs2 := Real.sqrt_pos.mpr (h 2)
  have hS : (0:ℝ) < Real.sqrt (v 0) + Real.sqrt (v 1) + Real.sqrt (v 2) := by linarith
  have hZs : (0:ℝ) < Real.sqrt Z := Real.sqrt_pos.mpr hZ
  rw [sum_scale, sqrtsum_scale hZ.le v hnn, mul_pow]
  have hZZ : Real.sqrt Z ^ 2 = Z := Real.sq_sqrt hZ.le
  rw [hZZ]
  rw [mul_div_mul_left _ _ (ne_of_gt hZ)]

/-! ## Anchored relations are not invariant

A claim of the form `v i = c * S`, with `S` an externally fixed scale that
does not participate in the rescaling, holds after rescaling only if `Z = 1`.
-/

/-- An anchored relation transforms with the factor `Z`, so it survives
rescaling only at `Z = 1`: it is a statement about one evaluation point. -/
theorem anchor_not_invariant {Z c S : ℝ} (v : Fin 3 → ℝ) (i : Fin 3)
    (hZ : 0 < Z) (hcS : c * S ≠ 0) (hold : v i = c * S) :
    scale Z v i = c * S ↔ Z = 1 := by
  unfold scale
  rw [hold]
  constructor
  · intro h
    have := mul_right_cancel₀ hcS (by linarith [h] : Z * (c * S) = 1 * (c * S))
    exact this
  · intro h; rw [h, one_mul]

/-- Contrapositive form, stated for the record: two distinct positive scales
cannot both satisfy the same anchored relation. -/
theorem anchor_unique_scale {Z₁ Z₂ c S : ℝ} (v : Fin 3 → ℝ) (i : Fin 3)
    (hZ₁ : 0 < Z₁) (hZ₂ : 0 < Z₂) (hcS : c * S ≠ 0) (hold : v i = c * S)
    (h1 : scale Z₁ v i = c * S) (h2 : scale Z₂ v i = c * S) : Z₁ = Z₂ := by
  rw [anchor_not_invariant v i hZ₁ hcS hold] at h1
  rw [anchor_not_invariant v i hZ₂ hcS hold] at h2
  rw [h1, h2]

end FrameInvariance
