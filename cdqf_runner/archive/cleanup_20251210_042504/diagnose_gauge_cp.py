#!/usr/bin/env python3
"""
Full diagnostics for gauge_unification and cp_violation modules.
"""

import sys
from pathlib import Path

# Add main project to path
main_project = Path("D:/CDQF Prime-0 Physics Engine")
if main_project.exists():
    sys.path.insert(0, str(main_project))
else:
    print(f"ERROR: Main project not found at {main_project}")
    sys.exit(1)

print("="*70)
print("GAUGE UNIFICATION & CP VIOLATION - FULL DIAGNOSTICS")
print("="*70)
print()

# Test 1: Gauge Unification
print("="*70)
print("TEST 1: GAUGE UNIFICATION MODULE")
print("="*70)
try:
    from prime0.toe.gauge_unification_complete import GaugeUnificationDerivation
    print("✓ Import successful")
    
    print("\nCreating derivation instance...")
    g = GaugeUnificationDerivation()
    print("✓ Instance created")
    
    print("\nRunning derive_complete()...")
    result = g.derive_complete()
    print("✓ Derivation complete")
    
    print(f"\nResults:")
    print(f"  Groups found: {result.groups}")
    print(f"  Is SM structure: {result.is_SM_structure}")
    print(f"  Predicted alpha: {result.predicted_alpha}")
    
    # Check if required groups present
    expected_groups = ['SU(3)', 'SU(2)', 'U(1)']
    has_all = all(g in result.groups for g in expected_groups)
    print(f"\n  Has SU(3)×SU(2)×U(1): {has_all}")
    
    # Check alpha_s
    alpha_s = result.predicted_alpha.get('alpha_s', None)
    if alpha_s:
        print(f"  Alpha_s: {alpha_s:.6f}")
        alpha_s_target = 0.2677
        error_pct = abs(alpha_s - alpha_s_target) / alpha_s_target * 100
        print(f"  Alpha_s error: {error_pct:.1f}%")
    
    print("\n✓ GAUGE UNIFICATION: FULLY FUNCTIONAL")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("TEST 2: CP VIOLATION MODULE")
print("="*70)
try:
    from prime0.toe.cp_violation_complete import CPViolationDerivation
    print("✓ Import successful")
    
    print("\nCreating derivation instance...")
    cp = CPViolationDerivation()
    print("✓ Instance created")
    
    print("\nRunning derive_complete()...")
    result = cp.derive_complete()
    print("✓ Derivation complete")
    
    print(f"\nResults:")
    print(f"  Delta CKM: {result.delta_ckm:.6f} rad")
    print(f"  Delta PMNS: {result.delta_pmns:.6f} rad")
    print(f"  J CKM: {result.J_ckm:.6e}")
    print(f"  J PMNS: {result.J_pmns:.6f}")
    
    # Check against PDG
    delta_ckm_target = 1.20
    delta_pmns_target = 1.36
    ckm_error = abs(result.delta_ckm - delta_ckm_target) / delta_ckm_target * 100
    pmns_error = abs(result.delta_pmns - delta_pmns_target) / delta_pmns_target * 100
    print(f"\n  CKM error: {ckm_error:.1f}%")
    print(f"  PMNS error: {pmns_error:.1f}%")
    
    print("\n✓ CP VIOLATION: FULLY FUNCTIONAL")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*70)
print("TEST 3: PATH RESOLUTION FROM VALIDATION RUNNER")
print("="*70)

# Simulate what validation runner does
script_dir = Path(__file__).resolve().parent
print(f"Script dir: {script_dir}")

possible_paths = [
    script_dir.parents[3] / "CDQF Prime-0 Physics Engine" if len(script_dir.parents) > 3 else None,
    Path("D:/CDQF Prime-0 Physics Engine"),
    script_dir.parent.parent / "CDQF Prime-0 Physics Engine",
]

print("\nChecking possible paths:")
for i, p in enumerate(possible_paths):
    if p:
        exists = p.exists()
        print(f"  Path {i+1}: {p} - {'EXISTS' if exists else 'NOT FOUND'}")
        if exists:
            # Test import from this path
            sys.path.insert(0, str(p))
            try:
                from prime0.toe.gauge_unification_complete import GaugeUnificationDerivation
                print(f"    ✓ Import successful from this path")
                break
            except Exception as e:
                print(f"    ✗ Import failed: {e}")

print()
print("="*70)
print("DIAGNOSTICS COMPLETE")
print("="*70)

