# Complete Citations and Attributions

**UDOF Validation Runner v4.0**  
**Date**: 2025-12-17

This document provides complete citations for all third-party data, software dependencies, and resources used in the validation suite.

---

## Table of Contents

1. [Observational Datasets](#observational-datasets)
2. [Software Dependencies](#software-dependencies)
3. [Computational Resources](#computational-resources)
4. [Reference Data](#reference-data)

---

## Observational Datasets

### BAO Data

**DESI DR1 BAO Measurements**
- **Dataset**: DESI DR1 BAO Mean Measurements
- **Version**: DR1
- **Source**: DESI Collaboration
- **Citation**: DESI Collaboration (2024), arXiv:2404.03002
- **DOI**: Not yet assigned (preprint)
- **arXiv**: 2404.03002
- **URL**: https://data.desi.lbl.gov/public/edr/vac/edr/bao/
- **Files**: `data/bao/desi_dr1_all/mean.txt`, `data/bao/desi_dr1_all/cov.txt`
- **Usage**: BAO domain tests

**DESI DR1 BAO Covariance Matrix**
- **Dataset**: DESI DR1 BAO Covariance Matrix
- **Version**: DR1
- **Source**: DESI Collaboration
- **Citation**: DESI Collaboration (2024), arXiv:2404.03002
- **arXiv**: 2404.03002
- **URL**: https://data.desi.lbl.gov/public/edr/vac/edr/bao/
- **Files**: `data/bao/desi_dr1_all/cov.txt`
- **Usage**: BAO domain tests

---

### Supernova Data

**Pantheon+SH0ES**
- **Dataset**: Pantheon+SH0ES Supernova Catalog
- **Version**: Pantheon+SH0ES
- **Source**: Scolnic et al.
- **Citation**: Scolnic, D. M., et al. (2022), "The Pantheon+ Analysis: The Full Data Set and Light-Curve Release", *The Astrophysical Journal*, 938, 113
- **DOI**: 10.3847/1538-4357/ac8b7a
- **arXiv**: 2112.03863
- **URL**: https://github.com/PantheonPlusSH0ES/DataRelease
- **Files**: `data/sne/pantheon_plus/Pantheon+SH0ES.dat`
- **Usage**: SNe domain tests

---

### Galaxy Rotation Curve Data

**SPARC Galaxy Catalog**
- **Dataset**: SPARC Galaxy Rotation Curve Catalog
- **Version**: v2.0
- **Source**: Lelli et al.
- **Citation**: Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016), "SPARC: Mass Models for 175 Disk Galaxies with Spitzer Photometry and Accurate Rotation Curves", *The Astronomical Journal*, 152, 157
- **DOI**: 10.3847/0004-6256/152/6/157
- **arXiv**: 1606.09251
- **URL**: https://www.astro.rug.nl/~sparc/
- **Files**: `data/sparc/sparc_full_catalog.csv`
- **Usage**: SPARC domain tests, dark matter domain tests

---

### Cosmic Microwave Background Data

**Planck 2018 TTTEEE+lowE**
- **Dataset**: Planck 2018 Cosmological Parameters
- **Version**: 2018 TTTEEE+lowE
- **Source**: Planck Collaboration
- **Citation**: Planck Collaboration (2020), "Planck 2018 results. VI. Cosmological parameters", *Astronomy & Astrophysics*, 641, A6
- **DOI**: 10.1051/0004-6361/201833910
- **arXiv**: 1807.06209
- **URL**: https://www.cosmos.esa.int/web/planck/legacy-2018
- **Files**: `data/cosmology/planck_2018.json`
- **Usage**: CMB domain tests, early universe domain tests, LSS domain tests, dark energy domain tests, inflation domain tests

---

### Particle Physics Data

**PDG 2024 Particle Masses**
- **Dataset**: PDG 2024 Review of Particle Physics - Mass Tables
- **Version**: 2024
- **Source**: Particle Data Group
- **Citation**: Workman, R. L., et al. (Particle Data Group) (2024), "Review of Particle Physics", *Progress of Theoretical and Experimental Physics*, 2024, 083C01
- **DOI**: 10.1093/ptep/ptac097
- **URL**: https://pdg.lbl.gov/2024/
- **Files**: `data/pdg/pdg_masses_2024.json`
- **Usage**: Fermion masses, PMNS mixing, CKM mixing, neutrino masses, CP violation, microphysics domain tests

---

### Precision Test Data

**PSR B1913+16 (Hulse-Taylor Binary Pulsar)**
- **Dataset**: PSR B1913+16 Orbital Parameters
- **Version**: Published values
- **Source**: Weisberg & Taylor
- **Citation**: Weisberg, J. M., & Taylor, J. H. (2005), "The Relativistic Binary Pulsar B1913+16: Thirty Years of Observations and Analysis", in *Binary Radio Pulsars*, ASP Conference Series, 328, 25
- **arXiv**: astro-ph/0407149
- **Usage**: Precision tests domain (binary pulsar timing)

**Lunar Laser Ranging Data**
- **Dataset**: Lunar Laser Ranging Constraints
- **Version**: Compilation
- **Source**: Various LLR stations
- **Citation**: Williams, J. G., Turyshev, S. G., & Boggs, D. H. (2014), "The past and present Earth-Moon system: the speed of light stays steady as tides evolve", *Journal of Geophysical Research: Planets*, 119, 1546
- **DOI**: 10.1002/2013JE004755
- **Usage**: Precision tests domain (lunar laser ranging)

**Mercury Perihelion Precession**
- **Dataset**: Mercury Perihelion Precession Observed Value
- **Version**: Observed value
- **Source**: Pitjeva & Pitjev
- **Citation**: Pitjeva, E. V., & Pitjev, N. P. (2018), "Relativistic effects and dark matter in the Solar system from observations of planets and spacecraft", *Astronomy Letters*, 44, 554
- **DOI**: 10.1134/S1063773718080050
- **Usage**: Precision tests domain (Mercury perihelion)

**Cassini Shapiro Time Delay**
- **Dataset**: Cassini Shapiro Time Delay Constraint
- **Version**: 2002-2017
- **Source**: Bertotti et al.
- **Citation**: Bertotti, B., Iess, L., & Tortora, P. (2003), "A test of general relativity using radio links with the Cassini spacecraft", *Nature*, 425, 374
- **DOI**: 10.1038/nature01997
- **Usage**: Precision tests domain (Cassini PPN gamma)

**JPL Ephemeris (Solar System)**
- **Dataset**: JPL Ephemeris DE430/DE440
- **Version**: DE430/DE440
- **Source**: JPL/NASA
- **Citation**: Folkner, W. M., Williams, J. G., Boggs, D. H., Park, R. S., & Kuchynka, P. (2014), "The Planetary and Lunar Ephemerides DE430 and DE431", IPN Progress Report 42-196
- **URL**: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/
- **Usage**: Precision tests domain (solar system ephemeris)

---

## Software Dependencies

### Python Packages

**NumPy**
- **Version**: 2.3.5 (installed)
- **Citation**: Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020), "Array programming with NumPy", *Nature*, 585, 357-362
- **DOI**: 10.1038/s41586-020-2649-2
- **URL**: https://numpy.org/
- **License**: BSD-3-Clause
- **Usage**: Core numerical computations, array operations
- **Alternative Citation**: Oliphant, T. E. (2007), "Python for Scientific Computing", *Computing in Science & Engineering*, 9, 10-20, DOI: 10.1109/MCSE.2007.58

**SciPy**
- **Version**: 1.16.3 (installed)
- **Citation**: Virtanen, P., et al. (2020), "SciPy 1.0: fundamental algorithms for scientific computing in Python", *Nature Methods*, 17, 261-272
- **DOI**: 10.1038/s41592-019-0686-2
- **URL**: https://scipy.org/
- **License**: BSD-3-Clause
- **Usage**: Linear algebra (matrix inversion), numerical integration, optimization

**SymPy**
- **Version**: 1.14.0 (installed)
- **Citation**: Meurer, A., et al. (2017), "SymPy: symbolic computing in Python", *PeerJ Computer Science*, 3, e103
- **DOI**: 10.7717/peerj-cs.103
- **URL**: https://www.sympy.org/
- **License**: BSD-3-Clause
- **Usage**: Symbolic mathematics, matrix exponentials

**CAMB (Code for Anisotropies in the Microwave Background)**
- **Version**: 1.6.5 (installed)
- **Citation**: Lewis, A., Challinor, A., & Lasenby, A. (2000), "Efficient computation of CMB anisotropies in closed FRW models", *The Astrophysical Journal*, 538, 473-476
- **DOI**: 10.1086/309179
- **arXiv**: astro-ph/9911177
- **URL**: https://camb.info/
- **License**: Modified LGPL
- **Usage**: CMB power spectrum computation (optional, fallback available)

**mpmath**
- **Version**: 1.3.0 (installed)
- **Citation**: Johansson, F. (2018), "mpmath: a Python library for arbitrary-precision floating-point arithmetic", version 1.1.0
- **URL**: https://mpmath.org/
- **License**: BSD-3-Clause
- **Usage**: High-precision numerical computations

**pandas**
- **Version**: Listed in requirements.txt (not currently installed in venv)
- **Citation**: McKinney, W. (2010), "Data Structures for Statistical Computing in Python", in *Proceedings of the 9th Python in Science Conference*, 56-61
- **DOI**: 10.25080/Majora-92bf1922-00a
- **URL**: https://pandas.pydata.org/
- **License**: BSD-3-Clause
- **Usage**: SPARC per-galaxy fitter (data manipulation)

---

## Computational Resources

### Python Runtime

**Python**
- **Version**: 3.12.7
- **Citation**: Van Rossum, G., & Drake, F. L. (2009), *Python 3 Reference Manual*, CreateSpace
- **URL**: https://www.python.org/
- **License**: PSF License
- **Usage**: Runtime environment

---

## Reference Data

### Physical Constants

Physical constants (c, G, hbar, etc.) are from:
- **CODATA 2018/2022**: Mohr, P. J., Newell, D. B., & Taylor, B. N. (2016), "CODATA recommended values of the fundamental physical constants: 2014", *Reviews of Modern Physics*, 88, 035009
- **DOI**: 10.1103/RevModPhys.88.035009

### Standard Model Parameters

Standard Model parameters (Higgs VEV, etc.) are from:
- **PDG 2024**: Workman et al. (2024), as cited above

---

## Citation Format

When citing this validation suite, please also cite:

1. **All datasets used** (see above)
2. **Software dependencies** (NumPy, SciPy, SymPy, CAMB)
3. **This validation suite**: UDOF Universal Validation Runner v4.0

---

## License Information

### Dataset Licenses

- **DESI DR1**: Public data release, use with attribution
- **Pantheon+SH0ES**: Public data release, use with attribution
- **SPARC**: Public catalog, use with attribution
- **Planck 2018**: Public data release, use with attribution
- **PDG 2024**: Public data, use with attribution

### Software Licenses

- **NumPy**: BSD-3-Clause
- **SciPy**: BSD-3-Clause
- **SymPy**: BSD-3-Clause
- **CAMB**: Modified LGPL
- **mpmath**: BSD-3-Clause
- **pandas**: BSD-3-Clause
- **Python**: PSF License

---

## Complete Attribution Statement

This validation suite uses:

1. **Observational Data**:
   - DESI DR1 BAO measurements (DESI Collaboration 2024)
   - Pantheon+SH0ES supernova catalog (Scolnic et al. 2022)
   - SPARC galaxy rotation curve catalog (Lelli et al. 2016)
   - Planck 2018 cosmological parameters (Planck Collaboration 2020)
   - PDG 2024 particle masses (Workman et al. 2024)
   - Precision test constraints (various sources, see above)

2. **Software Libraries**:
   - NumPy 2.3.5 (Harris et al. 2020)
   - SciPy 1.16.3 (Virtanen et al. 2020)
   - SymPy 1.14.0 (Meurer et al. 2017)
   - CAMB 1.6.5 (Lewis et al. 2000)
   - mpmath 1.3.0 (Johansson 2018)

3. **Computational Environment**:
   - Python 3.12.7

All datasets and software are used in accordance with their respective licenses and citation requirements.

---

## Notes

- All dataset files are stored in `data/` directory
- Dataset checksums are recorded in `RUN_MANIFEST.json` for reproducibility
- Exact versions of all dependencies are recorded in `RUN_MANIFEST.json`
- For complete dataset citation details, see `integrated_modules/dataset_citations.py`

---

**Last Updated**: 2025-12-17
