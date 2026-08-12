/-
Frame invariance of same-sector mass relations.

Companion to the heavy-pair letter and to the light-sector map.

WHY THIS MATTERS.  The corpus contains three kinds of statement and they are
not equally robust:

  frame-invariant   holds at every renormalization scale
  scale-fixed       holds at one scale, that scale determined independently
  convention-bound  requires a choice between defensible alternatives

Under pure QCD running inside a fixed-nf window every member of a same-charge
triple carries the SAME anomalous dimension, so the masses are multiplied by a
common factor Z(mu).  This file certifies which functionals survive that.

CERTIFIED HERE
  ratio_invariant       m_j / m_i is unchanged
  Q_invariant           the participation ratio is unchanged (degree-zero)
  Qinv_invariant        the ratio in INVERSE coordinates is likewise unchanged
  geom_mean_not_invariant  a geometric mean against an EXTERNAL scale is NOT:
                        it picks up a factor sqrt(Z), so such a relation
                        selects a scale rather than holding at all of them
  power_ratio_invariant the protection is power-blind: (sum v^p)/(sum v^(p/2))^2
                        sheds the common factor for every real exponent p

CONSEQUENCE.  m_s/m_d = alpha^-2 is a scale-free claim; m_s = alpha^2 mu* is
not, and is a statement about the scale mu* specifically.  The letter's
heavy-pair relations are of the second kind and are labelled as such.

Toolchain: leanprover/lean4 v4.31.0 with Mathlib.
-/
import Mathlib

noncomputable section
open Real
namespace FrameInvariance

/-! ## Common rescaling -/

/-- Ratios of same-sector masses are invariant under a common rescaling. -/
theorem ratio_invariant {Z x y : ℝ} (hZ : Z ≠ 0) (hy : y ≠ 0) :
    (Z * x) / (Z * y) = x / y := by
  field_simp

/-- The participation ratio is invariant: it is degree-zero homogeneous. -/
theorem Q_invariant {Z a b c : ℝ} (hZ : 0 < Z) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hc : 0 ≤ c) (hS : Real.sqrt a + Real.sqrt b + Real.sqrt c ≠ 0) :
    (Z*a + Z*b + Z*c) / (Real.sqrt (Z*a) + Real.sqrt (Z*b) + Real.sqrt (Z*c)) ^ 2
      = (a + b + c) / (Real.sqrt a + Real.sqrt b + Real.sqrt c) ^ 2 := by
  have hZ0 : (0:ℝ) ≤ Z := hZ.le
  rw [Real.sqrt_mul hZ0, Real.sqrt_mul hZ0, Real.sqrt_mul hZ0]
  have hsz : Real.sqrt Z ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hZ)
  have hzz : Real.sqrt Z * Real.sqrt Z = Z := Real.mul_self_sqrt hZ0
  have : Real.sqrt Z * Real.sqrt a + Real.sqrt Z * Real.sqrt b
       + Real.sqrt Z * Real.sqrt c
       = Real.sqrt Z * (Real.sqrt a + Real.sqrt b + Real.sqrt c) := by ring
  rw [this, mul_pow]
  field_simp
  nlinarith [hzz]

/-- The same holds in inverse coordinates: the down-sector cone is frame-free. -/
theorem Qinv_invariant {Z a b c : ℝ} (hZ : 0 < Z) (ha : 0 < a) (hb : 0 < b)
    (hc : 0 < c) :
    (1/(Z*a) + 1/(Z*b) + 1/(Z*c))
      / (Real.sqrt (1/(Z*a)) + Real.sqrt (1/(Z*b)) + Real.sqrt (1/(Z*c))) ^ 2
    = (1/a + 1/b + 1/c) / (Real.sqrt (1/a) + Real.sqrt (1/b) + Real.sqrt (1/c)) ^ 2 := by
  have hZ' : Z ≠ 0 := ne_of_gt hZ
  have e : ∀ x : ℝ, 0 < x → (1:ℝ)/(Z*x) = (1/Z) * (1/x) := by
    intro x hx; field_simp
  rw [e a ha, e b hb, e c hc]
  have hinv : (0:ℝ) < 1/Z := by positivity
  exact Q_invariant hinv (by positivity) (by positivity) (by positivity)
    (by positivity)

