# UDOF Validation Runner Data Directory

This directory contains all observational data files required for UDOF validation tests.

## Directory Structure

```
data/
├── bao/
│   └── desi_dr1_all/
│       ├── mean.txt          # DESI DR1 BAO measurements
│       └── cov.txt           # DESI DR1 BAO covariance matrix
├── sne/
│   └── pantheon_plus/
│       └── Pantheon+SH0ES.dat    # Pantheon+SH0ES supernova data
└── sparc/
    └── sparc_full_catalog.csv    # SPARC galaxy rotation curve catalog
```

## Data Sources

**⚠️ IMPORTANT:** Please see `../CITATIONS.md` in the root directory for complete 
bibliographic citations for all data sources listed below.

### BAO Data (DESI DR1)
- **Source:** DESI (Dark Energy Spectroscopic Instrument) Data Release 1
- **Citation:** DESI Collaboration (2024), arXiv:2404.03002
- **Files:** `mean.txt` (measurements), `cov.txt` (covariance matrix)
- **Use:** Baryon Acoustic Oscillation (BAO) distance measurements
- **Location:** `bao/desi_dr1_all/`

### Supernova Data (Pantheon+SH0ES)
- **Source:** Pantheon+SH0ES compilation
- **Citation:** Scolnic et al. (2022), ApJ 938, 113, arXiv:2112.03863
- **File:** `Pantheon+SH0ES.dat`
- **Use:** Type Ia supernova distance modulus measurements
- **Location:** `sne/pantheon_plus/`

### SPARC Galaxy Catalog
- **Source:** SPARC (Spitzer Photometry & Accurate Rotation Curves)
- **Citation:** Lelli et al. (2016), AJ 152, 157, arXiv:1606.09251
- **File:** `sparc_full_catalog.csv`
- **Use:** Galaxy rotation curve data for ESE (dark matter) tests
- **Location:** `sparc/`

### Planck 2018 Cosmological Parameters
- **Source:** Planck Collaboration
- **Citation:** Planck Collaboration (2020), A&A 641, A6, arXiv:1807.06209
- **File:** `cosmology/planck_2018.json`
- **Use:** Reference cosmological parameter values
- **Location:** `cosmology/`

### PDG 2024 Particle Masses
- **Source:** Particle Data Group
- **Citation:** Workman et al. (2024), PTEP 2024, 083C01
- **File:** `pdg/pdg_masses_2024.json`
- **Use:** Reference particle mass values for validation
- **Location:** `pdg/`

## Data Files Required by Runner

| Test Domain | Required Files | Status |
|-------------|---------------|--------|
| BAO | `bao/desi_dr1_all/mean.txt`, `bao/desi_dr1_all/cov.txt` | ✅ |
| SNe Ia | `sne/pantheon_plus/Pantheon+SH0ES.dat` | ✅ |
| SPARC | `sparc/sparc_full_catalog.csv` | ✅ |

## File Verification

All files are required for complete validation. The runner will:
1. First check `udof_runner/data/` (this directory)
2. Fall back to `prime0/data/` if not found
3. Report errors if data files are missing

## Data File Sizes

- `mean.txt`: ~few KB (BAO measurements)
- `cov.txt`: ~few MB (BAO covariance matrix)
- `Pantheon+SH0ES.dat`: ~few MB (SNe catalog)
- `sparc_full_catalog.csv`: ~few KB (galaxy catalog)

## Notes

- These are real observational data files, not simulations
- All data is used as-is from original sources
- No preprocessing or modification of observational data
- Missing files will cause corresponding tests to be skipped or error

