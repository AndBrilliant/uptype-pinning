#!/usr/bin/env python3
"""Correlation stress test for the 9Q_U(M_Z) band.

Explores the full correlation envelope: how the uncertainty on 9Q_U(M_Z)
varies as the input correlations span from fully-correlated to
anti-correlated (where the sensitivity signs permit).

Also computes the INDUCED correlation of (y_u, y_c, y_t) at M_Z from
independent PDG primaries — this correlation is not assumed; it emerges
from the shared α_s dependence in the QCD running.

Usage:
    python3 correlation_stress.py              # full analysis
    python3 correlation_stress.py --quick N=10000  # quick test
"""
import sys
import json
import time
import numpy as np

from qcd import reconstruct_9q
from extract_inputs import INPUTS, AHS


def correlation_envelope(n_draws=100000, seed=12345):
    """Compute the 9Q band under different input correlation assumptions.

    Returns three scenarios:
      - independent:   all inputs uncorrelated (baseline)
      - fully_corr:    all inputs perfectly correlated (widest band)
      - anti_corr:     inputs anti-correlated where possible (narrowest band)

    Note: "fully correlated" means all input random variables move together
    in units of their standard deviation. The anti-correlated scenario
    uses signs that minimize 9Q variance (determined by the sensitivity
    derivatives).
    """
    rng = np.random.default_rng(seed)

    # Base normal draws (standardized)
    z_u = rng.normal(0, 1, n_draws)
    z_c = rng.normal(0, 1, n_draws)
    z_t = rng.normal(0, 1, n_draws)
    z_a = rng.normal(0, 1, n_draws)

    central = {
        "m_u": INPUTS["m_u"]["value"], "m_u_err": INPUTS["m_u"]["uncertainty"],
        "m_c": INPUTS["m_c"]["value"], "m_c_err": INPUTS["m_c"]["uncertainty"],
        "m_t": INPUTS["m_t_pole"]["value"], "m_t_err": INPUTS["m_t_pole"]["uncertainty"],
        "a_s": INPUTS["alpha_s_MZ"]["value"], "a_s_err": INPUTS["alpha_s_MZ"]["uncertainty"],
    }

    scenarios = {}

    # ── Scenario 1: All inputs independent ──
    print("Scenario 1/4: independent inputs ...", file=sys.stderr)
    draws_ind = {
        "m_u": central["m_u"] + z_u * central["m_u_err"],
        "m_c": central["m_c"] + z_c * central["m_c_err"],
        "m_t": central["m_t"] + z_t * central["m_t_err"],
        "a_s": central["a_s"] + z_a * central["a_s_err"],
    }
    nine_q_ind = _eval_draws(draws_ind, n_draws)
    scenarios["independent"] = _stats(nine_q_ind, "Independent inputs")

    # ── Scenario 2: Fully correlated (all move together) ──
    print("Scenario 2/4: fully correlated ...", file=sys.stderr)
    z_common = rng.normal(0, 1, n_draws)
    draws_full = {
        "m_u": central["m_u"] + z_common * central["m_u_err"],
        "m_c": central["m_c"] + z_common * central["m_c_err"],
        "m_t": central["m_t"] + z_common * central["m_t_err"],
        "a_s": central["a_s"] + z_common * central["a_s_err"],
    }
    nine_q_full = _eval_draws(draws_full, n_draws)
    scenarios["fully_correlated"] = _stats(nine_q_full, "Fully correlated inputs")

    # ── Scenario 3: Anti-correlated (minimize 9Q variance) ──
    # The sensitivity signs: ∂(9Q)/∂m_c > 0, ∂(9Q)/∂m_t < 0, ∂(9Q)/∂m_u ~ 0
    # Anti-correlating m_c and m_t reduces the 9Q spread
    print("Scenario 3/4: anti-correlated (m_c vs m_t) ...", file=sys.stderr)
    draws_anti = {
        "m_u": central["m_u"] + z_u * central["m_u_err"],
        "m_c": central["m_c"] + z_c * central["m_c_err"],
        "m_t": central["m_t"] - z_c * central["m_t_err"],  # anti-correlated with m_c
        "a_s": central["a_s"] + z_a * central["a_s_err"],  # independent α_s
    }
    nine_q_anti = _eval_draws(draws_anti, n_draws)
    scenarios["anticorrelated"] = _stats(nine_q_anti, "Anti-correlated (m_c↔m_t)")

    # ── Scenario 4: Induced-only (PDG independent → correlated outputs) ──
    print("Scenario 4/4: computing induced Yukawa correlations ...", file=sys.stderr)
    # This scenario is the SAME as independent inputs but we extract the
    # induced output correlations. Run at higher statistics.
    induced = compute_induced_correlation(draws_ind, n_draws)
    scenarios["induced_yukawa_corr"] = induced

    return scenarios


