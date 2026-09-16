#!/usr/bin/env python3
"""
AQARION ARO-1 provenance verification.

FILE:
    verification/provenance.py

TYPE:
    PYTHON SCRIPT

Important distinction:

    output agreement != independence
    reproduction != formal proof
    provenance integrity != mathematical truth

A successful reproduction requires output agreement.

Independence is evaluated separately.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import json


class ProvenanceError(Exception):
    """Raised when an ARO-1 receipt is invalid."""


def sha256_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def canonical_json(value: Any) -> bytes:
    """
    Deterministic local JSON representation.

    IMPORTANT:
        This is NOT claimed to be RFC 8785 JCS.

    It is used only by this non-normative verifier for local
    deterministic hashing.
    """
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class ReproductionReceipt:
    claim_id: str
    source_root: str
    executable: str
    executable_sha256: str
    command: tuple[str, ...]
    execution_performed: bool
    exit_code: int
    observed_output_sha256: str
    expected_output_sha256: str
    independence_status: str
    independence_basis: tuple[str, ...]
    formal_status: str

    @classmethod
    def from_mapping(
        cls,
        value: dict[str, Any],
    ) -> "ReproductionReceipt":
        required = {
            "claim_id",
            "source_root",
            "executable",
            "executable_sha256",
            "command",
            "execution_performed",
            "exit_code",
            "observed_output_sha256",
            "expected_output_sha256",
            "independence_status",
            "independence_basis",
            "formal_status",
        }

        missing = sorted(required - value.keys())

        if missing:
            raise ProvenanceError(
                f"missing receipt fields: {missing}"
            )

        return cls(
            claim_id=str(value["claim_id"]),
            source_root=str(value["source_root"]),
            executable=str(value["executable"]),
            executable_sha256=str(value["executable_sha256"]),
            command=tuple(value["command"]),
            execution_performed=bool(value["execution_performed"]),
            exit_code=int(value["exit_code"]),
            observed_output_sha256=str(
                value["observed_output_sha256"]
            ),
            expected_output_sha256=str(
                value["expected_output_sha256"]
            ),
            independence_status=str(
                value["independence_status"]
            ),
            independence_basis=tuple(
                value["independence_basis"]
            ),
            formal_status=str(value["formal_status"]),
        )


def verify_reproduction(
    receipt: ReproductionReceipt,
    *,
    repository_root: Path,
    expected_source_root: str,
) -> dict[str, Any]:
    """
    Verify the reproduction layer.

    This function deliberately does NOT require independence
    for ordinary reproduction.

    It also does NOT infer mathematical truth from the result.
    """

    if receipt.source_root != expected_source_root:
        raise ProvenanceError(
            "source_root mismatch: "
            f"{receipt.source_root!r} != "
            f"{expected_source_root!r}"
        )

    executable = repository_root / receipt.executable

    if not executable.is_file():
        raise ProvenanceError(
            f"executable does not exist: {receipt.executable}"
        )

    actual_executable_hash = sha256_file(executable)

    if actual_executable_hash != receipt.executable_sha256:
        raise ProvenanceError(
            "executable digest mismatch"
        )

    if not receipt.command:
        raise ProvenanceError("empty execution command")

    if not receipt.execution_performed:
        raise ProvenanceError(
            "execution_performed=false"
        )

    if receipt.exit_code != 0:
        raise ProvenanceError(
            f"execution exit code was {receipt.exit_code}"
        )

    if not receipt.observed_output_sha256:
        raise ProvenanceError(
            "missing observed output digest"
        )

    if not receipt.expected_output_sha256:
        raise ProvenanceError(
            "missing expected output digest"
        )

    output_match = (
        receipt.observed_output_sha256
        == receipt.expected_output_sha256
    )

    if not output_match:
        raise ProvenanceError(
            "observed output does not match expected output"
        )

    if receipt.independence_status == "ESTABLISHED":
        if not receipt.independence_basis:
            raise ProvenanceError(
                "independence marked ESTABLISHED without a basis"
            )

    elif receipt.independence_status not in {
        "NOT_ESTABLISHED",
        "ESTABLISHED",
    }:
        raise ProvenanceError(
            "invalid independence_status"
        )

    if receipt.formal_status not in {
        "OPEN",
        "PROVED",
        "PROVED_AND_CHECKED",
    }:
        raise ProvenanceError(
            "invalid formal_status"
        )

    reproduced = True
    independently_reproduced = (
        reproduced
        and receipt.independence_status == "ESTABLISHED"
    )
    formally_verified = (
        reproduced
        and receipt.formal_status
        in {"PROVED", "PROVED_AND_CHECKED"}
    )

    return {
        "claim_id": receipt.claim_id,
        "executed": True,
        "source_bound": True,
        "executable_bound": True,
        "output_match": True,
        "reproduced": reproduced,
        "independence_established": independently_reproduced,
        "formal_proof": formally_verified,
    }


def load_and_verify(
    receipt_path: Path,
    *,
    repository_root: Path,
    expected_source_root: str,
) -> dict[str, Any]:
    if not receipt_path.is_file():
        raise ProvenanceError(
            f"receipt does not exist: {receipt_path}"
        )

    try:
        raw = json.loads(
            receipt_path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise ProvenanceError(
            f"invalid receipt JSON: {exc}"
        ) from exc

    receipt = ReproductionReceipt.from_mapping(raw)

    return verify_reproduction(
        receipt,
        repository_root=repository_root,
        expected_source_root=expected_source_root,
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--receipt",
        required=True,
    )

    parser.add_argument(
        "--source-root",
        required=True,
    )

    args = parser.parse_args()

    try:
        result = load_and_verify(
            Path(args.receipt).resolve(),
            repository_root=Path.cwd().resolve(),
            expected_source_root=args.source_root,
        )
    except ProvenanceError as exc:
        print(f"PROVENANCE FAIL: {exc}")
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    print("PROVENANCE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
