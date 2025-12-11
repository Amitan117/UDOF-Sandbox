# Citations and Data Sources

This document provides proper attribution for all external data sources and software libraries used in the CDQF Validation Runner.

**Last Updated:** 2025-12-10  
**Runner Version:** 4.0.0

---

## Observational Data Sources

### 1. DESI DR1 Baryon Acoustic Oscillation (BAO) Data

**Source:** DESI Collaboration  
**Data Release:** Data Release 1 (DR1)  
**Files Used:**
- `data/bao/desi_dr1_all/mean.txt` - BAO measurements
- `data/bao/desi_dr1_all/cov.txt` - Covariance matrix

**Citation:**
```
DESI Collaboration (2024). "DESI 2024 VI: Cosmological Constraints from the 
Measurements of Baryon Acoustic Oscillations." arXiv:2404.03002
```

**Additional References:**
- DESI Collaboration (2023). "The Early Data Release of the Dark Energy 
  Spectroscopic Instrument." AJ 167, 207. DOI: 10.3847/1538-3881/ad1c67

**Data Access:**
- Official DESI data portal: https://data.desi.lbl.gov/
- Data used for BAO distance measurements in the validation suite

**License/Acknowledgement:** DESI data is publicly available. Use of DESI data 
requires acknowledgment in publications. See: https://www.desi.lbl.gov/citingdesi/

---

### 2. Pantheon+SH0ES Type Ia Supernova Data

**Source:** Pantheon+ Collaboration (Scolnic et al.)  
**Compilation:** Pantheon+SH0ES  
**File Used:**
- `data/sne/pantheon_plus/Pantheon+SH0ES.dat` - Supernova distance modulus catalog

**Citation:**
```
Scolnic, D. M., et al. (2022). "The Pantheon+ Analysis: Cosmological Constraints." 
ApJ 938, 113. DOI: 10.3847/1538-4357/ac8b7a
arXiv: 2112.03863
```

**Additional References:**
- Riess, A. G., et al. (2022). "A Comprehensive Measurement of the Local Value of 
  the Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope 
  and the SH0ES Team." ApJL 934, L7. DOI: 10.3847/2041-8213/ac5c5b

**Data Access:**
- Pantheon+ data release: https://github.com/PantheonPlusSH0ES/DataRelease
- Data used for Type Ia supernova distance modulus measurements

**License/Acknowledgement:** Pantheon+ data is publicly available under the 
provided license. Please cite the papers above when using this data.

---

### 3. SPARC Galaxy Rotation Curve Catalog

**Source:** SPARC (Spitzer Photometry & Accurate Rotation Curves)  
**Catalog:** SPARC Galaxy Catalog  
**File Used:**
- `data/sparc/sparc_full_catalog.csv` - Galaxy rotation curve data

**Citation:**
```
Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016). "SPARC: Mass Models for 
175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves." AJ 152, 
157. DOI: 10.3847/0004-6256/152/6/157
arXiv: 1606.09251
```

**Additional References:**
- SPARC database: http://astroweb.cwru.edu/SPARC/
- Data used for galaxy rotation curve validation of dark sector models

**License/Acknowledgement:** SPARC data is publicly available. Please cite 
the paper above when using this data.

---

### 4. Planck 2018 Cosmological Parameters

**Source:** Planck Collaboration  
**Release:** Planck 2018 results  
**File Used:**
- `data/cosmology/planck_2018.json` - Cosmological parameter values

**Citation:**
```
Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters." 
A&A 641, A6. DOI: 10.1051/0004-6361/201833910
arXiv: 1807.06209
```

**Additional References:**
- Planck Legacy Archive: https://pla.esac.esa.int/
- Full Planck 2018 results: A&A volume 641, 2020

**License/Acknowledgement:** Planck data products are publicly available. 
Please cite the paper above when using Planck data.

---

### 5. Particle Data Group (PDG) 2024 Particle Masses

**Source:** Particle Data Group  
**Edition:** 2024 Review of Particle Physics  
**File Used:**
- `data/pdg/pdg_masses_2024.json` - Particle mass values and uncertainties

