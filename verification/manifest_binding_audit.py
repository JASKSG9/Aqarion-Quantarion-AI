#!/usr/bin/env python3
"""
AQ-SIDE-PIVOT-002
MANIFEST BINDING AUDITOR

Governance:
FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED

Purpose:
    Independently verify that every executable registered in
    verification/manifest.json is actually bound to an existing file.

This is a binding audit only.
It does NOT execute the registered checks.

Exit codes:
    0 = all registered executable bindings resolve
    1 = one or more bindings are invalid
    2 = manifest/schema/input error
"""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "verification" / "manifest.json"


class BindingError(Exception):
    pass


def fail(message: str) -> None:
    print(f"FAIL: {message}")


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.is_file():
        raise BindingError(f"missing manifest: {MANIFEST}")

    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        raise BindingError(f"cannot parse manifest: {exc}") from exc

    if not isinstance(data, dict):
        raise BindingError("manifest root is not an object")

    checks = data.get("checks")

    if not isinstance(checks, list):
        raise BindingError("manifest.checks is not a list")

    return data


def exact_case_path(path: Path) -> bool:
    """
    Check every component against the directory listing.

    This matters on case-insensitive filesystems: a path can appear to
    exist while its Git-tracked spelling is different.
    """
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False

    current = ROOT

    for part in relative.parts:
        if not current.is_dir():
            return False

        names = {entry.name for entry in current.iterdir()}

        if part not in names:
            return False

        current = current / part

    return True


def validate_command(
    check_id: str,
    command: Any,
) -> tuple[bool, str]:
    if not isinstance(command, list) or not command:
        return False, "command must be a non-empty argv list"

    for item in command:
        if not isinstance(item, str) or not item:
            return False, "command contains a non-string/empty argv element"

    executable = command[0]

    # Python commands are expected to have a script as argv[1].
    if executable in {"python", "python3", sys.executable}:
        if len(command) < 2:
            return False, "Python command has no script argument"

        script = command[1]

        if script.startswith("-"):
            return False, "Python command uses an option instead of a script"

        candidate = ROOT / script

        if not candidate.is_file():
            return False, f"missing registered script: {script}"

        if not exact_case_path(candidate):
            return False, f"case/path mismatch for registered script: {script}"

        return True, f"bound: {script}"

    # Generic executable:
    # absolute path must exist, otherwise PATH resolution is required.
    if os.path.isabs(executable):
        candidate = Path(executable)
        if not candidate.exists():
            return False, f"missing absolute executable: {executable}"
        return True, f"bound executable: {executable}"

    # For non-Python commands, verify that the executable is resolvable.
    resolved = shutil_which(executable)

    if resolved is None:
        return False, f"executable not found on PATH: {executable}"

    return True, f"PATH executable: {resolved}"


def shutil_which(command: str) -> str | None:
    import shutil

    return shutil.which(command)


def main() -> int:
    print("AQ-SIDE-PIVOT-002 / MANIFEST BINDING AUDIT")
    print("Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED")
    print(f"Repository root: {ROOT}")
    print(f"Manifest: {MANIFEST}")
    print()

    try:
        manifest = load_manifest()
    except BindingError as exc:
        fail(str(exc))
        return 2

    checks = manifest["checks"]

    failures = 0

    seen_ids: set[str] = set()

    for check in checks:
        if not isinstance(check, dict):
            fail("manifest contains non-object check")
            failures += 1
            continue

        check_id = check.get("id")

        if not isinstance(check_id, str) or not check_id:
            fail("check has missing/invalid id")
            failures += 1
            continue

        if check_id in seen_ids:
            fail(f"duplicate check id: {check_id}")
            failures += 1
            continue

        seen_ids.add(check_id)

        command = check.get("command")

        ok, detail = validate_command(check_id, command)

        if ok:
            print(f"PASS  {check_id}: {detail}")
        else:
            print(f"FAIL  {check_id}: {detail}")
            failures += 1

    print()
    print(f"REGISTERED_CHECKS={len(checks)}")
    print(f"BINDING_FAILURES={failures}")

    if failures:
        print("RESULT=FAIL")
        return 1

    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
