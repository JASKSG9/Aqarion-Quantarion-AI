#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== verify.sh ==="
./scripts/verify.sh

echo
echo "=== verify_axioms.sh ==="
./scripts/verify_axioms.sh

echo
echo "ALL GATES PASSED"
