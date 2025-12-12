# UDOF Validation Runner Data Manifest

**Last Updated:** 2025-12-10  
**Runner Version:** 4.0.0

**Citations:** See `CITATIONS.md` in the root directory for complete 
bibliographic information for all data sources.

## Directory Structure

```
udof_runner/data/
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
| File | Size | Description | Source | Citation |
|------|------|-------------|--------|----------|
| `bao/desi_dr1_all/mean.txt` | 0.37 KB | DESI DR1 BAO mean measurements | DESI Collaboration | DESI Collaboration (2024), arXiv:2404.03002 |
| `bao/desi_dr1_all/cov.txt` | 2.12 KB | DESI DR1 BAO covariance matrix | DESI Collaboration | DESI Collaboration (2024), arXiv:2404.03002 |

### Supernova Data (Domain: `sne`)
| File | Size | Description | Source | Citation |
|------|------|-------------|--------|----------|
| `sne/pantheon_plus/Pantheon+SH0ES.dat` | 565.71 KB | Pantheon+SH0ES catalog | Scolnic et al. 2022 | Scolnic et al. (2022), ApJ 938, 113, arXiv:2112.03863 |

### SPARC Galaxy Data (Domain: `sparc`)
| File | Size | Description | Source | Citation |
|------|------|-------------|--------|----------|
| `sparc/sparc_full_catalog.csv` | 26.13 KB | SPARC galaxy catalog | Lelli et al. 2016 | Lelli et al. (2016), AJ 152, 157, arXiv:1606.09251 |

### Cosmological Parameters (Domain: `cosmology`)
| File | Size | Description | Source | Citation |
|------|------|-------------|--------|----------|
| `cosmology/planck_2018.json` | ~few KB | Planck 2018 cosmological parameters | Planck Collaboration | Planck Collaboration (2020), A&A 641, A6, arXiv:1807.06209 |

### Particle Data (Domain: `pdg`)
| File | Size | Description | Source | Citation |
|------|------|-------------|--------|----------|
| `pdg/pdg_masses_2024.json` | ~few KB | PDG 2024 particle masses | Particle Data Group | Workman et al. (2024), PTEP 2024, 083C01 |

## Data Verification

All files verified and accessible:
- ✅ BAO mean.txt: Present
- ✅ BAO cov.txt: Present  
- ✅ SNe Pantheon+SH0ES.dat: Present
- ✅ SPARC catalog: Present

## Data Usage

The validation runner automatically:
1. Checks `udof_runner/data/` first (this directory)
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

