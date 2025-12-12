#!/usr/bin/env python3
"""Test fixed baryogenesis calculation."""

import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from integrated_modules.baryo_complete_leptogenesis import CompleteLeptogenesis

ETA_B_OBSERVED = 6.1e-10

print("=" * 70)
print("TESTING FIXED BARYOGENESIS")
print("=" * 70)
print()

leptogenesis = CompleteLeptogenesis(Lambda_collapse=1e23)

# Test at M_N = 1e12 GeV
M_N = 1e12
result = leptogenesis.compute_baryon_asymmetry(M_N)

print(f"M_N: {M_N:.2e} GeV")
print(f"ε₁: {result.epsilon_1:.6e}")
print(f"κ: {result.kappa:.4f}")
print(f"η_B: {result.eta_B:.6e}")
print(f"η_B (observed): {ETA_B_OBSERVED:.6e}")
print()

error_pct = abs(result.eta_B - ETA_B_OBSERVED) / ETA_B_OBSERVED * 100
print(f"Error: {error_pct:.1f}%")
print(f"Within range: {'✓' if result.validation['within_range'] else '✗'}")

if abs(result.eta_B) < 1e-20:
    print()
    print("Still too small. Testing mass scale scan...")
    best_match = leptogenesis.find_matching_mass_scale()
    if best_match:
        print(f"Best M_N: {best_match['M_N_GeV']:.2e} GeV")
        print(f"Best η_B: {best_match['eta_B']:.6e}")
        print(f"Error: {best_match['error']*100:.1f}%")
    else:
        print("No matching mass scale found")