/-! ## What is NOT invariant -/

/-- A relation of the form `m_j^2 = m_i * S` with `S` an external, non-running
scale is **not** invariant: rescaling the quarks by `Z` multiplies the left
side by `Z^2` and the right by `Z`, so the relation can hold at one scale
only.  This is the formal content of the distinction between frame-invariant
and scale-fixed statements. -/
theorem external_scale_not_invariant {Z x y S : ℝ} (hZ : 0 < Z) (hZ1 : Z ≠ 1)
    (hx : 0 < x) (hy : 0 < y) (hS : 0 < S) (h : x ^ 2 = y * S) :
    (Z*x) ^ 2 ≠ (Z*y) * S := by
  intro hcon
  have hyS : (0:ℝ) < y * S := mul_pos hy hS
  have h1 : Z ^ 2 * (y * S) = Z * (y * S) := by
    calc Z ^ 2 * (y * S) = (Z * x) ^ 2 := by rw [← h]; ring
      _ = (Z * y) * S := hcon
      _ = Z * (y * S) := by ring
  have h2 : Z ^ 2 = Z := mul_right_cancel₀ (ne_of_gt hyS) h1
  have hz1 : Z = 1 := by
    have hz : Z * (Z - 1) = 0 := by nlinarith [h2]
    rcases mul_eq_zero.mp hz with h3 | h3
    · exact absurd h3 (ne_of_gt hZ)
    · linarith
  exact hZ1 hz1

/-! ## Power-blindness -/

/-- Squaring the half-power recovers the full power, for a positive base. -/
theorem half_pow_sq {w p : ℝ} (hw : 0 < w) : (w ^ (p/2)) ^ (2:ℕ) = w ^ p := by
  rw [← Real.rpow_natCast (w ^ (p/2)) 2, ← Real.rpow_mul hw.le]
  norm_num

/-- **Power-blindness.**  The protection does not depend on the exponent: for
every real `p`, the generalized ratio sheds a common factor.  Setting `p = 1`
recovers `Q_invariant`; the inverse-coordinate cone is `p = -1`. -/
theorem power_ratio_invariant {Z a b c : ℝ} (hZ : 0 < Z) (ha : 0 < a)
    (hb : 0 < b) (hc : 0 < c) (p : ℝ)
    (hS : a ^ (p/2) + b ^ (p/2) + c ^ (p/2) ≠ 0) :
    ((Z*a) ^ p + (Z*b) ^ p + (Z*c) ^ p)
      / ((Z*a) ^ (p/2) + (Z*b) ^ (p/2) + (Z*c) ^ (p/2)) ^ (2:ℕ)
    = (a ^ p + b ^ p + c ^ p) / (a ^ (p/2) + b ^ (p/2) + c ^ (p/2)) ^ (2:ℕ) := by
  have hZ0 : (0:ℝ) ≤ Z := hZ.le
  rw [Real.mul_rpow hZ0 ha.le, Real.mul_rpow hZ0 hb.le, Real.mul_rpow hZ0 hc.le,
      Real.mul_rpow hZ0 ha.le, Real.mul_rpow hZ0 hb.le, Real.mul_rpow hZ0 hc.le]
  have e1 : Z ^ p * a ^ p + Z ^ p * b ^ p + Z ^ p * c ^ p
          = Z ^ p * (a ^ p + b ^ p + c ^ p) := by ring
  have e2 : Z ^ (p/2) * a ^ (p/2) + Z ^ (p/2) * b ^ (p/2) + Z ^ (p/2) * c ^ (p/2)
          = Z ^ (p/2) * (a ^ (p/2) + b ^ (p/2) + c ^ (p/2)) := by ring
  rw [e1, e2, mul_pow, half_pow_sq hZ]
  have hzp : (0:ℝ) < Z ^ p := Real.rpow_pos_of_pos hZ p
  have hden : ((a ^ (p/2) + b ^ (p/2) + c ^ (p/2)) ^ (2:ℕ)) ≠ 0 := pow_ne_zero 2 hS
  field_simp

end FrameInvariance
