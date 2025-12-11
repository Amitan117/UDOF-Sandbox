"""
SPARC Separated Formula Per-Galaxy Fitter

Fits CDQF rotation curves to all SPARC galaxies individually.
Computes per-galaxy χ² and rotation curve profiles.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Import SPARC computation
try:
    from integrated_modules.sparc_ese_computation import compute_S_ESE_proper
except ImportError:
    compute_S_ESE_proper = None


def load_sparc_catalog(catalog_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load SPARC catalog.
    
    Parameters:
    -----------
    catalog_path : Path, optional
        Path to SPARC catalog CSV. If None, uses default.
    
    Returns:
    --------
    df : DataFrame
        SPARC catalog
    """
    if catalog_path is None:
        catalog_path = Path(__file__).parent.parent / "data" / "sparc" / "sparc_full_catalog.csv"
    
    if not catalog_path.exists():
        raise FileNotFoundError(f"SPARC catalog not found: {catalog_path}")
    
    df = pd.read_csv(catalog_path)
    return df


def compute_rotation_curve_cdqf(
    r_kpc: np.ndarray,
    M_star: float,  # M☉
    M_gas: float,   # M☉
    R_d: float,     # kpc
    R_b: Optional[float] = None,
    locks: Optional[Dict] = None,
    method: str = 'gradient'
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute CDQF rotation curve.
    
    v²(r) = v_baryon²(r) * (1 + S_ESE(r))
    
    Parameters:
    -----------
    r_kpc : array
        Radii in kpc
    M_star, M_gas : float
        Stellar and gas masses in M☉
    R_d : float
        Disk scale length in kpc
    R_b : float, optional
        Bulge scale length
    locks : dict, optional
        CDQF parameter locks
    method : str
        S_ESE computation method
    
    Returns:
    --------
    v_cdqf : array
        CDQF rotation velocities in km/s
    S_ESE : array
        ESE enhancement factor
    """
    if compute_S_ESE_proper is None:
        raise ImportError("SPARC ESE computation module not available")
    
    # Compute S_ESE
    S_ESE = compute_S_ESE_proper(
        r_kpc, M_star, M_gas, R_d,
        locks=locks, method=method
    )
    
    # Baryonic rotation curve (simplified - exponential disk)
    # v_baryon² = G * M_enc(r) / r
    # For exponential disk: M_enc(r) = M * (1 - (1 + r/R_d)*exp(-r/R_d))
    from scipy.special import gammainc
    
    # Input masses are in M☉
    M_tot = M_star + M_gas  # M☉
    M_tot_kg = M_tot * 1.989e30  # kg
    
    G_SI = 6.67430e-11  # m³/(kg·s²)
    kpc_to_m = 3.086e19  # meters per kpc
    
    r_m = r_kpc * kpc_to_m  # meters
    
    # Enclosed mass (exponential disk approximation)
    # M_enc(r) = M_tot * (1 - (1 + r/R_d)*exp(-r/R_d))
    x = r_kpc / R_d
    # Avoid division by zero for R_d = 0
    x = np.where(R_d > 0, x, r_kpc)
    M_enc_frac = 1.0 - (1.0 + x) * np.exp(-x)
    M_enc_frac = np.maximum(M_enc_frac, 0.0)  # Ensure non-negative
    M_enc_kg = M_tot_kg * M_enc_frac
    
    # Baryonic velocity: v² = G * M_enc / r
    # Avoid division by zero for r = 0
    r_m_safe = np.maximum(r_m, 1.0)  # Minimum 1 meter to avoid division by zero
    v_baryon_mps = np.sqrt(G_SI * M_enc_kg / r_m_safe)
    v_baryon_kms = v_baryon_mps / 1000.0  # Convert to km/s
    
    # CDQF velocity: v² = v_baryon² * (1 + S_ESE)
    v_sq_cdqf = v_baryon_kms**2 * (1.0 + S_ESE)
    v_cdqf = np.sqrt(np.maximum(v_sq_cdqf, 0.0))
    
    return v_cdqf, S_ESE


def fit_single_galaxy(
    galaxy_name: str,
    r_obs: np.ndarray,
    v_obs: np.ndarray,
    v_err: np.ndarray,
    M_star: float,
    M_gas: float,
    R_d: float,
    R_b: Optional[float] = None,
    locks: Optional[Dict] = None
) -> Dict[str, float]:
    """
    Fit CDQF model to a single galaxy.
    
    Parameters:
    -----------
    galaxy_name : str
        Galaxy identifier
    r_obs : array
        Observed radii in kpc
    v_obs : array
        Observed velocities in km/s
    v_err : array
        Velocity errors in km/s
    M_star, M_gas : float
        Stellar and gas masses in M☉
    R_d : float
        Disk scale length in kpc
    R_b : float, optional
        Bulge scale length
    locks : dict, optional
        CDQF parameter locks
    
    Returns:
    --------
    dict with fit results (chi2, dof, v_model, etc.)
    """
    try:
        # Compute model velocities
        v_model, S_ESE = compute_rotation_curve_cdqf(
            r_obs, M_star, M_gas, R_d, R_b, locks=locks
        )
        
        # Chi-squared
        valid = (v_err > 0) & np.isfinite(v_obs) & np.isfinite(v_model)
        if valid.sum() == 0:
            return {'chi2': np.inf, 'dof': 0, 'valid': False}
        
        chi2 = np.sum(((v_model[valid] - v_obs[valid]) / v_err[valid])**2)
        dof = valid.sum()
        chi2_per_dof = chi2 / dof if dof > 0 else np.inf
        
        return {
            'galaxy_name': galaxy_name,
            'chi2': float(chi2),
            'dof': int(dof),
            'chi2_per_dof': float(chi2_per_dof),
            'n_points': int(dof),
            'valid': True,
            'v_model': v_model.tolist(),
            'S_ESE_mean': float(np.mean(S_ESE))
        }
    except Exception as e:
        return {
            'galaxy_name': galaxy_name,
            'chi2': np.inf,
            'dof': 0,
            'valid': False,
            'error': str(e)
        }


def load_sparc_rotation_curve(
    galaxy_name: str,
    rotation_curves_dir: Path
) -> Optional[pd.DataFrame]:
    """
    Load rotation curve data for a single galaxy.
    
    SPARC files are named like: {galaxy_name}_rotmod.dat
    Format: radius [kpc], v_obs [km/s], v_err, v_gas, v_disk, v_bulge, ...
    """
    patterns = [
        f"{galaxy_name}_rotmod.dat",
        f"{galaxy_name.upper()}_rotmod.dat",
        f"{galaxy_name.lower()}_rotmod.dat",
        f"{galaxy_name}.dat",
    ]
    
    for pattern in patterns:
        rc_file = rotation_curves_dir / pattern
        if rc_file.exists():
            try:
                # SPARC format: space-separated, may have header
                df = pd.read_csv(rc_file, sep=r'\s+', comment='#', skipinitialspace=True)
                
                # Map columns - SPARC format: Rad Vobs errV Vgas Vdisk Vbul SBdisk SBbul
                # Standardize column names
                if len(df.columns) >= 6:
                    col_names = ['r_kpc', 'v_obs', 'v_err', 'v_gas', 'v_disk', 'v_bulge']
                    df.columns = col_names[:len(df.columns)] + [f'col_{i}' for i in range(len(col_names), len(df.columns))]
                elif len(df.columns) >= 3:
                    df.columns = ['r_kpc', 'v_obs', 'v_err'] + [f'col_{i}' for i in range(3, len(df.columns))]
                else:
                    df.columns = ['r_kpc', 'v_obs'] + [f'col_{i}' for i in range(2, len(df.columns))]
                
                # Convert to numeric
                for col in ['r_kpc', 'v_obs', 'v_err', 'v_gas', 'v_disk', 'v_bulge']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                
                # Clean data
                df = df.dropna(subset=['r_kpc', 'v_obs'])
                df = df[df['r_kpc'] > 0]
                df = df[df['v_obs'] > 0]
                
                # Default v_err if missing
                if 'v_err' not in df.columns or df['v_err'].isna().all():
                    df['v_err'] = df['v_obs'] * 0.05  # 5% default error
                
                return df
            except Exception as e:
                continue
    
    return None


def fit_all_sparc_galaxies(
    catalog_path: Optional[Path] = None,
    rotation_curves_dir: Optional[Path] = None,
    locks: Optional[Dict] = None,
    max_galaxies: Optional[int] = None
) -> Dict[str, any]:
    """
    Fit CDQF model to all SPARC galaxies.
    
    Parameters:
    -----------
    catalog_path : Path, optional
        Path to SPARC catalog
    rotation_curves_dir : Path, optional
        Directory containing rotation curve .dat files
    locks : dict, optional
        CDQF parameter locks
    max_galaxies : int, optional
        Maximum number of galaxies to fit (for testing)
    
    Returns:
    --------
    dict with per-galaxy results and summary statistics
    """
    if compute_S_ESE_proper is None:
        return {
            'status': 'SKIP',
            'note': 'SPARC ESE computation module not available'
        }
    
    # Set up paths
    if catalog_path is None:
        catalog_path = Path(__file__).parent.parent / "data" / "sparc" / "sparc_full_catalog.csv"
    
    if rotation_curves_dir is None:
        rotation_curves_dir = Path(__file__).parent.parent / "data" / "sparc" / "rotation_curves"
    
    # Load catalog
    df = load_sparc_catalog(catalog_path)
    
    if max_galaxies is not None:
        df = df.head(max_galaxies)
    
    results = []
    valid_fits = 0
    
    for idx, row in df.iterrows():
        # SPARC catalog uses 'Name' column
        galaxy_name = row.get('Name', row.get('Galaxy', row.get('galaxy', f'SPARC_{idx}')))
        
        # Load rotation curve data
        rc_data = load_sparc_rotation_curve(galaxy_name, rotation_curves_dir)
        
        if rc_data is None or len(rc_data) == 0:
            # Skip if no rotation curve data
            result = {
                'galaxy_name': galaxy_name,
                'chi2': np.nan,
                'dof': 0,
                'valid': False,
                'note': 'Rotation curve data file not found'
            }
            results.append(result)
            continue
        
        # Extract galaxy parameters from catalog
        # SPARC catalog has L3_6 (3.6μm luminosity in 10^9 L☉) and MHI (HI mass in 10^9 M☉)
        # Convert luminosity to stellar mass: M/L at 3.6μm ≈ 0.6 M☉/L☉ (Meidt+ 2014)
        L3_6 = row.get('L3_6', np.nan)
        if not pd.isna(L3_6):
            # L3_6 is in 10^9 L☉, convert to stellar mass in M☉
            M_L_ratio_3_6 = 0.6  # M☉/L☉ at 3.6μm
            M_star = L3_6 * 1e9 * M_L_ratio_3_6  # M☉
        else:
            # Fallback: try Mstar column (if exists)
            M_star_raw = row.get('Mstar', row.get('logMstar', np.nan))
            if not pd.isna(M_star_raw):
                # If log mass, convert to linear
                if M_star_raw < 20:
                    M_star = 10.0**M_star_raw  # log10(M/M☉) to M☉
                else:
                    M_star = M_star_raw  # Already linear
            else:
                # Default: assume ~10^8 M☉ (small galaxy)
                M_star = 1e8
        
        # Gas mass: SPARC catalog has MHI in 10^9 M☉
        MHI = row.get('MHI', np.nan)
        if not pd.isna(MHI) and MHI > 0:
            # MHI is in 10^9 M☉
            M_gas = MHI * 1e9  # Convert to M☉
        else:
            # Fallback: try Mgas column
            M_gas_raw = row.get('Mgas', row.get('logMgas', np.nan))
            if not pd.isna(M_gas_raw):
                if M_gas_raw < 20:
                    M_gas = 10.0**M_gas_raw
                else:
                    M_gas = M_gas_raw
            else:
                # Default: 10% of stellar mass
                M_gas = 0.1 * M_star
        
        # Disk scale length
        R_d = row.get('Rdisk', row.get('Rd', np.nan))  # kpc
        if pd.isna(R_d) or R_d <= 0:
            # Fallback: use effective radius
            R_d = row.get('Reff', 2.0)  # kpc
            if pd.isna(R_d) or R_d <= 0:
                R_d = 2.0  # Default
        
        # Get rotation curve data
        r_obs = rc_data['r_kpc'].values
        v_obs = rc_data['v_obs'].values
        v_err = rc_data['v_err'].values if 'v_err' in rc_data.columns else v_obs * 0.05
        
        # Fit single galaxy
        # Note: compute_rotation_curve_cdqf expects masses in M☉
        result = fit_single_galaxy(
            galaxy_name, r_obs, v_obs, v_err,
            M_star,   # Already in M☉
            M_gas,    # Already in M☉
            R_d,
            locks=locks
        )
        
        results.append(result)
        if result.get('valid', False):
            valid_fits += 1
    
    total_chi2 = sum(r.get('chi2', 0) for r in results if r.get('valid', False))
    total_dof = sum(r.get('dof', 0) for r in results if r.get('valid', False))
    
    return {
        'status': 'COMPLETE' if valid_fits > 0 else 'NO_DATA',
        'n_galaxies': len(results),
        'valid_fits': valid_fits,
        'total_chi2': float(total_chi2),
        'total_dof': int(total_dof),
        'global_chi2_per_dof': float(total_chi2 / total_dof) if total_dof > 0 else np.nan,
        'per_galaxy_results': results
    }

