"""
Domain: Early Universe

Tests CMB and BBN predictions - ESE inactive at cosmic scales.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run early universe tests."""
    result = DomainResult(domain_name="early_universe")

    # At CMB epoch: no local mixing, ESE off
    s_cmb = ctx.formulas.compute_s(100, 1e-5, sigma_g=10.0)  # σ << 1 km/s
    passed = s_cmb < 0.01

    result.tests.append(TestResult(
        test_name="cmb_lcdm", status="PASS" if passed else "FAIL",
        value=s_cmb, expected="< 0.01",
        notes="No local mixing at CMB → ESE off → ΛCDM preserved"
    ))
    result.n_pass += 1 if passed else 0
    result.n_fail += 0 if passed else 1

    # BBN preservation - compute abundances with UDOF dark sector
    try:
        from integrated_modules.bbn_solver import UDOFBBNSolver

        # Get baryon-to-photon ratio from locks (from baryogenesis)
        # Use standard value if not available
        eta_B = 6.1e-10  # Standard value
        if 'baryogenesis' in ctx.locks or 'early_universe' in ctx.locks:
            # Try to get from locks if available
            eta_B = ctx.locks.get('baryogenesis', {}).get('eta_B', eta_B)

        # Create BBN solver
        Lambda_rate = ctx.locks.get('collapse', {}).get(
            'Lambda_rate_sinv', 1e23)
        ell_length = ctx.locks.get('collapse', {}).get('ell_length_m', 1e-15)
        bbn_solver = UDOFBBNSolver(
            Lambda_rate=Lambda_rate, ell_length=ell_length)

        # Compute BBN abundances
        bbn_result = bbn_solver.compute_bbn_abundances(eta_B=eta_B)

        # Check if abundances are within observed ranges
        # Y_p: 0.2449 ± 0.0040 (PDG 2022)
        # D/H: 2.547e-5 ± 0.025e-5
        Y_p_obs = 0.2449
        Y_p_err = 0.0040
        D_H_obs = 2.547e-5
        D_H_err = 0.025e-5

        Y_p_match = abs(bbn_result.Y_p - Y_p_obs) < 2.5 * Y_p_err
        D_H_match = abs(bbn_result.D_H - D_H_obs) < 3.5 * D_H_err
        bbn_ok = Y_p_match and D_H_match

        result.tests.append(TestResult(
            test_name="bbn_preserved", status="PASS" if bbn_ok else "FAIL",
            value=f"Y_p: {bbn_result.Y_p:.4f}, D/H: {bbn_result.D_H:.2e}",
            expected=f"Y_p: {Y_p_obs:.4f}±{Y_p_err:.4f}, D/H: {D_H_obs:.2e}±{D_H_err:.2e}",
            notes=f"COMPUTED: Y_p within {abs(bbn_result.Y_p - Y_p_obs)/Y_p_err:.1f}σ, D/H within {abs(bbn_result.D_H - D_H_obs)/D_H_err:.1f}σ"
        ))
        result.n_pass += 1 if bbn_ok else 0
        result.n_fail += 0 if bbn_ok else 1
    except ImportError:
        result.tests.append(TestResult(
            test_name="bbn_preserved", status="SKIP",
            value=None, expected="Standard BBN predictions",
            notes="bbn_solver module not available"
        ))
        result.n_skip += 1
    except Exception as e:
        result.tests.append(TestResult(
            test_name="bbn_preserved", status="ERROR",
            value=None, expected="Standard BBN predictions",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1

    return result
