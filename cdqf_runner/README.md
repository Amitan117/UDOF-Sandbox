# CDQF Universal Validation Runner

A self-contained, transparent validation framework for the **Curvature-Dynamics-Quantum-Field (CDQF)** unified physics model.

## Features

- Complete validation across 14 CDQF physics domains (38 tests)
- Self-contained with all formulas explicitly documented
- Configurable input parameters via JSON or CLI
- Timestamped outputs for scientific reproducibility
- Modular domain-specific test functions

## Quick Start

```bash
# Run full validation with default CDQF parameters
python cdqf_validation_runner.py

# Run specific domain
python cdqf_validation_runner.py --domain fermion_masses

# Run multiple domains
python cdqf_validation_runner.py --domain fermion_masses pmns_mixing h4_geometry

# Use custom parameters
python cdqf_validation_runner.py --config my_params.json

# Export default parameters for modification
python cdqf_validation_runner.py --export-defaults my_defaults.json
```

## Requirements

**Required:**
- Python 3.8+
- NumPy

**Optional (for full functionality):**
- SciPy (for PMNS matrix computation and RG evolution)

Install with:
```bash
pip install numpy scipy
```

## Available Test Domains

| Domain | Description | Tests |
|--------|-------------|-------|
| `fermion_masses` | 9 charged fermion mass predictions | t, c, u, b, s, d, tau, mu, e |
| `pmns_mixing` | PMNS neutrino mixing angles | theta12, theta23, theta13 |
| `h4_geometry` | H4 icosahedral symmetry constraints | trace, det(Gamma), det(Sigma) |
| `gauge_symmetry` | SU(3)xSU(2)xU(1) emergence | Lindblad CP, gauge groups |
| `rg_evolution` | 2-loop RG and Higgs stability | lambda_min, Landau poles |
| `ward_identities` | Ward identity violation bounds | charge conservation, photon mass |
| `cosmology` | Cosmological parameters | H0, Omega_m, flatness |
| `dark_matter` | ESE dark matter behavior | galactic activation, LCDM recovery |
| `dark_energy` | Dark energy equation of state | DE dominance, w = -1 |
| `early_universe` | CMB epoch, BBN | LCDM regime, BBN preservation |
| `lss` | Large scale structure | BAO sound horizon, structure transition |
| `strong_field` | Strong gravity limits | GR recovery at horizons |
| `lab_tests` | Laboratory precision tests | SM preservation, Cassini bounds |
| `ckm_mixing` | CKM quark mixing | theta12, theta23, theta13 |

## Directory Structure

```
cdqf_runner/
├── cdqf_validation_runner.py    # Main runner script
├── README.md                    # This file
├── data/                        # Input data directory
│   ├── pdg/                     # Particle Data Group reference values
│   │   └── pdg_masses_2024.json
│   └── cosmology/               # Cosmological datasets
│       └── planck_2018.json
└── run_results/                 # Output directory
    └── cdqf_YYYYMMDD_HHMMSS_xxx/
        ├── validation_results.json
        ├── summary.csv
        └── <domain>/
            └── <domain>_results.json
```

## Custom Parameters

Export default parameters and modify:

```bash
python cdqf_validation_runner.py --export-defaults my_params.json
# Edit my_params.json
python cdqf_validation_runner.py --config my_params.json
```

### Parameter Structure

```json
{
  "version": "2.3.5_H4_ULTRA_WIDE",
  "geometry_eigenvalues": {
    "gamma": [1.469331, 1.750000, 1.594506],
    "sigma": [0.118172, 1.651012, 3.416979]
  },
  "fermion_masses": {
    "lambda_0": 0.593...,
    "beta_ql": 1.621...,
    "a_u": -0.682..., "b_u": 3.456...,
    "a_d": 2.077..., "b_d": 1.974...,
    "a_e": 1.258..., "b_e": 3.129...,
    "c_tau": 2.326...
  },
  "pmns_mixing": {
    "epsilon_comm": -2.000...,
    "epsilon_diff": -0.958...,
    "Delta_a": 0.468...,
    "Delta_b": 5.641...
  },
  "ese_map": {
    "ell_IR": 4.7e-5,
    "ell_star": 2e-15,
    "eta_star": 0.171,
    "X0": 0.6481,
    "K": 1.5,
    "sigma0": 0.217
  }
}
```

## Scientific Transparency

All formulas are explicitly documented in the code:

### Fermion Mass Formula
```
H = a * gamma_i + b * sigma_i
Y = lambda_0 * sector_scale * exp(-H) * tau_correction
m = Y * v_higgs / sqrt(2)
```

### PMNS Matrix Formula
```
K_comm_ij = gamma_i * sigma_j - gamma_j * sigma_i
K_diff_ij = Delta_a * (gamma_i - gamma_j) + Delta_b * (sigma_i - sigma_j)
U_PMNS = exp(epsilon_comm * K_comm + epsilon_diff * K_diff)
```

### H4 Constraints
```
Tr(Gamma) + Tr(Sigma) = 10
det(Gamma) = 4.1
det(Sigma) = 2/3
```

### ESE Map
```
S_struct = delta^2 / (1 + delta^2)
X = (Sigma_b / Sigma_0)^eta_star * S_struct
s = 1 / (1 + exp(-K * (ln(X) - ln(X0))))
ell_eff = exp(ln(ell_IR) + s * (ln(ell_star) - ln(ell_IR)))
```

## Output Format

### JSON Results

Each run produces timestamped JSON with:

```json
{
  "run_id": "cdqf_20251128_123456_abc12345",
  "cdqf_version": "2.3.5_H4_ULTRA_WIDE",
  "timestamp_start": "2025-11-28T12:34:56.789Z",
  "domains": {
    "fermion_masses": {
      "n_pass": 9,
      "n_fail": 0,
      "chi2_total": 0.0442,
      "tests": [...]
    }
  },
  "system_info": {...},
  "parameters": {...}
}
```

### CSV Summary

```csv
domain,test,status,value,expected,error,error_percent
fermion_masses,mass_t,PASS,186.95,172.69,14.26,8.3
fermion_masses,mass_c,PASS,1.133,1.27,0.137,10.8
...
```

## CLI Reference

```
usage: cdqf_validation_runner.py [-h] [--domain DOMAIN [DOMAIN ...]]
                                  [--config CONFIG] [--data-dir DATA_DIR]
                                  [--output OUTPUT] [--no-save] [--quiet]
                                  [--list-domains] [--export-defaults PATH]
                                  [--version]

Options:
  --domain, -d      Domain(s) to test (default: all)
  --config, -c      Path to custom parameters JSON
  --data-dir        Path to data directory
  --output, -o      Output directory for results
  --no-save         Don't save results to disk
  --quiet, -q       Suppress progress output
  --list-domains    List available domains and exit
  --export-defaults Export default parameters to file
  --version, -v     Show version and exit
```

## License

MIT License

## References

- CDQF Theoretical Foundations Summary (see `docs/CDQF_THEORETICAL_FOUNDATIONS_SUMMARY.md`)
- Particle Data Group: https://pdg.lbl.gov
- Planck Collaboration 2018: arXiv:1807.06209
