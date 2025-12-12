#!/usr/bin/env python3
"""
Run full CDQF validation and save results.
"""

import sys
import importlib.util
from pathlib import Path

# Import the validation runner module
spec = importlib.util.spec_from_file_location(
    "cdqf_validation_runner_v4_0",
    Path(__file__).parent / "cdqf_validation_runner_v4.0.py"
)
runner_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner_module)
CDQFValidationRunner = runner_module.CDQFValidationRunner


def main():
    """Run full validation."""
    runner = CDQFValidationRunner()

    print("\n" + "="*70)
    print("RUNNING FULL CDQF VALIDATION")
    print("="*70 + "\n")

    # Run all domains
    summary = runner.run_validation()

    # Print summary
    print("\n" + "="*70)
    print("VALIDATION COMPLETE")
    print("="*70)
    print(f"Run ID: {summary['run_id']}")
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['total_pass']}")
    print(f"Failed: {summary['total_fail']}")
    print(f"Theoretical: {summary['total_theoretical']}")
    print("="*70 + "\n")

    # Check gauge and CP violation specifically
    print("\nChecking gauge_symmetry and cp_violation domains...")
    gauge_result = runner.run_domain('gauge_symmetry')
    cp_result = runner.run_domain('cp_violation')

    print("\n[GAUGE_SYMMETRY]")
    for test in gauge_result.tests:
        print(f"  {test.test_name}: {test.status} - {test.notes[:60]}")

    print("\n[CP_VIOLATION]")
    for test in cp_result.tests:
        print(f"  {test.test_name}: {test.status} - {test.notes[:60]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
