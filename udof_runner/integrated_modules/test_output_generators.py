"""
Test Output Generators

Generates structured output following testing standards:
- Summary tables (human readable)
- Raw artifacts (machine readable)
- Exact equations used
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
import numpy as np


@dataclass
class SummaryTableRow:
    """Single row in summary table."""
    test_id: str
    domain: str
    observable: str
    requirement: str
    result: Any
    status: str  # PASS/FAIL

    def to_markdown_row(self) -> str:
        """Convert to markdown table row."""
        result_str = str(self.result)
        if isinstance(self.result, float):
            result_str = f"{self.result:.6e}"
        elif isinstance(self.result, (list, np.ndarray)):
            result_str = "[...]"

        return f"| {self.test_id} | {self.domain} | {self.observable} | {self.requirement} | {result_str} | {self.status} |"


def generate_summary_table(
    test_results: List[SummaryTableRow],
    output_path: Path
) -> str:
    """
    Generate human-readable summary table.

    Returns markdown table string.
    """
    table = """# Test Summary Table

| Test ID | Domain | Observable | Requirement | Result | PASS/FAIL |
| ------- | ------ | ---------- | ----------- | ------ | --------- |
"""

    for row in test_results:
        table += row.to_markdown_row() + "\n"

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(table)

    return table


def save_raw_artifact(
    test_id: str,
    dataset: str,
    lock_hash: str,
    timestamp: str,
    data: Dict[str, Any],
    output_dir: Path,
    artifact_type: str = 'json'
) -> Path:
    """
    Save raw artifact with standardized naming.

    Returns path to saved file.
    """
    from integrated_modules.test_standards_compliance import generate_artifact_filename

    filename = generate_artifact_filename(
        test_id=test_id,
        dataset=dataset,
        lock_hash=lock_hash,
        timestamp=timestamp,
        extension=artifact_type
    )

    output_path = output_dir / filename

    if artifact_type == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    elif artifact_type == 'txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(data))
    else:
        raise ValueError(f"Unknown artifact type: {artifact_type}")

    return output_path


def extract_equations_from_test(test_name: str, domain: str) -> List[str]:
    """
    Extract exact equations used for a test.

    This is a registry of equations for each test. In a full implementation,
    this would be automatically extracted from code or explicitly documented.
    """
    equations_registry = {
        # Collapse: No-signaling
        ('no_signaling', 'collapse_no_signaling'): [
            r"\rho_{AB} = \mathrm{Tr}_E\left[|\Psi\rangle\langle\Psi|\right]",
            r"\rho_B = \mathrm{Tr}_A(\rho_{AB})",
            r"\Delta\rho_B = \|\rho_B^{(\mathrm{before})} - \rho_B^{(\mathrm{after})}\|_1",
            r"\text{Requirement: } \Delta\rho_B < 10^{-15}",
        ],
        # Strong-field: GR limit at horizon (suppression → GR)
        ('gr_at_horizon', 'strong_field'): [
            r"s(R)\to 0 \text{ in strong-field bandpass}",
            r"g_{\mu\nu}^{\mathrm{UDOF}}(r)\approx g_{\mu\nu}^{\mathrm{GR}}(r) \ \text{for } r\sim r_s",
            r"\text{Requirement: fractional deviation} < 10^{-6}",
        ],
        # GW Propagation Speed
        ('gw_speed', 'strong_field'): [
            r"c_{GW} = c \left(1 + \Delta(s, \ell_{\text{eff}})\right)",
            r"\Delta(s, \ell_{\text{eff}}) = s \cdot \frac{\ell_{\text{eff}} \Lambda_{\text{rate}}}{c}",
            r"\text{Constraint: } |c_{GW}/c - 1| < 10^{-15} \text{ (GW170817)}",
        ],

        # Lunar Laser Ranging
        ('lunar_ranging', 'precision_tests'): [
            r"\dot{G}/G = s \cdot \frac{\Lambda_{\text{rate}}}{\text{year\_scale}}",
            r"\text{Constraint: } |\dot{G}/G| < 7 \times 10^{-14} \text{ yr}^{-1}",
            r"\text{At Solar System: } s \to 0 \Rightarrow \dot{G}/G \to 0",
        ],

        # Mercury Perihelion
        ('mercury_perihelion', 'precision_tests'): [
            r"\Delta\omega = \frac{6\pi GM}{c^2 a (1-e^2)} \text{ per orbit}",
            r"\text{GR prediction: } 43.0 \text{ arcsec/century}",
            r"\text{UDOF (s→0): } \Delta\omega_{\text{UDOF}} = \Delta\omega_{\text{GR}}",
        ],

        # Binary Pulsar
        ('binary_pulsars', 'precision_tests'): [
            r"\dot{P} = -\frac{192\pi}{5c^5} \left(\frac{2\pi G}{P}\right)^{5/3} \frac{(M_1 M_2)}{(M_1 + M_2)^{1/3}} \frac{1 + \frac{73}{24}e^2 + \frac{37}{96}e^4}{(1-e^2)^{7/2}}",
            r"\text{UDOF (s→0): } \dot{P}_{\text{UDOF}} = \dot{P}_{\text{GR}}",
        ],

        # 3-Body Sun-Earth-Moon
        ('three_body_sun_earth_moon', 'precision_tests'): [
            r"\frac{d^2 \mathbf{r}_i}{dt^2} = \sum_{j \neq i} G M_j \frac{\mathbf{r}_j - \mathbf{r}_i}{|\mathbf{r}_j - \mathbf{r}_i|^3}",
            r"E = T + U = \sum_i \frac{1}{2} M_i v_i^2 - \sum_{i<j} \frac{G M_i M_j}{|\mathbf{r}_i - \mathbf{r}_j|}",
            r"\delta a / a = \frac{|a_{\text{final}} - a_{\text{initial}}|}{a_{\text{initial}}}",
            r"\text{Stability: } \delta a_{\text{Earth-Sun}} < 0.0001, \delta a_{\text{Moon-Earth}} < 0.005",
        ],

        # BBN
        ('bbn_preserved', 'early_universe'): [
            r"Y_p = 0.2470 + 0.0136 \ln(\eta_B / 6.1 \times 10^{-10}) + 0.008 \ln(N_{\text{eff}} / 3.046)",
            r"\log(D/H) = -4.594 + 0.135 \ln(\eta_B / 6.1 \times 10^{-10})",
            r"\log(\text{Li}^7/\text{H}) = -9.99 + 0.5 \ln(\eta_B / 6.1 \times 10^{-10})",
        ],

        # SPARC
        ('sparc_separated_formula', 'sparc'): [
            r"v^2(r) = v_{\text{bar}}^2(r) \left[1 + A S_{\text{ESE}}(r)\right] \left[1 + B R_X(k)\right]",
            r"S_{\text{ESE}}(r) = \int_0^r \frac{ds}{dr'} dr'",
            r"X(r) = \frac{a_0}{g_{\text{bar}}(r)}",
            r"s(X) = \frac{1}{1 + \exp(-k (\ln X - \ln X_0))}",
        ],
        ('sparc_ese_activation', 'sparc'): [
            r"\Sigma_b \approx \frac{M_b}{\pi R^2}",
            r"X = (\Sigma_b/\Sigma_0)^{\eta_*}(\sigma_g/\sigma_0)^p",
            r"s(X)=\frac{1}{1+\exp(-k(\ln X-\ln X_0))}\cdot B(R)",
            r"\text{Requirement: median}(s) > 0.5",
        ],
        ('sparc_catalog_loaded', 'sparc'): [
            r"N_{\mathrm{rows}}(\mathrm{catalog}) > 100",
        ],

        # σ₈
        ('sigma_8', 'lss'): [
            r"\sigma_8^2 = \int_0^\infty P(k) W^2(kR) k^2 dk",
            r"W(kR) = \frac{3(\sin(kR) - kR\cos(kR))}{(kR)^3}",
            r"R = 8 h^{-1} \text{ Mpc}",
        ],

        # LSS Transition
        ('structure_transition', 'lss'): [
            r"D(z) = \int_{z}^{\infty} \frac{1 + z'}{H(z')} dz'",
            r"H(z) = H_0 \sqrt{\Omega_m (1+z)^3 + \Omega_\Lambda}",
            r"f\sigma_8(z) = \frac{d\ln D}{d\ln a} \sigma_8(z)",
        ],
        ('growth_factor_D1', 'lss'): [
            r"D'' + \left[2 + \frac{d\ln H}{d\ln a}\right] D' - \frac{3}{2}\mu_{\mathrm{eff}}(a)\Omega_{\mathrm{cl}}(a)D = 0",
            r"\Omega_{\mathrm{cl}}(a)=\Omega_b(a)+\xi(a)\Omega_{\mathrm{geom}}(a)",
            r"D(0)=1",
        ],

        # Cassini PPN γ
        ('cassini_ppn_gamma', 'precision_tests'): [
            r"\gamma_{\text{PPN}} = 1 + s",
            r"s = \frac{1}{1 + \exp(-k (\ln X - \ln X_0))} \cdot B(R)",
            r"B(R) = 0 \text{ when } \sigma_g < 1000 \text{ m/s}",
            r"\text{Constraint: } |\gamma - 1| < 2.3 \times 10^{-5} \text{ (Cassini)}",
        ],

        # BAO
        ('bao_chi2', 'bao'): [
            r"D_V(z) = \left[z D_M^2(z) D_H(z)\right]^{1/3}",
            r"D_M(z) = \int_0^z \frac{c}{H(z')} dz'",
            r"D_H(z) = \frac{c}{H(z)}",
            r"\chi^2 = \sum_{i,j} (O_i - T_i) C_{ij}^{-1} (O_j - T_j)",
        ],
        ('bao_sound_horizon', 'bao'): [
            r"r_d = \int_{z_d}^{\infty} \frac{c_s(z)}{H(z)} dz",
            r"c_s(z)=\frac{c}{\sqrt{3(1+R_b(z))}}",
            r"\text{Runner uses locked } r_d \text{ from master lock}",
        ],

        # SNe
        ('sne_chi2', 'sne'): [
            r"\mu(z) = 5\log_{10}(D_L(z)) + 25",
            r"D_L(z) = (1+z) D_M(z)",
            r"D_M(z) = \int_0^z \frac{c}{H(z')} dz'",
            r"\chi^2 = \sum_i \left(\frac{\mu_{\text{obs},i} - \mu_{\text{pred},i}}{\sigma_i}\right)^2",
        ],

        # CMB Power Spectrum
        ('cmb_power_spectrum', 'cmb'): [
            r"C_\ell = \int_0^\infty k^2 dk P(k) \left|\int_0^{\chi_*} d\chi W(\chi) j_\ell(k\chi)\right|^2",
            r"\ell_A = \pi \frac{r_s(z_*)}{D_A(z_*)}",
            r"D_A(z) = \frac{c}{1+z} \int_0^z \frac{dz'}{H(z')}",
        ],
        ('cmb_lcdm', 'cmb'): [
            r"s\to 0 \Rightarrow \ell_{\mathrm{eff}}=\ell_{\mathrm{IR}}",
            r"\text{Requirement: } |\ell_{\mathrm{eff}}/\ell_{\mathrm{IR}}-1|<10^{-6}",
        ],

        # Inflation
        ('spectral_index', 'inflation'): [
            r"n_s = 1 - 2\epsilon - \eta",
            r"\epsilon = \frac{3}{4N^2}",
            r"\eta = -\frac{1}{N}",
        ],
        ('slow_roll_r', 'inflation'): [
            r"r = 16\epsilon",
            r"\epsilon = \frac{M_{\text{Pl}}^2}{2}\left(\frac{V'}{V}\right)^2",
        ],
        ('slow_roll_eps', 'inflation'): [
            r"\epsilon = \frac{3}{4N^2}",
            r"N = \int_{\phi_i}^{\phi_f} \frac{d\phi}{M_{\text{Pl}} \sqrt{2\epsilon}}",
        ],
        ('slow_roll_eta', 'inflation'): [
            r"\eta = -\frac{1}{N}",
            r"\eta = M_{\text{Pl}}^2 \frac{V''}{V}",
        ],

        # CP Violation
        ('ckm_cp_phase', 'cp_violation'): [
            r"\delta_{\text{CKM}} = \arg(V_{ud} V_{cb} V_{ub}^* V_{cd}^*)",
            r"J_{\text{CKM}} = \text{Im}(V_{ud} V_{cs} V_{us}^* V_{cd}^*)",
        ],
        ('jarlskog_pmns', 'cp_violation'): [
            r"\delta_{\text{PMNS}} = \arg(U_{e1} U_{\mu2} U_{e2}^* U_{\mu1}^*)",
            r"J_{\text{PMNS}} = \text{Im}(U_{e1} U_{\mu2} U_{e2}^* U_{\mu1}^*)",
        ],

        # Fermion Masses
        ('fermion_masses', 'fermion_masses'): [
            r"m_i = m_0 \cdot f_i(\text{TSI parameters})",
            r"f_i \text{ from H4 geometry and gauge structure}",
        ],

        # PMNS Mixing
        ('pmns_mixing', 'pmns_mixing'): [
            r"U_{\text{PMNS}} = \exp(i \theta_{ij} \sigma_{ij})",
            r"\theta_{ij} \text{ from TSI commutator structure}",
        ],

        # CKM Mixing
        ('ckm_mixing', 'ckm_mixing'): [
            r"V_{\text{CKM}} = \exp(i \theta_{ij} \sigma_{ij})",
            r"\theta_{ij} \text{ from TSI commutator structure (scaled)}",
        ],

        # Neutrino Masses
        ('neutrino_masses', 'neutrino_masses'): [
            r"\Delta m_{ij}^2 = m_i^2 - m_j^2",
            r"m_i \text{ from TSI neutrino parameters}",
        ],

        # H4 Geometry
        ('h4_geometry', 'h4_geometry'): [
            r"\text{Tr}(\gamma) = 10",
            r"\det(\gamma) = 4.1",
            r"\det(\sigma) = 2/3",
        ],
        # RG evolution (runner-level summaries)
        ('lambda_min', 'rg_evolution'): [
            r"\frac{d\lambda}{d\ln\mu}=\beta_\lambda^{(1)}+\beta_\lambda^{(2)}",
            r"\text{Requirement: } \min_\mu \lambda(\mu) > 0",
        ],
        ('gauge_crossing', 'rg_evolution'): [
            r"\frac{dg_i}{d\ln\mu}=\beta_{g_i}^{(1)}+\beta_{g_i}^{(2)}",
            r"\mu:\ g_2(\mu)=g_3(\mu)\ (\text{pair crossing})",
        ],
    }

    key = (test_name, domain)
    return equations_registry.get(key, [f"Equation extraction not yet implemented for {test_name}"])


def generate_equations_document(
    test_results: List[Dict[str, Any]],
    output_path: Path
) -> str:
    """
    Generate document with exact equations used for each test.

    Returns markdown string.
    """
    doc = """# Exact Equations Used

