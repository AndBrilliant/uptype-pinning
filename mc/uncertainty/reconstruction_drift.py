#!/usr/bin/env python3
"""Reconstruction drift: correlated 9Q_U at M_Z and 3 TeV from draw-once MC.

PURPOSE
The independent PDG-primaries reconstruction gives 9Q_U(M_Z) = 7.9778, agreeing
with the tabulation's 7.9886 at 1.0 sigma (charm-dominated). The manuscript's
central claim has two parts: proximity to 8/9, and FLATNESS across M_Z → 3 TeV.

Absolute values are extraction-dependent; the DRIFT between scales should be
far more robust because correlated extraction systematics cancel. This job
tests that by evolving the SAME reconstructed inputs to both scales and
comparing the reconstructed excursion against the tabulated excursion 0.0125.

METHOD
- Draw-once MC: each universe's PDG primaries are drawn once, then
  reconstruct_9q gives the M_Z endpoint and evolve_to_3tev gives the 3 TeV
  endpoint from the SAME m_i(M_Z) and mt_msbar. Endpoints are correlated as the
  evolution requires.
- N = 20000 (full), N = 100 (--quick smoke test).

GATE T1: M_Z central value (single-point at PDG centrals) reproduces 7.9778
         from the archived run to 1e-4.
GATE T2: every reported number is COMPUTED (finite, non-NaN).
GATE T3 (evolution is real): |9Q_U(3 TeV) - 9Q_U(M_Z)| > 1e-4 for the central
         reconstruction.  A drift below threshold means the evolution did not
         run — STOP, never report as a physics result.

OUTPUT
mc/uncertainty/results/drift/drift.json
mc/uncertainty/results/drift/gate_T1.json
mc/uncertainty/results/drift/gate_T2.json
mc/uncertainty/results/drift/gate_T3.json

Usage:
    python3 reconstruction_drift.py           # full run (N=20000)
    python3 reconstruction_drift.py --quick   # smoke test (N=100)
    python3 reconstruction_drift.py --n 5000  # custom N
"""

import sys
import json
import time
import os
import argparse
import numpy as np

# ── Import the existing pipeline ──────────────────────────────────────────
from qcd import (
    reconstruct_9q, compute_9q, masses_to_yukawas,
    VEV, SQRT2, MZ,
    run_alpha_s, _run_mass_segment,
    match_alpha_s_inverse, _zeta_m_numerical,
)
from extract_inputs import INPUTS, AHS


# ── Paths ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results", "drift")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Reference constants ───────────────────────────────────────────────────
ARCHIVED_MZ_9Q = 7.9778          # archived single-point central value
MU_HIGH        = 3000.0          # 3 TeV
TAB_9Q_MZ      = AHS["nine_Q_MZ"]  # 7.9886
TAB_9Q_3TEV    = 8.0011          # AHS tabulation at 3 TeV
TAB_DRIFT      = TAB_9Q_3TEV - TAB_9Q_MZ   # 0.0125
TAB_DRIFT_PCT  = TAB_DRIFT / 8.0 * 100.0   # 0.15625%


# ── Yukawa RGE coefficients (1-loop SM, up-type sector) ──────────────────
# d ln y_i / d ln μ = -γ_QCD + κ_i · y_t²/(16π²)
# γ_QCD is flavour-universal (handled by qcd._run_mass_segment).
# κ_i are from the Y_u†Y_u diagonal + Tr(3Y_u†Y_u) trace in Machacek & Vaughn
# (Nucl. Phys. B 236 (1984) 221), keeping only the dominant y_t² terms.
#
#   κ_t = 9/2    (3/2 from diagonal y_t^3 term + 3 from trace)
#   κ_c = 3      (trace only; diagonal y_c^3 term is negligible)
#   κ_u = 3      (trace only; diagonal y_u^3 term is negligible)
KAPPA_T = 4.5    # 9/2
KAPPA_C = 3.0
KAPPA_U = 3.0


