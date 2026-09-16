# AQARION Verification Surface

## Purpose

This directory contains executable finite verification and provenance
infrastructure for the AQARION research corpus.

A passing computational replay does not establish a universal mathematical
theorem.

A passing provenance check does not establish mathematical truth.

A public repository does not constitute independent reproduction.

---

## Canonical Runner

Use:

```text
python3 verification/run_all.py \
  --manifest verification/manifest.json \
  --receipt verification/receipts/run_all_receipt.json
