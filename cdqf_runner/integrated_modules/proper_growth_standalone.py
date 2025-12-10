#!/usr/bin/env python3
"""
Standalone Proper Corrected Growth Computation
===============================================

Extracted from ProperCorrectedGrowth without CLASS dependency.
Implements corrected growth equation with:
- Clustering fraction ξ(a)
- Effective gravitational coupling μ_eff(a)

This is a standalone version for the validation runner.
"""

import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d
from typing import Optional, Tuple


class ProperGrowthStandalone:
    """
    Standalone growth factor computation without CLASS dependency.

    Implements:
    - Clustering fraction ξ(a) from pivot decomposition
    - Effective gravitational coupling μ_eff(a)
    - Corrected growth ODE: D'' + [2 + dlnH/dlna] D' - (3/2) μ_eff(a) Ω_cl(a) D = 0
    """

    def __init__(
        self,
        H0: float,
        Omega_m: float,
        Omega_b: float,
        Omega_geom_0: float,
        alpha_geom: float,
        p_op: float,
        a_pivot: float = 0.95,
        beta_ESE: float = -0.10,
        use_mu_eff: bool = True
    ):
        """
        Initialize with CDQF parameters.

        Parameters:
            H0: Hubble constant [km/s/Mpc]
            Omega_m: Total matter density
            Omega_b: Baryon density
            Omega_geom_0: Geometric DM normalization (today)
            alpha_geom: Geometry coupling
            p_op: Operational scale trajectory
            a_pivot: Pivot scale factor for ξ(a) decomposition
            beta_ESE: ESE enhancement parameter for μ_eff
            use_mu_eff: If True, include ESE modifications to μ
        """
        self.H0 = H0
        self.h = H0 / 100.0
        self.Omega_m = Omega_m
        self.Omega_b = Omega_b
        self.Omega_geom_0 = Omega_geom_0
        self.alpha_geom = alpha_geom
        self.p_op = p_op
        self.a_pivot = a_pivot
        self.beta_ESE = beta_ESE
        self.use_mu_eff = use_mu_eff

        # Derived quantities
        self.Omega_cdm = Omega_m - Omega_b
        self.Omega_Lambda = 1.0 - Omega_m

        # Background exponent
        alpha_p_op = alpha_geom * p_op
        self.w_eff = -(alpha_p_op) / 3.0
        self.epsilon = alpha_p_op

        # Growth factor interpolators (computed on demand)
        self._z_growth = None
        self._D_growth = None
        self._dD_dlna_growth = None
        self._growth_computed = False

    def Omega_dm_cdqf(self, a: float) -> float:
        """
        Dark matter density parameter at scale factor a.

        Ω_dm(a) = Ω_geom₀ × [μ_op(a)/μ_op(1)]^α_geom × a^-3
        """
        # μ_op(a) ∝ a^(-p_op)
        mu_a = a ** (-self.p_op)
        mu_1 = 1.0 ** (-self.p_op)  # = 1

        # ρ_geom ∝ [μ_op(a)/μ_op(1)]^α_geom × a^-3
        rho_ratio = (mu_a / mu_1) ** self.alpha_geom
        return self.Omega_geom_0 * rho_ratio * (a ** (-3.0))

    def xi_clustering_fraction(self, a: float) -> float:
        """
        Clustering fraction ξ(a) from pivot decomposition.

        Decomposes ρ_geom into:
        - Clustering piece: ρ_cl ∝ a^{-3} (fixed at pivot)
        - Smooth piece: ρ_smooth = ρ_geom - ρ_cl

        Then: ξ(a) = ρ_cl(a) / ρ_geom(a)

        Properties:
        - ξ(a_pivot) = 1
        - ξ(a) ≈ 1 at early times (a < a_pivot)
        - ξ(a) < 1 at late times (a > a_pivot)
        """
        # Geometric DM density
        rho_geom_a = self.Omega_geom_0 * (a ** (-3.0 + self.epsilon))

        # At pivot: ρ_cl,0 = ρ_geom(a_pivot)
        rho_cl_pivot = self.Omega_geom_0 * \
            (self.a_pivot ** (-3.0 + self.epsilon))

        # Clustering piece: evolves as a^{-3} from pivot
        rho_cl_a = rho_cl_pivot * ((a / self.a_pivot) ** (-3.0))

        # Clustering fraction
        if rho_geom_a > 0:
            xi = rho_cl_a / rho_geom_a
            # Ensure 0 <= xi <= 1
            xi = max(0.0, min(1.0, xi))
        else:
            xi = 1.0

        return xi

    def mu_effective(self, a: float) -> float:
        """
        Effective gravitational coupling μ_eff(a) = 1 + δμ_ESE(a).

        Simplified: μ_eff = 1 + β_ESE * (1 - s_bar(a))
        where s_bar(a) is an averaged ESE activation.
        """
        if not self.use_mu_eff:
            return 1.0

        # Simplified ESE activation: s_bar(a) = a^2
        # (screened at early times, active at late times)
        s_bar = a ** 2

        # μ_eff = 1 + β_ESE * (1 - s_bar)
        mu_eff = 1.0 + self.beta_ESE * (1.0 - s_bar)

        return mu_eff

    def Omega_clustering(self, a: float) -> float:
        """
        Effective clustering density parameter.

        Ω_cl(a) = Ω_b(a) + ξ(a) Ω_geom(a)
        """
        # Baryons (always cluster)
        Omega_b_a = self.Omega_b * (a ** (-3.0))

        # Geometric DM (clustering fraction)
        xi_a = self.xi_clustering_fraction(a)
        Omega_geom_a = self.Omega_geom_0 * (a ** (-3.0 + self.epsilon))

        Omega_cl = Omega_b_a + xi_a * Omega_geom_a

        return Omega_cl

    def _growth_ode_corrected(self, y: np.ndarray, lna: float) -> np.ndarray:
        """
        Corrected growth ODE.

        D'' + [2 + dlnH/dlna] D' - (3/2) μ_eff(a) Ω_cl(a) D = 0

        Uses proper clustering density and ESE modifications.
        """
        D, dD_dlna = y
        a = np.exp(lna)

        # Effective clustering matter
        Omega_cl_a = self.Omega_clustering(a)

        # Effective gravitational coupling
        mu_eff_a = self.mu_effective(a)

        # d ln H / d ln a (approximation)
        # From original CDQFBoltzmannFull._growth_ode:
        # Uses simplified: dlnH/dlna ≈ 1.5 * Omega_m(a)
        # This is exact for matter-dominated and close for CDQF modified expansion

        # Matter density parameter at scale factor a (CDQF modified)
        Omega_dm_a = self.Omega_dm_cdqf(a)
        Omega_b_a = self.Omega_b * (a ** (-3.0))
        Omega_m_a = Omega_dm_a + Omega_b_a

        # Simplified: dlnH/dlna ≈ 1.5 * Omega_m(a)
        # This matches the original implementation and is stable
        dlnH_dlna = 1.5 * Omega_m_a

        # Corrected growth equation
        # D'' + [2 + dlnH/dlna] D' - (3/2) μ_eff Ω_cl D = 0
        d2D_dlna2 = -(2.0 + dlnH_dlna) * dD_dlna + \
            (3.0/2.0) * mu_eff_a * Omega_cl_a * D

        return np.array([dD_dlna, d2D_dlna2])

    def compute_growth_factor_corrected(
        self, a_init: float = 0.001, n_points: int = 1000
    ) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Compute growth factor using corrected equation.

        Returns:
            (z_grid, D_grid) or None if computation fails
        """
        # Array of ln(a)
        lna_init = np.log(a_init)
        lna_today = 0.0
        lna_arr = np.linspace(lna_init, lna_today, n_points)

        # Initial conditions
        D_init = a_init
        dD_dlna_init = a_init
        y0 = np.array([D_init, dD_dlna_init])

        # Solve ODE
        try:
            solution = odeint(
                self._growth_ode_corrected,
                y0,
                lna_arr,
                atol=1e-8,
                rtol=1e-8
            )
            D_arr = solution[:, 0]
            dD_dlna_arr = solution[:, 1]

            if np.any(~np.isfinite(D_arr)) or np.any(D_arr <= 0):
                return None
        except Exception:
            return None

        # Normalize to D(a=1) = 1
        D_today = D_arr[-1]
        if D_today > 0 and np.isfinite(D_today):
            D_arr = D_arr / D_today
            dD_dlna_arr = dD_dlna_arr / D_today
        else:
            return None

        # Convert to redshift
        a_arr = np.exp(lna_arr)
        z_arr = 1.0 / a_arr - 1.0

        # Store for interpolation (increasing z order)
        z_grid = z_arr[::-1]
        D_grid = D_arr[::-1]
        dD_dlna_grid = dD_dlna_arr[::-1]

        self._z_growth = z_grid
        self._D_growth = D_grid
        self._dD_dlna_growth = dD_dlna_grid
        self._growth_computed = True

        return z_grid, D_grid

    def growth_factor(self, z: float) -> float:
        """
        Growth factor D(z) normalized to D(0) = 1.

        Parameters:
            z: Redshift

        Returns:
            Growth factor D(z)
        """
        if not self._growth_computed:
            result = self.compute_growth_factor_corrected()
            if result is None:
                return np.nan

        if self._z_growth is None or len(self._z_growth) == 0:
            return np.nan

        return np.interp(z, self._z_growth, self._D_growth)

    def growth_rate(self, z: float) -> float:
        """
        Growth rate f(z) = d(ln D)/d(ln a).

        Parameters:
            z: Redshift

        Returns:
            Growth rate f(z)
        """
        if not self._growth_computed:
            result = self.compute_growth_factor_corrected()
            if result is None:
                return np.nan

        if self._z_growth is None or len(self._z_growth) == 0:
            return np.nan

        D_z = np.interp(z, self._z_growth, self._D_growth)
        dD_dlna_z = np.interp(z, self._z_growth, self._dD_dlna_growth)

        if D_z > 0:
            return dD_dlna_z / D_z
        return np.nan