def _yukawa_factor(y_t_start, y_t_end_qcd, dt, kappa):
    """Multiplicative Yukawa RGE correction over one segment.

    Uses geometric-mean midpoint approximation for ∫ y_t² d ln μ.
    Accurate to O(dt²); the Yukawa contribution is a ~3–10 % perturbation
    on top of QCD running, so the midpoint error is negligible for 9Q drift.

    Parameters
    ----------
    y_t_start : float
        Top Yukawa at the start of the segment.
    y_t_end_qcd : float
        Top Yukawa at the end, evolved with QCD ONLY (same factor as u,c).
    dt : float
        ln(mu_end / mu_start).
    kappa : float
        Flavour-dependent RGE coefficient.

    Returns
    -------
    float — multiplicative factor to apply AFTER QCD running.
    """
    y_t_mid = np.sqrt(y_t_start * y_t_end_qcd)
    return np.exp(kappa * y_t_mid ** 2 * dt / (16.0 * np.pi ** 2))


# ── High-scale evolution ──────────────────────────────────────────────────

def evolve_to_3tev(m_u_MZ, m_c_MZ, m_t_MZ, mt_msbar, alphas_mz):
    """Evolve M_Z MSbar masses to 3 TeV through the top threshold.

    Path
    ----
    M_Z ──[nf=5, QCD + Yukawa, UP]──▶ m_t(m_t)
         ──[match 5→6]──▶ 3 TeV [nf=6, QCD + Yukawa, UP]

    The QCD part (4-loop RGE + 3-loop threshold matching) uses the
    existing qcd.py functions.  The Yukawa part adds the 1-loop SM
    Yukawa RGE corrections (κ_t=9/2, κ_c=κ_u=3), which break the
    flavour universality of pure QCD and make 9Q run.

    Parameters
    ----------
    m_u_MZ, m_c_MZ, m_t_MZ : float
        MSbar masses at M_Z in the nf=5 scheme (GeV).
    mt_msbar : float
        m_t(m_t) in MSbar — defines the top threshold location.
    alphas_mz : float
        alpha_s(M_Z) in the nf=5 scheme.

    Returns
    -------
    dict with {mu_high_GeV, mu_thresh_GeV, m_u/c/t_3TeV_GeV,
               y_u/c/t_3TeV, nine_Q}
    """
    a_mz_4pi = alphas_mz / (4.0 * np.pi)
    mu_thresh = mt_msbar

    # Starting Yukawas (for the Yukawa RGE correction)
    y_u_MZ = SQRT2 * m_u_MZ / VEV
    y_c_MZ = SQRT2 * m_c_MZ / VEV
    y_t_MZ = SQRT2 * m_t_MZ / VEV

    # ── Segment 1: M_Z → top threshold (nf=5, QCD UP) ──
    a5_at_thresh_4pi = run_alpha_s(a_mz_4pi, MZ, mu_thresh, 5)

    m_u_5_qcd = _run_mass_segment(MZ, m_u_MZ, a_mz_4pi, mu_thresh, 5)
    m_c_5_qcd = _run_mass_segment(MZ, m_c_MZ, a_mz_4pi, mu_thresh, 5)
    m_t_5_qcd = _run_mass_segment(MZ, m_t_MZ, a_mz_4pi, mu_thresh, 5)

    # QCD-only Yukawas at threshold (for midpoint y_t in Yukawa factor)
    y_t_5_qcd = SQRT2 * m_t_5_qcd / VEV
    dt_1 = np.log(mu_thresh / MZ)

    yuk_fac_t_1 = _yukawa_factor(y_t_MZ, y_t_5_qcd, dt_1, KAPPA_T)
    yuk_fac_c_1 = _yukawa_factor(y_t_MZ, y_t_5_qcd, dt_1, KAPPA_C)
    yuk_fac_u_1 = _yukawa_factor(y_t_MZ, y_t_5_qcd, dt_1, KAPPA_U)

    m_u_5 = m_u_5_qcd * yuk_fac_u_1
    m_c_5 = m_c_5_qcd * yuk_fac_c_1
    m_t_5 = m_t_5_qcd * yuk_fac_t_1
    y_t_5 = y_t_5_qcd * yuk_fac_t_1  # for the next segment's midpoint

    # ── Match 5 → 6 at the top threshold ──
    as5_pi = a5_at_thresh_4pi * 4.0
    as6_pi = match_alpha_s_inverse(as5_pi, 5)
    a6_4pi = as6_pi / 4.0

    d2, d3, d4 = _zeta_m_numerical(5)
    zeta_m = 1.0 + d2 * as6_pi ** 2 + d3 * as6_pi ** 3 + d4 * as6_pi ** 4

    m_u_6 = m_u_5 / zeta_m
    m_c_6 = m_c_5 / zeta_m
    m_t_6 = m_t_5 / zeta_m

    # ── Segment 2: Threshold → 3 TeV (nf=6, QCD UP) ──
    a6_at_3tev_4pi = run_alpha_s(a6_4pi, mu_thresh, MU_HIGH, 6)

    m_u_3tev_qcd = _run_mass_segment(mu_thresh, m_u_6, a6_4pi, MU_HIGH, 6)
    m_c_3tev_qcd = _run_mass_segment(mu_thresh, m_c_6, a6_4pi, MU_HIGH, 6)
    m_t_3tev_qcd = _run_mass_segment(mu_thresh, m_t_6, a6_4pi, MU_HIGH, 6)

    # QCD-only y_t at 3 TeV for the midpoint
    y_t_3tev_qcd = SQRT2 * m_t_3tev_qcd / VEV
    dt_2 = np.log(MU_HIGH / mu_thresh)

    yuk_fac_t_2 = _yukawa_factor(y_t_5, y_t_3tev_qcd, dt_2, KAPPA_T)
    yuk_fac_c_2 = _yukawa_factor(y_t_5, y_t_3tev_qcd, dt_2, KAPPA_C)
    yuk_fac_u_2 = _yukawa_factor(y_t_5, y_t_3tev_qcd, dt_2, KAPPA_U)

    m_u_3tev = m_u_3tev_qcd * yuk_fac_u_2
    m_c_3tev = m_c_3tev_qcd * yuk_fac_c_2
    m_t_3tev = m_t_3tev_qcd * yuk_fac_t_2

    # ── Yukawas and 9Q at 3 TeV ──
    y = masses_to_yukawas(m_u_3tev, m_c_3tev, m_t_3tev)
    nine_q = compute_9q(y)

    return {
        "mu_high_GeV":   MU_HIGH,
        "mu_thresh_GeV": mu_thresh,
        "m_u_3TeV_GeV":  float(m_u_3tev),
        "m_c_3TeV_GeV":  float(m_c_3tev),
        "m_t_3TeV_GeV":  float(m_t_3tev),
        "y_u_3TeV":      float(y[0]),
        "y_c_3TeV":      float(y[1]),
        "y_t_3TeV":      float(y[2]),
        "nine_Q":        float(nine_q),
    }


