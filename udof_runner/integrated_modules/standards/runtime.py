"""
Runtime standards and manifest generation.

Provides manifest generation with deterministic hashing for reproducibility.
"""

import hashlib
import json
import sys
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional


def compute_file_hash(file_path: Path) -> str:
    """
    Compute SHA256 hash of a file.

    Args:
        file_path: Path to the file to hash

    Returns:
        SHA256 hash as hexadecimal string
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (IOError, OSError) as e:
        # Return empty hash if file cannot be read
        return ""


def hash_integrated_modules(integrated_modules_root: Path) -> Dict[str, str]:
    """
    Hash all Python files in integrated_modules directory.

    Args:
        integrated_modules_root: Root path to integrated_modules directory

    Returns:
        Dictionary mapping relative file paths to SHA256 hashes
    """
    module_hashes = {}

    if not integrated_modules_root.exists():
        return module_hashes

    # Find all .py files recursively under integrated_modules
    for py_file in integrated_modules_root.rglob("*.py"):
        # Get relative path from integrated_modules_root
        rel_path = py_file.relative_to(integrated_modules_root)
        rel_path_str = str(rel_path).replace(
            "\\", "/")  # Normalize to forward slashes

        file_hash = compute_file_hash(py_file)
        if file_hash:  # Only include if hash was successfully computed
            module_hashes[rel_path_str] = file_hash

    return module_hashes


def get_git_commit_hash(repo_path: Path) -> Optional[str]:
    """
    Get git commit hash if in a git repository.

    Args:
        repo_path: Path to check for git repository

    Returns:
        Commit hash string or None if not in git repo
    """
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


def get_python_version_info() -> Dict[str, str]:
    """
    Get Python version and platform information.

    Returns:
        Dictionary with Python version and platform details
    """
    return {
        "python_version": sys.version.split()[0],
        "python_full": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0]
    }


def get_dependency_versions() -> Dict[str, str]:
    """
    Get installed package versions.

    Returns:
        Dictionary mapping package names to versions
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format=json'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            packages = json.loads(result.stdout)
            return {pkg['name']: pkg['version'] for pkg in packages}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError, subprocess.SubprocessError):
        pass

    # Fallback: try reading requirements.txt
    deps = {}
    try:
        req_file = Path(__file__).parent.parent.parent / "requirements.txt"
        if req_file.exists():
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse "package==version" or "package>=version"
                        if '==' in line:
                            name, version = line.split('==', 1)
                            deps[name.strip()] = version.strip()
                        elif '>=' in line:
                            name = line.split('>=')[0].strip()
                            deps[name] = "unknown"
    except Exception:
        pass

    return deps


def compute_dataset_checksums(data_root: Path) -> Dict[str, Any]:
    """
    Compute checksums for key dataset files.

    Args:
        data_root: Root path to data directory

    Returns:
        Dictionary with dataset checksums and metadata
    """
    datasets = {}

    # BAO data - try DESI DR1 first
    bao_dir = data_root / "bao" / "desi_dr1_all"
    if not bao_dir.exists():
        # Fallback to other BAO locations
        bao_dir = data_root / "bao"
    if bao_dir.exists():
        bao_files = {}
        for file in ["mean.txt", "cov.txt"]:
            file_path = bao_dir / file
            if file_path.exists():
                bao_files[file] = {
                    "sha256": compute_file_hash(file_path),
                    "size_bytes": file_path.stat().st_size
                }
        if bao_files:
            datasets["bao"] = {
                "dataset": "DESI DR1 BAO",
                "path": str(bao_dir),
                "files": bao_files,
                "version": "DESI DR1",
                "citation": "DESI Collaboration (2024), arXiv:2404.03002"
            }

    # SNe data (Pantheon+)
    sne_file = data_root / "sne" / "pantheon_plus" / "Pantheon+SH0ES.dat"
    if sne_file.exists():
        datasets["sne"] = {
            "dataset": "Pantheon+SH0ES",
            "path": str(sne_file),
            "sha256": compute_file_hash(sne_file),
            "size_bytes": sne_file.stat().st_size,
            "version": "Pantheon+SH0ES",
            "citation": "Scolnic et al. (2022), ApJ 938, 113, arXiv:2112.03863"
        }

    # SPARC catalog
    sparc_file = data_root / "sparc" / "sparc_full_catalog.csv"
    if sparc_file.exists():
        datasets["sparc"] = {
            "dataset": "SPARC",
            "path": str(sparc_file),
            "sha256": compute_file_hash(sparc_file),
            "size_bytes": sparc_file.stat().st_size,
            "version": "SPARC v2.0",
            "citation": "Lelli et al. (2016), AJ 152, 157, arXiv:1606.09251"
        }

    # PDG masses
    pdg_file = data_root / "pdg" / "pdg_masses_2024.json"
    if pdg_file.exists():
        datasets["pdg"] = {
            "dataset": "PDG 2024",
            "path": str(pdg_file),
            "sha256": compute_file_hash(pdg_file),
            "size_bytes": pdg_file.stat().st_size,
            "version": "PDG 2024",
            "citation": "Workman et al. (2024), PTEP 2024, 083C01"
        }

    return datasets


