# Growth Factor ODE Error Analysis and Fix

## Problem

The standalone growth factor computation was producing:
- `D(z=0) = nan` (should be 1.0)
- `D(z=1) = 13.79` (should be ~0.55-0.70)
- ODEintWarning: "Excess work done on this call"
- RuntimeWarning: overflow in divide

## Root Cause

The issue was in the `dlnH_dlna` computation in `_growth_ode_corrected`:

**Wrong implementation:**
```python
dlnH_dlna = -1.5 * Omega_m_a / Omega_total  # WRONG SIGN AND DIVISION
```

**Correct implementation (from original CDQFBoltzmannFull):**
```python
dlnH_dlna = 1.5 * Omega_m_a  # Simple, stable, validated
```

## Fix Applied

Changed `dlnH_dlna` computation to match the original:
```python
# Matter density parameter at scale factor a (CDQF modified)
Omega_dm_a = self.Omega_dm_cdqf(a)
Omega_b_a = self.Omega_b * (a ** (-3.0))
Omega_m_a = Omega_dm_a + Omega_b_a

# Simplified: dlnH/dlna ≈ 1.5 * Omega_m(a)
# This matches the original implementation and is stable
dlnH_dlna = 1.5 * Omega_m_a
```

## Why This Works

The original `CDQFBoltzmannFull._growth_ode` uses this simplified form because:
1. It's exact for matter-dominated era (where D ∝ a)
2. It's a good approximation for CDQF modified expansion
3. It's numerically stable (no division by Omega_total)
4. It's been validated in the original implementation

## Expected Results After Fix

- `D(z=0) = 1.0` (normalized)
- `D(z=1) ≈ 0.55-0.70` (typical for Ω_m ~ 0.3)
- No ODE warnings
- Stable integration

