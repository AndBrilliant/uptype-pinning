/-
Formal verification of the sensitivity (amplification) lemma.

Companion to the heavy-pair letter and to the light-sector map.

THE PROBLEM THIS SOLVES.  Several residuals in the corpus look inconsistent
with one another until this lemma is stated.  The down-sector cone holds to
0.11% yet the m_b/m_d prediction it implies is 2.4% off; the up-sector cone
holds to 0.14% yet the charm it implies is 2.65% off; and m_u cannot be
predicted from the up cone at any achievable precision.  All three are one
phenomenon: the participation ratio constrains the SHAPE of a triple, shape
information is carried almost entirely by the members with the largest share
of the square-root sum, and a member with a small share is nearly free.

THE RESULT.  For a positive triple v with

    S₁ = Σ vᵢ,   S₂ = Σ √vᵢ,   Q = S₁ / S₂²,

the logarithmic sensitivity of Q to the k-th member is EXACTLY

    ∂lnQ/∂ln v_k  =  v_k/S₁  −  √v_k/S₂.                            (★)

The gain in the inverse direction — how much a member must move to absorb a
given perturbation of Q — is the reciprocal, and it diverges as √v_k/S₂ → 0.

Verified numerically against the tabulated triples before formalising:
    up (u,c,t)     k=u: −0.00253014   gain 395
                   k=c: −0.05339128   gain  18.7
                   k=t: +0.05592141   gain  17.9
    down inverse   k=b: −0.02558270   gain  39.1
    leptons        k=τ: +0.15047674   gain   6.7

Toolchain: leanprover/lean4 v4.31.0 with Mathlib.
-/
import Mathlib

noncomputable section
open Real
namespace Sensitivity

/-! ## Setup -/

/-- Sum of a triple. -/
def S₁ (a b c : ℝ) : ℝ := a + b + c

/-- Sum of square roots of a triple. -/
def S₂ (a b c : ℝ) : ℝ := Real.sqrt a + Real.sqrt b + Real.sqrt c

/-- The participation ratio of a triple. -/
def Q (a b c : ℝ) : ℝ := S₁ a b c / (S₂ a b c) ^ 2

