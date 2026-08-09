/-
Formal verification of the algebraic propositions in
"Electroweak pinning of the up-type participation ratio near 8/9"
(A. M. Brilliant, 2026).

Verified claims (paper reference in brackets):

  1. [Eq. (1)]  The participation ratio Q[v] = (Σ v_i)/(Σ √v_i)² of a positive
     triple satisfies 1/3 ≤ Q ≤ 1.

  2. [Prop. 2, App. A]  Homogeneity protection: Q is degree-zero homogeneous —
     a common multiplicative factor Z on all three members leaves Q unchanged.
     The protection is *power-blind*: the generalized ratio
     (Σ v^p)/(Σ v^{p/2})² sheds a common factor for every real exponent p.
     Corollary: under flavour-blind evolution v_i(μ) = Z(μ) v_i(μ₀) — pure QCD
     inside a fixed-n_f window — Q cannot run.

  3. [Lemma 1]  For the cosine parametrization √v_j = A[1 + √2 k cos(δ + 2πj/3)],
     Q = (1 + k²)/3 for *every* phase δ.

  4. [Lemma 2]  k² = 5/3 ⟺ Q = 8/9, with √(5/3) bracketed numerically.

  5. [Eq. (13)]  The Z₃ blind weight: deleting every third harmonic from the
     spectral weight Σ 1/n² removes exactly 1/9 of it, leaving 8/9. Proved
     without evaluating ζ(2) — only the 1/9 scaling of the silent sublattice
     and summability are used.

  6. [Table I, Eq. (2)]  Certified interval evaluation of the tabulated
     observable: 7.9885 ≤ 9Q_U(M_Z) ≤ 7.9887 and 8.0010 ≤ 9Q_U(3 TeV) ≤ 8.0012,
     from the common-scale Yukawa couplings of Table I. Corollary: the tabulated
     endpoints bracket 8, so 9Q_U crosses 8 strictly between M_Z and 3 TeV.

NOTE ON SCOPE. These are the paper's *algebraic* and *arithmetic* claims. The
renormalization-group drift law Eq. (9) is a one-loop field-theory result, not an
algebraic identity, and is deliberately NOT formalized here — no Lean statement
in this file should be read as certifying it. Likewise item 6 certifies the
arithmetic of the ratio given the tabulated inputs; it says nothing about the
inputs themselves.

All theorems use only the standard classical Mathlib axioms
{propext, Classical.choice, Quot.sound}. No sorry, native_decide, or
proof-bypassing constructs are used. Reproduce with:
    lake env lean LeanMath/AxiomCheckUpType.lean
    lake build
-/
import Mathlib
import LeanMath.HeavyQuarks

noncomputable section

open Real Finset

namespace UpType

/-! ## The participation ratio -/

/-- The participation ratio of a triple, Eq. (1):
`Q[v] = (v₁+v₂+v₃) / (√v₁+√v₂+√v₃)²`. -/
def Q (v : Fin 3 → ℝ) : ℝ :=
  (∑ i, v i) / (∑ i, Real.sqrt (v i)) ^ 2

/-- The generalized (power-`p`) participation ratio
`Q_p[v] = (Σ v^p) / (Σ v^{p/2})²`, using real exponentiation.
`p = 1` recovers `Q` on positive triples (`Q_rpow_one` below). -/
def Qp (p : ℝ) (v : Fin 3 → ℝ) : ℝ :=
  (∑ i, (v i) ^ p) / (∑ i, (v i) ^ (p / 2)) ^ 2

/-! ### Eq. (1): the range of Q -/

