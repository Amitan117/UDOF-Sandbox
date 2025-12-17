"""
Domain modules registry for UDOF validation.

Each domain module exports a single `run(ctx)` function that takes a DomainContext
and returns a DomainResult.
"""

from typing import Dict, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .context import DomainContext
    from integrated_modules.types import DomainResult

# Import domain modules
from .fermion_masses import run as run_fermion_masses
from .pmns_mixing import run as run_pmns_mixing
from .ckm_mixing import run as run_ckm_mixing
from .neutrino_masses import run as run_neutrino_masses
from .h4_geometry import run as run_h4_geometry
from .gauge_symmetry import run as run_gauge_symmetry
from .rg_evolution import run as run_rg_evolution
from .ward_identities import run as run_ward_identities
from .bao import run as run_bao
from .sne import run as run_sne
from .sparc import run as run_sparc
from .dark_matter import run as run_dark_matter
from .dark_energy import run as run_dark_energy
from .early_universe import run as run_early_universe
from .lss import run as run_lss
from .strong_field import run as run_strong_field
from .precision_tests import run as run_precision_tests
from .cmb import run as run_cmb
from .inflation import run as run_inflation
from .cp_violation import run as run_cp_violation
from .microphysics import run as run_microphysics
from .gw_ringdown import run as run_gw_ringdown

# Domain registry
# Maps domain name to run function: run(DomainContext) -> DomainResult
DOMAIN_REGISTRY: Dict[str, Callable[['DomainContext'], 'DomainResult']] = {
    'fermion_masses': run_fermion_masses,
    'pmns_mixing': run_pmns_mixing,
    'ckm_mixing': run_ckm_mixing,
    'neutrino_masses': run_neutrino_masses,
    'h4_geometry': run_h4_geometry,
    'gauge_symmetry': run_gauge_symmetry,
    'rg_evolution': run_rg_evolution,
    'ward_identities': run_ward_identities,
    'bao': run_bao,
    'sne': run_sne,
    'sparc': run_sparc,
    'dark_matter': run_dark_matter,
    'dark_energy': run_dark_energy,
    'early_universe': run_early_universe,
    'lss': run_lss,
    'strong_field': run_strong_field,
    'precision_tests': run_precision_tests,
    'cmb': run_cmb,
    'inflation': run_inflation,
    'cp_violation': run_cp_violation,
    'microphysics': run_microphysics,
    'gw_ringdown': run_gw_ringdown,
}

