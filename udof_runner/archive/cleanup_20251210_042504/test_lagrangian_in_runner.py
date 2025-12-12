#!/usr/bin/env python3
"""Quick test to verify Lagrangian integration in v4.0 runner."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from cdqf_validation_runner_v4_0 import CDQFTests

# Create test instance
tests = CDQFTests({})

# Test inflation
print("Testing inflation domain...")
try:
    result = tests.test_inflation()
    print(f"  Status: {result.n_pass}/{len(result.tests)} tests passed")
    for test in result.tests:
        print(f"    {test.test_name}: {test.status} = {test.value}")
        if 'LAGRANGIAN' in test.notes:
            print(f"      ✓ Using Lagrangian module")
except Exception as e:
    print(f"  ERROR: {e}")

print()

# Test dark energy
print("Testing dark energy domain...")
try:
    result = tests.test_dark_energy()
    print(f"  Status: {result.n_pass}/{len(result.tests)} tests passed")
    for test in result.tests:
        print(f"    {test.test_name}: {test.status} = {test.value}")
        if 'LAGRANGIAN' in test.notes:
            print(f"      ✓ Using Lagrangian module")
except Exception as e:
    print(f"  ERROR: {e}")

