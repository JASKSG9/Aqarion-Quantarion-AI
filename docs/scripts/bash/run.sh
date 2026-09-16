#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'
\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

mkdir -p receipts

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_LOG="receipts/AQARION-QUANTARION-AI-${STAMP}.txt"
RECEIPT="receipts/AQARION-QUANTARION-AI-${STAMP}.json"
HASHES="receipts/AQARION-QUANTARION-AI-${STAMP}.sha256"

{
  echo "RUN_ID=AQARION-QUANTARION-AI-LOCAL"
  echo "START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "PWD=$(pwd)"
  echo "PYTHON=$(command -v python3)"
  echo "PYTHON_VERSION=$(python3 --version 2>&1)"
  echo

  echo "== JSON VALIDATION =="
  python3 -m json.tool claim.json >/dev/null
  python3 -m json.tool policies/research-policy.json >/dev/null
  python3 -m json.tool fixtures/scope-mismatch.json >/dev/null
  echo "JSON_VALIDATION=PASS"
  echo

  echo "== PYTHON COMPILE =="
  python3 -m py_compile src/claimlock.py tests/test_claimlock.py
  echo "PY_COMPILE=PASS"
  echo

  echo "== TESTS =="
  python3 -m pytest -q
  test_rc=$?
  echo "PYTEST_EXIT=$test_rc"
  echo

  echo "== CLAIMLOCK DECISION =="
  python3 src/claimlock.py \
    --claim claim.json \
    --policy policies/research-policy.json \
    --receipt "$RECEIPT"
  claimlock_rc=$?
  echo "CLAIMLOCK_EXIT=$claimlock_rc"
  echo

  echo "== EXPECTED OUTCOME =="
  echo "The example claim should be BLOCKED because INSTANCE evidence"
  echo "does not authorize FORMALLY_PROVED promotion of a UNIVERSAL claim."
  echo

  echo "END_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  if [ "$test_rc" -ne 0 ]; then
    exit "$test_rc"
  fi

  # CLAIMLOCK returning 1 is expected for the intentionally blocked fixture.
  if [ "$claimlock_rc" -ne 1 ]; then
    exit "$claimlock_rc"
  fi

  exit 0
} 2>&1 | tee "$RUN_LOG"

rc=${PIPESTATUS[0]}

printf 'RUN_EXIT=%s
' "$rc" >> "$RUN_LOG"

sha256sum \
  README.md \
  claim.json \
  policies/research-policy.json \
  fixtures/scope-mismatch.json \
  src/claimlock.py \
  tests/test_claimlock.py \
  "$RUN_LOG" \
  "$RECEIPT" \
  > "$HASHES"

sha256sum -c "$HASHES"

exit "$rc"
