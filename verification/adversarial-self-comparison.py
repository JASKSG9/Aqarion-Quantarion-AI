#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from provenance import ExecutionReceipt, ProvenanceError, verify_receipt


def main() -> int:
    receipt = ExecutionReceipt(
        claim_id="SELF-COMPARISON",
        source_root="root",
        executable="verification/run_all.py",
        executable_sha256="0" * 64,
        command=("verification/run_all.py",),
        observed_output_sha256="same",
        expected_output_sha256="different",
        execution_performed=True,
        independent_from=(),
        result="PASS",
    )

    try:
        verify_receipt(
            receipt,
            repository_root=Path(__file__).resolve().parents[2],
            expected_root="root",
        )
    except ProvenanceError:
        print("SELF-COMPARISON=REJECTED")
        return 0

    print("SELF-COMPARISON=ACCEPTED -- SECURITY FAILURE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
