"""
Domain: GW Ringdown

Tests QNM frequencies computed from f = c³/(2π√27 GM).
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run GW ringdown tests."""
    result = DomainResult(domain_name="gw_ringdown")

    # Compute QNM frequency for 30 M_sun BH
    M = 30
    f_qnm = ctx.formulas.qnm_frequency(M)
    passed = 200 < f_qnm < 400

    result.tests.append(TestResult(
        test_name="qnm_frequency", status="PASS" if passed else "FAIL",
        value=f_qnm, expected="200-400 Hz",
        notes=f"COMPUTED: f = c³/(2π√27 GM) for {M} M☉"
    ))
    result.n_pass += 1 if passed else 0
    result.n_fail += 0 if passed else 1

    # QNM deviation from GR
    delta = ctx.formulas.qnm_deviation()
    passed = delta < 0.01

    result.tests.append(TestResult(
        test_name="qnm_gr_deviation", status="PASS" if passed else "FAIL",
        value=delta, expected="< 1%",
        notes="COMPUTED: Strong-field suppression → GR QNMs"
    ))
    result.n_pass += 1 if passed else 0
    result.n_fail += 0 if passed else 1

    return result

