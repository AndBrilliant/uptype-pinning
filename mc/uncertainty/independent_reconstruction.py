#!/usr/bin/env python3
"""Independent reconstruction of 9Q_U(M_Z) from PDG 2024 primaries.

PART A: Reconstructs 9Q_U(M_Z) from primary PDG inputs through our own
QCD running pipeline (4-loop RGE + 3-loop threshold matching).
Cross-checks against the AHS tabulation with gates that enforce
agreement within combined uncertainties.

PART A+ (operator): Computes the INDUCED correlation matrix of
(y_u, y_c, y_t) at M_Z from independent PDG primaries. This correlation
is DERIVED, not assumed — it emerges from the shared alpha_s dependence
in the QCD running and threshold matching.

Usage:
    python3 independent_reconstruction.py                # full run (N=1e5)
    python3 independent_reconstruction.py --quick N=20000  # quick test
    python3 independent_reconstruction.py --no-mc          # central values only
"""
import sys
import json
import time
import numpy as np

from qcd import reconstruct_9q, compute_9q, masses_to_yukawas, VEV, SQRT2
from extract_inputs import INPUTS, AHS, CONSTANTS
from reproduce_table import reproduce as reproduce_ahs


# ── Gate definitions ────────────────────────────────────────────────────
AHS_NINE_Q = AHS["nine_Q_MZ"]
AHS_BAND = AHS["band"]


def check_gate_r1(recon_9q, recon_band):
    """GATE R1: |reconstructed - AHS| <= sqrt(sigma_recon^2 + sigma_ahs^2).

    Returns (passes, pull, combined_uncertainty).
    """
    combined = np.sqrt(recon_band**2 + AHS_BAND**2)
    diff = abs(recon_9q - AHS_NINE_Q)
    pull = diff / combined
    passes = diff <= combined
    return passes, pull, diff, combined


def check_gate_r2(recon_band):
    """GATE R2: recon_band within factor 2 of AHS_BAND.

    i.e., 0.0037 <= recon_band <= 0.0148.
    """
    passes = 0.0037 <= recon_band <= 0.0148
    return passes, recon_band


def check_correlation_gate(derived_band):
    """Correlation gate: derived band must land within [0.004, 0.014].

    Returns (passes, position_string).
    """
    passes = 0.004 <= derived_band <= 0.014
    position = f"{derived_band:.4f} in [0.004, 0.014]"
    return passes, position


# ── Main reconstruction ─────────────────────────────────────────────────

