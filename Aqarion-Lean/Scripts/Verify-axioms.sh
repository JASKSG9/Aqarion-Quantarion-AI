#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[axioms] running check_axioms.lean via lake env lean"
OUT="$(lake env lean scripts/check_axioms.lean 2>&1 || true)"
echo "$OUT"

if echo "$OUT" | grep -q "error:"; then
  echo "FAIL: lean reported an error"
  exit 1
fi

if echo "$OUT" | grep -q "depends on axioms:"; then
  echo "FAIL: unexpected axioms found"
  exit 1
fi

EXPECTED=2
ACTUAL=$(echo "$OUT" | grep -c "does not depend on any axioms" || true)
if [ "$ACTUAL" -ne "$EXPECTED" ]; then
  echo "FAIL: expected $EXPECTED axiom-free declarations, found $ACTUAL"
  exit 1
fi

echo "PASS: all public theorems are axiom-free"
