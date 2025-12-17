"""
Test Standards Compliance Module

Enforces meta-standards for all tests:
1. Single lock, no retuning
2. Frozen datasets (hashes recorded)
3. Blind thresholds (defined before results)
4. Trace completeness (equations, parameters, methods, seeds, timestamps, artifacts)
"""

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

# Try to get git commit hash


def get_git_commit_hash(repo_path: Path) -> Optional[str]:
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    return None


def compute_file_checksum(file_path: Path, algorithm: str = 'sha256') -> Optional[str]:
    """Compute checksum of a file."""
    try:
        if not file_path.exists():
            return None

        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception:
        return None


def get_python_version_info() -> Dict[str, str]:
    """Get Python version and key dependency versions."""
    info = {
        'python_version': sys.version.split()[0],
        'python_full': sys.version,
    }

    # Try to get key dependency versions
    for module_name in ['numpy', 'scipy', 'camb']:
        try:
            mod = __import__(module_name)
            if hasattr(mod, '__version__'):
                info[f'{module_name}_version'] = mod.__version__
        except ImportError:
            info[f'{module_name}_version'] = 'NOT_INSTALLED'

    return info


def get_machine_info() -> Dict[str, str]:
    """Get machine information."""
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'platform': platform.platform(),
        'processor': platform.processor(),
        'machine': platform.machine(),
        'python_arch': platform.architecture()[0],
    }


def compute_dataset_checksums(data_root: Path) -> Dict[str, Optional[str]]:
    """
    Compute checksums for key datasets.

    Returns dict mapping dataset name to checksum.
    """
    checksums = {}

    # Key datasets to checksum
    datasets = {
        'planck_2018': data_root / 'cosmology' / 'planck_2018.json',
        'sparc_catalog': data_root / 'sparc' / 'sparc_full_catalog.csv',
        'pantheon_plus': data_root / 'sne' / 'pantheon_plus' / 'Pantheon+SH0ES.dat',
        'desi_bao_mean': data_root / 'bao' / 'desi_dr1_all' / 'mean.txt',
        'desi_bao_cov': data_root / 'bao' / 'desi_dr1_all' / 'cov.txt',
        'pdg_masses': data_root / 'pdg' / 'pdg_masses_2024.json',
    }

    for name, path in datasets.items():
        checksums[name] = compute_file_checksum(
            path) if path.exists() else None

    return checksums


def get_dataset_versions() -> Dict[str, Dict[str, str]]:
    """
    Get exact dataset versions with full citations.

    Uses dataset_citations module for complete citation information.
    """
    try:
        from integrated_modules.dataset_citations import DATASET_CITATIONS

        result = {}
        for key, citation in DATASET_CITATIONS.items():
            result[key] = {
                'name': citation.name,
                'version': citation.version,
                'source': citation.source,
                'citation': citation.citation,
                'doi': citation.doi,
                'arxiv': citation.arxiv,
                'url': citation.url,
            }
        return result
    except ImportError:
        # Fallback if module not available
        return {
            'planck_2018': {
                'name': 'Planck 2018 TTTEEE+lowE',
                'version': '2018 TTTEEE+lowE',
                'source': 'Planck Collaboration',
                'citation': 'Planck Collaboration (2020), A&A 641, A6',
                'doi': '10.1051/0004-6361/201833910',
                'arxiv': '1807.06209',
                'url': 'https://www.cosmos.esa.int/web/planck/legacy-2018'
            },
            'sparc_catalog': {
                'name': 'SPARC Galaxy Rotation Curve Catalog',
                'version': 'v2.0',
                'source': 'Lelli et al.',
                'citation': 'Lelli et al. (2016), AJ 152, 157',
                'doi': '10.3847/0004-6256/152/6/157',
                'arxiv': '1606.09251',
                'url': 'https://www.astro.rug.nl/~sparc/'
            },
            'pantheon_plus': {
                'name': 'Pantheon+SH0ES',
                'version': 'Pantheon+SH0ES',
                'source': 'Scolnic et al.',
                'citation': 'Scolnic et al. (2022), ApJ 938, 113',
                'doi': '10.3847/1538-4357/ac8b7a',
                'arxiv': '2112.03863',
                'url': 'https://github.com/PantheonPlusSH0ES/DataRelease'
            },
            'desi_bao_mean': {
                'name': 'DESI DR1 BAO Measurements',
                'version': 'DR1',
                'source': 'DESI Collaboration',
                'citation': 'DESI Collaboration (2024), arXiv:2404.03002',
                'arxiv': '2404.03002',
                'url': 'https://data.desi.lbl.gov/public/edr/vac/edr/bao/'
            },
            'desi_bao_cov': {
                'name': 'DESI DR1 BAO Covariance Matrix',
                'version': 'DR1',
                'source': 'DESI Collaboration',
                'citation': 'DESI Collaboration (2024), arXiv:2404.03002',
                'arxiv': '2404.03002',
                'url': 'https://data.desi.lbl.gov/public/edr/vac/edr/bao/'
            },
            'pdg_masses': {
                'name': 'PDG 2024 Particle Masses',
                'version': '2024',
                'source': 'Particle Data Group',
                'citation': 'Workman et al. (2024), PTEP 2024, 083C01',
                'doi': '10.1093/ptep/ptac097',
                'url': 'https://pdg.lbl.gov/2024/'
            },
        }


