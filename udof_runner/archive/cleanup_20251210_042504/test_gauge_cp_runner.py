#!/usr/bin/env python3
"""Test gauge and CP modules the same way validation runner does."""

import sys
from pathlib import Path

# Mimic validation runner path resolution
script_dir = Path(__file__).resolve().parent
possible_paths = [
    script_dir.parents[3] / "CDQF Prime-0 Physics Engine" if len(script_dir.parents) > 3 else None,
    Path("D:/CDQF Prime-0 Physics Engine"),
    script_dir.parent.parent / "CDQF Prime-0 Physics Engine",
]

main_project = None
for p in possible_paths:
    if p and p.exists():
        main_project = p
        print(f"Using path: {p}")
        break

if main_project:
    sys.path.insert(0, str(main_project))
else:
    print("ERROR: No valid path found")
    sys.exit(1)

print("\n=== Testing Gauge Unification ===")
try:
    from prime0.toe.gauge_unification_complete import GaugeUnificationDerivation
    derivation = GaugeUnificationDerivation()
    structure = derivation.derive_complete()
    
    groups_found = structure.groups
    expected_groups = ['SU(3)', 'SU(2)', 'U(1)']
    has_sm_structure = all(g in groups_found for g in expected_groups)
    
    print(f"Groups: {groups_found}")
    print(f"Has SM structure: {has_sm_structure}")
    print(f"Is SM structure (property): {structure.is_SM_structure}")
    
    alpha_s = structure.predicted_alpha.get('alpha_s', 0)
    print(f"Alpha_s: {alpha_s}")
    
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing CP Violation ===")
try:
    from prime0.toe.cp_violation_complete import CPViolationDerivation
    derivation = CPViolationDerivation()
    result = derivation.derive_complete()
    
    print(f"Delta CKM: {result.delta_ckm:.4f}")
    print(f"Delta PMNS: {result.delta_pmns:.4f}")
    print(f"J CKM: {result.J_ckm:.6e}")
    print(f"J PMNS: {result.J_pmns:.6f}")
    
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

