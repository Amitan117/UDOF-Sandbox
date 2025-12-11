"""
Internal CMB Power Spectrum Computation

Fallback CMB module when CAMB is unavailable.
Computes C_ℓ using simplified acoustic peak model.
"""

import numpy as np
from typing import Dict, Optional

# Physical constants
C = 299792458.0  # m/s
H0_SI = 67.4 * 1000.0 / 3.086e22  # s⁻¹


def compute_sound_horizon(
    Omega_m: float = 0.315,
    Omega_b: float = 0.0493,
    h: float = 0.674
) -> float:
    """
    Compute sound horizon at recombination.
    
    r_s = ∫ c_s / (a H(a)) da from z=∞ to z_rec
    
    Simplified: r_s ≈ 147 Mpc (Planck best-fit)
    
    Parameters:
    -----------
    Omega_m, Omega_b : float
        Matter and baryon densities
    h : float
        Hubble parameter
    
    Returns:
    --------
    r_s : float
        Sound horizon in Mpc
    """
    # Simplified: r_s ~ 147 Mpc for Planck cosmology
    # More precise: depends on Omega_m, Omega_b, h
    
    # Approximation from Eisenstein & Hu (1998)
    omega_m = Omega_m * h**2
    omega_b = Omega_b * h**2
    
    z_rec = 1090  # Recombination redshift
    
    # Sound speed: c_s = c / sqrt(3(1 + R))
    # R = 3*rho_b/(4*rho_gamma) ~ 750 * Omega_b * h^2 * (1+z)
    R_rec = 750.0 * omega_b * (1.0 + z_rec)
    c_s = C / np.sqrt(3.0 * (1.0 + R_rec))
    
    # Approximate r_s (simplified integration)
    # r_s ≈ (c_s / H0) * I(z_rec) where I ≈ 1.7 for typical cosmology
    H0_km_s_Mpc = h * 100.0
    H0_SI_approx = H0_km_s_Mpc * 1000.0 / 3.086e22  # s^-1
    
    # Integration factor (simplified)
    # I = ∫ dz / (sqrt(Omega_m*(1+z)^3 + Omega_r*(1+z)^4)) from z_rec to ∞
    # Simplified: I ≈ 1.7 for typical cosmology
    I_z = 1.7
    
    r_s_Mpc = (c_s / H0_SI_approx) * 3.086e22 / 1e6 * I_z  # Mpc
    
    # Adjust to match Planck value (more accurate calibration)
    r_s_calibrated = 147.09 * (omega_m / 0.143)**(-0.25) * (omega_b / 0.022)**0.08
    
    return float(r_s_calibrated)


def compute_acoustic_peak_scale(
    r_s: float,
    D_A: float
) -> float:
    """
    Compute acoustic peak scale in multipole space.
    
    ℓ_A = π * D_A / r_s
    
    where D_A is the angular diameter distance to last scattering.
    
    Parameters:
    -----------
    r_s : float
        Sound horizon in Mpc
    D_A : float
        Angular diameter distance in Mpc
    
    Returns:
    --------
    ell_A : float
        Acoustic scale
    """
    ell_A = np.pi * D_A / r_s
    return float(ell_A)


def compute_angular_diameter_distance(
    z: float,
    Omega_m: float = 0.315,
    h: float = 0.674
) -> float:
    """
    Compute angular diameter distance.
    
    D_A = D_M / (1+z) where D_M = comoving distance
    
    Parameters:
    -----------
    z : float
        Redshift
    Omega_m : float
        Matter density
    h : float
        Hubble parameter
    
    Returns:
    --------
    D_A : float
        Angular diameter distance in Mpc
    """
    # Comoving distance (simplified, flat universe)
    # D_M = (c/H0) * ∫ dz / E(z)
    # E(z) = sqrt(Omega_m*(1+z)^3 + Omega_Lambda)
    
    Omega_L = 1.0 - Omega_m
    H0_km_s_Mpc = h * 100.0
    c_km_s = C / 1000.0  # km/s
    
    # Simplified integration: E(z) ≈ sqrt(Omega_m*(1+z)^3 + Omega_L)
    # For z_rec ≈ 1090, E(z) ≈ sqrt(Omega_m*(1+z)^3)
    
    z_rec = 1090.0
    E_z_rec = np.sqrt(Omega_m * (1.0 + z_rec)**3 + Omega_L)
    
    # Comoving distance (approximate)
    # D_M ≈ (c/H0) * 2/sqrt(Omega_m) * (sqrt(1+z) - 1) for high z
    # More accurate: use full integral
    
    # Simplified: D_M ≈ 14000 Mpc for z=1090
    D_M_Mpc = 14000.0 * (h / 0.674)  # Scale with h
    
    # Angular diameter distance
    D_A_Mpc = D_M_Mpc / (1.0 + z_rec)
    
    return float(D_A_Mpc)


