#!/usr/bin/env python3
"""Extract PDG 2024 primary inputs with full citation detail.

All values come from PDG 2024 (Phys. Rev. D 110, 030001).
These are INDEPENDENT of the AHS tabulation — they are the raw PDG inputs,
not taken from any intermediate processing.

Usage:
    python3 extract_inputs.py           # print the input table
    python3 extract_inputs.py --json    # machine-readable JSON
"""
import json
import sys

# ── Primary PDG 2024 inputs ─────────────────────────────────────────────
# All masses in GeV; all are MSbar at the stated scale unless noted.

INPUTS = {
    "m_u": {
        "value": 0.00216,       # GeV = 2.16 MeV
        "uncertainty": 0.00007,  # ±0.07 MeV
        "scale_GeV": 2.0,
        "scheme": "MSbar",
        "nf": 3,
        "description": "Up-quark MSbar mass at 2 GeV",
        "source": "PDG 2024 Table 72.1, FLAG 2021 lattice average",
    },
    "m_c": {
        "value": 1.2730,
        "uncertainty": 0.0046,
        "scale_GeV": 1.2730,  # m_c(m_c) — running mass at its own scale
        "scheme": "MSbar",
        "nf": 4,
        "description": "Charm-quark MSbar mass at m_c(m_c)",
        "source": "PDG 2024 Table 72.1",
    },
    "m_t_pole": {
        "value": 172.4,
        "uncertainty": 0.7,
        "scale_GeV": 172.4,
        "scheme": "pole",
        "nf": 5,
        "description": "Top-quark pole mass (cross-section average)",
        "source": "PDG 2024 Table 72.1, cross-section measurement average",
    },
    "alpha_s_MZ": {
        "value": 0.1180,
        "uncertainty": 0.0009,
        "scale_GeV": 91.1876,
        "scheme": "MSbar",
        "nf": 5,
        "description": "Strong coupling at M_Z (world average)",
        "source": "PDG 2024 QCD review (S. Bethke et al.)",
    },
    "m_b": {
        "value": 4.183,
        "uncertainty": 0.007,
        "scale_GeV": 4.183,
        "scheme": "MSbar",
        "nf": 5,
        "description": "Bottom-quark MSbar mass at m_b(m_b), for flavour threshold",
        "source": "PDG 2024 Table 72.1; used for threshold location only",
    },
}

# Physical constants
CONSTANTS = {
    "G_F_GeV": 1.1663788e-5,
    "M_Z_GeV": 91.1876,
    "VEV_GeV": 246.21971,  # (sqrt(2)*G_F)^(-1/2)
}

# AHS reference values (target, NOT input)
AHS = {
    "nine_Q_MZ": 7.9886,
    "band": 0.0074,
    "y_u_MZ": 7.04e-6,
    "y_c_MZ": 0.00356,
    "y_t_MZ": 0.967,
}


def print_table():
    """Human-readable input table."""
    print("PDG 2024 Primary Inputs for Independent Reconstruction")
    print("=" * 72)
    print(f"{'Parameter':<16} {'Value':>12} {'±':>10} {'Scale':>10}  {'nf':>3}  Source")
    print("-" * 72)
    for key, d in INPUTS.items():
        name = {"m_u": "m_u(2 GeV)", "m_c": "m_c(m_c)", "m_t_pole": "m_t(pole)",
                "alpha_s_MZ": "α_s(M_Z)", "m_b": "m_b(m_b)"}[key]
        unit = "GeV" if key != "alpha_s_MZ" else ""
        val_str = f"{d['value']:.4f} {unit}" if key != 'm_u' else f"{d['value']*1000:.2f} MeV"
        unc_str = f"±{d['uncertainty']:.4f} {unit}" if key != 'm_u' else f"±{d['uncertainty']*1000:.2f} MeV"
        scale_str = f"{d['scale_GeV']:.1f} GeV" if key != 'alpha_s_MZ' else "M_Z"
        if key == 'm_c':
            scale_str = f"m_c ({d['scale_GeV']:.3f} GeV)"
        if key == 'm_b':
            scale_str = f"m_b ({d['scale_GeV']:.3f} GeV)"
        print(f"{name:<16} {val_str:>12} {unc_str:>10} {scale_str:>10}  {d['nf']:>3}  {d['source']}")

    print()
    print("Physical Constants:")
    print(f"  G_F = {CONSTANTS['G_F_GeV']:.7e} GeV⁻²")
    print(f"  M_Z = {CONSTANTS['M_Z_GeV']:.4f} GeV")
    print(f"  v   = {CONSTANTS['VEV_GeV']:.6f} GeV  (from G_F)")
    print()
    print("AHS Reference (target, NOT input):")
    print(f"  9Q_U(M_Z) = {AHS['nine_Q_MZ']:.4f} ± {AHS['band']:.4f}")
    print(f"  y_u(M_Z)  = {AHS['y_u_MZ']:.2e}")
    print(f"  y_c(M_Z)  = {AHS['y_c_MZ']:.6f}")
    print(f"  y_t(M_Z)  = {AHS['y_t_MZ']:.4f}")


def as_dict():
    """Return inputs as a plain dict suitable for JSON serialization."""
    return {"inputs": INPUTS, "constants": CONSTANTS, "ahs_reference": AHS}


if __name__ == "__main__":
    if "--json" in sys.argv:
        json.dump(as_dict(), sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_table()
