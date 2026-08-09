# Frozen specification — single-claim coincidence budget

This document states the specification in prose. The machine-readable copy is
the `SPEC_CANON` string in `engine_p4.py`, and it is authoritative: the
production seed is derived from its SHA-256.

```
spec sha256 : 3948c0d5b42c0881ae0103488182c9f56aa9fa3bed2c9bcb620d74a52d0d7397
seed        : 961069269
```

## Why the seed is derived rather than chosen

A seed that is simply written down invites the question of how many other
seeds were tried. Deriving it from the hash of the specification removes the
freedom: the seed cannot be changed without changing the specification text,
and any change to the specification changes the seed. Cherry-picking is
excluded by construction rather than by assurance.

The first release used seed `20270301`. That value is retained as
`LEGACY_SEED` and reachable with `--legacy-seed`, because it reproduces the
counts published with that release. It is not the production seed.

## The observable

For a mass triple, Q = (Σ mᵢ) / (Σ √mᵢ)², reported as 9Q. Q is degree-zero
homogeneous: a common factor on all three members leaves it unchanged. Q is
bounded by 1/3 ≤ Q ≤ 1, so 9Q ∈ [3, 9]; the executable asserts this on the
drawn sample rather than assuming it.

## The null sampling measure

Three iid log-coordinates, uniform over a span of

    W = ln(2×10⁵ / 0.5) = ln(4×10⁵) = 12.899220,  i.e. 5.602060 decades.

Because Q is homogeneous, **the endpoints carry no meaning individually** —
only the logarithmic span does. Translating the common log-scale leaves every
result unchanged. The endpoints 0.5 MeV and 2×10⁵ MeV should therefore not be
read as physically motivated bounds; they fix a width, nothing more.

For context, the observed y_t/y_u hierarchy at M_Z spans about 5.14 decades,
so the null support is neither absurdly broad nor tuned to the observation.
Sensitivity to W is measured in `ROBUSTNESS.md`.

This is a **null sampling measure**, not a prior: no Bayesian inference is
performed anywhere in this calculation.

## The distance convention

A draw is a hit when |9Q − target| ≤ 0.0114, an **absolute** distance in 9Q.

The tolerance is not free: 0.0114 is the observed miss |9Q_U(M_Z) − 8|. The
fixed-target calculation is therefore an ordinary retrospective tail
statistic, P(D ≤ D_obs).

Absolute distance is used because Q is a bounded, dimensionless coordinate
and the phenomenological claim is formulated as additive proximity in Q. The
alternative — applying the observed *fractional* miss to every target — is a
defensible choice too, and is reported in `ROBUSTNESS.md` rather than left
for a referee to find.

## The target menu

Twenty irreducible rationals p/q with p, q ≤ 9 lying in the **closed**
admissible range 1/3 ≤ Q ≤ 1:

    1/3, 3/8, 2/5, 3/7, 4/9, 1/2, 5/9, 4/7, 3/5, 5/8,
    2/3, 5/7, 3/4, 7/9, 4/5, 5/6, 6/7, 7/8, 8/9, 1

The executable regenerates this list and writes it into `RESULTS.md`; the
enumeration is asserted at import time, so the two cannot drift apart.

**Both endpoints are included, and this is a correction to the first
release.** Eq. (1) of the manuscript gives the admissible range as
1/3 ≤ Q ≤ 1, closed at both ends, so a menu over that range should contain
both endpoint rationals. The first release excluded 1/3 while including 1,
giving 19 targets.

The two endpoints behave differently, which is what makes the asymmetry
worth correcting rather than merely tidying:

- **Q = 1/3 is attained exactly**, at the equal-mass triple, and contributes
  hits — 14,899 of them per 10⁷ draws in the first release's configuration.
- **Q = 1 is a limit only.** It requires two of the three masses to vanish,
  so no positive triple reaches it and it contributes no hits at all. Running
  the 18-target interior menu reproduces the 19-target count exactly.

The first release therefore counted one inert target and omitted the only
live boundary target. The closed-range menu of 20 is the consistent choice.

## Reporting doctrine

Frequencies are reported with exact two-sided Clopper–Pearson 95% intervals,
computed by the executable. No significance conversion is performed anywhere:
these are model-conditional coincidence frequencies under a stated null, not
p-values.

Menus price listed freedom only; unlisted freedom caps inference and is not
quantified here.

## Files

| file | role |
|---|---|
| `engine_p4.py` | generator; writes `RESULTS.md` and `results.json` |
| `quadrature.py` | deterministic 2-D cross-check of the same frequencies |
| `robustness.py` | support-width and distance-convention sensitivity |
| `verify.py` | re-runs production and asserts the committed results |
| `RESULTS.md`, `results.json` | generated, never hand-edited |
| `ROBUSTNESS.md`, `robustness.json` | generated, never hand-edited |
