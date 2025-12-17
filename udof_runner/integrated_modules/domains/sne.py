"""
Domain: SNe Ia (Supernovae)

Tests UDOF cosmology predictions against Pantheon+SH0ES supernova data.
"""

from integrated_modules.domains.context import DomainContext
from integrated_modules.core.constants import SCIPY_AVAILABLE
from integrated_modules.types import DomainResult, TestResult
import numpy as np


def run(ctx: DomainContext) -> DomainResult:
    """Run SNe tests."""
    result = DomainResult(domain_name="sne")

    if not SCIPY_AVAILABLE:
        result.tests.append(TestResult(
            test_name="sne_chi2", status="SKIP", value=None, notes="scipy required"
        ))
        result.n_skip = 1
        return result

    try:
        sne_data = ctx.data_loader.load_sne_pantheon()
    except Exception as e:
        result.tests.append(TestResult(
            test_name="sne_chi2", status="ERROR", value=None, notes=str(e)
        ))
        result.n_error = 1
        return result

    z = sne_data['z']
    mu_obs = sne_data['mu']
    sigma = sne_data['sigma']

    # Distance modulus: mu = 5 * log10(D_L / 10pc)
    # D_L = (1+z) * D_M in Mpc
    mu_pred = []
    for zi in z:
        D_M = ctx.formulas.comoving_distance(zi)
        D_L = (1 + zi) * D_M  # Luminosity distance in Mpc
        # 25 = 5*log10(1 Mpc / 10 pc)
        mu_pred.append(5 * np.log10(D_L) + 25)

    mu_pred = np.array(mu_pred)

    # Fit for absolute magnitude offset
    M_offset = np.mean(mu_obs - mu_pred)
    mu_pred_adj = mu_pred + M_offset

    chi2 = float(np.sum(((mu_obs - mu_pred_adj) / sigma)**2))
    n_dof = len(z) - 2
    chi2_nu = chi2 / n_dof if n_dof > 0 else chi2
    passed = chi2_nu < 2.0

    result.tests.append(TestResult(
        test_name="sne_chi2", status="PASS" if passed else "FAIL",
        value=chi2_nu, expected="< 2.0", chi2=chi2,
        notes=f"Pantheon+, {len(z)} points, chi2={chi2:.2f}"
    ))
    result.n_pass += 1 if passed else 0
    result.n_fail += 0 if passed else 1

    return result

