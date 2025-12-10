#!/usr/bin/env python3
"""
Detailed Growth Factor Analysis
================================

Check normalization, ODE solution, and potential sources of 0.4% overshoot.
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
print("DETAILED GROWTH FACTOR ANALYSIS")
print("=" * 80)
print()

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

# Test at very high resolution
n_points = 100000
print(f"Testing at resolution: {n_points} points")
print()

z_grid, D_grid = growth.compute_growth_factor_corrected(
    a_init=0.001, n_points=n_points)

if z_grid is not None and D_grid is not None:
    # Check normalization
    print("Normalization check:")
    D_today_unnormalized = growth._D_growth[-1] if hasattr(
        growth, '_D_growth') else None

    # Check what D_arr[-1] was before normalization
    # We need to recompute to see unnormalized value
    from scipy.integrate import odeint

    lna_init = np.log(0.001)
    lna_today = 0.0
    lna_arr = np.linspace(lna_init, lna_today, n_points)

    D_init = 0.001
    dD_dlna_init = 0.001
    y0 = np.array([D_init, dD_dlna_init])

    solution = odeint(
        growth._growth_ode_corrected,
        y0,
        lna_arr,
        atol=1e-10,  # Very tight tolerance
        rtol=1e-10
    )

    D_arr_unnorm = solution[:, 0]
    D_today_unnorm = D_arr_unnorm[-1]
    D_arr_norm = D_arr_unnorm / D_today_unnorm

    print(f"  D_today (unnormalized): {D_today_unnorm:.12e}")
    print(
        f"  D_today (after normalization): {D_arr_norm[-1]:.12f} (should be 1.0)")
    print(f"  D(z=0) from grid: {D_grid[0]:.12f}")
    print(f"  D(z=0) from interpolation: {growth.growth_factor(0.0):.12f}")

    # Check if D_today might have numerical error
    print()
    print("Checking for numerical precision issues:")
    a_arr_test = np.exp(lna_arr)
    z_arr_test = 1.0 / a_arr_test - 1.0

    # Check if a=1.0 is exact
    a_last = a_arr_test[-1]
    print(f"  a_arr[-1] = {a_last:.15e} (should be 1.0)")
    print(f"  Distance from 1.0: {abs(a_last - 1.0):.15e}")

    # Check ODE solution near a=1
    print()
    print("ODE solution near a=1 (last 10 points):")
    for i in range(max(0, len(lna_arr)-10), len(lna_arr)):
        a_val = a_arr_test[i]
        z_val = z_arr_test[i]
        D_unnorm = D_arr_unnorm[i]
        D_norm = D_arr_norm[i]
        print(
            f"  [{i}] a={a_val:.10f}, z={z_val:.10f}, D_unnorm={D_unnorm:.10e}, D_norm={D_norm:.12f}")

    # Check if the issue is in the ODE itself
    print()
    print("ODE evaluation at a=1 (lna=0):")
    y_test = np.array([1.0, 0.0])  # D=1, dD/dlna = some value
    lna_test = 0.0
    dydlna = growth._growth_ode_corrected(y_test, lna_test)

    a_test = np.exp(lna_test)
    Omega_cl_test = growth.Omega_clustering(a_test)
    mu_eff_test = growth.mu_effective(a_test)
    Omega_dm_test = growth.Omega_dm_cdqf(a_test)
    Omega_b_test = growth.Omega_b * (a_test ** (-3.0))
    Omega_m_test = Omega_dm_test + Omega_b_test
    dlnH_dlna_test = 1.5 * Omega_m_test

    print(f"  a = {a_test:.10f}")
    print(f"  Omega_cl = {Omega_cl_test:.10f}")
    print(f"  mu_eff = {mu_eff_test:.10f}")
    print(f"  Omega_m = {Omega_m_test:.10f}")
    print(f"  dlnH/dlna = {dlnH_dlna_test:.10f}")
    print(f"  dD/dlna = {dydlna[0]:.10e}")
    print(f"  d²D/d(ln a)² = {dydlna[1]:.10e}")

    # Check if overshoot appears in comparisons
    print()
    print("Comparison with reference values:")

    # Typical D(z=1) should be ~0.55-0.70 for Omega_m ~ 0.3
    D_z1 = growth.growth_factor(1.0)
    D_z1_ref = 0.65  # Approximate reference
    diff_z1 = (D_z1 - D_z1_ref) / D_z1_ref * 100

    print(f"  D(z=1) = {D_z1:.8f}")
    print(f"  D(z=1) reference ~ 0.65")
    print(f"  Difference: {diff_z1:+.4f}%")

    # Check if 0.4% is relative to something specific
    print()
    print("Checking for 0.4% overshoot relative to:")
    print(
        f"  1. D(z=0) itself: {growth.growth_factor(0.0):.10f} (should be 1.0)")
    print(f"  2. D(z=1) * scale: {growth.growth_factor(1.0) * 1.004:.10f}")

    # Maybe the issue is when comparing to a reference cosmology?
    print()
    print("Comparing with simple LCDM growth (D ∝ a for matter-dominated):")
    # At z=0, D=1 by normalization
    # At z=1 (a=0.5), for LCDM: D ≈ a × (Omega_m/Omega_m0)^0.6 ≈ 0.5 × (0.3/0.3)^0.6 = 0.5
    # But actual D(z=1) is larger due to dark energy
    D_z1_lcdm_approx = 0.5
    D_z1_actual = growth.growth_factor(1.0)
    overshoot_vs_lcdm = (D_z1_actual / D_z1_lcdm_approx - 1.0) * 100
    print(f"  Simple LCDM D(z=1) ≈ 0.5")
    print(f"  Actual D(z=1) = {D_z1_actual:.8f}")
    print(f"  Difference: {overshoot_vs_lcdm:+.4f}%")

else:
    print("Computation failed!")

print()
print("=" * 80)