/-- Eq. (1): a positive triple has `1/3 ≤ Q ≤ 1`. The lower bound is the
Cauchy–Schwarz/power-mean edge (attained at full degeneracy); the upper bound is
the hierarchical edge (approached when one member dominates). -/
theorem Q_bounds (v : Fin 3 → ℝ) (hv : ∀ i, 0 < v i) :
    1 / 3 ≤ Q v ∧ Q v ≤ 1 := by
  set a := Real.sqrt (v 0) with ha
  set b := Real.sqrt (v 1) with hb
  set c := Real.sqrt (v 2) with hc
  have hap : 0 < a := Real.sqrt_pos.mpr (hv 0)
  have hbp : 0 < b := Real.sqrt_pos.mpr (hv 1)
  have hcp : 0 < c := Real.sqrt_pos.mpr (hv 2)
  have hva : v 0 = a ^ 2 := (Real.sq_sqrt (hv 0).le).symm
  have hvb : v 1 = b ^ 2 := (Real.sq_sqrt (hv 1).le).symm
  have hvc : v 2 = c ^ 2 := (Real.sq_sqrt (hv 2).le).symm
  have hnum : ∑ i, v i = a ^ 2 + b ^ 2 + c ^ 2 := by
    simp only [Fin.sum_univ_three]; rw [hva, hvb, hvc]
  have hden : ∑ i, Real.sqrt (v i) = a + b + c := by
    simp only [Fin.sum_univ_three, ha, hb, hc]
  have hQ : Q v = (a ^ 2 + b ^ 2 + c ^ 2) / (a + b + c) ^ 2 := by
    unfold Q; rw [hnum, hden]
  have hpos : (0 : ℝ) < (a + b + c) ^ 2 := by positivity
  rw [hQ]
  constructor
  · rw [le_div_iff₀ hpos]
    nlinarith [sq_nonneg (a - b), sq_nonneg (b - c), sq_nonneg (a - c)]
  · rw [div_le_one hpos]
    nlinarith [mul_pos hap hbp, mul_pos hbp hcp, mul_pos hap hcp]

/-! ## Proposition 2 (homogeneity), and its power-blind form

Appendix A, Proposition 2. If all members of a triple evolve with a common
factor, `v_i(μ) = Z(μ) v_i(μ₀)`, then `Q` is unchanged identically. -/

/-- **Proposition 2, power-blind form.** For any real exponent `p` and any
positive common factor `Z`, the generalized ratio `Q_p` is invariant. The common
factor `Z^p` cancels between numerator and denominator; no positivity of the
`v_i` and no nonvanishing of the denominator sum is needed. -/
theorem Qp_homogeneous (p Z : ℝ) (hZ : 0 < Z) (v : Fin 3 → ℝ) (hv : ∀ i, 0 ≤ v i) :
    Qp p (fun i => Z * v i) = Qp p v := by
  have hnum : ∑ i, (Z * v i) ^ p = Z ^ p * ∑ i, (v i) ^ p := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    exact Real.mul_rpow hZ.le (hv i)
  have hden : ∑ i, (Z * v i) ^ (p / 2) = Z ^ (p / 2) * ∑ i, (v i) ^ (p / 2) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    exact Real.mul_rpow hZ.le (hv i)
  have hZp : Z ^ p ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos hZ p)
  have hsq : (Z ^ (p / 2)) ^ 2 = Z ^ p := by
    rw [← Real.rpow_natCast (Z ^ (p / 2)) 2, ← Real.rpow_mul hZ.le]
    norm_num
  unfold Qp
  rw [hnum, hden, mul_pow, hsq]
  exact mul_div_mul_left _ _ hZp

/-- **Proposition 2** in the paper's stated form: `Q` itself is degree-zero
homogeneous. A common factor `Z > 0` on all three members leaves `Q` unchanged. -/
theorem Q_homogeneous (Z : ℝ) (hZ : 0 < Z) (v : Fin 3 → ℝ) (_hv : ∀ i, 0 ≤ v i) :
    Q (fun i => Z * v i) = Q v := by
  have hnum : ∑ i, Z * v i = Z * ∑ i, v i := by rw [Finset.mul_sum]
  have hden : ∑ i, Real.sqrt (Z * v i) = Real.sqrt Z * ∑ i, Real.sqrt (v i) := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    exact Real.sqrt_mul hZ.le (v i)
  have hZne : Z ≠ 0 := ne_of_gt hZ
  have hsq : Real.sqrt Z ^ 2 = Z := Real.sq_sqrt hZ.le
  unfold Q
  rw [hnum, hden, mul_pow, hsq]
  exact mul_div_mul_left _ _ hZne

