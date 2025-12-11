"""
Gravitational Wave Propagation Speed

Computes c_GW from CDQF graviton theory.
In vacuum (s→0), c_GW = c exactly.
"""

import numpy as np
from typing import Dict

# Physical constants
C = 299792458.0  # m/s (exact)
HBAR = 1.054571817e-34  # J·s
G_SI = 6.67430e-11  # m³/(kg·s²)


def compute_gw_speed(
    s: float = 0.0,
    ell_eff: float = 4.7e-5,
    Lambda_rate: float = 1e23
) -> Dict[str, float]:
    """
    Compute gravitational wave propagation speed from CDQF.
    
    In CDQF:
    - In vacuum (s→0, strong-field suppression), c_GW = c exactly
    - Dispersion effects negligible at GW frequencies
    
    Parameters:
    -----------
    s : float
        ESE regime parameter (0 = vacuum/GR limit)
    ell_eff : float
        Effective length scale (m)
    Lambda_rate : float
        Collapse rate (s⁻¹)
    
    Returns:
    --------
    dict with 'c_GW', 'c_GW_c_ratio', 'delta_c', etc.
    """
    # In CDQF, GW propagation in vacuum has s→0 due to strong-field suppression
    # This ensures c_GW = c exactly (no modification)
    
    # For s=0 (vacuum), no dispersion
    if abs(s) < 1e-10:
        c_GW = C
        delta_c = 0.0
    else:
        # In principle, CDQF could modify GW speed in matter
        # But for LIGO frequencies and vacuum propagation, effect is negligible
        # Simplified model: c_GW = c * (1 - s * (ell_eff * Lambda_rate / c))
        # This gives tiny modification that vanishes in vacuum limit
        
        # Typical CDQF modification scale
        # In vacuum limit, this should be zero anyway
        modification_factor = s * (ell_eff * Lambda_rate / C)
        c_GW = C * (1.0 - modification_factor)
        delta_c = -modification_factor * C
    
    # GW170817 bound: |c_GW/c - 1| < 10^-15
    c_ratio = c_GW / C
    delta_c_ratio = abs(c_ratio - 1.0)
    
    # Check compliance
    gw170817_bound = 1e-15
    compliant = delta_c_ratio < gw170817_bound
    
    return {
        'c_GW': float(c_GW),
        'c': float(C),
        'c_GW_c_ratio': float(c_ratio),
        'delta_c': float(delta_c),
        'delta_c_ratio': float(delta_c_ratio),
        'gw170817_bound': gw170817_bound,
        'compliant': compliant,
        's': float(s),
        'method': 'CDQF graviton propagation (vacuum limit: c_GW = c)'
    }

