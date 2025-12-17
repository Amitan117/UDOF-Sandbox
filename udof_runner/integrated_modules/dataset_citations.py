"""
Dataset Citations Registry

Complete registry of all datasets used in validation tests with exact names,
versions, sources, and citations.

This ensures full traceability and reproducibility.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DatasetCitation:
    """Complete citation information for a dataset."""
    name: str  # Exact dataset name
    version: str  # Exact version/release
    source: str  # Source organization/authors
    citation: str  # Full citation string
    doi: Optional[str] = None
    arxiv: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None  # Relative path in data/ directory


# Complete dataset citation registry
DATASET_CITATIONS: Dict[str, DatasetCitation] = {
    # BAO Data
    'desi_bao_mean': DatasetCitation(
        name='DESI DR1 BAO Mean Measurements',
        version='DR1',
        source='DESI Collaboration',
        citation='DESI Collaboration (2024), arXiv:2404.03002',
        arxiv='2404.03002',
        url='https://data.desi.lbl.gov/public/edr/vac/edr/bao/',
        file_path='bao/desi_dr1_all/mean.txt'
    ),
    'desi_bao_cov': DatasetCitation(
        name='DESI DR1 BAO Covariance Matrix',
        version='DR1',
        source='DESI Collaboration',
        citation='DESI Collaboration (2024), arXiv:2404.03002',
        arxiv='2404.03002',
        url='https://data.desi.lbl.gov/public/edr/vac/edr/bao/',
        file_path='bao/desi_dr1_all/cov.txt'
    ),

    # Supernova Data
    'pantheon_plus': DatasetCitation(
        name='Pantheon+SH0ES',
        version='Pantheon+SH0ES',
        source='Scolnic et al.',
        citation='Scolnic et al. (2022), ApJ 938, 113',
        doi='10.3847/1538-4357/ac8b7a',
        arxiv='2112.03863',
        url='https://github.com/PantheonPlusSH0ES/DataRelease',
        file_path='sne/pantheon_plus/Pantheon+SH0ES.dat'
    ),

    # SPARC Galaxy Data
    'sparc_catalog': DatasetCitation(
        name='SPARC Galaxy Rotation Curve Catalog',
        version='v2.0',
        source='Lelli et al.',
        citation='Lelli et al. (2016), AJ 152, 157',
        doi='10.3847/0004-6256/152/6/157',
        arxiv='1606.09251',
        url='https://www.astro.rug.nl/~sparc/',
        file_path='sparc/sparc_full_catalog.csv'
    ),

    # CMB Data
    'planck_2018': DatasetCitation(
        name='Planck 2018 TTTEEE+lowE',
        version='2018 TTTEEE+lowE',
        source='Planck Collaboration',
        citation='Planck Collaboration (2020), A&A 641, A6',
        doi='10.1051/0004-6361/201833910',
        arxiv='1807.06209',
        url='https://www.cosmos.esa.int/web/planck/legacy-2018',
        file_path='cosmology/planck_2018.json'
    ),

    # Particle Data
    'pdg_masses': DatasetCitation(
        name='PDG 2024 Particle Masses',
        version='2024',
        source='Particle Data Group',
        citation='Workman et al. (2024), PTEP 2024, 083C01',
        doi='10.1093/ptep/ptac097',
        url='https://pdg.lbl.gov/2024/',
        file_path='pdg/pdg_masses_2024.json'
    ),

    # Solar System Data (for precision tests)
    'solar_system_ephemeris': DatasetCitation(
        name='JPL Ephemeris (DE430/DE440)',
        version='DE430/DE440',
        source='JPL/NASA',
        citation='Folkner et al. (2014), IPN Progress Report 42-196',
        url='https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/',
        file_path=None  # Not stored, computed from constants
    ),

    # Binary Pulsar Data
    'psr_b1913_16': DatasetCitation(
        name='PSR B1913+16 (Hulse-Taylor)',
        version='Published values',
        source='Weisberg & Taylor (2005)',
        citation='Weisberg & Taylor (2005), ASP Conf. Ser. 328, 25',
        arxiv='astro-ph/0407149',
        file_path=None  # Published parameters, not a file
    ),

    # Lunar Laser Ranging
    'llr_data': DatasetCitation(
        name='Lunar Laser Ranging Data',
        version='Compilation',
        source='Various LLR stations',
        citation='Williams et al. (2014), J. Geophys. Res. Planets 119, 1546',
        doi='10.1002/2013JE004755',
        file_path=None  # Compiled constraints, not raw data file
    ),

    # Mercury Perihelion
    'mercury_ephemeris': DatasetCitation(
        name='Mercury Perihelion Precession',
        version='Observed value',
        source='Pitjeva & Pitjev (2018)',
        citation='Pitjeva & Pitjev (2018), Astron. Lett. 44, 554',
        doi='10.1134/S1063773718080050',
        file_path=None  # Published value, not a file
    ),

    # Cassini Shapiro Delay
    'cassini_data': DatasetCitation(
        name='Cassini Shapiro Time Delay',
        version='2002-2017',
        source='Bertotti et al. (2003)',
        citation='Bertotti et al. (2003), Nature 425, 374',
        doi='10.1038/nature01997',
        file_path=None  # Published constraint, not raw data
    ),
}


# Mapping of test domains to datasets used
TEST_DATASET_MAPPING: Dict[str, List[str]] = {
    'bao': ['desi_bao_mean', 'desi_bao_cov'],
    'sne': ['pantheon_plus'],
    'sparc': ['sparc_catalog'],
    'cmb': ['planck_2018'],
    'fermion_masses': ['pdg_masses'],
    'pmns_mixing': ['pdg_masses'],
    'ckm_mixing': ['pdg_masses'],
    'neutrino_masses': ['pdg_masses'],
    'precision_tests': ['solar_system_ephemeris', 'llr_data', 'psr_b1913_16', 'mercury_ephemeris', 'cassini_data'],
    'early_universe': ['planck_2018'],  # BBN uses cosmological parameters
    'lss': ['planck_2018'],  # Uses cosmological parameters
    'cp_violation': ['pdg_masses'],
    # Theoretical/computed tests don't use external datasets
    'h4_geometry': [],
    'gauge_symmetry': [],
    'rg_evolution': [],
    'ward_identities': [],
    'dark_matter': ['sparc_catalog'],  # Uses SPARC for validation
    'dark_energy': ['planck_2018'],  # Uses cosmological parameters
    'inflation': ['planck_2018'],  # Uses CMB constraints
    'microphysics': ['pdg_masses'],
    'gw_ringdown': [],  # Theoretical computation
    'quantum_gravity': [],  # Theoretical computation
    'baryogenesis': ['pdg_masses'],
    'master_action': [],  # Theoretical computation
    'strong_field': [],  # Theoretical computation
}


def get_datasets_for_test(domain: str) -> List[DatasetCitation]:
    """Get all datasets used by a test domain."""
    dataset_keys = TEST_DATASET_MAPPING.get(domain, [])
    return [DATASET_CITATIONS[key] for key in dataset_keys if key in DATASET_CITATIONS]


def get_dataset_citation(dataset_key: str) -> Optional[DatasetCitation]:
    """Get citation for a specific dataset."""
    return DATASET_CITATIONS.get(dataset_key)


def format_dataset_citation(dataset: DatasetCitation) -> str:
    """Format dataset citation as string."""
    parts = [f"{dataset.name} ({dataset.version})"]
    if dataset.source:
        parts.append(f"Source: {dataset.source}")
    if dataset.citation:
        parts.append(f"Citation: {dataset.citation}")
    if dataset.doi:
        parts.append(f"DOI: {dataset.doi}")
    if dataset.arxiv:
        parts.append(f"arXiv: {dataset.arxiv}")
    return " | ".join(parts)
