#!/usr/bin/env python3
"""
Test Growth Factor Precision at Higher Resolution
===================================================

Check for 0.4% overshoot at z=0 and investigate cause.
"""

import sys
import numpy as np
from pathlib import Path

# Add parent project to path
PROJECT_ROOT = Path("D:/CDQF Prime-0 Physics Engine")
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "boltzmann_mcmc"))

# Test parameters
H0 = 70.21
Omega_m = 0.3185
Omega_b = 0.05
Omega_geom_0 = 0.3266
alpha_geom = -0.1885
p_op = 0.7577

print("=" * 80)
print("TESTING GROWTH FACTOR PRECISION")
print("=" * 80)
print()

# Test 1: Integrated Standalone Version
print("Test 1: ProperGrowthStandalone")
print("-" * 80)

try:
    sys.path.insert(0, str(Path(__file__).parent))
    from integrated_modules import ProperGrowthStandalone

    # Test at different resolutions
    resolutions = [1000, 2000, 5000, 10000]

    for n_points in resolutions:
        growth = ProperGrowthStandalone(
            H0=H0,
            Omega_m=Omega_m,
            Omega_b=Omega_b,
            Omega_geom_0=Omega_geom_0,
            alpha_geom=alpha_geom,
            p_op=p_op,
            a_pivot=0.95,
            beta_ESE=-0.10,
            use_mu_eff=True
        )

        # Force recomputation at this resolution
        growth._growth_computed = False
        z_grid, D_grid = growth.compute_growth_factor_corrected(
            a_init=0.001, n_points=n_points)

        if z_grid is not None and D_grid is not None:
            # Check D(z=0) - should be exactly 1.0
            D_z0 = growth.growth_factor(0.0)
            D_z1 = growth.growth_factor(1.0)

            # Check the actual last value in the array
            D_last = D_grid[-1] if len(D_grid) > 0 else np.nan
            z_last = z_grid[-1] if len(z_grid) > 0 else np.nan

            overshoot = (D_z0 - 1.0) * 100  # Percentage overshoot

            print(f"n_points={n_points:5d}: D(z=0)={D_z0:.8f} (overshoot={overshoot:+.4f}%), "
                  f"D(z=1)={D_z1:.6f}, D_last={D_last:.8f}, z_last={z_last:.6f}")
        else:
            print(f"n_points={n_points:5d}: FAILED")

    print()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    print()

# Test 2: Original ProperCorrectedGrowth (if available)
print("Test 2: Original ProperCorrectedGrowth (for comparison)")
print("-" * 80)

try:
    from cdqf_boltzmann_corrected import ProperCorrectedGrowth

    # Test at different resolutions (if possible)
    growth_orig = ProperCorrectedGrowth(
        H0=H0,
        Omega_m=Omega_m,
        Omega_b=Omega_b,
        Omega_geom_0=Omega_geom_0,
        alpha_geom=alpha_geom,
        p_op=p_op,
        a_pivot=0.95,
        beta_ESE=-0.10,
        use_mu_eff=True
    )

    # Force recomputation
    if hasattr(growth_orig, '_D_growth_corrected'):
        delattr(growth_orig, '_D_growth_corrected')

    # Check what method is called
    # The original uses growth_factor(a) where a = 1/(1+z)
    a0 = 1.0  # z=0
    a1 = 0.5  # z=1

    D_z0_orig = growth_orig.D_corrected(0.0)
    D_z1_orig = growth_orig.D_corrected(1.0)

    # Check if there's direct access to the array
    if hasattr(growth_orig, '_D_growth_corrected'):
        D_grid_orig = growth_orig._D_growth_corrected
        z_grid_orig = growth_orig._z_growth_corrected
        if len(D_grid_orig) > 0:
            D_last_orig = D_grid_orig[-1]
            z_last_orig = z_grid_orig[-1]
        else:
            D_last_orig = np.nan
            z_last_orig = np.nan
    else:
        D_last_orig = np.nan
        z_last_orig = np.nan

    overshoot_orig = (D_z0_orig - 1.0) * 100

    print(f"Original: D(z=0)={D_z0_orig:.8f} (overshoot={overshoot_orig:+.4f}%), "
          f"D(z=1)={D_z1_orig:.6f}")
    if not np.isnan(D_last_orig):
        print(f"          D_last={D_last_orig:.8f}, z_last={z_last_orig:.6f}")
    print()

except Exception as e:
    print(f"Not available: {e}")
    print()

# Test 3: Check interpolation at z=0 boundary
print("Test 3: Interpolation Boundary Check")
print("-" * 80)

try:
    from integrated_modules import ProperGrowthStandalone

    growth = ProperGrowthStandalone(
        H0=H0,
        Omega_m=Omega_m,
        Omega_b=Omega_b,
        Omega_geom_0=Omega_geom_0,
        alpha_geom=alpha_geom,
        p_op=p_op,
        a_pivot=0.95,
        beta_ESE=-0.10,
        use_mu_eff=True
    )

    # Force high resolution
    z_grid, D_grid = growth.compute_growth_factor_corrected(
        a_init=0.001, n_points=5000)

    if z_grid is not None and D_grid is not None:
        # Check values near z=0
        z_test = [0.0, 0.0001, 0.001, 0.01]

        print("Values near z=0:")
        for z in z_test:
            D_val = growth.growth_factor(z)
            # Find closest point in grid
            idx = np.argmin(np.abs(z_grid - z))
            D_grid_val = D_grid[idx] if idx < len(D_grid) else np.nan
            z_grid_val = z_grid[idx] if idx < len(z_grid) else np.nan

            print(f"  z={z:.6f}: D(z)={D_val:.8f}, "
                  f"D_grid[{idx}]={D_grid_val:.8f}, z_grid={z_grid_val:.6f}")

        # Check if z=0 is exactly in the grid
        z0_idx = np.where(np.abs(z_grid) < 1e-10)[0]
        if len(z0_idx) > 0:
            print(f"\n  z=0 found at indices: {z0_idx}")
            for idx in z0_idx:
                print(
                    f"    z_grid[{idx}]={z_grid[idx]:.12f}, D_grid[{idx}]={D_grid[idx]:.12f}")
        else:
            print("\n  z=0 NOT in grid (interpolation used)")
            print(
                f"  Closest: z_grid[0]={z_grid[0]:.12f}, D_grid[0]={D_grid[0]:.12f}")

    print()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
