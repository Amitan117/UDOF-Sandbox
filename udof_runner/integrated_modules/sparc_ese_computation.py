#!/usr/bin/env python3
"""
SPARC ESE Structure Function Computation
=========================================

Integrated version of compute_S_ESE_proper with dependency handling.
Computes proper S_ESE(r) from ESE framework for SPARC rotation curves.

This module handles imports gracefully, falling back if prime0 modules unavailable.
"""

import numpy as np
import sys
from pathlib import Path
import warnings
from typing import Dict, Any, Optional, Tuple

# Physical constants
KPC_TO_M = 3.0857e19  # kpc to meters
M_SUN = 1.98847e30  # Solar mass [kg]

# Self-contained sandbox implementation (no external project imports)
ESE_MODULES_AVAILABLE = True


def compute_X_from_observables(
    Sigma_b: np.ndarray,
    sigma_g: np.ndarray,
    eta_star: float,
    p: float,
    Sigma0: float,
    sigma0: float,
) -> np.ndarray:
    """
    Compute control variable X from observables (self-contained).

    X = (Sigma_b / Sigma0)^eta_star * (sigma_g / sigma0)^p
    """
    Sigma_b = np.asarray(Sigma_b, dtype=float)
    sigma_g = np.asarray(sigma_g, dtype=float)
    Sigma0 = max(float(Sigma0), 1e-30)
    sigma0 = max(float(sigma0), 1e-30)

    X = (np.maximum(Sigma_b, 1e-30) / Sigma0) ** float(eta_star) * \
        (np.maximum(sigma_g, 1e-30) / sigma0) ** float(p)
    return np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)


def compute_dX_dr(
    r_m: np.ndarray,
    Sigma_b: np.ndarray,
    sigma_g: np.ndarray,
    eta_star: float,
    p: float,
    Sigma0: float,
    sigma0: float,
) -> np.ndarray:
    """Numerical gradient dX/dr on the provided radius grid."""
    r_m = np.asarray(r_m, dtype=float)
    X = compute_X_from_observables(Sigma_b, sigma_g, eta_star, p, Sigma0, sigma0)
    if r_m.size < 2:
        return np.zeros_like(X)
    # Use np.gradient with spacing r_m (handles non-uniform grids)
    dX_dr = np.gradient(X, r_m, edge_order=1)
    return np.nan_to_num(dX_dr, nan=0.0, posinf=0.0, neginf=0.0)


