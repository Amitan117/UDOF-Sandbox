#!/usr/bin/env python3
"""
Test Different Interpolation Methods for Growth Factor
=======================================================

Check if cubic interpolation causes 0.4% overshoot vs linear.
"""

from integrated_modules import ProperGrowthStandalone
import sys
import numpy as np
from scipy.interpolate import interp1d
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


H0 = 70.21
Omega_m = 0.3185
Omega_b = 0.05
Omega_geom_0 = 0.3266
alpha_geom = -0.1885
p_op = 0.7577

print("=" * 80)
print("TESTING INTERPOLATION METHODS")
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

# Test at very high resolution
n_points = 50000
z_grid, D_grid = growth.compute_growth_factor_corrected(
    a_init=0.001, n_points=n_points)

if z_grid is not None and D_grid is not None:
    print(f"Resolution: {n_points} points")
    print()

    # Test different interpolation methods
    methods = [
        ('linear', 'linear'),
        ('cubic', 'cubic'),
        ('quadratic', 'quadratic')
    ]

    print("Interpolation comparison at z=0:")
    print()

    for method_name, kind in methods:
        interp_func = interp1d(
            z_grid, D_grid,
            kind=kind,
            bounds_error=False,
            fill_value='extrapolate'
        )

        D_z0 = float(interp_func(0.0))
        overshoot_pct = (D_z0 - 1.0) * 100

        # Check near z=0
        z_near = [0.0, 1e-6, 1e-5, 1e-4, 0.001]
        print(
            f"{method_name:12s}: D(0) = {D_z0:.10f} (overshoot = {overshoot_pct:+.6f}%)")

        for z in z_near[:3]:  # Just show first few
            D_val = float(interp_func(z))
            print(f"               D({z:.1e}) = {D_val:.10f}")
        print()

    # Test explicit boundary handling
    print("Explicit boundary handling (force D(0)=1.0):")
    print()

    # Create interpolator with boundary fix
    def growth_factor_with_fix(z):
        if z == 0.0 or abs(z) < 1e-12:
            return 1.0
        else:
            return float(np.interp(z, z_grid, D_grid))

    D_z0_fixed = growth_factor_with_fix(0.0)
    overshoot_fixed = (D_z0_fixed - 1.0) * 100
    print(
        f"Fixed method:  D(0) = {D_z0_fixed:.10f} (overshoot = {overshoot_fixed:+.6f}%)")
    print()

    # Check original method
    print("Original method (np.interp):")
    D_z0_orig = float(np.interp(0.0, z_grid, D_grid))
    overshoot_orig = (D_z0_orig - 1.0) * 100
    print(
        f"np.interp:     D(0) = {D_z0_orig:.10f} (overshoot = {overshoot_orig:+.6f}%)")
    print()

    # Check what growth_factor() actually returns
    print("Current growth_factor() method:")
    D_z0_current = growth.growth_factor(0.0)
    overshoot_current = (D_z0_current - 1.0) * 100
    print(
        f"growth_factor: D(0) = {D_z0_current:.10f} (overshoot = {overshoot_current:+.6f}%)")

else:
    print("Computation failed!")

print()
print("=" * 80)
