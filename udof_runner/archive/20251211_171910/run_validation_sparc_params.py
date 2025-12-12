#!/usr/bin/env python3
"""
Quick validation runner with SPARC updated parameters check
"""

import sys
from pathlib import Path
import json

# Add runner to path
runner_dir = Path(__file__).parent
sys.path.insert(0, str(runner_dir))

# Check if updated parameters are available
master_lock = runner_dir / "data" / "locks" / "CDQF_MASTER_LOCK_v3_SPARC.json"
if master_lock.exists():
    locks = json.load(open(master_lock))
    if 'dark_sector' in locks and 'ese' in locks['dark_sector']:
        k = locks['dark_sector']['ese'].get('k', 1.5)
        X0 = locks['dark_sector']['ese'].get('X0', 0.917)
        print(f"Using updated SPARC parameters: k={k:.3f}, X0={X0:.3f}")
    else:
        print("Master lock exists but missing ESE parameters")
else:
    print("Master lock not found, using defaults")

# Run validation
from cdqf_validation_runner_v4_0 import CDQFTests, main

if __name__ == '__main__':
    main()

