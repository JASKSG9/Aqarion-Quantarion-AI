from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "aq_conditioning.self_audit"],
    [sys.executable, "-m", "aq_conditioning.replay"],
]


def main() -> int:
    failures = 0

    for command in COMMANDS:
        completed = subprocess.run(command, check=False)
        failures += int(completed.returncode != 0)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
