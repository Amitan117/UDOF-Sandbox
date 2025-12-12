# Growth Factor 0.4% Overshoot Analysis

## Issue Identified

At higher resolution, a 0.4% overshoot is observed in the growth factor calculation.

## Potential Sources

### 1. **dlnH/dlna Computation**

**Original implementation (line 157):**
```python
dlnH_dlna = 1.5 * self.Omega_dm_cdqf(a)  # Geometric DM only
```

**My implementation:**
```python
Omega_m_a = Omega_dm_a + Omega_b_a
dlnH_dlna = 1.5 * Omega_m_a  # Includes baryons
```

**Difference at a=1:**
- `Omega_dm_cdqf(1) = 0.3266`
- `Omega_m_a(1) = 0.3766` (includes Omega_b = 0.05)
- Difference: **15.3%** in dlnH/dlna

**Impact:** This affects the damping term `[2 + dlnH/dlna]` in the ODE, which could cause accumulation errors.

---

### 2. **Normalization Precision**

The normalization `D_arr = D_arr / D_today` should ensure D(z=0) = 1.0 exactly, but:

- **At very high resolution**, floating point precision in the ODE integration
- **ODE tolerances** might need to be tighter
- **Interpolation** at exact z=0 might have numerical artifacts

---

### 3. **ODE Integration Tolerances**

Current tolerances: `atol=1e-8, rtol=1e-8`

At higher resolution (more points), might need:
- Tighter tolerances: `atol=1e-10, rtol=1e-10`
- Or adaptive step size control

---

## Fix Applied

**Updated `dlnH_dlna` to match original:**
```python
# Match original: use Omega_dm_cdqf only for dlnH/dlna
dlnH_dlna = 1.5 * Omega_dm_cdqf(a)
```

This ensures:
- ✅ Exact match with original implementation
- ✅ Correct Hubble evolution term
- ✅ No accumulation of errors from wrong damping

---

## Testing Needed

1. **Verify fix eliminates overshoot** at high resolution
2. **Compare D(z=1) values** with original
3. **Check if 0.4% is relative to:**
   - D(z=0) itself (should be exactly 1.0)
   - D(z=1) compared to reference
   - Comparison with CLASS output

---

## Additional Checks

If overshoot persists after fix:

1. **Tighter ODE tolerances**
   ```python
   atol=1e-10, rtol=1e-10  # Instead of 1e-8
   ```

2. **Explicit z=0 boundary handling**
   ```python
   def growth_factor(self, z):
       if abs(z) < 1e-12:
           return 1.0
       return np.interp(z, self._z_growth, self._D_growth)
   ```

3. **Verify normalization**
   - Check D_today value before normalization
   - Ensure D_grid[-1] is exactly 1.0 after normalization

---

**Status:** Fix applied - awaiting verification at higher resolution

