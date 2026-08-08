# uptype-pinning
Artifacts for "Electroweak pinning of the up-type participation
ratio near 8/9" (A. M. Brilliant).

mc/coincidence/ — the paper's single-claim coincidence budget:
engine_p4.py (generator; run with no args for the full N=1e7
paper configuration, --quick for CI) and RESULTS.md (the paper's
Table, with Clopper-Pearson intervals).

Formal certificate layer (Lean 4): to be added in a later tagged
release; see release notes. The Monte-Carlo layer here is complete
and self-contained.
