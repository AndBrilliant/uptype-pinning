/-
Axiom audit for LeanMath/UpTypeParticipation.lean — the formal certificates for
"Electroweak pinning of the up-type participation ratio near 8/9"
(A. M. Brilliant, 2026).

A proof is trusted iff its axiom set is a subset of the standard classical
Mathlib footprint {propext, Classical.choice, Quot.sound} and contains no
`sorryAx`. Run with:

    lake env lean LeanMath/AxiomCheckUpType.lean

`#check` lines print each statement in full so that the audit records *what* was
proved, not merely that something was.
-/
import LeanMath.UpTypeParticipation

open UpType

/-! ## Statements as proved -/

#check @UpType.Q
#check @UpType.Qp
#check @UpType.Q_bounds
#check @UpType.Qp_homogeneous
#check @UpType.Q_homogeneous
#check @UpType.Q_cannot_run
#check @UpType.lemma1
#check @UpType.lemma2
#check @UpType.lemma2_abstract
#check @UpType.k_at_eight_ninths_bracket
#check @UpType.silent_weight
#check @UpType.blind_weight
#check @UpType.Q_interval
#check @UpType.nineQ_at_MZ
#check @UpType.nineQ_at_3TeV
#check @UpType.crossing_bracketed
#check @UpType.pinning_within_0_15_percent

/-! ## Axiom sweep -/

-- Eq. (1): range of the participation ratio
#print axioms UpType.Q_bounds

-- Proposition 2 (App. A): homogeneity protection, power-blind and standard forms
#print axioms UpType.Qp_homogeneous
#print axioms UpType.Q_homogeneous
#print axioms UpType.Q_cannot_run

-- Lemma 1 and its supporting sums
#print axioms UpType.coneRoot_sum
#print axioms UpType.coneTriple_sum
#print axioms UpType.lemma1

-- Lemma 2 and the cone-opening bracket
#print axioms UpType.lemma2
#print axioms UpType.lemma2_abstract
#print axioms UpType.k_at_eight_ninths_bracket

-- Eq. (13): the Z3 blind weight
#print axioms UpType.w_summable
#print axioms UpType.w_three_mul
#print axioms UpType.tsum_w_pos
#print axioms UpType.silent_weight
#print axioms UpType.tsum_silent_subtype
#print axioms UpType.blind_weight

-- Table I: certified interval evaluation of the observable
#print axioms UpType.Q_interval
#print axioms UpType.nineQ_at_MZ
#print axioms UpType.nineQ_at_3TeV
#print axioms UpType.crossing_bracketed
#print axioms UpType.pinning_within_0_15_percent

