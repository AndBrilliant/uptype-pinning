# Geometric-Mean Census — findings
Autonomous run, 2026-08-12. Spec SHA-256 `6fd71ee7…`, seed 805894403742576142.

## Summary in one line

The census is built, gated and reproducible, and **it does not support a
rarity claim**. Three independent reasons, any one of which is sufficient.

---

## 1. Literature audit — nothing was missed, and most of it is dead

Four geometric-mean relations exist in the published literature. Tested
across five frames with current PDG/FLAG values:

| relation | source | best residual | verdict |
|---|---|---|---|
| m_s² = m_d m_b | Ng, hep-ph/9204221 | −54.7% | **dead** |
| m_c² = m_u m_t | Ng, hep-ph/9204221 | +187% | **dead** |
| m_c² = m_d m_t | Davidson–Schwartz–Wali, hep-ph/9510444 | +32% | **dead** |
| m_s² = m_u m_b | Davidson–Schwartz–Wali | −1.5% (self-scale) | **holds** |

Ng (1992) and DSW (1995) predate the modern lattice determinations;
three of their four relations do not survive them. The single survivor
was independently recovered by the blind enumeration, which is a genuine
external check on the enumerator.

Two relations from the author's own 2025 work also died on updated
lattice values, and this is recorded as the out-of-sample test working:

- `m_c = 4π m_s` : was 0.27σ with m_s ≈ 101 MeV, now **−7.7%**
- `m_s = m_b/10^φ` : was 0.86σ, now **+7.8%**

Both used the pre-2024 strange mass.

## 2. The parameter-free argument is correct

Of ~22 relations in the two-year record, 15 carry a fitted constant
(`e^{π/√7}`, `7e³/π`, `4π`, `12`, `5/7`, `19.23`, …) and 7 do not. The
fitted-constant family fits *better* — median |dev| 0.32% against 1.22%
— which is exactly what a free knob buys. Only the parameter-free family
has enumerable freedom, so only it can be priced. That reasoning stands.

## 3. But the census fails three independent tests

### 3a. Under the principled tolerance it is null

Using propagated measurement uncertainties (σ_D = √(4f_j² + f_i² + f_k²),
hit iff |D| < 2σ_D):

| object set | observed | p (worst admissible prior) |
|---|---|---|
| with G | 5 | **0.70** |
| without G | 3 | **0.85** |

The light quarks carry 1.5–9.6% fractional errors, so the 2σ windows are
wide enough that random spectra walk into them.

### 3b. The flat-tolerance signal is marginal and leans on G

| object set | observed at 2% | p (worst admissible prior) |
|---|---|---|
| with G | 6 | 0.0075 |
| without G | 4 | 0.036 |

A4 (uniform-in-mass) is **excluded by the support gate**, not for being
unfavourable: its median hierarchy is 203 against the observed 7.4×10⁴,
and only 0.4% of its draws reach half the observed hierarchy. Clustered
spectra get *more* geometric-mean hits (corr = −0.27 between hierarchy
and hit count), so A4's high null rate is an artifact of its inability to
contain the observation.

### 3c. **Decisive: every frame-invariant geometric mean fails**

A relation m_j² = m_i m_k is invariant under QCD running iff all three
objects share an anomalous dimension — i.e. all three are quarks of the
same charge. There are exactly three such triples in the Standard Model,
and all three fail:

| triple | m_mid²/(m_lo m_hi) | residual |
|---|---|---|
| (d, s, b) | 0.445 | −55.5% |
| (u, c, t) | 4.595 | +359% |
| (e, μ, τ) | 12.295 | +1130% |

Every relation that *does* hold is cross-sector, hence quoted in a mixed
frame. Repeating the census at a genuine common scale:

| frame | relations at 2% |
|---|---|
| mixed (sector-native) | 6 |
| common 2 GeV | 2 |
| common m_c, 3 GeV, m_b | **0** |

Per-relation frame dependence spans −33% to +38%. The census is a
statement about masses in sector-native frames, not about the spectrum.

## 4. Connectivity is not extra evidence

The six observed relations do form a single connected component over ten
objects. But **88% of null draws with ≥6 relations are also connected**.
Chaining is expected at that count, not informative.

## 5. What this means

The vision — that geometric means are the only parameter-free family and
therefore the only priceable one — is correct and worth keeping. What the
census cannot do, as built, is convert that into a rarity claim, because
the relations that hold are precisely the ones whose truth depends on a
frame convention.

**This does not damage the heavy-pair letter.** That letter already
states the convention dependence of G² = m_c m_b explicitly, gives the
common-scale numbers, and declines to claim scale-freeness. The census
result is consistent with it and reinforces the disclosure.

**What would rescue a rarity claim**, in order of tractability:

1. Defend the frame assignment on physical grounds *before* counting, so
   the mixed frame is a premise rather than a choice. The heavy-pair
   letter's argument (each sector evaluated where it is defined) is the
   start of this, but it must cover leptons and cross-sector pairs too.
2. Improve the light-quark inputs. The measurement-tolerance test is null
   mainly because m_u carries ~10%. A factor-3 improvement would make
   that test informative either way.
3. Restrict to same-sector relations — where the test is frame-free — and
   accept that all three currently fail, i.e. report a null result.

Option 3 is the honest one available today.

## Artifacts

    gmc/SPEC_GMC.md        frozen spec, hashed, seeds the RNG
    gmc/gmc_engine.py      enumerator, priors, 7 gates
    gmc/gmc_run.py         production runner
    gmc/frame_variant.py   the frame robustness cell
    gmc/results/           gates, manifest, census, nulls, frame variant

---

## 6. The one thing that does survive — and it is frame-free

Under QCD running the only invariant quantities are same-sector *ratios*
(the common factor Z cancels). There are exactly nine. Expressed as
powers of 1/α:

| ratio | value | n = ln r / ln(1/α) |
|---|---|---|
| τ/μ | 16.82 | 1.891 |
| **s/d** | **19.89** | **2.003** |
| b/s | 44.71 | 2.546 |
| t/c | 127.95 | 3.250 |
| μ/e | 206.77 | 3.572 |
| c/u | 587.96 | 4.272 |
| b/d | 889.36 | 4.549 |
| τ/e | 3477.23 | 5.462 |
| t/u | 75231 | 7.522 |

Exactly one lands on an integer: **m_s/m_d = α⁻² to +0.48%**. No two of
the nine are equal; none is the geometric mean of two others.

This is the single frame-invariant structural claim in the corpus, and it
is the companion's, not the heavy-pair letter's. Priced against the three
admissible priors, N = 2×10⁵ each:

| test | p |
|---|---|
| open search: any of 9 ratios, any power n = 1…8 (72 targets), 0.5% | 0.040 – 0.052 |
| pre-registered: s/d specifically, n = 2 specifically, 0.5% | 0.0009 – 0.0016 |

So the honest range is **1 in 20 if the search is counted, 1 in ~700 if
the target was fixed in advance**. Which applies depends on a provenance
question, not a statistical one: α is fixed by the charged-lepton
relation independently of any quark, and the s/d identification was made
once, at sight, against a remembered menu of order ten FLAG ratios. That
argues for something between the two numbers, closer to the open end.

**Recommendation.** This — not the census — is the rarity statement the
corpus can defend. It is frame-free, the test space can be declared in
advance, and the residual is measurement-limited rather than
convention-limited. The census should be reported as a negative result
and as the reason the frame question must be settled first.
