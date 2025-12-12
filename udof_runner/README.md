# UDOF Universal Validation Runner v4.0

**Self-contained validation suite for the complete UDOF model**

---

## Quick Start

### Setup Environment

```powershell
.\setup_environment.ps1
```

Or manually:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run Validation

**All domains:**
```powershell
python udof_validation_runner_v4.0.py
```

**Specific domains:**
```powershell
python udof_validation_runner_v4.0.py --domain quantum_gravity --domain baryogenesis
```

**Quiet mode (JSON only):**
```powershell
python udof_validation_runner_v4.0.py --quiet
```

---

## Available Domains (25)

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
23. **quantum_gravity** - Quantum gravity quantization
24. **baryogenesis** - Baryon asymmetry from leptogenesis
25. **master_action** - Unified master action

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
- **Comprehensive**: 25 physics domains, 72+ tests
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

## Results

Results are saved to `results/` directory as JSON files:
- Run ID: `udof_v4.0_TIMESTAMP.json`
- Includes: Test results, values, errors, notes

---

## Parameters

Configuration in `default_params.json`:
- Cosmological parameters (H₀, Ωₘ, etc.)
- Particle physics parameters
- Dark sector parameters
- MCMC-validated values

---

## Citations

See `CITATIONS.md` for attribution of:
- External datasets (BAO, SNe, SPARC, PDG)
- Software dependencies (CAMB, NumPy, SciPy)

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

## Status

✅ **Production Ready**
- All domains functional
- All missing components implemented
- Cross-domain consistency verified
- Physical values validated
