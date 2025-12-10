# Full Validation Run Instructions

**Date:** 2025-12-10  
**Purpose:** Run complete validation with physical consistency checks

## What Was Added

### 1. Cross-Domain Consistency Checks
- Validates parameter consistency across domains (e.g., H0 values)
- Checks for physical consistency (no negative masses, superluminal speeds)
- Detects placeholders marked as PASS
- Identifies NaN/Inf values

### 2. Physical Validation
- Checks all PASS tests for unphysical values
- Validates speed limits (c)
- Validates mass/energy/length scales
- Flags extremely large values

### 3. Automatic Results Saving
- Results automatically saved to `results/` directory
- JSON format with full test details
- Timestamped files

## Running Full Validation

### Option 1: Direct Runner
```bash
cd D:\CDQF-Sandbox\cdqf_runner
python cdqf_validation_runner_v4.0.py
```

### Option 2: Using Venv (if available)
```bash
cd D:\CDQF-Sandbox\cdqf_runner
venv\Scripts\python.exe cdqf_validation_runner_v4.0.py
```

### Option 3: Test Specific Domains
```bash
python cdqf_validation_runner_v4.0.py --domain quantum_gravity --domain baryogenesis --domain master_action
```

## What Gets Validated

### All 25 Domains:
1. fermion_masses
2. pmns_mixing
3. ckm_mixing
4. neutrino_masses
5. h4_geometry
6. gauge_symmetry
7. rg_evolution
8. ward_identities
9. bao
10. sne
11. sparc
12. dark_matter
13. dark_energy
14. early_universe
15. lss
16. strong_field
17. precision_tests
18. cmb
19. inflation
20. cp_violation
21. microphysics
22. gw_ringdown
23. **quantum_gravity** (NEW)
24. **baryogenesis** (NEW)
25. **master_action** (NEW)

### Consistency Checks:
- H0 consistency across cosmology domains
- Fermion mass consistency
- Gauge coupling consistency
- Physical value validation
- Placeholder detection
- NaN/Inf detection

## Output

### Console Output:
- Domain-by-domain test results
- Physical consistency validation
- Cross-domain consistency checks
- Summary statistics

### JSON Results:
- Saved to `results/cdqf_v4.0_TIMESTAMP.json`
- Full test details
- All computed values
- Error information

## Expected Issues to Review

1. **New domains** may have calibration issues (baryogenesis η_B)
2. **Cross-domain** parameter consistency
3. **Physical values** - all should be reasonable
4. **No placeholders** - all values should be computed

## After Running

1. Review console output for consistency issues
2. Check JSON results file for detailed values
3. Use `validate_physical_consistency.py` for additional analysis:
   ```bash
   python validate_physical_consistency.py
   ```

