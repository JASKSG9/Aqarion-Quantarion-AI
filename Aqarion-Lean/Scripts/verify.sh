#!/usr/bin/env bash
# AqarionLean verification gate.
# Fails if the public library contains sorry/admit.
# pending/ and killed/ are exempt (open and refuted statements live there).

set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/3] source scan: sorry/admit in public library"
if grep -rn --include='*.lean' -E '\bsorry\b|\badmit\b' AqarionLean.lean AqarionLean/ ; then
  echo "FAIL: sorry or admit found in public library source"
  exit 1
fi
echo "  ok - no sorry/admit in public source"

echo "[2/3] lake clean"
lake clean

echo "[3/3] lake build"
lake build

if grep -rn --include='*.lean' -E '\bsorry\b|\badmit\b' AqarionLean.lean AqarionLean/ ; then
  echo "FAIL: sorry or admit found after build"
  exit 1
fi

echo "PASS: public library is sorry-free"
