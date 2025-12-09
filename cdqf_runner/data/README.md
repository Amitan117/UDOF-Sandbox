# CDQF Validation Runner Data Directory

This directory contains all observational data files required for CDQF validation tests.

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

### BAO Data (DESI DR1)
- **Source:** DESI (Dark Energy Spectroscopic Instrument) Data Release 1
- **Files:** `mean.txt` (measurements), `cov.txt` (covariance matrix)
- **Use:** Baryon Acoustic Oscillation (BAO) distance measurements
- **Location:** `bao/desi_dr1_all/`

### Supernova Data (Pantheon+SH0ES)
- **Source:** Pantheon+SH0ES compilation
- **File:** `Pantheon+SH0ES.dat`
- **Use:** Type Ia supernova distance modulus measurements
- **Location:** `sne/pantheon_plus/`

### SPARC Galaxy Catalog
- **Source:** SPARC (Spitzer Photometry & Accurate Rotation Curves)
- **File:** `sparc_full_catalog.csv`
- **Use:** Galaxy rotation curve data for ESE (dark matter) tests
- **Location:** `sparc/`

## Data Files Required by Runner

| Test Domain | Required Files | Status |
|-------------|---------------|--------|
| BAO | `bao/desi_dr1_all/mean.txt`, `bao/desi_dr1_all/cov.txt` | ✅ |
| SNe Ia | `sne/pantheon_plus/Pantheon+SH0ES.dat` | ✅ |
| SPARC | `sparc/sparc_full_catalog.csv` | ✅ |

## File Verification

All files are required for complete validation. The runner will:
1. First check `cdqf_runner/data/` (this directory)
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

