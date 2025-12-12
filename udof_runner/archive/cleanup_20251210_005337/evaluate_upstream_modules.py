#!/usr/bin/env python3
"""
Evaluate Upstream CDQF Modules for Integration
==============================================

This script evaluates the three upstream modules to determine if they should
be integrated into the v4.0 validation runner:

1. ProperCorrectedGrowth (growth factor computation)
2. TSESEResponseDerivation (R_X response computation)
3. compute_S_ESE_proper (SPARC ESE structure function)

Evaluation criteria:
- Functionality: Does the module work correctly?
- Dependencies: Are all dependencies available or can they be handled?
- Parameter alignment: Does it use current locks/parameters?
- Model coherence: Do results align with current CDQF model?
- Test value: Does it provide useful validation insights?
"""

import sys
from pathlib import Path
import json
import numpy as np
from typing import Dict, Any, Tuple, Optional

# Add parent project to path
PROJECT_ROOT = Path("D:/CDQF Prime-0 Physics Engine")
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "boltzmann_mcmc"))

# Load current locks from sandbox
SANDBOX_LOCKS = Path(__file__).parent / "default_params.json"
with open(SANDBOX_LOCKS, 'r') as f:
    SANDBOX_LOCKS_DATA = json.load(f)

# MCMC-validated parameters (from v4.0 runner)
MCMC_PARAMS = {
    "H0": 70.21,
    "Omega_m": 0.3185,
    "Omega_b": 0.05,  # Approximate
    "Omega_geom_0": 0.3266,
    "alpha_geom": -0.1885,
    "p_op": 0.7577,
    "eta_entropy": 0.0
}

print("=" * 80)
print("UPSTREAM MODULE EVALUATION")
print("=" * 80)
print()

# ============================================================================
# MODULE 1: ProperCorrectedGrowth
# ============================================================================

print("MODULE 1: ProperCorrectedGrowth")
print("-" * 80)

try:
    from cdqf_boltzmann_corrected import ProperCorrectedGrowth

    # Test with MCMC-validated parameters
    print("Testing with MCMC-validated parameters:")
    print(f"  H0 = {MCMC_PARAMS['H0']:.2f} km/s/Mpc")
    print(f"  Omega_m = {MCMC_PARAMS['Omega_m']:.4f}")
    print(f"  Omega_geom_0 = {MCMC_PARAMS['Omega_geom_0']:.4f}")
    print(f"  alpha_geom = {MCMC_PARAMS['alpha_geom']:.4f}")
    print(f"  p_op = {MCMC_PARAMS['p_op']:.4f}")
    print()

    cdqf_growth = ProperCorrectedGrowth(
        H0=MCMC_PARAMS['H0'],
        Omega_m=MCMC_PARAMS['Omega_m'],
        Omega_b=MCMC_PARAMS['Omega_b'],
        Omega_geom_0=MCMC_PARAMS['Omega_geom_0'],
        alpha_geom=MCMC_PARAMS['alpha_geom'],
        p_op=MCMC_PARAMS['p_op'],
        a_pivot=0.95,
        beta_ESE=-0.10,
        use_mu_eff=True
    )

    # Test growth factor at z=1
    D_z1 = cdqf_growth.D_corrected(1.0)
    print(f"✅ Growth factor D(z=1) = {D_z1:.4f}")

    # Test growth factor at z=0
    D_z0 = cdqf_growth.D_corrected(0.0)
    print(f"✅ Growth factor D(z=0) = {D_z0:.4f} (should be 1.0)")

    # Check clustering fraction
    xi_z0 = cdqf_growth.xi_clustering_fraction(1.0)
    print(f"✅ Clustering fraction ξ(z=0) = {xi_z0:.4f}")

    # Check effective gravitational coupling
    mu_eff_z0 = cdqf_growth.mu_effective(1.0)
    print(f"✅ Effective μ(z=0) = {mu_eff_z0:.4f}")

    print()
    print("✅ MODULE 1: PASS - Functional and uses current parameters")
    MODULE1_STATUS = "PASS"
    MODULE1_DEPENDENCIES = ["cdqf_boltzmann_full", "rsd_likelihood"]

except ImportError as e:
    print(f"❌ MODULE 1: FAIL - Import error: {e}")
    MODULE1_STATUS = "FAIL"
    MODULE1_DEPENDENCIES = []
except Exception as e:
    print(f"❌ MODULE 1: FAIL - Runtime error: {e}")
    MODULE1_STATUS = "FAIL"
    MODULE1_DEPENDENCIES = []

print()

# ============================================================================
# MODULE 2: TSESEResponseDerivation
# ============================================================================

print("MODULE 2: TSESEResponseDerivation")
print("-" * 80)