def generate_run_manifest(
    runner_file_path: Path,
    integrated_modules_root: Path,
    run_id: str,
    locks: Dict[str, Any],
    domains: List[str],
    output_dir: Path = None,
    master_lock_path: Optional[Path] = None,
    data_root: Optional[Path] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a run manifest with deterministic hashing for reproducibility.

    Includes SHA256 hashes of:
    - The runner file
    - All integrated_modules/**/*.py files
    - Master lock file
    - Dataset files (BAO, SNe, SPARC, etc.)

    Also includes:
    - Python version and platform info
    - Dependency versions
    - Git commit hash (if available)

    Args:
        runner_file_path: Path to the validation runner script
        integrated_modules_root: Root path to integrated_modules directory
        run_id: Unique identifier for this run
        locks: UDOF locks dictionary
        domains: List of domains that were executed
        output_dir: Optional output directory path
        master_lock_path: Path to master lock file (for checksum)
        data_root: Root path to data directory (for dataset checksums)
        **kwargs: Additional metadata to include in manifest

    Returns:
        Dictionary containing the complete manifest
    """
    timestamp = datetime.now(timezone.utc).isoformat()

    # Hash the runner file
    runner_hash = compute_file_hash(runner_file_path)
    runner_path_str = str(runner_file_path.name)  # Just the filename

    # Hash all integrated_modules Python files
    module_hashes = hash_integrated_modules(integrated_modules_root)

    # Master lock checksum
    master_lock_info = {}
    if master_lock_path and master_lock_path.exists():
        master_lock_info = {
            "filename": master_lock_path.name,
            "path": str(master_lock_path),
            "sha256": compute_file_hash(master_lock_path)
        }

    # Dataset checksums
    dataset_info = {}
    if data_root:
        dataset_info = compute_dataset_checksums(data_root)

    # Python and platform info
    python_info = get_python_version_info()
    dependency_versions = get_dependency_versions()

    # Git commit hash (if in git repo)
    repo_path = runner_file_path.parent
    git_commit_hash = get_git_commit_hash(repo_path)

    # Build manifest
    manifest = {
        "run_id": run_id,
        "timestamp": timestamp,
        "runner": {
            "file": runner_path_str,
            "sha256": runner_hash,
            "path": str(runner_file_path)
        },
        "integrated_modules": {
            "root": str(integrated_modules_root),
            "file_count": len(module_hashes),
            "hashes": module_hashes
        },
        "udof_version": locks.get("version", "unknown"),
        "domains_executed": domains,
        "domain_count": len(domains),
        "master_lock": master_lock_info,
        "datasets": dataset_info,
        "environment": {
            **python_info,
            "dependencies": dependency_versions
        },
        **kwargs
    }

    # Add git commit hash if available
    if git_commit_hash:
        manifest["git_commit_hash"] = git_commit_hash

    # If output directory is provided, write manifest to file
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "RUN_MANIFEST.json"

        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
        except (IOError, OSError) as e:
            # Don't fail if we can't write, but log it somehow
            pass

    return manifest
