#!/usr/bin/env python3
"""
================================================================================
UDOF UNIVERSAL VALIDATION RUNNER v4.0
================================================================================

Thin runner: CLI + orchestration layer only.
- Domain dispatch via DOMAIN_REGISTRY
- Output directory creation
- Manifest generation with hashing
- Summary table generation
- Standards enforcement

All domain logic lives in integrated_modules/domains/
All physics formulas live in integrated_modules/core/
All data loading lives in integrated_modules/data/

VERSION: 4.0.0
DATE: 2025-12-XX

ARCHITECTURE:
- Runner: CLI + orchestration only
- Domain modules: integrated_modules/domains/<domain>.py
- Core physics: integrated_modules/core/
- Data layer: integrated_modules/data/
- Standards: integrated_modules/standards/

================================================================================
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
import numpy as np
import importlib.util

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import modular components
from integrated_modules.core.formulas import UDOFFormulas
from integrated_modules.data.loaders import DataLoader
from integrated_modules.domains import DOMAIN_REGISTRY
from integrated_modules.domains.context import DomainContext
from integrated_modules.types import DomainResult, TestResult
from integrated_modules.standards.runtime import generate_run_manifest

# ============================================================================
# PATHS
# ============================================================================

SCRIPT_DIR = Path(__file__).parent
# PROJECT_ROOT not used for data/locks - everything must come from SANDBOX

# SANDBOX DIRECTORY - All locks and data MUST be self-contained here
# Uses the directory containing this script as the sandbox root
SANDBOX_ROOT = Path(__file__).parent.resolve()

# Verify sandbox directory exists
if not SANDBOX_ROOT.exists():
    raise FileNotFoundError(
        f"Sandbox directory not found: {SANDBOX_ROOT}\n"
        "All locks and data must be self-contained in the sandbox directory."
    )

# Lock files - ALL FROM SANDBOX DIRECTORY ONLY
MASTER_LOCK_PATH = SANDBOX_ROOT / "data" / \
    "locks" / "udof_MASTER_LOCK_v3_SPARC.json"
LOCKS_PATH = SANDBOX_ROOT / "data" / "locks" / \
    "udof_unified_x_locks_v2.3.8_FINAL_HYBRID.json"
# Dark sector locks (MCMC-validated) - from sandbox only
DARK_SECTOR_LOCKS_PATH = SANDBOX_ROOT / "data" / \
    "locks" / "dark_sector_locks_entropy_v1.json"

# Data root: SANDBOX ONLY - all data must be self-contained
DATA_ROOT = SANDBOX_ROOT / "data"

# ============================================================================
# LOAD LOCKS
# ============================================================================

DEFAULT_LOCKS = {
    "version": "4.0.0_mcmc_validated",
    "fermion_masses": {
        "geometry_eigenvalues": {
            "g": [1.469331, 1.750000, 1.594506],
            "sigma": [0.118172, 1.651012, 3.416979]
        },
        "lambda_0": 0.5931386921464596,
        "beta_ql": 1.6214006567601995,
        "hierarchy_parameters": {
            "a_u": -0.6825280277986697,
            "b_u": 3.456207839323256,
            "a_d": 2.076995670202104,
            "b_d": 1.9735669287176074,
            "a_e": 1.2580627785433611,
            "b_e": 3.1292659928542936,
            "c_tau": 2.325920549818307
        },
        "neutrino_v8_mixing_parameters": {
            "epsilon_comm": -2.000082277364097,
            "epsilon_diff": -0.9576239196736189,
            "Delta_a": 0.46774550986231506,
            "Delta_b": 5.641001373829542
        },
        "neutrino_v8_mass_parameters": {
            "a_nu": 1.0249,
            "b_nu": 0.7644,
            "S_nu": 9.475e-13
        },
        "neutrino_v9_mass_parameters": {
            "a_nu": -1.1757944741134752,
            "b_nu": 1.3497396966701392,
            "S_nu": 5.935237314215294e-14
        },
        # NOTE: CKM parameters need optimization for exact matches
        # Sandbox achieved perfect CKM matches (13.04°, 2.38°, 0.201°)
        # These defaults will need to be optimized separately
        "ckm_mixing_parameters": {
            "epsilon_comm": -13.407168247988992,
            "epsilon_diff": -2.1395858079636887,
            "Delta_a": -26.16069197838864,
            "Delta_b": 10.162448648190658,
            "note": "Default values - requires optimization for exact CKM matches like sandbox"
        }
    },
    "ese_map": {
        "ell_IR": 4.7e-5,
        "ell_star": 2e-15
    },
    "calibrated_locks": {
        "eta_star": 0.171,
        "X0": 0.6481
    },
    "pivots": {
        "Sigma0_kg_m2": 1.0
    },
    "cosmology": {
        "H0": 70.21,  # MCMC-validated
        "Om": 0.3185,  # MCMC-validated
        "r_d_Mpc": 147.09
    },
    "dark_sector": {
        "Omega_geom_0": 0.3266,  # MCMC-validated
        "alpha_geom": -0.1885,
        "p_op": 0.7577,
        "eta_entropy": 0.0
    },
    "strong_field": {
        "K_ref": 1e10,
        "zeta": 2.0
    }
}


def convert_master_lock_to_unified(master_lock: Dict, unified_template: Dict) -> Dict:
    """
    Convert master lock format to unified format expected by formulas.

    Master lock structure:
    - fermions_tsi.params: hierarchy parameters
    - neutrinos_tsi.params: neutrino parameters
    - cosmology: cosmology parameters
    - dark_sector.ese: ESE parameters

    Unified format expected:
    - fermion_masses.hierarchy_parameters
    - fermion_masses.geometry_eigenvalues
    - fermion_masses.lambda_0, beta_ql
    - cosmology: H0, Om, r_d_Mpc
    - ese_map: ell_IR, ell_star
    - calibrated_locks: eta_star, X0
    """
    unified = unified_template.copy()

    # Extract fermion parameters from master lock
    if 'fermions_tsi' in master_lock and 'params' in master_lock['fermions_tsi']:
        params = master_lock['fermions_tsi']['params']

        # Hierarchy parameters
        if 'fermion_masses' not in unified:
            unified['fermion_masses'] = {}
        if 'hierarchy_parameters' not in unified['fermion_masses']:
            unified['fermion_masses']['hierarchy_parameters'] = {}

        unified['fermion_masses']['hierarchy_parameters'].update({
            'a_u': params.get('a_u', 0.228),
            'b_u': params.get('b_u', 3.574),
            'a_d': params.get('a_d', 3.063),
            'b_d': params.get('b_d', 1.967),
            'a_e': params.get('a_e', 2.825),
            'b_e': params.get('b_e', 2.065),
            'c_tau': params.get('c_tau', 0.761)
        })

        # lambda_0 and beta_ql
        unified['fermion_masses']['lambda_0'] = params.get('lambda_0', 0.5931)
        unified['fermion_masses']['beta_ql'] = params.get('beta_ql', 1.6214)

    # Extract neutrino parameters
    if 'neutrinos_tsi' in master_lock and 'params' in master_lock['neutrinos_tsi']:
        nu_params = master_lock['neutrinos_tsi']['params']

        if 'fermion_masses' not in unified:
            unified['fermion_masses'] = {}
        if 'neutrino_v8_mass_parameters' not in unified['fermion_masses']:
            unified['fermion_masses']['neutrino_v8_mass_parameters'] = {}

        unified['fermion_masses']['neutrino_v8_mass_parameters'].update({
            'a_nu': nu_params.get('a_nu', 1.0249),
            'b_nu': nu_params.get('b_nu', 0.7644),
            'S_nu': nu_params.get('S_nu', 9.475e-13) if 'S_nu' in nu_params else
            10**(nu_params.get('log10_kappa', -11.95)
                 ) if 'log10_kappa' in nu_params else 9.475e-13
        })

        # PMNS mixing parameters (if available)
        if 'theta12_input_deg' in nu_params:
            if 'neutrino_v8_mixing_parameters' not in unified['fermion_masses']:
                unified['fermion_masses']['neutrino_v8_mixing_parameters'] = {
                    'epsilon_comm': -2.000082277364097,
                    'epsilon_diff': -0.9576239196736189,
                    'Delta_a': 0.46774550986231506,
                    'Delta_b': 5.641001373829542
                }

    # Extract cosmology parameters
    if 'cosmology' in master_lock:
        cosmo = master_lock['cosmology']
        if 'cosmology' not in unified:
            unified['cosmology'] = {}
        unified['cosmology']['H0'] = cosmo.get('H0_km_per_s_Mpc', 70.21)
        unified['cosmology']['Om'] = cosmo.get('Omega_m0', 0.3185)
        unified['cosmology']['r_d_Mpc'] = master_lock.get('rd_Mpc', 147.09)

    # Extract ESE parameters
    if 'dark_sector' in master_lock and 'ese' in master_lock['dark_sector']:
        ese = master_lock['dark_sector']['ese']
        if 'ese_map' not in unified:
            unified['ese_map'] = {}
        unified['ese_map']['ell_IR'] = 4.7e-5  # Standard value
        unified['ese_map']['ell_star'] = 2e-15  # Standard value
        unified['ese_map']['k'] = ese.get('k', 1.5)  # ESE logistic parameter

        # Calibrated locks (X0 from ESE)
        if 'calibrated_locks' not in unified:
            unified['calibrated_locks'] = {}
        unified['calibrated_locks']['X0'] = ese.get('X0', 0.6481)
        # eta_star might be in dark_sector or use default
        if 'udof_entropy' in master_lock.get('dark_sector', {}):
            # Could extract from entropy params if needed
            pass
        unified['calibrated_locks']['eta_star'] = 0.171  # Default

    # Geometry eigenvalues from SANDBOX master lock file - fully self-contained!
    # The master lock file already contains geometry_eigenvalues in fermion_masses section
    if 'fermion_masses' not in unified:
        unified['fermion_masses'] = {}

    # Extract geometry eigenvalues from master lock file (SANDBOX - fully self-contained)
    if 'fermion_masses' in master_lock and 'geometry_eigenvalues' in master_lock['fermion_masses']:
        unified['fermion_masses']['geometry_eigenvalues'] = master_lock['fermion_masses']['geometry_eigenvalues']

    # Fallback: Get geometry eigenvalues from sandbox unified lock file if not in master lock
    if 'geometry_eigenvalues' not in unified.get('fermion_masses', {}):
        if LOCKS_PATH.exists():
            with open(LOCKS_PATH, 'r') as f:
                unified_locks = json.load(f)
                if 'fermion_masses' in unified_locks and 'geometry_eigenvalues' in unified_locks['fermion_masses']:
                    unified['fermion_masses']['geometry_eigenvalues'] = unified_locks['fermion_masses']['geometry_eigenvalues']

    # NOTE: CKM parameters are not in master lock file format
    # The sandbox achieved perfect CKM matches, suggesting optimized parameters exist
    # For now, use defaults (will need optimization to match sandbox exact results)
    # TODO: Extract or optimize CKM parameters to match sandbox perfect matches
    if 'fermion_masses' in unified and 'ckm_mixing_parameters' not in unified['fermion_masses']:
        unified['fermion_masses']['ckm_mixing_parameters'] = {
            'epsilon_comm': -13.407,
            'epsilon_diff': -2.140,
            'Delta_a': -26.161,
            'Delta_b': 10.162,
            'note': 'Default values - need optimization for exact CKM matches'
        }

    return unified


def load_locks() -> Dict:
    """Load locks from file or use defaults.

    Priority:
    1. Master lock file (if exists) - converted to unified format
    2. Unified lock file (if exists)
    3. Default locks
    """
    locks = DEFAULT_LOCKS.copy()

    # Load master lock file from SANDBOX ONLY (no fallback to prime0)
    if MASTER_LOCK_PATH.exists():
        with open(MASTER_LOCK_PATH, 'r') as f:
            master_lock = json.load(f)

            # Master lock already has the correct structure - use it directly
            # COMPLETELY REPLACE (not merge) to ensure master lock values override defaults
            if 'fermion_masses' in master_lock:
                # Deep copy to avoid reference issues
                locks['fermion_masses'] = master_lock['fermion_masses'].copy()
            if 'cosmology' in master_lock:
                # Convert cosmology keys to expected format (H0_km_per_s_Mpc -> H0, Omega_m0 -> Om)
                cosmo_master = master_lock['cosmology'].copy()
                cosmo_unified = {}
                cosmo_unified['H0'] = cosmo_master.get(
                    'H0_km_per_s_Mpc', cosmo_master.get('H0', 70.21))
                cosmo_unified['Om'] = cosmo_master.get(
                    'Omega_m0', cosmo_master.get('Om', 0.3185))
                cosmo_unified['r_d_Mpc'] = master_lock.get(
                    'rd_Mpc', cosmo_master.get('r_d_Mpc', 147.09))
                locks['cosmology'] = cosmo_unified
            if 'ese_map' in master_lock:
                locks['ese_map'] = master_lock['ese_map'].copy()
            if 'calibrated_locks' in master_lock:
                locks['calibrated_locks'] = master_lock['calibrated_locks'].copy()
            if 'pivots' in master_lock:
                locks['pivots'] = master_lock['pivots'].copy()
            if 'dark_sector' in master_lock:
                locks['dark_sector'] = master_lock['dark_sector'].copy()
    elif LOCKS_PATH.exists():
        # Use unified lock file from sandbox if master lock not available
        with open(LOCKS_PATH, 'r') as f:
            file_locks = json.load(f)
            # Merge file locks into defaults
            locks.update(file_locks)
    else:
        # NO FALLBACK - all locks must be in sandbox directory
        raise FileNotFoundError(
            f"Neither master lock nor unified lock found in sandbox directory: {SANDBOX_ROOT / 'data' / 'locks'}\n"
            "All lock files must be self-contained in the sandbox directory."
        )

    # Load dark sector locks from SANDBOX ONLY (MCMC-validated)
    # Note: This is optional - if it doesn't exist in sandbox, we continue without it
    if DARK_SECTOR_LOCKS_PATH.exists():
        with open(DARK_SECTOR_LOCKS_PATH, 'r') as f:
            dark_locks = json.load(f)
            # Extract dark sector params
            if 'params' in dark_locks:
                locks.setdefault('dark_sector', {}).update(
                    dark_locks['params'])
            if 'metadata' in dark_locks and 'H0' in dark_locks['metadata']:
                locks.setdefault('cosmology', {})[
                    'H0'] = dark_locks['metadata']['H0']

    return locks

# ============================================================================
# DOMAIN REGISTRY
# ============================================================================


AVAILABLE_DOMAINS = list(DOMAIN_REGISTRY.keys())

# ============================================================================
# RUNNER
# ============================================================================


class UDOFValidationRunner:
    """
    Thin runner: CLI + orchestration layer only.

    Responsibilities:
    - Load locks and create shared resources (formulas, data_loader)
    - Create output directories
    - Dispatch to domain modules via DOMAIN_REGISTRY
    - Aggregate results
    - Generate manifest with hashing
    - Generate summary tables
    """

    def __init__(self,
                 quiet: bool = False,
                 cosmology_method: str = 'proper',
                 use_rx: bool = True,
                 sparc_formula: str = 'separated',
                 sparc_b_prediction: bool = False,
                 output_dir: Path = None):
        self.locks = load_locks()
        self.quiet = quiet
        self.cosmology_method = cosmology_method
        self.use_rx = use_rx
        self.sparc_formula = sparc_formula
        self.sparc_b_prediction = sparc_b_prediction

        # Create shared resources
        self.formulas = UDOFFormulas(self.locks)
        self.data_loader = DataLoader(DATA_ROOT)

        # Output directory (will be set per run)
        self.output_dir = output_dir

    def log(self, msg: str):
        """Log message if not quiet."""
        if not self.quiet:
            print(msg)

    def create_domain_context(self) -> DomainContext:
        """Create DomainContext for domain modules."""
        return DomainContext(
            locks=self.locks,
            data_root=DATA_ROOT,
            formulas=self.formulas,
            data_loader=self.data_loader,
            cosmology_method=self.cosmology_method,
            use_rx=self.use_rx,
            sparc_formula=self.sparc_formula,
            sparc_b_prediction=self.sparc_b_prediction
        )

    def run_domain(self, domain: str, ctx: DomainContext,
                   output_dirs: Dict[str, Path] = None) -> DomainResult:
        """
        Run a single domain via registry.

        Args:
            domain: Domain name
            ctx: DomainContext for the domain
            output_dirs: Optional dict mapping domain names to output directories

        Returns:
            DomainResult from the domain module
        """
        if domain not in DOMAIN_REGISTRY:
            result = DomainResult(domain_name=domain)
            result.n_error = 1
            result.tests.append(TestResult(
                test_name="domain_not_found",
                status="ERROR",
                value=None,
                notes=f"Domain '{domain}' not found in registry"
            ))
            return result

        try:
            # Call domain module via registry
            return DOMAIN_REGISTRY[domain](ctx)
        except Exception as e:
            result = DomainResult(domain_name=domain)
            result.n_error = 1
            result.tests.append(TestResult(
                test_name="error",
                status="ERROR",
                value=None,
                notes=str(e)
            ))
            return result

    def create_output_directories(self, run_id: str, domains: List[str]) -> Dict[str, Path]:
        """
        Create output directory structure for specified domains.

        Args:
            run_id: Run identifier
            domains: List of domains to create directories for

        Returns:
            Dict mapping domain names to their output directories
        """
        base_output = self.output_dir or (SCRIPT_DIR / "run_results" / run_id)
        base_output.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each domain that will be run
        output_dirs = {}
        for domain in domains:
            domain_dir = base_output / domain
            domain_dir.mkdir(parents=True, exist_ok=True)
            output_dirs[domain] = domain_dir

        return output_dirs

    def save_domain_results(self, domain: str, result: DomainResult,
                            output_dir: Path):
        """Save domain results to JSON file."""
        result_file = output_dir / f"{domain}_results.json"
        result_dict = {
            "domain_name": result.domain_name,
            "n_pass": result.n_pass,
            "n_fail": result.n_fail,
            "n_error": result.n_error,
            "n_skip": result.n_skip,
            "n_theoretical": result.n_theoretical,
            "chi2_total": result.chi2_total,
            "tests": [
                {
                    "test_name": t.test_name,
                    "status": t.status,
                    "value": t.value,
                    "expected": t.expected,
                    "error": t.error,
                    "chi2": t.chi2,
                    "notes": t.notes
                }
                for t in result.tests
            ]
        }

        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2,
                      ensure_ascii=False, default=str)

    def generate_summary_table(self, results: Dict[str, DomainResult],
                               output_dir: Path):
        """Generate SUMMARY_TABLE.md with all domain results."""
        summary_file = output_dir / "SUMMARY_TABLE.md"

        lines = [
            "# UDOF Validation Summary",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
            "| Domain | Status | Pass | Fail | Error | Skip | Theoretical |",
            "|--------|--------|------|------|-------|------|-------------|"
        ]

        for domain in sorted(results.keys()):
            result = results[domain]
            n_total = (result.n_pass + result.n_fail + result.n_error +
                       result.n_skip + result.n_theoretical)

            if result.n_fail == 0 and result.n_error == 0:
                status = "PASS" if result.n_theoretical == 0 else "THEORETICAL"
            else:
                status = "FAIL"

            lines.append(
                f"| {domain} | {status} | {result.n_pass} | {result.n_fail} | "
                f"{result.n_error} | {result.n_skip} | {result.n_theoretical} |"
            )

        # Add totals
        total_pass = sum(r.n_pass for r in results.values())
        total_fail = sum(r.n_fail for r in results.values())
        total_error = sum(r.n_error for r in results.values())
        total_skip = sum(r.n_skip for r in results.values())
        total_theoretical = sum(r.n_theoretical for r in results.values())
        total_tests = total_pass + total_fail + \
            total_error + total_skip + total_theoretical

        lines.extend([
            "",
            "## Totals",
            f"- Total Tests: {total_tests}",
            f"- Passed: {total_pass}",
            f"- Failed: {total_fail}",
            f"- Errors: {total_error}",
            f"- Skipped: {total_skip}",
            f"- Theoretical: {total_theoretical}"
        ])

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def save_results_json(self, results: Dict[str, DomainResult],
                          run_id: str, output_dir: Path):
        """Save aggregated results to logs/RESULTS.json."""
        logs_dir = output_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        results_file = logs_dir / "RESULTS.json"

        results_dict = {
            "run_id": run_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domains": {}
        }

        for domain, result in results.items():
            results_dict["domains"][domain] = {
                "domain_name": result.domain_name,
                "n_pass": result.n_pass,
                "n_fail": result.n_fail,
                "n_error": result.n_error,
                "n_skip": result.n_skip,
                "n_theoretical": result.n_theoretical,
                "chi2_total": result.chi2_total,
                "tests": [
                    {
                        "test_name": t.test_name,
                        "status": t.status,
                        "value": t.value,
                        "expected": t.expected,
                        "error": t.error,
                        "chi2": t.chi2,
                        "notes": t.notes
                    }
                    for t in result.tests
                ]
            }

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2,
                      ensure_ascii=False, default=str)

    def run_validation(self, domains: List[str] = None) -> Dict:
        """
        Run validation for specified domains (or all if None).

        Returns:
            Dict with run_id, totals, and manifest
        """
        domains = domains or AVAILABLE_DOMAINS
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_id = f"udof_v4.0_{timestamp}"

        self.log("=" * 70)
        self.log("UDOF UNIVERSAL VALIDATION RUNNER v4.0")
        self.log("Thin Runner - Modular Architecture")
        self.log("=" * 70)
        self.log(f"Run ID: {run_id}")
        self.log(f"Version: {self.locks['version']}")
        self.log(f"Domains: {len(domains)}")
        self.log("=" * 70)
        self.log("")

        # Create output directories
        output_dirs = self.create_output_directories(run_id, domains)
        base_output = output_dirs[domains[0]].parent if domains else (
            self.output_dir or (SCRIPT_DIR / "run_results" / run_id))

        # Create domain context (shared across all domains)
        ctx = self.create_domain_context()

        # Run domains
        results = {}
        total_pass = total_fail = total_error = total_skip = total_theoretical = 0

        for domain in domains:
            self.log(f"[{domain.upper()}]")
            self.log("-" * 50)

            result = self.run_domain(domain, ctx, output_dirs)
            results[domain] = result

            # Save domain results
            if domain in output_dirs:
                self.save_domain_results(domain, result, output_dirs[domain])

            # Log test results
            for test in result.tests:
                status = f"[{test.status}]"
                if isinstance(test.value, float):
                    val = f"{test.value:.6g}"
                elif isinstance(test.value, (list, np.ndarray)):
                    val = "[...]"
                else:
                    val = str(test.value)[:40] if test.value else "N/A"
                self.log(f"  {test.test_name:30s} {status:12s} = {val}")

            n = (result.n_pass + result.n_fail + result.n_error +
                 result.n_skip + result.n_theoretical)
            self.log(
                f"  Subtotal: {result.n_pass}/{n} (theoretical: {result.n_theoretical})")
            self.log("")

            total_pass += result.n_pass
            total_fail += result.n_fail
            total_error += result.n_error
            total_skip += result.n_skip
            total_theoretical += result.n_theoretical

        # Summary
        self.log("=" * 70)
        self.log("VALIDATION SUMMARY")
        self.log("=" * 70)

        for domain, result in results.items():
            n = (result.n_pass + result.n_fail + result.n_error +
                 result.n_skip + result.n_theoretical)
            if result.n_fail == 0 and result.n_error == 0:
                status = "[PASS]" if result.n_theoretical == 0 else "[THEORETICAL]"
            else:
                status = "[FAIL]"
            self.log(f"  {domain:25s} {status:14s} ({result.n_pass}/{n})")

        total_tests = total_pass + total_fail + \
            total_error + total_skip + total_theoretical
        self.log("-" * 50)
        self.log(
            f"TOTAL: {total_pass}/{total_tests} passed, {total_fail} failed, "
            f"{total_error} errors, {total_theoretical} theoretical")
        self.log("=" * 70)

        # Generate manifest with hashing for reproducibility
        runner_file = Path(__file__)
        integrated_modules_root = SCRIPT_DIR / "integrated_modules"

        manifest = generate_run_manifest(
            runner_file_path=runner_file,
            integrated_modules_root=integrated_modules_root,
            run_id=run_id,
            locks=self.locks,
            domains=domains,
            output_dir=base_output,
            master_lock_path=MASTER_LOCK_PATH,
            data_root=DATA_ROOT,
            total_pass=total_pass,
            total_tests=total_tests,
            total_fail=total_fail,
            total_error=total_error,
            total_skip=total_skip,
            total_theoretical=total_theoretical,
            cosmology_method=self.cosmology_method,
            use_rx=self.use_rx,
            sparc_formula=self.sparc_formula,
            sparc_b_prediction=self.sparc_b_prediction
        )

        # Generate summary table
        self.generate_summary_table(results, base_output)

        # Generate EQUATIONS_USED.md
        from integrated_modules.standards.equations_generator import generate_equations_used_md
        equations_path = base_output / "EQUATIONS_USED.md"
        generate_equations_used_md(results, equations_path)

        # Save aggregated results JSON
        self.save_results_json(results, run_id, base_output)

        return {
            'run_id': run_id,
            'total_pass': total_pass,
            'total_tests': total_tests,
            'total_fail': total_fail,
            'total_error': total_error,
            'total_skip': total_skip,
            'total_theoretical': total_theoretical,
            'manifest': manifest
        }


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="UDOF Validation Runner v4.0 - Modular Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python udof_validation_runner_v4.0.py

  # Run specific domains
  python udof_validation_runner_v4.0.py --domain fermion_masses sparc

  # Use simple cosmology (fallback)
  python udof_validation_runner_v4.0.py --cosmology-method simple

  # Disable R_X response
  python udof_validation_runner_v4.0.py --no-rx

  # Use standard SPARC formula
  python udof_validation_runner_v4.0.py --sparc-formula standard

  # List available domains
  python udof_validation_runner_v4.0.py --list-domains
        """)
    parser.add_argument('--domain', '-d', nargs='+',
                        help='Domain(s) to test (default: all)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress progress output')
    parser.add_argument('--list-domains', action='store_true',
                        help='List available domains and exit')
    parser.add_argument('--version', '-v', action='store_true',
                        help='Show version and exit')
    parser.add_argument('--cosmology-method', choices=['simple', 'proper'],
                        default='proper',
                        help='Cosmology method: simple (ΛCDM) or proper (ProperCorrectedGrowth)')
    parser.add_argument('--no-rx', action='store_true',
                        help='Disable R_X response (use standard ESE only)')
    parser.add_argument('--sparc-formula', choices=['standard', 'separated'],
                        default='separated',
                        help='SPARC formula: standard or separated (v4.0 default)')
    parser.add_argument('--sparc-b-prediction', action='store_true',
                        help='Use multivariate B prediction for SPARC (0-param model)')
    parser.add_argument('--output-dir', type=Path,
                        help='Output directory (default: run_results/<run_id>)')

    args = parser.parse_args()

    if args.version:
        locks = load_locks()
        print(f"UDOF Validation Runner v4.0")
        print(f"UDOF Version: {locks.get('version', 'unknown')}")
        return

    if args.list_domains:
        print("Available domains:")
        for domain in sorted(AVAILABLE_DOMAINS):
            print(f"  - {domain}")
        return

    runner = UDOFValidationRunner(
        quiet=args.quiet,
        cosmology_method=args.cosmology_method,
        use_rx=not args.no_rx,
        sparc_formula=args.sparc_formula,
        sparc_b_prediction=args.sparc_b_prediction,
        output_dir=args.output_dir
    )

    domains = args.domain if args.domain else None
    runner.run_validation(domains=domains)


if __name__ == '__main__':
    main()
