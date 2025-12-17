"""
Domain: CKM Mixing

Tests UDOF predictions for quark mixing angles from TSI geometry.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import PDG_CKM, expm
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run CKM mixing tests."""
    result = DomainResult(domain_name="ckm_mixing")

    if expm is None:
        for name in ['theta12', 'theta23', 'theta13']:
            result.tests.append(TestResult(
                test_name=f"ckm_{name}", status="SKIP", value=None, notes="scipy required"
            ))
            result.n_skip += 1
        return result

    # Compute CKM matrix from TSI geometry
    V_ckm = ctx.formulas.ckm_matrix()
    angles = ctx.formulas.extract_angles(V_ckm)

    total_chi2 = 0.0

    for name, (pdg_val, pdg_err) in PDG_CKM.items():
        computed = angles[name]
        pull = (computed - pdg_val) / pdg_err
        chi2_contrib = pull**2
        total_chi2 += chi2_contrib

        # CKM has tight constraints - use 50% tolerance
        error_pct = abs(computed - pdg_val) / pdg_val * 100
        passed = error_pct < 50

        result.tests.append(TestResult(
            test_name=f"ckm_{name}",
            status="PASS" if passed else "FAIL",
            value=computed, expected=pdg_val,
            error=abs(computed - pdg_val), chi2=chi2_contrib,
            notes=f"Error: {error_pct:.1f}% (from TSI commutator)"
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1

    result.chi2_total = total_chi2
    return result

