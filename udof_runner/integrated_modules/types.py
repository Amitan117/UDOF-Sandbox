"""
Shared types for domain modules.
"""

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class TestResult:
    test_name: str
    status: str  # PASS, FAIL, ERROR, SKIP, THEORETICAL
    value: Any
    expected: Any = None
    error: float = None
    chi2: float = None
    notes: str = ""


@dataclass
class DomainResult:
    domain_name: str
    n_pass: int = 0
    n_fail: int = 0
    n_error: int = 0
    n_skip: int = 0
    n_theoretical: int = 0
    tests: List[TestResult] = field(default_factory=list)
    chi2_total: float = None