# ── Main drift computation ────────────────────────────────────────────────

def run_drift(n_mc=20000, seed=54321):
    """Run the draw-once drift computation.

    Each universe draws PDG primaries once → reconstruct_9q at M_Z →
    evolve_to_3tev from those M_Z masses.  Endpoints are correlated
    by construction (shared draw, shared evolution path to M_Z).
    """
    print("=" * 72)
    print("RECONSTRUCTION DRIFT: 9Q_U(M_Z) → 9Q_U(3 TeV)")
    print("Draw-once MC — endpoints correlated as evolution requires")
    print("=" * 72)
    print()

    # ── Central-value check (GATE T1 pre-flight) ──
    print("── Central-value check (PDG centrals → reconstruct_9q) ──")
    r_cv = reconstruct_9q(
        INPUTS["m_u"]["value"],
        INPUTS["m_c"]["value"],
        INPUTS["m_t_pole"]["value"],
        INPUTS["alpha_s_MZ"]["value"],
    )
    cv_nine_q = r_cv["nine_Q"]
    cv_diff = abs(cv_nine_q - ARCHIVED_MZ_9Q)
    t1_pass = cv_diff <= 1e-4
    print(f"  Single-point 9Q_U(M_Z) = {cv_nine_q:.4f}")
    print(f"  Archived               = {ARCHIVED_MZ_9Q:.4f}")
    print(f"  |Δ| = {cv_diff:.6f}")
    print()

    # Central-value 3 TeV evolution
    r_cv_3tev = evolve_to_3tev(
        r_cv["m_u_MZ"], r_cv["m_c_MZ"], r_cv["m_t_MZ"],
        r_cv["mt_msbar"], INPUTS["alpha_s_MZ"]["value"],
    )
    cv_nine_q_3tev = r_cv_3tev["nine_Q"]
    cv_drift = cv_nine_q_3tev - cv_nine_q
    print(f"  Yukawa triples at M_Z:")
    print(f"    y_u = {r_cv['y_u']:.8f}")
    print(f"    y_c = {r_cv['y_c']:.6f}")
    print(f"    y_t = {r_cv['y_t']:.4f}")
    print(f"  Yukawa triples at 3 TeV:")
    print(f"    y_u = {r_cv_3tev['y_u_3TeV']:.8f}")
    print(f"    y_c = {r_cv_3tev['y_c_3TeV']:.6f}")
    print(f"    y_t = {r_cv_3tev['y_t_3TeV']:.4f}")
    print(f"  Single-point 9Q_U(M_Z)   = {cv_nine_q:.4f}")
    print(f"  Single-point 9Q_U(3 TeV) = {cv_nine_q_3tev:.4f}")
    print(f"  Single-point drift        = {cv_drift:+.4f}")
    print()

    # ── Draw inputs ──
    rng = np.random.default_rng(seed)

    m_u_draws = rng.normal(INPUTS["m_u"]["value"], INPUTS["m_u"]["uncertainty"], n_mc)
    m_c_draws = rng.normal(INPUTS["m_c"]["value"], INPUTS["m_c"]["uncertainty"], n_mc)
    m_t_draws = rng.normal(INPUTS["m_t_pole"]["value"], INPUTS["m_t_pole"]["uncertainty"], n_mc)
    a_s_draws = rng.normal(INPUTS["alpha_s_MZ"]["value"], INPUTS["alpha_s_MZ"]["uncertainty"], n_mc)

    m_u_draws = np.clip(m_u_draws, 1e-5, 1.0)
    m_c_draws = np.clip(m_c_draws, 0.5, 2.5)
    m_t_draws = np.clip(m_t_draws, 165.0, 180.0)
    a_s_draws = np.clip(a_s_draws, 0.110, 0.126)

    # ── Storage ──
    nine_q_mz   = np.full(n_mc, np.nan)
    nine_q_3tev = np.full(n_mc, np.nan)

    print(f"── Draw-once MC (N={n_mc:,}) ──")
    t0 = time.time()
    n_done = 0

    for i in range(n_mc):
        try:
            # (A) Reconstruct at M_Z via the existing pipeline
            r_mz = reconstruct_9q(
                m_u_draws[i], m_c_draws[i], m_t_draws[i], a_s_draws[i],
            )
            nine_q_mz[i] = r_mz["nine_Q"]

            # (B) Evolve the SAME M_Z masses onward to 3 TeV
            r_hi = evolve_to_3tev(
                r_mz["m_u_MZ"], r_mz["m_c_MZ"], r_mz["m_t_MZ"],
                r_mz["mt_msbar"], a_s_draws[i],
            )
            nine_q_3tev[i] = r_hi["nine_Q"]

            n_done += 1
        except Exception:
            pass

        if (i + 1) % 5000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (n_mc - i - 1) / rate if rate > 0 else 0
            print(f"  {i+1}/{n_mc}  ({rate:.0f}/s, ETA {eta:.0f}s)", file=sys.stderr)

    t_total = time.time() - t0
    print(f"  Completed in {t_total:.1f}s  ({n_done}/{n_mc} converged)")
    print()

    # ── Statistics ──
    mask = ~np.isnan(nine_q_mz) & ~np.isnan(nine_q_3tev)
    mz   = nine_q_mz[mask]
    t3   = nine_q_3tev[mask]
    drift_arr = t3 - mz

    mz_mean = float(np.mean(mz))
    mz_std  = float(np.std(mz))
    t3_mean = float(np.mean(t3))
    t3_std  = float(np.std(t3))

    drift_mean = float(np.mean(drift_arr))
    drift_std  = float(np.std(drift_arr))
    drift_p16  = float(np.percentile(drift_arr, 15.87))
    drift_p84  = float(np.percentile(drift_arr, 84.13))

    # Endpoint correlation
    corr_matrix = np.corrcoef(mz, t3)
    endpoint_corr = float(corr_matrix[0, 1])

    # Independent-endpoint drift uncertainty (no correlation)
    independent_drift_std = np.sqrt(mz_std ** 2 + t3_std ** 2)

    # Correlation benefit (% reduction in drift uncertainty)
    corr_benefit = (1.0 - drift_std / independent_drift_std) * 100.0

    # Deviation from 8 (percent)
    mz_pct  = (mz_mean  - 8.0) / 8.0 * 100.0
    t3_pct  = (t3_mean  - 8.0) / 8.0 * 100.0
    cv_mz_pct  = (cv_nine_q  - 8.0) / 8.0 * 100.0
    cv_t3_pct  = (cv_nine_q_3tev  - 8.0) / 8.0 * 100.0

    reco_drift_pct = drift_mean / 8.0 * 100.0

    # ── Report ──
    print("── RESULTS ──")
    print(f"  9Q_U(M_Z)      = {mz_mean:.4f} ± {mz_std:.4f}")
    print(f"  9Q_U(3 TeV)    = {t3_mean:.4f} ± {t3_std:.4f}")
    print(f"  Drift          = {drift_mean:+.4f} ± {drift_std:.4f}")
    print(f"  Drift 68% CI   = [{drift_p16:+.4f}, {drift_p84:+.4f}]")
    print()
    print(f"  CV 9Q(M_Z)     = {cv_nine_q:.4f}  ({cv_mz_pct:+.3f}% from 8)")
    print(f"  CV 9Q(3 TeV)   = {cv_nine_q_3tev:.4f}  ({cv_t3_pct:+.3f}% from 8)")
    print()
    print(f"  MC 9Q(M_Z)     = {mz_mean:.4f}  ({mz_pct:+.3f}% from 8)")
    print(f"  MC 9Q(3 TeV)   = {t3_mean:.4f}  ({t3_pct:+.3f}% from 8)")
    print()
    print(f"  Reconstructed drift  = {drift_mean:+.4f}  ({reco_drift_pct:+.3f}% of 8)")
    print(f"  Tabulated drift      = {TAB_DRIFT:+.4f}  ({TAB_DRIFT_PCT:.3f}% of 8)")
    print(f"  Tabulated endpoints  = {TAB_9Q_MZ:.4f} → {TAB_9Q_3TEV:.4f}")
    print()
    print(f"  Endpoint correlation     = {endpoint_corr:.4f}")
    print(f"  Independent-drift σ      = {independent_drift_std:.4f}")
    print(f"  Correlated-drift σ       = {drift_std:.4f}")
    print(f"  Correlation benefit      = {corr_benefit:.1f}% narrower")
    print()

    # ── GATE T1 ──
    print("── GATE T1: M_Z central value reproduces archived 7.9778 ──")
    print(f"  |{cv_nine_q:.4f} - {ARCHIVED_MZ_9Q:.4f}| = {cv_diff:.6f}")
    print(f"  Tolerance: ≤ 1e-4")
    print(f"  RESULT: {'✅ PASS' if t1_pass else '❌ FAIL — STOP, DO NOT TUNE'}")
    print()

    gate_t1 = {
        "description":   "M_Z single-point central value must reproduce 7.9778 to 1e-4",
        "reconstructed": cv_nine_q,
        "archived":      ARCHIVED_MZ_9Q,
        "difference":    cv_diff,
        "tolerance":     1e-4,
        "pass":          bool(t1_pass),
    }

    # ── GATE T2 ──
    reported = {
        "cv_nine_q":          cv_nine_q,
        "cv_nine_q_3tev":     cv_nine_q_3tev,
        "cv_drift":           cv_drift,
        "cv_mz_pct":          cv_mz_pct,
        "cv_t3_pct":          cv_t3_pct,
        "mz_mean":            mz_mean,
        "mz_std":             mz_std,
        "t3_mean":            t3_mean,
        "t3_std":             t3_std,
        "drift_mean":         drift_mean,
        "drift_std":          drift_std,
        "drift_p16":          drift_p16,
        "drift_p84":          drift_p84,
        "mz_pct":             mz_pct,
        "t3_pct":             t3_pct,
        "reco_drift_pct":     reco_drift_pct,
        "endpoint_corr":      endpoint_corr,
        "independent_drift_std": independent_drift_std,
        "corr_benefit":       corr_benefit,
        "n_done":             n_done,
        "t_total_s":          t_total,
    }

    all_finite = all(
        isinstance(v, (int, float)) and np.isfinite(v)
        for v in reported.values()
    )
    t2_pass = all_finite

    print("── GATE T2: Every reported number is COMPUTED ──")
    print(f"  All values finite: {all_finite}")
    print(f"  RESULT: {'✅ PASS' if t2_pass else '❌ FAIL — STOP, PRINT FOR OPERATOR'}")
    print()

    gate_t2 = {
        "description": "Every reported number must be COMPUTED (finite, non-NaN)",
        "all_finite":  all_finite,
        "pass":        bool(t2_pass),
    }

    # ── GATE T3 ──
    t3_pass = abs(cv_drift) > 1e-4

    print("── GATE T3: |9Q(3 TeV) - 9Q(M_Z)| > 1e-4 (evolution is real) ──")
    print(f"  |drift| = {abs(cv_drift):.6f}")
    print(f"  Threshold: > 1e-4")
    print(f"  RESULT: {'✅ PASS — evolution is real' if t3_pass else '❌ FAIL — evolution did not run, STOP'}")
    print()

    gate_t3 = {
        "description": "|9Q_U(3 TeV) - 9Q_U(M_Z)| must exceed 1e-4 — evolution is real",
        "drift_abs":    abs(cv_drift),
        "threshold":    1e-4,
        "pass":         bool(t3_pass),
    }

    # ── Write outputs ──
    drift_json = {
        "spec_version": "v1.0",
        "title": "Reconstruction Drift: 9Q_U(M_Z) → 9Q_U(3 TeV)",
        "method": "Draw-once MC — endpoints correlated as evolution requires",
        "n_draws":      n_mc,
        "n_converged":  n_done,
        "runtime_s":    t_total,
        "central_value": {
            "mz_9Q":            cv_nine_q,
            "tev_9Q":           cv_nine_q_3tev,
            "drift":            cv_drift,
            "mz_pct_dev_from_8": cv_mz_pct,
            "tev_pct_dev_from_8": cv_t3_pct,
        },
        "mc_propagation": {
            "mz": {
                "nine_Q_mean": mz_mean,
                "nine_Q_std":  mz_std,
                "pct_dev_from_8": mz_pct,
            },
            "tev": {
                "nine_Q_mean": t3_mean,
                "nine_Q_std":  t3_std,
                "pct_dev_from_8": t3_pct,
            },
            "drift": {
                "value":       drift_mean,
                "std":         drift_std,
                "p16":         drift_p16,
                "p84":         drift_p84,
                "pct_of_8":    reco_drift_pct,
            },
        },
        "tabulated": {
            "mz_9Q":          TAB_9Q_MZ,
            "tev_9Q":         TAB_9Q_3TEV,
            "drift":          TAB_DRIFT,
            "drift_pct_of_8": TAB_DRIFT_PCT,
        },
        "correlation": {
            "endpoint_correlation":       endpoint_corr,
            "independent_drift_std":      independent_drift_std,
            "correlated_drift_std":       drift_std,
            "correlation_benefit_pct":    corr_benefit,
        },
        "gates": {
            "T1": gate_t1,
            "T2": gate_t2,
            "T3": gate_t3,
        },
    }

    out_drift  = os.path.join(RESULTS_DIR, "drift.json")
    out_t1     = os.path.join(RESULTS_DIR, "gate_T1.json")
    out_t2     = os.path.join(RESULTS_DIR, "gate_T2.json")
    out_t3     = os.path.join(RESULTS_DIR, "gate_T3.json")

    with open(out_drift, "w") as f:
        json.dump(drift_json, f, indent=2)
    with open(out_t1, "w") as f:
        json.dump(gate_t1, f, indent=2)
    with open(out_t2, "w") as f:
        json.dump(gate_t2, f, indent=2)
    with open(out_t3, "w") as f:
        json.dump(gate_t3, f, indent=2)

    print(f"Wrote {out_drift}")
    print(f"Wrote {out_t1}")
    print(f"Wrote {out_t2}")
    print(f"Wrote {out_t3}")

    if not t1_pass:
        print("\n⛔ GATE T1 FAILED.  Stopping as required — do NOT tune.")
        return None
    if not t2_pass:
        print("\n⛔ GATE T2 FAILED.  Stopping — print for operator ruling.")
        return None
    if not t3_pass:
        print("\n⛔ GATE T3 FAILED.  Evolution did not run — STOP, never report as physics.")
        return None

    print()
    print("=" * 72)
    print("ALL GATES PASSED — drift computation complete.")
    print("=" * 72)
    return drift_json


# ── CLI ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reconstruction drift: correlated 9Q_U at M_Z and 3 TeV"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="Quick smoke test (N=100)"
    )
    parser.add_argument(
        "--n", type=int, default=20000,
        help="Number of MC draws (default: 20000)"
    )
    args = parser.parse_args()

    n_mc = 100 if args.quick else args.n

    result = run_drift(n_mc=n_mc)
    if result is None:
        sys.exit(1)