This document lists the exact equations evaluated for each test.

**Note**: These are the effective equations actually evaluated, not just references to code.

---

"""

    for result in test_results:
        test_name = result.get('test_name', 'UNKNOWN')
        domain = result.get('domain', 'UNKNOWN')
        equations = result.get('equations', [])

        if not equations:
            equations = extract_equations_from_test(test_name, domain)

        doc += f"## {test_name} ({domain})\n\n"

        if equations:
            for i, eq in enumerate(equations, 1):
                doc += f"{i}. ${eq}$\n\n"
        else:
            doc += "*Equations not yet documented*\n\n"

        doc += "---\n\n"

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(doc)

    return doc


def create_test_output_structure(
    run_id: str,
    output_base: Path,
    manifest: Dict[str, Any]
) -> Dict[str, Path]:
    """
    Create directory structure for test outputs.

    Returns dict mapping output type to path.
    """
    lock_hash_short = manifest['master_lock']['sha256'][:
                                                        8] if manifest['master_lock']['sha256'] != 'NOT_FOUND' else 'NOHASH'
    timestamp = manifest['run_timestamp'].replace(
        ':', '-').replace('T', '_').split('.')[0]

    # Create directories
    run_dir = output_base / f"run_{run_id}_{lock_hash_short}_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    plots_dir = run_dir / "plots"
    plots_dir.mkdir(exist_ok=True)

    logs_dir = run_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    return {
        'run_dir': run_dir,
        'artifacts_dir': artifacts_dir,
        'plots_dir': plots_dir,
        'logs_dir': logs_dir,
        'summary_table': run_dir / "SUMMARY_TABLE.md",
        'equations_doc': run_dir / "EQUATIONS_USED.md",
        'manifest': run_dir / "RUN_MANIFEST.md",
    }
