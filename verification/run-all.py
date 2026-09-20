#!/usr/bin/env python3
"""
AQARION VERIFICATION RUNNER
AQ-SIDE-PIVOT-002 hardened runner

Governance:
FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED

Design:
    1. Load manifest.
    2. Validate every registered executable binding.
    3. Refuse to execute anything if binding validation fails.
    4. Execute each registered check independently.
    5. Convert launch failures into structured FAIL records.
    6. Emit a deterministic JSON receipt.
    7. Exit nonzero unless every registered check passes.

No external fallback paths are permitted.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
VERIFICATION = ROOT / "verification"
MANIFEST = VERIFICATION / "manifest.json"
RECEIPT = VERIFICATION / "last-run-receipt.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


def exact_case_path(path: Path) -> bool:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return False

    current = ROOT

    for component in relative.parts:
        if not current.is_dir():
            return False

        names = {entry.name for entry in current.iterdir()}

        if component not in names:
            return False

        current = current / component

    return True


def resolve_binding(command: list[str]) -> tuple[bool, str, Path | None]:
    if not command:
        return False, "empty command", None

    if any(not isinstance(x, str) or not x for x in command):
        return False, "invalid argv element", None

    executable = command[0]

    if executable in {"python", "python3", sys.executable}:
        if len(command) < 2:
            return False, "Python command has no script", None

        script = command[1]

        if script.startswith("-"):
            return False, "Python command has no script path", None

        candidate = ROOT / script

        if not candidate.is_file():
            return False, f"missing registered script: {script}", None

        if not exact_case_path(candidate):
            return False, f"case/path mismatch: {script}", None

        return True, f"script:{script}", candidate

    if os.path.isabs(executable):
        candidate = Path(executable)

        if not candidate.exists():
            return False, f"missing executable: {executable}", None

        return True, f"absolute:{executable}", candidate

    resolved = shutil.which(executable)

    if resolved is None:
        return False, f"executable not found on PATH: {executable}", None

    return True, f"PATH:{resolved}", Path(resolved)


def load_manifest() -> dict[str, Any]:
    with MANIFEST.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")

    checks = data.get("checks")

    if not isinstance(checks, list):
        raise ValueError("manifest.checks must be a list")

    return data


def binding_audit(
    manifest: dict[str, Any],
) -> tuple[bool, list[dict[str, Any]]]:
    checks = manifest["checks"]

    results: list[dict[str, Any]] = []

    seen: set[str] = set()

    for check in checks:
        if not isinstance(check, dict):
            results.append({
                "id": None,
                "status": "FAIL",
                "reason": "check is not an object",
            })
            continue

        check_id = check.get("id")

        if not isinstance(check_id, str) or not check_id:
            results.append({
                "id": None,
                "status": "FAIL",
                "reason": "invalid check id",
            })
            continue

        if check_id in seen:
            results.append({
                "id": check_id,
                "status": "FAIL",
                "reason": "duplicate check id",
            })
            continue

        seen.add(check_id)

        command = check.get("command")

        if not isinstance(command, list):
            results.append({
                "id": check_id,
                "status": "FAIL",
                "reason": "command is not an argv list",
            })
            continue

        ok, detail, resolved = resolve_binding(command)

        record: dict[str, Any] = {
            "id": check_id,
            "status": "PASS" if ok else "FAIL",
            "binding": detail,
        }

        if resolved is not None and resolved.is_file():
            record["artifact_sha256"] = sha256_file(resolved)

        if not ok:
            record["reason"] = detail

        results.append(record)

    return all(r["status"] == "PASS" for r in results), results


def execute_check(check: dict[str, Any]) -> dict[str, Any]:
    check_id = check["id"]
    command = check["command"]

    started = time.time()

    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=3600,
            env=os.environ.copy(),
        )

        duration = time.time() - started

        return {
            "id": check_id,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "exit_code": proc.returncode,
            "duration_seconds": duration,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }

    except FileNotFoundError as exc:
        duration = time.time() - started

        return {
            "id": check_id,
            "status": "FAIL",
            "exit_code": None,
            "duration_seconds": duration,
            "launch_error": f"FileNotFoundError: {exc}",
        }

    except subprocess.TimeoutExpired as exc:
        duration = time.time() - started

        return {
            "id": check_id,
            "status": "FAIL",
            "exit_code": None,
            "duration_seconds": duration,
            "launch_error": f"TimeoutExpired: {exc}",
        }

    except Exception as exc:
        duration = time.time() - started

        return {
            "id": check_id,
            "status": "FAIL",
            "exit_code": None,
            "duration_seconds": duration,
            "launch_error": f"{type(exc).__name__}: {exc}",
        }


def write_receipt(receipt: dict[str, Any]) -> None:
    temporary = RECEIPT.with_suffix(".tmp")

    encoded = json.dumps(
        receipt,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )

    temporary.write_text(
        encoded + "\n",
        encoding="utf-8",
    )

    temporary.replace(RECEIPT)


def main() -> int:
    started = time.time()

    print("AQARION VERIFICATION RUNNER")
    print("AQ-SIDE-PIVOT-002 HARDENED MODE")
    print("Governance: FROZEN AUDIT · NO PROMOTION · C4 BLOCKED · PUBLICATION BLOCKED")
    print()

    try:
        manifest_bytes = MANIFEST.read_bytes()
        manifest_sha256 = sha256_bytes(manifest_bytes)
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except Exception as exc:
        receipt = {
            "status": "FAIL",
            "stage": "MANIFEST_LOAD",
            "error": f"{type(exc).__name__}: {exc}",
        }

        write_receipt(receipt)

        print("RESULT=FAIL")
        print("STAGE=MANIFEST_LOAD")
        return 2

    binding_ok, binding_results = binding_audit(manifest)

    print("MANIFEST_BINDING_AUDIT")

    for result in binding_results:
        print(
            f"  {result['id']}: "
            f"{result['status']} "
            f"{result.get('reason', result.get('binding', ''))}"
        )

    if not binding_ok:
        receipt = {
            "schema": "AQARION-RUN-RECEIPT-1",
            "status": "FAIL",
            "stage": "MANIFEST_BINDING",
            "manifest_sha256": manifest_sha256,
            "binding_results": binding_results,
            "checks_executed": 0,
            "checks_passed": 0,
            "checks_failed": len(binding_results),
            "duration_seconds": time.time() - started,
        }

        write_receipt(receipt)

        print()
        print("RESULT=FAIL")
        print("STAGE=MANIFEST_BINDING")
        print(f"RECEIPT={RECEIPT}")
        return 1

    print()
    print("ALL REGISTERED EXECUTABLE BINDINGS RESOLVE.")
    print()

    results = []

    for check in manifest["checks"]:
        result = execute_check(check)
        results.append(result)

        print(
            f"{result['id']}: "
            f"{result['status']}"
        )

    failures = [
        result for result in results
        if result["status"] != "PASS"
    ]

    receipt = {
        "schema": "AQARION-RUN-RECEIPT-1",
        "status": "PASS" if not failures else "FAIL",
        "stage": "EXECUTION",
        "manifest_sha256": manifest_sha256,
        "binding_results": binding_results,
        "results": results,
        "checks_registered": len(manifest["checks"]),
        "checks_executed": len(results),
        "checks_passed": len(results) - len(failures),
        "checks_failed": len(failures),
        "duration_seconds": time.time() - started,
    }

    write_receipt(receipt)

    print()
    print(f"REGISTERED={len(manifest['checks'])}")
    print(f"PASSED={len(results) - len(failures)}")
    print(f"FAILED={len(failures)}")

    if failures:
        print("RESULT=FAIL")
        print(f"RECEIPT={RECEIPT}")
        return 1

    print("RESULT=PASS")
    print(f"RECEIPT={RECEIPT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
