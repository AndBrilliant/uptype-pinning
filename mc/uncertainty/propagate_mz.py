#!/usr/bin/env python3
"""Mass propagation to M_Z with full uncertainty propagation.

Propagates PDG 2024 primary inputs through the QCD running pipeline to M_Z,
computing the resulting Yukawa couplings and 9Q_U(M_Z) with uncertainties.

Usage:
    python3 propagate_mz.py               # single-point propagation
    python3 propagate_mz.py --mc N=100000  # Monte Carlo uncertainty propagation
    python3 propagate_mz.py --ahs          # reproduce AHS tabulation
"""
import sys
import json
import time
import numpy as np

from qcd import reconstruct_9q, VEV, SQRT2, masses_to_yukawas, compute_9q
from extract_inputs import INPUTS, AHS


def single_point():
    """Run the pipeline at the PDG central values."""
    r = reconstruct_9q(
        INPUTS["m_u"]["value"],
        INPUTS["m_c"]["value"],
        INPUTS["m_t_pole"]["value"],
        INPUTS["alpha_s_MZ"]["value"],
    )
    r["ahs_9q"] = AHS["nine_Q_MZ"]
    r["diff"] = r["nine_Q"] - AHS["nine_Q_MZ"]
    return r


def mc_propagation(n_draws=100000, seed=42):
    """Monte Carlo propagation of PDG input uncertainties.

    Draws the four primary inputs from independent Gaussians,
    runs the full pipeline for each draw, and returns the
    distribution of 9Q_U(M_Z) and the Yukawa couplings.
    """
    rng = np.random.default_rng(seed)

    # Draw inputs
    m_u = rng.normal(INPUTS["m_u"]["value"], INPUTS["m_u"]["uncertainty"], n_draws)
    m_c = rng.normal(INPUTS["m_c"]["value"], INPUTS["m_c"]["uncertainty"], n_draws)
    m_t = rng.normal(INPUTS["m_t_pole"]["value"], INPUTS["m_t_pole"]["uncertainty"], n_draws)
    alphas = rng.normal(INPUTS["alpha_s_MZ"]["value"], INPUTS["alpha_s_MZ"]["uncertainty"], n_draws)

    # Clip to physically sensible ranges
    m_u = np.clip(m_u, 1e-5, 1.0)       # m_u in [0.01 MeV, 1 GeV]
    m_c = np.clip(m_c, 0.5, 2.5)        # m_c in [0.5, 2.5] GeV
    m_t = np.clip(m_t, 165.0, 180.0)    # m_t in [165, 180] GeV
    alphas = np.clip(alphas, 0.110, 0.126)  # α_s in sensible range

    results = {
        "nine_Q": np.zeros(n_draws),
        "y_u": np.zeros(n_draws),
        "y_c": np.zeros(n_draws),
        "y_t": np.zeros(n_draws),
        "m_u_MZ": np.zeros(n_draws),
        "m_c_MZ": np.zeros(n_draws),
        "m_t_MZ": np.zeros(n_draws),
    }

    t0 = time.time()
    for i in range(n_draws):
        try:
            r = reconstruct_9q(m_u[i], m_c[i], m_t[i], alphas[i])
            results["nine_Q"][i] = r["nine_Q"]
            results["y_u"][i] = r["y_u"]
            results["y_c"][i] = r["y_c"]
            results["y_t"][i] = r["y_t"]
            results["m_u_MZ"][i] = r["m_u_MZ"]
            results["m_c_MZ"][i] = r["m_c_MZ"]
            results["m_t_MZ"][i] = r["m_t_MZ"]
        except Exception:
            results["nine_Q"][i] = np.nan
            results["y_u"][i] = np.nan
            results["y_c"][i] = np.nan
            results["y_t"][i] = np.nan

        if (i + 1) % 10000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (n_draws - i - 1) / rate
            print(f"  {i+1}/{n_draws} draws ({rate:.0f}/s, ETA {eta:.0f}s)", file=sys.stderr)

    # Remove failed draws
    mask = ~np.isnan(results["nine_Q"])
    for k in results:
        results[k] = results[k][mask]

    n_good = mask.sum()
    print(f"  {n_good}/{n_draws} draws converged", file=sys.stderr)

    # Compute statistics
    stats = {}
    for key in ["nine_Q", "y_u", "y_c", "y_t"]:
        vals = results[key]
        stats[key] = {
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals)),
            "median": float(np.median(vals)),
            "p16": float(np.percentile(vals, 15.87)),
            "p84": float(np.percentile(vals, 84.13)),
        }

    # Induced covariance / correlation of Yukawa couplings
    Y = np.column_stack([results["y_u"], results["y_c"], results["y_t"]])
    cov = np.cov(Y, rowvar=False)
    corr = np.corrcoef(Y, rowvar=False)

    stats["y_covariance"] = cov.tolist()
    stats["y_correlation"] = corr.tolist()
    stats["y_labels"] = ["y_u", "y_c", "y_t"]
    stats["n_draws"] = n_draws
    stats["n_converged"] = int(n_good)

    return stats, results


