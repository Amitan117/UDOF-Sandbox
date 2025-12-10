#!/usr/bin/env python3
"""
Final Growth Factor Test - High Resolution
===========================================

Test at very high resolution to check for 0.4% overshoot.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from integrated_modules import ProperGrowthStandalone

H0 = 70.21
Omega_m = 0.3185
Omega_b = 0.05
Omega_geom_0 = 0.3266
alpha_geom = -0.1885
p_op = 0.7577

print("=" * 80)
print("HIGH RESOLUTION GROWTH FACTOR TEST")
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

# Test at very high resolutions
resolutions = [1000, 5000, 10000, 50000, 100000]

print("Testing at different resolutions:")
print()
print(f"{'Resolution':<12} {'D(z=0)':<15} {'Overshoot':<12} {'D(z=1)':<15}")
print("-" * 60)

results = []

for n_points in resolutions:
    # Force recomputation
    growth._growth_computed = False
    growth._z_growth = None
    growth._D_growth = None
    
    z_grid, D_grid = growth.compute_growth_factor_corrected(a_init=0.001, n_points=n_points)
    
    if z_grid is not None and D_grid is not None:
        D_z0 = growth.growth_factor(0.0)
        D_z1 = growth.growth_factor(1.0)
        overshoot = (D_z0 - 1.0) * 100
        
        results.append({
            'n_points': n_points,
            'D_z0': D_z0,
            'D_z1': D_z1,
            'overshoot': overshoot
        })
        
        print(f"{n_points:<12} {D_z0:<15.10f} {overshoot:+.6f}%     {D_z1:<15.10f}")

print()
print("=" * 80)
print()

# Check for overshoot pattern
print("Analysis:")
if len(results) > 1:
    max_overshoot = max(r['overshoot'] for r in results)
    min_overshoot = min(r['overshoot'] for r in results)
    
    print(f"  Max overshoot: {max_overshoot:+.6f}%")
    print(f"  Min overshoot: {min_overshoot:+.6f}%")
    print(f"  Range: {max_overshoot - min_overshoot:.6f}%")
    
    if abs(max_overshoot) > 0.1:
        print(f"  WARNING: Overshoot exceeds 0.1%")
    else:
        print(f"  OK: Overshoot within tolerance")

print()
print("=" * 80)

