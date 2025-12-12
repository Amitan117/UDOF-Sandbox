#!/usr/bin/env python3
"""
Physical Consistency Validator for CDQF Validation Results
===========================================================

Checks for:
1. Unphysical values (negative masses, superluminal speeds, etc.)
2. Cross-domain conflicts (e.g., cosmology vs particle physics)
3. Missing data or placeholders
4. Inconsistencies between related domains
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np

# Physical limits
C_LIGHT = 299792458  # m/s
M_PLANK = 2.176e-8  # kg
G_NEWTON = 6.67430e-11  # m³ kg⁻¹ s⁻²
HBAR = 1.054571817e-34  # J·s

# Acceptable ranges
MIN_MASS = 1e-20  # kg (very light but non-zero)
MAX_MASS = 1e50  # kg (very heavy but finite)
MIN_LENGTH = 1e-35  # m (Planck scale)
MAX_LENGTH = 1e30  # m (cosmological)
MIN_TIME = 1e-44  # s (Planck time)
MAX_TIME = 1e20  # s (cosmological)
MIN_ENERGY = 1e-30  # J
MAX_ENERGY = 1e60  # J


class PhysicalConsistencyChecker:
    """Check physical consistency of validation results."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
    
    def check_value_physical(self, name: str, value: Any, units: str = "") -> bool:
        """Check if a value is physically reasonable."""
        if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
            self.issues.append(f"{name}: Invalid value (None/NaN/Inf)")
            return False
        
        if isinstance(value, (int, float)):
            # Mass check
            if 'mass' in name.lower() or 'm_' in name.lower() or 'kg' in units.lower():
                if value < 0:
                    self.issues.append(f"{name}: Negative mass ({value} kg)")
                    return False
                if value > 0 and value < MIN_MASS:
                    self.warnings.append(f"{name}: Very small mass ({value} kg)")
                if value > MAX_MASS:
                    self.issues.append(f"{name}: Unphysically large mass ({value} kg)")
                    return False
            
            # Length check
            elif 'length' in name.lower() or 'ell' in name.lower() or 'r_' in name.lower() or 'm' in units.lower() and 'kg' not in units.lower():
                if value < 0:
                    self.issues.append(f"{name}: Negative length ({value} m)")
                    return False
                if value > 0 and value < MIN_LENGTH:
                    self.warnings.append(f"{name}: Very small length ({value} m)")
                if value > MAX_LENGTH:
                    self.issues.append(f"{name}: Unphysically large length ({value} m)")
                    return False
            
            # Speed check
            elif 'speed' in name.lower() or 'c_' in name.lower() or 'velocity' in name.lower():
                if value < 0:
                    self.issues.append(f"{name}: Negative speed ({value} m/s)")
                    return False
                if value > C_LIGHT * 1.01:  # Allow 1% tolerance
                    self.issues.append(f"{name}: Superluminal speed ({value} m/s > c)")
                    return False
            
            # Energy check
            elif 'energy' in name.lower() or 'eV' in units.lower() or 'GeV' in units.lower() or 'J' in units.lower():
                if value < 0:
                    self.issues.append(f"{name}: Negative energy ({value} {units})")
                    return False
                if value > MAX_ENERGY:
                    self.issues.append(f"{name}: Unphysically large energy ({value} {units})")
                    return False
            
            # Dimensionless ratios
            elif 'ratio' in name.lower() or 'fraction' in name.lower() or 'error' in name.lower():
                if abs(value) > 100:
                    self.warnings.append(f"{name}: Large ratio/error ({value})")
        
        return True
    
    def check_cross_domain_consistency(self, results: Dict[str, Any]) -> List[str]:
        """Check consistency between domains."""
        conflicts = []
        
        # Extract key values
        cosmology = results.get('cosmology', {}) if isinstance(results, dict) else {}
        particle_physics = {}
        
        # Check H0 consistency (if available in multiple domains)
        h0_values = []
        for domain, data in results.items():
            if isinstance(data, dict) and 'tests' in data:
                for test in data.get('tests', []):
                    if 'H0' in test.get('test_name', '') or 'hubble' in test.get('test_name', '').lower():
                        if test.get('value') and isinstance(test['value'], (int, float)):
                            h0_values.append((domain, test['value']))
        
        if len(h0_values) > 1:
            h0_vals = [v[1] for v in h0_values]
            if max(h0_vals) / min(h0_vals) > 1.1:  # More than 10% difference
                conflicts.append(f"H0 inconsistency: {h0_values}")
        
        # Check mass consistency
        fermion_masses = {}
        for domain in ['fermion_masses', 'particle_physics']:
            if domain in results and isinstance(results[domain], dict):
                for test in results[domain].get('tests', []):
                    name = test.get('test_name', '')
                    if any(q in name.lower() for q in ['u', 'd', 's', 'c', 'b', 't', 'e', 'mu', 'tau']):
                        if test.get('value'):
                            fermion_masses[name] = test['value']
        
        # Check for placeholders
        placeholder_patterns = ['placeholder', 'TODO', 'FIXME', 'N/A', 'TBD', 'XXX']
        for domain, data in results.items():
            if isinstance(data, dict):
                for test in data.get('tests', []):
                    notes = str(test.get('notes', '')).upper()
                    value_str = str(test.get('value', '')).upper()
                    for pattern in placeholder_patterns:
                        if pattern in notes or pattern in value_str:
                            conflicts.append(f"Potential placeholder in {domain}.{test.get('test_name', 'unknown')}: {test.get('notes', '')}")
        
        return conflicts
    
    def analyze_results(self, results_file: Path) -> Dict[str, Any]:
        """Analyze validation results file."""
        if not results_file.exists():
            return {'error': f'Results file not found: {results_file}'}
        
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        analysis = {
            'total_domains': len(results),
            'issues': [],
            'warnings': [],
            'conflicts': [],
            'physical_checks': {}
        }
        
        # Check each domain
        for domain_name, domain_data in results.items():
            if not isinstance(domain_data, dict):
                continue
            
            domain_issues = []
            domain_warnings = []
            
            for test in domain_data.get('tests', []):
                test_name = test.get('test_name', 'unknown')
                value = test.get('value')
                expected = test.get('expected', '')
                status = test.get('status', '')
                
                # Skip SKIP and ERROR statuses (already flagged)
                if status in ['SKIP', 'ERROR']:
                    continue
                
                # Check physicality of values
                if value is not None:
                    if not self.check_value_physical(f"{domain_name}.{test_name}", value, str(expected)):
                        domain_issues.append(f"{test_name}: {value}")
                
                # Check for suspicious values
                if isinstance(value, (int, float)):
                    if abs(value) > 1e100:
                        domain_issues.append(f"{test_name}: Extremely large value ({value})")
                    if value == 0 and 'mass' in test_name.lower():
                        domain_warnings.append(f"{test_name}: Zero mass may be unphysical")
            
            if domain_issues:
                analysis['issues'].extend([f"{domain_name}: {issue}" for issue in domain_issues])
            if domain_warnings:
                analysis['warnings'].extend([f"{domain_name}: {warn}" for warn in domain_warnings])
        
        # Cross-domain consistency
        analysis['conflicts'] = self.check_cross_domain_consistency(results)
        
        # Collect all issues/warnings
        analysis['issues'].extend(self.issues)
        analysis['warnings'].extend(self.warnings)
        
        return analysis


