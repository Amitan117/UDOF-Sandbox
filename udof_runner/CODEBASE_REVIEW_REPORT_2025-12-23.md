# UDOF Runner Codebase Review Report (Sandbox)
**Date:** 2025-12-23  
**Scope root:** `udof_runner/` (sandbox directory)  
**Primary request:** Identify incomplete/stub/placeholder code, TODOs, and deviations from README “standards compliance”; assess whether issues impact tests/results and whether any hard-coded values bypass locks/parameters.

---

## Executive summary

### What is incomplete (actionable)
- **Dead/unused stubs exist in-repo**: `integrated_modules/core/{cosmology,tsi,lss,ese}.py` are explicit migration placeholders that raise `NotImplementedError`. They are not imported by the runner/domains today, but they contradict “complete implementation” claims and can become future runtime failures if someone imports them.
- **Unresolved TODO in production runner**: `udof_validation_runner_v4.0.py` includes a TODO indicating CKM parameters are defaults and “need optimization” for “sandbox perfect matches.”
- **Lock bypass / hard-coded physics inputs exist**: several critical physics parameters are **hard-coded** (or defaulted) outside the lock system. These can materially affect test outcomes if lock contents differ or if you consider these values “parameters” that should be lock-frozen.

### What is impacting results today (highest signal)
1. **Hard-coded `Omega_b` and `n_s` in domains/formulas**  
   - `Omega_b=0.046` and `n_s=0.965` are used in the CMB and σ₈ logic as constants, not read from locks or Planck JSON.
   - `Omega_b=0.046` is hard-coded inside `UDOFFormulas.growth_factor()` and `UDOFFormulas.compute_R_X()` (proper-growth and response derivation paths).
2. **Hard-coded ESE calibration fallbacks** (`ell_IR`, `ell_star`, `eta_star`, `X0`)  
   - If lock files omit these fields, the code falls back to defaults in `DEFAULT_LOCKS`, and in some conversion logic.
3. **Hard-coded astrophysical modeling constants in SPARC**  
   - M/L ratio, overdensity, sample-size caps, and wavenumber constants are hard-coded and can influence pass/fail and computed medians.

### What is not impacting results today (but is a standards risk)
- The migration stub modules (`integrated_modules/core/*.py`) are **not imported** in current execution paths.
- A skeleton registry module (`integrated_modules/data/registry.py`) is not referenced by the runner/data loader and therefore doesn’t affect current runs.
- Some “standards artifacts” (manifest/equations docs) can fail silently due to `pass` on exceptions; that doesn’t change physics results but can undermine “trace completeness.”

---

## Methodology & boundaries

### Reviewed
- `udof_runner/udof_validation_runner_v4.0.py` (runner + lock loading)
- `udof_runner/integrated_modules/**` (domains, formulas, standards, utilities)
- README/standards statements in `udof_runner/README.md`, `udof_runner/data/README.md`, `udof_runner/data/MANIFEST.md`

### Automated search signals used
- TODO-like markers: `TODO`, `FIXME`, `TBD`, `XXX`, `WIP`
- Stubs/placeholders: `raise NotImplementedError`, empty registries, bare `pass` in exception handlers
- Lock bypass patterns: “Standard value”, “fallback”, hard-coded constants (`0.046`, `0.965`, `4.7e-5`, `2e-15`, etc.)

### Note on third-party noise
The repository currently contains a tracked virtualenv and compiled artifacts, which means “whole-repo TODO scan” returns many third-party TODOs and stubs. This report focuses on **your maintained source** in `udof_runner/` and explicitly ignores third-party packages.

---

## Findings: incomplete / TODO / placeholder code

### 1) Explicit migration stubs raising `NotImplementedError` (unused today)
These modules self-identify as “to be populated during migration” and raise `NotImplementedError` for core functions:
- `integrated_modules/core/cosmology.py`
  - TODO migration notes and stubs: `hubble_parameter`, `distance_calculations`, `bao_helpers`.
- `integrated_modules/core/tsi.py`
  - TODO migration notes and stubs: `tsi_geometry`, `projectors`.
- `integrated_modules/core/lss.py`
  - TODO migration notes and stubs: `growth_factor`, `rx_calculations`, `sigma8_hooks`.
- `integrated_modules/core/ese.py`
  - TODO migration notes and stubs: `x_definition`, `s_parameter`, `bandpass`.

**Trace / impact**
- Current runner imports `integrated_modules.core.formulas.UDOFFormulas` (not these modules). A search for `integrated_modules.core.cosmology|lss|ese|tsi` imports in runner/domains returns **no matches**.
- **Impact today:** none (dead code).  
- **Impact risk:** if these modules are imported by future code (or referenced by README claims), they will hard-crash.

