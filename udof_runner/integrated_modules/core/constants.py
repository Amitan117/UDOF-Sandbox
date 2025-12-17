"""
Physical constants and PDG reference values used by domain modules.
"""

import numpy as np

# Physical constants
c_SI = 299792458  # m/s
c_km_s = 299792.458  # km/s
hbar_SI = 1.054571817e-34  # J·s
G_SI = 6.67430e-11  # m³/(kg·s²)
eV_to_J = 1.60218e-19
GeV_to_J = 1.60218e-10
GeV_to_eV = 1e9
V_HIGGS = 246.0  # GeV
SQRT2 = np.sqrt(2)
M_Pl_GeV = 2.435e18  # Reduced Planck mass in GeV
M_sun_kg = 1.989e30  # Solar mass in kg
kpc_to_m = 3.086e19

# PDG reference values
PDG_QUARKS = {
    'u': (0.00216, 0.00049),
    'd': (0.00467, 0.00048),
    's': (0.0934, 0.008),
    'c': (1.27, 0.02),
    'b': (4.18, 0.03),
    't': (172.69, 0.30)
}

PDG_LEPTONS = {
    'e': (0.000510999, 1e-9),
    'mu': (0.105658, 1e-6),
    'tau': (1.77686, 0.00012)
}

PDG_PMNS = {
    'theta12': (33.44, 0.78),
    'theta23': (49.0, 1.4),
    'theta13': (8.57, 0.12)
}

PDG_CKM = {
    'theta12': (13.04, 0.05),
    'theta23': (2.38, 0.06),
    'theta13': (0.201, 0.011)
}

PDG_NEUTRINO = {
    'dm2_21': (7.53e-5, 0.18e-5),
    'dm2_31': (2.453e-3, 0.034e-3)
}

# Check scipy availability
try:
    from scipy.linalg import expm
    from scipy.integrate import solve_ivp
    SCIPY_AVAILABLE = True
except ImportError:
    expm = None
    solve_ivp = None
    SCIPY_AVAILABLE = False