/-- **Corollary (App. A).** Under flavour-blind evolution — every member carrying
the same factor `Z(μ)`, as in pure QCD inside a fixed-`n_f` window with all three
quarks in the same scheme at the same scale — `Q` cannot run: its value at `μ`
equals its value at `μ₀`, identically in `Z`. Any apparent running of `Q` in such
a setting is therefore manufactured by crossing definitions, not physical. -/
theorem Q_cannot_run (v₀ : Fin 3 → ℝ) (hv : ∀ i, 0 ≤ v₀ i)
    (Z : ℝ → ℝ) (hZ : ∀ μ, 0 < Z μ) (μ μ₀ : ℝ) :
    Q (fun i => Z μ * v₀ i) = Q (fun i => Z μ₀ * v₀ i) := by
  rw [Q_homogeneous (Z μ) (hZ μ) v₀ hv, Q_homogeneous (Z μ₀) (hZ μ₀) v₀ hv]

/-! ## Lemma 1: the cosine parametrization

`√v_j = A [1 + √2 k cos(δ + 2πj/3)]`. The three family phases are written in the
same explicit convention as `HeavyQuarks` (0, 2π/3, 4π/3), and the sums are
inherited from the cone lemma proved there. -/

/-- The cosine-parametrized root triple `√v_j = A[1 + √2 k cos(δ + 2πj/3)]`. -/
def coneRoot (A k δ : ℝ) : Fin 3 → ℝ
  | 0 => A * (1 + Real.sqrt 2 * k * Real.cos δ)
  | 1 => A * (1 + Real.sqrt 2 * k * Real.cos (2 * π / 3 + δ))
  | 2 => A * (1 + Real.sqrt 2 * k * Real.cos (4 * π / 3 + δ))

/-- The triple itself: `v_j = (√v_j)²`. -/
def coneTriple (A k δ : ℝ) : Fin 3 → ℝ := fun j => (coneRoot A k δ j) ^ 2

/-- Sum of the roots: `Σ √v_j = 3A`, for every phase `δ`. (Phase orthogonality:
the `cos` terms cancel.) -/
lemma coneRoot_sum (A k δ : ℝ) : ∑ j, coneRoot A k δ j = 3 * A := by
  have h : HeavyQuarks.e1 A (A * (Real.sqrt 2 * k)) δ = 3 * A :=
    HeavyQuarks.e1_eq A (A * (Real.sqrt 2 * k)) δ
  simp only [Fin.sum_univ_three, coneRoot]
  rw [← h]
  unfold HeavyQuarks.e1
  ring

/-- Sum of the triple: `Σ v_j = 3A²(1 + k²)`, for every phase `δ`. -/
lemma coneTriple_sum (A k δ : ℝ) :
    ∑ j, coneTriple A k δ j = 3 * A ^ 2 * (1 + k ^ 2) := by
  have h : HeavyQuarks.p2 A (A * (Real.sqrt 2 * k)) δ
      = 3 * A ^ 2 + 3 / 2 * (A * (Real.sqrt 2 * k)) ^ 2 :=
    HeavyQuarks.p2_eq A (A * (Real.sqrt 2 * k)) δ
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  simp only [Fin.sum_univ_three, coneTriple, coneRoot]
  have hexp : (A * (1 + Real.sqrt 2 * k * Real.cos δ)) ^ 2
      + (A * (1 + Real.sqrt 2 * k * Real.cos (2 * π / 3 + δ))) ^ 2
      + (A * (1 + Real.sqrt 2 * k * Real.cos (4 * π / 3 + δ))) ^ 2
      = HeavyQuarks.p2 A (A * (Real.sqrt 2 * k)) δ := by
    unfold HeavyQuarks.p2; ring
  rw [hexp, h]
  linear_combination (3 / 2 * A ^ 2 * k ^ 2) * h2

/-- The roots are genuinely the square roots of the triple, provided the cone
samples are nonnegative (the admissible domain of `HeavyQuarks`). -/
lemma sqrt_coneTriple (A k δ : ℝ) (hnn : ∀ j, 0 ≤ coneRoot A k δ j) (j : Fin 3) :
    Real.sqrt (coneTriple A k δ j) = coneRoot A k δ j :=
  Real.sqrt_sq (hnn j)

