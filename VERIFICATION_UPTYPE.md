# Verification — UpTypeParticipation.lean

Formal verification record for the algebraic and arithmetic propositions in
"Electroweak pinning of the up-type participation ratio near 8/9"
(A. M. Brilliant, 2026).

- **Source:** `LeanMath/UpTypeParticipation.lean`
  (sha256 `80e411953951325499260500d6cfc4cb7b6af0fde12d83486dafe19ebf723595`)
- **Audit driver:** `LeanMath/AxiomCheckUpType.lean`
  (sha256 `b1ea5e3ace623fc7b3c9f76368eafd17ed6eb87898dc804cde2435b9653699af`)
- **Supporting library:** `LeanMath/HeavyQuarks.lean` — supplies the phase
  orthogonality results (`e1_eq`, `p2_eq`) that Lemma 1 reuses. Vendored here
  unmodified from the author's Lean development; its own verification record is
  `VERIFICATION_HEAVYQUARKS.md` and its axiom driver is
  `LeanMath/AxiomCheck.lean` (15 theorems, same standard axiom set).
- **Toolchain:** `leanprover/lean4:v4.31.0`, Mathlib `v4.31.0`, pinned exactly by
  the committed `lean-toolchain` and `lake-manifest.json` (Mathlib rev
  `fabf563a7c95`)
- **Reproduce:**
  ```bash
  lake exe cache get            # fetch Mathlib oleans
  lake build LeanMath           # compile the certificates
  lake env lean LeanMath/AxiomCheckUpType.lean   # print statements + axiom sweep
  ```

Two independent checks are recorded here, following the protocol of
`VERIFICATION_HEAVYQUARKS.md`:

1. **Axiom check** — `#print axioms` on every theorem. A proof is trusted iff its
   axiom set is a subset of `{propext, Classical.choice, Quot.sound}` (the
   standard classical-Mathlib footprint) and contains no `sorryAx`.
2. **Source-pattern scan** — ripgrep sweep for proof-bypassing constructs
   (`sorry`, `admit`, `stop`, `sorryAx`, `native_decide`, bare `axiom`, `unsafe`,
   `implemented_by`, `@[extern]`, `opaque`, `set_option`).

Both were run on 2026-08-07, and re-run on 2026-08-09 against this repository's
standalone package after the certificates were vendored in. Every theorem passes
in both runs: 21 declarations swept, 0 with a non-standard axiom set, 0 `sorryAx`.
The two sha256 digests above were re-checked at vendoring time and match, so the
certificate sources here are byte-identical to the audited originals.

The audit driver also `#check`s every statement, so the record shows *what* was
proved, not merely that something was — see "Statements as proved" below.

## Axiom sweep (21 declarations)

Every declaration depends on exactly `[propext, Classical.choice, Quot.sound]` and
nothing else — no `sorryAx`, no custom axioms.

| # | Declaration | Paper reference | Axioms | Result |
|---|-------------|-----------------|--------|--------|
| 1 | `Q_bounds` | Eq. (1), range `1/3 ≤ Q ≤ 1` | standard | ✅ pass |
| 2 | `Qp_homogeneous` | Prop. 2, power-blind form | standard | ✅ pass |
| 3 | `Q_homogeneous` | Prop. 2 (App. A) | standard | ✅ pass |
| 4 | `Q_cannot_run` | Prop. 2 corollary | standard | ✅ pass |
| 5 | `coneRoot_sum` | Lemma 1 support (Σ√v = 3A) | standard | ✅ pass |
| 6 | `coneTriple_sum` | Lemma 1 support (Σv = 3A²(1+k²)) | standard | ✅ pass |
| 7 | `lemma1` | **Lemma 1** | standard | ✅ pass |
| 8 | `lemma2` | **Lemma 2** | standard | ✅ pass |
| 9 | `lemma2_abstract` | Lemma 2, parametrization-free | standard | ✅ pass |
| 10 | `k_at_eight_ninths_bracket` | `√(5/3) = 1.2909…` vs fitted `k_U` | standard | ✅ pass |
| 11 | `w_summable` | Eq. (13) support | standard | ✅ pass |
| 12 | `w_three_mul` | Eq. (13) support (1/9 self-similarity) | standard | ✅ pass |
| 13 | `tsum_w_pos` | Eq. (13) support (denominator ≠ 0) | standard | ✅ pass |
| 14 | `silent_weight` | Eq. (13) core | standard | ✅ pass |
| 15 | `tsum_silent_subtype` | Eq. (13) reindexing | standard | ✅ pass |
| 16 | `blind_weight` | **Eq. (13)** | standard | ✅ pass |
| 17 | `Q_interval` | interval propagation lemma | standard | ✅ pass |
| 18 | `nineQ_at_MZ` | **Table I / Eq. (2)** | standard | ✅ pass |
| 19 | `nineQ_at_3TeV` | **Table I** | standard | ✅ pass |
| 20 | `crossing_bracketed` | Sec. V, existence of `μ_{8/9}` | standard | ✅ pass |
| 21 | `pinning_within_0_15_percent` | Sec. III, "within 0.15% of 8" | standard | ✅ pass |

