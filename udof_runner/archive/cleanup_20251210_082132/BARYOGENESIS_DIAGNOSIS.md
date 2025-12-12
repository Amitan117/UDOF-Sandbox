# Baryogenesis η_B Issue - Diagnostic Analysis

**Date:** 2025-12-10  
**Problem:** η_B = 2.47×10⁻⁴⁹ vs expected 6.1×10⁻¹⁰ (10³⁹ too small)

---

## Current Calculation Chain

### 1. Base CP Asymmetry ε₁
```
ε_base = (3/16π) × (M_N/M_P) × (Δm²/M_N²) × sin(δ_PMNS)
```

**For M_N = 1e12 GeV:**
- M_N/M_P = 1e12 / 2.435e18 = 4.1×10⁻⁷
- Δm² ≈ 2.5×10⁻³ eV² = 2.5×10⁻²¹ GeV² (using dm2_31)
- Δm²/M_N² = 2.5×10⁻²¹ / (1e12)² = 2.5×10⁻⁴⁵ GeV⁻²
- sin(1.36) ≈ 0.977

**Result:** ε_base ≈ 2×10⁻⁵² (extremely small!)

### 2. Collapse Enhancement f_collapse
```
f_collapse = 1 + (Γ/Γ_ref)^α
```
- Γ = 1e23 s⁻¹ (cluster scale)
- Γ_ref = 1e15 s⁻¹
- α = 0.7
- f_collapse = 1 + (1e8)^0.7 ≈ 2.5×10⁵

**Enhanced:** ε₁ = ε_base × f_collapse ≈ 5×10⁻⁴⁷

### 3. Efficiency Factor κ
```
κ_thermal = 1/(1+K) for K<1, or 0.1/K for K>>1
collapse_enhancement = 1 + 10×(Γ/1e20)^0.3
κ = κ_thermal × collapse_enhancement (bounded ≤ 1)
```

For M_N = 1e12 GeV:
- collapse_enhancement ≈ 81
- κ ≈ 1.0 (hits bound)

### 4. Baryon Asymmetry
```
η_L = -ε₁ × κ ≈ -5×10⁻⁴⁷
η_B = -0.01 × η_L ≈ 5×10⁻⁴⁹
```

---

## Root Cause Analysis

### Issue 1: Base ε₁ Formula May Be Wrong

The standard leptogenesis formula uses:
```
ε₁ ≈ (3/16π) × (M_N/M_P) × (Δm²/M_N²) × sin(δ)
```

But this gives **extremely small** values because:
- (M_N/M_P) is very small (heavy neutrino << Planck scale)
- (Δm²/M_N²) is extremely small (light neutrino splitting << heavy neutrino mass)

**This formula may need M_N-dependent Yukawa couplings!**

Standard leptogenesis typically uses:
```
ε₁ ≈ (3/16π) × (M_1/M_P) × (m_ν/M_1) × sin(δ)
```
where m_ν is the light neutrino mass scale, not Δm²!

### Issue 2: Enhancement Factors Not Strong Enough

Even with f_collapse ≈ 2.5×10⁵, we need ~10³⁹ more enhancement!

---

## Solution Approach

1. **Fix Base Formula:** Use light neutrino mass scale m_ν instead of Δm²
2. **Increase Enhancement:** Make collapse enhancement more aggressive
3. **Calibrate Carefully:** Ensure changes don't break other domains