lemma S₂_pos {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : 0 < S₂ a b c := by
  unfold S₂
  have := Real.sqrt_pos.mpr ha
  have := Real.sqrt_pos.mpr hb
  have := Real.sqrt_pos.mpr hc
  linarith

lemma S₁_pos {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : 0 < S₁ a b c := by
  unfold S₁; linarith

lemma Q_pos {a b c : ℝ} (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : 0 < Q a b c := by
  unfold Q
  exact div_pos (S₁_pos ha hb hc) (pow_pos (S₂_pos ha hb hc) 2)

/-! ## The derivative of the first member

We differentiate in the first slot; the other two follow by the symmetry of
`Q` under permutation of its arguments, recorded below.
-/

/-- `S₁` has derivative `1` in its first argument. -/
theorem hasDerivAt_S₁ (b c x : ℝ) : HasDerivAt (fun t => S₁ t b c) 1 x := by
  unfold S₁
  simpa using ((hasDerivAt_id x).add_const b).add_const c

/-- `S₂` has derivative `1/(2√x)` in its first argument, for `x > 0`. -/
theorem hasDerivAt_S₂ {x : ℝ} (hx : 0 < x) (b c : ℝ) :
    HasDerivAt (fun t => S₂ t b c) (1 / (2 * Real.sqrt x)) x := by
  unfold S₂
  simpa using ((Real.hasDerivAt_sqrt (ne_of_gt hx)).add_const
    (Real.sqrt b)).add_const (Real.sqrt c)

/-- The derivative of `Q` in its first argument.  The value is stated in the
raw quotient-rule form; `deriv_Q_eq` below puts it in closed form. -/
theorem hasDerivAt_Q {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    HasDerivAt (fun t => Q t b c)
      ((1 * (S₂ x b c) ^ 2
        - S₁ x b c * (2 * S₂ x b c ^ 1 * (1 / (2 * Real.sqrt x))))
        / ((S₂ x b c) ^ 2) ^ 2) x := by
  have h2 : 0 < S₂ x b c := S₂_pos hx hb hc
  have hd₁ := hasDerivAt_S₁ b c x
  have hd₂ := (hasDerivAt_S₂ hx b c).pow 2
  have hne : (S₂ x b c) ^ 2 ≠ 0 := ne_of_gt (pow_pos h2 2)
  exact hd₁.div hd₂ hne

/-- The derivative in closed form. -/
theorem deriv_Q_eq {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    ((1 * (S₂ x b c) ^ 2
      - S₁ x b c * (2 * S₂ x b c ^ 1 * (1 / (2 * Real.sqrt x))))
      / ((S₂ x b c) ^ 2) ^ 2)
    = 1 / (S₂ x b c) ^ 2 - S₁ x b c / ((S₂ x b c) ^ 3 * Real.sqrt x) := by
  have h2 : (0:ℝ) < S₂ x b c := S₂_pos hx hb hc
  have hs : (0:ℝ) < Real.sqrt x := Real.sqrt_pos.mpr hx
  field_simp

/-! ## The sensitivity identity (★)

This is the statement the corpus uses.  Written multiplicatively it says the
logarithmic derivative of `Q` with respect to the first member equals
`x/S₁ − √x/S₂`.
-/

/-- **Sensitivity lemma.**  The logarithmic sensitivity of the participation
ratio to a member equals that member's share of the sum minus its share of
the square-root sum. -/
theorem log_sensitivity {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    (x / Q x b c) *
      (1 / (S₂ x b c) ^ 2 - S₁ x b c / ((S₂ x b c) ^ 3 * Real.sqrt x))
      = x / S₁ x b c - Real.sqrt x / S₂ x b c := by
  have h1 : 0 < S₁ x b c := S₁_pos hx hb hc
  have h2 : 0 < S₂ x b c := S₂_pos hx hb hc
  have hs : (0:ℝ) < Real.sqrt x := Real.sqrt_pos.mpr hx
  have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
  unfold Q
  field_simp
  nlinarith [hsq, sq_nonneg (S₂ x b c), h1.le, h2.le, hs.le]

/-- The sensitivity vanishes exactly when the member's share of `S₁` equals its
share of `S₂`; near that point the inverse gain diverges. -/
theorem sensitivity_zero_iff {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    x / S₁ x b c - Real.sqrt x / S₂ x b c = 0 ↔
      x * S₂ x b c = Real.sqrt x * S₁ x b c := by
  have h1 : (0:ℝ) < S₁ x b c := S₁_pos hx hb hc
  have h2 : (0:ℝ) < S₂ x b c := S₂_pos hx hb hc
  rw [sub_eq_zero, div_eq_div_iff (ne_of_gt h1) (ne_of_gt h2)]

/-- Cauchy–Schwarz for the triple: `S₂² ≤ 3 S₁`.  Equivalently `Q ≥ 1/3`. -/
theorem S₂_sq_le {a b c : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) :
    (S₂ a b c) ^ 2 ≤ 3 * S₁ a b c := by
  unfold S₁ S₂
  have hA := Real.sq_sqrt ha
  have hB := Real.sq_sqrt hb
  have hC := Real.sq_sqrt hc
  nlinarith [sq_nonneg (Real.sqrt a - Real.sqrt b),
             sq_nonneg (Real.sqrt b - Real.sqrt c),
             sq_nonneg (Real.sqrt a - Real.sqrt c), hA, hB, hC]

/-- **Small-member bound.**  Writing `s = √x / S₂` for a member's share of the
square-root sum, its share of the plain sum obeys `x/S₁ ≤ 3 s²`.  Hence the
logarithmic sensitivity is at most `s(3s − 1)`, which is negative for
`s < 1/3` and bounded by `s` in magnitude: the gain needed to move `Q`
through that member is at least `1/s`.  This is why a light member cannot be
predicted from a cone condition at any achievable precision. -/
theorem share_sq_bound {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    x / S₁ x b c ≤ 3 * (Real.sqrt x / S₂ x b c) ^ 2 := by
  have h1 : (0:ℝ) < S₁ x b c := S₁_pos hx hb hc
  have h2 : (0:ℝ) < S₂ x b c := S₂_pos hx hb hc
  have hcs := S₂_sq_le hx.le hb.le hc.le
  have hxx : Real.sqrt x ^ 2 = x := Real.sq_sqrt hx.le
  have h2s : (0:ℝ) < (S₂ x b c) ^ 2 := pow_pos h2 2
  rw [div_pow, hxx]
  have e : 3 * (x / (S₂ x b c) ^ 2) - x / S₁ x b c
      = x * (3 * S₁ x b c - (S₂ x b c) ^ 2) / (S₁ x b c * (S₂ x b c) ^ 2) := by
    field_simp
  have hnum : 0 ≤ x * (3 * S₁ x b c - (S₂ x b c) ^ 2) := by nlinarith [hcs, hx.le]
  have hden : (0:ℝ) < S₁ x b c * (S₂ x b c) ^ 2 := mul_pos h1 h2s
  have : 0 ≤ 3 * (x / (S₂ x b c) ^ 2) - x / S₁ x b c := by
    rw [e]; exact div_nonneg hnum hden.le
  linarith

/-- The sensitivity is bounded above by `s(3s − 1)` where `s` is the share. -/
theorem sensitivity_le {x b c : ℝ} (hx : 0 < x) (hb : 0 < b) (hc : 0 < c) :
    x / S₁ x b c - Real.sqrt x / S₂ x b c
      ≤ (Real.sqrt x / S₂ x b c) * (3 * (Real.sqrt x / S₂ x b c) - 1) := by
  have h := share_sq_bound hx hb hc
  nlinarith [h]

/-! ## Permutation symmetry

`Q` is symmetric, so the identity for the first slot gives the other two.
-/

theorem Q_comm₁₂ (a b c : ℝ) : Q a b c = Q b a c := by
  unfold Q S₁ S₂; ring_nf

theorem Q_comm₂₃ (a b c : ℝ) : Q a b c = Q a c b := by
  unfold Q S₁ S₂; ring_nf

theorem Q_comm₁₃ (a b c : ℝ) : Q a b c = Q c b a := by
  unfold Q S₁ S₂; ring_nf

end Sensitivity
