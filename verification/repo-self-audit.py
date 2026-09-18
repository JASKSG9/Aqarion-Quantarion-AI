#!/usr/bin/env python3
"""
AQARION repository closure self-audit.

Fail closed on:
- declared files that do not exist
- case/path mismatches
- stale claim artifacts
- incomplete workflow heredocs
- executable bindings without files
"""

from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "aqarion.toml",
    "claims/sv-001-v2.json",
    "verification/manifest.json",
    "verification/sv-001-v2/contract.json",
    "verification/sv-001-v2/oracle.py",
    "verification/sv-001-v2/verifier.py",
    "verification/sv-001-v2/replay.py",
    "verification/sv-001-v2/mutation/executor.py",
    "verification/sv-001-v2/mutation/metamorphic.py",
    "verification/sv-001-v2/receipt/schema.json",
    "verification/sv-001-v2/receipt/writer.py",
    ".github/workflows/verify.yml",
]

def exact_file(path_string: str) -> bool:
    parts = Path(path_string).parts
    current = ROOT
    for part in parts:
        if not current.is_dir():
            return False
        if part not in [c.name for c in current.iterdir()]:
            return False
        current = current / part
    return current.is_file()

def check_required_files(errors):
    for path in REQUIRED:
        if not exact_file(path):
            errors.append(f"REQUIRED_FILE_MISSING:{path}")

def check_claim(errors):
    p = ROOT / "claims" / "sv-001-v2.json"
    if not p.is_file():
        return
    try:
        claim = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"CLAIM_JSON_INVALID:{exc}")
        return
    artifact = claim.get("evidence", {}).get("artifact", "")
    if artifact and not exact_file(artifact):
        errors.append("CLAIM_REPLAYABLE_WITHOUT_ARTIFACT")

def check_workflow(errors):
    p = ROOT / ".github" / "workflows" / "verify.yml"
    if not p.is_file():
        return
    text = p.read_text(encoding="utf-8")
    starts = len(re.findall(r"(?m)^[ \t]*python(?:3)?[ \t]+-[ \t]*<<['\"]?PY['\"]?[ \t]*$", text))
    ends = len(re.findall(r"(?m)^[ \t]*PY[ \t]*$", text))
    if starts != ends:
        errors.append("WORKFLOW_UNTERMINATED_HEREDOC")
    if "verification/sv-001-v2/replay.py" not in text:
        errors.append("WORKFLOW_MISSING_REPLAY_COMMAND")
    if "verification/repo_self_audit.py" not in text:
        errors.append("WORKFLOW_MISSING_SELF_AUDIT")

def check_deprecated_domain(errors):
    package = ROOT / "verification" / "sv-001-v2"
    if not package.is_dir():
        return
    for path in package.rglob("*"):
        if not path.is_file() or path.suffix not in {".py",".json",".toml",".yaml",".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'"cases"\s*:\s*5720', text):
            errors.append(f"DEPRECATED_5720_ACTIVE:{path.relative_to(ROOT)}")

def check_receipt_policy(errors):
    for p in [ROOT / "verification" / "sv-001-v2" / "receipt.json",
              ROOT / "verification" / "sv-001-v2" / "receipt" / "receipt.json"]:
        if p.exists():
            errors.append(f"PREGENERATED_RECEIPT_FORBIDDEN:{p.relative_to(ROOT)}")

def main():
    errors = []
    check_required_files(errors)
    check_claim(errors)
    check_workflow(errors)
    check_deprecated_domain(errors)
    check_receipt_policy(errors)
    print("AQARION REPOSITORY SELF-AUDIT")
    if errors:
        print("status=FAIL")
        for e in errors:
            print(f"ERROR:{e}")
        raise SystemExit(1)
    print("status=PASS")

if __name__ == "__main__":
    main()
