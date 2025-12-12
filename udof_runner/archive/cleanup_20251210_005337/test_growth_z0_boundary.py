#!/usr/bin/env python3
"""
Test Growth Factor z=0 Boundary Handling
=========================================

Check if z=0 is exactly in the grid and if interpolation causes overshoot.
"""

from integrated_modules import ProperGrowthStandalone
import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


H0 = 70.21
Omega_m = 0.3185
Omega_b = 0.05
Omega_geom_0 = 0.3266
alpha_geom = -0.1885
p_op = 0.7577

print("=" * 80)
print("TESTING z=0 BOUNDARY HANDLING")
print("=" * 80)
print()

growth = ProperGrowthStandalone(
    H0=H0,
    Omega_m=Omega_m,
    Omega_b=Omega_b,
    Omega_geom_0=Omega_geom_0,
    alpha_geom=alpha_geom,
    p_op=p_op
)

# Test at high resolution
n_points = 10000
z_grid, D_grid = growth.compute_growth_factor_corrected(
    a_init=0.001, n_points=n_points)

if z_grid is not None and D_grid is not None:
    print(f"Resolution: {n_points} points")
    print()

    # Check first few points
    print("First 5 grid points (should include z=0):")
    for i in range(min(5, len(z_grid))):
        print(f"  [{i}] z={z_grid[i]:.12f}, D={D_grid[i]:.12f}")

    print()
    print("Last 5 grid points (high z):")
    for i in range(max(0, len(z_grid)-5), len(z_grid)):
        print(f"  [{i}] z={z_grid[i]:.12f}, D={D_grid[i]:.12f}")

    print()

    # Check if z=0 is exactly in grid
    z0_mask = np.abs(z_grid) < 1e-10
    z0_indices = np.where(z0_mask)[0]

    if len(z0_indices) > 0:
        print(f"z=0 found at indices: {z0_indices}")
        for idx in z0_indices:
            print(f"  z_grid[{idx}] = {z_grid[idx]:.15e}")
            print(f"  D_grid[{idx}] = {D_grid[idx]:.15e}")
    else:
        print("z=0 NOT found in grid!")
        print(f"  Closest: z_grid[0] = {z_grid[0]:.15e}")
        print(f"  Distance from 0: {abs(z_grid[0]):.15e}")

    print()

    # Test interpolation at various z values
    print("Interpolation test:")
    z_test_values = [0.0, 1e-10, 1e-8, 1e-6, 1e-4, 0.001]

    for z_test in z_test_values:
        D_interp = growth.growth_factor(z_test)
        # Find closest grid point
        idx_closest = np.argmin(np.abs(z_grid - z_test))
        z_closest = z_grid[idx_closest]
        D_closest = D_grid[idx_closest]

        diff_from_1 = (D_interp - 1.0) * 100  # Percentage

        print(f"  z={z_test:.10f}: D(z)={D_interp:.10f} (diff={diff_from_1:+.6f}%), "
              f"closest grid: z={z_closest:.10f}, D={D_closest:.10f}")

    print()

    # Check a_arr to see if a=1.0 is exact
    a_arr = 1.0 / (1.0 + z_grid)
    a_last = a_arr[-1] if len(a_arr) > 0 else np.nan
    a_first = a_arr[0] if len(a_arr) > 0 else np.nan

    print("Scale factor check:")
    print(f"  a_arr[0] = {a_first:.15e} (should be ~1.0 for z=0)")
    print(f"  a_arr[-1] = {a_last:.15e} (should be ~0.001 for high z)")
    print(f"  Distance from 1.0: {abs(a_first - 1.0):.15e}")

    # Check if the issue is in the conversion
    print()
    print("Checking conversion z = 1/a - 1:")
    a_exact_1 = 1.0
    z_from_a = 1.0 / a_exact_1 - 1.0
    print(f"  For a=1.0 exactly: z = {z_from_a:.15e}")

    # Check what z we get for a very close to 1
    a_near_1 = np.float64(1.0 - 1e-12)
    z_near_1 = 1.0 / (1.0 + z_grid[0]) - 1.0
    print(f"  For z_grid[0]={z_grid[0]:.15e}: a = {1.0/(1.0+z_grid[0]):.15e}")

else:
    print("Computation failed!")

print()
print("=" * 80)
