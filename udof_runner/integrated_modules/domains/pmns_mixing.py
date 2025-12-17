"""
Domain: PMNS Mixing

Tests UDOF predictions for neutrino mixing angles against PDG values.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import PDG_PMNS, expm
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run PMNS mixing tests."""
    result = DomainResult(domain_name="pmns_mixing")
    if expm is None:
        result.n_skip = 3
        return result

    U = ctx.formulas.pmns_matrix()
    angles = ctx.formulas.extract_angles(U)
    total_chi2 = 0.0

    for name, (pdg_val, pdg_err) in PDG_PMNS.items():
        computed = angles[name]
        pull = (computed - pdg_val) / pdg_err
        chi2_contrib = pull**2
        total_chi2 += chi2_contrib
        passed = abs(computed - pdg_val) < 1.0

        result.tests.append(TestResult(
            test_name=f"pmns_{name}",
            status="PASS" if passed else "FAIL",
            value=computed, expected=pdg_val,
            error=abs(computed - pdg_val), chi2=chi2_contrib
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1

    result.chi2_total = total_chi2
    return result

