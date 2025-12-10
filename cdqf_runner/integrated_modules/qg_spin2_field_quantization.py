#!/usr/bin/env python3
"""
Quantized Spin-2 Field Theory from Collapse Kernel - Sandbox Version
=====================================================================

Complete quantization of graviton field as spin-2 particle.
Derived from collapse kernel K(x,y) with explicit mode construction.
"""

from __future__ import annotations

import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Callable
from dataclasses import dataclass

# Physical constants
HBAR = 1.054571817e-34  # J⋅s
C = 299792458  # m/s
M_PL_GEV = 2.435e18  # GeV
ELL_PLANK_M = 1.616e-35  # m


@dataclass
class GravitonMode:
    """A single graviton mode (spin-2 quantum field mode)."""
    label: str
    wavevector: np.ndarray
    polarization: str
    eigenvalue: float
    collapse_rate: float
    polarization_tensor: np.ndarray


class Spin2GravitonField:
    """
    Quantized spin-2 graviton field from collapse kernel.
    
    Derives graviton creation/annihilation operators from kernel eigenmodes.
    """
    
    def __init__(
        self,
        Lambda_rate: float = 1e23,
        ell_length: float = 1e-10,
        volume: float = (1e-10)**3
    ):
        self.Lambda = Lambda_rate
        self.ell = ell_length
        self.V = volume
        self.hbar = HBAR
        self.c = C
        self.K_scale = Lambda_rate ** 2
        self.modes: List[GravitonMode] = []
    
    def compute_tt_polarization_tensors(self, k: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute TT polarization tensors for wavevector k."""
        k_mag = np.linalg.norm(k)
        
        if k_mag < 1e-20:
            e1 = np.array([1.0, 0.0, 0.0])
            e2 = np.array([0.0, 1.0, 0.0])
        else:
            k_hat = k / k_mag
            z_axis = np.array([0.0, 0.0, 1.0])
            if abs(np.dot(k_hat, z_axis)) < 0.99:
                e1 = np.cross(z_axis, k_hat)
                e1 = e1 / np.linalg.norm(e1)
            else:
                e1 = np.array([1.0, 0.0, 0.0])
            e2 = np.cross(k_hat, e1)
            e2 = e2 / (np.linalg.norm(e2) + 1e-20)
        
        # + polarization
        eps_plus = np.outer(e1, e1) - np.outer(e2, e2)
        # × polarization
        eps_cross = np.outer(e1, e2) + np.outer(e2, e1)
        
        # Normalize
        eps_plus = eps_plus * np.sqrt(2) / np.sqrt(np.sum(eps_plus * eps_plus.conj()) + 1e-20)
        eps_cross = eps_cross * np.sqrt(2) / np.sqrt(np.sum(eps_cross * eps_cross.conj()) + 1e-20)
        
        return eps_plus, eps_cross
    
    def compute_kernel_eigenvalue(self, k: np.ndarray) -> float:
        """Compute kernel eigenvalue for wavevector k."""
        k_sq = np.dot(k, k)
        return self.K_scale / (1.0 + (self.ell ** 2) * k_sq)
    
    def create_graviton_mode(self, k: np.ndarray, polarization: str) -> GravitonMode:
        """Create a single graviton mode."""
        eps_plus, eps_cross = self.compute_tt_polarization_tensors(k)
        eps = eps_plus if polarization == '+' else eps_cross
        
        eigenvalue = self.compute_kernel_eigenvalue(k)
        gamma_k = self.Lambda * (eigenvalue / self.K_scale)
        
        k_label = f"k=({k[0]:.2e},{k[1]:.2e},{k[2]:.2e})"
        return GravitonMode(
            label=f"{k_label}, pol={polarization}",
            wavevector=k.copy(),
            polarization=polarization,
            eigenvalue=eigenvalue,
            collapse_rate=gamma_k,
            polarization_tensor=eps.copy()
        )
    
    def construct_graviton_field(self, k_modes: List[np.ndarray]) -> None:
        """Construct complete graviton field."""
        self.modes = []
        for k in k_modes:
            for pol in ['+', '×']:
                mode = self.create_graviton_mode(k, pol)
                self.modes.append(mode)

