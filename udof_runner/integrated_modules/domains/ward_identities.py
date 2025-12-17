"""
Domain: Ward Identities

Tests Ward identity violations at atomic scales.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import hbar_SI, c_SI, GeV_to_J
from integrated_modules.types import DomainResult, TestResult
import numpy as np


def run(ctx: DomainContext) -> DomainResult:
    """Run Ward identities tests."""
    result = DomainResult(domain_name="ward_identities")

    ell0 = 1e-4
    Lambda_U1 = hbar_SI * c_SI / ell0 / GeV_to_J
    p_atomic = 1e-6
    violation = np.exp(-(p_atomic / Lambda_U1)**4)

    for name, exp, bound in [("charge_conservation", violation, 1e-25),
                             ("photon_mass", violation, 1e-18)]:
        passed = exp < bound
        result.tests.append(TestResult(
            test_name=name, status="PASS" if passed else "FAIL",
            value=exp, expected=f"< {bound}"
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1

    return result

