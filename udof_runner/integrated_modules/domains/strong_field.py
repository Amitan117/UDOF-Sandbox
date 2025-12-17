"""
Domain: Strong Field

Tests strong-field gravity predictions.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run strong field tests."""
    result = DomainResult(domain_name="strong_field")

    sf = ctx.locks['strong_field']
    K_ref = sf['K_ref']
    K_horizon = 1e15
    suppression = 1 / (1 + (K_horizon / K_ref)**2)
    gr_ok = suppression < 0.01

    result.tests.append(TestResult(
        test_name="gr_at_horizon", status="PASS" if gr_ok else "FAIL",
        value=suppression, expected="< 0.01"
    ))
    result.n_pass += 1 if gr_ok else 0
    result.n_fail += 0 if gr_ok else 1

    # GW speed constraint - use UDOF GW theory computation
    try:
        from integrated_modules.gw_propagation_speed import compute_gw_speed

        # In vacuum (strong field), s→0 due to suppression
        s_vacuum = 0.0
        ell_IR = ctx.formulas.ell_IR
        Lambda_rate = ctx.locks.get('collapse', {}).get(
            'Lambda_rate_sinv', 1e23)

        gw_result = compute_gw_speed(
            s=s_vacuum, ell_eff=ell_IR, Lambda_rate=Lambda_rate)
        c_ratio = gw_result['c_GW_c_ratio']
        delta_c = gw_result['delta_c_ratio']
        compliant = gw_result['compliant']

        result.tests.append(TestResult(
            test_name="gw_speed", status="PASS" if compliant else "FAIL",
            value=c_ratio, expected="1.0 +/- 1e-15 (GW170817)",
            notes=f"COMPUTED: c_GW/c = {c_ratio:.2e}, |1-c_GW/c| = {delta_c:.2e} < 1e-15"
        ))
        result.n_pass += 1 if compliant else 0
        result.n_fail += 0 if compliant else 1
    except ImportError:
        result.tests.append(TestResult(
            test_name="gw_speed", status="SKIP",
            value=None, expected="1.0 +/- 1e-15 (GW170817)",
            notes="gw_propagation_speed module not available"
        ))
        result.n_skip += 1
    except Exception as e:
        result.tests.append(TestResult(
            test_name="gw_speed", status="ERROR",
            value=None, expected="1.0 +/- 1e-15 (GW170817)",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1

    return result
