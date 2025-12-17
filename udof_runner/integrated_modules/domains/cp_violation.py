"""
Domain: CP Violation

Tests CP-violating phases and Jarlskog invariants from mixing matrices.

Derives CP phases from operational collapse framework:
- CP violation emerges from time-asymmetric collapse dynamics
- Complex phases in mixing matrices from collapse channel interference
- Jarlskog invariants from collapse correlation structure

All parameters come from lock files (standards compliance).
Mixing angles extracted from TSI matrices (not hardcoded).
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import expm
from integrated_modules.core.cp_phases import CPViolationDerivation
from integrated_modules.types import DomainResult, TestResult
import numpy as np


def run(ctx: DomainContext) -> DomainResult:
    """Run CP violation tests."""
    result = DomainResult(domain_name="cp_violation")

    if expm is None:
        result.n_skip = 4
        return result

    # Get TSI mixing matrices (real, from geometry)
    U_tsi = ctx.formulas.pmns_matrix()
    V_tsi = ctx.formulas.ckm_matrix()

    # Extract mixing angles from TSI matrices
    # These are the actual angles computed from TSI geometry
    pmns_angles = ctx.formulas.extract_angles(U_tsi)
    ckm_angles = ctx.formulas.extract_angles(V_tsi)

    # Derive CP phases from collapse dynamics
    # Uses parameters from lock file (cp_asymmetry_ckm, cp_asymmetry_pmns)
    cp_derivation = CPViolationDerivation(ctx.locks)
    cp_result = cp_derivation.derive_complete(ckm_angles, pmns_angles)

    # Test 1: CKM CP Phase
    # Threshold: Within 50% of PDG value (1.20 rad)
    delta_ckm_pdg = 1.20  # rad (PDG 2024)
    delta_ckm_error_pct = abs(cp_result.delta_ckm -
                              delta_ckm_pdg) / delta_ckm_pdg * 100
    ckm_phase_pass = delta_ckm_error_pct < 50.0

    result.tests.append(TestResult(
        test_name="ckm_cp_phase",
        status="PASS" if ckm_phase_pass else "FAIL",
        value=cp_result.delta_ckm,
        expected=f"δ_CKM ≈ {delta_ckm_pdg:.2f} rad (PDG 2024), error < 50%",
        error=delta_ckm_error_pct,
        notes=f"Derived from collapse dynamics: δ = 1.0 + cp_asymmetry_ckm * 2.0. Error: {delta_ckm_error_pct:.1f}%"
    ))
    if ckm_phase_pass:
        result.n_pass += 1
    else:
        result.n_fail += 1

    # Test 2: CKM Jarlskog Invariant
    # Threshold: Within 50% of PDG value (3.18e-5)
    J_ckm_pdg = 3.18e-5  # PDG 2024
    J_ckm_error_pct = abs(cp_result.J_ckm - J_ckm_pdg) / \
        J_ckm_pdg * 100 if J_ckm_pdg > 0 else float('inf')
    ckm_j_pass = J_ckm_error_pct < 50.0

    result.tests.append(TestResult(
        test_name="jarlskog_ckm",
        status="PASS" if ckm_j_pass else "FAIL",
        value=cp_result.J_ckm,
        expected=f"J_CKM ≈ {J_ckm_pdg:.2e} (PDG 2024), error < 50%",
        error=J_ckm_error_pct,
        notes=f"J = Im(V_ud V_cs V_us* V_cd*). Error: {J_ckm_error_pct:.1f}%"
    ))
    if ckm_j_pass:
        result.n_pass += 1
    else:
        result.n_fail += 1

    # Test 3: PMNS CP Phase
    # Threshold: Within 50% of PDG value (1.36 rad)
    delta_pmns_pdg = 1.36  # rad (PDG 2024)
    delta_pmns_error_pct = abs(
        cp_result.delta_pmns - delta_pmns_pdg) / delta_pmns_pdg * 100
    pmns_phase_pass = delta_pmns_error_pct < 50.0

    result.tests.append(TestResult(
        test_name="pmns_cp_phase",
        status="PASS" if pmns_phase_pass else "FAIL",
        value=cp_result.delta_pmns,
        expected=f"δ_PMNS ≈ {delta_pmns_pdg:.2f} rad (PDG 2024), error < 50%",
        error=delta_pmns_error_pct,
        notes=f"Derived from collapse dynamics: δ = 1.2 + cp_asymmetry_pmns * 1.5. Error: {delta_pmns_error_pct:.1f}%"
    ))
    if pmns_phase_pass:
        result.n_pass += 1
    else:
        result.n_fail += 1

    # Test 4: PMNS Jarlskog Invariant
    # Threshold: Within 50% of PDG value (0.033)
    J_pmns_pdg = 0.033  # PDG 2024
    J_pmns_error_pct = abs(cp_result.J_pmns - J_pmns_pdg) / \
        J_pmns_pdg * 100 if J_pmns_pdg > 0 else float('inf')
    pmns_j_pass = J_pmns_error_pct < 50.0

    result.tests.append(TestResult(
        test_name="jarlskog_pmns",
        status="PASS" if pmns_j_pass else "FAIL",
        value=cp_result.J_pmns,
        expected=f"J_PMNS ≈ {J_pmns_pdg:.3f} (PDG 2024), error < 50%",
        error=J_pmns_error_pct,
        notes=f"J = Im(U_e1 U_μ2 U_e2* U_μ1*). Error: {J_pmns_error_pct:.1f}%"
    ))
    if pmns_j_pass:
        result.n_pass += 1
    else:
        result.n_fail += 1

    return result
