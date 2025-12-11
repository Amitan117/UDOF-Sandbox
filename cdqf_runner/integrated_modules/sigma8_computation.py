"""
Sigma-8 (σ₈) Computation from Matter Power Spectrum

Computes σ₈ by integrating P(k) with top-hat window function.
σ₈² = (1/(2π²)) ∫ P(k) W²(kR) k² dk
where R = 8 h⁻¹ Mpc and W is the top-hat window function.
"""

import numpy as np
from typing import Dict, Optional
from scipy.integrate import quad
from scipy.special import spherical_jn

# Physical constants
M_SUN_KG = 1.989e30
G_SI = 6.67430e-11
C = 299792458.0
HBAR = 1.054571817e-34


def top_hat_window(kR: np.ndarray) -> np.ndarray:
    """
    Top-hat window function in Fourier space.
    
    W(kR) = 3 * [sin(kR) - kR*cos(kR)] / (kR)³
    
    Parameters:
    -----------
    kR : array
        Dimensionless wavenumber k * R
    
    Returns:
    --------
    W : array
        Window function
    """
    kR = np.asarray(kR)
    # Avoid division by zero
    mask = np.abs(kR) < 1e-10
    W = np.zeros_like(kR)
    
    # For small kR, use Taylor expansion: W(kR) ≈ 1 - (kR)²/10
    W[mask] = 1.0 - kR[mask]**2 / 10.0
    
    # For larger kR, use exact formula
    kR_large = kR[~mask]
    W[~mask] = 3.0 * (np.sin(kR_large) - kR_large * np.cos(kR_large)) / kR_large**3
    
    return W


def compute_eisenstein_hu_pk(
    k_h_Mpc: np.ndarray,
    h: float = 0.674,
    Omega_m: float = 0.315,
    Omega_b: float = 0.0493,
    n_s: float = 0.965,
    A_s: float = 2.1e-9
) -> np.ndarray:
    """
    Compute linear matter power spectrum using Eisenstein-Hu (1998) formula.
    
    Parameters:
    -----------
    k_h_Mpc : array
        Wavenumbers in h/Mpc
    h : float
        Hubble parameter h = H0/100
    Omega_m : float
        Matter density parameter
    Omega_b : float
        Baryon density parameter
    n_s : float
        Scalar spectral index
    A_s : float
        Primordial amplitude
    
    Returns:
    --------
    P_k : array
        Power spectrum in (Mpc/h)³
    """
    k_h_Mpc = np.asarray(k_h_Mpc)
    
    # Physical densities
    omega_m = Omega_m * h**2
    omega_b = Omega_b * h**2
    
    # Sound horizon (Mpc)
    s = 44.5 * np.log(9.83 / omega_m) / np.sqrt(1.0 + 10.0 * omega_b**0.75)
    
    # Equality scale (h/Mpc)
    k_eq = 7.46e-2 * omega_m / h
    
    # Transfer function (Eisenstein-Hu)
    q = k_h_Mpc / (13.41 * k_eq)
    
    # CDM transfer function
    L = np.log(2.0 * np.e + 1.8 * q)
    C = 14.2 + 386.0 / (1.0 + 69.9 * q**1.08)
    T_0 = L / (L + C * q**2)
    
    # Baryon suppression
    alpha_b = 2.07 * k_eq * s * (1.0 + omega_b / omega_m)**(-0.75)
    T_b = T_0 / (1.0 + (k_h_Mpc * s / 5.4)**2)
    
    # Total transfer function
    f_b = Omega_b / Omega_m
    f_c = 1.0 - f_b
    T_k = f_c * T_0 + f_b * T_b * np.sinc(k_h_Mpc * s / np.pi)
    
    # Primordial power spectrum
    k_pivot = 0.05  # Mpc^-1
    P_k = A_s * (k_h_Mpc * h / k_pivot)**(n_s - 1.0) * T_k**2
    
    return P_k


def compute_sigma8_from_pk(
    k_array: np.ndarray,
    P_k_array: np.ndarray,
    R_Mpc_h: float = 8.0,
    h: float = 0.674
) -> float:
    """
    Compute σ₈ from power spectrum.
    
    σ₈² = (1/(2π²)) ∫ P(k) W²(kR) k² dk
    
    Parameters:
    -----------
    k_array : array
        Wavenumbers in h/Mpc
    P_k_array : array
        Power spectrum in (Mpc/h)³
    R_Mpc_h : float
        Filter radius in Mpc/h (default: 8.0 for σ₈)
    h : float
        Hubble parameter
    
    Returns:
    --------
    sigma8 : float
        σ₈ value
    """
    k_array = np.asarray(k_array)
    P_k_array = np.asarray(P_k_array)
    
    # Integrand: P(k) * W²(kR) * k² / (2π²)
    kR = k_array * R_Mpc_h
    W_kR = top_hat_window(kR)
    
    integrand = P_k_array * W_kR**2 * k_array**2 / (2.0 * np.pi**2)
    
    # Integrate using trapezoidal rule (log-space is better for power spectrum)
    # Use log integration for better accuracy
    log_k = np.log(k_array)
    sigma8_sq = np.trapz(integrand * k_array, log_k)  # d(ln k) = dk/k
    
    sigma8 = np.sqrt(max(0, sigma8_sq))
    
    return float(sigma8)


def compute_sigma8(
    h: float = 0.674,
    Omega_m: float = 0.315,
    Omega_b: float = 0.0493,
    n_s: float = 0.965,
    A_s: float = 2.1e-9,
    k_min: float = 1e-4,
    k_max: float = 10.0,
    n_k: int = 200
) -> Dict[str, float]:
    """
    Compute σ₈ from cosmological parameters.
    
    Parameters:
    -----------
    h : float
        Hubble parameter
    Omega_m : float
        Matter density
    Omega_b : float
        Baryon density
    n_s : float
        Spectral index
    A_s : float
        Primordial amplitude
    k_min, k_max : float
        Integration range (h/Mpc)
    n_k : int
        Number of k points
    
    Returns:
    --------
    dict with 'sigma8' value and integration details
    """
    # Create k array (log-spaced for better integration)
    k_array = np.logspace(np.log10(k_min), np.log10(k_max), n_k)
    
    # Compute power spectrum
    P_k = compute_eisenstein_hu_pk(k_array, h, Omega_m, Omega_b, n_s, A_s)
    
    # Compute σ₈
    sigma8 = compute_sigma8_from_pk(k_array, P_k, R_Mpc_h=8.0, h=h)
    
    return {
        'sigma8': sigma8,
        'R_Mpc_h': 8.0,
        'k_min': k_min,
        'k_max': k_max,
        'n_k': n_k,
        'method': 'Eisenstein-Hu power spectrum + top-hat filter'
    }