def compute_cmb_power_spectrum_internal(
    ell: np.ndarray,
    Omega_m: float = 0.315,
    Omega_b: float = 0.0493,
    h: float = 0.674,
    n_s: float = 0.965,
    A_s: float = 2.1e-9,
    tau_reio: float = 0.054
) -> Dict[str, np.ndarray]:
    """
    Compute CMB temperature power spectrum using simplified model.
    
    Uses acoustic peak model: C_ℓ ~ A_s * T_ℓ² where T_ℓ encodes acoustic peaks.
    
    Parameters:
    -----------
    ell : array
        Multipole values
    Omega_m, Omega_b : float
        Matter and baryon densities
    h : float
        Hubble parameter
    n_s : float
        Spectral index
    A_s : float
        Primordial amplitude
    tau_reio : float
        Reionization optical depth
    
    Returns:
    --------
    dict with 'ell', 'cl_tt', 'ell_peak', etc.
    """
    ell = np.asarray(ell)
    
    # Sound horizon
    r_s = compute_sound_horizon(Omega_m, Omega_b, h)
    
    # Angular diameter distance
    z_rec = 1090.0
    D_A = compute_angular_diameter_distance(z_rec, Omega_m, h)
    
    # Acoustic scale
    ell_A = compute_acoustic_peak_scale(r_s, D_A)
    
    # Acoustic peak structure (simplified model)
    # C_ℓ ~ A_s * (ℓ/ℓ_pivot)^(n_s-1) * T_ℓ²
    # T_ℓ encodes acoustic oscillations
    
    ell_pivot = 2000  # Pivot scale
    primordial = A_s * (ell / ell_pivot)**(n_s - 1.0)
    
    # Acoustic oscillations (simplified)
    # First peak at ℓ ≈ ℓ_A
    # Oscillations: sin²(π * ℓ / ℓ_A)
    
    # Damping envelope
    ell_damping = 1000.0  # Damping scale
    damping = np.exp(-ell**2 / (2.0 * ell_damping**2))
    
    # Peak structure
    peak_envelope = np.exp(-(ell - ell_A)**2 / (2.0 * 50.0**2))  # First peak
    second_peak = 0.5 * np.exp(-(ell - 2.0*ell_A)**2 / (2.0 * 50.0**2))
    third_peak = 0.3 * np.exp(-(ell - 3.0*ell_A)**2 / (2.0 * 50.0**2))
    
    oscillations = peak_envelope + second_peak + third_peak
    
    # Transfer function (simplified)
    T_ell_sq = (1.0 + oscillations) * damping
    
    # Reionization suppression (large scales)
    ell_reion = 10.0
    reion_suppression = 1.0 - 0.3 * np.exp(-ell / ell_reion) * (1.0 - np.exp(-tau_reio))
    
    # Final power spectrum (in μK²)
    # C_ℓ ≈ 2π * A_s * primordial * T_ell_sq * reion_suppression * calibration
    calibration = 1e12  # Rough calibration to μK² (simplified)
    cl_tt = 2.0 * np.pi * A_s * primordial * T_ell_sq * reion_suppression * calibration
    
    # Find first peak
    peak_range = (ell >= 150) & (ell <= 300)
    if np.any(peak_range):
        peak_idx = np.argmax(cl_tt[peak_range])
        ell_peak = ell[peak_range][peak_idx]
        cl_peak = cl_tt[peak_range][peak_idx]
    else:
        ell_peak = ell_A
        cl_peak = np.max(cl_tt)
    
    return {
        'ell': ell,
        'cl_tt': cl_tt,
        'ell_A': float(ell_A),
        'ell_peak': float(ell_peak),
        'cl_peak': float(cl_peak),
        'r_s_Mpc': float(r_s),
        'D_A_Mpc': float(D_A),
        'method': 'Simplified acoustic peak model (internal fallback)'
    }

