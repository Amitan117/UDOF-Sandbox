# Exact Equations Used

This document lists the exact equations evaluated for each test.

**Note**: These are the effective equations actually evaluated, not just references to code.

---

## fermion_masses

### mass_u

1. $m_u = \lambda_0 Y_u v_H / \sqrt{2}$ where $Y_u = \exp(-(a_u \gamma + b_u \sigma))$

### mass_d

1. $m_d = \lambda_0 Y_d v_H / \sqrt{2}$ where $Y_d = \exp(-(a_d \gamma + b_d \sigma))$

### mass_s

1. $m_s = \lambda_0 Y_s v_H / \sqrt{2}$ where $Y_s = \exp(-(a_d \gamma + b_d \sigma + \Delta_a))$

### mass_c

1. $m_c = \lambda_0 Y_c v_H / \sqrt{2}$ where $Y_c = \exp(-(a_u \gamma + b_u \sigma + c_\tau))$

### mass_b

1. $m_b = \lambda_0 Y_b v_H / \sqrt{2}$ where $Y_b = \exp(-(a_d \gamma + b_d \sigma + \Delta_b))$

### mass_t

1. $m_t = \lambda_0 Y_t v_H / \sqrt{2}$ where $Y_t = \exp(-(a_u \gamma + b_u \sigma))$

### mass_e

1. $m_e = \lambda_0 Y_e v_H / \sqrt{2}$ where $Y_e = \exp(-(a_e \gamma + b_e \sigma))$

### mass_mu

1. $m_\mu = \lambda_0 Y_\mu v_H / \sqrt{2}$ where $Y_\mu = \exp(-(a_e \gamma + b_e \sigma + \Delta_a))$

### mass_tau

1. $m_\tau = \lambda_0 Y_\tau v_H / \sqrt{2}$ where $Y_\tau = \exp(-(a_e \gamma + b_e \sigma + c_\tau))$

---

## pmns_mixing

### pmns_theta12

1. $\theta_{12} = \arctan(|U_{e2}/U_{e1}|)$ from PMNS matrix $U$

### pmns_theta23

1. $\theta_{23} = \arcsin(|U_{\mu 3}|)$ from PMNS matrix $U$

### pmns_theta13

1. $\theta_{13} = \arcsin(|U_{e3}|)$ from PMNS matrix $U$

---

## ckm_mixing

### ckm_theta12

1. $\theta_{12}^{CKM} = \arctan(|V_{us}/V_{ud}|)$ from CKM matrix $V$

### ckm_theta23

1. $\theta_{23}^{CKM} = \arctan(|V_{cb}/V_{tb}|)$ from CKM matrix $V$

### ckm_theta13

1. $\theta_{13}^{CKM} = \arcsin(|V_{ub}|)$ from CKM matrix $V$

---

## neutrino_masses

### dm2_21

1. $\Delta m_{21}^2 = m_2^2 - m_1^2$ from neutrino mass eigenvalues

### dm2_31

1. $\Delta m_{31}^2 = m_3^2 - m_1^2$ from neutrino mass eigenvalues

### sum_masses

1. $\sum m_\nu = m_1 + m_2 + m_3$ from neutrino mass eigenvalues

---

## h4_geometry

### h4_trace

1. $\text{Tr}(\Gamma) + \text{Tr}(\Sigma) = 10$ (H4 constraint)

### h4_det_gamma

1. $\det(\Gamma) = 4.1$ (H4 constraint)

### h4_det_sigma

1. $\det(\Sigma) = 2/3$ (H4 constraint)

---

## gauge_symmetry

### gauge_groups

1. Gauge groups derived: SU(3), SU(2), U(1) from collapse dynamics

### lindblad_cp

1. CP symmetry preserved under Lindblad evolution: $\text{Tr}(L^\dagger L \rho) \geq 0$

---

## rg_evolution

### no_landau_poles

1. All coupling constants remain finite for $\mu \in [\mu_0, \mu_{\max}]$

### lambda_min

1. $\lambda_{\min} > 0$ (vacuum stability constraint)

### vacuum_stable

1. $\lambda(\mu) > 0$ for all $\mu$ (no vacuum decay)

### gauge_crossing

1. Gauge couplings cross at unification scale $\mu_{\text{GUT}}$

---

## ward_identities

### charge_conservation

1. $\partial_\mu J^\mu = 0$ (charge conservation from Ward identity)

### photon_mass

1. $m_\gamma = 0$ (photon remains massless, no explicit breaking)

---

## bao

### bao_chi2

1. $\chi^2 = \sum_{i,j} (D_i^{\text{obs}} - D_i^{\text{theory}}) C_{ij}^{-1} (D_j^{\text{obs}} - D_j^{\text{theory}})$ where $D_V(z) = [z D_M^2(z) D_H(z)]^{1/3}$

---

## sne

### sne_chi2

1. $\chi^2 = \sum_i \frac{(\mu_i^{\text{obs}} - \mu_i^{\text{theory}})^2}{\sigma_i^2}$ where $\mu = 5\log_{10}(D_L(z)) + 25$

---

## sparc

### sparc_ese_activation

1. $s(r) = \frac{1}{1 + \exp(-k(\ln X(r) - \ln X_0))}$ where $X(r) = a_0 / g_{\text{bar}}(r)$

### sparc_catalog_loaded