def generate_run_manifest(
    repo_path: Path,
    lock_path: Path,
    data_root: Path,
    output_path: Path
) -> Dict[str, Any]:
    """
    Generate RUN_MANIFEST.md with all required metadata.

    Returns the manifest dict.
    """
    manifest = {
        'run_timestamp': datetime.now(timezone.utc).isoformat(),
        'run_timestamp_local': datetime.now().isoformat(),
    }

    # Commit hash (or deterministic fallback if repo is not a git checkout)
    commit_hash = get_git_commit_hash(repo_path)
    if commit_hash:
        manifest['git_commit_hash'] = commit_hash
    else:
        # Sandbox may be shipped without .git; record a deterministic code fingerprint
        # so runs remain reproducible and uniquely identifiable.
        runner_file = repo_path / "udof_runner" / "udof_validation_runner_v4.0.py"
        if not runner_file.exists():
            runner_file = repo_path / "udof_validation_runner_v4.0.py"
        runner_hash = compute_file_checksum(
            runner_file) if runner_file.exists() else None
        manifest['git_commit_hash'] = f"FILE_SHA256:{runner_hash}" if runner_hash else "NOT_AVAILABLE"

    # Master lock checksum
    lock_checksum = compute_file_checksum(lock_path)
    manifest['master_lock'] = {
        'filename': str(lock_path.name),
        'path': str(lock_path),
        'sha256': lock_checksum or 'NOT_FOUND',
    }

    # Dataset checksums with full citations
    dataset_checksums = compute_dataset_checksums(data_root)
    dataset_versions = get_dataset_versions()

    manifest['datasets'] = {}
    for name, checksum in dataset_checksums.items():
        dataset_info = dataset_versions.get(name, {})
        if dataset_info:
            manifest['datasets'][name] = {
                'name': dataset_info.get('name', name),
                'version': dataset_info.get('version', 'UNKNOWN'),
                'source': dataset_info.get('source', 'UNKNOWN'),
                'citation': dataset_info.get('citation', 'UNKNOWN'),
                'doi': dataset_info.get('doi'),
                'arxiv': dataset_info.get('arxiv'),
                'url': dataset_info.get('url'),
                'sha256': checksum or 'NOT_FOUND',
            }
        else:
            # Fallback for unknown datasets
            manifest['datasets'][name] = {
                'name': name,
                'version': 'UNKNOWN',
                'source': 'UNKNOWN',
                'citation': 'UNKNOWN',
                'sha256': checksum or 'NOT_FOUND',
            }

    # Python and dependency versions
    manifest['python'] = get_python_version_info()

    # Machine info
    manifest['machine'] = get_machine_info()

    # Write manifest to file
    manifest_md = f"""# RUN MANIFEST

**Generated**: {manifest['run_timestamp']}

## Repository

- **Commit Hash**: `{manifest['git_commit_hash']}`

## Master Lock

- **Filename**: `{manifest['master_lock']['filename']}`
- **Path**: `{manifest['master_lock']['path']}`
- **SHA256**: `{manifest['master_lock']['sha256']}`

## Datasets

"""

    for name, info in manifest['datasets'].items():
        manifest_md += f"- **{name}**: {info.get('name', name)}\n"
        manifest_md += f"  - **Version**: {info.get('version', 'UNKNOWN')}\n"
        manifest_md += f"  - **Source**: {info.get('source', 'UNKNOWN')}\n"
        manifest_md += f"  - **Citation**: {info.get('citation', 'UNKNOWN')}\n"
        if info.get('doi'):
            manifest_md += f"  - **DOI**: {info['doi']}\n"
        if info.get('arxiv'):
            manifest_md += f"  - **arXiv**: {info['arxiv']}\n"
        if info.get('url'):
            manifest_md += f"  - **URL**: {info['url']}\n"
        manifest_md += f"  - **SHA256**: `{info['sha256']}`\n"
        manifest_md += "\n"

    manifest_md += f"""
## Python Environment

- **Python Version**: {manifest['python']['python_version']}
- **NumPy**: {manifest['python'].get('numpy_version', 'UNKNOWN')}
- **SciPy**: {manifest['python'].get('scipy_version', 'UNKNOWN')}
- **CAMB**: {manifest['python'].get('camb_version', 'UNKNOWN')}

## Machine

- **OS**: {manifest['machine']['os']} {manifest['machine']['os_version']}
- **Platform**: {manifest['machine']['platform']}
- **Processor**: {manifest['machine']['processor']}
- **Architecture**: {manifest['machine']['python_arch']}

---

## JSON Manifest

```json
{json.dumps(manifest, indent=2)}
```
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(manifest_md)

    # Also save JSON version
    json_path = output_path.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    return manifest


class TestTrace:
    """Container for trace completeness information."""

    def __init__(
        self,
        test_id: str,
        equations: Optional[List[str]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        numerical_method: Optional[str] = None,
        runtime_seed: Optional[int] = None,
        timestamp: Optional[str] = None,
        datasets: Optional[List[str]] = None,  # Dataset keys used by this test
    ):
        self.test_id = test_id
        self.equations = equations or []
        self.parameters = parameters or {}
        self.numerical_method = numerical_method
        self.runtime_seed = runtime_seed
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.artifacts: List[Dict[str, str]] = []
        self.datasets = datasets or []  # List of dataset keys

    def add_artifact(self, artifact_type: str, file_path: Path, description: str = ""):
        """Add an output artifact."""
        self.artifacts.append({
            'type': artifact_type,
            'path': str(file_path),
            'description': description,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            'test_id': self.test_id,
            'equations': self.equations,
            'parameters': self.parameters,
            'numerical_method': self.numerical_method,
            'runtime_seed': self.runtime_seed,
            'timestamp': self.timestamp,
            'artifacts': self.artifacts,
        }
        if self.datasets:
            # Include dataset citations
            try:
                from integrated_modules.dataset_citations import DATASET_CITATIONS, format_dataset_citation
                result['datasets'] = [
                    {
                        'key': key,
                        'citation': format_dataset_citation(DATASET_CITATIONS[key])
                    }
                    for key in self.datasets if key in DATASET_CITATIONS
                ]
            except ImportError:
                result['datasets'] = [{'key': key} for key in self.datasets]
        return result


class BlindThreshold:
    """Container for blind threshold (defined before results)."""

    def __init__(
        self,
        test_id: str,
        observable: str,
        requirement: str,
        threshold_value: Optional[float] = None,
        threshold_type: str = 'absolute',  # 'absolute', 'relative', 'chi2'
    ):
        self.test_id = test_id
        self.observable = observable
        self.requirement = requirement
        self.threshold_value = threshold_value
        self.threshold_type = threshold_type
        self.defined_at = datetime.now(timezone.utc).isoformat()

    def check(self, result_value: Any) -> Tuple[bool, str]:
        """
        Check if result passes threshold.

        Returns (passed, status_message)
        """
        if self.threshold_value is None:
            return True, "NO_THRESHOLD"

        # Parse requirement string to determine comparison type
        req_str = str(self.requirement).strip()
        is_greater_than = '>' in req_str and '<' not in req_str.split('>')[0]
        is_less_than = '<' in req_str and '>' not in req_str.split('<')[0]
        is_range = '<' in req_str and '>' in req_str

        if self.threshold_type == 'absolute':
            if is_greater_than:
                # For "> threshold", check if result > threshold_value
                passed = float(result_value) > float(self.threshold_value)
            elif is_less_than or not (is_greater_than or is_range):
                # For "< threshold" or default, check if result < threshold_value
                passed = abs(float(result_value)) < float(self.threshold_value)
            elif is_range:
                # For ranges like "0.95 < R_X < 1.05", parse both bounds
                # This is handled by the test code itself, so default to less-than
                passed = abs(float(result_value)) < float(self.threshold_value)
            else:
                passed = abs(float(result_value)) < float(self.threshold_value)
        elif self.threshold_type == 'relative':
            passed = abs(float(result_value)) / \
                abs(float(self.threshold_value)) < 1.0
        elif self.threshold_type == 'chi2':
            passed = float(result_value) < float(self.threshold_value)
        elif self.threshold_type == 'boolean':
            # For boolean thresholds, check if result matches expected boolean value
            result_bool = bool(result_value)
            threshold_bool = bool(self.threshold_value)
            passed = result_bool == threshold_bool
        else:
            return False, f"UNKNOWN_THRESHOLD_TYPE: {self.threshold_type}"

        status = "PASS" if passed else "FAIL"
        return passed, status

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_id': self.test_id,
            'observable': self.observable,
            'requirement': self.requirement,
            'threshold_value': self.threshold_value,
            'threshold_type': self.threshold_type,
            'defined_at': self.defined_at,
        }


def generate_artifact_filename(
    test_id: str,
    dataset: str,
    lock_hash: str,
    timestamp: str,
    extension: str = 'json'
) -> str:
    """
    Generate artifact filename following convention:
    <test_id>_<dataset>_<lock_hash>_<timestamp>.<extension>
    """
    # Clean up timestamp for filename (remove colons, etc.)
    timestamp_clean = timestamp.replace(
        ':', '-').replace('T', '_').split('.')[0]
    lock_hash_short = lock_hash[:8] if lock_hash else 'NOHASH'

    return f"{test_id}_{dataset}_{lock_hash_short}_{timestamp_clean}.{extension}"


def validate_meta_standards(
    lock_path: Path,
    lock_checksum: str,
    dataset_checksums: Dict[str, Optional[str]],
    test_traces: List[TestTrace],
    blind_thresholds: List[BlindThreshold],
) -> Tuple[bool, List[str]]:
    """
    Validate that all meta-standards are met.

    Returns (all_passed, violations)
    """
    violations = []

    # 1. Single lock, no retuning
    if not lock_path.exists():
        violations.append(
            "META-STANDARD 1 VIOLATION: Master lock file not found")

    current_checksum = compute_file_checksum(lock_path)
    if current_checksum != lock_checksum:
        violations.append(
            "META-STANDARD 1 VIOLATION: Lock checksum changed (retuning detected)")

    # 2. Frozen datasets
    for name, expected_checksum in dataset_checksums.items():
        if expected_checksum is None:
            continue  # Dataset not found is OK (might be optional)
        # Note: We can't check if datasets changed during run, but we record checksums

    # 3. Blind thresholds
    for threshold in blind_thresholds:
        if threshold.threshold_value is None and 'qualitative' not in threshold.requirement.lower():
            violations.append(
                f"META-STANDARD 3 VIOLATION: Test {threshold.test_id} has no blind threshold")

    # 4. Trace completeness
    for trace in test_traces:
        if not trace.equations:
            violations.append(
                f"META-STANDARD 4 VIOLATION: Test {trace.test_id} missing equations")
        if not trace.parameters:
            violations.append(
                f"META-STANDARD 4 VIOLATION: Test {trace.test_id} missing parameters")
        if not trace.numerical_method:
            violations.append(
                f"META-STANDARD 4 VIOLATION: Test {trace.test_id} missing numerical method")
        if trace.runtime_seed is None and 'random' in str(trace.numerical_method).lower():
            violations.append(
                f"META-STANDARD 4 VIOLATION: Test {trace.test_id} uses random but no seed recorded")

    return len(violations) == 0, violations
