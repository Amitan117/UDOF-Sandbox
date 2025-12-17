"""
Domain: Inflation

Tests slow-roll parameters from V(φ) = V₀[1-exp(-√(2/3)φ/M_Pl)]².
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run inflation tests."""
    result = DomainResult(domain_name="inflation")

    # Compute slow-roll parameters
    sr = ctx.formulas.slow_roll_parameters(N_efolds=55)

    # n_s test
    n_s = sr['n_s']
    pdg_ns, pdg_ns_err = 0.9649, 0.0042
    pull_ns = abs(n_s - pdg_ns) / pdg_ns_err
    passed_ns = pull_ns < 3

    result.tests.append(TestResult(
        test_name="spectral_index", status="PASS" if passed_ns else "FAIL",
        value=n_s, expected=f"{pdg_ns} ± {pdg_ns_err}",
        notes=f"COMPUTED: N={sr['N_efolds']}, ε={sr['epsilon']:.5f}"
    ))
    result.n_pass += 1 if passed_ns else 0
    result.n_fail += 0 if passed_ns else 1

    # r test
    r = sr['r']
    r_bound = 0.036
    passed_r = r < r_bound

    result.tests.append(TestResult(
        test_name="tensor_to_scalar", status="PASS" if passed_r else "FAIL",
        value=r, expected=f"< {r_bound}",
        notes=f"COMPUTED: r = 16ε = {r:.5f}"
    ))
    result.n_pass += 1 if passed_r else 0
    result.n_fail += 0 if passed_r else 1

    # ε test
    eps_ok = sr['epsilon'] < 0.01
    result.tests.append(TestResult(
        test_name="slow_roll_epsilon", status="PASS" if eps_ok else "FAIL",
        value=sr['epsilon'], expected="< 0.01",
        notes="COMPUTED from ε = 3/(4N²)"
    ))
    result.n_pass += 1 if eps_ok else 0
    result.n_fail += 0 if eps_ok else 1

    # η test
    eta_ok = abs(sr['eta']) < 0.1
    result.tests.append(TestResult(
        test_name="slow_roll_eta", status="PASS" if eta_ok else "FAIL",
        value=sr['eta'], expected="|η| < 0.1",
        notes="COMPUTED from η = -1/N"
    ))
    result.n_pass += 1 if eta_ok else 0
    result.n_fail += 0 if eta_ok else 1

    return result