1. SPARC catalog loaded and validated: $N_{\text{galaxies}} > 100$

### sparc_separated_formula

1. $v^2(r) = v_{\text{bar}}^2(r) \times [1 + A \times S_{\text{ESE}}(r)] \times [1 + B \times R_X(k)]$

---

## dark_matter

### ese_galactic

1. $s_{\text{gal}} = \frac{1}{1 + \exp(-k(\ln X_{\text{gal}} - \ln X_0))}$ at galactic scale

### lcdm_recovery

1. $\Omega_{\text{geom}} \to 0$ in LCDM limit (no ESE activation)

### rx_galaxy_scale

1. $R_X(k) = \text{response function}$ computed from $\ell_{\text{eff}}$ variation

---

## dark_energy

### de_dominance

1. $\Omega_\Lambda(z=0) > 0.6$ (dark energy dominance at present)

### w_eos

1. $w(z) = p/\rho$ (equation of state parameter)

---

## early_universe

### cmb_lcdm

1. $s_{\text{CMB}} < 0.01$ (ESE inactive at CMB scale, preserves LCDM)

### bbn_preserved

1. BBN abundances computed from $\eta_B = n_B/n_\gamma$ using UDOF dark sector parameters

---

## lss

### bao_sound_horizon

1. $r_d = \int_0^{z_d} \frac{c_s(z)}{H(z)} dz$ (sound horizon at drag epoch)

### structure_transition

1. $k_{\text{nl}}$ computed from growth factor transition where $\delta(k, z) \sim 1$

### growth_factor_D1

1. $D_1(z) = \text{linear growth factor}$ computed from perturbation theory

### sigma_8

1. $\sigma_8 = \left[\int_0^\infty \frac{dk}{k} \Delta^2(k) W^2(kR) \right]^{1/2}$ with $R = 8 \text{ h}^{-1} \text{ Mpc}$

---

## strong_field

### gr_at_horizon

1. $s(R) \to 0$ in strong-field bandpass, $g_{\mu\nu}^{\text{UDOF}}(r) \approx g_{\mu\nu}^{\text{GR}}(r)$ for $r \sim r_s$

### gw_speed

1. $c_{GW} = c(1 + \Delta(s, \ell_{\text{eff}}))$ with constraint $|c_{GW}/c - 1| < 10^{-15}$

---

## precision_tests

### cassini_ppn_gamma

1. $\gamma_{\text{PPN}} = 1 + s$ with constraint $|\gamma - 1| < 2.3 \times 10^{-5}$

### lunar_ranging

1. $\dot{G}/G = s \times \Lambda_{\text{rate}} / \text{year\_scale}$ with constraint $|\dot{G}/G| < 7 \times 10^{-14} \text{ yr}^{-1}$

### binary_pulsars

1. $\dot{P} = -\frac{192\pi}{5c^5} \left(\frac{2\pi G}{P}\right)^{5/3} \frac{(M_1 M_2)}{(M_1 + M_2)^{1/3}} \frac{1 + \frac{73}{24}e^2 + \frac{37}{96}e^4}{(1-e^2)^{7/2}}$ (Peters & Mathews)

---

## cmb

### cmb_ell_ratio

1. $\ell_{\text{eff}} = \ell_{\text{IR}}$ when $s = 0$ (ESE inactive at CMB scale)

### cmb_power_spectrum

1. $C_\ell^{TT} = \int \frac{dk}{k} \Delta^2_T(k) j_\ell^2(k r_*) $ where $r_*$ is sound horizon

---

## inflation

### spectral_index

1. $n_s = 1 - 6\epsilon + 2\eta$ from slow-roll parameters

### tensor_to_scalar

1. $r = 16\epsilon$ from tensor-to-scalar ratio

### slow_roll_epsilon

1. $\epsilon = \frac{M_P^2}{2}\left(\frac{V'}{V}\right)^2$ (first slow-roll parameter)

### slow_roll_eta

1. $\eta = M_P^2 \frac{V''}{V}$ (second slow-roll parameter)

---

## cp_violation

### ckm_cp_phase

1. $\delta_{\text{CKM}} = 1.0 + \alpha_{\text{CKM}} \times 2.0$ where $\alpha_{\text{CKM}}$ is collapse asymmetry parameter from lock file

### jarlskog_ckm

1. $J_{\text{CKM}} = \text{Im}(V_{ud} V_{cs} V_{us}^* V_{cd}^*)$ where $V$ is CKM matrix with CP phase $\delta_{\text{CKM}}$

### pmns_cp_phase

1. $\delta_{\text{PMNS}} = 1.2 + \alpha_{\text{PMNS}} \times 1.5$ where $\alpha_{\text{PMNS}}$ is collapse asymmetry parameter from lock file

### jarlskog_pmns

1. $J_{\text{PMNS}} = \text{Im}(U_{e1} U_{\mu 2} U_{e2}^* U_{\mu 1}^*)$ where $U$ is PMNS matrix with CP phase $\delta_{\text{PMNS}}$

---

## microphysics

### sm_preserved

1. Standard Model predictions preserved in UDOF framework

---

## gw_ringdown

### qnm_frequency

1. $\omega_{\text{QNM}} = \text{quasinormal mode frequency}$ from black hole perturbation

### qnm_gr_deviation

1. $\Delta \omega = \omega_{\text{UDOF}} - \omega_{\text{GR}}$ (deviation from GR)

---
