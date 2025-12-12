#!/usr/bin/env python3
"""
Run full validation with comprehensive physical consistency checks.

This script:
1. Runs the full validation suite
2. Performs cross-domain consistency checks
3. Validates physical values
4. Saves detailed results
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from cdqf_validation_runner_v4_0 import CDQFValidationRunner, AVAILABLE_DOMAINS

def main():
    """Run full validation with all checks."""
    print("=" * 70)
    print("CDQF FULL VALIDATION WITH PHYSICAL CONSISTENCY CHECKS")
    print("=" * 70)
    print()
    
    # Run validation
    runner = CDQFValidationRunner(
        quiet=False,
        cosmology_method='proper',
        use_rx=True,
        sparc_formula='separated',
        sparc_b_prediction=False
    )
    
    print("Running full validation suite...")
    print()
    
    results = runner.run_validation(domains=AVAILABLE_DOMAINS)
    
    # Save results
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    results_file = results_dir / f"validation_full_{timestamp}.json"
    
    # Convert results to JSON-serializable format
    results_dict = {
        'run_id': results['run_id'],
        'timestamp': timestamp,
        'total_pass': results['total_pass'],
        'total_tests': results['total_tests'],
        'total_fail': results['total_fail'],
        'total_theoretical': results['total_theoretical'],
        'consistency_issues': results.get('consistency_issues', []),
        'domains': {}
    }
    
    # Save domain results
    for domain in AVAILABLE_DOMAINS:
        domain_result = runner.run_domain(domain)
        results_dict['domains'][domain] = {
            'n_pass': domain_result.n_pass,
            'n_fail': domain_result.n_fail,
            'n_error': domain_result.n_error,
            'n_skip': domain_result.n_skip,
            'n_theoretical': domain_result.n_theoretical,
            'tests': [
                {
                    'test_name': t.test_name,
                    'status': t.status,
                    'value': t.value,
                    'expected': t.expected,
                    'error': t.error,
                    'chi2': t.chi2,
                    'notes': t.notes
                }
                for t in domain_result.tests
            ]
        }
    
    with open(results_file, 'w') as f:
        json.dump(results_dict, f, indent=2, default=str)
    
    print()
    print("=" * 70)
    print(f"Results saved to: {results_file}")
    print("=" * 70)
    
    # Final status
    if results['total_fail'] > 0 or results.get('consistency_issues'):
        print()
        print("⚠️  VALIDATION COMPLETE WITH ISSUES")
        if results['total_fail'] > 0:
            print(f"   Failed tests: {results['total_fail']}")
        if results.get('consistency_issues'):
            print(f"   Consistency issues: {len(results['consistency_issues'])}")
        return 1
    else:
        print()
        print("✅ VALIDATION COMPLETE - ALL CHECKS PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())