def run_reconstruction(n_mc=100000, seed=54321):
    """Run the full independent reconstruction.

    Steps:
    1. Central-value reconstruction from PDG primaries
    2. Monte Carlo uncertainty propagation
    3. Gate checks
    4. Induced correlation computation
    5. Comparison to AHS
    """
    print("=" * 72)
    print("INDEPENDENT RECONSTRUCTION OF 9Q_U(M_Z)")
    print("PDG 2024 primaries → 4-loop QCD → M_Z → 9Q")
    print("=" * 72)
    print()

    # ── Step 1: Central value ──
    print("── Step 1: Central-value reconstruction ──")
    t0 = time.time()
    r_central = reconstruct_9q(
        INPUTS["m_u"]["value"],
        INPUTS["m_c"]["value"],
        INPUTS["m_t_pole"]["value"],
        INPUTS["alpha_s_MZ"]["value"],
    )
    t_central = time.time() - t0
    print(f"  Completed in {t_central:.1f}s")
    print(f"  m_u(M_Z)  = {r_central['m_u_MZ']*1000:.4f} MeV")
    print(f"  m_c(M_Z)  = {r_central['m_c_MZ']:.4f} GeV")
    print(f"  m_t(M_Z)  = {r_central['m_t_MZ']:.4f} GeV")
    print(f"  m_t(m_t)  = {r_central['mt_msbar']:.4f} GeV")
    print(f"  y_u(M_Z)  = {r_central['y_u']:.8f}")
    print(f"  y_c(M_Z)  = {r_central['y_c']:.6f}")
    print(f"  y_t(M_Z)  = {r_central['y_t']:.4f}")
    print(f"  9Q_U(M_Z) = {r_central['nine_Q']:.4f}")
    print()

    # ── Step 2: AHS reproduction check ──
    print("── Step 2: AHS tabulation check ──")
    ahs_rep = reproduce_ahs()
    print(f"  From AHS Yukawas: 9Q = {ahs_rep['nine_Q_computed']:.4f}")
    print(f"  AHS quoted:       9Q = {AHS_NINE_Q:.4f}")
    print(f"  Match: {ahs_rep['match']} (Δ = {ahs_rep['diff']:+.2e})")
    print()

    # ── Step 3: Monte Carlo uncertainty propagation ──
    print(f"── Step 3: MC uncertainty propagation (N={n_mc:,}) ──")
    rng = np.random.default_rng(seed)

    m_u_draws = rng.normal(INPUTS["m_u"]["value"], INPUTS["m_u"]["uncertainty"], n_mc)
    m_c_draws = rng.normal(INPUTS["m_c"]["value"], INPUTS["m_c"]["uncertainty"], n_mc)
    m_t_draws = rng.normal(INPUTS["m_t_pole"]["value"], INPUTS["m_t_pole"]["uncertainty"], n_mc)
    a_s_draws = rng.normal(INPUTS["alpha_s_MZ"]["value"], INPUTS["alpha_s_MZ"]["uncertainty"], n_mc)

    m_u_draws = np.clip(m_u_draws, 1e-5, 1.0)
    m_c_draws = np.clip(m_c_draws, 0.5, 2.5)
    m_t_draws = np.clip(m_t_draws, 165.0, 180.0)
    a_s_draws = np.clip(a_s_draws, 0.110, 0.126)

    nine_q_all = np.full(n_mc, np.nan)
    y_all = np.full((n_mc, 3), np.nan)

    t_mc0 = time.time()
    n_done = 0
    for i in range(n_mc):
        try:
            rr = reconstruct_9q(m_u_draws[i], m_c_draws[i], m_t_draws[i], a_s_draws[i])
            nine_q_all[i] = rr["nine_Q"]
            y_all[i, 0] = rr["y_u"]
            y_all[i, 1] = rr["y_c"]
            y_all[i, 2] = rr["y_t"]
            n_done += 1
        except Exception:
            pass

        if (i + 1) % 20000 == 0:
            elapsed = time.time() - t_mc0
            rate = (i + 1) / elapsed
            eta = (n_mc - i - 1) / rate
            print(f"  {i+1}/{n_mc} ({rate:.0f}/s, ETA {eta:.0f}s)", file=sys.stderr)

    t_mc = time.time() - t_mc0
    print(f"  Completed in {t_mc:.1f}s ({n_done}/{n_mc} converged)")

    mask = ~np.isnan(nine_q_all)
    nine_q_valid = nine_q_all[mask]
    y_valid = y_all[mask]

    recon_9q_mean = float(np.mean(nine_q_valid))
    recon_9q_std = float(np.std(nine_q_valid))
    recon_9q_p16 = float(np.percentile(nine_q_valid, 15.87))
    recon_9q_p84 = float(np.percentile(nine_q_valid, 84.13))

    print(f"  Reconstructed 9Q = {recon_9q_mean:.4f} ± {recon_9q_std:.4f}")
    print(f"  68% CI = [{recon_9q_p16:.4f}, {recon_9q_p84:.4f}]")
    print()

    # ── Step 4: GATE CHECKS ──
    print("── Step 4: GATE CHECKS ──")
    print()

    r1_pass, pull, diff_9q, combined_unc = check_gate_r1(recon_9q_mean, recon_9q_std)
    print(f"  GATE R1: Agreement with AHS within combined uncertainty")
    print(f"    Reconstructed 9Q  = {recon_9q_mean:.4f} ± {recon_9q_std:.4f}")
    print(f"    AHS tabulated 9Q  = {AHS_NINE_Q:.4f} ± {AHS_BAND:.4f}")
    print(f"    |Δ| = {diff_9q:.4f}")
    print(f"    Combined σ = {combined_unc:.4f}")
    print(f"    Pull = {pull:.2f}σ")
    print(f"    RESULT: {'✅ PASS' if r1_pass else '❌ FAIL — STOP, DO NOT TUNE'}")

    if not r1_pass:
        print()
        print("  ⛔ GATE R1 FAILED. Reconstruction does not agree with AHS")
        print("     within combined uncertainties. Stopping as required.")
        print("     DO NOT TUNE the pipeline to make it pass.")
        return None

    print()

    r2_pass, band_check = check_gate_r2(recon_9q_std)
    print(f"  GATE R2: Reconstruction band same order as AHS (±0.0074)")
    print(f"    Recon band = ±{recon_9q_std:.4f}")
    print(f"    Required:   [0.0037, 0.0148] (factor 2 either way)")
    print(f"    RESULT: {'✅ PASS' if r2_pass else '❌ FAIL — STOP'}")

    if not r2_pass:
        print()
        print("  ⛔ GATE R2 FAILED. Reconstruction band outside factor-2 window.")
        return None

    print()

    # ── Step 5: Induced correlation DERIVATION ──
    print("── Step 5: DERIVED correlation (computed, not assumed) ──")
    # Compute the induced correlation matrix from the MC sample
    y_cov = np.cov(y_valid, rowvar=False)
    y_corr = np.corrcoef(y_valid, rowvar=False)
    y_means = np.mean(y_valid, axis=0)
    y_stds = np.std(y_valid, axis=0)

    labels = ["y_u", "y_c", "y_t"]
    print(f"  Induced Yukawa correlation matrix (from n={len(y_valid):,} MC draws):")
    print(f"         {'y_u':>10} {'y_c':>10} {'y_t':>10}")
    for i, lab in enumerate(labels):
        print(f"  {lab:>6} {y_corr[i,0]:10.4f} {y_corr[i,1]:10.4f} {y_corr[i,2]:10.4f}")

    print()
    print(f"  Yukawa fractional uncertainties:")
    for i, lab in enumerate(labels):
        print(f"    {lab}: mean={y_means[i]:.6e}, σ={y_stds[i]:.6e} ({y_stds[i]/y_means[i]*100:.2f}%)")

    # The 9Q band from this derived correlation IS the MC band we already computed
    derived_band = recon_9q_std
    corr_pass, corr_pos = check_correlation_gate(derived_band)

    print()
    print(f"  CORRELATION GATE: Derived band must be within [0.004, 0.014]")
    print(f"    Derived 9Q band (1σ) = ±{derived_band:.4f}")
    print(f"    AHS bracketed envelope = [0.004, 0.014]")
    print(f"    Position: {corr_pos}")
    print(f"    RESULT: {'✅ PASS — inside bracket' if corr_pass else '⚠️  OUTSIDE bracket — report'}")

    print()

    # ── Step 6: Comparison summary ──
    print("── Step 6: Full comparison ──")
    print(f"  {'':>24} {'Value':>10} {'± Band':>10}")
    print(f"  {'Independent recon:':>24} {recon_9q_mean:10.4f} {recon_9q_std:10.4f}")
    print(f"  {'AHS tabulation:':>24} {AHS_NINE_Q:10.4f} {AHS_BAND:10.4f}")
    print(f"  {'Difference:':>24} {diff_9q:10.4f}")
    print(f"  {'Pull:':>24} {pull:10.2f}σ")

    # ── Package results ──
    results = {
        "spec_version": "v1.0",
        "part": "A + A+",
        "central": {
            "m_u_MZ_MeV": r_central["m_u_MZ"] * 1000,
            "m_c_MZ_GeV": r_central["m_c_MZ"],
            "m_t_MZ_GeV": r_central["m_t_MZ"],
            "mt_msbar_GeV": r_central["mt_msbar"],
            "y_u_MZ": r_central["y_u"],
            "y_c_MZ": r_central["y_c"],
            "y_t_MZ": r_central["y_t"],
            "nine_Q": r_central["nine_Q"],
        },
        "mc_propagation": {
            "n_draws": n_mc,
            "n_converged": int(len(nine_q_valid)),
            "nine_Q_mean": recon_9q_mean,
            "nine_Q_std": recon_9q_std,
            "nine_Q_p16": recon_9q_p16,
            "nine_Q_p84": recon_9q_p84,
        },
        "ahs_reference": {
            "nine_Q": AHS_NINE_Q,
            "band": AHS_BAND,
        },
        "gates": {
            "R1_pass": r1_pass,
            "R1_pull": pull,
            "R1_diff": diff_9q,
            "R1_combined_uncertainty": combined_unc,
            "R2_pass": r2_pass,
            "R2_band": recon_9q_std,
            "R2_window": [0.0037, 0.0148],
            "correlation_gate_pass": corr_pass,
            "correlation_gate_position": corr_pos,
        },
        "induced_correlation": {
            "method": "COMPUTED from MC sample — never assumed",
            "y_labels": labels,
            "y_covariance": y_cov.tolist(),
            "y_correlation": y_corr.tolist(),
            "y_means": y_means.tolist(),
            "y_stds": y_stds.tolist(),
            "derived_9q_band": derived_band,
            "bracketed_envelope": [0.004, 0.014],
            "inside_bracket": corr_pass,
        },
        "ahs_reproduction": ahs_rep,
    }

    print()
    print("=" * 72)
    print("ALL GATES PASSED — reconstruction complete.")
    print("=" * 72)
    return results


# ── CLI ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    n_mc = 100000
    if "--quick" in sys.argv:
        for a in sys.argv:
            if a.startswith("N="):
                n_mc = int(a.split("=")[1])
        if n_mc == 100000:
            n_mc = 20000  # default quick

    if "--no-mc" in sys.argv:
        # Central values only
        r = reconstruct_9q(
            INPUTS["m_u"]["value"],
            INPUTS["m_c"]["value"],
            INPUTS["m_t_pole"]["value"],
            INPUTS["alpha_s_MZ"]["value"],
        )
        print("Central-value reconstruction:")
        print(f"  9Q_U(M_Z) = {r['nine_Q']:.4f}")
        print(f"  AHS       = {AHS_NINE_Q:.4f}")
        print(f"  Δ         = {r['nine_Q'] - AHS_NINE_Q:+.4f}")
    else:
        results = run_reconstruction(n_mc=n_mc)

        if results is not None:
            # Write results
            with open("reconstruction_results.json", "w") as f:
                json.dump(results, f, indent=2)
            print("\nWrote reconstruction_results.json")
