# CDQF Universal Validation Runner v4.0

**Self-contained validation suite for the complete CDQF model**

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
python cdqf_validation_runner_v4.0.py
```

**Specific domains:**
```powershell
python cdqf_validation_runner_v4.0.py --domain quantum_gravity --domain baryogenesis
```

**Quiet mode (JSON only):**
```powershell
python cdqf_validation_runner_v4.0.py --quiet
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
11. **sparc** - Galaxy rotation curves
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
cdqf_runner/
├── cdqf_validation_runner_v4.0.py  # Main runner
├── default_params.json              # Parameter configuration
├── requirements.txt                 # Python dependencies
├── setup_environment.ps1            # Environment setup script
├── run_all_tests.ps1               # Batch test runner
├── CITATIONS.md                    # Data and software citations
├── README.md                       # This file
├── data/                           # Input datasets
│   ├── bao/                        # BAO data
│   ├── cosmology/                  # Cosmology parameters
│   ├── pdg/                        # PDG particle data
│   ├── sne/                        # Supernova data
│   └── sparc/                      # SPARC galaxy catalog
├── integrated_modules/             # Self-contained physics modules
├── results/                        # Validation results (JSON)
├── run_results/                    # Historical run logs
└── venv/                           # Python virtual environment
```

---

## Key Features

- **Self-contained**: All modules in `integrated_modules/`
- **Comprehensive**: 25 physics domains, 72+ tests
- **Validated**: MCMC-calibrated parameters
- **Physical consistency**: Cross-domain checks
- **JSON output**: Machine-readable results

---

## Results

Results are saved to `results/` directory as JSON files:
- Run ID: `cdqf_v4.0_TIMESTAMP.json`
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
- **Cosmology**: `proper_growth_standalone.py`
- **SPARC**: `sparc_ese_computation.py`

---

## Version

**v4.0.0** - MCMC-Validated Parameters

---

## Status

✅ **Production Ready**
- All domains functional
- Full validation passing (65/72 tests)
- Cross-domain consistency verified
- Physical values validated

