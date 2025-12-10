# Archive - Cleanup 2025-12-10

This directory contains files archived during repository cleanup.

## Contents

### Test Scripts
- `test_*.py` - Temporary test scripts for growth factor validation and debugging
- `evaluate_upstream_modules.py` - Script for evaluating upstream module dependencies

### Documentation Files
- `ANSWERS_TO_USER_QUESTIONS.md` - Q&A about CLASS dependency and growth factor ODE
- `CLASS_DEPENDENCY_ANALYSIS.md` - Analysis of CLASS dependency usage
- `DEPENDENCY_STRATEGY.md` - Strategy for handling dependencies
- `EXTERNAL_ASSESSMENT.md` - External assessment findings
- `GROWTH_FACTOR_FIXES_APPLIED.md` - Documentation of growth factor fixes
- `GROWTH_FACTOR_ODE_FIX.md` - Details of ODE fix
- `GROWTH_FACTOR_OVERSHOOT_ANALYSIS.md` - Analysis of 0.4% overshoot issue
- `INTEGRATION_COMPLETE.md` - Integration status documentation
- `MISSING_DEPENDENCIES.md` - Documentation of missing dependencies
- `UPSTREAM_MODULES_EVALUATION.md` - Evaluation of upstream modules

## Reason for Archival

These files were created during development and debugging phases but are not needed for:
- Production use of the validation runner
- User documentation
- Core functionality

They are preserved here for historical reference and development context.

## Current Active Files

The following files remain in the main directory:
- `cdqf_validation_runner_v4.0.py` - Main validation runner
- `README.md` - User documentation
- `CITATIONS.md` - Citations for external work
- `requirements.txt` - Python dependencies
- `default_params.json` - Default parameters
- `setup_environment.ps1` - Environment setup script
- `run_all_tests.ps1` - Test execution script
- `data/` - Data files
- `integrated_modules/` - Integrated module implementations
- `run_results/` - Test results directory (empty)

