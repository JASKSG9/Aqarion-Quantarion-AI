import pathlib, subprocess, sys
real=pathlib.Path(__file__).parent.parent/"AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-"/"VERIFICATION"/"sv001_v2_check.py"
local=pathlib.Path("/mnt/data/aqarion_proofledger/VERIFICATION/sv001_v2_check.py")
target=real if real.exists() else local
if not target.exists():
    print(f"ARTIFACT_MISSING: {target}"); sys.exit(2)
print(f"Running {target}")
result=subprocess.run([sys.executable, str(target)], capture_output=True, text=True)
print(result.stdout); print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