**Citation:**
```
Workman, R. L., et al. (Particle Data Group) (2024). "Review of Particle Physics." 
PTEP 2024, 083C01. DOI: 10.1093/ptep/ptae097
```

**Additional References:**
- PDG website: https://pdg.lbl.gov/
- PDG Live (current values): https://pdg.lbl.gov/
- Data used for validation of fermion mass predictions

**License/Acknowledgement:** PDG data is publicly available for scientific use. 
Please cite the Review of Particle Physics when using PDG values.

---

## Software Libraries

### 1. CAMB (Code for Anisotropies in the Microwave Background)

**Purpose:** CMB power spectrum computation  
**Version:** 1.6.5 (or compatible)  
**Usage:** Computes cosmic microwave background temperature power spectra for 
validation of cosmological models

**Citation:**
```
Lewis, A., & Challinor, A. (2011). "CAMB: Code for Anisotropies in the 
Microwave Background." Astrophysics Source Code Library, record ascl:1102.026
```

**Additional References:**
- CAMB website: https://camb.info/
- GitHub repository: https://github.com/cmbant/CAMB
- Documentation: https://camb.readthedocs.io/

**License:** CAMB is distributed under a permissive open source license. 
Please cite the paper above when using CAMB.

---

### 2. NumPy

**Purpose:** Numerical computing  
**Version:** >=1.20.0  
**Usage:** Array operations, numerical computations, data manipulation

**Citation:**
```
Harris, C. R., et al. (2020). "Array programming with NumPy." Nature 585, 357-362. 
DOI: 10.1038/s41586-020-2649-2
```

**Additional References:**
- NumPy website: https://numpy.org/
- GitHub repository: https://github.com/numpy/numpy

**License:** BSD-3-Clause License (open source)

---

### 3. SciPy

**Purpose:** Scientific computing  
**Version:** >=1.7.0  
**Usage:** Integration, optimization, linear algebra, special functions

**Citation:**
```
Virtanen, P., et al. (2020). "SciPy 1.0: fundamental algorithms for scientific 
computing in Python." Nature Methods 17, 261-272. 
DOI: 10.1038/s41592-019-0686-2
```

**Additional References:**
- SciPy website: https://scipy.org/
- GitHub repository: https://github.com/scipy/scipy

**License:** BSD-3-Clause License (open source)

---

## Recommended Citation Format for CDQF Validation Runner

If you use the CDQF Validation Runner or reference its results in publications, 
please cite:

1. **All relevant data sources** listed above (DESI, Pantheon+, SPARC, Planck, PDG)
2. **Software libraries** used (CAMB, NumPy, SciPy)
3. **The CDQF model** itself (if applicable)

### Example Acknowledgment Section:

```
Data used in this work includes:
- BAO measurements from DESI DR1 (DESI Collaboration 2024)
- Type Ia supernova data from Pantheon+SH0ES (Scolnic et al. 2022)
- Galaxy rotation curves from SPARC (Lelli et al. 2016)
- Cosmological parameters from Planck 2018 (Planck Collaboration 2020)
- Particle masses from PDG 2024 (Workman et al. 2024)

Computations were performed using:
- CAMB for CMB power spectrum calculations (Lewis & Challinor 2011)
- NumPy (Harris et al. 2020) and SciPy (Virtanen et al. 2020) for numerical computing
```

---

## Data Integrity and Usage

- **No Modifications:** All observational data files are used as-is from original sources
- **Verification:** Data files are verified to match original sources
- **Transparency:** All data sources are documented and publicly accessible
- **Reproducibility:** Exact versions and sources are recorded for reproducibility

---

## Contact and Questions

For questions about data sources or software usage:
- DESI: https://www.desi.lbl.gov/
- Pantheon+: https://github.com/PantheonPlusSH0ES
- SPARC: http://astroweb.cwru.edu/SPARC/
- Planck: https://www.cosmos.esa.int/web/planck
- PDG: https://pdg.lbl.gov/
- CAMB: https://camb.info/

---

**Note:** This citations file should be kept updated as new data sources or 
software are added to the validation suite.

