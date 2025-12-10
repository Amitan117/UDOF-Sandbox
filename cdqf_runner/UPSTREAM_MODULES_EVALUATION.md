# Upstream Modules Evaluation Report

**Date:** 2025-12-10  
**Runner Version:** 4.0.0  
**Evaluation Status:** Complete

---

## Executive Summary

**Module 3 (compute_S_ESE_proper): ✅ READY FOR INTEGRATION**  
**Modules 1 & 2: ⚠️ REQUIRE DEPENDENCY EXTRACTION**

---

## Module 1: ProperCorrectedGrowth

### Status: ⚠️ REQUIRES EXTRACTION

**Location:** `boltzmann_mcmc/cdqf_boltzmann_corrected.py`  
**Inherits from:** `CDQFBoltzmannFull` (which requires `classy`)

### Functionality Assessment

**✅ Core Growth Computation:**
- Implements corrected growth ODE: `D'' + [2 + dlnH/dlna] D' - (3/2) μ_eff(a) Ω_cl(a) D = 0`
- Uses clustering fraction ξ(a) from pivot decomposition
- Includes effective gravitational coupling μ_eff(a)
- Growth factor computation is **standalone** (doesn't require CLASS)

**❌ Dependency Issue:**
- Inherits from `CDQFBoltzmannFull` which imports `classy` (CLASS Python wrapper)
- CLASS is only used for σ₈ normalization, not for growth computation
- For validation runner, we can extract just the growth ODE

### Parameter Alignment: ✅ PASS

**Uses MCMC-validated parameters:**
- H0, Omega_m, Omega_b from cosmology locks
- Omega_geom_0, alpha_geom, p_op from dark_sector locks
- Parameters match v4.0 runner defaults

### Model Coherence: ✅ PASS

**Results align with CDQF model:**
- Clustering fraction ξ(a) matches validated pivot decomposition
- Growth factor D(z) properly normalized to D(0)=1
- Effective gravitational coupling μ_eff includes ESE modifications
- Consistent with current CDQF dark sector framework

### Test Value: ✅ HIGH

**Provides valuable validation:**
- Tests growth factor D(z) at multiple redshifts
- Validates clustering fraction approach
- Tests ESE modifications to gravitational coupling
- Critical for LSS and RSD constraints

### Integration Strategy

**Extract standalone growth computation:**
1. Copy `_growth_ode_corrected` method
2. Copy `compute_growth_factor_corrected` method
3. Copy `xi_clustering_fraction` method
4. Copy `mu_effective` method
5. Copy `Omega_clustering` method
6. Remove CLASS dependency (use simple σ₈ normalization or skip)

**Estimated LOC:** ~150 lines (standalone version)

---

## Module 2: TSESEResponseDerivation

### Status: ⚠️ REQUIRES DEPENDENCY HANDLING

**Location:** `boltzmann_mcmc/ruthless_analysis/phase2_theory/response_model/derive_from_ese_kernel.py`  
**Dependencies:** `ProperCorrectedGrowth` (which requires CLASS)

### Functionality Assessment

**✅ Core R_X Computation:**
- Derives C_X(a) = ξ(a) from validated pivot decomposition
- Implements R_X(a,k) = 1 / [1 + (k/k_⋆(a))^n]
- Uses constraint: R_X(k=0.1) ≈ 1 (from k_star MCMC)
- Scale-dependent response at halo/galaxy scales

**❌ Dependency Issue:**
- Requires `ProperCorrectedGrowth` for ξ(a) computation
- Can be extracted to standalone if we extract ProperCorrectedGrowth first

### Parameter Alignment: ✅ PASS

**Uses MCMC-validated parameters:**
- H0, Omega_m, Omega_b from cosmology locks
- Omega_geom_0, alpha_geom, p_op from dark_sector locks
- ESE parameters (ell_IR, ell_star, k_ese, X0) from locks
- Parameters match v4.0 runner defaults

### Model Coherence: ✅ PASS

**Results align with CDQF model:**
- C_X(a) = ξ(a) ensures consistency with validated growth
- R_X constraint from k_star MCMC validation
- Scale-dependent response matches TS-ESE kernel structure
- Consistent with current CDQF response model

### Test Value: ✅ HIGH

**Provides valuable validation:**
- Tests R_X at cosmological scales (k=0.1 h/Mpc, should be ~1)
- Tests R_X at galaxy scales (k=0.5 h/Mpc, shows suppression)
- Validates scale-dependent dark matter response
- Critical for SPARC and halo-scale tests

### Integration Strategy

**Extract standalone R_X computation:**
1. Extract ξ(a) computation (from ProperCorrectedGrowth)
2. Copy `_derive_C_X` method
3. Copy `_derive_R_X` method
4. Copy `R_X` method
5. Copy `C_X` method
6. Remove ProperCorrectedGrowth dependency (use extracted ξ(a))

**Estimated LOC:** ~200 lines (standalone version)

---

## Module 3: compute_S_ESE_proper

### Status: ✅ READY FOR INTEGRATION

**Location:** `prime0/toe/sparc_campaign/compute_proper_s_ese.py`  
**Dependencies:** `prime0.modules.ese_dark_sector` (available in parent repo)

### Functionality Assessment

**✅ Core S_ESE Computation:**
- Computes X(r) from surface density Σ(r) and velocity dispersion σ_g(r)
- Computes s(X) from ESE map
- Builds S_ESE(r) using multiple methods:
  - `gradient`: S(r) ∝ |ds/dr| (gradient energy)
  - `enhancement`: S(r) ∝ F(s) (enhancement factor)
  - `combined`: S(r) ∝ |ds/dr| × F(s)
  - `s_activation`: S(r) = s(X) (direct activation)

**✅ Test Results:**
- Gradient method: S_ESE range [0.77, 1.00] ✓
- s_activation method: S_ESE range [0.27, 0.64] ✓
- Properly handles edge cases and normalization

### Parameter Alignment: ✅ PASS

**Uses current locks structure:**
- `calibrated_locks.eta_star` (0.171)
- `calibrated_locks.X0` (0.6481)
- `pivots.Sigma0_kg_m2` (0.217)
- `ese_map.ell_IR`, `ese_map.ell_star`
- Matches v4.0 runner lock structure exactly

### Model Coherence: ✅ PASS

**Results align with CDQF model:**
- Uses proper ESE framework (ESEDarkSector/ESEDarkSectorDerived)
- Computes X from observables using calibrated parameters
- S_ESE structure function derived from first principles
- Consistent with SPARC separated formula approach

### Test Value: ✅ HIGH

**Provides valuable validation:**
- Enables SPARC separated formula test (currently SKIP)
- Tests ESE structure function at galaxy scales
- Validates proper ESE computation vs. toy models
- Critical for dark matter phenomenology tests

### Integration Strategy

**Direct integration (with dependency handling):**
1. Copy `compute_S_ESE_proper` function
2. Copy `compute_S_ESE_from_X` function
3. Copy `compute_surface_density_profile` function
4. Import `ESEDarkSector` and `ESEDarkSectorDerived` from parent repo
5. Add graceful fallback if `prime0.modules.ese_dark_sector` unavailable

**Estimated LOC:** ~300 lines (with dependencies)

**Alternative:** Copy `ESEDarkSector` classes into runner (breaks isolation)

---

## Integration Plan

### Phase 1: Extract Standalone Growth Computation ✅

**Goal:** Extract ProperCorrectedGrowth without CLASS dependency

**Steps:**
1. Extract `xi_clustering_fraction` method (standalone)
2. Extract `mu_effective` method (standalone)
3. Extract `Omega_clustering` method (standalone)
4. Extract `_growth_ode_corrected` method (standalone)
5. Extract `compute_growth_factor_corrected` method (standalone)
6. Extract `D_corrected` and `f_growth_corrected` methods
7. Remove CLASS dependency (use simple σ₈ normalization or reference value)

**Files to create:**
- `cdqf_runner/integrated_modules/proper_growth_standalone.py`

**Estimated Size:** ~200 lines

---

### Phase 2: Extract Standalone R_X Computation ✅

**Goal:** Extract TSESEResponseDerivation without ProperCorrectedGrowth dependency

**Steps:**
1. Use extracted ξ(a) from Phase 1
2. Extract `_derive_C_X` method
3. Extract `_derive_R_X` method
4. Extract `R_X` and `C_X` methods
5. Remove ProperCorrectedGrowth dependency

**Files to create:**
- `cdqf_runner/integrated_modules/rx_response_standalone.py`

**Estimated Size:** ~150 lines

---

### Phase 3: Integrate S_ESE Computation ✅

**Goal:** Integrate compute_S_ESE_proper with dependency handling

**Steps:**
1. Copy `compute_S_ESE_proper` function
2. Copy helper functions
3. Add import with graceful fallback:
   ```python
   try:
       from prime0.modules.ese_dark_sector import ESEDarkSector, ESEDarkSectorDerived
   except ImportError:
       # Fallback: use simplified version or SKIP test
   ```
4. Update SPARC test to use integrated function

**Files to create:**
- `cdqf_runner/integrated_modules/sparc_ese_computation.py`

**Estimated Size:** ~300 lines

---

## Validation Tests

### Test 1: Growth Factor Coherence

**Test:** Compare extracted growth factor with reference values
- D(z=0) should be 1.0
- D(z=1) should be ~0.55-0.70
- Growth rate f(z) should be ~0.5-0.7

### Test 2: R_X Response Coherence

**Test:** Verify R_X matches expected behavior
- R_X(k=0.1, z=0) should be ~1.0 (cosmological scale)
- R_X(k=0.5, z=0) should be ~0.95-0.99 (galaxy scale)
- C_X(z=0) should match clustering fraction ξ(z=0)

### Test 3: S_ESE Structure Function

**Test:** Verify S_ESE produces reasonable values
- S_ESE should be in range [0, 1] (normalized)
- Gradient method should show radial structure
- s_activation method should show smooth decline

---

## Risk Assessment

### Low Risk ✅
- **Module 3 (S_ESE):** Already functional, just needs import handling
- **Parameter alignment:** All modules use current locks structure
- **Model coherence:** All modules align with current CDQF model

### Medium Risk ⚠️
- **Dependency extraction:** Need to carefully extract growth/R_X without breaking logic
- **Testing:** Need to verify extracted modules produce same results as originals

### Mitigation
- Extract modules incrementally
- Add unit tests for each extracted component
- Compare results with original modules before integration
- Keep fallback to simple computations if extraction fails

---

## Recommendation

**✅ PROCEED WITH INTEGRATION**

All three modules:
1. ✅ Are functional and current
2. ✅ Use MCMC-validated parameters
3. ✅ Align with current CDQF model
4. ✅ Provide valuable test insights
5. ✅ Are coherent with full CDQF story

**Integration approach:**
1. Extract standalone versions (Phases 1-2) to avoid CLASS dependency
2. Integrate S_ESE directly with dependency handling (Phase 3)
3. Add comprehensive error handling and fallbacks
4. Test thoroughly before final integration

**Expected outcome:**
- Growth factor test uses proper corrected growth
- R_X test computes actual scale-dependent response
- SPARC separated formula test becomes functional
- All tests provide deeper validation insights

---

**Next Steps:**
1. Extract standalone growth computation
2. Extract standalone R_X computation
3. Integrate S_ESE computation
4. Update runner tests to use integrated modules
5. Verify all tests pass with integrated functionality

