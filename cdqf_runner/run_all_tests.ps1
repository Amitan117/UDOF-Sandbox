# CDQF Validation Runner - Run All Tests
# PowerShell script to run full validation suite

Write-Host "=" * 80 -ForegroundColor Green
Write-Host "CDQF Validation Runner - Full Test Suite" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Green
Write-Host ""

$sandboxDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $sandboxDir

# Activate virtual environment if exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & ".\venv\Scripts\Activate.ps1"
}
else {
    Write-Host "WARNING: Virtual environment not found. Using system Python." -ForegroundColor Yellow
    Write-Host "  Run setup_environment.ps1 first for isolated environment." -ForegroundColor Yellow
    Write-Host ""
}

# Check if runner exists
if (-not (Test-Path "cdqf_validation_runner_v4.0.py")) {
    Write-Host "ERROR: cdqf_validation_runner_v4.0.py not found!" -ForegroundColor Red
    exit 1
}

# Run all tests
Write-Host "Running full validation suite..." -ForegroundColor Cyan
Write-Host ""

python cdqf_validation_runner_v4.0.py

$exitCode = $LASTEXITCODE

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Green
if ($exitCode -eq 0) {
    Write-Host "All tests completed successfully!" -ForegroundColor Green
}
else {
    Write-Host "Tests completed with errors (exit code: $exitCode)" -ForegroundColor Yellow
}
Write-Host "=" * 80 -ForegroundColor Green

exit $exitCode