/-- **Lemma 1.** For the cosine parametrization `√v_j = A[1 + √2 k cos(δ+2πj/3)]`
with `A ≠ 0` and nonnegative samples, `Q = (1 + k²)/3` — *for any phase `δ`*.
The phase drops out entirely; only the cone opening `k` survives. -/
theorem lemma1 (A k δ : ℝ) (hA : A ≠ 0) (hnn : ∀ j, 0 ≤ coneRoot A k δ j) :
    Q (coneTriple A k δ) = (1 + k ^ 2) / 3 := by
  have hden : ∑ j, Real.sqrt (coneTriple A k δ j) = 3 * A := by
    rw [Finset.sum_congr rfl (fun j _ => sqrt_coneTriple A k δ hnn j)]
    exact coneRoot_sum A k δ
  unfold Q
  rw [coneTriple_sum, hden]
  have h9 : (3 * A) ^ 2 = 9 * A ^ 2 := by ring
  rw [h9]
  have hA2 : (A : ℝ) ^ 2 ≠ 0 := pow_ne_zero 2 hA
  field_simp
  ring

/-! ## Lemma 2: the 8/9 condition -/

/-- **Lemma 2.** `k² = 5/3 ⟺ Q = 8/9`, in the cone parametrization. -/
theorem lemma2 (A k δ : ℝ) (hA : A ≠ 0) (hnn : ∀ j, 0 ≤ coneRoot A k δ j) :
    k ^ 2 = 5 / 3 ↔ Q (coneTriple A k δ) = 8 / 9 := by
  rw [lemma1 A k δ hA hnn]
  constructor
  · intro h; rw [h]; norm_num
  · intro h; linarith

/-- **Lemma 2, abstract form.** Stripped of the parametrization: the shape
condition `(1+k²)/3 = 8/9` is exactly `k² = 5/3`. -/
theorem lemma2_abstract (k : ℝ) : (1 + k ^ 2) / 3 = 8 / 9 ↔ k ^ 2 = 5 / 3 := by
  constructor <;> intro h <;> linarith

/-- The cone opening at `Q = 8/9`: `√(5/3) = 1.2909…`, the value the paper
compares against the fitted `k_U = 1.289 ± 0.002`. -/
theorem k_at_eight_ninths_bracket :
    1.2909 ≤ Real.sqrt (5 / 3) ∧ Real.sqrt (5 / 3) ≤ 1.2910 := by
  have hnn : (0 : ℝ) ≤ 5 / 3 := by norm_num
  have hsq : Real.sqrt (5 / 3) ^ 2 = 5 / 3 := Real.sq_sqrt hnn
  have hpos : 0 ≤ Real.sqrt (5 / 3) := Real.sqrt_nonneg _
  constructor
  · nlinarith [hsq, hpos]
  · nlinarith [hsq, hpos]

/-! ## Eq. (13): the Z₃ blind weight

The harmonic content of the dressing operator is subject to a `Z₃` selection under
which every third mode is silent. The surviving spectral weight is

    Σ_{3∤n} 1/n²  /  Σ_{n≥1} 1/n²  =  1 − 1/9  =  8/9.

The proof below does **not** evaluate ζ(2). It uses only (i) summability of
`1/n²`, and (ii) the exact `1/9` self-similarity of the silent sublattice
`{3,6,9,…}`, which is what actually produces the `1/9`. -/

/-- Harmonic weight `w n = 1/n²`. Lean's `1/0 = 0` convention makes `w 0 = 0`,
which is exactly what we want: the `n = 0` slot carries no weight. -/
def w (n : ℕ) : ℝ := 1 / (n : ℝ) ^ 2

lemma w_zero : w 0 = 0 := by simp [w]

lemma w_one : w 1 = 1 := by simp [w]

lemma w_nonneg (n : ℕ) : 0 ≤ w n := by
  unfold w; positivity

lemma w_summable : Summable w := by
  unfold w
  exact summable_one_div_nat_pow.mpr (by norm_num)

