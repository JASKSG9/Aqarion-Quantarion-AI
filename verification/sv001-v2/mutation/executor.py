#!/usr/bin/env python3
from __future__ import annotations
import os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
VERIFIER = PACKAGE / "verifier.py"

MUTANTS = ("wrong_trace","wrong_norm","wrong_gram","nan_error")

def run(mutant: str) -> bool:
    env = os.environ.copy()
    env["AQ_SV001_MUTANT"] = mutant
    proc = subprocess.run(
        [sys.executable, str(VERIFIER), "--case", "4", "3", "5"],
        cwd=PACKAGE, env=env, text=True, capture_output=True,
    )
    killed = proc.returncode != 0
    print(f"mutant={mutant} returncode={proc.returncode} killed={killed}")
    if not killed:
        print(proc.stdout)
        print(proc.stderr)
    return killed

def run_wrong_case_count() -> bool:
    proc = subprocess.run(
        [sys.executable, "-c",
         "from oracle import enumerate_cases; "
         "raise SystemExit(0 if len(list(enumerate_cases())) == 1175 else 1)"],
        cwd=PACKAGE, text=True, capture_output=True,
    )
    killed = proc.returncode != 0
    print(f"mutant=wrong_case_count killed={killed}")
    return killed

def main():
    results = {name: run(name) for name in MUTANTS}
    results["wrong_case_count"] = run_wrong_case_count()
    killed = sum(results.values())
    total = len(results)
    print(f"killed={killed} total={total}")
    if killed != total:
        print("status=FAIL")
        raise SystemExit(1)
    print("status=PASS")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""SV-001-V2 adversarial mutation executor."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
VERIFIER = PACKAGE / "verifier.py"

MUTANTS = ("wrong_trace", "wrong_norm", "wrong_gram", "nan_error")


def run(mutant: str) -> bool:
    env = os.environ.copy()
    env["AQ_SV001_MUTANT"] = mutant
    proc = subprocess.run(
        [sys.executable, str(VERIFIER), "--case", "4", "3", "5"],
        cwd=PACKAGE,
        env=env,
        text=True,
        capture_output=True,
    )
    killed = proc.returncode != 0
    print(f"mutant={mutant} returncode={proc.returncode} killed={killed}")
    if not killed:
        print(proc.stdout)
        print(proc.stderr)
    return killed


def run_wrong_case_count() -> bool:
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from oracle import enumerate_cases; "
                "raise SystemExit(0 if len(list(enumerate_cases())) == 1175 else 1)"
            ),
        ],
        cwd=PACKAGE,
        text=True,
        capture_output=True,
    )
    killed = proc.returncode != 0
    print(f"mutant=wrong_case_count killed={killed}")
    return killed


def main():
    results = {name: run(name) for name in MUTANTS}
    results["wrong_case_count"] = run_wrong_case_count()

    killed = sum(results.values())
    total = len(results)

    print(f"killed={killed} total={total}")

    if killed != total:
        print("status=FAIL")
        raise SystemExit(1)

    print("status=PASS")


if __name__ == "__main__":
    main()
