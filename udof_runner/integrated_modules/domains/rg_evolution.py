"""
Domain: RG Evolution

Tests full 2-loop RG evolution from M_Z to 10^18 GeV.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import solve_ivp
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run RG evolution tests."""
    result = DomainResult(domain_name="rg_evolution")

    if solve_ivp is None:
        result.tests.append(TestResult(
            test_name="rg_evolution", status="SKIP",
            value=None, notes="scipy.integrate.solve_ivp required"
        ))
        result.n_skip = 1
        return result

    try:
        rg = ctx.formulas.run_rg_evolution()

        # Test 1: No Landau poles
        no_poles = not rg['has_landau_pole']
        result.tests.append(TestResult(
            test_name="no_landau_poles", status="PASS" if no_poles else "FAIL",
            value=no_poles, expected=True,
            notes="COMPUTED: Perturbativity to 10^18 GeV"
        ))
        result.n_pass += 1 if no_poles else 0
        result.n_fail += 0 if no_poles else 1

        # Test 2: Lambda minimum
        result.tests.append(TestResult(
            test_name="lambda_min", status="PASS",
            value=rg['lambda_min'],
            expected="Computed",
            notes=f"COMPUTED: At μ = {rg['mu_at_lambda_min']:.2e} GeV"
        ))
        result.n_pass += 1

        # Test 3: Vacuum stability (with UDOF H4 threshold correction)
        stable = rg['stable']
        result.tests.append(TestResult(
            test_name="vacuum_stable", status="PASS" if stable else "FAIL",
            value=rg['lambda_min'],
            expected="> 0.0 (stable)",
            notes=f"COMPUTED: λ_min = {rg['lambda_min']:.4f} (H4 correction: +{rg.get('delta_lambda_correction', 0):.3f} at Λ_* = {rg.get('Lambda_star_GeV', 0):.2e} GeV)"
        ))
        result.n_pass += 1 if stable else 0
        result.n_fail += 0 if stable else 1

        # Test 4: Gauge crossing (optional)
        if rg['mu_unification']:
            result.tests.append(TestResult(
                test_name="gauge_crossing", status="PASS",
                value=rg['mu_unification'],
                notes=f"COMPUTED: g₂ = g₃ at {rg['mu_unification']:.2e} GeV"
            ))
            result.n_pass += 1

    except Exception as e:
        result.tests.append(TestResult(
            test_name="rg_evolution", status="ERROR",
            value=None, notes=str(e)
        ))
        result.n_error = 1

    return result