def compute_induced_correlation(draws_input, n_draws):
    """Compute the induced correlation of (y_u, y_c, y_t) at M_Z.

    Even with independent input uncertainties, the outputs are correlated
    because all three Yukawas share the α_s dependence in the QCD running.
    """
    # We already have the draws; re-evaluate with the Yukawa outputs
    y_u_arr = np.zeros(n_draws)
    y_c_arr = np.zeros(n_draws)
    y_t_arr = np.zeros(n_draws)
    nine_q_arr = np.zeros(n_draws)

    m_u = np.clip(draws_input["m_u"], 1e-5, 1.0)
    m_c = np.clip(draws_input["m_c"], 0.5, 2.5)
    m_t = np.clip(draws_input["m_t"], 165.0, 180.0)
    a_s = np.clip(draws_input["a_s"], 0.110, 0.126)

    t0 = time.time()
    for i in range(n_draws):
        try:
            r = reconstruct_9q(m_u[i], m_c[i], m_t[i], a_s[i])
            y_u_arr[i] = r["y_u"]
            y_c_arr[i] = r["y_c"]
            y_t_arr[i] = r["y_t"]
            nine_q_arr[i] = r["nine_Q"]
        except Exception:
            y_u_arr[i] = np.nan

        if (i + 1) % 20000 == 0:
            elapsed = time.time() - t0
            print(f"  induced corr: {i+1}/{n_draws} ({n_draws/(i+1)*elapsed:.0f}s elapsed)", file=sys.stderr)

    mask = ~np.isnan(y_u_arr)
    Y = np.column_stack([y_u_arr[mask], y_c_arr[mask], y_t_arr[mask]])
    cov = np.cov(Y, rowvar=False)
    corr = np.corrcoef(Y, rowvar=False)

    # Standard deviations (relative, in percent)
    rel_std = np.std(Y, axis=0) / np.mean(Y, axis=0) * 100

    # Band on 9Q from independent inputs
    nine_q_std = np.std(nine_q_arr[mask])

    return {
        "description": "Induced Yukawa correlation from independent PDG primaries",
        "y_covariance": cov.tolist(),
        "y_correlation": corr.tolist(),
        "y_labels": ["y_u", "y_c", "y_t"],
        "y_means": np.mean(Y, axis=0).tolist(),
        "y_std": np.std(Y, axis=0).tolist(),
        "y_rel_std_pct": rel_std.tolist(),
        "nine_Q_std": float(nine_q_std),
        "nine_Q_band_1sigma": float(nine_q_std),
        "ahs_band": AHS["band"],
        "within_bracket": 0.004 <= nine_q_std <= 0.014,
        "bracket_position": f"{nine_q_std:.4f} in [0.004, 0.014]",
    }


def _eval_draws(draws, n_draws):
    """Evaluate 9Q for a set of input draws."""
    m_u = np.clip(draws["m_u"], 1e-5, 1.0)
    m_c = np.clip(draws["m_c"], 0.5, 2.5)
    m_t = np.clip(draws["m_t"], 165.0, 180.0)
    a_s = np.clip(draws["a_s"], 0.110, 0.126)

    nine_q = np.full(n_draws, np.nan)
    t0 = time.time()
    for i in range(n_draws):
        try:
            r = reconstruct_9q(m_u[i], m_c[i], m_t[i], a_s[i])
            nine_q[i] = r["nine_Q"]
        except Exception:
            pass
        if (i + 1) % 20000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            print(f"    {i+1}/{n_draws} ({rate:.0f}/s)", file=sys.stderr)
    return nine_q[~np.isnan(nine_q)]


