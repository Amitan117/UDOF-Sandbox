# CDQF Validation Runner Data Manifest

**Last Updated:** 2025-11-29  
**Runner Version:** 3.3.0

## Directory Structure

```
cdqf_runner/data/
├── README.md                    # This file
├── MANIFEST.md                  # Data manifest (this file)
├── bao/
│   └── desi_dr1_all/
│       ├── mean.txt            # DESI DR1 BAO measurements
│       └── cov.txt             # DESI DR1 BAO covariance matrix
├── sne/
│   └── pantheon_plus/
│       └── Pantheon+SH0ES.dat  # Pantheon+SH0ES supernova catalog
└── sparc/
    └── sparc_full_catalog.csv  # SPARC galaxy rotation curve catalog
```

## File Inventory

### BAO Data (Domain: `bao`)
| File | Size | Description | Source |
|------|------|-------------|--------|
| `bao/desi_dr1_all/mean.txt` | 0.37 KB | DESI DR1 BAO mean measurements | DESI Collaboration |
| `bao/desi_dr1_all/cov.txt` | 2.12 KB | DESI DR1 BAO covariance matrix | DESI Collaboration |

### Supernova Data (Domain: `sne`)
| File | Size | Description | Source |
|------|------|-------------|--------|
| `sne/pantheon_plus/Pantheon+SH0ES.dat` | 565.71 KB | Pantheon+SH0ES catalog | Scolnic et al. 2022 |

### SPARC Galaxy Data (Domain: `sparc`)
| File | Size | Description | Source |
|------|------|-------------|--------|
| `sparc/sparc_full_catalog.csv` | 26.13 KB | SPARC galaxy catalog | Lelli et al. 2016 |

## Data Verification

All files verified and accessible:
- ✅ BAO mean.txt: Present
- ✅ BAO cov.txt: Present  
- ✅ SNe Pantheon+SH0ES.dat: Present
- ✅ SPARC catalog: Present

## Data Usage

The validation runner automatically:
1. Checks `cdqf_runner/data/` first (this directory)
2. Falls back to `prime0/data/` if files not found
3. Reports errors if required data files are missing

## Requirements

All files in this directory are **required** for full validation:
- Missing BAO data → BAO tests will error
- Missing SNe data → SNe tests will error
- Missing SPARC data → SPARC tests will error

## Data Integrity

All files are copied from `prime0/data/` and verified to match original sources.

## Notes

- These are **real observational data files**, not simulations
- No preprocessing or modification of observational data
- All data used as-is from original sources
- File sizes are approximate and may vary slightly

