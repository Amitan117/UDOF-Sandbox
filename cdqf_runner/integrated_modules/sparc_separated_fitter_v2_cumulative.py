"""
SPARC Separated Formula Per-Galaxy Fitter (Cumulative ESE Version)
====================================================================

Updated to use cumulative-based S_ESE approach and SPARC-derived parameters.

Uses:
- Cumulative-based X(r) = a₀ / g_bar(r) (acceleration-based)
- Optimized ESE parameters: k = 1.119, X0 = 10.0
- Universal law: v² = v_bar² × [1 + A × S_ESE] where A = 1.90
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

# Constants
KPC_TO_M = 3.0857e19  # kpc to meters
M_SUN = 1.98847e30  # Solar mass in kg
G = 6.67430e-11  # m³/(kg·s²)
C = 299792458  # m/s
A0_MOND = 1.2e-10  # m/s² (MOND acceleration scale)


def load_sparc_catalog(catalog_path: Optional[Path] = None) -> pd.DataFrame:
    """Load SPARC catalog."""
    if catalog_path is None:
        catalog_path = Path(__file__).parent.parent / "data" / "sparc" / "sparc_full_catalog.csv"
    
    if not catalog_path.exists():
        raise FileNotFoundError(f"SPARC catalog not found: {catalog_path}")
    
    df = pd.read_csv(catalog_path)
    return df


def load_sparc_rotation_curve(galaxy_name: str, rotation_curves_dir: Path) -> Optional[pd.DataFrame]:
    """Load rotation curve data for a galaxy."""
    rc_file = rotation_curves_dir / f"{galaxy_name}.dat"
    if not rc_file.exists():
        return None
    
    try:
        df = pd.read_csv(rc_file, comment='#', sep=r'\s+', header=None, 
                         names=['r_kpc', 'v_obs', 'v_err'], engine='python')
        return df
    except:
        return None


def compute_baryonic_rotation_curve(
    r_kpc: np.ndarray,
    M_star: float,  # M☉
    M_bulge: float,  # M☉
    M_gas: float,   # M☉
    R_d: float,     # kpc
    R_b: Optional[float] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute baryonic rotation curve.
    
    Returns:
    --------
    v_baryon : array
        Baryonic rotation velocity (km/s)
    M_enc : array
        Enclosed mass (M☉)
    g_bar : array
        Baryonic acceleration (m/s²)
    r_m : array
        Radius in meters
    """
    r_m = r_kpc * KPC_TO_M
    M_tot_kg = (M_star + M_bulge + M_gas) * M_SUN
    
    # Exponential disk approximation
    x = r_kpc / R_d
    M_enc_frac = 1.0 - (1.0 + x) * np.exp(-x)
    M_enc_kg = M_tot_kg * M_enc_frac
    M_enc = M_enc_kg / M_SUN  # M☉
    
    # Baryonic velocity
    v_baryon_mps = np.sqrt(G * M_enc_kg / r_m)
    v_baryon = v_baryon_mps / 1000.0  # km/s
    
    # Baryonic acceleration
    g_bar = np.zeros_like(r_m)
    valid = r_m > 0
    g_bar[valid] = v_baryon_mps[valid]**2 / r_m[valid]
    
    return v_baryon, M_enc, g_bar, r_m


def compute_X_from_acceleration(
    r_kpc: np.ndarray,
    g_bar: np.ndarray,  # m/s²
    a0: float = A0_MOND
) -> np.ndarray:
    """
    Compute control variable X from baryonic acceleration (RAR-like).
    
    X(r) = a₀ / g_bar(r)
    """
    X = np.zeros_like(g_bar)
    valid = g_bar > 1e-30
    X[valid] = a0 / g_bar[valid]
    
    # Clip to prevent extreme values
    X = np.clip(X, 1e-5, 1e5)
    
    return X


def compute_S_ESE_cumulative(
    X: np.ndarray,
    locks: Dict,
    method: str = "acceleration"
) -> np.ndarray:
    """
    Compute S_ESE from cumulative-based X.
    
    Uses ESE framework with optimized parameters.
    """
    # Get ESE parameters from locks
    ell_IR = locks.get('ell_IR', 4.7e-5)
    ell_star = locks.get('ell_star', 2e-15)
    
    # Use optimized parameters if available
    if 'dark_sector' in locks and 'ese' in locks['dark_sector']:
        k = locks['dark_sector']['ese'].get('k', 1.5)
        X0 = locks['dark_sector']['ese'].get('X0', 0.9166)
    elif 'ese_map' in locks:
        k = locks['ese_map'].get('k', 1.5)
        X0 = locks.get('calibrated_locks', {}).get('X0', 0.9166)
    else:
        k = locks.get('k', 1.5)
        X0 = locks.get('X0', 0.9166)
    
    # Compute s(X) using logistic
    X_safe = np.maximum(X, 1e-30)
    z = k * (np.log(X_safe) - np.log(X0))
    s = 1.0 / (1.0 + np.exp(-z))
    
    # For S_ESE, we use s directly (normalized if needed)
    # The enhancement comes from the gradient structure
    S_ESE = s
    
    # Normalize to reasonable range if needed
    if np.max(S_ESE) > 0:
        S_ESE = S_ESE / np.max(S_ESE)  # Normalize to [0, 1]
    
    return S_ESE


