/-
The light-sector map: an iterated geometric ladder terminating at a threshold.

Companion to "One map, iterated: the light-fermion masses from a single scale".

The construction is one map applied repeatedly,

    M : x ↦ α² x,     α = √(3/2) − 1,

started at the charged-lepton pole sum μ⋆ and stopped at the pair-production
threshold 2mₑ.  This file certifies the ALGEBRAIC content of that description:
that the orbit is a geometric ladder, that consecutive rungs make each interior
rung the geometric mean of its neighbours, that the ladder is strictly
decreasing and injective, and that α is the unique positive root of the cone
condition (1+α)⁻² = 2/3 that fixes it.

WHAT IS NOT CERTIFIED.  No mass value, and nothing about renormalization-group
running.  The map is an arithmetic object here; whether the physical masses
sit on its orbit is the empirical claim of the companion paper and is not a
theorem.

Toolchain: leanprover/lean4 v4.31.0 with Mathlib.
-/
import Mathlib

noncomputable section
open Real
namespace LightMap

/-! ## The constant -/

/-- The ladder constant. -/
def α : ℝ := Real.sqrt (3/2) - 1

theorem α_pos : 0 < α := by
  unfold α
  have h : (1:ℝ) < Real.sqrt (3/2) := by
    have : (1:ℝ) = Real.sqrt 1 := (Real.sqrt_one).symm
    rw [this]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

theorem α_lt_one : α < 1 := by
  unfold α
  have h : Real.sqrt (3/2) < 2 := by
    have : Real.sqrt (3/2) < Real.sqrt 4 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    simpa [show (4:ℝ) = 2^2 by norm_num, Real.sqrt_sq] using this
  linarith

/-- The cone condition: `(1+α)⁻² = 2/3`, which is what fixes `α`. -/
theorem cone_condition : (1 + α) ^ 2 = 3/2 := by
  unfold α
  have h : Real.sqrt (3/2) ^ 2 = 3/2 := Real.sq_sqrt (by norm_num)
  have : (1 + (Real.sqrt (3/2) - 1)) = Real.sqrt (3/2) := by ring
  rw [this, h]

/-- `α` is the unique positive solution of the cone condition. -/
theorem α_unique {x : ℝ} (hx : 0 < x) (h : (1 + x) ^ 2 = 3/2) : x = α := by
  have hA : (1 + α) ^ 2 = 3/2 := cone_condition
  have hαp := α_pos
  have hz : (x - α) * (x + α + 2) = 0 := by nlinarith [h, hA]
  rcases mul_eq_zero.mp hz with h1 | h1
  · linarith
  · linarith

/-! ## The map and its orbit -/

/-- One step of the ladder. -/
def M (x : ℝ) : ℝ := α ^ 2 * x

/-- The `n`-th rung from a starting scale. -/
def rung (μ : ℝ) (n : ℕ) : ℝ := α ^ (2 * n) * μ

theorem rung_zero (μ : ℝ) : rung μ 0 = μ := by unfold rung; norm_num

theorem rung_succ (μ : ℝ) (n : ℕ) : rung μ (n + 1) = M (rung μ n) := by
  unfold rung M
  rw [show 2 * (n + 1) = 2 * n + 2 by ring, pow_add]
  ring

theorem rung_pos {μ : ℝ} (hμ : 0 < μ) (n : ℕ) : 0 < rung μ n := by
  unfold rung
  exact mul_pos (pow_pos α_pos _) hμ

/-- The ladder is strictly decreasing. -/
theorem α_sq_lt_one : α ^ 2 < 1 := by
  have h1 := α_pos
  have h2 := α_lt_one
  nlinarith

theorem rung_strictAnti {μ : ℝ} (hμ : 0 < μ) (n : ℕ) :
    rung μ (n + 1) < rung μ n := by
  unfold rung
  have hp : 0 < α ^ (2 * n) := pow_pos α_pos _
  have hsplit : α ^ (2 * (n+1)) = α ^ (2 * n) * α ^ 2 := by
    rw [show 2 * (n+1) = 2*n + 2 by ring, pow_add]
  have hlt : α ^ (2 * (n+1)) < α ^ (2 * n) := by
    rw [hsplit]
    nlinarith [α_sq_lt_one, hp]
  exact mul_lt_mul_of_pos_right hlt hμ

/-! ## The geometric-mean property

The defining feature of a geometric ladder: every interior rung is the
geometric mean of its two neighbours.  This is what makes the light sector a
*chain* rather than a set of unrelated relations.
-/

/-- **Each interior rung is the geometric mean of its neighbours.** -/
theorem rung_geometric_mean (μ : ℝ) (n : ℕ) :
    (rung μ (n + 1)) ^ 2 = rung μ n * rung μ (n + 2) := by
  unfold rung
  rw [show 2 * (n+1) = 2*n + 2 by ring, show 2 * (n+2) = 2*n + 4 by ring]
  rw [pow_add, pow_add]
  ring

/-- Consecutive rungs are in constant ratio `α²`, so the ladder is geometric. -/
theorem rung_ratio {μ : ℝ} (hμ : 0 < μ) (n : ℕ) :
    rung μ (n + 1) / rung μ n = α ^ 2 := by
  have hμ' : μ ≠ 0 := ne_of_gt hμ
  have hα : α ≠ 0 := ne_of_gt α_pos
  have hp : α ^ (2 * n) ≠ 0 := pow_ne_zero _ hα
  unfold rung
  rw [show 2 * (n+1) = 2*n + 2 by ring, pow_add]
  field_simp

/-- The ladder is strictly decreasing as a function of the rung index. -/
theorem rung_strictAnti_full {μ : ℝ} (hμ : 0 < μ) : StrictAnti (rung μ) :=
  strictAnti_nat_of_succ_lt (fun n => rung_strictAnti hμ n)

/-- Rung indices are therefore well defined: distinct indices give distinct
rungs, so a mass cannot sit on two rungs of the same ladder. -/
theorem rung_injective {μ : ℝ} (hμ : 0 < μ) : Function.Injective (rung μ) :=
  (rung_strictAnti_full hμ).injective

end LightMap
