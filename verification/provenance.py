#!/usr/bin/env python3
"""Evidence provenance primitives.

This module does not establish mathematical truth.
It establishes whether an evidence receipt is internally bound to:
- a source root,
- an executable,
- an observed artifact,
- a digest,
- an execution event,
- and an independence declaration.

A provenance PASS is therefore an integrity/policy result, not a theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import subprocess


class ProvenanceError(Exception):
    """Evidence provenance failure."""


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class ExecutionReceipt:
    claim_id: str
    source_root: str
    executable: str
    executable_sha256: str
    command: tuple[str, ...]
    observed_output_sha256: str
    expected_output_sha256: str
    execution_performed: bool
    independent_from: tuple[str, ...]
    result: str

    @classmethod
    def from_mapping(cls, obj: dict[str, Any]) -> "ExecutionReceipt":
        required = {
            "claim_id",
            "source_root",
            "executable",
            "executable_sha256",
            "command",
            "observed_output_sha256",
            "expected_output_sha256",
            "execution_performed",
            "independent_from",
            "result",
        }

        missing = required - obj.keys()
        if missing:
            raise ProvenanceError(
                f"receipt missing required fields: {sorted(missing)}"
            )

        return cls(
            claim_id=obj["claim_id"],
            source_root=obj["source_root"],
            executable=obj["executable"],
            executable_sha256=obj["executable_sha256"],
            command=tuple(obj["command"]),
            observed_output_sha256=obj["observed_output_sha256"],
            expected_output_sha256=obj["expected_output_sha256"],
            execution_performed=bool(obj["execution_performed"]),
            independent_from=tuple(obj["independent_from"]),
            result=obj["result"],
        )


def verify_receipt(
    receipt: ExecutionReceipt,
    *,
    repository_root: Path,
    expected_root: str,
) -> None:
    """Raise ProvenanceError unless the receipt passes integrity checks."""

    if receipt.result != "PASS":
        raise ProvenanceError(
            f"receipt result is not PASS: {receipt.result!r}"
        )

    if not receipt.execution_performed:
        raise ProvenanceError(
            "PASS receipt claims success without recorded execution"
        )

    if receipt.source_root != expected_root:
        raise ProvenanceError(
            f"stale/wrong source root: {receipt.source_root!r}"
        )

    executable = repository_root / receipt.executable

    if not executable.is_file():
        raise ProvenanceError(
            f"declared executable does not exist: {receipt.executable}"
        )

    actual_hash = sha256_file(executable)

    if actual_hash != receipt.executable_sha256:
        raise ProvenanceError(
            "executable digest mismatch: "
            f"declared={receipt.executable_sha256} "
            f"actual={actual_hash}"
        )

    if not receipt.command:
        raise ProvenanceError("empty execution command")

    if receipt.executable not in receipt.command:
        raise ProvenanceError(
            "execution command is not bound to declared executable"
        )

    if not receipt.independent_from:
        raise ProvenanceError(
            "independence basis is absent"
        )

    if receipt.observed_output_sha256 == receipt.expected_output_sha256:
        raise ProvenanceError(
            "observed and expected output digests are identical; "
            "independent observation has not been established"
        )


def execute(
    command: list[str],
    *,
    cwd: Path,
) -> tuple[int, bytes, bytes]:
    """Execute a registered command and return code/stdout/stderr."""
    proc = subprocess.run(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode, proc.stdout, proc.stderr
