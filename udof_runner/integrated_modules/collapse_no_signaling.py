"""
No-Signaling Constraint Test (B1)

Tests that collapse dynamics do not violate no-signaling:
- Two spacelike-separated subsystems A and B
- Apply collapse to subsystem A only
- Measure reduced density matrix evolution of subsystem B
- Requirement: (∂_t ρ_B) independent of operations on A
- Numerical deviation < machine precision
"""

import numpy as np
from typing import Dict, Tuple


def partial_trace_A(rho_AB_full: np.ndarray, dA: int, dB: int) -> np.ndarray:
    """Trace out subsystem A to get reduced density matrix of B."""
    rho_B = np.zeros((dB, dB), dtype=complex)
    for i in range(dB):
        for j in range(dB):
            for k in range(dA):
                idx_ik = k * dB + i
                idx_jk = k * dB + j
                if idx_ik < rho_AB_full.shape[0] and idx_jk < rho_AB_full.shape[1]:
                    rho_B[i, j] += rho_AB_full[idx_ik, idx_jk]
    return rho_B


def _measurement_channel_on_A(rho_AB: np.ndarray, p: float, dA: int, dB: int) -> np.ndarray:
    """
    Apply a stable CPTP "partial measurement" channel on subsystem A only.

    rho' = (1-p) rho + p * sum_i (P_i ⊗ I) rho (P_i ⊗ I)

    This is trace-preserving and completely positive by construction.
    """
    p = float(np.clip(p, 0.0, 1.0))
    dim = dA * dB
    if rho_AB.shape != (dim, dim):
        raise ValueError(
            f"rho_AB shape mismatch: expected {(dim, dim)}, got {rho_AB.shape}")

    I_B = np.eye(dB, dtype=complex)
    measured = np.zeros_like(rho_AB, dtype=complex)

    for i in range(dA):
        P_i_A = np.zeros((dA, dA), dtype=complex)
        P_i_A[i, i] = 1.0
        P_i = np.kron(P_i_A, I_B)
        measured += P_i @ rho_AB @ P_i.conj().T

    rho_prime = (1.0 - p) * rho_AB + p * measured
    # Numerical cleanup
    tr = np.trace(rho_prime)
    if abs(tr) > 1e-15:
        rho_prime = rho_prime / tr
    return rho_prime


def compute_collapse_evolution(
    rho_AB: np.ndarray,
    collapse_rate_A: float,
    dt: float,
    dA: int,
    dB: int,
    apply_to_A_only: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Evolve rho_AB one step and return reduced rho_B.

    Uses p = 1 - exp(-Γ dt) as the per-step collapse probability.
    """
    if apply_to_A_only:
        p = 1.0 - float(np.exp(-float(collapse_rate_A) * float(dt)))
        rho_evolved = _measurement_channel_on_A(rho_AB, p=p, dA=dA, dB=dB)
    else:
        rho_evolved = rho_AB

    rho_B_reduced = partial_trace_A(rho_evolved, dA, dB)
    rho_B_control = partial_trace_A(rho_AB, dA, dB)
    return rho_evolved, rho_B_reduced, rho_B_control


def test_no_signaling(
    collapse_rate: float = 1e23,  # s^-1 (cluster scale)
    dt: float = 1e-30,  # s (ensure Γ·dt << 1 for numerical stability)
    dA: int = 2,  # Dimension of subsystem A
    dB: int = 2,  # Dimension of subsystem B
    n_steps: int = 100
) -> Dict[str, float]:
    """
    Test no-signaling constraint.

    Requirement: (∂_t ρ_B) independent of operations on A.
    Numerical deviation < machine precision.

    Returns
    -------
    Dict with:
    - max_deviation: Maximum deviation in ρ_B evolution
    - signaling_violation: True if violation detected
    - rho_B_final_A_only: Final ρ_B when collapse on A
    - rho_B_final_control: Final ρ_B when no collapse
    """
    # Initialize maximally entangled state |Ψ⟩ = (|00⟩ + |11⟩)/√2
    rho_AB = np.zeros((dA * dB, dA * dB), dtype=complex)
    rho_AB[0, 0] = 0.5  # |00⟩⟨00|
    rho_AB[-1, -1] = 0.5  # |11⟩⟨11|
    rho_AB[0, -1] = 0.5  # |00⟩⟨11|
    rho_AB[-1, 0] = 0.5  # |11⟩⟨00|

    max_deviation = 0.0

    # Evolve full bipartite system
    rho_AB_A_only = rho_AB.copy()
    rho_AB_control = rho_AB.copy()

    for step in range(n_steps):
        # Evolve with collapse on A
        rho_AB_A_only, rho_B_A_only_new, _ = compute_collapse_evolution(
            rho_AB_A_only, collapse_rate, dt, dA=dA, dB=dB, apply_to_A_only=True
        )

        # Evolve without collapse (control)
        rho_AB_control, _, rho_B_control_new = compute_collapse_evolution(
            rho_AB_control, 0.0, dt, dA=dA, dB=dB, apply_to_A_only=False
        )

        # Check deviation
        deviation = np.max(np.abs(rho_B_A_only_new - rho_B_control_new))
        max_deviation = max(max_deviation, deviation)

    # Machine precision threshold
    machine_precision = np.finfo(float).eps

    signaling_violation = max_deviation > machine_precision

    # Get final reduced density matrices
    _, rho_B_final_A_only, _ = compute_collapse_evolution(
        rho_AB_A_only, collapse_rate, 0.0, dA=dA, dB=dB, apply_to_A_only=True
    )
    _, _, rho_B_final_control_ref = compute_collapse_evolution(
        rho_AB_control, 0.0, 0.0, dA=dA, dB=dB, apply_to_A_only=False
    )

    return {
        'max_deviation': float(max_deviation),
        'signaling_violation': bool(signaling_violation),
        'machine_precision': float(machine_precision),
        'compliant': not signaling_violation,
        'rho_B_final_A_only': np.array(rho_B_final_A_only).tolist(),
        'rho_B_final_control': np.array(rho_B_final_control_ref).tolist(),
    }