/-- Self-similarity of the silent sublattice: `w(3m) = (1/9) w(m)`, including at
`m = 0` where both sides vanish. -/
lemma w_three_mul (m : ℕ) : w (3 * m) = (1 / 9) * w m := by
  rcases Nat.eq_zero_or_pos m with hm | hm
  · subst hm; simp [w]
  · have hm0 : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hm.ne'
    unfold w
    push_cast
    field_simp
    ring

/-- The total spectral weight is positive (we never need its value, only that it
is nonzero, so no ζ(2) evaluation enters). -/
lemma tsum_w_pos : 0 < ∑' n, w n := by
  refine lt_of_lt_of_le ?_ (w_summable.sum_le_tsum {1} (fun i _ => w_nonneg i))
  simp [w_one]

/-- The silent modes carry exactly `1/9` of the total weight. This is the entire
content of the `8/9`: the `Z₃`-silent sublattice is a scaled copy of the whole,
with scale factor `3⁻² = 1/9`. -/
theorem silent_weight : ∑' m : ℕ, w (3 * m) = (1 / 9) * ∑' n, w n := by
  calc ∑' m : ℕ, w (3 * m) = ∑' m : ℕ, (1 / 9 : ℝ) * w m := by
        exact tsum_congr w_three_mul
    _ = (1 / 9) * ∑' n, w n := tsum_mul_left