def compute_rotation_curve_cdqf(
    r_kpc: np.ndarray,
    v_baryon: np.ndarray,  # km/s
    g_bar: np.ndarray,     # m/s²
    locks: Dict,
    A: float = 1.90,  # Universal coupling constant
    B: float = 0.0,   # R_X coefficient (usually 0)
    X_method: str = "acceleration"
) -> Tuple[np.ndarray, Dict]:
    """
    Compute CDQF rotation curve using cumulative ESE approach.
    
    v²(r) = v_bar²(r) × [1 + A × S_ESE(r)] × [1 + B × R_X(k)]
    
    Parameters:
    -----------
    r_kpc : array
        Radii in kpc
    v_baryon : array
        Baryonic rotation velocity in km/s
    g_bar : array
        Baryonic acceleration in m/s²
    locks : dict
        CDQF parameter locks (with SPARC-derived parameters)
    A : float
        Universal coupling constant (default: 1.90)
    B : float
        R_X coefficient (default: 0.0, usually negligible)
    X_method : str
        Method for computing X(r) (default: "acceleration")
    
    Returns:
    --------
    v_model : array
        Model rotation velocity in km/s
    diagnostics : dict
        Diagnostic information
    """
    # Compute X(r) from acceleration
    if X_method == "acceleration":
        X = compute_X_from_acceleration(r_kpc, g_bar)
    else:
        raise ValueError(f"Unknown X_method: {X_method}")
    
    # Compute S_ESE
    S_ESE = compute_S_ESE_cumulative(X, locks, method=X_method)
    
    # R_X is approximately constant (≈ 0.989) for local galaxies
    # So [1 + B × R_X] ≈ [1 + B] ≈ 1 when B ≈ 0
    R_X = 0.989  # Approximate constant for local galaxies
    
    # Compute model velocity
    v_bar_sq = v_baryon**2
    v_model_sq = v_bar_sq * (1.0 + A * S_ESE) * (1.0 + B * R_X)
    v_model = np.sqrt(v_model_sq)
    
    diagnostics = {
        'X': X,
        'S_ESE': S_ESE,
        'A': A,
        'B': B,
        'R_X': R_X,
        'enhancement': 1.0 + A * S_ESE
    }
    
    return v_model, diagnostics


def fit_single_galaxy(
    galaxy_name: str,
    r_obs: np.ndarray,
    v_obs: np.ndarray,
    v_err: np.ndarray,
    M_star: float,  # M☉
    M_gas: float,   # M☉
    R_d: float,     # kpc
    locks: Dict,
    A_fixed: Optional[float] = None  # If None, fit A; otherwise use fixed value
) -> Dict:
    """
    Fit a single galaxy.
    
    Returns:
    --------
    fit_result : dict
        Fit results including A, B, chi2, etc.
    """
    # Compute baryonic rotation curve
    v_baryon, M_enc, g_bar, r_m = compute_baryonic_rotation_curve(
        r_obs, M_star, 0.0, M_gas, R_d
    )
    
    # Get A from locks if not provided
    if A_fixed is None:
        # Try to get A from locks
        if 'dark_sector' in locks and 'ese' in locks['dark_sector']:
            A_default = locks['dark_sector']['ese'].get('A_parameter', {}).get('value', 1.90)
        else:
            A_default = 1.90
        
        # Fit A and B
        def objective(params):
            A, B = params
            v_model, _ = compute_rotation_curve_cdqf(
                r_obs, v_baryon, g_bar, locks, A=A, B=B
            )
            valid = (v_err > 0) & np.isfinite(v_obs) & np.isfinite(v_model)
            chi2 = np.sum(((v_model[valid] - v_obs[valid]) / v_err[valid])**2)
            return chi2
        
        # Initial guess
        x0 = [A_default, 0.0]
        bounds = [(0.1, 10.0), (-1.0, 1.0)]
        
        try:
            result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
            A_opt = result.x[0]
            B_opt = result.x[1]
        except:
            A_opt = A_default
            B_opt = 0.0
    else:
        A_opt = A_fixed
        # Fit B only
        def objective_B(B):
            v_model, _ = compute_rotation_curve_cdqf(
                r_obs, v_baryon, g_bar, locks, A=A_opt, B=B
            )
            valid = (v_err > 0) & np.isfinite(v_obs) & np.isfinite(v_model)
            chi2 = np.sum(((v_model[valid] - v_obs[valid]) / v_err[valid])**2)
            return chi2
        
        try:
            result = minimize(objective_B, [0.0], bounds=[(-1.0, 1.0)], method='L-BFGS-B')
            B_opt = result.x[0]
        except:
            B_opt = 0.0
    
    # Compute final model
    v_model, diagnostics = compute_rotation_curve_cdqf(
        r_obs, v_baryon, g_bar, locks, A=A_opt, B=B_opt
    )
    
    # Compute chi2
    valid = (v_err > 0) & np.isfinite(v_obs) & np.isfinite(v_model)
    dof = valid.sum() - 2  # A and B are free
    chi2 = np.sum(((v_model[valid] - v_obs[valid]) / v_err[valid])**2)
    chi2_per_dof = chi2 / dof if dof > 0 else np.inf
    
    return {
        'galaxy_name': galaxy_name,
        'A_opt': float(A_opt),
        'B_opt': float(B_opt),
        'chi2': float(chi2),
        'chi2_per_dof': float(chi2_per_dof),
        'dof': int(dof),
        'v_model': v_model.tolist(),
        'S_ESE': diagnostics['S_ESE'].tolist(),
        'status': 'SUCCESS' if np.isfinite(chi2_per_dof) else 'FAIL'
    }


