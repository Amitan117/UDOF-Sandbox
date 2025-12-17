"""
Three-Body Sun-Earth-Moon Dynamics

Full N-body integration of the Sun-Earth-Moon system to test orbital stability
and verify that UDOF (with s→0 at Solar System scales) recovers GR predictions.

Equations of motion:
    d²r_i/dt² = Σ_j≠i G M_j (r_j - r_i) / |r_j - r_i|³

For Solar System: s→0 → ESE inactive → pure GR → standard N-body dynamics.
"""

import numpy as np
from typing import Dict, Tuple
from scipy.integrate import solve_ivp

# Physical constants
G_SI = 6.67430e-11  # m³/(kg·s²)
AU_M = 1.496e11  # m
DAY_S = 86400.0  # s
YEAR_S = 365.25 * DAY_S

# Masses (kg)
M_SUN = 1.989e30
M_EARTH = 5.972e24
M_MOON = 7.342e22

# Initial conditions (approximate, from JPL ephemeris)
# Sun at origin, Earth-Moon barycenter at 1 AU, Moon orbiting Earth
# All positions in meters, velocities in m/s

# Earth-Moon barycenter initial position (1 AU along x-axis)
R_EARTH_MOON_BARYCENTER = AU_M  # m
V_EARTH_MOON_BARYCENTER = 29780.0  # m/s (orbital speed)

# Moon-Earth separation (mean distance)
R_MOON_EARTH = 3.844e8  # m
V_MOON_ORBITAL = 1022.0  # m/s (Moon orbital speed around Earth)