def _stats(arr, label):
    """Compute summary statistics."""
    std = float(np.std(arr))
    return {
        "label": label,
        "mean": float(np.mean(arr)),
        "std": std,
        "band_1sigma": std,
        "p16": float(np.percentile(arr, 15.87)),
        "p84": float(np.percentile(arr, 84.13)),
        "n": len(arr),
        "within_factor2_of_ahs": 0.0037 <= std <= 0.0148,
    }


def print_report(scenarios):
    """Print the correlation stress report."""
    print()
    print("=" * 72)
    print("CORRELATION STRESS REPORT")
    print("=" * 72)
    print(f"AHS quoted 9Q_U(M_Z) = {AHS['nine_Q_MZ']:.4f} ± {AHS['band']:.4f}")
    print(f"GATE R2: band must be within factor 2 of 0.0074 → [0.0037, 0.0148]")
    print()

    for key, s in scenarios.items():
        if key == "induced_yukawa_corr":
            continue
        gate_str = "PASS" if s["within_factor2_of_ahs"] else "FAIL"
        print(f"  {s['label']}:")
        print(f"    9Q mean = {s['mean']:.4f}, 1σ band = ±{s['std']:.4f}")
        print(f"    68% CI  = [{s['p16']:.4f}, {s['p84']:.4f}]")
        print(f"    GATE R2: {gate_str} (band {s['std']:.4f} in [0.0037,0.0148])")
        print()

    # Induced correlation
    ind = scenarios["induced_yukawa_corr"]
    print("─" * 72)
    print("INDUCED YUKAWA CORRELATION (from independent PDG primaries)")
    print("─" * 72)
    corr = np.array(ind["y_correlation"])
    labels = ind["y_labels"]
    print(f"  Correlation matrix:")
    print(f"         {'y_u':>10} {'y_c':>10} {'y_t':>10}")
    for i, lab in enumerate(labels):
        print(f"  {lab:>6} {corr[i,0]:10.4f} {corr[i,1]:10.4f} {corr[i,2]:10.4f}")

    print(f"\n  Yukawa means:   y_u={ind['y_means'][0]:.8f}, y_c={ind['y_means'][1]:.6f}, y_t={ind['y_means'][2]:.4f}")
    print(f"  Yukawa rel std:  {ind['y_rel_std_pct'][0]:.2f}%, {ind['y_rel_std_pct'][1]:.2f}%, {ind['y_rel_std_pct'][2]:.2f}%")
    print(f"\n  Derived 9Q band (1σ from induced correlation): ±{ind['nine_Q_band_1sigma']:.4f}")
    print(f"  AHS quoted band:                                 ±{AHS['band']:.4f}")
    print(f"  Within bracketed envelope [0.004, 0.014]?       {ind['within_bracket']}")
    print(f"  Position: {ind['bracket_position']}")
    print()
    print("NOTE: This correlation is COMPUTED from the MC sample, not assumed.")
    print("It arises from the shared α_s dependence in QCD running + threshold matching.")


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    n = 10000 if quick else 100000
    if "--quick" in sys.argv:
        n_str = [a for a in sys.argv if a.startswith("N=")]
        if n_str:
            n = int(n_str[0].split("=")[1])
    print(f"Running correlation stress with N={n:,} draws ...", file=sys.stderr)
    scenarios = correlation_envelope(n_draws=n)
    print_report(scenarios)

    if "--json" in sys.argv or "--save" in sys.argv:
        with open("correlation_stress.json", "w") as f:
            json.dump(scenarios, f, indent=2, default=str)
        print("\nWrote correlation_stress.json")
