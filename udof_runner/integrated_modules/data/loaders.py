"""
Data Loaders Module

Contains data loading utilities for observational datasets.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import numpy as np


class DataLoader:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def load_bao_desi(self) -> Dict:
        bao_dir = self.data_root / "bao" / "desi_dr1_all"
        measurements = []
        with open(bao_dir / "mean.txt", 'r') as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                parts = line.split()
                measurements.append({
                    'z': float(parts[0]),
                    'value': float(parts[1]),
                    'quantity': parts[2]
                })
        cov = np.loadtxt(bao_dir / "cov.txt")
        return {'measurements': measurements, 'covariance': cov}

    def load_sne_pantheon(self) -> Dict:
        """Load real Pantheon+SH0ES data."""
        sne_file = self.data_root / "sne" / "pantheon_plus" / "Pantheon+SH0ES.dat"
        data = {'z': [], 'mu': [], 'sigma': []}

        with open(sne_file, 'r') as f:
            header = f.readline().strip().split()
            # Find column indices
            z_idx = header.index(
                'zCMB') if 'zCMB' in header else header.index('zHD')
            mu_idx = header.index(
                'MU_SH0ES') if 'MU_SH0ES' in header else header.index('m_b_corr')
            err_idx = header.index(
                'MU_SH0ES_ERR_DIAG') if 'MU_SH0ES_ERR_DIAG' in header else header.index('m_b_corr_err_DIAG')

            for line in f:
                parts = line.strip().split()
                if len(parts) > max(z_idx, mu_idx, err_idx):
                    try:
                        z = float(parts[z_idx])
                        mu = float(parts[mu_idx])
                        sigma = float(parts[err_idx])
                        # Filter: z > 0.01, valid mu (not -9)
                        if z > 0.01 and mu > 0 and sigma > 0 and sigma < 10:
                            data['z'].append(z)
                            data['mu'].append(mu)
                            data['sigma'].append(sigma)
                    except (ValueError, IndexError):
                        continue

        return {k: np.array(v) for k, v in data.items()}

    def load_sparc_catalog(self) -> List[Dict]:
        sparc_file = self.data_root / "sparc" / "sparc_full_catalog.csv"
        galaxies = []
        with open(sparc_file, 'r') as f:
            header = next(f).strip().split(',')
            for line in f:
                parts = line.strip().split(',')
                gal = {}
                for i, key in enumerate(header):
                    try:
                        gal[key] = float(parts[i]) if i > 1 else parts[i]
                    except (ValueError, IndexError):
                        gal[key] = parts[i] if i < len(parts) else None
                galaxies.append(gal)
        return galaxies