def fit_all_sparc_galaxies(
    catalog_path: Path,
    rotation_curves_dir: Path,
    locks: Dict,
    max_galaxies: Optional[int] = None,
    A_fixed: Optional[float] = None
) -> Dict:
    """
    Fit all SPARC galaxies.
    
    Parameters:
    -----------
    catalog_path : Path
        Path to SPARC catalog CSV
    rotation_curves_dir : Path
        Directory containing rotation curve .dat files
    locks : dict
        CDQF parameter locks
    max_galaxies : int, optional
        Maximum number of galaxies to fit (None = all)
    A_fixed : float, optional
        If provided, use fixed A value (default: 1.90 from locks)
    
    Returns:
    --------
    results : dict
        Summary of fits
    """
    # Load catalog
    df_catalog = load_sparc_catalog(catalog_path)
    
    # Get default A
    if A_fixed is None:
        if 'dark_sector' in locks and 'ese' in locks['dark_sector']:
            A_fixed = locks['dark_sector']['ese'].get('A_parameter', {}).get('value', 1.90)
        else:
            A_fixed = 1.90
    
    # Fit galaxies
    results = []
    n_galaxies = 0
    valid_fits = 0
    
    for idx, row in df_catalog.iterrows():
        if max_galaxies is not None and n_galaxies >= max_galaxies:
            break
        
        # Get galaxy name
        galaxy_name = row.get('Name', f'SPARC_{idx}')
        
        # Load rotation curve
        df_rc = load_sparc_rotation_curve(galaxy_name, rotation_curves_dir)
        if df_rc is None:
            continue
        
        r_obs = df_rc['r_kpc'].values
        v_obs = df_rc['v_obs'].values
        v_err = df_rc['v_err'].values if 'v_err' in df_rc.columns else v_obs * 0.05
        
        # Get galaxy parameters
        L_3_6 = row.get('L3_6', np.nan)
        if pd.isna(L_3_6):
            M_star = 1.0e9
        else:
            M_star = L_3_6 * 1e9 * 0.6  # M☉
        
        MHI = row.get('MHI', np.nan)
        if pd.isna(MHI) or MHI <= 0:
            M_gas = 0.1 * M_star
        else:
            M_gas = MHI * 1e9  # M☉
        
        R_d = row.get('Rdisk', 2.0)
        if pd.isna(R_d) or R_d <= 0:
            R_d = 2.0
        
        # Fit galaxy
        try:
            result = fit_single_galaxy(
                galaxy_name, r_obs, v_obs, v_err,
                M_star, M_gas, R_d, locks, A_fixed=A_fixed
            )
            
            if result['status'] == 'SUCCESS':
                valid_fits += 1
            
            results.append(result)
            n_galaxies += 1
        except Exception as e:
            results.append({
                'galaxy_name': galaxy_name,
                'status': 'ERROR',
                'error': str(e)
            })
            n_galaxies += 1
    
    # Summary statistics
    if valid_fits > 0:
        A_values = [r['A_opt'] for r in results if r.get('status') == 'SUCCESS']
        chi2_values = [r['chi2_per_dof'] for r in results if r.get('status') == 'SUCCESS']
        
        global_chi2 = np.sum([r['chi2'] for r in results if r.get('status') == 'SUCCESS'])
        global_dof = np.sum([r['dof'] for r in results if r.get('status') == 'SUCCESS'])
        global_chi2_per_dof = global_chi2 / global_dof if global_dof > 0 else np.inf
    else:
        A_values = []
        chi2_values = []
        global_chi2_per_dof = np.inf
    
    return {
        'status': 'COMPLETE',
        'n_galaxies': n_galaxies,
        'valid_fits': valid_fits,
        'global_chi2_per_dof': float(global_chi2_per_dof),
        'A_fixed': A_fixed,
        'A_median': float(np.median(A_values)) if len(A_values) > 0 else None,
        'A_mean': float(np.mean(A_values)) if len(A_values) > 0 else None,
        'chi2_median': float(np.median(chi2_values)) if len(chi2_values) > 0 else None,
        'results': results
    }

