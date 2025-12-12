#!/usr/bin/env python3
"""
Diagnostic script for baryogenesis η_B calculation.

Investigates why η_B is 10³⁹ too small and tests fixes.
"""

import numpy as np
import sys
from pathlib import Path

# Add integrated_modules to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from integrated_modules.baryo_complete_leptogenesis import CompleteLeptogenesis
    HAS_MODULE = True
except ImportError as e:
    print(f"Import error: {e}")
    HAS_MODULE = False

# Physical constants
M_PLANK_GEV = 2.435e18
ETA_B_OBSERVED = 6.1e-10

def diagnose_current_calculation():
    """Diagnose current calculation step by step."""
    print("=" * 70)
    print("BARYOGENESIS DIAGNOSIS")
    print("=" * 70)
    print()
    
    if not HAS_MODULE:
        print("ERROR: Cannot import module")
        return
    
    leptogenesis = CompleteLeptogenesis(Lambda_collapse=1e23)
    
    # Test parameters
    M_N = 1e12  # GeV
    delta_pmns = 1.36  # rad
    m_light = (5.77e-4, 8.30e-3, 5.04e-2)  # eV
    
    print(f"[Test Parameters]")
    print(f"  M_N: {M_N:.2e} GeV")
    print(f"  δ_PMNS: {delta_pmns:.4f} rad")
    print(f"  m_light: {m_light} eV")
    print(f"  Γ_collapse: {leptogenesis.Lambda:.2e} s⁻¹")
    print()
    
    # Step 1: Base CP asymmetry
    print(f"[Step 1: Base CP Asymmetry]")
    m1, m2, m3 = m_light
    dm2_21 = (m2**2 - m1**2) * 1e-18  # eV² → GeV²
    dm2_31 = (m3**2 - m1**2) * 1e-18
    dm2_used = max(dm2_21, dm2_31)
    
    epsilon_base_standard = (3.0 / (16.0 * np.pi)) * (M_N / M_PLANK_GEV) * \
                            (dm2_used / (M_N ** 2)) * np.sin(delta_pmns)
    
    print(f"  Δm² (larger): {dm2_used:.2e} GeV²")
    print(f"  (M_N/M_P): {M_N/M_PLANK_GEV:.2e}")
    print(f"  (Δm²/M_N²): {dm2_used/(M_N**2):.2e}")
    print(f"  sin(δ): {np.sin(delta_pmns):.4f}")
    print(f"  ε_base (standard formula): {epsilon_base_standard:.2e}")
    print()
    
    # Alternative: Use light neutrino mass scale
    m_nu_scale = np.sqrt(dm2_31 * 1e18)  # Light neutrino mass scale [eV]
    m_nu_scale_GeV = m_nu_scale * 1e-9  # Convert to GeV
    
    epsilon_base_alternative = (3.0 / (16.0 * np.pi)) * (M_N / M_PLANK_GEV) * \
                               (m_nu_scale_GeV / M_N) * np.sin(delta_pmns)
    
    print(f"  m_ν (scale): {m_nu_scale:.2e} eV = {m_nu_scale_GeV:.2e} GeV")
    print(f"  (m_ν/M_N): {m_nu_scale_GeV/M_N:.2e}")
    print(f"  ε_base (alternative formula): {epsilon_base_alternative:.2e}")
    print(f"  Ratio (alt/std): {epsilon_base_alternative/epsilon_base_standard:.2e}")
    print()
    
    # Step 2: Collapse enhancement
    print(f"[Step 2: Collapse Enhancement]")
    Gamma = leptogenesis.Lambda
    Gamma_ref = 1e15
    alpha = 0.7
    f_collapse = 1.0 + (Gamma / Gamma_ref) ** alpha
    
    print(f"  Γ: {Gamma:.2e} s⁻¹")
    print(f"  Γ_ref: {Gamma_ref:.2e} s⁻¹")
    print(f"  (Γ/Γ_ref): {Gamma/Gamma_ref:.2e}")
    print(f"  f_collapse: {f_collapse:.2e}")
    print()
    
    # Enhanced epsilon
    epsilon_enhanced = epsilon_base_standard * f_collapse
    epsilon_enhanced_alt = epsilon_base_alternative * f_collapse
    
    print(f"[Step 3: Enhanced ε₁]")
    print(f"  ε₁ (standard): {epsilon_enhanced:.2e}")
    print(f"  ε₁ (alternative): {epsilon_enhanced_alt:.2e}")
    print()
    
    # Step 4: Efficiency
    print(f"[Step 4: Efficiency κ]")
    kappa = leptogenesis.compute_efficiency_factor(M_N)
    print(f"  κ: {kappa:.4f}")
    print()
    
    # Step 5: Final asymmetry
    print(f"[Step 5: Baryon Asymmetry]")
    eta_L_std = -epsilon_enhanced * kappa
    eta_B_std = -0.01 * eta_L_std
    
    eta_L_alt = -epsilon_enhanced_alt * kappa
    eta_B_alt = -0.01 * eta_L_alt
    
    print(f"  η_L (standard): {abs(eta_L_std):.2e}")
    print(f"  η_B (standard): {abs(eta_B_std):.2e}")
    print(f"  η_L (alternative): {abs(eta_L_alt):.2e}")
    print(f"  η_B (alternative): {abs(eta_B_alt):.2e}")
    print(f"  η_B (observed): {ETA_B_OBSERVED:.2e}")
    print()
    
    print(f"[Analysis]")
    ratio_std = ETA_B_OBSERVED / abs(eta_B_std)
    ratio_alt = ETA_B_OBSERVED / abs(eta_B_alt)
    
    print(f"  Standard formula needs {ratio_std:.2e}× enhancement")
    print(f"  Alternative formula needs {ratio_alt:.2e}× enhancement")
    print()
    
    # Check if alternative is better
    if ratio_alt < ratio_std:
        print(f"  ✓ Alternative formula is {ratio_std/ratio_alt:.1f}× better")
    else:
        print(f"  ✗ Alternative formula doesn't help much")
    
    return {
        'epsilon_base_standard': epsilon_base_standard,
        'epsilon_base_alternative': epsilon_base_alternative,
        'f_collapse': f_collapse,
        'kappa': kappa,
        'eta_B_standard': abs(eta_B_std),
        'eta_B_alternative': abs(eta_B_alt),
        'needed_enhancement_std': ratio_std,
        'needed_enhancement_alt': ratio_alt
    }


if __name__ == "__main__":
    results = diagnose_current_calculation()
    print("=" * 70)

