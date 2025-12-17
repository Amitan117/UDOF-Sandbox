# UDOF Universal Validation Runner v4.0

**Self-contained validation suite for the complete UDOF model**

This validation suite provides comprehensive testing of the UDOF (Universal Dynamics of Fields) model across 22 physics domains with 61 tests. All tests use frozen parameters from lock files and produce fully reproducible results with complete metadata.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Usage](#usage)
5. [Available Domains](#available-domains)
6. [Command-Line Options](#command-line-options)
7. [Output Files](#output-files)
8. [Troubleshooting](#troubleshooting)
9. [Configuration](#configuration)

---

## System Requirements

### Prerequisites

- **Python**: 3.8 or higher (tested with 3.12.7)
- **Operating System**: Windows, Linux, or macOS
- **Disk Space**: ~300 MB for virtual environment + dependencies
- **Memory**: 2 GB RAM minimum (4 GB recommended)

### Required Software

- Python 3.8+ (download from [python.org](https://www.python.org/downloads/))
- pip (usually included with Python)

### Optional but Recommended

- Git (for version control, if cloning repository)

---

## Installation

### Step 1: Navigate to Directory

```powershell
# Windows PowerShell
cd D:\CDQF-Sandbox\udof_runner

# Linux/Mac
cd /path/to/udof_runner
```

### Step 2: Set Up Virtual Environment

**Windows (PowerShell):**
```powershell
# Automated setup (recommended)
.\setup_environment.ps1

# Or manually:
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation

```powershell
# Windows
.\venv\Scripts\python.exe -c "import numpy, scipy, sympy; print('Installation successful!')"

# Linux/Mac
python -c "import numpy, scipy, sympy; print('Installation successful!')"
```

Expected output: `Installation successful!`

---

## Quick Start

### Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Run All Tests

```powershell
# Windows
python udof_validation_runner_v4.0.py

# Linux/Mac
python3 udof_validation_runner_v4.0.py
```

This will run all 22 domains (61 tests) and generate results in `run_results/`.

### Expected Output

You should see:
- Progress output for each domain
- Test results (PASS/FAIL) for each test
- Final summary: `TOTAL: 61/61 passed, 0 failed, 0 errors`
- Generated files in `run_results/<run_id>/`

---

## Usage

### Run All Domains

```powershell
python udof_validation_runner_v4.0.py
```

### Run Specific Domains

```powershell
# Single domain
python udof_validation_runner_v4.0.py --domain bao

# Multiple domains
python udof_validation_runner_v4.0.py --domain bao --domain sne --domain sparc
```

### List Available Domains

```powershell
python udof_validation_runner_v4.0.py --list-domains
```

### Quiet Mode (JSON Output Only)

```powershell
python udof_validation_runner_v4.0.py --quiet
```

Suppresses console output, only writes JSON results.

### Custom Output Directory

```powershell
python udof_validation_runner_v4.0.py --output-dir ./my_results
```

### Advanced Options

```powershell
# Use different cosmology method
python udof_validation_runner_v4.0.py --cosmology-method proper

# Disable R_X response function
python udof_validation_runner_v4.0.py --no-rx

# Use different SPARC formula
python udof_validation_runner_v4.0.py --sparc-formula separated
```

---

## Available Domains (22)

1. **fermion_masses** - Quark and lepton masses
2. **pmns_mixing** - Neutrino mixing angles
3. **ckm_mixing** - Quark mixing angles
4. **neutrino_masses** - Neutrino mass splittings
5. **h4_geometry** - 4D geometry constraints
6. **gauge_symmetry** - Gauge groups and couplings
7. **rg_evolution** - Renormalization group flow
8. **ward_identities** - Gauge invariance
9. **bao** - Baryon acoustic oscillations
10. **sne** - Supernova cosmology
11. **sparc** - Galaxy rotation curves (175 galaxies)
12. **dark_matter** - Dark matter structure
13. **dark_energy** - Dark energy equation of state
14. **early_universe** - Early universe cosmology
15. **lss** - Large scale structure
16. **strong_field** - Strong gravitational fields
17. **precision_tests** - Precision gravity tests
18. **cmb** - Cosmic microwave background
19. **inflation** - Inflation parameters
20. **cp_violation** - CP-violating phases
21. **microphysics** - Particle physics tests
22. **gw_ringdown** - Gravitational wave ringdown

---

## Directory Structure

```
udof_runner/
├── udof_validation_runner_v4.0.py  # Production runner (MAIN - use this!)
├── default_params.json              # Parameter configuration
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── setup_environment.ps1            # Environment setup script
├── run_all_tests.ps1               # Batch test runner
├── data/                           # Input datasets
│   ├── bao/                        # BAO data (DESI DR1)
│   ├── cosmology/                  # Cosmology parameters
│   ├── pdg/                        # PDG particle data
│   ├── sne/                        # Supernova data (Pantheon+)
│   └── sparc/                      # SPARC galaxy catalog + rotation curves
│       ├── sparc_full_catalog.csv
│       ├── manifest.json
│       └── rotation_curves/        # 175 rotation curve data files
├── integrated_modules/             # Self-contained physics modules
│   ├── bbn_solver.py               # BBN abundance computation
│   ├── sigma8_computation.py       # σ₈ from power spectrum
│   ├── lss_transition.py           # Structure transition scale
│   ├── gw_propagation_speed.py     # GW speed c_GW
│   ├── llr_precision_gravity.py    # Lunar Laser Ranging
│   ├── binary_pulsar_timing.py     # Binary pulsar orbital decay
│   ├── sparc_separated_fitter.py   # Per-galaxy rotation curve fitter
│   ├── cmb_internal.py             # CMB power spectrum (CAMB fallback)
│   ├── quantum_gravity modules     # QG quantization, gravitons, G derivation
│   ├── baryogenesis modules        # CP violation, leptogenesis
│   ├── gauge modules               # Gauge unification, RG evolution, CP
│   └── ... (other modules)
├── run_results/                    # Historical run logs
├── venv/                           # Python virtual environment
└── archive/                        # Archived documents, diagnostic scripts, and old runners
```

**Note**: The `udof_validation_runner_v4.0.py` is the **only production runner**. Diagnostic helper scripts (like `run_validation_no_hang.py` and `run_validation_sparc_params.py`) have been archived as they were only temporary wrappers for troubleshooting.

---

## Key Features

- **Self-contained**: All modules in `integrated_modules/`
- **Comprehensive**: 22 physics domains, 61 tests
- **Complete**: All missing components implemented
  - ✅ BBN solver
  - ✅ σ₈ computation
  - ✅ LSS transition
  - ✅ GW propagation speed
  - ✅ LLR precision gravity
  - ✅ Binary pulsar timing
  - ✅ SPARC per-galaxy fitter (175 galaxies)
  - ✅ CMB internal fallback
- **Validated**: MCMC-calibrated parameters
- **Physical consistency**: Cross-domain checks
- **JSON output**: Machine-readable results

---

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--domain DOMAIN` | Run specific domain(s) (can be used multiple times) | All domains |
| `--list-domains` | List all available domains and exit | - |
| `--quiet` | Suppress console output, only write JSON | False |
| `--output-dir PATH` | Custom output directory | `run_results/` |
| `--cosmology-method METHOD` | Cosmology computation method (`proper` or `simplified`) | `proper` |
| `--no-rx` | Disable R_X response function | False (R_X enabled) |
| `--sparc-formula FORMULA` | SPARC formula type (`separated` or `combined`) | `separated` |
| `--sparc-b-prediction` | Use B parameter prediction for SPARC | False |
| `--version` | Show version and exit | - |

### Examples

```powershell
# Run only BAO and SNe tests
python udof_validation_runner_v4.0.py --domain bao --domain sne

# Run with custom output directory
python udof_validation_runner_v4.0.py --output-dir ./validation_results

# Quiet mode with specific domains
python udof_validation_runner_v4.0.py --quiet --domain fermion_masses --domain pmns_mixing
```

---

## Output Files

Results are saved to `run_results/<run_id>/` directory (or custom `--output-dir`):

### Generated Files

1. **RUN_MANIFEST.json**
   - Complete run metadata
   - File hashes (runner, modules, datasets, lock files)
   - Environment info (Python version, dependencies, platform)
   - Git commit hash (if in git repo)
   - Dataset checksums

2. **EQUATIONS_USED.md**
   - Exact equations evaluated for each test
   - LaTeX format
   - Organized by domain

3. **SUMMARY_TABLE.md**
   - Human-readable summary table
   - Test ID, domain, observable, requirement, result, status

4. **Domain Results** (`<domain>/<domain>_results.json`)
   - Machine-readable JSON results per domain
   - Test values, errors, chi², notes

5. **Aggregated Results** (`logs/RESULTS.json`)
   - Complete aggregated results
   - All domain results in single file

### Run ID Format

`udof_v4.0_YYYYMMDD_HHMMSS`

Example: `udof_v4.0_20251217_012539`

---

## Troubleshooting

### Installation Issues

**Problem**: `python: command not found`
- **Solution**: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- **Verify**: `python --version` should show 3.8 or higher

**Problem**: `pip: command not found`
- **Solution**: Python 3.4+ includes pip. If missing, install via: `python -m ensurepip --upgrade`

**Problem**: Permission denied when creating venv
- **Solution**: Ensure you have write permissions in the directory
- **Alternative**: Use `--user` flag or run with appropriate permissions

**Problem**: Package installation fails
- **Solution**: Upgrade pip first: `python -m pip install --upgrade pip`
- **Solution**: Install packages individually to identify problematic package
- **Solution**: Check Python version compatibility

### Runtime Issues

**Problem**: `ModuleNotFoundError: No module named 'integrated_modules'`
- **Solution**: Ensure you're running from the `udof_runner` directory
- **Solution**: Check that `integrated_modules/` directory exists

**Problem**: `FileNotFoundError: Sandbox directory not found`
- **Solution**: The runner uses the directory it's run from as the sandbox root
- **Solution**: Ensure you're running from the `udof_runner` directory
- **Solution**: If you need to change the path, update `SANDBOX_ROOT` in `udof_validation_runner_v4.0.py` (line ~64)

**Problem**: Missing data files
- **Solution**: Ensure all data files are present in `data/` directory
- **Solution**: Check `data/MANIFEST.md` for required files
- **Solution**: Missing files will cause specific domain tests to error

**Problem**: Tests fail unexpectedly
- **Solution**: Check `run_results/<run_id>/logs/stdout.log` for error messages
- **Solution**: Verify lock files are present in `data/locks/`
- **Solution**: Ensure all dependencies are installed: `pip list`

### Performance Issues

**Problem**: Tests run very slowly
- **Solution**: This is normal - full suite takes several minutes
- **Solution**: Run specific domains to test faster: `--domain bao`
- **Solution**: Use `--quiet` to reduce console I/O overhead

**Problem**: Out of memory errors
- **Solution**: Close other applications
- **Solution**: Run domains individually instead of all at once

### Verification

**Verify installation:**
```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "import numpy, scipy, sympy, camb; print('All packages available')"
```

**Verify data files:**
```powershell
# Check data directory structure
ls data/bao/
ls data/sne/
ls data/sparc/
ls data/locks/
```

**Verify successful run:**
- Check `run_results/<run_id>/SUMMARY_TABLE.md` for test results
- Check `run_results/<run_id>/RUN_MANIFEST.json` for metadata
- Look for `TOTAL: 61/61 passed` in console output

---

## Configuration

### Parameter Files

**Lock Files** (in `data/locks/`):
- `udof_MASTER_LOCK_v3_SPARC.json` - Master parameter lock
- `udof_unified_x_locks_v2.3.8_FINAL_HYBRID.json` - Unified parameter locks
- `dark_sector_locks_entropy_v1.json` - Dark sector parameters

**Default Parameters** (`default_params.json`):
- Fallback parameters if lock files unavailable
- Not used when lock files are present

**Note**: The validation suite uses lock files from `data/locks/` exclusively. All parameters are frozen and cannot be modified during runs (per standards compliance).

### Customizing Parameters

⚠️ **Important**: Per standards compliance, parameters are **frozen** and cannot be changed during validation runs. To use different parameters:

1. Replace lock files in `data/locks/` with your parameter files
2. Ensure file names match expected names (see runner code)
3. Run validation with new parameters

**Warning**: Changing parameters invalidates reproducibility. All runs should use the same lock files for comparison.

---

## Citations

See `CITATIONS.md` for complete attribution of:
- **Observational datasets**: DESI DR1 BAO, Pantheon+SH0ES, SPARC, Planck 2018, PDG 2024
- **Software dependencies**: NumPy, SciPy, SymPy, CAMB, mpmath (with full citations and DOIs)
- **Precision test data**: Binary pulsars, lunar laser ranging, Mercury perihelion, Cassini
- **Computational resources**: Python runtime

All citations include DOI, arXiv, and URL where available.

---

## Module Architecture

All physics modules are self-contained in `integrated_modules/`:
- **Quantum Gravity**: `qg_*` modules
- **Baryogenesis**: `baryo_*` modules
- **Gauge Theory**: `gauge_*` modules
- **Cosmology**: `proper_growth_standalone.py`, `sigma8_computation.py`
- **SPARC**: `sparc_ese_computation.py`, `sparc_separated_fitter.py`
- **Precision Tests**: `llr_precision_gravity.py`, `binary_pulsar_timing.py`
- **Early Universe**: `bbn_solver.py`, `lss_transition.py`
- **CMB**: `cmb_internal.py` (fallback when CAMB unavailable)

---

## Version

**v4.0.0** - Complete Implementation
- All 9 missing components integrated
- SPARC per-galaxy fits enabled
- Full validation suite operational

---

## Expected Runtime

- **Full suite (all 22 domains)**: ~2-5 minutes (depending on hardware)
- **Single domain**: ~5-30 seconds
- **CMB domain**: May take longer if CAMB is used

## Interpreting Results

### Test Status

- **PASS**: Test passed threshold criteria
- **FAIL**: Test failed threshold criteria
- **ERROR**: Test encountered an error during execution
- **SKIP**: Test was skipped (missing data or optional dependency)
- **THEORETICAL**: Test is theoretical (no observational comparison)

### Summary Table

The `SUMMARY_TABLE.md` shows:
- Test ID and domain
- Observable being tested
- Requirement (threshold)
- Result (computed value)
- Status (PASS/FAIL)

### Manifest

The `RUN_MANIFEST.json` contains:
- Complete reproducibility metadata
- File hashes for verification
- Environment information
- Dataset checksums

---

## Status

✅ **Production Ready**
- All domains functional
- All missing components implemented
- Cross-domain consistency verified
- Physical values validated
- 100% standards compliant
- Complete citations provided

---

## Support

For issues or questions:
1. Check `TROUBLESHOOTING` section above
2. Review `run_results/<run_id>/logs/stdout.log` for errors
3. Verify all prerequisites are installed
4. Ensure data files are present in `data/` directory
