"""
Domain: H4 Geometry

Tests H4 geometry constraints from UDOF.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run H4 geometry tests."""
    result = DomainResult(domain_name="h4_geometry")
    h4 = ctx.formulas.h4_constraints()

    tests = [
        ("h4_trace", h4['trace_sum'], 10.0, 0.01),
        ("h4_det_gamma", h4['det_gamma'], 4.1, 0.1),
        ("h4_det_sigma", h4['det_sigma'], 2/3, 0.01)
    ]

    for name, value, target, tol in tests:
        passed = abs(value - target) < tol
        result.tests.append(TestResult(
            test_name=name, status="PASS" if passed else "FAIL",
            value=value, expected=target, error=abs(value - target)
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1

    return result

