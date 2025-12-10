# Testing New Master Unification Domains

**Date:** 2025-12-10  
**Status:** Ready for Testing

## New Domains Added

1. **quantum_gravity** - Tests graviton operators, Wheeler-DeWitt equation, G derivation
2. **baryogenesis** - Tests CP violation from collapse, complete leptogenesis  
3. **master_action** - Tests unified master action and sector limits

## Test Commands

### Test Individual Domains
```bash
cd D:\CDQF-Sandbox\cdqf_runner
python cdqf_validation_runner_v4.0.py --domain quantum_gravity
python cdqf_validation_runner_v4.0.py --domain baryogenesis
python cdqf_validation_runner_v4.0.py --domain master_action
```

### Test All New Domains
```bash
python cdqf_validation_runner_v4.0.py --domain quantum_gravity --domain baryogenesis --domain master_action
```

### Test Everything (includes new domains)
```bash
python cdqf_validation_runner_v4.0.py
```

## Expected Results

### quantum_gravity
- **graviton_cptp**: PASS (CPTP verification of Lindblad operators)
- **g_derivation**: PASS (G derived from operational framework, error < 10%)
- **wheeler_dewitt_classical**: PASS (Quantum/classical ratio < 1e-6)

### baryogenesis
- **cp_from_collapse**: PASS (δ_CKM and δ_PMNS within 50% of PDG)
- **baryon_asymmetry**: PASS/FAIL (η_B may need calibration)
- **mass_scale_scan**: PASS/SKIP (M_N matching η_B)

### master_action
- **action_components**: PASS (All action components computed)
- **sector_limits**: PASS (All sector limits verified)

## Integration Status

✅ All modules copied to sandbox  
✅ Imports updated for self-contained environment  
✅ Test methods added to validation runner  
✅ Domain list updated (22 → 25 domains)  
✅ Ready for validation run

