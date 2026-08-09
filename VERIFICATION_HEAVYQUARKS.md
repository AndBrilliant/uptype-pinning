# Verification — HeavyQuarks.lean

Formal verification record for the algebraic propositions in the Descartes–Soddy
heavy-quark cascade paper (A. M. Brilliant, draft 2026).

- **Source:** `LeanMath/HeavyQuarks.lean`
- **Toolchain:** `leanprover/lean4:v4.31.0`, Mathlib `v4.31.0`
- **Reproduce:** `lake env lean LeanMath/AxiomCheck.lean` (axiom check) — see `LeanMath/AxiomCheck.lean`

Two independent checks are recorded here:

1. **Axiom check** — `#print axioms` on every theorem. A proof is trusted iff its
   axiom set is a subset of `{propext, Classical.choice, Quot.sound}` (the standard
   classical-Mathlib footprint) and contains no `sorryAx`.
2. **Source-pattern scan** — ripgrep sweep for proof-bypassing constructs
   (`sorry`, `admit`, `stop`, `sorryAx`, `native_decide`, bare `axiom`, `unsafe`,
   `implemented_by`, `@[extern]`, `opaque`, `set_option`).

Both were run on 2026-07-17. Every theorem passes.

## Axiom sweep (15 theorems)

Every theorem depends on exactly `[propext, Classical.choice, Quot.sound]` and nothing
else — no `sorryAx`, no custom axioms.

| # | Theorem | Group | Axioms | Result |
|---|---------|-------|--------|--------|
| 1 | `alphaK_sq` | Supporting identity | propext, Classical.choice, Quot.sound | ✅ pass |
| 2 | `alphaK_add_one_sq` | Supporting identity | propext, Classical.choice, Quot.sound | ✅ pass |
| 3 | `two_alphaK` | Supporting identity | propext, Classical.choice, Quot.sound | ✅ pass |
| 4 | `three_div_alphaK` | Supporting identity | propext, Classical.choice, Quot.sound | ✅ pass |
| 5 | `e1_eq` | Prop 1 | propext, Classical.choice, Quot.sound | ✅ pass |
| 6 | `p2_eq` | Prop 1 | propext, Classical.choice, Quot.sound | ✅ pass |
| 7 | `ratio_iff` | Prop 1 | propext, Classical.choice, Quot.sound | ✅ pass |
| 8 | `alpha_from_cone` | Prop 1 | propext, Classical.choice, Quot.sound | ✅ pass |
| 9 | `sample_pos_at_zero` | Prop 1 (positivity) | propext, Classical.choice, Quot.sound | ✅ pass |
| 10 | `admissible_nonempty` | Prop 1 (positivity) | propext, Classical.choice, Quot.sound | ✅ pass |
| 11 | `norm_scale_sq` | Prop 2 | propext, Classical.choice, Quot.sound | ✅ pass |
| 12 | `mb_from_involution` | Prop 2 | propext, Classical.choice, Quot.sound | ✅ pass |
| 13 | `mb_closed_form` | Prop 2 | propext, Classical.choice, Quot.sound | ✅ pass |
| 14 | `bridge` | Prop 2 | propext, Classical.choice, Quot.sound | ✅ pass |
| 15 | `geometric_mean` | Prop 2 | propext, Classical.choice, Quot.sound | ✅ pass |

> **Count history.** The original formalization had 13 theorems; the task list named
> 12 and flagged a 13th to confirm from source — that is **`norm_scale_sq`**
> (`G = (α+1)μ★`, i.e. `G² = (3/2)μ★²`), a Prop 2 supporting identity. Closing the
> positivity caveat (Task 3) added two more — `sample_pos_at_zero` and
> `admissible_nonempty` — bringing the total to **15**.
>
> The file also contains helper *lemmas* (`sqrt6_eq`, `sqrt_three_halves_sq`,
> `alphaK_pos`, `alphaK_ne_zero`, `sqrt2_lt_two`, and the six `cos/sin` phase lemmas)
> and the `Admissible` predicate definition; the lemmas are covered transitively by
> the axiom check above (any bad axiom in a helper would surface in every theorem that
> uses it).

## Source-pattern scan

`rg` sweep of `LeanMath/HeavyQuarks.lean` — **zero** matches in every category:

| Pattern | Matches |
|---------|---------|
| `sorry` / `admit` / `stop` | 0 |
| `sorryAx` / `native_decide` | 0 |
| bare `axiom` declarations | 0 |
| `unsafe` / `implemented_by` / `@[extern]` / `opaque` | 0 |
| `set_option` (proof-bypass flags) | 0 |

## Positivity of the physical domain (formerly the standing caveat — now closed)

`ratio_iff` and `alpha_from_cone` are algebraic identities that hold for *every* δ;
positivity is not needed for them to be true. The physical *reading* √m_a = Z(φ_a)
does require each sample `Z(φ_a) ≥ 0`, and with `A = √2·c₀` the sample
`c₀(1 + √2·cos(φ+δ))` can dip to `c₀(1 − √2) < 0` at some phases — so the physically
meaningful configurations form a proper subset of δ-space.

That subset — the **admissible domain** the observed spectra occupy — is now formalized
and shown realizable rather than assumed:

- `Admissible c0 δ := ∀ a : Fin 3, 0 < sample c0 δ a` — the domain predicate.
- `sample_pos_at_zero` — at δ = 0 all three samples are strictly positive.
- `admissible_nonempty` — for any `c₀ > 0`, `δ = 0 ∈ Admissible`, so the domain is
  nonempty.

This closes the last asterisk carried through prover → Lean → paper. It does not alter
any Proposition 1 or 2 result (those are δ-general); it establishes that the physical
reading is not vacuous. Full positivity across the *entire* observed δ-interval (as
opposed to a witnessed point) remains a possible future strengthening but is not needed
for any claim.
