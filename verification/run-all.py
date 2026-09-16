#!/usr/bin/env python3
"""Canonical AQARION verification orchestrator.

Runs only checks explicitly listed in a JSON manifest and emits a receipt.
"""
from __future__ import annotations

import argparse, hashlib, json, platform, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def self_check() -> int:
    required = [ROOT / "verification" / name for name in (
        "run_all.py", "replay_harness.py", "manifest.json", "requirements.txt", "README.md"
    )]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    print(json.dumps({"self_check": "PASS" if not missing else "FAIL", "missing": missing}, sort_keys=True))
    return 0 if not missing else 1

def run_manifest(manifest_path: Path, receipt_path: Path) -> int:
    manifest = load_json(manifest_path)
    rows = []
    overall = "PASS"
    for item in manifest.get("checks", []):
        path = ROOT / item["path"]
        if not path.is_file():
            rows.append({"check_id": item["check_id"], "status": "INDETERMINATE", "reason": "MISSING_REGISTERED_PATH", "path": item["path"]})
            overall = "FAIL"
            continue
        command = [x.replace("{python}", sys.executable) for x in item["command"]]
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = "PASS" if result.returncode == 0 else "FAIL"
        rows.append({
            "check_id": item["check_id"], "status": status, "scope": item.get("scope", "UNDECLARED"),
            "path": item["path"], "path_sha256": sha256(path), "command": command,
            "exit_code": result.returncode,
            "stdout_sha256": "sha256:" + hashlib.sha256(result.stdout.encode()).hexdigest(),
            "stderr_sha256": "sha256:" + hashlib.sha256(result.stderr.encode()).hexdigest()
        })
        if result.returncode != 0 and item.get("required", True): overall = "FAIL"
    receipt = {
        "receipt_schema": "aqarion.verification.receipt.v1",
        "receipt_id": "AQ-S16-CANONICAL-REPLAY",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": {"path": str(manifest_path), "sha256": sha256(manifest_path)},
        "environment": {"python": sys.version, "platform": platform.platform()},
        "status": overall,
        "checks": rows,
        "governance": manifest.get("governance", {}),
        "limitations": manifest.get("limitations", [])
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": overall, "receipt": str(receipt_path), "checks": len(rows)}, sort_keys=True))
    return 0 if overall == "PASS" else 1

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path)
    p.add_argument("--receipt", type=Path)
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args()
    if args.self_check: return self_check()
    if not args.manifest or not args.receipt:
        p.error("--manifest and --receipt are required unless --self-check is used")
    return run_manifest(args.manifest, args.receipt)

if __name__ == "__main__":
    raise SystemExit(main())