**Resolution options**
- Remove them (if not part of your intended API), or
- Complete the migration by moving the real implementations from `core/formulas.py` into these modules and wiring imports accordingly.

### 2) Data registry skeleton (unused today)
- `integrated_modules/data/registry.py` defines empty `DATASET_PATHS` and `EXPECTED_FILES` dicts with TODOs to populate, plus accessors that raise `KeyError` until populated.

**Trace / impact**
- No code references `DATASET_PATHS`, `EXPECTED_FILES`, `get_dataset_path()`, or `get_expected_files()` outside this file.
- **Impact today:** none.  
- **Impact risk:** if later adopted by `DataLoader` or standards checks, it will fail until populated.

### 3) TODO indicating known parameter gap in runner (CKM)
- In `udof_validation_runner_v4.0.py`, a TODO states CKM parameters aren’t in master lock format, defaults are used, and optimization/extraction is needed to match “sandbox perfect matches.”

**Trace / impact**
- `UDOFFormulas.__init__` reads CKM parameters from `locks['fermion_masses']['ckm_mixing_parameters']` if present; otherwise it falls back to hard-coded defaults.
- **Impact today:** CKM-domain tests can pass/fail depending on whether the lock includes optimized CKM parameters. If locks omit them, the defaults are used.
- **Standards impact:** this contradicts “fully complete” if you consider “perfect matches” part of the expected standards baseline.

### 4) “Derive from first principles” TODO in baryogenesis
- `integrated_modules/baryo_complete_leptogenesis.py` contains a TODO to derive an early-universe enhancement factor from first principles.

**Trace / impact**
- The factor is taken from `locks['baryogenesis_parameters']['f_baryogenesis_specific']` (defaults exist in `DEFAULT_LOCKS`).
- **Impact today:** baryogenesis results depend on that calibrated factor; the TODO is about theoretical derivation, not runtime completeness.

---

## Findings: lock/parameter compliance and hard-coded values (active)

### A) Runner establishes a lock system, but includes non-lock “physics knobs”

#### A1) Lock loading behavior
- `udof_validation_runner_v4.0.py` defines a large `DEFAULT_LOCKS` dict (fallback parameter set).
- `load_locks()` loads a master lock from sandbox if present; otherwise loads unified lock; otherwise errors (sandbox-only).

**Impact**
- If any fields are missing from the lock(s), defaults may be used, which can change test outputs silently unless validated.

#### A2) Unused conversion path still embeds hard-coded ESE defaults
- `convert_master_lock_to_unified()` includes hard-coded ESE defaults:
  - `ell_IR = 4.7e-5`, `ell_star = 2e-15`, `eta_star = 0.171`
- This function is currently **not used** by `load_locks()` (the code directly maps master-lock sections).

**Impact**
- Not affecting current results, but the presence of hard-coded ESE values in a conversion helper can reintroduce lock bypass if re-enabled later.

### B) Hard-coded values used in active numerical paths (can affect results)

#### B1) `Omega_b` hard-coded inside core formulas (affects “proper” growth + R_X)
File: `integrated_modules/core/formulas.py`
- `UDOFFormulas.growth_factor(... use_proper=True)` instantiates `ProperCorrectedGrowth` with:
  - `Omega_b=0.046` (hard-coded)
  - other non-lock constants: `a_pivot=0.95`, `beta_ESE=-0.10`, `use_mu_eff=True`
- `UDOFFormulas.compute_R_X(...)` instantiates `TSESEResponseDerivation` with:
  - `Omega_b=0.046` (hard-coded)

**Potential impacts**
- If your lock system is expected to freeze baryon density, `Omega_b` being hard-coded violates that standard.
- This can shift growth-factor predictions and any tests that depend on them.
- `compute_R_X` falls back to `1.0` on any ImportError/Exception; disabling that path can change results (becoming “no suppression”).

#### B2) `Omega_b` and `n_s` hard-coded in LSS σ₈ test
File: `integrated_modules/domains/lss.py`
- σ₈ computation uses:
  - `Ob = 0.046` (hard-coded)
  - `n_s = 0.965` (hard-coded)
  - It reads Planck JSON only for σ₈ reference value, not for `Omega_b` or `n_s`.

**Potential impacts**
- If your Planck dataset or locks specify different `Omega_b` or `n_s`, σ₈ computation is not aligned with frozen configuration.
- Results may be stable across runs (reproducible), but not necessarily correct “per-lock.”

#### B3) `Omega_b` and `n_s` hard-coded in CMB test
File: `integrated_modules/domains/cmb.py`
- Uses:
  - `Ob = 0.046` (hard-coded)
  - `n_s = 0.965` (hard-coded)

**Potential impacts**
- Same lock-bypass risk as LSS; can move peak behavior in the simplified internal model.