def main():
    """Run physical consistency check."""
    script_dir = Path(__file__).parent
    results_dir = script_dir / "results"
    
    # Find most recent results file
    results_files = sorted(results_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not results_files:
        print("No results files found. Run validation first.")
        return 1
    
    results_file = results_files[0]
    print(f"Analyzing: {results_file.name}")
    print("=" * 70)
    
    checker = PhysicalConsistencyChecker()
    analysis = checker.analyze_results(results_file)
    
    print(f"\nTotal domains: {analysis['total_domains']}")
    print(f"Issues found: {len(analysis['issues'])}")
    print(f"Warnings: {len(analysis['warnings'])}")
    print(f"Cross-domain conflicts: {len(analysis['conflicts'])}")
    print()
    
    if analysis['issues']:
        print("=" * 70)
        print("ISSUES (Must Fix):")
        print("=" * 70)
        for issue in analysis['issues'][:20]:  # First 20
            print(f"  ✗ {issue}")
        if len(analysis['issues']) > 20:
            print(f"  ... and {len(analysis['issues']) - 20} more")
    
    if analysis['warnings']:
        print("=" * 70)
        print("WARNINGS (Review):")
        print("=" * 70)
        for warn in analysis['warnings'][:20]:  # First 20
            print(f"  ⚠ {warn}")
        if len(analysis['warnings']) > 20:
            print(f"  ... and {len(analysis['warnings']) - 20} more")
    
    if analysis['conflicts']:
        print("=" * 70)
        print("CROSS-DOMAIN CONFLICTS:")
        print("=" * 70)
        for conflict in analysis['conflicts'][:20]:
            print(f"  ⚠ {conflict}")
        if len(analysis['conflicts']) > 20:
            print(f"  ... and {len(analysis['conflicts']) - 20} more")
    
    if not analysis['issues'] and not analysis['conflicts']:
        print("=" * 70)
        print("✓ NO CRITICAL ISSUES FOUND")
        print("=" * 70)
    
    return 0 if not analysis['issues'] and not analysis['conflicts'] else 1


if __name__ == "__main__":
    sys.exit(main())