## Statements as proved

Verbatim from `lake env lean LeanMath/AxiomCheckUpType.lean`:

```
Q_bounds : ∀ (v : Fin 3 → ℝ), (∀ (i : Fin 3), 0 < v i) → 1 / 3 ≤ Q v ∧ Q v ≤ 1

Qp_homogeneous : ∀ (p Z : ℝ), 0 < Z → ∀ (v : Fin 3 → ℝ), (∀ (i : Fin 3), 0 ≤ v i) →
  (Qp p fun i => Z * v i) = Qp p v

Q_homogeneous : ∀ (Z : ℝ), 0 < Z → ∀ (v : Fin 3 → ℝ), (∀ (i : Fin 3), 0 ≤ v i) →
  (Q fun i => Z * v i) = Q v

Q_cannot_run : ∀ (v₀ : Fin 3 → ℝ), (∀ (i : Fin 3), 0 ≤ v₀ i) →
  ∀ (Z : ℝ → ℝ), (∀ (μ : ℝ), 0 < Z μ) → ∀ (μ μ₀ : ℝ),
  (Q fun i => Z μ * v₀ i) = Q fun i => Z μ₀ * v₀ i

lemma1 : ∀ (A k δ : ℝ), A ≠ 0 → (∀ (j : Fin 3), 0 ≤ coneRoot A k δ j) →
  Q (coneTriple A k δ) = (1 + k ^ 2) / 3

lemma2 : ∀ (A k δ : ℝ), A ≠ 0 → (∀ (j : Fin 3), 0 ≤ coneRoot A k δ j) →
  (k ^ 2 = 5 / 3 ↔ Q (coneTriple A k δ) = 8 / 9)

lemma2_abstract : ∀ (k : ℝ), (1 + k ^ 2) / 3 = 8 / 9 ↔ k ^ 2 = 5 / 3

k_at_eight_ninths_bracket : 1.2909 ≤ √(5 / 3) ∧ √(5 / 3) ≤ 1.2910

silent_weight : ∑' (m : ℕ), w (3 * m) = 1 / 9 * ∑' (n : ℕ), w n

blind_weight : (∑' (n : { n // ¬3 ∣ n }), w ↑n) / ∑' (n : ℕ), w n = 8 / 9

Q_interval : ∀ (v lo hi : Fin 3 → ℝ), (∀ (i : Fin 3), 0 ≤ lo i) → (∀ (i : Fin 3), 0 ≤ hi i) →
  (∀ (i : Fin 3), lo i ^ 2 ≤ v i) → (∀ (i : Fin 3), v i ≤ hi i ^ 2) →
  0 < ∑ i, lo i → 0 ≤ ∑ i, v i →
  (∑ i, v i) / (∑ i, hi i) ^ 2 ≤ Q v ∧ Q v ≤ (∑ i, v i) / (∑ i, lo i) ^ 2

nineQ_at_MZ : 7.9885 ≤ 9 * Q yMZ ∧ 9 * Q yMZ ≤ 7.9887

nineQ_at_3TeV : 8.0010 ≤ 9 * Q y3TeV ∧ 9 * Q y3TeV ≤ 8.0012

crossing_bracketed : 9 * Q yMZ < 8 ∧ 8 < 9 * Q y3TeV

pinning_within_0_15_percent : |9 * Q yMZ - 8| ≤ 15e-4 * 8 ∧ |9 * Q y3TeV - 8| ≤ 15e-4 * 8
```

## Source-pattern scan

`grep` sweep of `LeanMath/UpTypeParticipation.lean` — **zero** matches in every
category:

| Pattern | Matches |
|---------|---------|
| `sorry` / `admit` / `stop` | 0 |
| `sorryAx` / `native_decide` | 0 |
| bare `axiom` declarations | 0 |
| `unsafe` / `implemented_by` / `@[extern]` / `opaque` | 0 |
| `set_option` (proof-bypass flags) | 0 |

(The strings `sorry` and `native_decide` occur once each on line 41, inside the
header comment that disclaims them. There are no occurrences in proof text.)

## What is and is not certified

This is the load-bearing part of the record, and it is deliberately narrow.

**Certified.** Everything in the table above. In particular:

- **Prop. 2 is proved in a stronger form than the paper states it.** The paper
  claims degree-zero homogeneity of `Q`; `Qp_homogeneous` proves it for the whole
  family `(Σ v^p)/(Σ v^{p/2})²` at arbitrary real exponent `p` (Mathlib `rpow`),
  which is the paper's "power-blind" remark. The common factor `Z^p` cancels
  identically — no positivity of the `v_i` and no nonvanishing of the denominator
  sum is required.
- **Lemma 1 is proved for every phase δ.** The phase drops out; only the cone
  opening `k` survives. The sums reuse the phase-orthogonality results
  (`e1_eq`, `p2_eq`) already verified in `LeanMath/HeavyQuarks.lean`.
- **Eq. (13) is proved without evaluating ζ(2).** Only two ingredients enter:
  summability of `1/n²`, and the exact `3⁻² = 1/9` self-similarity of the silent
  sublattice `{3,6,9,…}`. The `8/9` is a statement about the *ratio* of the
  surviving weight to the total, so the value of the total never appears. This is
  a strictly more robust proof than one routed through `π²/6`.
  Indexing note: Lean's `1/0 = 0` convention gives `w 0 = 0`, so the `n = 0` slot
  carries no weight and lands harmlessly in the silent set (`3 ∣ 0`).
- **Table I is certified by interval arithmetic**, not floating point. Rational
  brackets on each `√y_i` are verified by squaring (`lo² ≤ y ≤ hi²`), then
  propagated through `Q_interval`. The resulting brackets are
  `9Q_U(M_Z) ∈ [7.9885, 7.9887]` and `9Q_U(3 TeV) ∈ [8.0010, 8.0012]`,
  consistent with the paper's quoted `7.9886` and `8.0011`.
- **The crossing is certified to exist, not to be located.** `crossing_bracketed`
  proves the tabulated endpoints straddle 8, so any continuous interpolation
  crosses somewhere in `(M_Z, 3 TeV)`. It says nothing about *where*; the paper's
  `μ_{8/9} ≈ 2–3 TeV` is reported as an output of the running, and the Lean file
  makes no claim about it.

**Not certified, and not to be represented as certified.**

- **The drift law, Eq. (9).** This is a one-loop renormalization-group result in
  quantum field theory, not an algebraic identity. It is deliberately absent from
  the Lean development. No statement in the file should be read as bearing on it.
  Its status in the paper's Table II ("theorem (1-loop); reproduced") refers to
  the field-theory derivation, not to a machine check.
- **The tabulated inputs themselves.** `nineQ_at_MZ` certifies the arithmetic
  *given* the Table I couplings. The couplings come from Ref. [AHS2026]; their
  uncertainties are Appendix B of the paper and are not a Lean object.
- **The GUT-scale overshoot, Eq. (14).** Depends on the source tabulation's
  two-loop running; not formalized.
- **The conjecture that the up-type sector inherits the weight Eq. (13).**
  `blind_weight` is a theorem about the *lepton-side* spectral construction only.
  Its appearance in the up-type ratio is, as the paper states, a numerical
  coincidence between a theorem in one sector and an observation in another. The
  Lean file proves the theorem; it does not, and cannot, prove the conjecture.

## Build note

The author's working Lean project also carries a demo executable target whose
native link step fails with a `clang` error arising from Mathlib's C objects.
That target is **not** part of this repository: the package here declares the
`LeanMath` library only, so `lake build` builds the certificates and nothing
else. Proof checking never involved the executable in any case.

## v2.2 Additions (2026-08-10)

### C. IVT Crossing
- `crossing_exists_of_continuous` — generic IVT theorem for continuous f with f(a)<8<f(b)
- `crossing_certified` — specialized to the tabulated straddle; continuity of the SM RG trajectory is an explicit hypothesis

### D. Exact Admissible Domain
- `delta_max` / `admissible_fraction` — definitions
- Forward direction (`admissible_of_delta_bound`) — left as a future formalization step; the proof sketch is documented in the source comments
- Gate L1 k=1: exact values certified (`delta_max_one`, `admissible_fraction_one`, `lepton_delta_lt_delta_max`, `lepton_delta_ratio`)

### Gate L1 Values
```
k² = 5/3:  delta_max = 0.056041 rad = 3.2109°  (computed: arccos(-√(3/10)) - 2π/3)
           admissible_fraction = 0.05352
           Spec target: 0.056043 rad (3.2110°) — discrep 2.0×10⁻⁶ rad

k² = 1:    delta_max = π/12 = 15° exactly (certified in Lean)
           admissible_fraction = 1/4 (certified in Lean)
           lepton δ = 2/9 rad = 12.7324° (< δ_max, certified in Lean)
           ratio = 8/(3π) ≈ 0.84883 (certified in Lean)
```

### Declaration count: 27 (21 original + 6 new)
### Axiom set: {propext, Classical.choice, Quot.sound} — verified for all 21 original declarations