def ahs_reproduction():
    """Reproduce the AHS tabulation using the AHS Yukawa couplings."""
    y_ahs = np.array([AHS["y_u_MZ"], AHS["y_c_MZ"], AHS["y_t_MZ"]])
    nine_q_ahs = compute_9q(y_ahs)
    print(f"AHS Yukawas: y_u={y_ahs[0]:.8f}, y_c={y_ahs[1]:.6f}, y_t={y_ahs[2]:.4f}")
    print(f"9Q_U(M_Z) from AHS Yukawas: {nine_q_ahs:.4f}")
    print(f"AHS quoted: 7.9886")
    return nine_q_ahs


def print_stats(stats):
    """Print Monte Carlo statistics."""
    print()
    print("=" * 72)
    print("Monte Carlo Propagation Results")
    print("=" * 72)
    print(f"Draws: {stats['n_draws']:,} requested, {stats['n_converged']:,} converged")
    print()
    for key, label in [("nine_Q", "9Q_U(M_Z)"), ("y_u", "y_u(M_Z)"), ("y_c", "y_c(M_Z)"), ("y_t", "y_t(M_Z)")]:
        s = stats[key]
        print(f"{label}:")
        print(f"  mean   = {s['mean']:.6f}")
        print(f"  std    = {s['std']:.6f}")
        print(f"  median = {s['median']:.6f}")
        print(f"  68% CI = [{s['p16']:.6f}, {s['p84']:.6f}]")
        print()

    print("Induced Yukawa Correlation Matrix:")
    corr = np.array(stats["y_correlation"])
    labels = stats["y_labels"]
    print(f"        {'':>8} {'y_u':>10} {'y_c':>10} {'y_t':>10}")
    for i, label in enumerate(labels):
        print(f"        {label:>8} {corr[i,0]:10.4f} {corr[i,1]:10.4f} {corr[i,2]:10.4f}")

    print()
    band = stats["nine_Q"]["std"]
    print(f"Derived 9Q band (1σ): ±{band:.4f}")
    print(f"AHS quoted band:     ±0.0074")
    print(f"Ratio: {band/0.0074:.2f}")


if __name__ == "__main__":
    if "--mc" in sys.argv:
        n_str = [a for a in sys.argv if a.startswith("--mc")][0]
        n = int(n_str.split("=")[-1]) if "=" in n_str else 100000
        stats, results = mc_propagation(n_draws=n)
        print_stats(stats)
        if "--json" in sys.argv:
            # Save statistics only (not raw results — those are large)
            with open("propagation_stats.json", "w") as f:
                json.dump(stats, f, indent=2)
            print("\nWrote propagation_stats.json")
    elif "--ahs" in sys.argv:
        ahs_reproduction()
    else:
        r = single_point()
        print("Single-point propagation (PDG 2024 central values):")
        print(f"  m_u(M_Z)  = {r['m_u_MZ']*1000:.4f} MeV")
        print(f"  m_c(M_Z)  = {r['m_c_MZ']:.4f} GeV")
        print(f"  m_t(M_Z)  = {r['m_t_MZ']:.4f} GeV")
        print(f"  m_t(m_t)  = {r['mt_msbar']:.4f} GeV")
        print(f"  y_u(M_Z)  = {r['y_u']:.8f}")
        print(f"  y_c(M_Z)  = {r['y_c']:.6f}")
        print(f"  y_t(M_Z)  = {r['y_t']:.4f}")
        print(f"  9Q_U(M_Z) = {r['nine_Q']:.4f}")
        print(f"  AHS 9Q    = {AHS['nine_Q_MZ']:.4f}")
        print(f"  Δ(9Q)     = {r['diff']:+.4f}")
