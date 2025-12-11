#!/usr/bin/env python3
"""
Non-interactive validation runner that avoids terminal hanging.

This script runs the validation and outputs to file directly,
avoiding PowerShell piping issues.
"""

from cdqf_validation_runner_v4_0 import main
import sys
import os
from pathlib import Path

# Force unbuffered output
os.environ['PYTHONUNBUFFERED'] = '1'
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import and run

if __name__ == '__main__':
    # Run with quiet mode to avoid hanging
    sys.argv = ['cdqf_validation_runner_v4.0.py', '--quiet']
    main()
