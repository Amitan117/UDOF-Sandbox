"""
Domain: Dark Energy

Tests dark energy equation of state from UDOF dark sector parameters.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult


def run(ctx: DomainContext) -> DomainResult:
    """Run dark energy tests."""
    result = DomainResult(domain_name="dark_energy")

    Om = ctx.locks['cosmology']['Om']
    OL = 1 - Om

    result.tests.append(TestResult(
        test_name="de_dominance", status="PASS" if OL > Om else "FAIL",
        value=OL, expected=f"> {Om}"
    ))
    result.n_pass += 1 if OL > Om else 0
    result.n_fail += 0 if OL > Om else 1

    # Compute w from UDOF dark sector parameters
    try:
        dark_sector = ctx.locks.get('dark_sector', {})
        alpha_geom = dark_sector.get('alpha_geom', -0.1885)
        p_op = dark_sector.get('p_op', 0.7577)

        # w_eff = -1 - (α_geom × p_op) / 3
        w_eff = -1.0 - (alpha_geom * p_op) / 3.0
        w_obs = -1.0  # Observed dark energy EOS

        error = abs(w_eff - w_obs)
        passed = error < 0.1  # Allow 10% deviation from -1

        result.tests.append(TestResult(
            test_name="w_eos", status="PASS" if passed else "FAIL",
            value=w_eff, expected=f"{w_obs} (observed)",
            error=error,
            notes=f"COMPUTED: w = -1 - (α_geom×p_op)/3 = {w_eff:.4f} (α={alpha_geom:.4f}, p_op={p_op:.4f})"
        ))
        result.n_pass += 1 if passed else 0
        result.n_fail += 0 if passed else 1
    except Exception as e:
        result.tests.append(TestResult(
            test_name="w_eos", status="ERROR",
            value=None, expected="-1.0",
            notes=f"COMPUTATION FAILED: {str(e)}"
        ))
        result.n_error += 1

    return result

