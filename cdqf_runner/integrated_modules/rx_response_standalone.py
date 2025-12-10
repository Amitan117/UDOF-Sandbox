#!/usr/bin/env python3
"""
Standalone R_X Response Computation
===================================

Extracted from TSESEResponseDerivation without CLASS/ProperCorrectedGrowth dependency.
Implements scale-dependent response function R_X(a,k) from TS-ESE kernel.

This is a standalone version for the validation runner.
"""

import numpy as np
from scipy.interpolate import interp1d
from typing import Optional

# Import standalone growth for ξ(a) computation
try:
    from .proper_growth_standalone import ProperGrowthStandalone
except ImportError:
    # Fallback for direct import
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from proper_growth_standalone import ProperGrowthStandalone


# ESE parameters (defaults, can be overridden)
ELL_IR = 4.7e-5  # meters (IR length scale)
ELL_STAR = 2e-15  # meters (UV length scale)
K_ESE = 1.5  # ESE sigmoid slope parameter
X0_ESE = 0.6481  # ESE transition point (from calibrated locks)


class RXResponseStandalone:
    """
    Standalone R_X(a,k) computation without CLASS dependency.

    Derives C_X(a) and R_X(a,k) from TS-ESE kernel structure.
    Uses standalone growth computation for ξ(a) = C_X(a).
    """

    def __init__(
        self,
        H0: float,
        Omega_m: float,
        Omega_b: float,
        Omega_geom_0: float,
        alpha_geom: float,
        p_op: float,
        ell_IR: float = ELL_IR,
        ell_star: float = ELL_STAR,
        k_ese: float = K_ESE,
        X0: float = X0_ESE
    ):
        """
        Initialize with CDQF parameters and ESE structure.

        Parameters:
            H0: Hubble constant [km/s/Mpc]
            Omega_m: Total matter density
            Omega_b: Baryon density
            Omega_geom_0: Geometric DM normalization
            alpha_geom: Geometry coupling
            p_op: Operational scale trajectory
            ell_IR: IR length scale [m]
            ell_star: UV length scale [m]
            k_ese: ESE sigmoid slope
            X0: ESE transition point
        """
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.Omega_geom_0 = Omega_geom_0
        self.alpha_geom = alpha_geom
        self.p_op = p_op

        # ESE parameters
        self.ell_IR = ell_IR
        self.ell_star = ell_star
        self.k_ese = k_ese
        self.X0 = X0

        # Derived quantities
        self.epsilon = -alpha_geom * p_op  # Background exponent

        # Initialize standalone growth for ξ(a) computation
        self.growth = ProperGrowthStandalone(
            H0=H0,
            Omega_m=Omega_m,
            Omega_b=Omega_b,
            Omega_geom_0=Omega_geom_0,
            alpha_geom=alpha_geom,
            p_op=p_op,
            a_pivot=0.95,
            beta_ESE=-0.10,
            use_mu_eff=True
        )

        # Compute C_X(a) from ξ(a)
        self._derive_C_X()

        # Set up R_X with constraint R_X(k=0.1) ≈ 1
        self._derive_R_X()

    def _derive_C_X(self, a_min: float = 0.001, a_max: float = 1.0, n_points: int = 1000):
        """
        Derive C_X(a) from TS-ESE structure.

        For the local model (R_X=1), we have validated that:
            C_X(a) = ξ(a)

        where ξ(a) is the clustering fraction from the pivot decomposition.
        """
        a_grid = np.logspace(np.log10(a_min), np.log10(a_max), n_points)
        C_X_a = np.zeros_like(a_grid)

        # Use the validated ξ(a) as C_X(a) for local model
        for i, a in enumerate(a_grid):
            # C_X(a) = ξ(a) for local response model
            xi_a = self.growth.xi_clustering_fraction(a)
            C_X_a[i] = xi_a

        # Store for interpolation
        self.a_grid_CX = a_grid
        self.C_X_grid = C_X_a

        # Create interpolator
        self._C_X_interp = interp1d(
            a_grid,
            C_X_a,
            kind='linear',
            bounds_error=False,
            fill_value=(C_X_a[0], C_X_a[-1])
        )

    def _derive_R_X(self):
        """
        Derive R_X(a,k) from TS-ESE kernel structure.

        Constraint: R_X(k=0.1 h/Mpc) ≈ 1 (from k_star MCMC)

        Model: R_X(a,k) = 1 / [1 + (k/k_⋆(a))^n]
        where k_⋆(a) is the scale where non-locality becomes important.
        """
        # Constraint: R_X(k=0.1) ≈ 1 means k_⋆ must be >> 0.1
        # From k_star MCMC: median k_star ≈ 4.77 h/Mpc
        self.k_star_constraint = 4.77  # h/Mpc (from MCMC validation)

        # Use constraint value but make it scale-dependent
        # At early times (small a), structures are smaller, so k_⋆ might be larger
        # Model: k_⋆(a) = k_⋆_0 × a^(-α_scale)
        self.k_star_0 = self.k_star_constraint
        # Can be tuned (0 = constant, >0 = increases with z)
        self.alpha_scale = 0.0

        # Power law index for R_X (2 = quadratic suppression, higher = sharper)
        self.n_power = 2

    def C_X(self, a: float) -> float:
        """Get response coefficient C_X(a)."""
        if np.isscalar(a):
            return float(self._C_X_interp(a))
        else:
            return self._C_X_interp(a)

    def k_star(self, a: float) -> float:
        """
        Characteristic scale for non-locality: k_⋆(a).

        This is the wavenumber where non-locality becomes important.
        """
        return self.k_star_0 * (a ** (-self.alpha_scale))

    def R_X(self, a: float, k: float, use_constraint: bool = True) -> float:
        """
        Scale-dependent response function R_X(a,k).

        Model: R_X(a,k) = 1 / [1 + (k/k_⋆(a))^n]

        Properties:
        - R_X(k << k_⋆) ≈ 1 (local response)
        - R_X(k >> k_⋆) ≈ 0 (non-local, suppressed)
        - Constraint: R_X(k=0.1) ≈ 1 → k_⋆ >> 0.1

        Parameters:
            a: Scale factor(s)
            k: Wavenumber(s) [h/Mpc]
            use_constraint: If True, enforce R_X(k=0.1) ≈ 1

        Returns:
            R_X values
        """
        # Handle scalar vs array inputs
        is_scalar = np.isscalar(a) and np.isscalar(k)

        # Convert to arrays for broadcasting
        a_arr = np.asarray(a)
        k_arr = np.asarray(k)
        a_arr, k_arr = np.broadcast_arrays(a_arr, k_arr)

        # Get k_⋆(a)
        k_star_a = self.k_star(a_arr)

        # Compute R_X
        k_ratio = k_arr / np.maximum(k_star_a, 1e-6)
        R_X = 1.0 / (1.0 + (k_ratio ** self.n_power))

        # Enforce constraint: R_X(k=0.1) ≈ 1
        if use_constraint:
            # For k <= 0.1, ensure R_X is very close to 1
            mask = k_arr <= 0.1
            if np.any(mask):
                # Force R_X = 1 for k <= 0.1
                R_X = np.where(mask, 1.0, R_X)

        if is_scalar:
            return float(R_X)
        else:
            return R_X
