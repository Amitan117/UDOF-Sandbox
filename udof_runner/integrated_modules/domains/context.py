"""
DomainContext - provides context to domain modules.

This is a simple dataclass that provides all the information a domain module
needs to run its tests, without requiring direct access to the runner.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from integrated_modules.core.formulas import UDOFFormulas
from integrated_modules.data.loaders import DataLoader


@dataclass
class DomainContext:
    """Context provided to domain modules."""
    locks: Dict
    data_root: Path
    formulas: UDOFFormulas
    data_loader: DataLoader
    cosmology_method: str = 'proper'
    use_rx: bool = True
    sparc_formula: str = 'separated'
    sparc_b_prediction: bool = False