class _ESELocalBase:
    """Minimal self-contained ESE map + derivatives."""

    def __init__(self, ell_IR: float, ell_star: float, k: float, X0: float):
        self.ell_IR = float(ell_IR)
        self.ell_star = float(ell_star)
        self.k = float(k)
        self.X0 = float(X0)

    def compute_s(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        X_safe = np.maximum(X, 1e-30)
        z = self.k * (np.log(X_safe) - np.log(max(self.X0, 1e-30)))
        return 1.0 / (1.0 + np.exp(-z))

    def compute_ds_dr(self, r_m: np.ndarray, X: np.ndarray, dX_dr_val: np.ndarray) -> np.ndarray:
        # ds/dX = s(1-s) * k / X
        X = np.asarray(X, dtype=float)
        dX_dr_val = np.asarray(dX_dr_val, dtype=float)
        s = self.compute_s(X)
        ds_dX = s * (1.0 - s) * self.k / np.maximum(X, 1e-30)
        return ds_dX * dX_dr_val


class ESEDarkSector(_ESELocalBase):
    """Compat name for gradient/s_activation usage."""


class ESEDarkSectorDerived(_ESELocalBase):
    """Compat name providing an enhancement function F(s)."""

    def compute_F(self, X: np.ndarray) -> np.ndarray:
        # Simple bounded enhancement proxy (self-contained).
        s = self.compute_s(X)
        return 1.0 + 4.0 * s  # O(1) to O(5) boost


def compute_surface_density_profile(
    r_kpc: np.ndarray,
    M_disk: float,  # M☉
    M_gas: float,  # M☉
    r_d: float  # kpc
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute surface density profile Σ(r) from galaxy properties.

    For exponential disk:
        Σ_disk(r) = M_disk / (2π r_d²) × exp(-r/r_d)

    For gas (assume same exponential):
        Σ_gas(r) = M_gas / (2π r_d²) × exp(-r/r_d)

    Total: Σ_b(r) = Σ_disk(r) + Σ_gas(r)

    Also estimate velocity dispersion σ_g(r) (constant for now, ~10 km/s).

    Parameters:
        r_kpc: Radial distances [kpc]
        M_disk: Disk mass [M☉]
        M_gas: Gas mass [M☉]
        r_d: Disk scale radius [kpc]

    Returns:
        Sigma_b: Surface density [kg/m²]
        sigma_g: Velocity dispersion [m/s]
    """
    r_m = r_kpc * KPC_TO_M  # kpc → m
    r_d_m = r_d * KPC_TO_M  # kpc → m

    # Surface density profiles
    Sigma_disk = (M_disk * M_SUN) / (2.0 * np.pi *
                                     r_d_m**2) * np.exp(-r_kpc / r_d)
    Sigma_gas = (M_gas * M_SUN) / (2.0 * np.pi *
                                   r_d_m**2) * np.exp(-r_kpc / r_d)
    Sigma_b = np.maximum(Sigma_disk + Sigma_gas, 1e-10)  # kg/m²

    # Velocity dispersion (simplified: constant ~10 km/s)
    sigma_g = np.full_like(r_kpc, 10.0e3)  # m/s

    return Sigma_b, sigma_g


def compute_S_ESE_from_X(
    r_kpc: np.ndarray,
    X: np.ndarray,
    dX_dr: np.ndarray,
    ese_model: Any,  # ESEDarkSector or ESEDarkSectorDerived
    method: str = "gradient"
) -> np.ndarray:
    """
    Compute ESE structure function S_ESE(r) from X(r) and ESE map.

    Methods:
    1. "gradient": S(r) ∝ |ds/dr| (gradient energy, normalized)
    2. "enhancement": S(r) ∝ F(s) (enhancement factor from ESEDarkSectorDerived)
    3. "combined": S(r) ∝ |ds/dr| × F(s)
    4. "s_activation": S(r) ∝ s(X) (activation function directly)

    Parameters:
        r_kpc: Radial distances [kpc]
        X: Control variable X(r) (dimensionless)
        dX_dr: Gradient dX/dr [1/m]
        ese_model: ESEDarkSector or ESEDarkSectorDerived instance
        method: Method for computing S_ESE

    Returns:
        S_ESE: ESE structure function (normalized, dimensionless)
    """
    r_m = r_kpc * KPC_TO_M  # kpc → m

    # Compute s(X) from ESE map
    s = ese_model.compute_s(X)

    if method == "gradient":
        # Use gradient: S(r) ∝ |ds/dr| (use absolute value for structure)
        ds_dr = ese_model.compute_ds_dr(r_m, X, dX_dr)
        S_ESE = np.abs(ds_dr)

        # Normalize to peak at ~1, but handle case where all zeros
        max_ds_dr = np.max(S_ESE)

        # Threshold check: Use relative threshold based on typical scale
        mean_ds_dr = np.mean(S_ESE[S_ESE > 0]) if np.any(S_ESE > 0) else 0
        threshold = max(1e-22, mean_ds_dr * 1e-6)  # Relative threshold

        if max_ds_dr > threshold and np.std(S_ESE) > 1e-30:
            # Gradient has meaningful variation - use it
            S_ESE = S_ESE / max_ds_dr
        else:
            # Fallback: use logarithmic gradient instead
            s_safe = np.maximum(s, 1e-10)
            r_safe = np.maximum(r_kpc, 1e-6)  # kpc

            # Compute d(log s)/d(log r) using chain rule
            dlogX_dlogr = (r_kpc * KPC_TO_M / np.maximum(X, 1e-30)) * dX_dr
            ds_dlogX = s_safe * (1 - s_safe) * ese_model.k
            dlogs_dlogr = ds_dlogX * dlogX_dlogr

            S_ESE = np.abs(dlogs_dlogr)
            max_S = np.max(S_ESE)
            if max_S > 1e-10:
                S_ESE = S_ESE / max_S
            else:
                # Final fallback: use s_activation
                warnings.warn(
                    "Gradient method: Both linear and logarithmic gradients too small, falling back to s_activation")
                S_ESE = s

    elif method == "enhancement":
        # Use enhancement factor F(s) from ESEDarkSectorDerived
        if not isinstance(ese_model, ESEDarkSectorDerived):
            raise TypeError(
                f"enhancement method requires ESEDarkSectorDerived, got {type(ese_model)}")

        F = ese_model.compute_F(X)
        S_ESE = F

        # Normalize (F(s) is typically ~1-100, normalize to [0,1] range)
        max_F = np.max(S_ESE)
        if max_F > 1e-10:
            S_ESE = S_ESE / max_F
        else:
            # Fallback to s if F is problematic
            S_ESE = s

    elif method == "combined":
        # Combined: gradient × enhancement
        if not isinstance(ese_model, ESEDarkSectorDerived):
            raise TypeError(
                f"combined method requires ESEDarkSectorDerived, got {type(ese_model)}")

        # Use logarithmic gradient (same approach as gradient method)
        ds_dr = ese_model.compute_ds_dr(r_m, X, dX_dr)
        ds_dr_abs = np.abs(ds_dr)
        max_ds_dr = np.max(ds_dr_abs)
        mean_ds_dr = np.mean(ds_dr_abs[ds_dr_abs > 0]) if np.any(
            ds_dr_abs > 0) else 0
        threshold = max(1e-22, mean_ds_dr * 1e-6)

        if max_ds_dr > threshold and np.std(ds_dr_abs) > 1e-30:
            # Use linear gradient
            gradient_term = ds_dr_abs / max_ds_dr
        else:
            # Use logarithmic gradient
            s_safe = np.maximum(s, 1e-10)
            dlogX_dlogr = (r_kpc * KPC_TO_M / np.maximum(X, 1e-30)) * dX_dr
            ds_dlogX = s_safe * (1 - s_safe) * ese_model.k
            dlogs_dlogr = ds_dlogX * dlogX_dlogr
            gradient_term = np.abs(dlogs_dlogr)
            max_grad = np.max(gradient_term)
            if max_grad > 1e-10:
                gradient_term = gradient_term / max_grad
            else:
                gradient_term = s  # Fallback

        F = ese_model.compute_F(X)

        # Combine: gradient × enhancement
        S_ESE = gradient_term * F

        # Normalize
        max_S = np.max(S_ESE)
        if max_S > 1e-10:
            S_ESE = S_ESE / max_S
        else:
            # Fallback to s if both terms are problematic
            S_ESE = s

    elif method == "s_activation":
        # Simple: S(r) = s(X) (activation function directly)
        S_ESE = s

    else:
        raise ValueError(f"Unknown method: {method}")

    return S_ESE


def compute_S_ESE_proper(
    r_kpc: np.ndarray,
    M_disk: float,  # M☉
    M_gas: float,  # M☉
    r_d: float,  # kpc
    locks: Optional[Dict[str, Any]] = None,
    method: str = "gradient"
) -> Optional[np.ndarray]:
    """
    Compute proper S_ESE(r) from ESE framework.

    Full pipeline:
    1. Σ_b(r) from galaxy properties
    2. X(r) = (Σ_b/Σ₀)^η* × (σ_g/σ₀)^p
    3. s(X) from ESE map
    4. S_ESE(r) from ESE physics

    Parameters:
        r_kpc: Radial distances [kpc]
        M_disk: Disk mass [M☉]
        M_gas: Gas mass [M☉]
        r_d: Disk scale radius [kpc]
        locks: UDOF lock parameters (optional)
        method: Method for computing S_ESE ("gradient", "enhancement", "combined", "s_activation")

    Returns:
        S_ESE: ESE structure function (dimensionless), or None if modules unavailable
    """
    # Self-contained sandbox: always available (local implementation)

    # Get pivot values from locks or defaults
    if locks is None:
        locks = {}

    # Handle different lock structures (v4.0 format)
    calibrated = locks.get('calibrated_locks', {})
    pivots = locks.get('pivots', {})
    ese_map = locks.get('ese_map', {})

    # Get parameters with fallbacks
    Sigma0 = pivots.get('Sigma0_kg_m2', 0.217)  # kg/m²
    sigma0 = pivots.get('sigma0_m_s', 10000.0)  # m/s
    eta_star = calibrated.get('eta_star', pivots.get(
        'eta_star', 0.171))  # From calibrated_locks
    p = pivots.get('p', 0.2)  # Velocity dispersion exponent

    # ESE parameters from locks
    ell_IR = ese_map.get('ell_IR', 4.7e-5)  # m
    ell_star = ese_map.get('ell_star', 2e-15)  # m
    k_ese = ese_map.get('k', 1.5)  # ESE sigmoid slope
    X0 = calibrated.get('X0', pivots.get('X0', 0.6481)
                        )  # From calibrated_locks

    # Compute surface density profile
    Sigma_b, sigma_g = compute_surface_density_profile(
        r_kpc, M_disk, M_gas, r_d)

    # Compute X(r) from observables
    X = compute_X_from_observables(
        Sigma_b, sigma_g, eta_star, p, Sigma0, sigma0)

    # Compute dX/dr using gradient function
    r_m = r_kpc * KPC_TO_M  # kpc → m
    dX_dr = compute_dX_dr(r_m, Sigma_b, sigma_g, eta_star, p, Sigma0, sigma0)

    # Ensure dX_dr is finite (gradient may have issues at boundaries)
    dX_dr = np.nan_to_num(dX_dr, nan=0.0, posinf=0.0, neginf=0.0)

    # Create ESE model - use ESEDarkSectorDerived for enhancement/combined methods
    if method in ["enhancement", "combined"]:
        ese_model = ESEDarkSectorDerived(ell_IR, ell_star, k_ese, X0)
    else:
        ese_model = ESEDarkSector(ell_IR, ell_star, k_ese, X0)

    # Compute S_ESE(r)
    S_ESE = compute_S_ESE_from_X(r_kpc, X, dX_dr, ese_model, method=method)

    return S_ESE