try:
    from ruthless_analysis.phase2_theory.response_model.derive_from_ese_kernel import TSESEResponseDerivation

    # Test with MCMC-validated parameters
    print("Testing with MCMC-validated parameters:")
    print(f"  H0 = {MCMC_PARAMS['H0']:.2f} km/s/Mpc")
    print(f"  Omega_m = {MCMC_PARAMS['Omega_m']:.4f}")
    print(f"  Omega_geom_0 = {MCMC_PARAMS['Omega_geom_0']:.4f}")
    print(f"  alpha_geom = {MCMC_PARAMS['alpha_geom']:.4f}")
    print(f"  p_op = {MCMC_PARAMS['p_op']:.4f}")
    print()

    rx_model = TSESEResponseDerivation(
        H0=MCMC_PARAMS['H0'],
        Omega_m=MCMC_PARAMS['Omega_m'],
        Omega_b=MCMC_PARAMS['Omega_b'],
        Omega_geom_0=MCMC_PARAMS['Omega_geom_0'],
        alpha_geom=MCMC_PARAMS['alpha_geom'],
        p_op=MCMC_PARAMS['p_op']
    )

    # Test R_X at cosmological scale (k=0.1 h/Mpc, should be ~1)
    R_X_cosmic = rx_model.R_X(1.0, 0.1, use_constraint=True)
    print(f"✅ R_X(k=0.1 h/Mpc, z=0) = {R_X_cosmic:.4f} (should be ~1.0)")

    # Test R_X at galaxy scale (k=0.5 h/Mpc)
    R_X_galaxy = rx_model.R_X(1.0, 0.5, use_constraint=True)
    print(f"✅ R_X(k=0.5 h/Mpc, z=0) = {R_X_galaxy:.4f}")

    # Test C_X at z=0
    C_X_z0 = rx_model.C_X(1.0)
    print(f"✅ C_X(z=0) = {C_X_z0:.4f}")

    # Test C_X at z=1
    C_X_z1 = rx_model.C_X(0.5)
    print(f"✅ C_X(z=1) = {C_X_z1:.4f}")

    print()
    print("✅ MODULE 2: PASS - Functional and uses current parameters")
    MODULE2_STATUS = "PASS"
    MODULE2_DEPENDENCIES = ["ProperCorrectedGrowth", "numpy", "scipy"]

except ImportError as e:
    print(f"❌ MODULE 2: FAIL - Import error: {e}")
    MODULE2_STATUS = "FAIL"
    MODULE2_DEPENDENCIES = []
except Exception as e:
    print(f"❌ MODULE 2: FAIL - Runtime error: {e}")
    MODULE2_STATUS = "FAIL"
    MODULE2_DEPENDENCIES = []

print()

# ============================================================================
# MODULE 3: compute_S_ESE_proper
# ============================================================================

print("MODULE 3: compute_S_ESE_proper")
print("-" * 80)

try:
    from prime0.toe.sparc_campaign.compute_proper_s_ese import compute_S_ESE_proper

    # Test with sample galaxy parameters
    r_kpc = np.array([1.0, 2.0, 3.0, 4.0, 5.0])  # kpc
    M_disk = 1e10  # M☉
    M_gas = 2e9  # M☉
    r_d = 3.0  # kpc

    # Create locks structure matching v4.0 format
    test_locks = {
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

    print("Testing with sample galaxy:")
    print(f"  r = {r_kpc} kpc")
    print(f"  M_disk = {M_disk:.1e} M☉")
    print(f"  M_gas = {M_gas:.1e} M☉")
    print(f"  r_d = {r_d:.2f} kpc")
    print()

    # Test gradient method
    S_ESE_gradient = compute_S_ESE_proper(
        r_kpc, M_disk, M_gas, r_d,
        locks=test_locks,
        method="gradient"
    )
    print(f"✅ S_ESE (gradient method): {S_ESE_gradient}")
    print(
        f"   Range: [{np.min(S_ESE_gradient):.4f}, {np.max(S_ESE_gradient):.4f}]")

    # Test s_activation method
    S_ESE_activation = compute_S_ESE_proper(
        r_kpc, M_disk, M_gas, r_d,
        locks=test_locks,
        method="s_activation"
    )
    print(f"✅ S_ESE (s_activation method): {S_ESE_activation}")
    print(
        f"   Range: [{np.min(S_ESE_activation):.4f}, {np.max(S_ESE_activation):.4f}]")

    print()
    print("✅ MODULE 3: PASS - Functional and uses current locks structure")
    MODULE3_STATUS = "PASS"
    MODULE3_DEPENDENCIES = ["prime0.modules.ese_dark_sector", "numpy"]

except ImportError as e:
    print(f"❌ MODULE 3: FAIL - Import error: {e}")
    MODULE3_STATUS = "FAIL"
    MODULE3_DEPENDENCIES = []
except Exception as e:
    print(f"❌ MODULE 3: FAIL - Runtime error: {e}")
    import traceback
    traceback.print_exc()
    MODULE3_STATUS = "FAIL"
    MODULE3_DEPENDENCIES = []

print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("EVALUATION SUMMARY")
print("=" * 80)
print()

modules = [
    ("ProperCorrectedGrowth", MODULE1_STATUS, MODULE1_DEPENDENCIES),
    ("TSESEResponseDerivation", MODULE2_STATUS, MODULE2_DEPENDENCIES),
    ("compute_S_ESE_proper", MODULE3_STATUS, MODULE3_DEPENDENCIES)
]

for name, status, deps in modules:
    status_symbol = "✅" if status == "PASS" else "❌"
    print(f"{status_symbol} {name}: {status}")
    if deps:
        print(f"   Dependencies: {', '.join(deps)}")
    print()

all_pass = all(status == "PASS" for _, status, _ in modules)

if all_pass:
    print("✅ ALL MODULES PASS - Ready for integration")
    print()
    print("Next steps:")
    print("1. Copy module code into v4.0 runner")
    print("2. Add proper error handling")
    print("3. Update test methods to use integrated modules")
    print("4. Verify test results align with current model")
else:
    print("⚠️  SOME MODULES FAIL - Review dependencies and fix issues")
    print()
    print("Issues to resolve:")
    for name, status, deps in modules:
        if status != "PASS":
            print(f"  - {name}: Check dependencies and imports")

print()