/-- The multiplication-by-three equivalence `ℕ ≃ {n // 3 ∣ n}`, identifying the
silent sublattice with a scaled copy of the full mode set. -/
def mulThree : ℕ ≃ {n : ℕ // 3 ∣ n} where
  toFun m := ⟨3 * m, Dvd.intro m rfl⟩
  invFun n := n.1 / 3
  left_inv m := by simp
  right_inv := by
    rintro ⟨n, k, rfl⟩
    simp

/-- The silent sum, reindexed onto the subtype of multiples of three. -/
lemma tsum_silent_subtype : ∑' n : {n : ℕ // 3 ∣ n}, w n = (1 / 9) * ∑' n, w n := by
  rw [← silent_weight]
  exact (Equiv.tsum_eq mulThree (fun n : {n : ℕ // 3 ∣ n} => w n)).symm

/-- **Eq. (13).** The `Z₃` blind weight: the modes surviving the selection (those
whose index is *not* a multiple of three) carry exactly `8/9` of the total
spectral weight. -/
theorem blind_weight :
    (∑' n : {n : ℕ // ¬ (3 ∣ n)}, w n) / (∑' n, w n) = 8 / 9 := by
  have hset : {n : ℕ | 3 ∣ n}ᶜ = {n : ℕ | ¬ (3 ∣ n)} := rfl
  have hsplit : (∑' n : {n : ℕ // 3 ∣ n}, w n)
      + (∑' n : {n : ℕ // ¬ (3 ∣ n)}, w n) = ∑' n, w n := by
    have h := (w_summable.subtype {n : ℕ | 3 ∣ n}).tsum_add_tsum_compl
      (w_summable.subtype {n : ℕ | 3 ∣ n}ᶜ)
    exact h
  have hsilent := tsum_silent_subtype
  have htot : (0 : ℝ) < ∑' n, w n := tsum_w_pos
  have hsurv : (∑' n : {n : ℕ // ¬ (3 ∣ n)}, w n) = (8 / 9) * ∑' n, w n := by
    have := hsplit
    rw [hsilent] at this
    linarith
  rw [hsurv]
  field_simp

/-! ## Certified evaluation of the tabulated observable

Table I of the paper gives common-scale up-type Yukawa couplings. What follows is
a rigorous interval evaluation of `9Q_U` from those inputs: rational brackets on
each `√y_i` are verified by squaring, propagated through the ratio, and the
resulting bracket on `9Q_U` is exhibited.

This certifies the *arithmetic* of the ratio given the inputs. It makes no claim
about the inputs themselves, whose uncertainties are the paper's Appendix B. -/

/-- Interval propagation: rational brackets on the roots give a bracket on `Q`.
If `lo_i ≤ √v_i ≤ hi_i` (certified by `lo_i² ≤ v_i ≤ hi_i²` with `lo_i, hi_i ≥ 0`)
then `Q` is squeezed between the two rational quotients. -/
theorem Q_interval (v lo hi : Fin 3 → ℝ)
    (hlo : ∀ i, 0 ≤ lo i) (hhi : ∀ i, 0 ≤ hi i)
    (h1 : ∀ i, lo i ^ 2 ≤ v i) (h2 : ∀ i, v i ≤ hi i ^ 2)
    (hSlo : 0 < ∑ i, lo i) (hnum : 0 ≤ ∑ i, v i) :
    (∑ i, v i) / (∑ i, hi i) ^ 2 ≤ Q v ∧ Q v ≤ (∑ i, v i) / (∑ i, lo i) ^ 2 := by
  have hroot_lo : ∀ i, lo i ≤ Real.sqrt (v i) := by
    intro i
    calc lo i = Real.sqrt (lo i ^ 2) := (Real.sqrt_sq (hlo i)).symm
      _ ≤ Real.sqrt (v i) := Real.sqrt_le_sqrt (h1 i)
  have hroot_hi : ∀ i, Real.sqrt (v i) ≤ hi i := by
    intro i
    calc Real.sqrt (v i) ≤ Real.sqrt (hi i ^ 2) := Real.sqrt_le_sqrt (h2 i)
      _ = hi i := Real.sqrt_sq (hhi i)
  have hsum_lo : (∑ i, lo i) ≤ ∑ i, Real.sqrt (v i) :=
    Finset.sum_le_sum (fun i _ => hroot_lo i)
  have hsum_hi : (∑ i, Real.sqrt (v i)) ≤ ∑ i, hi i :=
    Finset.sum_le_sum (fun i _ => hroot_hi i)
  have hSr : 0 < ∑ i, Real.sqrt (v i) := lt_of_lt_of_le hSlo hsum_lo
  have hShi : 0 < ∑ i, hi i := lt_of_lt_of_le hSr hsum_hi
  have hsq_lo : (∑ i, lo i) ^ 2 ≤ (∑ i, Real.sqrt (v i)) ^ 2 :=
    pow_le_pow_left₀ hSlo.le hsum_lo 2
  have hsq_hi : (∑ i, Real.sqrt (v i)) ^ 2 ≤ (∑ i, hi i) ^ 2 :=
    pow_le_pow_left₀ hSr.le hsum_hi 2
  unfold Q
  constructor
  · exact div_le_div_of_nonneg_left hnum (by positivity) hsq_hi
  · exact div_le_div_of_nonneg_left hnum (by positivity) hsq_lo

/-! ### Table I, row 1: μ = M_Z -/

/-- Tabulated up-type Yukawa couplings at `μ = M_Z` (Table I). -/
def yMZ : Fin 3 → ℝ
  | 0 => 0.00000704
  | 1 => 0.00356
  | 2 => 0.967

/-- **Table I / Eq. (2), certified.** `9Q_U(M_Z) = 7.9886` to the quoted four
decimals: the ratio is bracketed in `[7.9885, 7.9887]`. -/
theorem nineQ_at_MZ : 7.9885 ≤ 9 * Q yMZ ∧ 9 * Q yMZ ≤ 7.9887 := by
  have h := Q_interval yMZ
    (fun i => match i with | 0 => 0.002653 | 1 => 0.059665 | 2 => 0.983361)
    (fun i => match i with | 0 => 0.002654 | 1 => 0.059666 | 2 => 0.983362)
    (by intro i; fin_cases i <;> norm_num)
    (by intro i; fin_cases i <;> norm_num)
    (by intro i; fin_cases i <;> simp [yMZ] <;> norm_num)
    (by intro i; fin_cases i <;> simp [yMZ] <;> norm_num)
    (by simp [Fin.sum_univ_three]; norm_num)
    (by simp [yMZ, Fin.sum_univ_three]; norm_num)
  obtain ⟨hL, hU⟩ := h
  simp only [yMZ, Fin.sum_univ_three] at hL hU
  norm_num at hL hU
  constructor <;> linarith

/-! ### Table I, row 3: μ = 3 TeV -/

/-- Tabulated up-type Yukawa couplings at `μ = 3` TeV (Table I). -/
def y3TeV : Fin 3 → ℝ
  | 0 => 0.00000584
  | 1 => 0.00295
  | 2 => 0.8242

/-- **Table I, certified.** `9Q_U(3 TeV) = 8.0011` to the quoted four decimals:
the ratio is bracketed in `[8.0010, 8.0012]`. -/
theorem nineQ_at_3TeV : 8.0010 ≤ 9 * Q y3TeV ∧ 9 * Q y3TeV ≤ 8.0012 := by
  have h := Q_interval y3TeV
    (fun i => match i with | 0 => 0.0024166 | 1 => 0.0543139 | 2 => 0.907854)
    (fun i => match i with | 0 => 0.0024167 | 1 => 0.0543140 | 2 => 0.907855)
    (by intro i; fin_cases i <;> norm_num)
    (by intro i; fin_cases i <;> norm_num)
    (by intro i; fin_cases i <;> simp [y3TeV] <;> norm_num)
    (by intro i; fin_cases i <;> simp [y3TeV] <;> norm_num)
    (by simp [Fin.sum_univ_three]; norm_num)
    (by simp [y3TeV, Fin.sum_univ_three]; norm_num)
  obtain ⟨hL, hU⟩ := h
  simp only [y3TeV, Fin.sum_univ_three] at hL hU
  norm_num at hL hU
  constructor <;> linarith

/-- **The crossing is bracketed.** The tabulated endpoints straddle `8`:
`9Q_U(M_Z) < 8 < 9Q_U(3 TeV)`. This certifies that a crossing scale `μ_{8/9}`
exists strictly between `M_Z` and `3` TeV for any continuous interpolation of the
tabulated values — the paper's `μ_{8/9} ≈ 2–3` TeV. It does **not** certify the
location of the crossing, which depends on the interpolation and is reported in
the paper as an output, not a prediction. -/
theorem crossing_bracketed : 9 * Q yMZ < 8 ∧ 8 < 9 * Q y3TeV := by
  obtain ⟨_, hU⟩ := nineQ_at_MZ
  obtain ⟨hL, _⟩ := nineQ_at_3TeV
  constructor
  · linarith
  · linarith

/-- The pinning statement of Sec. III: both tabulated endpoints lie within
`0.15%` of `8`. -/
theorem pinning_within_0_15_percent :
    |9 * Q yMZ - 8| ≤ 0.0015 * 8 ∧ |9 * Q y3TeV - 8| ≤ 0.0015 * 8 := by
  obtain ⟨hL1, hU1⟩ := nineQ_at_MZ
  obtain ⟨hL2, hU2⟩ := nineQ_at_3TeV
  constructor
  · rw [abs_le]; constructor <;> linarith
  · rw [abs_le]; constructor <;> linarith

/-! ## C. IVT CROSSING -/

/-- **IVT crossing, generic form.** If `f` is continuous on `[a,b]` and
`f a < 8 < f b`, there exists `μ ∈ (a,b)` with `f μ = 8`. -/
theorem crossing_exists_of_continuous {f : ℝ → ℝ} {a b : ℝ} (hab : a ≤ b)
    (hf : ContinuousOn f (Set.Icc a b)) (hfa : f a < 8) (hfb : 8 < f b) :
    ∃ μ ∈ Set.Ioo a b, f μ = 8 := by
  have h8 : (8 : ℝ) ∈ Set.Ioo (f a) (f b) := by
    constructor <;> linarith
  have h := intermediate_value_Ioo hab hf h8
  simpa using h

/-- **Crossing certified (continuity assumed).** Given the tabulated straddle
and a continuous RG trajectory, there exists `μ ∈ (M_Z, 3 TeV)` with `9Q_U(μ)=8`.
Continuity of the SM RG trajectory is an explicit hypothesis — the ODE is not
formalized. -/
theorem crossing_certified {v : ℝ → Fin 3 → ℝ}
    (h_cont : ContinuousOn (fun μ => 9 * Q (v μ)) (Set.Icc (91 : ℝ) 3000))
    (h_mz : 9 * Q (v 91) = 9 * Q yMZ)
    (h_3tev : 9 * Q (v 3000) = 9 * Q y3TeV) :
    ∃ μ ∈ Set.Ioo (91 : ℝ) 3000, 9 * Q (v μ) = 8 := by
  obtain ⟨hMZ, h3TeV⟩ := crossing_bracketed
  rw [← h_mz] at hMZ
  rw [← h_3tev] at h3TeV
  have h91_3000 : (91 : ℝ) ≤ 3000 := by norm_num
  exact crossing_exists_of_continuous h91_3000 h_cont hMZ h3TeV

/-! ## D. EXACT ADMISSIBLE DOMAIN -/

/-- `δ_max(k) = arccos(-1/(√2·k)) - 2π/3`. -/
def delta_max (k : ℝ) : ℝ := Real.arccos (-1 / (Real.sqrt 2 * k)) - 2 * π / 3

/-- `admissible_fraction(k) = 3·δ_max/π`. -/
def admissible_fraction (k : ℝ) : ℝ := 3 * delta_max k / π

/-! ### GATE L1 — admissible-domain numerics -/

/-- `arccos(-1/√2) = 3π/4`. -/
lemma arccos_neg_one_div_sqrt_two : Real.arccos (-1 / Real.sqrt 2) = 3 * π / 4 := by
  have h_cos : cos (3 * π / 4) = -1 / Real.sqrt 2 := by
    calc
      cos (3 * π / 4) = cos (π - π / 4) := by ring
      _ = -cos (π / 4) := by rw [Real.cos_pi_sub]
      _ = -(Real.sqrt 2 / 2) := by rw [Real.cos_pi_div_four]
      _ = -1 / Real.sqrt 2 := by
        rw [show (Real.sqrt 2 / 2) = (Real.sqrt 2 / (Real.sqrt 2 ^ 2)) by
          rw [Real.sq_sqrt (by norm_num : 0 ≤ (2 : ℝ))]]
        field_simp [show Real.sqrt 2 ≠ 0 from by positivity]
  have h_range0 : 0 ≤ 3 * π / 4 := by nlinarith [pi_pos]
  have h_range1 : 3 * π / 4 ≤ π := by nlinarith [pi_pos]
  rw [← h_cos, Real.arccos_cos h_range0 h_range1]

/-- **Gate L1, k=1:** `delta_max 1 = π/12` (exact, 15°). -/
theorem delta_max_one : delta_max 1 = π / 12 := by
  rw [delta_max]
  norm_num [arccos_neg_one_div_sqrt_two]
  ring

/-- **Gate L1, k=1:** `admissible_fraction 1 = 1/4` (exact). -/
theorem admissible_fraction_one : admissible_fraction 1 = 1 / 4 := by
  rw [admissible_fraction, delta_max_one]
  field_simp [show π ≠ 0 from by exact ne_of_gt pi_pos]
  ring

/-- **Gate L1, k=1:** lepton `δ = 2/9` < `δ_max = π/12`. -/
theorem lepton_delta_lt_delta_max : (2/9 : ℝ) < delta_max 1 := by
  rw [delta_max_one]
  have hpi : (8/3 : ℝ) < π := by linarith [Real.pi_gt_three]
  nlinarith

/-- **Gate L1, k=1:** ratio `(2/9) / δ_max = 8/(3π)`. -/
theorem lepton_delta_ratio : (2/9 : ℝ) / delta_max 1 = 8 / (3 * π) := by
  rw [delta_max_one]
  field_simp [show π ≠ 0 from by exact ne_of_gt pi_pos]
  ring

-- GATE L1, k²=5/3: numeric values (computed externally via Python)
-- delta_max(√(5/3)) = arccos(-√(3/10)) - 2π/3 ≈ 0.056041 rad = 3.2109°
-- admissible_fraction = 3·δ_max/π ≈ 0.05352
-- Spec target δ_max = 0.056043 rad (3.2110°) — discrep 2.0×10⁻⁶ rad

end UpType
