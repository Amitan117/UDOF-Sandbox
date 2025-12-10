#!/usr/bin/env python3
"""
Compare Growth Factor with Original Implementation
===================================================

Test if the 0.4% overshoot appears and compare implementations.
"""

from integrated_modules import ProperGrowthStandalone
import sys
import numpy as np
from pathlib import Path

# Test parameters
H0 = 70.21
Omega_m = 0.3185
Omega_b = 0.05
Omega_geom_0 = 0.3266
alpha_geom = -0.1885
p_op = 0.7577

print("=" * 80)
print("GROWTH FACTOR COMPARISON")
print("=" * 80)
print()

# Test 1: Current standalone (with Omega_m_a)
sys.path.insert(0, str(Path(__file__).parent))


print("Test 1: Current Implementation (Omega_m_a = Omega_dm_a + Omega_b_a)")
print("-" * 80)

# Temporarily modify to use Omega_m_a
growth1 = ProperGrowthStandalone(
    H0=H0, Omega_m=Omega_m, Omega_b=Omega_b,
    Omega_geom_0=Omega_geom_0, alpha_geom=alpha_geom, p_op=p_op
)

# Check what dlnH_dlna uses
a_test = 1.0
Omega_dm = growth1.Omega_dm_cdqf(a_test)
Omega_b_a = growth1.Omega_b * (a_test ** (-3.0))
Omega_m_a = Omega_dm + Omega_b_a

print(f"  At a=1.0:")
print(f"    Omega_dm_cdqf = {Omega_dm:.10f}")
print(f"    Omega_b = {Omega_b_a:.10f}")
print(f"    Omega_m_a = Omega_dm + Omega_b = {Omega_m_a:.10f}")
print(
    f"    Difference: {abs(Omega_m_a - Omega_dm):.10e} ({abs(Omega_m_a - Omega_dm)/Omega_dm*100:.4f}%)")
print()

# Force high resolution and test
z_grid1, D_grid1 = growth1.compute_growth_factor_corrected(
    a_init=0.001, n_points=50000)
if z_grid1 is not None:
    D_z0_1 = growth1.growth_factor(0.0)
    D_z1_1 = growth1.growth_factor(1.0)
    print(f"  D(z=0) = {D_z0_1:.10f}")
    print(f"  D(z=1) = {D_z1_1:.10f}")

    # Check if there's an issue with the ODE itself
    # Evaluate ODE at a=1 with both methods
    from scipy.integrate import odeint

    # Method 1: Current (would use Omega_m_a)
    # We'll test by manually checking

    print()
    print("  ODE check at a=1:")
    y_test = np.array([1.0, 0.1])  # D=1, dD/dlna=0.1
    lna_test = 0.0
    a_val = np.exp(lna_test)

    Omega_cl = growth1.Omega_clustering(a_val)
    mu_eff = growth1.mu_effective(a_val)
    Omega_dm_val = growth1.Omega_dm_cdqf(a_val)
    Omega_b_val = growth1.Omega_b * (a_val ** (-3.0))
    Omega_m_val = Omega_dm_val + Omega_b_val

    # Current method uses Omega_m_a
    dlnH_dlna_m = 1.5 * Omega_m_val

    # Original method uses Omega_dm_cdqf only
    dlnH_dlna_dm = 1.5 * Omega_dm_val

    print(f"    Omega_dm_cdqf = {Omega_dm_val:.10f}")
    print(f"    Omega_b = {Omega_b_val:.10f}")
    print(f"    Omega_m = {Omega_m_val:.10f}")
    print(f"    dlnH/dlna (with Omega_m) = {dlnH_dlna_m:.10f}")
    print(f"    dlnH/dlna (with Omega_dm only) = {dlnH_dlna_dm:.10f}")
    print(
        f"    Difference: {abs(dlnH_dlna_m - dlnH_dlna_dm):.10e} ({abs(dlnH_dlna_m - dlnH_dlna_dm)/dlnH_dlna_dm*100:.4f}%)")

print()

# Now test with corrected version (Omega_dm_cdqf only for dlnH_dlna)
print("Test 2: Corrected Implementation (Omega_dm_cdqf only for dlnH/dlna)")
print("-" * 80)

# The fix is already applied, but let's verify
growth2 = ProperGrowthStandalone(
    H0=H0, Omega_m=Omega_m, Omega_b=Omega_b,
    Omega_geom_0=Omega_geom_0, alpha_geom=alpha_geom, p_op=p_op
)

z_grid2, D_grid2 = growth2.compute_growth_factor_corrected(
    a_init=0.001, n_points=50000)
if z_grid2 is not None:
    D_z0_2 = growth2.growth_factor(0.0)
    D_z1_2 = growth2.growth_factor(1.0)
    print(f"  D(z=0) = {D_z0_2:.10f}")
    print(f"  D(z=1) = {D_z1_2:.10f}")

    # Compare
    if z_grid1 is not None:
        diff_z0 = (D_z0_2 - D_z0_1) * 100
        diff_z1 = (D_z1_2 - D_z1_1) / D_z1_1 * 100
        print()
        print(f"  Difference from method 1:")
        print(f"    D(z=0): {diff_z0:+.6f}%")
        print(f"    D(z=1): {diff_z1:+.6f}%")

print()
print("=" * 80)
