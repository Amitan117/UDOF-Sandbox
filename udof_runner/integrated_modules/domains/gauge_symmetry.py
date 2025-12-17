"""
Domain: Gauge Symmetry

Tests gauge symmetry properties from UDOF operational collapse framework.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult

try:
    from integrated_modules.gauge_unification_complete import GaugeUnificationDerivation
    GAUGE_AVAILABLE = True
except ImportError:
    GAUGE_AVAILABLE = False


def run(ctx: DomainContext) -> DomainResult:
    """Run gauge symmetry tests."""
    result = DomainResult(domain_name="gauge_symmetry")

    if not GAUGE_AVAILABLE:
        result.tests.append(TestResult(
            test_name="lindblad_cp", status="SKIP",
            value=None, expected="CP preservation from Lindblad operators",
            notes="gauge_unification_complete module not available"
        ))
        result.n_skip += 1
        result.tests.append(TestResult(
            test_name="gauge_groups", status="SKIP",
            value=None, expected="SU(3)×SU(2)×U(1) emergence",
            notes="gauge_unification_complete module not available"
        ))
        result.n_skip += 1
        return result

    try:
        # Create gauge derivation
        derivation = GaugeUnificationDerivation(
            mu_op_gev=0.07)  # 70 MeV operational scale

        # Run complete derivation
        structure = derivation.derive_complete()

        # Test 1: Gauge groups
        expected_groups = {'SU(3)', 'SU(2)', 'U(1)'}
        found_groups = set(structure.groups)
        groups_match = expected_groups == found_groups

        result.tests.append(TestResult(
            test_name="gauge_groups", status="PASS" if groups_match else "FAIL",
            value=structure.groups, expected=list(expected_groups),
            notes=f"Groups identified: {', '.join(structure.groups)}"
        ))
        result.n_pass += 1 if groups_match else 0
        result.n_fail += 0 if groups_match else 1

        # Test 2: Lindblad CP preservation
        cp_check = structure.validation.get('cp_preservation', {})
        # Use correct key name and convert np.True_ to bool
        cp_preserved = bool(cp_check.get('cp_preserving', False))

        result.tests.append(TestResult(
            test_name="lindblad_cp", status="PASS" if cp_preserved else "FAIL",
            value=cp_preserved, expected=True,
            notes=f"CP preservation: {cp_check.get('method', 'N/A')}, positive_semidef={cp_check.get('positive_semidef', False)}, trace_preserving={cp_check.get('trace_preserving', False)}"
        ))
        result.n_pass += 1 if cp_preserved else 0
        result.n_fail += 0 if cp_preserved else 1

    except Exception as e:
        result.tests.append(TestResult(
            test_name="gauge_groups", status="ERROR",
            value=None, expected="SU(3)×SU(2)×U(1)",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1
        result.tests.append(TestResult(
            test_name="lindblad_cp", status="ERROR",
            value=None, expected="CP preservation",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1

    return result
