"""
LSS Transition / Structure Growth

Computes structure transition scale and growth factor D(z) including
UDOF structure factor S_struct = δ²/(1+δ²).
"""

import numpy as np
from typing import Dict, Optional, Tuple

# Physical constants
C = 299792458.0  # m/s
G_SI = 6.67430e-11  # m³/(kg·s²)
H0_SI = 67.4 * 1000.0 / 3.086e22  # s⁻¹ (H0 in km/s/Mpc)


def compute_structure_factor(delta: float) -> float:
    """
    Compute UDOF structure factor S_struct = δ²/(1+δ²).
    
    This factor modulates the growth at different density contrasts.
    
    Parameters:
    -----------
    delta : float
        Density contrast δ = ρ/ρ_mean - 1
    
    Returns:
    --------
    S_struct : float
        Structure factor
    """
    delta_sq = delta**2
    return delta_sq / (1.0 + delta_sq)


def compute_transition_scale(
    Omega_m: float = 0.315,
    h: float = 0.674,
    z: float = 0.0
) -> Dict[str, float]:
    """
    Compute structure transition scale (linear to nonlinear).
    
    The transition occurs when δ ~ 1 (nonlinear regime).
    This corresponds to a characteristic wavenumber k_nl or mass scale M_nl.
    
    Parameters:
    -----------
    Omega_m : float
        Matter density parameter
    h : float
        Hubble parameter
    z : float
        Redshift
    
    Returns:
    --------
    dict with transition scale info
    """
    # Linear to nonlinear transition when δ ~ 1
    # Using spherical collapse: δ_c ≈ 1.686
    
    # Characteristic transition wavenumber (approximate)
    # k_nl ~ (Ω_m H²(z))^(1/3) / c
    H_z = H0_SI * np.sqrt(Omega_m * (1.0 + z)**3 + (1.0 - Omega_m))
    
    # Rough estimate: k_nl ~ 0.1-0.3 h/Mpc at z=0
    k_nl_h_Mpc = 0.2 * (Omega_m * (1.0 + z)**3)**(1.0/3.0)  # h/Mpc
    
    # Corresponding mass scale (M ~ 4π/3 * ρ_m * (2π/k)³)
    rho_m = Omega_m * 3.0 * H_z**2 / (8.0 * np.pi * G_SI)
    r_nl_Mpc = 2.0 * np.pi / (k_nl_h_Mpc * h * 1e6 / 3.086e22)  # Mpc
    r_nl_m = r_nl_Mpc * 3.086e22  # m
    M_nl_kg = (4.0 * np.pi / 3.0) * rho_m * r_nl_m**3
    M_nl_Msun = M_nl_kg / 1.989e30
    
    return {
        'k_nl_h_Mpc': float(k_nl_h_Mpc),
        'M_nl_Msun': float(M_nl_Msun),
        'r_nl_Mpc': float(r_nl_Mpc),
        'delta_c': 1.686,
        'z': float(z),
        'method': 'Linear-to-nonlinear transition scale'
    }


def compute_growth_rate(
    z: float,
    Omega_m: float = 0.315,
    w_de: float = -1.0
) -> float:
    """
    Compute linear growth rate f = d ln D / d ln a.
    
    In ΛCDM: f ≈ Ω_m(z)^(0.55)
    Modified for dark energy with w.
    
    Parameters:
    -----------
    z : float
        Redshift
    Omega_m : float
        Matter density at z=0
    w_de : float
        Dark energy equation of state
    
    Returns:
    --------
    f : float
        Growth rate
    """
    # Omega_m(z) = Omega_m * (1+z)^3 / E(z)^2
    # E(z) = sqrt(Omega_m*(1+z)^3 + Omega_DE*(1+z)^(3(1+w)))
    
    Omega_DE = 1.0 - Omega_m
    E_z_sq = Omega_m * (1.0 + z)**3 + Omega_DE * (1.0 + z)**(3.0 * (1.0 + w_de))
    Omega_m_z = Omega_m * (1.0 + z)**3 / E_z_sq
    
    # Growth rate: f ≈ Ω_m(z)^γ where γ ≈ 0.55 for ΛCDM
    gamma = 0.55
    f = Omega_m_z**gamma
    
    return float(f)


def compute_fsigma8(
    z: float,
    D_z: float,
    Omega_m: float = 0.315,
    sigma8_z0: float = 0.811,
    w_de: float = -1.0
) -> float:
    """
    Compute fσ₈(z) = f(z) × σ₈(z).
    
    This is a key observable for testing modified gravity.
    
    Parameters:
    -----------
    z : float
        Redshift
    D_z : float
        Growth factor at redshift z (normalized to D(0)=1)
    Omega_m : float
        Matter density
    sigma8_z0 : float
        σ₈ at z=0
    w_de : float
        Dark energy equation of state
    
    Returns:
    --------
    fsigma8 : float
        fσ₈(z)
    """
    f = compute_growth_rate(z, Omega_m, w_de)
    sigma8_z = sigma8_z0 * D_z  # σ₈(z) = σ₈(0) × D(z)
    fsigma8 = f * sigma8_z
    
    return float(fsigma8)


def compute_structure_transition(
    locks: Optional[Dict] = None,
    z: float = 0.0
) -> Dict[str, float]:
    """
    Compute structure transition properties.
    
    Parameters:
    -----------
    locks : dict, optional
        UDOF parameter locks
    z : float
        Redshift
    
    Returns:
    --------
    dict with transition info
    """
    if locks is None:
        Omega_m = 0.315
        h = 0.674
    else:
        cosmo = locks.get('cosmology', {})
        Omega_m = cosmo.get('Om', 0.315)
        h = cosmo.get('H0', 67.4) / 100.0
    
    transition = compute_transition_scale(Omega_m, h, z)
    
    # Compute growth rate at transition
    f_transition = compute_growth_rate(z, Omega_m)
    
    return {
        **transition,
        'f_growth_rate': float(f_transition),
        'method': 'UDOF structure transition computation'
    }

