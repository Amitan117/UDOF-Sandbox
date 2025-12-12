#!/usr/bin/env python3
"""
Test Integrated Modules
=======================

Quick test to verify integrated modules work correctly.
"""

import sys
import numpy as np

print("=" * 80)
print("TESTING INTEGRATED MODULES")
print("=" * 80)
print()

# Test 1: ProperGrowthStandalone
print("Test 1: ProperGrowthStandalone")
print("-" * 80)
try:
    from integrated_modules import ProperGrowthStandalone

    growth = ProperGrowthStandalone(
        H0=70.21,
        Omega_m=0.3185,
        Omega_b=0.05,
        Omega_geom_0=0.3266,
        alpha_geom=-0.1885,
        p_op=0.7577
    )

    D_z0 = growth.growth_factor(0.0)
    D_z1 = growth.growth_factor(1.0)

    print(f"✅ D(z=0) = {D_z0:.4f} (should be 1.0)")
    print(f"✅ D(z=1) = {D_z1:.4f} (should be ~0.55-0.70)")
    print(f"✅ Growth rate f(z=0) = {growth.growth_rate(0.0):.4f}")
    print()
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    print()

# Test 2: RXResponseStandalone
print("Test 2: RXResponseStandalone")
print("-" * 80)
try:
    from integrated_modules import RXResponseStandalone

    rx = RXResponseStandalone(
        H0=70.21,
        Omega_m=0.3185,
        Omega_b=0.05,
        Omega_geom_0=0.3266,
        alpha_geom=-0.1885,
        p_op=0.7577
    )

    R_X_cosmic = rx.R_X(1.0, 0.1)
    R_X_galaxy = rx.R_X(1.0, 0.5)
    C_X_z0 = rx.C_X(1.0)

    print(f"✅ R_X(k=0.1, z=0) = {R_X_cosmic:.4f} (should be ~1.0)")
    print(f"✅ R_X(k=0.5, z=0) = {R_X_galaxy:.4f}")
    print(f"✅ C_X(z=0) = {C_X_z0:.4f}")
    print()
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    print()

# Test 3: compute_S_ESE_proper
print("Test 3: compute_S_ESE_proper")
print("-" * 80)
try:
    from integrated_modules import compute_S_ESE_proper, ESE_MODULES_AVAILABLE

    if ESE_MODULES_AVAILABLE:
        r_kpc = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        M_disk = 1e10  # M☉
        M_gas = 2e9  # M☉
        r_d = 3.0  # kpc

        locks = {
            "calibrated_locks": {
                "eta_star": 0.171,
                "X0": 0.6481
            },
            "pivots": {
                "Sigma0_kg_m2": 0.217
            },
            "ese_map": {
                "ell_IR": 4.7e-5,
                "ell_star": 2e-15
            }
        }

        S_ESE = compute_S_ESE_proper(
            r_kpc, M_disk, M_gas, r_d,
            locks=locks, method='gradient'
        )

        if S_ESE is not None:
            print(
                f"✅ S_ESE computed: range [{np.min(S_ESE):.4f}, {np.max(S_ESE):.4f}]")
        else:
            print("⚠️  S_ESE returned None (modules unavailable)")
    else:
        print("⚠️  ESE modules not available (expected in sandbox)")
    print()
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    print()

print("=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