#### B4) Hard-coded astrophysical modeling constants in SPARC test
File: `integrated_modules/domains/sparc.py`
- Hard-coded modeling assumptions affecting computed `s` median and pass/fail:
  - Stellar mass-to-light ratio: `M/L ~ 0.5`
  - Overdensity: `delta = 1e5`
  - Sample-size caps: `[:50]`, `[:10]`
  - Galaxy-scale `k_gal = 0.5`

**Potential impacts**
- These choices can alter the distribution of computed `s` and the median threshold comparison.
- If your standard requires all such knobs be lock-frozen, these violate that.

---

## Findings: standards artifacts & trace completeness robustness

### 1) Manifest generation can silently degrade
File: `integrated_modules/standards/runtime.py`
- Several exception handlers use `pass` (e.g., git hash lookup; dependency detection; manifest write). In particular, manifest write failure is swallowed.

**Impact**
- Physics results unchanged, but “complete reproducibility metadata” may be missing without a loud failure.

### 2) Equations documentation can degrade to placeholders
File: `integrated_modules/standards/equations_generator.py`
- If a test isn’t mapped, it emits a generic placeholder (“Equation extracted…”).
- Write failures are swallowed.

**Impact**
- Produces `EQUATIONS_USED.md`, but not guaranteed to contain exact equations for all tests nor guaranteed to exist on disk if write fails.

---

## Repository hygiene issues (auditability & future maintenance)

These magnify review noise and can hide real TODOs behind third-party ones:
- **Tracked virtual environment**: `udof_runner/venv/` contains thousands of tracked files.
- **Tracked compiled artifacts**: thousands of tracked `*.pyc`.
- **Tracked run outputs**: `udof_runner/run_results/**` contains historical generated outputs tracked in git.

**Impact**
- Whole-repo scans for TODO/NotImplemented will be dominated by third-party packages and generated artifacts.
- Risk of committing machine-specific build artifacts.
- Larger repo size and slower tooling.

---

## Impact matrix (what could change tests/results)

| Finding | Active in current run? | Can change numeric results? | Can change PASS/FAIL? | Standards compliance risk? | Notes |
|---|---:|---:|---:|---:|---|
| `integrated_modules/core/*` NotImplemented stubs | No | No | No | Yes | Future crash risk if imported |
| CKM TODO / default CKM parameters | Yes | Yes | Yes | Yes | Depends on lock completeness |
| Hard-coded `Omega_b=0.046` in growth_factor/R_X | Yes (when used) | Yes | Yes | Yes | Bypasses lock-specified `Omega_b` |
| Hard-coded `Ob=0.046`, `n_s=0.965` in LSS σ₈ | Yes | Yes | Yes | Yes | Locks/Planck not used for these |
| Hard-coded `Ob=0.046`, `n_s=0.965` in CMB | Yes | Yes | Yes/Skip | Yes | Simplified model marks out-of-range as SKIP |
| SPARC hard-coded modeling constants | Yes | Yes | Yes | Yes | Consider locking these if required |
| Silent failures in manifest/equations | Yes | No | No | Yes | Trace completeness can be lost silently |
| Tracked `venv/`, `*.pyc`, `run_results/` | Yes (repo state) | No | No | Yes | Tooling noise + audit risk |

---

## Recommended resolution plan (prioritized)

### Priority 0 (stop unexpected parameter bypass)
- Decide whether `Omega_b` and `n_s` are **lock-governed** parameters.
  - If yes: add them to locks (or read from Planck JSON deterministically) and remove hard-coded constants from:
    - `integrated_modules/core/formulas.py` (proper growth + R_X derivation)
    - `integrated_modules/domains/lss.py` (σ₈)
    - `integrated_modules/domains/cmb.py` (CMB internal spectrum)

### Priority 1 (make standards artifacts fail loudly or at least report)
- Replace `pass` in manifest/equations writers with structured warnings (or record failure in results).
- Ensure `EQUATIONS_USED.md` is complete or explicitly marked incomplete for unmapped tests.

### Priority 2 (remove dead stubs or complete migration)
- Either delete unused `integrated_modules/core/{cosmology,tsi,lss,ese}.py` stubs, or implement them and refactor usage to match README architecture claims.

### Priority 3 (repo hygiene)
- Stop tracking `udof_runner/venv/`, `*.pyc`, and generated `run_results/` if not explicitly required by your standards.
- If you intentionally ship the sandbox with venv/results, document that as a standard and adjust review tooling to exclude them.

---

## Notes about the current execution environment (this review session)
- The environment running this review did not have `python` on PATH (`python: command not found`). This did not prevent static analysis, but it prevented executing the runner here to empirically measure sensitivity.

