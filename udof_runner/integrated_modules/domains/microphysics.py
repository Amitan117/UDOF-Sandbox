"""
Domain: Microphysics

Tests that ESE doesn't affect SM interactions at collider scales.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run microphysics tests."""
    result = DomainResult(domain_name="microphysics")

    # Compute actual ESE suppression at collider scales
    # Collider environment: high density but NO astrophysical mixing
    try:
        # Typical collider: Sigma ~ 1e10 kg/m² (very dense), but no mixing
        sigma_g_collider = 1.0  # m/s - effectively no mixing
        s_collider = ctx.formulas.compute_s(
            1e10, 1e15, sigma_g=sigma_g_collider)

        # ESE should be completely suppressed (s ≈ 0) at particle physics scales
        passed = s_collider < 1e-6

        result.tests.append(TestResult(
            test_name="sm_preserved", status="PASS" if passed else "FAIL",
            value=s_collider, expected="< 1e-6 (ESE suppressed)",
            error=s_collider,
            notes=f"COMPUTED: s = {s_collider:.2e} at collider scales (σ_g={sigma_g_collider} m/s, no mixing)"
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1
    except Exception as e:
        result.tests.append(TestResult(
            test_name="sm_preserved", status="ERROR",
            value=None, expected="< 1e-6",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1

    return result

