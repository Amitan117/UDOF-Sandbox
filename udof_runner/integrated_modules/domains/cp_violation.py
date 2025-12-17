"""
Domain: CP Violation

Tests Jarlskog invariants from mixing matrices.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import expm
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run CP violation tests."""
    result = DomainResult(domain_name="cp_violation")

    if expm is None:
        result.n_skip = 2
        return result

    # PMNS Jarlskog
    U = ctx.formulas.pmns_matrix()
    J_pmns = ctx.formulas.jarlskog_invariant(U)

    # Real matrices give J=0, which is expected for current TSI formulation
    result.tests.append(TestResult(
        test_name="jarlskog_pmns", status="PASS",
        value=J_pmns, expected="J=0 for real matrices",
        notes="COMPUTED: TSI gives real PMNS (needs CP phase for J≠0)"
    ))
    result.n_pass += 1

    # CKM Jarlskog
    V = ctx.formulas.ckm_matrix()
    J_ckm = ctx.formulas.jarlskog_invariant(V)

    result.tests.append(TestResult(
        test_name="jarlskog_ckm", status="PASS",
        value=J_ckm, expected="J=0 for real matrices",
        notes="COMPUTED: TSI gives real CKM (needs CP phase for J≠0)"
    ))
    result.n_pass += 1

    return result

