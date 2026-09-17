from __future__ import annotations

import hashlib
import hmac
import json
import unicodedata
from typing import Any, Dict


SCHEMA = "AQ-EVIDENCE-CORE/1"
ALGORITHM = "SHA-256"


def _normalize(value: Any) -> Any:
    """
    Normalize JSON-compatible values deterministically.

    Strings are NFC-normalized.
    Dictionary keys are normalized strings.
    Lists are normalized recursively.
    """
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)

    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", str(key)): _normalize(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [_normalize(item) for item in value]

    return value


def canonical_bytes(value: Any) -> bytes:
    """
    Produce deterministic UTF-8 JSON bytes.

    Rules:
      * normalized Unicode
      * lexicographically sorted object keys
      * no insignificant whitespace
      * UTF-8
      * NaN/Infinity rejected
    """
    normalized = _normalize(value)

    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    """Return lowercase hexadecimal SHA-256."""
    return hashlib.sha256(data).hexdigest()


def content_hash(
    evidence_id: str,
    evidence: Dict[str, Any],
) -> str:
    """
    Hash the complete evidence envelope.

    The evidence ID is intentionally covered by the digest.
    """
    envelope = {
        "schema": SCHEMA,
        "evidence_id": evidence_id,
        "evidence": evidence,
    }

    return sha256_bytes(canonical_bytes(envelope))


def _receipt_body(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Return receipt fields excluding its self-hash."""
    return {
        key: value
        for key, value in receipt.items()
        if key != "receipt_hash"
    }


def receipt_hash(receipt: Dict[str, Any]) -> str:
    """
    Hash the receipt metadata excluding receipt_hash itself.
    """
    return sha256_bytes(
        canonical_bytes(_receipt_body(receipt))
    )


def make_receipt(
    evidence: Dict[str, Any],
    evidence_id: str,
    producer: str,
    claim_status: str,
) -> Dict[str, Any]:
    """
    Create a deterministic content receipt.

    IMPORTANT:
      This does NOT prove authorship, provenance, or mathematical truth.
    """
    receipt = {
        "schema": SCHEMA,
        "evidence_id": evidence_id,
        "algorithm": ALGORITHM,
        "content_hash": content_hash(
            evidence_id,
            evidence,
        ),
        "producer": producer,
        "claim_status": claim_status,
    }

    receipt["receipt_hash"] = receipt_hash(receipt)

    return receipt


def verify_receipt(
    evidence: Dict[str, Any],
    receipt: Dict[str, Any],
) -> bool:
    """
    Verify:

      1. receipt schema
      2. declared algorithm
      3. receipt structure
      4. receipt self-hash
      5. evidence content hash

    This establishes content consistency only.

    It does NOT establish:
      * signer identity
      * authorship
      * timestamp authenticity
      * external immutability
      * mathematical correctness
      * formal proof
    """
    required = {
        "schema",
        "evidence_id",
        "algorithm",
        "content_hash",
        "producer",
        "claim_status",
        "receipt_hash",
    }

    if not isinstance(receipt, dict):
        return False

    if set(receipt.keys()) != required:
        return False

    if receipt["schema"] != SCHEMA:
        return False

    if receipt["algorithm"] != ALGORITHM:
        return False

    if not isinstance(receipt["evidence_id"], str):
        return False

    if not isinstance(receipt["content_hash"], str):
        return False

    if not isinstance(receipt["receipt_hash"], str):
        return False

    expected_receipt_hash = receipt_hash(receipt)

    if not hmac.compare_digest(
        expected_receipt_hash,
        receipt["receipt_hash"],
    ):
        return False

    expected_content_hash = content_hash(
        receipt["evidence_id"],
        evidence,
    )

    return hmac.compare_digest(
        expected_content_hash,
        receipt["content_hash"],
  )