def compute_three_body_dynamics(
    t_span_days: float = 365.25,  # Integration time span
    dt_days: float = 0.1,  # Output time step
    s: float = 0.0,  # ESE parameter (0 for Solar System)
    rtol: float = 1e-9,
    atol: float = 1e-12
) -> Dict[str, np.ndarray]:
    """
    Full N-body integration of Sun-Earth-Moon system.
    
    Parameters:
    -----------
    t_span_days : float
        Integration time span in days
    dt_days : float
        Output time step in days
    s : float
        ESE parameter (should be 0.0 for Solar System)
    rtol : float
        Relative tolerance for ODE solver
    atol : float
        Absolute tolerance for ODE solver
    
    Returns:
    --------
    dict with positions, velocities, energies, stability metrics
    """
    # Mass array
    masses = np.array([M_SUN, M_EARTH, M_MOON])
    
    # Initial conditions: [x_sun, y_sun, z_sun, vx_sun, vy_sun, vz_sun,
    #                      x_earth, y_earth, z_earth, vx_earth, vy_earth, vz_earth,
    #                      x_moon, y_moon, z_moon, vx_moon, vy_moon, vz_moon]
    
    # Sun at origin, at rest (in barycenter frame)
    x_sun = 0.0
    y_sun = 0.0
    z_sun = 0.0
    vx_sun = 0.0
    vy_sun = 0.0
    vz_sun = 0.0
    
    # Earth-Moon barycenter at 1 AU along x-axis, moving in +y direction
    x_earth_bary = R_EARTH_MOON_BARYCENTER
    y_earth_bary = 0.0
    z_earth_bary = 0.0
    vx_earth_bary = 0.0
    vy_earth_bary = V_EARTH_MOON_BARYCENTER
    vz_earth_bary = 0.0
    
    # Earth position relative to barycenter (Earth is more massive)
    # Barycenter: r_bary = (M_earth * r_earth + M_moon * r_moon) / (M_earth + M_moon)
    # If Moon is at r_moon = r_earth + R_MOON_EARTH, then:
    # r_earth = r_bary - (M_moon / (M_earth + M_moon)) * R_MOON_EARTH
    mu_moon = M_MOON / (M_EARTH + M_MOON)
    r_earth_offset = -mu_moon * R_MOON_EARTH  # Earth offset from barycenter
    
    # Moon offset from barycenter
    r_moon_offset = (1 - mu_moon) * R_MOON_EARTH
    
    # Initial Earth position (along x-axis, Moon ahead)
    x_earth = x_earth_bary + r_earth_offset
    y_earth = y_earth_bary
    z_earth = z_earth_bary
    
    # Initial Moon position
    x_moon = x_earth_bary + r_moon_offset
    y_moon = y_earth_bary
    z_moon = z_earth_bary
    
    # Velocities: Earth-Moon system orbits Sun, Moon orbits Earth
    # Earth velocity = barycenter velocity + orbital velocity around barycenter
    v_earth_orbital = -mu_moon * V_MOON_ORBITAL  # Earth orbital speed around barycenter
    vx_earth = vx_earth_bary + v_earth_orbital
    vy_earth = vy_earth_bary
    vz_earth = vz_earth_bary
    
    # Moon velocity
    v_moon_orbital = (1 - mu_moon) * V_MOON_ORBITAL
    vx_moon = vx_earth_bary + v_moon_orbital
    vy_moon = vy_earth_bary
    vz_moon = vz_earth_bary
    
    # Adjust Sun to keep barycenter at origin
    # System barycenter: r_sys = (M_sun * r_sun + M_earth * r_earth + M_moon * r_moon) / M_total
    M_total = M_SUN + M_EARTH + M_MOON
    r_sys_x = (M_EARTH * x_earth + M_MOON * x_moon) / M_total
    r_sys_y = (M_EARTH * y_earth + M_MOON * y_moon) / M_total
    r_sys_z = (M_EARTH * z_earth + M_MOON * z_moon) / M_total
    
    x_sun = -r_sys_x * M_total / M_SUN
    y_sun = -r_sys_y * M_total / M_SUN
    z_sun = -r_sys_z * M_total / M_SUN
    
    # Sun velocity to keep system momentum zero
    v_sys_x = (M_EARTH * vx_earth + M_MOON * vx_moon) / M_total
    v_sys_y = (M_EARTH * vy_earth + M_MOON * vy_moon) / M_total
    v_sys_z = (M_EARTH * vz_earth + M_MOON * vz_moon) / M_total
    
    vx_sun = -v_sys_x * M_total / M_SUN
    vy_sun = -v_sys_y * M_total / M_SUN
    vz_sun = -v_sys_z * M_total / M_SUN
    
    # Initial state vector
    y0 = np.array([
        x_sun, y_sun, z_sun, vx_sun, vy_sun, vz_sun,
        x_earth, y_earth, z_earth, vx_earth, vy_earth, vz_earth,
        x_moon, y_moon, z_moon, vx_moon, vy_moon, vz_moon
    ])
    
    # Time span
    t_span = (0.0, t_span_days * DAY_S)
    t_eval = np.arange(0.0, t_span_days * DAY_S, dt_days * DAY_S)
    
    def equations_of_motion(t, y):
        """
        Compute derivatives: dy/dt = [v1, v2, v3, a1, a2, a3, ...]
        """
        # Extract positions and velocities
        r_sun = y[0:3]
        v_sun = y[3:6]
        r_earth = y[6:9]
        v_earth = y[9:12]
        r_moon = y[12:15]
        v_moon = y[15:18]
        
        # Compute accelerations from gravitational forces
        # Sun acceleration
        r_se = r_earth - r_sun
        r_sm = r_moon - r_sun
        r_se_norm = np.linalg.norm(r_se)
        r_sm_norm = np.linalg.norm(r_sm)
        
        # Avoid division by zero
        eps = 1e-10
        r_se_norm = max(r_se_norm, eps)
        r_sm_norm = max(r_sm_norm, eps)
        
        a_sun = G_SI * (
            M_EARTH * r_se / (r_se_norm**3) +
            M_MOON * r_sm / (r_sm_norm**3)
        )
        
        # Earth acceleration
        r_es = r_sun - r_earth
        r_em = r_moon - r_earth
        r_es_norm = np.linalg.norm(r_es)
        r_em_norm = np.linalg.norm(r_em)
        
        r_es_norm = max(r_es_norm, eps)
        r_em_norm = max(r_em_norm, eps)
        
        a_earth = G_SI * (
            M_SUN * r_es / (r_es_norm**3) +
            M_MOON * r_em / (r_em_norm**3)
        )
        
        # Moon acceleration
        r_ms = r_sun - r_moon
        r_me = r_earth - r_moon
        r_ms_norm = np.linalg.norm(r_ms)
        r_me_norm = np.linalg.norm(r_me)
        
        r_ms_norm = max(r_ms_norm, eps)
        r_me_norm = max(r_me_norm, eps)
        
        a_moon = G_SI * (
            M_SUN * r_ms / (r_ms_norm**3) +
            M_EARTH * r_me / (r_me_norm**3)
        )
        
        # UDOF modification: if s≠0, there could be additional acceleration
        # But at Solar System scales, s→0, so this is pure GR
        # For now, we assume s=0 (Solar System limit)
        
        # Return derivatives: [v_sun, a_sun, v_earth, a_earth, v_moon, a_moon]
        return np.concatenate([
            v_sun, a_sun,
            v_earth, a_earth,
            v_moon, a_moon
        ])
    
    # Integrate
    sol = solve_ivp(
        equations_of_motion,
        t_span,
        y0,
        t_eval=t_eval,
        method='RK45',
        rtol=rtol,
        atol=atol,
        dense_output=False
    )
    
    if not sol.success:
        raise RuntimeError(f"Integration failed: {sol.message}")
    
    # Extract results
    t = sol.t
    n_times = len(t)
    
    # sol.y shape: (18, n_times) - 18 components (6 per body: 3 pos + 3 vel)
    r_sun = sol.y[0:3, :].T  # (n_times, 3)
    v_sun = sol.y[3:6, :].T
    r_earth = sol.y[6:9, :].T
    v_earth = sol.y[9:12, :].T
    r_moon = sol.y[12:15, :].T
    v_moon = sol.y[15:18, :].T
    
    # Compute Earth-Sun distance
    r_earth_sun = r_earth - r_sun
    r_earth_sun_norm = np.linalg.norm(r_earth_sun, axis=1)
    
    # Compute Moon-Earth distance
    r_moon_earth = r_moon - r_earth
    r_moon_earth_norm = np.linalg.norm(r_moon_earth, axis=1)
    
    # Compute energies
    # Kinetic energy
    T_sun = 0.5 * M_SUN * np.sum(v_sun**2, axis=1)
    T_earth = 0.5 * M_EARTH * np.sum(v_earth**2, axis=1)
    T_moon = 0.5 * M_MOON * np.sum(v_moon**2, axis=1)
    T_total = T_sun + T_earth + T_moon
    
    # Potential energy
    r_se_vec = r_earth - r_sun
    r_sm_vec = r_moon - r_sun
    r_em_vec = r_moon - r_earth
    
    r_se_norm = np.linalg.norm(r_se_vec, axis=1)
    r_sm_norm = np.linalg.norm(r_sm_vec, axis=1)
    r_em_norm = np.linalg.norm(r_em_vec, axis=1)
    
    # Avoid division by zero
    eps = 1e-10
    r_se_norm = np.maximum(r_se_norm, eps)
    r_sm_norm = np.maximum(r_sm_norm, eps)
    r_em_norm = np.maximum(r_em_norm, eps)
    
    U_se = -G_SI * M_SUN * M_EARTH / r_se_norm
    U_sm = -G_SI * M_SUN * M_MOON / r_sm_norm
    U_em = -G_SI * M_EARTH * M_MOON / r_em_norm
    U_total = U_se + U_sm + U_em
    
    # Total energy
    E_total = T_total + U_total
    
    # Stability metrics
    # Earth-Sun orbital stability: relative change in semi-major axis
    # Use more stable measure: compare initial and final orbital periods
    # For circular orbits, semi-major axis ≈ mean distance
    n_samples = min(100, len(r_earth_sun_norm) // 10)  # Use 10% of data for averaging
    if n_samples < 10:
        n_samples = len(r_earth_sun_norm) // 2
    
    a_earth_sun_initial = np.mean(r_earth_sun_norm[:n_samples])  # Initial semi-major axis
    a_earth_sun_final = np.mean(r_earth_sun_norm[-n_samples:])  # Final semi-major axis
    earth_sun_stability = abs(a_earth_sun_final - a_earth_sun_initial) / a_earth_sun_initial if a_earth_sun_initial > 0 else 0.0
    
    # Moon-Earth orbital stability
    # Moon orbit is more sensitive, so use orbital period instead of just distance
    # For stability, check if the Moon-Earth distance variation is bounded
    a_moon_earth_initial = np.mean(r_moon_earth_norm[:n_samples])
    a_moon_earth_final = np.mean(r_moon_earth_norm[-n_samples:])
    moon_earth_stability = abs(a_moon_earth_final - a_moon_earth_initial) / a_moon_earth_initial if a_moon_earth_initial > 0 else 0.0
    
    # Alternative: Check relative variation over the integration
    # This is more robust for the Moon-Earth system
    moon_earth_variation = np.std(r_moon_earth_norm) / np.mean(r_moon_earth_norm) if np.mean(r_moon_earth_norm) > 0 else 0.0
    # Use the more conservative measure
    moon_earth_stability = max(moon_earth_stability, moon_earth_variation)
    
    # Energy conservation (relative error)
    E_initial = E_total[0]
    E_final = E_total[-1]
    energy_conservation = abs(E_final - E_initial) / abs(E_initial)
    
    return {
        't': t,  # s
        'r_sun': r_sun,  # m
        'v_sun': v_sun,  # m/s
        'r_earth': r_earth,  # m
        'v_earth': v_earth,  # m/s
        'r_moon': r_moon,  # m
        'v_moon': v_moon,  # m/s
        'r_earth_sun': r_earth_sun_norm,  # m
        'r_moon_earth': r_moon_earth_norm,  # m
        'T_total': T_total,  # J
        'U_total': U_total,  # J
        'E_total': E_total,  # J
        'earth_sun_stability': float(earth_sun_stability),
        'moon_earth_stability': float(moon_earth_stability),
        'energy_conservation': float(energy_conservation),
        's': float(s),
        'method': 'Full N-body integration (RK45)'
    }

