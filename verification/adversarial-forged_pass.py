#!/usr/bin/env python3

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from provenance import ExecutionReceipt, ProvenanceError, verify_receipt


def main() -> int:
    receipt = ExecutionReceipt(
        claim_id="FORGED-PASS",
        source_root="correct-root",
        executable="verification/run_all.py",
        executable_sha256="0" * 64,
        command=("verification/run_all.py",),
        observed_output_sha256="1" * 64,
        expected_output_sha256="2" * 64,
        execution_performed=True,
        independent_from=("external-replay",),
        result="PASS",
    )

    try:
        verify_receipt(
            receipt,
            repository_root=Path(__file__).resolve().parents[2],
            expected_root="correct-root",
        )
    except ProvenanceError:
        print("FORGED-PASS=REJECTED")
        return 0

    print("FORGED-PASS=ACCEPTED -- SECURITY FAILURE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
