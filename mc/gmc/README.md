# Geometric-mean census and the mu-star Monte Carlo

Supporting computation for the heavy-pair letter and its companions.

Everything here is driven by `SPEC_GMC.md`, which is frozen: its SHA-256 seeds
the RNG, so every number below is reproducible from this tree alone.

    SPEC_GMC.md        frozen specification, 8 gates, hashes to the seed
    gmc_engine.py      enumerator, four null priors, gate implementations
    gmc_run.py         census production runner
    mustar_mc.py       the five constraints at mu*, one value per mass
    joint_mc.py        joint pricing with Koide granted as prior art
    cumulative.py      monotonicity: every subset, every ordering
    o5_ladder.py       the 105-pair ladder menu null
    frame_variant.py   frame-robustness cell (common-scale census)
    frame_free_mc.py   the frame-invariant subset

    FINDINGS.md        census result (negative) and why
    CONSOLIDATED.md    corrected classification: invariant / scale-fixed / ambiguous
    TAXONOMY.md        five operation families, each with its declared menu
    FORECAST.md        falsification timescale under both scenarios
    TRAJECTORY.md      out-of-sample: PDG 2014 / 2019 / 2024
    LEMMAS.md          what b/c can and cannot be made theorem-shaped
    WORKLOG.md         running state

## Headline numbers

- census as a rarity claim: NEGATIVE (see FINDINGS.md)
- mu* constraints, 2e6 draws: p < 1.5e-6, null never exceeded 3 of 5
- look-elsewhere corrected, all menus granted to the null: O1 0.081-0.104,
  O2 0.091-0.171, O3 0.057-0.075, O4 0.072-0.136, O5 0.013
- monotonicity: no subset at any depth plateaus; cheapest single relation 1 in 20

## Reproducing

    python3 gmc_engine.py        # runs the gates; must print all PASS
    python3 gmc_run.py --quick   # census smoke test
    python3 mustar_mc.py         # the five constraints

Requires numpy, scipy, and (for the frame cells) rundec.
