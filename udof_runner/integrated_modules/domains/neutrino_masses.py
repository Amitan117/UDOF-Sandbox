"""
Domain: Neutrino Masses

Tests UDOF predictions for neutrino mass splittings from TSI geometry.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import PDG_NEUTRINO
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run neutrino masses tests."""
    result = DomainResult(domain_name="neutrino_masses")

    masses_eV, splittings = ctx.formulas.compute_neutrino_masses()
    total_chi2 = 0.0

    for name, (pdg_val, pdg_err) in PDG_NEUTRINO.items():
        computed = splittings[name]
        pull = (computed - pdg_val) / pdg_err
        chi2_contrib = pull**2
        total_chi2 += chi2_contrib
        error_pct = abs(computed - pdg_val) / pdg_val * 100

        # Standard pass/fail with 30% tolerance (neutrino has large uncertainties)
        passed = error_pct < 30

        result.tests.append(TestResult(
            test_name=name,
            status="PASS" if passed else "FAIL",
            value=computed, expected=pdg_val,
            error=abs(computed - pdg_val), chi2=chi2_contrib,
            notes=f"Error: {error_pct:.1f}%"
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1

    # Sum of masses - cosmological bound
    sum_ok = splittings['sum'] < 0.12
    result.tests.append(TestResult(
        test_name="sum_masses",
        status="PASS" if sum_ok else "FAIL",
        value=splittings['sum'],
        expected="< 0.12 eV",
        notes="Cosmological bound"
    ))
    result.n_pass += 1 if sum_ok else 0
    result.n_fail += 0 if sum_ok else 1

    result.chi2_total = total_chi2
    return result

