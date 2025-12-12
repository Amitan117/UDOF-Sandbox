#!/usr/bin/env python3
"""
Test script for integrated Lagrangian module.
"""

from lagrangian_cdqf_updated import CDQFLagrangian, create_lagrangian_from_locks
import sys
from pathlib import Path
import numpy as np

# Add integrated_modules to path
sys.path.insert(0, str(Path(__file__).parent / "integrated_modules"))


# v4.0 runner default locks
LOCKS = {
    "cosmology": {
        "H0": 70.21,
        "Om": 0.3185,
        "Ob": 0.0493,
        "r_d_Mpc": 147.09
    },
    "dark_sector": {
        "Omega_geom_0": 0.3266,
        "alpha_geom": -0.1885,
        "p_op": 0.7577,
        "eta_entropy": 0.0
    }
}


def test_lagrangian():
    """Test Lagrangian module."""
    print("=" * 70)
    print("CDQF LAGRANGIAN INTEGRATION TEST")
    print("=" * 70)
    print()

    # Create Lagrangian from locks
    print("[1] Creating Lagrangian from v4.0 locks...")
    lag = create_lagrangian_from_locks(LOCKS)

    print(f"  H0: {lag.H0:.2f} km/s/Mpc")
    print(f"  Omega_m: {lag.Omega_m:.4f}")
    print(f"  Omega_geom_0: {lag.Omega_geom_0:.4f}")
    print(f"  alpha_geom: {lag.alpha_geom:.4f}")
    print(f"  p_op: {lag.p_op:.4f}")
    print(f"  V0: {lag.V0:.2e} GeV^4")
    print(f"  U0: {lag.U0:.2e} GeV^4")
    print()

    # Test inflation observables
    print("[2] Computing inflation observables...")
    infl_obs = lag.compute_inflation_observables(N_efolds=55.0)
    print(f"  n_s: {infl_obs['n_s']:.4f}")
    print(f"  r: {infl_obs['r']:.6f}")
    print(f"  epsilon: {infl_obs['epsilon']:.6f}")
    print(f"  eta: {infl_obs['eta']:.4f}")
    print()

    # Test w_eff formula
    print("[3] Testing dark energy EOS...")
    w_formula = lag.get_w_eff_formula()
    print(f"  w_eff (formula): {w_formula:.4f}")
    print(
        f"  Expected: -1 - (alpha*p_op)/3 = -1 - ({lag.alpha_geom:.4f}*{lag.p_op:.4f})/3")
    expected = -1.0 - (lag.alpha_geom * lag.p_op) / 3.0
    print(f"  Expected value: {expected:.4f}")
    match_status = "YES" if abs(w_formula - expected) < 1e-6 else "NO"
    print(f"  Match: {match_status}")
    print()

    # Test FRW evolution (lightweight - smaller range for testing)
    print("[4] Testing FRW background evolution...")
    print("  Note: Full ODE integration is complex and may require fine-tuning.")
    print("  For validation purposes, simplified formulas (tested above) are sufficient.")
    try:
        evolution = lag.solve_frw_background(
            a_init=0.1,  # Start from later time for faster, more stable computation
            a_final=1.0,
            n_points=50  # Fewer points for testing
        )
        print(f"  ✅ Evolution computed successfully")
        print(
            f"  Scale factor range: {evolution['a'][0]:.2e} to {evolution['a'][-1]:.2f}")
        print(
            f"  H range: {np.min(evolution['H']):.2e} to {np.max(evolution['H']):.2e} GeV")
        print(
            f"  φ range: {np.min(evolution['phi']):.2e} to {np.max(evolution['phi']):.2e} GeV")
        print(
            f"  χ range: {np.min(evolution['chi']):.2e} to {np.max(evolution['chi']):.2e} GeV")
        print()

        # Test late-time observables
        print("[5] Computing late-time observables from evolution...")
        late_obs = lag.compute_late_time_observables()
        print(f"  H0 (from evolution): {late_obs['H0_km_s_Mpc']:.2f} km/s/Mpc")
        print(f"  w_eff (from evolution): {late_obs['w_eff']:.4f}")
        print(
            f"  H0 match: {'✅' if abs(late_obs['H0_km_s_Mpc'] - lag.H0) < 1.0 else '❌'} (within 1 km/s/Mpc)")
        print(
            f"  w_eff match: {'✅' if abs(late_obs['w_eff'] - w_formula) < 0.1 else '❌'} (within 0.1)")
        print()

    except Exception as e:
        print(f"  ❌ Evolution failed: {e}")
        import traceback
        traceback.print_exc()
        print()

    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_lagrangian()
