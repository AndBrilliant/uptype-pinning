# uptype-pinning

Artifacts for "Electroweak pinning of the up-type participation ratio
near 8/9" (A. M. Brilliant).

Two independent layers, both self-contained and both enforced by CI.

## Formal certificate layer (Lean 4)

Machine-checked proofs of the paper's algebraic and arithmetic claims.

| Paper reference | Declaration |
|---|---|
| Prop. 2 (App. A), power-blind form | `Qp_homogeneous`, `Q_homogeneous`, `Q_cannot_run` |
| Lemma 1 | `lemma1` |
| Lemma 2 | `lemma2`, `lemma2_abstract` |
| Eq. (13), the Z₃ blind weight 8/9 | `blind_weight` |
| Table I / Eq. (2), interval-certified | `nineQ_at_MZ`, `nineQ_at_3TeV` |
| Sec. V, existence of μ_{8/9} in (M_Z, 3 TeV) | `crossing_bracketed` |
| Sec. III, "within 0.15% of 8" | `pinning_within_0_15_percent` |

Twenty-one declarations, plus fifteen in the supporting library, each
depending on exactly the standard classical Mathlib axiom set
`{propext, Classical.choice, Quot.sound}` — no `sorry`, no `native_decide`,
no custom axioms.

```
LeanMath/UpTypeParticipation.lean   the certificates
LeanMath/AxiomCheckUpType.lean      audit driver: #check every statement, then #print axioms
LeanMath/HeavyQuarks.lean           supporting library (phase orthogonality, reused by Lemma 1)
LeanMath/AxiomCheck.lean            audit driver for the supporting library
VERIFICATION_UPTYPE.md              verification record, and the scope statement
VERIFICATION_HEAVYQUARKS.md         verification record for the supporting library
```

```bash
lake exe cache get                            # fetch Mathlib oleans
lake build LeanMath                           # compile the certificates
lake env lean LeanMath/AxiomCheckUpType.lean  # print statements + axiom sweep
```

Toolchain `leanprover/lean4:v4.31.0` with Mathlib `v4.31.0`, pinned exactly by
`lean-toolchain` and `lake-manifest.json`.

**Read `VERIFICATION_UPTYPE.md` before citing any of this.** It states what is
certified and, equally, what is not: the drift law Eq. (9) is a one-loop
field-theory result and is deliberately *not* formalized; the Table I inputs
are taken from Ref. [AHS2026] and are not themselves a Lean object; the
crossing is certified to *exist*, not to be located; and `blind_weight` is a
theorem about the lepton-side construction only, not a proof of the up-type
inheritance conjecture.

## Monte-Carlo layer

The paper's single-claim coincidence budget: how often random spectra land as
close to a simple rational as the observed 9Q_U lands to 8.

```
mc/coincidence/SPEC.md           the frozen specification (read this first)
mc/coincidence/engine_p4.py      generator; writes RESULTS.md and results.json
mc/coincidence/quadrature.py     deterministic 2-D cross-check, no random numbers
mc/coincidence/robustness.py     support-width and distance-convention sensitivity
mc/coincidence/verify.py         re-runs production, asserts the committed results
mc/coincidence/requirements.txt  pinned NumPy and SciPy
```

```bash
cd mc/coincidence
pip install -r requirements.txt
python3 verify.py         # reproduce and assert the committed numbers (~6 s)
python3 quadrature.py     # independent deterministic evaluation
python3 robustness.py     # sensitivity tables
```

`RESULTS.md`, `results.json`, `ROBUSTNESS.md` and `robustness.json` are
**generated**. No number in them is hand-entered, and CI fails if they drift
from what the executable produces.

Three properties are worth stating plainly, because each removes a degree of
freedom a reader would otherwise have to take on trust:

- **The seed is derived, not chosen.** It is the leading four bytes of the
  SHA-256 of the specification text. The seed cannot be changed without
  changing the specification, so seed-shopping is excluded by construction.
  The first release's seed is retained behind `--legacy-seed` for continuity.
- **The Monte Carlo is checked against an exact calculation.** Because Q is
  homogeneous, the null collapses to a two-dimensional integral over the
  ordered log-mass gaps, with density `6(W−a−b)/W³`. `quadrature.py` evaluates
  it deterministically and agrees with the sampled result within combined
  sampling and discretisation error.
- **The declared choices are measured, not asserted.** `ROBUSTNESS.md`
  reports sensitivity to the null support width and to the absolute-versus-
  relative distance convention.

These are model-conditional coincidence frequencies under a stated null
sampling measure. They are not p-values, and no significance conversion is
performed. Menus price listed freedom only; unlisted freedom caps inference
and is not quantified here.
